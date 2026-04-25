/* Respiro Calmo — Esercizio di respirazione guidato */
(function () {
  'use strict';

  var TOTAL_ROUNDS = 4;
  var timers = [];
  var stopped = false;
  var currentRound = 0;

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }

  function clearAllTimers() {
    while (timers.length) {
      clearTimeout(timers.pop());
    }
  }

  function setPhase(cls, text) {
    var circle = document.getElementById('breath-circle');
    var label = document.getElementById('breath-text');
    circle.classList.remove('inhale', 'hold', 'exhale');
    if (cls) circle.classList.add(cls);
    label.textContent = text;
  }

  function doRound(roundIndex) {
    if (stopped) return;
    currentRound = roundIndex + 1;
    document.getElementById('round-n').textContent = currentRound;

    // Inhale 4s → Hold 2s → Exhale 6s  = 12s per round
    setPhase('inhale', 'Inspira dal naso');
    timers.push(setTimeout(function () {
      if (stopped) return;
      setPhase('hold', 'Trattieni…');
      timers.push(setTimeout(function () {
        if (stopped) return;
        setPhase('exhale', 'Butta fuori l’aria');
        timers.push(setTimeout(function () {
          if (stopped) return;
          if (roundIndex + 1 < TOTAL_ROUNDS) {
            doRound(roundIndex + 1);
          } else {
            finish();
          }
        }, 6000));
      }, 2000));
    }, 4000));
  }

  function finish() {
    clearAllTimers();
    hide(document.getElementById('breath-screen'));
    show(document.getElementById('end-screen'));
  }

  function startExercise() {
    stopped = false;
    clearAllTimers();
    document.getElementById('round-total').textContent = TOTAL_ROUNDS;
    document.getElementById('round-n').textContent = 1;
    setPhase(null, 'Preparati…');
    hide(document.getElementById('intro-screen'));
    hide(document.getElementById('end-screen'));
    show(document.getElementById('breath-screen'));
    // Breve preparazione di 2s prima del primo inspiro
    timers.push(setTimeout(function () {
      if (stopped) return;
      doRound(0);
    }, 2000));
  }

  document.getElementById('start-btn').addEventListener('click', startExercise);
  document.getElementById('restart-btn').addEventListener('click', startExercise);

  document.getElementById('stop-btn').addEventListener('click', function () {
    stopped = true;
    clearAllTimers();
    finish();
  });
})();
