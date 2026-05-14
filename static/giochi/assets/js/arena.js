/* arena.js — Launcher "Arena PC Genzano" (idea #11 roadmap).
 *
 * Trasforma l'hub /giochi/ in un launcher in stile videogioco:
 *  - griglia di TUTTI i giochi (da GiochiPC.CATALOGO + elencoBadge)
 *  - badge di progresso su ogni card (completato % / badge ottenuto)
 *  - "continua dove avevi lasciato" (ultimo gioco aperto dal launcher)
 *  - filtri per fascia d'eta'
 *  - skin "Arena" (gaming) / "Classica" (sobria AGID), persistita
 *  - tutorial al primo accesso
 *
 * localStorage minimal: skin, ultimo gioco aperto, flag "intro vista".
 * Nessun account, nessun cloud. Coerente con progressione.js.
 *
 * Accessibilita': la skin "Arena" NON e' il default se prefers-reduced-motion
 * (in quel caso parte "Classica"). Le animazioni sono solo decorative e
 * disattivabili. Filtri e skin con <button> + aria-pressed.
 */
(function () {
  "use strict";

  if (!window.GiochiPC) return;
  var GP = window.GiochiPC;

  var K_SKIN = "pcgenzano.giochi.skin";
  var K_ULTIMO = "pcgenzano.giochi.ultimo";
  var K_INTRO = "pcgenzano.giochi.intro-vista";

  // Override: per 2 giochi l'id-catalogo != cartella
  var PERCORSO = { "quiz-primaria": "quiz", "memory-primaria": "memory" };
  var FASCIA_LABEL = { infanzia: "Infanzia", primaria: "Primaria", ragazzi: "Ragazzi" };

  function ls(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function pathGioco(b) {
    var slug = PERCORSO[b.id] || b.id;
    return b.fascia + "/" + slug + "/index.html";
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // ── Skin Arena / Classica ────────────────────────────────────────────────
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var skin = ls(K_SKIN);
  if (skin !== "arena" && skin !== "classica") {
    skin = reduce ? "classica" : "arena"; // default rispettoso di reduced-motion
  }
  function applicaSkin() {
    document.body.classList.toggle("arena-skin-on", skin === "arena");
    document.querySelectorAll(".arena-skin-btn").forEach(function (b) {
      var on = b.getAttribute("data-skin") === skin;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.classList.toggle("is-attivo", on);
    });
  }
  document.querySelectorAll(".arena-skin-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      skin = b.getAttribute("data-skin");
      lsSet(K_SKIN, skin);
      applicaSkin();
    });
  });
  applicaSkin();

  // ── Card di un gioco ─────────────────────────────────────────────────────
  function cardGioco(b, continua) {
    var col = document.createElement("div");
    col.className = continua ? "arena-continua-col" : "col-6 col-md-4 col-lg-3 arena-card-col";
    col.setAttribute("data-fascia", b.fascia);

    var statoCls, statoTxt, statoIco;
    if (b.ottenuto) { statoCls = "stato-badge"; statoTxt = "Badge · " + b.percentuale + "%"; statoIco = "bi-award-fill"; }
    else if (b.completato) { statoCls = "stato-corso"; statoTxt = "Giocato · " + b.percentuale + "%"; statoIco = "bi-hourglass-split"; }
    else { statoCls = "stato-nuovo"; statoTxt = "Da giocare"; statoIco = "bi-play-fill"; }

    col.innerHTML =
      '<a class="arena-card arena-card-' + b.fascia + (continua ? " arena-card-continua" : "") + '" href="' + esc(pathGioco(b)) + '" data-gid="' + esc(b.id) + '">' +
        '<span class="arena-card-ico" aria-hidden="true"><i class="bi ' + esc(b.icona || "bi-controller") + '"></i></span>' +
        '<span class="arena-card-nome">' + esc(b.nome) + '</span>' +
        '<span class="arena-card-fascia">' + (FASCIA_LABEL[b.fascia] || "") + '</span>' +
        '<span class="arena-card-stato ' + statoCls + '"><i class="bi ' + statoIco + '" aria-hidden="true"></i> ' + statoTxt + '</span>' +
        (continua ? '<span class="arena-card-cta">Riprendi <i class="bi bi-arrow-right" aria-hidden="true"></i></span>' : '') +
      '</a>';

    // Traccia l'ultimo gioco aperto dal launcher
    col.querySelector("a").addEventListener("click", function () {
      lsSet(K_ULTIMO, b.id);
    });
    return col;
  }

  // ── Render griglia + continua + riepilogo ────────────────────────────────
  var griglia = document.getElementById("arena-griglia");
  var riepilogo = document.getElementById("arena-riepilogo");
  var contSez = document.getElementById("arena-continua");
  var contCard = document.getElementById("arena-continua-card");
  var filtroAttivo = "";

  function render() {
    var badge = GP.elencoBadge();
    var perId = {};
    badge.forEach(function (b) { perId[b.id] = b; });

    // riepilogo
    var ottenuti = badge.filter(function (b) { return b.ottenuto; }).length;
    var giocati = badge.filter(function (b) { return b.completato; }).length;
    riepilogo.textContent = "Hai " + ottenuti + " badge su " + badge.length +
      " · " + giocati + " giochi provati";

    // continua
    var ultimo = ls(K_ULTIMO);
    if (ultimo && perId[ultimo]) {
      contCard.innerHTML = "";
      contCard.appendChild(cardGioco(perId[ultimo], true));
      contSez.hidden = false;
    } else {
      contSez.hidden = true;
    }

    // griglia
    griglia.innerHTML = "";
    var visibili = 0;
    badge.forEach(function (b) {
      if (filtroAttivo && b.fascia !== filtroAttivo) return;
      griglia.appendChild(cardGioco(b, false));
      visibili++;
    });
    if (!visibili) {
      griglia.innerHTML = '<div class="col-12"><p class="text-muted">Nessun gioco in questa fascia.</p></div>';
    }
  }

  // filtri
  document.querySelectorAll(".arena-filtro").forEach(function (f) {
    f.addEventListener("click", function () {
      filtroAttivo = f.getAttribute("data-fascia");
      document.querySelectorAll(".arena-filtro").forEach(function (x) {
        var on = x === f;
        x.setAttribute("aria-pressed", on ? "true" : "false");
        x.classList.toggle("is-attivo", on);
      });
      render();
    });
  });

  // reset progressi
  var btnReset = document.getElementById("btn-reset-badge");
  if (btnReset) {
    btnReset.addEventListener("click", function () {
      if (!confirm("Sei sicuro di voler azzerare tutti i progressi e i badge ottenuti?")) return;
      GP.reset();
      render();
    });
  }

  // tutorial primo accesso
  var intro = document.getElementById("arena-intro");
  if (intro && !ls(K_INTRO)) {
    intro.hidden = false;
    var chiudi = document.getElementById("arena-intro-chiudi");
    if (chiudi) chiudi.addEventListener("click", function () {
      intro.hidden = true;
      lsSet(K_INTRO, "1");
    });
  }

  render();
})();
