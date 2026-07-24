"""
Configuración central de AcademyMap.

Se usa una clase de configuración simple, lista para escalar hacia
PostgreSQL en producción (basta con cambiar SQLALCHEMY_DATABASE_URI).
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Clave usada para firmar la sesión (login admin, mensajes flash, quiz).
    SECRET_KEY = os.environ.get("SECRET_KEY", "academy-map-dev-secret-2026")

    # SQLite para desarrollo / feria. Preparado para migrar a PostgreSQL:
    # SQLALCHEMY_DATABASE_URI = "postgresql://usuario:clave@host:5432/academymap"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'database', 'academymap.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Credenciales simples del panel administrador (feria técnico-profesional).
    # Para producción real se recomienda migrar a hash + tabla de usuarios.
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "academymap2026")

    # Comunas cubiertas por la primera versión de la plataforma.
    COMUNAS_DISPONIBLES = [
        "La Cisterna",
        "San Ramón",
        "La Granja",
        "San Miguel",
        "El Bosque",
    ]
