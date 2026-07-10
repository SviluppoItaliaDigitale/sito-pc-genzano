/* ============================================================
   BARRA AVANZAMENTO LETTURA v1.0
   Riempie la barra fissa in cima al viewport (.barra-lettura)
   in proporzione a quanto corpo dell'articolo e' gia' scorso
   sopra la finestra. Il contenuto misurato e' indicato dal
   data-target del wrapper (default .article-body).

   - scroll listener passivo + requestAnimationFrame (no jank);
   - transform: scaleX sul riempimento (compositor-only, niente
     reflow);
   - aria-valuenow aggiornato solo a passi del 5% per non
     inondare gli screen reader;
   - se il contenuto misurato non esiste, la barra si nasconde.
   ============================================================ */
(function () {
  'use strict';

  var bar = document.querySelector('.barra-lettura');
  if (!bar) return;
  var fill = bar.querySelector('.barra-lettura-fill');
  var target = document.querySelector(bar.getAttribute('data-target') || '.article-body');
  if (!fill || !target) { bar.hidden = true; return; }

  var lastAria = -1;
  var ticking = false;

  function update() {
    ticking = false;
    var rect = target.getBoundingClientRect();
    var viewport = window.innerHeight || document.documentElement.clientHeight;
    var total = rect.height - viewport;
    var progress;
    if (total <= 0) {
      /* Contenuto piu' corto dello schermo: pieno appena visibile. */
      progress = rect.top < viewport ? 1 : 0;
    } else {
      progress = -rect.top / total;
    }
    if (progress < 0) progress = 0;
    if (progress > 1) progress = 1;

    fill.style.transform = 'scaleX(' + progress + ')';

    var pct = Math.round(progress * 20) * 5; /* passi del 5% */
    if (pct !== lastAria) {
      lastAria = pct;
      fill.setAttribute('aria-valuenow', String(pct));
    }
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
})();
