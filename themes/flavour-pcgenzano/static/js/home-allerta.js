/* ============================================================
   HOME-ALLERTA v1.0 — logica client delle barre di stato homepage.
   Estratto da layouts/index.html il 15/07/2026 (audit esterno:
   troppa logica inline nel template + parser CSV naïf).

   Contiene:
   1. Guard scadenza barra rischio incendi (nasconde la barra se la
      data di validità è passata anche quando l'HTML statico non è
      stato rigenerato — difesa complementare al guard di build Hugo).
   2. Giorni delle strisce («Oggi», «Domani», a mezzanotte) e passaggio
      dell'avviso meteo da previsto a in vigore, ogni minuto.
   3. Stato dell'allerta letto dal sito (/allerta-stato/index.json, scritto
      da check-allerta.py con le fonti ufficiali): la pagina lasciata aperta
      si aggiorna quando c'è un controllo più recente. A ogni visita, ogni
      10 minuti e tornando sulla scheda. Fino all'11/11/2026 il browser
      leggeva i CSV del mirror opendatasicilia (circa 3 MB l'uno da leggere,
      un centinaio di KB compressi).
   ============================================================ */
(function () {
  'use strict';

  /* ── 1. Guard scadenza barra incendi ── */
  (function () {
    var b = document.getElementById('incendi-bar'); if (!b) return;
    var d = b.getAttribute('data-valido'); if (!d) return;
    var t = new Date();
    var oggi = t.getFullYear() + '-' + ('0' + (t.getMonth() + 1)).slice(-2) + '-' + ('0' + t.getDate()).slice(-2);
    if (d < oggi) { b.style.display = 'none'; }
  })();

  /* ── 2. Giorni e avviso meteo: «Oggi», «Domani», «in vigore» ──
     Le etichette dei giorni le scrive la build, in ora italiana
     (partials/etichetta-giorno.html), ma la pagina può restare aperta oltre
     la mezzanotte o venire da una build della sera prima: qui si ricalcolano
     con l'orologio del dispositivo, sempre in ora italiana, al caricamento,
     ogni minuto e quando la scheda torna in primo piano. A mezzanotte
     «Domani, giovedì 12 novembre» diventa «Oggi, giovedì 12 novembre».
     Stesse parole del partial: chi cambia l'uno cambia anche l'altro.
     L'avviso meteo passa da «Da domani…» (toni tenui, role="status") a
     «in vigore» (toni pieni, role="alert", subito sotto la striscia di oggi)
     all'ora d'inizio, e sparisce alla scadenza. Nato l'11/11/2026: la
     striscia del vento previsto per il giorno dopo non diceva il giorno e,
     sotto «Nessuna allerta», sembrava già in vigore. */
  var GIORNI = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
  var MESI_NOMI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
  var TITOLO_PRECISATO = 'NESSUNA ALLERTA PER RISCHIO IDROGEOLOGICO E IDRAULICO';
  var RE_GIORNO = /^\d{4}-\d{2}-\d{2}$/;

  function due(x) { return (x < 10 ? '0' : '') + x; }

  // Giorno 'AAAA-MM-GG' di un istante, in ora italiana.
  function giornoRoma(d) {
    try {
      var parti = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(d);
      var o = {};
      for (var i = 0; i < parti.length; i++) o[parti[i].type] = parti[i].value;
      if (o.year && o.month && o.day) return o.year + '-' + o.month + '-' + o.day;
    } catch (e) { /* browser senza fusi orari: si usa l'ora del dispositivo */ }
    return d.getFullYear() + '-' + due(d.getMonth() + 1) + '-' + due(d.getDate());
  }

  function utcDaGiorno(g, piu) {
    var a = g.split('-');
    return new Date(Date.UTC(+a[0], +a[1] - 1, +a[2] + (piu || 0)));
  }

  function nomeGiorno(g) {
    var d = utcDaGiorno(g);
    return GIORNI[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MESI_NOMI[d.getUTCMonth()];
  }

  // Ora di scadenza in ora italiana, nella forma del partial: «alle 18»,
  // «all'una», «alle 18:30»; "" a mezzanotte (allora vale «fine giornata»).
  function oraFine(d) {
    var h, m;
    try {
      var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(d);
      var o = {};
      for (var i = 0; i < p.length; i++) o[p[i].type] = p[i].value;
      h = +o.hour % 24; m = +o.minute;
    } catch (e) { h = d.getHours(); m = d.getMinutes(); }
    if (isNaN(h) || isNaN(m) || (h === 0 && m === 0)) return '';
    if (m) return 'alle ' + h + ':' + due(m);
    return h === 1 ? 'all\'una' : 'alle ' + h;
  }

  function etichetta(g, forma, oggi, ora) {
    var nome = nomeGiorno(g);
    var dd = utcDaGiorno(oggi, 1);
    var domani = dd.getUTCFullYear() + '-' + due(dd.getUTCMonth() + 1) + '-' + due(dd.getUTCDate());
    if (forma === 'da') return g === oggi ? 'Da oggi, ' + nome : (g === domani ? 'Da domani, ' + nome : 'Da ' + nome);
    if (forma === 'fino') {
      if (g === oggi) return ora ? 'fino ' + ora : 'fino a fine giornata';
      if (g === domani) return 'fino a domani, ' + nome + (ora ? ', ' + ora : '');
      return 'fino a ' + nome + (ora ? ' ' + ora : '');
    }
    return g === oggi ? 'Oggi, ' + nome : (g === domani ? 'Domani, ' + nome : nome.charAt(0).toUpperCase() + nome.slice(1));
  }

  // Oggi verde con un avviso in vigore: «Nessuna allerta» da sola
  // contraddirebbe la striscia dell'avviso, quindi si dice di quale rischio
  // parla. Solo se la striscia di oggi è davvero di oggi (dopo mezzanotte,
  // finché la pagina non si ricostruisce, è quella di ieri e resta com'è).
  // Si torna al testo della build quando l'avviso finisce. Non tocca gli altri
  // stati (livello aggiornato dallo stato del sito, «da confermare»).
  function precisaOggi(tipo, inVigore, oggi) {
    var oggiBar = document.getElementById('allerta-bar');
    var t = document.getElementById('allerta-titolo');
    var d = document.getElementById('allerta-desc');
    var g = document.getElementById('allerta-giorno');
    if (!oggiBar || !t) return;
    var originale = oggiBar.getAttribute('data-titolo') || 'NESSUNA ALLERTA';
    var diOggi = !g || g.getAttribute('data-giorno') === oggi;
    if (inVigore && diOggi && oggiBar.classList.contains('allerta-bar-verde')) {
      if (t.textContent === originale) {
        t.textContent = TITOLO_PRECISATO;
        if (d) d.textContent = '— È in vigore l\'avviso meteo per ' + tipo + ' qui sotto.';
      }
    } else if ((!inVigore || !diOggi) && t.textContent === TITOLO_PRECISATO) {
      t.textContent = originale;
      if (d) d.textContent = '— ' + (oggiBar.getAttribute('data-desc') || '');
    }
  }

  function aggiornaAvviso(adesso, oggi) {
    var bar = document.getElementById('avviso-meteo-bar');
    if (!bar) return;
    var ini = new Date(bar.getAttribute('data-inizio') || '');
    var fin = new Date(bar.getAttribute('data-fine') || '');
    if (isNaN(ini.getTime()) || isNaN(fin.getTime())) return;
    var tipoEl = document.getElementById('avviso-meteo-tipo');
    var tipo = tipoEl ? tipoEl.textContent : '';
    if (adesso > fin) {
      bar.style.display = 'none';
      precisaOggi(tipo, false, oggi);
      return;
    }
    var inVigore = adesso >= ini;
    var q = document.getElementById('avviso-meteo-quando');
    var st = document.getElementById('avviso-meteo-stato');
    var va = document.getElementById('avviso-meteo-validita');
    // scrivi(): ogni minuto si riscrive solo ciò che cambia, perché la striscia
    // in vigore è role="alert" e lo stesso testo riscritto si rileggerebbe.
    if (inVigore) {
      scrivi(q, etichetta(oggi, 'giorno', oggi));
      scrivi(st, ' in vigore');
      scrivi(va, etichetta(giornoRoma(new Date(fin.getTime() - 60000)), 'fino', oggi, oraFine(fin)));
      bar.classList.remove('avviso-meteo-bar-previsto');
      bar.setAttribute('role', 'alert');
      var oggiBar = document.getElementById('allerta-bar');
      if (oggiBar && oggiBar.parentNode && oggiBar.nextElementSibling !== bar) {
        oggiBar.parentNode.insertBefore(bar, oggiBar.nextSibling);
      }
    } else {
      scrivi(q, etichetta(giornoRoma(ini), 'da', oggi));
      scrivi(st, '');
      if (va) {
        var parti = [];
        if (bar.getAttribute('data-dal')) parti.push(bar.getAttribute('data-dal'));
        if (bar.getAttribute('data-durata')) parti.push('per ' + bar.getAttribute('data-durata'));
        scrivi(va, parti.join(', '));
      }
      bar.classList.add('avviso-meteo-bar-previsto');
      bar.setAttribute('role', 'status');
    }
    precisaOggi(tipo, inVigore, oggi);
  }

  function aggiornaGiorni() {
    var adesso = new Date();
    var oggi = giornoRoma(adesso);
    var el = document.querySelectorAll('#allerta-bar [data-giorno], #allerta-bar-domani [data-giorno]');
    for (var i = 0; i < el.length; i++) {
      var g = el[i].getAttribute('data-giorno');
      if (!RE_GIORNO.test(g)) continue;
      var testo = etichetta(g, el[i].getAttribute('data-forma') || 'giorno', oggi);
      if (el[i].textContent !== testo) el[i].textContent = testo;
    }
    aggiornaAvviso(adesso, oggi);
  }


  /* ── 3. Stato dell'allerta letto dal sito ──
     Fino all'11/11/2026 il browser scaricava a ogni visita, e ogni 30 minuti,
     i due CSV del mirror opendatasicilia (circa 3 MB l'uno da leggere, un
     centinaio di KB compressi), che quel giorno erano fermi all'8/11, e la
     striscia di oggi restava trasparente finché non arrivavano. Ora legge /allerta-stato/index.json: lo stato che
     check-allerta.py ricava ogni 5 minuti dalle fonti ufficiali (repository
     del Dipartimento e bollettino del Centro Funzionale della Regione Lazio),
     pochi KB e dallo stesso sito. La pagina nasce già con quello stato: il
     controllo serve alla pagina lasciata aperta, che si aggiorna quando arriva
     un controllo più recente di quello con cui è stata costruita. Le stesse
     regole della build: titolo e descrizione sono quelli scritti dallo
     script, il giorno della striscia di oggi è quello del controllo.
     Se lo stato non si legge, o non è più recente, resta la pagina; se il suo
     ultimo controllo ha più di 6 ore, segnalaDatoNonRecente lo dice. */
  var LIVELLI = ['verde', 'gialla', 'arancione', 'rossa'];
  var NORM_LIV = { giallo: 'gialla', rosso: 'rossa' };
  var TITOLI = { verde: 'NESSUNA ALLERTA', gialla: 'ALLERTA GIALLA', arancione: 'ALLERTA ARANCIONE', rossa: 'ALLERTA ROSSA' };
  var ultimaLettura = 0;

  function livello(v) {
    var l = String(v || '').toLowerCase();
    l = NORM_LIV[l] || l;
    return LIVELLI.indexOf(l) >= 0 ? l : '';
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Cambia il testo solo se è diverso: dentro una zona role="alert" anche lo
  // stesso testo riscritto può essere riletto dallo screen reader.
  function scrivi(el, s) { if (el && el.textContent !== s) el.textContent = s; }

  // «11 novembre 2026, 17:54» in ora italiana, come la riga della build.
  function dataOraRoma(d) {
    try {
      var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Rome', year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' }).formatToParts(d);
      var o = {};
      for (var i = 0; i < p.length; i++) o[p[i].type] = p[i].value;
      if (o.year && o.month && o.day && o.hour && o.minute) {
        return (+o.day) + ' ' + MESI_NOMI[+o.month - 1] + ' ' + o.year + ', ' + o.hour + ':' + o.minute;
      }
    } catch (e) { /* browser senza fusi orari: si usa l'ora del dispositivo */ }
    return d.getDate() + ' ' + MESI_NOMI[d.getMonth()] + ' ' + d.getFullYear() + ', ' + due(d.getHours()) + ':' + due(d.getMinutes());
  }

  /* Stato neutro «da confermare»: quando l'ultimo controllo riuscito ha
     più di 6 ore, il colore e il titolo della barra non possono continuare a
     rassicurare (il verde resta il messaggio più forte della pagina). La barra
     passa al grigio e rimanda al bollettino ufficiale; la riga «Verificato»
     conserva l'ora dell'ultimo controllo riuscito (audit 25/09/2026; mai
     spacciare per attuale un dato che non lo è, rule 06). */
  function impostaStatoNonVerificato(bar) {
    var classi = bar.className.split(/\s+/);
    for (var i = 0; i < classi.length; i++) {
      if (classi[i].indexOf('allerta-bar-') === 0 && classi[i] !== 'allerta-bar-loading') {
        bar.classList.remove(classi[i]);
      }
    }
    bar.classList.add('allerta-bar-nonverificato');
    scrivi(document.getElementById('allerta-titolo'), 'STATO DELL’ALLERTA DA CONFERMARE');
    scrivi(document.getElementById('allerta-desc'), '— consulta il bollettino ufficiale del Centro Funzionale regionale.');
    var ic = document.getElementById('allerta-icon');
    if (ic) ic.className = 'bi bi-question-circle-fill me-2';
  }

  function segnalaDatoNonRecente(bar) {
    var t = new Date(bar.getAttribute('data-controllo') || '');
    if (isNaN(t.getTime())) return;
    if (Date.now() - t.getTime() < 6 * 60 * 60 * 1000) return;
    impostaStatoNonVerificato(bar);
    scrivi(document.getElementById('allerta-controllo'), dataOraRoma(t) + ' — ultimo controllo di oltre 6 ore fa');
  }

  function applicaOggi(bar, j, controllo) {
    var liv = livello(j.livello);
    if (!liv) return false;
    var titolo = j.titolo || TITOLI[liv];
    bar.className = 'allerta-bar allerta-bar-' + liv;
    bar.setAttribute('data-controllo', j.ultimo_controllo || j.ultimo_aggiornamento);
    if (j.ultimo_aggiornamento) bar.setAttribute('data-aggiornamento', j.ultimo_aggiornamento);
    bar.setAttribute('data-titolo', titolo);
    bar.setAttribute('data-desc', j.descrizione || '');
    // Se c'era la precisazione dell'avviso in vigore, precisaOggi la rimette
    // sul testo nuovo (aggiornaGiorni, subito dopo).
    scrivi(document.getElementById('allerta-titolo'), titolo);
    scrivi(document.getElementById('allerta-desc'), '— ' + (j.descrizione || ''));
    var ic = document.getElementById('allerta-icon');
    if (ic) ic.className = liv === 'verde' ? 'bi bi-shield-check me-2' : 'bi bi-exclamation-triangle-fill me-2';
    var g = document.getElementById('allerta-giorno');
    if (g) g.setAttribute('data-giorno', giornoRoma(controllo));
    scrivi(document.getElementById('allerta-controllo'), dataOraRoma(controllo));
    return true;
  }

  // Come la build: la striscia di domani c'è se il livello previsto è almeno
  // giallo, con il giorno e i rischi scritti dallo script.
  function applicaDomani(dom) {
    var barDomani = document.getElementById('allerta-bar-domani');
    if (!barDomani) return;
    var liv = dom ? livello(dom.livello) : '';
    var g = dom && RE_GIORNO.test(dom.data || '') ? dom.data : '';
    if (!liv || liv === 'verde' || !dom.titolo || !g) {
      barDomani.style.display = 'none';
      barDomani.className = 'allerta-bar-domani allerta-bar-domani-verde';
      if (barDomani.innerHTML) barDomani.innerHTML = '';
      return;
    }
    var rischi = Object.prototype.toString.call(dom.rischi) === '[object Array]' ? dom.rischi.join(', ') : '';
    var html = '<div class="container"><i class="bi bi-calendar-event me-2" aria-hidden="true"></i>' +
      '<strong><span data-giorno="' + g + '">' + esc(etichetta(g, 'giorno', giornoRoma(new Date()))) + '</span>:</strong> ' +
      'prevista <span id="allerta-domani-titolo">allerta ' + liv + '</span>' +
      (rischi ? ' <span class="text-nowrap">— ' + esc(rischi) + '</span>' : '') + '</div>';
    barDomani.className = 'allerta-bar-domani allerta-bar-domani-' + liv;
    barDomani.style.display = '';
    if (barDomani.innerHTML !== html) barDomani.innerHTML = html;
  }

  function checkStatoAllerta() {
    var bar = document.getElementById('allerta-bar');
    if (!bar) return;
    ultimaLettura = Date.now();
    var url = bar.getAttribute('data-stato');
    function fine(j) {
      bar.classList.remove('allerta-bar-loading');
      var nuovo = j && Date.parse(j.ultimo_controllo || j.ultimo_aggiornamento || '');
      var pagina = Date.parse(bar.getAttribute('data-controllo') || '');
      if (nuovo && !isNaN(nuovo) && (isNaN(pagina) || nuovo > pagina) && applicaOggi(bar, j, new Date(nuovo))) {
        applicaDomani(j.domani);
        aggiornaGiorni();
      }
      segnalaDatoNonRecente(bar);
    }
    if (!url || !window.fetch) { fine(null); return; }
    fetch(url, { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(fine, function () { fine(null); });
  }

  aggiornaGiorni();
  setInterval(aggiornaGiorni, 60 * 1000);
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) return;
    aggiornaGiorni();
    // Tornando sulla scheda, lo stato si rilegge se l'ultima lettura ha più di 2 minuti.
    if (Date.now() - ultimaLettura > 2 * 60 * 1000) checkStatoAllerta();
  });

  // La striscia di oggi parte trasparente (allerta-bar-loading) per non
  // cambiare colore sotto gli occhi se lo stato è più recente della pagina:
  // con la rete lenta non deve restare nascosta, quindi dopo 1,5 secondi si
  // mostra comunque quella della pagina.
  setTimeout(function () {
    var b = document.getElementById('allerta-bar');
    if (b) b.classList.remove('allerta-bar-loading');
  }, 1500);
  checkStatoAllerta();
  setInterval(checkStatoAllerta, 10 * 60 * 1000);
})();
