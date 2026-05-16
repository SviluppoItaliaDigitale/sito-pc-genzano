/* ============================================================
 * glossario-inline.js (v1.0)
 *
 * Cosa fa:
 *   Alla prima occorrenza di ogni termine del glossario in
 *   .article-body o .list-intro-content, sostituisce il termine
 *   con un <button class="gloss-term"> + popover accessibile
 *   (definizione breve + link al glossario completo).
 *
 * Beneficiari: cittadini non tecnici, anziani, italiano L2,
 * persone in stress da emergenza che incontrano sigle
 * specialistiche (DPC, COC, AeDES, AIB, IT-alert, ecc.).
 *
 * Vincoli:
 *   - Solo PRIMA occorrenza per articolo (ogni id viene marcato
 *     "consumato" e ignorato per il resto del walk).
 *   - Mai dentro: <a>, <button>, <code>, <pre>, <h1>, <kbd>,
 *     [aria-hidden=true], .no-gloss, .tts-wrapper, .gloss-term.
 *   - Mega-regex unica con alternazione di tutte le varianti:
 *     scansione O(N) sulla lunghezza del testo, non O(N×termini).
 *   - Popover non-modal, posizionato sotto il button con flip
 *     se overflow viewport. Tastiera: Enter/Space apre, ESC chiude,
 *     Tab esce. Click-outside chiude.
 *
 * Sorgente dati: window.PCGENZANO_GLOSSARIO iniettato dal partial
 *                 glossario-inline.html (legge data/glossario.yaml).
 * ============================================================ */
