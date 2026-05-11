/* ============================================================
   STRUMENTI DI ACCESSIBILITÀ — Toolbar utente
   Logica di apertura/chiusura dialog, persistenza preferenze
   in localStorage, applicazione classi su <html>.
   Vanilla JS, nessuna dipendenza.
   ============================================================ */
(function () {
  'use strict';

  var STORAGE_KEY = 'pcgenzano-a11y-prefs';
  // Chiave già usata dal partial `leggi-ad-alta-voce.html` (pill inline) —
  // qui leggiamo/scriviamo lo stesso valore per sync bidirezionale.
  var TTS_RATE_KEY = 'pcgenzano-tts-rate';
  var TTS_RATE_EVENT = 'pcgenzano:tts-rate-change';
  var TTS_RATES_ALLOWED = ['0.75', '0.95', '1.15'];

  // Default state
  var defaults = {
    textSize: '0',
    textAlign: 'default',
    // fontFamily ha tre valori: 'default' | 'readable' | 'dyslexic'.
    // Sostituisce il vecchio bool `readableFont` (vedi migrazione in load()).
    fontFamily: 'default',
    spacing: false,
    // readingMode (Sera 2): macro-toggle che attiva spaziatura + sfondo crema
    // + max-width + align-left + (se fontFamily=='default') forza 'readable'.
    readingMode: false,
    contrast: 'default',
    grayscale: false,
    hideImages: false,
    pauseAnimations: false,
    highlightLinks: false,
    bigCursor: false,
    hideAssistantFab: false,
    hideSosFab: false,
    hideTranslateButton: false,
    // ttsRate: stringa fra '0.75' | '0.95' | '1.15'. Persistita nella
    // chiave separata TTS_RATE_KEY (non in STORAGE_KEY) per restare
    // compatibile col partial inline `leggi-ad-alta-voce.html`.
    ttsRate: '0.95'
  };
  var FONT_FAMILY_ALLOWED = ['default', 'readable', 'dyslexic'];

  var state = Object.assign({}, defaults);
  // Guard anti-loop: quando aggiorniamo la UI in risposta a un evento
  // esterno (pill inline → toolbar), non vogliamo rilanciare l'evento.
  var ttsRateSyncing = false;

  // ----------- Storage helpers -----------
  function load() {
    var migratedFromLegacy = false;
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        var saved = JSON.parse(raw);
        if (saved && typeof saved === 'object') {
          Object.keys(defaults).forEach(function (k) {
            // ttsRate lo leggiamo solo dalla sua chiave dedicata, mai dal blob.
            if (k === 'ttsRate') return;
            if (Object.prototype.hasOwnProperty.call(saved, k)) {
              state[k] = saved[k];
            }
          });

          // MIGRAZIONE LEGACY (Sera 2): chi aveva il vecchio bool
          // `readableFont:true` deve ritrovarsi con il nuovo
          // `fontFamily:"readable"`. Se entrambi sono presenti vince il
          // nuovo. Il vecchio campo viene poi rimosso dal blob al
          // prossimo save() (vedi save() che salva solo le chiavi di
          // defaults, e readableFont non c'è più).
          if (Object.prototype.hasOwnProperty.call(saved, 'readableFont')) {
            if (saved.readableFont === true && (!saved.fontFamily || saved.fontFamily === 'default')) {
              state.fontFamily = 'readable';
              migratedFromLegacy = true;
            }
          }

          // Sanitize: fontFamily deve essere uno dei tre valori validi.
          if (FONT_FAMILY_ALLOWED.indexOf(state.fontFamily) === -1) {
            state.fontFamily = defaults.fontFamily;
          }
        }
      }
    } catch (e) { /* localStorage non disponibile o JSON corrotto: usa default */ }
    // Se abbiamo migrato, salva subito così il vecchio blob viene riscritto
    // senza il campo `readableFont` legacy.
    if (migratedFromLegacy) {
      try {
        var blob = {};
        Object.keys(defaults).forEach(function (k) {
          if (k === 'ttsRate') return;
          blob[k] = state[k];
        });
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(blob));
      } catch (e) { /* */ }
    }
    // ttsRate: leggi dalla chiave dedicata condivisa con la pill inline.
    try {
      var r = window.localStorage.getItem(TTS_RATE_KEY);
      if (r && TTS_RATES_ALLOWED.indexOf(r) !== -1) state.ttsRate = r;
    } catch (e) { /* */ }
  }

  function save() {
    try {
      // Salva tutte le pref tranne ttsRate, che vive nella sua chiave dedicata.
      var blob = {};
      Object.keys(defaults).forEach(function (k) {
        if (k === 'ttsRate') return;
        blob[k] = state[k];
      });
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(blob));
    } catch (e) { /* fallisce silenziosamente in private mode */ }
  }

  // Scrive ttsRate sulla chiave dedicata e notifica gli altri componenti
  // (pill inline) via CustomEvent. La guard ttsRateSyncing evita il
  // re-broadcast quando siamo NOI stessi i destinatari di un evento.
  function saveTtsRate() {
    try { window.localStorage.setItem(TTS_RATE_KEY, String(state.ttsRate)); }
    catch (e) { /* */ }
    if (ttsRateSyncing) return;
    try {
      window.dispatchEvent(new CustomEvent(TTS_RATE_EVENT, {
        detail: { rate: state.ttsRate, source: 'toolbar' }
      }));
    } catch (e) { /* CustomEvent non supportato su browser molto vecchi */ }
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

    // Testo: famiglia carattere (mutuamente esclusive: solo UNA classe
    // viene aggiunta su <html>, mai entrambe. Il CSS ha selettori
    // separati `html.a11y-readable-font` e `html.a11y-dyslexic-font`).
    if (state.fontFamily === 'readable') html.classList.add('a11y-readable-font');
    else if (state.fontFamily === 'dyslexic') html.classList.add('a11y-dyslexic-font');

    // Testo: spaziatura
    if (state.spacing) html.classList.add('a11y-spacing');

    // Testo: modalità lettura (macro-toggle Sera 2). Applica classe
    // `a11y-reading-mode` che attiva: sfondo crema, max-width 65ch,
    // align-left, spaziatura. Il font è gestito a parte da fontFamily —
    // vedi side-effect in setPref('readingMode', true) che alza
    // fontFamily a 'readable' se era 'default'.
    if (state.readingMode) html.classList.add('a11y-reading-mode');

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

    // Pulsante traduzione: nasconde il selettore lingua del sito (#lang-toggle
    // in alto a destra) + chiede al browser di non offrire la traduzione
    // automatica (meta notranslate). Effetto IMMEDIATO sul pulsante del sito;
    // il browser leggera' il meta al prossimo caricamento.
    if (state.hideTranslateButton) {
      html.classList.add('a11y-hide-translate-button');
      html.setAttribute('translate', 'no');
      html.classList.add('notranslate');
      var meta = document.querySelector('meta[name="google"][content="notranslate"]');
      if (!meta) {
        meta = document.createElement('meta');
        meta.setAttribute('name', 'google');
        meta.setAttribute('content', 'notranslate');
        document.head.appendChild(meta);
      }
    } else {
      html.classList.remove('a11y-hide-translate-button');
      html.removeAttribute('translate');
      html.classList.remove('notranslate');
      var existing = document.querySelector('meta[name="google"][content="notranslate"]');
      if (existing) existing.remove();
    }
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
      // Side-effect coerente: attivando Modalità lettura, se l'utente
      // ha "Predefinito" come font, lo alziamo a "Alta leggibilità"
      // perché la modalità lettura nasce per ridurre la fatica visiva
      // e il font sans-serif comune è meno adatto. Se ha già scelto
      // "Per dislessia" (OpenDyslexic), lo lasciamo: rispetta la scelta.
      // La regola è stata richiesta esplicitamente in Sera 2.
      if (name === 'readingMode' && value === true && state.fontFamily === 'default') {
        state.fontFamily = 'readable';
      }
      if (name === 'ttsRate') saveTtsRate();
      else save();
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
      // Anche ttsRate torna al default 0.95 e notifica la pill inline.
      try { window.localStorage.removeItem(TTS_RATE_KEY); } catch (e) { /* */ }
      try {
        window.dispatchEvent(new CustomEvent(TTS_RATE_EVENT, {
          detail: { rate: state.ttsRate, source: 'toolbar-reset' }
        }));
      } catch (e) { /* */ }
      applyState();
      syncUI();
      announce('Impostazioni reimpostate.');
    });

    // Listener cross-component: se la pill inline cambia velocità, la
    // toolbar si aggiorna senza ri-emettere l'evento (guard ttsRateSyncing).
    window.addEventListener(TTS_RATE_EVENT, function (ev) {
      var d = ev && ev.detail; if (!d) return;
      if (d.source === 'toolbar' || d.source === 'toolbar-reset') return;
      if (TTS_RATES_ALLOWED.indexOf(String(d.rate)) === -1) return;
      ttsRateSyncing = true;
      state.ttsRate = String(d.rate);
      // Persistito anche se sappiamo che la pill l'ha già scritto: idempotente.
      try { window.localStorage.setItem(TTS_RATE_KEY, state.ttsRate); } catch (e) { /* */ }
      syncUI();
      ttsRateSyncing = false;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }
})();
