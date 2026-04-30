/* L'Acqua Sale! — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🌊',
      title: 'Acqua per strada',
      desc: 'Piove tantissimo. L\'acqua per strada arriva alla caviglia. Devi tornare a casa. Cosa fai?',
      choices: [
        { text: 'Resto dove sono al riparo e chiamo casa', icon: '🏠', correct: true },
        { text: 'Cammino veloce nell\'acqua per arrivare prima', icon: '🚶', correct: false },
        { text: 'Scendo in metropolitana', icon: '🚇', correct: false }
      ],
      feedback: 'Bravo! Anche l\'acqua bassa può nascondere tombini aperti o trascinare via. Resta al riparo e avvisa. Mai entrare in acqua corrente.'
    },
    {
      icon: '🏚️',
      title: 'Acqua entra in casa',
      desc: 'L\'acqua sta entrando dal piano terra di casa tua. Cosa fai prima?',
      choices: [
        { text: 'Salgo al piano alto e chiamo il 112', icon: '⬆️', correct: true },
        { text: 'Scendo in cantina a salvare le cose', icon: '⬇️', correct: false },
        { text: 'Apro la porta per far uscire l\'acqua', icon: '🚪', correct: false }
      ],
      feedback: 'Bravo! Sali sempre ai piani alti. Mai scendere in cantina o seminterrato durante un\'alluvione: l\'acqua arriva veloce e blocca le uscite.'
    },
    {
      icon: '🚗',
      title: 'In auto, strada allagata',
      desc: 'Sei in auto con un familiare. La strada davanti è allagata. Cosa dici?',
      choices: [
        { text: 'Torniamo indietro o cambiamo strada', icon: '↩️', correct: true },
        { text: 'Passiamo veloci, è solo acqua', icon: '⚡', correct: false },
        { text: 'Scendiamo e attraversiamo a piedi', icon: '🚶', correct: false }
      ],
      feedback: 'Bravo! Bastano 30 cm d\'acqua per trascinare via un\'auto. Mai attraversare una strada allagata: torna indietro e cerca un\'altra via.'
    },
    {
      icon: '🌉',
      title: 'Sottopasso allagato',
      desc: 'Il sottopasso che usi sempre è pieno d\'acqua. Stai andando a scuola. Cosa fai?',
      choices: [
        { text: 'Faccio una strada più lunga ma asciutta', icon: '🚶', correct: true },
        { text: 'Ci provo, sono solo pochi metri', icon: '➡️', correct: false },
        { text: 'Aspetto un\'ora che l\'acqua scenda', icon: '⏰', correct: false }
      ],
      feedback: 'Bravo! I sottopassi allagati sono pericolosi: l\'acqua può salire in pochi minuti e non si vede il fondo. Allunga la strada, non rischiare.'
    },
    {
      icon: '📱',
      title: 'Allerta arancione',
      desc: 'Il telefono suona: "Allerta meteo arancione domani". Cosa fai?',
      choices: [
        { text: 'Preparo il kit emergenza e resto a casa', icon: '🎒', correct: true },
        { text: 'Vado in gita con gli amici', icon: '🚌', correct: false },
        { text: 'Non leggo il messaggio, è sempre uguale', icon: '📵', correct: false }
      ],
      feedback: 'Bravo! Allerta arancione vuol dire pioggia forte attesa. Prepara il kit (acqua, torcia, medicine) e segui le istruzioni del Comune. Non sottovalutare l\'avviso.'
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
