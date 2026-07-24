"""
Panel administrador: login simple (usuario/clave fija en config.py),
y CRUD completo de liceos.

Seguridad: para la feria se usa un login simple basado en sesión, tal
como fue solicitado. Para un entorno productivo real se recomienda
migrar a contraseñas con hash (werkzeug.security) y una tabla de
usuarios en la base de datos.
"""
from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, flash, current_app, abort,
)

from models import liceo as liceo_repo
from services.quiz_data import AREAS

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("admin_autenticado"):
            flash("Debes iniciar sesión para acceder al panel administrador.", "warning")
            return redirect(url_for("admin.login"))
        return vista(*args, **kwargs)
    return envoltura


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave = request.form.get("clave", "")
        if usuario == current_app.config["ADMIN_USERNAME"] and clave == current_app.config["ADMIN_PASSWORD"]:
            session["admin_autenticado"] = True
            flash("Sesión iniciada correctamente.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("admin/login.html", title="Acceso administrador — AcademyMap")


@admin_bp.route("/logout")
def logout():
    session.pop("admin_autenticado", None)
    flash("Sesión cerrada.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_requerido
def dashboard():
    liceos = liceo_repo.listar_todos()

    estadisticas = {
        "total": len(liceos),
        "verificados": sum(1 for l in liceos if l.verificado),
        "demostracion": sum(1 for l in liceos if not l.verificado),
        "comunas": len({l.comuna for l in liceos}),
    }

    return render_template(
        "admin/dashboard.html",
        title="Panel administrador — AcademyMap",
        liceos=liceos,
        estadisticas=estadisticas,
    )


@admin_bp.route("/agregar", methods=["GET", "POST"])
@login_requerido
def agregar():
    if request.method == "POST":
        datos = _datos_desde_formulario()
        nuevo_id = liceo_repo.crear(datos)
        flash("Liceo agregado correctamente.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/agregar.html",
        title="Agregar liceo — AcademyMap",
        areas=AREAS,
        comunas=current_app.config["COMUNAS_DISPONIBLES"],
    )


@admin_bp.route("/editar/<int:liceo_id>", methods=["GET", "POST"])
@login_requerido
def editar(liceo_id):
    liceo = liceo_repo.obtener(liceo_id)
    if liceo is None:
        abort(404)

    if request.method == "POST":
        datos = _datos_desde_formulario()
        liceo_repo.actualizar(liceo_id, datos)
        flash("Liceo actualizado correctamente.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/editar.html",
        title=f"Editar {liceo.nombre} — AcademyMap",
        liceo=liceo,
        areas=AREAS,
        comunas=current_app.config["COMUNAS_DISPONIBLES"],
    )


@admin_bp.route("/eliminar/<int:liceo_id>", methods=["POST"])
@login_requerido
def eliminar(liceo_id):
    liceo = liceo_repo.obtener(liceo_id)
    if liceo is None:
        abort(404)
    liceo_repo.eliminar(liceo_id)
    flash(f"'{liceo.nombre}' fue eliminado.", "info")
    return redirect(url_for("admin.dashboard"))


def _datos_desde_formulario() -> dict:
    """Mapea los campos del formulario (agregar/editar) a un dict para el repositorio."""
    return {
        "nombre": request.form.get("nombre", "").strip(),
        "comuna": request.form.get("comuna", "").strip(),
        "direccion": request.form.get("direccion", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "especialidades": request.form.get("especialidades", "").strip(),
        "areas": ",".join(request.form.getlist("areas")),
        "caracteristicas": request.form.get("caracteristicas", "").strip(),
        "tipo": request.form.get("tipo", "Municipal"),
        "jornada": request.form.get("jornada", "Diurna"),
        "imagen": "",
        "contacto": request.form.get("contacto", "").strip(),
        "gratuito": 1 if request.form.get("gratuito") == "on" else 0,
        "matricula": int(request.form.get("matricula") or 0),
        "rating": float(request.form.get("rating") or 4.0),
        "admision_pct": int(request.form.get("admision_pct") or 60),
        "empleabilidad_pct": int(request.form.get("empleabilidad_pct") or 75),
        "verificado": 1 if request.form.get("verificado") == "on" else 0,
    }
