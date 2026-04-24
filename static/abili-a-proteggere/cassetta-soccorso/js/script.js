/* Cassetta di Soccorso — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var items = [
    {
      emoji: '\uD83E\uDE79',
      title: 'Cerotti',
      desc: 'Una scatola di cerotti nuovi di misura varia.',
      correct: 'yes',
      feedback: 'Sì, va nella cassetta. I cerotti servono per le piccole ferite: metti sempre il cerotto dopo aver pulito la pelle.'
    },
    {
      emoji: '\uD83E\uDDF4',
      title: 'Carta igienica',
      desc: 'Un rotolo di carta igienica.',
      correct: 'no',
      feedback: 'No, non va nella cassetta. Per pulire le ferite serve qualcosa di sterile: usa garze, non carta.'
    },
    {
      emoji: '\uD83E\uDEB7',
      title: 'Garze sterili',
      desc: 'Pacchetti di garze chiuse nella bustina.',
      correct: 'yes',
      feedback: 'Sì, va nella cassetta. Le garze sterili servono per coprire le ferite e fermare un piccolo sanguinamento.'
    },
    {
      emoji: '\uD83C\uDF6C',
      title: 'Caramelle',
      desc: 'Una busta di caramelle gommose.',
      correct: 'no',
      feedback: 'No, non vanno nella cassetta. Le caramelle non curano: possono stare in borsa, ma non nel kit di emergenza.'
    },
    {
      emoji: '\uD83D\uDC8A',
      title: 'Disinfettante',
      desc: 'Una bottiglietta di disinfettante per la pelle.',
      correct: 'yes',
      feedback: 'Sì, va nella cassetta. Pulisce le ferite e toglie i germi. Prima di usarlo chiedi a un adulto.'
    },
    {
      emoji: '\uD83D\uDD2A',
      title: 'Coltello da cucina',
      desc: 'Un coltello da cucina appuntito.',
      correct: 'no',
      feedback: 'No, non va nella cassetta. È pericoloso. Nella cassetta bastano piccole forbici con la punta tonda, usate solo da un adulto.'
    }
  ];

  var answers = {
    yes: { label: 'Va nella cassetta', icon: 'bi-check-lg',       cls: 'a-yes' },
    no:  { label: 'Non ci va',         icon: 'bi-x-lg',           cls: 'a-no' }
  };

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

  function loadItem() {
    var s = items[currentIndex];
    document.getElementById('sit-emoji').textContent = s.emoji;
    document.getElementById('sit-title').textContent = s.title;
    document.getElementById('sit-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = items.length;
    document.getElementById('score').textContent = score;

    hide(document.getElementById('feedback-box'));

    var container = document.getElementById('answers');
    container.innerHTML = '';

    ['yes', 'no'].forEach(function (key) {
      var a = answers[key];
      var btn = document.createElement('button');
      btn.className = 'answer-btn ' + a.cls;
      btn.innerHTML =
        '<span class="answer-icon"><i class="bi ' + a.icon + '" aria-hidden="true"></i></span>' +
        '<span>' + a.label + '</span>';
      btn.setAttribute('aria-label', a.label);
      btn.addEventListener('click', function () { handleChoice(btn, key === s.correct, s); });
      container.appendChild(btn);
    });
  }

  function handleChoice(btn, isCorrect, item) {
    document.querySelectorAll('.answer-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');

    if (isCorrect) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box fb-ok';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + item.feedback;
    } else {
      btn.classList.add('wrong');
      document.querySelectorAll('.answer-btn').forEach(function (b) {
        if (!b.classList.contains('wrong')) b.classList.add('correct');
      });
      fb.className = 'feedback-box fb-no';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + item.feedback;
    }
    show(fb);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < items.length) {
        loadItem();
      } else {
        hide(document.getElementById('game-screen'));
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = items.length;
        show(document.getElementById('end-screen'));
      }
    }, 3500);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(document.getElementById('intro-screen'));
    show(document.getElementById('game-screen'));
    currentIndex = 0;
    score = 0;
    shuffle(items);
    loadItem();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(document.getElementById('end-screen'));
    show(document.getElementById('intro-screen'));
  });
})();
