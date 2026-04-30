/* Casa al Buio — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🌑',
      title: 'È andata via la luce',
      desc: 'Sei in salotto e all\'improvviso tutto si spegne. Cosa accendi prima?',
      choices: [
        { text: 'La torcia che ho nel cassetto', icon: '🔦', correct: true },
        { text: 'Una candela con i fiammiferi', icon: '🕯️', correct: false },
        { text: 'L\'accendino sopra al fornello', icon: '🔥', correct: false }
      ],
      feedback: 'Bravo! La torcia è la scelta più sicura: niente fiamma libera, niente fumo. Le candele sono pericolose, soprattutto se ci sono bambini o animali.'
    },
    {
      icon: '❄️',
      title: 'Frigorifero pieno',
      desc: 'Il blackout dura da un\'ora. Hai fame, vuoi prendere uno yogurt. Cosa fai?',
      choices: [
        { text: 'Lo prendo veloce e richiudo subito', icon: '⚡', correct: true },
        { text: 'Lascio aperto il frigo per vedere meglio', icon: '🚪', correct: false },
        { text: 'Tolgo tutto dal frigo e lo metto sul tavolo', icon: '🍽️', correct: false }
      ],
      feedback: 'Bravo! Ogni volta che apri il frigo perdi freddo. Apri il meno possibile: così il cibo dura 4-6 ore anche senza corrente.'
    },
    {
      icon: '🛗',
      title: 'In ascensore',
      desc: 'L\'ascensore si ferma di colpo: blackout. Cosa fai dentro?',
      choices: [
        { text: 'Premo il pulsante di allarme e aspetto', icon: '🔔', correct: true },
        { text: 'Forzo le porte per uscire', icon: '💪', correct: false },
        { text: 'Salto per riavviare l\'ascensore', icon: '🦘', correct: false }
      ],
      feedback: 'Bravo! Il pulsante di allarme funziona anche senza corrente: si collega alla portineria o ai vigili del fuoco. Resta dentro: forzare le porte è pericoloso.'
    },
    {
      icon: '📱',
      title: 'Telefono e luce',
      desc: 'Il blackout dura da molto. Vuoi risparmiare la batteria del telefono. Cosa fai?',
      choices: [
        { text: 'Metto il telefono in modalità risparmio', icon: '🔋', correct: true },
        { text: 'Guardo video per passare il tempo', icon: '📺', correct: false },
        { text: 'Spengo del tutto il telefono', icon: '⏹️', correct: false }
      ],
      feedback: 'Bravo! Modalità risparmio + niente video. Il telefono ti serve per chiamare il 112 se c\'è bisogno. Spegnerlo del tutto ti lascia isolato.'
    },
    {
      icon: '🏠',
      title: 'È inverno e fa freddo',
      desc: 'Senza corrente non funziona il riscaldamento. Hai freddo. Cosa fai?',
      choices: [
        { text: 'Mi metto vestiti pesanti e sto in una stanza sola', icon: '🧥', correct: true },
        { text: 'Accendo il forno a gas con sportello aperto', icon: '🔥', correct: false },
        { text: 'Apro le finestre per cambiare aria', icon: '🪟', correct: false }
      ],
      feedback: 'Bravo! Vestiti a strati, coperte, una stanza sola riscaldata dal corpo. Mai usare forno o bracieri dentro casa: producono monossido di carbonio, un gas mortale.'
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
