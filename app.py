"""
AcademyMap — Punto de entrada de la aplicación Flask.

Ejecutar con:
    python app.py

y abrir en:
    http://localhost:5000
"""
from flask import Flask, render_template

from config import Config
from database import db as database
from routes import register_routes


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    database.init_app(app)
    register_routes(app)

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

    @app.errorhandler(404)
    def pagina_no_encontrada(_error):
        return render_template("404.html", title="Página no encontrada — AcademyMap"), 404

    with app.app_context():
        _sembrar_datos_iniciales()

    return app


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
