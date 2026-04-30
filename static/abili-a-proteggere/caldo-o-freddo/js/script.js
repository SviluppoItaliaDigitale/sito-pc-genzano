/* Caldo o Freddo? — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '☀️',
      title: 'Caldo molto forte, ore 14',
      desc: 'È agosto, fa 38 gradi. Hai sete. Cosa bevi?',
      choices: [
        { text: 'Acqua fresca, a piccoli sorsi', icon: '💧', correct: true },
        { text: 'Una birra ghiacciata', icon: '🍺', correct: false },
        { text: 'Una bibita gassata zuccherata', icon: '🥤', correct: false }
      ],
      feedback: 'Bravo! L\'acqua è la scelta giusta. Birra e alcolici disidratano. Bevande zuccherate non aiutano. Bevi spesso anche se non hai sete.'
    },
    {
      icon: '🥵',
      title: 'Esci con il caldo',
      desc: 'Devi uscire alle 15 a fare la spesa. Cosa metti?',
      choices: [
        { text: 'Cappellino, occhiali da sole, vestiti chiari leggeri', icon: '🧢', correct: true },
        { text: 'Maglietta nera, pantaloni stretti', icon: '👕', correct: false },
        { text: 'Niente, così sento meno caldo', icon: '🩳', correct: false }
      ],
      feedback: 'Bravo! Cappello e vestiti chiari riflettono il sole. Il nero scalda di più. La pelle scoperta scotta. Meglio uscire prima delle 11 o dopo le 18.'
    },
    {
      icon: '👵',
      title: 'Una vicina anziana',
      desc: 'C\'è il bollino rosso per il caldo. La signora del piano sotto vive sola. Cosa fai?',
      choices: [
        { text: 'Suono al campanello e chiedo se sta bene', icon: '🔔', correct: true },
        { text: 'Niente, non sono affari miei', icon: '🤷', correct: false },
        { text: 'Le porto un caffè caldo', icon: '☕', correct: false }
      ],
      feedback: 'Bravo! Gli anziani soffrono molto il caldo e a volte non se ne accorgono. Un controllo veloce può salvargli la vita. Il caffè caldo no, è bene chiedere se ha acqua.'
    },
    {
      icon: '🥶',
      title: 'Freddo intenso, neve',
      desc: 'Sei a Genzano, è gennaio, sono -2 gradi. Devi andare a scuola. Cosa metti?',
      choices: [
        { text: 'Vestiti a strati: maglietta, felpa, giacca', icon: '🧥', correct: true },
        { text: 'Solo una maglia spessa pesante', icon: '👚', correct: false },
        { text: 'Tre giacche una sopra l\'altra', icon: '🥼', correct: false }
      ],
      feedback: 'Bravo! Vestirsi a strati è meglio: l\'aria tra gli strati scalda. Una maglia sola, anche pesante, scalda meno. Tre giacche stringono e fanno male alle braccia.'
    },
    {
      icon: '🚗',
      title: 'Auto al sole',
      desc: 'Esci dal supermercato, l\'auto è ferma al sole da 2 ore. C\'è dentro un cane (non tuo). Cosa fai?',
      choices: [
        { text: 'Chiamo il 112 e resto vicino all\'auto', icon: '📞', correct: true },
        { text: 'Aspetto che torni il padrone', icon: '⏰', correct: false },
        { text: 'Rompo il vetro subito', icon: '🔨', correct: false }
      ],
      feedback: 'Bravo! Un\'auto al sole arriva a 60 gradi: il cane può morire in 15 minuti. Chiama il 112: i Carabinieri o i Vigili intervengono. Rompere il vetro è reato se non c\'è autorità presente.'
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
