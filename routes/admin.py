from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.liceo import Liceo
from extensions import db
from sqlalchemy import func

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin.before_request
def verificar_autenticacion():
    """Esta función corre automáticamente ANTES de cualquier ruta de admin.
    Si no existe una sesión activa de usuario, bloquea el paso."""
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para acceder al panel administrativo.", "warning")
        return redirect(url_for("auth.login"))


# ==========================================================
# RUTAS DEL PANEL ADMINISTRATIVO + DASHBOARD
# ==========================================================

@admin.route("/")
def index():
    # 1. Obtener todos los liceos para listarlos en la tabla
    todos_los_liceos = Liceo.query.all()
    
    # 2. Métrica: Total General de Liceos
    total_liceos = len(todos_los_liceos)
    
    # 3. Métrica avanzada: Contar cuántos liceos hay por cada Comuna
    # Esto equivale a un: SELECT comuna, COUNT(id) FROM liceos GROUP BY comuna
    conteo_comunas = db.session.query(
        Liceo.comuna, 
        func.count(Liceo.id)
    ).group_by(Liceo.comuna).all()
    
    # 4. Métrica avanzada: Contar cuántos liceos hay por Tipo
    conteo_tipos = db.session.query(
        Liceo.tipo, 
        func.count(Liceo.id)
    ).group_by(Liceo.tipo).all()

    return render_template(
        "admin/index.html", 
        liceos=todos_los_liceos,
        total_liceos=total_liceos,
        conteo_comunas=conteo_comunas,
        conteo_tipos=conteo_tipos
    )

@admin.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        comuna = request.form.get("comuna", "").strip()
        direccion = request.form.get("direccion", "").strip()
        especialidades = request.form.get("especialidades", "").strip()
        tipo = request.form.get("tipo", "Polivalente")
        jornada = request.form.get("jornada", "Completa Diurna")
        contacto = request.form.get("contacto", "").strip()
        sitio_web = request.form.get("sitio_web", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        imagen = request.form.get("imagen", "").strip() or None

        nuevo_liceo = Liceo(
            nombre=nombre,
            comuna=comuna,
            direccion=direccion,
            especialidades=especialidades,
            tipo=tipo,
            jornada=jornada,
            contacto=contacto,
            sitio_web=sitio_web,
            descripcion=descripcion,
            imagen=imagen
        )

        db.session.add(nuevo_liceo)
        db.session.commit()
        flash("Liceo registrado exitosamente.", "success")
        return redirect(url_for("admin.index"))

    return render_template("admin/formulario.html", liceo=None)

@admin.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    liceo = Liceo.query.get_or_404(id)

    if request.method == "POST":
        liceo.nombre = request.form.get("nombre", "").strip()
        liceo.comuna = request.form.get("comuna", "").strip()
        liceo.direccion = request.form.get("direccion", "").strip()
        liceo.especialidades = request.form.get("especialidades", "").strip()
        liceo.tipo = request.form.get("tipo")
        liceo.jornada = request.form.get("jornada")
        liceo.contacto = request.form.get("contacto", "").strip()
        liceo.sitio_web = request.form.get("sitio_web", "").strip()
        liceo.descripcion = request.form.get("descripcion", "").strip()
        liceo.imagen = request.form.get("imagen", "").strip() or None

        db.session.commit()
        flash("Liceo actualizado exitosamente.", "success")
        return redirect(url_for("admin.index"))

    return render_template("admin/formulario.html", liceo=liceo)

@admin.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    liceo = Liceo.query.get_or_404(id)
    db.session.delete(liceo)
    db.session.commit()
    flash("Liceo eliminado correctamente de los registros.", "danger")
    return redirect(url_for("admin.index"))