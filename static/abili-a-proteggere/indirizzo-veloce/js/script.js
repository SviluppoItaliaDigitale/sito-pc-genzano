/* L'Indirizzo Veloce — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🏠',
      title: 'Sei a casa tua',
      desc: 'Hai chiamato il 112. L\'operatore dice: "Buongiorno, mi dica dove si trova". Sei nel salotto di casa tua. Cosa dici?',
      choices: [
        { text: 'Via, numero civico, e "Genzano di Roma"', icon: '📍', correct: true },
        { text: 'Sono a casa mia', icon: '🏡', correct: false },
        { text: 'Vicino al supermercato', icon: '🛒', correct: false }
      ],
      feedback: 'Bravo! "Via Italia 12, Genzano di Roma" è perfetto. "Casa mia" e "vicino al supermercato" non bastano: il 112 non sa dove abiti.'
    },
    {
      icon: '🏬',
      title: 'In un negozio',
      desc: 'Sei al supermercato e vedi una persona stare male. Chiami il 112. Cosa dici subito?',
      choices: [
        { text: 'Sono al supermercato di via X numero Y a Genzano', icon: '🏬', correct: true },
        { text: 'Sono nel supermercato vicino al parco', icon: '🌳', correct: false },
        { text: 'Sono in centro città', icon: '🏙️', correct: false }
      ],
      feedback: 'Bravo! Dai sempre il nome del posto + via + numero + paese. Se non lo sai, leggilo dallo scontrino o chiedi a un commesso.'
    },
    {
      icon: '🌲',
      title: 'In gita al lago',
      desc: 'Sei al Lago di Nemi. Tuo nonno cade e si fa male. Chiami il 112. Non sai l\'indirizzo esatto. Cosa dici?',
      choices: [
        { text: 'Siamo al Lago di Nemi, sentiero blu, vicino a un cartello con scritto "Belvedere"', icon: '🪧', correct: true },
        { text: 'Siamo al lago, venite presto', icon: '⏱️', correct: false },
        { text: 'Siamo nel bosco', icon: '🌳', correct: false }
      ],
      feedback: 'Bravo! Quando non hai l\'indirizzo, dai riferimenti visibili: nome del lago, cartelli, panchine, fontane, il colore del sentiero. Anche un albero grande aiuta.'
    },
    {
      icon: '📱',
      title: 'Non ricordo l\'indirizzo',
      desc: 'Sei agitato e ti sei dimenticato la via di casa. L\'operatore aspetta. Cosa fai?',
      choices: [
        { text: 'Apro la mappa del telefono e leggo dove sono', icon: '🗺️', correct: true },
        { text: 'Riattacco e ci penso meglio', icon: '☎️', correct: false },
        { text: 'Dico un indirizzo a caso', icon: '🎲', correct: false }
      ],
      feedback: 'Bravo! Il telefono sa sempre dove sei: apri Google Maps o Apple Mappe e leggi a voce. Mai riattaccare il 112: l\'operatore ti aiuta a trovare le parole.'
    },
    {
      icon: '🚗',
      title: 'In macchina, in autostrada',
      desc: 'Sei in autostrada e vedi un incidente. Chiami il 112. Come dici dove sei?',
      choices: [
        { text: 'Autostrada A1, direzione Roma, vicino al km 25', icon: '🛣️', correct: true },
        { text: 'In autostrada', icon: '🚙', correct: false },
        { text: 'In direzione del Sud', icon: '🧭', correct: false }
      ],
      feedback: 'Bravo! Sull\'autostrada ci sono cartelli verdi con il chilometro ogni 100 metri. Dai: nome dell\'autostrada (A1, A24...), direzione (Roma, Napoli), e il chilometro più vicino.'
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
