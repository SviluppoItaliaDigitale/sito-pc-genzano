/* Indice di pagina: evidenzia la voce della sezione visibile mentre si scorre
   (scrollspy). Nessuna dipendenza: scroll listener con throttle rAF. */
(function () {
  'use strict';
  var idx = document.querySelector('.page-index');
  if (!idx) return;
  var links = [].slice.call(idx.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  var targets = [];
  links.forEach(function (a) {
    var id = (a.getAttribute('href') || '').replace(/^#/, '');
    var el = id && document.getElementById(id);
    if (el) targets.push({ id: id, el: el, link: a });
  });
  if (!targets.length) return;

  var attivo = null;
  function setActive(id) {
    if (id === attivo) return;
    attivo = id;
    targets.forEach(function (t) {
      var on = t.id === id;
      t.link.classList.toggle('active', on);
      if (on) t.link.setAttribute('aria-current', 'true');
      else t.link.removeAttribute('aria-current');
    });
  }

  var ticking = false;
  function aggiorna() {
    ticking = false;
    var off = 110; // sotto la navbar
    var cur = targets[0];
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].el.getBoundingClientRect().top <= off) cur = targets[i];
      else break;
    }
    // se siamo in fondo alla pagina, attiva l'ultima voce
    if ((window.innerHeight + window.scrollY) >= (document.body.offsetHeight - 4)) {
      cur = targets[targets.length - 1];
    }
    if (cur) setActive(cur.id);
  }
  function onScroll() {
    if (!ticking) { ticking = true; window.requestAnimationFrame(aggiorna); }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  aggiorna();
})();
