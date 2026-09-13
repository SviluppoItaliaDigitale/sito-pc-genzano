# -*- coding: utf-8 -*-
"""Contenuti delle otto tavole del libro pop-up di protezione civile.

Ogni istruzione di autoprotezione è ripresa da una pagina già pubblicata sul
sito, che a sua volta cita la fonte istituzionale: le pagine del rischio
(campi howto_prima/durante/dopo), /allerte-meteo/ per i livelli, l'articolo
sugli incendi domestici (fonte Vigili del Fuoco) per il fumo in casa,
/numeri-utili/ per il 112. Il campo `fonte` di ogni tavola dice da dove
viene, e finisce stampato sul foglio: un docente deve poter risalire.

NIENTE si inventa qui. Se una frase non ha una pagina nostra alle spalle,
non entra nel libro.
"""

# I quattro livelli di allerta, nelle parole di /allerte-meteo/, accorciate
# per un bambino ma senza cambiarne il senso. La chiusura delle scuole NON
# compare: è un'ordinanza del Sindaco, non una conseguenza del colore.
ALLERTA = [
    ("VERDE",     "#16a34a", "Nessuna allerta",
     "Giornata normale. Niente da fare di speciale."),
    ("GIALLA",    "#ca8a04", "Attenzione",
     "Possono esserci temporali forti in qualche zona. Sta' lontano da fossi e sottopassaggi."),
    ("ARANCIONE", "#ea580c", "Preallarme",
     "I fenomeni possono essere diffusi. Si esce solo se serve, e il kit è pronto."),
    ("ROSSA",     "#dc2626", "Allarme",
     "Fenomeni molto intensi. Non si esce se non serve davvero, e si sta lontani dai piani interrati."),
]

