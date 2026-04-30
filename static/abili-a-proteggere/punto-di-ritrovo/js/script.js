/* Il Punto di Ritrovo — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🏛️',
      title: 'Quale punto scegli?',
      desc: 'Devi scegliere un posto dove ritrovarti con la famiglia. Quale è meglio?',
      choices: [
        { text: 'Una piazza grande, lontana da edifici alti', icon: '🟦', correct: true },
        { text: 'Sotto un albero del parco', icon: '🌳', correct: false },
        { text: 'Davanti a casa nostra', icon: '🏠', correct: false }
      ],
      feedback: 'Bravo! Una piazza grande e aperta è sicura: niente cose che cadono. Gli alberi possono cadere. Davanti a casa è rischioso se la casa è danneggiata.'
    },
    {
      icon: '🏫',
      title: 'Sei a scuola, c\'è il terremoto',
      desc: 'È finito il terremoto. La maestra dice di uscire. Tua mamma è al lavoro, papà a fare la spesa. Avete deciso un punto di ritrovo. Cosa fai?',
      choices: [
        { text: 'Aspetto a scuola che venga un genitore o resto con la maestra', icon: '👩‍🏫', correct: true },
        { text: 'Vado da solo al punto di ritrovo', icon: '🚶', correct: false },
        { text: 'Torno a casa correndo', icon: '🏃', correct: false }
      ],
      feedback: 'Bravo! Se sei a scuola, la maestra è responsabile di te. Aspetta lì che arrivi un genitore. Il punto di ritrovo è per chi è già fuori, non per i bambini a scuola.'
    },
    {
      icon: '📋',
      title: 'Quanti punti di ritrovo?',
      desc: 'State decidendo i punti di ritrovo. Quanti ne servono?',
      choices: [
        { text: 'Due: uno vicino a casa, uno fuori dal quartiere', icon: '2️⃣', correct: true },
        { text: 'Uno solo, così non si confonde nessuno', icon: '1️⃣', correct: false },
        { text: 'Cinque o più, per tutte le situazioni', icon: '5️⃣', correct: false }
      ],
      feedback: 'Bravo! Due punti: uno vicino casa per emergenze locali (es. fuga di gas), uno più lontano per emergenze grandi (es. evacuazione del paese). Più di due si confondono.'
    },
    {
      icon: '🤝',
      title: 'Punto vicino a casa',
      desc: 'Quale di questi è un buon punto di ritrovo VICINO casa tua?',
      choices: [
        { text: 'Davanti alla farmacia, sul marciapiede largo', icon: '🏥', correct: true },
        { text: 'In cima alla scala del condominio', icon: '🪜', correct: false },
        { text: 'Nella nostra cantina', icon: '⬇️', correct: false }
      ],
      feedback: 'Bravo! La farmacia è un punto chiaro, conosciuto da tutti, su strada larga. Le scale e la cantina sono dentro l\'edificio: in emergenza si potrebbero non poter raggiungere.'
    },
    {
      icon: '✏️',
      title: 'Cosa fai dopo aver scelto?',
      desc: 'Avete deciso il punto di ritrovo: piazza Tommaso Frasconi a Genzano. Cosa fate adesso?',
      choices: [
        { text: 'Lo scriviamo nel piano familiare e lo proviamo', icon: '📝', correct: true },
        { text: 'Lo ricordiamo a memoria, non serve scriverlo', icon: '🤔', correct: false },
        { text: 'Lo dimentichiamo finché non serve davvero', icon: '😴', correct: false }
      ],
      feedback: 'Bravo! Scriverlo + provarlo (es. fare un\'esercitazione una volta l\'anno) lo rende automatico. In emergenza la paura cancella la memoria: avere un foglio o un messaggio sul telefono salva tempo.'
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
