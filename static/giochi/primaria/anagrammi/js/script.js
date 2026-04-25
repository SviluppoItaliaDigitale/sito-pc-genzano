/* Anagrammi della Sicurezza — Protezione Civile Genzano
   Randomizzazione: ad ogni partita cambia sia la selezione delle parole
   sia l'ordine delle lettere nel pool. */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Parole divise per difficoltà ───────────────────────────────
  // facile = 4-6 lettere · medio = 7-9 · difficile = 10+
  const wordBank = {
    facile: [
      { w: 'ZAINO',       cat: 'Oggetto dello zaino di emergenza',       hint: 'Lo porti in spalla quando scappi' },
      { w: 'ACQUA',       cat: 'Scorta fondamentale in emergenza',        hint: 'Serve per bere e lavarsi' },
      { w: 'CASCO',       cat: 'Dispositivo di protezione',               hint: 'Protegge la testa del volontario' },
      { w: 'RADIO',       cat: 'Strumento di comunicazione',              hint: 'Trasmette e riceve messaggi' },
      { w: 'FRANA',       cat: 'Rischio del territorio',                  hint: 'Terreno che scivola a valle' },
      { w: 'FUOCO',       cat: 'Elemento pericoloso',                     hint: 'Brucia e scotta' },
      { w: 'PIOGGIA',     cat: 'Fenomeno meteo',                          hint: 'Cade dal cielo' },
      { w: 'NEVE',        cat: 'Fenomeno meteo',                          hint: 'Bianca e fredda' },
      { w: 'VENTO',       cat: 'Fenomeno meteo',                          hint: 'Muove le foglie' },
      { w: 'AIUTO',       cat: 'Richiesta di soccorso',                   hint: 'Lo chiedi in caso di pericolo' },
      { w: 'SCOSSA',      cat: 'Terremoto',                               hint: 'Movimento improvviso del terreno' },
      { w: 'TORCIA',      cat: 'Oggetto dello zaino di emergenza',        hint: 'Fa luce al buio' },
      { w: 'FISCHIO',     cat: 'Strumento di segnalazione',               hint: 'Suono acuto per farsi sentire' },
      { w: 'ALLERTA',     cat: 'Livello di avviso',                       hint: 'Avviso di un possibile pericolo' },
      { w: 'NUMERI',      cat: 'Emergenza',                               hint: 'Quelli da chiamare sono utili' },
      { w: 'ELMETTO',     cat: 'Dispositivo di protezione',               hint: 'Copre la testa in cantiere o in zona crollo' },
      { w: 'USCITA',      cat: 'Via di fuga',                             hint: 'Dove si va quando suona l’allarme' },
      { w: 'GUANTI',      cat: 'Protezione personale',                    hint: 'Proteggono le mani dei volontari' },
      { w: 'MAPPA',       cat: 'Strumento di orientamento',               hint: 'Disegno del territorio per non perdersi' },
      { w: 'BUSSOLA',     cat: 'Strumento di orientamento',               hint: 'Indica sempre il nord' },
      { w: 'BATTERIA',    cat: 'Oggetto dello zaino di emergenza',        hint: 'Serve a far funzionare radio e torcia' },
      { w: 'CORDA',       cat: 'Attrezzatura di soccorso',                hint: 'Si usa per legare e calarsi' },
      { w: 'COPERTA',     cat: 'Oggetto dello zaino',                     hint: 'Tiene caldo se fa freddo fuori' },
      { w: 'VERDE',       cat: 'Colore allerta',                          hint: 'Nessun rischio previsto' },
      { w: 'ROSSO',       cat: 'Colore allerta',                          hint: 'Massima attenzione, rischio elevato' }
    ],
    medio: [
      { w: 'VOLONTARIO',     cat: 'Protezione Civile',                    hint: 'Offre tempo e aiuto gratis' },
      { w: 'EMERGENZA',      cat: 'Situazione urgente',                   hint: 'Richiede interventi rapidi' },
      { w: 'TERREMOTO',      cat: 'Rischio del territorio',               hint: 'La terra trema' },
      { w: 'INCENDIO',       cat: 'Rischio del territorio',               hint: 'Fuoco fuori controllo' },
      { w: 'ALLUVIONE',      cat: 'Rischio del territorio',               hint: 'Acqua che invade le strade' },
      { w: 'SICUREZZA',      cat: 'Obiettivo primario',                   hint: 'Stare lontani dai pericoli' },
      { w: 'ESERCITAZIONE',  cat: 'Formazione',                           hint: 'Prova di una situazione reale' },
      { w: 'PREVENZIONE',    cat: 'Protezione Civile',                    hint: 'Evitare il pericolo prima' },
      { w: 'BOLLETTINO',     cat: 'Comunicazione',                        hint: 'Previsioni e avvisi ufficiali' },
      { w: 'SEGNALE',        cat: 'Comunicazione',                        hint: 'Serve ad avvisare' },
      { w: 'RIFUGIO',        cat: 'Luogo sicuro',                         hint: 'Posto dove ripararsi' },
      { w: 'MASCHERINA',     cat: 'Protezione personale',                 hint: 'Copre naso e bocca' },
      { w: 'IDRANTE',        cat: 'Strumento dei pompieri',               hint: 'Da qui esce l’acqua' },
      { w: 'SOCCORSO',       cat: 'Aiuto in emergenza',                   hint: 'Chi corre ad aiutare' },
      { w: 'ESTINTORE',      cat: 'Strumento antincendio',                hint: 'Serve per spegnere piccole fiamme' },
      { w: 'ASCENSORE',      cat: 'Da evitare in emergenza',              hint: 'Non si usa mai durante un terremoto' },
      { w: 'PUNTO DI RACCOLTA', cat: 'Luogo di sicurezza',                hint: 'Dove ci si ritrova dopo l’evacuazione' },
      { w: 'CAPOFILA',       cat: 'Ruolo in evacuazione',                 hint: 'Guida la fila della classe' },
      { w: 'FOGLIO NOTE',    cat: 'Oggetto dello zaino',                  hint: 'Per scrivere informazioni o messaggi' },
      { w: 'DOCUMENTI',      cat: 'Cosa portare in evacuazione',          hint: 'Carta d’identità e tessera sanitaria' },
      { w: 'VIGILANZA',      cat: 'Attività di controllo',           hint: 'Osservare per prevenire pericoli' },
      { w: 'PRESIDIO',       cat: 'Postazione operativa',                 hint: 'Posto dove si presta servizio' },
      { w: 'CENTRALE',       cat: 'Coordinamento',                        hint: 'Da qui si dirigono gli interventi' },
      { w: 'BINOCOLO',       cat: 'Strumento di osservazione',            hint: 'Serve a vedere lontano' }
    ],
    difficile: [
      { w: 'EVACUAZIONE',         cat: 'Azione di emergenza',             hint: 'Tutti fuori in fila e con calma' },
      { w: 'AUTOPROTEZIONE',      cat: 'Comportamento',                   hint: 'Imparare a difendersi da soli' },
      { w: 'IDROGEOLOGICO',       cat: 'Tipo di rischio',                 hint: 'Acqua + terreno che frana' },
      { w: 'COMUNICAZIONE',       cat: 'Scambio di informazioni',         hint: 'Serve per avvisare tutti' },
      { w: 'TEMPORALE',           cat: 'Fenomeno meteo intenso',          hint: 'Tuoni, fulmini e pioggia' },
      { w: 'BOSCHIVO',            cat: 'Rischio stagionale',              hint: 'Incendio che colpisce i boschi' },
      { w: 'ANTINCENDIO',         cat: 'Prevenzione',                     hint: 'Attività contro le fiamme' },
      { w: 'COORDINAMENTO',       cat: 'Organizzazione',                  hint: 'Lavorare insieme senza confusione' },
      { w: 'RADIOCOMUNICAZIONE',  cat: 'Strumento dei volontari',         hint: 'Messaggi via radio tra squadre' },
      { w: 'SORVEGLIANZA',        cat: 'Attività di controllo',           hint: 'Tenere d’occhio una zona' },
      { w: 'ESONDAZIONE',         cat: 'Rischio del territorio',          hint: 'Il fiume esce dal letto' },
      { w: 'AUTOPROTEZIONE',      cat: 'Comportamento',                   hint: 'Difendere se stessi con i gesti giusti' },
      { w: 'PROTEZIONECIVILE',    cat: 'Sistema nazionale',               hint: 'Tutti gli enti che si occupano di emergenze' },
      { w: 'VOLONTARIATO',        cat: 'Donare tempo',                    hint: 'Aiuto gratuito alla comunità' },
      { w: 'AUTOMEZZO',           cat: 'Mezzo operativo',                 hint: 'Veicolo dei volontari' },
      { w: 'PIANOFAMILIARE',      cat: 'Preparazione domestica',          hint: 'Cosa fa ciascuno in caso di emergenza' },
      { w: 'COMUNICAZIONE',       cat: 'Scambio informazioni',            hint: 'Avvisare e coordinare via radio' },
      { w: 'CARTOGRAFIA',         cat: 'Scienza delle mappe',             hint: 'Disegno scientifico del territorio' },
      { w: 'SICUREZZASCOLASTICA', cat: 'Piano d’emergenza',          hint: 'Regole per evacuare le scuole' },
      { w: 'SISMOGRAFO',          cat: 'Strumento scientifico',           hint: 'Registra i movimenti della terra' },
      { w: 'METEOROLOGIA',        cat: 'Scienza del tempo',               hint: 'Studia e prevede il tempo atmosferico' }
    ]
  };

  // ─── Stato ─────────────────────────────────────────────────────
  let selectedLevel = 'facile';
  let selectedCount = 5;
  let roundWords = [];        // parole di questa partita
  let currentIndex = 0;
  let score = 0;
  let hintsLeft = 3;
  let answerSequence = [];    // storia delle lettere inserite (per undo)
  let currentWord = '';       // parola target (con spazi conservati)
  let solvedThisWord = false;

  // ─── Elementi DOM ──────────────────────────────────────────────
  const startScreen   = document.getElementById('start-screen');
  const gameScreen    = document.getElementById('game-screen');
  const resultsScreen = document.getElementById('results-screen');
  const startBtn      = document.getElementById('start-btn');
  const restartBtn    = document.getElementById('restart-btn');
  const currentWSpan  = document.getElementById('current-w');
  const totalWSpan    = document.getElementById('total-w');
  const scoreLive     = document.getElementById('score-live');
  const progressFill  = document.getElementById('progress-fill');
  const hintText      = document.getElementById('hint-text');
  const categoryText  = document.getElementById('category-text');
  const answerSlots   = document.getElementById('answer-slots');
  const letterPool    = document.getElementById('letter-pool');
  const feedbackBox   = document.getElementById('feedback-box');
  const undoBtn       = document.getElementById('undo-btn');
  const resetBtn      = document.getElementById('reset-btn');
  const hintBtn       = document.getElementById('hint-btn');
  const hintsLeftSpan = document.getElementById('hints-left');
  const nextBtn       = document.getElementById('next-btn');
  const scoreSpan     = document.getElementById('score');
  const maxScoreSpan  = document.getElementById('max-score');
  const feedbackMsg   = document.getElementById('feedback-message');

  // ─── Helpers ───────────────────────────────────────────────────
  const shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  const pickWords = (level, count) => {
    const bank = wordBank[level] || wordBank.facile;
    const shuffled = shuffle(bank);
    return shuffled.slice(0, Math.min(count, shuffled.length));
  };

  // Mescola le lettere assicurandosi che NON siano nell'ordine originale
  const shuffleLetters = (word) => {
    const letters = word.replace(/\s+/g, '').split('');
    if (letters.length < 2) return letters;
    let out;
    let attempts = 0;
    do {
      out = shuffle(letters);
      attempts++;
    } while (out.join('') === letters.join('') && attempts < 20);
    return out;
  };

  // ─── Selettori difficoltà e conteggio ──────────────────────────
  document.querySelectorAll('.difficulty-selector .btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.difficulty-selector .btn').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-checked', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-checked', 'true');
      selectedLevel = btn.dataset.level;
    });
  });
  document.querySelectorAll('.count-selector .btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.count-selector .btn').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-checked', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-checked', 'true');
      selectedCount = parseInt(btn.dataset.count, 10);
    });
  });

  // ─── Avvio / riavvio ───────────────────────────────────────────
  const startGame = () => {
    roundWords = pickWords(selectedLevel, selectedCount);
    currentIndex = 0;
    score = 0;
    hintsLeft = 3;
    hintsLeftSpan.textContent = hintsLeft;
    totalWSpan.textContent = roundWords.length;
    startScreen.classList.add('hide');
    resultsScreen.classList.add('hide');
    gameScreen.classList.remove('hide');
    loadWord();
  };

  const loadWord = () => {
    solvedThisWord = false;
    answerSequence = [];
    feedbackBox.classList.add('hide');
    feedbackBox.classList.remove('correct', 'wrong');
    feedbackBox.textContent = '';
    nextBtn.classList.add('hide');

    const entry = roundWords[currentIndex];
    currentWord = entry.w.toUpperCase();
    categoryText.textContent = entry.cat;
    hintText.textContent = 'Suggerimento: ' + entry.hint;

    currentWSpan.textContent = currentIndex + 1;
    scoreLive.textContent = 'Punti: ' + score;
    progressFill.style.width = ((currentIndex) / roundWords.length * 100) + '%';

    buildSlots();
    buildPool();
  };

  const buildSlots = () => {
    answerSlots.innerHTML = '';
    for (const ch of currentWord) {
      const slot = document.createElement('div');
      if (ch === ' ') {
        slot.className = 'slot space';
        slot.setAttribute('aria-hidden', 'true');
      } else {
        slot.className = 'slot';
        slot.setAttribute('role', 'button');
        slot.setAttribute('tabindex', '-1');
        slot.setAttribute('aria-label', 'Casella vuota');
        slot.addEventListener('click', () => {
          // permette di rimuovere la lettera cliccando lo slot pieno
          if (slot.classList.contains('filled') && !solvedThisWord) {
            const idx = [...answerSlots.children].filter(c => !c.classList.contains('space')).indexOf(slot);
            removeLetterAt(idx);
          }
        });
      }
      answerSlots.appendChild(slot);
    }
  };

  const buildPool = () => {
    letterPool.innerHTML = '';
    const letters = shuffleLetters(currentWord);
    letters.forEach((letter, i) => {
      const tile = document.createElement('button');
      tile.type = 'button';
      tile.className = 'letter-tile';
      tile.textContent = letter;
      tile.dataset.index = i;
      tile.setAttribute('aria-label', 'Lettera ' + letter);
      tile.addEventListener('click', () => placeLetter(tile));
      letterPool.appendChild(tile);
    });
  };

  // Inserisci la lettera nel primo slot disponibile
  const placeLetter = (tile) => {
    if (solvedThisWord) return;
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    const target = slots.find(s => !s.classList.contains('filled'));
    if (!target) return;
    const letter = tile.textContent;
    target.textContent = letter;
    target.classList.add('filled');
    target.setAttribute('aria-label', 'Lettera ' + letter);
    tile.classList.add('used');
    tile.disabled = true;
    answerSequence.push({ tileIndex: tile.dataset.index, slot: target });
    checkComplete();
  };

  const removeLetterAt = (letterIndexInSlots) => {
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    const slot = slots[letterIndexInSlots];
    if (!slot || !slot.classList.contains('filled')) return;
    // trova l'entry più recente che corrisponde a questo slot
    const entryIdx = [...answerSequence].reverse().findIndex(e => e.slot === slot);
    if (entryIdx === -1) return;
    const realIdx = answerSequence.length - 1 - entryIdx;
    const entry = answerSequence.splice(realIdx, 1)[0];
    slot.textContent = '';
    slot.classList.remove('filled', 'correct', 'wrong');
    slot.setAttribute('aria-label', 'Casella vuota');
    const tile = letterPool.querySelector(`.letter-tile[data-index="${entry.tileIndex}"]`);
    if (tile) { tile.classList.remove('used'); tile.disabled = false; }
  };

  const undoLast = () => {
    if (!answerSequence.length || solvedThisWord) return;
    const entry = answerSequence.pop();
    entry.slot.textContent = '';
    entry.slot.classList.remove('filled', 'correct', 'wrong');
    entry.slot.setAttribute('aria-label', 'Casella vuota');
    const tile = letterPool.querySelector(`.letter-tile[data-index="${entry.tileIndex}"]`);
    if (tile) { tile.classList.remove('used'); tile.disabled = false; }
  };

  const resetWord = () => {
    if (solvedThisWord) return;
    answerSequence = [];
    [...answerSlots.children].forEach(s => {
      if (!s.classList.contains('space')) {
        s.textContent = '';
        s.classList.remove('filled', 'correct', 'wrong');
        s.setAttribute('aria-label', 'Casella vuota');
      }
    });
    [...letterPool.children].forEach(t => {
      t.classList.remove('used');
      t.disabled = false;
    });
    feedbackBox.classList.add('hide');
  };

  // Aiuto: riempie la prossima casella con la lettera giusta
  const useHint = () => {
    if (hintsLeft <= 0 || solvedThisWord) return;
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    const wordLetters = currentWord.replace(/\s+/g, '').split('');
    // trova il primo slot vuoto
    const firstEmptyIdx = slots.findIndex(s => !s.classList.contains('filled'));
    if (firstEmptyIdx === -1) return;
    const neededLetter = wordLetters[firstEmptyIdx];
    // se lo slot successivo è errato (già pieno) lo svuotiamo (non dovrebbe succedere qui)
    // trova una tile non usata con quella lettera
    const tile = [...letterPool.children].find(t => !t.classList.contains('used') && t.textContent === neededLetter);
    if (!tile) return;
    hintsLeft -= 1;
    hintsLeftSpan.textContent = hintsLeft;
    placeLetter(tile);
  };

  const checkComplete = () => {
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    if (slots.every(s => s.classList.contains('filled'))) {
      const built = slots.map(s => s.textContent).join('');
      const target = currentWord.replace(/\s+/g, '');
      if (built === target) {
        solvedThisWord = true;
        slots.forEach(s => s.classList.add('correct'));
        const pointsBase = currentWord.replace(/\s+/g, '').length * 10;
        const hintPenalty = (3 - hintsLeft) * 5;
        const earned = Math.max(pointsBase - hintPenalty, 10);
        score += earned;
        scoreLive.textContent = 'Punti: ' + score;
        feedbackBox.classList.remove('hide', 'wrong');
        feedbackBox.classList.add('correct');
        feedbackBox.innerHTML = `<i class="bi bi-check-circle-fill" aria-hidden="true"></i> Bravissimo! +${earned} punti`;
        nextBtn.classList.remove('hide');
        nextBtn.focus();
      } else {
        slots.forEach(s => s.classList.add('wrong'));
        feedbackBox.classList.remove('hide', 'correct');
        feedbackBox.classList.add('wrong');
        feedbackBox.innerHTML = '<i class="bi bi-x-circle-fill" aria-hidden="true"></i> Non è corretto. Riprova!';
        // sblocca le tile per farle riposizionare
        setTimeout(() => {
          resetWord();
        }, 900);
      }
    }
  };

  const nextWord = () => {
    currentIndex += 1;
    if (currentIndex >= roundWords.length) {
      showResults();
    } else {
      loadWord();
    }
  };

  const showResults = () => {
    gameScreen.classList.add('hide');
    resultsScreen.classList.remove('hide');
    // punteggio massimo = somma (lunghezza * 10) senza penalità
    const max = roundWords.reduce((s, e) => s + e.w.replace(/\s+/g, '').length * 10, 0);
    scoreSpan.textContent = score;
    maxScoreSpan.textContent = max;
    const perc = max > 0 ? (score / max) : 0;
    let msg;
    if (perc >= 0.9)      msg = 'Perfetto! Sei pronto a unirti ai volontari!';
    else if (perc >= 0.7) msg = 'Ottimo lavoro! Conosci bene le parole della sicurezza.';
    else if (perc >= 0.5) msg = 'Bene! Continua a esercitarti per migliorare.';
    else                  msg = 'Non mollare! Ogni partita è un passo avanti.';
    feedbackMsg.textContent = msg;
    if (window.GiochiUtil) window.GiochiUtil.salvaEMostraAttestato('anagrammi', score, max, '#results-screen');
  };

  // ─── Listener ──────────────────────────────────────────────────
  startBtn.addEventListener('click', startGame);
  restartBtn.addEventListener('click', () => {
    resultsScreen.classList.add('hide');
    startScreen.classList.remove('hide');
  });
  undoBtn.addEventListener('click', undoLast);
  resetBtn.addEventListener('click', resetWord);
  hintBtn.addEventListener('click', useHint);
  nextBtn.addEventListener('click', nextWord);

  // Tastiera: lettere fisiche digitate inseriscono la prima tile disponibile
  document.addEventListener('keydown', (e) => {
    if (gameScreen.classList.contains('hide') || solvedThisWord) return;
    if (e.key === 'Backspace') { e.preventDefault(); undoLast(); return; }
    if (e.key === 'Enter' && !nextBtn.classList.contains('hide')) { e.preventDefault(); nextWord(); return; }
    const key = (e.key || '').toUpperCase();
    if (!/^[A-Z]$/.test(key)) return;
    const tile = [...letterPool.children].find(t => !t.classList.contains('used') && t.textContent === key);
    if (tile) { e.preventDefault(); placeLetter(tile); }
  });

});
