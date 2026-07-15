/* ============================================================
   HOME-CONTATORI v1.0 — contatori animati del hero homepage.
   Estratto da layouts/index.html il 15/07/2026 (audit esterno:
   troppa logica inline nel template).
   Il valore finale è già nell'HTML (SEO/a11y/no-JS); con
   prefers-reduced-motion non si anima affatto.
   ============================================================ */
(function () {
  'use strict';
  var counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      var target = parseInt(el.getAttribute('data-count'), 10);
      var suffix = (target === 20 || target === 10 ? '+' : '');
      var start = 0, step = Math.ceil(target / 50);
      el.textContent = '0' + suffix;
      var timer = setInterval(function () {
        start += step;
        if (start >= target) { start = target; clearInterval(timer); }
        el.textContent = start + suffix;
      }, 30);
      obs.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(function (c) { obs.observe(c); });
})();
