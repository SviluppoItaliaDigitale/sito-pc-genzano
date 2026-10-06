/* ============================================================
   I MIEI CONTENUTI v1.0 (06/10/2026)
   Pagine salvate dal cittadino, senza registrazione: l'elenco vive
   solo nel browser (localStorage, chiave pcgenzano-miei-contenuti)
   e non viene mai inviato al sito né a terzi.
   - pulsante .btn-salva-pagina (partial page-tools.html): salva o
     toglie la pagina corrente; resta nascosto se il browser non
     permette di salvare (navigazione privata con memoria bloccata);
   - elenco #miei-contenuti-elenco (pagina /i-miei-contenuti/):
     link, data di salvataggio, pulsante «Togli», «Togli tutto».
   ============================================================ */
(function () {
  'use strict';

  var CHIAVE = 'pcgenzano-miei-contenuti';
  var MASSIMO = 200;

  function leggi() {
    try {
      var v = JSON.parse(localStorage.getItem(CHIAVE) || '[]');
      return Array.isArray(v) ? v.filter(function (x) { return x && typeof x.p === 'string'; }) : [];
    } catch (e) { return []; }
  }
  function scrivi(lista) {
    try { localStorage.setItem(CHIAVE, JSON.stringify(lista.slice(0, MASSIMO))); return true; }
    catch (e) { return false; }
  }
  function memoriaDisponibile() {
    try { localStorage.setItem(CHIAVE + '-prova', '1'); localStorage.removeItem(CHIAVE + '-prova'); return true; }
    catch (e) { return false; }
  }
  function indice(lista, p) {
    for (var i = 0; i < lista.length; i++) if (lista[i].p === p) return i;
    return -1;
  }
  function avvisa(titolo, testo) {
    if (window.pcNotifica) window.pcNotifica(titolo, testo, 'success');
  }

  /* ── Pulsante sulle pagine ── */
  function preparaPulsante(btn) {
    var p = location.pathname;
    var testo = btn.querySelector('.btn-salva-testo');
    var icona = btn.querySelector('.bi');
    var link = document.querySelector('.link-miei-contenuti');
    function aggiorna() {
      var lista = leggi();
      var salvata = indice(lista, p) !== -1;
      testo.textContent = salvata ? 'Togli dai miei contenuti' : 'Salva tra i miei contenuti';
      icona.className = 'bi ' + (salvata ? 'bi-bookmark-check-fill' : 'bi-bookmark') + ' me-1';
      if (link) link.hidden = lista.length === 0;
    }
    btn.addEventListener('click', function () {
      var lista = leggi();
      var i = indice(lista, p);
      if (i === -1) {
        lista.unshift({
          p: p,
          t: btn.getAttribute('data-titolo') || document.title,
          s: btn.getAttribute('data-sezione') || '',
          d: new Date().toISOString().slice(0, 10)
        });
        if (scrivi(lista)) avvisa('Pagina salvata', 'La trovi in «I miei contenuti», solo su questo dispositivo.');
      } else {
        lista.splice(i, 1);
        if (scrivi(lista)) avvisa('Pagina tolta', 'Non è più tra i tuoi contenuti.');
      }
      aggiorna();
    });
    btn.hidden = false;
    aggiorna();
  }

  /* ── Elenco nella pagina /i-miei-contenuti/ ── */
  function dataLeggibile(iso) {
    var d = new Date(iso + 'T12:00:00');
    if (isNaN(d)) return '';
    return d.toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' });
  }
  function preparaElenco(box) {
    var vuoto = document.getElementById('miei-contenuti-vuoto');
    var tuttoBtn = document.getElementById('miei-contenuti-togli-tutto');
    var stato = document.getElementById('miei-contenuti-stato');
    function disegna() {
      var lista = leggi();
      box.textContent = '';
      vuoto.hidden = lista.length > 0;
      tuttoBtn.hidden = lista.length === 0;
      lista.forEach(function (v) {
        var li = document.createElement('li');
        li.className = 'miei-contenuti-voce';
        var a = document.createElement('a');
        a.href = v.p;
        a.textContent = v.t || v.p;
        var info = document.createElement('span');
        info.className = 'miei-contenuti-info';
        var parti = [];
        if (v.s) parti.push(v.s);
        if (v.d) parti.push('salvata il ' + dataLeggibile(v.d));
        info.textContent = parti.join(' · ');
        var togli = document.createElement('button');
        togli.type = 'button';
        togli.className = 'btn btn-sm btn-outline-primary';
        togli.textContent = 'Togli';
        togli.setAttribute('aria-label', 'Togli «' + (v.t || v.p) + '» dai miei contenuti');
        togli.addEventListener('click', function () {
          var l = leggi(); var i = indice(l, v.p);
          if (i !== -1) { l.splice(i, 1); scrivi(l); }
          stato.textContent = '«' + (v.t || v.p) + '» tolta dai tuoi contenuti.';
          disegna();
          var primo = box.querySelector('a') || document.getElementById('miei-contenuti-titolo');
          if (primo) primo.focus();
        });
        var testo = document.createElement('div');
        testo.appendChild(a);
        testo.appendChild(info);
        li.appendChild(testo);
        li.appendChild(togli);
        box.appendChild(li);
      });
    }
    tuttoBtn.addEventListener('click', function () {
      if (!window.confirm('Vuoi togliere tutte le pagine salvate da questo dispositivo?')) return;
      scrivi([]);
      stato.textContent = 'Hai tolto tutte le pagine salvate.';
      disegna();
      // il pulsante premuto ora è nascosto: il fuoco va al titolo dell'elenco
      var titolo = document.getElementById('miei-contenuti-titolo');
      if (titolo) titolo.focus();
    });
    if (!memoriaDisponibile()) {
      vuoto.textContent = 'Questo browser non permette di salvare pagine (succede, per esempio, in navigazione privata). Puoi usare i preferiti del browser.';
      vuoto.hidden = false;
      return;
    }
    disegna();
    window.addEventListener('storage', function (e) { if (e.key === CHIAVE) disegna(); });
  }

  function avvia() {
    if (!memoriaDisponibile()) {
      var e = document.getElementById('miei-contenuti-elenco');
      if (e) preparaElenco(e);
      return;
    }
    var btn = document.querySelector('.btn-salva-pagina');
    if (btn) preparaPulsante(btn);
    var box = document.getElementById('miei-contenuti-elenco');
    if (box) preparaElenco(box);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
