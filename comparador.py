{% extends "base.html" %}

{% block content %}
<section class="container py-5">

  <div class="text-center mb-5">
    <span class="am-hero-badge"><i class="bi bi-bar-chart-line"></i> Comparador</span>
    <h1 class="am-section-title">Compara dos liceos lado a lado</h1>
    <p class="text-muted-soft">Elige dos establecimientos para ver sus diferencias de un vistazo.</p>
  </div>

  <div class="row g-3 justify-content-center mb-5" style="max-width: 720px; margin-inline:auto;">
    <div class="col-md-6">
      <label class="form-label small fw-semibold">Liceo A</label>
      <select id="comparar-select-a" class="form-select rounded-3">
        <option value="">Selecciona un liceo...</option>
        {% for l in todos %}
          <option value="{{ l.id }}" {{ 'selected' if liceo_a and liceo_a.id == l.id }}>{{ l.nombre }} — {{ l.comuna }}</option>
        {% endfor %}
      </select>
    </div>
    <div class="col-md-6">
      <label class="form-label small fw-semibold">Liceo B</label>
      <select id="comparar-select-b" class="form-select rounded-3">
        <option value="">Selecciona un liceo...</option>
        {% for l in todos %}
          <option value="{{ l.id }}" {{ 'selected' if liceo_b and liceo_b.id == l.id }}>{{ l.nombre }} — {{ l.comuna }}</option>
        {% endfor %}
      </select>
    </div>
  </div>

  {% if liceo_a and liceo_b %}
  <div class="am-card p-0 overflow-hidden">
    <table class="table am-compare-table mb-0">
      <thead>
        <tr>
          <th style="width: 26%;">Característica</th>
          <th class="text-center">{{ liceo_a.nombre }}</th>
          <th class="text-center">{{ liceo_b.nombre }}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="fw-semibold">Comuna</td>
          <td class="text-center">{{ liceo_a.comuna }}</td>
          <td class="text-center">{{ liceo_b.comuna }}</td>
        </tr>
        <tr>
          <td class="fw-semibold">Dirección</td>
          <td class="text-center small">{{ liceo_a.direccion }}</td>
          <td class="text-center small">{{ liceo_b.direccion }}</td>
        </tr>
        <tr>
          <td class="fw-semibold">Especialidades</td>
          <td class="text-center small">{{ liceo_a.especialidades.replace(',', ', ') }}</td>
          <td class="text-center small">{{ liceo_b.especialidades.replace(',', ', ') }}</td>
        </tr>
        <tr>
          <td class="fw-semibold">Jornada</td>
          <td class="text-center">{{ liceo_a.jornada }}</td>
          <td class="text-center">{{ liceo_b.jornada }}</td>
        </tr>
        <tr>
          <td class="fw-semibold">Tipo de dependencia</td>
          <td class="text-center">{{ liceo_a.tipo }}</td>
          <td class="text-center">{{ liceo_b.tipo }}</td>
        </tr>
        <tr>
          <td class="fw-semibold">Costo</td>
          <td class="text-center">{{ 'Gratuito' if liceo_a.gratuito else 'Con arancel' }}</td>
          <td class="text-center">{{ 'Gratuito' if liceo_b.gratuito else 'Con arancel' }}</td>
        </tr>
        <tr>
          <td class="fw-semibold">Calificación</td>
          <td class="text-center"><span class="am-rating"><i class="bi bi-star-fill"></i> {{ liceo_a.rating }}</span></td>
          <td class="text-center"><span class="am-rating"><i class="bi bi-star-fill"></i> {{ liceo_b.rating }}</span></td>
        </tr>
        <tr>
          <td class="fw-semibold">Tasa de admisión</td>
          <td class="text-center">{{ liceo_a.admision_pct }}%</td>
          <td class="text-center">{{ liceo_b.admision_pct }}%</td>
        </tr>
        <tr>
          <td class="fw-semibold">Empleabilidad estimada</td>
          <td class="text-center">{{ liceo_a.empleabilidad_pct }}%</td>
          <td class="text-center">{{ liceo_b.empleabilidad_pct }}%</td>
        </tr>
        <tr>
          <td class="fw-semibold">Matrícula aproximada</td>
          <td class="text-center">{{ liceo_a.matricula | miles }}</td>
          <td class="text-center">{{ liceo_b.matricula | miles }}</td>
        </tr>
        <tr>
          <td class="fw-semibold">Estado del dato</td>
          <td class="text-center">
            <span class="badge {{ 'bg-success' if liceo_a.verificado else 'bg-warning text-dark' }}">
              {{ 'Verificado' if liceo_a.verificado else 'Demostración' }}
            </span>
          </td>
          <td class="text-center">
            <span class="badge {{ 'bg-success' if liceo_b.verificado else 'bg-warning text-dark' }}">
              {{ 'Verificado' if liceo_b.verificado else 'Demostración' }}
            </span>
          </td>
        </tr>
        <tr>
          <td></td>
          <td class="text-center py-3"><a href="{{ url_for('liceos.detalle_liceo', liceo_id=liceo_a.id) }}" class="btn-am-outline btn-sm">Ver perfil completo</a></td>
          <td class="text-center py-3"><a href="{{ url_for('liceos.detalle_liceo', liceo_id=liceo_b.id) }}" class="btn-am-outline btn-sm">Ver perfil completo</a></td>
        </tr>
      </tbody>
    </table>
  </div>
  {% else %}
  <div class="am-card p-5 text-center">
    <i class="bi bi-arrow-up-circle fs-1 text-am-primary mb-3 d-block"></i>
    <p class="text-muted-soft mb-0">Selecciona dos liceos arriba para ver la comparación.</p>
  </div>
  {% endif %}

</section>
{% endblock %}
