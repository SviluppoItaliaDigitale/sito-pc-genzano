/* Al Sicuro a Casa — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var situations = [
    {
      emoji: '\uD83E\uDED6',
      title: 'Pentola sul fuoco',
      desc: 'Il manico della pentola calda sporge fuori dal fornello.',
      correct: 'danger',
      feedback: 'Pericoloso. Chi passa può urtare il manico e rovesciarsi addosso la pentola. Gira il manico verso l\u2019interno.'
    },
    {
      emoji: '\uD83E\uDDEF',
      title: 'Estintore a vista',
      desc: 'Vicino alla porta c\u2019è un estintore pulito, in vista, facile da prendere.',
      correct: 'safe',
      feedback: 'Sicuro. Un estintore a vista e raggiungibile è una cosa buona. In caso di piccolo incendio si usa subito.'
    },
    {
      emoji: '\uD83D\uDD0C',
      title: 'Tante prese insieme',
      desc: 'Nella stessa presa sono collegate la lavatrice, il phon e la stufetta.',
      correct: 'danger',
      feedback: 'Pericoloso. Troppi elettrodomestici nella stessa presa si scaldano e possono prendere fuoco. Distribuisci i carichi.'
    },
    {
      emoji: '\uD83D\uDEAA',
      title: 'Porta non bloccata',
      desc: 'La porta d\u2019ingresso si chiude bene ma non è bloccata da mobili.',
      correct: 'safe',
      feedback: 'Sicuro. Se serve uscire in fretta, una porta libera è la cosa giusta. Non mettere mai mobili davanti alla via di fuga.'
    },
    {
      emoji: '\uD83E\uDDF9',
      title: 'Tappeto che si arriccia',
      desc: 'Un tappeto nel corridoio si alza da un lato e fa inciampare.',
      correct: 'danger',
      feedback: 'Pericoloso. Un tappeto che si alza fa cadere: appiattiscilo o toglilo, specialmente vicino a gradini.'
    },
    {
      emoji: '\uD83D\uDCA1',
      title: 'Luce dopo il temporale',
      desc: 'Dopo il temporale c\u2019è di nuovo corrente. Accendi prima una lampadina e controlli se funziona.',
      correct: 'safe',
      feedback: 'Sicuro. Accendere una luce normale per provare è corretto. Se senti odore di bruciato, spegni e chiama un adulto.'
    }
  ];

  var answers = {
    safe:   { label: 'Sicuro',     icon: 'bi-check-lg',          cls: 'a-safe' },
    danger: { label: 'Pericoloso', icon: 'bi-exclamation-lg',    cls: 'a-danger' }
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

  function loadSituation() {
    var s = situations[currentIndex];
    document.getElementById('sit-emoji').textContent = s.emoji;
    document.getElementById('sit-title').textContent = s.title;
    document.getElementById('sit-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = situations.length;
    document.getElementById('score').textContent = score;

    hide(document.getElementById('feedback-box'));

    var container = document.getElementById('answers');
    container.innerHTML = '';

    ['safe', 'danger'].forEach(function (key) {
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

  function handleChoice(btn, isCorrect, situation) {
    document.querySelectorAll('.answer-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');

    if (isCorrect) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box fb-ok';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    } else {
      btn.classList.add('wrong');
      document.querySelectorAll('.answer-btn').forEach(function (b) {
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
