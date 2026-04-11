document.addEventListener('DOMContentLoaded', () => {
    const selectionScreen = document.getElementById('selection-screen');
    const gameScreen = document.getElementById('game-screen');
    const winScreen = document.getElementById('win-screen');
    const scenarioButtonsContainer = document.getElementById('scenario-buttons');
    const sceneContainer = document.getElementById('scene-container');
    const sceneImage = document.getElementById('scene-image');
    const risksList = document.getElementById('risks-list');
    const totalRisksSpan = document.getElementById('total-risks');
    const scenarioTitle = document.getElementById('scenario-title');
    const restartButton = document.getElementById('restart-button');
    const backToSelectionButton = document.getElementById('back-to-selection');
    let foundCount = 0;
    let currentVariation, currentScenario;

    const scenarios = [
        {
            id: 'casa', name: 'In Casa',
            variations: [
                { image: 'img/scena-casa.jpg', risks: [
  { id: 'presa_elettrica', name: 'Presa elettrica senza copertura di sicurezza per bambini', top: 69.24, left: 21.56, size: 10 },
  { id: 'cassetti_aperti', name: 'Cassetti aperti con rischio di chiusura improvvisa', top: 66.15, left: 87.04, size: 10 },
  { id: 'lampada', name: 'Lampada accesa che scotta se toccata', top: 42.67, left: 17.42, size: 10 }
]},
                { image: 'img/scenariocasa1.jpg', risks: [
  { id: 'finestre_aperte', name: 'Finestre aperte che possono chiudersi all'improvviso', top: 57.3, left: 47.94, size: 20 },
  { id: 'gradini', name: 'Inciampare sui gradini delle scale', top: 83.55, left: 63.35, size: 10 },
  { id: 'tappeto', name: 'Tappeto stropicciato può causare inciampo', top: 84.42, left: 42.42, size: 10 },
  { id: 'spigolo_tavolo', name: 'Il bordo dello spigolo del tavolo, se urtato, può causare dolore.', top: 84.57, left: 82.21, size: 10 }
] },
                { image: 'img/scenariocasa2.jpg', risks: [
  { id: 'lampadina', name: 'Lampadina che scotta al tocco della mano.', top: 56.36, left: 84.67, size: 10 },
  { id: 'tavolo', name: 'Gli spigoli del tavolo possono provocare dolore se urtati.', top: 83.81, left: 57.37, size: 10 },
  { id: 'testata_letto', name: 'La testata del letto può causare dolore se urtata.', top: 55.83, left: 26.16, size: 10 },
  { id: 'piedi_letto', name: 'I piedi del letto possono causare dolore se urtati.', top: 89.65, left: 11.14, size: 10 },
  { id: 'cassetti', name: 'Chiusura dei cassetti senza attenzione.', top: 65.91, left: 77.15, size: 10 }
] }
                  
                      ]
        },
        {
            id: 'cucina', name: 'In Cucina',
            variations: [
                { image: 'img/scenariocucina1.jpg', risks: [
  { id: 'forno_acceso', name: 'Fornelli e forno accesi', top: 44.74, left: 40.81, size: 20 },
  { id: 'spigoli', name: 'Spigoli sporgenti.', top: 28.1, left: 46.71, size: 10 },
  { id: 'apertura_ante', name: 'Apertura ante con spigoli sporgenti.', top: 58.65, left: 79.53, size: 10 },
  { id: 'tappeto', name: 'Tappeto se arricciato, causa inciampo.', top: 84.02, left: 62.51, size: 10 }
] },
                { image: 'img/scenariocucina2.jpg', risks: [
  { id: 'spigoli', name: 'Spigoli dei mobili sporgenti.', top: 29, left: 55.38, size: 10 },
  { id: 'fornello_acceso', name: 'Fornello e forno accesi', top: 49.95, left: 43.49, size: 20 },
  { id: 'tappeto', name: 'Tappeto arricciato.', top: 84.47, left: 78.69, size: 10 },
  { id: 'cassettiere', name: 'Cassetti e ante aperte.', top: 62.49, left: 19.34, size: 10 },
  { id: 'barattoli', name: 'Barattoli sporgenti.', top: 50.75, left: 12.98, size: 10 },
  { id: 'attrezzi', name: 'Attrezzi pericolosi', top: 40.97, left: 67.64, size: 10 }
] }
            ]
        },
        {
            id: 'bagno', name: 'In Bagno',
            variations: [ { image: 'img/scenariobagno.jpg', risks: [
  { id: 'tappeto_scivoloso', name: 'Tappeto scivoloso.', top: 80.83, left: 58.75, size: 10 },
  { id: 'spigoli', name: 'Spigoli sporgenti.', top: 58.56, left: 40.81, size: 10 },
  { id: 'oblo', name: 'Oblò della lavatrice: rischio di schiacciamento dita', top: 67.05, left: 16.58, size: 10 },
  { id: 'sgabello', name: 'Sgabello instabile: rischio di caduta', top: 71.88, left: 75.77, size: 10 }
] } ]
        },
        {
            id: 'cameretta', name: 'In Cameretta',
            variations: [
                { image: 'img/scenariogiochi1.jpg', risks: [
  { id: 'tappeto', name: 'Tappeto arricciato.', top: 82.6, left: 62.89, size: 10 },
  { id: 'giochi', name: 'Giochi disordinati causano inciampo.', top: 82.12, left: 35.37, size: 10 },
  { id: 'lampadina', name: 'Lampada che scotta.', top: 41.78, left: 6.54, size: 10 },
  { id: 'monitor', name: 'Monitor del computer affatica gli occhi.', top: 33.81, left: 88.19, size: 10 },
  { id: 'spigoli', name: 'Spigoli del letto se urtati provocano dolore.', top: 58.36, left: 43.72, size: 25 }
] },
                { image: 'img/scenariogiochi2.jpg', risks: [
  { id: 'scivolo', name: 'Scivolo pericoloso.', top: 57.81, left: 82.21, size: 10 },
  { id: 'giochi', name: 'Giochi sparsi.', top: 84.26, left: 21.03, size: 10 },
  { id: 'spigoli', name: 'Spigoli appuntiti.', top: 75.08, left: 43.8, size: 10 },
  { id: 'lampadina', name: 'Lampadina che scotta.', top: 36.69, left: 27.54, size: 10 },
  { id: 'finestra', name: 'Apertura finestra.', top: 61.22, left: 36.36, size: 10 }
] }
            ]
        },
        {
            id: 'classe', name: 'In Classe',
            variations: [ { image: 'img/scenarioclasse.jpg', risks: [
  { id: 'spigoli', name: 'Spigoli appuntiti.', top: 61.46, left: 39.35, size: 10 },
  { id: 'finestra', name: 'Finestra apribile.', top: 47.76, left: 96.55, size: 10 },
  { id: 'spigolo', name: 'Spigolo del ripiano.', top: 44.08, left: 22.56, size: 10 }
] } ]
        },
        {
            id: 'parco', name: 'Al Parco Giochi',
            variations: [ { image: 'img/scenarioparco1.jpg', risks: [
  { id: 'inciampo', name: 'Inciampare sul ponte.', top: 56.12, left: 16.27, size: 10 },
  { id: 'cadere', name: 'Scivolare e cadere dal gioco.', top: 78.84, left: 14.28, size: 10 },
  { id: 'scivolo', name: 'Scivolare senza visione di un adulto.', top: 64.81, left: 51.54, size: 10 },
  { id: 'caduta', name: 'Cadere dal cavallo a molla.', top: 57.36, left: 40.2, size: 10 },
  { id: 'mani', name: 'Farsi male alle braccia e alle mani.', top: 49.73, left: 91.8, size: 10 }
] } ]
        },
        {
            id: 'scuolabus', name: 'Sullo Scuolabus',
            variations: [ { image: 'img/scenarioscuolabus.jpg', risks: [
  { id: 'autista', name: 'Disturbare il conducente.', top: 43.65, left: 38.36, size: 10 },
  { id: 'inciampo', name: 'Inciampare sugli scalini.', top: 71.88, left: 50.01, size: 10 },
  { id: 'attraversamento', name: 'Attraversare la strada.', top: 72.11, left: 76.77, size: 25 }
] } ]
        }
    ];

    function showSelectionScreen() {
        if (!selectionScreen) return;
        gameScreen.classList.add('hide');
        winScreen.classList.add('hide');
        selectionScreen.classList.remove('hide');
        scenarioButtonsContainer.innerHTML = '';
        scenarios.forEach(scenario => {
            const button = document.createElement('button');
            button.classList.add('scenario-btn');
            button.innerText = scenario.name;
            button.dataset.id = scenario.id;
            button.addEventListener('click', () => startGame(scenario.id));
            scenarioButtonsContainer.appendChild(button);
        });
    }
    
    function startGame(scenarioId) {
        currentScenario = scenarios.find(s => s.id === scenarioId);
        if (!currentScenario) return;
        const variations = currentScenario.variations;
        currentVariation = variations[Math.floor(Math.random() * variations.length)];
        selectionScreen.classList.add('hide');
        gameScreen.classList.remove('hide');
        winScreen.classList.add('hide');
        initializeGame();
    }

    function initializeGame() {
        foundCount = 0;
        sceneImage.src = currentVariation.image;
        const scenarioButton = document.querySelector(`[data-id="${currentScenario.id}"]`);
        scenarioTitle.innerText = `Caccia al Rischio: ${scenarioButton.textContent}`;
        risksList.innerHTML = '';
        sceneContainer.querySelectorAll('.hotspot').forEach(el => el.remove());
        totalRisksSpan.textContent = currentVariation.risks.length;
        currentVariation.risks.forEach(risk => {
            const listItem = document.createElement('li');
            listItem.id = `li-${risk.id}`;
            listItem.textContent = risk.name;
            risksList.appendChild(listItem);
            const hotspot = document.createElement('div');
            hotspot.classList.add('hotspot');
            hotspot.id = `hotspot-${risk.id}`;
            hotspot.style.top = `${risk.top}%`;
            hotspot.style.left = `${risk.left}%`;
            hotspot.style.width = `${risk.size}%`;
            hotspot.style.height = `${risk.size}%`;
            hotspot.addEventListener('click', () => foundRisk(risk));
            sceneContainer.appendChild(hotspot);
        });
    }

    function foundRisk(risk) {
        const listItem = document.getElementById(`li-${risk.id}`);
        const hotspot = document.getElementById(`hotspot-${risk.id}`);
        if (!listItem.classList.contains('found')) {
            listItem.classList.add('found');
            hotspot.classList.add('found');
            foundCount++;
        }
        if (foundCount === currentVariation.risks.length) {
             setTimeout(() => winScreen.classList.remove('hide'), 500);
        }
    }

    if (restartButton) {
        restartButton.addEventListener('click', () => {
            winScreen.classList.add('hide');
            initializeGame();
        });
    }
    
    if (backToSelectionButton) {
        backToSelectionButton.addEventListener('click', (e) => {
            e.preventDefault();
            showSelectionScreen();
        });
    }
    
    if (selectionScreen) {
        showSelectionScreen();
    }
});