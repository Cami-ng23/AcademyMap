"""
Suite de pruebas automatizadas de AcademyMap, usando `unittest` (librería
estándar de Python, sin dependencias extra como pytest).

Ejecutar desde la carpeta raíz del proyecto con:

    python -m unittest discover -s tests -v

Cada método de prueba usa una base de datos SQLite temporal (separada de
database/academymap.db), por lo que correr los tests NUNCA modifica ni
borra los datos reales del proyecto.
"""
import os
import re
import tempfile
import unittest

# IMPORTANTE: la variable de entorno se define ANTES de importar `app`,
# para que database/db.py use una base de datos temporal aislada en vez de
# la base de datos real del proyecto.
_TMP_DB = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["ACADEMYMAP_DB_PATH"] = _TMP_DB.name

from app import create_app  # noqa: E402
from config import Config  # noqa: E402


class TestConfig(Config):
    TESTING = True


class AcademyMapTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.app.testing = True

    def setUp(self):
        self.client = self.app.test_client()

    # ------------------------------------------------------------------ #
    # Páginas públicas
    # ------------------------------------------------------------------ #
    def test_landing_page_carga(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("AcademyMap", resp.get_data(as_text=True))

    def test_sobre_proyecto_y_faq(self):
        self.assertEqual(self.client.get("/sobre-el-proyecto").status_code, 200)
        self.assertEqual(self.client.get("/preguntas-frecuentes").status_code, 200)

    def test_mapa_publico_carga_con_puntos(self):
        resp = self.client.get("/mapa")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("mapa-liceos", html)
        # Los 16 liceos sembrados ya tienen coordenadas de fábrica.
        self.assertIn('"nombre"', html)

    def test_admin_formulario_incluye_mapa(self):
        with self.client as c:
            c.post("/admin/login", data={"usuario": "admin", "clave": "academymap2026"})
            resp = c.get("/admin/agregar")
            html = resp.get_data(as_text=True)
            self.assertIn("mapa-admin", html)
            self.assertIn("btn-geocodificar", html)
            c.get("/admin/logout")

    def test_admin_crear_liceo_con_coordenadas(self):
        with self.client as c:
            c.post("/admin/login", data={"usuario": "admin", "clave": "academymap2026"})
            c.post(
                "/admin/agregar",
                data={
                    "nombre": "Liceo Con Ubicación Test",
                    "comuna": "La Cisterna",
                    "direccion": "Calle Falsa 123",
                    "descripcion": "Prueba de geocodificación",
                    "especialidades": "Test",
                    "areas": ["tecnologia"],
                    "tipo": "Municipal",
                    "jornada": "Diurna",
                    "contacto": "test@test.cl",
                    "matricula": "100",
                    "rating": "4.5",
                    "admision_pct": "50",
                    "empleabilidad_pct": "80",
                    "latitud": "-33.5300",
                    "longitud": "-70.6650",
                },
                follow_redirects=True,
            )

            with self.app.app_context():
                from models import liceo as liceo_repo
                creado = next(
                    l for l in liceo_repo.listar_todos()
                    if l.nombre == "Liceo Con Ubicación Test"
                )
                self.assertTrue(creado.tiene_ubicacion)
                self.assertAlmostEqual(creado.latitud, -33.5300, places=3)
                self.assertAlmostEqual(creado.longitud, -70.6650, places=3)
                liceo_repo.eliminar(creado.id)

            c.get("/admin/logout")

    def test_admin_crear_liceo_sin_coordenadas_queda_sin_ubicacion(self):
        with self.client as c:
            c.post("/admin/login", data={"usuario": "admin", "clave": "academymap2026"})
            c.post(
                "/admin/agregar",
                data={
                    "nombre": "Liceo Sin Ubicación Test",
                    "comuna": "La Cisterna",
                    "direccion": "Calle Falsa 456",
                    "descripcion": "Prueba sin coordenadas",
                    "especialidades": "Test",
                    "areas": ["tecnologia"],
                    "tipo": "Municipal",
                    "jornada": "Diurna",
                    "contacto": "test@test.cl",
                    "matricula": "100",
                    "rating": "4.5",
                    "admision_pct": "50",
                    "empleabilidad_pct": "80",
                    # sin latitud/longitud, como si no se hubiera usado el buscador
                },
                follow_redirects=True,
            )

            with self.app.app_context():
                from models import liceo as liceo_repo
                creado = next(
                    l for l in liceo_repo.listar_todos()
                    if l.nombre == "Liceo Sin Ubicación Test"
                )
                self.assertFalse(creado.tiene_ubicacion)
                # No debe aparecer entre los liceos con ubicación para el mapa.
                ids_con_ubicacion = [l.id for l in liceo_repo.listar_con_ubicacion()]
                self.assertNotIn(creado.id, ids_con_ubicacion)
                liceo_repo.eliminar(creado.id)

            c.get("/admin/logout")

    # ------------------------------------------------------------------ #
    # Opiniones anónimas
    # ------------------------------------------------------------------ #
    def test_pagina_opiniones_carga(self):
        resp = self.client.get("/opiniones")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Danos tu opinión", resp.get_data(as_text=True))

    def test_enviar_opinion_valida_queda_aprobada(self):
        # Sin ANTHROPIC_API_KEY en el entorno de tests, se usa el filtro
        # heurístico, que aprueba comentarios normales sin groserías/spam.
        resp = self.client.post(
            "/opiniones",
            data={"texto": "Me encantó el test vocacional, muy fácil de usar."},
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Gracias por tu opinión", resp.get_data(as_text=True))

        with self.app.app_context():
            from models import opinion as opinion_repo
            aprobadas = opinion_repo.listar(estado="aprobada")
            self.assertTrue(any("test vocacional" in o["texto"] for o in aprobadas))

    def test_enviar_opinion_vacia_no_se_guarda(self):
        resp = self.client.post("/opiniones", data={"texto": "   "}, follow_redirects=True)
        self.assertIn("Escribe algo", resp.get_data(as_text=True))

    def test_enviar_opinion_con_spam_queda_rechazada(self):
        resp = self.client.post(
            "/opiniones",
            data={"texto": "visita www.spam-ejemplo.cl para ganar dinero ya"},
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)

        with self.app.app_context():
            from models import opinion as opinion_repo
            rechazadas = opinion_repo.listar(estado="rechazada")
            self.assertTrue(any("spam-ejemplo" in o["texto"] for o in rechazadas))

    def test_admin_ve_opiniones_aprobadas_y_rechazadas(self):
        self.client.post("/opiniones", data={"texto": "Sugerencia: agregar más liceos de Puente Alto."})
        self.client.post("/opiniones", data={"texto": "http://spam.cl compra ahora barato"})

        with self.client as c:
            c.post("/admin/login", data={"usuario": "admin", "clave": "academymap2026"})

            resp_aprobadas = c.get("/admin/opiniones?estado=aprobada")
            self.assertEqual(resp_aprobadas.status_code, 200)
            self.assertIn("Puente Alto", resp_aprobadas.get_data(as_text=True))

            resp_rechazadas = c.get("/admin/opiniones?estado=rechazada")
            self.assertEqual(resp_rechazadas.status_code, 200)
            self.assertIn("spam.cl", resp_rechazadas.get_data(as_text=True))

            c.get("/admin/logout")

    def test_admin_puede_eliminar_opinion(self):
        self.client.post("/opiniones", data={"texto": "Opinión de prueba para eliminar después."})

        with self.app.app_context():
            from models import opinion as opinion_repo
            creada = next(
                o for o in opinion_repo.listar(estado="aprobada")
                if "eliminar después" in o["texto"]
            )

        with self.client as c:
            c.post("/admin/login", data={"usuario": "admin", "clave": "academymap2026"})
            resp = c.post(
                f"/admin/opiniones/{creada['id']}/eliminar",
                data={"estado": "aprobada"},
                follow_redirects=True,
            )
            self.assertEqual(resp.status_code, 200)
            c.get("/admin/logout")

        with self.app.app_context():
            ids_restantes = [o["id"] for o in opinion_repo.listar()]
            self.assertNotIn(creada["id"], ids_restantes)

    def test_admin_opiniones_requiere_login(self):
        resp = self.client.get("/admin/opiniones", follow_redirects=True)
        self.assertIn("Acceso administrador", resp.get_data(as_text=True))

    def test_moderacion_heuristica_directamente(self):
        from services.moderacion import moderar_opinion

        ok = moderar_opinion("El sitio está muy bien hecho, felicitaciones al equipo.")
        self.assertTrue(ok["aprobada"])
        self.assertEqual(ok["metodo"], "heuristica")

        corto = moderar_opinion("ok")
        self.assertFalse(corto["aprobada"])

        vacio = moderar_opinion("")
        self.assertFalse(vacio["aprobada"])

    def test_robots_y_sitemap(self):
        robots = self.client.get("/robots.txt")
        self.assertEqual(robots.status_code, 200)
        self.assertIn(b"Sitemap:", robots.data)

        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap.status_code, 200)
        self.assertIn(b"<urlset", sitemap.data)
        self.assertIn(b"<loc>", sitemap.data)

    # ------------------------------------------------------------------ #
    # Explorador de liceos
    # ------------------------------------------------------------------ #
    def test_explorador_filtro_comuna(self):
        resp = self.client.get("/liceos?comuna=San+Miguel")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("San Miguel", resp.get_data(as_text=True))

    def test_explorador_busqueda_por_nombre(self):
        resp = self.client.get("/liceos?q=Gastronom%C3%ADa")
        self.assertEqual(resp.status_code, 200)

    def test_explorador_ordenamiento(self):
        for orden in ["rating_desc", "nombre_asc", "matricula_desc"]:
            resp = self.client.get(f"/liceos?orden={orden}")
            self.assertEqual(resp.status_code, 200, f"orden={orden} falló")

    def test_detalle_liceo_y_404(self):
        self.assertEqual(self.client.get("/liceo/1").status_code, 200)
        self.assertEqual(self.client.get("/liceo/999999").status_code, 404)

    def test_comparador(self):
        resp = self.client.get("/comparar?a=1&b=2")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("am-compare-table", resp.get_data(as_text=True))

    # ------------------------------------------------------------------ #
    # Quiz vocacional
    # ------------------------------------------------------------------ #
    def test_quiz_muestra_diez_preguntas(self):
        resp = self.client.get("/quiz")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("Pregunta 1 de 10", html)
        ids = set(re.findall(r'name="(q\d+)"', html))
        self.assertEqual(len(ids), 10)

    def test_quiz_preguntas_son_aleatorias(self):
        """Dos visitas seguidas no deberían mostrar siempre el mismo set de 10."""
        vistos = set()
        for _ in range(5):
            html = self.client.get("/quiz").get_data(as_text=True)
            ids = tuple(sorted(re.findall(r'name="(q\d+)"', html)))
            vistos.add(ids)
        # Con 20 preguntas eligiendo 10 al azar, 5 intentos casi seguro
        # producen más de una combinación distinta.
        self.assertGreater(len(vistos), 1)

    def test_quiz_envio_completo_muestra_resultados(self):
        with self.client as c:
            html = c.get("/quiz").get_data(as_text=True)
            ids = sorted(set(re.findall(r'name="(q\d+)"', html)))
            data = {qid: "0" for qid in ids}
            resp = c.post("/resultados", data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Liceos recomendados para ti", resp.get_data(as_text=True))

    def test_quiz_respuestas_incompletas_redirige(self):
        with self.client as c:
            c.get("/quiz")
            resp = c.post("/resultados", data={"q1": "0"})
            self.assertEqual(resp.status_code, 302)

    def test_quiz_sin_sesion_previa_redirige(self):
        # Cliente nuevo, sin haber visitado /quiz antes.
        resp = self.client.post("/resultados", data={"q1": "0"})
        self.assertEqual(resp.status_code, 302)

    def test_resultado_compartible(self):
        with self.client as c:
            html = c.get("/quiz").get_data(as_text=True)
            ids = sorted(set(re.findall(r'name="(q\d+)"', html)))
            data = {qid: "0" for qid in ids}
            c.post("/resultados", data=data, follow_redirects=True)

            with c.session_transaction() as sess:
                resultado_id = sess.get("ultimo_resultado_id")
            self.assertIsNotNone(resultado_id)

        # Se puede ver el resultado guardado desde OTRO cliente (simulando
        # que alguien más abre el link compartido), sin sesión previa.
        cliente_externo = self.app.test_client()
        resp = cliente_externo.get(f"/r/{resultado_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("resultado del test vocacional guardado", resp.get_data(as_text=True).lower())

    def test_banner_resultado_anterior_en_quiz(self):
        with self.client as c:
            html = c.get("/quiz").get_data(as_text=True)
            ids = sorted(set(re.findall(r'name="(q\d+)"', html)))
            data = {qid: "0" for qid in ids}
            c.post("/resultados", data=data, follow_redirects=True)

            # Al volver a /quiz en la misma sesión, debería aparecer el banner.
            html2 = c.get("/quiz").get_data(as_text=True)
            self.assertIn("Ya respondiste el test antes", html2)

    # ------------------------------------------------------------------ #
    # Panel administrador
    # ------------------------------------------------------------------ #
    def test_admin_requiere_login(self):
        resp = self.client.get("/admin/", follow_redirects=True)
        self.assertIn("Acceso administrador", resp.get_data(as_text=True))

    def test_admin_login_y_logout(self):
        with self.client as c:
            resp = c.post(
                "/admin/login",
                data={"usuario": "admin", "clave": "academymap2026"},
                follow_redirects=True,
            )
            self.assertIn("Gestión de liceos", resp.get_data(as_text=True))
            c.get("/admin/logout")

    def test_admin_login_credenciales_invalidas(self):
        resp = self.client.post(
            "/admin/login",
            data={"usuario": "admin", "clave": "incorrecta"},
            follow_redirects=True,
        )
        self.assertIn("incorrectos", resp.get_data(as_text=True))

    def test_admin_crud_completo(self):
        with self.client as c:
            c.post("/admin/login", data={"usuario": "admin", "clave": "academymap2026"})

            # Crear
            resp = c.post(
                "/admin/agregar",
                data={
                    "nombre": "Liceo de Prueba Unitaria",
                    "comuna": "La Cisterna",
                    "direccion": "Calle Falsa 123",
                    "descripcion": "Descripción de prueba",
                    "especialidades": "Test",
                    "areas": ["tecnologia"],
                    "tipo": "Municipal",
                    "jornada": "Diurna",
                    "contacto": "test@test.cl",
                    "matricula": "100",
                    "rating": "4.5",
                    "admision_pct": "50",
                    "empleabilidad_pct": "80",
                },
                follow_redirects=True,
            )
            self.assertEqual(resp.status_code, 200)

            with self.app.app_context():
                from models import liceo as liceo_repo
                creado = next(
                    l for l in liceo_repo.listar_todos()
                    if l.nombre == "Liceo de Prueba Unitaria"
                )
                nuevo_id = creado.id

            # Editar
            resp_edit = c.post(
                f"/admin/editar/{nuevo_id}",
                data={
                    "nombre": "Liceo Editado por Test",
                    "comuna": "La Cisterna",
                    "direccion": "Calle Falsa 123",
                    "descripcion": "Editado",
                    "especialidades": "Test",
                    "areas": ["tecnologia"],
                    "tipo": "Municipal",
                    "jornada": "Diurna",
                    "contacto": "test@test.cl",
                    "matricula": "100",
                    "rating": "4.5",
                    "admision_pct": "50",
                    "empleabilidad_pct": "80",
                },
                follow_redirects=True,
            )
            self.assertEqual(resp_edit.status_code, 200)

            with self.app.app_context():
                editado = liceo_repo.obtener(nuevo_id)
                self.assertEqual(editado.nombre, "Liceo Editado por Test")

            # Eliminar
            resp_del = c.post(f"/admin/eliminar/{nuevo_id}", follow_redirects=True)
            self.assertEqual(resp_del.status_code, 200)

            with self.app.app_context():
                self.assertIsNone(liceo_repo.obtener(nuevo_id))

            c.get("/admin/logout")

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(_TMP_DB.name)
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
