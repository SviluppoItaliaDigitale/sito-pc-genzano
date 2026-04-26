/* Giorno e Notte — Cosa cambia in emergenza al buio */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🌃',
      title: 'È andata via la corrente, è notte',
      desc: 'Sei a casa, è notte. Si spegne la luce in tutto il palazzo.',
      choices: [
        { text: 'Accendo la torcia che tengo vicino al letto', icon: '🔦', correct: true },
        { text: 'Accendo l’accendino o un fiammifero', icon: '🔥', correct: false },
        { text: 'Mi sposto di corsa in altra stanza', icon: '🏃', correct: false }
      ],
      feedback: 'La torcia è la prima cosa: tienila sempre vicino al letto. Mai usare fiamme libere al buio (rischio incendio se c’è una fuga di gas).'
    },
    {
      icon: '🚪',
      title: 'Devo uscire al buio dalla mia camera',
      desc: 'Devi raggiungere la porta di casa. Non vedi niente perché è buio.',
      choices: [
        { text: 'Mi muovo piano, con una mano sul muro come guida', icon: '🧱', correct: true },
        { text: 'Cammino veloce a memoria', icon: '🏃', correct: false },
        { text: 'Resto fermo sul letto', icon: '🛏️', correct: false }
      ],
      feedback: 'Al buio si va piano, una mano sul muro come guida. Camminare a memoria fa cadere su mobili o oggetti spostati.'
    },
    {
      icon: '📱',
      title: 'Il telefono ha solo il 10% di batteria',
      desc: 'Sei al buio. Devi chiamare aiuto ma il telefono ha poca batteria.',
      choices: [
        { text: 'Chiamo subito il 112 prima che si spenga', icon: '🚨', correct: true },
        { text: 'Uso prima la torcia del telefono', icon: '🔦', correct: false },
        { text: 'Aspetto di vedere se la corrente torna', icon: '⏳', correct: false }
      ],
      feedback: 'La priorità è la chiamata al 112. La torcia consuma molta batteria: meglio una torcia vera o aspettare al chiaro.'
    },
    {
      icon: '🔑',
      title: 'Devo trovare le chiavi al buio',
      desc: 'Devi uscire ma le chiavi sono "da qualche parte" nell’ingresso.',
      choices: [
        { text: 'Le chiavi stanno sempre nello stesso posto, le trovo subito', icon: '🪝', correct: true },
        { text: 'Frugo a caso ovunque', icon: '🔍', correct: false },
        { text: 'Sfondo la porta', icon: '🔨', correct: false }
      ],
      feedback: 'Avere un posto fisso per le chiavi (ganci all’ingresso, ciotola fissa) è la soluzione: al buio le trovi anche con gli occhi chiusi.'
    },
    {
      icon: '😨',
      title: 'Sento un rumore strano al buio',
      desc: 'Senti un rumore che non capisci. Sei a letto, è notte.',
      choices: [
        { text: 'Resto calmo, ascolto, accendo la torcia', icon: '👂', correct: true },
        { text: 'Urlo subito', icon: '😱', correct: false },
        { text: 'Salto giù dal letto al buio', icon: '🦘', correct: false }
      ],
      feedback: 'Calma, ascolto, luce: nove volte su dieci il rumore ha una spiegazione semplice. Saltare al buio fa cadere; urlare spaventa altri inutilmente.'
    },
    {
      icon: '🏠',
      title: 'Devo aspettare i soccorsi a casa, di notte',
      desc: 'Hai chiamato il 112. Devi aspettare che arrivino. È notte.',
      choices: [
        { text: 'Accendo una luce visibile dalla strada e apro la porta del palazzo', icon: '💡', correct: true },
        { text: 'Spengo tutte le luci', icon: '🌑', correct: false },
        { text: 'Esco in strada al buio', icon: '🚶', correct: false }
      ],
      feedback: 'Una luce accesa aiuta i soccorsi a trovarti subito. Aprire il portone del palazzo (se sei al sicuro) accorcia ancora i tempi.'
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
