"""
Registro centralizado de blueprints. app.py solo llama a register_routes(app).
"""


def register_routes(app):
    from .main import main_bp
    from .quiz import quiz_bp
    from .liceos import liceos_bp
    from .comparador import comparador_bp
    from .admin import admin_bp
    from .opiniones import opiniones_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(liceos_bp)
    app.register_blueprint(comparador_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(opiniones_bp)
