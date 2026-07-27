"""
Capa de acceso a datos con sqlite3 puro (librería estándar de Python).

Se optó por sqlite3 nativo en lugar de un ORM externo para que el proyecto
funcione con `pip install -r requirements.txt` mínimo y sin dependencias
de red adicionales, manteniendo igualmente una arquitectura limpia:
- Esta es la ÚNICA capa que ejecuta SQL.
- models/liceo.py expone objetos y funciones de repositorio.
- routes/ solo llama funciones del repositorio, nunca SQL directo.

Migración a PostgreSQL: bastaría con reemplazar `sqlite3.connect(...)` por
`psycopg2.connect(...)` (o SQLAlchemy) en `get_db()` y ajustar los
placeholders `?` por `%s` en las consultas de models/liceo.py.
"""
import os
import sqlite3
from pathlib import Path

from flask import g

# Permite sobreescribir la ruta de la base de datos (usado por la suite de
# tests para no tocar la base de datos real durante las pruebas).
DB_PATH = Path(os.environ.get("ACADEMYMAP_DB_PATH", str(Path(__file__).parent / "academymap.db")))

SCHEMA = """
CREATE TABLE IF NOT EXISTS liceos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    comuna TEXT NOT NULL,
    direccion TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    especialidades TEXT NOT NULL DEFAULT '',
    areas TEXT NOT NULL DEFAULT '',
    caracteristicas TEXT NOT NULL DEFAULT '',
    tipo TEXT NOT NULL DEFAULT 'Municipal',
    jornada TEXT NOT NULL DEFAULT 'Diurna',
    imagen TEXT NOT NULL DEFAULT '',
    contacto TEXT NOT NULL DEFAULT '',
    gratuito INTEGER NOT NULL DEFAULT 1,
    matricula INTEGER NOT NULL DEFAULT 0,
    rating REAL NOT NULL DEFAULT 4.0,
    admision_pct INTEGER NOT NULL DEFAULT 60,
    empleabilidad_pct INTEGER NOT NULL DEFAULT 75,
    verificado INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS resultados_quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resumen_areas TEXT NOT NULL,
    liceos_ids TEXT NOT NULL DEFAULT '',
    creado_en TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def get_db():
    """Devuelve la conexión SQLite de la petición actual (una por request)."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Registra el cierre automático de la conexión al final de cada request."""
    app.teardown_appcontext(close_db)

    with app.app_context():
        _crear_tablas()


def _crear_tablas():
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()