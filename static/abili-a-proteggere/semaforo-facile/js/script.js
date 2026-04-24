/* Semaforo della Sicurezza — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var colors = {
    verde:     { label: 'Verde' },
    giallo:    { label: 'Giallo' },
    arancione: { label: 'Arancione' },
    rosso:     { label: 'Rosso' }
  };

  var situations = [
    {
      emoji: '\u2600\uFE0F',
      title: 'Sole e cielo sereno',
      desc: 'Oggi il tempo è bello e non ci sono pericoli.',
      correct: 'verde',
      wrong: 'giallo',
      feedback: 'Verde: tutto tranquillo. Puoi uscire senza preoccuparti.'
    },
    {
      emoji: '\u26C5',
      title: 'Qualche pioggia',
      desc: 'Oggi piove un po\u2019 e il vento è leggero.',
      correct: 'giallo',
      wrong: 'verde',
      feedback: 'Giallo: serve attenzione. Fai attenzione a strade bagnate e piccoli allagamenti.'
    },
    {
      emoji: '\u26C8\uFE0F',
      title: 'Temporale forte',
      desc: 'C\u2019è un temporale con vento forte e lampi.',
      correct: 'arancione',
      wrong: 'giallo',
      feedback: 'Arancione: pericolo. Resta in casa e allontanati dalle finestre.'
    },
    {
      emoji: '\uD83C\uDF0A',
      title: 'Alluvione',
      desc: 'L\u2019acqua è salita tanto e ha invaso le strade.',
      correct: 'rosso',
      wrong: 'arancione',
      feedback: 'Rosso: grave. Sali ai piani alti e chiama il 112 se serve aiuto.'
    },
    {
      emoji: '\uD83C\uDF2C\uFE0F',
      title: 'Vento forte',
      desc: 'Il vento è forte e sposta rami e oggetti.',
      correct: 'arancione',
      wrong: 'verde',
      feedback: 'Arancione: pericolo. Non stare sotto alberi o vicino a cose che volano.'
    },
    {
      emoji: '\uD83D\uDD25',
      title: 'Incendio vicino al bosco',
      desc: 'Si vedono fiamme e tanto fumo vicino al paese.',
      correct: 'rosso',
      wrong: 'giallo',
      feedback: 'Rosso: grave. Chiudi porte e finestre e chiama il 112.'
    }
  ];

  var currentIndex = 0;
  var score = 0;

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }
  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function loadSituation() {
    var s = situations[currentIndex];
    document.getElementById('sit-emoji').textContent = s.emoji;
    document.getElementById('sit-title').textContent = s.title;
    document.getElementById('sit-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = situations.length;
    document.getElementById('score').textContent = score;

    var fb = document.getElementById('feedback-box');
    hide(fb);

    var container = document.getElementById('colors');
    container.innerHTML = '';

    var options = shuffle([
      { key: s.correct, isCorrect: true },
      { key: s.wrong, isCorrect: false }
    ]);

    options.forEach(function (opt) {
      var btn = document.createElement('button');
      btn.className = 'color-btn c-' + opt.key;
      btn.innerHTML = '<span class="color-disc" aria-hidden="true"></span><span>' + colors[opt.key].label + '</span>';
      btn.setAttribute('aria-label', 'Colore ' + colors[opt.key].label);
      btn.addEventListener('click', function () { handleChoice(btn, opt.isCorrect, s); });
      container.appendChild(btn);
    });
  }

  function handleChoice(btn, isCorrect, situation) {
    document.querySelectorAll('.color-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');

    if (isCorrect) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box fb-ok';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    } else {
      btn.classList.add('wrong');
      document.querySelectorAll('.color-btn').forEach(function (b) {
        if (!b.classList.contains('wrong')) b.classList.add('correct');
      });
      fb.className = 'feedback-box fb-no';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    }
    show(fb);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < situations.length) {
        loadSituation();
      } else {
        hide(document.getElementById('game-screen'));
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = situations.length;
        show(document.getElementById('end-screen'));
      }
    }, 3500);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(document.getElementById('intro-screen'));
    show(document.getElementById('game-screen'));
    currentIndex = 0;
    score = 0;
    shuffle(situations);
    loadSituation();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(document.getElementById('end-screen'));
    show(document.getElementById('intro-screen'));
  });
})();
