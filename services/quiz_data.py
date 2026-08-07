"""
Banco de datos del test vocacional: áreas técnico-profesionales y preguntas.

Este módulo NO usa IA externa. La lógica de recomendación es una suma de
ponderaciones por respuesta (ver services/recommendation.py), pero el
diccionario AREAS y la lista QUESTIONS están aislados aquí para poder
enchufar en el futuro un motor más sofisticado (ej. un modelo de IA) sin
tocar las rutas ni las plantillas.
"""

# Cada área agrupa a los liceos según su oferta formativa y se usa tanto en
# el quiz como en los filtros del explorador de liceos.
AREAS = {
    "tecnologia": {
        "nombre": "Tecnología e Informática",
        "icono": "bi-cpu",
        "color": "#4f46e5",
        "descripcion": "Programación, redes, soporte y telecomunicaciones.",
    },
    "industrial": {
        "nombre": "Industrial y Mecánica",
        "icono": "bi-gear-wide-connected",
        "color": "#0ea5a4",
        "descripcion": "Mecánica automotriz, mecánica industrial y mantenimiento.",
    },
    "salud": {
        "nombre": "Salud y Bienestar",
        "icono": "bi-heart-pulse",
        "color": "#ef4770",
        "descripcion": "Atención de enfermería y cuidado de personas.",
    },
    "gastronomia": {
        "nombre": "Gastronomía y Turismo",
        "icono": "bi-cup-hot",
        "color": "#f59e0b",
        "descripcion": "Cocina, alimentación colectiva y servicios turísticos.",
    },
    "administracion": {
        "nombre": "Administración y Comercio",
        "icono": "bi-briefcase",
        "color": "#7c3aed",
        "descripcion": "Contabilidad, administración, ventas y logística.",
    },
    "construccion": {
        "nombre": "Construcción",
        "icono": "bi-hammer",
        "color": "#b45309",
        "descripcion": "Edificación, obras civiles y dibujo técnico.",
    },
    "electricidad": {
        "nombre": "Electricidad y Electrónica",
        "icono": "bi-lightning-charge",
        "color": "#eab308",
        "descripcion": "Instalaciones eléctricas, electrónica y química industrial.",
    },
    "parvulos": {
        "nombre": "Atención de Párvulos y Textil",
        "icono": "bi-palette",
        "color": "#ec4899",
        "descripcion": "Atención de párvulos, vestuario y confección textil.",
    },
}

