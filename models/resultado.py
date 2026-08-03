"""
Repositorio para resultados de quiz guardados: permite generar un link
compartible (/r/<id>) y mostrar un banner de "ya respondiste antes" sin
depender de que la sesión siga teniendo las preguntas originales.

No se guarda ningún dato personal: solo el desglose de afinidad por área
(porcentajes) y los IDs de los liceos recomendados.
"""
import json
from typing import Optional

from database.db import get_db


def crear(resumen_areas: list, liceos_ids: list) -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO resultados_quiz (resumen_areas, liceos_ids) VALUES (?, ?)",
        (json.dumps(resumen_areas), ",".join(str(i) for i in liceos_ids)),
    )
    db.commit()
    return cursor.lastrowid


def obtener(resultado_id: int) -> Optional[dict]:
    fila = get_db().execute(
        "SELECT * FROM resultados_quiz WHERE id = ?", (resultado_id,)
    ).fetchone()
    if fila is None:
        return None

    liceos_ids = [int(i) for i in fila["liceos_ids"].split(",") if i]
    return {
        "id": fila["id"],
        "resumen_areas": json.loads(fila["resumen_areas"]),
        "liceos_ids": liceos_ids,
        "creado_en": fila["creado_en"],
    }
