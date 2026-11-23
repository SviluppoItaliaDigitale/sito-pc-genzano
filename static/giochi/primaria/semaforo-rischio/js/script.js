document.addEventListener('DOMContentLoaded', () => {
    const introScreen = document.getElementById('intro-screen');
    const gameScreen = document.getElementById('game-screen');
    const resultScreen = document.getElementById('result-screen');
    const situationText = document.getElementById('situation-text');
    const situationCard = document.getElementById('situation-card');
    const feedback = document.getElementById('feedback');
    const progressBar = document.getElementById('progress-bar');
    const currentQSpan = document.getElementById('current-q');
    const totalQSpan = document.getElementById('total-q');
    const scoreSpan = document.getElementById('score');
    const finalScore = document.getElementById('final-score');
    const finalTotal = document.getElementById('final-total');
    const finalMessage = document.getElementById('final-message');
    const buttons = document.querySelectorAll('.sem-btn');

    const situations = [
        { text: 'Piove leggermente, il cielo è grigio.', answer: 'verde', tip: 'Pioggia leggera: nessun pericolo, vita normale.' },
        { text: 'C\'è un temporale molto forte con fulmini e grandine.', answer: 'rosso', tip: 'Temporale forte: ripararsi subito in un edificio, lontano dalle finestre!' },
        { text: 'Il cielo è nuvoloso e tira un po\' di vento.', answer: 'verde', tip: 'Nuvole e vento leggero: niente di preoccupante.' },
        { text: 'Senti un forte odore di gas in cucina.', answer: 'rosso', tip: 'Fuga di gas! Apri le finestre, esci e chiama un adulto. Non toccare gli interruttori!' },
        { text: 'La radio dice che domani sono previste piogge intense.', answer: 'giallo', tip: 'Allerta prevista: preparati, evita zone a rischio e tieniti informato.' },
        { text: 'Stai giocando al parco e fa bel tempo.', answer: 'verde', tip: 'Tutto tranquillo, divertiti!' },
        { text: 'Vedi del fumo uscire da un bosco vicino.', answer: 'rosso', tip: 'Possibile incendio! Allontanati e chiama subito il 112, il numero unico di emergenza.' },
        { text: 'È uscita un\'allerta rossa per rischio alluvione.', answer: 'rosso', tip: 'Allerta rossa: fenomeni molto intensi, resta al sicuro e segui le indicazioni del Comune!' },
        { text: 'Fa molto caldo, il termometro segna 38 gradi.', answer: 'giallo', tip: 'Ondata di calore: bevi acqua, resta all\'ombra nelle ore più calde (11-18).' },
        { text: 'La terra trema per qualche secondo.', answer: 'rosso', tip: 'Terremoto! Riparati sotto un tavolo, proteggiti la testa. Non uscire durante la scossa.' },
        { text: 'Il meteo prevede neve in montagna domani.', answer: 'verde', tip: 'Neve in montagna: normale in inverno. Attenzione se devi viaggiare.' },
        { text: 'L\'acqua del fosso vicino a casa sta salendo velocemente.', answer: 'rosso', tip: 'Rischio alluvione! Vai ai piani alti e non avvicinarti al fosso.' },
        { text: 'C\'è vento forte e oggetti che volano in strada.', answer: 'giallo', tip: 'Vento forte: resta in casa se puoi, stai lontano da alberi e cartelloni.' },
        { text: 'Il tuo vicino anziano non risponde da ieri e fa molto caldo.', answer: 'rosso', tip: 'Potrebbe stare male per il caldo! Chiama il 112 o chiedi aiuto a un adulto.' },
        { text: 'La maestra dice che oggi si fa la prova di evacuazione.', answer: 'giallo', tip: 'Esercitazione: segui le istruzioni con attenzione, è un\'occasione per imparare!' },
        { text: 'Un\'amica ti mostra un video allarmante sui social.', answer: 'giallo', tip: 'Attenzione alle fake news! Verifica sempre le notizie sulle fonti ufficiali.' },
        { text: 'Sei in macchina e il sottopassaggio è pieno d\'acqua.', answer: 'rosso', tip: 'Non entrare mai! Torna indietro e cerca un\'altra strada.' },
        { text: 'È una bella giornata di sole, sei a scuola.', answer: 'verde', tip: 'Tutto tranquillo, buona giornata!' },
        { text: 'Senti la sirena dei vigili del fuoco passare in strada.', answer: 'giallo', tip: 'Stanno andando a un intervento. Resta attento e lascia libera la strada.' },
        { text: 'Le luci di casa si spengono all\'improvviso.', answer: 'giallo', tip: 'Blackout: usa una torcia (non candele), controlla se è solo casa tua o tutto il quartiere.' },
        { text: 'Stai facendo merenda all\'uscita di scuola.', answer: 'verde', tip: 'Tutto normale: goditi la merenda!' },
        { text: 'Un cane randagio abbaia forte da un cortile chiuso.', answer: 'verde', tip: 'Abbaia ma è nel cortile: allontanati con calma, non serve il 112.' },
        { text: 'Il termometro ha segnato 41 gradi per 3 giorni di fila.', answer: 'rosso', tip: 'Ondata di calore estrema: evita di uscire tra le 11 e le 18, bevi molto, controlla anziani e bambini.' },
        { text: 'La scuola annuncia che domani c\'è un\'esercitazione antincendio.', answer: 'giallo', tip: 'Esercitazione: preparati ad ascoltare bene il segnale e seguire la maestra.' },
        { text: 'Cammini in montagna e senti un rombo come di tuono, ma il cielo è sereno.', answer: 'rosso', tip: 'Potrebbe essere una frana o una valanga in lontananza! Allontanati dai versanti e avvisa un adulto.' },
        { text: 'È appena iniziato l\'autunno e piove per la prima volta dopo l\'estate.', answer: 'giallo', tip: 'Prima pioggia: il terreno asciutto non la assorbe e le strade possono diventare scivolose.' },
        { text: 'Il papà sta usando il barbecue in giardino con vento forte.', answer: 'rosso', tip: 'Vento forte e fuoco aperto: rischio incendio! Spegnete il barbecue finché non cala il vento.' },
        { text: 'La campanella della scuola suona per la fine delle lezioni.', answer: 'verde', tip: 'È la campanella di tutti i giorni: niente di preoccupante.' },
        { text: 'Un cavo elettrico è caduto a terra in strada dopo un temporale.', answer: 'rosso', tip: 'Pericolosissimo! Non avvicinarti e non toccarlo, avvisa un adulto e chiamate il 112: potrebbe essere sotto tensione.' },
        { text: 'Il bollettino dice "nebbia fitta in pianura domattina".', answer: 'giallo', tip: 'Nebbia: guida piano se ci sei in auto, usa luci adeguate. Per i pedoni niente panico, ma attenzione alle strade.' },
        { text: 'Un compagno a scuola sbatte la testa e ha un piccolo bernoccolo.', answer: 'giallo', tip: 'Avvisa subito la maestra o la bidella. Se sta male, si chiama il 112.' },
        { text: 'Al telegiornale dicono che c\'è stato un terremoto a 300 km da qui.', answer: 'verde', tip: 'Non sei nella zona colpita. Puoi informarti, ma dove sei non c\'è pericolo.' },
        { text: 'Sei in spiaggia e vedi la bandiera rossa esposta.', answer: 'rosso', tip: 'Bandiera rossa: divieto di balneazione! Mare pericoloso, non entrare in acqua.' },
        { text: 'In auto con i genitori vedi una colonna di fumo nero alta nel cielo.', answer: 'rosso', tip: 'Incendio grande in corso: segnalate posizione e fumate chiamando il 112, tenetevi a distanza.' },
        { text: 'Il nonno ha dimenticato il gas acceso ma senza fiamma da 5 minuti.', answer: 'rosso', tip: 'Fuga di gas! Apri le finestre, chiudi il rubinetto del gas, esci e chiama adulti. Non accendere luci.' },
        { text: 'Stai tornando a casa e vedi un vicino di casa stare male per terra.', answer: 'rosso', tip: 'Chiama subito il 112! Descrivi la situazione e non allontanarti fino all\'arrivo dei soccorsi.' },
        { text: 'La neve ha coperto le strade ma mamma deve accompagnarti a scuola.', answer: 'giallo', tip: 'Attenzione: gomme da neve o catene, velocità ridotta. Se c\'è troppo ghiaccio, meglio restare a casa.' },
        { text: 'Allerta meteo gialla per temporali nel pomeriggio.', answer: 'giallo', tip: 'Preparati: evita parchi, stadi, piscine. Se scoppia il temporale, rifugiati in un edificio.' },
        { text: 'Sei a casa e non hai connessione internet da 5 minuti.', answer: 'verde', tip: 'Internet può guastarsi per tanti motivi: aspetta, riavvia il router. Non è un\'emergenza.' },
        { text: 'Vedi un bambino più piccolo di te che sembra essersi perso al supermercato.', answer: 'giallo', tip: 'Chiedigli come si chiama e portalo da un commesso o alla cassa: loro chiameranno al microfono.' },

        // Tema "comunicazione del rischio" — fonti ufficiali + IT-alert + fake news
        { text: 'Tuo cugino ti gira un audio WhatsApp: "ho saputo che stanotte fanno saltare la diga di Nemi!".', answer: 'giallo', tip: 'Attenzione: audio anonimi su WhatsApp = quasi sempre fake news. Non lo inoltri, non ci credi, verifichi sul sito del Comune.' },
        { text: 'Sul cellulare arriva un messaggio "IT-alert" con un suono speciale. Non è un test: è un allarme.', answer: 'rosso', tip: 'IT-alert è un allarme ufficiale per una grave emergenza. Leggi il messaggio con un adulto e segui le indicazioni delle autorità.' },
        { text: 'Un meteorologo TikTok dice: "domani il Lazio sarà colpito da uragano!".', answer: 'giallo', tip: 'Attenzione: TikTok non è fonte ufficiale. Verifica sul sito del Centro Funzionale Regionale: senza allerta ufficiale, è sensazionalismo.' },
        { text: 'Il sindaco di Genzano pubblica un video sui canali ufficiali del Comune: allerta rossa confermata.', answer: 'rosso', tip: 'Comunicazione ufficiale del sindaco: prendi sul serio. Limita gli spostamenti e segui le indicazioni.' },
        { text: 'Su Instagram vedi un post di un negozio "evacuazione totale di Genzano stanotte!" con tante condivisioni.', answer: 'giallo', tip: 'Attenzione: le condivisioni non rendono vera una notizia. Mai un\'evacuazione si comunica via post di un negozio: la comunicano il Comune e la Protezione Civile.' },
        { text: 'Sul sito del Centro Funzionale Regionale Lazio leggi: codice giallo per temporali domani 12-18.', answer: 'giallo', tip: 'Bollettino ufficiale codice giallo: criticità ordinaria. Preparati, ma niente panico.' },
        { text: 'Un amico ti chiede di rilanciare un suo post che chiede preghiere per "il terremoto in arrivo".', answer: 'giallo', tip: 'Attenzione: i terremoti non si possono prevedere. Niente preghiere preventive, niente allarmismo: si chiama "diffondere falsi allarmi".' },
        { text: 'Il bollettino del Ministero della Salute sulle ondate di calore segna il livello più alto per la tua città.', answer: 'rosso', tip: 'Livello più alto: rischio elevato, soprattutto per anziani e bambini. Bevi spesso, evita il sole dalle 11 alle 18, controlla i nonni.' },
        { text: 'Un canale Telegram non ufficiale dice "il Comune sta nascondendo l\'emergenza!".', answer: 'giallo', tip: 'Attenzione: tipico schema cospirazionista. Le emergenze vere vengono comunicate dai canali ufficiali, non "rivelate" da canali anonimi.' },
        { text: 'A scuola la maestra vi chiede di cercare con i genitori dove si leggono le allerte meteo ufficiali.', answer: 'giallo', tip: 'Utile per prepararsi: le allerte del Centro Funzionale Regionale si leggono sul sito della Regione Lazio, nella pagina Allerte meteo di questo sito e sui canali del Comune.' }
    ];

    let queue, index, score, locked;
    // Doppio tocco: `locked` ferma i tasti dopo la risposta; `partita` impedisce
    // che il timer di una partita finita faccia avanzare quella nuova.
    let partita = 0;

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function startGame() {
        partita++;
        introScreen.classList.add('hide');
        resultScreen.classList.add('hide');
        gameScreen.classList.remove('hide');
        queue = shuffle([...situations]).slice(0, 15);
        index = 0; score = 0; locked = false;
        totalQSpan.textContent = queue.length;
        scoreSpan.textContent = 0;
        showSituation();
    }

    function showSituation() {
        locked = false;
        feedback.classList.add('hide');
        feedback.classList.remove('correct', 'wrong');
        situationCard.classList.remove('flash-correct', 'flash-wrong');
        currentQSpan.textContent = index + 1;
        progressBar.style.width = ((index / queue.length) * 100) + '%';
        situationText.textContent = queue[index].text;
        buttons.forEach(b => { b.disabled = false; });
        if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
    }

    function handleAnswer(chosen) {
        if (locked) return;
        locked = true;
        const sit = queue[index];
        const correct = chosen === sit.answer;
        buttons.forEach(b => { b.disabled = true; });
        if (window.AudioSintetico) {
            if (correct) window.AudioSintetico.dingPositivo(); else window.AudioSintetico.tonoNeutro();
        }
        if (correct) {
            score++;
            scoreSpan.textContent = score;
            situationCard.classList.add('flash-correct');
            feedback.className = 'feedback-box correct';
            feedback.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> Giusto! ' + sit.tip;
        } else {
            situationCard.classList.add('flash-wrong');
            feedback.className = 'feedback-box wrong';
            const colorLabel = { verde: 'Verde', giallo: 'Giallo', rosso: 'Rosso' };
            feedback.innerHTML = '<i class="bi bi-x-circle-fill me-1"></i> La risposta era <strong>' + colorLabel[sit.answer] + '</strong>. ' + sit.tip;
            if (window.GameCoach && window.GameCoach.hint) {
                window.GameCoach.hint('Verde = sicuro (lo puoi fare). Giallo = attenzione (rischio basso). Rosso = pericoloso o vietato. Stessa logica dell\'allerta meteo.', '/allerte-meteo/');
            }
        }
        feedback.classList.remove('hide');
        const questa = partita;
        setTimeout(() => {
            if (questa !== partita) return;
            index++;
            if (index < queue.length) { showSituation(); }
            else { showResults(); }
        }, 2500);
    }

    function showResults() {
        gameScreen.classList.add('hide');
        resultScreen.classList.remove('hide');
        finalScore.textContent = score;
        finalTotal.textContent = queue.length;
        const pct = (score / queue.length) * 100;
        if (pct >= 90) finalMessage.textContent = 'Fantastico! Sai riconoscere benissimo i pericoli!';
        else if (pct >= 70) finalMessage.textContent = 'Molto bravo! Hai un buon occhio per la sicurezza.';
        else if (pct >= 50) finalMessage.textContent = 'Non male! Riprova per migliorare ancora.';
        else finalMessage.textContent = 'Puoi fare di meglio! Rileggi i consigli e riprova.';
        if (window.GiochiUtil) window.GiochiUtil.salvaEMostraAttestato('semaforo-rischio', score, queue.length, '#result-screen');
    }

    buttons.forEach(btn => {
        btn.addEventListener('click', () => handleAnswer(btn.dataset.color));
    });

    document.getElementById('start-btn').addEventListener('click', startGame);
    document.getElementById('restart-btn').addEventListener('click', startGame);
});
