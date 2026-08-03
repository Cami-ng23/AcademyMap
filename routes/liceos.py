"""
Rutas del explorador de liceos: listado con filtros (/liceos), perfil
individual (/liceo/<id>) y mapa interactivo (/mapa).
"""
import json

from flask import Blueprint, render_template, request, abort, current_app, url_for

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


@liceos_bp.route("/mapa")
def mapa():
    """Mapa interactivo con todos los liceos que tienen coordenadas cargadas."""
    liceos_geo = liceo_repo.listar_con_ubicacion()
    total_liceos = liceo_repo.contar()

    puntos = []
    for l in liceos_geo:
        area_principal = l.lista_areas[0] if l.lista_areas else None
        area_info = AREAS.get(area_principal, {})
        puntos.append({
            "id": l.id,
            "nombre": l.nombre,
            "comuna": l.comuna,
            "lat": l.latitud,
            "lng": l.longitud,
            "especialidades": l.lista_especialidades[:3],
            "color": area_info.get("color", "#4f46e5"),
            "icono": area_info.get("icono", "bi-mortarboard"),
            "url": url_for("liceos.detalle_liceo", liceo_id=l.id),
        })

    liceo_centrado_id = request.args.get("liceo", type=int)

    return render_template(
        "mapa.html",
        title="Mapa de liceos técnico-profesionales — AcademyMap",
        puntos_json=json.dumps(puntos),
        total_con_ubicacion=len(liceos_geo),
        total_liceos=total_liceos,
        liceo_centrado_id=liceo_centrado_id,
    )
