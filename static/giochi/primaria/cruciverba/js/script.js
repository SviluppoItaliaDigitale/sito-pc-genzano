/* Cruciverba della Sicurezza — logica di gioco */
(function () {
  'use strict';

  var PUZZLES = window.CRUCIVERBA_PUZZLES || { facile: [], medio: [], difficile: [] };

  var startScreen = document.getElementById('start-screen');
  var gameScreen = document.getElementById('game-screen');
  var resultsScreen = document.getElementById('results-screen');
  var difficultyBtns = document.querySelectorAll('.difficulty-selector .btn');
  var startBtn = document.getElementById('start-btn');
  var gridEl = document.getElementById('grid');
  var cluesAcross = document.getElementById('clues-across');
  var cluesDown = document.getElementById('clues-down');
  var currentClue = document.getElementById('current-clue');
  var solvedSpan = document.getElementById('cw-solved');
  var totalSpan = document.getElementById('cw-total');
  var hintsSpan = document.getElementById('cw-hints');
  var checkBtn = document.getElementById('check-btn');
  var hintBtn = document.getElementById('hint-btn');
  var resetBtn = document.getElementById('reset-btn');
  var newGridBtn = document.getElementById('new-grid-btn');
  var feedbackBox = document.getElementById('feedback-box');
  var restartBtn = document.getElementById('restart-btn');
  var finalSolved = document.getElementById('final-solved');
  var finalHints = document.getElementById('final-hints');
  var feedbackMessage = document.getElementById('feedback-message');

  var difficulty = 'facile';
  var puzzle = null;
  var cellMap = {};
  var solvedCount = 0;
  var hintsLeft = 3;
  var activeWord = null;

  difficultyBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      difficultyBtns.forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-checked', 'false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-checked', 'true');
      difficulty = btn.dataset.level;
    });
  });

  startBtn.addEventListener('click', function () {
    startScreen.classList.add('hide');
    gameScreen.classList.remove('hide');
    loadPuzzle();
  });

  restartBtn.addEventListener('click', function () {
    resultsScreen.classList.add('hide');
    startScreen.classList.remove('hide');
  });

  newGridBtn.addEventListener('click', function () {
    loadPuzzle();
  });

  resetBtn.addEventListener('click', function () {
    if (!puzzle) return;
    Object.keys(cellMap).forEach(function (k) {
      var inp = cellMap[k].input;
      if (inp) {
        inp.value = '';
        cellMap[k].el.classList.remove('correct', 'wrong');
      }
    });
    puzzle.words.forEach(function (w) { w.solved = false; });
    solvedCount = 0;
    updateStats();
    refreshCluesList();
  });

  checkBtn.addEventListener('click', verifyAll);
  hintBtn.addEventListener('click', useHint);

  function pickPuzzle() {
    var pool = PUZZLES[difficulty] || [];
    if (!pool.length) return null;
    return JSON.parse(JSON.stringify(pool[Math.floor(Math.random() * pool.length)]));
  }

  function loadPuzzle() {
    puzzle = pickPuzzle();
    if (!puzzle) return;
    hintsLeft = 3;
    solvedCount = 0;
    hintsSpan.textContent = hintsLeft;
    feedbackBox.classList.add('hide');
    totalSpan.textContent = puzzle.words.length;
    solvedSpan.textContent = 0;
    buildGrid();
    buildClues();
    currentClue.textContent = 'Seleziona una casella per vedere la definizione.';
  }

  function buildGrid() {
    cellMap = {};
    gridEl.innerHTML = '';
    gridEl.style.gridTemplateColumns = 'repeat(' + puzzle.cols + ', 40px)';
    var usedCells = {};

    puzzle.words.forEach(function (w) {
      w.solved = false;
      var len = w.answer.length;
      for (var i = 0; i < len; i++) {
        var r = w.row + (w.dir === 'D' ? i : 0);
        var c = w.col + (w.dir === 'A' ? i : 0);
        var key = r + ',' + c;
        if (!usedCells[key]) {
          usedCells[key] = { letter: w.answer.charAt(i), words: [] };
        }
        usedCells[key].words.push({ word: w, pos: i });
      }
    });

    for (var r = 0; r < puzzle.rows; r++) {
      for (var c = 0; c < puzzle.cols; c++) {
        var cell = document.createElement('div');
        cell.className = 'cell';
        var key = r + ',' + c;
        if (!usedCells[key]) {
          cell.classList.add('black');
          gridEl.appendChild(cell);
          continue;
        }
        var numWord = puzzle.words.find(function (w) { return w.row === r && w.col === c; });
        if (numWord) {
          var numEl = document.createElement('span');
          numEl.className = 'cell-number';
          numEl.textContent = numWord.n;
          cell.appendChild(numEl);
        }
        var input = document.createElement('input');
        input.type = 'text';
        input.maxLength = 1;
        input.autocomplete = 'off';
        input.setAttribute('aria-label', 'Riga ' + (r + 1) + ' colonna ' + (c + 1));
        input.dataset.row = r;
        input.dataset.col = c;
        input.addEventListener('focus', function (e) { onFocusCell(+e.target.dataset.row, +e.target.dataset.col); });
        input.addEventListener('input', function (e) { onInputCell(e); });
        input.addEventListener('keydown', function (e) { onKeyDown(e); });
        cell.appendChild(input);
        cellMap[key] = { el: cell, input: input, letter: usedCells[key].letter, words: usedCells[key].words };
        gridEl.appendChild(cell);
      }
    }
  }

  function buildClues() {
    cluesAcross.innerHTML = '';
    cluesDown.innerHTML = '';
    puzzle.words.forEach(function (w) {
      var li = document.createElement('li');
      li.innerHTML = '<span class="num">' + w.n + '.</span> ' + w.clue;
      li.dataset.wordKey = w.n + '-' + w.dir;
      li.tabIndex = 0;
      li.addEventListener('click', function () { focusWord(w); });
      li.addEventListener('keydown', function (e) { if (e.key === 'Enter') focusWord(w); });
      if (w.dir === 'A') cluesAcross.appendChild(li); else cluesDown.appendChild(li);
    });
    refreshCluesList();
  }

  function refreshCluesList() {
    puzzle.words.forEach(function (w) {
      var li = document.querySelector('[data-word-key="' + w.n + '-' + w.dir + '"]');
      if (!li) return;
      li.classList.toggle('solved', !!w.solved);
      li.classList.toggle('active', activeWord && activeWord.n === w.n && activeWord.dir === w.dir);
    });
  }

  function focusWord(w) {
    activeWord = w;
    var key = w.row + ',' + w.col;
    var c = cellMap[key];
    if (c && c.input) c.input.focus();
    highlightActiveWord();
    currentClue.textContent = w.n + (w.dir === 'A' ? ' orizzontale' : ' verticale') + ': ' + w.clue;
    refreshCluesList();
  }

  function highlightActiveWord() {
    Object.keys(cellMap).forEach(function (k) { cellMap[k].el.classList.remove('highlight'); });
    if (!activeWord) return;
    var len = activeWord.answer.length;
    for (var i = 0; i < len; i++) {
      var r = activeWord.row + (activeWord.dir === 'D' ? i : 0);
      var c = activeWord.col + (activeWord.dir === 'A' ? i : 0);
      var cell = cellMap[r + ',' + c];
      if (cell) cell.el.classList.add('highlight');
    }
  }

  function onFocusCell(r, c) {
    var cell = cellMap[r + ',' + c];
    if (!cell) return;
    if (cell.words.length > 0) {
      var pref = cell.words.find(function (ww) { return ww.word.dir === 'A'; }) || cell.words[0];
      activeWord = pref.word;
      currentClue.textContent = activeWord.n + (activeWord.dir === 'A' ? ' orizzontale' : ' verticale') + ': ' + activeWord.clue;
      highlightActiveWord();
      refreshCluesList();
    }
  }

  function onInputCell(e) {
    var v = e.target.value.toUpperCase().replace(/[^A-ZÀÁÈÉÌÍÒÓÙÚ]/g, '');
    e.target.value = v.slice(-1);
    var r = +e.target.dataset.row;
    var c = +e.target.dataset.col;
    var cellObj = cellMap[r + ',' + c];
    cellObj.el.classList.remove('correct', 'wrong');
    if (e.target.value && activeWord) {
      moveInWord(1);
      maybeCheckWord(activeWord);
    }
  }

  function onKeyDown(e) {
    var r = +e.target.dataset.row;
    var c = +e.target.dataset.col;
    if (e.key === 'Backspace' && !e.target.value) {
      e.preventDefault();
      moveInWord(-1);
    } else if (e.key === 'ArrowRight') { e.preventDefault(); moveTo(r, c + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); moveTo(r, c - 1); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); moveTo(r + 1, c); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); moveTo(r - 1, c); }
  }

  function moveTo(r, c) {
    var cell = cellMap[r + ',' + c];
    if (cell && cell.input) cell.input.focus();
  }

  function moveInWord(delta) {
    if (!activeWord) return;
    var input = document.activeElement;
    if (!input || input.tagName !== 'INPUT') return;
    var r = +input.dataset.row;
    var c = +input.dataset.col;
    var dr = activeWord.dir === 'D' ? delta : 0;
    var dc = activeWord.dir === 'A' ? delta : 0;
    moveTo(r + dr, c + dc);
  }

  function maybeCheckWord(w) {
    var ans = '';
    for (var i = 0; i < w.answer.length; i++) {
      var r = w.row + (w.dir === 'D' ? i : 0);
      var c = w.col + (w.dir === 'A' ? i : 0);
      var cell = cellMap[r + ',' + c];
      ans += (cell && cell.input && cell.input.value) ? cell.input.value.toUpperCase() : ' ';
    }
    if (ans === w.answer) {
      w.solved = true;
      for (var j = 0; j < w.answer.length; j++) {
        var rr = w.row + (w.dir === 'D' ? j : 0);
        var cc = w.col + (w.dir === 'A' ? j : 0);
        var c2 = cellMap[rr + ',' + cc];
        if (c2) c2.el.classList.add('correct');
      }
      recountSolved();
      refreshCluesList();
      // Feedback con spiegazione didattica (quando presente nel puzzle):
      // permette di fissare la nozione invece di limitarsi a "Bravo!".
      var msg = '<strong>' + w.answer + '</strong> completata!';
      if (w.explain) msg += '<br><small>' + w.explain + '</small>';
      showFeedback(msg, true);
      if (solvedCount === puzzle.words.length) finishPuzzle();
    }
  }

  function verifyAll() {
    var wrong = 0;
    puzzle.words.forEach(function (w) {
      var ans = '';
      for (var i = 0; i < w.answer.length; i++) {
        var r = w.row + (w.dir === 'D' ? i : 0);
        var c = w.col + (w.dir === 'A' ? i : 0);
        var cell = cellMap[r + ',' + c];
        ans += (cell && cell.input && cell.input.value) ? cell.input.value.toUpperCase() : ' ';
      }
      if (ans === w.answer) {
        w.solved = true;
        for (var j = 0; j < w.answer.length; j++) {
          var rr = w.row + (w.dir === 'D' ? j : 0);
          var cc = w.col + (w.dir === 'A' ? j : 0);
          var c2 = cellMap[rr + ',' + cc];
          if (c2) c2.el.classList.add('correct');
        }
      } else if (ans.replace(/ /g, '').length > 0) {
        for (var k = 0; k < w.answer.length; k++) {
          var rr2 = w.row + (w.dir === 'D' ? k : 0);
          var cc2 = w.col + (w.dir === 'A' ? k : 0);
          var c3 = cellMap[rr2 + ',' + cc2];
          var letter = (c3 && c3.input && c3.input.value) ? c3.input.value.toUpperCase() : '';
          if (c3 && !c3.el.classList.contains('correct') && letter && letter !== w.answer.charAt(k)) {
            c3.el.classList.add('wrong');
            wrong++;
          }
        }
      }
    });
    recountSolved();
    refreshCluesList();
    if (wrong > 0) showFeedback('Ci sono ' + wrong + ' lettere da correggere (evidenziate in rosso).', false);
    else if (solvedCount === puzzle.words.length) finishPuzzle();
    else showFeedback('Nessun errore finora. Continua!', true);
  }

  function useHint() {
    if (hintsLeft <= 0) {
      showFeedback('Hai finito gli aiuti.', false);
      return;
    }
    var target = activeWord && !activeWord.solved ? activeWord : puzzle.words.find(function (w) { return !w.solved; });
    if (!target) return;
    var filled = null;
    for (var i = 0; i < target.answer.length; i++) {
      var r = target.row + (target.dir === 'D' ? i : 0);
      var c = target.col + (target.dir === 'A' ? i : 0);
      var cell = cellMap[r + ',' + c];
      if (cell && cell.input && !cell.input.value) {
        cell.input.value = target.answer.charAt(i);
        filled = { r: r, c: c };
        break;
      }
    }
    if (!filled) return;
    hintsLeft--;
    hintsSpan.textContent = hintsLeft;
    maybeCheckWord(target);
    showFeedback('Aiuto usato. Aiuti rimasti: ' + hintsLeft + '.', true);
  }

  function recountSolved() {
    solvedCount = puzzle.words.filter(function (w) { return w.solved; }).length;
    solvedSpan.textContent = solvedCount;
  }

  function updateStats() {
    solvedSpan.textContent = solvedCount;
    hintsSpan.textContent = hintsLeft;
  }

  function showFeedback(msg, ok) {
    feedbackBox.className = 'cw-feedback ' + (ok ? 'correct' : 'wrong');
    feedbackBox.innerHTML = '<i class="bi ' + (ok ? 'bi-check-circle-fill' : 'bi-exclamation-circle-fill') + ' me-1"></i>' + msg;
    feedbackBox.classList.remove('hide');
  }

  function finishPuzzle() {
    gameScreen.classList.add('hide');
    resultsScreen.classList.remove('hide');
    finalSolved.textContent = solvedCount;
    finalHints.textContent = 3 - hintsLeft;
    var msg;
    if (hintsLeft === 3) msg = 'Perfetto! Hai risolto tutto senza nessun aiuto.';
    else if (hintsLeft >= 1) msg = 'Molto bene! Hai usato solo ' + (3 - hintsLeft) + ' aiuti.';
    else msg = 'Ottimo! Hai completato lo schema.';
    feedbackMessage.textContent = msg;
    var punti = Math.max(solvedCount * 10 - (3 - hintsLeft) * 5, solvedCount);
    var max = puzzle.words.length * 10;
    if (window.GiochiUtil) window.GiochiUtil.salvaEMostraAttestato('cruciverba', punti, max, '#results-screen');
  }
})();
