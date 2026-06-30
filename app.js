(function () {
  "use strict";

  const STORAGE_KEY = "aspi-quiz-progress";
  const MAX_HEARTS = 3;
  const TIME_PER_QUESTION = 15;
  const XP_CORRECT = 10;
  const XP_BONUS_STREAK = 5;
  const LETTERS = ["A", "B", "C", "D"];

  let data = null;
  let progress = loadProgress();

  let currentCatalog = null;
  let questions = [];
  let currentIndex = 0;
  let hearts = MAX_HEARTS;
  let streak = 0;
  let bestStreak = 0;
  let correctCount = 0;
  let sessionXP = 0;
  let answered = false;
  let timerInterval = null;
  let timeLeft = TIME_PER_QUESTION;

  const $ = (sel) => document.querySelector(sel);

  const screens = {
    loading: $("#screen-loading"),
    home: $("#screen-home"),
    quiz: $("#screen-quiz"),
    results: $("#screen-results"),
  };

  function loadProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { totalXP: 0, bestStreak: 0, catalogs: {} };
    } catch {
      return { totalXP: 0, bestStreak: 0, catalogs: {} };
    }
  }

  function saveProgress() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    updateGlobalStats();
  }

  function showScreen(name) {
    Object.values(screens).forEach((el) => el.classList.add("hidden"));
    screens[name].classList.remove("hidden");
  }

  function updateGlobalStats() {
    $("#total-xp").textContent = progress.totalXP;
    $("#best-streak").textContent = progress.bestStreak;

    const homeXp = $("#home-total-xp");
    const homeStreak = $("#home-best-streak");
    const homeCatalogs = $("#home-catalogs-done");
    if (homeXp) homeXp.textContent = progress.totalXP;
    if (homeStreak) homeStreak.textContent = progress.bestStreak;
    if (homeCatalogs && data) {
      const started = data.catalogos.filter((c) => progress.catalogs[c.id]).length;
      homeCatalogs.textContent = started;
    }
  }

  const HOME_SECTIONS = [
    {
      id: "seccion-cafe",
      titulo: "Mc Café",
      subtitulo: "Temperaturas, almacenamiento y estándares de bebidas",
      icono: "☕",
      filtro: (cat) => cat.seccion === "cafe",
    },
    {
      id: "seccion-operaciones",
      titulo: "Operaciones",
      subtitulo: "Cocina, servicio, limpieza y áreas del restaurante",
      icono: "🍔",
      filtro: (cat) => cat.seccion === "operaciones",
    },
    {
      id: "seccion-equipo",
      titulo: "Aspi Couch — Repaso total",
      subtitulo: "Practica preguntas de Mc Café, Cocina, Servicio y todas las áreas",
      icono: "🛋️",
      filtro: (cat) => cat.seccion === "equipo",
    },
  ];

  function createCatalogCard(cat) {
    const pct = getCatalogProgress(cat.id);
    const count = cat.preguntas ? cat.preguntas.length : 0;
    const card = document.createElement("button");
    card.type = "button";
    card.className = "catalog-card";
    card.style.setProperty("--cat-color", cat.color);
    card.innerHTML = `
      <span class="cat-icon">${cat.icono}</span>
      <h3>${cat.nombre}</h3>
      <p class="cat-desc">${cat.descripcion || ""}</p>
      <span class="cat-count">${count} preguntas</span>
      <div class="progress-ring" role="progressbar" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100">
        <div class="progress-fill" style="width:${pct}%"></div>
      </div>
      <span class="cat-progress-label">${pct}% completado</span>
    `;
    card.addEventListener("click", () => startQuiz(cat));
    return card;
  }

  function renderCatalogs() {
    const container = $("#home-sections");
    if (!container) return;
    container.innerHTML = "";

    HOME_SECTIONS.forEach((section) => {
      const catalogs = data.catalogos.filter(section.filtro);
      if (!catalogs.length) return;

      const block = document.createElement("section");
      block.className = "home-section card-glass";
      block.id = section.id;

      block.innerHTML = `
        <header class="section-header">
          <div class="section-header__icon">${section.icono}</div>
          <div>
            <h2>${section.titulo}</h2>
            <p>${section.subtitulo}</p>
          </div>
        </header>
        <div class="catalog-grid"></div>
      `;

      const grid = block.querySelector(".catalog-grid");
      catalogs.forEach((cat) => grid.appendChild(createCatalogCard(cat)));
      container.appendChild(block);
    });

    updateGlobalStats();
  }

  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function getCatalogProgress(catalogId) {
    const cat = progress.catalogs[catalogId];
    if (!cat) return 0;
    const catalog = data.catalogos.find((c) => c.id === catalogId);
    if (!catalog || !catalog.preguntas) return 0;
    const best = cat.bestScore || 0;
    return best;
  }

  function startQuiz(catalog) {
    currentCatalog = catalog;
    questions = shuffle(catalog.preguntas);
    currentIndex = 0;
    hearts = MAX_HEARTS;
    streak = 0;
    bestStreak = 0;
    correctCount = 0;
    sessionXP = 0;
    answered = false;

    $("#catalog-label").textContent = catalog.nombre;
    $("#catalog-label").style.color = catalog.color;

    showScreen("quiz");
    renderHearts();
    showQuestion();
  }

  function renderHearts() {
    const container = $("#hearts-display");
    container.innerHTML = "";
    for (let i = 0; i < MAX_HEARTS; i++) {
      const span = document.createElement("span");
      span.className = "heart" + (i >= hearts ? " lost" : "");
      span.textContent = "❤️";
      container.appendChild(span);
    }
  }

  function startTimer() {
    clearInterval(timerInterval);
    timeLeft = TIME_PER_QUESTION;
    updateTimerUI();

    timerInterval = setInterval(() => {
      timeLeft--;
      updateTimerUI();
      if (timeLeft <= 0) {
        clearInterval(timerInterval);
        if (!answered) handleTimeout();
      }
    }, 1000);
  }

  function updateTimerUI() {
    const circle = $("#timer-circle");
    const text = $("#timer-text");
    const ring = $("#timer-ring");
    const circumference = 125.6;
    const offset = circumference * (1 - timeLeft / TIME_PER_QUESTION);

    circle.style.strokeDashoffset = offset;
    text.textContent = timeLeft;

    if (timeLeft <= 5) {
      ring.classList.add("urgent");
    } else {
      ring.classList.remove("urgent");
    }
  }

  function showQuestion() {
    if (currentIndex >= questions.length) {
      finishQuiz();
      return;
    }

    answered = false;
    const q = questions[currentIndex];

    $("#question-counter").textContent = `${currentIndex + 1} / ${questions.length}`;
    $("#quiz-progress").style.width = `${(currentIndex / questions.length) * 100}%`;
    $("#question-text").textContent = q.pregunta;

    const grid = $("#options-grid");
    grid.innerHTML = "";

    q.opciones.forEach((opt, i) => {
      const btn = document.createElement("button");
      btn.className = "option-btn";
      btn.innerHTML = `<span class="letter">${LETTERS[i]}</span><span>${opt}</span>`;
      btn.addEventListener("click", () => selectAnswer(i, btn));
      grid.appendChild(btn);
    });

    hideFeedback();
    startTimer();
  }

  function selectAnswer(index, btn) {
    if (answered) return;
    answered = true;
    clearInterval(timerInterval);

    const q = questions[currentIndex];
    const isCorrect = index === q.correcta;
    const buttons = $("#options-grid").querySelectorAll(".option-btn");

    buttons.forEach((b, i) => {
      b.disabled = true;
      if (i === q.correcta) b.classList.add("correct");
      else if (i === index && !isCorrect) b.classList.add("wrong");
      else b.classList.add("dimmed");
    });

    if (isCorrect) {
      streak++;
      correctCount++;
      let xp = XP_CORRECT;
      if (streak >= 3) {
        xp += XP_BONUS_STREAK;
        showStreakToast(`🔥 ¡Racha de ${streak}! +${XP_BONUS_STREAK} XP extra`);
      }
      sessionXP += xp;
      showFeedback(true, q.explicacion);
      spawnConfetti();
    } else {
      streak = 0;
      hearts--;
      renderHearts();
      showFeedback(false, q.explicacion);

      if (hearts <= 0) {
        setTimeout(() => finishQuiz(true), 1800);
      }
    }

    if (streak > bestStreak) bestStreak = streak;
  }

  function handleTimeout() {
    answered = true;
    const q = questions[currentIndex];
    const buttons = $("#options-grid").querySelectorAll(".option-btn");

    buttons.forEach((b, i) => {
      b.disabled = true;
      if (i === q.correcta) b.classList.add("correct");
      else b.classList.add("dimmed");
    });

    streak = 0;
    hearts--;
    renderHearts();
    showFeedback(false, "⏱️ ¡Se acabó el tiempo! " + q.explicacion);

    if (hearts <= 0) {
      setTimeout(() => finishQuiz(true), 1800);
    }
  }

  function showFeedback(isCorrect, explanation) {
    const panel = $("#feedback-panel");
    panel.className = "feedback-panel show " + (isCorrect ? "correct" : "wrong");
    $("#feedback-title").textContent = isCorrect ? "¡Correcto! 🎉" : "¡Ups! 😅";
    $("#feedback-explanation").textContent = explanation;

    if (hearts <= 0 && !isCorrect) {
      $("#btn-continue").textContent = "Ver resultados";
    } else {
      $("#btn-continue").textContent = currentIndex + 1 >= questions.length ? "Ver resultados" : "Continuar";
    }
  }

  function hideFeedback() {
    $("#feedback-panel").className = "feedback-panel";
  }

  $("#btn-continue").addEventListener("click", () => {
    hideFeedback();
    if (hearts <= 0) {
      finishQuiz(true);
      return;
    }
    currentIndex++;
    showQuestion();
  });

  function finishQuiz(outOfHearts = false) {
    clearInterval(timerInterval);
    hideFeedback();

    const total = questions.length;
    const pct = Math.round((correctCount / total) * 100);

    progress.totalXP += sessionXP;
    if (bestStreak > progress.bestStreak) progress.bestStreak = bestStreak;

    if (!progress.catalogs[currentCatalog.id]) {
      progress.catalogs[currentCatalog.id] = { completed: 0, bestScore: 0 };
    }
    const catProg = progress.catalogs[currentCatalog.id];
    if (correctCount > catProg.completed) catProg.completed = correctCount;
    if (pct > catProg.bestScore) catProg.bestScore = pct;

    saveProgress();

    let emoji, title, subtitle;
    if (outOfHearts) {
      emoji = "💔";
      title = "¡Sin vidas!";
      subtitle = "No te rindas, inténtalo de nuevo";
    } else if (pct === 100) {
      emoji = "🏆";
      title = "¡Perfecto!";
      subtitle = "Dominaste este catálogo";
      spawnConfetti(40);
    } else if (pct >= 70) {
      emoji = "⭐";
      title = "¡Muy bien!";
      subtitle = "Vas por buen camino";
    } else {
      emoji = "💪";
      title = "¡Sigue practicando!";
      subtitle = "Cada intento te hace mejor";
    }

    $("#results-emoji").textContent = emoji;
    $("#results-title").textContent = title;
    $("#results-subtitle").textContent = subtitle;
    $("#results-score").textContent = pct + "%";
    $("#stat-correct").textContent = `${correctCount}/${total}`;
    $("#stat-xp").textContent = "+" + sessionXP;
    $("#stat-streak").textContent = bestStreak;

    showScreen("results");
  }

  function showStreakToast(msg) {
    const toast = $("#streak-toast");
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2200);
  }

  function spawnConfetti(count = 20) {
    const colors = ["#FFC72C", "#DA291C", "#FFBC0D", "#ffffff", "#B01E13", "#E8A800"];
    for (let i = 0; i < count; i++) {
      const piece = document.createElement("div");
      piece.className = "confetti-piece";
      piece.style.left = Math.random() * 100 + "vw";
      piece.style.background = colors[Math.floor(Math.random() * colors.length)];
      piece.style.animationDuration = 1.5 + Math.random() * 2 + "s";
      piece.style.borderRadius = Math.random() > 0.5 ? "50%" : "2px";
      document.body.appendChild(piece);
      setTimeout(() => piece.remove(), 4000);
    }
  }

  $("#btn-retry").addEventListener("click", () => startQuiz(currentCatalog));
  $("#btn-home").addEventListener("click", goHome);
  $("#btn-quiz-back")?.addEventListener("click", goHome);

  function goHome() {
    renderCatalogs();
    showScreen("home");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function fetchJson(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`No se pudo cargar ${url}`);
    return res.json();
  }

  async function loadCatalogQuestions(catalog) {
    if (catalog.preguntas) return catalog.preguntas;

    if (catalog.fuente === "separado") {
      const [preguntasData, respuestasData] = await Promise.all([
        fetchJson(catalog.archivos.preguntas),
        fetchJson(catalog.archivos.respuestas),
      ]);

      catalog.preguntas = preguntasData.preguntas.map((q) => {
        const resp = respuestasData.respuestas[q.id];
        if (!resp) throw new Error(`Falta respuesta para ${q.id}`);
        return {
          id: q.id,
          pregunta: q.pregunta,
          opciones: resp.opciones,
          correcta: resp.correcta,
          explicacion: resp.explicacion,
        };
      });
      return catalog.preguntas;
    }

    if (catalog.fuente === "archivo") {
      const archivo = await fetchJson(catalog.archivo);
      catalog.preguntas = archivo.preguntas;
      return catalog.preguntas;
    }

    throw new Error(`Catálogo sin fuente de preguntas: ${catalog.id}`);
  }

  async function loadAllCatalogs(catalogos) {
    const normales = catalogos.filter((c) => c.fuente !== "repaso-total");
    await Promise.all(normales.map((cat) => loadCatalogQuestions(cat)));

    const repaso = catalogos.find((c) => c.fuente === "repaso-total");
    if (repaso) {
      repaso.preguntas = [];
      normales.forEach((cat) => {
        if (!cat.preguntas?.length) return;
        cat.preguntas.forEach((q) => {
          repaso.preguntas.push({
            ...q,
            id: `repaso-${cat.id}-${q.id}`,
            catalogoOrigen: cat.nombre,
            pregunta: `[${cat.nombre}] ${q.pregunta}`,
          });
        });
      });
    }
  }

  async function init() {
    try {
      const manifest = await fetchJson("data/catalogos.json");
      data = manifest;
      await loadAllCatalogs(data.catalogos);
      updateGlobalStats();
      renderCatalogs();
      showScreen("home");
    } catch (err) {
      screens.loading.innerHTML = `
        <div class="loading">
          <p style="color:var(--wrong);font-weight:700;">Error al cargar</p>
          <p>${err.message}</p>
          <p style="margin-top:1rem;font-size:0.85rem;">Abre el proyecto con un servidor local (Live Server en VS Code) para que funcionen los JSON.</p>
        </div>
      `;
    }
  }

  init();
})();
