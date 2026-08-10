// =============================================================================
// AcademyMap — script.js
// Comportamiento del navbar, menú móvil y del test vocacional paso a paso.
// =============================================================================

document.addEventListener("DOMContentLoaded", function () {
  // --- Navbar: efecto "glass" al hacer scroll ------------------------------
  const navbar = document.querySelector(".am-navbar");
  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll);
  }

  // --- Menú móvil ------------------------------------------------------------
  const toggleBtn = document.getElementById("am-menu-toggle");
  const mobileMenu = document.getElementById("am-mobile-menu");
  if (toggleBtn && mobileMenu) {
    toggleBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("d-none");
    });
  }

  // --- Alertas: auto-cierre suave --------------------------------------------
  document.querySelectorAll(".alert.alert-dismissible").forEach((alerta) => {
    setTimeout(() => {
      alerta.classList.add("fade");
      alerta.classList.remove("show");
    }, 5000);
  });

  initQuiz();
  initComparador();
});

// =============================================================================
// Test vocacional: navegación paso a paso, barra de progreso y validación.
// =============================================================================
function initQuiz() {
  const quizForm = document.getElementById("quiz-form");
  if (!quizForm) return;

  const steps = Array.from(quizForm.querySelectorAll(".am-quiz-step"));
  const progressBar = document.getElementById("quiz-progress-bar");
  const progressLabel = document.getElementById("quiz-progress-label");
  const btnAtras = document.getElementById("quiz-btn-atras");
  const btnSiguiente = document.getElementById("quiz-btn-siguiente");
  const btnEnviar = document.getElementById("quiz-btn-enviar");

  let indiceActual = 0;

  function actualizarVista() {
    steps.forEach((paso, i) => paso.classList.toggle("active", i === indiceActual));

    const porcentaje = Math.round(((indiceActual + 1) / steps.length) * 100);
    if (progressBar) progressBar.style.width = porcentaje + "%";
    if (progressLabel) progressLabel.textContent = `Pregunta ${indiceActual + 1} de ${steps.length}`;

    if (btnAtras) btnAtras.style.visibility = indiceActual === 0 ? "hidden" : "visible";
    if (btnSiguiente) btnSiguiente.classList.toggle("d-none", indiceActual === steps.length - 1);
    if (btnEnviar) btnEnviar.classList.toggle("d-none", indiceActual !== steps.length - 1);
  }

  function pasoRespondido(paso) {
    return paso.querySelector('input[type="radio"]:checked') !== null;
  }

  // Selección de alternativa: resalta la opción y avanza automáticamente.
  // IMPORTANTE: se escucha "change" en el input (no "click" en el label),
  // porque un <label> que envuelve un <input> reenvía el clic de forma
  // nativa hacia el input, disparando el evento dos veces si se escucha
  // "click" en el label — eso hacía que el quiz saltara una pregunta sin
  // responderla y luego marcara "faltan preguntas" por responder.
  quizForm.querySelectorAll(".am-quiz-step").forEach((paso) => {
    paso.querySelectorAll(".am-option-input").forEach((input) => {
      input.addEventListener("change", () => {
        const opcion = input.closest(".am-option");

        paso.querySelectorAll(".am-option").forEach((o) => o.classList.remove("selected"));
        opcion.classList.add("selected");

        // Avanza automáticamente tras una breve pausa (mejor UX en celular).
        setTimeout(() => {
          if (indiceActual < steps.length - 1) {
            indiceActual++;
            actualizarVista();
          }
        }, 280);
      });
    });
  });

  if (btnSiguiente) {
    btnSiguiente.addEventListener("click", () => {
      if (!pasoRespondido(steps[indiceActual])) {
        steps[indiceActual].classList.add("shake");
        setTimeout(() => steps[indiceActual].classList.remove("shake"), 400);
        return;
      }
      indiceActual = Math.min(indiceActual + 1, steps.length - 1);
      actualizarVista();
    });
  }

  if (btnAtras) {
    btnAtras.addEventListener("click", () => {
      indiceActual = Math.max(indiceActual - 1, 0);
      actualizarVista();
    });
  }

  quizForm.addEventListener("submit", (evento) => {
    const faltante = steps.some((paso) => !pasoRespondido(paso));
    if (faltante) {
      evento.preventDefault();
      alert("Por favor responde todas las preguntas antes de continuar.");
    } else if (btnEnviar) {
      btnEnviar.disabled = true;
      btnEnviar.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Calculando...';
    }
  });

  actualizarVista();
}

// =============================================================================
// Comparador: al elegir un liceo en los selects, recarga con los parámetros.
// =============================================================================
function initComparador() {
  const selectA = document.getElementById("comparar-select-a");
  const selectB = document.getElementById("comparar-select-b");
  if (!selectA || !selectB) return;

  function actualizarUrl() {
    const params = new URLSearchParams(window.location.search);
    if (selectA.value) params.set("a", selectA.value); else params.delete("a");
    if (selectB.value) params.set("b", selectB.value); else params.delete("b");
    window.location.search = params.toString();
  }

  selectA.addEventListener("change", actualizarUrl);
  selectB.addEventListener("change", actualizarUrl);
}
