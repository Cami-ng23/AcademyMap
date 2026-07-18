from flask import Blueprint, render_template, request
from models.liceo import Liceo

liceos = Blueprint(
    "liceos",
    __name__,
    url_prefix="/liceos"
)

@liceos.route("/")
def lista():
    buscar = request.args.get("buscar", "").strip()
    comuna_sel = request.args.get("comuna", "").strip()
    especialidad_sel = request.args.get("especialidad", "").strip()

    query = Liceo.query

    if buscar:
        query = query.filter(Liceo.nombre.ilike(f"%{buscar}%"))
    
    if comuna_sel:
        query = query.filter(Liceo.comuna == comuna_sel)
        
    if especialidad_sel:
        query = query.filter(Liceo.especialidades.ilike(f"%{especialidad_sel}%"))

    liceos_filtrados = query.all()

    comunas_permitidas = ["La Cisterna", "San Ramón", "La Granja", "San Miguel", "El Bosque"]
    especialidades_comunes = ["Programación", "Conectividad y Redes", "Electricidad", "Mecánica Automotriz", "Administración", "Enfermería", "Atención de Párvulos"]

    return render_template(
        "liceos.html",
        liceos=liceos_filtrados,
        comunas=comunas_permitidas,
        especialidades=especialidades_comunes,
        comuna_sel=comuna_sel,
        especialidad_sel=especialidad_sel,
        buscar=buscar
    )

@liceos.route("/<int:id>")
def detalle(id):
    liceo = Liceo.query.get_or_404(id)
    return render_template("detalle_liceo.html", liceo=liceo)