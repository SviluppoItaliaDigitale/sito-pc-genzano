/* Anagrammi della Sicurezza — Protezione Civile Genzano
   Randomizzazione: ad ogni partita cambia sia la selezione delle parole
   sia l'ordine delle lettere nel pool. */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Parole divise per difficoltà ───────────────────────────────
  // facile = 4-6 lettere · medio = 7-9 · difficile = 10+
  // Ogni voce: { w: parola (può contenere spazi), cat: categoria, hint:
  //   suggerimento, explain: nota didattica mostrata dopo la risoluzione }.
  const wordBank = {
    facile: [
      { w: 'ZAINO', cat: 'Kit di emergenza', hint: 'Lo porti in spalla con dentro l\'essenziale',
        explain: 'Lo zaino di emergenza domestico ha acqua, cibo a lunga scadenza, torcia, radio a pile, medicine personali. Tieni vicino alla porta.' },
      { w: 'ACQUA', cat: 'Scorta fondamentale', hint: 'Si beve e spegne le fiamme',
        explain: 'In emergenza idrica si parla di almeno 4 litri al giorno per persona, per bere e per l\'igiene minima.' },
      { w: 'CASCO', cat: 'Dispositivo di protezione', hint: 'Protegge la testa del volontario',
        explain: 'Il casco protegge la testa da sassi, rami e oggetti che cadono dall\'alto: i volontari lo indossano nei servizi dove serve.' },
      { w: 'RADIO', cat: 'Comunicazione', hint: 'Trasmette voci anche senza rete cellulare',
        explain: 'Le radio dei volontari (UHF/VHF) funzionano dove la rete telefonica è satura o assente: indispensabili in emergenza.' },
      { w: 'FRANA', cat: 'Rischio del territorio', hint: 'Terreno che scivola a valle',
        explain: 'Nei Castelli Romani i versanti ripidi dei crateri, come quello del lago di Nemi, possono franare con le piogge intense.' },
      { w: 'FUOCO', cat: 'Pericolo', hint: 'Brucia e fa salire fumo',
        explain: 'Mai usare l\'ascensore in caso d\'incendio: usa le scale, copri naso e bocca con un panno bagnato.' },
      { w: 'PIOGGIA', cat: 'Fenomeno meteo', hint: 'Cade dal cielo: se intensa diventa allerta',
        explain: 'Pioggia forte per molte ore = rischio di allagamenti e frane. Il bollettino del Centro Funzionale Regionale del Lazio avvisa prima, con i codici colore.' },
      { w: 'NEVE', cat: 'Fenomeno meteo', hint: 'Bianca, fredda, copre i Castelli d\'inverno',
        explain: 'Allerta neve: il Comune attiva il piano neve, sale antighiaccio in strada, talvolta chiusura scuole.' },
      { w: 'VENTO', cat: 'Fenomeno meteo', hint: 'Quando è forte fa cadere alberi',
        explain: 'Allerta vento (gialla/arancione): chiudi finestre, evita parchi alberati, attenzione a oggetti che volano.' },
      { w: 'AIUTO', cat: 'Soccorso', hint: 'Lo chiedi in caso di pericolo',
        explain: 'In Italia per qualsiasi emergenza si chiama il 112: la centrale unica smista a vigili del fuoco, ambulanza o forze dell\'ordine.' },
      { w: 'SCOSSA', cat: 'Terremoto', hint: 'Movimento improvviso del terreno',
        explain: 'In una scossa: sotto un tavolo robusto, lontano da finestre. Resta lì finché non finisce.' },
      { w: 'TORCIA', cat: 'Kit di emergenza', hint: 'Fa luce al buio durante un blackout',
        explain: 'Sempre meglio una torcia a pile (o a manovella) delle candele: niente fiamme libere = niente incendi domestici.' },
      { w: 'FISCHIO', cat: 'Segnalazione', hint: 'Suono acuto per farsi sentire',
        explain: 'Sotto le macerie un fischietto fa rumore con poco sforzo: utile per essere localizzati dai soccorritori.' },
      { w: 'ALLERTA', cat: 'Avviso', hint: 'Annuncio che un pericolo è atteso',
        explain: 'L\'allerta meteo del Centro Funzionale Regionale Lazio ha 4 livelli: verde, giallo, arancione, rosso.' },
      { w: 'NEMI', cat: 'Castelli Romani', hint: 'Lago di Genzano dentro un cratere',
        explain: 'Il lago di Nemi è in un cratere vulcanico dei Colli Albani, un vulcano quiescente (in pausa, non spento): zona di rischio frana per i versanti ripidi.' },
      { w: 'ELMETTO', cat: 'Dispositivo di protezione', hint: 'Copre la testa in cantiere',
        explain: 'L\'elmetto è un dispositivo di protezione certificato: protegge la testa da sassi, mattoni e calcinacci che cadono.' },
      { w: 'USCITA', cat: 'Via di fuga', hint: 'Dove si va quando suona l\'allarme',
        explain: 'Le uscite di emergenza sono indicate dai cartelli verdi ISO 7010: porta la tua classe lì in fila ordinata.' },
      { w: 'GUANTI', cat: 'Protezione personale', hint: 'Proteggono le mani dei volontari',
        explain: 'I guanti AIB sono ignifughi e in pelle: per spostare macerie si usano guanti rinforzati anti-taglio.' },
      { w: 'MAPPA', cat: 'Orientamento', hint: 'Disegno del territorio per non perdersi',
        explain: 'Le mappe del Piano di Emergenza Comunale segnano vie di fuga, aree di accoglienza, punti critici.' },
      { w: 'BUSSOLA', cat: 'Orientamento', hint: 'Indica sempre il nord',
        explain: 'Senza GPS, una bussola e una mappa cartacea sono ancora oggi i metodi più affidabili in montagna.' },
      { w: 'BATTERIA', cat: 'Kit di emergenza', hint: 'Serve a far funzionare radio e torcia',
        explain: 'Tieni nello zaino pile di scorta: in un blackout lungo radio e torcia restano accese, anche quando il telefono è scarico.' },
      { w: 'CORDA', cat: 'Soccorso', hint: 'Si usa per legare e per calarsi in sicurezza',
        explain: 'Nel soccorso si usano solo corde certificate, controllate prima di ogni servizio: le usano soccorritori formati.' },
      { w: 'COPERTA', cat: 'Kit di emergenza', hint: 'Tiene caldo se fa freddo fuori',
        explain: 'La coperta termica isotermica (oro/argento) riduce la dispersione di calore: leggera, occupa pochissimo spazio.' },
      { w: 'VERDE', cat: 'Codice colore', hint: 'Nessun rischio previsto',
        explain: 'Allerta verde = situazione ordinaria. Non significa "tutto fermo": è il livello base di vigilanza.' },
      { w: 'ROSSO', cat: 'Codice colore', hint: 'Massima attenzione, rischio elevato',
        explain: 'Allerta rossa = fenomeni molto intensi con rischio per la popolazione. Segui le indicazioni del Comune.' },
      { w: 'TUFO', cat: 'Castelli Romani', hint: 'Roccia vulcanica con cui sono fatte molte case di Genzano',
        explain: 'Il tufo di Genzano è una piroclastite dei Colli Albani: poroso, tenero, ha condizionato l\'architettura locale.' },
      { w: 'BOSCO', cat: 'Ambiente', hint: 'D\'estate è a rischio incendio',
        explain: 'D\'estate i boschi sono secchi e il rischio di incendio è alto: a Genzano, nel 2026, il periodo di grave pericolosità va dal 17 giugno al 15 ottobre. Mai accendere fuochi.' }
    ],
    medio: [
      { w: 'VOLONTARIO', cat: 'Protezione Civile', hint: 'Offre tempo e competenze gratis',
        explain: 'Il volontariato di protezione civile fa parte del Servizio nazionale: lo regola il Codice della protezione civile (D.Lgs. 1/2018).' },
      { w: 'EMERGENZA', cat: 'Situazione urgente', hint: 'Richiede interventi immediati',
        explain: 'Emergenza = evento in corso. Diversa dall\'allerta (previsione). Sono fasi distinte del ciclo del rischio.' },
      { w: 'TERREMOTO', cat: 'Rischio sismico', hint: 'La terra trema',
        explain: 'I Castelli Romani sono in zona sismica 2B. L\'INGV monitora 24/7 con sismografi.' },
      { w: 'INCENDIO', cat: 'Rischio AIB', hint: 'Fuoco fuori controllo nei boschi o in casa',
        explain: 'Per gli incendi boschivi (AIB) chiama il 112: la centrale attiva i Vigili del Fuoco e le squadre AIB regionali.' },
      { w: 'ALLUVIONE', cat: 'Rischio idrogeologico', hint: 'Acqua che invade strade ed edifici',
        explain: 'In alluvione: sali ai piani alti, mai negli scantinati. Mai attraversare sottopassi allagati in macchina.' },
      { w: 'SICUREZZA', cat: 'Obiettivo PC', hint: 'Stare lontani dai pericoli',
        explain: 'La sicurezza si costruisce insieme: le attività della protezione civile sono previsione, prevenzione, gestione dell\'emergenza e superamento (D.Lgs. 1/2018).' },
      { w: 'PREVENZIONE', cat: 'Protezione Civile', hint: 'Evitare che il pericolo diventi danno',
        explain: 'La prevenzione è la prima missione della PC (D.Lgs. 1/2018, Codice). Costa meno di ricostruire.' },
      { w: 'BOLLETTINO', cat: 'Comunicazione', hint: 'Previsioni e avvisi ufficiali del CFR',
        explain: 'Il bollettino di criticità del Centro Funzionale Regionale Lazio è pubblicato ogni giorno, di norma entro le 14:00.' },
      { w: 'SEGNALE', cat: 'Comunicazione', hint: 'Serve ad avvisare di un pericolo',
        explain: 'I segnali ISO 7010 sono internazionali: codice colore + forma indicano la natura del pericolo.' },
      { w: 'RIFUGIO', cat: 'Luogo sicuro', hint: 'Posto strutturato per ripararsi in emergenza',
        explain: 'In emergenza il Comune indica le aree e le strutture dove trovare riparo e assistenza: sono scritte nel piano di protezione civile comunale.' },
      { w: 'MASCHERINA', cat: 'Protezione', hint: 'Copre naso e bocca, utile in caso di fumo',
        explain: 'Con fumo o polvere nell\'aria una mascherina FFP2 trattiene le particelle più fini. Non protegge dai gas.' },
      { w: 'IDRANTE', cat: 'Antincendio', hint: 'Da qui i pompieri prendono l\'acqua',
        explain: 'Gli idranti antincendio in strada vanno tenuti liberi: chi parcheggia davanti rischia una multa.' },
      { w: 'SOCCORSO', cat: 'Aiuto in emergenza', hint: 'Chi corre ad aiutare i feriti',
        explain: 'Il primo gesto di soccorso è chiamare il 112. Gli adulti formati sanno fare anche il massaggio cardiaco in attesa dell\'ambulanza.' },
      { w: 'ESTINTORE', cat: 'Antincendio', hint: 'Spegne piccole fiamme',
        explain: 'L\'estintore deve essere a portata di mano e controllato da un tecnico ogni sei mesi. Solo gli adulti formati lo usano.' },
      { w: 'ASCENSORE', cat: 'Da evitare', hint: 'Mai durante un\'evacuazione',
        explain: 'In sisma o incendio, l\'ascensore può bloccarsi tra i piani. Sempre le scale, mai l\'ascensore.' },
      { w: 'CAPOFILA', cat: 'Evacuazione', hint: 'Guida la fila della classe',
        explain: 'Il capofila (apri-fila) è scelto dall\'insegnante e guida la classe; l\'ultimo (chiudi-fila) controlla che nessuno resti indietro.' },
      { w: 'DOCUMENTI', cat: 'Evacuazione', hint: 'Carta d\'identità e tessera sanitaria',
        explain: 'In evacuazione veloce porta solo documenti + cellulare + medicine personali. Tutto il resto si recupera dopo.' },
      { w: 'VIGILANZA', cat: 'Controllo', hint: 'Osservare per prevenire pericoli',
        explain: 'In allerta arancione/rossa, i volontari fanno turni di vigilanza ai punti critici (sottopassi, argini, versanti).' },
      { w: 'PRESIDIO', cat: 'Postazione operativa', hint: 'Posto dove si presta servizio',
        explain: 'Un presidio è un posto dove soccorritori o volontari restano in servizio per controllare una zona o aiutare le persone.' },
      { w: 'CENTRALE', cat: 'Coordinamento', hint: 'Da qui si dirigono gli interventi',
        explain: 'La Sala Operativa di PC (Comune o Regione) coordina mezzi, volontari, comunicazioni in emergenza.' },
      { w: 'BINOCOLO', cat: 'Osservazione', hint: 'Serve a vedere lontano',
        explain: 'Sui versanti boscati a rischio AIB i volontari osservano dai punti panoramici col binocolo, alla ricerca di fumo.' },
      { w: 'CRATERE', cat: 'Castelli Romani', hint: 'Buco circolare di un vulcano',
        explain: 'Il cratere del lago di Nemi appartiene al complesso vulcanico dei Colli Albani: non è spento, è in pausa ed è sorvegliato dagli scienziati.' },
      { w: 'VULCANO', cat: 'Rischio territorio', hint: 'Montagna che può eruttare',
        explain: 'Il vulcano dei Colli Albani è classificato "quiescente": l\'ultima eruzione risale a circa 36.000 anni fa, ma ci sono ancora piccoli terremoti.' },
      { w: 'PIANO FAMILIARE', cat: 'Preparazione domestica', hint: 'Cosa fa ciascuno in caso di emergenza',
        explain: 'Il piano familiare risponde a 4 domande: chi fa cosa? dove ci ritroviamo? chi avvisiamo? cosa portiamo? Stampalo e tienilo a casa.' },
      { w: 'PUNTO RACCOLTA', cat: 'Sicurezza', hint: 'Dove ci si ritrova dopo l\'evacuazione',
        explain: 'Il punto di raccolta a scuola è in cortile, segnalato dal cartello ISO verde. Nessuno torna in classe a prendere lo zaino.' }
    ],
    difficile: [
      { w: 'EVACUAZIONE', cat: 'Azione di emergenza', hint: 'Tutti fuori in fila e con calma',
        explain: 'L\'evacuazione segue il Piano di Emergenza Scolastico: fila ordinata, capofila con giubbino, conta dei presenti al punto di raccolta.' },
      { w: 'AUTOPROTEZIONE', cat: 'Comportamento', hint: 'Difendere se stessi con i gesti giusti',
        explain: 'L\'autoprotezione è la prima difesa: conoscere i rischi del proprio territorio e sapere che cosa fare prima, durante e dopo un\'emergenza.' },
      { w: 'IDROGEOLOGICO', cat: 'Rischio', hint: 'Acqua + terreno che frana',
        explain: 'Il rischio idrogeologico riguarda frane e alluvioni. Le mappe ufficiali delle zone a rischio sono sulla piattaforma IdroGEO dell\'ISPRA.' },
      { w: 'COMUNICAZIONE', cat: 'Informazione', hint: 'Avvisare e coordinare in emergenza',
        explain: 'In emergenza la comunicazione usa solo fonti ufficiali: Comune, Centro Funzionale Regionale, Dipartimento della Protezione Civile.' },
      { w: 'TEMPORALE', cat: 'Fenomeno meteo', hint: 'Tuoni, fulmini e pioggia intensa',
        explain: 'In temporale: dentro casa, lontano da finestre, doccia, oggetti elettrici. Niente telefono fisso.' },
      { w: 'BOSCHIVO', cat: 'Rischio AIB', hint: 'Incendio che colpisce i boschi',
        explain: 'Gli incendi boschivi sono regolati dalla Legge 353/2000. Appiccare un incendio a un bosco è un reato grave: per l\'incendio doloso il Codice penale prevede fino a 10 anni di carcere.' },
      { w: 'ANTINCENDIO', cat: 'Prevenzione', hint: 'Tutto ciò che serve a contrastare il fuoco',
        explain: 'Contro gli incendi boschivi lavorano insieme Vigili del Fuoco, squadre regionali, mezzi aerei e volontari antincendio boschivo.' },
      { w: 'COORDINAMENTO', cat: 'Organizzazione', hint: 'Lavorare insieme senza confusione',
        explain: 'Il coordinamento PC ha più livelli: COC (Comune), COM (intercomunale), CCS (Provinciale), DI.COMA.C (nazionale).' },
      { w: 'RADIO COMUNICAZIONE', cat: 'Strumento PC', hint: 'Messaggi via radio tra le squadre',
        explain: 'Il Gruppo Comunale di Genzano ha la sezione Radiocomunicazioni: rete UHF/VHF dedicata, indipendente dalla rete cellulare.' },
      { w: 'SORVEGLIANZA', cat: 'Controllo', hint: 'Tenere d\'occhio una zona a rischio',
        explain: 'In allerta rossa, i volontari sorvegliano argini, sottopassi, scarpate frana. Turni 24/7 fino a fine evento.' },
      { w: 'ESONDAZIONE', cat: 'Rischio idrogeologico', hint: 'Il fiume esce dal letto',
        explain: 'In esondazione: sali ai piani alti, mai attraversare in macchina. Circa 30 cm d\'acqua che scorre portano via la maggior parte delle auto.' },
      { w: 'PROTEZIONE CIVILE', cat: 'Sistema nazionale', hint: 'Tutti gli enti che gestiscono le emergenze',
        explain: 'Il Servizio nazionale della protezione civile è regolato dal D.Lgs. 1/2018 (Codice): ne fanno parte Stato, Regioni, Comuni e volontariato.' },
      { w: 'VOLONTARIATO', cat: 'Donare tempo', hint: 'Aiuto gratuito alla comunità',
        explain: 'Il volontariato di PC nel Lazio è coordinato dalla Regione Lazio - Direzione Protezione Civile, con Albo Regionale.' },
      { w: 'AUTOMEZZO', cat: 'Mezzo operativo', hint: 'Veicolo dei volontari',
        explain: 'I volontari usano automezzi attrezzati per portare persone, materiali e attrezzature dove servono.' },
      { w: 'CARTOGRAFIA', cat: 'Mappe del territorio', hint: 'Disegno scientifico del territorio',
        explain: 'La cartografia dei rischi è consultabile sulla piattaforma IdroGEO di ISPRA e sul Geoportale della Regione Lazio.' },
      { w: 'SICUREZZA SCOLASTICA', cat: 'Piano d\'emergenza', hint: 'Regole per evacuare le scuole',
        explain: 'Il Piano di Emergenza Scolastico è obbligatorio per ogni istituto: 2 prove di evacuazione l\'anno + addestramento docenti.' },
      { w: 'SISMOGRAFO', cat: 'Strumento scientifico', hint: 'Registra i movimenti della terra',
        explain: 'L\'INGV ha in Italia la Rete Sismica Nazionale, con circa 500 stazioni: dai loro dati calcola magnitudo, profondità ed epicentro.' },
      { w: 'METEOROLOGIA', cat: 'Scienza del tempo', hint: 'Studia e prevede il tempo atmosferico',
        explain: 'In Italia la fonte ufficiale meteo per la PC è il Centro Funzionale Regionale (CFR) di ogni Regione, integrato con Aeronautica.' },
      { w: 'IT ALERT', cat: 'Allarme pubblico', hint: 'Sistema italiano che manda allarmi ai cellulari',
        explain: 'IT-alert è operativo dal 2024: invia un messaggio cell broadcast ai cellulari accesi nell\'area di pericolo, in italiano e in inglese.' },
      { w: 'ALLERTAMENTO', cat: 'Sistema di allerta', hint: 'Il sistema che avvisa prima che arrivi il pericolo',
        explain: 'Il sistema di allertamento nazionale segue la Direttiva PCM 27/02/2004: i Centri Funzionali emettono i bollettini con i codici colore.' }
    ]
  };

  // ─── Stato ─────────────────────────────────────────────────────
  let selectedLevel = 'facile';
  let selectedCount = 5;
  let roundWords = [];        // parole di questa partita
  let currentIndex = 0;
  let score = 0;
  let hintsLeft = 3;
  let answerSequence = [];    // storia delle lettere inserite (per undo)
  let currentWord = '';       // parola target (con spazi conservati)
  let solvedThisWord = false;
  let hintsUsedThisWord = 0;  // la penalità degli aiuti vale solo per la parola in cui li usi
  // Doppio tocco: dopo una parola sbagliata i tasti restano fermi finché le
  // caselle non si svuotano; dopo «Prossima parola» un secondo tocco non salta parole.
  let inPassaggio = false;
  let partita = 0;

  const suono = (giusta) => {
    if (!window.AudioSintetico) return;
    if (giusta) window.AudioSintetico.dingPositivo(); else window.AudioSintetico.tonoNeutro();
  };

  // ─── Elementi DOM ──────────────────────────────────────────────
  const startScreen   = document.getElementById('start-screen');
  const gameScreen    = document.getElementById('game-screen');
  const resultsScreen = document.getElementById('results-screen');
  const startBtn      = document.getElementById('start-btn');
  const restartBtn    = document.getElementById('restart-btn');
  const currentWSpan  = document.getElementById('current-w');
  const totalWSpan    = document.getElementById('total-w');
  const scoreLive     = document.getElementById('score-live');
  const progressFill  = document.getElementById('progress-fill');
  const hintText      = document.getElementById('hint-text');
  const categoryText  = document.getElementById('category-text');
  const answerSlots   = document.getElementById('answer-slots');
  const letterPool    = document.getElementById('letter-pool');
  const feedbackBox   = document.getElementById('feedback-box');
  const undoBtn       = document.getElementById('undo-btn');
  const resetBtn      = document.getElementById('reset-btn');
  const hintBtn       = document.getElementById('hint-btn');
  const hintsLeftSpan = document.getElementById('hints-left');
  const nextBtn       = document.getElementById('next-btn');
  const scoreSpan     = document.getElementById('score');
  const maxScoreSpan  = document.getElementById('max-score');
  const feedbackMsg   = document.getElementById('feedback-message');

  // ─── Helpers ───────────────────────────────────────────────────
  const shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  const pickWords = (level, count) => {
    const bank = wordBank[level] || wordBank.facile;
    const shuffled = shuffle(bank);
    return shuffled.slice(0, Math.min(count, shuffled.length));
  };

  // Mescola le lettere assicurandosi che NON siano nell'ordine originale
  const shuffleLetters = (word) => {
    const letters = word.replace(/\s+/g, '').split('');
    if (letters.length < 2) return letters;
    let out;
    let attempts = 0;
    do {
      out = shuffle(letters);
      attempts++;
    } while (out.join('') === letters.join('') && attempts < 20);
    return out;
  };

  // ─── Selettori difficoltà e conteggio ──────────────────────────
  document.querySelectorAll('.difficulty-selector .btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.difficulty-selector .btn').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-checked', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-checked', 'true');
      selectedLevel = btn.dataset.level;
    });
  });
  document.querySelectorAll('.count-selector .btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.count-selector .btn').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-checked', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-checked', 'true');
      selectedCount = parseInt(btn.dataset.count, 10);
    });
  });

  // ─── Avvio / riavvio ───────────────────────────────────────────
  const startGame = () => {
    partita++;
    roundWords = pickWords(selectedLevel, selectedCount);
    currentIndex = 0;
    score = 0;
    hintsLeft = 3;
    hintsLeftSpan.textContent = hintsLeft;
    totalWSpan.textContent = roundWords.length;
    startScreen.classList.add('hide');
    resultsScreen.classList.add('hide');
    gameScreen.classList.remove('hide');
    loadWord();
  };

  const loadWord = () => {
    solvedThisWord = false;
    inPassaggio = false;
    hintsUsedThisWord = 0;
    answerSequence = [];
    feedbackBox.classList.add('hide');
    feedbackBox.classList.remove('correct', 'wrong');
    feedbackBox.textContent = '';
    nextBtn.classList.add('hide');

    const entry = roundWords[currentIndex];
    currentWord = entry.w.toUpperCase();
    categoryText.textContent = entry.cat;
    hintText.textContent = 'Suggerimento: ' + entry.hint;

    currentWSpan.textContent = currentIndex + 1;
    scoreLive.textContent = 'Punti: ' + score;
    progressFill.style.width = ((currentIndex) / roundWords.length * 100) + '%';

    buildSlots();
    buildPool();
  };

  const buildSlots = () => {
    answerSlots.innerHTML = '';
    for (const ch of currentWord) {
      const slot = document.createElement('div');
      if (ch === ' ') {
        slot.className = 'slot space';
        slot.setAttribute('aria-hidden', 'true');
      } else {
        slot.className = 'slot';
        slot.setAttribute('role', 'button');
        slot.setAttribute('tabindex', '-1');
        slot.setAttribute('aria-label', 'Casella vuota');
        slot.addEventListener('click', () => {
          // permette di rimuovere la lettera cliccando lo slot pieno
          if (slot.classList.contains('filled') && !solvedThisWord && !inPassaggio) {
            const idx = [...answerSlots.children].filter(c => !c.classList.contains('space')).indexOf(slot);
            removeLetterAt(idx);
          }
        });
      }
      answerSlots.appendChild(slot);
    }
  };

  const buildPool = () => {
    letterPool.innerHTML = '';
    const letters = shuffleLetters(currentWord);
    letters.forEach((letter, i) => {
      const tile = document.createElement('button');
      tile.type = 'button';
      tile.className = 'letter-tile';
      tile.textContent = letter;
      tile.dataset.index = i;
      tile.setAttribute('aria-label', 'Lettera ' + letter);
      tile.addEventListener('click', () => placeLetter(tile));
      letterPool.appendChild(tile);
    });
  };

  // Inserisci la lettera nel primo slot disponibile
  const placeLetter = (tile) => {
    if (solvedThisWord || inPassaggio || tile.disabled) return;
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    const target = slots.find(s => !s.classList.contains('filled'));
    if (!target) return;
    const letter = tile.textContent;
    target.textContent = letter;
    target.classList.add('filled');
    target.setAttribute('aria-label', 'Lettera ' + letter);
    tile.classList.add('used');
    tile.disabled = true;
    answerSequence.push({ tileIndex: tile.dataset.index, slot: target });
    checkComplete();
  };

  const removeLetterAt = (letterIndexInSlots) => {
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    const slot = slots[letterIndexInSlots];
    if (!slot || !slot.classList.contains('filled')) return;
    // trova l'entry più recente che corrisponde a questo slot
    const entryIdx = [...answerSequence].reverse().findIndex(e => e.slot === slot);
    if (entryIdx === -1) return;
    const realIdx = answerSequence.length - 1 - entryIdx;
    const entry = answerSequence.splice(realIdx, 1)[0];
    slot.textContent = '';
    slot.classList.remove('filled', 'correct', 'wrong');
    slot.setAttribute('aria-label', 'Casella vuota');
    const tile = letterPool.querySelector(`.letter-tile[data-index="${entry.tileIndex}"]`);
    if (tile) { tile.classList.remove('used'); tile.disabled = false; }
  };

  const undoLast = () => {
    if (!answerSequence.length || solvedThisWord || inPassaggio) return;
    const entry = answerSequence.pop();
    entry.slot.textContent = '';
    entry.slot.classList.remove('filled', 'correct', 'wrong');
    entry.slot.setAttribute('aria-label', 'Casella vuota');
    const tile = letterPool.querySelector(`.letter-tile[data-index="${entry.tileIndex}"]`);
    if (tile) { tile.classList.remove('used'); tile.disabled = false; }
  };

  const resetWord = () => {
    if (solvedThisWord || inPassaggio) return;
    answerSequence = [];
    [...answerSlots.children].forEach(s => {
      if (!s.classList.contains('space')) {
        s.textContent = '';
        s.classList.remove('filled', 'correct', 'wrong');
        s.setAttribute('aria-label', 'Casella vuota');
      }
    });
    [...letterPool.children].forEach(t => {
      t.classList.remove('used');
      t.disabled = false;
    });
    feedbackBox.classList.add('hide');
  };

  // Aiuto: riempie la prossima casella con la lettera giusta
  const useHint = () => {
    if (hintsLeft <= 0 || solvedThisWord || inPassaggio) return;
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    const wordLetters = currentWord.replace(/\s+/g, '').split('');
    // trova il primo slot vuoto
    const firstEmptyIdx = slots.findIndex(s => !s.classList.contains('filled'));
    if (firstEmptyIdx === -1) return;
    const neededLetter = wordLetters[firstEmptyIdx];
    // se lo slot successivo è errato (già pieno) lo svuotiamo (non dovrebbe succedere qui)
    // trova una tile non usata con quella lettera
    const tile = [...letterPool.children].find(t => !t.classList.contains('used') && t.textContent === neededLetter);
    if (!tile) return;
    hintsLeft -= 1;
    hintsUsedThisWord += 1;
    hintsLeftSpan.textContent = hintsLeft;
    placeLetter(tile);
  };

  const checkComplete = () => {
    const slots = [...answerSlots.children].filter(c => !c.classList.contains('space'));
    if (slots.every(s => s.classList.contains('filled'))) {
      const built = slots.map(s => s.textContent).join('');
      const target = currentWord.replace(/\s+/g, '');
      if (built === target) {
        solvedThisWord = true;
        slots.forEach(s => s.classList.add('correct'));
        const pointsBase = currentWord.replace(/\s+/g, '').length * 10;
        const hintPenalty = hintsUsedThisWord * 5;
        const earned = Math.max(pointsBase - hintPenalty, 10);
        score += earned;
        scoreLive.textContent = 'Punti: ' + score;
        feedbackBox.classList.remove('hide', 'wrong');
        feedbackBox.classList.add('correct');
        // Feedback con spiegazione didattica (quando presente nella voce):
        // serve a fissare la nozione, non solo a celebrare il +punti.
        const entry = roundWords[currentIndex];
        let html = `<div class="feedback-head"><i class="bi bi-check-circle-fill" aria-hidden="true"></i> Bravissimo! +${earned} punti</div>`;
        if (entry && entry.explain) {
          html += `<p class="feedback-explain"><strong>${entry.w}:</strong> ${entry.explain}</p>`;
        }
        feedbackBox.innerHTML = html;
        suono(true);
        if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
        nextBtn.classList.remove('hide');
        nextBtn.focus();
      } else {
        slots.forEach(s => s.classList.add('wrong'));
        feedbackBox.classList.remove('hide', 'correct');
        feedbackBox.classList.add('wrong');
        feedbackBox.innerHTML = '<i class="bi bi-x-circle-fill" aria-hidden="true"></i> Non è corretto. Riprova!';
        suono(false);
        inPassaggio = true;
        const questa = partita;
        if (window.GameCoach && window.GameCoach.hint) {
          window.GameCoach.hint('Le parole sono tutte legate alla Protezione Civile. Conta le lettere e pensa alla definizione: il glossario del sito ha quasi tutte le parole.', '/glossario/');
        }
        // sblocca le tile per farle riposizionare
        setTimeout(() => {
          if (questa !== partita || solvedThisWord) return;
          inPassaggio = false;
          resetWord();
        }, 900);
      }
    }
  };

  const nextWord = () => {
    // Un secondo tocco su «Prossima parola» (o Invio ripetuto) non salta parole.
    if (!solvedThisWord || nextBtn.classList.contains('hide')) return;
    nextBtn.classList.add('hide');
    currentIndex += 1;
    if (currentIndex >= roundWords.length) {
      showResults();
    } else {
      loadWord();
    }
  };

  const showResults = () => {
    gameScreen.classList.add('hide');
    resultsScreen.classList.remove('hide');
    // punteggio massimo = somma (lunghezza * 10) senza penalità
    const max = roundWords.reduce((s, e) => s + e.w.replace(/\s+/g, '').length * 10, 0);
    scoreSpan.textContent = score;
    maxScoreSpan.textContent = max;
    const perc = max > 0 ? (score / max) : 0;
    let msg;
    if (perc >= 0.9)      msg = 'Perfetto! Sei pronto a unirti ai volontari!';
    else if (perc >= 0.7) msg = 'Ottimo lavoro! Conosci bene le parole della sicurezza.';
    else if (perc >= 0.5) msg = 'Bene! Continua a esercitarti per migliorare.';
    else                  msg = 'Non mollare! Ogni partita è un passo avanti.';
    feedbackMsg.textContent = msg;
    if (window.GiochiUtil) window.GiochiUtil.salvaEMostraAttestato('anagrammi', score, max, '#results-screen');
  };

  // ─── Listener ──────────────────────────────────────────────────
  startBtn.addEventListener('click', startGame);
  restartBtn.addEventListener('click', () => {
    partita++;
    resultsScreen.classList.add('hide');
    startScreen.classList.remove('hide');
  });
  undoBtn.addEventListener('click', undoLast);
  resetBtn.addEventListener('click', resetWord);
  hintBtn.addEventListener('click', useHint);
  nextBtn.addEventListener('click', nextWord);

  // Tastiera: lettere fisiche digitate inseriscono la prima tile disponibile
  document.addEventListener('keydown', (e) => {
    if (gameScreen.classList.contains('hide')) return;
    if (e.key === 'Enter' && !nextBtn.classList.contains('hide')) { e.preventDefault(); nextWord(); return; }
    if (solvedThisWord) return;
    if (e.key === 'Backspace') { e.preventDefault(); undoLast(); return; }
    const key = (e.key || '').toUpperCase();
    if (!/^[A-Z]$/.test(key)) return;
    const tile = [...letterPool.children].find(t => !t.classList.contains('used') && t.textContent === key);
    if (tile) { e.preventDefault(); placeLetter(tile); }
  });

});
