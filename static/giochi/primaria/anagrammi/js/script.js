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
        explain: 'In emergenza idrica si parla di 3 litri al giorno per persona: 1 per bere, 2 per igiene minima.' },
      { w: 'CASCO', cat: 'Dispositivo di protezione', hint: 'Protegge la testa del volontario',
        explain: 'I caschi dei volontari (tipo cantiere o AIB) proteggono da oggetti fino a 5 kg che cadono dall\'alto.' },
      { w: 'RADIO', cat: 'Comunicazione', hint: 'Trasmette voci anche senza rete cellulare',
        explain: 'Le radio dei volontari (UHF/VHF) funzionano dove la rete telefonica è satura o assente: indispensabili in emergenza.' },
      { w: 'FRANA', cat: 'Rischio del territorio', hint: 'Terreno che scivola a valle',
        explain: 'I Castelli Romani sono a rischio frana medio: i versanti del cratere possono cedere con piogge intense.' },
      { w: 'FUOCO', cat: 'Pericolo', hint: 'Brucia e fa salire fumo',
        explain: 'Mai usare l\'ascensore in caso d\'incendio: usa le scale, copri naso e bocca con un panno bagnato.' },
      { w: 'PIOGGIA', cat: 'Fenomeno meteo', hint: 'Cade dal cielo: se intensa diventa allerta',
        explain: 'Pioggia persistente per molte ore = rischio idrogeologico. Il bollettino del CFR Lazio lo prevede 24h prima.' },
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
        explain: 'Il lago di Nemi è in un cratere vulcanico spento dei Colli Albani: zona di rischio frana per i versanti ripidi.' },
      { w: 'ELMETTO', cat: 'Dispositivo di protezione', hint: 'Copre la testa in cantiere',
        explain: 'L\'elmetto giallo dei volontari di PC è certificato CE: protegge da scarpe, mattoni e calcinacci.' },
      { w: 'USCITA', cat: 'Via di fuga', hint: 'Dove si va quando suona l\'allarme',
        explain: 'Le uscite di emergenza sono indicate dai cartelli verdi ISO 7010: porta la tua classe lì in fila ordinata.' },
      { w: 'GUANTI', cat: 'Protezione personale', hint: 'Proteggono le mani dei volontari',
        explain: 'I guanti AIB sono ignifughi e in pelle: per spostare macerie si usano guanti rinforzati anti-taglio.' },
      { w: 'MAPPA', cat: 'Orientamento', hint: 'Disegno del territorio per non perdersi',
        explain: 'Le mappe del Piano di Emergenza Comunale segnano vie di fuga, aree di accoglienza, punti critici.' },
      { w: 'BUSSOLA', cat: 'Orientamento', hint: 'Indica sempre il nord',
        explain: 'Senza GPS, una bussola e una mappa cartacea sono ancora oggi i metodi più affidabili in montagna.' },
      { w: 'BATTERIA', cat: 'Kit di emergenza', hint: 'Serve a far funzionare radio e torcia',
        explain: 'Tieni nello zaino batterie di scorta: in blackout esteso le ricariche cellulare possono volare via in 1 giorno.' },
      { w: 'CORDA', cat: 'Soccorso', hint: 'Si usa per legare e per calarsi in sicurezza',
        explain: 'I volontari del soccorso alpino o speleo hanno corde dinamiche certificate UIAA: 60-100 metri tipici.' },
      { w: 'COPERTA', cat: 'Kit di emergenza', hint: 'Tiene caldo se fa freddo fuori',
        explain: 'La coperta termica isotermica (oro/argento) riduce la dispersione di calore: leggera, occupa pochissimo spazio.' },
      { w: 'VERDE', cat: 'Codice colore', hint: 'Nessun rischio previsto',
        explain: 'Allerta verde = situazione ordinaria. Non significa "tutto fermo": è il livello base di vigilanza.' },
      { w: 'ROSSO', cat: 'Codice colore', hint: 'Massima attenzione, rischio elevato',
        explain: 'Allerta rossa = fenomeni molto intensi con rischio per la popolazione. Segui le indicazioni del Comune.' },
      { w: 'TUFO', cat: 'Castelli Romani', hint: 'Roccia vulcanica con cui sono fatte molte case di Genzano',
        explain: 'Il tufo di Genzano è una piroclastite dei Colli Albani: poroso, tenero, ha condizionato l\'architettura locale.' },
      { w: 'BOSCO', cat: 'Ambiente', hint: 'D\'estate è a rischio incendio',
        explain: 'Nei boschi del Lazio luglio-settembre è il periodo di massima pericolosità AIB: mai accendere fuochi.' }
    ],
    medio: [
      { w: 'VOLONTARIO', cat: 'Protezione Civile', hint: 'Offre tempo e competenze gratis',
        explain: 'Il volontariato di PC è regolato dal Codice del Terzo Settore (D.Lgs. 117/2017) e iscritto all\'Albo Regionale.' },
      { w: 'EMERGENZA', cat: 'Situazione urgente', hint: 'Richiede interventi immediati',
        explain: 'Emergenza = evento in corso. Diversa dall\'allerta (previsione). Sono fasi distinte del ciclo del rischio.' },
      { w: 'TERREMOTO', cat: 'Rischio sismico', hint: 'La terra trema',
        explain: 'I Castelli Romani sono in zona sismica 2B (sismicità media). L\'INGV monitora 24/7 con sismografi.' },
      { w: 'INCENDIO', cat: 'Rischio AIB', hint: 'Fuoco fuori controllo nei boschi o in casa',
        explain: 'Per gli incendi boschivi (AIB) chiama il 112: la centrale smista al 1515 (CFS) e all\'AIB regionale.' },
      { w: 'ALLUVIONE', cat: 'Rischio idrogeologico', hint: 'Acqua che invade strade ed edifici',
        explain: 'In alluvione: sali ai piani alti, mai negli scantinati. Mai attraversare sottopassi allagati in macchina.' },
      { w: 'SICUREZZA', cat: 'Obiettivo PC', hint: 'Stare lontani dai pericoli',
        explain: 'La sicurezza è un risultato: deriva da prevenzione + preparazione + risposta + ricostruzione (4 fasi DPC).' },
      { w: 'PREVENZIONE', cat: 'Protezione Civile', hint: 'Evitare che il pericolo diventi danno',
        explain: 'La prevenzione è la prima missione della PC (D.Lgs. 1/2018, Codice). Costa meno di ricostruire.' },
      { w: 'BOLLETTINO', cat: 'Comunicazione', hint: 'Previsioni e avvisi ufficiali del CFR',
        explain: 'Il bollettino di criticità del Centro Funzionale Regionale Lazio è pubblicato ogni giorno alle 13:00.' },
      { w: 'SEGNALE', cat: 'Comunicazione', hint: 'Serve ad avvisare di un pericolo',
        explain: 'I segnali ISO 7010 sono internazionali: codice colore + forma indicano la natura del pericolo.' },
      { w: 'RIFUGIO', cat: 'Luogo sicuro', hint: 'Posto strutturato per ripararsi in emergenza',
        explain: 'I rifugi antiaerei della WWII oggi sono dismessi. Per emergenze attuali si usano edifici scolastici antisismici.' },
      { w: 'MASCHERINA', cat: 'Protezione', hint: 'Copre naso e bocca, utile in caso di fumo',
        explain: 'In incendio o smog post-eruzione: una mascherina FFP2 trattiene il particolato fine PM2.5.' },
      { w: 'IDRANTE', cat: 'Antincendio', hint: 'Da qui i pompieri prendono l\'acqua',
        explain: 'Gli idranti antincendio in strada vanno tenuti liberi: chi parcheggia davanti rischia una multa.' },
      { w: 'SOCCORSO', cat: 'Aiuto in emergenza', hint: 'Chi corre ad aiutare i feriti',
        explain: 'Il primo soccorso si chiama BLS (Basic Life Support): massaggio cardiaco e ventilazioni in attesa del 112.' },
      { w: 'ESTINTORE', cat: 'Antincendio', hint: 'Spegne piccole fiamme',
        explain: 'L\'estintore deve essere a portata di mano e ricaricato ogni anno. Solo gli adulti formati lo usano.' },
      { w: 'ASCENSORE', cat: 'Da evitare', hint: 'Mai durante un\'evacuazione',
        explain: 'In sisma o incendio, l\'ascensore può bloccarsi tra i piani. Sempre le scale, mai l\'ascensore.' },
      { w: 'CAPOFILA', cat: 'Evacuazione', hint: 'Guida la fila della classe',
        explain: 'Il capofila è scelto dall\'insegnante e ha un giubbino visibile. La maestra in fondo controlla che non manchi nessuno.' },
      { w: 'DOCUMENTI', cat: 'Evacuazione', hint: 'Carta d\'identità e tessera sanitaria',
        explain: 'In evacuazione veloce porta solo documenti + cellulare + medicine personali. Tutto il resto si recupera dopo.' },
      { w: 'VIGILANZA', cat: 'Controllo', hint: 'Osservare per prevenire pericoli',
        explain: 'In allerta arancione/rossa, i volontari fanno turni di vigilanza ai punti critici (sottopassi, argini, versanti).' },
      { w: 'PRESIDIO', cat: 'Postazione operativa', hint: 'Posto dove si presta servizio',
        explain: 'Il presidio sanitario in emergenza è gestito da CRI o ASL: triage, primo soccorso, smistamento agli ospedali.' },
      { w: 'CENTRALE', cat: 'Coordinamento', hint: 'Da qui si dirigono gli interventi',
        explain: 'La Sala Operativa di PC (Comune o Regione) coordina mezzi, volontari, comunicazioni in emergenza.' },
      { w: 'BINOCOLO', cat: 'Osservazione', hint: 'Serve a vedere lontano',
        explain: 'Sui versanti boscati a rischio AIB i volontari osservano dai punti panoramici col binocolo, alla ricerca di fumo.' },
      { w: 'CRATERE', cat: 'Castelli Romani', hint: 'Buco circolare di un vulcano spento',
        explain: 'Il cratere del lago di Nemi appartiene al complesso vulcanico dei Colli Albani: spento ma monitorato.' },
      { w: 'VULCANO', cat: 'Rischio territorio', hint: 'Montagna che può eruttare',
        explain: 'Il vulcano dei Colli Albani è classificato "quiescente": ultima eruzione 19.000 anni fa, ma sismicità di fondo presente.' },
      { w: 'PIANO FAMILIARE', cat: 'Preparazione domestica', hint: 'Cosa fa ciascuno in caso di emergenza',
        explain: 'Il piano familiare risponde a 4 domande: chi fa cosa? dove ci ritroviamo? chi avvisiamo? cosa portiamo? Stampalo e tienilo a casa.' },
      { w: 'PUNTO RACCOLTA', cat: 'Sicurezza', hint: 'Dove ci si ritrova dopo l\'evacuazione',
        explain: 'Il punto di raccolta a scuola è in cortile, segnalato dal cartello ISO verde. Nessuno torna in classe a prendere lo zaino.' }
    ],
    difficile: [
      { w: 'EVACUAZIONE', cat: 'Azione di emergenza', hint: 'Tutti fuori in fila e con calma',
        explain: 'L\'evacuazione segue il Piano di Emergenza Scolastico: fila ordinata, capofila con giubbino, conta dei presenti al punto di raccolta.' },
      { w: 'AUTOPROTEZIONE', cat: 'Comportamento', hint: 'Difendere se stessi con i gesti giusti',
        explain: 'L\'autoprotezione è la prima difesa: conoscere i rischi del proprio territorio + sapere cosa fare nei primi 30 minuti.' },
      { w: 'IDROGEOLOGICO', cat: 'Rischio', hint: 'Acqua + terreno che frana',
        explain: 'Il rischio idrogeologico (frane + alluvioni) è il più diffuso in Italia. CNR-IRPI lo monitora con database storici dal 1900.' },
      { w: 'COMUNICAZIONE', cat: 'Informazione', hint: 'Avvisare e coordinare in emergenza',
        explain: 'La comunicazione del rischio segue la Direttiva Mattarella 2008 e la Direttiva PCM 30/4/2021. Solo fonti ufficiali.' },
      { w: 'TEMPORALE', cat: 'Fenomeno meteo', hint: 'Tuoni, fulmini e pioggia intensa',
        explain: 'In temporale: dentro casa, lontano da finestre, doccia, oggetti elettrici. Niente telefono fisso.' },
      { w: 'BOSCHIVO', cat: 'Rischio AIB', hint: 'Incendio che colpisce i boschi',
        explain: 'Il rischio incendio boschivo è regolato dalla Legge 353/2000: chi causa un AIB rischia carcere fino a 7 anni.' },
      { w: 'ANTINCENDIO', cat: 'Prevenzione', hint: 'Tutto ciò che serve a contrastare il fuoco',
        explain: 'Le squadre AIB regionali del Lazio operano da terra e da aria (Canadair). Il volontariato è una componente fondamentale.' },
      { w: 'COORDINAMENTO', cat: 'Organizzazione', hint: 'Lavorare insieme senza confusione',
        explain: 'Il coordinamento PC ha più livelli: COC (Comune), COM (intercomunale), CCS (Provinciale), DI.COMA.C (nazionale).' },
      { w: 'RADIO COMUNICAZIONE', cat: 'Strumento PC', hint: 'Messaggi via radio tra le squadre',
        explain: 'Il Gruppo Comunale di Genzano ha la sezione Radiocomunicazioni: rete UHF/VHF dedicata, indipendente dalla rete cellulare.' },
      { w: 'SORVEGLIANZA', cat: 'Controllo', hint: 'Tenere d\'occhio una zona a rischio',
        explain: 'In allerta rossa, i volontari sorvegliano argini, sottopassi, scarpate frana. Turni 24/7 fino a fine evento.' },
      { w: 'ESONDAZIONE', cat: 'Rischio idrogeologico', hint: 'Il fiume esce dal letto',
        explain: 'In esondazione: sali ai piani alti, mai attraversare in macchina. Bastano 30 cm d\'acqua per far galleggiare un\'auto.' },
      { w: 'PROTEZIONE CIVILE', cat: 'Sistema nazionale', hint: 'Tutti gli enti che gestiscono le emergenze',
        explain: 'Il Servizio Nazionale di PC è regolato dal D.Lgs. 1/2018 (Codice). Articulato su Stato, Regioni, Comuni, volontariato.' },
      { w: 'VOLONTARIATO', cat: 'Donare tempo', hint: 'Aiuto gratuito alla comunità',
        explain: 'Il volontariato di PC nel Lazio è coordinato dalla Regione Lazio - Direzione Protezione Civile, con Albo Regionale.' },
      { w: 'AUTOMEZZO', cat: 'Mezzo operativo', hint: 'Veicolo dei volontari',
        explain: 'Il Gruppo Comunale di Genzano ha automezzi 4x4 attrezzati per AIB e logistica, con marchio "Protezione Civile".' },
      { w: 'CARTOGRAFIA', cat: 'Mappe del territorio', hint: 'Disegno scientifico del territorio',
        explain: 'La cartografia di rischio dei Castelli Romani è disponibile sulla Sit-IT del CNR-IRPI: livelli di pericolo per ogni sotto-area.' },
      { w: 'SICUREZZA SCOLASTICA', cat: 'Piano d\'emergenza', hint: 'Regole per evacuare le scuole',
        explain: 'Il Piano di Emergenza Scolastico è obbligatorio per ogni istituto: 2 prove di evacuazione l\'anno + addestramento docenti.' },
      { w: 'SISMOGRAFO', cat: 'Strumento scientifico', hint: 'Registra i movimenti della terra',
        explain: 'L\'INGV ha una rete di oltre 600 sismografi in Italia: registrano in tempo reale magnitudo, profondità, epicentro.' },
      { w: 'METEOROLOGIA', cat: 'Scienza del tempo', hint: 'Studia e prevede il tempo atmosferico',
        explain: 'In Italia la fonte ufficiale meteo per la PC è il Centro Funzionale Regionale (CFR) di ogni Regione, integrato con Aeronautica.' },
      { w: 'IT ALERT', cat: 'Allarme pubblico', hint: 'Sistema italiano di SMS d\'emergenza dal Governo',
        explain: 'IT-alert è operativo dal 2024: invia un messaggio cell broadcast a tutti i cellulari nell\'area di pericolo, anche stranieri.' },
      { w: 'DIRETTIVA MATTARELLA', cat: 'Norma 2008', hint: 'Linee guida sulla comunicazione del rischio',
        explain: 'La Direttiva PCM del 2008 (firmata da Mattarella allora Vicepresidente del Consiglio) fissa gli indirizzi nazionali sulla comunicazione del rischio in emergenza.' }
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
          if (slot.classList.contains('filled') && !solvedThisWord) {
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
    if (solvedThisWord) return;
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
    if (!answerSequence.length || solvedThisWord) return;
    const entry = answerSequence.pop();
    entry.slot.textContent = '';
    entry.slot.classList.remove('filled', 'correct', 'wrong');
    entry.slot.setAttribute('aria-label', 'Casella vuota');
    const tile = letterPool.querySelector(`.letter-tile[data-index="${entry.tileIndex}"]`);
    if (tile) { tile.classList.remove('used'); tile.disabled = false; }
  };

  const resetWord = () => {
    if (solvedThisWord) return;
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
    if (hintsLeft <= 0 || solvedThisWord) return;
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
        const hintPenalty = (3 - hintsLeft) * 5;
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
        if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
        nextBtn.classList.remove('hide');
        nextBtn.focus();
      } else {
        slots.forEach(s => s.classList.add('wrong'));
        feedbackBox.classList.remove('hide', 'correct');
        feedbackBox.classList.add('wrong');
        feedbackBox.innerHTML = '<i class="bi bi-x-circle-fill" aria-hidden="true"></i> Non è corretto. Riprova!';
        if (window.GameCoach && window.GameCoach.hint) {
          window.GameCoach.hint('Le parole sono tutte legate alla Protezione Civile. Conta le lettere e pensa alla definizione: il glossario del sito ha quasi tutte le parole.', '/glossario/');
        }
        // sblocca le tile per farle riposizionare
        setTimeout(() => {
          resetWord();
        }, 900);
      }
    }
  };

  const nextWord = () => {
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
    resultsScreen.classList.add('hide');
    startScreen.classList.remove('hide');
  });
  undoBtn.addEventListener('click', undoLast);
  resetBtn.addEventListener('click', resetWord);
  hintBtn.addEventListener('click', useHint);
  nextBtn.addEventListener('click', nextWord);

  // Tastiera: lettere fisiche digitate inseriscono la prima tile disponibile
  document.addEventListener('keydown', (e) => {
    if (gameScreen.classList.contains('hide') || solvedThisWord) return;
    if (e.key === 'Backspace') { e.preventDefault(); undoLast(); return; }
    if (e.key === 'Enter' && !nextBtn.classList.contains('hide')) { e.preventDefault(); nextWord(); return; }
    const key = (e.key || '').toUpperCase();
    if (!/^[A-Z]$/.test(key)) return;
    const tile = [...letterPool.children].find(t => !t.classList.contains('used') && t.textContent === key);
    if (tile) { e.preventDefault(); placeLetter(tile); }
  });

});
