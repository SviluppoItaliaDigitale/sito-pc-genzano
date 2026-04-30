/* Il Fischietto SOS — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🆘',
      title: 'Quanti fischi per chiedere aiuto?',
      desc: 'Sei fermo e non riesci a muoverti. Ti hanno detto che il fischietto serve a chiamare aiuto. Quanti fischi fai?',
      choices: [
        { text: 'Tre fischi forti, poi pausa, poi tre fischi forti', icon: '3️⃣', correct: true },
        { text: 'Un solo fischio molto lungo', icon: '1️⃣', correct: false },
        { text: 'Tantissimi fischi velocissimi', icon: '🔁', correct: false }
      ],
      feedback: 'Bravo! Il segnale internazionale è "tre fischi". Si ripete con pause: tre, pausa, tre, pausa, tre. Si distingue dai rumori normali della natura.'
    },
    {
      icon: '🌳',
      title: 'Persi nel bosco',
      desc: 'Sei in gita con la famiglia e ti sei perso. Hai un fischietto al collo. Cosa fai?',
      choices: [
        { text: 'Resto fermo e fischio tre volte ogni minuto', icon: '⏸️', correct: true },
        { text: 'Cammino veloce cercando l\'uscita', icon: '🏃', correct: false },
        { text: 'Urlo "aiuto" più forte che posso', icon: '😱', correct: false }
      ],
      feedback: 'Bravo! Restare fermi è la regola d\'oro: chi ti cerca trova un punto fisso. Il fischietto si sente molto più lontano della voce e fa meno fatica della gola.'
    },
    {
      icon: '🏚️',
      title: 'Sotto le macerie',
      desc: 'Dopo un terremoto sei intrappolato sotto qualcosa che è caduto. Senti voci dei soccorritori che cercano. Hai un fischietto in tasca. Cosa fai?',
      choices: [
        { text: 'Fischio tre volte ogni 30 secondi', icon: '🦺', correct: true },
        { text: 'Fischio senza fermarmi mai', icon: '♾️', correct: false },
        { text: 'Aspetto che mi trovino da soli', icon: '🤐', correct: false }
      ],
      feedback: 'Bravo! Il fischio passa attraverso il rumore e i muri. Risparmia fiato: 3 fischi, pausa, 3 fischi. Battere su tubi metallici fa lo stesso effetto.'
    },
    {
      icon: '🎒',
      title: 'Cosa metto nello zaino emergenza?',
      desc: 'Stai preparando il kit emergenza. C\'è un cassetto con vari oggetti. Cosa scegli?',
      choices: [
        { text: 'Un fischietto a sfera, leggero e attaccato a un cordino', icon: '🪈', correct: true },
        { text: 'Una tromba ad aria, fa più rumore', icon: '📯', correct: false },
        { text: 'Un campanello da bici', icon: '🔔', correct: false }
      ],
      feedback: 'Bravo! Il fischietto a sfera (con la pallina dentro) funziona anche bagnato e con poco fiato. La tromba ad aria si esaurisce. Il campanello si sente poco.'
    },
    {
      icon: '👶',
      title: 'Ho un fratellino piccolo',
      desc: 'Tuo fratello ha 4 anni. Vuoi insegnargli a usare il fischietto. Cosa gli dici?',
      choices: [
        { text: 'Soffia 3 volte solo se hai bisogno di aiuto', icon: '👨‍👦', correct: true },
        { text: 'Fischialo quando vuoi, è un giocattolo', icon: '🎮', correct: false },
        { text: 'Non glielo do, è troppo piccolo', icon: '🚫', correct: false }
      ],
      feedback: 'Bravo! Anche un bambino di 4 anni può imparare la regola "3 fischi = aiuto". Spiega quando usarlo (perso, paura, male) e che NON è un giocattolo.'
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
