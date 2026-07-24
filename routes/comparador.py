"""
Ruta del comparador: /comparar?a=<id>&b=<id>
"""
from flask import Blueprint, render_template, request

from models import liceo as liceo_repo

comparador_bp = Blueprint("comparador", __name__)


@comparador_bp.route("/comparar")
def comparar():
    todos = liceo_repo.listar_todos()

    id_a = request.args.get("a", type=int)
    id_b = request.args.get("b", type=int)

    liceo_a = liceo_repo.obtener(id_a) if id_a else None
    liceo_b = liceo_repo.obtener(id_b) if id_b else None

    return render_template(
        "comparar.html",
        title="Comparar liceos — AcademyMap",
        todos=todos,
        liceo_a=liceo_a,
        liceo_b=liceo_b,
    )
