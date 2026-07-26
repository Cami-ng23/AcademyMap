"""
Modelo Liceo (dataclass) + repositorio de acceso a datos sobre sqlite3.

Los campos multivaluados (especialidades, áreas, características) se
guardan como texto separado por comas y se exponen como listas mediante
propiedades Python, para mantener el esquema simple en SQLite.
"""
from dataclasses import dataclass
from typing import Optional, List

from database.db import get_db


@dataclass
class Liceo:
    nombre: str
    comuna: str
    direccion: str
    descripcion: str
    especialidades: str = ""
    areas: str = ""
    caracteristicas: str = ""
    tipo: str = "Municipal"
    jornada: str = "Diurna"
    imagen: str = ""
    contacto: str = ""
    gratuito: bool = True
    matricula: int = 0
    rating: float = 4.0
    admision_pct: int = 60
    empleabilidad_pct: int = 75
    verificado: bool = False
    id: Optional[int] = None

    # ---- Propiedades de conveniencia -------------------------------------
    @property
    def lista_especialidades(self) -> List[str]:
        return [e.strip() for e in self.especialidades.split(",") if e.strip()]

    @property
    def lista_areas(self) -> List[str]:
        return [a.strip() for a in self.areas.split(",") if a.strip()]

    @property
    def lista_caracteristicas(self) -> List[str]:
        return [c.strip() for c in self.caracteristicas.split(",") if c.strip()]

    @classmethod
    def from_row(cls, row) -> "Liceo":
        return cls(
            id=row["id"],
            nombre=row["nombre"],
            comuna=row["comuna"],
            direccion=row["direccion"],
            descripcion=row["descripcion"],
            especialidades=row["especialidades"],
            areas=row["areas"],
            caracteristicas=row["caracteristicas"],
            tipo=row["tipo"],
            jornada=row["jornada"],
            imagen=row["imagen"],
            contacto=row["contacto"],
            gratuito=bool(row["gratuito"]),
            matricula=row["matricula"],
            rating=row["rating"],
            admision_pct=row["admision_pct"],
            empleabilidad_pct=row["empleabilidad_pct"],
            verificado=bool(row["verificado"]),
        )


# ============================================================================
# Repositorio: única capa que ejecuta SQL. Las rutas solo llaman estas
# funciones (nunca sqlite3 directo), tal como pide la arquitectura del
# proyecto ("separar lógica y presentación").
# ============================================================================

_COLUMNAS = [
    "nombre", "comuna", "direccion", "descripcion", "especialidades", "areas",
    "caracteristicas", "tipo", "jornada", "imagen", "contacto", "gratuito",
    "matricula", "rating", "admision_pct", "empleabilidad_pct", "verificado",
]


def contar() -> int:
    fila = get_db().execute("SELECT COUNT(*) AS total FROM liceos").fetchone()
    return fila["total"]


_ORDENES_VALIDOS = {
    "rating_desc": "rating DESC",
    "nombre_asc": "nombre COLLATE NOCASE ASC",
    "matricula_desc": "matricula DESC",
}


def listar(comuna: str = "", area: str = "", tipo: str = "", busqueda: str = "", orden: str = "rating_desc") -> List[Liceo]:
    sql = "SELECT * FROM liceos WHERE 1=1"
    params = []

    if comuna:
        sql += " AND comuna = ?"
        params.append(comuna)
    if tipo:
        sql += " AND tipo = ?"
        params.append(tipo)
    if area:
        sql += " AND areas LIKE ?"
        params.append(f"%{area}%")
    if busqueda:
        sql += " AND (nombre LIKE ? OR especialidades LIKE ?)"
        params.append(f"%{busqueda}%")
        params.append(f"%{busqueda}%")

    sql += f" ORDER BY {_ORDENES_VALIDOS.get(orden, _ORDENES_VALIDOS['rating_desc'])}"
    filas = get_db().execute(sql, params).fetchall()
    return [Liceo.from_row(f) for f in filas]


def listar_todos() -> List[Liceo]:
    filas = get_db().execute("SELECT * FROM liceos ORDER BY comuna, nombre").fetchall()
    return [Liceo.from_row(f) for f in filas]


def obtener(liceo_id: int) -> Optional[Liceo]:
    fila = get_db().execute("SELECT * FROM liceos WHERE id = ?", (liceo_id,)).fetchone()
    return Liceo.from_row(fila) if fila else None


def tipos_disponibles() -> List[str]:
    filas = get_db().execute("SELECT DISTINCT tipo FROM liceos ORDER BY tipo").fetchall()
    return [f["tipo"] for f in filas]


def especialidades_unicas() -> set:
    filas = get_db().execute("SELECT especialidades FROM liceos").fetchall()
    resultado = set()
    for f in filas:
        resultado.update(e.strip() for e in f["especialidades"].split(",") if e.strip())
    return resultado


def crear(datos: dict) -> int:
    db = get_db()
    valores = [datos.get(col) for col in _COLUMNAS]
    marcadores = ", ".join("?" for _ in _COLUMNAS)
    cursor = db.execute(
        f"INSERT INTO liceos ({', '.join(_COLUMNAS)}) VALUES ({marcadores})",
        valores,
    )
    db.commit()
    return cursor.lastrowid


def actualizar(liceo_id: int, datos: dict) -> None:
    db = get_db()
    asignaciones = ", ".join(f"{col} = ?" for col in _COLUMNAS)
    valores = [datos.get(col) for col in _COLUMNAS] + [liceo_id]
    db.execute(f"UPDATE liceos SET {asignaciones} WHERE id = ?", valores)
    db.commit()


def eliminar(liceo_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM liceos WHERE id = ?", (liceo_id,))
    db.commit()