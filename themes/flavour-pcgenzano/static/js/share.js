/* Share buttons v1.0 — Copy Link + Web Share API
 * Solo API native del browser. Nessun tracker, nessun script di terze parti.
 * Vedi MANUALE-SITO.md Parte 4.x per regola operativa. */
(function () {
  'use strict';

  // ── Copy Link ──────────────────────────────────────────────
  // Bottone .share-copy: copia data-share-url negli appunti.
  // Feedback visivo: classe .copied + cambio icona/aria-label per 2 secondi.
  document.querySelectorAll('.share-copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-share-url') || window.location.href;
      var done = function () {
        btn.classList.add('copied');
        var icon = btn.querySelector('i');
        var prevClass = icon ? icon.className : '';
        if (icon) icon.className = 'bi bi-check2';
        var prevLabel = btn.getAttribute('aria-label');
        btn.setAttribute('aria-label', 'Link copiato negli appunti');
        setTimeout(function () {
          btn.classList.remove('copied');
          if (icon) icon.className = prevClass;
          if (prevLabel) btn.setAttribute('aria-label', prevLabel);
        }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, function () {
          // Fallback se Clipboard API fallisce (HTTP non sicuro o policy)
          fallbackCopy(url, done);
        });
      } else {
        fallbackCopy(url, done);
      }
    });
  });

  function fallbackCopy(text, onDone) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      if (onDone) onDone();
    } catch (e) {
      // niente da fare
    }
    document.body.removeChild(ta);
  }

  // ── Web Share API nativa ──────────────────────────────────
  // Bottone .share-native: visibile solo se il browser supporta navigator.share
  // (di solito mobile). Apre il selettore di app del sistema operativo.
  document.querySelectorAll('.share-native').forEach(function (btn) {
    if (!navigator.share) {
      btn.style.display = 'none';
      return;
    }
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-share-url') || window.location.href;
      var title = btn.getAttribute('data-share-title') || document.title;
      navigator.share({ title: title, url: url }).catch(function (err) {
        // AbortError = utente ha annullato, non è un errore reale
        if (err && err.name !== 'AbortError') {
          console.error('Share fallita:', err);
        }
      });
    });
  });
})();
