from flask import Blueprint, render_template, request, redirect, url_for
from models.liceo import Liceo

quiz = Blueprint(
    "quiz",
    __name__,
    url_prefix="/quiz"
)

@quiz.route("/", methods=["GET", "POST"])
def cuestionario():
    if request.method == "POST":
        respuestas = [
            request.form.get("p1"),
            request.form.get("p2"),
            request.form.get("p3"),
            request.form.get("p4"),
            request.form.get("p5"),
            request.form.get("p6")
        ]
        
        respuestas = [r for r in respuestas if r]

        votos = {}
        for r in respuestas:
            votos[r] = votos.get(r, 0) + 1
            
        area_predominante = max(votos, key=votos.get) if votos else "Tecnologia"
        return redirect(url_for("quiz.resultados", area=area_predominante))

    preguntas = [
        {
            "id": "p1",
            "texto": "¿Cuál de estas actividades te entusiasma más para desarrollar como proyecto?",
            "opciones": [
                {"valor": "Tecnologia", "texto": "Crear una aplicación móvil, diseñar una base de datos o configurar una red local."},
                {"valor": "Mecanica", "texto": "Desarmar un motor, diagnosticar fallas mecánicas o ajustar piezas de precisión."},
                {"valor": "Salud", "texto": "Aprender sobre control de signos vitales, anatomía y asistencia médica básica."},
                {"valor": "Administracion", "texto": "Gestionar la contabilidad de un negocio, organizar inventarios y flujos de caja."}
            ]
        },
        {
            "id": "p2",
            "texto": "Cuando un aparato electrónico o sistema falla en tu casa, ¿qué haces?",
            "opciones": [
                {"valor": "Electronica", "texto": "Busco un multímetro, reviso los circuitos, cables y busco soldar el componente dañado."},
                {"valor": "Tecnologia", "texto": "Reviso la configuración del software, el sistema operativo o el enrutador de internet."},
                {"valor": "Mecanica", "texto": "Estudio las piezas móviles, engranajes y estructuras físicas para ver qué se trancó."},
                {"valor": "Diseño", "texto": "Me fijo en cómo está construido visualmente o prefiero llamar a un servicio técnico."}
            ]
        },
        {
            "id": "p3",
            "texto": "Si tuvieras que elegir el entorno de trabajo ideal para tu futuro, ¿cuál sería?",
            "opciones": [
                {"valor": "Salud", "texto": "Un hospital, clínica o centro de atención comunitaria ayudando directamente a pacientes."},
                {"valor": "Administracion", "texto": "Una oficina corporativa coordinando equipos, contratos, finanzas y operaciones."},
                {"valor": "Diseño", "texto": "Un estudio creativo, agencia de publicidad o taller de imprenta y maquetación digital."},
                {"valor": "Electronica", "texto": "Una planta automatizada, laboratorio de hardware o terreno supervisando instalaciones."}
            ]
        },
        {
            "id": "p4",
            "texto": "¿Qué tipo de habilidades te gustaría perfeccionar en la educación media?",
            "opciones": [
                {"valor": "Tecnologia", "texto": "Escribir código en lenguajes de programación y administrar servidores en la nube."},
                {"valor": "Mecanica", "texto": "Operar maquinaria industrial, sistemas hidráulicos y herramientas automotrices."},
                {"valor": "Salud", "texto": "Técnicas de enfermería, primeros auxilios y cuidado integral de párvulos o adultos."},
                {"valor": "Diseño", "texto": "Fotografía digital, ilustración vectorial, edición de video y diseño de interfaces."}
            ]
        },
        {
            "id": "p5",
            "texto": "En un trabajo en equipo para una feria escolar, ¿qué rol asumes naturalmente?",
            "opciones": [
                {"valor": "Administracion", "texto": "El que distribuye el presupuesto, organiza los tiempos de entrega y lidera la exposición."},
                {"valor": "Diseño", "texto": "El que diseña la presentación, los folletos, el logo del stand y cuida la estética."},
                {"valor": "Tecnologia", "texto": "El que configura la pantalla, los computadores, el software o la interacción digital."},
                {"valor": "Electronica", "texto": "El que arma los sistemas de luces, cableados o mecanismos eléctricos del stand."}
            ]
        },
        {
            "id": "p6",
            "texto": "¿Qué tipo de lectura, videos o contenidos te llaman más la atención en internet?",
            "opciones": [
                {"valor": "Salud", "texto": "Casos médicos, avances en salud, psicología o el desarrollo y cuidado infantil."},
                {"valor": "Mecanica", "texto": "Restauración de vehículos, cómo funcionan las fábricas o maquinaria pesada."},
                {"valor": "Administracion", "texto": "Historias de startups, estrategias de marketing, emprendimiento y economía."},
                {"valor": "Diseño", "texto": "Portafolios artísticos, tendencias tipográficas, modelado 3D o animación."}
            ]
        }
    ]

    return render_template("quiz.html", preguntas=preguntas)

