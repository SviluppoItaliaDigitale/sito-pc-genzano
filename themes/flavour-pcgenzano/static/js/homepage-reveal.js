/* Homepage reveal-on-scroll — Proposta 2 enhancements home v1.0
 *
 * Aggiunge la classe .is-revealed alle card della homepage quando
 * entrano nel viewport, attivando una transizione opacity + translateY
 * definita in custom.css.
 *
 * Rispetta prefers-reduced-motion: in quel caso le card sono già
 * visibili dal CSS (opacity 1, no transform).
 *
 * Selettori coperti:
 *   - body.home-page .quick-action-card
 *   - body.home-page .card-servizio
 *   - body.home-page .card-notizia-hero
 *   - body.home-page section .card.border-danger     (rischi)
 *   - body.home-page .stat-hero-item
 */
(function () {
  if (!document.body.classList.contains('home-page')) return;

  // Se l'utente ha richiesto reduced motion, non aggiungiamo la classe
  // di partenza (il CSS lascia tutto visibile).
  var reduce = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  var selectors = [
    '.quick-action-card',
    '.card-servizio',
    '.card-notizia-hero',
    'section .card.border-danger',
    '.stat-hero-item',
    '.card-numero-utile'
  ];

  var targets = document.querySelectorAll(selectors.join(','));
  if (!targets.length) return;

  // Se il browser non supporta IntersectionObserver, lasciamo le card
  // visibili senza animazione (graceful degradation).
  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('is-revealed'); });
    return;
  }

  // Parto dallo stato "nascosto"
  targets.forEach(function (el) { el.classList.add('reveal-on-scroll'); });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-revealed');
      io.unobserve(entry.target);
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  });

  targets.forEach(function (el) { io.observe(el); });
})();
