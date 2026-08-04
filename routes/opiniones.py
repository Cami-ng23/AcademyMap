"""
Ruta pública para dejar una opinión anónima sobre AcademyMap.

Cada opinión pasa por services/moderacion.py (IA de Claude si hay
ANTHROPIC_API_KEY configurada, o un filtro heurístico de respaldo) antes
de guardarse. No se guarda ningún dato personal ni identificador de quien
la envía.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for

from models import opinion as opinion_repo
from services.moderacion import moderar_opinion
from services import rate_limit

opiniones_bp = Blueprint("opiniones", __name__)


@opiniones_bp.route("/opiniones", methods=["GET", "POST"])
def opiniones():
    if request.method == "POST":
        clave_intento = f"opinion:{request.remote_addr}"
        if not rate_limit.permitir(clave_intento, max_intentos=5, ventana_segundos=600):
            flash("Enviaste varias opiniones seguidas. Espera un momento antes de enviar otra.", "warning")
            return redirect(url_for("opiniones.opiniones"))

        texto = request.form.get("texto", "").strip()

        if not texto:
            flash("Escribe algo antes de enviar tu opinión.", "warning")
            return redirect(url_for("opiniones.opiniones"))

        resultado = moderar_opinion(texto)
        estado = "aprobada" if resultado["aprobada"] else "rechazada"
        opinion_repo.crear(texto, estado, resultado["motivo"], resultado["metodo"])

        if resultado["aprobada"]:
            flash("¡Gracias por tu opinión! Fue enviada de forma anónima.", "success")
        else:
            # Mensaje genérico a propósito: no se detalla el motivo exacto del
            # rechazo, para no facilitar que alguien intente "esquivar" el filtro.
            flash("No pudimos publicar tu comentario. Intenta reformularlo, por favor.", "warning")

        return redirect(url_for("opiniones.opiniones"))

    return render_template("opiniones.html", title="Danos tu opinión — AcademyMap")
