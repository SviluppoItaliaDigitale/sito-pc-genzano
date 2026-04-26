/* Le Mie Emozioni — Auto-regolazione emotiva in emergenza */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '😨',
      title: 'Sono molto spaventato',
      desc: 'Hai sentito una scossa o un rumore forte e adesso il cuore batte velocemente.',
      choices: [
        { text: 'Respiro lentamente: dentro dal naso, fuori dalla bocca', icon: '🫁', correct: true },
        { text: 'Inizio a urlare', icon: '😱', correct: false },
        { text: 'Trattengo il respiro', icon: '😶', correct: false }
      ],
      feedback: 'Il respiro lento (dentro 4 secondi, fuori 6) calma davvero il cuore. È la tecnica più semplice e funziona in pochi minuti.'
    },
    {
      icon: '😵',
      title: 'Sono confuso, non capisco cosa fare',
      desc: 'Ti senti la testa piena, non riesci a decidere cosa fare prima.',
      choices: [
        { text: 'Mi fermo, dico ad alta voce: "Prima respiro, poi guardo, poi scelgo"', icon: '🧠', correct: true },
        { text: 'Provo a fare tante cose insieme', icon: '🌀', correct: false },
        { text: 'Aspetto che qualcuno decida per me', icon: '⏳', correct: false }
      ],
      feedback: 'Parlare a voce alta a sé stessi aiuta a riordinare i pensieri. Una cosa alla volta: è la regola d’oro nella confusione.'
    },
    {
      icon: '😢',
      title: 'Mi viene da piangere',
      desc: 'Senti gli occhi che si riempiono di lacrime. È normale, non sei debole.',
      choices: [
        { text: 'Piango per qualche secondo, poi ricomincio a respirare', icon: '💧', correct: true },
        { text: 'Mi vergogno e blocco le lacrime', icon: '🙈', correct: false },
        { text: 'Mi nascondo da tutti', icon: '🚪', correct: false }
      ],
      feedback: 'Piangere libera la tensione. Non c’è nulla di cui vergognarsi: è una reazione sana. Dopo, riprendi a respirare e vai avanti.'
    },
    {
      icon: '😡',
      title: 'Sono molto arrabbiato',
      desc: 'Senti rabbia per la situazione, vorresti urlare o rompere qualcosa.',
      choices: [
        { text: 'Stringo i pugni forte, conto fino a 10, poi rilascio', icon: '✊', correct: true },
        { text: 'Lancio l’oggetto più vicino', icon: '🪨', correct: false },
        { text: 'Litigo con chi mi sta vicino', icon: '🗣️', correct: false }
      ],
      feedback: 'Stringere e rilasciare i pugni scarica la rabbia in modo sicuro. Litigare o lanciare oggetti durante un’emergenza fa solo danni.'
    },
    {
      icon: '😶',
      title: 'Mi sento congelato, non riesco a muovermi',
      desc: 'Il corpo è bloccato, le gambe non rispondono. È una reazione normale alla paura.',
      choices: [
        { text: 'Muovo prima un dito, poi una mano, poi un piede, lentamente', icon: '☝️', correct: true },
        { text: 'Provo a saltare in piedi all’improvviso', icon: '🦘', correct: false },
        { text: 'Mi sgrido per non muovermi', icon: '😤', correct: false }
      ],
      feedback: 'Quando il corpo si blocca si riparte dal piccolo: un dito, una mano. È un trucco usato anche dai soccorritori per "scongelarsi".'
    },
    {
      icon: '🤝',
      title: 'Ho bisogno di non essere solo',
      desc: 'Ti senti meglio se hai qualcuno vicino. Anche solo una voce al telefono.',
      choices: [
        { text: 'Chiamo un familiare o un vicino di fiducia', icon: '📞', correct: true },
        { text: 'Faccio finta di stare bene', icon: '😶', correct: false },
        { text: 'Mi chiudo in camera senza dire niente', icon: '🚪', correct: false }
      ],
      feedback: 'Chiedere compagnia quando si ha paura non è debolezza, è intelligenza. Anche una voce al telefono fa molta differenza.'
    }
  ];

  var currentIndex = 0;
  var score = 0;

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }
  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function loadScenario() {
    var s = scenarios[currentIndex];
    document.getElementById('scenario-icon').textContent = s.icon;
    document.getElementById('scenario-title').textContent = s.title;
    document.getElementById('scenario-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = scenarios.length;
    document.getElementById('score').textContent = score;
    hide(document.getElementById('feedback-box'));

    var container = document.getElementById('choices');
    container.innerHTML = '';
    var shuffled = shuffle(s.choices.slice());
    shuffled.forEach(function (c) {
      var btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.innerHTML = '<span class="choice-icon" aria-hidden="true">' + c.icon + '</span><span>' + c.text + '</span>';
      btn.addEventListener('click', function () { handleChoice(btn, c, s); });
      container.appendChild(btn);
    });
  }

  function handleChoice(btn, choice, scenario) {
    document.querySelectorAll('.choice-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');
    if (choice.correct) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box feedback-correct';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    } else {
      btn.classList.add('wrong');
      var correctText = scenario.choices.filter(function (c) { return c.correct; })[0].text;
      document.querySelectorAll('.choice-btn').forEach(function (b) {
        if (b.querySelector('span:last-child').textContent === correctText) {
          b.classList.add('correct');
        }
      });
      fb.className = 'feedback-box feedback-wrong';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + scenario.feedback;
    }
    show(fb);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < scenarios.length) {
        loadScenario();
      } else {
        hide(document.getElementById('game-screen'));
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = scenarios.length;
        show(document.getElementById('end-screen'));
      }
    }, 4000);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(document.getElementById('intro-screen'));
    show(document.getElementById('game-screen'));
    currentIndex = 0;
    score = 0;
    shuffle(scenarios);
    loadScenario();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(document.getElementById('end-screen'));
    show(document.getElementById('intro-screen'));
  });
})();
