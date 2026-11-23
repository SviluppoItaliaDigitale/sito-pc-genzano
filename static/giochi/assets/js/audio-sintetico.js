/* Audio sintetico — Protezione Civile Genzano
   Suoni generati via Web Audio API; per i suoni naturali e quotidiani (tuono,
   pioggia, vento, cane, campanello, campanella, rilevatore di fumo) registrazioni
   vere CC0 in /giochi/assets/audio/, con il suono sintetico come riserva.
   Rispetta masterVolume (persistito in localStorage). */

(function (global) {
  'use strict';

  var KEY_VOLUME = 'pcgenzano.giochi.v1.audio.volume';
  var ctx = null;
  var inizializzato = false;
  var masterVolume = 0.6;

  function leggiVolumeSalvato() {
    try {
      var v = localStorage.getItem(KEY_VOLUME);
      if (v === null) return 0.6;
      var n = parseFloat(v);
      if (isNaN(n)) return 0.6;
      return Math.max(0, Math.min(1, n));
    } catch (e) { return 0.6; }
  }

  function persistiVolume(v) {
    try { localStorage.setItem(KEY_VOLUME, String(v)); } catch (e) { /* noop */ }
  }

  function init() {
    if (inizializzato) return true;
    try {
      var AC = global.AudioContext || global.webkitAudioContext;
      if (!AC) return false;
      ctx = new AC();
      // Sblocca iOS / Safari con un oscillatore silenzioso
      try {
        var o = ctx.createOscillator();
        var g = ctx.createGain();
        g.gain.value = 0.0001;
        o.connect(g); g.connect(ctx.destination);
        o.start(0); o.stop(ctx.currentTime + 0.01);
      } catch (e) { /* noop */ }
      masterVolume = leggiVolumeSalvato();
      inizializzato = true;
      return true;
    } catch (e) {
      return false;
    }
  }

  function setVolume(v) {
    masterVolume = Math.max(0, Math.min(1, Number(v) || 0));
    persistiVolume(masterVolume);
  }

  function getVolume() { return masterVolume; }

  // Suoni programmati e non ancora finiti: ferma() li interrompe tutti, così una
  // sirena lunga non continua sopra la domanda successiva.
  var programmati = [];
  function traccia(nodo) {
    programmati.push(nodo);
    nodo.onended = function () {
      var i = programmati.indexOf(nodo);
      if (i !== -1) programmati.splice(i, 1);
    };
  }

  // Primitiva: tono con inviluppo ADSR
  function tono(opts) {
    if (!init()) return;
    opts = opts || {};
    try {
      var t0 = ctx.currentTime + (opts.delay || 0);
      var durata = opts.durata || 0.3;
      var attack = opts.attack || 0.015;
      var release = opts.release || 0.05;
      var gainMax = (opts.gain || 0.25) * masterVolume;
      var osc = ctx.createOscillator();
      osc.type = opts.tipo || 'sine';
      osc.frequency.value = opts.freq || 440;
      if (opts.freqFine) osc.frequency.linearRampToValueAtTime(opts.freqFine, t0 + durata);
      var g = ctx.createGain();
      g.gain.setValueAtTime(0, t0);
      g.gain.linearRampToValueAtTime(gainMax, t0 + attack);
      g.gain.setValueAtTime(gainMax, t0 + Math.max(attack, durata - release));
      g.gain.linearRampToValueAtTime(0, t0 + durata);
      osc.connect(g); g.connect(ctx.destination);
      osc.start(t0);
      osc.stop(t0 + durata + 0.02);
      traccia(osc);
    } catch (e) { /* noop */ }
  }

  function rumoreBianco(opts) {
    if (!init()) return;
    opts = opts || {};
    try {
      var durata = opts.durata || 1.5;
      var gainMax = (opts.gain || 0.3) * masterVolume;
      var sampleRate = ctx.sampleRate;
      var buffer = ctx.createBuffer(1, Math.floor(sampleRate * durata), sampleRate);
      var data = buffer.getChannelData(0);
      for (var i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1);
      var src = ctx.createBufferSource();
      src.buffer = buffer;
      if (opts.playbackRate) src.playbackRate.value = opts.playbackRate;
      var g = ctx.createGain();
      var t0 = ctx.currentTime;
      g.gain.setValueAtTime(0, t0);
      g.gain.linearRampToValueAtTime(gainMax, t0 + 0.1);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + durata);
      var nodo = src;
      if (opts.filtroLowpass) {
        var f = ctx.createBiquadFilter();
        f.type = 'lowpass';
        f.frequency.value = opts.filtroLowpass;
        src.connect(f); f.connect(g);
      } else {
        src.connect(g);
      }
      g.connect(ctx.destination);
      src.start(t0);
      src.stop(t0 + durata + 0.05);
      traccia(src);
    } catch (e) { /* noop */ }
  }

  // Registrazioni vere (MP3 in /giochi/assets/audio/, licenze nella pagina del gioco).
  // Se il browser non riesce a riprodurle, suona `riserva` (il suono sintetico).
  var audioInCorso = null;
  var turno = 0; // cresce a ogni ferma(): i callback di una riproduzione annullata non valgono più
  function ferma() {
    turno++;
    if (audioInCorso) {
      try { audioInCorso.pause(); } catch (e) { /* noop */ }
      audioInCorso = null;
    }
    var nodi = programmati;
    programmati = [];
    for (var i = 0; i < nodi.length; i++) {
      try { nodi[i].onended = null; nodi[i].stop(0); } catch (e) { /* già finito */ }
    }
  }
  function registrazione(nome, riserva) {
    init();
    ferma();
    var usataRiserva = false;
    var mio = turno;
    function usaRiserva(err) {
      // Riproduzione fermata da noi (risposta data, nuovo ascolto): nessuna riserva.
      if (mio !== turno || (err && err.name === 'AbortError')) return;
      if (usataRiserva) return;
      usataRiserva = true;
      if (typeof riserva === 'function') riserva();
    }
    try {
      if (typeof global.Audio !== 'function') { usaRiserva(); return; }
      var a = new global.Audio('/giochi/assets/audio/' + nome + '.mp3');
      a.volume = masterVolume;
      a.onerror = usaRiserva;
      audioInCorso = a;
      var p = a.play();
      if (p && typeof p.then === 'function') p.then(null, usaRiserva);
    } catch (e) { usaRiserva(); }
  }

  // Preset: suoni dell'emergenza
  // Sirena bitonale di ambulanze e vigili del fuoco come nel DM 17/10/1980, art. 2:
  // note 392 Hz e 660 Hz, ciclo di 3 secondi diviso in 1/3 (392), 1/18 (660),
  // 1/18 (392), 1/18 (660), 1/3 (392), 1/18 (660), 1/18 (392), 1/18 (660).
  function sirenaSoccorso(cicli) {
    if (!init()) return;
    cicli = cicli || 1;
    var ciclo = 3;
    var schema = [[392, 6], [660, 1], [392, 1], [660, 1], [392, 6], [660, 1], [392, 1], [660, 1]];
    var t = 0;
    for (var c = 0; c < cicli; c++) {
      for (var i = 0; i < schema.length; i++) {
        var d = ciclo * schema[i][1] / 18;
        tono({ freq: schema[i][0], durata: d, tipo: 'sawtooth', gain: 0.16, delay: t, attack: 0.01, release: 0.01 });
        t += d;
      }
    }
  }
  // Nome storico, tenuto per compatibilità: suona la sirena del decreto.
  function sirenaAmbulanza() { sirenaSoccorso(1); }

  function tuono() {
    if (!init()) return;
    rumoreBianco({ durata: 1.8, gain: 0.4, filtroLowpass: 200, playbackRate: 0.8 + Math.random() * 0.4 });
  }

  function allarmeIncendio() {
    if (!init()) return;
    var cicli = 8;
    var on = 0.2, off = 0.1;
    for (var i = 0; i < cicli; i++) {
      tono({ freq: 3000, durata: on, tipo: 'square', gain: 0.12, delay: i * (on + off), attack: 0.02, release: 0.04 });
    }
  }

  // Suono di esempio per il gioco: non riproduce il suono ufficiale dei messaggi IT-alert.
  function itAlert() {
    if (!init()) return;
    for (var i = 0; i < 3; i++) {
      tono({ freq: 1000, durata: 0.15, tipo: 'sine', gain: 0.22, delay: i * 0.25, attack: 0.01, release: 0.03 });
    }
    tono({ freq: 800, durata: 0.5, tipo: 'sine', gain: 0.22, delay: 0.9, attack: 0.02, release: 0.08 });
  }

  function campanello() {
    if (!init()) return;
    tono({ freq: 660, durata: 0.4, tipo: 'triangle', gain: 0.25, attack: 0.01, release: 0.35 });
    tono({ freq: 550, durata: 0.4, tipo: 'triangle', gain: 0.25, delay: 0.42, attack: 0.01, release: 0.35 });
  }

  // Feedback UI
  function dingPositivo() {
    if (!init()) return;
    tono({ freq: 660, durata: 0.12, tipo: 'sine', gain: 0.2, attack: 0.01, release: 0.08 });
    tono({ freq: 880, durata: 0.18, tipo: 'sine', gain: 0.22, delay: 0.1, attack: 0.01, release: 0.12 });
  }

  function tonoNeutro() {
    if (!init()) return;
    tono({ freq: 400, durata: 0.25, tipo: 'sine', gain: 0.15, attack: 0.02, release: 0.1 });
  }

  // Fine partita: arpeggio breve e allegro; con meno della metà dei punti è più
  // morbido, mai un suono di «bocciatura».
  function fineGioco(percentuale) {
    if (!init()) return;
    var note = (percentuale === undefined || percentuale >= 50) ? [523, 659, 784, 1047] : [440, 523, 659];
    for (var i = 0; i < note.length; i++) {
      tono({ freq: note[i], durata: 0.22, tipo: 'triangle', gain: 0.2, delay: i * 0.13, attack: 0.01, release: 0.15 });
    }
  }

  function pipRadio() {
    if (!init()) return;
    tono({ freq: 1200, durata: 0.09, tipo: 'sine', gain: 0.2, attack: 0.005, release: 0.02 });
  }

  global.AudioSintetico = {
    init: init,
    setVolume: setVolume,
    getVolume: getVolume,
    tono: tono,
    rumoreBianco: rumoreBianco,
    sirenaAmbulanza: sirenaAmbulanza,
    sirenaSoccorso: sirenaSoccorso,
    registrazione: registrazione,
    ferma: ferma,
    tuono: tuono,
    allarmeIncendio: allarmeIncendio,
    itAlert: itAlert,
    campanello: campanello,
    dingPositivo: dingPositivo,
    tonoNeutro: tonoNeutro,
    fineGioco: fineGioco,
    pipRadio: pipRadio
  };
})(typeof window !== 'undefined' ? window : this);
