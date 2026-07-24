"""
Motor de recomendación de AcademyMap.

Regla simple y transparente (sin IA externa), pero aislada en su propio
módulo para poder reemplazarla más adelante por un modelo de aprendizaje
automático sin modificar las rutas ni las plantillas:

    1. Cada respuesta del quiz suma puntos a una o más áreas vocacionales.
    2. Se ordenan las áreas de mayor a menor puntaje.
    3. Se buscan liceos (dentro de las 5 comunas disponibles) cuya oferta
       de especialidades coincida con las áreas mejor puntuadas.
    4. Los liceos se ordenan por cantidad de áreas coincidentes y luego
       por rating, para mostrar primero las mejores coincidencias.
"""
from collections import defaultdict

from services.quiz_data import AREAS, QUESTIONS


def calcular_puntajes(respuestas: dict) -> dict:
    """
    respuestas: { "q1": indice_opcion_elegida, "q2": indice_opcion_elegida, ... }
    Devuelve: { "tecnologia": 5, "salud": 2, ... } ordenado de mayor a menor.
    """
    puntajes = defaultdict(int)

    for pregunta in QUESTIONS:
        idx = respuestas.get(pregunta["id"])
        if idx is None:
            continue
        try:
            opcion = pregunta["opciones"][int(idx)]
        except (ValueError, IndexError):
            continue
        for area, peso in opcion["weights"].items():
            puntajes[area] += peso

    # Orden descendente por puntaje
    return dict(sorted(puntajes.items(), key=lambda kv: kv[1], reverse=True))


def areas_top(puntajes: dict, n: int = 3) -> list:
    """Devuelve los n ids de área con mayor puntaje."""
    return list(puntajes.keys())[:n]


def recomendar_liceos(liceos: list, puntajes: dict, limite: int = 6) -> list:
    """
    liceos: lista de objetos Liceo (o dicts con clave 'areas' -> lista de ids)
    puntajes: salida de calcular_puntajes()

    Devuelve la lista de liceos ordenada por afinidad vocacional.
    """
    top = areas_top(puntajes, n=len(AREAS))  # todas las áreas, con su orden de relevancia
    peso_area = {area: len(top) - i for i, area in enumerate(top)}  # más puntos = más relevante

    def afinidad(liceo):
        areas_liceo = liceo.lista_areas if hasattr(liceo, "lista_areas") else liceo.get("areas", [])
        return sum(peso_area.get(a, 0) for a in areas_liceo)

    candidatos = [l for l in liceos if afinidad(l) > 0]
    candidatos.sort(key=lambda l: (afinidad(l), l.rating if hasattr(l, "rating") else l.get("rating", 0)), reverse=True)

    if not candidatos:
        # Si ninguna especialidad calza exactamente, se muestran los mejor
        # evaluados como alternativa general.
        candidatos = sorted(liceos, key=lambda l: l.rating if hasattr(l, "rating") else l.get("rating", 0), reverse=True)

    return candidatos[:limite]
