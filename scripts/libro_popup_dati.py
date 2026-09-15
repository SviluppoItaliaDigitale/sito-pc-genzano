#!/usr/bin/env python3
"""Contenuti del libro pop-up: una tavola per rischio documentato dal sito.

Le frasi non si inventano qui. Ogni tavola dichiara la pagina del sito da cui
vengono le indicazioni di autoprotezione, e quella pagina cita a sua volta la
fonte istituzionale. Se una pagina del sito cambia, questa lista va riletta:
il libro finisce stampato e appeso in classe, dove nessuno lo aggiorna più.
"""

# scena = figura che sta sul gradino e si alza dalla pagina
# pitto = figura a lato del testo
TAVOLE = [
    {
        "id": "tav1", "tema": "LA SQUADRA DELLA SICUREZZA",
        "titolo": "Chi è la Protezione Civile",
        "sottotitolo": "Il Sindaco, i volontari e il numero da chiamare",
        "intro": "La <strong>Protezione Civile</strong> è fatta di persone che si preparano "
                 "prima che succeda qualcosa, e che intervengono quando succede: per proteggere "
                 "le persone, gli animali, le case e l'ambiente. Nel Comune la prima autorità di "
                 "protezione civile è il <strong>Sindaco</strong>. I <strong>volontari</strong> "
                 "sono cittadini che si sono formati e danno il loro tempo: non sono pagati, e si "
                 "riconoscono dalla divisa ad alta visibilità.",
        "regole": [
            "I volontari non si chiamano direttamente: in emergenza si chiama il 112.",
            "Il bollettino di allerta dice che tempo è previsto, non che cosa è già successo.",
            "Prepararsi prima serve più che correre dopo.",
        ],
        "pitto": ("alf-p-protezione-civile.png", "Simbolo della protezione civile"),
        "scena": ("dis-volontari.png", "Volontari in divisa"),
        "scena_eti": "I VOLONTARI",
        "fonte": "pagine «Chi siamo» e «Allerte meteo» del sito",
    },
    {
        "id": "tav2", "tema": "TERREMOTO",
        "titolo": "Sotto il tavolo, e tieni la testa",
        "sottotitolo": "Che cosa fare mentre la terra trema, e che cosa fare dopo",
        "intro": "Durante una scossa la cosa più pericolosa non è il pavimento che si muove: "
                 "sono le <strong>cose che cadono</strong>. Un tavolo robusto ti fa da tetto.",
        "regole": [
            "Mettiti sotto un tavolo robusto e copriti la testa con le braccia.",
            "Non correre fuori mentre trema: le cose cadono proprio davanti alle porte.",
            "Sta' lontano da finestre, vetri, specchi e mobili pesanti.",
            "Non prendere l'ascensore. Quando la scossa finisce, esci con calma dalle scale.",
            "Se sei all'aperto, va' in uno spazio aperto, lontano da edifici e alberi.",
        ],
        "pitto": ("alf-t-terremoto.png", "Persona che si ripara sotto un tavolo"),
        "scena": ("pop-tavolo.png", "Tavolo robusto visto di lato"),
        "scena_eti": "IL TAVOLO",
        "fonte": "pagina «Rischio sismico» del sito",
    },
    {
        "id": "tav3", "tema": "ALLUVIONE",
        "titolo": "Si sale, non si scende",
        "sottotitolo": "L'acqua riempie prima le cantine: i piani alti sono il posto giusto",
        "intro": "Quando arriva tanta acqua, riempie per prima la parte più bassa della casa: "
                 "<strong>cantine, garage e locali interrati</strong>. È lì che non si va, "
                 "nemmeno per prendere qualcosa.",
        "regole": [
            "Sali ai piani alti della casa.",
            "Non scendere in cantina, in garage o nei locali interrati.",
            "Non attraversare strade allagate, né a piedi né in auto: non si vede quanto è profondo.",
            "Sta' lontano da fossi, ponti e corsi d'acqua.",
            "Se un adulto te lo chiede, aiuta a chiudere le porte verso i locali più bassi.",
        ],
        "pitto": ("oca-pioggia.png", "Pioggia forte"),
        "scena": ("pop-scala.png", "Scala che porta ai piani alti"),
        "scena_eti": "LE SCALE",
        "fonte": "pagina «Rischio idrogeologico» del sito",
    },
    {
        "id": "tav4", "tema": "TEMPORALE E FULMINI",
        "titolo": "Quando tuona, si entra",
        "sottotitolo": "Il posto sicuro è dentro un edificio, non sotto un albero",
        "intro": "Durante un temporale il posto sicuro è <strong>dentro</strong>: un edificio "
                 "solido, oppure un'auto con i finestrini chiusi. Un albero isolato non è un "
                 "riparo, e una tettoia leggera nemmeno.",
        "regole": [
            "Entra in un edificio solido, oppure in auto con i finestrini chiusi.",
            "Sta' lontano da alberi isolati, pali di metallo e recinzioni metalliche.",
            "Non ripararti sotto una tettoia o una struttura leggera.",
            "Dentro casa, sta' lontano dalle finestre e dalle porte finestre.",
            "Non attraversare un sottopassaggio allagato.",
        ],
        "pitto": ("dis-temporale.png", "Nuvola con pioggia e fulmine"),
        "scena": ("pop-casa.png", "Casa vista di fronte"),
        "scena_eti": "DENTRO CASA",
        "fonte": "pagina «Temporali intensi» del sito",
    },
    {
        "id": "tav5", "tema": "VENTO FORTE",
        "titolo": "Il pericolo è quello che vola",
        "sottotitolo": "Non è il vento a far male: sono i rami, le tegole e i cartelloni",
        "intro": "Con il vento forte il pericolo non è l'aria che spinge: sono le cose che si "
                 "staccano e <strong>volano</strong> — rami, tegole, vasi, cartelloni. Per "
                 "questo si sta lontani da tutto ciò che può cadere.",
        "regole": [
            "Resta in casa, lontano da finestre e vetrate.",
            "Se sei fuori, allontanati da alberi, pali della luce, impalcature e cartelloni.",
            "Non fermarti sotto un cornicione o sotto qualcosa di appeso.",
            "Tieni chiuse porte e finestre.",
            "Un cavo elettrico caduto non si tocca mai: dillo a un adulto, che chiama il 112.",
        ],
        "pitto": ("alf-w-warning.png", "Segnale di pericolo generico"),
        "scena": ("oca-albero.png", "Albero piegato dal vento"),
        "scena_eti": "L'ALBERO",
        "fonte": "pagina «Vento forte» del sito",
    },
    {
        "id": "tav6", "tema": "INCENDIO FUORI, NEL BOSCO",
        "titolo": "Va' via dalla parte opposta al fumo",
        "sottotitolo": "Nel bosco e nei campi ci si allontana: qui non si striscia",
        "intro": "Un incendio in un bosco o in un campo si muove <strong>con il vento</strong> e "
                 "può correre più di una persona. Qui la regola non è stare bassi: è "
                 "<strong>andare via</strong>, dalla parte da cui il fumo non arriva.",
        "regole": [
            "Di' subito a un adulto di chiamare il 112, oppure chiamalo tu.",
            "Allontanati nella direzione opposta a quella in cui va il fumo.",
            "Non avvicinarti alle fiamme e non provare a spegnerle.",
            "Non fermarti nelle strade dove passa il fumo.",
            "Se non puoi allontanarti, entra in casa e chiudi porte, finestre e persiane.",
        ],
        "pitto": ("alf-i-incendio.png", "Incendio"),
        "scena": ("pop-fuoco.png", "Fiamme in un campo"),
        "scena_eti": "IL FUOCO",
        "fonte": "pagina «Rischio incendi boschivi» del sito",
    },
    {
        "id": "tav7", "tema": "INCENDIO DENTRO CASA",
        "titolo": "Il fumo sta in alto, tu sta' in basso",
        "sottotitolo": "Dentro un edificio la regola si capovolge: si esce rasoterra",
        "intro": "Il fumo è caldo, quindi <strong>sale verso il soffitto</strong>. L'aria che si "
                 "respira resta in basso, a circa <strong>30-40 centimetri da terra</strong>. "
                 "Per questo, se c'è molto fumo, si esce procedendo a carponi.",
        "regole": [
            "Se c'è molto fumo, va' a carponi verso l'uscita: in basso si respira.",
            "Non usare l'ascensore.",
            "Non aprire una porta se al tocco è calda: dietro c'è il fuoco.",
            "Chiama il 112 quando sei fuori, in un posto sicuro.",
            "Una volta fuori non rientrare: si torna dentro quando lo dicono i vigili del fuoco.",
        ],
        "pitto": ("alf-u-uscita.png", "Persona che esce da una porta aperta"),
        "scena": ("pop-strisciare.png", "Persona che avanza carponi sotto il fumo"),
        "scena_eti": "A CARPONI",
        "fonte": "articolo «Incendi domestici» del sito, che cita i Vigili del Fuoco",
    },
    {
        "id": "tav8", "tema": "CALDO",
        "titolo": "Bevi prima di avere sete",
        "sottotitolo": "Nelle ore più calde si sta all'ombra, e in macchina non resta nessuno",
        "intro": "Quando fa molto caldo il corpo fatica a raffreddarsi, e la sete arriva "
                 "<strong>dopo</strong> che il corpo ha già cominciato a soffrire. Per questo "
                 "si beve prima, e all'ombra ci si sta per scelta, non per premio.",
        "regole": [
            "Bevi acqua spesso, anche se non hai sete.",
            "Nelle ore più calde, fra le 11 e le 17, resta all'ombra o in casa.",
            "Metti vestiti leggeri e chiari, il cappello e gli occhiali da sole.",
            "In casa abbassa le tapparelle quando il sole batte sulla finestra.",
            "In una macchina parcheggiata al sole non resta nessuno: né le persone né gli animali.",
        ],
        "pitto": ("dis-sole.png", "Sole"),
        "scena": ("oca-bottiglia.png", "Bottiglia d'acqua"),
        "scena_eti": "L'ACQUA",
        "fonte": "pagina «Ondate di calore» del sito",
    },
    {
        "id": "tav9", "tema": "BLACKOUT",
        "titolo": "Via la luce: si accende la torcia",
        "sottotitolo": "Non la candela, e il frigorifero resta chiuso",
        "intro": "Quando va via la corrente di solito non è successo niente di grave, e torna da "
                 "sola. La candela invece può dare fuoco alle cose: la <strong>torcia</strong> no.",
        "regole": [
            "Usa la torcia elettrica, non le candele.",
            "Tieni chiusi il frigorifero e il congelatore: il cibo si conserva per ore.",
            "Non prendere l'ascensore.",
            "Se sei in ascensore quando va via la luce, premi il pulsante di allarme e aspetta: "
            "non provare a uscire da solo.",
            "Lasciate accesa una sola lampada: così vi accorgete quando la corrente torna.",
        ],
        "pitto": ("dis-radio.png", "Radio a pile"),
        "scena": ("oca-torcia.png", "Torcia elettrica accesa"),
        "scena_eti": "LA TORCIA",
        "fonte": "pagina «Blackout» del sito",
    },
    {
        "id": "tav10", "tema": "BUCHE E POSTI CHIUSI",
        "titolo": "Nelle buche non si entra",
        "sottotitolo": "Dalle nostre parti certi gas si fermano in basso, dove non si vedono",
        "intro": "Ai Castelli Romani, sotto terra, c'è un gas che ogni tanto esce dal suolo. "
                 "<strong>Non ha odore</strong> ed è pesante: si ferma nei posti bassi e chiusi, "
                 "come pozzi, cantine e buche. Chi entra non si accorge di niente.",
        "regole": [
            "Non entrare mai in un pozzo, in una buca o in una cantina che non conosci.",
            "Se una persona è dentro e non risponde, <strong>non entrare a prenderla</strong>: "
            "chi entra per aiutare diventa la seconda persona in pericolo.",
            "Chiama subito un adulto e il 112, e di' che c'è qualcuno dentro un posto chiuso.",
            "Tieni lontani gli altri e aspetta i vigili del fuoco: hanno le bombole per respirare.",
            "Il gas per cucinare ha un odore aggiunto apposta, diverso da quello delle buche: se lo senti "
            "in casa, non accendere niente, apri le finestre, esci e chiama un adulto.",
        ],
        "pitto": ("alf-a-allerta.png", "Segnale di allerta"),
        "scena": ("alf-a-allerta.png", "Cartello di pericolo"),
        "scena_eti": "IL CARTELLO",
        "fonte": "pagina «Rischio vulcanico» del sito",
    },
    {
        "id": "tav11", "tema": "A SCUOLA",
        "titolo": "Suona l'allarme: in fila, fino al punto di raccolta",
        "sottotitolo": "L'uscita di emergenza si prova prima, così il giorno vero si sa già",
        "intro": "A scuola l'uscita di emergenza non si improvvisa: si <strong>prova</strong>. "
                 "Ogni classe ha una via di uscita, un punto di raccolta e due compagni con un "
                 "compito. Il giorno in cui suona davvero, si fa quello che si è provato.",
        "regole": [
            "Quando suona, lascia tutto dov'è: lo zaino resta, tu vai.",
            "Mettiti in fila e segui chi apre la fila.",
            "Cammina, non correre, e resta in silenzio per sentire le indicazioni.",
            "Al punto di raccolta resta con la tua classe finché non ti chiamano per nome.",
            "Non tornare indietro a prendere niente.",
        ],
        "pitto": ("pop-sirena.png", "Sirena di allarme"),
        "scena": ("pop-fila.png", "Bambini in fila verso l'uscita"),
        "scena_eti": "LA FILA",
        "fonte": "articolo «Le prove di evacuazione» del sito",
    },
    {
        "id": "tav12", "tema": "LO ZAINO",
        "titolo": "Che cosa c'è nello zaino di emergenza",
        "sottotitolo": "Si prepara quando non serve, e si controlla ogni sei mesi",
        "intro": "Lo zaino di emergenza è quello che si prende <strong>se bisogna uscire di casa "
                 "in fretta</strong>. Si prepara quando non serve, si tiene vicino alla porta, e "
                 "si controlla ogni sei mesi.",
        "regole": [
            "Ritaglia le tessere qui sotto e infila dietro il gradino quelle che servono davvero.",
            "Aggiungi la tua: una medicina che prendi, il gioco piccolo, la foto di famiglia.",
            "Ogni sei mesi controlla con un adulto: l'acqua scade e le pile si scaricano.",
        ],
        "pitto": ("alf-k-kit.png", "Kit di emergenza"),
        "scena": ("alf-z-zaino.png", "Zaino di emergenza"),
        "scena_eti": "LO ZAINO",
        "fonte": "pagina «Kit di emergenza» del sito",
        "tessere": [
            ("oca-bottiglia.png", "Acqua"), ("pop-scatoletta.png", "Cibo"),
            ("oca-torcia.png", "Torcia"), ("oca-radio.png", "Radio"),
            ("kcb-coperta.png", "Coperta"), ("alf-n-telefono.png", "Numeri"),
            ("dis-lettera.png", "Documenti"),
        ],
    },
    {
        "id": "tav13", "tema": "CHIEDERE AIUTO",
        "titolo": "La telefonata al 112",
        "sottotitolo": "Un numero solo, e quattro cose da dire",
        "intro": "In Italia il numero delle emergenze è <strong>uno solo: il 112</strong>. "
                 "Risponde una persona che ti fa delle domande e manda chi serve — l'ambulanza, "
                 "i vigili del fuoco o i carabinieri. È gratuito, e funziona anche dal telefono "
                 "di casa.",
        "regole": [
            "Di' dove sei: il paese, la via, il numero, un posto che si riconosce.",
            "Di' che cosa è successo, con parole semplici.",
            "Di' se c'è qualcuno che sta male, e quante persone siete.",
            "Rispondi alle domande e non chiudere finché non te lo dicono.",
            "Non chiamare il 112 per gioco: mentre parli tu, qualcuno aspetta davvero.",
        ],
        "pitto": ("alf-n-telefono.png", "Telefono"),
        "scena": ("dis-al-telefono.png", "Bambino che parla al telefono"),
        "scena_eti": "IL TELEFONO",
        "fonte": "pagina «Numeri utili» del sito",
    },
]
