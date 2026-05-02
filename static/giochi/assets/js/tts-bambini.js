/* ============================================================
   TTS Bambini — Modulo audio per i giochi della scuola infanzia
   Web Speech API (gratuito, browser-native, raccomandato W3C-WAI
   per la PA al posto degli overlay commerciali tipo AccessiBe).

   Fascia target: 3-6 anni (bambini che non sanno ancora leggere).

   USO IN UN GIOCO:
   1. Includi nello <head>:
      <link rel="stylesheet" href="/giochi/assets/css/tts-bambini.css">
   2. Includi prima di </body>:
      <script src="/giochi/assets/js/tts-bambini.js" defer></script>
   3. Aggiungi il bottone vicino al testo da leggere:
      <button class="tts-bambini-btn" data-tts-target="#question-text"
              type="button" aria-label="Ascolta la domanda">🔊</button>

      Il modulo legge il testo del selettore CSS specificato in
      data-tts-target. Il testo puo' cambiare dinamicamente: a ogni
      click viene letto il testo PRESENTE nel momento del click.

   PRINCIPI ACCESSIBILI:
   - Niente auto-play (rules accessibility "evita audio aggressivo").
   - Bottone tocca-target 56px (sopra WCAG 24x24 minimo).
   - Stato visivo "parlando" con animazione (rispetta prefers-reduced-motion).
   - Voce italiana di default, fallback a default browser.
   - Velocita' 0.85x (piu' lenta del default, chiara per i bambini).
   - Stop automatico se: nuovo speak, page unload, page hidden.
   ============================================================ */

(function(){
  'use strict';

  if (typeof window === 'undefined' || !window.speechSynthesis) {
    // Fallback graceful: niente audio API => bottoni nascosti via CSS
    document.documentElement.classList.add('no-tts-bambini');
    window.GiochiTTS = { parla: function(){}, stop: function(){}, supportato: false };
    return;
  }

  var voce = null;

  function trovaVoce(){
    var voci = window.speechSynthesis.getVoices();
    if (!voci || voci.length === 0) return;
    voce = voci.find(function(v){ return v.lang === 'it-IT'; })
        || voci.find(function(v){ return v.lang && v.lang.indexOf('it') === 0; })
        || null;
  }
  trovaVoce();
  if ('onvoiceschanged' in window.speechSynthesis) {
    window.speechSynthesis.addEventListener('voiceschanged', trovaVoce);
  }

  var btnAttivo = null;

  function rimuoviStatoAttivo(){
    if (btnAttivo) {
      btnAttivo.classList.remove('parlando');
      btnAttivo = null;
    }
  }

  function parla(testo, btn){
    if (!testo) return;
    var t = String(testo).trim();
    if (!t) return;
    // Stop eventuale TTS in corso (utente preme di nuovo o nuova scena)
    window.speechSynthesis.cancel();
    rimuoviStatoAttivo();

    var u = new SpeechSynthesisUtterance(t);
    if (voce) u.voice = voce;
    u.lang = 'it-IT';
    u.rate = 0.85;   // piu' lento del default 1.0 per chiarezza ai bambini
    u.pitch = 1.05;  // leggermente piu' alto = voce piu' "amica"
    u.volume = 1.0;

    u.onstart = function(){
      if (btn) {
        btn.classList.add('parlando');
        btnAttivo = btn;
      }
    };
    u.onend = u.onerror = function(){
      rimuoviStatoAttivo();
    };

    window.speechSynthesis.speak(u);
  }

  function stop(){
    window.speechSynthesis.cancel();
    rimuoviStatoAttivo();
  }

  // Event delegation: tutti i .tts-bambini-btn su qualsiasi pagina
  // del sito che includa questo script vengono gestiti automaticamente.
  document.addEventListener('click', function(e){
    var btn = e.target.closest('.tts-bambini-btn');
    if (!btn) return;
    e.preventDefault();
    // Se l'utente preme di nuovo lo stesso bottone mentre sta parlando,
    // ferma (toggle).
    if (btn === btnAttivo) {
      stop();
      return;
    }
    var testo = btn.dataset.tts || '';
    var target = btn.dataset.ttsTarget;
    if (target) {
      var el = document.querySelector(target);
      if (el) testo = el.textContent || '';
    }
    parla(testo, btn);
  });

  // Stop quando la pagina e' nascosta (cambio tab) o si chiude
  document.addEventListener('visibilitychange', function(){
    if (document.hidden) stop();
  });
  window.addEventListener('beforeunload', stop);
  window.addEventListener('pagehide', stop);

  window.GiochiTTS = {
    parla: parla,
    stop: stop,
    supportato: true
  };
})();
