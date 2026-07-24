"""
Paquete de acceso a datos. Expone get_db()/init_app() desde db.py para que
el resto de la aplicación importe simplemente `from database import db`.
"""
from . import db  # noqa: F401
