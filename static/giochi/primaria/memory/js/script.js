// Memory dei Segnali — gioco rifatto maggio 2026.
// Le carte non si abbinano per identita ma per significato: un pittogramma ISO 7010
// (segnale di sicurezza standard) si abbina al comportamento corretto. Tre livelli
// (4/6/8 coppie) estratti random da un pool di 12. Dopo ogni match, breve spiegazione
// del segnale per fissare la nozione (rules 03 — apprendimento, non solo decorativo).

document.addEventListener('DOMContentLoaded', () => {
  const introScreen = document.getElementById('intro-screen');
  const gameScreen = document.getElementById('game-screen');
  const winScreen = document.getElementById('win-screen');
  const grid = document.querySelector('.memory-grid');
  const movesCountSpan = document.getElementById('moves-count');
  const pairsCountSpan = document.getElementById('pairs-count');
  const pairsTotalSpan = document.getElementById('pairs-total');
  const livelloSpan = document.getElementById('livello-corrente');
  const restartButton = document.getElementById('restart-button');
  const resetLevelBtn = document.getElementById('reset-level-btn');
  const explainBox = document.getElementById('explain-box');
  const explainTitle = document.getElementById('explain-title');
  const explainBody = document.getElementById('explain-body');
  const winStats = document.getElementById('win-stats');

  const POOL = [
    { id: 'estintore', sign: 'estintore', name: 'Estintore', action: 'Spegne le fiamme piccole',
      explain: 'L\'estintore è il segnale antincendio rosso. Solo gli adulti lo usano per fiamme appena nate. Tu chiama un adulto e il 112.' },
    { id: 'telefono', sign: 'telefono-emergenza', name: 'Telefono di emergenza', action: 'Chiama il 112',
      explain: 'In Italia il numero unico delle emergenze è 112. Una chiamata, smistano a vigili del fuoco, ambulanza o forze dell\'ordine.' },
    { id: 'uscita', sign: 'uscita-emergenza-destra', name: 'Uscita di emergenza', action: 'Esci di qua se c\'è allarme',
      explain: 'I cartelli verdi indicano le uscite di sicurezza. Segui sempre le frecce, mai tornare indietro a prendere lo zaino.' },
    { id: 'punto-raccolta', sign: 'punto-raccolta', name: 'Punto di raccolta', action: 'Mi fermo qui in fila',
      explain: 'Dopo l\'evacuazione tutti si ritrovano qui. Resta in fila con l\'insegnante: serve per sapere chi è uscito.' },
    { id: 'scala', sign: 'scala-antincendio', name: 'Scala antincendio', action: 'Mai ascensore se c\'è allarme',
      explain: 'Durante un\'evacuazione (incendio, terremoto, allarme) MAI l\'ascensore: usa sempre le scale.' },
    { id: 'primo-soccorso', sign: 'cassetta-primo-soccorso', name: 'Cassetta di primo soccorso', action: 'Bende e medicazioni',
      explain: 'La cassetta verde con la croce bianca contiene cerotti, bende e disinfettante per le piccole ferite.' },
    { id: 'dae', sign: 'defibrillatore-dae', name: 'Defibrillatore (DAE)', action: 'Aiuta chi ha un malore al cuore',
      explain: 'Il DAE riavvia il cuore quando smette di battere. Lo usano gli adulti formati: tu chiama subito il 112.' },
    { id: 'elettrico', sign: 'pericolo-elettrico', name: 'Pericolo elettrico', action: 'Non toccare i fili',
      explain: 'Il triangolo giallo col fulmine avvisa di alta tensione. Mai toccare cavi scoperti o pali della luce.' },
    { id: 'infiammabile', sign: 'materiale-infiammabile', name: 'Materiale infiammabile', action: 'Lontano da fiamme',
      explain: 'Liquidi che prendono fuoco facilmente: benzina, alcol, vernici. Mai accendere fiamme vicino.' },
    { id: 'massi', sign: 'caduta-massi', name: 'Caduta massi', action: 'Attento alle frane',
      explain: 'Nei sentieri di montagna e lungo i versanti questo segnale avvisa che possono cadere sassi: non fermarti sotto.' },
    { id: 'fuochi', sign: 'vietato-fuochi', name: 'Vietato accendere fuochi', action: 'Niente fiamme nel bosco',
      explain: 'D\'estate è vietato accendere fuochi nei boschi: bastano poche scintille per un grande incendio.' },
    { id: 'acqua', sign: 'acqua-potabile', name: 'Acqua potabile', action: 'Si può bere senza paura',
      explain: 'Il rubinetto con simbolo verde dice che l\'acqua è sicura da bere. Senza simbolo, chiedi prima a un adulto.' }
  ];

  const LIVELLI = {
    facile: { coppie: 4, label: 'Facile', cols: 4 },
    medio:  { coppie: 6, label: 'Medio',  cols: 4 },
    esperto:{ coppie: 8, label: 'Esperto',cols: 4 }
  };

  // Stato corrente
  let livelloCorrente = 'facile';
  let coppieScelte = [];
  let moves = 0;
  let matchedPairs = 0;
  let hasFlipped = false;
  let lockBoard = false;
  let firstCard = null, secondCard = null;

  function shuffle(array){
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  function avviaLivello(livello){
    livelloCorrente = livello;
    const cfg = LIVELLI[livello];
    livelloSpan.textContent = cfg.label;
    pairsTotalSpan.textContent = cfg.coppie;
    coppieScelte = shuffle([...POOL]).slice(0, cfg.coppie);
    introScreen.classList.add('hide');
    winScreen.classList.add('hide');
    gameScreen.classList.remove('hide');
    creaGriglia();
  }

  function creaGriglia(){
    grid.innerHTML = '';
    matchedPairs = 0;
    moves = 0;
    movesCountSpan.textContent = '0';
    pairsCountSpan.textContent = '0';
    explainBox.classList.add('hide');

    grid.style.setProperty('--mappa-cols', LIVELLI[livelloCorrente].cols);

    // Crea due tipi di carte per ogni coppia: una "sign" (immagine) e una "action" (testo)
    const cards = [];
    coppieScelte.forEach(p => {
      cards.push({ id: p.id, type: 'sign', data: p });
      cards.push({ id: p.id, type: 'action', data: p });
    });
    shuffle(cards);

    cards.forEach((c, idx) => {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'card';
      card.dataset.id = c.id;
      card.dataset.type = c.type;
      const aria = c.type === 'sign'
        ? `Segnale: ${c.data.name}`
        : `Comportamento: ${c.data.action}`;
      card.setAttribute('aria-label', aria);

      const front = document.createElement('span');
      front.className = 'card-face card-front';
      front.setAttribute('aria-hidden', 'true');

      const back = document.createElement('span');
      back.className = 'card-face card-back card-' + c.type;
      back.setAttribute('aria-hidden', 'true');

      if (c.type === 'sign') {
        const img = document.createElement('img');
        img.src = `/pittogrammi/iso7010/${c.data.sign}.svg`;
        img.alt = '';  // testo equivalente sull'aria-label del button
        img.loading = 'lazy';
        back.appendChild(img);
      } else {
        const txt = document.createElement('span');
        txt.className = 'card-action-text';
        txt.textContent = c.data.action;
        back.appendChild(txt);
      }

      card.appendChild(front);
      card.appendChild(back);
      card.addEventListener('click', flipCard);
      grid.appendChild(card);
    });
  }

  function flipCard(){
    if (lockBoard || this.classList.contains('matched') || this === firstCard) return;
    this.classList.add('flipped');
    if (!hasFlipped) {
      hasFlipped = true;
      firstCard = this;
      return;
    }
    secondCard = this;
    lockBoard = true;
    moves++;
    movesCountSpan.textContent = moves;
    checkForMatch();
  }

  function checkForMatch(){
    const sameId = firstCard.dataset.id === secondCard.dataset.id;
    const differentType = firstCard.dataset.type !== secondCard.dataset.type;
    if (sameId && differentType) {
      vinciCoppia();
    } else {
      sbagliaCoppia();
    }
  }

  function vinciCoppia(){
    firstCard.classList.add('matched');
    secondCard.classList.add('matched');
    firstCard.removeEventListener('click', flipCard);
    secondCard.removeEventListener('click', flipCard);
    matchedPairs++;
    pairsCountSpan.textContent = matchedPairs;
    showMatchToast(firstCard);

    // Spiegazione didattica del segnale appena abbinato
    const pair = coppieScelte.find(p => p.id === firstCard.dataset.id);
    if (pair) {
      explainTitle.textContent = '✓ ' + pair.name;
      explainBody.textContent = pair.explain;
      explainBox.classList.remove('hide');
    }

    resetTurno();

    if (matchedPairs === LIVELLI[livelloCorrente].coppie) {
      setTimeout(fineLivello, 800);
    }
  }

  function sbagliaCoppia(){
    setTimeout(() => {
      firstCard.classList.remove('flipped');
      secondCard.classList.remove('flipped');
      resetTurno();
    }, 1200);
    if (window.GameCoach && window.GameCoach.hint) {
      const fc = firstCard;
      window.GameCoach.hint(
        'Le carte si abbinano segnale ↔ comportamento. Cerca la coppia che si spiegano a vicenda.',
        '/cartografia/'
      );
    }
  }

  function resetTurno(){
    hasFlipped = false;
    lockBoard = false;
    firstCard = null;
    secondCard = null;
  }

  function fineLivello(){
    gameScreen.classList.add('hide');
    winScreen.classList.remove('hide');
    const cfg = LIVELLI[livelloCorrente];
    const minMosse = cfg.coppie;       // mosse perfette teoriche
    const stats = `Livello ${cfg.label} · ${cfg.coppie} coppie · ${moves} mosse`;
    winStats.textContent = stats;
    if (window.GiochiUtil) {
      window.GiochiUtil.salvaEMostraAttestato(
        'memory-primaria-' + livelloCorrente,
        cfg.coppie, cfg.coppie,
        '#win-screen .win-box'
      );
    }
  }

  const matchMessages = ['Bravo!', 'Giusto!', 'Ottimo!', 'Bene!', 'Super!', 'Grande!'];
  function showMatchToast(card){
    const msg = matchMessages[Math.floor(Math.random() * matchMessages.length)];
    const toast = document.createElement('div');
    toast.className = 'match-toast';
    toast.textContent = msg;
    toast.setAttribute('aria-live', 'polite');
    const rect = card.getBoundingClientRect();
    toast.style.left = rect.left + rect.width / 2 + 'px';
    toast.style.top = rect.top + 'px';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 900);
  }

  // Bottoni livelli intro
  document.querySelectorAll('[data-livello]').forEach(btn => {
    btn.addEventListener('click', () => avviaLivello(btn.dataset.livello));
  });

  // Restart dal win screen — rigioca stesso livello
  restartButton.addEventListener('click', () => avviaLivello(livelloCorrente));

  // Cambia livello dal win screen
  document.querySelectorAll('[data-cambia-livello]').forEach(btn => {
    btn.addEventListener('click', () => {
      winScreen.classList.add('hide');
      introScreen.classList.remove('hide');
    });
  });

  // Reset livello in corso
  if (resetLevelBtn) {
    resetLevelBtn.addEventListener('click', () => {
      gameScreen.classList.add('hide');
      introScreen.classList.remove('hide');
    });
  }
});
