/* Audio sintetico — Protezione Civile Genzano
   Tutti i suoni generati via Web Audio API. Nessun file audio nel repo.
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
    } catch (e) { /* noop */ }
  }

  // Preset: suoni dell'emergenza
  function sirenaAmbulanza() {
    if (!init()) return;
    var t0 = ctx.currentTime;
    var cicli = 3;
    var durata = 0.4;
    for (var i = 0; i < cicli; i++) {
      tono({ freq: 600, durata: durata, tipo: 'square', gain: 0.18, delay: i * durata * 2, attack: 0.02, release: 0.05 });
      tono({ freq: 800, durata: durata, tipo: 'square', gain: 0.18, delay: i * durata * 2 + durata, attack: 0.02, release: 0.05 });
    }
  }

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
    tuono: tuono,
    allarmeIncendio: allarmeIncendio,
    itAlert: itAlert,
    campanello: campanello,
    dingPositivo: dingPositivo,
    tonoNeutro: tonoNeutro,
    pipRadio: pipRadio
  };
})(typeof window !== 'undefined' ? window : this);
