/* Memoria della Sicurezza — Memory accessibile a 12 carte (6 coppie) */
(function () {
  'use strict';

  // Ogni coppia ha lo stesso pairId. Una carta è "oggetto", l'altra è "situazione".
  var pairs = [
    {
      pairId: 'estintore',
      hint: 'L’estintore serve a spegnere un piccolo incendio.',
      a: { emoji: '🧯', label: 'Estintore' },
      b: { emoji: '🔥', label: 'Piccolo incendio' }
    },
    {
      pairId: 'torcia',
      hint: 'La torcia serve quando manca la luce.',
      a: { emoji: '🔦', label: 'Torcia' },
      b: { emoji: '🌑', label: 'Buio' }
    },
    {
      pairId: 'acqua',
      hint: 'L’acqua serve quando si ha sete o per lavare una ferita.',
      a: { emoji: '💧', label: 'Bottiglia d’acqua' },
      b: { emoji: '😓', label: 'Ho sete' }
    },
    {
      pairId: 'cerotto',
      hint: 'Il cerotto serve quando ti sei fatto un piccolo taglio.',
      a: { emoji: '🩹', label: 'Cerotto' },
      b: { emoji: '🤕', label: 'Piccola ferita' }
    },
    {
      pairId: 'telefono',
      hint: 'Il telefono serve per chiamare il 112 in emergenza.',
      a: { emoji: '📞', label: 'Telefono' },
      b: { emoji: '🆘', label: 'Chiamare il 112' }
    },
    {
      pairId: 'coperta',
      hint: 'La coperta serve a coprirsi se fa freddo o per proteggersi.',
      a: { emoji: '🛏️', label: 'Coperta' },
      b: { emoji: '🥶', label: 'Ho freddo' }
    }
  ];

  var deck = [];
  var first = null;
  var second = null;
  var lockBoard = false;
  var pairsFound = 0;

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }
  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  function buildDeck() {
    deck = [];
    pairs.forEach(function (p) {
      deck.push({ pairId: p.pairId, side: 'a', emoji: p.a.emoji, label: p.a.label, hint: p.hint });
      deck.push({ pairId: p.pairId, side: 'b', emoji: p.b.emoji, label: p.b.label, hint: p.hint });
    });
    shuffle(deck);
  }

  function render() {
    var grid = document.getElementById('memory-grid');
    grid.innerHTML = '';
    deck.forEach(function (card, idx) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mem-card';
      btn.dataset.idx = idx;
      btn.dataset.pair = card.pairId;
      btn.setAttribute('role', 'gridcell');
      btn.setAttribute('aria-label', 'Carta ' + (idx + 1) + ', coperta');
      btn.innerHTML =
        '<span class="face-back" aria-hidden="true"></span>' +
        '<span class="face-front" aria-hidden="true">' +
          '<span class="mem-emoji">' + card.emoji + '</span>' +
          '<span class="mem-label">' + card.label + '</span>' +
        '</span>';
      btn.addEventListener('click', function () { handleFlip(btn, card); });
      grid.appendChild(btn);
    });

    document.getElementById('pairs-found').textContent = pairsFound;
    document.getElementById('pairs-total').textContent = pairs.length;
    hide(document.getElementById('last-match'));
  }

  function handleFlip(btn, card) {
    if (lockBoard) return;
    if (btn.classList.contains('flipped') || btn.classList.contains('matched')) return;

    btn.classList.add('flipped');
    btn.setAttribute('aria-label', card.label + ', scoperta');

    if (!first) {
      first = { btn: btn, card: card };
      return;
    }
    second = { btn: btn, card: card };
    lockBoard = true;

    if (first.card.pairId === second.card.pairId && first.card.side !== second.card.side) {
      // Match
      first.btn.classList.add('matched');
      second.btn.classList.add('matched');
      pairsFound++;
      document.getElementById('pairs-found').textContent = pairsFound;

      var lm = document.getElementById('last-match');
      lm.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i>Coppia trovata: ' + first.card.hint;
      show(lm);

      first = null;
      second = null;
      lockBoard = false;

      if (pairsFound === pairs.length) {
        setTimeout(function () {
          hide(document.getElementById('game-screen'));
          show(document.getElementById('end-screen'));
        }, 1200);
      }
    } else {
      // Mismatch: mostra brevemente e copri di nuovo
      first.btn.classList.add('wrong');
      second.btn.classList.add('wrong');
      setTimeout(function () {
        first.btn.classList.remove('flipped', 'wrong');
        second.btn.classList.remove('flipped', 'wrong');
        first.btn.setAttribute('aria-label', 'Carta coperta');
        second.btn.setAttribute('aria-label', 'Carta coperta');
        first = null;
        second = null;
        lockBoard = false;
      }, 1500);
    }
  }

  function startGame() {
    pairsFound = 0;
    first = null;
    second = null;
    lockBoard = false;
    buildDeck();
    render();
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(document.getElementById('intro-screen'));
    show(document.getElementById('game-screen'));
    startGame();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(document.getElementById('end-screen'));
    show(document.getElementById('intro-screen'));
  });

  document.getElementById('restart-mid').addEventListener('click', function () {
    startGame();
  });
})();
