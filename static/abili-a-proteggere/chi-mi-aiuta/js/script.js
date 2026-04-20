/* Chi Mi Aiuta? — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var helpers = {
    pompieri: { icon: '🚒', label: 'Vigili del Fuoco', number: '112' },
    ambulanza: { icon: '🚑', label: 'Ambulanza', number: '112' },
    volontari: { icon: '🧡', label: 'Volontari PC', number: '112' },
    carabinieri: { icon: '👮', label: 'Carabinieri', number: '112' }
  };

  var situations = [
    {
      emoji: '🔥',
      title: 'C\u2019è un incendio!',
      desc: 'Vedi delle fiamme che escono da un bosco vicino a casa.',
      correct: 'pompieri',
      wrong: 'ambulanza',
      feedback: 'I Vigili del Fuoco spengono gli incendi. Per chiamarli componi il 112, il numero unico di emergenza.'
    },
    {
      emoji: '🤕',
      title: 'Qualcuno sta male!',
      desc: 'Il nonno si è sentito male e non riesce ad alzarsi.',
      correct: 'ambulanza',
      wrong: 'pompieri',
      feedback: 'L\u2019ambulanza porta i medici. Per chiamarla componi il 112: la centrale invia subito i soccorsi sanitari.'
    },
    {
      emoji: '🏠💨',
      title: 'Terremoto!',
      desc: 'C\u2019è stato un forte terremoto e un muro è caduto.',
      correct: 'pompieri',
      wrong: 'volontari',
      feedback: 'I Vigili del Fuoco intervengono per i crolli. Chiama il 112!'
    },
    {
      emoji: '🌊',
      title: 'Alluvione!',
      desc: 'L\u2019acqua sta salendo e alcune famiglie hanno bisogno di aiuto.',
      correct: 'volontari',
      wrong: 'ambulanza',
      feedback: 'I volontari della Protezione Civile aiutano le persone durante le alluvioni. Per le emergenze chiama il 112!'
    },
    {
      emoji: '🚗💥',
      title: 'Incidente stradale!',
      desc: 'Due macchine si sono scontrate e una persona è ferita.',
      correct: 'ambulanza',
      wrong: 'volontari',
      feedback: 'L\u2019ambulanza porta i medici per soccorrere i feriti. Chiama subito il 112!'
    },
    {
      emoji: '🏠🔒',
      title: 'Porta bloccata!',
      desc: 'Un anziano è rimasto chiuso in casa e non riesce ad aprire la porta.',
      correct: 'pompieri',
      wrong: 'carabinieri',
      feedback: 'I Vigili del Fuoco possono aprire le porte. Chiama il 112!'
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

    var container = document.getElementById('helpers');
    container.innerHTML = '';

    var correctHelper = helpers[s.correct];
    var wrongHelper = helpers[s.wrong];

    var options = shuffle([
      { helper: correctHelper, isCorrect: true },
      { helper: wrongHelper, isCorrect: false }
    ]);

    options.forEach(function (opt) {
      var btn = document.createElement('button');
      btn.className = 'helper-btn';
      btn.innerHTML =
        '<span class="helper-icon" aria-hidden="true">' + opt.helper.icon + '</span>' +
        '<span class="helper-label">' + opt.helper.label + '</span>' +
        (opt.helper.number ? '<span class="helper-number">' + opt.helper.number + '</span>' : '');
      btn.setAttribute('aria-label', opt.helper.label + (opt.helper.number ? ' ' + opt.helper.number : ''));
      btn.addEventListener('click', function () { handleChoice(btn, opt.isCorrect, s); });
      container.appendChild(btn);
    });
  }

  function handleChoice(btn, isCorrect, situation) {
    document.querySelectorAll('.helper-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');

    if (isCorrect) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box fb-ok';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    } else {
      btn.classList.add('wrong');
      // highlight correct
      document.querySelectorAll('.helper-btn').forEach(function (b) {
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
    }, 3000);
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
