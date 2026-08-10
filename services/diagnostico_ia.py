# -*- coding: utf-8 -*-
"""
Síntesis opcional con IA para el Diagnóstico Vocacional Avanzado.

El diagnóstico funciona completo SIN esto: se arma con los puntajes por
área y las respuestas abiertas mostradas tal cual (ver routes/quiz_avanzado.py).
Este módulo solo agrega un párrafo adicional de síntesis si hay una
ANTHROPIC_API_KEY configurada; si no la hay, o la llamada falla, la
función devuelve None y el diagnóstico se muestra igual, sin ese párrafo.

Usa el mismo patrón (y la misma variable de entorno) que
services/moderacion.py.
"""
import json
import urllib.error
import urllib.request

from services.moderacion import ANTHROPIC_API_KEY, ANTHROPIC_URL, ANTHROPIC_MODEL

PROMPT_SISTEMA = (
    "Eres un orientador vocacional para estudiantes de enseñanza media en "
    "Chile que están eligiendo una especialidad técnico-profesional. Vas a "
    "recibir el perfil de un estudiante: sus áreas vocacionales con mayor "
    "puntaje, y sus respuestas a preguntas abiertas de reflexión personal.\n\n"
    "Escribe un párrafo breve (máximo 120 palabras), cálido pero profesional, "
    "en segunda persona ('tú'), que conecte sus respuestas abiertas con sus "
    "áreas de mayor puntaje, sin inventar datos que no te dieron. No repitas "
    "literalmente sus respuestas, sintetiza. No dés consejos genéricos de "
    "autoayuda, sé concreto y específico a lo que la persona escribió.\n\n"
    "Responde ÚNICAMENTE con el párrafo de texto plano, sin comillas, sin "
    "JSON, sin encabezados."
)


def generar_sintesis(top_areas: list, respuestas_abiertas: dict):
    """
    top_areas: [{"nombre": "...", "descripcion": "..."}, ...] (top 3)
    respuestas_abiertas: {"abierta_1": "texto...", ...}

    Devuelve el párrafo de síntesis (str) si hay IA configurada y responde
    bien, o None si no hay clave / falla la llamada (el diagnóstico se
    arma igual sin este párrafo).
    """
    if not ANTHROPIC_API_KEY:
        return None

    areas_texto = ", ".join(a["nombre"] for a in top_areas)
    respuestas_texto = "\n".join(f"- {v}" for v in respuestas_abiertas.values() if v and v.strip())

    if not respuestas_texto:
        return None

    contenido_usuario = (
        f"Áreas de mayor puntaje: {areas_texto}\n\n"
        f"Respuestas abiertas del estudiante:\n{respuestas_texto}"
    )

    payload = json.dumps({
        "model": ANTHROPIC_MODEL,
        "max_tokens": 300,
        "system": PROMPT_SISTEMA,
        "messages": [{"role": "user", "content": contenido_usuario}],
    }).encode("utf-8")

    peticion = urllib.request.Request(
        ANTHROPIC_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(peticion, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        texto = "".join(
            bloque.get("text", "")
            for bloque in data.get("content", [])
            if bloque.get("type") == "text"
        ).strip()
        return texto or None
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError, OSError):
        return None
