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
        { text: 'Piove leggermente, il cielo e grigio.', answer: 'verde', tip: 'Pioggia leggera: nessun pericolo, vita normale.' },
        { text: 'C\'e un temporale molto forte con fulmini e grandine.', answer: 'rosso', tip: 'Temporale forte: ripararsi subito in un edificio, lontano dalle finestre!' },
        { text: 'Il cielo e nuvoloso e tira un po\' di vento.', answer: 'verde', tip: 'Nuvole e vento leggero: niente di preoccupante.' },
        { text: 'Senti un forte odore di gas in cucina.', answer: 'rosso', tip: 'Fuga di gas! Apri le finestre, esci e chiama un adulto. Non toccare gli interruttori!' },
        { text: 'La radio dice che domani sono previste piogge intense.', answer: 'giallo', tip: 'Allerta prevista: preparati, evita zone a rischio e tieniti informato.' },
        { text: 'Stai giocando al parco e fa bel tempo.', answer: 'verde', tip: 'Tutto tranquillo, divertiti!' },
        { text: 'Vedi del fumo uscire da un bosco vicino.', answer: 'rosso', tip: 'Possibile incendio! Allontanati e chiama subito il 112, il numero unico di emergenza.' },
        { text: 'E uscita un\'allerta arancione per rischio alluvione.', answer: 'rosso', tip: 'Allerta arancione: fenomeni intensi, resta al sicuro e segui le indicazioni!' },
        { text: 'Fa molto caldo, il termometro segna 38 gradi.', answer: 'giallo', tip: 'Ondata di calore: bevi acqua, resta all\'ombra nelle ore piu calde (11-17).' },
        { text: 'La terra trema per qualche secondo.', answer: 'rosso', tip: 'Terremoto! Riparati sotto un tavolo, proteggiti la testa. Non uscire durante la scossa.' },
        { text: 'Il meteo prevede neve in montagna domani.', answer: 'verde', tip: 'Neve in montagna: normale in inverno. Attenzione se devi viaggiare.' },
        { text: 'L\'acqua del fosso vicino a casa sta salendo velocemente.', answer: 'rosso', tip: 'Rischio alluvione! Vai ai piani alti e non avvicinarti al fosso.' },
        { text: 'C\'e vento forte e oggetti che volano in strada.', answer: 'giallo', tip: 'Vento forte: resta in casa se puoi, stai lontano da alberi e cartelloni.' },
        { text: 'Il tuo vicino anziano non risponde da ieri e fa molto caldo.', answer: 'rosso', tip: 'Potrebbe stare male per il caldo! Chiama il 112 o chiedi aiuto a un adulto.' },
        { text: 'La maestra dice che oggi si fa la prova di evacuazione.', answer: 'giallo', tip: 'Esercitazione: segui le istruzioni con attenzione, e un\'occasione per imparare!' },
        { text: 'Un\'amica ti mostra un video allarmante sui social.', answer: 'giallo', tip: 'Attenzione alle fake news! Verifica sempre le notizie sulle fonti ufficiali.' },
        { text: 'Sei in macchina e il sottopassaggio e pieno d\'acqua.', answer: 'rosso', tip: 'Non entrare mai! Torna indietro e cerca un\'altra strada.' },
        { text: 'E una bella giornata di sole, sei a scuola.', answer: 'verde', tip: 'Tutto tranquillo, buona giornata!' },
        { text: 'Senti la sirena dei vigili del fuoco passare in strada.', answer: 'giallo', tip: 'Stanno andando a un intervento. Resta attento e lascia libera la strada.' },
        { text: 'Le luci di casa si spengono all\'improvviso.', answer: 'giallo', tip: 'Blackout: usa una torcia (non candele), controlla se e solo casa tua o tutto il quartiere.' },
        { text: 'Stai facendo merenda all\'uscita di scuola.', answer: 'verde', tip: 'Tutto normale: goditi la merenda!' },
        { text: 'Un cane randagio abbaia forte da un cortile chiuso.', answer: 'verde', tip: 'Abbaia ma e nel cortile: allontanati con calma, non serve il 112.' },
        { text: 'Il termometro ha segnato 41 gradi per 3 giorni di fila.', answer: 'rosso', tip: 'Ondata di calore estrema: evita di uscire tra le 11 e le 17, bevi molto, controlla anziani e bambini.' },
        { text: 'La scuola annuncia che domani c\'e un\'esercitazione antincendio.', answer: 'giallo', tip: 'Esercitazione: preparati ad ascoltare bene il segnale e seguire la maestra.' },
        { text: 'Cammini in montagna e senti un rombo come di tuono, ma il cielo e sereno.', answer: 'rosso', tip: 'Potrebbe essere una frana o una valanga in lontananza! Allontanati dai versanti e avvisa un adulto.' },
        { text: 'E appena iniziato l\'autunno e piove per la prima volta dopo l\'estate.', answer: 'giallo', tip: 'Prima pioggia: il terreno asciutto non la assorbe e le strade possono diventare scivolose.' },
        { text: 'Il papa sta usando la barbecue in giardino con vento forte.', answer: 'rosso', tip: 'Vento forte e fuoco aperto: rischio incendio! Spegnete il barbecue finche non cala il vento.' },
        { text: 'La sirena di una casa di riposo suona per 30 secondi a mezzogiorno.', answer: 'verde', tip: 'Spesso e una prova settimanale. Se dura piu a lungo o a orari strani, diventa giallo.' },
        { text: 'Un cavo elettrico e caduto a terra in strada dopo un temporale.', answer: 'rosso', tip: 'Pericolosissimo! Resta lontano almeno 10 metri e chiama subito il 112: potrebbe essere sotto tensione.' },
        { text: 'Il bollettino dice "nebbia fitta in pianura domattina".', answer: 'giallo', tip: 'Nebbia: guida piano se ci sei in auto, usa luci adeguate. Per i pedoni niente panico, ma attenzione alle strade.' },
        { text: 'Un compagno a scuola sbatte la testa e ha un piccolo bernoccolo.', answer: 'giallo', tip: 'Avvisa subito la maestra o la bidella. Se sta male, si chiama il 112.' },
        { text: 'Al telegiornale dicono che c\'e stato un terremoto a 300 km da qui.', answer: 'verde', tip: 'Non sei nella zona colpita. Puoi informarti, ma dove sei non c\'e pericolo.' },
        { text: 'Sei in spiaggia e vedi la bandiera rossa esposta.', answer: 'rosso', tip: 'Bandiera rossa: divieto di balneazione! Mare pericoloso, non entrare in acqua.' },
        { text: 'In auto con i genitori vedi una colonna di fumo nero alta nel cielo.', answer: 'rosso', tip: 'Incendio grande in corso: segnalate posizione e fumate chiamando il 112, tenetevi a distanza.' },
        { text: 'Il nonno ha dimenticato il gas acceso ma senza fiamma da 5 minuti.', answer: 'rosso', tip: 'Fuga di gas! Apri le finestre, chiudi il rubinetto del gas, esci e chiama adulti. Non accendere luci.' },
        { text: 'Stai tornando a casa e vedi un vicino di casa stare male per terra.', answer: 'rosso', tip: 'Chiama subito il 112! Descrivi la situazione e non allontanarti fino all\'arrivo dei soccorsi.' },
        { text: 'La neve ha coperto le strade ma mamma deve accompagnarti a scuola.', answer: 'giallo', tip: 'Attenzione: gomme da neve o catene, velocita ridotta. Se c\'e troppo ghiaccio, meglio restare a casa.' },
        { text: 'Allerta meteo gialla per temporali nel pomeriggio.', answer: 'giallo', tip: 'Preparati: evita parchi, stadi, piscine. Se scoppia il temporale, rifugiati in un edificio.' },
        { text: 'Sei a casa e non hai connessione internet da 5 minuti.', answer: 'verde', tip: 'Internet puo guastarsi per tanti motivi: aspetta, riavvia il router. Non e un\'emergenza.' },
        { text: 'Vedi un bambino piu piccolo di te che sembra essersi perso al supermercato.', answer: 'giallo', tip: 'Chiedigli come si chiama e portalo da un commesso o alla cassa: loro chiameranno al microfono.' },
    ];

    let queue, index, score, locked;

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function startGame() {
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
    }

    function handleAnswer(chosen) {
        if (locked) return;
        locked = true;
        const sit = queue[index];
        const correct = chosen === sit.answer;
        buttons.forEach(b => { b.disabled = true; });
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
        }
        feedback.classList.remove('hide');
        setTimeout(() => {
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
