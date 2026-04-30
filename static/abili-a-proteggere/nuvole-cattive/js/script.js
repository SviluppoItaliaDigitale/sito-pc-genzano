/* Nuvole Cattive — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '☁️',
      title: 'Nuvole grandi nere a forma di torre',
      desc: 'Guardi il cielo: enormi nuvole nere alte come torri. Sei al parco con gli amici. Cosa fai?',
      choices: [
        { text: 'Torno subito a casa o trovo un riparo solido', icon: '🏃', correct: true },
        { text: 'Resto a giocare, manca il temporale', icon: '⚽', correct: false },
        { text: 'Aspetto le prime gocce per rientrare', icon: '💧', correct: false }
      ],
      feedback: 'Bravo! Le nuvole alte e nere a forma di torre (cumulonembi) portano temporali forti con fulmini. Sui Castelli arrivano in fretta. Rientra prima delle gocce.'
    },
    {
      icon: '⚡',
      title: 'Conto i secondi tra fulmine e tuono',
      desc: 'Vedi un fulmine. Conti "1, 2, 3" e senti il tuono. Cosa vuol dire?',
      choices: [
        { text: 'Il temporale è a circa 1 km, troppo vicino', icon: '⚠️', correct: true },
        { text: 'È molto lontano, posso restare fuori', icon: '✅', correct: false },
        { text: 'Non vuol dire niente', icon: '❓', correct: false }
      ],
      feedback: 'Bravo! Ogni 3 secondi tra lampo e tuono = circa 1 km di distanza. Sotto i 30 secondi (10 km) sei in zona pericolo: rientra subito al chiuso.'
    },
    {
      icon: '🌬️',
      title: 'Vento improvviso forte',
      desc: 'C\'era sole, all\'improvviso il vento si alza forte e fa volare cose. Cosa stai per arrivare?',
      choices: [
        { text: 'Un temporale: rientro subito', icon: '⛈️', correct: true },
        { text: 'Solo aria fresca, non importa', icon: '🍃', correct: false },
        { text: 'È normale, può restare cosi tutto il giorno', icon: '😌', correct: false }
      ],
      feedback: 'Bravo! Vento forte improvviso è il segnale che arriva la corrente fredda del temporale. In 10-15 minuti piove e fulmina. Rientra subito.'
    },
    {
      icon: '🌥️',
      title: 'Cielo bianco lattiginoso',
      desc: 'Il cielo è coperto di un velo bianco uniforme. Caldo umido. Cosa pensi?',
      choices: [
        { text: 'Possibile temporale nelle prossime ore: controllo le previsioni', icon: '📱', correct: true },
        { text: 'Brutto tempo per giorni, niente da fare', icon: '😞', correct: false },
        { text: 'Tempo bellissimo, esco senza pensieri', icon: '☀️', correct: false }
      ],
      feedback: 'Bravo! Il cielo lattiginoso d\'estate spesso anticipa temporali pomeridiani. Non è certezza, ma è motivo per controllare l\'allerta meteo prima di una gita o partita.'
    },
    {
      icon: '🌈',
      title: 'Allerta arancione sul telefono',
      desc: 'Arriva un messaggio: "Allerta meteo arancione: temporali forti previsti nelle prossime 12 ore". Cosa fai?',
      choices: [
        { text: 'Sposto le piante dai balconi e chiudo le finestre', icon: '🪴', correct: true },
        { text: 'Cancello la festa al parco e resto a casa', icon: '🎉', correct: true },
        { text: 'Esco subito a fare la spesa con calma', icon: '🛒', correct: false }
      ],
      feedback: 'Bravo! Allerta arancione = limita gli spostamenti. Spostare oggetti dai balconi (vasi, antenne, grucce) evita che cadano col vento. Posticipa eventi all\'aperto.'
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
