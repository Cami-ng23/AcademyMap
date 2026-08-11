agregar simce 

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

## Opiniones anónimas con moderación por IA

Cualquier visitante puede dejar una opinión anónima en `/opiniones` (no se
guarda IP, nombre ni ningún dato identificable). Cada comentario pasa por
un filtro antes de guardarse:

- **Con IA (recomendado):** define la variable de entorno
  `ANTHROPIC_API_KEY` con una clave de la API de Claude antes de correr
  `python app.py`. Cada opinión se envía a Claude (`claude-haiku-4-5`) para
  clasificarla como comentario genuino o como spam/broma/ofensivo antes de
  guardarla.
- **Sin IA (respaldo automático):** si no hay clave configurada, o la
  llamada a la API falla (sin internet, etc.), se usa un filtro básico
  (largo mínimo/máximo, lista de palabras prohibidas, detección de texto
  repetitivo tipo spam). La sección de opiniones nunca queda bloqueada.

```bash
# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."
python app.py

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."
python app.py
```

Las opiniones aprobadas se leen desde `/admin/opiniones` (requiere login).
También se pueden auditar las rechazadas (`?estado=rechazada`) para
revisar qué filtró el moderador. El panel avisa con un aviso amarillo si
la IA no está configurada.

## Acceso administrador (discreto)

El acceso al panel ya no aparece como un link visible tipo "Panel" en el
menú — para no anunciarle a cualquier visitante que existe una sección de
administración. Se accede desde un ícono pequeño (👤) en la esquina
superior derecha del sitio, o directamente en `/admin/login`.

## Diagnóstico Vocacional Avanzado

Además del test rápido de la portada (10 de 50 preguntas al azar), existe
un segundo cuestionario más extenso y formal en `/diagnostico-vocacional`,
pensado para quienes quieren un perfil más completo antes de postular:

- **Autoevaluación** (8 afirmaciones, escala 1-5, una por área).
- **Escenarios de decisión** (5 situaciones con alternativas que implican
  comparar varias opciones a la vez, no solo declarar una preferencia).
- **Preguntas abiertas** (4 preguntas de reflexión personal en texto libre).

Al final se genera un diagnóstico con el desglose completo por área, las
respuestas abiertas mostradas como parte del perfil, liceos recomendados,
y un botón para ir a postular al **Sistema de Admisión Escolar (SAE)**
oficial del Mineduc (`sistemadeadmisionescolar.cl`).

Este cuestionario usa un tema visual distinto (navy + dorado, tipografía
serif para los títulos) para diferenciarse claramente del test rápido —
se abre en una pestaña nueva desde el botón al final de los resultados
del test rápido.

Si hay `ANTHROPIC_API_KEY` configurada (ver sección de Opiniones más
abajo), el diagnóstico agrega además un párrafo de síntesis generado con
IA que conecta las respuestas abiertas con las áreas de mayor puntaje. Sin
la clave, el diagnóstico se genera igual de completo, solo sin ese párrafo
extra.

## Imágenes de los liceos

Cada liceo puede tener una imagen (URL) cargada desde el panel
administrador, con vista previa en vivo mientras se escribe el link. Si un
liceo no tiene imagen cargada, se usa automáticamente una ilustración con
degradado + ícono según su área vocacional principal — así ningún liceo
se ve "vacío" mientras no se cargan fotos reales.

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
│    opinion.py               → Repositorio de opiniones anónimas moderadas
│
├─ routes/                  → Blueprints Flask (lógica separada de la vista)
│    main.py                 → Landing, "Sobre el proyecto", FAQ, robots.txt, sitemap.xml
│    quiz.py                 → Test vocacional, resultados y links compartibles "/r/<id>"
│    liceos.py                → Explorador (búsqueda/filtros/orden), perfil "/liceo/<id>" y "/mapa"
│    comparador.py             → "/comparar"
│    admin.py                  → Panel administrador, CRUD "/admin/*" y "/admin/opiniones"
│    opiniones.py               → "/opiniones" (formulario público anónimo)
│
├─ services/
│    quiz_data.py             → Banco de 20 preguntas + áreas vocacionales
│    recommendation.py         → Motor de recomendación (sin IA externa)
│    moderacion.py              → Moderación de opiniones (Claude API + respaldo heurístico)
│
├─ templates/                → Jinja2 (extienden base.html)
│    components/               → navbar, footer, tarjeta de liceo reutilizable
│    admin/                    → login, dashboard, formulario agregar/editar, opiniones
│    sobre_proyecto.html, faq.html, mapa.html, opiniones.html
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

