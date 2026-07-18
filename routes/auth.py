from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["GET", "POST"])
def login():
    # Si ya está logueado, mandarlo directo al admin
    if "usuario_id" in session:
        return redirect(url_for("admin.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Buscar al usuario en la base de datos
        usuario = Usuario.query.filter_by(username=username).first()

        # Validar usuario y contraseña
        if usuario and usuario.check_password(password):
            session["usuario_id"] = usuario.id
            session["usuario_name"] = usuario.username
            return redirect(url_for("admin.index"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")

@auth.route("/logout")
def logout():
    # Limpiar la sesión por completo
    session.clear()
    return redirect(url_for("inicio"))