/* Galleria/carosello foto: avanzamento manuale (prev/next + scroll/tocco).
   Nessun autoplay (WCAG 2.2.2). Idempotente su più gallerie nella pagina.
   - contatore "n / N" fra le due frecce
   - i comandi spariscono (classe .galleria-statica) quando tutte le slide
     sono già visibili e non c'è nulla da scorrere. */
(function () {
  'use strict';
  function initGalleria(g) {
    if (g.dataset.gInit) return;
    g.dataset.gInit = '1';
    var track = g.querySelector('.galleria-track');
    var prev = g.querySelector('[data-galleria="prev"]');
    var next = g.querySelector('[data-galleria="next"]');
    if (!track || !prev || !next) return;
    var count = g.querySelector('[data-galleria-count]');
    var figs = track.querySelectorAll('figure');
    var totale = figs.length;
    function passo() {
      var fig = track.querySelector('figure');
      return fig ? fig.getBoundingClientRect().width + 10 : track.clientWidth * 0.9;
    }
    function indiceCorrente() {
      if (totale <= 1) return 0;
      var i = Math.round(track.scrollLeft / passo());
      if (i < 0) i = 0;
      if (i > totale - 1) i = totale - 1;
      return i;
    }
    function aggiorna() {
      var max = track.scrollWidth - track.clientWidth - 2;
      // niente da scorrere: nascondi del tutto i comandi
      var statica = max <= 2;
      g.classList.toggle('galleria-statica', statica);
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
      if (count) count.textContent = (indiceCorrente() + 1) + ' / ' + totale;
    }
    prev.addEventListener('click', function () { track.scrollBy({ left: -passo(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: passo(), behavior: 'smooth' }); });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(aggiorna); }, { passive: true });
    window.addEventListener('resize', aggiorna, { passive: true });
    aggiorna();
  }
  function init() {
    [].forEach.call(document.querySelectorAll('.galleria'), initGalleria);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
