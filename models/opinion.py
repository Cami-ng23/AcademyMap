"""
Repositorio de opiniones anónimas. Toda opinión pasa primero por
services/moderacion.py antes de guardarse; este módulo solo persiste el
resultado.
"""
from database.db import get_db


def crear(texto: str, estado: str, motivo: str, metodo: str) -> int:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO opiniones (texto, estado, motivo_moderacion, metodo_moderacion) "
        "VALUES (?, ?, ?, ?)",
        (texto, estado, motivo, metodo),
    )
    db.commit()
    return cursor.lastrowid


def listar(estado: str = "") -> list:
    sql = "SELECT * FROM opiniones"
    params = []
    if estado:
        sql += " WHERE estado = ?"
        params.append(estado)
    sql += " ORDER BY creado_en DESC"
    filas = get_db().execute(sql, params).fetchall()
    return [dict(f) for f in filas]


def contar_no_leidas() -> int:
    fila = get_db().execute(
        "SELECT COUNT(*) AS total FROM opiniones WHERE estado = 'aprobada' AND leida = 0"
    ).fetchone()
    return fila["total"]


def marcar_leidas(ids: list) -> None:
    if not ids:
        return
    db = get_db()
    marcadores = ",".join("?" for _ in ids)
    db.execute(f"UPDATE opiniones SET leida = 1 WHERE id IN ({marcadores})", ids)
    db.commit()


def eliminar(opinion_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM opiniones WHERE id = ?", (opinion_id,))
    db.commit()
