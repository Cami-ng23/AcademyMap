"""
AcademyMap — Punto de entrada de la aplicación Flask.

Ejecutar con:
    python app.py

y abrir en:
    http://localhost:5000
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from config import Config
from database import db as database
from routes import register_routes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENDOR_DIR = os.path.join(BASE_DIR, "static", "vendor")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    database.init_app(app)
    register_routes(app)
    _configurar_logging(app)

    # Filtro Jinja simple para formatear números en las plantillas (miles).
    @app.template_filter("miles")
    def formato_miles(valor):
        try:
            return f"{int(valor):,}".replace(",", ".")
        except (TypeError, ValueError):
            return valor

    # Disponibiliza el diccionario de áreas vocacionales (íconos/colores) en
    # todas las plantillas, sin tener que pasarlo manualmente en cada vista.
    @app.context_processor
    def inject_areas():
        from services.quiz_data import AREAS
        return {"AREAS": AREAS}

    # Disponibiliza si las dependencias (Bootstrap, Leaflet, etc.) ya se
    # descargaron localmente con scripts/descargar_dependencias.py. Si no,
    # las plantillas caen de vuelta al CDN automáticamente.
    @app.context_processor
    def inject_vendor_disponible():
        return {"VENDOR": _vendor_disponible()}

    @app.errorhandler(404)
    def pagina_no_encontrada(_error):
        return render_template("404.html", title="Página no encontrada — AcademyMap"), 404

    @app.errorhandler(500)
    def error_interno(error):
        app.logger.error("Error interno del servidor: %s", error, exc_info=True)
        return render_template("500.html", title="Algo salió mal — AcademyMap"), 500

    with app.app_context():
        _sembrar_datos_iniciales()

    return app


def _vendor_disponible() -> dict:
    """Revisa qué dependencias ya se descargaron localmente (static/vendor/)."""
    def existe(nombre):
        return os.path.isfile(os.path.join(VENDOR_DIR, nombre))

    return {
        "bootstrap_css": existe("bootstrap.min.css"),
        "bootstrap_js": existe("bootstrap.bundle.min.js"),
        "bootstrap_icons_css": existe("bootstrap-icons.min.css"),
        "leaflet_css": existe("leaflet.css"),
        "leaflet_js": existe("leaflet.js"),
    }


def _configurar_logging(app):
    """
    Guarda los errores en logs/academymap.log además de la consola, para
    poder revisar qué pasó después de una presentación en vivo sin haber
    estado mirando la terminal en ese momento.
    """
    carpeta_logs = os.path.join(BASE_DIR, "logs")
    os.makedirs(carpeta_logs, exist_ok=True)

    manejador = RotatingFileHandler(
        os.path.join(carpeta_logs, "academymap.log"), maxBytes=512_000, backupCount=3, encoding="utf-8"
    )
    manejador.setLevel(logging.WARNING)
    manejador.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    ))
    app.logger.addHandler(manejador)


def _sembrar_datos_iniciales():
    """Si la base de datos está vacía, la puebla con los liceos iniciales."""
    from models import liceo as liceo_repo
    from seed_data import LICEOS_SEED

    if liceo_repo.contar() > 0:
        return

    for datos in LICEOS_SEED:
        liceo_repo.crear(datos)


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
