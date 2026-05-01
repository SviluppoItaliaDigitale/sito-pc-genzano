document.addEventListener('DOMContentLoaded', () => {
    const selectScreen = document.getElementById('select-screen');
    const gameScreen = document.getElementById('game-screen');
    const endScreen = document.getElementById('end-screen');
    const categoryList = document.getElementById('category-list');
    const catTitle = document.getElementById('cat-title');
    const leftCol = document.getElementById('left-col');
    const rightCol = document.getElementById('right-col');
    const matchedCount = document.getElementById('matched-count');
    const matchedTotal = document.getElementById('matched-total');
    const gameFeedback = document.getElementById('game-feedback');
    const endMsg = document.getElementById('end-msg');
    const anotherBtn = document.getElementById('another-btn');

    const categories = [
        {
            title: 'Numeri di emergenza', icon: '\uD83D\uDCDE',
            pairs: [
                { left: '112', right: 'Numero unico di emergenza nel Lazio' },
                { left: '803 555', right: 'Sala Operativa Protezione Civile Lazio' },
                { left: 'Chiamata al 112', right: 'Gratis, senza credito, da qualsiasi telefono' },
                { left: '112 in Europa', right: 'Stesso numero in tutti i Paesi europei' },
                { left: 'Cosa dire al 112', right: 'Cosa succede, dove sei, chi ha bisogno di aiuto' },
                { left: 'Chiamata per scherzo', right: 'E un reato e toglie aiuto a chi ne ha davvero bisogno' }
            ]
        },
        {
            title: 'Codici colore allerta', icon: '\uD83D\uDEA6',
            pairs: [
                { left: '\uD83D\uDFE2 Verde', right: 'Nessuna allerta, tutto tranquillo' },
                { left: '\uD83D\uDFE1 Giallo', right: 'Criticita ordinaria, presta attenzione' },
                { left: '\uD83D\uDFE0 Arancione', right: 'Criticita moderata, fenomeni intensi' },
                { left: '\uD83D\uDD34 Rosso', right: 'Criticita elevata, rischio alto' }
            ]
        },
        {
            title: 'Rischi e comportamenti', icon: '\u26A0\uFE0F',
            pairs: [
                { left: 'Terremoto', right: 'Riparati sotto un tavolo, proteggiti la testa' },
                { left: 'Alluvione', right: 'Sali ai piani alti, non scendere in cantina' },
                { left: 'Incendio boschivo', right: 'Chiama il 112 e allontanati dal fuoco' },
                { left: 'Temporale con fulmini', right: 'Entra in un edificio, stai lontano dagli alberi' },
                { left: 'Ondata di calore', right: 'Bevi molto, resta all\'ombra dalle 11 alle 17' },
                { left: 'Fuga di gas', right: 'Apri le finestre, esci, non toccare interruttori' }
            ]
        },
        {
            title: 'Oggetti dello zaino', icon: '\uD83C\uDF92',
            pairs: [
                { left: 'Torcia a pile', right: 'Per vedere al buio senza fiamme' },
                { left: 'Fischietto', right: 'Per farsi trovare dai soccorritori' },
                { left: 'Radio a pile', right: 'Per ascoltare le notizie senza corrente' },
                { left: 'Coperta termica', right: 'Per scaldarsi in caso di freddo' },
                { left: 'Documenti (copie)', right: 'Per farsi identificare in emergenza' },
                { left: 'Acqua (2 litri)', right: 'Per bere se manca l\'acqua potabile' }
            ]
        },
        {
            title: 'Cartelli di sicurezza', icon: '\uD83D\uDEA9',
            pairs: [
                { left: '\uD83D\uDFE9 Verde', right: 'Uscita di emergenza e vie di fuga' },
                { left: '\uD83D\uDFE5 Rosso', right: 'Dispositivi antincendio (estintore, idrante)' },
                { left: '\u26A0\uFE0F Giallo triangolo', right: 'Avvertimento: pericolo generico' },
                { left: '\uD83D\uDEAB Rosso con sbarra', right: 'Divieto: vietato fumare, vietato entrare' },
                { left: '\uD83D\uDD35 Blu rotondo', right: 'Prescrizione: obbligo di DPI (casco, guanti)' },
                { left: '\uD83C\uDDE8 Cassetta rossa', right: 'Punto di primo soccorso' }
            ]
        },
        {
            title: 'Classi di fuoco', icon: '\uD83D\uDD25',
            pairs: [
                { left: 'Classe A', right: 'Materiali solidi: legno, carta, tessuti' },
                { left: 'Classe B', right: 'Liquidi infiammabili: benzina, solventi' },
                { left: 'Classe C', right: 'Gas infiammabili: metano, GPL' },
                { left: 'Classe D', right: 'Metalli combustibili: magnesio, sodio' },
                { left: 'Classe F', right: 'Oli e grassi da cucina' },
                { left: 'Tecnica PASS', right: 'Prendi, Avvicinati, Schiaccia, Spazza' }
            ]
        },
        {
            title: 'Ruoli in emergenza', icon: '\uD83D\uDC65',
            pairs: [
                { left: 'Vigili del Fuoco', right: 'Incendi, soccorso tecnico, sostanze pericolose' },
                { left: 'Protezione Civile', right: 'Coordina aiuti e volontari in emergenza' },
                { left: 'Carabinieri / Polizia', right: 'Ordine pubblico e sicurezza' },
                { left: 'Ambulanza (ARES 118)', right: 'Emergenza sanitaria' },
                { left: 'Sindaco', right: 'Autorità di PC nel Comune' },
                { left: 'Volontario', right: 'Cittadino che aiuta gratuitamente' }
            ]
        },
        {
            title: 'Meteo e allerte', icon: '\uD83C\uDF24\uFE0F',
            pairs: [
                { left: 'Temporale', right: 'Pioggia + fulmini + vento forte' },
                { left: 'Nebbia', right: 'Visibilità ridotta, soprattutto in auto' },
                { left: 'Grandine', right: 'Ghiaccio in chicchi che cade dal cielo' },
                { left: 'Ondata di calore', right: 'Temperature molto alte per giorni' },
                { left: 'Gelo', right: 'Strade scivolose, attenzione al ghiaccio' },
                { left: 'Vento forte', right: 'Attenzione ad alberi e cartelloni' }
            ]
        }
    ];

    let selectedLeft = null, matched = 0, total = 0, errors = 0, currentCat = null;

    // Mappa titolo categoria → pagina teoria del sito
    const TEORIA_CAT = {
        'Numeri di emergenza':    { url: '/numeri-utili/',                       titolo: 'numeri utili' },
        'Codici colore allerta':  { url: '/allerte-meteo/',                      titolo: 'allerte meteo' },
        'Rischi e comportamenti': { url: '/rischi-prevenzione/',                 titolo: 'rischi e prevenzione' },
        'Oggetti dello zaino':    { url: '/rischi-prevenzione/kit-emergenza/',   titolo: 'kit di emergenza' },
        'Cartelli di sicurezza':  { url: '/pittogrammi/',                        titolo: 'pittogrammi' },
        'Classi di fuoco':        { url: '/rischi-prevenzione/rischio-incendio/',titolo: 'rischio incendio' },
        'Ruoli in emergenza':     { url: '/chi-siamo/',                          titolo: 'chi siamo' },
        'Meteo e allerte':        { url: '/allerte-meteo/',                      titolo: 'allerte meteo' }
    };

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function renderCategories() {
        selectScreen.classList.remove('hide');
        gameScreen.classList.add('hide');
        endScreen.classList.add('hide');
        categoryList.innerHTML = '';
        categories.forEach(cat => {
            const col = document.createElement('div');
            col.className = 'col-6 col-md-3';
            col.innerHTML = '<div class="cat-card" role="button" tabindex="0"><span class="cat-icon">' + cat.icon + '</span><span class="cat-title">' + cat.title + '</span></div>';
            col.querySelector('.cat-card').addEventListener('click', () => startCategory(cat));
            categoryList.appendChild(col);
        });
    }

    function startCategory(cat) {
        selectScreen.classList.add('hide');
        gameScreen.classList.remove('hide');
        catTitle.textContent = cat.title;
        currentCat = cat;
        matched = 0; errors = 0; selectedLeft = null;
        total = cat.pairs.length;
        matchedCount.textContent = 0;
        matchedTotal.textContent = total;
        gameFeedback.classList.add('hide');

        const leftItems = shuffle(cat.pairs.map((p, i) => ({ id: i, text: p.left })));
        const rightItems = shuffle(cat.pairs.map((p, i) => ({ id: i, text: p.right })));

        leftCol.innerHTML = '';
        rightCol.innerHTML = '';

        leftItems.forEach(item => {
            const el = document.createElement('div');
            el.className = 'match-item';
            el.textContent = item.text;
            el.dataset.id = item.id;
            el.dataset.side = 'left';
            el.addEventListener('click', () => selectItem(el, 'left'));
            leftCol.appendChild(el);
        });

        rightItems.forEach(item => {
            const el = document.createElement('div');
            el.className = 'match-item';
            el.textContent = item.text;
            el.dataset.id = item.id;
            el.dataset.side = 'right';
            el.addEventListener('click', () => selectItem(el, 'right'));
            rightCol.appendChild(el);
        });
    }

    function selectItem(el, side) {
        if (el.classList.contains('matched')) return;

        if (side === 'left') {
            leftCol.querySelectorAll('.match-item').forEach(e => e.classList.remove('selected'));
            el.classList.add('selected');
            selectedLeft = el;
            gameFeedback.classList.add('hide');
        } else if (side === 'right' && selectedLeft) {
            if (selectedLeft.dataset.id === el.dataset.id) {
                selectedLeft.classList.remove('selected');
                selectedLeft.classList.add('matched');
                el.classList.add('matched');
                matched++;
                matchedCount.textContent = matched;
                gameFeedback.className = 'game-feedback correct';
                gameFeedback.textContent = 'Giusto!';
                gameFeedback.classList.remove('hide');
                if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
                selectedLeft = null;
                if (matched === total) {
                    setTimeout(showEnd, 800);
                }
            } else {
                errors++;
                el.classList.add('wrong-flash');
                selectedLeft.classList.add('wrong-flash');
                gameFeedback.className = 'game-feedback wrong';
                gameFeedback.textContent = 'Non corrispondono, riprova!';
                gameFeedback.classList.remove('hide');
                if (window.GameCoach && window.GameCoach.hint && currentCat) {
                    const t = TEORIA_CAT[currentCat.title] || { url: '/rischi-prevenzione/', titolo: 'rischi e prevenzione' };
                    window.GameCoach.hint('Pensa al collegamento più diretto. La pagina ' + t.titolo + ' del sito ti dà gli abbinamenti giusti.', t.url);
                }
                setTimeout(() => {
                    el.classList.remove('wrong-flash');
                    if (selectedLeft) selectedLeft.classList.remove('wrong-flash', 'selected');
                    selectedLeft = null;
                }, 600);
            }
        }
    }

    function showEnd() {
        gameScreen.classList.add('hide');
        endScreen.classList.remove('hide');
        if (errors === 0) { endMsg.textContent = 'Perfetto! Tutti abbinati senza errori!'; }
        else if (errors <= 3) { endMsg.textContent = 'Bravo! Solo ' + errors + ' errore' + (errors > 1 ? 'i' : '') + '.'; }
        else { endMsg.textContent = 'Fatto! Hai commesso ' + errors + ' errori. Riprova per migliorare!'; }
        var punti = Math.max(0, total - errors);
        if (window.GiochiUtil) window.GiochiUtil.salvaEMostraAttestato('abbina-impara', punti, total, '#end-screen');
    }

    anotherBtn.addEventListener('click', renderCategories);
    renderCategories();
});
