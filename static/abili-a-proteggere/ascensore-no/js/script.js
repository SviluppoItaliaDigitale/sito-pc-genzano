/* L'Ascensore NO! — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🔥',
      title: 'C\'è un incendio nel palazzo',
      desc: 'Senti l\'allarme antincendio e vedi del fumo nel corridoio. Devi scendere dal terzo piano. Cosa fai?',
      choices: [
        { text: 'No, prendo le scale', icon: '🚶', correct: true },
        { text: 'Sì, è più veloce', icon: '🛗', correct: false }
      ],
      feedback: 'Bravo! In incendio mai usare l\'ascensore: si può bloccare al piano del fuoco e il fumo entra nella cabina. Sempre le scale.'
    },
    {
      icon: '🌍',
      title: 'La terra ha tremato',
      desc: 'Una scossa di terremoto è appena finita. Sei al quinto piano e vuoi scendere a controllare. Cosa fai?',
      choices: [
        { text: 'No, prendo le scale', icon: '🚶', correct: true },
        { text: 'Sì, scendo veloce', icon: '🛗', correct: false }
      ],
      feedback: 'Bravo! Dopo un terremoto l\'ascensore può essere danneggiato e bloccarsi tra i piani. Le scale sono più sicure anche se più faticose.'
    },
    {
      icon: '⚡',
      title: 'È andata via la luce',
      desc: 'Blackout in tutto il palazzo. Devi scendere a chiamare un parente. Cosa fai?',
      choices: [
        { text: 'No, prendo le scale con la torcia', icon: '🔦', correct: true },
        { text: 'Sì, c\'è il gruppo elettrogeno', icon: '🛗', correct: false }
      ],
      feedback: 'Bravo! Senza corrente l\'ascensore non funziona o si ferma tra i piani. Anche se c\'è il gruppo elettrogeno, può guastarsi. Scale + torcia.'
    },
    {
      icon: '🌬️',
      title: 'Sento puzza di gas',
      desc: 'In casa senti odore di gas. Devi uscire subito. Cosa fai?',
      choices: [
        { text: 'No, scale e basta — niente bottoni', icon: '🚶', correct: true },
        { text: 'Sì, premo il pulsante per uscire', icon: '🛗', correct: false }
      ],
      feedback: 'Bravo! Premere un pulsante elettrico vicino al gas può accendere una scintilla. Esci dalle scale, niente luci, niente ascensori, e chiama il 112.'
    },
    {
      icon: '🚑',
      title: 'Un anziano si è sentito male',
      desc: 'Tuo nonno deve scendere per salire in ambulanza. È al quarto piano e non cammina bene. I soccorritori sono arrivati. Cosa dici?',
      choices: [
        { text: 'Sì, l\'ascensore se lo dicono i soccorritori', icon: '🛗', correct: true },
        { text: 'No, sempre scale anche per i feriti', icon: '🚶', correct: false }
      ],
      feedback: 'Bravo! In situazione non emergenza per l\'edificio (nessun incendio o sisma) i soccorritori valutano e possono usare l\'ascensore se è sicuro. La regola "no ascensore" vale per emergenze sull\'edificio stesso.'
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
    document.querySelectorAll('.choice-btn').forEach(function (b) { b.disabled = true; });
    if (choice.correct) {
      btn.classList.add('correct');
      score++;
      scoreEl.textContent = score;
      feedbackBox.className = 'feedback-box feedback-correct';
      feedbackBox.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    } else {
      btn.classList.add('wrong');
      document.querySelectorAll('.choice-btn').forEach(function (b) {
        var matchText = scenario.choices.filter(function (c) { return c.correct; })[0].text;
        if (b.querySelector('span:last-child').textContent === matchText) b.classList.add('correct');
      });
      feedbackBox.className = 'feedback-box feedback-wrong';
      feedbackBox.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    }
    show(feedbackBox);
    setTimeout(function () {
      currentIndex++;
      if (currentIndex < scenarios.length) loadScenario();
      else showEnd();
    }, 3500);
  }

  function showEnd() {
    hide(gameScreen);
    document.getElementById('final-score').textContent = score;
    document.getElementById('final-total').textContent = scenarios.length;
    show(endScreen);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(introScreen); show(gameScreen);
    currentIndex = 0; score = 0;
    shuffle(scenarios);
    loadScenario();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(endScreen); show(introScreen);
  });
})();
