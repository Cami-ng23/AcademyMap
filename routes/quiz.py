"""
Rutas del test vocacional: /quiz (formulario) y /resultados (procesamiento).

Para que el test se sienta distinto cada vez que alguien lo responde, en
cada visita a /quiz se eligen 10 preguntas al azar desde un banco de 20
(services/quiz_data.QUESTIONS) y se baraja el orden de las alternativas de
cada una. Esa selección exacta se guarda en la sesión del usuario, para
poder interpretar correctamente sus respuestas en /resultados (los índices
de las alternativas ya no corresponden al orden "original" del banco).
"""
import random

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from models import liceo as liceo_repo
from services.quiz_data import QUESTIONS, AREAS, PREGUNTAS_POR_INTENTO
from services.recommendation import (
    calcular_puntajes, areas_top, recomendar_liceos, porcentajes_por_area,
)

quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/quiz")
def quiz():
    """Muestra una selección aleatoria de preguntas (opciones también en orden aleatorio)."""
    cantidad = min(PREGUNTAS_POR_INTENTO, len(QUESTIONS))
    seleccionadas = random.sample(QUESTIONS, k=cantidad)

    preguntas_sesion = []
    for pregunta in seleccionadas:
        opciones = list(pregunta["opciones"])
        random.shuffle(opciones)
        preguntas_sesion.append({**pregunta, "opciones": opciones})

    # Se guarda en la sesión para poder interpretar las respuestas en /resultados.
    session["quiz_preguntas"] = preguntas_sesion

    return render_template(
        "quiz.html",
        title="Test vocacional — AcademyMap",
        preguntas=preguntas_sesion,
    )


@quiz_bp.route("/resultados", methods=["GET", "POST"])
def resultados():
    """Procesa las respuestas del quiz y muestra las recomendaciones."""
    if request.method == "GET":
        flash("Primero debes responder el test vocacional.", "info")
        return redirect(url_for("quiz.quiz"))

    preguntas = session.get("quiz_preguntas")
    if not preguntas:
        # La sesión expiró o se accedió sin pasar por /quiz primero.
        flash("Tu test vocacional expiró. Por favor, respóndelo de nuevo.", "warning")
        return redirect(url_for("quiz.quiz"))

    respuestas = {}
    for pregunta in preguntas:
        valor = request.form.get(pregunta["id"])
        if valor is None:
            flash("Por favor responde todas las preguntas para ver tus resultados.", "warning")
            return redirect(url_for("quiz.quiz"))
        respuestas[pregunta["id"]] = valor

    puntajes = calcular_puntajes(respuestas, preguntas=preguntas)
    session.pop("quiz_preguntas", None)  # ya no se necesita, se limpia la sesión

    top_areas_ids = areas_top(puntajes, n=3)
    top_areas = [{"id": a, **AREAS[a]} for a in top_areas_ids if a in AREAS]

    afinidad = porcentajes_por_area(puntajes)
    resumen_areas = [{"id": a, "porcentaje": pct, **AREAS[a]} for a, pct in afinidad.items()]

    todos_los_liceos = liceo_repo.listar_todos()
    recomendados = recomendar_liceos(todos_los_liceos, puntajes, limite=6)

    return render_template(
        "resultados.html",
        title="Tus resultados — AcademyMap",
        top_areas=top_areas,
        resumen_areas=resumen_areas,
        recomendados=recomendados,
    )