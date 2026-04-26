/* Il Mio Posto Sicuro — Punto sicuro durante un terremoto, stanza per stanza */
(function () {
  'use strict';

  var scenarios = [
    {
      icon: '🛏️',
      title: 'Camera da letto',
      desc: 'Sei in camera tua. Trema la terra. Dove ti metti?',
      choices: [
        { text: 'Sotto la scrivania o un tavolino robusto', icon: '🪑', correct: true },
        { text: 'Sopra il letto, fermo', icon: '🛏️', correct: false },
        { text: 'Vicino allo specchio', icon: '🪞', correct: false }
      ],
      feedback: 'Sotto un mobile robusto sei protetto da quello che può cadere dall’alto. Specchi e finestre sono pericolosi: possono rompersi.'
    },
    {
      icon: '🍳',
      title: 'Cucina',
      desc: 'Sei in cucina. Trema la terra. Dove ti metti?',
      choices: [
        { text: 'Mi allontano dai pensili e mi metto vicino al muro portante', icon: '🧱', correct: true },
        { text: 'Resto vicino al frigorifero', icon: '🥶', correct: false },
        { text: 'Mi metto sotto i pensili dei piatti', icon: '🍽️', correct: false }
      ],
      feedback: 'In cucina cadono piatti, pentole e pensili. Allontanati subito da loro e cerca un muro portante (gli angoli sono i più solidi).'
    },
    {
      icon: '🛋️',
      title: 'Soggiorno',
      desc: 'Sei in salotto. Trema la terra. Dove ti metti?',
      choices: [
        { text: 'Sotto il tavolo da pranzo, ben coperto', icon: '🪑', correct: true },
        { text: 'Sul divano, davanti alla TV', icon: '📺', correct: false },
        { text: 'Vicino alla libreria piena di libri', icon: '📚', correct: false }
      ],
      feedback: 'Il tavolo solido protegge dalla caduta di oggetti. Le librerie alte e la TV possono ribaltarsi: stanne lontano.'
    },
    {
      icon: '🚿',
      title: 'Bagno',
      desc: 'Sei in bagno. Trema la terra. Dove ti metti?',
      choices: [
        { text: 'Vicino alla porta, lontano dallo specchio e dal vetro della doccia', icon: '🚪', correct: true },
        { text: 'Dentro la vasca da bagno', icon: '🛁', correct: false },
        { text: 'Davanti allo specchio', icon: '🪞', correct: false }
      ],
      feedback: 'In bagno gli specchi e il vetro della doccia sono pericolosi. La porta del bagno è in genere solida e vicina al muro portante.'
    },
    {
      icon: '🪜',
      title: 'Scale del palazzo',
      desc: 'Stai salendo le scale del tuo palazzo. Trema la terra. Cosa fai?',
      choices: [
        { text: 'Mi fermo dove sono e mi appoggio al muro interno', icon: '🧱', correct: true },
        { text: 'Salgo di corsa al mio piano', icon: '🏃', correct: false },
        { text: 'Scendo di corsa in strada', icon: '🏃', correct: false }
      ],
      feedback: 'Sulle scale non si corre mai durante una scossa: si rischia di cadere. Ci si ferma e ci si appoggia al muro interno.'
    },
    {
      icon: '🌳',
      title: 'In giardino o in cortile',
      desc: 'Sei fuori, in cortile, e trema la terra. Dove vai?',
      choices: [
        { text: 'In mezzo al cortile, lontano da muri e alberi', icon: '🌍', correct: true },
        { text: 'Vicino al muro del palazzo', icon: '🧱', correct: false },
        { text: 'Sotto un albero grande', icon: '🌳', correct: false }
      ],
      feedback: 'All’aperto il punto sicuro è uno spazio aperto, lontano da muri (possono cadere calcinacci) e alberi (possono spezzarsi rami).'
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
    }, 3500);
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
