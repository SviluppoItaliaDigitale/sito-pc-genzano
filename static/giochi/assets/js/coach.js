/* ============================================================
   Coach — Consigli e teoria di rinforzo per i giochi
   Auto-init via attributo data-coach-game sul body.
   API:
     window.GameCoach.open()                — apre il dialog
     window.GameCoach.hint(testo, urlOpz)   — mostra suggerimento contestuale
     window.GameCoach.clearHint()           — pulisce il suggerimento
   ============================================================ */
(function () {
  'use strict';

  // ──────────────────────────────────────────────────────────
  // Manifest dei consigli (regola, come si gioca, teoria)
  // Ogni voce è breve e in italiano AGID (frasi <20 parole, voce attiva).
  // I link teoria puntano a pagine già pubblicate sul sito.
  // ──────────────────────────────────────────────────────────
  var CONTENUTI = {
    /* ── INFANZIA (3-6 anni) — testi semplici, frasi corte ── */
    'acchiappa-pericolo': {
      fascia: 'infanzia',
      titolo: 'Consigli per Acchiappa il Pericolo',
      regola: 'Tocca SOLO le cose pericolose. Lascia stare le cose sicure.',
      come: [
        'Guarda bene ogni immagine prima di toccare.',
        'Se è un fuoco, una presa, un coltello: è pericoloso.',
        'Se è un libro, un peluche, l\'acqua da bere: è sicuro.'
      ],
      teoria: [
        { titolo: 'Cosa fare in emergenza', url: '/cosa-fare-adesso/' }
      ]
    },
    'cielo-oggi': {
      fascia: 'infanzia',
      titolo: 'Consigli per Che Tempo Fa',
      regola: 'Guarda il cielo dal disegno e scegli il tempo giusto.',
      come: [
        'Sole giallo = bel tempo.',
        'Nuvole grigie + pioggia = brutto tempo.',
        'Fulmini = temporale, meglio stare in casa.'
      ],
      teoria: [
        { titolo: 'Allerte meteo', url: '/allerte-meteo/' },
        { titolo: 'Temporali intensi', url: '/rischi-prevenzione/temporali-intensi/' }
      ]
    },
    'memory-facile': {
      fascia: 'infanzia',
      titolo: 'Consigli per Memory Facile',
      regola: 'Trova due carte uguali. Ricorda dove sono!',
      come: [
        'Gira una carta e guarda il disegno.',
        'Gira un\'altra carta: se è uguale, è una coppia!',
        'Se sono diverse, prova a ricordarle per dopo.'
      ],
      teoria: [
        { titolo: 'Pittogrammi della sicurezza', url: '/pittogrammi/' }
      ]
    },
    'mezzo-giusto': {
      fascia: 'infanzia',
      titolo: 'Consigli per Il Mezzo Giusto',
      regola: 'Per ogni emergenza c\'è il mezzo giusto da chiamare.',
      come: [
        'C\'è un fuoco? Chiama i Vigili del Fuoco.',
        'C\'è un malato? Chiama l\'ambulanza.',
        'C\'è un ladro? Chiama i Carabinieri.',
        'In Italia chiami sempre il 1-1-2.'
      ],
      teoria: [
        { titolo: 'Numeri utili — il 112', url: '/numeri-utili/' }
      ]
    },
    'numero-emergenza': {
      fascia: 'infanzia',
      titolo: 'Consigli per il Numero di Emergenza',
      regola: 'In emergenza, il numero da chiamare è uno solo: 1-1-2.',
      come: [
        'Il 112 chiama tutti: ambulanza, pompieri, carabinieri.',
        'Si chiama gratis, anche senza credito.',
        'Devi dire: cosa succede, dove sei, come ti chiami.'
      ],
      teoria: [
        { titolo: 'Come si chiama il 112', url: '/numeri-utili/' },
        { titolo: 'Cosa fare in emergenza', url: '/cosa-fare-adesso/' }
      ]
    },
    'rifugio-tina': {
      fascia: 'infanzia',
      titolo: 'Consigli per il Rifugio di Tina',
      regola: 'In emergenza Tina cerca un riparo sicuro: aiutala!',
      come: [
        'Sotto al tavolo se trema la terra.',
        'Lontano dalle finestre se piove forte.',
        'In un posto basso se c\'è vento o tornado.'
      ],
      teoria: [
        { titolo: 'Cosa fare se trema la terra', url: '/rischi-prevenzione/rischio-sismico/' },
        { titolo: 'Vento forte', url: '/rischi-prevenzione/vento-forte/' }
      ]
    },
    'suoni-emergenza': {
      fascia: 'infanzia',
      titolo: 'Consigli per i Suoni dell\'Emergenza',
      regola: 'Ogni emergenza ha il suo suono. Imparalo!',
      come: [
        'La sirena dell\'ambulanza ha tre toni.',
        'Il tuono fa "boom" dopo il fulmine.',
        'L\'allarme della scuola dice di uscire in ordine.',
        'IT-alert è un suono lungo del telefono: leggi il messaggio.'
      ],
      teoria: [
        { titolo: 'Allerte meteo', url: '/allerte-meteo/' }
      ]
    },
    'tartaruga-saggia': {
      fascia: 'infanzia',
      titolo: 'Consigli con Tina la Tartaruga',
      regola: 'Tina ti spiega cosa fare: ascoltala con calma.',
      come: [
        'Tina parla piano: leggi due volte se serve.',
        'Scegli la risposta che ti sembra più sicura.',
        'Se sbagli, non importa: si impara così.'
      ],
      teoria: [
        { titolo: 'Cosa fare in emergenza', url: '/cosa-fare-adesso/' },
        { titolo: 'Pagina facile da leggere', url: '/facile-da-leggere/' }
      ]
    },
    'trova-cartello': {
      fascia: 'infanzia',
      titolo: 'Consigli per Trova il Cartello',
      regola: 'I cartelli ci dicono dove andare e cosa fare. Ognuno ha un colore.',
      come: [
        'Verde = posto sicuro (uscita, primo soccorso).',
        'Rosso = vietato (no fumare, no ascensore).',
        'Giallo = attenzione (pavimento bagnato, fuoco).',
        'Blu = obbligo (mettere il casco, i guanti).'
      ],
      teoria: [
        { titolo: 'Pittogrammi della sicurezza', url: '/pittogrammi/' }
      ]
    },
    'vesti-tina': {
      fascia: 'infanzia',
      titolo: 'Consigli per Vesti Tina',
      regola: 'Aiuta Tina a mettere nello zaino le cose giuste per l\'emergenza.',
      come: [
        'Acqua e biscotti: SÌ.',
        'Torcia, casco, giacchetto: SÌ.',
        'Caramelle, videogioco, peluche: NO.',
        'Pochi oggetti, ma utili.'
      ],
      teoria: [
        { titolo: 'Lo zaino per l\'emergenza', url: '/rischi-prevenzione/kit-emergenza/' }
      ]
    },

    /* ── PRIMARIA (6-11 anni) — testo breve + link teoria ── */
    'abbina-impara': {
      fascia: 'primaria',
      titolo: 'Consigli per Abbina e Impara',
      regola: 'Ogni rischio ha il suo comportamento giusto: collegali bene.',
      come: [
        'Leggi prima la categoria (es. terremoto, alluvione).',
        'Pensa a cosa fa la Protezione Civile in quel caso.',
        'Se non sai, leggi le pagine sui rischi del nostro sito.',
        'Le risposte sono sul sito: cercale prima di tirare a indovinare.'
      ],
      teoria: [
        { titolo: 'Rischi e prevenzione', url: '/rischi-prevenzione/' },
        { titolo: 'Cosa fare adesso', url: '/cosa-fare-adesso/' }
      ]
    },
    'anagrammi': {
      fascia: 'primaria',
      titolo: 'Consigli per gli Anagrammi della Sicurezza',
      regola: 'Riordina le lettere per trovare una parola della Protezione Civile.',
      come: [
        'Leggi la definizione: dà l\'indizio principale.',
        'Conta le lettere: la lunghezza ti aiuta.',
        'Pensa alle parole che hai imparato: rischio, allerta, soccorso, evacuazione.',
        'Se sei bloccato, usa l\'aiuto.'
      ],
      teoria: [
        { titolo: 'Glossario della Protezione Civile', url: '/glossario/' },
        { titolo: 'Rischi e prevenzione', url: '/rischi-prevenzione/' }
      ]
    },
    'caccia-al-rischio': {
      fascia: 'primaria',
      titolo: 'Consigli per la Caccia al Rischio',
      regola: 'Pericoli quotidiani che durante un\'emergenza diventano grandi: trovali e impara cosa fare.',
      come: [
        'Guarda bene tutta la scena, non solo il centro.',
        'Clicca sul pericolo: leggi la spiegazione "perche conta per la PC".',
        'Spigoli, tappeti e mobili instabili in casa = problema durante un terremoto.',
        'Fornelli e candele accese = rischio incendio se va via la luce.',
        'Finestre aperte = pericolo con vento forte o temporali.'
      ],
      teoria: [
        { titolo: 'Rischio sismico', url: '/rischi-prevenzione/rischio-sismico/' },
        { titolo: 'Rischio incendio', url: '/rischi-prevenzione/rischio-incendio/' },
        { titolo: 'Temporali intensi', url: '/rischi-prevenzione/temporali-intensi/' },
        { titolo: 'Vento forte', url: '/rischi-prevenzione/vento-forte/' }
      ]
    },
    'chiamata-112': {
      fascia: 'primaria',
      titolo: 'Consigli per la Chiamata al 112',
      regola: 'Quando chiami il 112 dici sempre tre cose: COSA succede, DOVE sei, QUANTI siete.',
      come: [
        'Resta calmo: l\'operatore ti aiuta.',
        'Parla chiaro: nome, indirizzo, cosa è successo.',
        'Non riagganciare per primo.',
        'Se sbagli numero, dillo: il 112 ti capisce.'
      ],
      teoria: [
        { titolo: 'Numeri utili — il 112', url: '/numeri-utili/' },
        { titolo: 'Cosa fare adesso', url: '/cosa-fare-adesso/' }
      ]
    },
    'cosa-faccio-se': {
      fascia: 'primaria',
      titolo: 'Consigli per Cosa Faccio Se…',
      regola: 'In emergenza scegli la risposta più sicura, non la più veloce.',
      come: [
        'Leggi tutte le opzioni prima di scegliere.',
        'Una risposta giusta protegge te e gli altri.',
        'In dubbio: non agire da solo, chiama un adulto o il 112.',
        'Le pagine "Rischi e prevenzione" del sito spiegano il perché.'
      ],
      teoria: [
        { titolo: 'Rischi e prevenzione', url: '/rischi-prevenzione/' },
        { titolo: 'Piano familiare', url: '/piano-familiare/' }
      ]
    },
    'cruciverba': {
      fascia: 'primaria',
      titolo: 'Consigli per il Cruciverba',
      regola: 'Le parole sono tutte legate alla Protezione Civile: rischi, soccorso, allerte.',
      come: [
        'Leggi le definizioni una a una.',
        'Inizia dalle più facili: ti danno lettere per le altre.',
        'Se ti blocchi, usa il pulsante Aiuto.',
        'Le parole che cerchi sono nelle pagine "Rischi" e "Numeri utili".'
      ],
      teoria: [
        { titolo: 'Glossario', url: '/glossario/' },
        { titolo: 'Rischi e prevenzione', url: '/rischi-prevenzione/' }
      ]
    },
    'labirinto-evacuazione': {
      fascia: 'primaria',
      titolo: 'Consigli per il Labirinto di Evacuazione',
      regola: 'Le regole dell\'evacuazione scolastica: niente ascensore, segui le frecce verdi, non tornare indietro.',
      come: [
        'NON usare l\'ascensore: in emergenza può fermarsi senza corrente.',
        'Segui le frecce VERDI: indicano la via di fuga sicura.',
        'Evita fuoco e fumo: cerca un\'altra strada.',
        'Non tornare indietro a prendere oggetti o amici.',
        'Raggiungi il punto di raccolta e resta in fila.'
      ],
      teoria: [
        { titolo: 'Rischio incendio', url: '/rischi-prevenzione/rischio-incendio/' },
        { titolo: 'Piano familiare', url: '/piano-familiare/' }
      ]
    },
    'memory': {
      fascia: 'primaria',
      titolo: 'Consigli per il Memory dei Segnali',
      regola: 'Ogni segnale ISO 7010 di sicurezza si abbina al comportamento corretto.',
      come: [
        'Scegli un livello (4, 6 o 8 coppie).',
        'Gira una carta: è un pittogramma o una frase di comportamento.',
        'Cerca la coppia: la "Scala antincendio" si abbina a "Mai ascensore se c\'è allarme".',
        'Dopo ogni coppia leggi la spiegazione del segnale.',
        'Memorizza dove sono le carte già viste per fare meno mosse.'
      ],
      teoria: [
        { titolo: 'Cosa fare adesso', url: '/cosa-fare-adesso/' },
        { titolo: 'Pittogrammi di sicurezza', url: '/pittogrammi/' }
      ]
    },
    'posiziona-cartelli': {
      fascia: 'primaria',
      titolo: 'Consigli per Posiziona i Cartelli',
      regola: 'I cartelli si mettono dove servono davvero: leggi cosa dice ogni posto.',
      come: [
        'Ogni posto vuoto ha una scritta breve (es. "Primo soccorso").',
        'Cerca il cartello con la stessa funzione.',
        'Forme e colori aiutano: rosso = divieto, blu = obbligo, verde = sicurezza, giallo = pericolo.',
        'L\'estintore si mette vicino ai pericoli di incendio, non in giardino.'
      ],
      teoria: [
        { titolo: 'Pittogrammi della sicurezza', url: '/pittogrammi/' }
      ]
    },
    'puzzle-scenari': {
      fascia: 'primaria',
      titolo: 'Consigli per Puzzle Scenari',
      regola: 'Ricostruisci la scena per capire come si gestisce un\'emergenza.',
      come: [
        'Guarda i pezzi prima di muoverli.',
        'Inizia dagli angoli e dai bordi.',
        'I colori e le forme aiutano a unire i pezzi.',
        'Quando finisci, leggi cosa rappresenta la scena.'
      ],
      teoria: [
        { titolo: 'Rischi e prevenzione', url: '/rischi-prevenzione/' }
      ]
    },
    'quiz': {
      fascia: 'primaria',
      titolo: 'Consigli per il Quiz della Sicurezza',
      regola: 'Le domande riguardano i rischi e i comportamenti corretti.',
      come: [
        'Leggi tutta la domanda prima di rispondere.',
        'Tutte le risposte sembrano possibili: scegli la più sicura.',
        'Se non sai, le pagine "Rischi" e "Numeri utili" spiegano il perché.',
        'Sbagliare aiuta a imparare: leggi la spiegazione dopo l\'errore.'
      ],
      teoria: [
        { titolo: 'Rischi e prevenzione', url: '/rischi-prevenzione/' },
        { titolo: 'Numeri utili', url: '/numeri-utili/' }
      ]
    },
    'semaforo-rischio': {
      fascia: 'primaria',
      titolo: 'Consigli per il Semaforo del Rischio',
      regola: 'Verde sicuro, giallo attenzione, rosso pericolo: come l\'allerta meteo.',
      come: [
        'Verde = puoi farlo, è sicuro.',
        'Giallo = stai attento, c\'è un piccolo rischio.',
        'Rosso = NO, è pericoloso o vietato.',
        'I codici colore della Protezione Civile funzionano così.'
      ],
      teoria: [
        { titolo: 'Allerte meteo e codici colore', url: '/allerte-meteo/' }
      ]
    },
    'zaino-emergenza': {
      fascia: 'primaria',
      titolo: 'Consigli per lo Zaino dell\'Emergenza',
      regola: 'Lo zaino di emergenza ha cose utili, non comode. Pochi oggetti, ben scelti.',
      come: [
        'Mettono dentro: acqua, cibo a lunga conservazione, torcia, radio, medicine, documenti, fischietto.',
        'NON metti dentro: videogiochi, peluche, oggetti pesanti.',
        'Lo zaino deve poterlo portare anche un bambino.',
        'Va lasciato vicino alla porta di casa, pronto.'
      ],
      teoria: [
        { titolo: 'Kit di emergenza', url: '/rischi-prevenzione/kit-emergenza/' },
        { titolo: 'Piano familiare', url: '/piano-familiare/' }
      ]
    },

    /* ── RAGAZZI (11-14 anni) — testo articolato + fonti ── */
    'cartelli-pericolo': {
      fascia: 'ragazzi',
      titolo: 'Consigli per i Cartelli di Pericolo',
      regola: 'Tre famiglie distinte: CLP per le sostanze chimiche (diamante bianco/rosso), ADR per il trasporto (diamante colorato con numero), UNI EN ISO 7010 per la sicurezza nei luoghi (forme/colori standard).',
      come: [
        'CLP: i nove pittogrammi UE per le sostanze pericolose vendute (es. infiammabile, tossico, corrosivo).',
        'ADR: classi di pericolo nel trasporto su strada (1=esplosivo, 2=gas, 3=liquido infiammabile, 7=radioattivo).',
        'ISO 7010: triangolo giallo=pericolo, cerchio rosso=divieto, cerchio blu=obbligo, quadrato verde=salvataggio, quadrato rosso=antincendio.',
        'Se non riconosci una famiglia, guarda la forma: triangolo, cerchio o quadrato.'
      ],
      teoria: [
        { titolo: 'Pittogrammi della sicurezza', url: '/pittogrammi/' },
        { titolo: 'Rischio incendio', url: '/rischi-prevenzione/rischio-incendio/' }
      ]
    },
    'codice-arancione': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Codice Arancione',
      regola: 'Allerta arancione = criticità moderata: prepararsi nelle prossime 24 ore. Non è ancora rosso, ma serve azione concreta.',
      come: [
        'Verifica il bollettino del Centro Funzionale Regionale Lazio: la fonte ufficiale, mai i social.',
        'Controlla zone allagabili, scantinati, garage: sposta cose preziose.',
        'Tieni pronto il kit di emergenza vicino alla porta.',
        'Allerta i familiari fragili (anziani, persone con disabilità).',
        'Limita gli spostamenti non necessari.'
      ],
      teoria: [
        { titolo: 'Allerte meteo', url: '/allerte-meteo/' },
        { titolo: 'Rischio idrogeologico', url: '/rischi-prevenzione/rischio-idrogeologico/' },
        { titolo: 'Kit di emergenza', url: '/rischi-prevenzione/kit-emergenza/' }
      ]
    },
    'emergency-responder': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Emergency Responder',
      regola: 'In emergenza pensi prima alle persone in pericolo, poi alla logistica. Le tue scelte hanno conseguenze.',
      come: [
        'Sicurezza personale prima: non puoi aiutare se ti fai male.',
        'Comunica subito alla Sala Operativa: cosa, dove, quanti.',
        'Priorità ai vulnerabili: bambini, anziani, persone con disabilità.',
        'Non sei un eroe da solo: lavori in squadra coordinata.',
        'Documenta tutto: i tempi e le decisioni servono dopo.'
      ],
      teoria: [
        { titolo: 'Diventa volontario', url: '/diventa-volontario/' },
        { titolo: 'Chi siamo', url: '/chi-siamo/' }
      ]
    },
    'linea-tempo-eventi': {
      fascia: 'ragazzi',
      titolo: 'Consigli per la Linea del Tempo',
      regola: 'Otto eventi che hanno cambiato la Protezione Civile italiana. Ognuno ha modificato leggi, organizzazione o tecnologie.',
      come: [
        'Parti dai più antichi: Vajont 1963, Friuli 1976, Irpinia 1980 sono i fondativi.',
        'L\'Aquila 2009 ha portato la valutazione del rischio sismico moderna.',
        'Centro Italia 2016 ha consolidato il sistema di gestione COC e COM.',
        'Se non sai un anno, ragiona sul contesto storico (TV in bianco e nero? smartphone già diffusi?).'
      ],
      teoria: [
        { titolo: 'Storia della Protezione Civile', url: '/chi-siamo/' },
        { titolo: 'Quadro normativo', url: '/normativa/' }
      ]
    },
    'mappa-rischio': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Mappa del Rischio',
      regola: 'Ogni territorio ha rischi specifici. Il Piano comunale di emergenza colloca aree di accoglienza, vie di fuga e presidi in funzione di geologia, urbanizzazione e accessibilità.',
      come: [
        'Aree di accoglienza, tendopoli, eliporti: spazi aperti pianeggianti (parco, area scuole).',
        'Versanti collinari del cratere: rischio frana e dissesto idrogeologico.',
        'Centro storico di Genzano: edifici antichi, sismico amplificato, vie di fuga strette.',
        'Caserme VVF e PMA: lungo strade primarie per accesso rapido dei mezzi.',
        'Distrattori (porto, centrale nucleare, metro): non si applicano a Genzano. Riconoscili.'
      ],
      teoria: [
        { titolo: 'Rischi e prevenzione', url: '/rischi-prevenzione/' },
        { titolo: 'Cartografia del territorio', url: '/cartografia/' },
        { titolo: 'Piano di emergenza', url: '/piano-emergenza/' }
      ]
    },
    'radio-emergency': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Radio Emergency',
      regola: 'Comunicare in radio è diverso dal parlare: alfabeto fonetico NATO, formato messaggio standard, parole chiave precise.',
      come: [
        'Alfabeto NATO: A=Alfa, B=Bravo, C=Charlie… per evitare confusione su nomi e numeri.',
        'Premi PTT, aspetta 1 secondo, parla, rilascia.',
        'Formato: "Da [chi parla] a [chi chiama], [messaggio], cambio."',
        'Numeri si dicono cifra per cifra: 112 = "uno-uno-due", non "centododici".',
        'Quando hai finito: "passo" (aspetto risposta) o "chiudo" (fine comunicazione).'
      ],
      teoria: [
        { titolo: 'Radiocomunicazioni del Gruppo', url: '/comunicazioni/?categoria=Radiocomunicazioni' },
        { titolo: 'Diventa volontario', url: '/diventa-volontario/' }
      ]
    },
    'scelte-difficili': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Scelte Difficili',
      regola: 'In emergenza non c\'è la risposta perfetta: c\'è la migliore disponibile con le informazioni che hai.',
      come: [
        'Salvare vite viene prima di salvare beni.',
        'Una decisione presa in 10 secondi è meglio di una perfetta presa in 10 minuti.',
        'Comunica al coordinatore le scelte che fai: lavori in catena.',
        'Dopo l\'emergenza, riflettere sull\'errore migliora la prossima risposta.',
        'Le linee guida DPC ("Io non rischio") ti danno la base; il contesto fa il resto.'
      ],
      teoria: [
        { titolo: 'Cosa fare in emergenza', url: '/cosa-fare-adesso/' },
        { titolo: 'Diventa volontario', url: '/diventa-volontario/' }
      ]
    },
    'simulatore-coc': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Simulatore COC',
      regola: 'Il Centro Operativo Comunale coordina l\'emergenza a livello di Comune. Nove funzioni, ognuna con compiti precisi.',
      come: [
        'F1 Tecnica e pianificazione: coordina ingegneri, geologi, dati territoriali.',
        'F2 Sanità: ASL, 112, ambulanze, evacuazione di feriti.',
        'F3 Volontariato: gestisce le squadre PC.',
        'F4 Materiali e mezzi: logistica, cibo, coperte.',
        'F5 Servizi essenziali: luce, gas, acqua, comunicazioni.',
        'Il sindaco è l\'autorità di Protezione Civile sul territorio comunale (D.Lgs. 1/2018).'
      ],
      teoria: [
        { titolo: 'Quadro normativo', url: '/normativa/' },
        { titolo: 'Piano emergenza', url: '/piano-emergenza/' }
      ]
    },
    'triage-start': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Triage START',
      regola: 'Il triage START classifica i feriti con quattro codici colore. È pre-ospedaliero: serve a decidere chi soccorrere prima.',
      come: [
        'ROSSO: pericolo di vita immediato (respira male, sanguina molto).',
        'GIALLO: ferito grave ma stabile, può aspettare 30-60 minuti.',
        'VERDE: ferito leggero, cammina, può aspettare ore.',
        'NERO: deceduto o non recuperabile sul campo.',
        'In emergenza con tante vittime, gestire prima i ROSSI salva più vite che cercare di salvare tutti subito.'
      ],
      teoria: [
        { titolo: 'Numeri utili', url: '/numeri-utili/' },
        { titolo: 'Cosa fare in emergenza', url: '/cosa-fare-adesso/' }
      ]
    },
    'vero-o-bufala': {
      fascia: 'ragazzi',
      titolo: 'Consigli per Vero o Bufala',
      regola: 'In emergenza la disinformazione amplifica il danno. Verifica la fonte prima di credere o condividere.',
      come: [
        'Cerca la fonte ufficiale: DPC, Regione Lazio, INGV, Comune.',
        'Una notizia "esclusiva" non confermata da altre fonti è quasi sempre falsa.',
        'Le foto possono essere vecchie o di altri eventi: cerca con Google Immagini.',
        'I numeri allarmanti senza fonte ("100 vittime!") sono red flag.',
        'Mai amplificare per smentire: condividere il falso, anche per criticarlo, lo diffonde.'
      ],
      teoria: [
        { titolo: 'Social Media Policy del Gruppo', url: '/social-media-policy/' },
        { titolo: 'Allerte meteo (fonti ufficiali)', url: '/allerte-meteo/' }
      ]
    }
  };

  // ──────────────────────────────────────────────────────────
  // Stato e helpers
  // ──────────────────────────────────────────────────────────
  var dialogEl = null;
  var lastFocus = null;
  var hintEl = null;
  var currentUtterance = null;
  var currentSpeakBtn = null;

  function escHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ──────────────────────────────────────────────────────────
  // Text-to-speech via Web Speech API (browser-native, niente file MP3)
  // ──────────────────────────────────────────────────────────
  function ttsSupported() {
    return typeof window.speechSynthesis !== 'undefined' &&
           typeof window.SpeechSynthesisUtterance !== 'undefined';
  }

  function pickItalianVoice() {
    if (!ttsSupported()) return null;
    var voices = window.speechSynthesis.getVoices() || [];
    return voices.find(function(v){ return v.lang === 'it-IT'; }) ||
           voices.find(function(v){ return v.lang && v.lang.indexOf('it') === 0; }) ||
           null;
  }

  function stopSpeaking() {
    if (!ttsSupported()) return;
    try { window.speechSynthesis.cancel(); } catch (e) { /* noop */ }
    if (currentSpeakBtn) {
      currentSpeakBtn.classList.remove('speaking');
      currentSpeakBtn.setAttribute('aria-label', currentSpeakBtn.dataset.labelPlay || 'Ascolta');
      currentSpeakBtn.querySelector('.coach-speak-text').textContent = currentSpeakBtn.dataset.textPlay || 'Ascolta';
    }
    currentUtterance = null;
    currentSpeakBtn = null;
  }

  function speak(text, btn) {
    if (!ttsSupported() || !text) return false;
    // Se sta già parlando lo stesso bottone: stop (toggle)
    if (currentSpeakBtn === btn && window.speechSynthesis.speaking) {
      stopSpeaking();
      return true;
    }
    stopSpeaking();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = 'it-IT';
    u.rate = 0.9;
    u.pitch = 1;
    var voice = pickItalianVoice();
    if (voice) u.voice = voice;
    u.onend = function () {
      if (currentSpeakBtn === btn) stopSpeaking();
    };
    u.onerror = function () {
      if (currentSpeakBtn === btn) stopSpeaking();
    };
    currentUtterance = u;
    currentSpeakBtn = btn;
    if (btn) {
      btn.classList.add('speaking');
      btn.setAttribute('aria-label', btn.dataset.labelStop || 'Ferma lettura');
      btn.querySelector('.coach-speak-text').textContent = btn.dataset.textStop || 'Ferma';
    }
    window.speechSynthesis.speak(u);
    return true;
  }

  function makeSpeakButton(text, labelPlay, textPlay) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'coach-speak-btn';
    btn.dataset.labelPlay = labelPlay || 'Ascolta';
    btn.dataset.labelStop = 'Ferma lettura';
    btn.dataset.textPlay = textPlay || 'Ascolta';
    btn.dataset.textStop = 'Ferma';
    btn.setAttribute('aria-label', btn.dataset.labelPlay);
    btn.innerHTML = '<span class="coach-speak-icon" aria-hidden="true">🔊</span><span class="coach-speak-text">' + escHtml(btn.dataset.textPlay) + '</span>';
    btn.addEventListener('click', function () { speak(text, btn); });
    return btn;
  }

  function buildSpeechText(c) {
    var parts = [];
    if (c.titolo) parts.push(c.titolo + '.');
    if (c.regola) parts.push(c.regola);
    if (c.come && c.come.length) {
      parts.push('Come si gioca.');
      c.come.forEach(function (item) { parts.push(item); });
    }
    return parts.join(' ');
  }

  function trapFocus(container, e) {
    if (e.key !== 'Tab') return;
    var focusable = container.querySelectorAll(
      'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable.length) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  // ──────────────────────────────────────────────────────────
  // Apertura / chiusura dialog
  // ──────────────────────────────────────────────────────────
  function open(gameId) {
    var c = CONTENUTI[gameId];
    if (!c) {
      console.warn('[GameCoach] gioco non in manifest:', gameId);
      return;
    }
    if (dialogEl) close();

    lastFocus = document.activeElement;

    var backdrop = document.createElement('div');
    backdrop.className = 'coach-backdrop';
    backdrop.addEventListener('click', function (e) {
      if (e.target === backdrop) close();
    });

    var dialog = document.createElement('div');
    dialog.className = 'coach-dialog';
    dialog.setAttribute('role', 'dialog');
    dialog.setAttribute('aria-modal', 'true');
    dialog.setAttribute('aria-labelledby', 'coach-title');
    dialog.dataset.fascia = c.fascia;
    dialog.tabIndex = -1;

    var html = '';
    html += '<button type="button" class="coach-btn-x" aria-label="Chiudi consigli">&times;</button>';
    html += '<h2 id="coach-title"><span aria-hidden="true">💡</span> ' + escHtml(c.titolo) + '</h2>';
    html += '<div class="coach-speak-row" data-coach-tts-anchor></div>';
    html += '<div class="coach-regola">' + escHtml(c.regola) + '</div>';
    if (c.come && c.come.length) {
      html += '<h3>Come si gioca</h3>';
      html += '<ul class="coach-come">';
      c.come.forEach(function (item) {
        html += '<li>' + escHtml(item) + '</li>';
      });
      html += '</ul>';
    }
    if (c.teoria && c.teoria.length) {
      html += '<div class="coach-teoria">';
      html += '<h3>Approfondisci sul sito</h3>';
      html += '<ul>';
      c.teoria.forEach(function (link) {
        html += '<li><a href="' + escHtml(link.url) + '">' + escHtml(link.titolo) + '</a></li>';
      });
      html += '</ul>';
      html += '</div>';
    }
    html += '<div class="coach-actions">';
    html += '<button type="button" class="coach-btn-close">Ho capito, gioco!</button>';
    html += '</div>';

    dialog.innerHTML = html;
    backdrop.appendChild(dialog);
    document.body.appendChild(backdrop);
    dialogEl = backdrop;

    // Bottone TTS "Ascolta i consigli" — solo se la Web Speech API è supportata
    if (ttsSupported()) {
      var anchor = dialog.querySelector('[data-coach-tts-anchor]');
      var speechText = buildSpeechText(c);
      var speakBtn = makeSpeakButton(speechText, 'Ascolta i consigli ad alta voce', 'Ascolta i consigli');
      anchor.appendChild(speakBtn);
    }

    dialog.querySelector('.coach-btn-x').addEventListener('click', close);
    dialog.querySelector('.coach-btn-close').addEventListener('click', close);
    document.addEventListener('keydown', onKeydown);

    setTimeout(function () { dialog.focus(); }, 30);
  }

  function close() {
    if (!dialogEl) return;
    stopSpeaking();
    dialogEl.remove();
    dialogEl = null;
    document.removeEventListener('keydown', onKeydown);
    if (lastFocus && typeof lastFocus.focus === 'function') {
      try { lastFocus.focus(); } catch (e) { /* noop */ }
    }
  }

  function onKeydown(e) {
    if (!dialogEl) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      close();
      return;
    }
    var dialog = dialogEl.querySelector('.coach-dialog');
    if (dialog) trapFocus(dialog, e);
  }

  // ──────────────────────────────────────────────────────────
  // Hint contestuale (chiamato dai giochi su errore)
  // ──────────────────────────────────────────────────────────
  function hint(testo, urlOpz) {
    clearHint();
    var trigger = document.querySelector('.coach-trigger');
    if (!trigger) return;
    hintEl = document.createElement('div');
    hintEl.className = 'coach-hint';
    hintEl.setAttribute('role', 'status');
    hintEl.setAttribute('aria-live', 'polite');
    var inner = document.createElement('div');
    inner.className = 'coach-hint-text';
    var introHtml = '<strong>Suggerimento:</strong> ' + escHtml(testo);
    if (urlOpz) {
      introHtml += '<br><a href="' + escHtml(urlOpz) + '">Scopri perché →</a>';
    }
    inner.innerHTML = introHtml;
    hintEl.appendChild(inner);
    if (ttsSupported()) {
      var speakBtn = makeSpeakButton(testo, 'Ascolta il suggerimento ad alta voce', 'Ascolta');
      speakBtn.classList.add('coach-speak-btn-mini');
      hintEl.appendChild(speakBtn);
    }
    trigger.parentNode.insertBefore(hintEl, trigger.nextSibling);
  }

  function clearHint() {
    if (hintEl && hintEl.parentNode) {
      // Se sta leggendo l'hint corrente, ferma la voce
      if (currentSpeakBtn && hintEl.contains(currentSpeakBtn)) {
        stopSpeaking();
      }
      hintEl.parentNode.removeChild(hintEl);
    }
    hintEl = null;
  }

  // ──────────────────────────────────────────────────────────
  // Auto-init: cerca data-coach-game, inserisce il bottone
  // ──────────────────────────────────────────────────────────
  function autoInit() {
    var host = document.querySelector('[data-coach-game]');
    if (!host) return;
    var gameId = host.getAttribute('data-coach-game');
    if (!CONTENUTI[gameId]) {
      console.warn('[GameCoach] gioco senza manifest:', gameId);
      return;
    }

    // Trova il punto di inserzione: dopo H1 o all'inizio del main
    var anchor = document.querySelector('main h1, .app-page-hero h1, .inf-home h1');
    if (!anchor) {
      anchor = document.querySelector('main') || document.body.firstElementChild;
    }

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'coach-trigger';
    btn.setAttribute('aria-haspopup', 'dialog');
    btn.innerHTML = '<span class="coach-trigger-icon" aria-hidden="true">💡</span> Consigli per giocare';
    btn.addEventListener('click', function () { open(gameId); });

    // Inserisci dopo il riferimento (lead/sottotitolo se esiste, altrimenti dopo H1)
    var afterAnchor = anchor.parentNode.querySelector('.lead, p.lead');
    var insertAfter = afterAnchor && afterAnchor.parentNode === anchor.parentNode ? afterAnchor : anchor;
    if (insertAfter.nextSibling) {
      insertAfter.parentNode.insertBefore(btn, insertAfter.nextSibling);
    } else {
      insertAfter.parentNode.appendChild(btn);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoInit);
  } else {
    autoInit();
  }

  // Stop speech quando l'utente lascia la pagina o passa in background
  if (typeof window !== 'undefined' && window.addEventListener) {
    window.addEventListener('pagehide', stopSpeaking);
    window.addEventListener('beforeunload', stopSpeaking);
  }

  // Esporta API pubblica
  window.GameCoach = {
    open: open,
    close: close,
    hint: hint,
    clearHint: clearHint,
    speak: speak,
    stopSpeaking: stopSpeaking,
    ttsSupported: ttsSupported,
    /* ammesso solo a fini di test/debug */
    _manifest: CONTENUTI
  };
})();
