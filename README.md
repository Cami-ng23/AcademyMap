# AcademyMap

Plataforma de orientación vocacional técnico-profesional para estudiantes de
**La Cisterna, San Ramón, La Granja, San Miguel y El Bosque**, desarrollada en
**Flask** (migrada desde el prototipo original en Next.js/React/Tailwind).

## Ejecutar el proyecto

```bash
pip install -r requirements.txt
python app.py
```

Abrir en el navegador: **http://localhost:5000**

La primera vez que se ejecuta, se crea automáticamente la base de datos
SQLite (`database/academymap.db`) y se puebla con los liceos iniciales
(`seed_data.py`). Para partir de cero, simplemente elimina ese archivo `.db`
y vuelve a ejecutar `python app.py`.

### Panel administrador

- URL: `http://localhost:5000/admin/login`
- Usuario: `admin`
- Contraseña: `academymap2026`

(Configurables mediante variables de entorno `ADMIN_USERNAME` / `ADMIN_PASSWORD`
o editando `config.py`.)

## Ejecutar las pruebas automatizadas

El proyecto incluye una suite de pruebas con `unittest` (librería estándar
de Python, no requiere instalar nada extra):

```bash
python -m unittest discover -s tests -v
```

Cada prueba usa una base de datos SQLite temporal, por lo que correr los
tests nunca modifica `database/academymap.db`. Cubre: landing page, quiz
(incluida la aleatoriedad de las preguntas y el flujo completo de envío),
explorador con filtros/búsqueda/orden, comparador, perfil de liceo y 404,
login y CRUD completo del panel administrador, resultados compartibles, y
robots.txt / sitemap.xml.

## Arquitectura

```
AcademyMap/
│  app.py                 → Punto de entrada, application factory
│  config.py               → Configuración (BD, credenciales admin, comunas)
│  requirements.txt
│  seed_data.py             → Datos iniciales de liceos (verificados)
│
├─ database/
│    db.py                 → Conexión sqlite3, esquema de tablas
│
├─ models/
│    liceo.py               → Dataclass Liceo + repositorio (única capa SQL)
│    resultado.py            → Repositorio de resultados de quiz guardados/compartibles
│
├─ routes/                  → Blueprints Flask (lógica separada de la vista)
│    main.py                 → Landing, "Sobre el proyecto", FAQ, robots.txt, sitemap.xml
│    quiz.py                 → Test vocacional, resultados y links compartibles "/r/<id>"
│    liceos.py                → Explorador (búsqueda/filtros/orden) y perfil "/liceo/<id>"
│    comparador.py             → "/comparar"
│    admin.py                  → Panel administrador y CRUD "/admin/*"
│
├─ services/
│    quiz_data.py             → Banco de 20 preguntas + áreas vocacionales
│    recommendation.py         → Motor de recomendación (sin IA externa)
│
├─ templates/                → Jinja2 (extienden base.html)
│    components/               → navbar, footer, tarjeta de liceo reutilizable
│    admin/                    → login, dashboard, formulario agregar/editar
│    sobre_proyecto.html, faq.html
│
├─ static/
│    css/style.css            → Sistema de diseño (tarjetas, navbar "glass", quiz, impresión)
│    js/script.js              → Stepper del quiz, navbar scroll, comparador
│    img/favicon.svg
│
└─ tests/
     test_app.py               → Suite de pruebas con unittest (ver sección de arriba)
```

## Sobre los datos

El catálogo reúne **16 liceos técnico-profesionales**, la totalidad
identificable mediante fuentes públicas en las 5 comunas de cobertura (no
todas las comunas tienen la misma cantidad de liceos TP reales):

| Comuna       | Liceos |
|--------------|--------|
| La Cisterna  | 5      |
| San Ramón    | 4      |
| San Miguel   | 3      |
| La Granja    | 2      |
| El Bosque    | 2      |

Todos están marcados **"Verificado"**: nombre, comuna, dirección y
especialidades provienen de fuentes públicas (sitios institucionales de
cada liceo, el directorio PACE-UMCE, findmyschool.cl, boletinoficial.cl y
grandescolegios.cl), consultadas en julio de 2026. Cifras como
calificación, tasa de admisión y empleabilidad estimada son estimaciones
referenciales; la matrícula usa el dato oficial cuando la fuente lo
entregó (indicado en la descripción de cada liceo).

Chile no cuenta con un buscador único del Ministerio de Educación
filtrado por comuna + modalidad técnico-profesional, por lo que este
catálogo se construyó cruzando múltiples fuentes públicas. Si detectas un
liceo técnico-profesional de estas comunas que falte, puedes agregarlo
fácilmente desde el panel administrador (`/admin/agregar`).

El campo `verificado` del modelo `Liceo` y la insignia correspondiente en
la interfaz se mantienen para que, si en el futuro se agrega un liceo sin
confirmar, quede claramente diferenciado de los datos reales.

## Base de datos

Se usa `sqlite3` de la librería estándar de Python (sin dependencias
externas de ORM) para que el proyecto corra con una instalación mínima.
Toda la lógica SQL vive en `models/liceo.py`; las rutas solo llaman a ese
repositorio. Para migrar a PostgreSQL, basta con:

1. Reemplazar `sqlite3.connect(...)` por `psycopg2.connect(...)` en
   `database/db.py`.
2. Cambiar los placeholders `?` por `%s` en las consultas de
   `models/liceo.py`.

El esquema de la tabla `liceos` es el mismo en ambos casos.

## Escalabilidad futura

- El motor de recomendación (`services/recommendation.py`) está aislado del
  resto de la app, listo para reemplazar la suma de ponderaciones actual por
  un modelo de aprendizaje automático sin tocar rutas ni plantillas.
- La cobertura geográfica (`config.py → COMUNAS_DISPONIBLES`) es una lista
  simple: agregar una comuna nueva no requiere cambios de arquitectura.