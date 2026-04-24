/*
 * Widget esterni click-to-load (Windy, INGV, futuri).
 * Pattern privacy-by-design: iframe caricato solo dopo esplicita
 * azione dell'utente. Uso class selector (no ID) per supportare
 * piu istanze dello stesso widget in paggine diverse o nella
 * stessa pagina senza duplicati di ID.
 */
(function () {
  'use strict';

  var placeholders = document.querySelectorAll('.ext-widget-placeholder');
  if (!placeholders.length) return;

  placeholders.forEach(function (ph) {
    var btn = ph.querySelector('.ext-widget-load-btn');
    if (!btn) return;

    btn.addEventListener('click', function () {
      var src = ph.getAttribute('data-widget-src');
      var title = ph.getAttribute('data-widget-title') || 'Contenuto esterno';
      if (!src) return;

      var iframe = document.createElement('iframe');
      iframe.setAttribute('src', src);
      iframe.setAttribute('title', title);
      iframe.setAttribute('loading', 'lazy');
      iframe.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
      iframe.setAttribute('allow', 'geolocation');
      iframe.setAttribute('tabindex', '0');
      iframe.className = 'ext-widget-iframe';

      ph.innerHTML = '';
      ph.classList.add('ext-widget-loaded');
      ph.appendChild(iframe);

      // Sposta il focus sull'iframe per annuncio screen reader
      iframe.focus();
    });
  });
})();
