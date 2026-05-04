/* ============================================================
   STRUMENTI DI ACCESSIBILITÀ — Toolbar utente
   Logica di apertura/chiusura dialog, persistenza preferenze
   in localStorage, applicazione classi su <html>.
   Vanilla JS, nessuna dipendenza.
   ============================================================ */
(function () {
  'use strict';

  var STORAGE_KEY = 'pcgenzano-a11y-prefs';

  // Default state
  var defaults = {
    textSize: '0',
    textAlign: 'default',
    readableFont: false,
    spacing: false,
    contrast: 'default',
    grayscale: false,
    hideImages: false,
    pauseAnimations: false,
    highlightLinks: false,
    bigCursor: false,
    hideAssistantFab: false,
    hideSosFab: false
  };

  var state = Object.assign({}, defaults);

  // ----------- Storage helpers -----------
  function load() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      var saved = JSON.parse(raw);
      if (saved && typeof saved === 'object') {
        Object.keys(defaults).forEach(function (k) {
          if (Object.prototype.hasOwnProperty.call(saved, k)) {
            state[k] = saved[k];
          }
        });
      }
    } catch (e) { /* localStorage non disponibile o JSON corrotto: usa default */ }
  }

  function save() {
    try { window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
    catch (e) { /* fallisce silenziosamente in private mode */ }
  }

  // ----------- Apply state to <html> -----------
  function applyState() {
    var html = document.documentElement;

    // Pulisco tutte le classi a11y-* esistenti
    var toRemove = [];
    for (var i = 0; i < html.classList.length; i++) {
      var c = html.classList[i];
      if (c.indexOf('a11y-') === 0) toRemove.push(c);
    }
    toRemove.forEach(function (c) { html.classList.remove(c); });

    // Testo: dimensione
    if (state.textSize === '1') html.classList.add('a11y-text-1');
    else if (state.textSize === '2') html.classList.add('a11y-text-2');
    else if (state.textSize === '3') html.classList.add('a11y-text-3');

    // Testo: allineamento
    if (state.textAlign === 'left') html.classList.add('a11y-align-left');
    else if (state.textAlign === 'justify') html.classList.add('a11y-align-justify');

    // Testo: carattere
    if (state.readableFont) html.classList.add('a11y-readable-font');

    // Testo: spaziatura
    if (state.spacing) html.classList.add('a11y-spacing');

    // Visivo: contrasto
    if (state.contrast === 'high') html.classList.add('a11y-contrast-high');
    else if (state.contrast === 'invert') html.classList.add('a11y-contrast-invert');

    // Visivo: scala di grigi
    if (state.grayscale) html.classList.add('a11y-grayscale');

    // Visivo: nascondi immagini
    if (state.hideImages) html.classList.add('a11y-hide-images');

    // Visivo: pausa animazioni
    if (state.pauseAnimations) html.classList.add('a11y-pause-animations');

    // Orientamento: evidenzia link
    if (state.highlightLinks) html.classList.add('a11y-highlight-links');

    // Orientamento: cursore grande
    if (state.bigCursor) html.classList.add('a11y-big-cursor');

    // Pulsanti flottanti: nascondi Assistente / SOS-112
    if (state.hideAssistantFab) html.classList.add('a11y-hide-assistant-fab');
    if (state.hideSosFab) html.classList.add('a11y-hide-sos-fab');
  }

  // Applica subito allo start (prima del DOM ready) per evitare flash
  load();
  applyState();

  // ----------- DOM ready -----------
  function onReady() {
    var fab = document.getElementById('a11yToolbarOpen');
    var dialog = document.getElementById('a11yDialog');
    var backdrop = document.getElementById('a11yBackdrop');
    var btnClose = document.getElementById('a11yDialogClose');
    var btnCloseFooter = document.getElementById('a11yDialogCloseFooter');
    var btnReset = document.getElementById('a11yReset');
    var statusEl = document.getElementById('a11yStatus');

    if (!fab || !dialog) return;
    // Guard idempotente: in caso di re-init (SPA navigation, chiamata
    // multipla), evitiamo di moltiplicare gli event listener su FAB,
    // bottoni segmentati, toggle e reset. Una volta wireup-ato, la
    // funzione esce subito.
    if (dialog.dataset.a11yWired === '1') return;
    dialog.dataset.a11yWired = '1';

    // Update UI controls per riflettere lo state corrente
    function syncUI() {
      // Segmented buttons
      var segs = dialog.querySelectorAll('.a11y-seg');
      segs.forEach(function (b) {
        var pref = b.getAttribute('data-pref');
        var val = b.getAttribute('data-value');
        b.setAttribute('aria-pressed', String(state[pref]) === val ? 'true' : 'false');
      });

      // Toggles
      var toggles = dialog.querySelectorAll('.a11y-toggle');
      toggles.forEach(function (b) {
        var pref = b.getAttribute('data-pref');
        var on = !!state[pref];
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
        var stateLbl = b.querySelector('.a11y-toggle-state');
        if (stateLbl) stateLbl.textContent = on ? 'On' : 'Off';
      });
    }

    function announce(msg) {
      if (!statusEl) return;
      statusEl.textContent = msg;
      // Pulisci dopo qualche secondo per non lasciare la stringa visibile
      setTimeout(function () { if (statusEl.textContent === msg) statusEl.textContent = ''; }, 2500);
    }

    // ----------- Open / Close dialog -----------
    var lastFocused = null;

    function openDialog() {
      lastFocused = document.activeElement;
      dialog.hidden = false;
      backdrop.hidden = false;
      fab.setAttribute('aria-expanded', 'true');
      syncUI();
      // Focus sul titolo (poi l'utente naviga col Tab)
      var firstFocusable = dialog.querySelector('.a11y-close');
      if (firstFocusable) firstFocusable.focus();
      document.addEventListener('keydown', onKeyDown);
    }

    function closeDialog() {
      dialog.hidden = true;
      backdrop.hidden = true;
      fab.setAttribute('aria-expanded', 'false');
      document.removeEventListener('keydown', onKeyDown);
      if (lastFocused && typeof lastFocused.focus === 'function') {
        lastFocused.focus();
      } else {
        fab.focus();
      }
    }

    function onKeyDown(e) {
      if (e.key === 'Escape') {
        e.preventDefault();
        closeDialog();
        return;
      }
      // Focus trap
      if (e.key === 'Tab') {
        var focusable = dialog.querySelectorAll(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        if (!focusable.length) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    }

    fab.addEventListener('click', openDialog);
    btnClose.addEventListener('click', closeDialog);
    btnCloseFooter.addEventListener('click', closeDialog);
    backdrop.addEventListener('click', closeDialog);

    // ----------- Handle controls -----------
    function setPref(name, value) {
      state[name] = value;
      save();
      applyState();
      syncUI();
    }

    // Segmented (radiogroup-like)
    dialog.querySelectorAll('.a11y-seg').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var pref = btn.getAttribute('data-pref');
        var val = btn.getAttribute('data-value');
        // textSize è una stringa numerica
        setPref(pref, val);
        announce('Impostazione aggiornata.');
      });
    });

    // Toggles
    dialog.querySelectorAll('.a11y-toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var pref = btn.getAttribute('data-pref');
        setPref(pref, !state[pref]);
        announce(state[pref] ? 'Attivato.' : 'Disattivato.');
      });
    });

    // Reset
    btnReset.addEventListener('click', function () {
      state = Object.assign({}, defaults);
      try { window.localStorage.removeItem(STORAGE_KEY); } catch (e) { /* */ }
      applyState();
      syncUI();
      announce('Impostazioni reimpostate.');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }
})();
