# -*- coding: utf-8 -*-
"""
Banco de preguntas del Diagnóstico Vocacional Avanzado.

A diferencia del test rápido (services/quiz_data.py, 50 preguntas al azar,
pensado para ser lúdico y tomar ~3 minutos), este cuestionario es fijo,
más extenso y deliberadamente más riguroso: combina una escala de
autoevaluación, escenarios de decisión con matices, y preguntas abiertas
de reflexión personal. Está pensado para quienes ya probaron el test
rápido y quieren un perfil más completo antes de postular.

Estructura:
  - AUTOEVALUACION: 8 afirmaciones (una por área), escala 1 a 5.
  - ESCENARIOS: 5 situaciones de decisión con 4 alternativas cada una.
  - PREGUNTAS_ABIERTAS: 4 preguntas de reflexión personal, sin puntaje
    automático — se muestran tal cual en el diagnóstico final como parte
    del perfil cualitativo de la persona.
"""

AUTOEVALUACION = [
    {
        "id": "auto_electricidad",
        "texto": "Disfruto entender cómo funcionan los aparatos electrónicos y las instalaciones eléctricas.",
        "area": "electricidad",
    },
    {
        "id": "auto_industrial",
        "texto": "Me siento cómodo/a trabajando con herramientas, motores o maquinaria.",
        "area": "industrial",
    },
    {
        "id": "auto_salud",
        "texto": "Me atrae la idea de cuidar la salud y el bienestar de otras personas.",
        "area": "salud",
    },
    {
        "id": "auto_gastronomia",
        "texto": "Disfruto preparar comida y pensar en experiencias gastronómicas.",
        "area": "gastronomia",
    },
    {
        "id": "auto_administracion",
        "texto": "Me resulta natural organizar tareas, presupuestos o información.",
        "area": "administracion",
    },
    {
        "id": "auto_construccion",
        "texto": "Me interesa cómo se diseñan y construyen espacios y edificaciones.",
        "area": "construccion",
    },
    {
        "id": "auto_tecnologia",
        "texto": "Me entusiasma programar, usar software o resolver problemas con tecnología.",
        "area": "tecnologia",
    },
    {
        "id": "auto_parvulos",
        "texto": "Disfruto acompañar, cuidar y estimular el aprendizaje de niños y niñas pequeños.",
        "area": "parvulos",
    },
]

OPCIONES_LIKERT = [
    {"valor": 1, "texto": "Muy en desacuerdo"},
    {"valor": 2, "texto": "En desacuerdo"},
    {"valor": 3, "texto": "Neutral"},
    {"valor": 4, "texto": "De acuerdo"},
    {"valor": 5, "texto": "Muy de acuerdo"},
]

ESCENARIOS = [
    {
        "id": "esc_1",
        "texto": "Te ofrecen 4 prácticas de una semana y debes elegir solo una. ¿Cuál eliges?",
        "opciones": [
            {"letra": "a", "texto": "Apoyar la mantención eléctrica de un edificio", "area": "electricidad"},
            {"letra": "b", "texto": "Apoyar la administración de bodega e inventario de una empresa", "area": "administracion"},
            {"letra": "c", "texto": "Ayudar en la cocina de un casino escolar", "area": "gastronomia"},
            {"letra": "d", "texto": "Acompañar a un equipo de enfermería en una posta", "area": "salud"},
        ],
    },
    {
        "id": "esc_2",
        "texto": "Un profesor te pide elegir un proyecto semestral. ¿Cuál elegirías?",
        "opciones": [
            {"letra": "a", "texto": "Diseñar y construir la maqueta de una vivienda social", "area": "construccion"},
            {"letra": "b", "texto": "Desarrollar una aplicación o página web simple", "area": "tecnologia"},
            {"letra": "c", "texto": "Organizar una feria de emprendimiento del colegio", "area": "administracion"},
            {"letra": "d", "texto": "Planificar una actividad de cuidado infantil con un jardín cercano", "area": "parvulos"},
        ],
    },
    {
        "id": "esc_3",
        "texto": "Se forma un equipo de proyecto y debes elegir tu rol. ¿Cuál tomarías?",
        "opciones": [
            {"letra": "a", "texto": "El que revisa y ajusta las máquinas o vehículos del equipo", "area": "industrial"},
            {"letra": "b", "texto": "El que prepara la comida para todo el grupo", "area": "gastronomia"},
            {"letra": "c", "texto": "El que se encarga del cuidado de los más pequeños del grupo", "area": "parvulos"},
            {"letra": "d", "texto": "El que atiende cualquier imprevisto de salud del equipo", "area": "salud"},
        ],
    },
    {
        "id": "esc_4",
        "texto": "Tienes que elegir un curso de verano de solo una semana. ¿Cuál eliges?",
        "opciones": [
            {"letra": "a", "texto": "Mecánica básica de motores", "area": "industrial"},
            {"letra": "b", "texto": "Dibujo técnico y construcción", "area": "construccion"},
            {"letra": "c", "texto": "Programación para principiantes", "area": "tecnologia"},
            {"letra": "d", "texto": "Gestión de un pequeño negocio", "area": "administracion"},
        ],
    },
    {
        "id": "esc_5",
        "texto": "Piensa en tu día a día ideal dentro de 3 años. ¿Cuál se parece más?",
        "opciones": [
            {"letra": "a", "texto": "Trabajando con instalaciones eléctricas o electrónica", "area": "electricidad"},
            {"letra": "b", "texto": "Cuidando y atendiendo directamente a personas", "area": "salud"},
            {"letra": "c", "texto": "En una cocina, produciendo alimentos", "area": "gastronomia"},
            {"letra": "d", "texto": "Frente a un computador, resolviendo problemas técnicos", "area": "tecnologia"},
        ],
    },
]

PREGUNTAS_ABIERTAS = [
    {
        "id": "abierta_1",
        "texto": "Cuenta sobre un momento en que resolviste un problema práctico (arreglaste algo, ayudaste a alguien, organizaste bien una tarea). ¿Qué pasó y cómo te sentiste?",
        "placeholder": "Puede ser algo pequeño del día a día, no tiene que ser grandioso...",
    },
    {
        "id": "abierta_2",
        "texto": "¿Qué actividad te hace perder la noción del tiempo, sin darte cuenta de que pasaron varias horas?",
        "placeholder": "Piensa en algo que haces por gusto, dentro o fuera del colegio...",
    },
    {
        "id": "abierta_3",
        "texto": "¿Dónde te imaginas trabajando en 5 años? Descríbelo con tus palabras: el lugar, con quién, haciendo qué.",
        "placeholder": "No hay que tener certeza, solo cuenta cómo te lo imaginas hoy...",
    },
    {
        "id": "abierta_4",
        "texto": "¿Hay algo que te preocupe o te genere dudas sobre elegir una especialidad técnico-profesional?",
        "placeholder": "Puedes contarlo con toda confianza, esto es solo para ti...",
    },
]
