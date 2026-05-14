/* glossario-pagina.js — Filtro alfabetico + ricerca live per la pagina /glossario/.
 *
 * Enhancement progressivo: la pagina funziona già senza JS (voci A-Z statiche +
 * suggerimento Ctrl+F nel <noscript>). Con JS aggiunge:
 *   - una barra di lettere A-Z che filtra le voci per iniziale
 *   - un campo di ricerca che filtra le voci in tempo reale (termine + definizione)
 *   - conteggio risultati annunciato a screen reader (aria-live)
 *
 * Si attiva solo se trova il contenitore #glossario-strumenti nella pagina.
 * Lavora sulla struttura esistente di .article-body: H2 = lettera, H3 = termine,
 * contenuto del termine = elementi fra un H3 e il successivo H3/H2.
 *
 * Accessibilità: <button> e <input type="search"> nativi, focus visibile dal
 * tema, stato premuto via aria-pressed, conteggio via aria-live="polite".
 */
(function () {
  "use strict";

  var strumenti = document.getElementById("glossario-strumenti");
  if (!strumenti) return;

  var body = document.querySelector(".article-body") || strumenti.parentElement;
  if (!body) return;

  // ── Raccoglie le sezioni-lettera (H2) e le voci (H3 + contenuto) ──────────
  var sezioni = [];   // { letter, h2, voci: [...] }
  var voci = [];      // { h3, nodi: [...], lettera, testo }
  var sezioneCorr = null;

  Array.prototype.forEach.call(body.children, function (el) {
    var tag = el.tagName;
    if (tag === "H2") {
      sezioneCorr = { letter: el.textContent.trim().toUpperCase(), h2: el, voci: [] };
      sezioni.push(sezioneCorr);
    } else if (tag === "H3" && sezioneCorr) {
      var voce = {
        h3: el,
        nodi: [el],
        lettera: sezioneCorr.letter,
        testo: el.textContent.toLowerCase()
      };
      sezioneCorr.voci.push(voce);
      voci.push(voce);
    } else if (voci.length && sezioneCorr && sezioneCorr.voci.length) {
      // elemento di contenuto: appartiene all'ultima voce della sezione corrente
      var ultima = sezioneCorr.voci[sezioneCorr.voci.length - 1];
      ultima.nodi.push(el);
      ultima.testo += " " + el.textContent.toLowerCase();
    }
  });

  if (!voci.length) return; // struttura non riconosciuta: lascia la pagina com'è

  var lettere = sezioni.map(function (s) { return s.letter; });

  // ── Costruisce l'interfaccia ─────────────────────────────────────────────
  strumenti.innerHTML = "";

  var label = document.createElement("label");
  label.className = "form-label fw-bold";
  label.setAttribute("for", "glossario-cerca");
  label.textContent = "Cerca un termine o una sigla";
  strumenti.appendChild(label);

  var input = document.createElement("input");
  input.type = "search";
  input.id = "glossario-cerca";
  input.className = "form-control";
  input.placeholder = "Es. COC, allerta, evacuazione…";
  input.setAttribute("autocomplete", "off");
  input.setAttribute("aria-describedby", "glossario-conteggio");
  strumenti.appendChild(input);

  var barra = document.createElement("div");
  barra.className = "glossario-lettere";
  barra.setAttribute("role", "group");
  barra.setAttribute("aria-label", "Filtra il glossario per lettera iniziale");
  strumenti.appendChild(barra);

  function creaBottone(testo, valore, premuto) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "glossario-lettera-btn";
    b.textContent = testo;
    b.dataset.lettera = valore;
    b.setAttribute("aria-pressed", premuto ? "true" : "false");
    return b;
  }

  var btnTutte = creaBottone("Tutte", "", true);
  barra.appendChild(btnTutte);
  lettere.forEach(function (l) {
    barra.appendChild(creaBottone(l, l, false));
  });

  var conteggio = document.createElement("p");
  conteggio.id = "glossario-conteggio";
  conteggio.className = "glossario-conteggio";
  conteggio.setAttribute("aria-live", "polite");
  strumenti.appendChild(conteggio);

  // ── Logica di filtro ─────────────────────────────────────────────────────
  var letteraAttiva = "";

  function applica() {
    var q = input.value.trim().toLowerCase();
    var visibili = 0;

    voci.forEach(function (voce) {
      var okLettera = !letteraAttiva || voce.lettera === letteraAttiva;
      var okTesto = !q || voce.testo.indexOf(q) > -1;
      var mostra = okLettera && okTesto;
      voce.nodi.forEach(function (n) {
        n.style.display = mostra ? "" : "none";
      });
      if (mostra) visibili++;
    });

    // Nasconde gli H2 delle sezioni senza voci visibili
    sezioni.forEach(function (s) {
      var qualcunaVisibile = s.voci.some(function (v) {
        return v.nodi[0].style.display !== "none";
      });
      s.h2.style.display = qualcunaVisibile ? "" : "none";
    });

    if (visibili === voci.length) {
      conteggio.textContent = voci.length + " termini nel glossario";
    } else if (visibili === 0) {
      conteggio.textContent = "Nessun termine trovato. Prova un'altra parola o scrivi a segreteria@protezionecivilegenzano.it";
    } else {
      conteggio.textContent = visibili + (visibili === 1 ? " termine trovato" : " termini trovati");
    }
  }

  barra.addEventListener("click", function (ev) {
    var btn = ev.target.closest(".glossario-lettera-btn");
    if (!btn) return;
    letteraAttiva = btn.dataset.lettera;
    Array.prototype.forEach.call(barra.children, function (b) {
      b.setAttribute("aria-pressed", b === btn ? "true" : "false");
    });
    applica();
  });

  var debounce;
  input.addEventListener("input", function () {
    window.clearTimeout(debounce);
    debounce = window.setTimeout(applica, 120);
  });

  applica(); // stato iniziale: conteggio totale
})();
