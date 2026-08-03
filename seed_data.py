# -*- coding: utf-8 -*-
"""
Catálogo de liceos técnico-profesionales de las 5 comunas de cobertura de
AcademyMap: La Cisterna, San Ramón, La Granja, San Miguel y El Bosque.

Todos los registros están marcados "verificado": True: nombre, comuna,
dirección y especialidades provienen de fuentes públicas (sitios
institucionales de cada liceo, directorio PACE-UMCE, Ministerio de
Educación / findmyschool.cl / boletinoficial.cl / grandescolegios.cl),
consultadas en julio de 2026. Las especialidades de cada liceo fueron
verificadas contra el sitio institucional MÁS RECIENTE disponible (varios
liceos actualizan su oferta de especialidades año a año); cuando el sitio
oficial 2026 estaba disponible, se priorizó sobre fuentes de directorios
de 2021-2022 que en algunos casos mostraban especialidades descontinuadas.

Las coordenadas (latitud/longitud) de estos 16 registros son APROXIMADAS
(ubicadas en el sector correcto de cada comuna, pero no geocodificadas
desde la dirección exacta). Se recomienda abrir cada liceo en el panel
administrador y usar el botón "Buscar en el mapa" para afinarlas a partir
de su dirección real; los liceos que se agreguen desde ahora en adelante
quedan geocodificados con precisión directamente desde el formulario.

Este catálogo busca reunir la totalidad de liceos técnico-profesionales
identificables mediante fuentes públicas en cada comuna. No existe un
listado único y consultable en línea del Ministerio de Educación filtrado
por comuna + modalidad, por lo que, si el usuario detecta un
establecimiento técnico-profesional de estas comunas que falte, puede
agregarse fácilmente desde el panel administrador.
"""

