import os
from flask import Flask, render_template
from extensions import db
from models.liceo import Liceo
from models.usuario import Usuario
from config import Config

# Importación de las rutas (Blueprints)
from routes.liceos import liceos
from routes.quiz import quiz
from routes.admin import admin
from routes.auth import auth

def create_app():
    app = Flask(__name__)
    
    # Carga la configuración centralizada
    app.config.from_object(Config)

    # Enlazar la instancia única de SQLAlchemy con esta aplicación Flask
    db.init_app(app)

    # Registro de todos los módulos de rutas (Blueprints)
    app.register_blueprint(liceos)
    app.register_blueprint(quiz)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    @app.route("/")
    def inicio():
        return render_template("index.html")

    # Forzar el contexto de la aplicación de manera segura
    with app.app_context():
        # Crea las tablas necesarias si no existen
        db.create_all()
        
        # Cargar Usuario Administrador por defecto si la tabla está vacía
        if Usuario.query.count() == 0:
            admin_usuario = Usuario(username="admin")
            admin_usuario.set_password("admin123")
            db.session.add(admin_usuario)
            db.session.commit()
            print("¡Usuario administrador inicial creado con éxito! (admin / admin123)")

        # Cargar Liceos base solo si la tabla estuviera vacía
        if Liceo.query.count() == 0:
            datos_iniciales = [
                Liceo(
                    nombre="Liceo Polivalente San Benjamín",
                    comuna="La Cisterna",
                    direccion="Av. El Parrón 0234",
                    especialidades="Programación, Conectividad y Redes, Administración",
                    tipo="Polivalente",
                    jornada="Completa Diurna",
                    contacto="+56 2 2555 1234",
                    sitio_web="https://www.sanbenjamin.cl",
                    descripcion="Establecimiento enfocado en la innovación tecnológica.",
                    imagen=None
                ),
                Liceo(
                    nombre="Liceo Industrial Metalmecánico",
                    comuna="San Ramón",
                    direccion="Santa Rosa 7890",
                    especialidades="Mecánica Automotriz, Construcciones Metálicas, Electricidad",
                    tipo="Industrial",
                    jornada="Completa Diurna",
                    contacto="+56 2 2555 5678",
                    sitio_web="https://www.industrialramon.cl",
                    descripcion="Líder en formación técnico-manual.",
                    imagen=None
                )
            ]
            db.session.bulk_save_objects(datos_iniciales)
            db.session.commit()
            print("¡Liceos base insertados con éxito!")

    return app

# Punto de ejecución único del servidor
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)