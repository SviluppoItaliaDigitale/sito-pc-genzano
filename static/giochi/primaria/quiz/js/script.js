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
        { id: 'sicurezza', name: 'Sicurezza in casa', icon: 'bi-house-check' },
        { id: 'comunicazione', name: 'Fonti ufficiali e IT-alert', icon: 'bi-broadcast' }
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
            explanation: 'Le scale sono la via di uscita più sicura. L\'ascensore potrebbe bloccarsi e la fretta può causare cadute.'
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
            explanation: 'Sotto il banco sei protetto da quello che può cadere. Le finestre possono rompersi, stai lontano!'
        },
        {
            category: 'terremoto',
            question: 'Se sei al parco e senti una scossa di terremoto, dove vai?',
            answers: [
                { text: 'Sotto un albero grande', correct: false },
                { text: 'Vicino a un muro alto', correct: false },
                { text: 'In uno spazio aperto, lontano da edifici e alberi', correct: true },
                { text: 'Dentro il bar più vicino', correct: false }
            ],
            explanation: 'In uno spazio aperto non rischi che ti cadano addosso muri, tegole o rami. Stai lontano da tutto quello che può crollare!'
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
            explanation: 'La testa è la parte più importante da proteggere. Usa le braccia, un cuscino o mettiti sotto qualcosa di solido!'
        },
        {
            category: 'terremoto',
            question: 'Dopo un terremoto, perché è meglio indossare le scarpe prima di uscire?',
            answers: [
                { text: 'Per correre più veloce', correct: false },
                { text: 'Perché per terra ci possono essere vetri rotti e calcinacci', correct: true },
                { text: 'Per non prendere freddo ai piedi', correct: false },
                { text: 'Non serve, si può uscire scalzi', correct: false }
            ],
            explanation: 'Dopo una scossa per terra ci possono essere pezzi di vetro, tegole e mattoni. Le scarpe ti proteggono i piedi!'
        },
        {
            category: 'terremoto',
            question: 'Si può prevedere quando arriva un terremoto?',
            answers: [
                { text: 'Sì, i meteorologi lo annunciano in TV', correct: false },
                { text: 'Sì, gli animali lo sentono sempre prima', correct: false },
                { text: 'No, i terremoti non si possono prevedere', correct: true },
                { text: 'Sì, basta guardare le crepe nei muri', correct: false }
            ],
            explanation: 'Nessuno può sapere in anticipo quando ci sarà un terremoto. Per questo bisogna essere sempre preparati!'
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
            explanation: 'In auto si è abbastanza protetti. Bisogna fermarsi in un posto aperto e aspettare che la scossa finisca.'
        },
        {
            category: 'terremoto',
            question: 'Dopo il terremoto, puoi rientrare subito in casa?',
            answers: [
                { text: 'Sì, per prendere i giocattoli', correct: false },
                { text: 'Sì, se la porta si apre', correct: false },
                { text: 'No, bisogna aspettare che le autorità dicano che è sicuro', correct: true },
                { text: 'Sì, se non ci sono crepe visibili', correct: false }
            ],
            explanation: 'Anche se la casa sembra a posto, potrebbero esserci danni nascosti. Solo i tecnici possono dire se è sicura!'
        },

        // ═══════════════════════════════════════
        // INCENDIO (9 domande)
        // ═══════════════════════════════════════
        {
            category: 'incendio',
            question: 'Se vedi un incendio in un bosco, cosa fai?',
            answers: [
                { text: 'Cerco di spegnerlo da solo', correct: false },
                { text: 'Chiamo subito il 112', correct: true },
                { text: 'Faccio un video da postare', correct: false },
                { text: 'Non faccio niente, passerà da solo', correct: false }
            ],
            explanation: 'Mai provare a spegnere un incendio da solo! Chiama subito il 112 e allontanati dal fuoco. Nel Lazio il 112 è l\'unico numero di emergenza da chiamare.'
        },
        {
            category: 'incendio',
            question: 'In caso di incendio in un edificio, cosa NON devi fare?',
            answers: [
                { text: 'Camminare carponi vicino al pavimento', correct: false },
                { text: 'Usare l\'ascensore per scendere più veloce', correct: true },
                { text: 'Coprirmi naso e bocca con un panno bagnato', correct: false },
                { text: 'Seguire le indicazioni dell\'insegnante', correct: false }
            ],
            explanation: 'L\'ascensore può bloccarsi e riempirsi di fumo. Usa sempre le scale e copri naso e bocca.'
        },
        {
            category: 'incendio',
            question: 'Perché durante un incendio bisogna stare bassi vicino al pavimento?',
            answers: [
                { text: 'Perché il pavimento è più fresco', correct: false },
                { text: 'Perché il fumo caldo sale verso l\'alto e in basso si respira meglio', correct: true },
                { text: 'Per non farsi vedere dalle fiamme', correct: false },
                { text: 'Perché è più facile correre', correct: false }
            ],
            explanation: 'Il fumo tossico sale verso l\'alto. Vicino al pavimento l\'aria è più pulita e puoi respirare meglio.'
        },
        {
            category: 'incendio',
            question: 'Cosa può causare un incendio nel bosco?',
            answers: [
                { text: 'La pioggia', correct: false },
                { text: 'Un mozzicone di sigaretta gettato a terra', correct: true },
                { text: 'Il vento leggero', correct: false },
                { text: 'Gli uccelli', correct: false }
            ],
            explanation: 'Un piccolo mozzicone può incendiare un intero bosco! Non si getta mai nulla per terra, soprattutto in estate.'
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
                { text: 'È un giocattolo rosso per decorare il corridoio', correct: false },
                { text: 'Serve a spegnere un piccolo fuoco appena iniziato', correct: true },
                { text: 'Serve a fare il ghiaccio', correct: false },
                { text: 'Si usa per pulire i pavimenti', correct: false }
            ],
            explanation: 'L\'estintore serve a spegnere un fuoco piccolo. Solo gli adulti addestrati devono usarlo. Tu devi allontanarti e dare l\'allarme!'
        },
        {
            category: 'incendio',
            question: 'In estate, perché è vietato accendere fuochi vicino al bosco?',
            answers: [
                { text: 'Perché fa troppo caldo per il fuoco', correct: false },
                { text: 'Perché la vegetazione secca prende fuoco facilmente', correct: true },
                { text: 'Perché si disturbano gli animali', correct: false },
                { text: 'Non è vietato, si può fare se si sta attenti', correct: false }
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
                { text: 'Saltare su e giù', correct: false }
            ],
            explanation: 'Fermati, buttati a terra e rotola: così soffochi le fiamme. Correre fa entrare più aria e il fuoco aumenta!'
        },
        {
            category: 'incendio',
            question: 'Se serve l\'intervento dei Vigili del Fuoco, quale numero si chiama?',
            answers: [
                { text: 'Non esiste un numero apposito', correct: false },
                { text: 'Il 112, il numero unico di emergenza', correct: true },
                { text: 'Si cerca su Internet durante l\'emergenza', correct: false },
                { text: 'Bisogna andare di persona alla caserma', correct: false }
            ],
            explanation: 'Nel Lazio si chiama sempre il 112, il numero unico europeo di emergenza. La centrale capisce di cosa hai bisogno e invia i Vigili del Fuoco, l\'ambulanza o i carabinieri.'
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
            explanation: 'I piani alti sono il posto più sicuro. L\'acqua può essere pericolosa anche se sembra bassa!'
        },
        {
            category: 'alluvione',
            question: 'Durante un\'alluvione, perché non bisogna scendere in cantina?',
            answers: [
                { text: 'Perché è buio', correct: false },
                { text: 'Perché l\'acqua può riempirla velocemente e restare intrappolati', correct: true },
                { text: 'Perché c\'è troppo disordine', correct: false },
                { text: 'Perché fa freddo', correct: false }
            ],
            explanation: 'La cantina è il primo posto che si riempie d\'acqua. Si rischia di restare intrappolati senza via di uscita.'
        },
        {
            category: 'alluvione',
            question: 'Perché non si deve attraversare una strada allagata a piedi?',
            answers: [
                { text: 'Perché ci si bagnano le scarpe', correct: false },
                { text: 'Perché sotto l\'acqua possono esserci buche, tombini aperti o correnti forti', correct: true },
                { text: 'Perché l\'acqua è sporca', correct: false },
                { text: 'Si può attraversare se l\'acqua è bassa', correct: false }
            ],
            explanation: 'Anche pochi centimetri d\'acqua possono nascondere pericoli. Non sai cosa c\'è sotto e la corrente ti può trascinare!'
        },
        {
            category: 'alluvione',
            question: 'Se sei in auto e trovi un sottopassaggio pieno d\'acqua, cosa fai?',
            answers: [
                { text: 'Passo veloce così non mi fermo', correct: false },
                { text: 'Mi fermo e torno indietro, cerco un\'altra strada', correct: true },
                { text: 'Aspetto che l\'acqua si abbassi', correct: false },
                { text: 'Passo piano piano', correct: false }
            ],
            explanation: 'Nei sottopassaggi l\'acqua può essere molto più profonda di quanto sembra. L\'auto si può bloccare e rimanere sommersa!'
        },
        {
            category: 'alluvione',
            question: 'Cosa significa allerta arancione per rischio idrogeologico?',
            answers: [
                { text: 'Che fa caldo', correct: false },
                { text: 'Che ci sarà il sole', correct: false },
                { text: 'Che sono previste piogge molto forti e bisogna fare attenzione', correct: true },
                { text: 'Che si può uscire normalmente', correct: false }
            ],
            explanation: 'Allerta arancione significa che possono arrivare piogge intense con rischio di allagamenti e frane. Meglio stare al sicuro!'
        },
        {
            category: 'alluvione',
            question: 'Dopo un\'alluvione, si può bere l\'acqua del rubinetto?',
            answers: [
                { text: 'Sì, sempre', correct: false },
                { text: 'Solo se è calda', correct: false },
                { text: 'No, finché le autorità non dicono che è sicura', correct: true },
                { text: 'Sì, basta farla bollire', correct: false }
            ],
            explanation: 'L\'acqua del rubinetto potrebbe essere inquinata. Aspetta sempre che le autorità dicano che si può bere!'
        },
        {
            category: 'alluvione',
            question: 'Cosa è una frana?',
            answers: [
                { text: 'Un forte vento che soffia dalla montagna', correct: false },
                { text: 'Una massa di terra e rocce che scivola lungo un pendio', correct: true },
                { text: 'Un tipo di terremoto', correct: false },
                { text: 'Un fiume che straripa', correct: false }
            ],
            explanation: 'Una frana è quando la terra di un pendio si stacca e scende verso il basso, portando con sé tutto quello che incontra.'
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
            explanation: 'I piani alti sono più sicuri. Il Comune indica anche le aree di raccolta dove andare in caso di evacuazione.'
        },

        // ═══════════════════════════════════════
        // NUMERI DI EMERGENZA (8 domande)
        // ═══════════════════════════════════════
        {
            category: 'numeri',
            question: 'Qual è il numero unico di emergenza da chiamare in Italia?',
            answers: [
                { text: '118', correct: false },
                { text: '115', correct: false },
                { text: '112', correct: true },
                { text: '113', correct: false }
            ],
            explanation: 'Il 112 è il numero unico di emergenza. Funziona per tutte le emergenze: polizia, ambulanza e vigili del fuoco.'
        },
        {
            category: 'numeri',
            question: 'Quando chiami il 112, cosa devi dire?',
            answers: [
                { text: 'Solo il mio nome', correct: false },
                { text: 'Cosa è successo, dove mi trovo e quante persone hanno bisogno di aiuto', correct: true },
                { text: 'Devo solo urlare "aiuto"', correct: false },
                { text: 'Non devo dire niente, loro sanno già tutto', correct: false }
            ],
            explanation: 'Quando chiami il 112, parla con calma e spiega cosa è successo, dove ti trovi e se qualcuno ha bisogno di aiuto.'
        },
        {
            category: 'numeri',
            question: 'Quale numero chiami per segnalare un incendio nel bosco?',
            answers: [
                { text: '118', correct: false },
                { text: '112', correct: true },
                { text: '113', correct: false },
                { text: '117', correct: false }
            ],
            explanation: 'Nel Lazio il 112 è il numero unico di emergenza, anche per gli incendi boschivi. La centrale manda subito i soccorsi giusti: Vigili del Fuoco, Forestale o Protezione Civile.'
        },
        {
            category: 'numeri',
            question: 'Il 112 funziona anche se non hai credito sul telefono?',
            answers: [
                { text: 'No, serve credito', correct: false },
                { text: 'Sì, il 112 è sempre gratuito e funziona anche senza credito', correct: true },
                { text: 'Solo con i telefoni fissi', correct: false },
                { text: 'Funziona solo di giorno', correct: false }
            ],
            explanation: 'Il 112 è gratuito e funziona sempre: senza credito, senza SIM e da qualsiasi telefono, anche da quello di un amico!'
        },
        {
            category: 'numeri',
            question: 'Quale numero chiami se qualcuno si sente molto male?',
            answers: [
                { text: '115', correct: false },
                { text: '117', correct: false },
                { text: 'Il 112', correct: true },
                { text: '1515', correct: false }
            ],
            explanation: 'Nel Lazio il 112 è il numero unico di emergenza, anche per l\'ambulanza. La centrale capisce il tipo di aiuto che serve e invia subito i soccorsi sanitari.'
        },
        {
            category: 'numeri',
            question: 'È giusto chiamare il 112 per scherzo?',
            answers: [
                { text: 'Sì, tanto non succede niente', correct: false },
                { text: 'Sì, per fare una prova', correct: false },
                { text: 'No, perché si occupano le linee e chi ha davvero bisogno potrebbe non riuscire a chiamare', correct: true },
                { text: 'Solo se lo faccio una volta sola', correct: false }
            ],
            explanation: 'Chiamare per scherzo è un reato! Ogni chiamata falsa toglie tempo e risorse a chi ha davvero bisogno di aiuto.'
        },
        {
            category: 'numeri',
            question: 'Il numero 112 funziona in tutta Europa?',
            answers: [
                { text: 'No, solo in Italia', correct: false },
                { text: 'Sì, è il numero di emergenza in tutta Europa', correct: true },
                { text: 'Solo in Italia e Francia', correct: false },
                { text: 'Solo se hai una SIM europea', correct: false }
            ],
            explanation: 'Il 112 è il numero unico europeo. Se sei in vacanza in un altro Paese, puoi sempre chiamare il 112!'
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
            explanation: 'Prima chiama un adulto di fiducia. Se non riesci a raggiungerlo, il 112 può aiutarti a farti trovare.'
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
            question: 'Perché nello zaino di emergenza serve un fischietto?',
            answers: [
                { text: 'Per giocare', correct: false },
                { text: 'Per farsi sentire dai soccorritori se si è bloccati', correct: true },
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
            explanation: 'Lo zaino deve essere facile da prendere e pronto: vicino alla porta o in corridoio. In emergenza non c\'è tempo di cercarlo!'
        },
        {
            category: 'zaino',
            question: 'Perché nello zaino di emergenza serve una radio a pile?',
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
                { text: 'Solo quando c\'è un\'emergenza', correct: false },
                { text: 'Ogni giorno', correct: false }
            ],
            explanation: 'L\'acqua scade, le pile si scaricano e i medicinali possono scadere. Controlla tutto almeno due volte l\'anno!'
        },
        {
            category: 'zaino',
            question: 'Nello zaino di emergenza servono anche i documenti?',
            answers: [
                { text: 'No, non servono a niente', correct: false },
                { text: 'Sì, una copia dei documenti della famiglia', correct: true },
                { text: 'Solo la tessera della biblioteca', correct: false },
                { text: 'Solo la tessera del supermercato', correct: false }
            ],
            explanation: 'Una copia dei documenti è importante per farsi identificare, ricevere aiuto e dimostrare chi sei durante l\'emergenza.'
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
                { text: 'Corro il più veloce possibile verso l\'uscita', correct: false },
                { text: 'Aspetto che i miei genitori vengano a prendermi', correct: false }
            ],
            explanation: 'Segui l\'insegnante in fila ordinata. Non portare le cose e non correre: la calma salva la vita!'
        },
        {
            category: 'evacuazione',
            question: 'A cosa serve il punto di raccolta della scuola?',
            answers: [
                { text: 'È il posto dove si gioca durante l\'intervallo', correct: false },
                { text: 'È il luogo sicuro dove ritrovarsi per controllare che ci siano tutti', correct: true },
                { text: 'È dove si parcheggia', correct: false },
                { text: 'È il posto dove aspettare l\'autobus', correct: false }
            ],
            explanation: 'Al punto di raccolta l\'insegnante fa l\'appello per verificare che nessuno manchi. È un posto sicuro!'
        },
        {
            category: 'evacuazione',
            question: 'Chi guida la fila durante l\'evacuazione a scuola?',
            answers: [
                { text: 'Il più veloce della classe', correct: false },
                { text: 'L\'aprifila, un compagno scelto dall\'insegnante', correct: true },
                { text: 'Il rappresentante di classe', correct: false },
                { text: 'Ognuno va per conto suo', correct: false }
            ],
            explanation: 'In ogni classe c\'è un aprifila che guida i compagni e un chiudifila che si assicura che nessuno resti indietro.'
        },
        {
            category: 'evacuazione',
            question: 'Durante l\'evacuazione, perché non devi correre?',
            answers: [
                { text: 'Perché l\'insegnante si arrabbia', correct: false },
                { text: 'Perché correndo si può cadere, fare cadere gli altri e creare panico', correct: true },
                { text: 'Perché si suda', correct: false },
                { text: 'Si può correre se si ha paura', correct: false }
            ],
            explanation: 'Camminare spediti ma senza correre evita cadute e panico. Quando tutti restano calmi, si esce più in fretta!'
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
            explanation: 'Aiutare un compagno in difficoltà è importante, ma senza bloccare la fila. Avvisa subito l\'insegnante!'
        },
        {
            category: 'evacuazione',
            question: 'Perché a scuola si fanno le prove di evacuazione?',
            answers: [
                { text: 'Per perdere un\'ora di lezione', correct: false },
                { text: 'Per imparare cosa fare in caso di emergenza vera', correct: true },
                { text: 'Perché il preside lo ordina per divertimento', correct: false },
                { text: 'Per fare ginnastica', correct: false }
            ],
            explanation: 'Le prove servono a imparare il percorso e i comportamenti corretti. Così, se succede davvero, sai già cosa fare!'
        },
        {
            category: 'evacuazione',
            question: 'Se sei in bagno quando suona l\'allarme di evacuazione, cosa fai?',
            answers: [
                { text: 'Resto in bagno ad aspettare', correct: false },
                { text: 'Torno in classe a prendere le cose', correct: false },
                { text: 'Esco subito e raggiungo il punto di raccolta o la classe più vicina', correct: true },
                { text: 'Chiamo i miei genitori', correct: false }
            ],
            explanation: 'Se sei fuori dalla classe, raggiungi il punto di raccolta o unisciti alla fila più vicina. L\'importante è farsi trovare!'
        },
        {
            category: 'evacuazione',
            question: 'Cosa NON devi portare con te durante l\'evacuazione?',
            answers: [
                { text: 'Me stesso', correct: false },
                { text: 'Lo zaino pesante, i libri e gli oggetti ingombranti', correct: true },
                { text: 'Il giubbotto se fa freddo', correct: false },
                { text: 'Un compagno in difficoltà', correct: false }
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
                { text: 'Persone che aiutano la comunità durante le emergenze, senza essere pagate', correct: true },
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
                { text: 'Si può uscire a giocare', correct: false },
                { text: 'È solo un consiglio, non è importante', correct: false }
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
            explanation: 'Prevenzione significa prepararsi in anticipo: conoscere i rischi, sapere cosa fare e avere tutto pronto. È la cosa più importante!'
        },
        {
            category: 'protezione-civile',
            question: 'Quale colore di allerta meteo indica il pericolo più alto?',
            answers: [
                { text: 'Giallo', correct: false },
                { text: 'Verde', correct: false },
                { text: 'Arancione', correct: false },
                { text: 'Rosso', correct: true }
            ],
            explanation: 'Rosso è il livello massimo: significa fenomeni molto forti e rischio elevato. Bisogna seguire tutte le indicazioni delle autorità!'
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
                { text: 'C\'è un pericolo legato alla natura', correct: false },
                { text: 'Si deve andare al punto di raccolta', correct: false }
            ],
            explanation: 'Verde significa tutto tranquillo: nessuna allerta in corso. Ma ricorda: essere preparati è sempre importante!'
        },
        {
            category: 'protezione-civile',
            question: 'Anche i bambini possono aiutare nella prevenzione?',
            answers: [
                { text: 'No, la prevenzione è solo per gli adulti', correct: false },
                { text: 'Sì, imparando le regole di sicurezza e aiutando la famiglia a prepararsi', correct: true },
                { text: 'Solo i bambini molto grandi', correct: false },
                { text: 'Solo se vanno a un corso speciale', correct: false }
            ],
            explanation: 'Certo che sì! Imparare i comportamenti corretti, preparare lo zaino di emergenza e conoscere i numeri da chiamare: anche tu fai prevenzione!'
        },
        {
            category: 'protezione-civile',
            question: 'Cos\'è il Piano di Emergenza Comunale?',
            answers: [
                { text: 'Un piano per costruire case nuove', correct: false },
                { text: 'Un documento che spiega cosa fare e dove andare in caso di emergenza nel proprio Comune', correct: true },
                { text: 'Un elenco di ristoranti', correct: false },
                { text: 'Un programma televisivo', correct: false }
            ],
            explanation: 'Ogni Comune ha un Piano di Emergenza che indica le aree sicure, i percorsi di evacuazione e chi fa cosa in caso di emergenza.'
        },
        {
            category: 'protezione-civile',
            question: 'Genzano di Roma si trova nella zona dei Castelli Romani. Che tipo di territorio è?',
            answers: [
                { text: 'Una pianura senza colline', correct: false },
                { text: 'Una zona collinare di origine vulcanica con laghi', correct: true },
                { text: 'Una zona di montagna con neve tutto l\'anno', correct: false },
                { text: 'Una zona di mare', correct: false }
            ],
            explanation: 'I Colli Albani sono un antico complesso vulcanico. I laghi di Nemi e Albano si sono formati nei crateri spenti. Il territorio è soggetto a rischio idrogeologico e sismico.'
        },
        {
            category: 'protezione-civile',
            question: 'Secondo la classificazione sismica della Regione Lazio, i Colli Albani sono in:',
            answers: [
                { text: 'Zona 1 (pericolosità massima)', correct: false },
                { text: 'Zona 2 (pericolosità media)', correct: true },
                { text: 'Zona 4 (pericolosità bassissima)', correct: false },
                { text: 'Non è zona sismica', correct: false }
            ],
            explanation: 'L\'area dei Castelli Romani è classificata come zona sismica 2: possono verificarsi terremoti di media intensità. È importante conoscere i comportamenti di autoprotezione.'
        },
        {
            category: 'protezione-civile',
            question: 'Nel nostro territorio dei Castelli Romani, quale è un rischio tipico dei mesi estivi?',
            answers: [
                { text: 'Valanghe', correct: false },
                { text: 'Maremoti', correct: false },
                { text: 'Incendi boschivi', correct: true },
                { text: 'Nevicate intense', correct: false }
            ],
            explanation: 'Da giugno a settembre la vegetazione dei boschi dei Castelli Romani può prendere fuoco molto facilmente. Nel Lazio per segnalare un incendio boschivo si chiama il 112, il numero unico di emergenza.'
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
                { text: 'Non faccio niente, è normale', correct: false }
            ],
            explanation: 'Il gas è pericoloso! Non toccare interruttori e non usare fiamme. Apri le finestre e chiama subito un adulto.'
        },
        {
            category: 'sicurezza',
            question: 'Perché è importante conoscere le vie di fuga della propria scuola?',
            answers: [
                { text: 'Per correre più veloci degli altri', correct: false },
                { text: 'Per sapere dove andare in caso di emergenza, senza perdere tempo', correct: true },
                { text: 'Per uscire prima durante l\'intervallo', correct: false },
                { text: 'Non è importante, ci pensa l\'insegnante', correct: false }
            ],
            explanation: 'Se conosci la via di fuga, in emergenza sai subito dove andare. La preparazione è la migliore protezione!'
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
            explanation: 'La torcia è sicura perché non ha fiamme. Candele e accendini possono causare incendi, soprattutto al buio!'
        },
        {
            category: 'sicurezza',
            question: 'Perché non si devono toccare le prese elettriche con le mani bagnate?',
            answers: [
                { text: 'Perché si sporcano le prese', correct: false },
                { text: 'Perché l\'acqua conduce l\'elettricità e si rischia una scossa', correct: true },
                { text: 'Perché si rompono', correct: false },
                { text: 'Si possono toccare, non è pericoloso', correct: false }
            ],
            explanation: 'L\'acqua fa passare la corrente elettrica attraverso il corpo. È molto pericoloso! Asciuga sempre bene le mani prima.'
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
                { text: 'Apro un po\' per vedere chi è', correct: false },
                { text: 'Grido "chi è?" e poi apro', correct: false }
            ],
            explanation: 'Non aprire mai la porta a sconosciuti quando sei solo! Guarda dallo spioncino e, se hai dubbi, chiama un adulto di fiducia.'
        },
        {
            category: 'sicurezza',
            question: 'Perché è importante che tutti in famiglia sappiano dove si chiude il gas?',
            answers: [
                { text: 'Per risparmiare sulla bolletta', correct: false },
                { text: 'Per chiuderlo subito in caso di fuga di gas o terremoto', correct: true },
                { text: 'Per pulire il tubo del gas', correct: false },
                { text: 'Non è importante, ci pensa il tecnico', correct: false }
            ],
            explanation: 'Se senti odore di gas o c\'è un terremoto, chiudere subito il rubinetto del gas può evitare esplosioni e incendi.'
        },
        {
            category: 'sicurezza',
            question: 'Qual è il posto più sicuro dove ripararsi in casa durante un temporale con fulmini?',
            answers: [
                { text: 'Vicino alla finestra per guardare', correct: false },
                { text: 'In balcone sotto la tettoia', correct: false },
                { text: 'Al centro della stanza, lontano da finestre e apparecchi elettrici', correct: true },
                { text: 'Nella vasca da bagno', correct: false }
            ],
            explanation: 'I fulmini possono colpire gli apparecchi collegati alla corrente e le finestre. Stai al centro della stanza, al sicuro!'
        },
        // ═══════════════════════════════════════
        // DOMANDE AGGIUNTIVE (v2 — 2026)
        // ═══════════════════════════════════════
        {
            category: 'terremoto',
            question: 'Durante una scossa di terremoto, se sei in classe, cosa devi fare?',
            answers: [
                { text: 'Uscire subito correndo per le scale', correct: false },
                { text: 'Ripararmi sotto il banco con le mani sulla testa', correct: true },
                { text: 'Affacciarmi alla finestra', correct: false },
                { text: 'Saltare sulla sedia', correct: false }
            ],
            explanation: 'Sotto il banco sei protetto dalla caduta di oggetti. Si esce dall’aula solo dopo la scossa, in fila, senza correre.'
        },
        {
            category: 'terremoto',
            question: 'Perché dopo un terremoto è meglio non usare l’ascensore?',
            answers: [
                { text: 'Perché è più lento delle scale', correct: false },
                { text: 'Perché può bloccarsi e lasciarti dentro', correct: true },
                { text: 'Perché costa di più', correct: false },
                { text: 'Perché fa troppo rumore', correct: false }
            ],
            explanation: 'Le scosse possono danneggiare l’impianto elettrico e fermare l’ascensore. Le scale sono sempre la via più sicura.'
        },
        {
            category: 'terremoto',
            question: 'Cos’è il "triangolo della vita" che insegnano a scuola?',
            answers: [
                { text: 'Un gioco di società', correct: false },
                { text: 'Lo spazio di riparo tra un mobile robusto e il pavimento', correct: true },
                { text: 'Una figura geometrica in matematica', correct: false },
                { text: 'Un simbolo sulla pagella', correct: false }
            ],
            explanation: 'In caso di crollo, accanto a un mobile robusto si forma uno spazio che può proteggerti. Vicino a un muro portante o sotto un tavolo robusto sei più al sicuro.'
        },
        {
            category: 'incendio',
            question: 'Se in casa c’è fumo denso, come ti muovi per uscire?',
            answers: [
                { text: 'Corro in piedi per fare prima', correct: false },
                { text: 'Mi abbasso e striscio, l’aria pulita è vicino al pavimento', correct: true },
                { text: 'Mi metto in piedi sulla sedia', correct: false },
                { text: 'Mi nascondo sotto il letto', correct: false }
            ],
            explanation: 'Il fumo caldo sale verso il soffitto. Vicino al pavimento c’è aria più pulita e più fresca: strisciando respiri meglio.'
        },
        {
            category: 'incendio',
            question: 'Se si accende una pentola di olio bollente, cosa NON devi fare?',
            answers: [
                { text: 'Spegnere il fornello', correct: false },
                { text: 'Coprire la pentola con un coperchio', correct: false },
                { text: 'Gettare acqua sull’olio in fiamme', correct: true },
                { text: 'Chiamare un adulto', correct: false }
            ],
            explanation: 'L’acqua sull’olio provoca un’esplosione di vapore bollente. Si spegne il fornello e si copre con un coperchio o con un panno bagnato strizzato.'
        },
        {
            category: 'incendio',
            question: 'Che colore hanno i cartelli che indicano l’uscita di emergenza?',
            answers: [
                { text: 'Rossi', correct: false },
                { text: 'Verdi con freccia bianca', correct: true },
                { text: 'Gialli con bordo nero', correct: false },
                { text: 'Blu rotondi', correct: false }
            ],
            explanation: 'Il verde con simboli bianchi indica salvataggio e vie di fuga. Il rosso indica dispositivi antincendio (estintori, idranti).'
        },
        {
            category: 'alluvione',
            question: 'Durante un’alluvione, dove ti metti in casa?',
            answers: [
                { text: 'In cantina o in garage', correct: false },
                { text: 'Ai piani alti della casa', correct: true },
                { text: 'Vicino alle finestre per guardare fuori', correct: false },
                { text: 'Sul balcone', correct: false }
            ],
            explanation: 'I piani alti sono più sicuri perché l’acqua sale dal basso. Cantine e garage possono allagarsi rapidamente.'
        },
        {
            category: 'alluvione',
            question: 'Se vedi un sottopasso allagato e sei in auto con i tuoi, cosa è giusto fare?',
            answers: [
                { text: 'Attraversarlo piano', correct: false },
                { text: 'Tornare indietro e cercare un’altra strada', correct: true },
                { text: 'Spegnere l’auto e aspettare', correct: false },
                { text: 'Aprire i finestrini', correct: false }
            ],
            explanation: 'Anche 30 cm d’acqua possono far galleggiare un’auto. Nei sottopassi l’acqua si raccoglie in fretta: non attraversare mai.'
        },
        {
            category: 'alluvione',
            question: 'Cos’è un "kit di emergenza" per l’alluvione?',
            answers: [
                { text: 'Una borsa di giochi', correct: false },
                { text: 'Una borsa con documenti, acqua, torcia, medicine e coperta', correct: true },
                { text: 'Un pallone e un paio di scarpe', correct: false },
                { text: 'Una valigia di vestiti eleganti', correct: false }
            ],
            explanation: 'Nel kit di emergenza ci sono le cose indispensabili per resistere alcune ore senza aiuto: acqua, torcia, radio, medicine, documenti.'
        },
        {
            category: 'numeri',
            question: 'Il 112 è il numero di emergenza di quanti Paesi europei?',
            answers: [
                { text: 'Solo dell’Italia', correct: false },
                { text: 'Di tutti i Paesi dell’Unione Europea', correct: true },
                { text: 'Solo di Italia e Francia', correct: false },
                { text: 'Di 3 Paesi', correct: false }
            ],
            explanation: 'Il 112 è il Numero Unico Europeo di Emergenza: funziona in tutti i Paesi dell’Unione Europea. Se vai in vacanza all’estero puoi chiamarlo allo stesso modo.'
        },
        {
            category: 'numeri',
            question: 'Quando chiami il 112, cosa ti chiedono per primo?',
            answers: [
                { text: 'Il tuo cognome', correct: false },
                { text: 'Dove ti trovi, cosa è successo e se ci sono feriti', correct: true },
                { text: 'La tua data di nascita', correct: false },
                { text: 'Il nome della scuola', correct: false }
            ],
            explanation: 'L’operatore del 112 deve capire subito dove mandare i soccorsi e cosa sta succedendo. Parla con calma e rispondi alle domande.'
        },
        {
            category: 'numeri',
            question: 'È vero che il 112 si può chiamare gratis anche da un cellulare senza credito?',
            answers: [
                { text: 'No, serve credito', correct: false },
                { text: 'Sì, è sempre gratuito anche senza credito', correct: true },
                { text: 'Solo di giorno', correct: false },
                { text: 'Solo se lo dici ai genitori', correct: false }
            ],
            explanation: 'Il 112 è gratuito e funziona sempre, anche senza credito e anche senza SIM in alcuni casi. È il numero da insegnare a tutti.'
        },
        {
            category: 'zaino',
            question: 'Nel tuo zaino di emergenza a scuola, cosa NON serve?',
            answers: [
                { text: 'Una bottiglietta d’acqua', correct: false },
                { text: 'Un fischietto', correct: false },
                { text: 'Un gioco elettronico', correct: true },
                { text: 'Un biglietto con i numeri dei genitori', correct: false }
            ],
            explanation: 'Nello zaino di emergenza servono cose utili: acqua, fischietto, coperta termica, numeri di emergenza, una foto dei genitori. I giochi elettronici non servono.'
        },
        {
            category: 'zaino',
            question: 'A cosa serve il fischietto nello zaino di emergenza?',
            answers: [
                { text: 'A giocare', correct: false },
                { text: 'A farsi sentire dai soccorritori se resti nascosto', correct: true },
                { text: 'A chiamare i gatti', correct: false },
                { text: 'A fare rumore in classe', correct: false }
            ],
            explanation: 'Il fischietto fa meno fatica della voce e si sente più lontano. Se sei bloccato o nascosto, soffia a gruppi di tre per farti trovare.'
        },
        {
            category: 'zaino',
            question: 'Perché nello zaino di emergenza si mette una coperta "termica" dorata?',
            answers: [
                { text: 'Perché è bella', correct: false },
                { text: 'Perché tiene caldo anche se è sottile', correct: true },
                { text: 'Perché è un regalo', correct: false },
                { text: 'Perché fa colore', correct: false }
            ],
            explanation: 'La coperta termica è leggera e pieghevole ma trattiene il calore del corpo. Utile se resti fuori casa o devi aspettare i soccorsi al freddo.'
        },
        {
            category: 'evacuazione',
            question: 'Quando suona l’allarme di evacuazione, cosa deve fare il capofila della classe?',
            answers: [
                { text: 'Correre avanti', correct: false },
                { text: 'Guidare i compagni in fila verso l’uscita indicata', correct: true },
                { text: 'Aspettare la maestra fuori', correct: false },
                { text: 'Chiudere le finestre', correct: false }
            ],
            explanation: 'Il capofila guida la fila con calma, seguendo le frecce verdi. Il chiudifila controlla che nessuno resti indietro.'
        },
        {
            category: 'evacuazione',
            question: 'Durante l’evacuazione, si possono prendere zaino e giacca?',
            answers: [
                { text: 'Sì, sempre', correct: false },
                { text: 'No, si esce subito senza cercare le proprie cose', correct: true },
                { text: 'Solo lo zaino', correct: false },
                { text: 'Solo la giacca', correct: false }
            ],
            explanation: 'Ogni secondo conta. Le cose personali si recuperano dopo, quando tutti sono al sicuro al punto di raccolta.'
        },
        {
            category: 'evacuazione',
            question: 'Cos’è il "punto di raccolta" durante un’evacuazione?',
            answers: [
                { text: 'Un luogo per giocare', correct: false },
                { text: 'Il posto dove ci si ritrova per contarsi', correct: true },
                { text: 'Un negozio', correct: false },
                { text: 'Un’aula di riserva', correct: false }
            ],
            explanation: 'Al punto di raccolta le maestre fanno l’appello per controllare che tutti siano usciti. Si rimane lì finché non arriva il segnale di fine emergenza.'
        },
        {
            category: 'protezione-civile',
            question: 'Cosa fanno i volontari di Protezione Civile?',
            answers: [
                { text: 'Guidano le ambulanze', correct: false },
                { text: 'Aiutano le persone durante emergenze e fanno prevenzione', correct: true },
                { text: 'Vendono biglietti', correct: false },
                { text: 'Controllano i parcheggi', correct: false }
            ],
            explanation: 'I volontari di Protezione Civile aiutano in caso di terremoto, alluvione, incendio boschivo e fanno prevenzione nelle scuole e nei quartieri.'
        },
        {
            category: 'protezione-civile',
            question: 'Qual è il colore ufficiale della Protezione Civile in Italia?',
            answers: [
                { text: 'Rosso', correct: false },
                { text: 'Blu e arancione (alta visibilità)', correct: true },
                { text: 'Verde e giallo', correct: false },
                { text: 'Viola', correct: false }
            ],
            explanation: 'La divisa della Protezione Civile è blu con parti arancioni ad alta visibilità, per essere riconoscibili anche di notte o con poca luce.'
        },
        {
            category: 'protezione-civile',
            question: 'Come puoi aiutare la Protezione Civile anche da bambino?',
            answers: [
                { text: 'Scaricando giochi sul telefono', correct: false },
                { text: 'Imparando i comportamenti giusti e spiegandoli ai parenti', correct: true },
                { text: 'Mettendo "mi piace" sui social', correct: false },
                { text: 'Comprando magliette', correct: false }
            ],
            explanation: 'La prevenzione parte dai bambini: se impari cosa fare in caso di terremoto, incendio o alluvione, puoi aiutare anche mamma, papà e nonni.'
        },
        {
            category: 'sicurezza',
            question: 'In casa, qual è il posto più sicuro se senti odore di gas?',
            answers: [
                { text: 'In cucina a controllare il fornello', correct: false },
                { text: 'Fuori casa, dopo aver aperto le finestre e avvisato un adulto', correct: true },
                { text: 'Accendendo la luce per vedere meglio', correct: false },
                { text: 'Chiudendo tutte le finestre', correct: false }
            ],
            explanation: 'Se senti odore di gas: non accendere luci o fiamme, apri subito le finestre, avverti un adulto e uscite di casa. Poi si chiama il 112.'
        },
        {
            category: 'sicurezza',
            question: 'Se il campanello suona e sei solo in casa, cosa fai?',
            answers: [
                { text: 'Apro subito la porta', correct: false },
                { text: 'Guardo dallo spioncino e non apro a sconosciuti', correct: true },
                { text: 'Urlo dalla finestra', correct: false },
                { text: 'Chiamo il 112 per ogni suono', correct: false }
            ],
            explanation: 'Se sei solo, non aprire mai a chi non conosci. Guarda dallo spioncino e, se ti senti in pericolo, chiama i genitori o il 112.'
        },
        {
            category: 'sicurezza',
            question: 'A cosa serve un rilevatore di fumo in casa?',
            answers: [
                { text: 'A rinfrescare l’aria', correct: false },
                { text: 'A suonare se c’è un inizio di incendio, anche di notte', correct: true },
                { text: 'A misurare la temperatura', correct: false },
                { text: 'A controllare il Wi-Fi', correct: false }
            ],
            explanation: 'Il rilevatore di fumo è un piccolo apparecchio che suona forte appena sente fumo. Può salvare la vita, soprattutto di notte quando si dorme.'
        },

        // ═══════════════════════════════════════════════════════════════
        // CATEGORIA 9: FONTI UFFICIALI E IT-ALERT (8 domande)
        // ═══════════════════════════════════════════════════════════════
        {
            category: 'comunicazione',
            question: 'Cosa è IT-alert?',
            answers: [
                { text: 'Un nuovo gioco di emergenza', correct: false },
                { text: 'Un messaggio del Governo che arriva su tutti i cellulari nella zona di pericolo', correct: true },
                { text: 'Una sigla dei volontari', correct: false },
                { text: 'Una radio per i pompieri', correct: false }
            ],
            explanation: 'IT-alert è il sistema italiano di allarme pubblico, attivo dal 2024: il Governo manda un messaggio (cell broadcast) a tutti i cellulari accesi nella zona del pericolo. Arriva anche se non hai i contatti del Comune.'
        },
        {
            category: 'comunicazione',
            question: 'Tuo cugino ti manda su WhatsApp un messaggio "Allerta rossa! È previsto terremoto stanotte!". Cosa fai?',
            answers: [
                { text: 'Lo inoltro a tutti per avvisare', correct: false },
                { text: 'Vado a dormire fuori casa', correct: false },
                { text: 'Verifico sul sito del Comune o della Protezione Civile e non lo inoltro', correct: true },
                { text: 'Chiamo subito il 112 per chiedere conferma', correct: false }
            ],
            explanation: 'I terremoti NON si possono prevedere. Ogni "allerta sismica" su WhatsApp è una bufala. Verifica sempre su fonti ufficiali (Comune, DPC, Centro Funzionale Regionale) prima di credere e di inoltrare.'
        },
        {
            category: 'comunicazione',
            question: 'Quale di queste NON è una fonte ufficiale per le allerte meteo nel Lazio?',
            answers: [
                { text: 'Il Centro Funzionale Regionale del Lazio', correct: false },
                { text: 'Il sito del Dipartimento di Protezione Civile (DPC)', correct: false },
                { text: 'Il sito del Comune di Genzano', correct: false },
                { text: 'Un canale Telegram di un meteo amatoriale', correct: true }
            ],
            explanation: 'I canali amatoriali e i meteo "sensazionalistici" non sono ufficiali. Le sole fonti affidabili per le allerte sono Centro Funzionale Regionale, DPC e Comune.'
        },
        {
            category: 'comunicazione',
            question: 'Perché il messaggio di IT-alert arriva fortissimo e non puoi metterlo in silenzio?',
            answers: [
                { text: 'Per fare uno scherzo', correct: false },
                { text: 'Perché in emergenza l\'allarme deve raggiungere TUTTI, anche chi dorme', correct: true },
                { text: 'Per pubblicizzare il Governo', correct: false },
                { text: 'Perché è un test', correct: false }
            ],
            explanation: 'IT-alert usa un suono forte e una vibrazione speciale che ignora le impostazioni silenziose: in emergenza vera, ogni minuto conta e la notifica deve svegliare anche chi dorme.'
        },
        {
            category: 'comunicazione',
            question: 'Una signora in metro ti dice che ha visto su Facebook che "il sindaco evacua mezzo paese stanotte". Come reagisci?',
            answers: [
                { text: 'La credo subito e lo dico ai miei genitori', correct: false },
                { text: 'La ignoro completamente', correct: false },
                { text: 'Le rispondo che è una bufala perché è su Facebook', correct: false },
                { text: 'Verifico sul sito del Comune o sul canale ufficiale prima di credere', correct: true }
            ],
            explanation: 'In emergenza non si crede né si esclude a priori. Si verifica sulle fonti ufficiali. I social non sono fonti ufficiali (anche se a volte le riportano).'
        },
        {
            category: 'comunicazione',
            question: 'Cosa significa "non amplificare la fake news"?',
            answers: [
                { text: 'Non urlare quando la racconti', correct: false },
                { text: 'Non condividere il post falso, nemmeno per smentirlo', correct: true },
                { text: 'Mettere il volume basso al video', correct: false },
                { text: 'Non parlare di politica', correct: false }
            ],
            explanation: 'Quando condividi una fake news (anche per criticarla) il post diventa più visibile e raggiunge più persone. Meglio rispondere SENZA citare il post falso, indicando solo la fonte ufficiale corretta.'
        },
        {
            category: 'comunicazione',
            question: 'In allerta arancione, dove cerchi le indicazioni del Comune di Genzano?',
            answers: [
                { text: 'Solo sui giornali del giorno dopo', correct: false },
                { text: 'Sul sito ufficiale del Comune e sui canali social istituzionali', correct: true },
                { text: 'Sul gruppo WhatsApp degli amici', correct: false },
                { text: 'Su Wikipedia', correct: false }
            ],
            explanation: 'Il Comune comunica le emergenze sul sito istituzionale e sui canali social ufficiali (verificati con il bollino blu). In più ci sono il sito della Regione Lazio e quello del DPC.'
        },
        {
            category: 'comunicazione',
            question: 'I codici colore delle allerte meteo (verde/giallo/arancione/rosso) chi li stabilisce per il Lazio?',
            answers: [
                { text: 'Il Comune di Genzano', correct: false },
                { text: 'Il Centro Funzionale Regionale del Lazio', correct: true },
                { text: 'Il meteo della TV nazionale', correct: false },
                { text: 'Il Sindaco', correct: false }
            ],
            explanation: 'Il Centro Funzionale Regionale (CFR) del Lazio è la struttura tecnica che valuta i bollettini di criticità ed emette i codici colore. Il Comune e il Sindaco poi attivano le misure operative.'
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
            if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
        } else {
            feedbackBox.classList.add('wrong');
            feedbackBox.innerHTML = '<div class="feedback-title">Risposta sbagliata</div>' + currentQ.explanation;
            // Layer 3: hint contestuale con link teoria in base alla categoria della domanda
            if (window.GameCoach && window.GameCoach.hint) {
                const TEORIA = {
                    'terremoto': { url: '/rischi-prevenzione/rischio-sismico/', titolo: 'rischio sismico' },
                    'incendio': { url: '/rischi-prevenzione/rischio-incendio/', titolo: 'rischio incendio' },
                    'alluvione': { url: '/rischi-prevenzione/rischio-idrogeologico/', titolo: 'rischio idrogeologico' },
                    'numeri': { url: '/numeri-utili/', titolo: 'numeri di emergenza' },
                    'zaino': { url: '/rischi-prevenzione/kit-emergenza/', titolo: 'kit di emergenza' },
                    'evacuazione': { url: '/piano-familiare/', titolo: 'piano familiare' },
                    'protezione-civile': { url: '/chi-siamo/', titolo: 'chi siamo' },
                    'sicurezza': { url: '/cosa-fare-adesso/', titolo: 'cosa fare in emergenza' }
                };
                const t = TEORIA[currentQ.category] || { url: '/rischi-prevenzione/', titolo: 'rischi e prevenzione' };
                window.GameCoach.hint('Vuoi capire il perché? Leggi la pagina ' + t.titolo + ' del sito.', t.url);
            }
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
        const percentage = Math.round((score / shuffledQuestions.length) * 100);
        if (percentage >= 90) { feedbackMessageElement.innerText = "Fantastico! Sei un vero esperto di sicurezza!"; }
        else if (percentage >= 70) { feedbackMessageElement.innerText = "Molto bravo! Conosci bene le regole di sicurezza."; }
        else if (percentage >= 50) { feedbackMessageElement.innerText = "Non male! Riprova per imparare ancora di più."; }
        else { feedbackMessageElement.innerText = "Puoi fare di meglio! Rileggi i consigli e riprova il quiz."; }

        // Salva progressione e offri attestato
        if (window.GiochiPC) {
            window.GiochiPC.salvaRisultato('quiz-primaria', score, shuffledQuestions.length);
        }
        renderAttestatoBox('quiz-primaria', percentage);
    }

    function renderAttestatoBox(idGioco, percentuale) {
        const box = document.getElementById('attestato-box');
        if (!box) return;
        if (percentuale < 80) {
            box.innerHTML = '<p class="text-muted small mb-0"><i class="bi bi-info-circle me-1" aria-hidden="true"></i> Per ottenere l’attestato devi rispondere correttamente almeno all’80% delle domande.</p>';
            return;
        }
        box.innerHTML = ''
          + '<div class="alert alert-success border-0" style="border-radius:12px;">'
          + '  <p class="mb-2"><strong><i class="bi bi-award-fill me-1" aria-hidden="true"></i> Hai sbloccato il badge!</strong> Vuoi l’attestato di partecipazione?</p>'
          + '  <div class="mb-2">'
          + '    <label for="nome-attestato" class="form-label small">Scrivi il tuo nome (max 40 caratteri):</label>'
          + '    <input type="text" id="nome-attestato" class="form-control" maxlength="40" placeholder="Il tuo nome">'
          + '  </div>'
          + '  <div class="d-flex flex-wrap gap-2 justify-content-center">'
          + '    <button type="button" id="btn-scarica-attestato" class="btn btn-success"><i class="bi bi-download me-1" aria-hidden="true"></i> Scarica attestato</button>'
          + '    <button type="button" id="btn-stampa-attestato" class="btn btn-outline-success"><i class="bi bi-printer me-1" aria-hidden="true"></i> Stampa attestato</button>'
          + '  </div>'
          + '</div>';
        const inp = document.getElementById('nome-attestato');
        document.getElementById('btn-scarica-attestato').addEventListener('click', function(){
            if (window.AttestatoPC) window.AttestatoPC.genera(inp.value, idGioco, percentuale);
        });
        document.getElementById('btn-stampa-attestato').addEventListener('click', function(){
            if (window.AttestatoPC) window.AttestatoPC.stampa(inp.value, idGioco, percentuale);
        });
    }

    function resetState() {
        feedbackBox.classList.add('hide');
        while (answerButtonsElement.firstChild) { answerButtonsElement.removeChild(answerButtonsElement.firstChild); }
        if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
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
