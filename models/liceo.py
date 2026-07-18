from extensions import db  # <-- Esto es lo más importante

class Liceo(db.Model):
    __tablename__ = "liceos"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    especialidades = db.Column(db.Text, nullable=False)  # Separadas por comas
    tipo = db.Column(db.String(50), default="Polivalente")
    jornada = db.Column(db.String(50), default="Completa Diurna")
    contacto = db.Column(db.String(100))
    sitio_web = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200), nullable=True)