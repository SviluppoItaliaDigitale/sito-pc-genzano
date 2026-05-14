/* quiz-preparazione.js — Quiz "Quanto sei preparato a un'emergenza?" (idea #7).
 *
 * Quiz adattivo: le domande di approfondimento dipendono dalla situazione
 * dichiarata (con chi vivi, casa, auto, animali). Alla fine: profilo di
 * preparazione + piano d'azione personalizzato (le cose che ti aiuterebbero
 * di più), badge PNG scaricabile (canvas) e versione stampabile (window.print).
 *
 * Tutto sul dispositivo: nessuna risposta inviata, nessun backend, niente
 * librerie esterne. localStorage solo per non perdere le risposte a un refresh.
 * Tono non giudicante: niente voti, solo "ecco cosa puoi rafforzare".
 * Accessibile: radiogroup nativi, navigazione da tastiera, aria-live.
 */
(function () {
  "use strict";

  var app = document.getElementById("quiz-app");
  if (!app) return;

  var KEY = "pcgenzano-quiz-preparazione";
  var BASE = (window.SITO_BASEURL || "/");
  function url(p) { return BASE.replace(/\/$/, "") + "/" + p.replace(/^\//, ""); }

  // ── Domande ──────────────────────────────────────────────────────────────
  // condizione(ans): se presente, la domanda compare solo se ritorna true.
  var DOMANDE = [
    { id: "situazione", testo: "Con chi vivi?", opzioni: [
      { val: "solo", testo: "Da solo / da sola" },
      { val: "famiglia", testo: "Con la mia famiglia" },
      { val: "fragili", testo: "Con persone anziane o fragili" },
      { val: "bambini", testo: "Con bambini piccoli" } ] },
    { id: "abitazione", testo: "Dove abiti?", opzioni: [
      { val: "indipendente", testo: "Casa indipendente" },
      { val: "appartamento", testo: "Appartamento ai piani bassi" },
      { val: "alto", testo: "Appartamento ai piani alti" } ] },
    { id: "auto", testo: "Hai un'auto che usi spesso?", opzioni: [
      { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },
    { id: "animali", testo: "Vivono animali domestici con te?", opzioni: [
      { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },

    { id: "kit", testo: "Hai un kit di emergenza pronto (acqua, torcia, radio a pile, power bank, fischietto)?",
      opzioni: [ { val: "si", testo: "Sì, è pronto e so dov'è" },
        { val: "parziale", testo: "Ho qualcosa, ma non è completo" },
        { val: "no", testo: "No" } ] },
    { id: "acqua", testo: "Hai in casa una scorta d'acqua potabile per qualche giorno?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No / non lo so" } ] },
    { id: "documenti", testo: "Hai copie dei documenti importanti, anche in formato digitale?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },
    { id: "numeri", testo: "Hai i numeri utili a portata di mano e sai che in emergenza, nel Lazio, si chiama il 112?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No / non ne sono sicuro" } ] },
    { id: "interruttori", testo: "Sai dove e come chiudere gas, acqua e corrente di casa?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },
    { id: "aree", testo: "Sai dove sono le aree di attesa del tuo Comune, dove andare in caso di evacuazione?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },
    { id: "piano", testo: "Hai concordato un piano: dove ritrovarsi, chi avvisare, cosa fare?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No, non ancora" } ] },
    { id: "italert", testo: "Sai cos'è IT-alert e cosa fare quando arriva un messaggio sul telefono?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },

    { id: "fragili_lista", condizione: function (a) { return a.situazione === "fragili"; },
      testo: "Hai una lista aggiornata di farmaci, terapie e bisogni delle persone fragili che vivono con te?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },
    { id: "bambini_sanno", condizione: function (a) { return a.situazione === "bambini"; },
      testo: "I bambini conoscono il proprio nome e cognome e sanno chi e come chiamare in caso di bisogno?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No / in parte" } ] },
    { id: "auto_kit", condizione: function (a) { return a.auto === "si"; },
      testo: "Tieni in auto un minimo di scorte (acqua, coperta, torcia, caricabatterie, triangolo)?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] },
    { id: "animali_kit", condizione: function (a) { return a.animali === "si"; },
      testo: "Hai un kit per i tuoi animali (trasportino, cibo e acqua, libretto sanitario, guinzaglio)?",
      opzioni: [ { val: "si", testo: "Sì" }, { val: "no", testo: "No" } ] }
  ];

  // Per ogni "lacuna" possibile: l'azione consigliata e il link di supporto.
  var AZIONI = {
    kit:           { t: "Prepara un kit di emergenza essenziale: acqua, torcia, radio a pile, power bank, fischietto, documenti.", l: "rischi-prevenzione/kit-emergenza/" },
    acqua:         { t: "Tieni in casa una scorta d'acqua potabile per qualche giorno.", l: "rischi-prevenzione/kit-emergenza/" },
    documenti:     { t: "Fai delle copie dei documenti importanti e conservane una versione digitale.", l: "piano-familiare/" },
    numeri:        { t: "Salva i numeri utili e ricorda: nel Lazio in emergenza si chiama il 112.", l: "numeri-utili/" },
    interruttori:  { t: "Impara dove e come chiudere gas, acqua e corrente di casa.", l: "rischi-prevenzione/" },
    aree:          { t: "Scopri dove sono le aree di attesa del tuo Comune.", l: "cartografia/" },
    piano:         { t: "Concorda un piano: punto di ritrovo, chi avvisa chi, cosa fare.", l: "piano-familiare/" },
    italert:       { t: "Informati su IT-alert e su cosa fare quando ricevi un messaggio.", l: "comunicazioni/" },
    fragili_lista: { t: "Prepara una lista aggiornata di farmaci e bisogni delle persone fragili con te.", l: "formazione/kit-calamita-anziani/" },
    bambini_sanno: { t: "Parla con i bambini di cosa fare in emergenza, in modo semplice e non spaventoso.", l: "formazione/kit-calamita-bambini/" },
    auto_kit:      { t: "Aggiungi un piccolo kit di scorte nell'auto.", l: "rischi-prevenzione/kit-emergenza/" },
    animali_kit:   { t: "Prepara un kit per i tuoi animali domestici.", l: "formazione/kit-calamita-animali/" }
  };
  var PUNTI_FORZA = {
    kit: "Hai un kit di emergenza", acqua: "Hai una scorta d'acqua",
    documenti: "Hai copie dei documenti", numeri: "Conosci i numeri utili e il 112",
    interruttori: "Sai chiudere gas, acqua e corrente", aree: "Sai dove sono le aree di attesa",
    piano: "Avete un piano condiviso", italert: "Conosci IT-alert",
    fragili_lista: "Hai la lista dei bisogni delle persone fragili",
    bambini_sanno: "I bambini sono coinvolti e informati",
    auto_kit: "Hai un kit in auto", animali_kit: "Hai un kit per gli animali"
  };

  var ans = {};
  try { ans = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { ans = {}; }
  var idx = 0;

  function attive() {
    return DOMANDE.filter(function (d) { return !d.condizione || d.condizione(ans); });
  }
  function salva() { try { localStorage.setItem(KEY, JSON.stringify(ans)); } catch (e) {} }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // ── Render di una domanda ────────────────────────────────────────────────
  function rendiDomanda() {
    var lista = attive();
    if (idx >= lista.length) { rendiRisultato(); return; }
    var d = lista[idx];
    var h = '<div class="quiz-progress">Domanda ' + (idx + 1) + " di " + lista.length + '</div>' +
      '<div class="quiz-barra" aria-hidden="true"><span style="width:' +
      Math.round(((idx) / lista.length) * 100) + '%"></span></div>' +
      '<fieldset class="quiz-fieldset">' +
      '<legend class="quiz-domanda">' + esc(d.testo) + "</legend>" +
      '<div class="quiz-opzioni" role="radiogroup" aria-label="' + esc(d.testo) + '">';
    d.opzioni.forEach(function (o) {
      var sel = ans[d.id] === o.val;
      h += '<button type="button" class="quiz-opt' + (sel ? " is-sel" : "") +
        '" role="radio" aria-checked="' + (sel ? "true" : "false") +
        '" data-val="' + esc(o.val) + '">' + esc(o.testo) + "</button>";
    });
    h += "</div></fieldset>" +
      '<div class="quiz-nav">' +
      (idx > 0 ? '<button type="button" class="quiz-btn quiz-btn-sec" data-az="indietro">Indietro</button>' : "<span></span>") +
      "</div>";
    app.innerHTML = h;

    app.querySelectorAll(".quiz-opt").forEach(function (b) {
      b.addEventListener("click", function () {
        ans[d.id] = b.getAttribute("data-val");
        salva();
        idx++;
        rendiDomanda();
      });
    });
    var ind = app.querySelector('[data-az="indietro"]');
    if (ind) ind.addEventListener("click", function () { idx = Math.max(0, idx - 1); rendiDomanda(); });
    var primo = app.querySelector(".quiz-opt");
    if (primo) primo.focus();
  }

  // ── Analisi e risultato ──────────────────────────────────────────────────
  function analizza() {
    var lista = attive();
    var forza = [], lacune = [];
    lista.forEach(function (d) {
      if (!AZIONI[d.id]) return; // le 4 domande "situazione" non sono punteggiate
      var v = ans[d.id];
      if (v === "si") forza.push(PUNTI_FORZA[d.id]);
      else lacune.push(AZIONI[d.id]); // "no" o "parziale"
    });
    var tot = forza.length + lacune.length;
    var quota = tot ? forza.length / tot : 0;
    var tier;
    if (quota >= 0.8) tier = { id: "alto", t: "Ben preparato", d: "Hai già le basi solide. Mancano pochi dettagli per essere completo." };
    else if (quota >= 0.45) tier = { id: "medio", t: "A buon punto", d: "Sei sulla strada giusta. Ecco le cose che farebbero la differenza per te." };
    else tier = { id: "base", t: "Da rafforzare", d: "Nessun giudizio: si parte sempre da qui. Ecco i primi passi più utili." };
    return { tier: tier, forza: forza, lacune: lacune.slice(0, 6), totLacune: lacune.length };
  }

  function rendiRisultato() {
    var r = analizza();
    var oggi = new Date().toLocaleDateString("it-IT", { day: "numeric", month: "long", year: "numeric" });
    var h = '<div class="quiz-risultato">' +
      '<div class="quiz-badge quiz-badge-' + r.tier.id + '" role="img" aria-label="Profilo di preparazione: ' + esc(r.tier.t) + '">' +
      '<span class="quiz-badge-label">Profilo di preparazione</span>' +
      '<span class="quiz-badge-tier">' + esc(r.tier.t) + "</span></div>" +
      "<p class=\"quiz-risultato-intro\">" + esc(r.tier.d) + "</p>";

    if (r.forza.length) {
      h += '<h2 class="quiz-sez">I tuoi punti di forza</h2><ul class="quiz-forza">';
      r.forza.forEach(function (f) { h += "<li>" + esc(f) + "</li>"; });
      h += "</ul>";
    }
    if (r.lacune.length) {
      h += '<h2 class="quiz-sez">Cosa ti aiuterebbe di più</h2><ol class="quiz-lacune">';
      r.lacune.forEach(function (a) {
        h += '<li><span>' + esc(a.t) + '</span> <a href="' + esc(url(a.l)) + '">Vai alla guida</a></li>';
      });
      h += "</ol>";
      if (r.totLacune > r.lacune.length) {
        h += '<p class="quiz-altre small">Ci sono altri punti da rafforzare: un passo alla volta, parti da questi.</p>';
      }
    } else {
      h += '<p class="quiz-sez">Hai risposto sì a tutto: complimenti, sei davvero preparato. Tieni il kit aggiornato e rifai il quiz ogni tanto.</p>';
    }

    h += '<div class="quiz-azioni no-print">' +
      '<button type="button" class="quiz-btn" data-az="badge">Scarica il badge</button>' +
      '<button type="button" class="quiz-btn" data-az="stampa">Stampa il piano</button>' +
      '<button type="button" class="quiz-btn quiz-btn-sec" data-az="rifai">Rifai il quiz</button>' +
      "</div>" +
      '<p class="quiz-data">Quiz completato il ' + esc(oggi) + " · Protezione Civile Genzano di Roma</p>" +
      "</div>";
    app.innerHTML = h;
    app.querySelector(".quiz-risultato").setAttribute("tabindex", "-1");
    app.querySelector(".quiz-risultato").focus();

    app.querySelector('[data-az="rifai"]').addEventListener("click", function () {
      ans = {}; idx = 0; salva(); rendiDomanda();
    });
    app.querySelector('[data-az="stampa"]').addEventListener("click", function () { window.print(); });
    app.querySelector('[data-az="badge"]').addEventListener("click", function () { scaricaBadge(r, oggi); });
  }

  // ── Badge PNG generato su canvas (niente librerie) ───────────────────────
  function scaricaBadge(r, oggi) {
    var S = 800;
    var c = document.createElement("canvas");
    c.width = S; c.height = S;
    var x = c.getContext("2d");
    var col = r.tier.id === "alto" ? "#15803d" : (r.tier.id === "medio" ? "#003366" : "#b45309");
    x.fillStyle = "#ffffff"; x.fillRect(0, 0, S, S);
    x.fillStyle = col; x.fillRect(0, 0, S, S);
    x.fillStyle = "#ffffff";
    x.fillRect(40, 40, S - 80, S - 80);
    x.fillStyle = col;
    x.textAlign = "center";
    x.font = "bold 34px Arial, sans-serif";
    x.fillText("PROFILO DI PREPARAZIONE", S / 2, 180);
    x.font = "bold 76px Arial, sans-serif";
    wrap(x, r.tier.t.toUpperCase(), S / 2, 320, S - 160, 84);
    x.font = "24px Arial, sans-serif";
    x.fillStyle = "#333333";
    x.fillText(r.forza.length + " punti di forza · " + r.totLacune + " da rafforzare", S / 2, 470);
    x.fillText('"Quanto sei preparato a un\'emergenza?"', S / 2, 540);
    x.font = "20px Arial, sans-serif";
    x.fillStyle = "#666666";
    x.fillText("Protezione Civile — Genzano di Roma", S / 2, 660);
    x.fillText(oggi, S / 2, 695);
    x.fillStyle = col;
    x.fillRect(40, S - 80, S - 80, 14);
    c.toBlob(function (blob) {
      if (!blob) return;
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "preparazione-pc-genzano.png";
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    }, "image/png");
  }
  function wrap(x, testo, cx, cy, max, lh) {
    var parole = testo.split(" "), riga = "", righe = [];
    parole.forEach(function (p) {
      var prova = riga ? riga + " " + p : p;
      if (x.measureText(prova).width > max && riga) { righe.push(riga); riga = p; }
      else riga = prova;
    });
    if (riga) righe.push(riga);
    var y = cy - ((righe.length - 1) * lh) / 2;
    righe.forEach(function (rg) { x.fillText(rg, cx, y); y += lh; });
  }

  // ── Avvio: se c'è già un quiz completo riprende dal risultato ────────────
  var completo = attive().every(function (d) { return ans[d.id]; });
  if (completo && Object.keys(ans).length) { idx = attive().length; rendiRisultato(); }
  else { rendiDomanda(); }
})();