(function () {
  'use strict';

  if (!Array.isArray(window.PCGENZANO_GLOSSARIO) || !window.PCGENZANO_GLOSSARIO.length) return;
  if (document.documentElement.classList.contains('no-glossario')) return;

  var GLOSSARIO = window.PCGENZANO_GLOSSARIO;

  // Indice di lookup: variante normalizzata (lowercase) → voce
  var INDEX = Object.create(null);
  var allVariants = [];
  GLOSSARIO.forEach(function (voce) {
    if (!voce.id || !voce.varianti || !voce.definizione) return;
    voce.varianti.forEach(function (v) {
      if (!v) return;
      var key = v.toLowerCase();
      if (!INDEX[key]) {
        INDEX[key] = voce;
        allVariants.push(v);
      }
    });
  });
  if (!allVariants.length) return;

  // Costruisce la mega-regex. Ordina le varianti per lunghezza decrescente
  // così "Centro Operativo Comunale" vince su "COC" se entrambe sarebbero
  // catturate (regex alternation è greedy sul primo match della lista).
  function escapeRegex(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  allVariants.sort(function (a, b) { return b.length - a.length; });
  var pattern = '\\b(' + allVariants.map(escapeRegex).join('|') + ')\\b';
  var MEGA_RE = new RegExp(pattern, 'gi');

  // Selettori da ignorare (no-glossario)
  var SKIP_TAGS = { A: 1, BUTTON: 1, CODE: 1, PRE: 1, KBD: 1, H1: 1, INPUT: 1, TEXTAREA: 1, SELECT: 1, OPTION: 1, LABEL: 1, SCRIPT: 1, STYLE: 1, MARK: 1, FIGCAPTION: 1 };
  var SKIP_CLASSES = ['no-gloss', 'no-glossario', 'tts-wrapper', 'tts-status', 'gloss-term', 'gloss-popover', 'visually-hidden', 'pittogramma', 'pittogramma-figure', 'reading-meta', 'badge'];

  function shouldSkipElement(node) {
    if (!node || node.nodeType !== 1) return false;
    if (SKIP_TAGS[node.tagName]) return true;
    if (node.getAttribute && node.getAttribute('aria-hidden') === 'true') return true;
    if (node.classList) {
      for (var i = 0; i < SKIP_CLASSES.length; i++) {
        if (node.classList.contains(SKIP_CLASSES[i])) return true;
      }
    }
    return false;
  }

  function isInsideSkip(node) {
    var p = node.parentNode;
    while (p && p.nodeType === 1) {
      if (shouldSkipElement(p)) return true;
      p = p.parentNode;
    }
    return false;
  }

  // Set degli id già "consumati" durante il walk (prima occorrenza only)
  var consumed = Object.create(null);

  // Walk dei TextNode discendenti di un container, restituisce array
  // (separato dal rendering perché i replace modificano il DOM)
  function collectTextNodes(root) {
    var out = [];
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        if (isInsideSkip(n)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) out.push(n);
    return out;
  }

  // Counter univoco per id popover
  var popoverCounter = 0;

  function makeGlossElement(matchedText, voce) {
    var idPop = 'gloss-pop-' + (++popoverCounter);
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'gloss-term';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-describedby', idPop);
    btn.setAttribute('data-gloss-id', voce.id);
    // No btn.title: il tooltip browser-native si sovrapponeva al popover
    // quando l'utente cliccava. L'icona ⓘ + sottolineato tratteggiato +
    // aria-describedby sono sufficienti come affordance visiva/screen-reader.
    btn.appendChild(document.createTextNode(matchedText));
    var ico = document.createElement('span');
    ico.className = 'gloss-icon';
    ico.setAttribute('aria-hidden', 'true');
    ico.textContent = 'ⓘ';
    btn.appendChild(ico);

    var pop = document.createElement('span');
    pop.className = 'gloss-popover';
    pop.id = idPop;
    pop.setAttribute('role', 'tooltip');
    pop.hidden = true;

    var defP = document.createElement('span');
    defP.className = 'gloss-popover-def';
    defP.textContent = voce.definizione;
    pop.appendChild(defP);

    if (voce.link) {
      var more = document.createElement('a');
      more.className = 'gloss-popover-link';
      more.href = voce.link;
      more.textContent = 'Scopri di più nel glossario';
      more.setAttribute('aria-label', 'Apri la voce «' + (voce.termine || matchedText) + '» nel glossario completo');
      pop.appendChild(more);
    }

    // Wrapper inline-block per posizionare il popover relativamente al button
    var wrap = document.createElement('span');
    wrap.className = 'gloss-wrap';
    wrap.appendChild(btn);
    wrap.appendChild(pop);
    return wrap;
  }

  // Sostituisce in-place le occorrenze di MEGA_RE in un singolo TextNode.
  function processTextNode(textNode) {
    var text = textNode.nodeValue;
    MEGA_RE.lastIndex = 0;
    var match;
    var lastIndex = 0;
    var fragment = null;
    while ((match = MEGA_RE.exec(text)) !== null) {
      var matched = match[0];
      var key = matched.toLowerCase();
      var voce = INDEX[key];
      if (!voce) continue;
      // Skip se id già consumato (prima occorrenza only)
      if (consumed[voce.id]) continue;
      // Lazy init fragment alla prima sostituzione utile
      if (!fragment) fragment = document.createDocumentFragment();
      var matchStart = match.index;
      // Testo prima del match
      if (matchStart > lastIndex) {
        fragment.appendChild(document.createTextNode(text.substring(lastIndex, matchStart)));
      }
      // Elemento glossario
      fragment.appendChild(makeGlossElement(matched, voce));
      consumed[voce.id] = true;
      lastIndex = matchStart + matched.length;
    }
    if (fragment) {
      // Testo residuo dopo l'ultima sostituzione
      if (lastIndex < text.length) {
        fragment.appendChild(document.createTextNode(text.substring(lastIndex)));
      }
      textNode.parentNode.replaceChild(fragment, textNode);
    }
  }

  // ============================================================
  // Popover behaviour: apri/chiudi, focus management, tastiera
  // ============================================================

  var openPopover = null;
  var openButton = null;

  function closePopover() {
    if (!openPopover) return;
    openPopover.hidden = true;
    openPopover.classList.remove('is-flipped-up');
    openPopover.style.cssText = '';
    if (openButton) openButton.setAttribute('aria-expanded', 'false');
    openPopover = null;
    openButton = null;
  }

  // Posiziona il popover via position: fixed con coordinate dal button.
  // Necessario perché position: absolute viene clippato quando il button
  // è dentro una <td> o un .table-responsive (overflow auto/hidden).
  function positionPopover(btn, pop) {
    var br = btn.getBoundingClientRect();
    var pw = pop.offsetWidth;
    var ph = pop.offsetHeight;
    var vw = window.innerWidth || document.documentElement.clientWidth;
    var vh = window.innerHeight || document.documentElement.clientHeight;
    // Default: sotto al button, allineato a sinistra
    var top = br.bottom + 6;
    var left = br.left;
    var flipped = false;
    // Se va fuori dal viewport in basso → flip sopra
    if (top + ph > vh - 10) {
      top = br.top - ph - 6;
      flipped = true;
    }
    // Se va fuori dal viewport a destra → riallinea
    if (left + pw > vw - 10) left = Math.max(10, vw - pw - 10);
    if (left < 10) left = 10;
    pop.style.position = 'fixed';
    pop.style.top = top + 'px';
    pop.style.left = left + 'px';
    pop.classList.toggle('is-flipped-up', flipped);
  }

  function openFor(btn) {
    var pop = btn.parentNode.querySelector('.gloss-popover');
    if (!pop) return;
    if (openPopover && openPopover !== pop) closePopover();
    pop.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    openPopover = pop;
    openButton = btn;
    // Posiziona con coordinate fisse dopo render iniziale per dimensioni reali
    requestAnimationFrame(function () { positionPopover(btn, pop); });
  }

  function togglePopover(btn) {
    var pop = btn.parentNode.querySelector('.gloss-popover');
    if (!pop) return;
    if (pop.hidden) openFor(btn); else closePopover();
  }

  // Click su un .gloss-term apre/chiude il suo popover
  document.addEventListener('click', function (ev) {
    var target = ev.target;
    var btn = target.closest && target.closest('.gloss-term');
    if (btn) {
      ev.preventDefault();
      togglePopover(btn);
      return;
    }
    // Click fuori da un popover aperto → chiudi
    if (openPopover && !target.closest('.gloss-popover') && !target.closest('.gloss-term')) {
      closePopover();
    }
  });

  // ESC chiude
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && openPopover) {
      var btnToFocus = openButton;
      closePopover();
      if (btnToFocus) btnToFocus.focus();
    }
  });

  // Hover desktop (con safety: niente hover su touch — pointer:fine)
  if (window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.addEventListener('mouseover', function (ev) {
      var btn = ev.target.closest && ev.target.closest('.gloss-term');
      if (btn && (!openPopover || openButton !== btn)) {
        openFor(btn);
      }
    });
    document.addEventListener('mouseout', function (ev) {
      var btn = ev.target.closest && ev.target.closest('.gloss-term');
      var wrap = ev.target.closest && ev.target.closest('.gloss-wrap');
      if (!wrap) return;
      // Se il mouse esce dal wrap (sia button sia popover)
      var related = ev.relatedTarget;
      if (!related || !wrap.contains(related)) {
        if (openButton === btn) closePopover();
      }
    });
  }

  // Chiudi su scroll della pagina (i popover non seguono lo scroll)
  var scrollTimer = null;
  window.addEventListener('scroll', function () {
    if (!openPopover) return;
    if (scrollTimer) clearTimeout(scrollTimer);
    scrollTimer = setTimeout(closePopover, 100);
  }, { passive: true });

  // ============================================================
  // Avvio: scansiona tutti i container target
  // ============================================================
  function processContainer(container) {
    if (!container) return;
    var nodes = collectTextNodes(container);
    for (var i = 0; i < nodes.length; i++) {
      processTextNode(nodes[i]);
      // Uscita anticipata se tutti i termini sono stati consumati
      if (Object.keys(consumed).length === GLOSSARIO.length) break;
    }
  }

  function init() {
    var containers = document.querySelectorAll('.article-body, .list-intro-content');
    for (var i = 0; i < containers.length; i++) processContainer(containers[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
