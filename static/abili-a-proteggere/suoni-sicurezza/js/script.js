/* Suoni della Sicurezza — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var situations = [
    {
      emoji: '🔔🏫',
      title: 'Suona l’allarme a scuola',
      desc: 'Senti un suono forte e continuo: è l’allarme della scuola!',
      actions: [
        { text: 'Mi metto in fila e esco con la maestra', icon: '🚶', correct: true },
        { text: 'Continuo a giocare', icon: '🎮', correct: false }
      ],
      feedback: 'Quando suona l’allarme, mettiti in fila e segui la maestra verso il punto di raccolta.'
    },
    {
      emoji: '🚒🔊',
      title: 'Sirena dei pompieri',
      desc: 'Senti la sirena dei vigili del fuoco che si avvicina.',
      actions: [
        { text: 'Mi fermo e lascio passare', icon: '✋', correct: true },
        { text: 'Corro in mezzo alla strada', icon: '🏃', correct: false }
      ],
      feedback: 'Quando senti la sirena, fermati e lascia passare il mezzo di soccorso. Non correre in strada!'
    },
    {
      emoji: '⚡🌧️',
      title: 'Tuono fortissimo',
      desc: 'Sei al parco e senti un tuono molto forte. Inizia a piovere.',
      actions: [
        { text: 'Entro subito in un edificio', icon: '🏠', correct: true },
        { text: 'Mi metto sotto un albero', icon: '🌳', correct: false }
      ],
      feedback: 'Entra in un edificio! Non metterti mai sotto un albero durante un temporale: attira i fulmini.'
    },
    {
      emoji: '📱🔔',
      title: 'Il telefono avvisa: allerta meteo',
      desc: 'Il telefono suona con un messaggio di allerta meteo arancione.',
      actions: [
        { text: 'Resto a casa e chiudo le finestre', icon: '🏠', correct: true },
        { text: 'Esco a fare una passeggiata', icon: '🚶', correct: false }
      ],
      feedback: 'Con l’allerta arancione è meglio restare a casa, chiudere le finestre e aspettare che passi.'
    },
    {
      emoji: '💨🏠',
      title: 'La casa trema',
      desc: 'Senti la casa che trema e gli oggetti si muovono. È un terremoto!',
      actions: [
        { text: 'Mi riparo sotto il tavolo', icon: '🪑', correct: true },
        { text: 'Corro verso l’ascensore', icon: '🛗', correct: false }
      ],
      feedback: 'Riparati sotto un tavolo robusto e proteggiti la testa. Non usare mai l’ascensore!'
    },
    {
      emoji: '🚨🔴',
      title: 'Suona l’allarme incendio',
      desc: 'Senti l’allarme incendio del palazzo. C’è un po’ di fumo.',
      actions: [
        { text: 'Esco dalle scale e chiamo il 112', icon: '📞', correct: true },
        { text: 'Apro tutte le porte per cercare il fuoco', icon: '🚪', correct: false }
      ],
      feedback: 'Esci subito dalle scale (mai dall’ascensore) e chiama il 112. Non aprire porte con fumo!'
    }
  ];

  var currentIndex = 0;
  var score = 0;

  var introScreen = document.getElementById('intro-screen');
  var gameScreen = document.getElementById('game-screen');
  var endScreen = document.getElementById('end-screen');

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }

  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function loadSituation() {
    var s = situations[currentIndex];
    document.getElementById('situation-emoji').textContent = s.emoji;
    document.getElementById('situation-title').textContent = s.title;
    document.getElementById('situation-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = situations.length;
    document.getElementById('score').textContent = score;

    var fb = document.getElementById('feedback-box');
    hide(fb);

    var container = document.getElementById('actions');
    container.innerHTML = '';
    var shuffled = shuffle(s.actions.slice());
    shuffled.forEach(function (a) {
      var btn = document.createElement('button');
      btn.className = 'action-btn';
      btn.innerHTML = '<span class="action-icon" aria-hidden="true">' + a.icon + '</span><span>' + a.text + '</span>';
      btn.addEventListener('click', function () { handleAction(btn, a, s); });
      container.appendChild(btn);
    });
  }

  function handleAction(btn, action, situation) {
    document.querySelectorAll('.action-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');

    if (action.correct) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box feedback-ok';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    } else {
      btn.classList.add('wrong');
      document.querySelectorAll('.action-btn').forEach(function (b) {
        var txt = b.querySelector('span:last-child').textContent;
        var correctText = situation.actions.filter(function (a) { return a.correct; })[0].text;
        if (txt === correctText) b.classList.add('correct');
      });
      fb.className = 'feedback-box feedback-no';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    }
    show(fb);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < situations.length) {
        loadSituation();
      } else {
        hide(gameScreen);
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = situations.length;
        show(endScreen);
      }
    }, 3500);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(introScreen);
    show(gameScreen);
    currentIndex = 0;
    score = 0;
    shuffle(situations);
    loadSituation();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(endScreen);
    show(introScreen);
  });
})();
