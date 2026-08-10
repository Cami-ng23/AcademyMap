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
        from services import rate_limit
        rate_limit.reiniciar()

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

    def test_mapa_sin_liceo_especifico_no_produce_none_invalido_en_js(self):
        """
        Regresión: sin ?liceo=ID, `liceo_centrado_json` debe renderizar como
        `null` (válido en JS), no como `None` (Python) — ese bug dejaba el
        mapa completamente en blanco por un error de JavaScript.
        """
        html = self.client.get("/mapa").get_data(as_text=True)
        self.assertIn("const liceoCentrado = null;", html)
        self.assertNotIn("= None;", html)

    def test_mapa_con_liceo_especifico_en_query(self):
        html = self.client.get("/mapa?liceo=1").get_data(as_text=True)
        self.assertIn("const liceoCentrado = 1;", html)

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

    # ------------------------------------------------------------------ #
    # Límite de intentos (rate limiting)
    # ------------------------------------------------------------------ #
    def test_rate_limit_opiniones(self):
        for i in range(5):
            resp = self.client.post("/opiniones", data={"texto": f"Comentario válido número {i} para probar el límite."})
            self.assertEqual(resp.status_code, 302)

        # El 6to envío en poco tiempo debería quedar bloqueado por el límite.
        resp_bloqueado = self.client.post(
            "/opiniones",
            data={"texto": "Este séptimo comentario no debería guardarse."},
            follow_redirects=True,
        )
        self.assertIn("Espera un momento", resp_bloqueado.get_data(as_text=True))

        with self.app.app_context():
            from models import opinion as opinion_repo
            self.assertFalse(any(
                "séptimo comentario" in o["texto"] for o in opinion_repo.listar()
            ))

    def test_rate_limit_login_admin(self):
        for _ in range(5):
            self.client.post("/admin/login", data={"usuario": "admin", "clave": "mala"})

        resp = self.client.post(
            "/admin/login",
            data={"usuario": "admin", "clave": "academymap2026"},  # incluso la correcta
            follow_redirects=True,
        )
        self.assertIn("Demasiados intentos", resp.get_data(as_text=True))

    # ------------------------------------------------------------------ #
    # Testimonios en la landing
    # ------------------------------------------------------------------ #
    def test_testimonios_aparecen_en_landing(self):
        self.client.post("/opiniones", data={"texto": "Comentario de prueba para salir como testimonio."})
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        # No siempre sale este comentario específico (son 3 al azar), pero la
        # sección debe existir si hay al menos una opinión aprobada.
        self.assertIn("Esto opinan otros estudiantes", resp.get_data(as_text=True))

    # ------------------------------------------------------------------ #
    # Página de error 500 y fallback de dependencias locales (vendor)
    # ------------------------------------------------------------------ #
    # ------------------------------------------------------------------ #
    # Diagnóstico Vocacional Avanzado
    # ------------------------------------------------------------------ #
    def test_intro_diagnostico_avanzado_carga(self):
        resp = self.client.get("/diagnostico-vocacional/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Diagnóstico Vocacional Avanzado", resp.get_data(as_text=True))

    def test_formulario_avanzado_tiene_todas_las_secciones(self):
        resp = self.client.get("/diagnostico-vocacional/formulario")
        html = resp.get_data(as_text=True)
        self.assertEqual(len(set(re.findall(r'name="(auto_\w+)"', html))), 8)
        self.assertEqual(len(set(re.findall(r'name="(esc_\d)"', html))), 5)
        self.assertEqual(len(set(re.findall(r'name="(abierta_\d)"', html))), 4)

    def test_diagnostico_avanzado_completo(self):
        datos = {
            "auto_electricidad": "5", "auto_industrial": "4", "auto_salud": "2",
            "auto_gastronomia": "2", "auto_administracion": "3", "auto_construccion": "2",
            "auto_tecnologia": "5", "auto_parvulos": "1",
            "esc_1": "a", "esc_2": "b", "esc_3": "a", "esc_4": "c", "esc_5": "d",
            "abierta_1": "Una vez arreglé el enchufe de mi casa.",
            "abierta_2": "Programar en el computador.",
            "abierta_3": "Trabajando con tecnología.",
            "abierta_4": "Un poco nervioso pero con ganas.",
        }
        with self.client as c:
            c.get("/diagnostico-vocacional/formulario")
            resp = c.post("/diagnostico-vocacional/diagnostico", data=datos)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Tecnología e Informática", html)
            self.assertIn("Sistema de Admisión Escolar", html)
            self.assertIn("sistemadeadmisionescolar.cl", html)
            self.assertIn("Una vez arreglé el enchufe", html)

    def test_diagnostico_avanzado_incompleto_redirige(self):
        resp = self.client.post("/diagnostico-vocacional/diagnostico", data={"auto_electricidad": "5"})
        self.assertEqual(resp.status_code, 302)

    def test_cta_diagnostico_avanzado_en_resultados_quiz_corto(self):
        with self.client as c:
            html = c.get("/quiz").get_data(as_text=True)
            ids = sorted(set(re.findall(r'name="(q\d+)"', html)))
            data = {qid: "0" for qid in ids}
            resp = c.post("/resultados", data=data, follow_redirects=True)
            self.assertIn("diagnostico-vocacional", resp.get_data(as_text=True))

    # ------------------------------------------------------------------ #
    # Acceso admin discreto
    # ------------------------------------------------------------------ #
    def test_boton_login_discreto_sin_mencionar_panel(self):
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("am-login-discreto", html)
        self.assertNotIn(">Panel<", html)
        self.assertNotIn("Panel administrador", html)

    # ------------------------------------------------------------------ #
    # Imagen del liceo
    # ------------------------------------------------------------------ #
    def test_admin_puede_guardar_imagen_del_liceo(self):
        with self.client as c:
            c.post("/admin/login", data={"usuario": "admin", "clave": "academymap2026"})
            c.post(
                "/admin/agregar",
                data={
                    "nombre": "Liceo Con Imagen Test",
                    "comuna": "La Cisterna",
                    "direccion": "Calle Falsa 789",
                    "descripcion": "Prueba de imagen",
                    "especialidades": "Test",
                    "areas": ["tecnologia"],
                    "tipo": "Municipal",
                    "jornada": "Diurna",
                    "contacto": "test@test.cl",
                    "matricula": "100",
                    "rating": "4.5",
                    "admision_pct": "50",
                    "empleabilidad_pct": "80",
                    "imagen": "https://ejemplo.cl/foto.jpg",
                },
                follow_redirects=True,
            )
            with self.app.app_context():
                from models import liceo as liceo_repo
                creado = next(l for l in liceo_repo.listar_todos() if l.nombre == "Liceo Con Imagen Test")
                self.assertEqual(creado.imagen, "https://ejemplo.cl/foto.jpg")
                nuevo_id = creado.id

            resp_detalle = c.get(f"/liceo/{nuevo_id}")
            self.assertIn("ejemplo.cl/foto.jpg", resp_detalle.get_data(as_text=True))

            with self.app.app_context():
                liceo_repo.eliminar(nuevo_id)
            c.get("/admin/logout")

    def test_pagina_500_personalizada_registrada(self):
        self.assertIn(500, self.app.error_handler_spec[None])

    def test_vendor_usa_cdn_cuando_no_hay_archivos_locales(self):
        resp = self.client.get("/")
        html = resp.get_data(as_text=True)
        self.assertIn("cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap", html)

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