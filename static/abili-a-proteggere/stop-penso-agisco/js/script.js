/* Stop, Penso, Agisco — Sequenza a 3 passi */
(function () {
  'use strict';

  // Ogni situazione ha 3 carte da ordinare: STOP, PENSO, AGISCO.
  // Le carte vengono mescolate; l'utente deve cliccarle nell'ordine 1-2-3.
  var situations = [
    {
      icon: '🌍',
      title: 'La terra trema',
      desc: 'Sei a casa e la terra inizia a tremare.',
      steps: [
        { order: 1, label: 'STOP', icon: '✋', text: 'Mi fermo e non corro fuori.' },
        { order: 2, label: 'PENSO', icon: '🧠', text: 'Cerco un tavolo o un muro robusto vicino.' },
        { order: 3, label: 'AGISCO', icon: '🛡️', text: 'Mi metto sotto il tavolo e mi proteggo la testa.' }
      ],
      feedback: 'Durante un terremoto: prima fermarsi (mai correre), poi guardare un riparo, poi proteggersi sotto il tavolo.'
    },
    {
      icon: '🔥',
      title: 'Vedo del fumo',
      desc: 'Esce del fumo dalla cucina di casa.',
      steps: [
        { order: 1, label: 'STOP', icon: '✋', text: 'Mi fermo e non apro la porta della cucina.' },
        { order: 2, label: 'PENSO', icon: '🧠', text: 'Cerco la via di fuga più lontana dal fumo.' },
        { order: 3, label: 'AGISCO', icon: '📞', text: 'Esco e chiamo il 112 da fuori.' }
      ],
      feedback: 'Davanti al fumo non si entra mai per "vedere": ci si ferma, si trova la via di fuga, si chiama il 112 da fuori.'
    },
    {
      icon: '⛈️',
      title: 'Temporale forte mentre cammino',
      desc: 'Cominciano lampi e tuoni mentre sei per strada.',
      steps: [
        { order: 1, label: 'STOP', icon: '✋', text: 'Mi fermo e non resto sotto un albero.' },
        { order: 2, label: 'PENSO', icon: '🧠', text: 'Guardo dov’è l’edificio più vicino.' },
        { order: 3, label: 'AGISCO', icon: '🏠', text: 'Entro nell’edificio e aspetto che passi.' }
      ],
      feedback: 'Sotto i fulmini: fermati, individua un edificio sicuro (mai alberi), entra e aspetta. Pochi minuti di attesa salvano la vita.'
    },
    {
      icon: '🤕',
      title: 'Cado per terra',
      desc: 'Inciampi e cadi. Hai un po’ di male a un ginocchio.',
      steps: [
        { order: 1, label: 'STOP', icon: '✋', text: 'Mi fermo e respiro lentamente.' },
        { order: 2, label: 'PENSO', icon: '🧠', text: 'Controllo se riesco a muovere la gamba.' },
        { order: 3, label: 'AGISCO', icon: '🆘', text: 'Chiamo o cerco un adulto per essere aiutato.' }
      ],
      feedback: 'Dopo una caduta non bisogna alzarsi di scatto: ci si calma, si controlla se ci si fa male, poi si chiede aiuto.'
    },
    {
      icon: '🚨',
      title: 'Suona l’allarme di evacuazione',
      desc: 'In un edificio pubblico inizia a suonare un allarme forte.',
      steps: [
        { order: 1, label: 'STOP', icon: '✋', text: 'Mi fermo e ascolto le indicazioni.' },
        { order: 2, label: 'PENSO', icon: '🧠', text: 'Cerco i cartelli verdi USCITA DI EMERGENZA.' },
        { order: 3, label: 'AGISCO', icon: '🚪', text: 'Esco con calma seguendo le frecce verdi.' }
      ],
      feedback: 'In evacuazione non si scappa mai: ci si ferma un attimo per ascoltare, si cercano i cartelli verdi, si esce con calma seguendoli.'
    }
  ];

  var currentIndex = 0;
  var score = 0;
  var pickedCount = 0;
  var roundActive = false;

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }
  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function resetSequenceUI() {
    [1, 2, 3].forEach(function (n) {
      document.getElementById('step-' + n).classList.remove('done');
    });
  }

  function loadSituation() {
    var s = situations[currentIndex];
    document.getElementById('sit-icon').textContent = s.icon;
    document.getElementById('sit-title').textContent = s.title;
    document.getElementById('sit-desc').textContent = s.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = situations.length;
    document.getElementById('score').textContent = score;
    hide(document.getElementById('feedback-box'));
    resetSequenceUI();
    pickedCount = 0;
    roundActive = true;

    var container = document.getElementById('cards-grid');
    container.innerHTML = '';
    var shuffled = shuffle(s.steps.slice());
    shuffled.forEach(function (step) {
      var btn = document.createElement('button');
      btn.className = 'seq-card';
      btn.dataset.order = step.order;
      btn.setAttribute('aria-label', step.label + ': ' + step.text);
      btn.innerHTML =
        '<span class="seq-card-icon" aria-hidden="true">' + step.icon + '</span>' +
        '<span><strong>' + step.label + '</strong><br><span style="font-weight:500;font-size:1rem;">' + step.text + '</span></span>';
      btn.addEventListener('click', function () { handlePick(btn, step, s); });
      container.appendChild(btn);
    });
  }

  function handlePick(btn, step, situation) {
    if (!roundActive) return;
    if (btn.disabled) return;
    pickedCount++;

    if (step.order === pickedCount) {
      btn.classList.add('correct');
      btn.disabled = true;
      var badge = document.createElement('span');
      badge.className = 'picked-badge';
      badge.textContent = pickedCount + '°';
      btn.appendChild(badge);
      document.getElementById('step-' + pickedCount).classList.add('done');

      if (pickedCount === 3) {
        roundActive = false;
        score++;
        document.getElementById('score').textContent = score;
        var fb = document.getElementById('feedback-box');
        fb.className = 'feedback-box feedback-correct';
        fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + situation.feedback;
        show(fb);
        scheduleNext();
      }
    } else {
      // Sbagliato: mostra feedback e ferma il round
      btn.classList.add('wrong');
      roundActive = false;
      document.querySelectorAll('.seq-card').forEach(function (b) { b.disabled = true; });
      var fb = document.getElementById('feedback-box');
      fb.className = 'feedback-box feedback-wrong';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>L\'ordine giusto è <strong>STOP → PENSO → AGISCO</strong>. ' + situation.feedback;
      show(fb);
      scheduleNext();
    }
  }

  function scheduleNext() {
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
    }, 4000);
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
