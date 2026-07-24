"""
Rutas principales: landing page (SEO friendly, "/").
"""
from flask import Blueprint, render_template, current_app

from models import liceo as liceo_repo

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing page con hero, beneficios, cómo funciona, comunas y estadísticas."""
    estadisticas = {
        "liceos": liceo_repo.contar(),
        "comunas": len(current_app.config["COMUNAS_DISPONIBLES"]),
        "especialidades": len(liceo_repo.especialidades_unicas()),
    }

    return render_template(
        "index.html",
        title="AcademyMap — Encuentra el liceo técnico-profesional ideal para ti",
        estadisticas=estadisticas,
        comunas=current_app.config["COMUNAS_DISPONIBLES"],
    )
