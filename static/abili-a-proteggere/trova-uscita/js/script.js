/* Trova l'Uscita — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🏠',
      title: 'A casa, c’è fumo',
      desc: 'Senti odore di fumo dalla cucina. Sei vicino alla porta di casa.',
      choices: [
        { text: 'Esco dalla porta di casa, piano e abbassato', icon: '🚪', correct: true },
        { text: 'Apro la finestra grande del soggiorno', icon: '🪟', correct: false },
        { text: 'Mi nascondo in bagno', icon: '🚿', correct: false }
      ],
      feedback: 'La porta di casa è la via di fuga principale. Esci abbassato per evitare il fumo e chiudi la porta dietro di te.'
    },
    {
      icon: '🏫',
      title: 'A scuola, suona l’allarme',
      desc: 'Suona l’allarme di evacuazione mentre sei in aula.',
      choices: [
        { text: 'Seguo la maestra fino al punto di raccolta', icon: '🚶', correct: true },
        { text: 'Prendo l’ascensore', icon: '🛀', correct: false },
        { text: 'Torno indietro a prendere lo zaino', icon: '🎒', correct: false }
      ],
      feedback: 'Si segue sempre la maestra in fila. Mai l’ascensore in emergenza, mai tornare indietro per prendere oggetti.'
    },
    {
      icon: '🏬',
      title: 'Al supermercato, c’è un’emergenza',
      desc: 'Suona l’allarme nel supermercato. Vedi la cassa e una porta con scritto USCITA DI EMERGENZA.',
      choices: [
        { text: 'Vado alla porta USCITA DI EMERGENZA', icon: '🚪', correct: true },
        { text: 'Resto in fila alla cassa', icon: '🛒', correct: false },
        { text: 'Torno al banco frigo', icon: '🧊', correct: false }
      ],
      feedback: 'Le porte con scritta verde USCITA DI EMERGENZA sono la via di fuga sicura. Lascia stare la spesa.'
    },
    {
      icon: '🎬',
      title: 'Al cinema, le luci si accendono',
      desc: 'Le luci si accendono e una voce dice di uscire. Vedi due porte: una col simbolo verde, una con scritto SOLO PERSONALE.',
      choices: [
        { text: 'Porta col simbolo verde dell’omino', icon: '🚶', correct: true },
        { text: 'Porta SOLO PERSONALE', icon: '🚫', correct: false },
        { text: 'Resto seduto al mio posto', icon: '💁', correct: false }
      ],
      feedback: 'Il cartello verde con l’omino che corre indica sempre la via di fuga sicura. SOLO PERSONALE non è per il pubblico.'
    },
    {
      icon: '🚌',
      title: 'In autobus, c’è un problema',
      desc: 'L’autobus si ferma e l’autista dice di scendere subito.',
      choices: [
        { text: 'Scendo dalla porta che apre l’autista, calmo', icon: '🚪', correct: true },
        { text: 'Rompo il vetro col martelletto rosso', icon: '🔨', correct: false },
        { text: 'Resto seduto e aspetto', icon: '💁', correct: false }
      ],
      feedback: 'Si scende dalla porta normale, in fila, senza spingere. Il martelletto si usa SOLO se la porta non si apre.'
    },
    {
      icon: '🏢',
      title: 'In un palazzo alto, suona l’allarme',
      desc: 'Sei al terzo piano di un palazzo. Suona l’allarme antincendio.',
      choices: [
        { text: 'Scendo dalle scale di emergenza', icon: '🪜', correct: true },
        { text: 'Prendo l’ascensore', icon: '🛀', correct: false },
        { text: 'Salto dalla finestra', icon: '🪟', correct: false }
      ],
      feedback: 'Le scale di emergenza sono sicure. L’ascensore in caso di incendio si può bloccare. Mai saltare dalla finestra.'
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

  function loadScenario() {
    var s = scenarios[currentIndex];
    document.getElementById('scenario-icon').textContent = s.icon;
    document.getElementById('scenario-title').textContent = s.title;
    document.getElementById('scenario-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = scenarios.length;
    document.getElementById('score').textContent = score;
    hide(document.getElementById('feedback-box'));

    var container = document.getElementById('choices');
    container.innerHTML = '';
    var shuffled = shuffle(s.choices.slice());
    shuffled.forEach(function (c) {
      var btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.innerHTML = '<span class="choice-icon" aria-hidden="true">' + c.icon + '</span><span>' + c.text + '</span>';
      btn.addEventListener('click', function () { handleChoice(btn, c, s); });
      container.appendChild(btn);
    });
  }

  function handleChoice(btn, choice, scenario) {
    document.querySelectorAll('.choice-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');
    if (choice.correct) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box feedback-correct';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    } else {
      btn.classList.add('wrong');
      var correctText = scenario.choices.filter(function (c) { return c.correct; })[0].text;
      document.querySelectorAll('.choice-btn').forEach(function (b) {
        if (b.querySelector('span:last-child').textContent === correctText) {
          b.classList.add('correct');
        }
      });
      fb.className = 'feedback-box feedback-wrong';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    }
    show(fb);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < scenarios.length) {
        loadScenario();
      } else {
        hide(document.getElementById('game-screen'));
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = scenarios.length;
        show(document.getElementById('end-screen'));
      }
    }, 3500);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(document.getElementById('intro-screen'));
    show(document.getElementById('game-screen'));
    currentIndex = 0;
    score = 0;
    shuffle(scenarios);
    loadScenario();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(document.getElementById('end-screen'));
    show(document.getElementById('intro-screen'));
  });
})();