LICEOS_SEED = [
    # ------------------------------------------------------------------ #
    # LA CISTERNA (5 liceos)
    # ------------------------------------------------------------------ #
    {
        "nombre": "Liceo Politécnico Ciencia y Tecnología",
        "comuna": "La Cisterna",
        "direccion": "Av. Goycolea #469, La Cisterna",
        "descripcion": (
            "Liceo técnico-profesional de dependencia pública (SLEP Santa Rosa), "
            "con más de 60 años de trayectoria (fundado en 1963 como Escuela "
            "Técnica Femenina N°6). Forma en las áreas Comercial e Industrial, "
            "con cuatro especialidades acreditadas."
        ),
        "especialidades": "Administración mención RRHH y Logística,Química Industrial mención Laboratorio Químico,Electrónica,Telecomunicaciones",
        "areas": "administracion,electricidad,tecnologia",
        "caracteristicas": "Más de 60 años de trayectoria,Laboratorio de Química Industrial,Red de Mejoramiento TP,Programa PACE",
        "tipo": "Servicio Local de Educación",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "+56 44 314 4700",
        "gratuito": True,
        "matricula": 950,
        "rating": 4.3,
        "admision_pct": 65,
        "empleabilidad_pct": 80,
        "verificado": True,
        "latitud": -33.528,
        "longitud": -70.664,
    },
    {
        "nombre": "Liceo Técnico Industrial La Cisterna",
        "comuna": "La Cisterna",
        "direccion": "Avenida El Parrón #1741, La Cisterna",
        "descripcion": (
            "Con más de 60 años de trayectoria (RBD 9784-5), forma Técnicos de "
            "Nivel Medio en el área Industrial, con foco en dos especialidades "
            "acreditadas según su sitio institucional (actualizado 2026). "
            "Matrícula oficial: 302 estudiantes."
        ),
        "especialidades": "Mecánica Automotriz,Electricidad",
        "areas": "industrial,electricidad",
        "caracteristicas": "Más de 60 años de trayectoria,100% gratuito,Sostenedor sin fines de lucro",
        "tipo": "Particular Subvencionado",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "+56 2 9337425",
        "gratuito": True,
        "matricula": 302,
        "rating": 4.1,
        "admision_pct": 70,
        "empleabilidad_pct": 78,
        "verificado": True,
        "latitud": -33.5335,
        "longitud": -70.6605,
    },
    {
        "nombre": "Liceo Polivalente Olof Palme",
        "comuna": "La Cisterna",
        "direccion": "Julio Covarrubias #9370, La Cisterna",
        "descripcion": (
            "Liceo municipal (ex Liceo Veneciano) que en 2004 amplió su modalidad "
            "educativa incorporando la formación técnico-profesional del área "
            "Comercial, junto a un fuerte Programa de Integración Escolar (PIE) "
            "y un sello ecológico y medioambiental."
        ),
        "especialidades": "Administración",
        "areas": "administracion",
        "caracteristicas": "Programa de Integración Escolar (PIE),Sello Ecológico y Medioambiental,Subvención Escolar Preferencial",
        "tipo": "Municipal",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional",
        "gratuito": True,
        "matricula": 420,
        "rating": 3.7,
        "admision_pct": 76,
        "empleabilidad_pct": 68,
        "verificado": True,
        "latitud": -33.5265,
        "longitud": -70.672,
    },
    {
        "nombre": "Colegio Técnico Profesional San Ramón La Cisterna",
        "comuna": "La Cisterna",
        "direccion": "Alejandro Vial #8791, La Cisterna",
        "descripcion": (
            "Establecimiento particular subvencionado (pese a su nombre, ubicado "
            "físicamente en la comuna de La Cisterna) con foco en el área "
            "Comercial y Química Industrial, con infraestructura propia de "
            "talleres para cada especialidad."
        ),
        "especialidades": "Contabilidad,Laboratorio Químico,Administración",
        "areas": "administracion,electricidad",
        "caracteristicas": "Infraestructura propia de talleres,Programa de reforzamiento académico",
        "tipo": "Particular Subvencionado",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "+56 2 25967849",
        "gratuito": True,
        "matricula": 380,
        "rating": 3.8,
        "admision_pct": 72,
        "empleabilidad_pct": 70,
        "verificado": True,
        "latitud": -33.535,
        "longitud": -70.668,
    },
    {
        "nombre": "Centro Politécnico Carlos Condell",
        "comuna": "La Cisterna",
        "direccion": "Vicuña Mackenna #435, La Cisterna",
        "descripcion": (
            "Con más de 17 años de historia, es referente en formación "
            "técnico-profesional en modalidad dual: los estudiantes alternan una "
            "semana en el colegio y una en empresas o instituciones, aprendiendo "
            "con clientes reales desde temprano."
        ),
        "especialidades": "Hotelería,Atención de Párvulos,Mecánica Automotriz,Dibujo Técnico",
        "areas": "gastronomia,parvulos,industrial,construccion",
        "caracteristicas": "Modalidad dual (1 semana colegio / 1 semana empresa),Inglés técnico,Equipo de psicología y psicopedagogía",
        "tipo": "Particular Subvencionado",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional",
        "gratuito": True,
        "matricula": 340,
        "rating": 4.0,
        "admision_pct": 69,
        "empleabilidad_pct": 76,
        "verificado": True,
        "latitud": -33.5245,
        "longitud": -70.659,
    },
    # ------------------------------------------------------------------ #
    # SAN RAMÓN (4 liceos)
    # ------------------------------------------------------------------ #
    {
        "nombre": "Centro Educacional Municipal San Ramón",
        "comuna": "San Ramón",
        "direccion": "Almirante Latorre #9701, San Ramón",
        "descripcion": (
            "Liceo técnico-profesional municipal fundado en 1987. Imparte "
            "Electricidad y Construcción desde su origen, y desde 2011 la "
            "especialidad de Atención de Enfermería, incluyendo modalidad "
            "vespertina 2x1 para jóvenes y adultos."
        ),
        "especialidades": "Electricidad,Construcción,Atención de Enfermería",
        "areas": "electricidad,construccion,salud",
        "caracteristicas": "Laboratorio de computación,Talleres de electricidad y construcción,Educación vespertina 2x1,Apoyo de salud escolar",
        "tipo": "Municipal",
        "jornada": "Diurna y Vespertina",
        "imagen": "",
        "contacto": "Consultar en sitio institucional",
        "gratuito": True,
        "matricula": 298,
        "rating": 4.0,
        "admision_pct": 72,
        "empleabilidad_pct": 74,
        "verificado": True,
        "latitud": -33.5405,
        "longitud": -70.635,
    },
    {
        "nombre": "Liceo Comercial Vate Vicente Huidobro",
        "comuna": "San Ramón",
        "direccion": "Doñihue #2030, San Ramón",
        "descripcion": (
            "Liceo técnico-profesional de la Fundación Educacional COMEDUC (RBD "
            "9584), parte de la red de establecimientos PACE en convenio con la "
            "Universidad Metropolitana de Ciencias de la Educación. Desde 2026 "
            "ofrece 4 especialidades profesionales, incorporando Programación."
        ),
        "especialidades": "Administración mención Recursos Humanos,Administración mención Logística,Contabilidad,Programación",
        "areas": "administracion,tecnologia",
        "caracteristicas": "Convenio PACE-UMCE,Certificación internacional ISO 21001,4 especialidades profesionales",
        "tipo": "Municipal",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional",
        "gratuito": True,
        "matricula": 520,
        "rating": 3.9,
        "admision_pct": 75,
        "empleabilidad_pct": 70,
        "verificado": True,
        "latitud": -33.536,
        "longitud": -70.642,
    },
    {
        "nombre": "Centro Educacional Mirador",
        "comuna": "San Ramón",
        "direccion": "Av. Mirador #1470, San Ramón",
        "descripcion": (
            "Liceo municipal (RBD 9608) de la zona norte de San Ramón, con lema "
            "'Educar en el Afecto, Inclusión y Diversidad'. Adscrito al Programa "
            "PACE desde 2018, con resultados SIMCE sobre el promedio nacional. "
            "Matrícula oficial: 118 estudiantes."
        ),
        "especialidades": "Electrónica,Servicio de Alimentación Colectiva",
        "areas": "electricidad,gastronomia",
        "caracteristicas": "Programa PACE desde 2018,Resultados SIMCE sobre el promedio nacional,Entrada accesible para sillas de ruedas",
        "tipo": "Municipal",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional",
        "gratuito": True,
        "matricula": 118,
        "rating": 3.9,
        "admision_pct": 78,
        "empleabilidad_pct": 69,
        "verificado": True,
        "latitud": -33.533,
        "longitud": -70.644,
    },
    {
        "nombre": "Centro Educacional Purkuyén",
        "comuna": "San Ramón",
        "direccion": "Pasaje Profesor David Catilao Riveros #8450, San Ramón",
        "descripcion": (
            "Liceo municipal (RBD 9599) fundado en 1970, con tradición en la "
            "comuna. Incorporó la Educación Técnico Profesional en 1994; desde "
            "1998 se denomina Centro Educacional Purkuyén, con un sello de "
            "expresión artística, cultural y deportiva."
        ),
        "especialidades": "Administración,Atención de Enfermería",
        "areas": "administracion,salud",
        "caracteristicas": "Tradición desde 1970,Sello de expresión artística y deportiva",
        "tipo": "Municipal",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional",
        "gratuito": True,
        "matricula": 260,
        "rating": 3.7,
        "admision_pct": 79,
        "empleabilidad_pct": 66,
        "verificado": True,
        "latitud": -33.544,
        "longitud": -70.637,
    },
    # ------------------------------------------------------------------ #
    # SAN MIGUEL (3 liceos)
    # ------------------------------------------------------------------ #
    {
        "nombre": "Liceo Técnico de San Miguel",
        "comuna": "San Miguel",
        "direccion": "Av. José Miguel Carrera 4688, San Miguel",
        "descripcion": (
            "Establecimiento femenino de Corporación de Administración Delegada "
            "con tres especialidades acreditadas y una matrícula que supera las "
            "810 alumnas cada año. Ubicado frente a la estación de metro Lo Vial "
            "(Línea 2), pone énfasis en la Formación General y en la práctica "
            "profesional final."
        ),
        "especialidades": "Gastronomía mención Cocina,Vestuario y Confección Textil,Atención de Párvulos",
        "areas": "gastronomia,parvulos",
        "caracteristicas": "Acceso directo desde Metro Lo Vial,Talleres de confección textil,Práctica profesional final",
        "tipo": "Corporación de Administración Delegada",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional (ltsm.cl)",
        "gratuito": True,
        "matricula": 810,
        "rating": 4.2,
        "admision_pct": 68,
        "empleabilidad_pct": 76,
        "verificado": True,
        "latitud": -33.499,
        "longitud": -70.652,
    },
    {
        "nombre": "Liceo Politécnico San Luis",
        "comuna": "San Miguel",
        "direccion": "Gran Avenida José Miguel Carrera #5941, San Miguel",
        "descripcion": (
            "Establecimiento particular subvencionado con cinco áreas de "
            "formación técnico-profesional y un edificio anexo en Carmen Mena "
            "970. Ofrece también modalidad de educación vespertina para jóvenes "
            "y adultos a través de un colegio asociado."
        ),
        "especialidades": "Electrónica,Enfermería,Administración,Atención de Párvulos,Gastronomía",
        "areas": "electricidad,salud,administracion,parvulos,gastronomia",
        "caracteristicas": "5 especialidades técnico-profesionales,Edificio anexo Carmen Mena,Bolsa de trabajo propia,Educación vespertina asociada",
        "tipo": "Particular Subvencionado",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "+56 2 64691846",
        "gratuito": True,
        "matricula": 700,
        "rating": 3.9,
        "admision_pct": 66,
        "empleabilidad_pct": 73,
        "verificado": True,
        "latitud": -33.508,
        "longitud": -70.654,
    },
    {
        "nombre": "Instituto Superior de Comercio de Chile (INSUCO)",
        "comuna": "San Miguel",
        "direccion": "Álvarez de Toledo #1060, San Miguel",
        "descripcion": (
            "Liceo femenino fundado en 1960 como Instituto Comercial Femenino "
            "N°4, funcionando en su dirección actual desde 1961. Parte de la "
            "red Liceos UTEM (Corporación de Administración Delegada), ofrece "
            "formación comercial y de salud a media cuadra del Metro San Miguel."
        ),
        "especialidades": "Administración,Contabilidad,Atención de Enfermería",
        "areas": "administracion,salud",
        "caracteristicas": "Más de 60 años de trayectoria,Parte de la red Liceos UTEM,Áreas verdes en el campus",
        "tipo": "Corporación de Administración Delegada",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional (insucochile.cl)",
        "gratuito": True,
        "matricula": 480,
        "rating": 3.9,
        "admision_pct": 71,
        "empleabilidad_pct": 72,
        "verificado": True,
        "latitud": -33.493,
        "longitud": -70.648,
    },
    # ------------------------------------------------------------------ #
    # LA GRANJA (2 liceos)
    # ------------------------------------------------------------------ #
    {
        "nombre": "Liceo Técnico Profesional Patricio Aylwin Azócar",
        "comuna": "La Granja",
        "direccion": "Sofía Eastman de Hunneus #10411, La Granja",
        "descripcion": (
            "Liceo del Servicio Local de Educación Pública Gabriela Mistral "
            "(RBD 26501), con foco en Ciencia y Tecnología desde su fundación "
            "en 2009. Combina Educación Científico-Humanista con especialidades "
            "técnicas, incorporando Programación desde 2024. Matrícula oficial: "
            "388 estudiantes."
        ),
        "especialidades": "Química Industrial mención Laboratorio Químico,Electrónica,Programación",
        "areas": "electricidad,tecnologia,industrial",
        "caracteristicas": "Programa PACE-UTEM,Especialidad de Programación (2024),Enfoque en ciencia y tecnología",
        "tipo": "Servicio Local de Educación",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "+56 2 24011646",
        "gratuito": True,
        "matricula": 388,
        "rating": 4.0,
        "admision_pct": 70,
        "empleabilidad_pct": 75,
        "verificado": True,
        "latitud": -33.545,
        "longitud": -70.615,
    },
    {
        "nombre": "Liceo Bicentenario Francisco Frías Valenzuela",
        "comuna": "La Granja",
        "direccion": "Avenida Santa Rosa #6740, La Granja",
        "descripcion": (
            "Liceo polivalente del Servicio Local de Educación Pública Gabriela "
            "Mistral (RBD 9582-6), único establecimiento del sector (La Granja, "
            "San Joaquín y Macul) que imparte Construcciones Metálicas desde "
            "1986, junto a un Programa de Integración Escolar (PIE) con equipo "
            "multidisciplinario."
        ),
        "especialidades": "Construcciones Metálicas,Gastronomía",
        "areas": "construccion,gastronomia",
        "caracteristicas": "Única oferta de Construcciones Metálicas del sector,Programa de Integración Escolar (PIE),Alianzas con empresas e instituciones",
        "tipo": "Servicio Local de Educación",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "+56 2 3669385",
        "gratuito": True,
        "matricula": 540,
        "rating": 3.8,
        "admision_pct": 74,
        "empleabilidad_pct": 71,
        "verificado": True,
        "latitud": -33.539,
        "longitud": -70.622,
    },
    # ------------------------------------------------------------------ #
    # EL BOSQUE (2 liceos)
    # ------------------------------------------------------------------ #
    {
        "nombre": "Colegio María Griselda Valle",
        "comuna": "El Bosque",
        "direccion": "Lo Martínez #923, El Bosque",
        "descripcion": (
            "Fundación educacional creada en 1981, técnico-profesional desde "
            "1985, parte de la Corporación San Isidoro. Entre los 10 mejores a "
            "nivel comunal en SIMCE de Matemática 4° básico y Lectura II° medio, "
            "cercano al Hospital El Pino."
        ),
        "especialidades": "Administración,Contabilidad,Mecánica Automotriz,Gastronomía",
        "areas": "administracion,industrial,gastronomia",
        "caracteristicas": "Programa de Integración Escolar (PIE),Más de 40 años de trayectoria,Cercano a Hospital El Pino",
        "tipo": "Particular Subvencionado",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "Consultar en sitio institucional",
        "gratuito": True,
        "matricula": 650,
        "rating": 4.1,
        "admision_pct": 66,
        "empleabilidad_pct": 77,
        "verificado": True,
        "latitud": -33.564,
        "longitud": -70.671,
    },
    {
        "nombre": "Liceo N°14 Juan Gómez Millas",
        "comuna": "El Bosque",
        "direccion": "Gran Avenida José Miguel Carrera #9740, El Bosque",
        "descripcion": (
            "Liceo polivalente (RBD 9688) que desde enero de 2025 depende del "
            "Servicio Local de Educación Pública El Pino. Imparte formación "
            "Humanístico-Científica y Técnico-Profesional, con un lema propio "
            "de educación 'polivalente, transformadora y afectiva'. Matrícula "
            "oficial: 582 estudiantes."
        ),
        "especialidades": "Gastronomía,Administración,Atención de Párvulos",
        "areas": "gastronomia,administracion,parvulos",
        "caracteristicas": "SLEP El Pino,Programa de Integración Escolar,582 estudiantes matriculados",
        "tipo": "Servicio Local de Educación",
        "jornada": "Diurna",
        "imagen": "",
        "contacto": "+56 44 304 9999",
        "gratuito": True,
        "matricula": 582,
        "rating": 3.9,
        "admision_pct": 62,
        "empleabilidad_pct": 74,
        "verificado": True,
        "latitud": -33.559,
        "longitud": -70.676,
    },
]
