document.addEventListener('DOMContentLoaded', () => {
    const introScreen = document.getElementById('intro-screen');
    const gameScreen = document.getElementById('game-screen');
    const winScreen = document.getElementById('win-screen');
    const winMessage = document.getElementById('win-message');
    const startBtn = document.getElementById('start-btn');
    const restartBtn = document.getElementById('restart-btn');
    const itemsGrid = document.getElementById('items-grid');
    const itemsCount = document.getElementById('items-count');
    const itemsTotal = document.getElementById('items-total');
    const errorsCount = document.getElementById('errors-count');
    const zainoFill = document.getElementById('zaino-fill');

    const allItems = [
        { name: 'Acqua', icon: '\uD83D\uDCA7', correct: true, tip: 'Almeno 2 litri a persona!' },
        { name: 'Torcia', icon: '\uD83D\uDD26', correct: true, tip: 'Per vedere al buio senza fiamme' },
        { name: 'Fischietto', icon: '\uD83D\uDCEF', correct: true, tip: 'Per farsi trovare dai soccorritori' },
        { name: 'Coperta', icon: '\uD83D\uDECF\uFE0F', correct: true, tip: 'Per scaldarsi senza corrente' },
        { name: 'Medicinali', icon: '\uD83D\uDC8A', correct: true, tip: 'Quelli che la famiglia usa ogni giorno' },
        { name: 'Documenti', icon: '\uD83D\uDCC4', correct: true, tip: 'Copie di carta d\'identità e tessera sanitaria' },
        { name: 'Radio a pile', icon: '\uD83D\uDCFB', correct: true, tip: 'Per ascoltare le notizie senza corrente' },
        { name: 'Scarpe chiuse', icon: '\uD83D\uDC5F', correct: true, tip: 'Per camminare su vetri e macerie' },
        { name: 'Cibo a lunga conservazione', icon: '\uD83E\uDD6B', correct: true, tip: 'Scatolette, crackers, barrette' },
        { name: 'Caricatore portatile', icon: '\uD83D\uDD0B', correct: true, tip: 'Per tenere il telefono carico' },
        { name: 'Kit primo soccorso', icon: '\u26D1\uFE0F', correct: true, tip: 'Cerotti, garze, disinfettante' },
        { name: 'Vestiti di ricambio', icon: '\uD83D\uDC55', correct: true, tip: 'Un cambio completo per ognuno' },
        { name: 'Videogiochi', icon: '\uD83C\uDFAE', correct: false, tip: 'Non servono, occupano spazio prezioso!' },
        { name: 'Gelato', icon: '\uD83C\uDF66', correct: false, tip: 'Si scioglie subito, non si conserva' },
        { name: 'Pallone', icon: '\u26BD', correct: false, tip: 'Non serve in emergenza!' },
        { name: 'Televisore', icon: '\uD83D\uDCFA', correct: false, tip: 'Troppo pesante e serve la corrente' },
        { name: 'Skateboard', icon: '\uD83D\uDEF9', correct: false, tip: 'Ingombrante e inutile in emergenza' },
        { name: 'Peluche gigante', icon: '\uD83E\uDDF8', correct: false, tip: 'Occupa troppo spazio nello zaino' },
        { name: 'Album figurine', icon: '\uD83C\uDCCF', correct: false, tip: 'Non aiuta in emergenza!' },
        { name: 'Ombrellone', icon: '\u26F1\uFE0F', correct: false, tip: 'Troppo grande, non entra nello zaino' },
    ];

    let correctTotal, found, errors;

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function showToast(text, isGood) {
        const t = document.createElement('div');
        t.className = 'feedback-toast ' + (isGood ? 'good' : 'bad');
        t.textContent = text;
        document.body.appendChild(t);
        setTimeout(() => t.remove(), 1600);
    }

    function startGame() {
        introScreen.classList.add('hide');
        gameScreen.classList.remove('hide');
        winScreen.classList.add('hide');
        found = 0; errors = 0;
        const items = shuffle([...allItems]);
        correctTotal = items.filter(i => i.correct).length;
        itemsTotal.textContent = correctTotal;
        itemsCount.textContent = 0;
        errorsCount.textContent = 0;
        zainoFill.style.height = '0';
        itemsGrid.innerHTML = '';
        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'item-card';
            card.setAttribute('role', 'button');
            card.setAttribute('aria-label', item.name);
            card.innerHTML = '<span class="item-icon">' + item.icon + '</span><span class="item-name">' + item.name + '</span>';
            card.addEventListener('click', () => pickItem(card, item));
            itemsGrid.appendChild(card);
        });
    }

    function pickItem(card, item) {
        if (item.correct) {
            card.classList.add('correct');
            found++;
            itemsCount.textContent = found;
            zainoFill.style.height = Math.round((found / correctTotal) * 100) + '%';
            showToast(item.tip, true);
            if (found === correctTotal) {
                setTimeout(() => {
                    if (errors === 0) {
                        winMessage.textContent = 'Perfetto! Hai preparato lo zaino senza nessun errore!';
                    } else if (errors <= 3) {
                        winMessage.textContent = 'Bravo! Zaino pronto con solo ' + errors + ' errore' + (errors > 1 ? 'i' : '') + '.';
                    } else {
                        winMessage.textContent = 'Zaino pronto! Hai fatto ' + errors + ' errori. Riprova per migliorare!';
                    }
                    winScreen.classList.remove('hide');
                    var punti = Math.max(0, correctTotal - errors);
                    if (window.GiochiUtil) window.GiochiUtil.salvaEMostraAttestato('zaino-emergenza', punti, correctTotal, '#win-screen .win-box');
                }, 600);
            }
        } else {
            card.classList.add('wrong');
            errors++;
            errorsCount.textContent = errors;
            showToast(item.tip, false);
        }
    }

    startBtn.addEventListener('click', startGame);
    restartBtn.addEventListener('click', startGame);
});
