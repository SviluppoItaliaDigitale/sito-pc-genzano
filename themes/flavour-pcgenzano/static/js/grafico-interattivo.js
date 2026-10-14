/* Grafici interattivi dello shortcode grafico-interattivo (14/10/2026).
   Barre: i pulsanti cambiano la misura mostrata e lo annunciano a voce.
   Calendario: un solo punto di tabulazione; frecce, Inizio e Fine spostano il
   giorno scelto, mouse e dito lo scelgono; il dettaglio del giorno è scritto
   sotto il calendario. Senza questo script il grafico resta leggibile. */
(function () {
  'use strict';

  function numero(v) { return String(v).replace('.', ','); }

  function barre(ul) {
    var misure;
    try { misure = JSON.parse(ul.getAttribute('data-gi-barre')); } catch (e) { return; }
    var fig = ul.closest('.gi');
    var gruppo = fig.querySelector('.gi-misure');
    var annuncio = fig.querySelector('.gi-annuncio');
    if (!gruppo || misure.length < 2) return;
    gruppo.hidden = false;
    var righe = ul.querySelectorAll('.gi-riga');
    var pulsanti = gruppo.querySelectorAll('.gi-misura');

    function mostra(indice) {
      var m = misure[indice];
      var max = Math.max.apply(null, m.valori) || 1;
      for (var i = 0; i < righe.length; i++) {
        var v = m.valori[i];
        righe[i].querySelector('.gi-barra').style.width = (v / max * 100) + '%';
        righe[i].querySelector('.gi-valore').innerHTML = '';
        var forte = document.createElement('strong');
        forte.textContent = numero(v);
        righe[i].querySelector('.gi-valore').appendChild(forte);
        righe[i].querySelector('.gi-valore').appendChild(document.createTextNode(' ' + (v === 1 && m.unita1 ? m.unita1 : m.unita)));
      }
      for (var j = 0; j < pulsanti.length; j++) {
        pulsanti[j].setAttribute('aria-pressed', j === indice ? 'true' : 'false');
      }
      if (annuncio) annuncio.textContent = 'Il grafico ora mostra: ' + m.nome.toLowerCase() + '.';
    }

    gruppo.addEventListener('click', function (ev) {
      var b = ev.target.closest('.gi-misura');
      if (b) mostra(parseInt(b.getAttribute('data-indice'), 10));
    });
  }

  function calendario(cal) {
    var fig = cal.closest('.gi');
    var det = fig.querySelector('.gi-dettaglio');
    var celle = Array.prototype.slice.call(cal.querySelectorAll('.gi-cella[data-frase]'));
    if (!celle.length || !det) return;
    var corrente = -1;
    cal.tabIndex = 0;
    det.hidden = false;
    det.textContent = 'Scegli un giorno, con il mouse, con il dito o con le frecce, per leggerne il dettaglio.';

    function scegli(i) {
      if (i < 0 || i >= celle.length) return;
      if (corrente >= 0) celle[corrente].classList.remove('gi-scelta');
      corrente = i;
      celle[i].classList.add('gi-scelta');
      var f = celle[i].getAttribute('data-frase');
      det.textContent = f.charAt(0).toUpperCase() + f.slice(1) + '.';
    }

    cal.addEventListener('click', function (ev) {
      var i = celle.indexOf(ev.target);
      if (i >= 0) scegli(i);
    });
    cal.addEventListener('mouseover', function (ev) {
      var i = celle.indexOf(ev.target);
      if (i >= 0) scegli(i);
    });
    cal.addEventListener('focus', function () {
      if (corrente < 0) {
        var primo = 0;
        for (var k = 0; k < celle.length; k++) { if (!celle[k].classList.contains('gi-l0')) { primo = k; break; } }
        scegli(primo);
      }
    });
    cal.addEventListener('keydown', function (ev) {
      var passi = { ArrowDown: 1, ArrowUp: -1, ArrowRight: 7, ArrowLeft: -7 };
      var nuovo = null;
      if (ev.key in passi) nuovo = corrente + passi[ev.key];
      else if (ev.key === 'Home') nuovo = 0;
      else if (ev.key === 'End') nuovo = celle.length - 1;
      if (nuovo === null) return;
      ev.preventDefault();
      scegli(Math.max(0, Math.min(celle.length - 1, nuovo)));
    });
  }

  function avvia() {
    document.querySelectorAll('[data-gi-barre]').forEach(barre);
    document.querySelectorAll('[data-gi-cal]').forEach(calendario);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
