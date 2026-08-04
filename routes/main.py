"""
Rutas principales: landing page, "Sobre el proyecto", FAQ, robots.txt y
sitemap.xml.
"""
from flask import Blueprint, render_template, current_app, Response, url_for

from models import liceo as liceo_repo
from models import opinion as opinion_repo

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
        testimonios=opinion_repo.aleatorias_aprobadas(limite=3),
    )


@main_bp.route("/sobre-el-proyecto")
def sobre_proyecto():
    """Metodología del proyecto: cobertura, verificación de datos, stack técnico."""
    liceos = liceo_repo.listar_todos()
    estadisticas = {
        "liceos": len(liceos),
        "verificados": sum(1 for l in liceos if l.verificado),
        "comunas": len(current_app.config["COMUNAS_DISPONIBLES"]),
    }
    return render_template(
        "sobre_proyecto.html",
        title="Sobre el proyecto — AcademyMap",
        estadisticas=estadisticas,
        comunas=current_app.config["COMUNAS_DISPONIBLES"],
    )


@main_bp.route("/preguntas-frecuentes")
def faq():
    return render_template(
        "faq.html",
        title="Preguntas frecuentes — AcademyMap",
    )


@main_bp.route("/robots.txt")
def robots_txt():
    contenido = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {url_for('main.sitemap_xml', _external=True)}\n"
    )
    return Response(contenido, mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap_xml():
    """Sitemap dinámico: páginas estáticas + un <url> por cada liceo."""
    paginas_estaticas = [
        url_for("main.index", _external=True),
        url_for("quiz.quiz", _external=True),
        url_for("liceos.liceos", _external=True),
        url_for("liceos.mapa", _external=True),
        url_for("comparador.comparar", _external=True),
        url_for("main.sobre_proyecto", _external=True),
        url_for("main.faq", _external=True),
        url_for("opiniones.opiniones", _external=True),
    ]
    urls_liceos = [
        url_for("liceos.detalle_liceo", liceo_id=l.id, _external=True)
        for l in liceo_repo.listar_todos()
    ]

    items = "".join(f"<url><loc>{u}</loc></url>" for u in paginas_estaticas + urls_liceos)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>'
    return Response(xml, mimetype="application/xml")
