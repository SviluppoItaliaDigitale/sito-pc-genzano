/* I Miei Vicini — Chi chiamare per primo nelle situazioni di prossimità */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🔑',
      title: 'Mi sono chiuso fuori casa',
      desc: 'Sei rimasto fuori senza chiavi. Non sei in pericolo, ma ti serve aiuto.',
      choices: [
        { text: 'Il vicino di casa o il parente che ha le tue chiavi di scorta', icon: '🏠', correct: true },
        { text: 'Il 112', icon: '🚨', correct: false },
        { text: 'I vigili del fuoco', icon: '🚒', correct: false }
      ],
      feedback: 'Il 112 è solo per le emergenze gravi. Per la chiave smarrita basta un vicino o un parente: lascia sempre una chiave di scorta a qualcuno di fiducia.'
    },
    {
      icon: '💡',
      title: 'È andata via la luce in tutto il palazzo',
      desc: 'Sei al buio. Anche le luci della scala sono spente.',
      choices: [
        { text: 'Il custode o l’amministratore del palazzo', icon: '🏢', correct: true },
        { text: 'Il 112', icon: '🚨', correct: false },
        { text: 'Un parente lontano', icon: '👵', correct: false }
      ],
      feedback: 'Per i guasti del palazzo si chiama il custode o l’amministratore. Il 112 si usa solo se c’è un’emergenza vera (incendio, infortunio).'
    },
    {
      icon: '🤕',
      title: 'Sono caduto e mi sono fatto male alla gamba',
      desc: 'Sei a terra, ti fa molto male muovere la gamba. Hai il telefono in mano.',
      choices: [
        { text: 'Il 112', icon: '🚨', correct: true },
        { text: 'Il vicino di casa', icon: '🏠', correct: false },
        { text: 'L’amministratore', icon: '🏢', correct: false }
      ],
      feedback: 'Una caduta con dolore forte è un’emergenza sanitaria: si chiama il 112. Mentre aspetti, se puoi avvisa anche un vicino così ti raggiunge subito.'
    },
    {
      icon: '🛒',
      title: 'Sono solo e non ho fatto la spesa',
      desc: 'È sera, sei a casa solo, non hai cena e fa brutto tempo.',
      choices: [
        { text: 'Un vicino, un parente o un amico vicino', icon: '👋', correct: true },
        { text: 'Il 112', icon: '🚨', correct: false },
        { text: 'La protezione civile', icon: '🦺', correct: false }
      ],
      feedback: 'Una spesa mancata non è un’emergenza. Chiedi aiuto a chi ti vive vicino: per questo è importante conoscere i propri vicini.'
    },
    {
      icon: '👴',
      title: 'Il mio vicino anziano non risponde da due giorni',
      desc: 'Il vicino di casa anziano non apre la porta e non risponde al telefono.',
      choices: [
        { text: 'Provo prima i suoi parenti, poi il 112 se non si trovano', icon: '📞', correct: true },
        { text: 'Aspetto un altro giorno', icon: '⏳', correct: false },
        { text: 'Sfondo la porta', icon: '🔨', correct: false }
      ],
      feedback: 'Si prova prima a contattare i suoi familiari. Se non si raggiungono e c’è preoccupazione concreta, si chiama il 112: gli operatori sanno cosa fare.'
    },
    {
      icon: '🛑',
      title: 'Una persona sconosciuta insiste per entrare',
      desc: 'Suonano alla porta e una persona che non conosci insiste per entrare. Sei solo.',
      choices: [
        { text: 'Non apro e chiamo il 112', icon: '🚨', correct: true },
        { text: 'Apro per vedere chi è', icon: '🚪', correct: false },
        { text: 'Aspetto che se ne vada', icon: '⏳', correct: false }
      ],
      feedback: 'Se uno sconosciuto insiste e tu sei solo, non aprire mai. Chiama il 112: è una situazione di sicurezza personale, non da sottovalutare.'
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
