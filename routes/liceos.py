from flask import Blueprint, render_template, request
from models.liceo import Liceo

liceos = Blueprint(
    "liceos",
    __name__,
    url_prefix="/liceos"
)

@liceos.route("/")
def lista():
    # 1. Capturar parámetros de la URL de manera segura
    buscar = request.args.get("buscar", "").strip()
    comuna_sel = request.args.get("comuna", "").strip()
    especialidad_sel = request.args.get("especialidad", "").strip()

    # 2. Iniciar la consulta base de營QLAlchemy
    query = Liceo.query

    # 3. Aplicar filtros acumulativos
    if buscar:
        query = query.filter(Liceo.nombre.ilike(f"%{buscar}%"))
    
    if comuna_sel:
        query = query.filter(Liceo.comuna == comuna_sel)
        
    if specialty_sel:
        query = query.filter(Liceo.especialidades.ilike(f"%{especialidad_sel}%"))

    # 4. Ejecutar la consulta final
    liceos_filtrados = query.all()

    # 5. Listas fijas obligatorias solicitadas para los selectores de la interfaz
    comunas_permitidas = [
        "La Cisterna", 
        "San Ramón", 
        "La Granja", 
        "San Miguel", 
        "El Bosque"
    ]
    
    especialidades_comunes = [
        "Programación",
        "Conectividad y Redes",
        "Electricidad",
        "Mecánica Automotriz",
        "Administración",
        "Enfermería",
        "Atención de Párvulos"
    ]

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
    # Buscar el liceo por ID en la base de datos o lanzar un error 404 si no existe
    liceo = Liceo.query.get_or_404(id)
    
    # Renderizar la plantilla pasando el objeto del liceo encontrado
    return render_template("detalle_liceo.html", liceo=liceo)