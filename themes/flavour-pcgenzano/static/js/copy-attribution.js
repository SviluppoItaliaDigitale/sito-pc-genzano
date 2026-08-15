/* ============================================================
   ATTRIBUZIONE AUTOMATICA AL COPIA v1.0
   Tutela della proprietà intellettuale dei contenuti (CC BY 4.0,
   come dichiarato in /note-legali/): quando l'utente copia più di
   120 caratteri di testo dalla pagina, alla clipboard viene
   appesa la fonte con URL e licenza.

   Garanzie:
   - Mai bloccare la copia: qualunque errore → comportamento nativo.
   - Non si attiva dentro input, textarea, contenteditable, pre/code
     o elementi con data-no-attribution (inclusa la textarea nascosta
     del fallback execCommand di share.js).
   - I pulsanti "Copia link" (share.js, condividi-cartina.js, ecc.)
     usano navigator.clipboard.writeText, che NON passa dall'evento
     `copy`: continuano a copiare solo l'URL pulito.
   - Preserva la versione text/html della selezione (per chi incolla
     in editor rich text) aggiungendo la fonte come <p> finale.
   - Zero DOM, zero ARIA, zero impatto su screen reader.
   ============================================================ */
(function () {
  'use strict';

  var SOGLIA = 120; // caratteri minimi di selezione per l'attribuzione
  var FONTE = 'Fonte: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma';
  var LICENZA = 'licenza CC BY 4.0 (attribuzione obbligatoria)';
  var LICENZA_URL = 'https://creativecommons.org/licenses/by/4.0/';

  // true se il nodo (o un suo antenato) è un contesto in cui la copia
  // non va alterata.
  function nodoEscluso(node) {
    if (!node) return false;
    var el = node.nodeType === 1 ? node : node.parentElement;
    if (!el) return false;
    if (el.isContentEditable) return true;
    if (!el.closest) return false;
    return !!el.closest('input, textarea, [contenteditable=""], [contenteditable="true"], pre, code, [data-no-attribution]');
  }

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  document.addEventListener('copy', function (event) {
    try {
      var sel = window.getSelection ? window.getSelection() : null;
      if (!sel || sel.isCollapsed || sel.rangeCount === 0) return;

      if (nodoEscluso(event.target) ||
          nodoEscluso(sel.anchorNode) ||
          nodoEscluso(sel.focusNode)) return;

      var testo = sel.toString();
      if (!testo || testo.length <= SOGLIA) return;

      if (!event.clipboardData ||
          typeof event.clipboardData.setData !== 'function') return;

      // URL della pagina senza parametri di query (l'hash resta:
      // identifica contenuti come /cruscotto/terremoto/#<id>).
      var url = location.origin + location.pathname + location.hash;

      var blocco = '\n\n—\n' + FONTE + '\n' +
                   url + ' — ' + LICENZA;

      // Versione HTML della selezione originale, se ricostruibile.
      var html = '';
      try {
        var contenitore = document.createElement('div');
        for (var i = 0; i < sel.rangeCount; i++) {
          contenitore.appendChild(sel.getRangeAt(i).cloneContents());
        }
        html = contenitore.innerHTML;
      } catch (errHtml) {
        html = '';
      }

      event.preventDefault();
      event.clipboardData.setData('text/plain', testo + blocco);

      if (html) {
        try {
          var fonteHtml = '<p>—<br>' + escapeHtml(FONTE) + '<br>' +
                          '<a href="' + escapeHtml(url) + '">' + escapeHtml(url) + '</a>' +
                          ' — <a href="' + LICENZA_URL + '">' + escapeHtml(LICENZA) + '</a></p>';
          event.clipboardData.setData('text/html', html + fonteHtml);
        } catch (errSet) { /* la versione text/plain è già in clipboard */ }
      }
    } catch (err) {
      // Qualunque errore: nessun preventDefault già chiamato a monte
      // dei setData → la copia nativa procede normalmente.
    }
  });
})();
