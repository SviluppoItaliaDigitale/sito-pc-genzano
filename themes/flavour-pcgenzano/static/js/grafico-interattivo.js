/* Grafici interattivi dello shortcode grafico-interattivo (v2, 15/10/2026).
   Barre: i pulsanti cambiano la misura; nel grafico dei mesi ogni mese è un
   pulsante che filtra gli altri grafici dello stesso file di dati (calendario
   e barre ricalcolate dalle singole uscite). Calendario: un solo punto di
   tabulazione (frecce, Inizio, Fine), mouse e dito scelgono il giorno; il
   dettaglio elenca le uscite del giorno e l'articolo che le racconta; il
   cursore «Rivivi la campagna» scorre i giorni. Ogni grafico ha «Scarica i
   dati» (CSV). Senza questo script i grafici restano leggibili. */
(function () {
  'use strict';

  var MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
  var SETTIMANA = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
  var archivi = {};

  function numero(v) { return String(v).replace('.', ','); }
  function maiuscola(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function minuscola(s) { return s.charAt(0).toLowerCase() + s.slice(1); }
  function lista(nodi) { return Array.prototype.slice.call(nodi); }
  function movimentoRidotto() {
    return (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) ||
      document.documentElement.classList.contains('a11y-pause-anim');
  }
  function dataLunga(iso) {
    var p = iso.split('-');
    var g = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])).getUTCDay();
    return SETTIMANA[g] + ' ' + (+p[2]) + ' ' + MESI[+p[1] - 1];
  }
  function durata(ore) {
    var mezze = Math.round(ore * 2) / 2;
    if (mezze < 0.5) return "meno di mezz'ora";
    if (mezze === 0.5) return "circa mezz'ora";
    var intere = Math.floor(mezze);
    return 'circa ' + (intere === 1 ? "un'ora" : intere + ' ore') + (mezze > intere ? ' e mezza' : '');
  }
  function fascia(f) {
    if (/^prima/i.test(f) || /^dopo/i.test(f)) return minuscola(f);
    var p = f.split('–');
    return p.length === 2 ? 'tra le ' + p[0] + ' e le ' + p[1] : f;
  }
  function elenco(nomi) {
    return nomi.length < 2 ? nomi.join('') : nomi.slice(0, -1).join(', ') + ' e ' + nomi[nomi.length - 1];
  }
  function quante(n, uno, molti) { return n + ' ' + (n === 1 ? uno : molti); }

  function archivio(chiave) {
    if (!(chiave in archivi)) {
      var el = document.querySelector('script.gi-dati[data-gi-chiave="' + chiave + '"]');
      var dati = null;
      if (el) { try { dati = JSON.parse(el.textContent); } catch (e) { dati = null; } }
      archivi[chiave] = dati && dati.interventi ? dati : null;
    }
    return archivi[chiave];
  }

  function filtra(chiave, mese, etichetta) {
    document.dispatchEvent(new CustomEvent('gi:filtro', { detail: { chiave: chiave, mese: mese, etichetta: etichetta } }));
  }

  /* Avviso «Stai guardando solo …» con il pulsante per tornare a tutta la campagna. */
  function avvisoFiltro(fig) {
    var p = document.createElement('p');
    p.className = 'gi-filtro';
    p.hidden = true;
    var testo = document.createElement('span');
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'gi-azzera';
    b.textContent = 'Mostra tutta la campagna';
    p.appendChild(testo);
    p.appendChild(document.createTextNode(' '));
    p.appendChild(b);
    var titolo = fig.querySelector('.gi-titolo');
    titolo.parentNode.insertBefore(p, titolo.nextSibling);
    b.addEventListener('click', function () {
      filtra(fig.getAttribute('data-gi-chiave'), null, null);
      titolo.tabIndex = -1;
      titolo.focus();
    });
    return function (etichetta) {
      testo.textContent = '';
      if (!etichetta) { p.hidden = true; return; }
      testo.appendChild(document.createTextNode('Stai guardando solo '));
      var forte = document.createElement('strong');
      forte.textContent = etichetta;
      testo.appendChild(forte);
      testo.appendChild(document.createTextNode('.'));
      p.hidden = false;
    };
  }

  function scaricaCsv(nome, righe) {
    var testo = '﻿' + righe.map(function (r) {
      return r.map(function (c) {
        var s = String(c);
        return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
      }).join(',');
    }).join('\r\n') + '\r\n';
    var url = URL.createObjectURL(new Blob([testo], { type: 'text/csv;charset=utf-8' }));
    var a = document.createElement('a');
    a.href = url;
    a.download = nome;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  }

  function pulsanteCsv(fig, righe) {
    var fonte = fig.querySelector('.gi-fonte');
    if (!fonte || !window.Blob || !window.URL || !URL.createObjectURL) return;
    var p = document.createElement('p');
    p.className = 'gi-azioni';
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'gi-scarica';
    b.textContent = 'Scarica i dati (CSV)';
    var nome = (fig.getAttribute('data-gi-chiave') + '-' + fig.getAttribute('data-gi-grafico')).replace(/_/g, '-') + '.csv';
    b.addEventListener('click', function () { scaricaCsv(nome, righe()); });
    p.appendChild(b);
    fonte.parentNode.insertBefore(p, fonte.nextSibling);
  }

  /* Unità di una misura per un valore: "37 interventi", "1 ora di intervento". */
  function conUnita(v, m, completa) {
    var nome = m.nome.toLowerCase();
    var u = v === 1 && m.unita1 ? m.unita1 : m.unita;
    if (completa && nome.indexOf(m.unita) === 0) u = u + nome.slice(m.unita.length);
    return numero(v) + ' ' + u;
  }

  function barre(ul) {
    var misure;
    try { misure = JSON.parse(ul.getAttribute('data-gi-barre')); } catch (e) { return; }
    var fig = ul.closest('.gi');
    var chiave = fig.getAttribute('data-gi-chiave');
    var gruppo = fig.querySelector('.gi-misure');
    var annuncio = fig.querySelector('.gi-annuncio');
    var righe = lista(ul.querySelectorAll('.gi-riga'));
    var etichette = righe.map(function (r) { return r.querySelector('.gi-etichetta').textContent.trim(); });
    var misura = 0;

    function disegna(valori, m) {
      var max = Math.max.apply(null, valori) || 1;
      righe.forEach(function (r, i) {
        r.querySelector('.gi-barra').style.width = (valori[i] / max * 100) + '%';
        var val = r.querySelector('.gi-valore');
        val.textContent = '';
        var forte = document.createElement('strong');
        forte.textContent = numero(valori[i]);
        val.appendChild(forte);
        val.appendChild(document.createTextNode(' ' + (valori[i] === 1 && m.unita1 ? m.unita1 : m.unita)));
      });
    }

    if (gruppo && misure.length > 1) {
      gruppo.hidden = false;
      var pulsanti = lista(gruppo.querySelectorAll('.gi-misura'));
      gruppo.addEventListener('click', function (ev) {
        var b = ev.target.closest('.gi-misura');
        if (!b) return;
        misura = parseInt(b.getAttribute('data-indice'), 10);
        disegna(misure[misura].valori, misure[misura]);
        pulsanti.forEach(function (p, j) { p.setAttribute('aria-pressed', j === misura ? 'true' : 'false'); });
        if (annuncio) annuncio.textContent = 'Il grafico ora mostra: ' + misure[misura].nome.toLowerCase() + '.';
      });
    }

    pulsanteCsv(fig, function () {
      var out = [['voce'].concat(misure.map(function (m) { return m.nome.toLowerCase(); }))];
      etichette.forEach(function (e, i) { out.push([e].concat(misure.map(function (m) { return m.valori[i]; }))); });
      return out;
    });

    var dati = archivio(chiave);
    if (!dati) return;

    /* Grafico dei mesi: ogni mese diventa un pulsante che filtra la pagina. */
    if (righe.every(function (r) { return r.hasAttribute('data-chiave'); })) {
      var suggerimento = document.createElement('p');
      suggerimento.className = 'gi-suggerimento';
      suggerimento.textContent = 'Scegli un mese: il calendario e gli altri grafici della pagina mostreranno solo quei giorni.';
      ul.parentNode.insertBefore(suggerimento, ul);
      var riepilogo = document.createElement('p');
      riepilogo.className = 'gi-riepilogo';
      riepilogo.setAttribute('aria-hidden', 'true');
      ul.parentNode.insertBefore(riepilogo, ul.nextSibling);
      var bottoni = righe.map(function (r, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'gi-riga-btn';
        b.setAttribute('aria-pressed', 'false');
        while (r.firstChild) b.appendChild(r.firstChild);
        var tutte = document.createElement('span');
        tutte.className = 'visually-hidden';
        tutte.id = fig.id + '-mese-' + i;
        tutte.textContent = 'In tutto: ' + misure.map(function (m) { return conUnita(m.valori[i], m, true); }).join(', ') +
          '. Premi per vedere solo questo mese negli altri grafici.';
        b.setAttribute('aria-describedby', tutte.id);
        r.appendChild(b);
        r.appendChild(tutte);
        r.classList.add('gi-riga-filtro');
        function mostraRiepilogo() {
          riepilogo.textContent = etichette[i] + ': ' + misure.map(function (m) { return conUnita(m.valori[i], m, true); }).join(', ') + '.';
        }
        b.addEventListener('mouseenter', mostraRiepilogo);
        b.addEventListener('focus', mostraRiepilogo);
        b.addEventListener('click', function () {
          var attivo = b.getAttribute('aria-pressed') === 'true';
          filtra(chiave, attivo ? null : r.getAttribute('data-chiave'), attivo ? null : minuscola(etichette[i]));
        });
        return b;
      });
      ul.addEventListener('mouseleave', function () { riepilogo.textContent = ''; });
      document.addEventListener('gi:filtro', function (ev) {
        if (ev.detail.chiave !== chiave) return;
        righe.forEach(function (r, i) {
          bottoni[i].setAttribute('aria-pressed', ev.detail.mese && r.getAttribute('data-chiave') === ev.detail.mese ? 'true' : 'false');
        });
      });
      return;
    }

    /* Barre che seguono il filtro: il campo delle uscite con le stesse voci
       (es. fascia oraria, mezzi) e gli stessi totali del grafico pubblicato. */
    if (misure.length !== 1) return;
    var campo = null;
    Object.keys(dati.interventi[0] || {}).some(function (k) {
      var conta = etichette.map(function (e) {
        return dati.interventi.filter(function (x) {
          return Array.isArray(x[k]) ? x[k].indexOf(e) >= 0 : x[k] === e;
        }).length;
      });
      if (conta.join() === misure[0].valori.join()) { campo = k; return true; }
      return false;
    });
    if (!campo) return;
    var mostraAvviso = avvisoFiltro(fig);
    document.addEventListener('gi:filtro', function (ev) {
      if (ev.detail.chiave !== chiave) return;
      var mese = ev.detail.mese;
      var scelte = dati.interventi.filter(function (x) { return !mese || x.d.indexOf(mese) === 0; });
      var valori = etichette.map(function (e) {
        return scelte.filter(function (x) {
          return Array.isArray(x[campo]) ? x[campo].indexOf(e) >= 0 : x[campo] === e;
        }).length;
      });
      disegna(valori, misure[0]);
      mostraAvviso(ev.detail.etichetta);
      if (annuncio) annuncio.textContent = mese ? 'Il grafico ora mostra ' + ev.detail.etichetta + '.' : 'Il grafico ora mostra tutta la campagna.';
    });
  }

  function calendario(cal) {
    var fig = cal.closest('.gi');
    var chiave = fig.getAttribute('data-gi-chiave');
    var dettaglio = fig.querySelector('.gi-dettaglio');
    var celle = lista(cal.querySelectorAll('.gi-cella[data-d]'));
    if (!celle.length || !dettaglio) return;
    var titoloDet = dettaglio.querySelector('.gi-det-titolo');
    var listaDet = dettaglio.querySelector('.gi-det-lista');
    var raccontoDet = dettaglio.querySelector('.gi-det-racconto');
    var dati = archivio(chiave);
    var perGiorno = {};
    if (dati) dati.interventi.forEach(function (x) { (perGiorno[x.d] = perGiorno[x.d] || []).push(x); });
    var racconti = (dati && dati.racconti) || {};
    var corrente = -1;
    cal.tabIndex = 0;
    dettaglio.hidden = false;
    pulsanteCsv(fig, function () {
      return [['giorno', 'interventi', 'ore di intervento']].concat(celle.map(function (c) {
        return [c.getAttribute('data-d'), c.getAttribute('data-n'), c.getAttribute('data-ore')];
      }));
    });
    titoloDet.textContent = 'Scegli un giorno, con il mouse, con il dito o con le frecce, per leggerne il dettaglio.';

    function scegli(i) {
      if (i < 0 || i >= celle.length) return;
      if (corrente >= 0) celle[corrente].classList.remove('gi-scelta');
      corrente = i;
      var c = celle[i];
      c.classList.add('gi-scelta');
      var d = c.getAttribute('data-d');
      var n = parseInt(c.getAttribute('data-n'), 10);
      titoloDet.textContent = maiuscola(dataLunga(d)) + ': ' +
        (n === 0 ? 'nessun intervento' : quante(n, 'intervento', 'interventi') + ', ' + numero(c.getAttribute('data-ore')) + ' ore') + '.';
      listaDet.textContent = '';
      (perGiorno[d] || []).forEach(function (x) {
        var li = document.createElement('li');
        var parti = [maiuscola(fascia(x.fascia)), durata(x.ore)];
        if (x.volontari) parti.push(quante(x.volontari, 'volontario', 'volontari'));
        if (x.mezzi && x.mezzi.length) parti.push(elenco(x.mezzi));
        li.textContent = parti.join(' · ');
        listaDet.appendChild(li);
      });
      listaDet.hidden = !listaDet.children.length;
      raccontoDet.textContent = '';
      var art = racconti[d] || [];
      art.forEach(function (a, j) {
        if (j === 0) raccontoDet.appendChild(document.createTextNode(art.length > 1 ? 'I racconti: ' : 'Il racconto: '));
        else raccontoDet.appendChild(document.createTextNode(j === art.length - 1 ? ' e ' : ', '));
        var link = document.createElement('a');
        link.href = a.u;
        link.textContent = a.t;
        raccontoDet.appendChild(link);
      });
      raccontoDet.hidden = !art.length;
    }

    /* Il passaggio del mouse mostra un'anteprima; il clic, il dito e la
       tastiera fissano il giorno, che torna quando il mouse esce dal
       calendario (così si può raggiungere il link del racconto). */
    var fissato = -1;
    cal.addEventListener('click', function (ev) { var i = celle.indexOf(ev.target); if (i >= 0) { fissato = i; scegli(i); } });
    cal.addEventListener('mouseover', function (ev) { var i = celle.indexOf(ev.target); if (i >= 0) scegli(i); });
    cal.addEventListener('mouseleave', function () { if (fissato >= 0 && fissato !== corrente) scegli(fissato); });
    cal.addEventListener('focus', function () {
      if (corrente >= 0) return;
      for (var k = 0; k < celle.length; k++) { if (celle[k].getAttribute('data-n') !== '0') { fissato = k; scegli(k); return; } }
      fissato = 0;
      scegli(0);
    });
    cal.addEventListener('keydown', function (ev) {
      var passi = { ArrowDown: 1, ArrowUp: -1, ArrowRight: 7, ArrowLeft: -7 };
      var nuovo = null;
      if (ev.key in passi) nuovo = corrente + passi[ev.key];
      else if (ev.key === 'Home') nuovo = 0;
      else if (ev.key === 'End') nuovo = celle.length - 1;
      if (nuovo === null) return;
      ev.preventDefault();
      fissato = Math.max(0, Math.min(celle.length - 1, nuovo));
      scegli(fissato);
    });

    /* Filtro per mese. */
    var numeri = fig.querySelector('.gi-sintesi-numeri');
    var numeriTutti = numeri ? numeri.textContent : '';
    var mostraAvviso = dati ? avvisoFiltro(fig) : null;
    document.addEventListener('gi:filtro', function (ev) {
      if (ev.detail.chiave !== chiave || !dati) return;
      var mese = ev.detail.mese;
      var n = 0, attivi = 0, giorni = 0;
      celle.forEach(function (c) {
        var dentro = !mese || c.getAttribute('data-d').indexOf(mese) === 0;
        c.classList.toggle('gi-fuori', !dentro);
        if (!dentro) return;
        var k = parseInt(c.getAttribute('data-n'), 10);
        giorni++;
        n += k;
        if (k > 0) attivi++;
      });
      if (numeri) numeri.textContent = mese ? maiuscola(ev.detail.etichetta) + ': ' + quante(n, 'intervento', 'interventi') + ' in ' + quante(attivi, 'giornata', 'giornate') + ' su ' + giorni + '.' : numeriTutti;
      mostraAvviso(ev.detail.etichetta);
    });

    /* Rivivi la campagna. */
    var rivivi = fig.querySelector('.gi-rivivi');
    if (!rivivi) return;
    var cursore = rivivi.querySelector('.gi-cursore');
    var play = rivivi.querySelector('.gi-play');
    var playTesto = rivivi.querySelector('.gi-play-testo');
    var playSegno = rivivi.querySelector('.gi-play-segno');
    var contatore = rivivi.querySelector('.gi-contatore');
    var cumN = [], cumOre = [], tn = 0, to = 0;
    celle.forEach(function (c) {
      tn += parseInt(c.getAttribute('data-n'), 10);
      to += parseFloat(c.getAttribute('data-ore')) || 0;
      cumN.push(tn);
      cumOre.push(Math.round(to * 10) / 10);
    });
    var timer = null;
    function posiziona(k) {
      celle.forEach(function (c, i) { c.classList.toggle('gi-dopo', i > k); });
      var testo = (k === celle.length - 1 ? 'Tutta la campagna, fino a ' : 'Fino a ') + dataLunga(celle[k].getAttribute('data-d')) + ': ' +
        quante(cumN[k], 'intervento', 'interventi') + ', ' + numero(cumOre[k]) + ' ore.';
      contatore.textContent = testo;
      cursore.setAttribute('aria-valuetext', testo);
    }
    function ferma() {
      if (!timer) return;
      clearInterval(timer);
      timer = null;
      playTesto.textContent = 'Avvia';
      playSegno.textContent = '▶';
    }
    cursore.addEventListener('input', function () { ferma(); posiziona(parseInt(cursore.value, 10)); });
    play.addEventListener('click', function () {
      if (timer) { ferma(); return; }
      var k = parseInt(cursore.value, 10);
      if (k >= celle.length - 1) k = -1;
      playTesto.textContent = 'Pausa';
      playSegno.textContent = '❚❚';
      timer = setInterval(function () {
        k++;
        cursore.value = k;
        posiziona(k);
        if (k >= celle.length - 1) ferma();
      }, 140);
    });
    document.addEventListener('visibilitychange', function () { if (document.hidden) ferma(); });
    if (movimentoRidotto()) play.hidden = true;
    rivivi.hidden = false;
    posiziona(celle.length - 1);
    window.addEventListener('beforeprint', function () {
      ferma();
      cursore.value = celle.length - 1;
      posiziona(celle.length - 1);
    });
  }

  function avvia() {
    document.querySelectorAll('[data-gi-barre]').forEach(barre);
    document.querySelectorAll('[data-gi-cal]').forEach(calendario);
    window.addEventListener('beforeprint', function () {
      Object.keys(archivi).forEach(function (k) { if (archivi[k]) filtra(k, null, null); });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
