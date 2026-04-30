/* Casa che Trema — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🏠',
      title: 'In cucina, mentre cucini',
      desc: 'La terra inizia a tremare. Sei in cucina vicino ai fornelli accesi. Cosa fai?',
      choices: [
        { text: 'Spengo il fuoco e mi riparo sotto al tavolo', icon: '🪑', correct: true },
        { text: 'Corro fuori in strada', icon: '🏃', correct: false },
        { text: 'Mi nascondo dentro il frigo', icon: '🧊', correct: false }
      ],
      feedback: 'Bravo! Spegni il fuoco se puoi farlo in un secondo, poi riparati sotto un tavolo robusto. Non correre fuori: in strada cadono cose.'
    },
    {
      icon: '🛏️',
      title: 'A letto, di notte',
      desc: 'Ti svegli e il letto trema forte. Cosa fai?',
      choices: [
        { text: 'Resto a letto e mi copro la testa con il cuscino', icon: '🛏️', correct: true },
        { text: 'Salto giù e corro alla porta', icon: '🚪', correct: false },
        { text: 'Accendo la luce e guardo dalla finestra', icon: '💡', correct: false }
      ],
      feedback: 'Giusto! Resta a letto e proteggi testa e collo con il cuscino. Saltare giù al buio è pericoloso, puoi cadere o ferirti.'
    },
    {
      icon: '🏫',
      title: 'A scuola, in classe',
      desc: 'Sei a scuola, la maestra grida "terremoto!". Cosa fai?',
      choices: [
        { text: 'Vado sotto al banco e mi tengo le gambe', icon: '📚', correct: true },
        { text: 'Corro subito alla finestra', icon: '🪟', correct: false },
        { text: 'Mi metto in fila per uscire', icon: '🚶', correct: false }
      ],
      feedback: 'Bravo! Sotto al banco sei al sicuro dalla caduta di lampadari e oggetti. Si esce solo dopo, quando smette di tremare e la maestra lo dice.'
    },
    {
      icon: '🛗',
      title: 'In ascensore',
      desc: 'Stai usando l\'ascensore e sentì la terra tremare. Cosa fai?',
      choices: [
        { text: 'Premo il piano più vicino ed esco subito', icon: '🛑', correct: true },
        { text: 'Continuo a salire fino a casa', icon: '⬆️', correct: false },
        { text: 'Premo il pulsante di allarme e aspetto dentro', icon: '🔔', correct: false }
      ],
      feedback: 'Bravo! L\'ascensore può bloccarsi durante il terremoto. Premi il piano più vicino ed esci appena si apre la porta. Poi usa le scale.'
    },
    {
      icon: '✅',
      title: 'La scossa è finita',
      desc: 'Ha smesso di tremare. Sei in casa, illeso. Cosa fai prima?',
      choices: [
        { text: 'Esco con calma e vado in un\'area aperta', icon: '🌳', correct: true },
        { text: 'Accendo la luce e il gas per vedere meglio', icon: '🔥', correct: false },
        { text: 'Chiamo subito amici per raccontare', icon: '📱', correct: false }
      ],
      feedback: 'Bravo! Esci con scarpe robuste e vai in un\'area aperta lontana da edifici. Non accendere fuoco o luce: potrebbero esserci fughe di gas.'
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
      if (currentIndex < scenarios.length) {
        loadScenario();
      } else {
        showEnd();
      }
    }, 3500);
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
