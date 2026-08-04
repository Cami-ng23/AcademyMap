"""
Límite de intentos simple, en memoria (sin Flask-Limiter ni Redis), para
frenar spam en /opiniones y fuerza bruta en el login del admin.

Al ser en memoria del proceso, se reinicia si se reinicia el servidor —
suficiente para un proyecto de feria con un solo proceso de Flask. Para
un despliegue real con varios workers, se recomendaría Flask-Limiter con
Redis como backend compartido.
"""
import time
from collections import defaultdict

_intentos = defaultdict(list)


def permitir(clave: str, max_intentos: int, ventana_segundos: int) -> bool:
    """
    Devuelve True si `clave` (ej: "login:1.2.3.4") todavía tiene intentos
    disponibles dentro de la ventana de tiempo; False si se pasó del límite.
    Cada llamada cuenta como un intento nuevo.
    """
    ahora = time.time()
    historial = _intentos[clave]

    # Descarta intentos fuera de la ventana de tiempo.
    historial[:] = [t for t in historial if ahora - t < ventana_segundos]

    if len(historial) >= max_intentos:
        return False

    historial.append(ahora)
    return True


def segundos_restantes(clave: str, ventana_segundos: int) -> int:
    """Cuánto falta para que se libere el intento más antiguo (para el mensaje de error)."""
    historial = _intentos.get(clave, [])
    if not historial:
        return 0
    return max(0, int(ventana_segundos - (time.time() - min(historial))))


def reiniciar():
    """Limpia todo el historial de intentos. Solo se usa en la suite de pruebas."""
    _intentos.clear()
