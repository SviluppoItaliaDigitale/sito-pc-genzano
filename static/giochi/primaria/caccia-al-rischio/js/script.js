// Caccia al Rischio — versione 2 (maggio 2026).
// Prima i "rischi" erano sicurezza domestica generica (spigoli, tappeti, lampadine):
// fuori dal mandato Protezione Civile. Audit ha indicato necessita' di angolo PC.
//
// Strategia: stessi scenari illustrati (le SVG di casa, cucina, bagno, classe, parco,
// scuolabus) ma ogni rischio e' rifrasato con il suo significato per la PC e
// accompagnato da una spiegazione didattica ("cosa fare in caso di terremoto/
// alluvione/blackout/evacuazione") quando il bambino lo trova.
// Scenari e variazioni mescolati a ogni partita (rigiocabilita').
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
  const scenarioIntro = document.getElementById('scenario-intro');
  const restartButton = document.getElementById('restart-button');
  const backToSelectionButton = document.getElementById('back-to-selection');
  const explainBox = document.getElementById('explain-box');
  const explainTitle = document.getElementById('explain-title');
  const explainBody = document.getElementById('explain-body');

  let foundCount = 0;
  let currentVariation = null;
  let currentScenario = null;

  // Ogni rischio: id, name, top/left/size (posizione hotspot %), explain (cosa
  // fare in caso di emergenza PC associata). Le explain pescano da:
  // /rischi-prevenzione/sismico, .../incendio, .../idrogeologico, .../temporali,
  // .../blackout, .../ondate-calore, .../vento (rules 06-pc-scientifica).
  const scenarios = [
    {
      id: 'casa', name: 'In Casa',
      intro: 'Ogni casa ha pericoli quotidiani che durante un\'emergenza diventano piu\' grossi. Trovali tutti.',
      variations: [
        { image: 'img/scena-casa.svg', risks: [
          { id: 'presa_elettrica', name: 'Presa elettrica scoperta',
            explain: 'In caso di blackout o temporale: non infilare le dita. Spegnere il quadro elettrico generale prima di rimettere mano alle prese.',
            top: 69.24, left: 21.56, size: 10 },
          { id: 'cassetti_aperti', name: 'Cassetti aperti',
            explain: 'Durante un terremoto i cassetti aperti possono cadere. Tienili sempre chiusi: meno cose volano in giro durante una scossa.',
            top: 66.15, left: 87.04, size: 10 },
          { id: 'lampada', name: 'Lampada accesa che scotta',
            explain: 'Se va via la luce, niente candele: usano fiamme libere e con tappeti o tende possono provocare incendi. Meglio una torcia a pile.',
            top: 42.67, left: 17.42, size: 10 }
        ]},
        { image: 'img/scenariocasa1.svg', risks: [
          { id: 'finestre_aperte', name: 'Finestre aperte',
            explain: 'Con vento forte (allerta gialla o arancione) chiudere le finestre: rami e oggetti possono entrare. In caso di temporale stare lontani da finestre per i fulmini.',
            top: 57.3, left: 47.94, size: 20 },
          { id: 'gradini', name: 'Inciampo sui gradini',
            explain: 'In evacuazione si scende dalle scale (mai ascensore!). Tieni sempre il corrimano e cammina, non correre: gli scalini sono il primo punto di caduta.',
            top: 83.55, left: 63.35, size: 10 },
          { id: 'tappeto', name: 'Tappeto stropicciato',
            explain: 'Allarme di evacuazione: bisogna uscire in fila in pochi secondi. Tappeti arricciati e oggetti per terra fanno cadere chi corre.',
            top: 84.42, left: 42.42, size: 10 },
          { id: 'spigolo_tavolo', name: 'Spigolo del tavolo',
            explain: 'Durante una scossa di terremoto si sta SOTTO il tavolo, non vicino allo spigolo. Sotto il tavolo proteggi testa e spalle se cade qualcosa dall\'alto.',
            top: 84.57, left: 82.21, size: 10 }
        ]},
        { image: 'img/scenariocasa2.svg', risks: [
          { id: 'lampadina', name: 'Lampadina che scotta',
            explain: 'Una lampadina che scotta segna che e\' accesa: durante un blackout si spegne da sola. Con la luce assente, una torcia a pile e\' piu\' sicura delle candele.',
            top: 56.36, left: 84.67, size: 10 },
          { id: 'tavolo', name: 'Spigoli del tavolo',
            explain: 'Durante una scossa metterti SOTTO il tavolo e non urtare lo spigolo. Resta li\' finche\' la scossa non finisce.',
            top: 83.81, left: 57.37, size: 10 },
          { id: 'testata_letto', name: 'Testata del letto',
            explain: 'Durante un terremoto, se sei a letto, copri la testa col cuscino e resta vicino alla testata: e\' una zona piu\' resistente del centro del letto.',
            top: 55.83, left: 26.16, size: 10 },
          { id: 'piedi_letto', name: 'Piedi del letto',
            explain: 'Mai mettere oggetti pesanti sopra l\'armadio o sopra la testata. In una scossa cadrebbero proprio dove dormi.',
            top: 89.65, left: 11.14, size: 10 },
          { id: 'cassetti', name: 'Cassetti senza fermo',
            explain: 'In zone sismiche fissare i mobili al muro. Cassetti che si aprono di colpo durante la scossa possono colpire le gambe.',
            top: 65.91, left: 77.15, size: 10 }
        ]}
      ]
    },
    {
      id: 'cucina', name: 'In Cucina',
      intro: 'La cucina ha gas e fuoco: e\' uno dei posti dove un piccolo incidente puo\' diventare un\'emergenza vera.',
      variations: [
        { image: 'img/scenariocucina1.svg', risks: [
          { id: 'forno_acceso', name: 'Fornelli e forno accesi',
            explain: 'In caso di terremoto o evacuazione: spegnere subito gas e forno. Se senti odore di gas dopo una scossa, non accendere niente, apri le finestre e chiama il 112.',
            top: 44.74, left: 40.81, size: 20 },
          { id: 'spigoli', name: 'Spigoli sporgenti',
            explain: 'Durante una scossa stare lontano da angoli appuntiti. Cerca un posto sotto un tavolo robusto o nel vano di una porta interna portante.',
            top: 28.1, left: 46.71, size: 10 },
          { id: 'apertura_ante', name: 'Ante aperte',
            explain: 'Bicchieri e piatti negli scaffali con la scossa cadono e si rompono. Tieni le ante chiuse, e in zone sismiche metti delle chiusure di sicurezza.',
            top: 58.65, left: 79.53, size: 10 },
          { id: 'tappeto', name: 'Tappeto arricciato',
            explain: 'In una fuga d\'emergenza un tappeto e\' un primo motivo di caduta. Toglilo prima dell\'allerta o bloccalo con strisce antiscivolo.',
            top: 84.02, left: 62.51, size: 10 }
        ]},
        { image: 'img/scenariocucina2.svg', risks: [
          { id: 'spigoli', name: 'Spigoli dei mobili',
            explain: 'Durante una scossa sotto al tavolo: mai vicino agli angoli sporgenti dei mobili che possono colpirti.',
            top: 29, left: 55.38, size: 10 },
          { id: 'fornello_acceso', name: 'Fornello e forno accesi',
            explain: 'Allerta o no, mai lasciare i fornelli accesi senza un adulto. In caso di scossa o evacuazione: chiudere il rubinetto del gas.',
            top: 49.95, left: 43.49, size: 20 },
          { id: 'tappeto', name: 'Tappeto arricciato',
            explain: 'In emergenza si esce di corsa: un tappeto arricciato fa cadere. Soprattutto a chi porta lo zaino di emergenza.',
            top: 84.47, left: 78.69, size: 10 },
          { id: 'cassettiere', name: 'Cassetti aperti',
            explain: 'Quando trema, i cassetti aperti diventano proiettili. Il primo passo della prevenzione e\' tenere le cose chiuse e fissate.',
            top: 62.49, left: 19.34, size: 10 },
          { id: 'barattoli', name: 'Barattoli sporgenti',
            explain: 'Vetri sugli scaffali alti = pericolo di taglio durante una scossa. In zona sismica: mensole basse, oggetti pesanti in basso.',
            top: 50.75, left: 12.98, size: 10 },
          { id: 'attrezzi', name: 'Coltelli a portata di mano',
            explain: 'In una scossa improvvisa, coltelli sul piano possono cadere. Vanno chiusi in cassetto, lontano dall\'altezza testa.',
            top: 40.97, left: 67.64, size: 10 }
        ]}
      ]
    },
    {
      id: 'bagno', name: 'In Bagno',
      intro: 'Il bagno ha acqua, elettricita\' e superfici scivolose: durante un\'emergenza serve estra cautela.',
      variations: [{ image: 'img/scenariobagno.svg', risks: [
        { id: 'tappeto_scivoloso', name: 'Tappetino scivoloso',
          explain: 'In una fuga d\'emergenza dalla doccia, un tappetino bagnato fa cadere. Antiscivolo sotto il tappeto o niente tappeto.',
          top: 80.83, left: 58.75, size: 10 },
        { id: 'spigoli', name: 'Spigoli sporgenti',
          explain: 'Durante un terremoto, evita di restare in piedi vicino agli spigoli del lavandino o della vasca. Meglio sedersi a terra in un angolo lontano da vetri.',
          top: 58.56, left: 40.81, size: 10 },
        { id: 'oblo', name: 'Oblo\' della lavatrice',
          explain: 'Durante un blackout l\'asciugatura si ferma: non aprire l\'oblo\' di colpo se ha acqua dentro, finisce sul pavimento e diventa scivoloso.',
          top: 67.05, left: 16.58, size: 10 },
        { id: 'sgabello', name: 'Sgabello instabile',
          explain: 'In allerta sismica non lasciare sgabelli o oggetti altri instabili: cadrebbero alla prima scossa. Mensole alte e oggetti pesanti vanno fissati al muro.',
          top: 71.88, left: 75.77, size: 10 }
      ]}]
    },
    {
      id: 'cameretta', name: 'In Cameretta',
      intro: 'In cameretta passi tante ore: anche di notte. Conoscere i rischi qui significa sapere cosa fare se trema mentre dormi.',
      variations: [
        { image: 'img/scenariogiochi1.svg', risks: [
          { id: 'tappeto', name: 'Tappeto arricciato',
            explain: 'Allarme di notte: bisogna alzarsi al buio e uscire. Tappeto arricciato + buio = caduta sicura. Tienilo piatto o usa antiscivolo.',
            top: 82.6, left: 62.89, size: 10 },
          { id: 'giochi', name: 'Giochi sparsi a terra',
            explain: 'Se trema mentre dormi devi uscire dal letto: giochi a terra e Lego sono lo stesso problema dei tappeti. Riponili prima di dormire.',
            top: 82.12, left: 35.37, size: 10 },
          { id: 'lampadina', name: 'Lampada vicina al letto',
            explain: 'Durante una scossa la lampada cade: se e\' sopra al letto puoi farti male. Spostala a terra o fissala.',
            top: 41.78, left: 6.54, size: 10 },
          { id: 'monitor', name: 'Monitor sul bordo',
            explain: 'Schermi e mensole alte cadono per primi. Fissali con strap o mettili a terra in zona sismica.',
            top: 33.81, left: 88.19, size: 10 },
          { id: 'spigoli', name: 'Spigoli del letto',
            explain: 'Sopra al letto non mettere mensole o quadri pesanti: in una scossa cadono dritti dove dormi.',
            top: 58.36, left: 43.72, size: 25 }
        ]},
        { image: 'img/scenariogiochi2.svg', risks: [
          { id: 'scivolo', name: 'Scivolo da gioco instabile',
            explain: 'Strutture da gioco grandi vanno fissate al muro. In una scossa cadono di lato e bloccano la via di fuga.',
            top: 57.81, left: 82.21, size: 10 },
          { id: 'giochi', name: 'Giochi sparsi',
            explain: 'In un\'evacuazione di notte la via dal letto alla porta deve essere libera. Riordinare prima di dormire e\' la prima regola.',
            top: 84.26, left: 21.03, size: 10 },
          { id: 'spigoli', name: 'Spigoli appuntiti',
            explain: 'In zone sismiche mobili spigolosi vicino al letto sono il primo problema. Cerca un posto sicuro lontano dagli angoli, sotto un tavolo robusto.',
            top: 75.08, left: 43.8, size: 10 },
          { id: 'lampadina', name: 'Lampada appesa',
            explain: 'Lampadari sopra al letto, in caso di scossa, possono staccarsi. Usa lampade fisse a parete o luci LED a soffitto a vite robusta.',
            top: 36.69, left: 27.54, size: 10 },
          { id: 'finestra', name: 'Finestra aperta',
            explain: 'In allerta vento (codice giallo o arancione) chiudere le finestre: vetri rotti = ferite gravi. In allerta temporale: lontano dai vetri.',
            top: 61.22, left: 36.36, size: 10 }
        ]}
      ]
    },
    {
      id: 'classe', name: 'In Classe',
      intro: 'A scuola ci sono prove di evacuazione due volte all\'anno. Conoscere i rischi della classe ti rende piu\' veloce nella vera emergenza.',
      variations: [{ image: 'img/scenarioclasse.svg', risks: [
        { id: 'spigoli', name: 'Banchi con spigoli',
          explain: 'Durante una scossa sotto al banco coprendo la testa: il banco assorbe il colpo se cade qualcosa dall\'alto. Resta li\' finche\' la maestra dice di uscire.',
          top: 61.46, left: 39.35, size: 10 },
        { id: 'finestra', name: 'Finestra apribile',
          explain: 'Mai uscire dalla finestra: si esce dalla porta con la fila. La finestra e\' un punto pericoloso durante un terremoto (vetri rotti) e va chiusa.',
          top: 47.76, left: 96.55, size: 10 },
        { id: 'spigolo', name: 'Spigolo del ripiano',
          explain: 'Mensole con libri sopra al banco = libri che cadono in scossa. Le scuole anti-sismiche hanno tutto fissato al muro con barre.',
          top: 44.08, left: 22.56, size: 10 }
      ]}]
    },
    {
      id: 'parco', name: 'Al Parco',
      intro: 'Anche all\'aperto ci sono rischi: e durante un\'allerta meteo o un terremoto, sapere cosa fare cambia tutto.',
      variations: [{ image: 'img/scenarioparco1.svg', risks: [
        { id: 'inciampo', name: 'Ponte sospeso',
          explain: 'In una scossa di terremoto, scendere subito da strutture sospese e sederti a terra in spazio aperto, lontano da alberi e pali.',
          top: 56.12, left: 16.27, size: 10 },
        { id: 'cadere', name: 'Struttura alta del gioco',
          explain: 'Durante un temporale: scendere subito dalle strutture alte e dai giochi metallici (attirano fulmini). Andare verso un edificio.',
          top: 78.84, left: 14.28, size: 10 },
        { id: 'scivolo', name: 'Scivolo metallico',
          explain: 'In allerta caldo (allerta arancione o rossa) il metallo scotta: aspetta che faccia ombra. In temporale, niente metallo per i fulmini.',
          top: 64.81, left: 51.54, size: 10 },
        { id: 'caduta', name: 'Cavallo a molla',
          explain: 'Durante una scossa sismica all\'aperto: scendi e siediti in spazio libero, lontano da alberi che possono cadere e da fili elettrici.',
          top: 57.36, left: 40.2, size: 10 },
        { id: 'mani', name: 'Sbarre alte',
          explain: 'Con vento forte (allerta gialla per vento) lascia subito le sbarre: rami e oggetti possono volare. Cerca un edificio robusto.',
          top: 49.73, left: 91.8, size: 10 }
      ]}]
    },
    {
      id: 'scuolabus', name: 'Sullo Scuolabus',
      intro: 'In viaggio si applicano regole di sicurezza piu\' strette: l\'autista non puo\' fermarsi ovunque.',
      variations: [{ image: 'img/scenarioscuolabus.svg', risks: [
        { id: 'autista', name: 'Disturbare l\'autista',
          explain: 'L\'autista in caso di terremoto deve fermarsi in posto sicuro (lontano da ponti, sottopassaggi, alberi alti). Non distrarlo, fagli sentire l\'avviso radio.',
          top: 43.65, left: 38.36, size: 10 },
        { id: 'inciampo', name: 'Scalini',
          explain: 'In evacuazione del bus si scende uno alla volta, mai correndo: lo scalino e\' alto e si cade facile. Le maestre in fondo controllano.',
          top: 71.88, left: 50.01, size: 10 },
        { id: 'attraversamento', name: 'Attraversare la strada',
          explain: 'Dopo aver lasciato il bus: aspettare che riparta prima di attraversare. In caso di allerta meteo, l\'autista chiama il Comune e segue le istruzioni.',
          top: 72.11, left: 76.77, size: 25 }
      ]}]
    }
  ];

  function shuffle(arr){
    for (let i = arr.length - 1; i > 0; i--){
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function showSelectionScreen(){
    if (!selectionScreen) return;
    gameScreen.classList.add('hide');
    winScreen.classList.add('hide');
    selectionScreen.classList.remove('hide');
    scenarioButtonsContainer.innerHTML = '';
    // Mostra gli scenari in ordine random a ogni ritorno
    const sorted = shuffle([...scenarios]);
    sorted.forEach(scenario => {
      const button = document.createElement('button');
      button.classList.add('scenario-btn');
      button.innerText = scenario.name;
      button.dataset.id = scenario.id;
      button.addEventListener('click', () => startGame(scenario.id));
      scenarioButtonsContainer.appendChild(button);
    });
  }

  function startGame(scenarioId){
    currentScenario = scenarios.find(s => s.id === scenarioId);
    if (!currentScenario) return;
    const variations = currentScenario.variations;
    currentVariation = variations[Math.floor(Math.random() * variations.length)];
    selectionScreen.classList.add('hide');
    gameScreen.classList.remove('hide');
    winScreen.classList.add('hide');
    initializeGame();
  }

  function initializeGame(){
    foundCount = 0;
    sceneImage.src = currentVariation.image;
    scenarioTitle.innerText = `Caccia al Rischio: ${currentScenario.name}`;
    if (scenarioIntro) scenarioIntro.textContent = currentScenario.intro || '';
    risksList.innerHTML = '';
    if (explainBox) explainBox.classList.add('hide');
    sceneContainer.querySelectorAll('.hotspot').forEach(el => el.remove());
    totalRisksSpan.textContent = currentVariation.risks.length;
    currentVariation.risks.forEach(risk => {
      const listItem = document.createElement('li');
      listItem.id = `li-${risk.id}`;
      listItem.textContent = risk.name;
      risksList.appendChild(listItem);
      const hotspot = document.createElement('button');
      hotspot.type = 'button';
      hotspot.classList.add('hotspot');
      hotspot.id = `hotspot-${risk.id}`;
      hotspot.setAttribute('aria-label', `Pericolo: ${risk.name}`);
      hotspot.style.top = `${risk.top}%`;
      hotspot.style.left = `${risk.left}%`;
      hotspot.style.width = `${risk.size}%`;
      hotspot.style.height = `${risk.size}%`;
      hotspot.addEventListener('click', () => foundRisk(risk));
      sceneContainer.appendChild(hotspot);
    });
  }

  function foundRisk(risk){
    const listItem = document.getElementById(`li-${risk.id}`);
    const hotspot = document.getElementById(`hotspot-${risk.id}`);
    if (!listItem.classList.contains('found')) {
      listItem.classList.add('found');
      hotspot.classList.add('found');
      foundCount++;

      // Mostra spiegazione PC del rischio
      if (explainBox && risk.explain) {
        explainTitle.textContent = `${risk.name} — perche conta per la PC`;
        explainBody.textContent = risk.explain;
        explainBox.classList.remove('hide');
      }
    }
    if (foundCount === currentVariation.risks.length) {
      setTimeout(() => {
        winScreen.classList.remove('hide');
        if (window.GiochiUtil) {
          window.GiochiUtil.salvaEMostraAttestato(
            'caccia-al-rischio',
            currentVariation.risks.length,
            currentVariation.risks.length,
            '#win-screen .win-box'
          );
        }
      }, 1500);
    }
  }

  if (restartButton) {
    restartButton.addEventListener('click', () => {
      winScreen.classList.add('hide');
      // estrai una variation diversa (se ce ne sono >1)
      const variations = currentScenario.variations;
      if (variations.length > 1) {
        let newVar;
        do { newVar = variations[Math.floor(Math.random() * variations.length)]; }
        while (newVar === currentVariation && variations.length > 1);
        currentVariation = newVar;
      }
      initializeGame();
    });
  }

  if (backToSelectionButton) {
    backToSelectionButton.addEventListener('click', (e) => {
      e.preventDefault();
      showSelectionScreen();
    });
  }

  if (selectionScreen) showSelectionScreen();
});
