/* Animale e Io — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🎒',
      title: 'Cosa metto nello zaino del cane?',
      desc: 'Stai preparando un kit emergenza per il tuo cane. Cosa è più importante avere?',
      choices: [
        { text: 'Trasportino, libretto sanitario, cibo, acqua, guinzaglio', icon: '📦', correct: true },
        { text: 'Tanti giocattoli e biscotti', icon: '🎾', correct: false },
        { text: 'Solo il guinzaglio, basta quello', icon: '🦮', correct: false }
      ],
      feedback: 'Bravo! Trasportino + libretto sanitario (con microchip) + cibo per 3 giorni + acqua + guinzaglio + museruola se prevista. Giocattoli sono in più, non essenziali.'
    },
    {
      icon: '🚪',
      title: 'Si esce di corsa',
      desc: 'C\'è un\'emergenza, devi uscire di casa. Hai un gatto. Cosa fai?',
      choices: [
        { text: 'Lo metto nel trasportino e lo porto con me', icon: '🐱', correct: true },
        { text: 'Lo lascio in casa, sa cavarsela', icon: '🏠', correct: false },
        { text: 'Lo metto in macchina libero', icon: '🚗', correct: false }
      ],
      feedback: 'Bravo! Mai lasciare un animale in casa: in emergenza non sa che fare e potrebbe non essere recuperabile. Mai libero in auto: si spaventa, scappa, può causare incidenti.'
    },
    {
      icon: '🆘',
      title: 'Centro di accoglienza',
      desc: 'Devi andare in un centro di accoglienza per emergenze. Hai il tuo cane. Cosa fai?',
      choices: [
        { text: 'Chiedo ai volontari se accettano animali', icon: '🙋', correct: true },
        { text: 'Lo lascio fuori legato a un palo', icon: '🪢', correct: false },
        { text: 'Lo nascondo nello zaino', icon: '🎒', correct: false }
      ],
      feedback: 'Bravo! In Italia molti centri accolgono animali (legge nazionale). I volontari di Protezione Civile ti dicono come fare. Mai lasciarlo fuori al freddo o al caldo.'
    },
    {
      icon: '🏷️',
      title: 'Identificazione',
      desc: 'Cosa è più utile per ritrovare il tuo cane se si perde in emergenza?',
      choices: [
        { text: 'Microchip + medaglietta col numero di telefono', icon: '📡', correct: true },
        { text: 'Una foto sul telefono', icon: '📸', correct: false },
        { text: 'Un fischietto speciale per chiamarlo', icon: '🪈', correct: false }
      ],
      feedback: 'Bravo! Microchip è obbligatorio per legge in Italia per i cani: i veterinari e i Carabinieri possono leggerlo. Medaglietta col tuo telefono = se chi lo trova è una persona normale, ti chiama subito.'
    },
    {
      icon: '🐦',
      title: 'Ho un canarino',
      desc: 'Hai un canarino in gabbia. Devi evacuare. Cosa fai?',
      choices: [
        { text: 'Copro la gabbia con un telo e la porto con me', icon: '🪶', correct: true },
        { text: 'Lo lascio andare libero, è meglio', icon: '🕊️', correct: false },
        { text: 'Lascio la gabbia in casa con cibo', icon: '🥣', correct: false }
      ],
      feedback: 'Bravo! Copri la gabbia (riduce stress) e portala. Liberare un canarino domestico in città vuol dire morte certa: non sa procurarsi cibo. La gabbia in casa con cibo non basta in emergenza prolungata.'
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
