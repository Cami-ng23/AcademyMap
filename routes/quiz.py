"""
Rutas del test vocacional: /quiz (formulario), /resultados (procesamiento)
y /r/<id> (ver un resultado guardado, para compartir o volver a mirarlo).

Para que el test se sienta distinto cada vez que alguien lo responde, en
cada visita a /quiz se eligen 10 preguntas al azar desde un banco de 20
(services/quiz_data.QUESTIONS) y se baraja el orden de las alternativas de
cada una. Esa selección exacta se guarda en la sesión del usuario, para
poder interpretar correctamente sus respuestas en /resultados (los índices
de las alternativas ya no corresponden al orden "original" del banco).

Cada resultado calculado también se guarda en la base de datos (sin datos
personales, solo el desglose de afinidad por área y los liceos
recomendados), lo que permite generar un link compartible /r/<id> y
mostrar un banner de "ya respondiste antes" en /quiz.
"""
import random

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

from models import liceo as liceo_repo
from models import resultado as resultado_repo
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

    # Si la persona ya respondió el test antes en esta sesión, se ofrece un
    # acceso directo a ese resultado en vez de obligarla a repetir todo.
    resultado_anterior_id = session.get("ultimo_resultado_id")

    return render_template(
        "quiz.html",
        title="Test vocacional — AcademyMap",
        preguntas=preguntas_sesion,
        resultado_anterior_id=resultado_anterior_id,
    )


@quiz_bp.route("/resultados", methods=["GET", "POST"])
def resultados():
    """Procesa las respuestas del quiz, guarda el resultado y muestra las recomendaciones."""
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

    afinidad = porcentajes_por_area(puntajes)
    resumen_areas = [{"id": a, "porcentaje": pct, **AREAS[a]} for a, pct in afinidad.items()]
    top_areas = resumen_areas[:3]

    todos_los_liceos = liceo_repo.listar_todos()
    recomendados = recomendar_liceos(todos_los_liceos, puntajes, limite=6)

    # Se guarda el resultado (sin datos personales) para poder compartirlo
    # con un link y para el banner de "ya respondiste antes".
    resumen_para_guardar = [{"id": a["id"], "porcentaje": a["porcentaje"]} for a in resumen_areas]
    resultado_id = resultado_repo.crear(resumen_para_guardar, [l.id for l in recomendados])
    session["ultimo_resultado_id"] = resultado_id

    return render_template(
        "resultados.html",
        title="Tus resultados — AcademyMap",
        top_areas=top_areas,
        resumen_areas=resumen_areas,
        recomendados=recomendados,
        resultado_id=resultado_id,
        compartido=False,
    )


@quiz_bp.route("/r/<int:resultado_id>")
def ver_resultado(resultado_id):
    """Muestra un resultado ya calculado (link compartible o 'ver de nuevo')."""
    datos = resultado_repo.obtener(resultado_id)
    if datos is None:
        abort(404)

    resumen_areas = [
        {"id": a["id"], "porcentaje": a["porcentaje"], **AREAS[a["id"]]}
        for a in datos["resumen_areas"] if a["id"] in AREAS
    ]
    top_areas = resumen_areas[:3]

    recomendados = [liceo_repo.obtener(i) for i in datos["liceos_ids"]]
    recomendados = [l for l in recomendados if l is not None]

    return render_template(
        "resultados.html",
        title="Resultado del test vocacional — AcademyMap",
        top_areas=top_areas,
        resumen_areas=resumen_areas,
        recomendados=recomendados,
        resultado_id=resultado_id,
        compartido=True,
    )