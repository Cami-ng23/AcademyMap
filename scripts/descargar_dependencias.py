# -*- coding: utf-8 -*-
"""
Descarga Bootstrap, Bootstrap Icons y Leaflet a static/vendor/, para que
AcademyMap funcione SIN internet una vez descargados (útil para la feria,
por si el wifi del lugar falla o es lento).

Se corre UNA sola vez, con internet:

    python scripts/descargar_dependencias.py

Después de correrlo, la app detecta automáticamente los archivos locales
y los usa en vez del CDN (ver la función `vendor_disponible()` en app.py).
Si nunca lo corres, el sitio sigue funcionando igual, cargando estas
librerías desde internet como hasta ahora.

No requiere librerías externas: usa solo `urllib` (librería estándar).
"""
import os
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR_DIR = os.path.join(BASE_DIR, "static", "vendor")

ARCHIVOS = [
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", "bootstrap.min.css"),
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js", "bootstrap.bundle.min.js"),
    ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css", "bootstrap-icons.min.css"),
    ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2", "fonts/bootstrap-icons.woff2"),
    ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff", "fonts/bootstrap-icons.woff"),
    ("https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css", "leaflet.css"),
    ("https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js", "leaflet.js"),
]


def main():
    os.makedirs(os.path.join(VENDOR_DIR, "fonts"), exist_ok=True)
    ok, fallidos = 0, []

    print("Descargando dependencias a static/vendor/ ...\n")

    for url, destino_relativo in ARCHIVOS:
        destino = os.path.join(VENDOR_DIR, destino_relativo)
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                contenido = resp.read()
            with open(destino, "wb") as f:
                f.write(contenido)
            print(f"  OK   {destino_relativo} ({len(contenido) // 1024} KB)")
            ok += 1
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            print(f"  FALLÓ {destino_relativo}: {error}")
            fallidos.append(destino_relativo)

    print(f"\n{ok}/{len(ARCHIVOS)} archivos descargados correctamente.")
    if fallidos:
        print("No se pudieron descargar (revisa tu conexión y vuelve a intentar):")
        for f in fallidos:
            print(f"  - {f}")
    else:
        print("¡Listo! AcademyMap ahora puede funcionar sin conexión a internet.")
        print("(Las fuentes de Google Fonts siguen necesitando internet la primera vez que carga cada dispositivo.)")


if __name__ == "__main__":
    main()
