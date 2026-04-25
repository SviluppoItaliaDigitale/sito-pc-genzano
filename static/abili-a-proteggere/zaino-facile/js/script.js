/* Zaino Facile — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var correctItems = [
    { emoji: '💧', name: 'Acqua', tip: 'L’acqua è la cosa più importante!' },
    { emoji: '🔦', name: 'Torcia', tip: 'La torcia serve se manca la luce.' },
    { emoji: '🧥', name: 'Coperta', tip: 'La coperta ti tiene al caldo.' },
    { emoji: '💊', name: 'Medicinali', tip: 'I medicinali sono importanti per chi li prende.' },
    { emoji: '📱', name: 'Telefono', tip: 'Il telefono serve per chiamare il 112.' },
    { emoji: '🍞', name: 'Cibo', tip: 'Un po’ di cibo che non si rovina.' }
  ];

  var wrongItems = [
    { emoji: '🎮', name: 'Videogiochi', tip: 'I videogiochi non servono in emergenza.' },
    { emoji: '⚽', name: 'Pallone', tip: 'Il pallone non serve nello zaino di emergenza.' }
  ];

  var found = 0;
  var errors = 0;

  var introScreen = document.getElementById('intro-screen');
  var gameScreen = document.getElementById('game-screen');
  var endScreen = document.getElementById('end-screen');
  var itemsGrid = document.getElementById('items-grid');
  var zainoItems = document.getElementById('zaino-items');
  var itemsCount = document.getElementById('items-count');
  var itemsTotal = document.getElementById('items-total');
  var errorsCount = document.getElementById('errors-count');
  var feedbackToast = document.getElementById('feedback-toast');

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }

  function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  var toastTimer;
  function showToast(msg, ok) {
    clearTimeout(toastTimer);
    feedbackToast.textContent = msg;
    feedbackToast.className = 'feedback-toast ' + (ok ? 'toast-ok' : 'toast-no');
    show(feedbackToast);
    toastTimer = setTimeout(function () { hide(feedbackToast); }, 2000);
  }

  function buildGrid() {
    itemsGrid.innerHTML = '';
    zainoItems.innerHTML = '';
    found = 0;
    errors = 0;
    itemsCount.textContent = '0';
    itemsTotal.textContent = correctItems.length;
    errorsCount.textContent = '0';

    var all = shuffle(correctItems.concat(wrongItems).slice());
    all.forEach(function (item) {
      var btn = document.createElement('button');
      btn.className = 'item-btn';
      btn.innerHTML = '<span class="item-emoji" aria-hidden="true">' + item.emoji + '</span><span>' + item.name + '</span>';
      var isCorrect = correctItems.some(function (c) { return c.name === item.name; });
      btn.addEventListener('click', function () {
        if (btn.disabled) return;
        if (isCorrect) {
          btn.classList.add('item-correct');
          btn.disabled = true;
          found++;
          itemsCount.textContent = found;
          showToast(item.tip, true);
          // Add to zaino
          var badge = document.createElement('span');
          badge.className = 'zaino-item-badge';
          badge.textContent = item.emoji;
          badge.setAttribute('aria-label', item.name);
          zainoItems.appendChild(badge);
          if (found >= correctItems.length) {
            setTimeout(showEnd, 1200);
          }
        } else {
          btn.classList.add('item-wrong');
          errors++;
          errorsCount.textContent = errors;
          showToast(item.tip, false);
          setTimeout(function () { btn.classList.remove('item-wrong'); }, 600);
        }
      });
      itemsGrid.appendChild(btn);
    });
  }

  function showEnd() {
    hide(gameScreen);
    var msg = errors === 0
      ? 'Perfetto! Nessun errore. Sei preparatissimo!'
      : 'Hai fatto ' + errors + (errors === 1 ? ' errore' : ' errori') + ', ma hai completato lo zaino. Bravo!';
    document.getElementById('end-message').textContent = msg;
    show(endScreen);
  }

  document.getElementById('start-btn').addEventListener('click', function () {
    hide(introScreen);
    show(gameScreen);
    buildGrid();
  });

  document.getElementById('restart-btn').addEventListener('click', function () {
    hide(endScreen);
    show(introScreen);
  });
})();
