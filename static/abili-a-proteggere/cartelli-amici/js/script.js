/* Cartelli Amici — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var signs = {
    exit:    { icon: 'bi-door-open-fill',        label: 'Uscita di sicurezza', cls: 'si-exit' },
    fire:    { icon: 'bi-fire',                  label: 'Attenzione: fuoco',    cls: 'si-fire' },
    danger:  { icon: 'bi-exclamation-lg',        label: 'Attenzione: pericolo', cls: 'si-danger' },
    ban:     { icon: 'bi-slash-circle-fill',     label: 'Divieto',              cls: 'si-ban' },
    info:    { icon: 'bi-info-lg',               label: 'Informazione',         cls: 'si-info' },
    first:   { icon: 'bi-bandaid-fill',          label: 'Pronto soccorso',      cls: 'si-first' },
    water:   { icon: 'bi-droplet-fill',          label: 'Acqua potabile',       cls: 'si-water' },
    meeting: { icon: 'bi-people-fill',           label: 'Punto di raccolta',    cls: 'si-meeting' }
  };

  var situations = [
    {
      emoji: '\uD83D\uDD25',
      title: 'C\u2019è fumo in corridoio',
      desc: 'Devi scappare dalla scuola. Quale cartello cerchi sul muro?',
      correct: 'exit',
      wrong: 'info',
      feedback: 'Il cartello verde con l\u2019uomo che corre indica la via di fuga. Seguilo per uscire in sicurezza.'
    },
    {
      emoji: '\uD83D\uDD29',
      title: 'Mi sono fatto un taglio',
      desc: 'Mi serve un cerotto o una medicazione. Quale cartello cerco?',
      correct: 'first',
      wrong: 'ban',
      feedback: 'Il cartello verde con la croce indica il pronto soccorso. Lì trovi i cerotti e chi ti cura.'
    },
    {
      emoji: '\uD83D\uDEB7',
      title: 'Qui non si passa',
      desc: 'Vicino a un lavoro in corso c\u2019è un cartello. Quale indica che è vietato entrare?',
      correct: 'ban',
      wrong: 'info',
      feedback: 'Il cerchio rosso con la barra è il segnale di divieto. Rispetta il divieto e cerca un\u2019altra strada.'
    },
    {
      emoji: '\uD83D\uDD14',
      title: 'Allarme: bisogna uscire',
      desc: 'Dopo aver lasciato l\u2019edificio, dove mi fermo con gli altri?',
      correct: 'meeting',
      wrong: 'danger',
      feedback: 'Il cartello verde con le persone indica il punto di raccolta. Aspetta lì l\u2019appello.'
    },
    {
      emoji: '\u26A0\uFE0F',
      title: 'Attenzione davanti a me',
      desc: 'Un cartello giallo con il punto esclamativo mi avvisa di qualcosa. Cosa significa?',
      correct: 'danger',
      wrong: 'info',
      feedback: 'Il triangolo giallo-arancione con il punto esclamativo dice: attento, c\u2019è un pericolo. Guarda bene prima di andare avanti.'
    },
    {
      emoji: '\uD83D\uDCA7',
      title: 'Ho sete',
      desc: 'Durante una prova di evacuazione voglio bere. Quale cartello mi guida a una fontanella sicura?',
      correct: 'water',
      wrong: 'fire',
      feedback: 'Il cartello azzurro con la goccia indica l\u2019acqua potabile. L\u2019acqua è sicura da bere.'
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

    var container = document.getElementById('signs');
    container.innerHTML = '';

    var options = shuffle([
      { key: s.correct, isCorrect: true },
      { key: s.wrong, isCorrect: false }
    ]);

    options.forEach(function (opt) {
      var data = signs[opt.key];
      var btn = document.createElement('button');
      btn.className = 'sign-btn';
      btn.innerHTML =
        '<span class="sign-icon ' + data.cls + '"><i class="bi ' + data.icon + '" aria-hidden="true"></i></span>' +
        '<span class="sign-label">' + data.label + '</span>';
      btn.setAttribute('aria-label', 'Cartello ' + data.label);
      btn.addEventListener('click', function () { handleChoice(btn, opt.isCorrect, s); });
      container.appendChild(btn);
    });
  }

  function handleChoice(btn, isCorrect, situation) {
    document.querySelectorAll('.sign-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');

    if (isCorrect) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box fb-ok';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
    } else {
      btn.classList.add('wrong');
      document.querySelectorAll('.sign-btn').forEach(function (b) {
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
