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

# 6 preguntas, 4 alternativas cada una. Los "pesos" indican cuántos puntos
# suma cada alternativa a cada área vocacional.
QUESTIONS = [
    {
        "id": "q1",
        "pregunta": "¿Qué actividad disfrutas más en tu tiempo libre?",
        "ayuda": "Elige la que más se acerca a ti.",
        "opciones": [
            {"texto": "Armar o reparar cosas", "weights": {"industrial": 3, "construccion": 2, "electricidad": 1}},
            {"texto": "Usar el computador y crear", "weights": {"tecnologia": 3, "administracion": 1}},
            {"texto": "Cocinar o compartir con gente", "weights": {"gastronomia": 3, "salud": 1}},
            {"texto": "Cuidar y jugar con niños pequeños", "weights": {"parvulos": 3, "salud": 1}},
        ],
    },
    {
        "id": "q2",
        "pregunta": "¿Cuál de estas materias se te da mejor?",
        "ayuda": "Piensa en dónde te sientes con más confianza.",
        "opciones": [
            {"texto": "Matemáticas y lógica", "weights": {"tecnologia": 2, "electricidad": 2, "administracion": 1}},
            {"texto": "Ciencias naturales y biología", "weights": {"salud": 3, "parvulos": 1}},
            {"texto": "Tecnología y talleres", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Lenguaje y trabajo en equipo", "weights": {"administracion": 2, "gastronomia": 1, "salud": 1}},
        ],
    },
    {
        "id": "q3",
        "pregunta": "¿Cómo te gustaría que fuera tu trabajo ideal?",
        "ayuda": "Imagina cómo sería tu día a día.",
        "opciones": [
            {"texto": "Frente a una pantalla resolviendo problemas", "weights": {"tecnologia": 3, "administracion": 1}},
            {"texto": "En terreno, usando herramientas", "weights": {"industrial": 2, "construccion": 2, "electricidad": 1}},
            {"texto": "Ayudando y cuidando a otras personas", "weights": {"salud": 3, "parvulos": 2}},
            {"texto": "En una cocina o atendiendo público", "weights": {"gastronomia": 3, "administracion": 1}},
        ],
    },
    {
        "id": "q4",
        "pregunta": "¿Qué habilidad crees que es tu punto fuerte?",
        "ayuda": "No hay respuestas incorrectas.",
        "opciones": [
            {"texto": "Ser ordenado y planificar", "weights": {"administracion": 3, "construccion": 1}},
            {"texto": "Ser creativo con las manos", "weights": {"gastronomia": 2, "industrial": 1, "construccion": 1}},
            {"texto": "Entender cómo funcionan las máquinas", "weights": {"electricidad": 2, "industrial": 2}},
            {"texto": "Aprender tecnología rápidamente", "weights": {"tecnologia": 3}},
        ],
    },
    {
        "id": "q5",
        "pregunta": "¿Qué proyecto te emocionaría más realizar?",
        "ayuda": "Elige el que te haría decir '¡quiero hacer eso!'.",
        "opciones": [
            {"texto": "Crear una app o reparar un equipo electrónico", "weights": {"tecnologia": 2, "electricidad": 2}},
            {"texto": "Diseñar o construir algo con tus manos", "weights": {"construccion": 3, "industrial": 1}},
            {"texto": "Preparar un banquete para un evento", "weights": {"gastronomia": 3}},
            {"texto": "Organizar las finanzas de un pequeño negocio", "weights": {"administracion": 3}},
        ],
    },
    {
        "id": "q6",
        "pregunta": "¿En qué tipo de ambiente rindes mejor?",
        "ayuda": "Piensa en dónde te concentras y disfrutas.",
        "opciones": [
            {"texto": "Una posta, clínica o sala cuna", "weights": {"salud": 2, "parvulos": 2}},
            {"texto": "Un taller con máquinas y herramientas", "weights": {"industrial": 2, "electricidad": 2}},
            {"texto": "Una oficina organizada", "weights": {"administracion": 3}},
            {"texto": "Una cocina o un casino escolar", "weights": {"gastronomia": 3}},
        ],
    },
]
