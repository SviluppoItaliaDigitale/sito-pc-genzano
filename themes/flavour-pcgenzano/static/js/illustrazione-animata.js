/* Illustrazioni animate (shortcode illustrazione-udl con «animazione»).
 *
 * Il disegno fermo resta sempre quello di partenza: l'animazione parte solo
 * premendo «Guarda l'animazione» e si ferma con lo stesso pulsante, che
 * rimette il disegno fermo (WCAG 2.2.2). Con «Pausa animazioni» del pannello
 * accessibilità o con il movimento ridotto del sistema il pulsante non
 * compare, e se l'animazione era partita torna il disegno fermo, anche
 * quando la preferenza cambia a pagina aperta (rule 03). Prima della stampa
 * si torna al disegno fermo. JavaScript entro ECMAScript 2018 (LIM).
 */
(function () {
  'use strict';
  var figure = document.querySelectorAll('figure[data-illustrazione-animata]');
  if (!figure.length) return;
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var radice = document.documentElement;

  function movimentoFermo() {
    return (mq && mq.matches) ||
      radice.classList.contains('a11y-pause-anim') ||
      radice.classList.contains('a11y-pause-animations');
  }

  function imposta(fig, avvia) {
    var img = fig.querySelector('img[data-animata]');
    var btn = fig.querySelector('.illustrazione-anima');
    if (!img || !btn) return;
    var acceso = fig.getAttribute('data-in-movimento') === '1';
    if (avvia === acceso) return;
    var picture = img.parentNode;
    if (avvia) {
      // la versione verticale per telefono è solo ferma: durante
      // l'animazione si toglie, così il browser usa l'immagine animata
      var source = picture.querySelector('source');
      if (source) { fig._source = source; picture.removeChild(source); }
      img.removeAttribute('loading');
      img.setAttribute('src', img.getAttribute('data-animata'));
      img.setAttribute('alt', img.getAttribute('data-alt-animata'));
    } else {
      img.setAttribute('src', img.getAttribute('data-statica'));
      img.setAttribute('alt', img.getAttribute('data-alt-statica'));
      if (fig._source) { picture.insertBefore(fig._source, img); fig._source = null; }
    }
    fig.setAttribute('data-in-movimento', avvia ? '1' : '0');
    btn.querySelector('.illustrazione-anima-testo').textContent = avvia ? "Ferma l'animazione" : "Guarda l'animazione";
    var icona = btn.querySelector('.bi');
    if (icona) icona.className = avvia ? 'bi bi-stop-fill' : 'bi bi-play-fill';
    var stato = fig.querySelector('.illustrazione-anima-stato');
    if (stato) stato.textContent = avvia ? 'Animazione avviata.' : 'Animazione fermata: torna il disegno fermo.';
  }

  function aggiorna() {
    var fermo = movimentoFermo();
    Array.prototype.forEach.call(figure, function (fig) {
      var comandi = fig.querySelector('.illustrazione-comandi');
      if (fermo) imposta(fig, false);
      if (comandi) comandi.hidden = fermo;
    });
  }

  Array.prototype.forEach.call(figure, function (fig) {
    var btn = fig.querySelector('.illustrazione-anima');
    if (!btn) return;
    btn.addEventListener('click', function () {
      imposta(fig, fig.getAttribute('data-in-movimento') !== '1');
    });
  });

  aggiorna();
  if (mq) {
    if (mq.addEventListener) mq.addEventListener('change', aggiorna);
    else if (mq.addListener) mq.addListener(aggiorna);
  }
  if (window.MutationObserver) {
    new MutationObserver(aggiorna).observe(radice, { attributes: true, attributeFilter: ['class'] });
  }
  window.addEventListener('beforeprint', function () {
    Array.prototype.forEach.call(figure, function (fig) { imposta(fig, false); });
  });
})();
