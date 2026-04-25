/*
 * Widget esterni click-to-load (Windy, INGV, futuri).
 * Pattern privacy-by-design: iframe caricato solo dopo esplicita
 * azione dell'utente. Uso class selector (no ID) per supportare
 * più istanze dello stesso widget in pagine diverse o nella
 * stessa pagina senza duplicati di ID.
 *
 * Dopo il caricamento, una toolbar sopra l'iframe espone un bottone
 * "Chiudi mappa": riporta al placeholder originale, indispensabile
 * su mobile dove l'iframe altrimenti cattura il touch e l'utente
 * non riesce più a scrollare la pagina.
 */
(function () {
  'use strict';

  var placeholders = document.querySelectorAll('.ext-widget-placeholder');
  if (!placeholders.length) return;

  placeholders.forEach(function (ph) {
    // Salviamo l'HTML originale per poterlo ripristinare al "Chiudi"
    var originale = ph.innerHTML;
    var classiOriginali = ph.className;

    bindLoadButton(ph, originale, classiOriginali);
  });

  function bindLoadButton(ph, originale, classiOriginali) {
    var btn = ph.querySelector('.ext-widget-load-btn');
    if (!btn) return;

    btn.addEventListener('click', function () {
      caricaIframe(ph, originale, classiOriginali);
    });
  }

  function caricaIframe(ph, originale, classiOriginali) {
    var src = ph.getAttribute('data-widget-src');
    var title = ph.getAttribute('data-widget-title') || 'Contenuto esterno';
    if (!src) return;

    // Toolbar con bottone "Chiudi mappa"
    var toolbar = document.createElement('div');
    toolbar.className = 'ext-widget-toolbar';
    var titoloSpan = document.createElement('span');
    titoloSpan.className = 'ext-widget-toolbar-title';
    titoloSpan.textContent = title;
    var chiudiBtn = document.createElement('button');
    chiudiBtn.type = 'button';
    chiudiBtn.className = 'ext-widget-close-btn';
    chiudiBtn.setAttribute('aria-label', 'Chiudi la mappa e torna all\'anteprima');
    chiudiBtn.innerHTML = '<i class="bi bi-x-lg" aria-hidden="true"></i> <span>Chiudi mappa</span>';
    toolbar.appendChild(titoloSpan);
    toolbar.appendChild(chiudiBtn);

    // Iframe
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
    ph.appendChild(toolbar);
    ph.appendChild(iframe);

    // Sposta il focus sul bottone Chiudi (esce facilmente da tastiera)
    chiudiBtn.focus();

    chiudiBtn.addEventListener('click', function () {
      // Ripristina lo stato originale
      ph.className = classiOriginali;
      ph.innerHTML = originale;
      // Ri-collega il listener "Carica"
      bindLoadButton(ph, originale, classiOriginali);
      // Sposta il focus al bottone "Carica" del placeholder ricreato
      var btn = ph.querySelector('.ext-widget-load-btn');
      if (btn) btn.focus();
      // Scroll verso il widget per mantenere il contesto
      ph.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }
})();
