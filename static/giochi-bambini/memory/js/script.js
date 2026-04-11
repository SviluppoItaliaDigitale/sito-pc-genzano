document.addEventListener('DOMContentLoaded', () => {
    const grid = document.querySelector('.memory-grid');
    const movesCountSpan = document.getElementById('moves-count');
    const winScreen = document.getElementById('win-screen');
    const restartButton = document.getElementById('restart-button');
    const pairsCountSpan = document.getElementById('pairs-count');
    const pairsTotalSpan = document.getElementById('pairs-total');
    let moves = 0, hasFlippedCard = false, lockBoard = false, firstCard, secondCard, matchedPairs = 0;
    const cardData = [
        { file: 'card-1', label: 'Fiamma — Incendio' },
        { file: 'card-2', label: 'Goccia d\'acqua — Alluvione' },
        { file: 'card-3', label: 'Casa con crepa — Terremoto' },
        { file: 'card-4', label: 'Croce — Primo soccorso' },
        { file: 'card-5', label: 'Telefono 112 — Emergenza' },
        { file: 'card-6', label: 'Casco — Protezione' },
        { file: 'card-7', label: 'Albero — Ambiente' },
        { file: 'card-8', label: 'Triangolo — Pericolo' }
    ];
    const cardNames = cardData.map(c => c.file);
    const cardsArray = [...cardNames, ...cardNames];

    function createBoard() {
        cardsArray.sort(() => Math.random() - 0.5);
        grid.innerHTML = '';
        matchedPairs = 0;
        moves = 0;
        movesCountSpan.textContent = moves;
        pairsCountSpan.textContent = 0;
        pairsTotalSpan.textContent = cardNames.length;
        cardsArray.forEach(name => {
            const card = document.createElement('div');
            card.classList.add('card');
            card.dataset.name = name;
            const data = cardData.find(c => c.file === name);
            const label = data ? data.label : name;
            card.setAttribute('aria-label', label);
            card.setAttribute('role', 'button');
            card.innerHTML = `<div class="card-face card-front"></div><div class="card-face card-back"><img src="img/${name}.svg" alt="${label}"></div>`;
            card.addEventListener('click', flipCard); // Aggiungiamo l'evento qui
            grid.appendChild(card);
        });
    }

    function flipCard() {
        if (lockBoard || this === firstCard || this.classList.contains('matched')) return; // Aggiunto controllo 'matched'
        this.classList.add('flipped');
        if (!hasFlippedCard) {
            hasFlippedCard = true;
            firstCard = this;
            return;
        }
        secondCard = this;
        lockBoard = true;
        moves++;
        movesCountSpan.textContent = moves;
        checkForMatch();
    }

    function checkForMatch() {
        (firstCard.dataset.name === secondCard.dataset.name) ? disableCards() : unflipCards();
    }

    function disableCards() {
        // --- CORREZIONE APPLICATA QUI ---
        // Rimuoviamo la possibilità di cliccare di nuovo sulle carte abbinate
        firstCard.removeEventListener('click', flipCard);
        secondCard.removeEventListener('click', flipCard);
        
        firstCard.classList.add('matched');
        secondCard.classList.add('matched');
        matchedPairs++;
        pairsCountSpan.textContent = matchedPairs;
        resetBoard();
        if (matchedPairs === cardNames.length) { 
            setTimeout(() => winScreen.classList.remove('hide'), 500); 
        }
    }

    function unflipCards() {
        setTimeout(() => {
            firstCard.classList.remove('flipped');
            secondCard.classList.remove('flipped');
            resetBoard();
        }, 1200);
    }

    function resetBoard() {
        [hasFlippedCard, lockBoard] = [false, false];
        [firstCard, secondCard] = [null, null];
    }

    restartButton.addEventListener('click', () => {
        winScreen.classList.add('hide');
        createBoard();
    });

    createBoard();
});