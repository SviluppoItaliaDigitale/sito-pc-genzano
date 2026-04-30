/* Trovare il Nord — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🌅',
      title: 'Il sole sorge',
      desc: 'È mattina presto. Guardi il sole che si alza sopra le colline. Da quale parte sorge il sole?',
      choices: [
        { text: 'A est', icon: '➡️', correct: true },
        { text: 'A ovest', icon: '⬅️', correct: false },
        { text: 'A nord', icon: '⬆️', correct: false }
      ],
      feedback: 'Bravo! Il sole sorge a est e tramonta a ovest. Se al mattino il sole è davanti a te, il nord è alla tua sinistra. Funziona ovunque sulla Terra.'
    },
    {
      icon: '☀️',
      title: 'Mezzogiorno con sole',
      desc: 'È mezzogiorno e il sole è alto. Vedi la tua ombra. In quale direzione punta l\'ombra (in Italia)?',
      choices: [
        { text: 'Verso nord', icon: '⬆️', correct: true },
        { text: 'Verso sud', icon: '⬇️', correct: false },
        { text: 'Non c\'è ombra a mezzogiorno', icon: '🚫', correct: false }
      ],
      feedback: 'Bravo! In Italia a mezzogiorno il sole è a sud (alto), quindi l\'ombra delle persone e degli alberi punta verso nord. Trucco utile per orientarsi senza bussola.'
    },
    {
      icon: '⛪',
      title: 'Le chiese italiane',
      desc: 'Sei in centro storico e vedi una chiesa antica. La maggior parte delle chiese italiane vecchie è costruita con l\'altare verso quale parte?',
      choices: [
        { text: 'Verso est (l\'altare guarda l\'alba)', icon: '☀️', correct: true },
        { text: 'Verso ovest', icon: '🌅', correct: false },
        { text: 'A caso', icon: '🎲', correct: false }
      ],
      feedback: 'Bravo! Per tradizione le chiese vecchie hanno l\'altare a est (verso il sole che nasce). L\'ingresso (e il campanile) è di solito a ovest. Riferimento utile in città.'
    },
    {
      icon: '🌳',
      title: 'Muschio sugli alberi',
      desc: 'Sei nel bosco. Hai sentito dire che il muschio cresce solo da una parte. È vero?',
      choices: [
        { text: 'Solo come indizio: di solito a nord, ma non sempre', icon: '🤏', correct: true },
        { text: 'Sì, sempre a nord, è una regola sicura', icon: '✅', correct: false },
        { text: 'No, non c\'entra niente con l\'orientamento', icon: '❌', correct: false }
      ],
      feedback: 'Bravo! Il muschio preferisce zone meno soleggiate (quindi spesso a nord), ma dipende anche da umidità, pioggia, alberi vicini. È un indizio, non una regola sicura: usalo insieme al sole.'
    },
    {
      icon: '📞',
      title: 'Mi sono perso, chiamo il 112',
      desc: 'Sei perso in campagna fuori Genzano. Chiami il 112. Vuoi aiutare a farti trovare. Cosa dici?',
      choices: [
        { text: 'Vedo il sole davanti a me alle ore 16, c\'è un capannone giallo a 100 metri', icon: '🌇', correct: true },
        { text: 'Sono a est, in mezzo al niente', icon: '🤷', correct: false },
        { text: 'Non lo so, venitemi a prendere', icon: '😰', correct: false }
      ],
      feedback: 'Bravo! Dai informazioni concrete: posizione del sole + ora (orientamento) + un riferimento visibile (capannone, antenna, fiume). Il 112 incrocia con la tua posizione GPS approssimativa e ti trova prima.'
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
