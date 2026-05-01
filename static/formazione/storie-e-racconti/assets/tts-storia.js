/* ============================================================
   TTS Storia — bottone "Ascolta la storia" via Web Speech API
   Auto-inietta nella .storia-toolbar di ogni storia/racconto.
   ============================================================ */
(function () {
  'use strict';

  function ttsSupported() {
    return typeof window.speechSynthesis !== 'undefined' &&
           typeof window.SpeechSynthesisUtterance !== 'undefined';
  }

  function pickItalianVoice() {
    if (!ttsSupported()) return null;
    var voices = window.speechSynthesis.getVoices() || [];
    return voices.find(function (v) { return v.lang === 'it-IT'; }) ||
           voices.find(function (v) { return v.lang && v.lang.indexOf('it') === 0; }) ||
           null;
  }

  // Estrae il testo leggibile dalla pagina storia
  function buildStoryText() {
    var parts = [];
    var titolo = document.querySelector('.storia-titolo-principale');
    if (titolo) parts.push(titolo.textContent.trim() + '.');
    var sotto = document.querySelector('.storia-sottotitolo');
    if (sotto) parts.push(sotto.textContent.trim() + '.');
    var corpo = document.querySelector('.storia-corpo');
    if (corpo) {
      // Solo i paragrafi <p>, ignora separatori decorativi
      corpo.querySelectorAll('p, h2, h3').forEach(function (el) {
        var t = el.textContent.trim();
        if (t) parts.push(t);
      });
    }
    return parts.join(' ');
  }

  // Spezza il testo in frasi per evitare cut-off su utterance lunghe
  function splitIntoChunks(text, maxLen) {
    if (!text) return [];
    var max = maxLen || 200;
    var result = [];
    var sentences = text.split(/(?<=[.!?])\s+/);
    var buf = '';
    sentences.forEach(function (s) {
      if ((buf + ' ' + s).length > max && buf) {
        result.push(buf.trim());
        buf = s;
      } else {
        buf = buf ? (buf + ' ' + s) : s;
      }
    });
    if (buf) result.push(buf.trim());
    return result;
  }

  var queue = [];
  var queueIdx = 0;
  var btnEl = null;
  var voiceCache = null;

  function setBtnState(state) {
    if (!btnEl) return;
    var icon = btnEl.querySelector('.tts-storia-icon');
    var label = btnEl.querySelector('.tts-storia-label');
    if (state === 'speaking') {
      btnEl.classList.add('speaking');
      btnEl.setAttribute('aria-label', 'Ferma la lettura');
      if (label) label.textContent = 'Ferma';
      if (icon) icon.textContent = '⏸';
    } else {
      btnEl.classList.remove('speaking');
      btnEl.setAttribute('aria-label', 'Ascolta la storia ad alta voce');
      if (label) label.textContent = 'Ascolta';
      if (icon) icon.textContent = '🔊';
    }
  }

  function stop() {
    if (!ttsSupported()) return;
    try { window.speechSynthesis.cancel(); } catch (e) { /* noop */ }
    queue = []; queueIdx = 0;
    setBtnState('idle');
  }

  function speakNext() {
    if (queueIdx >= queue.length) { stop(); return; }
    var u = new SpeechSynthesisUtterance(queue[queueIdx]);
    u.lang = 'it-IT';
    u.rate = 0.9;
    u.pitch = 1;
    if (voiceCache) u.voice = voiceCache;
    u.onend = function () {
      queueIdx++;
      if (queueIdx < queue.length) speakNext();
      else stop();
    };
    u.onerror = function () { stop(); };
    window.speechSynthesis.speak(u);
  }

  function start() {
    if (!ttsSupported()) return;
    if (window.speechSynthesis.speaking) { stop(); return; }
    var text = buildStoryText();
    if (!text) return;
    voiceCache = pickItalianVoice();
    queue = splitIntoChunks(text, 200);
    queueIdx = 0;
    setBtnState('speaking');
    speakNext();
  }

  function injectButton() {
    if (!ttsSupported()) return;
    var toolbar = document.querySelector('.storia-toolbar');
    if (!toolbar) return;

    btnEl = document.createElement('button');
    btnEl.type = 'button';
    btnEl.className = 'tts-storia-btn';
    btnEl.setAttribute('aria-label', 'Ascolta la storia ad alta voce');
    btnEl.innerHTML = '<span class="tts-storia-icon" aria-hidden="true">🔊</span><span class="tts-storia-label">Ascolta</span>';
    btnEl.addEventListener('click', start);

    // Inserisci il bottone come secondo elemento (dopo "Torna alle storie")
    var first = toolbar.firstElementChild;
    if (first && first.nextSibling) {
      toolbar.insertBefore(btnEl, first.nextSibling);
    } else {
      toolbar.appendChild(btnEl);
    }
  }

  // Stop TTS quando si lascia la pagina
  if (typeof window !== 'undefined' && window.addEventListener) {
    window.addEventListener('pagehide', stop);
    window.addEventListener('beforeunload', stop);
  }

  // Auto-init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectButton);
  } else {
    injectButton();
  }
})();