# 12 preguntas, 4 alternativas cada una, con un ícono representativo por
# alternativa (usado en la interfaz del quiz). Los "pesos" indican cuántos
# puntos suma cada alternativa a cada área vocacional. Con 12 preguntas se
# obtiene una resolución mucho más fina que con 6, evitando empates y dando
# una base más sólida para el resumen de resultados.
QUESTIONS = [
    {
        "id": "q1",
        "pregunta": "¿Qué actividad disfrutas más en tu tiempo libre?",
        "ayuda": "Elige la que más se acerca a ti.",
        "opciones": [
            {"texto": "Armar o reparar cosas", "icono": "bi-tools", "weights": {"industrial": 3, "construccion": 2, "electricidad": 1}},
            {"texto": "Usar el computador y crear", "icono": "bi-laptop", "weights": {"tecnologia": 3, "administracion": 1}},
            {"texto": "Cocinar o compartir con gente", "icono": "bi-egg-fried", "weights": {"gastronomia": 3, "salud": 1}},
            {"texto": "Cuidar y jugar con niños pequeños", "icono": "bi-balloon-heart", "weights": {"parvulos": 3, "salud": 1}},
        ],
    },
    {
        "id": "q2",
        "pregunta": "¿Cuál de estas materias se te da mejor?",
        "ayuda": "Piensa en dónde te sientes con más confianza.",
        "opciones": [
            {"texto": "Matemáticas y lógica", "icono": "bi-calculator", "weights": {"tecnologia": 2, "electricidad": 2, "administracion": 1}},
            {"texto": "Ciencias naturales y biología", "icono": "bi-clipboard-pulse", "weights": {"salud": 3, "parvulos": 1}},
            {"texto": "Tecnología y talleres", "icono": "bi-wrench-adjustable", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Lenguaje y trabajo en equipo", "icono": "bi-people", "weights": {"administracion": 2, "gastronomia": 1, "salud": 1}},
        ],
    },
    {
        "id": "q3",
        "pregunta": "¿Cómo te gustaría que fuera tu trabajo ideal?",
        "ayuda": "Imagina cómo sería tu día a día.",
        "opciones": [
            {"texto": "Frente a una pantalla resolviendo problemas", "icono": "bi-code-slash", "weights": {"tecnologia": 3, "administracion": 1}},
            {"texto": "En terreno, usando herramientas", "icono": "bi-cone-striped", "weights": {"industrial": 2, "construccion": 2, "electricidad": 1}},
            {"texto": "Ayudando y cuidando a otras personas", "icono": "bi-hand-thumbs-up", "weights": {"salud": 3, "parvulos": 2}},
            {"texto": "En una cocina o atendiendo público", "icono": "bi-shop", "weights": {"gastronomia": 3, "administracion": 1}},
        ],
    },
    {
        "id": "q4",
        "pregunta": "¿Qué habilidad crees que es tu punto fuerte?",
        "ayuda": "No hay respuestas incorrectas.",
        "opciones": [
            {"texto": "Ser ordenado y planificar", "icono": "bi-list-check", "weights": {"administracion": 3, "construccion": 1}},
            {"texto": "Ser creativo con las manos", "icono": "bi-palette2", "weights": {"gastronomia": 2, "industrial": 1, "construccion": 1}},
            {"texto": "Entender cómo funcionan las máquinas", "icono": "bi-gear", "weights": {"electricidad": 2, "industrial": 2}},
            {"texto": "Aprender tecnología rápidamente", "icono": "bi-lightning", "weights": {"tecnologia": 3}},
        ],
    },
    {
        "id": "q5",
        "pregunta": "¿Qué proyecto te emocionaría más realizar?",
        "ayuda": "Elige el que te haría decir '¡quiero hacer eso!'.",
        "opciones": [
            {"texto": "Crear una app o reparar un equipo electrónico", "icono": "bi-phone", "weights": {"tecnologia": 2, "electricidad": 2}},
            {"texto": "Diseñar o construir algo con tus manos", "icono": "bi-rulers", "weights": {"construccion": 3, "industrial": 1}},
            {"texto": "Preparar un banquete para un evento", "icono": "bi-cake2", "weights": {"gastronomia": 3}},
            {"texto": "Organizar las finanzas de un pequeño negocio", "icono": "bi-graph-up", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q6",
        "pregunta": "¿En qué tipo de ambiente rindes mejor?",
        "ayuda": "Piensa en dónde te concentras y disfrutas.",
        "opciones": [
            {"texto": "Una posta, clínica o sala cuna", "icono": "bi-hospital", "weights": {"salud": 2, "parvulos": 2}},
            {"texto": "Un taller con máquinas y herramientas", "icono": "bi-nut", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Una oficina organizada", "icono": "bi-building", "weights": {"administracion": 3}},
            {"texto": "Una cocina o un casino escolar", "icono": "bi-cup-straw", "weights": {"gastronomia": 3}},
        ],
    },
    {
        "id": "q7",
        "pregunta": "¿Qué tipo de problema te gusta más resolver?",
        "ayuda": "Todos resolvemos problemas distintos, ¿cuál te acomoda?",
        "opciones": [
            {"texto": "Algo que no enciende o no funciona bien", "icono": "bi-plug", "weights": {"electricidad": 2, "industrial": 2}},
            {"texto": "Un error en un programa o sistema", "icono": "bi-bug", "weights": {"tecnologia": 3}},
            {"texto": "Un conflicto entre personas", "icono": "bi-emoji-smile", "weights": {"salud": 2, "parvulos": 1, "administracion": 1}},
            {"texto": "Cómo hacer que algo se vea o sepa mejor", "icono": "bi-stars", "weights": {"gastronomia": 2, "construccion": 2}},
        ],
    },
    {
        "id": "q8",
        "pregunta": "Si tuvieras que dar una breve charla, ¿de qué tema hablarías con más gusto?",
        "ayuda": "Elige el tema que te resulte más natural explicar.",
        "opciones": [
            {"texto": "Las últimas novedades en tecnología", "icono": "bi-cpu-fill", "weights": {"tecnologia": 3}},
            {"texto": "Cómo funciona un motor o una instalación eléctrica", "icono": "bi-car-front", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Alimentación saludable o una receta especial", "icono": "bi-basket", "weights": {"gastronomia": 3}},
            {"texto": "Primeros auxilios o cuidado de otras personas", "icono": "bi-bandaid", "weights": {"salud": 3}},
        ],
    },
    {
        "id": "q9",
        "pregunta": "¿Qué tipo de video verías por puro gusto?",
        "ayuda": "Piensa en lo último que buscaste por curiosidad.",
        "opciones": [
            {"texto": "Un tutorial de programación o edición", "icono": "bi-terminal", "weights": {"tecnologia": 3}},
            {"texto": "La construcción de una casa desde cero", "icono": "bi-house-gear", "weights": {"construccion": 3}},
            {"texto": "Una receta paso a paso", "icono": "bi-egg", "weights": {"gastronomia": 3}},
            {"texto": "Consejos de cuidado y estimulación infantil", "icono": "bi-emoji-laughing", "weights": {"parvulos": 3}},
        ],
    },
    {
        "id": "q10",
        "pregunta": "En un trabajo en grupo, ¿qué rol tomas naturalmente?",
        "ayuda": "Piensa en la última vez que trabajaste en equipo.",
        "opciones": [
            {"texto": "El o la que organiza tareas y lleva las cuentas", "icono": "bi-kanban", "weights": {"administracion": 3}},
            {"texto": "El o la que arregla los problemas técnicos", "icono": "bi-tools", "weights": {"electricidad": 2, "industrial": 1}},
            {"texto": "El o la que se preocupa de que todos estén bien", "icono": "bi-heart", "weights": {"salud": 2, "parvulos": 2}},
            {"texto": "El o la que presenta o vende la idea final", "icono": "bi-megaphone", "weights": {"administracion": 1, "gastronomia": 1, "tecnologia": 1}},
        ],
    },
    {
        "id": "q11",
        "pregunta": "¿Qué te importa más al pensar en tu futuro trabajo?",
        "ayuda": "Elige lo que más peso tiene para ti hoy.",
        "opciones": [
            {"texto": "Estabilidad y un buen sueldo", "icono": "bi-cash-coin", "weights": {"administracion": 2, "electricidad": 1}},
            {"texto": "Ayudar directamente a otras personas", "icono": "bi-hand-thumbs-up", "weights": {"salud": 3, "parvulos": 1}},
            {"texto": "Crear cosas con tus propias manos", "icono": "bi-hammer", "weights": {"industrial": 2, "construccion": 2}},
            {"texto": "Estar siempre a la vanguardia tecnológica", "icono": "bi-rocket-takeoff", "weights": {"tecnologia": 3}},
        ],
    },
    {
        "id": "q12",
        "pregunta": "Elige la palabra que más te representa",
        "ayuda": "Confía en tu primera reacción.",
        "opciones": [
            {"texto": "Preciso/a", "icono": "bi-bullseye", "weights": {"electricidad": 2, "tecnologia": 2}},
            {"texto": "Cuidadoso/a", "icono": "bi-shield-heart", "weights": {"salud": 2, "parvulos": 2}},
            {"texto": "Creativo/a", "icono": "bi-brush", "weights": {"gastronomia": 2, "construccion": 2}},
            {"texto": "Organizado/a", "icono": "bi-card-checklist", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q13",
        "pregunta": "¿Qué app usarías más si pudieras crear una?",
        "ayuda": "Piensa en qué problema te gustaría resolver.",
        "opciones": [
            {"texto": "Una app de delivery de comida", "icono": "bi-basket2", "weights": {"gastronomia": 3}},
            {"texto": "Una app para aprender un oficio", "icono": "bi-wrench", "weights": {"industrial": 2, "electricidad": 1}},
            {"texto": "Una app de finanzas personales", "icono": "bi-piggy-bank", "weights": {"administracion": 3}},
            {"texto": "Una app o videojuego nuevo", "icono": "bi-controller", "weights": {"tecnologia": 3}},
        ],
    },
    {
        "id": "q14",
        "pregunta": "Si ganaras un curso gratis, ¿cuál elegirías?",
        "ayuda": "Elige el que te den más ganas de tomar.",
        "opciones": [
            {"texto": "Robótica o programación", "icono": "bi-robot", "weights": {"tecnologia": 2, "electricidad": 1}},
            {"texto": "Repostería o cocina", "icono": "bi-cake", "weights": {"gastronomia": 3}},
            {"texto": "Primeros auxilios", "icono": "bi-heart-pulse-fill", "weights": {"salud": 3}},
            {"texto": "Emprendimiento y negocios", "icono": "bi-graph-up-arrow", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q15",
        "pregunta": "¿Qué objeto te gustaría entender mejor cómo funciona por dentro?",
        "ayuda": "Elige el que más curiosidad te da.",
        "opciones": [
            {"texto": "Un computador o celular", "icono": "bi-motherboard", "weights": {"tecnologia": 3}},
            {"texto": "El motor de un auto", "icono": "bi-car-front-fill", "weights": {"industrial": 3}},
            {"texto": "La instalación eléctrica de una casa", "icono": "bi-lightning-charge-fill", "weights": {"electricidad": 3}},
            {"texto": "Una máquina de coser", "icono": "bi-scissors", "weights": {"parvulos": 2, "industrial": 1}},
        ],
    },
    {
        "id": "q16",
        "pregunta": "Si ayudaras a organizar un evento del colegio, ¿qué tarea elegirías?",
        "ayuda": "Piensa en tu rol ideal dentro del equipo.",
        "opciones": [
            {"texto": "Hacer el presupuesto y las compras", "icono": "bi-receipt", "weights": {"administracion": 3}},
            {"texto": "Preparar la comida para todos", "icono": "bi-egg-fried", "weights": {"gastronomia": 3}},
            {"texto": "Armar la decoración y estructuras", "icono": "bi-tools", "weights": {"construccion": 3}},
            {"texto": "Cuidar a los niños que asistan", "icono": "bi-emoji-smile-fill", "weights": {"parvulos": 3}},
        ],
    },
    {
        "id": "q17",
        "pregunta": "¿Qué te da más satisfacción?",
        "ayuda": "Elige lo que más te llena.",
        "opciones": [
            {"texto": "Ver algo terminado y bien construido", "icono": "bi-house-check", "weights": {"construccion": 2, "industrial": 2}},
            {"texto": "Ver a alguien sentirse mejor gracias a ti", "icono": "bi-emoji-heart-eyes", "weights": {"salud": 3}},
            {"texto": "Ver que un sistema funciona sin errores", "icono": "bi-check2-square", "weights": {"tecnologia": 3}},
            {"texto": "Ver que las cuentas cuadran perfecto", "icono": "bi-clipboard-data", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q18",
        "pregunta": "Elige un lugar de práctica que te llame la atención",
        "ayuda": "Imagina tu primer día de práctica profesional.",
        "opciones": [
            {"texto": "Un taller mecánico", "icono": "bi-gear-fill", "weights": {"industrial": 3}},
            {"texto": "La oficina de una empresa", "icono": "bi-building-fill", "weights": {"administracion": 3}},
            {"texto": "Un jardín infantil", "icono": "bi-flower1", "weights": {"parvulos": 3}},
            {"texto": "Un laboratorio o centro de datos", "icono": "bi-server", "weights": {"tecnologia": 2, "electricidad": 1}},
        ],
    },
    {
        "id": "q19",
        "pregunta": "¿Qué feria o exposición visitarías con más ganas?",
        "ayuda": "Elige la que te daría más curiosidad visitar.",
        "opciones": [
            {"texto": "Una feria de tecnología y robótica", "icono": "bi-cpu", "weights": {"tecnologia": 3}},
            {"texto": "Una feria gastronómica", "icono": "bi-cup-hot-fill", "weights": {"gastronomia": 3}},
            {"texto": "Una expo de construcción y arquitectura", "icono": "bi-buildings", "weights": {"construccion": 3}},
            {"texto": "Una feria de salud y bienestar", "icono": "bi-heart-pulse", "weights": {"salud": 3}},
        ],
    },
    {
        "id": "q20",
        "pregunta": "Si pudieras aprender un oficio este fin de semana, ¿cuál sería?",
        "ayuda": "Elige el que más te llame.",
        "opciones": [
            {"texto": "Electricidad básica", "icono": "bi-plug-fill", "weights": {"electricidad": 3}},
            {"texto": "Cocina", "icono": "bi-egg-fill", "weights": {"gastronomia": 3}},
            {"texto": "Cuidado de bebés", "icono": "bi-balloon-heart-fill", "weights": {"parvulos": 3}},
            {"texto": "Reparación de celulares", "icono": "bi-phone-vibrate", "weights": {"tecnologia": 2, "electricidad": 1}},
        ],
    },
    {
        "id": "q21",
        "pregunta": "¿Qué te gustaría reparar si se rompe en tu casa?",
        "ayuda": "Piensa en qué te dan ganas de intentar arreglar tú mismo/a.",
        "opciones": [
            {"texto": "Un enchufe o interruptor", "icono": "bi-plug", "weights": {"electricidad": 3}},
            {"texto": "Una llave de agua o cañería", "icono": "bi-droplet", "weights": {"construccion": 3}},
            {"texto": "El motor de un vehículo", "icono": "bi-car-front", "weights": {"industrial": 3}},
            {"texto": "Nada, prefiero coordinar quién lo arregla", "icono": "bi-clipboard-check", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q22",
        "pregunta": "¿Qué tipo de videojuego jugarías por horas?",
        "ayuda": "El que más te enganchó alguna vez, o te gustaría probar.",
        "opciones": [
            {"texto": "Uno de construir ciudades o gestionar recursos", "icono": "bi-building", "weights": {"construccion": 2, "administracion": 2}},
            {"texto": "Uno de simulación de cocina o restaurante", "icono": "bi-egg-fried", "weights": {"gastronomia": 3}},
            {"texto": "Uno de resolver acertijos tecnológicos", "icono": "bi-puzzle", "weights": {"tecnologia": 3}},
            {"texto": "Uno de cuidar mascotas o personajes", "icono": "bi-heart", "weights": {"parvulos": 2, "salud": 1}},
        ],
    },
    {
        "id": "q23",
        "pregunta": "Si trabajaras en un hospital sin ser médico/a, ¿qué rol elegirías?",
        "ayuda": "Todos los roles son igual de importantes.",
        "opciones": [
            {"texto": "Apoyar en la atención de pacientes", "icono": "bi-heart-pulse", "weights": {"salud": 3}},
            {"texto": "Mantener los equipos funcionando", "icono": "bi-tools", "weights": {"electricidad": 2, "industrial": 1}},
            {"texto": "Administrar horarios y fichas", "icono": "bi-calendar-check", "weights": {"administracion": 3}},
            {"texto": "Estar a cargo de la cafetería", "icono": "bi-cup-hot", "weights": {"gastronomia": 3}},
        ],
    },
    {
        "id": "q24",
        "pregunta": "¿Qué te gustaría diseñar desde cero?",
        "ayuda": "Elige lo que más te motivaría crear.",
        "opciones": [
            {"texto": "Los planos de una casa", "icono": "bi-rulers", "weights": {"construccion": 3}},
            {"texto": "El menú de un restaurante", "icono": "bi-journal-richtext", "weights": {"gastronomia": 3}},
            {"texto": "Una app o página web", "icono": "bi-window", "weights": {"tecnologia": 3}},
            {"texto": "La instalación eléctrica de un edificio", "icono": "bi-lightning", "weights": {"electricidad": 3}},
        ],
    },
    {
        "id": "q25",
        "pregunta": "¿Qué actividad de fin de semana preferirías?",
        "ayuda": "Imagina un sábado libre para hacer lo que quieras.",
        "opciones": [
            {"texto": "Armar un mueble siguiendo instrucciones", "icono": "bi-hammer", "weights": {"industrial": 2, "construccion": 2}},
            {"texto": "Hornear algo que nunca has hecho", "icono": "bi-cake2", "weights": {"gastronomia": 3}},
            {"texto": "Configurar o probar un equipo tecnológico nuevo", "icono": "bi-laptop", "weights": {"tecnologia": 3}},
            {"texto": "Cuidar a un primo o hermano pequeño", "icono": "bi-balloon-heart", "weights": {"parvulos": 3}},
        ],
    },
    {
        "id": "q26",
        "pregunta": "¿Qué te gustaría que dijeran de ti en el futuro?",
        "ayuda": "Piensa en cómo te gustaría que te recordaran en un trabajo.",
        "opciones": [
            {"texto": "\"Es muy bueno/a arreglando cosas\"", "icono": "bi-wrench-adjustable", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "\"Siempre ayuda a los demás\"", "icono": "bi-hand-thumbs-up", "weights": {"salud": 2, "parvulos": 2}},
            {"texto": "\"Tiene todo súper organizado\"", "icono": "bi-list-check", "weights": {"administracion": 3}},
            {"texto": "\"Cocina increíble\"", "icono": "bi-stars", "weights": {"gastronomia": 3}},
        ],
    },
    {
        "id": "q27",
        "pregunta": "Si tuvieras un rincón propio en tu casa para hacer lo que quieras, ¿cuál sería?",
        "ayuda": "Imagina tu espacio ideal.",
        "opciones": [
            {"texto": "Un taller con herramientas", "icono": "bi-tools", "weights": {"industrial": 3}},
            {"texto": "Un rincón con computador y cables", "icono": "bi-cpu", "weights": {"tecnologia": 2, "electricidad": 1}},
            {"texto": "Una cocina de pruebas", "icono": "bi-cup-straw", "weights": {"gastronomia": 3}},
            {"texto": "Un espacio de manualidades y costura", "icono": "bi-scissors", "weights": {"parvulos": 2, "construccion": 1}},
        ],
    },
    {
        "id": "q28",
        "pregunta": "¿Qué se te hace más entretenido de ver en videos?",
        "ayuda": "Lo que verías sin aburrirte.",
        "opciones": [
            {"texto": "Retos o técnicas de cocina", "icono": "bi-egg-fried", "weights": {"gastronomia": 3}},
            {"texto": "Reseñas de tecnología nueva", "icono": "bi-phone", "weights": {"tecnologia": 3}},
            {"texto": "Transformaciones de autos", "icono": "bi-car-front-fill", "weights": {"industrial": 3}},
            {"texto": "Cómo se construyen edificios grandes", "icono": "bi-building-fill-gear", "weights": {"construccion": 3}},
        ],
    },
    {
        "id": "q29",
        "pregunta": "Si ganaras un premio en el colegio, ¿en qué área te gustaría destacar?",
        "ayuda": "El reconocimiento que más te gustaría recibir.",
        "opciones": [
            {"texto": "En un taller técnico", "icono": "bi-gear", "weights": {"electricidad": 2, "industrial": 2}},
            {"texto": "En apoyar a compañeros más chicos", "icono": "bi-emoji-smile", "weights": {"parvulos": 3}},
            {"texto": "En organizar una actividad del curso", "icono": "bi-kanban", "weights": {"administracion": 3}},
            {"texto": "En una feria de ciencias o tecnología", "icono": "bi-cpu-fill", "weights": {"tecnologia": 3}},
        ],
    },
    {
        "id": "q30",
        "pregunta": "¿Qué herramienta te llama más la atención?",
        "ayuda": "La que te den ganas de tomar y probar.",
        "opciones": [
            {"texto": "Un multitester o taladro eléctrico", "icono": "bi-plug-fill", "weights": {"electricidad": 3}},
            {"texto": "Una llave de tuercas o herramientas de mecánica", "icono": "bi-wrench", "weights": {"industrial": 3}},
            {"texto": "Un computador o tablet", "icono": "bi-tablet", "weights": {"tecnologia": 3}},
            {"texto": "Un set de cuchillos de cocina", "icono": "bi-egg", "weights": {"gastronomia": 3}},
        ],
    },
    {
        "id": "q31",
        "pregunta": "Si tuvieras que enseñarle algo a un amigo, ¿qué elegirías?",
        "ayuda": "Piensa en algo que sabes hacer y te gusta compartir.",
        "opciones": [
            {"texto": "A arreglar o armar algo", "icono": "bi-tools", "weights": {"industrial": 2, "electricidad": 1}},
            {"texto": "A cocinar una receta fácil", "icono": "bi-cup-hot", "weights": {"gastronomia": 3}},
            {"texto": "A usar un programa o app", "icono": "bi-display", "weights": {"tecnologia": 3}},
            {"texto": "A cuidar a un hermano/a menor", "icono": "bi-people", "weights": {"parvulos": 3}},
        ],
    },
    {
        "id": "q32",
        "pregunta": "¿Qué te generaría más orgullo terminar?",
        "ayuda": "El resultado que más satisfacción te daría ver hecho.",
        "opciones": [
            {"texto": "Una reparación que hiciste tú mismo/a", "icono": "bi-check2-circle", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Un plato que preparaste desde cero", "icono": "bi-award", "weights": {"gastronomia": 3}},
            {"texto": "Un mueble o estructura que armaste", "icono": "bi-house-check", "weights": {"construccion": 3}},
            {"texto": "Un evento que ayudaste a organizar", "icono": "bi-calendar-event", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q33",
        "pregunta": "¿Qué tipo de noticias te llaman más la atención?",
        "ayuda": "Lo que más te haría detenerte a leer.",
        "opciones": [
            {"texto": "Avances tecnológicos", "icono": "bi-cpu", "weights": {"tecnologia": 3}},
            {"texto": "Nuevos proyectos de construcción en tu ciudad", "icono": "bi-buildings", "weights": {"construccion": 3}},
            {"texto": "Temas de salud y bienestar", "icono": "bi-heart-pulse", "weights": {"salud": 3}},
            {"texto": "Economía y negocios", "icono": "bi-graph-up", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q34",
        "pregunta": "Si tuvieras tu propio canal de redes sociales, ¿de qué tratarían tus videos?",
        "ayuda": "El contenido que te imaginas creando.",
        "opciones": [
            {"texto": "Tips de tecnología", "icono": "bi-phone", "weights": {"tecnologia": 3}},
            {"texto": "Recetas y cocina", "icono": "bi-egg-fried", "weights": {"gastronomia": 3}},
            {"texto": "Tutoriales de reparaciones", "icono": "bi-wrench-adjustable", "weights": {"electricidad": 2, "industrial": 1}},
            {"texto": "Rutinas de cuidado y bienestar", "icono": "bi-flower1", "weights": {"salud": 3}},
        ],
    },
    {
        "id": "q35",
        "pregunta": "¿En cuál de estos lugares te imaginas trabajando en unos años?",
        "ayuda": "Piensa en el ambiente, no en el cargo exacto.",
        "opciones": [
            {"texto": "Un taller o una fábrica", "icono": "bi-gear-wide-connected", "weights": {"industrial": 3}},
            {"texto": "Una obra en construcción", "icono": "bi-cone-striped", "weights": {"construccion": 3}},
            {"texto": "Un colegio o una sala cuna", "icono": "bi-mortarboard", "weights": {"parvulos": 3}},
            {"texto": "Una empresa de tecnología", "icono": "bi-laptop", "weights": {"tecnologia": 3}},
        ],
    },
    {
        "id": "q36",
        "pregunta": "¿Qué actividad harías gratis, solo porque te gusta?",
        "ayuda": "Algo que harías aunque no te pagaran.",
        "opciones": [
            {"texto": "Cocinar para tus amigos o familia", "icono": "bi-cup-hot", "weights": {"gastronomia": 3}},
            {"texto": "Armar o desarmar aparatos", "icono": "bi-cpu", "weights": {"electricidad": 2, "tecnologia": 2}},
            {"texto": "Cuidar niños del barrio o primos chicos", "icono": "bi-balloon-heart", "weights": {"parvulos": 3}},
            {"texto": "Ayudar a organizar las cuentas de la casa", "icono": "bi-wallet2", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q37",
        "pregunta": "¿Qué te da más curiosidad de cómo funciona el mundo?",
        "ayuda": "El misterio cotidiano que más te intriga.",
        "opciones": [
            {"texto": "Cómo se construyen los edificios", "icono": "bi-building", "weights": {"construccion": 3}},
            {"texto": "Cómo funciona internet", "icono": "bi-router", "weights": {"tecnologia": 3}},
            {"texto": "Cómo se preparan los alimentos que comemos", "icono": "bi-basket", "weights": {"gastronomia": 3}},
            {"texto": "Cómo el cuerpo se recupera de una enfermedad", "icono": "bi-heart-pulse", "weights": {"salud": 3}},
        ],
    },
    {
        "id": "q38",
        "pregunta": "Si armaras un equipo de trabajo, ¿qué rol elegirías para ti?",
        "ayuda": "El rol donde te sentirías más útil.",
        "opciones": [
            {"texto": "El/la técnico que resuelve problemas prácticos", "icono": "bi-tools", "weights": {"electricidad": 2, "industrial": 2}},
            {"texto": "El/la que administra el presupuesto", "icono": "bi-cash-coin", "weights": {"administracion": 3}},
            {"texto": "El/la que se encarga de la comida del equipo", "icono": "bi-cup-straw", "weights": {"gastronomia": 3}},
            {"texto": "El/la que cuida el ambiente entre las personas", "icono": "bi-emoji-smile", "weights": {"salud": 1, "parvulos": 2}},
        ],
    },
    {
        "id": "q39",
        "pregunta": "¿Qué olor te trae mejores recuerdos?",
        "ayuda": "A veces un olor dice más que mil palabras.",
        "opciones": [
            {"texto": "El de un taller o aceite de motor", "icono": "bi-droplet-half", "weights": {"industrial": 3}},
            {"texto": "El de pan recién horneado", "icono": "bi-cake", "weights": {"gastronomia": 3}},
            {"texto": "El de una sala llena de niños jugando", "icono": "bi-balloon", "weights": {"parvulos": 3}},
            {"texto": "El de una oficina ordenada con papeles nuevos", "icono": "bi-file-earmark-text", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q40",
        "pregunta": "¿Qué tipo de problema disfrutas más explicándole a otra persona?",
        "ayuda": "Cuando explicas algo, ¿de qué tema te resulta más natural?",
        "opciones": [
            {"texto": "Por qué algo eléctrico no prendía", "icono": "bi-lightbulb", "weights": {"electricidad": 3}},
            {"texto": "Cómo armar algo paso a paso", "icono": "bi-list-ol", "weights": {"construccion": 2, "industrial": 1}},
            {"texto": "Cómo se hace un cálculo o un programa", "icono": "bi-code-square", "weights": {"tecnologia": 3}},
            {"texto": "Cómo cuidar mejor a alguien enfermo", "icono": "bi-bandaid", "weights": {"salud": 3}},
        ],
    },
    {
        "id": "q41",
        "pregunta": "Si te invitaran a un taller de un día, ¿a cuál irías?",
        "ayuda": "El que más te llamaría la atención probar.",
        "opciones": [
            {"texto": "Taller de soldadura o mecánica", "icono": "bi-fire", "weights": {"industrial": 3}},
            {"texto": "Taller de gastronomía", "icono": "bi-egg-fried", "weights": {"gastronomia": 3}},
            {"texto": "Taller de programación de videojuegos", "icono": "bi-joystick", "weights": {"tecnologia": 3}},
            {"texto": "Taller de primeros auxilios con niños", "icono": "bi-bandaid", "weights": {"salud": 2, "parvulos": 2}},
        ],
    },
    {
        "id": "q42",
        "pregunta": "¿Qué te haría sentir más realizado/a un viernes después de trabajar?",
        "ayuda": "Piensa en el cierre de una buena semana.",
        "opciones": [
            {"texto": "Haber arreglado algo que estaba roto", "icono": "bi-check2-circle", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Haber alimentado bien a mucha gente", "icono": "bi-cup-hot", "weights": {"gastronomia": 3}},
            {"texto": "Haber ayudado a alguien que lo necesitaba", "icono": "bi-heart", "weights": {"salud": 3}},
            {"texto": "Haber dejado todo ordenado y al día", "icono": "bi-clipboard-check", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q43",
        "pregunta": "¿Qué tipo de páginas o apps visitas más seguido?",
        "ayuda": "Las que abres sin pensarlo, por costumbre.",
        "opciones": [
            {"texto": "De recetas o cocina", "icono": "bi-journal-bookmark", "weights": {"gastronomia": 3}},
            {"texto": "De tecnología o videojuegos", "icono": "bi-controller", "weights": {"tecnologia": 3}},
            {"texto": "De diseño de casas o decoración", "icono": "bi-house-heart", "weights": {"construccion": 3}},
            {"texto": "De bienestar o ejercicio", "icono": "bi-heart-pulse", "weights": {"salud": 3}},
        ],
    },
    {
        "id": "q44",
        "pregunta": "Si tuvieras que cuidar algo por un día, ¿qué elegirías?",
        "ayuda": "Piensa en la responsabilidad que te acomodaría más.",
        "opciones": [
            {"texto": "Un bebé o mascota de la familia", "icono": "bi-balloon-heart", "weights": {"parvulos": 2, "salud": 1}},
            {"texto": "Una máquina o vehículo", "icono": "bi-car-front", "weights": {"industrial": 3}},
            {"texto": "Un pequeño negocio", "icono": "bi-shop", "weights": {"administracion": 3}},
            {"texto": "Una obra en construcción cercana", "icono": "bi-cone-striped", "weights": {"construccion": 3}},
        ],
    },
    {
        "id": "q45",
        "pregunta": "¿Qué tipo de desafío te gustaría superar?",
        "ayuda": "El logro que más satisfacción te daría.",
        "opciones": [
            {"texto": "Arreglar algo que nadie más pudo", "icono": "bi-trophy", "weights": {"electricidad": 2, "industrial": 2}},
            {"texto": "Cocinar para muchas personas sin equivocarte", "icono": "bi-cup-straw", "weights": {"gastronomia": 3}},
            {"texto": "Aprender un programa nuevo muy rápido", "icono": "bi-lightning-charge", "weights": {"tecnologia": 3}},
            {"texto": "Cuidar a varios niños a la vez", "icono": "bi-people", "weights": {"parvulos": 3}},
        ],
    },
    {
        "id": "q46",
        "pregunta": "¿Cuál de estas frases te representa más?",
        "ayuda": "Elige la que sientas más cercana a ti.",
        "opciones": [
            {"texto": "\"Me gusta que las cosas funcionen bien\"", "icono": "bi-gear", "weights": {"electricidad": 2, "industrial": 2}},
            {"texto": "\"Me gusta que todo esté ordenado\"", "icono": "bi-list-check", "weights": {"administracion": 3}},
            {"texto": "\"Me gusta que la gente se sienta bien\"", "icono": "bi-emoji-heart-eyes", "weights": {"salud": 2, "parvulos": 2}},
            {"texto": "\"Me gusta crear cosas ricas o bonitas\"", "icono": "bi-palette", "weights": {"gastronomia": 2, "construccion": 2}},
        ],
    },
    {
        "id": "q47",
        "pregunta": "¿Qué te gustaría aprender a construir?",
        "ayuda": "Algo que te encantaría poder hacer con tus manos.",
        "opciones": [
            {"texto": "Un mueble de madera", "icono": "bi-hammer", "weights": {"construccion": 3}},
            {"texto": "Un circuito o robot simple", "icono": "bi-cpu", "weights": {"electricidad": 2, "tecnologia": 2}},
            {"texto": "Un plato elaborado", "icono": "bi-award", "weights": {"gastronomia": 3}},
            {"texto": "Nada, prefiero coordinar quién lo hace", "icono": "bi-clipboard-check", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q48",
        "pregunta": "¿En qué actividad del colegio te sientes más cómodo/a?",
        "ayuda": "Donde el tiempo se te pasa más rápido.",
        "opciones": [
            {"texto": "En el taller de tecnología", "icono": "bi-cpu", "weights": {"tecnologia": 2, "electricidad": 1}},
            {"texto": "En actividades de cuidado grupal", "icono": "bi-people", "weights": {"parvulos": 2, "salud": 1}},
            {"texto": "En organizar el curso o sus actividades", "icono": "bi-kanban", "weights": {"administracion": 3}},
            {"texto": "En ferias de comida o eventos", "icono": "bi-cup-hot", "weights": {"gastronomia": 3}},
        ],
    },
    {
        "id": "q49",
        "pregunta": "¿Qué te gustaría que pasara en tu práctica profesional ideal?",
        "ayuda": "Imagina tu primer acercamiento real al mundo laboral.",
        "opciones": [
            {"texto": "Reparar o mantener equipos reales", "icono": "bi-tools", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Preparar comida para clientes reales", "icono": "bi-egg-fried", "weights": {"gastronomia": 3}},
            {"texto": "Trabajar directo con niños o pacientes", "icono": "bi-heart", "weights": {"parvulos": 2, "salud": 2}},
            {"texto": "Llevar la administración de una oficina", "icono": "bi-briefcase", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q50",
        "pregunta": "Para cerrar: si solo pudieras probar UN taller gratis, ¿cuál sería?",
        "ayuda": "Última pregunta, elige con el corazón.",
        "opciones": [
            {"texto": "Mecánica o electricidad", "icono": "bi-gear-wide-connected", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Gastronomía", "icono": "bi-cup-hot", "weights": {"gastronomia": 3}},
            {"texto": "Tecnología o programación", "icono": "bi-laptop", "weights": {"tecnologia": 3}},
            {"texto": "Atención de párvulos o enfermería", "icono": "bi-heart-pulse", "weights": {"parvulos": 2, "salud": 2}},
        ],
    },
]

# Cantidad de preguntas que se muestran en cada intento del quiz. Se elige
# una muestra aleatoria de este tamaño desde QUESTIONS (banco de 50), y se
# baraja el orden de las alternativas de cada una, para que el test se
# sienta distinto cada vez que alguien lo responde.
PREGUNTAS_POR_INTENTO = 10