document.addEventListener('DOMContentLoaded', () => {
    const startScreen = document.getElementById('start-screen');
    const quizScreen = document.getElementById('quiz-screen');
    const resultsScreen = document.getElementById('results-screen');
    const startButton = document.getElementById('start-btn');
    const restartButton = document.getElementById('restart-btn');
    const questionElement = document.getElementById('question');
    const answerButtonsElement = document.getElementById('answer-buttons');
    const scoreElement = document.getElementById('score');
    const totalQuestionsElement = document.getElementById('total-questions');
    const feedbackMessageElement = document.getElementById('feedback-message');
    const feedbackBox = document.getElementById('feedback-box');
    const progressFill = document.getElementById('progress-fill');
    const currentQSpan = document.getElementById('current-q');
    const totalQSpan = document.getElementById('total-q');
    const scoreLive = document.getElementById('score-live');
    const categorySelector = document.getElementById('category-selector');

    let shuffledQuestions, currentQuestionIndex, score, selectedCount;

    // Definizione categorie con icone e colori
    const categories = [
        { id: 'terremoto', name: 'Terremoto', icon: 'bi-house-exclamation' },
        { id: 'incendio', name: 'Incendio', icon: 'bi-fire' },
        { id: 'alluvione', name: 'Alluvione', icon: 'bi-cloud-rain-heavy' },
        { id: 'numeri', name: 'Numeri di emergenza', icon: 'bi-telephone' },
        { id: 'zaino', name: 'Zaino di emergenza', icon: 'bi-backpack2' },
        { id: 'evacuazione', name: 'Evacuazione scuola', icon: 'bi-door-open' },
        { id: 'protezione-civile', name: 'Protezione Civile', icon: 'bi-shield-check' },
        { id: 'sicurezza', name: 'Sicurezza in casa', icon: 'bi-house-check' }
    ];

    const questions = [
        // ═══════════════════════════════════════
        // TERREMOTO (9 domande)
        // ═══════════════════════════════════════
        {
            category: 'terremoto',
            question: 'Cosa fai se senti una scossa di terremoto mentre sei in casa?',
            answers: [
                { text: 'Corro fuori in strada', correct: false },
                { text: 'Mi riparo sotto un tavolo robusto', correct: true },
                { text: 'Uso l\'ascensore per scendere', correct: false },
                { text: 'Mi affaccio alla finestra per vedere cosa succede', correct: false }
            ],
            explanation: 'Sotto un tavolo robusto sei protetto dalla caduta di oggetti. Non usare mai l\'ascensore durante un terremoto!'
        },
        {
            category: 'terremoto',
            question: 'Dopo una scossa di terremoto, quale uscita devi usare?',
            answers: [
                { text: 'L\'ascensore, per fare in fretta', correct: false },
                { text: 'La finestra al piano terra', correct: false },
                { text: 'Le scale, con calma e senza correre', correct: true },
                { text: 'Resto sempre dentro casa', correct: false }
            ],
            explanation: 'Le scale sono la via di uscita pi\u00f9 sicura. L\'ascensore potrebbe bloccarsi e la fretta pu\u00f2 causare cadute.'
        },
        {
            category: 'terremoto',
            question: 'Durante un terremoto a scuola, cosa fai?',
            answers: [
                { text: 'Scappo subito fuori dall\'aula', correct: false },
                { text: 'Mi nascondo sotto il banco e proteggo la testa', correct: true },
                { text: 'Mi metto vicino alla finestra', correct: false },
                { text: 'Chiamo i miei genitori al telefono', correct: false }
            ],
            explanation: 'Sotto il banco sei protetto da quello che pu\u00f2 cadere. Le finestre possono rompersi, stai lontano!'
        },
        {
            category: 'terremoto',
            question: 'Se sei al parco e senti una scossa di terremoto, dove vai?',
            answers: [
                { text: 'Sotto un albero grande', correct: false },
                { text: 'Vicino a un muro alto', correct: false },
                { text: 'In uno spazio aperto, lontano da edifici e alberi', correct: true },
                { text: 'Dentro il bar pi\u00f9 vicino', correct: false }
            ],
            explanation: 'In uno spazio aperto non rischi che ti cadano addosso muri, tegole o rami. Stai lontano da tutto quello che pu\u00f2 crollare!'
        },
        {
            category: 'terremoto',
            question: 'Cosa devi proteggere per prima cosa durante una scossa?',
            answers: [
                { text: 'Il telefono', correct: false },
                { text: 'Lo zaino di scuola', correct: false },
                { text: 'La testa e il collo', correct: true },
                { text: 'Le scarpe', correct: false }
            ],
            explanation: 'La testa \u00e8 la parte pi\u00f9 importante da proteggere. Usa le braccia, un cuscino o mettiti sotto qualcosa di solido!'
        },
        {
            category: 'terremoto',
            question: 'Dopo un terremoto, perch\u00e9 \u00e8 meglio indossare le scarpe prima di uscire?',
            answers: [
                { text: 'Per correre pi\u00f9 veloce', correct: false },
                { text: 'Perch\u00e9 per terra ci possono essere vetri rotti e calcinacci', correct: true },
                { text: 'Per non prendere freddo ai piedi', correct: false },
                { text: 'Non serve, si pu\u00f2 uscire scalzi', correct: false }
            ],
            explanation: 'Dopo una scossa per terra ci possono essere pezzi di vetro, tegole e mattoni. Le scarpe ti proteggono i piedi!'
        },
        {
            category: 'terremoto',
            question: 'Si pu\u00f2 prevedere quando arriva un terremoto?',
            answers: [
                { text: 'S\u00ec, i meteorologi lo annunciano in TV', correct: false },
                { text: 'S\u00ec, gli animali lo sentono sempre prima', correct: false },
                { text: 'No, i terremoti non si possono prevedere', correct: true },
                { text: 'S\u00ec, basta guardare le crepe nei muri', correct: false }
            ],
            explanation: 'Nessuno pu\u00f2 sapere in anticipo quando ci sar\u00e0 un terremoto. Per questo bisogna essere sempre preparati!'
        },
        {
            category: 'terremoto',
            question: 'Se durante un terremoto sei in auto con i tuoi genitori, cosa bisogna fare?',
            answers: [
                { text: 'Scendere subito e correre', correct: false },
                { text: 'Fermarsi lontano da ponti e edifici e restare in auto', correct: true },
                { text: 'Accelerare per fuggire', correct: false },
                { text: 'Suonare il clacson per chiedere aiuto', correct: false }
            ],
            explanation: 'In auto si \u00e8 abbastanza protetti. Bisogna fermarsi in un posto aperto e aspettare che la scossa finisca.'
        },
        {
            category: 'terremoto',
            question: 'Dopo il terremoto, puoi rientrare subito in casa?',
            answers: [
                { text: 'S\u00ec, per prendere i giocattoli', correct: false },
                { text: 'S\u00ec, se la porta si apre', correct: false },
                { text: 'No, bisogna aspettare che le autorit\u00e0 dicano che \u00e8 sicuro', correct: true },
                { text: 'S\u00ec, se non ci sono crepe visibili', correct: false }
            ],
            explanation: 'Anche se la casa sembra a posto, potrebbero esserci danni nascosti. Solo i tecnici possono dire se \u00e8 sicura!'
        },

        // ═══════════════════════════════════════
        // INCENDIO (9 domande)
        // ═══════════════════════════════════════
        {
            category: 'incendio',
            question: 'Se vedi un incendio in un bosco, cosa fai?',
            answers: [
                { text: 'Cerco di spegnerlo da solo', correct: false },
                { text: 'Chiamo subito il 112 o il 115', correct: true },
                { text: 'Faccio un video da postare', correct: false },
                { text: 'Non faccio niente, passer\u00e0 da solo', correct: false }
            ],
            explanation: 'Mai provare a spegnere un incendio da solo! Chiama subito il 112 e allontanati dal fuoco.'
        },
        {
            category: 'incendio',
            question: 'In caso di incendio in un edificio, cosa NON devi fare?',
            answers: [
                { text: 'Camminare carponi vicino al pavimento', correct: false },
                { text: 'Usare l\'ascensore per scendere pi\u00f9 veloce', correct: true },
                { text: 'Coprirmi naso e bocca con un panno bagnato', correct: false },
                { text: 'Seguire le indicazioni dell\'insegnante', correct: false }
            ],
            explanation: 'L\'ascensore pu\u00f2 bloccarsi e riempirsi di fumo. Usa sempre le scale e copri naso e bocca.'
        },
        {
            category: 'incendio',
            question: 'Perch\u00e9 durante un incendio bisogna stare bassi vicino al pavimento?',
            answers: [
                { text: 'Perch\u00e9 il pavimento \u00e8 pi\u00f9 fresco', correct: false },
                { text: 'Perch\u00e9 il fumo caldo sale verso l\'alto e in basso si respira meglio', correct: true },
                { text: 'Per non farsi vedere dalle fiamme', correct: false },
                { text: 'Perch\u00e9 \u00e8 pi\u00f9 facile correre', correct: false }
            ],
            explanation: 'Il fumo tossico sale verso l\'alto. Vicino al pavimento l\'aria \u00e8 pi\u00f9 pulita e puoi respirare meglio.'
        },
        {
            category: 'incendio',
            question: 'Cosa pu\u00f2 causare un incendio nel bosco?',
            answers: [
                { text: 'La pioggia', correct: false },
                { text: 'Un mozzicone di sigaretta gettato a terra', correct: true },
                { text: 'Il vento leggero', correct: false },
                { text: 'Gli uccelli', correct: false }
            ],
            explanation: 'Un piccolo mozzicone pu\u00f2 incendiare un intero bosco! Non si getta mai nulla per terra, soprattutto in estate.'
        },
        {
            category: 'incendio',
            question: 'Se vedi del fumo uscire da sotto la porta di una stanza, cosa fai?',
            answers: [
                { text: 'Apro la porta per vedere cosa succede', correct: false },
                { text: 'Non apro la porta e cerco un\'altra via di uscita', correct: true },
                { text: 'Butto acqua sotto la porta', correct: false },
                { text: 'Aspetto che il fumo passi', correct: false }
            ],
            explanation: 'Se apri la porta, le fiamme e il fumo possono entrare di colpo! Cerca un\'altra uscita e chiedi aiuto.'
        },
        {
            category: 'incendio',
            question: 'A cosa serve l\'estintore che vedi a scuola?',
            answers: [
                { text: '\u00c8 un giocattolo rosso per decorare il corridoio', correct: false },
                { text: 'Serve a spegnere un piccolo fuoco appena iniziato', correct: true },
                { text: 'Serve a fare il ghiaccio', correct: false },
                { text: 'Si usa per pulire i pavimenti', correct: false }
            ],
            explanation: 'L\'estintore serve a spegnere un fuoco piccolo. Solo gli adulti addestrati devono usarlo. Tu devi allontanarti e dare l\'allarme!'
        },
        {
            category: 'incendio',
            question: 'In estate, perch\u00e9 \u00e8 vietato accendere fuochi vicino al bosco?',
            answers: [
                { text: 'Perch\u00e9 fa troppo caldo per il fuoco', correct: false },
                { text: 'Perch\u00e9 la vegetazione secca prende fuoco facilmente', correct: true },
                { text: 'Perch\u00e9 si disturbano gli animali', correct: false },
                { text: 'Non \u00e8 vietato, si pu\u00f2 fare se si sta attenti', correct: false }
            ],
            explanation: 'In estate piove poco e le foglie secche prendono fuoco con una sola scintilla. Basta pochissimo per un disastro!'
        },
        {
            category: 'incendio',
            question: 'Se i tuoi vestiti prendono fuoco, cosa devi fare?',
            answers: [
                { text: 'Correre velocissimo', correct: false },
                { text: 'Fermarmi, buttarmi a terra e rotolarmi', correct: true },
                { text: 'Togliere i vestiti tirando forte', correct: false },
                { text: 'Saltare su e gi\u00f9', correct: false }
            ],
            explanation: 'Fermati, buttati a terra e rotola: cos\u00ec soffochi le fiamme. Correre fa entrare pi\u00f9 aria e il fuoco aumenta!'
        },
        {
            category: 'incendio',
            question: 'Dove si trova il numero dei Vigili del Fuoco?',
            answers: [
                { text: 'Non esiste un numero apposito', correct: false },
                { text: 'Si chiama il 115 oppure il 112', correct: true },
                { text: 'Si cerca su Internet durante l\'emergenza', correct: false },
                { text: 'Bisogna andare di persona alla caserma', correct: false }
            ],
            explanation: 'I Vigili del Fuoco si chiamano al 115. In ogni emergenza puoi anche chiamare il 112, il numero unico europeo.'
        },

        // ═══════════════════════════════════════
        // ALLUVIONE (8 domande)
        // ═══════════════════════════════════════
        {
            category: 'alluvione',
            question: 'Se piove molto forte e l\'acqua sale in strada, cosa fai?',
            answers: [
                { text: 'Esco a giocare con l\'acqua', correct: false },
                { text: 'Scendo in cantina a controllare', correct: false },
                { text: 'Vado ai piani alti e resto lontano dall\'acqua', correct: true },
                { text: 'Attraverso la strada allagata a piedi', correct: false }
            ],
            explanation: 'I piani alti sono il posto pi\u00f9 sicuro. L\'acqua pu\u00f2 essere pericolosa anche se sembra bassa!'
        },
        {
            category: 'alluvione',
            question: 'Durante un\'alluvione, perch\u00e9 non bisogna scendere in cantina?',
            answers: [
                { text: 'Perch\u00e9 \u00e8 buio', correct: false },
                { text: 'Perch\u00e9 l\'acqua pu\u00f2 riempirla velocemente e restare intrappolati', correct: true },
                { text: 'Perch\u00e9 c\'\u00e8 troppo disordine', correct: false },
                { text: 'Perch\u00e9 fa freddo', correct: false }
            ],
            explanation: 'La cantina \u00e8 il primo posto che si riempie d\'acqua. Si rischia di restare intrappolati senza via di uscita.'
        },
        {
            category: 'alluvione',
            question: 'Perch\u00e9 non si deve attraversare una strada allagata a piedi?',
            answers: [
                { text: 'Perch\u00e9 ci si bagnano le scarpe', correct: false },
                { text: 'Perch\u00e9 sotto l\'acqua possono esserci buche, tombini aperti o correnti forti', correct: true },
                { text: 'Perch\u00e9 l\'acqua \u00e8 sporca', correct: false },
                { text: 'Si pu\u00f2 attraversare se l\'acqua \u00e8 bassa', correct: false }
            ],
            explanation: 'Anche pochi centimetri d\'acqua possono nascondere pericoli. Non sai cosa c\'\u00e8 sotto e la corrente ti pu\u00f2 trascinare!'
        },
        {
            category: 'alluvione',
            question: 'Se sei in auto e trovi un sottopassaggio pieno d\'acqua, cosa fai?',
            answers: [
                { text: 'Passo veloce cos\u00ec non mi fermo', correct: false },
                { text: 'Mi fermo e torno indietro, cerco un\'altra strada', correct: true },
                { text: 'Aspetto che l\'acqua si abbassi', correct: false },
                { text: 'Passo piano piano', correct: false }
            ],
            explanation: 'Nei sottopassaggi l\'acqua pu\u00f2 essere molto pi\u00f9 profonda di quanto sembra. L\'auto si pu\u00f2 bloccare e rimanere sommersa!'
        },
        {
            category: 'alluvione',
            question: 'Cosa significa allerta arancione per rischio idrogeologico?',
            answers: [
                { text: 'Che fa caldo', correct: false },
                { text: 'Che ci sar\u00e0 il sole', correct: false },
                { text: 'Che sono previste piogge molto forti e bisogna fare attenzione', correct: true },
                { text: 'Che si pu\u00f2 uscire normalmente', correct: false }
            ],
            explanation: 'Allerta arancione significa che possono arrivare piogge intense con rischio di allagamenti e frane. Meglio stare al sicuro!'
        },
        {
            category: 'alluvione',
            question: 'Dopo un\'alluvione, si pu\u00f2 bere l\'acqua del rubinetto?',
            answers: [
                { text: 'S\u00ec, sempre', correct: false },
                { text: 'Solo se \u00e8 calda', correct: false },
                { text: 'No, finch\u00e9 le autorit\u00e0 non dicono che \u00e8 sicura', correct: true },
                { text: 'S\u00ec, basta farla bollire', correct: false }
            ],
            explanation: 'L\'acqua del rubinetto potrebbe essere inquinata. Aspetta sempre che le autorit\u00e0 dicano che si pu\u00f2 bere!'
        },
        {
            category: 'alluvione',
            question: 'Cosa \u00e8 una frana?',
            answers: [
                { text: 'Un forte vento che soffia dalla montagna', correct: false },
                { text: 'Una massa di terra e rocce che scivola lungo un pendio', correct: true },
                { text: 'Un tipo di terremoto', correct: false },
                { text: 'Un fiume che straripa', correct: false }
            ],
            explanation: 'Una frana \u00e8 quando la terra di un pendio si stacca e scende verso il basso, portando con s\u00e9 tutto quello che incontra.'
        },
        {
            category: 'alluvione',
            question: 'Dove bisogna andare se la propria casa rischia di essere allagata?',
            answers: [
                { text: 'In cantina', correct: false },
                { text: 'In garage', correct: false },
                { text: 'Ai piani alti o in un luogo sicuro indicato dal Comune', correct: true },
                { text: 'Sul tetto', correct: false }
            ],
            explanation: 'I piani alti sono pi\u00f9 sicuri. Il Comune indica anche le aree di raccolta dove andare in caso di evacuazione.'
        },

        // ═══════════════════════════════════════
        // NUMERI DI EMERGENZA (8 domande)
        // ═══════════════════════════════════════
        {
            category: 'numeri',
            question: 'Qual \u00e8 il numero unico di emergenza da chiamare in Italia?',
            answers: [
                { text: '118', correct: false },
                { text: '115', correct: false },
                { text: '112', correct: true },
                { text: '113', correct: false }
            ],
            explanation: 'Il 112 \u00e8 il numero unico di emergenza. Funziona per tutte le emergenze: polizia, ambulanza e vigili del fuoco.'
        },
        {
            category: 'numeri',
            question: 'Quando chiami il 112, cosa devi dire?',
            answers: [
                { text: 'Solo il mio nome', correct: false },
                { text: 'Cosa \u00e8 successo, dove mi trovo e quante persone hanno bisogno di aiuto', correct: true },
                { text: 'Devo solo urlare "aiuto"', correct: false },
                { text: 'Non devo dire niente, loro sanno gi\u00e0 tutto', correct: false }
            ],
            explanation: 'Quando chiami il 112, parla con calma e spiega cosa \u00e8 successo, dove ti trovi e se qualcuno ha bisogno di aiuto.'
        },
        {
            category: 'numeri',
            question: 'Quale numero chiami per segnalare un incendio nel bosco?',
            answers: [
                { text: '118', correct: false },
                { text: '1515', correct: true },
                { text: '113', correct: false },
                { text: '117', correct: false }
            ],
            explanation: 'Il 1515 \u00e8 il numero per gli incendi boschivi. Puoi anche chiamare il 112 o il 115 (Vigili del Fuoco).'
        },
        {
            category: 'numeri',
            question: 'Il 112 funziona anche se non hai credito sul telefono?',
            answers: [
                { text: 'No, serve credito', correct: false },
                { text: 'S\u00ec, il 112 \u00e8 sempre gratuito e funziona anche senza credito', correct: true },
                { text: 'Solo con i telefoni fissi', correct: false },
                { text: 'Funziona solo di giorno', correct: false }
            ],
            explanation: 'Il 112 \u00e8 gratuito e funziona sempre: senza credito, senza SIM e da qualsiasi telefono, anche da quello di un amico!'
        },
        {
            category: 'numeri',
            question: 'Quale numero chiami se qualcuno si sente molto male?',
            answers: [
                { text: '115', correct: false },
                { text: '117', correct: false },
                { text: '118 oppure il 112', correct: true },
                { text: '1515', correct: false }
            ],
            explanation: 'Il 118 \u00e8 il numero dell\'emergenza sanitaria: manda l\'ambulanza. Puoi anche chiamare il 112, che smista la chiamata.'
        },
        {
            category: 'numeri',
            question: '\u00c8 giusto chiamare il 112 per scherzo?',
            answers: [
                { text: 'S\u00ec, tanto non succede niente', correct: false },
                { text: 'S\u00ec, per fare una prova', correct: false },
                { text: 'No, perch\u00e9 si occupano le linee e chi ha davvero bisogno potrebbe non riuscire a chiamare', correct: true },
                { text: 'Solo se lo faccio una volta sola', correct: false }
            ],
            explanation: 'Chiamare per scherzo \u00e8 un reato! Ogni chiamata falsa toglie tempo e risorse a chi ha davvero bisogno di aiuto.'
        },
        {
            category: 'numeri',
            question: 'Il numero 112 funziona in tutta Europa?',
            answers: [
                { text: 'No, solo in Italia', correct: false },
                { text: 'S\u00ec, \u00e8 il numero di emergenza in tutta Europa', correct: true },
                { text: 'Solo in Italia e Francia', correct: false },
                { text: 'Solo se hai una SIM europea', correct: false }
            ],
            explanation: 'Il 112 \u00e8 il numero unico europeo. Se sei in vacanza in un altro Paese, puoi sempre chiamare il 112!'
        },
        {
            category: 'numeri',
            question: 'Se ti perdi in un luogo che non conosci, chi chiami?',
            answers: [
                { text: 'Nessuno, cerco da solo la strada', correct: false },
                { text: 'I miei genitori o, se non rispondono, il 112', correct: true },
                { text: 'Un amico per farmi compagnia al telefono', correct: false },
                { text: 'Il pizzaiolo', correct: false }
            ],
            explanation: 'Prima chiama un adulto di fiducia. Se non riesci a raggiungerlo, il 112 pu\u00f2 aiutarti a farti trovare.'
        },

        // ═══════════════════════════════════════
        // ZAINO DI EMERGENZA (8 domande)
        // ═══════════════════════════════════════
        {
            category: 'zaino',
            question: 'Cosa non deve mancare in uno zaino di emergenza?',
            answers: [
                { text: 'Videogiochi e caricabatterie', correct: false },
                { text: 'Album di figurine', correct: false },
                { text: 'Torcia, acqua e un fischietto', correct: true },
                { text: 'Libri di scuola', correct: false }
            ],
            explanation: 'La torcia serve per vedere al buio, l\'acqua per bere e il fischietto per farti sentire dai soccorritori.'
        },
        {
            category: 'zaino',
            question: 'Perch\u00e9 nello zaino di emergenza serve un fischietto?',
            answers: [
                { text: 'Per giocare', correct: false },
                { text: 'Per farsi sentire dai soccorritori se si \u00e8 bloccati', correct: true },
                { text: 'Per spaventare gli animali', correct: false },
                { text: 'Per chiamare gli amici', correct: false }
            ],
            explanation: 'Il fischietto si sente molto lontano e non ti fa stancare la voce. I soccorritori lo cercano!'
        },
        {
            category: 'zaino',
            question: 'Dove bisogna tenere lo zaino di emergenza?',
            answers: [
                { text: 'In cantina, nascosto', correct: false },
                { text: 'Nella macchina', correct: false },
                { text: 'Vicino alla porta di casa, facile da prendere', correct: true },
                { text: 'A scuola', correct: false }
            ],
            explanation: 'Lo zaino deve essere facile da prendere e pronto: vicino alla porta o in corridoio. In emergenza non c\'\u00e8 tempo di cercarlo!'
        },
        {
            category: 'zaino',
            question: 'Perch\u00e9 nello zaino di emergenza serve una radio a pile?',
            answers: [
                { text: 'Per ascoltare la musica', correct: false },
                { text: 'Per ricevere le informazioni ufficiali anche se manca la corrente', correct: true },
                { text: 'Per parlare con i vicini', correct: false },
                { text: 'Non serve, basta il telefono', correct: false }
            ],
            explanation: 'Se manca la corrente e il telefono non ha batteria, la radio a pile funziona sempre e ti permette di ascoltare le notizie!'
        },
        {
            category: 'zaino',
            question: 'Ogni quanto bisogna controllare lo zaino di emergenza?',
            answers: [
                { text: 'Mai, una volta preparato va bene per sempre', correct: false },
                { text: 'Almeno due volte l\'anno, per verificare scadenze e pile', correct: true },
                { text: 'Solo quando c\'\u00e8 un\'emergenza', correct: false },
                { text: 'Ogni giorno', correct: false }
            ],
            explanation: 'L\'acqua scade, le pile si scaricano e i medicinali possono scadere. Controlla tutto almeno due volte l\'anno!'
        },
        {
            category: 'zaino',
            question: 'Nello zaino di emergenza servono anche i documenti?',
            answers: [
                { text: 'No, non servono a niente', correct: false },
                { text: 'S\u00ec, una copia dei documenti della famiglia', correct: true },
                { text: 'Solo la tessera della biblioteca', correct: false },
                { text: 'Solo la tessera del supermercato', correct: false }
            ],
            explanation: 'Una copia dei documenti \u00e8 importante per farsi identificare, ricevere aiuto e dimostrare chi sei durante l\'emergenza.'
        },
        {
            category: 'zaino',
            question: 'Quale tipo di scarpe bisogna avere pronte nello zaino?',
            answers: [
                { text: 'Ciabatte da spiaggia', correct: false },
                { text: 'Scarpe chiuse e robuste', correct: true },
                { text: 'Scarpe con i tacchi', correct: false },
                { text: 'Non servono scarpe', correct: false }
            ],
            explanation: 'Dopo un\'emergenza per terra possono esserci vetri, macerie e fango. Le scarpe chiuse proteggono i piedi!'
        },
        {
            category: 'zaino',
            question: 'Se hai un animale domestico, cosa devi aggiungere allo zaino?',
            answers: [
                { text: 'I suoi giocattoli preferiti', correct: false },
                { text: 'Cibo, acqua e il suo libretto sanitario', correct: true },
                { text: 'Niente, gli animali si arrangiano', correct: false },
                { text: 'Solo il guinzaglio', correct: false }
            ],
            explanation: 'Anche il tuo animale ha bisogno di cibo, acqua e documenti. Non dimenticarlo nello zaino di emergenza!'
        },

        // ═══════════════════════════════════════
        // EVACUAZIONE SCUOLA (8 domande)
        // ═══════════════════════════════════════
        {
            category: 'evacuazione',
            question: 'Quando suona l\'allarme di evacuazione a scuola, cosa fai?',
            answers: [
                { text: 'Prendo tutte le mie cose dallo zaino', correct: false },
                { text: 'Mi metto in fila e seguo l\'insegnante verso il punto di raccolta', correct: true },
                { text: 'Corro il pi\u00f9 veloce possibile verso l\'uscita', correct: false },
                { text: 'Aspetto che i miei genitori vengano a prendermi', correct: false }
            ],
            explanation: 'Segui l\'insegnante in fila ordinata. Non portare le cose e non correre: la calma salva la vita!'
        },
        {
            category: 'evacuazione',
            question: 'A cosa serve il punto di raccolta della scuola?',
            answers: [
                { text: '\u00c8 il posto dove si gioca durante l\'intervallo', correct: false },
                { text: '\u00c8 il luogo sicuro dove ritrovarsi per controllare che ci siano tutti', correct: true },
                { text: '\u00c8 dove si parcheggia', correct: false },
                { text: '\u00c8 il posto dove aspettare l\'autobus', correct: false }
            ],
            explanation: 'Al punto di raccolta l\'insegnante fa l\'appello per verificare che nessuno manchi. \u00c8 un posto sicuro!'
        },
        {
            category: 'evacuazione',
            question: 'Chi guida la fila durante l\'evacuazione a scuola?',
            answers: [
                { text: 'Il pi\u00f9 veloce della classe', correct: false },
                { text: 'L\'aprifila, un compagno scelto dall\'insegnante', correct: true },
                { text: 'Il rappresentante di classe', correct: false },
                { text: 'Ognuno va per conto suo', correct: false }
            ],
            explanation: 'In ogni classe c\'\u00e8 un aprifila che guida i compagni e un chiudifila che si assicura che nessuno resti indietro.'
        },
        {
            category: 'evacuazione',
            question: 'Durante l\'evacuazione, perch\u00e9 non devi correre?',
            answers: [
                { text: 'Perch\u00e9 l\'insegnante si arrabbia', correct: false },
                { text: 'Perch\u00e9 correndo si pu\u00f2 cadere, fare cadere gli altri e creare panico', correct: true },
                { text: 'Perch\u00e9 si suda', correct: false },
                { text: 'Si pu\u00f2 correre se si ha paura', correct: false }
            ],
            explanation: 'Camminare spediti ma senza correre evita cadute e panico. Quando tutti restano calmi, si esce pi\u00f9 in fretta!'
        },
        {
            category: 'evacuazione',
            question: 'Se durante l\'evacuazione un compagno cade, cosa fai?',
            answers: [
                { text: 'Lo scavalco e continuo', correct: false },
                { text: 'Lo aiuto ad alzarsi e avviso l\'insegnante', correct: true },
                { text: 'Mi fermo e aspetto', correct: false },
                { text: 'Torno in classe', correct: false }
            ],
            explanation: 'Aiutare un compagno in difficolt\u00e0 \u00e8 importante, ma senza bloccare la fila. Avvisa subito l\'insegnante!'
        },
        {
            category: 'evacuazione',
            question: 'Perch\u00e9 a scuola si fanno le prove di evacuazione?',
            answers: [
                { text: 'Per perdere un\'ora di lezione', correct: false },
                { text: 'Per imparare cosa fare in caso di emergenza vera', correct: true },
                { text: 'Perch\u00e9 il preside lo ordina per divertimento', correct: false },
                { text: 'Per fare ginnastica', correct: false }
            ],
            explanation: 'Le prove servono a imparare il percorso e i comportamenti corretti. Cos\u00ec, se succede davvero, sai gi\u00e0 cosa fare!'
        },
        {
            category: 'evacuazione',
            question: 'Se sei in bagno quando suona l\'allarme di evacuazione, cosa fai?',
            answers: [
                { text: 'Resto in bagno ad aspettare', correct: false },
                { text: 'Torno in classe a prendere le cose', correct: false },
                { text: 'Esco subito e raggiungo il punto di raccolta o la classe pi\u00f9 vicina', correct: true },
                { text: 'Chiamo i miei genitori', correct: false }
            ],
            explanation: 'Se sei fuori dalla classe, raggiungi il punto di raccolta o unisciti alla fila pi\u00f9 vicina. L\'importante \u00e8 farsi trovare!'
        },
        {
            category: 'evacuazione',
            question: 'Cosa NON devi portare con te durante l\'evacuazione?',
            answers: [
                { text: 'Me stesso', correct: false },
                { text: 'Lo zaino pesante, i libri e gli oggetti ingombranti', correct: true },
                { text: 'Il giubbotto se fa freddo', correct: false },
                { text: 'Un compagno in difficolt\u00e0', correct: false }
            ],
            explanation: 'Zaini e oggetti rallentano la fila e possono far inciampare. Lascia tutto in classe e pensa solo a uscire in sicurezza!'
        },

        // ═══════════════════════════════════════
        // PROTEZIONE CIVILE (8 domande)
        // ═══════════════════════════════════════
        {
            category: 'protezione-civile',
            question: 'Chi sono i volontari di Protezione Civile?',
            answers: [
                { text: 'Persone che aiutano la comunit\u00e0 durante le emergenze, senza essere pagate', correct: true },
                { text: 'Soldati dell\'esercito', correct: false },
                { text: 'Dottori dell\'ospedale', correct: false },
                { text: 'Vigili urbani', correct: false }
            ],
            explanation: 'I volontari sono persone comuni che dedicano il loro tempo libero per aiutare gli altri durante le emergenze.'
        },
        {
            category: 'protezione-civile',
            question: 'Cosa significa il colore arancione in un\'allerta meteo?',
            answers: [
                { text: 'Tutto tranquillo, nessun pericolo', correct: false },
                { text: 'Fenomeni intensi: bisogna fare molta attenzione', correct: true },
                { text: 'Si pu\u00f2 uscire a giocare', correct: false },
                { text: '\u00c8 solo un consiglio, non \u00e8 importante', correct: false }
            ],
            explanation: 'Arancione significa attenzione! Possono arrivare piogge forti o vento. Meglio restare al sicuro.'
        },
        {
            category: 'protezione-civile',
            question: 'Cosa significa "prevenzione" nella Protezione Civile?',
            answers: [
                { text: 'Aspettare che succeda qualcosa e poi intervenire', correct: false },
                { text: 'Prepararsi prima che arrivi un\'emergenza per ridurre i danni', correct: true },
                { text: 'Prevedere il futuro', correct: false },
                { text: 'Costruire muri altissimi', correct: false }
            ],
            explanation: 'Prevenzione significa prepararsi in anticipo: conoscere i rischi, sapere cosa fare e avere tutto pronto. \u00c8 la cosa pi\u00f9 importante!'
        },
        {
            category: 'protezione-civile',
            question: 'Quale colore di allerta meteo indica il pericolo pi\u00f9 alto?',
            answers: [
                { text: 'Giallo', correct: false },
                { text: 'Verde', correct: false },
                { text: 'Arancione', correct: false },
                { text: 'Rosso', correct: true }
            ],
            explanation: 'Rosso \u00e8 il livello massimo: significa fenomeni molto forti e rischio elevato. Bisogna seguire tutte le indicazioni delle autorit\u00e0!'
        },
        {
            category: 'protezione-civile',
            question: 'Cosa fa la Protezione Civile quando non ci sono emergenze?',
            answers: [
                { text: 'Niente, aspetta che succeda qualcosa', correct: false },
                { text: 'Si allena, fa prevenzione, controlla il territorio e forma i volontari', correct: true },
                { text: 'Va in vacanza', correct: false },
                { text: 'Lavora solo in ufficio', correct: false }
            ],
            explanation: 'La Protezione Civile lavora soprattutto quando non ci sono emergenze: si prepara, fa esercitazioni e aiuta i cittadini a essere pronti.'
        },
        {
            category: 'protezione-civile',
            question: 'Allerta verde significa che:',
            answers: [
                { text: 'Bisogna stare a casa', correct: false },
                { text: 'Non ci sono pericoli particolari, situazione tranquilla', correct: true },
                { text: 'C\'\u00e8 un pericolo legato alla natura', correct: false },
                { text: 'Si deve andare al punto di raccolta', correct: false }
            ],
            explanation: 'Verde significa tutto tranquillo: nessuna allerta in corso. Ma ricorda: essere preparati \u00e8 sempre importante!'
        },
        {
            category: 'protezione-civile',
            question: 'Anche i bambini possono aiutare nella prevenzione?',
            answers: [
                { text: 'No, la prevenzione \u00e8 solo per gli adulti', correct: false },
                { text: 'S\u00ec, imparando le regole di sicurezza e aiutando la famiglia a prepararsi', correct: true },
                { text: 'Solo i bambini molto grandi', correct: false },
                { text: 'Solo se vanno a un corso speciale', correct: false }
            ],
            explanation: 'Certo che s\u00ec! Imparare i comportamenti corretti, preparare lo zaino di emergenza e conoscere i numeri da chiamare: anche tu fai prevenzione!'
        },
        {
            category: 'protezione-civile',
            question: 'Cos\'\u00e8 il Piano di Emergenza Comunale?',
            answers: [
                { text: 'Un piano per costruire case nuove', correct: false },
                { text: 'Un documento che spiega cosa fare e dove andare in caso di emergenza nel proprio Comune', correct: true },
                { text: 'Un elenco di ristoranti', correct: false },
                { text: 'Un programma televisivo', correct: false }
            ],
            explanation: 'Ogni Comune ha un Piano di Emergenza che indica le aree sicure, i percorsi di evacuazione e chi fa cosa in caso di emergenza.'
        },

        // ═══════════════════════════════════════
        // SICUREZZA IN CASA (8 domande)
        // ═══════════════════════════════════════
        {
            category: 'sicurezza',
            question: 'Se senti odore di gas in casa, cosa fai?',
            answers: [
                { text: 'Accendo la luce per vedere meglio', correct: false },
                { text: 'Apro le finestre, esco e chiamo un adulto', correct: true },
                { text: 'Cerco da dove viene con un accendino', correct: false },
                { text: 'Non faccio niente, \u00e8 normale', correct: false }
            ],
            explanation: 'Il gas \u00e8 pericoloso! Non toccare interruttori e non usare fiamme. Apri le finestre e chiama subito un adulto.'
        },
        {
            category: 'sicurezza',
            question: 'Perch\u00e9 \u00e8 importante conoscere le vie di fuga della propria scuola?',
            answers: [
                { text: 'Per correre pi\u00f9 veloci degli altri', correct: false },
                { text: 'Per sapere dove andare in caso di emergenza, senza perdere tempo', correct: true },
                { text: 'Per uscire prima durante l\'intervallo', correct: false },
                { text: 'Non \u00e8 importante, ci pensa l\'insegnante', correct: false }
            ],
            explanation: 'Se conosci la via di fuga, in emergenza sai subito dove andare. La preparazione \u00e8 la migliore protezione!'
        },
        {
            category: 'sicurezza',
            question: 'Se manca la corrente in casa, cosa usi per fare luce?',
            answers: [
                { text: 'Le candele', correct: false },
                { text: 'L\'accendino', correct: false },
                { text: 'Una torcia elettrica a pile', correct: true },
                { text: 'Il forno acceso', correct: false }
            ],
            explanation: 'La torcia \u00e8 sicura perch\u00e9 non ha fiamme. Candele e accendini possono causare incendi, soprattutto al buio!'
        },
        {
            category: 'sicurezza',
            question: 'Perch\u00e9 non si devono toccare le prese elettriche con le mani bagnate?',
            answers: [
                { text: 'Perch\u00e9 si sporcano le prese', correct: false },
                { text: 'Perch\u00e9 l\'acqua conduce l\'elettricit\u00e0 e si rischia una scossa', correct: true },
                { text: 'Perch\u00e9 si rompono', correct: false },
                { text: 'Si possono toccare, non \u00e8 pericoloso', correct: false }
            ],
            explanation: 'L\'acqua fa passare la corrente elettrica attraverso il corpo. \u00c8 molto pericoloso! Asciuga sempre bene le mani prima.'
        },
        {
            category: 'sicurezza',
            question: 'Dove si conservano i prodotti per la pulizia in modo sicuro?',
            answers: [
                { text: 'Sul tavolo della cucina', correct: false },
                { text: 'Vicino al cibo', correct: false },
                { text: 'In un mobile chiuso, lontano dalla portata dei bambini', correct: true },
                { text: 'In camera da letto', correct: false }
            ],
            explanation: 'I prodotti per la pulizia sono velenosi. Devono stare in un mobile chiuso a chiave o in alto dove i bambini non arrivano.'
        },
        {
            category: 'sicurezza',
            question: 'Se sei da solo in casa e qualcuno bussa alla porta, cosa fai?',
            answers: [
                { text: 'Apro subito', correct: false },
                { text: 'Guardo dallo spioncino e se non conosco la persona non apro', correct: true },
                { text: 'Apro un po\' per vedere chi \u00e8', correct: false },
                { text: 'Grido "chi \u00e8?" e poi apro', correct: false }
            ],
            explanation: 'Non aprire mai la porta a sconosciuti quando sei solo! Guarda dallo spioncino e, se hai dubbi, chiama un adulto di fiducia.'
        },
        {
            category: 'sicurezza',
            question: 'Perch\u00e9 \u00e8 importante che tutti in famiglia sappiano dove si chiude il gas?',
            answers: [
                { text: 'Per risparmiare sulla bolletta', correct: false },
                { text: 'Per chiuderlo subito in caso di fuga di gas o terremoto', correct: true },
                { text: 'Per pulire il tubo del gas', correct: false },
                { text: 'Non \u00e8 importante, ci pensa il tecnico', correct: false }
            ],
            explanation: 'Se senti odore di gas o c\'\u00e8 un terremoto, chiudere subito il rubinetto del gas pu\u00f2 evitare esplosioni e incendi.'
        },
        {
            category: 'sicurezza',
            question: 'Qual \u00e8 il posto pi\u00f9 sicuro dove ripararsi in casa durante un temporale con fulmini?',
            answers: [
                { text: 'Vicino alla finestra per guardare', correct: false },
                { text: 'In balcone sotto la tettoia', correct: false },
                { text: 'Al centro della stanza, lontano da finestre e apparecchi elettrici', correct: true },
                { text: 'Nella vasca da bagno', correct: false }
            ],
            explanation: 'I fulmini possono colpire gli apparecchi collegati alla corrente e le finestre. Stai al centro della stanza, al sicuro!'
        }
    ];

    // Fisher-Yates shuffle
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    // Genera i pulsanti delle categorie
    let selectedCategories = new Set(categories.map(c => c.id));

    function renderCategoryButtons() {
        categorySelector.innerHTML = '';
        // Pulsante "Tutti"
        const allBtn = document.createElement('button');
        allBtn.className = 'btn btn-sm category-toggle-btn' + (selectedCategories.size === categories.length ? ' active' : '');
        allBtn.innerHTML = '<i class="bi bi-check2-all me-1" aria-hidden="true"></i> Tutti';
        allBtn.addEventListener('click', () => {
            if (selectedCategories.size === categories.length) {
                selectedCategories.clear();
            } else {
                selectedCategories = new Set(categories.map(c => c.id));
            }
            renderCategoryButtons();
        });
        categorySelector.appendChild(allBtn);

        categories.forEach(cat => {
            const btn = document.createElement('button');
            const isActive = selectedCategories.has(cat.id);
            btn.className = 'btn btn-sm category-toggle-btn' + (isActive ? ' active' : '');
            btn.innerHTML = '<i class="bi ' + cat.icon + ' me-1" aria-hidden="true"></i> ' + cat.name;
            btn.setAttribute('aria-pressed', isActive);
            btn.addEventListener('click', () => {
                if (selectedCategories.has(cat.id)) {
                    selectedCategories.delete(cat.id);
                } else {
                    selectedCategories.add(cat.id);
                }
                renderCategoryButtons();
            });
            categorySelector.appendChild(btn);
        });

        // Aggiorna il conteggio domande disponibili
        const available = questions.filter(q => selectedCategories.has(q.category)).length;
        startButton.disabled = available === 0;
        if (available === 0) {
            startButton.textContent = 'Scegli almeno un argomento';
        } else {
            startButton.innerHTML = '<i class="bi bi-play-fill me-1" aria-hidden="true"></i> Inizia il Quiz! (' + available + ' domande disponibili)';
        }
    }

    renderCategoryButtons();

    // Selettore numero domande
    const countButtons = document.querySelectorAll('.question-count-selector .btn');
    selectedCount = 'all';
    countButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            countButtons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-checked', 'false'); });
            btn.classList.add('active');
            btn.setAttribute('aria-checked', 'true');
            selectedCount = btn.dataset.count;
        });
    });

    function startGame() {
        startScreen.classList.add('hide');
        resultsScreen.classList.add('hide');
        quizScreen.classList.remove('hide');

        let pool = shuffle([...questions.filter(q => selectedCategories.has(q.category))]);
        if (selectedCount !== 'all') {
            const count = parseInt(selectedCount, 10);
            pool = pool.slice(0, Math.min(count, pool.length));
        }
        shuffledQuestions = pool;
        currentQuestionIndex = 0;
        score = 0;
        totalQSpan.textContent = shuffledQuestions.length;
        updateProgress();
        setNextQuestion();
    }

    function updateProgress() {
        currentQSpan.textContent = currentQuestionIndex + 1;
        const pct = (currentQuestionIndex / shuffledQuestions.length) * 100;
        progressFill.style.width = pct + '%';
        scoreLive.textContent = score + ' corrette';
    }

    function setNextQuestion() {
        resetState();
        showQuestion(shuffledQuestions[currentQuestionIndex]);
        updateProgress();
    }

    function showQuestion(question) {
        questionElement.innerText = question.question;
        const shuffledAnswers = shuffle([...question.answers]);
        shuffledAnswers.forEach(answer => {
            const button = document.createElement('button');
            button.innerText = answer.text;
            button.classList.add('btn');
            if (answer.correct) { button.dataset.correct = answer.correct; }
            button.addEventListener('click', selectAnswer);
            answerButtonsElement.appendChild(button);
        });
    }

    function selectAnswer(e) {
        const selectedButton = e.target;
        const correct = selectedButton.dataset.correct === 'true';
        const currentQ = shuffledQuestions[currentQuestionIndex];

        if (correct) { score++; }

        Array.from(answerButtonsElement.children).forEach(button => {
            setStatusClass(button, button.dataset.correct === 'true');
            button.disabled = true;
        });

        feedbackBox.classList.remove('hide', 'correct', 'wrong');
        if (correct) {
            feedbackBox.classList.add('correct');
            feedbackBox.innerHTML = '<div class="feedback-title">Risposta esatta!</div>' + currentQ.explanation;
        } else {
            feedbackBox.classList.add('wrong');
            feedbackBox.innerHTML = '<div class="feedback-title">Risposta sbagliata</div>' + currentQ.explanation;
        }

        scoreLive.textContent = score + ' corrette';

        setTimeout(() => {
            currentQuestionIndex++;
            if (currentQuestionIndex < shuffledQuestions.length) {
                setNextQuestion();
            } else {
                showResults();
            }
        }, 3000);
    }

    function showResults() {
        quizScreen.classList.add('hide');
        resultsScreen.classList.remove('hide');
        scoreElement.innerText = score;
        totalQuestionsElement.innerText = shuffledQuestions.length;
        const percentage = (score / shuffledQuestions.length) * 100;
        if (percentage >= 90) { feedbackMessageElement.innerText = "Fantastico! Sei un vero esperto di sicurezza!"; }
        else if (percentage >= 70) { feedbackMessageElement.innerText = "Molto bravo! Conosci bene le regole di sicurezza."; }
        else if (percentage >= 50) { feedbackMessageElement.innerText = "Non male! Riprova per imparare ancora di pi\u00f9."; }
        else { feedbackMessageElement.innerText = "Puoi fare di meglio! Rileggi i consigli e riprova il quiz."; }
    }

    function resetState() {
        feedbackBox.classList.add('hide');
        while (answerButtonsElement.firstChild) { answerButtonsElement.removeChild(answerButtonsElement.firstChild); }
    }

    function setStatusClass(element, correct) {
        if (correct) { element.classList.add('correct'); } else { element.classList.add('wrong'); }
    }

    startButton.addEventListener('click', startGame);
    restartButton.addEventListener('click', () => {
        resultsScreen.classList.add('hide');
        startScreen.classList.remove('hide');
    });
});
