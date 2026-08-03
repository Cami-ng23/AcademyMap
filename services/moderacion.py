# -*- coding: utf-8 -*-
"""
Moderación de opiniones anónimas antes de guardarlas.

Si hay una ANTHROPIC_API_KEY configurada como variable de entorno, se usa
la API de Claude para clasificar el comentario (¿es una opinión genuina y
respetuosa sobre AcademyMap, o es spam/broma/ofensivo/irrelevante?).

Si no hay clave configurada, o la llamada a la API falla (sin internet,
error de red, tiempo de espera agotado, etc.), se usa un filtro
heurístico simple como respaldo — para que la sección de opiniones nunca
quede totalmente bloqueada por falta de configuración.

No se usa ninguna librería externa (solo `urllib` de la librería
estándar), para mantener la filosofía de "sin dependencias extra" del
resto del proyecto.
"""
import json
import os
import urllib.error
import urllib.request

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

# Filtro heurístico de respaldo: lista breve de spam/groserías comunes.
_PALABRAS_PROHIBIDAS = [
    "csm", "ctm", "conchetumadre", "qliao", "culiao", "maricon", "weon culiao",
    "http://", "https://", "www.",
]

PROMPT_SISTEMA = (
    "Eres un moderador de comentarios para AcademyMap, una plataforma chilena "
    "de orientación vocacional técnico-profesional para estudiantes de "
    "enseñanza media. Vas a recibir una opinión anónima enviada por alguien "
    "que usó el sitio.\n\n"
    "Apruébala si es un comentario genuino sobre la plataforma: sugerencia, "
    "crítica constructiva (incluso dura), agradecimiento, o reporte de un "
    "error o dato incorrecto.\n\n"
    "Recházala solo si es claramente spam, publicidad, una broma sin "
    "sentido, contenido ofensivo o discriminatorio, o texto totalmente "
    "irrelevante al sitio.\n\n"
    "Responde ÚNICAMENTE con un JSON válido de la forma "
    '{"aprobada": true o false, "motivo": "razón breve en español, menos de 15 palabras"}. '
    "No agregues explicación ni texto adicional fuera del JSON."
)


def moderar_opinion(texto: str) -> dict:
    """Devuelve {"aprobada": bool, "motivo": str, "metodo": "ia"|"heuristica"}."""
    texto = (texto or "").strip()

    if not texto or len(texto) < 5:
        return {"aprobada": False, "motivo": "El comentario está vacío o es muy corto.", "metodo": "heuristica"}
    if len(texto) > 1000:
        return {"aprobada": False, "motivo": "El comentario es demasiado largo (máx. 1000 caracteres).", "metodo": "heuristica"}

    if ANTHROPIC_API_KEY:
        resultado_ia = _moderar_con_ia(texto)
        if resultado_ia is not None:
            return resultado_ia

    return _moderar_heuristica(texto)


def _moderar_con_ia(texto: str):
    """Intenta moderar con la API de Claude. Devuelve None si falla (se usa el respaldo)."""
    payload = json.dumps({
        "model": ANTHROPIC_MODEL,
        "max_tokens": 200,
        "system": PROMPT_SISTEMA,
        "messages": [{"role": "user", "content": texto}],
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
        with urllib.request.urlopen(peticion, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        texto_respuesta = "".join(
            bloque.get("text", "")
            for bloque in data.get("content", [])
            if bloque.get("type") == "text"
        ).strip()
        texto_limpio = texto_respuesta.replace("```json", "").replace("```", "").strip()
        resultado = json.loads(texto_limpio)

        return {
            "aprobada": bool(resultado.get("aprobada")),
            "motivo": str(resultado.get("motivo", ""))[:300],
            "metodo": "ia",
        }
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError, OSError):
        # Sin internet, API caída, respuesta inesperada, etc. -> se usa el respaldo heurístico.
        return None


def _moderar_heuristica(texto: str) -> dict:
    texto_lower = texto.lower()

    for palabra in _PALABRAS_PROHIBIDAS:
        if palabra in texto_lower:
            return {"aprobada": False, "motivo": "Contiene lenguaje o enlaces no permitidos.", "metodo": "heuristica"}

    palabras = texto_lower.split()
    if len(palabras) > 4 and len(set(palabras)) <= 2:
        return {"aprobada": False, "motivo": "Parece spam (texto repetitivo).", "metodo": "heuristica"}

    return {"aprobada": True, "motivo": "Aprobado por filtro básico (sin IA configurada).", "metodo": "heuristica"}
