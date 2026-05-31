/* Galleria/carosello foto: avanzamento manuale (prev/next + scroll/tocco).
   Nessun autoplay (WCAG 2.2.2). Idempotente su più gallerie nella pagina. */
(function () {
  'use strict';
  function initGalleria(g) {
    if (g.dataset.gInit) return;
    g.dataset.gInit = '1';
    var track = g.querySelector('.galleria-track');
    var prev = g.querySelector('[data-galleria="prev"]');
    var next = g.querySelector('[data-galleria="next"]');
    if (!track || !prev || !next) return;
    function passo() {
      var fig = track.querySelector('figure');
      return fig ? fig.getBoundingClientRect().width + 10 : track.clientWidth * 0.9;
    }
    function aggiorna() {
      var max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
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
