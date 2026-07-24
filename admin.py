{% extends "base.html" %}

{% block meta_description %}Responde el test vocacional de AcademyMap y descubre qué liceo técnico-profesional se adapta mejor a tus intereses.{% endblock %}

{% block content %}
<section class="container py-5" style="max-width: 720px;">

  <div class="text-center mb-4">
    <span class="am-hero-badge"><i class="bi bi-clipboard2-check"></i> Test vocacional</span>
    <h1 class="am-section-title">¿Qué área técnica va contigo?</h1>
    <p class="text-muted-soft">Elige la opción que más se parezca a ti en cada pregunta. No hay respuestas incorrectas.</p>
  </div>

  <div class="mb-4">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <span id="quiz-progress-label" class="small fw-semibold text-am-primary">Pregunta 1 de {{ preguntas|length }}</span>
    </div>
    <div class="am-quiz-progress">
      <div id="quiz-progress-bar" class="am-quiz-progress-bar" style="width: {{ (100/preguntas|length)|round(0,'floor') }}%;"></div>
    </div>
  </div>

  <form id="quiz-form" method="POST" action="{{ url_for('quiz.resultados') }}">
    {% for pregunta in preguntas %}
    <div class="am-quiz-step {{ 'active' if loop.first }}">
      <div class="am-card-soft p-4 p-md-5">
        <h3 class="mb-1">{{ pregunta.pregunta }}</h3>
        <p class="text-muted-soft small mb-4">{{ pregunta.ayuda }}</p>

        {% for opcion in pregunta.opciones %}
        <label class="am-option">
          <input type="radio" name="{{ pregunta.id }}" value="{{ loop.index0 }}" class="d-none" required>
          {{ opcion.texto }}
        </label>
        {% endfor %}
      </div>
    </div>
    {% endfor %}

    <div class="d-flex justify-content-between mt-4">
      <button type="button" id="quiz-btn-atras" class="btn-am-outline">
        <i class="bi bi-arrow-left me-1"></i> Atrás
      </button>
      <div>
        <button type="button" id="quiz-btn-siguiente" class="btn-am-primary">
          Siguiente <i class="bi bi-arrow-right ms-1"></i>
        </button>
        <button type="submit" id="quiz-btn-enviar" class="btn-am-primary d-none">
          Ver mis resultados <i class="bi bi-check2-circle ms-1"></i>
        </button>
      </div>
    </div>
  </form>
</section>
{% endblock %}
