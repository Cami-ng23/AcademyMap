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
]

# Cantidad de preguntas que se muestran en cada intento del quiz. Se elige
# una muestra aleatoria de este tamaño desde QUESTIONS (banco de 20), y se
# baraja el orden de las alternativas de cada una, para que el test se
# sienta distinto cada vez que alguien lo responde.
PREGUNTAS_POR_INTENTO = 10