## Funcionar sin internet (recomendado para el día de la feria)

Bootstrap, sus íconos y el mapa (Leaflet) se cargan desde internet (CDN)
por defecto. Para que el sitio funcione aunque el wifi del lugar falle,
corre esto UNA vez, con internet:

```bash
python scripts/descargar_dependencias.py
```

Esto descarga esas librerías a `static/vendor/`. Desde ese momento, la app
detecta automáticamente los archivos locales y los usa en vez del CDN —
sin tener que cambiar nada más. Si nunca corres el script, el sitio sigue
funcionando igual, cargando todo desde internet como antes.

> Las tipografías de Google Fonts siguen necesitando internet la primera
> vez que carga cada dispositivo (no se pueden auto-hospedar fácilmente).
> Si no hay conexión, el sitio usa una tipografía del sistema como
> respaldo — se ve un poco distinto, pero nada se rompe.

## Otras mejoras de calidad

- **Página de error personalizada:** si algo falla inesperadamente, se
  muestra una página con el estilo del sitio (no el error feo de Flask
  por defecto), y el error queda registrado en `logs/academymap.log` para
  poder revisarlo después de una presentación en vivo.
- **Límite de intentos (rate limiting):** máximo 5 opiniones cada 10
  minutos por IP, y máximo 5 intentos de login del admin cada 5 minutos,
  para frenar spam y fuerza bruta sin depender de librerías externas.
- **Testimonios en la portada:** la landing muestra 3 opiniones aprobadas
  al azar como prueba social (solo aparecen si ya hay opiniones
  aprobadas).
- **Números animados en el hero:** las estadísticas de la portada cuentan
  desde 0 hasta su valor real al cargar la página.

## Mapa interactivo

`/mapa` muestra todos los liceos con coordenadas cargadas en un mapa
interactivo (Leaflet + tiles de OpenStreetMap, sin necesidad de API key).
Cada liceo se agrega al mapa con un pin de color según su área vocacional
principal; al hacer clic se abre un popup con especialidades y un link al
perfil completo.

**Desde el panel administrador**, al agregar o editar un liceo hay una
sección "Ubicación en el mapa": se escribe la dirección (reutiliza el
campo "Dirección" de arriba), se presiona "Buscar en el mapa" y el
formulario geocodifica automáticamente esa dirección usando
[Nominatim](https://nominatim.org/) (el buscador gratuito de
OpenStreetMap) y deja caer un pin arrastrable para ajustar la ubicación
exacta a mano si hace falta. Un liceo sin coordenadas simplemente no
aparece en `/mapa` (pero sigue funcionando normal en el resto del sitio).

Los 16 liceos del catálogo inicial (`seed_data.py`) traen coordenadas
*aproximadas* (ubicadas en el sector correcto de su comuna, no
geocodificadas desde su dirección exacta) para que el mapa no arranque
vacío. Se recomienda abrir cada uno desde el panel administrador y usar
"Buscar en el mapa" para afinar su ubicación real.

> Tanto el mapa como la búsqueda de direcciones necesitan que el
> **navegador** (no el servidor) tenga acceso a internet, ya que las
> imágenes del mapa y la búsqueda de direcciones se piden directamente
> desde el navegador de quien está usando la página.

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
