/* Vestiti Giusti — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var outfits = {
    impermeabile: { emoji: '\uD83E\uDDE5\uD83C\uDF27\uFE0F', label: 'Impermeabile e stivali' },
    tshirt:       { emoji: '\uD83D\uDC55',                  label: 'Maglietta e pantaloncini' },
    piumino:      { emoji: '\uD83E\uDDE5\u2744\uFE0F',       label: 'Piumino e cappello' },
    antifumo:     { emoji: '\uD83E\uDDE3',                  label: 'Straccio bagnato sulla bocca' },
    scarpeChiuse: { emoji: '\uD83D\uDC5F',                  label: 'Scarpe chiuse e robuste' },
    ciabatte:     { emoji: '\uD83E\uDE74',                  label: 'Ciabatte aperte' },
    gialloFluo:   { emoji: '\uD83E\uDD7C',                  label: 'Pettorina gialla riflettente' },
    cappello:     { emoji: '\uD83E\uDDE2',                  label: 'Cappello e crema solare' }
  };

  var situations = [
    {
      emoji: '\uD83C\uDF27\uFE0F',
      title: 'Piove forte',
      desc: 'Oggi piove molto e devi uscire per andare a scuola.',
      correct: 'impermeabile',
      wrong: 'tshirt',
      feedback: 'Impermeabile e stivali. Ti proteggono dalla pioggia e non ti bagnano i piedi. Sarai asciutto e al caldo.'
    },
    {
      emoji: '\u2744\uFE0F',
      title: 'C\u2019è la neve',
      desc: 'Fa molto freddo, c\u2019è neve per terra.',
      correct: 'piumino',
      wrong: 'tshirt',
      feedback: 'Piumino e cappello. Il freddo ti può far male: copri bene anche la testa e le mani.'
    },
    {
      emoji: '\uD83D\uDD25',
      title: 'Fumo in casa',
      desc: 'C\u2019è fumo e devi attraversare il corridoio per uscire.',
      correct: 'antifumo',
      wrong: 'cappello',
      feedback: 'Straccio bagnato sulla bocca. Filtra il fumo e ti aiuta a respirare meglio. Stai basso e cammina verso l\u2019uscita.'
    },
    {
      emoji: '\uD83C\uDF2A\uFE0F',
      title: 'Terremoto, esco da scuola',
      desc: 'Dopo una scossa devi uscire e camminare sulle macerie piccole.',
      correct: 'scarpeChiuse',
      wrong: 'ciabatte',
      feedback: 'Scarpe chiuse e robuste. Ti proteggono dai vetri rotti e dai pezzi di intonaco. Meglio sempre con i lacci legati.'
    },
    {
      emoji: '\uD83C\uDF1E',
      title: 'Sole molto forte',
      desc: 'In estate, all\u2019aperto, il sole è forte e fa caldo.',
      correct: 'cappello',
      wrong: 'piumino',
      feedback: 'Cappello e crema solare. Ti proteggono dal colpo di sole. Bevi spesso acqua.'
    },
    {
      emoji: '\uD83C\uDF19',
      title: 'Esercitazione al buio',
      desc: 'Il volontario ti chiede di partecipare a una prova serale vicino alla strada.',
      correct: 'gialloFluo',
      wrong: 'tshirt',
      feedback: 'Pettorina gialla riflettente. Così le macchine ti vedono da lontano e sei più sicuro.'
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

  function loadSituation() {
    var s = situations[currentIndex];
    document.getElementById('sit-emoji').textContent = s.emoji;
    document.getElementById('sit-title').textContent = s.title;
    document.getElementById('sit-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = situations.length;
    document.getElementById('score').textContent = score;

    hide(document.getElementById('feedback-box'));

    var container = document.getElementById('outfits');
    container.innerHTML = '';

    var options = shuffle([
      { key: s.correct, isCorrect: true },
      { key: s.wrong, isCorrect: false }
    ]);

    options.forEach(function (opt) {
      var data = outfits[opt.key];
      var btn = document.createElement('button');
      btn.className = 'outfit-btn';
      btn.innerHTML =
        '<span class="outfit-emoji" aria-hidden="true">' + data.emoji + '</span>' +
        '<span class="outfit-label">' + data.label + '</span>';
      btn.setAttribute('aria-label', data.label);
      btn.addEventListener('click', function () { handleChoice(btn, opt.isCorrect, s); });
      container.appendChild(btn);
    });
  }

  function handleChoice(btn, isCorrect, situation) {
    document.querySelectorAll('.outfit-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');

    if (isCorrect) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box fb-ok';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    } else {
      btn.classList.add('wrong');
      document.querySelectorAll('.outfit-btn').forEach(function (b) {
        if (!b.classList.contains('wrong')) b.classList.add('correct');
      });
      fb.className = 'feedback-box fb-no';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    }
    show(fb);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < situations.length) {
        loadSituation();
      } else {
        hide(document.getElementById('game-screen'));
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = situations.length;
        show(document.getElementById('end-screen'));
      }
    }, 3500);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(document.getElementById('intro-screen'));
    show(document.getElementById('game-screen'));
    currentIndex = 0;
    score = 0;
    shuffle(situations);
    loadSituation();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(document.getElementById('end-screen'));
    show(document.getElementById('intro-screen'));
  });
})();
