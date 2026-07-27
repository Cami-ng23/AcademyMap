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