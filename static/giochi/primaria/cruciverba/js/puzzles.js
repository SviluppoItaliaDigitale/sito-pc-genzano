/* Cruciverba della Sicurezza — Schemi tematici (rifatti maggio 2026)
 *
 * Ogni schema specifica griglia (rows x cols) e parole con posizione, direzione
 * e definizione. Il campo `explain` (nuovo) contiene la nota didattica che il
 * gioco mostra quando la parola viene completata: serve a fissare la nozione
 * (rules 03 — apprendimento, non solo decorativo).
 *
 * Temi:
 * - Facile: cosa fare adesso, casco, numero 112, codici colore base.
 * - Medio: allerta meteo, fonti ufficiali, volontariato, evacuazione scolastica.
 * - Difficile: IT-alert e fake news, rischio sismico Castelli, AIB.
 *
 * Le definizioni rispettano AGID (frasi brevi, voce attiva, italiano chiaro).
 */

window.CRUCIVERBA_PUZZLES = {

  // ═══════════════════════════════════════════════════════════════
  // FACILE
  // ═══════════════════════════════════════════════════════════════
  facile: [

    // ── F1: "Casco e Campo" — schema interlocking 5x5 ────────────
    {
      id: 'facile-1',
      rows: 5, cols: 5,
      title: 'Schema "Casco e Campo"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'CASCO',
          clue: 'Si mette in testa per proteggerla durante un\'emergenza',
          explain: 'Il casco è obbligatorio per i volontari sul campo: protegge da oggetti che cadono.' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'CAMPO',
          clue: 'Area di accoglienza per chi è stato evacuato',
          explain: 'Il campo di accoglienza è installato in spazi aperti (parchi, piazze) lontano da edifici a rischio.' },
        { n: 2, dir: 'D', row: 0, col: 2, answer: 'SOLE',
          clue: 'D\'estate quando picchia forte serve bere tanta acqua',
          explain: 'Le ondate di calore (allerta arancione/rossa) sono pericolose per anziani e bambini: stai all\'ombra e bevi.' },
        { n: 3, dir: 'D', row: 0, col: 3, answer: 'CASA',
          clue: 'Durante una scossa di terremoto, ci si mette sotto il tavolo qui dentro',
          explain: 'In caso di terremoto: sotto un tavolo robusto, lontano da finestre e mobili pesanti.' },
        { n: 4, dir: 'D', row: 0, col: 4, answer: 'OSSO',
          clue: 'Lo si può rompere cadendo: lo controlla il pronto soccorso',
          explain: 'Per traumi gravi chiama subito il 112: gli operatori inviano l\'ambulanza più vicina.' },
        { n: 5, dir: 'A', row: 4, col: 0, answer: 'OASI',
          clue: 'Acqua e ombra nel deserto: la prima cosa per non disidratarsi',
          explain: 'Acqua e ombra sono i primi rimedi contro l\'ondata di calore, anche in città.' }
      ]
    },

    // ── F2: Comb "Numero unico 112" ───────────────────────────────
    {
      id: 'facile-2',
      rows: 11, cols: 7,
      title: 'Schema "Chiamare 112"',
      words: [
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'EMERGENZA',
          clue: 'Situazione urgente che richiede aiuto immediato',
          explain: 'In emergenza chiami il 112: una chiamata, smistano a vigili del fuoco, ambulanza o forze dell\'ordine.' },
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'EUROPA',
          clue: 'Continente di cui fa parte l\'Italia',
          explain: 'Il 112 è il Numero Unico Europeo: funziona in tutti i Paesi UE.' },
        { n: 2, dir: 'A', row: 1, col: 0, answer: 'MAPPA',
          clue: 'Foglio che mostra strade e luoghi',
          explain: 'Quando chiami il 112, l\'app Where Are U geolocalizza la tua posizione automaticamente.' },
        { n: 3, dir: 'A', row: 2, col: 0, answer: 'EROE',
          clue: 'Si dice di chi fa azioni coraggiose',
          explain: 'I volontari di Protezione Civile non sono eroi: sono cittadini formati che aiutano nelle emergenze.' },
        { n: 4, dir: 'A', row: 3, col: 0, answer: 'RADIO',
          clue: 'Strumento dei volontari per comunicare a distanza senza linea telefonica',
          explain: 'Le radio di servizio (UHF/VHF) funzionano anche dove il cellulare non prende.' },
        { n: 5, dir: 'A', row: 4, col: 0, answer: 'GENZANO',
          clue: 'Comune dei Castelli Romani affacciato sul lago di Nemi',
          explain: 'Genzano è in zona sismica 2B e a rischio idrogeologico medio per i versanti del cratere.' },
        { n: 6, dir: 'A', row: 5, col: 0, answer: 'EVACUARE',
          clue: 'Lasciare un edificio o una zona quando arriva un pericolo',
          explain: 'Si evacua sempre dalle scale, mai dall\'ascensore: durante un\'emergenza l\'ascensore può bloccarsi.' },
        { n: 7, dir: 'A', row: 6, col: 0, answer: 'NEVE',
          clue: 'Cade dal cielo quando fa freddo',
          explain: 'La neve abbondante (allerta gialla per neve) può rendere strade impraticabili e crollare tetti deboli.' },
        { n: 8, dir: 'A', row: 7, col: 0, answer: 'ZAINO',
          clue: 'Lo prepari prima dell\'emergenza con acqua, torcia e medicine',
          explain: 'Il kit di emergenza domestico va tenuto vicino alla porta: acqua, cibo a lunga scadenza, torcia, radio a pile, medicine personali.' },
        { n: 9, dir: 'A', row: 8, col: 0, answer: 'AIUTO',
          clue: 'Lo chiedi quando sei in difficoltà',
          explain: 'Chiedere aiuto al 112 non è un disturbo: gli operatori valutano e attivano i soccorsi giusti.' }
      ]
    },

    // ── F3: Comb "Codici colore allerta" ─────────────────────────
    {
      id: 'facile-3',
      rows: 9, cols: 8,
      title: 'Schema "Codici colore allerta"',
      words: [
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'ALLERTA',
          clue: 'Avviso ufficiale che un pericolo potrebbe arrivare',
          explain: 'L\'allerta meteo del Centro Funzionale Regionale Lazio ha 4 livelli: verde, giallo, arancione, rosso.' },
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'ARANCIO',
          clue: 'Codice colore di allerta meteo elevata: fenomeni intensi attesi',
          explain: 'Allerta arancione: fenomeni intensi con possibili effetti rilevanti. Limita gli spostamenti e segui i bollettini.' },
        { n: 2, dir: 'A', row: 1, col: 0, answer: 'LAGO',
          clue: 'Genzano si affaccia su quello di Nemi',
          explain: 'Il lago di Nemi è dentro un cratere vulcanico spento: zona di rischio frana per i versanti ripidi.' },
        { n: 3, dir: 'A', row: 2, col: 0, answer: 'LAZIO',
          clue: 'Regione in cui si trova Genzano',
          explain: 'Il Centro Funzionale Regionale Lazio emette i bollettini di criticità per allerte meteo e idrogeologiche.' },
        { n: 4, dir: 'A', row: 3, col: 0, answer: 'EMERGENZA',
          clue: 'Evento in corso che richiede azione immediata',
          explain: 'Allerta = fase di previsione. Emergenza = evento in corso. Sono due fasi distinte del ciclo del rischio.' },
        { n: 5, dir: 'A', row: 4, col: 0, answer: 'ROSSO',
          clue: 'Codice colore di allerta meteo massima',
          explain: 'Allerta rossa: fenomeni molto intensi con rischio elevato per la popolazione. Segui le indicazioni del Comune.' },
        { n: 6, dir: 'A', row: 5, col: 0, answer: 'TUONO',
          clue: 'Rumore forte che segue il fulmine durante un temporale',
          explain: 'Durante un temporale stai dentro casa, lontano da finestre, doccia e oggetti elettrici.' },
        { n: 7, dir: 'A', row: 6, col: 0, answer: 'AIUTARE',
          clue: 'Cosa fanno i volontari di Protezione Civile',
          explain: 'I volontari del Gruppo Comunale aiutano in emergenza ma anche con campagne di prevenzione tutto l\'anno.' }
      ]
    }

  ],

  // ═══════════════════════════════════════════════════════════════
  // MEDIO
  // ═══════════════════════════════════════════════════════════════
  medio: [

    // ── M1: Comb "Allerta meteo" ──────────────────────────────────
    {
      id: 'medio-1',
      rows: 9, cols: 11,
      title: 'Schema "Allerta meteo"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'PREVENZIONE',
          clue: 'Insieme di azioni per evitare che un pericolo si verifichi o per ridurne le conseguenze',
          explain: 'La prevenzione è la prima missione della Protezione Civile (D.Lgs. 1/2018, Codice della PC).' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'PIOGGIA',
          clue: 'Quando è intensa per ore può causare allagamenti e frane',
          explain: 'Piogge persistenti = rischio idrogeologico. Il bollettino di criticità lo prevede 24 ore prima.' },
        { n: 2, dir: 'D', row: 0, col: 1, answer: 'RISCHIO',
          clue: 'Possibilità che accada un evento dannoso',
          explain: 'Rischio = pericolo × esposizione × vulnerabilità. Riducendo uno dei tre, si riduce il rischio.' },
        { n: 3, dir: 'D', row: 0, col: 2, answer: 'EVACUARE',
          clue: 'Lasciare ordinatamente un edificio o un\'area in pericolo',
          explain: 'L\'evacuazione si fa dalle scale, mai dall\'ascensore. Punto di raccolta: in spazio aperto.' },
        { n: 4, dir: 'D', row: 0, col: 3, answer: 'VENTO',
          clue: 'Quando è forte fa cadere alberi e tegole',
          explain: 'Allerta vento (gialla/arancione) = chiudi le finestre, evita i parchi alberati, attenzione a oggetti che volano.' },
        { n: 5, dir: 'D', row: 0, col: 4, answer: 'ESONDA',
          clue: 'Esce dagli argini quando il fiume è in piena',
          explain: 'In caso di esondazione: sali ai piani alti, mai negli scantinati o in macchina nei sottopassi.' },
        { n: 6, dir: 'D', row: 0, col: 5, answer: 'NUMERI',
          clue: 'Nel Lazio quello unico per le emergenze è il 112',
          explain: 'Il 112 (Numero Unico Europeo) è attivo nel Lazio dal 2017: smista a 113, 115 e 118 secondo il caso.' },
        { n: 7, dir: 'D', row: 0, col: 6, answer: 'INCENDIO',
          clue: 'Fuoco fuori controllo, in casa o nei boschi',
          explain: 'In casa: chiama 112, esci, mai usare l\'ascensore, copri naso e bocca con un panno bagnato se c\'è fumo.' },
        { n: 8, dir: 'D', row: 0, col: 7, answer: 'OPERA',
          clue: 'Lavoro fatto, opera d\'arte o spettacolo',
          explain: 'Sul nostro territorio: il santuario della Madonna del Cielo è un\'opera storica da tutelare anche in emergenza.' },
        { n: 9, dir: 'D', row: 0, col: 8, answer: 'NORMA',
          clue: 'Regola scritta che tutti devono rispettare',
          explain: 'La PC è regolata da norme precise: D.Lgs. 1/2018 (Codice PC) e Direttiva PCM 30 aprile 2021.' },
        { n: 10, dir: 'D', row: 0, col: 9, answer: 'ELMO',
          clue: 'Casco antico, anche dei soldati',
          explain: 'I caschi moderni dei volontari proteggono da oggetti fino a 5 chili che cadono dall\'alto.' },
        { n: 11, dir: 'D', row: 0, col: 10, answer: 'ESCAVA',
          clue: 'Macchina che scava nel terreno (verbo)',
          explain: 'Le ruspe sono mezzi di Protezione Civile per liberare strade dopo frane o allagamenti.' }
      ]
    },

    // ── M2: Comb "Fonti ufficiali" ─────────────────────────────────
    {
      id: 'medio-2',
      rows: 9, cols: 9,
      title: 'Schema "Fonti ufficiali"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'COMUNE',
          clue: 'Ente territoriale che attiva il COC in emergenza',
          explain: 'Il Sindaco è la prima autorità di Protezione Civile sul territorio (art. 12 D.Lgs. 1/2018).' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'CITTADINO',
          clue: 'Persona che vive in un Comune e ne fa parte attiva',
          explain: 'Il cittadino informato è il primo soccorritore: 30 minuti dopo un evento, prima dei VVF.' },
        { n: 2, dir: 'D', row: 0, col: 1, answer: 'OPERATORE',
          clue: 'Chi lavora in sala radio o in Centro Operativo Comunale (COC)',
          explain: 'Il COC si attiva in emergenza: coordina volontari, assistenza alla popolazione, informazione.' },
        { n: 3, dir: 'D', row: 0, col: 2, answer: 'MEDIA',
          clue: 'Insieme di TV, radio, giornali, siti ufficiali',
          explain: 'Per le emergenze: usa solo i media istituzionali (Comune, DPC, CFR Regione). Mai i forward WhatsApp.' },
        { n: 4, dir: 'D', row: 0, col: 3, answer: 'UFFICIO',
          clue: 'Sede dove lavorano i dipendenti pubblici',
          explain: 'L\'Ufficio Tecnico Comunale gestisce il Piano di Emergenza Comunale (PEC), il documento base della PC locale.' },
        { n: 5, dir: 'D', row: 0, col: 4, answer: 'NEVE',
          clue: 'Bianca, fredda, attesa con allerta meteo specifica',
          explain: 'Allerta neve: il Comune attiva il piano neve, sale in strada, chiusura scuole se necessario.' },
        { n: 6, dir: 'D', row: 0, col: 5, answer: 'EVITARE',
          clue: 'Stare alla larga: cosa fare con i sottopassi allagati',
          explain: 'Mai attraversare sottopassi allagati in macchina: l\'auto galleggia con 30 cm d\'acqua.' }
      ]
    },

    // ── M3: Comb "Volontariato" ───────────────────────────────────
    {
      id: 'medio-3',
      rows: 11, cols: 11,
      title: 'Schema "Volontariato"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'VOLONTARI',
          clue: 'Donano tempo e competenze per aiutare gli altri',
          explain: 'I volontari di Protezione Civile sono inseriti nel Servizio Nazionale (Legge 225/1992, oggi D.Lgs. 1/2018).' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'VIGILANZA',
          clue: 'Attenzione costante per prevenire i pericoli',
          explain: 'In allerta arancione/rossa, i volontari fanno turni di vigilanza ai punti critici del territorio.' },
        { n: 2, dir: 'D', row: 0, col: 1, answer: 'OPERATORE',
          clue: 'Volontario in sala radio o sul campo',
          explain: 'Per diventare operatore servono corsi specifici (TLC, AIB, DOS, sanitari).' },
        { n: 3, dir: 'D', row: 0, col: 2, answer: 'LOGISTICA',
          clue: 'Organizzazione di mezzi, materiali e spostamenti',
          explain: 'In emergenza la logistica è la differenza tra aiuto efficace e caos: chi porta cosa, dove, quando.' },
        { n: 4, dir: 'D', row: 0, col: 3, answer: 'ORGANICO',
          clue: 'Insieme dei volontari iscritti al gruppo',
          explain: 'L\'organico del Gruppo Comunale Genzano viene aggiornato annualmente all\'Albo Regionale.' },
        { n: 5, dir: 'D', row: 0, col: 4, answer: 'NUMERI',
          clue: 'Quello del 112, del 115 e del 118 sono fondamentali',
          explain: 'Dal 2017 nel Lazio basta il 112: Vigili del Fuoco, ambulanza e forze dell\'ordine sono smistate dalla centrale unica.' },
        { n: 6, dir: 'D', row: 0, col: 5, answer: 'TORMENTA',
          clue: 'Tempesta intensa di neve e vento',
          explain: 'In tormenta: stai in casa, chiudi le finestre, non viaggiare. Allerta arancione o rossa scatta automaticamente.' },
        { n: 7, dir: 'D', row: 0, col: 6, answer: 'ALLERTA',
          clue: 'Avviso ufficiale che un pericolo è atteso',
          explain: 'Allerta = fase prima dell\'evento. Si attiva con il bollettino del Centro Funzionale Regionale.' },
        { n: 8, dir: 'D', row: 0, col: 7, answer: 'RADIO',
          clue: 'Apparecchio che trasmette voci via onde, anche senza rete cellulare',
          explain: 'Le radio dei volontari (VHF/UHF) sono indispensabili: funzionano dove la rete telefonica è satura o assente.' },
        { n: 9, dir: 'D', row: 0, col: 8, answer: 'IDRANTE',
          clue: 'Da qui i Vigili del Fuoco prendono l\'acqua',
          explain: 'Gli idranti antincendio in strada vanno tenuti liberi: chi parcheggia davanti rischia una multa.' }
      ]
    }

  ],

  // ═══════════════════════════════════════════════════════════════
  // DIFFICILE
  // ═══════════════════════════════════════════════════════════════
  difficile: [

    // ── D1: Comb "IT-alert e fake news" ──────────────────────────
    {
      id: 'difficile-1',
      rows: 12, cols: 9,
      title: 'Schema "IT-alert e fake news"',
      words: [
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'INFORMARSI',
          clue: 'Cercare notizie verificate da fonti ufficiali, non dai social',
          explain: 'In emergenza: solo Comune, DPC, Regione, Centro Funzionale. Mai i forward WhatsApp non verificati.' },
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'ITALIA',
          clue: 'Paese in cui è nato IT-alert',
          explain: 'IT-alert è il sistema italiano di allarme pubblico via cell broadcast: mandato dal Governo, ricevuto da tutti i cellulari della zona.' },
        { n: 2, dir: 'A', row: 1, col: 0, answer: 'NUOVI',
          clue: 'Si dice di sistemi mai visti prima, come IT-alert',
          explain: 'IT-alert è operativo dal 2024 dopo sperimentazione 2023. Manda un messaggio a tutti i cellulari nell\'area di pericolo.' },
        { n: 3, dir: 'A', row: 2, col: 0, answer: 'FALSO',
          clue: 'Contrario di vero: caratteristica delle fake news',
          explain: 'Le fake news in emergenza creano panico inutile. Non condividere se non sai che è ufficiale.' },
        { n: 4, dir: 'A', row: 3, col: 0, answer: 'OBIETTIVO',
          clue: 'Risultato che si vuole raggiungere, anche in Protezione Civile',
          explain: 'L\'obiettivo della Protezione Civile: salvare vite, ridurre danni, assistere chi è in difficoltà.' },
        { n: 5, dir: 'A', row: 4, col: 0, answer: 'RUMORE',
          clue: 'Suono confuso: come le voci che girano sui social in emergenza',
          explain: 'Il "rumore informativo" è il primo nemico in emergenza: tante voci, poche verificate.' },
        { n: 6, dir: 'A', row: 5, col: 0, answer: 'MARCO',
          clue: 'Nome italiano comune (e cognome del Presidente Mattarella, autore della Direttiva 2008)',
          explain: 'La Direttiva Mattarella 2008 fissa le linee guida sulla comunicazione del rischio in emergenza.' },
        { n: 7, dir: 'A', row: 6, col: 0, answer: 'AVVISO',
          clue: 'Messaggio breve di attenzione su un pericolo',
          explain: 'L\'avviso meteo del CFR Lazio è disponibile su sito Regione e via app gratuita "Allerta Lazio".' },
        { n: 8, dir: 'A', row: 7, col: 0, answer: 'RADIO',
          clue: 'Ancora oggi è il mezzo più affidabile in emergenza (anche con blackout)',
          explain: 'In blackout esteso, una radio a pile o a manovella è insostituibile: cell broadcast e Internet vanno giù.' },
        { n: 9, dir: 'A', row: 8, col: 0, answer: 'SISMICO',
          clue: 'Aggettivo che riguarda i terremoti',
          explain: 'I Castelli Romani sono in zona sismica 2B (sismicità media). L\'INGV monitora 24/7.' },
        { n: 10, dir: 'A', row: 9, col: 0, answer: 'IRPINIA',
          clue: 'Terremoto del 1980 che ha portato alla nascita del DPC',
          explain: 'Sisma Irpinia 1980: 2914 vittime. Spinta decisiva alla creazione del Dipartimento di Protezione Civile (1982, Zamberletti).' }
      ]
    },

    // ── D2: Comb "Sismo Castelli Romani" ─────────────────────────
    {
      id: 'difficile-2',
      rows: 9, cols: 11,
      title: 'Schema "Sismo Castelli"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'SISMOLOGIA',
          clue: 'Scienza che studia i terremoti',
          explain: 'INGV è l\'Istituto Nazionale di Geofisica e Vulcanologia: monitora le scosse 24/7 in tutta Italia.' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'SCOSSA',
          clue: 'Movimento improvviso del terreno',
          explain: 'In una scossa: sotto un tavolo robusto, lontano da finestre. Resta lì finché non finisce.' },
        { n: 2, dir: 'D', row: 0, col: 1, answer: 'INCENDIO',
          clue: 'Fuoco fuori controllo che dopo una scossa può divampare',
          explain: 'Dopo una scossa di terremoto: chiudi gas e luce, controlla incendi, esci ordinatamente.' },
        { n: 3, dir: 'D', row: 0, col: 2, answer: 'SOTTO',
          clue: 'Posizione del bambino durante la scossa: ___ il banco a scuola',
          explain: 'A scuola: sotto al banco, lontano dai vetri. La maestra dà ordini chiari: prima protezione, poi evacuazione.' },
        { n: 4, dir: 'D', row: 0, col: 3, answer: 'MOLTI',
          clue: 'Plurale di molto: i danni di un sisma forte sono ___',
          explain: 'Dopo un sisma forte servono giorni per tutte le verifiche strutturali: gli edifici si rientrano solo se dichiarati agibili.' },
        { n: 5, dir: 'D', row: 0, col: 4, answer: 'ORARIO',
          clue: 'Quando avviene un evento (giorno e ___)',
          explain: 'L\'orario di una scossa è importante: di notte le persone sono in casa, di giorno a scuola o al lavoro. Cambia tutto la pianificazione.' },
        { n: 6, dir: 'D', row: 0, col: 5, answer: 'LAGO',
          clue: 'Specchio d\'acqua come quello di Nemi nei Castelli',
          explain: 'Il lago di Nemi è in un cratere vulcanico spento. La caldera è monitorata insieme al complesso dei Vulcani Laziali.' },
        { n: 7, dir: 'D', row: 0, col: 6, answer: 'ONDA',
          clue: 'Movimento del suolo durante un terremoto (___ sismica)',
          explain: 'Le onde sismiche P arrivano per prime, le S e di superficie dopo. Tra P e S: il tempo per cercare riparo.' },
        { n: 8, dir: 'D', row: 0, col: 7, answer: 'GENZANO',
          clue: 'Comune dei Castelli Romani sede del nostro Gruppo Comunale',
          explain: 'Genzano in zona sismica 2B (sismicità media): edifici post-1981 hanno norme antisismiche, quelli storici no.' },
        { n: 9, dir: 'D', row: 0, col: 8, answer: 'INGV',
          clue: 'Istituto Nazionale di Geofisica e Vulcanologia (acronimo)',
          explain: 'INGV pubblica in tempo reale magnitudo, profondità, epicentro di ogni scossa su ingv.it (sezione Lista Eventi).' },
        { n: 10, dir: 'D', row: 0, col: 9, answer: 'AMARO',
          clue: 'Sapore non dolce, come il ricordo di Amatrice 2016',
          explain: 'Sisma Centro Italia 2016 (Amatrice, Norcia, Arquata): sequenza prolungata, oltre 300 vittime, ricostruzione ancora in corso.' },
        { n: 11, dir: 'D', row: 0, col: 10, answer: 'AVVISO',
          clue: 'Messaggio di attenzione, prima dell\'allerta',
          explain: 'Il bollettino sismico è informativo: l\'INGV non emette "allerta" sismica perché i terremoti non si prevedono. Comunicano solo dopo.' }
      ]
    },

    // ── D3: Comb "AIB e incendi boschivi" ─────────────────────────
    {
      id: 'difficile-3',
      rows: 9, cols: 9,
      title: 'Schema "Incendi boschivi"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'INCENDIO',
          clue: 'Fuoco fuori controllo, in casa o nei boschi',
          explain: 'In Italia il 95% degli incendi boschivi è causato da uomo (negligenza o doloso). Mai accendere fuochi nei boschi d\'estate.' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'INFIAMMA',
          clue: 'Verbo: prendere fuoco rapidamente',
          explain: 'Erba secca, legno, foglie: in luglio-agosto si infiammano in pochi secondi con una scintilla.' },
        { n: 2, dir: 'D', row: 0, col: 1, answer: 'NUMERO',
          clue: 'Per chiamare i Vigili del Fuoco è il 112 (il vecchio era il 115)',
          explain: 'Dal 2017 nel Lazio si chiama solo il 112. La centrale unica smista al 115 (VVF) per gli incendi.' },
        { n: 3, dir: 'D', row: 0, col: 2, answer: 'CASCO',
          clue: 'Si mette in testa, anche dai volontari AIB',
          explain: 'Il casco AIB (Anti Incendio Boschivo) è ignifugo, con visiera e protezione collo. Obbligatorio sul fronte fuoco.' },
        { n: 4, dir: 'D', row: 0, col: 3, answer: 'ESTATE',
          clue: 'Stagione più calda dell\'anno e più pericolosa per gli incendi',
          explain: 'Periodo di massima pericolosità AIB nel Lazio: 15 giugno - 30 settembre. Allerta caldo + secco = rischio massimo.' },
        { n: 5, dir: 'D', row: 0, col: 4, answer: 'NORMA',
          clue: 'Regola scritta: la legge quadro sugli incendi è la 353/2000',
          explain: 'Legge 353/2000: chi causa un incendio boschivo (anche colposo) rischia carcere fino a 7 anni e perdita del terreno.' },
        { n: 6, dir: 'D', row: 0, col: 5, answer: 'DRONE',
          clue: 'Velivolo senza pilota, oggi usato anche per monitorare gli incendi',
          explain: 'I droni AIB con telecamera termica trovano focolai nascosti sotto fronde o nelle zone difficili da raggiungere a piedi.' },
        { n: 7, dir: 'D', row: 0, col: 6, answer: 'ITALIA',
          clue: 'Paese che ha il sistema "Io non rischio" del DPC',
          explain: '"Io non rischio" è la campagna del DPC con piazze in oltre 600 Comuni: spiega rischio sismico, vulcanico, alluvioni.' },
        { n: 8, dir: 'D', row: 0, col: 7, answer: 'OPACO',
          clue: 'Non trasparente: come il fumo di un incendio',
          explain: 'In incendio, il fumo opaco fa più vittime delle fiamme: copre naso e bocca con un panno bagnato e stai basso.' }
      ]
    }

  ]
};