# ---------------------------------------------------------------------------
# Le otto tavole. `meccanismo` sceglie il disegno tecnico della fustella.
# `regole` sono le frasi che il bambino legge: imperativi brevi, mai divieti
# assoluti senza scenario (gate materiali scolastici).
# ---------------------------------------------------------------------------
TAVOLE = [
    dict(
        n=1, id="tav1",
        tag="LA SQUADRA DELLA SICUREZZA",
        titolo="Chi è la Protezione Civile",
        sottotitolo="Il Sindaco, i volontari e il semaforo dell'allerta meteo",
        meccanismo="volvella",
        testo=(
            "La <strong>Protezione Civile</strong> è fatta di persone che si preparano "
            "prima che succeda qualcosa, e che intervengono quando succede: per "
            "proteggere le persone, gli animali, le case e l'ambiente.<br>"
            "Nel Comune la prima autorità di protezione civile è il <strong>Sindaco</strong>. "
            "I <strong>volontari</strong> sono cittadini che si sono formati e danno il "
            "loro tempo: non sono pagati, e si riconoscono dalla divisa ad alta visibilità."
        ),
        regole=[
            "I volontari non si chiamano direttamente: in emergenza si chiama il 112.",
            "Il bollettino di allerta dice che tempo è previsto, non che cosa è già successo.",
        ],
        pittogrammi=[("dis-volontari", "Due volontari in divisa aiutano e sostengono una persona"),
                     ("alf-y-semaforo", "Semaforo")],
        fonte="Livelli di allerta: pagina «Allerte meteo» del sito, che riprende il "
              "Centro Funzionale Regionale del Lazio.",
    ),
    dict(
        n=2, id="tav2",
        tag="TERREMOTO",
        titolo="Sotto il tavolo, e tieni la testa",
        sottotitolo="Che cosa fare mentre la terra trema, e che cosa fare dopo",
        meccanismo="vfold",
        figura=("pop-tavolo", "Tavolo robusto visto di lato"),
        testo=(
            "Durante una scossa la cosa più pericolosa non è il pavimento che si "
            "muove: sono le <strong>cose che cadono</strong>. Un tavolo robusto ti fa "
            "da tetto."
        ),
        regole=[
            "Mettiti sotto un tavolo robusto e copriti la testa con le braccia.",
            "Non correre fuori mentre trema: le cose cadono proprio davanti alle porte.",
            "Sta' lontano da finestre, vetri, specchi e mobili pesanti.",
            "Non prendere l'ascensore. Quando la scossa finisce, esci con calma dalle scale.",
            "Se sei all'aperto, va' in uno spazio aperto, lontano da edifici e alberi.",
        ],
        pittogrammi=[("alf-t-terremoto", "Persona che si ripara sotto un tavolo durante un terremoto")],
        fonte="Pagina «Rischio Sismico: Cosa Fare» del sito.",
    ),
    dict(
        n=3, id="tav3",
        tag="ALLUVIONE",
        titolo="Si sale, non si scende",
        sottotitolo="L'acqua riempie prima le cantine: i piani alti sono il posto giusto",
        meccanismo="gradino",
        figura=("pop-scala", "Scala con i gradini"),
        testo=(
            "Quando arriva tanta acqua, riempie per prima la parte più bassa della "
            "casa: <strong>cantine, garage e locali interrati</strong>. È lì che non "
            "si va, nemmeno per prendere qualcosa."
        ),
        regole=[
            "Sali ai piani alti della casa.",
            "Non scendere in cantina, in garage o nei locali interrati.",
            "Non attraversare strade allagate, né a piedi né in auto: non si vede quanto è profondo.",
            "Sta' lontano da fossi, ponti e corsi d'acqua.",
            "Se un adulto te lo chiede, aiuta a chiudere le porte verso i locali più bassi.",
        ],
        pittogrammi=[("oca-pioggia", "Pioggia forte"), ("pop-casa", "Casa")],
        fonte="Pagina «Rischio idrogeologico» del sito.",
    ),
    dict(
        n=4, id="tav4",
        tag="INCENDIO FUORI, NEL BOSCO",
        titolo="Va' via dalla parte opposta al fumo",
        sottotitolo="Nel bosco e nei campi ci si allontana: qui non si striscia",
        meccanismo="vfold",
        figura=("pop-fuoco", "Fiamme"),
        testo=(
            "Un incendio in un bosco o in un campo si muove <strong>con il vento</strong> "
            "e può correre più di una persona. Qui la regola non è stare bassi: è "
            "<strong>andare via</strong>, dalla parte da cui il fumo non arriva."
        ),
        regole=[
            "Di' subito a un adulto di chiamare il 112, oppure chiamalo tu.",
            "Allontanati nella direzione opposta a quella in cui va il fumo.",
            "Non avvicinarti alle fiamme e non provare a spegnerle.",
            "Non fermarti nelle strade dove passa il fumo.",
            "Se non puoi allontanarti, entra in casa e chiudi porte, finestre e persiane.",
        ],
        pittogrammi=[("alf-i-incendio", "Incendio"), ("dis-autopompa", "Autopompa dei vigili del fuoco")],
        fonte="Pagina «Rischio Incendi Boschivi» del sito.",
    ),
    dict(
        n=5, id="tav5",
        tag="INCENDIO DENTRO CASA",
        titolo="Il fumo sta in alto, tu sta' in basso",
        sottotitolo="Dentro un edificio la regola si capovolge: si esce rasoterra",
        meccanismo="linguetta",
        figura=("pop-strisciare", "Bambino disteso che avanza sotto una linea bassa"),
        testo=(
            "Il fumo è caldo, quindi <strong>sale verso il soffitto</strong>. L'aria "
            "che si respira resta in basso, a circa <strong>30-40 centimetri da "
            "terra</strong>. Per questo, se c'è molto fumo, si esce procedendo a "
            "carponi."
        ),
        regole=[
            "Se c'è molto fumo, va' a carponi verso l'uscita: in basso si respira.",
            "Non usare l'ascensore.",
            "Non aprire una porta se al tocco è calda: dietro c'è il fuoco.",
            "Chiama il 112 quando sei fuori, in un posto sicuro.",
            "Una volta fuori non rientrare: si torna dentro solo quando i vigili del fuoco dicono che si può.",
        ],
        pittogrammi=[("alf-u-uscita", "Persona che esce da una porta aperta"), ("pop-fuoco", "Fiamme")],
        fonte="Articolo «Incendi domestici: cause più comuni e come prevenirli» del sito, che cita i Vigili del Fuoco.",
    ),
    dict(
        n=6, id="tav6",
        tag="A SCUOLA",
        titolo="Suona l'allarme: in fila, fino al punto di raccolta",
        sottotitolo="L'uscita di emergenza si prova prima, così il giorno vero si sa già",
        meccanismo="gradino",
        figura=("pop-fila", "Cinque persone in fila indiana"),
        testo=(
            "A scuola l'uscita di emergenza non si improvvisa: si <strong>prova</strong>. "
            "Ogni classe ha una via di uscita, un punto di raccolta e due compagni con "
            "un compito. Il giorno in cui suona davvero, si fa quello che si è provato."
        ),
        regole=[
            "Quando suona, lascia tutto dov'è: lo zaino resta, tu vai.",
            "Mettiti in fila e segui chi apre la fila.",
            "Cammina, non correre, e resta in silenzio per sentire le indicazioni.",
            "Al punto di raccolta resta con la tua classe finché non ti chiamano per nome.",
            "Non tornare indietro a prendere niente.",
        ],
        pittogrammi=[("pop-sirena", "Sirena di allarme"), ("dis-cortile", "Cortile della scuola")],
        fonte="Articolo «Primo giorno di scuola: le prove di evacuazione non sono un dettaglio» del sito.",
    ),
    dict(
        n=7, id="tav7",
        tag="LO ZAINO",
        titolo="Che cosa c'è nello zaino di emergenza",
        sottotitolo="Una tasca da riempire con le tessere, e da rifare ogni sei mesi",
        meccanismo="tasca",
        figura=("alf-z-zaino", "Zaino"),
        testo=(
            "Lo zaino di emergenza è quello che si prende <strong>se bisogna uscire "
            "di casa in fretta</strong>. Si prepara quando non serve, si tiene vicino "
            "alla porta, e si controlla ogni sei mesi."
        ),
        regole=[
            "Ritaglia le tessere e metti nella tasca quelle che servono davvero.",
            "Aggiungi la tua: una medicina che prendi, il gioco piccolo, la foto di famiglia.",
            "Ogni sei mesi controlla con un adulto: l'acqua scade e le pile si scaricano.",
        ],
        tessere=[("dis-acqua", "Acqua"), ("oca-torcia", "Torcia"), ("oca-radio", "Radio a pile"),
                 ("alf-k-kit", "Cassetta di pronto soccorso"), ("dis-lettera", "Un foglio con i tuoi dati"),
                 ("pop-scatoletta", "Cibo in scatola"), ("dis-famiglia", "Numeri di famiglia")],
        pittogrammi=[("alf-z-zaino", "Zaino")],
        fonte="Pagina «Kit di emergenza: casa, evacuazione e auto» del sito.",
    ),
    dict(
        n=8, id="tav8",
        tag="CHIEDERE AIUTO",
        titolo="La telefonata al 112",
        sottotitolo="Un numero solo, e quattro cose da dire",
        meccanismo="linguetta",
        figura=("dis-al-telefono", "Persona che parla al telefono"),
        testo=(
            "In Italia il numero delle emergenze è <strong>uno solo: il 112</strong>. "
            "Risponde una persona che ti fa delle domande e manda chi serve — "
            "l'ambulanza, i vigili del fuoco o i carabinieri. È gratuito, e funziona "
            "anche dal telefono di casa."
        ),
        regole=[
            "Di' dove sei: il paese, la via, il numero, un posto che si riconosce.",
            "Di' che cosa è successo, con parole semplici.",
            "Di' se c'è qualcuno che sta male, e quante persone sono.",
            "Rispondi alle domande e non chiudere finché non te lo dicono.",
            "Non chiamare il 112 per gioco: mentre parli con te, qualcuno aspetta davvero.",
        ],
        pittogrammi=[("alf-n-telefono", "Telefono"), ("dis-ambulanza", "Ambulanza")],
        fonte="Pagina «Numeri utili» del sito.",
    ),
]
