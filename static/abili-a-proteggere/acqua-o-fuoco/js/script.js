/* Acqua o Fuoco? — Distinguere comportamenti per alluvione e incendio */
(function () {
  'use strict';

  // correct: 'water' | 'fire' | 'both' | 'none'
  var actions = [
    {
      icon: '🪜',
      title: 'Salire ai piani alti',
      desc: 'Andare al piano di sopra del palazzo.',
      correct: 'water',
      feedback: 'In alluvione si sale: l’acqua arriva in basso. In incendio invece si esce: il fumo sale e i piani alti diventano una trappola.'
    },
    {
      icon: '🚪',
      title: 'Uscire piegato in basso',
      desc: 'Camminare piegato in avanti, vicino al pavimento.',
      correct: 'fire',
      feedback: 'In incendio il fumo sta in alto: ci si muove abbassati. In alluvione no: l’acqua è in basso, è un comportamento sbagliato.'
    },
    {
      icon: '📞',
      title: 'Chiamare il 112',
      desc: 'Chiamare il numero unico delle emergenze.',
      correct: 'both',
      feedback: 'Il 112 si chiama sempre, in entrambe le emergenze. È il primo numero da memorizzare.'
    },
    {
      icon: '🛗',
      title: 'Prendere l’ascensore',
      desc: 'Usare l’ascensore per scendere.',
      correct: 'none',
      feedback: 'Mai usare l’ascensore in un’emergenza! In incendio si può bloccare con dentro le persone, in alluvione si allaga. Sempre le scale.'
    },
    {
      icon: '🪟',
      title: 'Chiudere porte e finestre',
      desc: 'Chiudere bene tutte le porte e le finestre della stanza.',
      correct: 'fire',
      feedback: 'In incendio si chiudono porte e finestre per rallentare il fuoco. In alluvione invece la priorità è andare in alto, non chiudere tutto.'
    },
    {
      icon: '🥾',
      title: 'Non camminare nell’acqua alta',
      desc: 'Restare al riparo, non attraversare strade allagate.',
      correct: 'water',
      feedback: 'In alluvione l’acqua corrente è pericolosa: anche 30 cm bastano a trascinare via una persona. In incendio non c’entra: la regola è uscire.'
    },
    {
      icon: '🔌',
      title: 'Staccare la corrente di casa',
      desc: 'Spegnere il quadro elettrico generale, se ci si arriva in sicurezza.',
      correct: 'water',
      feedback: 'In alluvione la corrente è pericolosa con l’acqua: si stacca il quadro se si può farlo asciutti. In incendio si esce e basta: non si torna indietro.'
    }
  ];

  var labels = {
    water: { text: 'Solo se c’è acqua/alluvione', icon: '💧', cls: 'a-water' },
    fire:  { text: 'Solo se c’è fuoco/incendio',   icon: '🔥', cls: 'a-fire'  },
    both:  { text: 'Sempre, in entrambi',          icon: '✅', cls: 'a-both'  },
    none:  { text: 'Mai, è sbagliato',             icon: '🚫', cls: 'a-none'  }
  };

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

  function loadAction() {
    var a = actions[currentIndex];
    document.getElementById('action-icon').textContent = a.icon;
    document.getElementById('action-title').textContent = a.title;
    document.getElementById('action-desc').textContent = a.desc;
    document.getElementById('current-q').textContent = currentIndex + 1;
    document.getElementById('total-q').textContent = actions.length;
    document.getElementById('score').textContent = score;
    hide(document.getElementById('feedback-box'));

    var container = document.getElementById('answers');
    container.innerHTML = '';
    ['water', 'fire', 'both', 'none'].forEach(function (key) {
      var l = labels[key];
      var btn = document.createElement('button');
      btn.className = 'ans-btn ' + l.cls;
      btn.dataset.key = key;
      btn.innerHTML = '<span class="ans-icon" aria-hidden="true">' + l.icon + '</span><span>' + l.text + '</span>';
      btn.setAttribute('aria-label', l.text);
      btn.addEventListener('click', function () { handleAnswer(btn, key, a); });
      container.appendChild(btn);
    });
  }

  function handleAnswer(btn, key, action) {
    document.querySelectorAll('.ans-btn').forEach(function (b) { b.disabled = true; });
    var fb = document.getElementById('feedback-box');
    if (key === action.correct) {
      btn.classList.add('correct');
      score++;
      document.getElementById('score').textContent = score;
      fb.className = 'feedback-box feedback-correct';
      fb.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>' + action.feedback;
    } else {
      btn.classList.add('wrong');
      var corrBtn = document.querySelector('.ans-btn[data-key="' + action.correct + '"]');
      if (corrBtn) corrBtn.classList.add('correct');
      fb.className = 'feedback-box feedback-wrong';
      fb.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>' + action.feedback;
    }
    show(fb);

    setTimeout(function () {
      currentIndex++;
      if (currentIndex < actions.length) {
        loadAction();
      } else {
        hide(document.getElementById('game-screen'));
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = actions.length;
        show(document.getElementById('end-screen'));
      }
    }, 4000);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(document.getElementById('intro-screen'));
    show(document.getElementById('game-screen'));
    currentIndex = 0;
    score = 0;
    shuffle(actions);
    loadAction();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(document.getElementById('end-screen'));
    show(document.getElementById('intro-screen'));
  });
})();
