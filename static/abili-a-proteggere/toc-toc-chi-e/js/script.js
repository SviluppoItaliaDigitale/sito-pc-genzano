/* Toc Toc — Chi è? — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🚒',
      title: 'Vigili del Fuoco',
      desc: 'Bussa una persona con divisa rossa, casco bianco, scritto "VIGILI DEL FUOCO" sulla giacca. Dice "C\'è un controllo dopo il terremoto, posso entrare?". Cosa fai?',
      choices: [
        { text: 'Apro: la divisa è quella vera dei VVF', icon: '✅', correct: true },
        { text: 'Non apro: sembra un travestimento', icon: '❌', correct: false }
      ],
      feedback: 'Bravo! La divisa rossa con casco bianco e scritta "Vigili del Fuoco" è autentica. Se vuoi essere sicuro al 100% puoi chiamare il 112 e chiedere conferma. Sono autorizzati ai controlli post-sisma.'
    },
    {
      icon: '👔',
      title: 'Vestito normale',
      desc: 'Bussa un signore in giacca e cravatta. Dice "Sono dell\'assicurazione del Comune, devo controllare la casa per i danni". Non ha tesserino visibile. Cosa fai?',
      choices: [
        { text: 'Non apro e chiamo il 112', icon: '🚫', correct: true },
        { text: 'Apro: sembra una persona perbene', icon: '🚪', correct: false }
      ],
      feedback: 'Bravo! Senza divisa e senza tesserino visibile è sospetto. Il Comune e le assicurazioni mandano sempre persone con tesserino di riconoscimento. Chiama il 112 o il Comune per conferma.'
    },
    {
      icon: '🚑',
      title: 'Ambulanza al portone',
      desc: 'Suonano dal citofono. Vedi sotto un\'ambulanza bianca e gialla. La voce dice "Soccorso 118, abbiamo ricevuto chiamata per il vostro palazzo". Cosa fai?',
      choices: [
        { text: 'Apro il portone, vado a verificare al pianerottolo', icon: '🛗', correct: true },
        { text: 'Non apro: io non ho chiamato il 118', icon: '🚫', correct: false }
      ],
      feedback: 'Bravo! Spesso le chiamate sono fatte da vicini di casa. Apri il portone ma resta vigile: i veri soccorritori arrivano in 2 con divisa, ambulanza visibile, e ti diranno chi ha chiamato.'
    },
    {
      icon: '👮',
      title: 'Persona in divisa militare',
      desc: 'Bussa un uomo con tuta militare verde, scarponi, niente scritte chiare. Dice "Sono dell\'esercito, dobbiamo perquisire". Cosa fai?',
      choices: [
        { text: 'Non apro e chiamo il 112', icon: '🚫', correct: true },
        { text: 'Apro: la divisa militare è ufficiale', icon: '✅', correct: false }
      ],
      feedback: 'Bravo! L\'esercito non perquisisce case private. I veri militari operano sempre in coordinamento con Carabinieri o Polizia, in gruppo, con ordini scritti. Chiama il 112: ti dicono se c\'è un\'operazione in corso.'
    },
    {
      icon: '🔵',
      title: 'Volontario PC con pettorina',
      desc: 'Una persona con pettorina blu o gialla con scritta "Protezione Civile" e tesserino. Dice "Stiamo distribuendo acqua e bombole per l\'emergenza". Cosa fai?',
      choices: [
        { text: 'Lo ascolto, prendo l\'acqua, ma non lo faccio entrare', icon: '🚪', correct: true },
        { text: 'Lo invito a entrare a riposare', icon: '🛋️', correct: false }
      ],
      feedback: 'Bravo! I volontari di Protezione Civile distribuiscono aiuti porta a porta in emergenza, ma non hanno bisogno di entrare. Ricevi l\'aiuto sulla porta. Chi insiste a entrare è sospetto.'
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