@quiz.route("/resultados")
def resultados():
    area_predominante = request.args.get("area", "Tecnologia")

    # Mapeo de perfiles con sus palabras clave para buscar en la BD
    perfiles = {
        "Tecnologia": {
            "titulo": "Área de Tecnología y Conectividad",
            "desc": "Te apasiona el desarrollo lógico, la infraestructura digital y las redes de datos. Tienes un perfil analítico ideal para especialidades de alta demanda.",
            "icono": "bi-code-slash",
            "color": "primary",
            "keywords": ["Programación", "Conectividad", "Telecomunicaciones"]
        },
        "Mecanica": {
            "titulo": "Área Industrial y Mecánica",
            "desc": "Disfrutas el trabajo de precisión, el diagnóstico de sistemas complejos y las soluciones tangibles. Tu perfil técnico es ideal para la manufactura u operación automotriz.",
            "icono": "bi-nut",
            "color": "secondary",
            "keywords": ["Mecánica", "Industrial", "Metalmecánica"]
        },
        "Salud": {
            "titulo": "Área de Salud y Servicios Sociales",
            "desc": "Tu vocación está fuertemente marcada por la empatía, el cuidado humano y la responsabilidad comunitaria.",
            "icono": "bi-heart-pulse",
            "color": "danger",
            "keywords": ["Enfermería", "Párvulos", "Social"]
        },
        "Administracion": {
            "titulo": "Área de Administración y Comercio",
            "desc": "Análisis organizado, gestión de flujos logísticos, finanzas claras y talento de planificación corporativa.",
            "icono": "bi-briefcase",
            "color": "success",
            "keywords": ["Administración", "Contabilidad", "Logística"]
        },
        "Electronica": {
            "titulo": "Área de Electricidad y Automatización",
            "desc": "Te fascina el control de la energía, la automatización de procesos y el funcionamiento del hardware interno de equipos.",
            "icono": "bi-lightning-charge",
            "color": "warning",
            "keywords": ["Electricidad", "Electrónica", "Automatización"]
        },
        "Diseño": {
            "titulo": "Área de Diseño y Comunicación Gráfica",
            "desc": "Tu mente es creativa, visual e innovadora. Tienes destreza para comunicar ideas a través de composiciones estéticas.",
            "icono": "bi-palette",
            "color": "info",
            "keywords": ["Gráfica", "Diseño", "Dibujo Técnico"]
        }
    }

    resultado_final = perfiles.get(area_predominante, perfiles["Tecnologia"])

    # --- MOTOR DE RECOMENDACIÓN DINÁMICO ---
    # Construimos un filtro acumulativo usando OR para buscar cualquier keyword del perfil
    condiciones = []
    for kw in resultado_final["keywords"]:
        condiciones.append(Liceo.especialidades.ilike(f"%{kw}%"))
    
    # Ejecutamos la consulta aplicando los filtros cruzados si existen condiciones
    liceos_recomendados = []
    if condiciones:
        from sqlalchemy import or_
        liceos_recomendados = Liceo.query.filter(or_(*condiciones)).limit(3).all()

    return render_template(
        "resultados.html", 
        resultado=resultado_final, 
        liceos=liceos_recomendados
    )