/* Comunicati stampa: pulsante «Copia il testo» (layout comunicati-stampa/single.html).
   Copia titolo, sottotitolo, testo e recapiti del comunicato come testo semplice,
   senza il riquadro delle cifre, e lo annuncia a voce (role="status").

   Il pulsante è nascosto (hidden) finché questo script non verifica che il
   browser possa copiare: senza JavaScript non compare un comando che non funziona.
   navigator.clipboard.writeText non genera l'evento «copy», quindi
   copy-attribution.js non aggiunge la riga della fonte: il testo resta quello
   del comunicato, che i recapiti in fondo già firmano. */
(function () {
  'use strict';

  var btn = document.querySelector('[data-cs-copia]');
  if (!btn) return;
  var etichetta = btn.querySelector('[data-cs-copia-testo]');
  var stato = document.querySelector('[data-cs-stato]');
  var testoIniziale = etichetta ? etichetta.textContent : '';
  var timer = null;

  var haClipboard = !!(navigator.clipboard && window.isSecureContext);
  var haExec = !!(document.queryCommandSupported && document.queryCommandSupported('copy'));
  if (!haClipboard && !haExec) return;
  btn.hidden = false;

  function riga(el) {
    return (el.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function componi() {
    var parti = [];
    document.querySelectorAll('[data-cs-parte]').forEach(function (el) {
      var t = riga(el);
      if (t) parti.push(t);
    });
    var corpo = document.querySelector('[data-cs-corpo]');
    if (corpo) {
      Array.prototype.forEach.call(corpo.children, function (el) {
        if (el.matches('aside, .cs-cifre, script, style, template, [hidden]')) return;
        var t = riga(el);
        if (t) parti.push(t);
      });
    }
    var contatti = document.querySelector('[data-cs-contatti]');
    if (contatti) {
      var righe = Array.prototype.map.call(contatti.querySelectorAll('h2, p'), riga)
        .filter(function (t) { return t; });
      if (righe.length) parti.push(righe.join('\n'));
    }
    return parti.join('\n\n');
  }

  function annuncia(msg) {
    if (!stato) return;
    stato.textContent = '';
    window.setTimeout(function () { stato.textContent = msg; }, 50);
  }

  function esito(ok) {
    if (ok) {
      if (etichetta) etichetta.textContent = 'Testo copiato';
      annuncia('Testo del comunicato copiato negli appunti.');
    } else {
      if (etichetta) etichetta.textContent = 'Copia non riuscita';
      annuncia('Non è stato possibile copiare il testo: selezionalo e copialo a mano.');
    }
    window.clearTimeout(timer);
    timer = window.setTimeout(function () {
      if (etichetta) etichetta.textContent = testoIniziale;
    }, 4000);
  }

  function copiaVecchioModo(testo) {
    var area = document.createElement('textarea');
    area.value = testo;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.top = '-1000px';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(area);
    btn.focus();
    return ok;
  }

  btn.addEventListener('click', function () {
    var testo = componi();
    if (haClipboard) {
      navigator.clipboard.writeText(testo).then(function () {
        esito(true);
      }, function () {
        esito(haExec ? copiaVecchioModo(testo) : false);
      });
    } else {
      esito(copiaVecchioModo(testo));
    }
  });
})();

/* Archivio dei comunicati: filtro per anno e mese (layout comunicati-stampa/list.html,
   richiesta dell'utente del 24/10/2026). I menu sono nascosti (hidden) finché questo
   script non parte: senza JavaScript si vede tutto, raggruppato per mese. Scelto un
   anno, il menu dei mesi mostra solo i mesi di quell'anno. Il filtro agisce sul
   posto, senza ricaricare e senza spostare il fuoco (WCAG 3.2.2); l'esito si legge
   sotto i menu ed è annunciato dagli screen reader (role="status"). La scelta resta
   nell'indirizzo (?anno=2026&mese=10), così si può condividere. */
(function () {
  'use strict';

  var box = document.querySelector('[data-cs-filtro]');
  if (!box) return;
  var selAnno = box.querySelector('[data-cs-anno]');
  var selMese = box.querySelector('[data-cs-mese]');
  var azzera = box.querySelector('[data-cs-azzera]');
  var esito = box.querySelector('[data-cs-esito]');
  var voci = Array.prototype.slice.call(document.querySelectorAll('.cs-voce[data-anno]'));
  var gruppi = Array.prototype.slice.call(document.querySelectorAll('[data-cs-gruppo]'));
  if (!selAnno || !selMese || !voci.length) return;

  // Nomi dei mesi presi dalle opzioni scritte da Hugo.
  var nomi = {};
  Array.prototype.forEach.call(selMese.options, function (o) {
    if (o.value) nomi[o.value] = o.textContent;
  });

  function mesiDi(anno) {
    var visti = {};
    voci.forEach(function (v) {
      if (!anno || v.getAttribute('data-anno') === anno) visti[v.getAttribute('data-mese')] = true;
    });
    return Object.keys(visti).sort();
  }

  function riempiMesi(anno, scelto) {
    var mesi = mesiDi(anno);
    while (selMese.options.length > 1) selMese.remove(1);
    mesi.forEach(function (m) {
      var o = document.createElement('option');
      o.value = m;
      o.textContent = nomi[m] || m;
      selMese.appendChild(o);
    });
    selMese.value = mesi.indexOf(scelto) >= 0 ? scelto : '';
  }

  function conta(n) {
    return n === 1 ? '1 comunicato' : n + ' comunicati';
  }

  function aggiornaIndirizzo(anno, mese) {
    try {
      var url = new URL(window.location.href);
      if (anno) url.searchParams.set('anno', anno); else url.searchParams.delete('anno');
      if (mese) url.searchParams.set('mese', mese); else url.searchParams.delete('mese');
      window.history.replaceState(null, '', url.pathname + url.search + url.hash);
    } catch (e) { /* indirizzo non aggiornabile: il filtro funziona lo stesso */ }
  }

  function applica() {
    var anno = selAnno.value;
    var mese = selMese.value;
    var n = 0;
    voci.forEach(function (v) {
      var ok = (!anno || v.getAttribute('data-anno') === anno) &&
               (!mese || v.getAttribute('data-mese') === mese);
      v.hidden = !ok;
      if (ok) n++;
    });
    gruppi.forEach(function (g) {
      g.hidden = !g.querySelector('.cs-voce:not([hidden])');
    });
    var periodo = '';
    if (mese && anno) periodo = (nomi[mese] || mese).toLowerCase() + ' ' + anno;
    else if (anno) periodo = 'anno ' + anno;
    else if (mese) periodo = (nomi[mese] || mese).toLowerCase() + ', tutti gli anni';
    var testo;
    if (!periodo) testo = conta(n) + ' in tutto.';
    else if (!n) testo = 'Nessun comunicato in questo periodo (' + periodo + ').';
    else testo = conta(n) + ' – ' + periodo + '.';
    if (esito) esito.textContent = testo;
    aggiornaIndirizzo(anno, mese);
  }

  // Stato iniziale dall'indirizzo, se valido.
  var annoIniziale = '';
  var meseIniziale = '';
  try {
    var q = new URLSearchParams(window.location.search);
    annoIniziale = q.get('anno') || '';
    meseIniziale = q.get('mese') || '';
  } catch (e) { /* browser senza URLSearchParams: si parte da tutti */ }
  var anniValidi = Array.prototype.map.call(selAnno.options, function (o) { return o.value; });
  if (anniValidi.indexOf(annoIniziale) < 0) annoIniziale = '';
  selAnno.value = annoIniziale;
  riempiMesi(annoIniziale, meseIniziale);

  selAnno.addEventListener('change', function () {
    riempiMesi(selAnno.value, selMese.value);
    applica();
  });
  selMese.addEventListener('change', applica);
  if (azzera) {
    azzera.addEventListener('click', function () {
      selAnno.value = '';
      riempiMesi('', '');
      applica();
    });
  }

  box.hidden = false;
  applica();
})();
