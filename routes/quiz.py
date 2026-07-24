"""
Rutas del test vocacional: /quiz (formulario) y /resultados (procesamiento).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import liceo as liceo_repo
from services.quiz_data import QUESTIONS, AREAS
from services.recommendation import calcular_puntajes, areas_top, recomendar_liceos

quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/quiz")
def quiz():
    """Muestra el cuestionario vocacional completo."""
    return render_template(
        "quiz.html",
        title="Test vocacional — AcademyMap",
        preguntas=QUESTIONS,
    )


@quiz_bp.route("/resultados", methods=["GET", "POST"])
def resultados():
    """Procesa las respuestas del quiz y muestra las recomendaciones."""
    if request.method == "GET":
        # Nadie debería llegar aquí sin haber respondido el test.
        flash("Primero debes responder el test vocacional.", "info")
        return redirect(url_for("quiz.quiz"))

    respuestas = {}
    for pregunta in QUESTIONS:
        valor = request.form.get(pregunta["id"])
        if valor is None:
            flash("Por favor responde todas las preguntas para ver tus resultados.", "warning")
            return redirect(url_for("quiz.quiz"))
        respuestas[pregunta["id"]] = valor

    puntajes = calcular_puntajes(respuestas)
    top_areas_ids = areas_top(puntajes, n=3)
    top_areas = [{"id": a, **AREAS[a]} for a in top_areas_ids if a in AREAS]

    todos_los_liceos = liceo_repo.listar_todos()
    recomendados = recomendar_liceos(todos_los_liceos, puntajes, limite=6)

    return render_template(
        "resultados.html",
        title="Tus resultados — AcademyMap",
        top_areas=top_areas,
        recomendados=recomendados,
    )
