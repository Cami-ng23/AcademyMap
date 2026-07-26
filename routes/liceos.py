"""
Rutas del explorador de liceos: listado con filtros (/liceos) y
perfil individual (/liceo/<id>).
"""
from flask import Blueprint, render_template, request, abort, current_app

from models import liceo as liceo_repo
from services.quiz_data import AREAS

liceos_bp = Blueprint("liceos", __name__)


@liceos_bp.route("/liceos")
def liceos():
    """Explorador con búsqueda, filtros y ordenamiento."""
    comuna = request.args.get("comuna", "").strip()
    area = request.args.get("area", "").strip()
    tipo = request.args.get("tipo", "").strip()
    busqueda = request.args.get("q", "").strip()
    orden = request.args.get("orden", "rating_desc").strip()

    resultados = liceo_repo.listar(comuna=comuna, area=area, tipo=tipo, busqueda=busqueda, orden=orden)
    tipos_disponibles = liceo_repo.tipos_disponibles()

    return render_template(
        "liceos.html",
        title="Explorar liceos técnico-profesionales — AcademyMap",
        liceos=resultados,
        comunas=current_app.config["COMUNAS_DISPONIBLES"],
        areas=AREAS,
        tipos=tipos_disponibles,
        filtro_comuna=comuna,
        filtro_area=area,
        filtro_tipo=tipo,
        filtro_busqueda=busqueda,
        filtro_orden=orden,
    )


@liceos_bp.route("/liceo/<int:liceo_id>")
def detalle_liceo(liceo_id):
    """Perfil completo de un liceo: historia, especialidades, contacto."""
    liceo = liceo_repo.obtener(liceo_id)
    if liceo is None:
        abort(404)

    return render_template(
        "detalle_liceo.html",
        title=f"{liceo.nombre} — AcademyMap",
        liceo=liceo,
        areas=AREAS,
    )