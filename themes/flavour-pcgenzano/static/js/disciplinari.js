/* Catalogo dei disciplinari DOP, IGP e STG (/cucina-emergenza/disciplinari/): ricerca per nome,
   regione e tipo di prodotto. Senza JavaScript il catalogo resta intero, diviso per tipo di prodotto.
   La scelta resta nell'indirizzo (?q=…&regione=…&tipo=…), così un elenco filtrato si può condividere.
   Sintassi entro ECMAScript 2018 (scripts/check-sintassi-js.cjs). */
(function () {
  'use strict';
  var filtri = document.querySelector('[data-disc="filtri"]');
  if (!filtri) return;
  var cerca = document.getElementById('disc-cerca');
  var regione = document.getElementById('disc-regione');
  var gruppo = document.getElementById('disc-gruppo');
  var conteggio = filtri.querySelector('[data-disc="conteggio"]');
  var azzera = filtri.querySelector('[data-disc="azzera"]');
  var nessuno = document.querySelector('[data-disc="nessuno"]');
  var blocchi = Array.prototype.slice.call(document.querySelectorAll('[data-disc-gruppo]'));
  if (!cerca || !regione || !gruppo || !conteggio || !blocchi.length) return;

  function norm(t) {
    return String(t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }

  var voci = [];
  blocchi.forEach(function (blocco) {
    var id = blocco.getAttribute('data-disc-gruppo');
    Array.prototype.forEach.call(blocco.querySelectorAll('.disc-voce'), function (li) {
      voci.push({
        li: li,
        gruppo: id,
        testo: norm(li.getAttribute('data-t')),
        regioni: (li.getAttribute('data-r') || '').split('|')
      });
    });
  });

  function haOpzione(select, valore) {
    return Array.prototype.some.call(select.options, function (o) { return o.value === valore; });
  }

  /* Titolo del gruppo (h2 prima del blocco) e sua voce nell'indice «In questa pagina». */
  function mostraGruppo(blocco, visibile) {
    blocco.hidden = !visibile;
    var titolo = blocco.previousElementSibling;
    if (titolo && /^H[2-3]$/.test(titolo.tagName)) {
      titolo.hidden = !visibile;
      if (titolo.id) {
        Array.prototype.forEach.call(document.querySelectorAll('a[href="#' + titolo.id + '"]'), function (a) {
          var li = a.closest ? a.closest('li') : null;
          if (li) li.hidden = !visibile;
        });
      }
    }
  }

  /* Il conteggio è una regione con role="status": si aggiorna poco dopo l'ultima scelta, così chi usa uno
     screen reader sente un solo annuncio. Al caricamento («subito») si scrive prima di mostrare i filtri,
     perché la pagina non parli da sola. */
  var attesa = null;
  function annuncia(n, subito) {
    var tot = voci.length;
    var testo = n === tot ? tot + ' prodotti.' : n + (n === 1 ? ' prodotto' : ' prodotti') + ' su ' + tot + '.';
    window.clearTimeout(attesa);
    if (subito) { conteggio.textContent = testo; return; }
    attesa = window.setTimeout(function () { conteggio.textContent = testo; }, 250);
  }

  function scriviIndirizzo() {
    if (!window.history || !window.history.replaceState || !window.URLSearchParams) return;
    var p = new URLSearchParams(window.location.search);
    [['q', cerca.value.trim()], ['regione', regione.value], ['tipo', gruppo.value]].forEach(function (c) {
      if (c[1]) p.set(c[0], c[1]); else p.delete(c[0]);
    });
    var s = p.toString();
    try {
      window.history.replaceState(null, '', window.location.pathname + (s ? '?' + s : '') + window.location.hash);
    } catch (e) { /* in un file locale o in una cornice l'indirizzo non si cambia: il filtro vale lo stesso */ }
  }

  function filtra(subito) {
    var parole = norm(cerca.value).split(' ').filter(Boolean);
    var r = regione.value;
    var g = gruppo.value;
    var n = 0;
    var vivi = {};
    voci.forEach(function (v) {
      var si = (!g || v.gruppo === g) && (!r || v.regioni.indexOf(r) >= 0) &&
        parole.every(function (p) { return v.testo.indexOf(p) >= 0; });
      v.li.hidden = !si;
      if (si) { n++; vivi[v.gruppo] = true; }
    });
    blocchi.forEach(function (blocco) { mostraGruppo(blocco, !!vivi[blocco.getAttribute('data-disc-gruppo')]); });
    if (nessuno) nessuno.hidden = n > 0;
    if (azzera) azzera.hidden = !(parole.length || r || g);
    annuncia(n, subito === true);
    scriviIndirizzo();
  }

  if (window.URLSearchParams) {
    var iniziali = new URLSearchParams(window.location.search);
    if (iniziali.get('q')) cerca.value = iniziali.get('q').slice(0, 80);
    if (iniziali.get('regione') && haOpzione(regione, iniziali.get('regione'))) regione.value = iniziali.get('regione');
    if (iniziali.get('tipo') && haOpzione(gruppo, iniziali.get('tipo'))) gruppo.value = iniziali.get('tipo');
  }

  cerca.addEventListener('input', function () { filtra(); });
  regione.addEventListener('change', function () { filtra(); });
  gruppo.addEventListener('change', function () { filtra(); });
  if (azzera) {
    azzera.addEventListener('click', function () {
      cerca.value = '';
      regione.value = '';
      gruppo.value = '';
      filtra();
      cerca.focus();
    });
  }
  filtra(true);
  filtri.hidden = false;
})();
