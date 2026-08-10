# -*- coding: utf-8 -*-
"""
Diagnóstico Vocacional Avanzado: un cuestionario más extenso y formal que
el test rápido de la página principal, con preguntas cerradas (escala +
escenarios) y abiertas, pensado para quienes ya probaron el test rápido y
quieren un perfil más completo antes de postular a un liceo.

No se guarda ningún dato personal identificable — las respuestas abiertas
viven solo en la sesión del navegador mientras dura el diagnóstico, no se
persisten en la base de datos.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from models import liceo as liceo_repo
from services.quiz_avanzado_data import AUTOEVALUACION, OPCIONES_LIKERT, ESCENARIOS, PREGUNTAS_ABIERTAS
from services.quiz_data import AREAS
from services.recommendation import calcular_puntajes_avanzado, porcentajes_por_area, recomendar_liceos
from services.diagnostico_ia import generar_sintesis

quiz_avanzado_bp = Blueprint("quiz_avanzado", __name__, url_prefix="/diagnostico-vocacional")

SAE_URL = "https://www.sistemadeadmisionescolar.cl/"


@quiz_avanzado_bp.route("/")
def intro():
    return render_template("quiz_avanzado/intro.html", title="Diagnóstico Vocacional Avanzado — AcademyMap")


@quiz_avanzado_bp.route("/formulario")
def formulario():
    return render_template(
        "quiz_avanzado/formulario.html",
        title="Diagnóstico Vocacional Avanzado — AcademyMap",
        autoevaluacion=AUTOEVALUACION,
        opciones_likert=OPCIONES_LIKERT,
        escenarios=ESCENARIOS,
        preguntas_abiertas=PREGUNTAS_ABIERTAS,
    )


@quiz_avanzado_bp.route("/diagnostico", methods=["GET", "POST"])
def diagnostico():
    if request.method == "GET":
        flash("Primero debes completar el formulario del diagnóstico.", "info")
        return redirect(url_for("quiz_avanzado.intro"))

    # --- Validar que todo esté respondido ------------------------------
    respuestas_likert = {}
    for item in AUTOEVALUACION:
        valor = request.form.get(item["id"])
        if valor is None:
            flash("Por favor responde todas las afirmaciones de autoevaluación.", "warning")
            return redirect(url_for("quiz_avanzado.formulario"))
        respuestas_likert[item["id"]] = valor

    respuestas_escenarios = {}
    for escenario in ESCENARIOS:
        letra = request.form.get(escenario["id"])
        if letra is None:
            flash("Por favor responde todos los escenarios.", "warning")
            return redirect(url_for("quiz_avanzado.formulario"))
        respuestas_escenarios[escenario["id"]] = letra

    respuestas_abiertas = {}
    for pregunta in PREGUNTAS_ABIERTAS:
        texto = request.form.get(pregunta["id"], "").strip()
        if not texto:
            flash("Por favor responde todas las preguntas abiertas, aunque sea brevemente.", "warning")
            return redirect(url_for("quiz_avanzado.formulario"))
        if len(texto) > 800:
            texto = texto[:800]
        respuestas_abiertas[pregunta["id"]] = texto

    # --- Calcular perfil -------------------------------------------------
    puntajes = calcular_puntajes_avanzado(respuestas_likert, respuestas_escenarios)
    afinidad = porcentajes_por_area(puntajes)
    resumen_areas = [{"id": a, "porcentaje": pct, **AREAS[a]} for a, pct in afinidad.items()]
    top_areas = resumen_areas[:3]

    todos_los_liceos = liceo_repo.listar_todos()
    recomendados = recomendar_liceos(todos_los_liceos, puntajes, limite=6)

    # Preguntas + respuestas abiertas emparejadas, para mostrarlas juntas.
    reflexiones = [
        {"pregunta": p["texto"], "respuesta": respuestas_abiertas[p["id"]]}
        for p in PREGUNTAS_ABIERTAS
    ]

    sintesis_ia = generar_sintesis(top_areas, respuestas_abiertas)

    return render_template(
        "quiz_avanzado/diagnostico.html",
        title="Tu diagnóstico vocacional — AcademyMap",
        top_areas=top_areas,
        resumen_areas=resumen_areas,
        recomendados=recomendados,
        reflexiones=reflexiones,
        sintesis_ia=sintesis_ia,
        sae_url=SAE_URL,
    )
