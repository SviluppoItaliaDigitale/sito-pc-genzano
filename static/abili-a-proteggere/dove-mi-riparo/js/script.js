/* Dove Mi Riparo? — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🏠💨',
      title: 'Terremoto in casa',
      desc: 'La terra trema mentre sei in casa. Dove ti ripari?',
      choices: [
        { text: 'Sotto il tavolo', icon: '🪑', correct: true },
        { text: 'Vicino alla finestra', icon: '🪟', correct: false },
        { text: 'Davanti all’ascensore', icon: '🛗', correct: false }
      ],
      feedback: 'Sotto il tavolo è il posto più sicuro! Proteggiti la testa e tieni le gambe del tavolo.'
    },
    {
      icon: '🏫💨',
      title: 'Terremoto a scuola',
      desc: 'Sei a scuola e la terra trema. Dove ti ripari?',
      choices: [
        { text: 'Corro fuori subito', icon: '🏃', correct: false },
        { text: 'Sotto il banco', icon: '📚', correct: true },
        { text: 'In piedi vicino alla porta', icon: '🚪', correct: false }
      ],
      feedback: 'Bravo! Sotto il banco sei al sicuro. Aspetta che la maestra dica di uscire.'
    },
    {
      icon: '⛈️',
      title: 'Temporale forte',
      desc: 'C’è un temporale forte con tanti fulmini. Sei fuori. Dove vai?',
      choices: [
        { text: 'Sotto un albero alto', icon: '🌳', correct: false },
        { text: 'Dentro un edificio', icon: '🏠', correct: true },
        { text: 'Nel campo aperto', icon: '🌾', correct: false }
      ],
      feedback: 'Dentro un edificio sei al sicuro dai fulmini! Mai stare sotto gli alberi durante un temporale.'
    },
    {
      icon: '🔥',
      title: 'Fumo in una stanza',
      desc: 'Vedi del fumo uscire da una stanza. Cosa fai?',
      choices: [
        { text: 'Apro la porta per guardare', icon: '🚪', correct: false },
        { text: 'Esco subito e chiamo aiuto', icon: '🚶', correct: true },
        { text: 'Mi nascondo sotto il letto', icon: '🛏️', correct: false }
      ],
      feedback: 'Giusto! Esci subito e chiama il 112 o un adulto. Non aprire mai la porta dove c’è fumo!'
    },
    {
      icon: '🌊',
      title: 'Acqua per strada',
      desc: 'Piove tantissimo e c’è acqua alta per strada. Dove stai?',
      choices: [
        { text: 'Ai piani alti di casa', icon: '🏠', correct: true },
        { text: 'In cantina', icon: '🪜', correct: false },
        { text: 'Cammino nell’acqua', icon: '🚶', correct: false }
      ],
      feedback: 'Ai piani alti sei al sicuro! Non scendere mai in cantina quando c’è un’alluvione.'
    }
  ];

  var currentIndex = 0;
  var score = 0;

  var introScreen = document.getElementById('intro-screen');
  var gameScreen = document.getElementById('game-screen');
  var endScreen = document.getElementById('end-screen');
  var scenarioIcon = document.getElementById('scenario-icon');
  var scenarioTitle = document.getElementById('scenario-title');
  var scenarioDesc = document.getElementById('scenario-desc');
  var choicesContainer = document.getElementById('choices');
  var feedbackBox = document.getElementById('feedback-box');
  var currentQ = document.getElementById('current-q');
  var totalQ = document.getElementById('total-q');
  var scoreEl = document.getElementById('score');

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }

  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
  }

  function loadScenario() {
    var s = scenarios[currentIndex];
    scenarioIcon.textContent = s.icon;
    scenarioTitle.textContent = s.title;
    scenarioDesc.textContent = s.desc;
    currentQ.textContent = currentIndex + 1;
    totalQ.textContent = scenarios.length;
    scoreEl.textContent = score;
    hide(feedbackBox);

    choicesContainer.innerHTML = '';
    var shuffled = shuffle(s.choices.slice());
    shuffled.forEach(function (c) {
      var btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.innerHTML = '<span class="choice-icon" aria-hidden="true">' + c.icon + '</span><span>' + c.text + '</span>';
      btn.addEventListener('click', function () { handleChoice(btn, c, s); });
      choicesContainer.appendChild(btn);
    });
  }

  function handleChoice(btn, choice, scenario) {
    // Disable all buttons
    document.querySelectorAll('.choice-btn').forEach(function (b) { b.disabled = true; });

    if (choice.correct) {
      btn.classList.add('correct');
      score++;
      scoreEl.textContent = score;
      feedbackBox.className = 'feedback-box feedback-correct';
      feedbackBox.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    } else {
      btn.classList.add('wrong');
      // Highlight the correct one
      document.querySelectorAll('.choice-btn').forEach(function (b, idx) {
        // Find the correct choice
        var matchText = scenario.choices.filter(function (c) { return c.correct; })[0].text;
        if (b.querySelector('span:last-child').textContent === matchText) {
          b.classList.add('correct');
        }
      });
      feedbackBox.className = 'feedback-box feedback-wrong';
      feedbackBox.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    }
    show(feedbackBox);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < scenarios.length) {
        loadScenario();
      } else {
        showEnd();
      }
    }, 3000);
  }

  function showEnd() {
    hide(gameScreen);
    document.getElementById('final-score').textContent = score;
    document.getElementById('final-total').textContent = scenarios.length;
    show(endScreen);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(introScreen);
    show(gameScreen);
    currentIndex = 0;
    score = 0;
    shuffle(scenarios);
    loadScenario();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(endScreen);
    show(introScreen);
  });
})();
