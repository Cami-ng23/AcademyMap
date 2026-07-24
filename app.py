{# Formulario compartido entre agregar.html y editar.html.
   Espera: `liceo` (None al agregar), `areas`, `comunas` #}

<div class="row g-4">
  <div class="col-md-8">
    <div class="am-card p-4 mb-4">
      <h6 class="fw-bold mb-3">Información general</h6>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Nombre del liceo</label>
        <input type="text" name="nombre" class="form-control rounded-3" required
               value="{{ liceo.nombre if liceo else '' }}">
      </div>
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label small fw-semibold">Comuna</label>
          <select name="comuna" class="form-select rounded-3" required>
            {% for c in comunas %}
              <option value="{{ c }}" {{ 'selected' if liceo and liceo.comuna == c }}>{{ c }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-6">
          <label class="form-label small fw-semibold">Dirección</label>
          <input type="text" name="direccion" class="form-control rounded-3" required
                 value="{{ liceo.direccion if liceo else '' }}">
        </div>
      </div>
      <div class="mt-3">
        <label class="form-label small fw-semibold">Descripción / historia</label>
        <textarea name="descripcion" class="form-control rounded-3" rows="4" required>{{ liceo.descripcion if liceo else '' }}</textarea>
      </div>
    </div>

    <div class="am-card p-4 mb-4">
      <h6 class="fw-bold mb-3">Oferta formativa</h6>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Especialidades <span class="text-muted-soft fw-normal">(separadas por coma)</span></label>
        <input type="text" name="especialidades" class="form-control rounded-3" required
               placeholder="Electricidad, Electrónica, Mecánica"
               value="{{ liceo.especialidades if liceo else '' }}">
      </div>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Áreas vocacionales</label>
        <div class="row g-2">
          {% set areas_liceo = liceo.lista_areas if liceo else [] %}
          {% for id, info in areas.items() %}
          <div class="col-6 col-md-4">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" name="areas" value="{{ id }}" id="area-{{ id }}"
                     {{ 'checked' if id in areas_liceo }}>
              <label class="form-check-label small" for="area-{{ id }}">{{ info.nombre }}</label>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
      <div>
        <label class="form-label small fw-semibold">Características destacadas <span class="text-muted-soft fw-normal">(separadas por coma)</span></label>
        <input type="text" name="caracteristicas" class="form-control rounded-3"
               placeholder="Laboratorios equipados, Práctica profesional garantizada"
               value="{{ liceo.caracteristicas if liceo else '' }}">
      </div>
    </div>
  </div>

  <div class="col-md-4">
    <div class="am-card p-4 mb-4">
      <h6 class="fw-bold mb-3">Detalles administrativos</h6>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Tipo de dependencia</label>
        <select name="tipo" class="form-select rounded-3">
          {% for t in ["Municipal", "Particular Subvencionado", "Servicio Local de Educación"] %}
            <option value="{{ t }}" {{ 'selected' if liceo and liceo.tipo == t }}>{{ t }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Jornada</label>
        <select name="jornada" class="form-select rounded-3">
          {% for j in ["Diurna", "Vespertina", "Diurna y Vespertina"] %}
            <option value="{{ j }}" {{ 'selected' if liceo and liceo.jornada == j }}>{{ j }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Contacto</label>
        <input type="text" name="contacto" class="form-control rounded-3"
               value="{{ liceo.contacto if liceo else '' }}">
      </div>
      <div class="form-check mb-2">
        <input class="form-check-input" type="checkbox" name="gratuito" id="gratuito"
               {{ 'checked' if not liceo or liceo.gratuito }}>
        <label class="form-check-label small" for="gratuito">Gratuito</label>
      </div>
      <div class="form-check">
        <input class="form-check-input" type="checkbox" name="verificado" id="verificado"
               {{ 'checked' if liceo and liceo.verificado }}>
        <label class="form-check-label small" for="verificado">Información verificada</label>
      </div>
    </div>

    <div class="am-card p-4 mb-4">
      <h6 class="fw-bold mb-3">Estadísticas</h6>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Matrícula aproximada</label>
        <input type="number" name="matricula" class="form-control rounded-3" min="0"
               value="{{ liceo.matricula if liceo else 0 }}">
      </div>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Calificación (0 a 5)</label>
        <input type="number" step="0.1" min="0" max="5" name="rating" class="form-control rounded-3"
               value="{{ liceo.rating if liceo else 4.0 }}">
      </div>
      <div class="mb-3">
        <label class="form-label small fw-semibold">Tasa de admisión (%)</label>
        <input type="number" min="0" max="100" name="admision_pct" class="form-control rounded-3"
               value="{{ liceo.admision_pct if liceo else 60 }}">
      </div>
      <div>
        <label class="form-label small fw-semibold">Empleabilidad estimada (%)</label>
        <input type="number" min="0" max="100" name="empleabilidad_pct" class="form-control rounded-3"
               value="{{ liceo.empleabilidad_pct if liceo else 75 }}">
      </div>
    </div>

    <button type="submit" class="btn-am-primary w-100">
      <i class="bi bi-check2-circle me-1"></i> {{ 'Guardar cambios' if liceo else 'Crear liceo' }}
    </button>
  </div>
</div>
