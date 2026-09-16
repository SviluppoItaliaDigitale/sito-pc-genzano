#!/usr/bin/env python3
"""«Flavia, Flavio e lo zaino rosso» — la storia del libro pop-up, capitolo per capitolo.

Flavia (la treccia), Flavio (sette anni, il nonno del trekking) e Anna (la
volontaria col nome sul taschino) sono i personaggi delle fiabe già pubblicate
su /formazione/storie-e-racconti/. Qui Flavia e Flavio sono fratelli: nelle
fiabe non compaiono mai insieme, quindi niente si contraddice. La famiglia è
quella canonica: mamma, papà, nonna e nonno.

I due bambini sono alla pari. A turno uno è tentato di fare la cosa sbagliata
e l'altro sa: non c'è quello che sbaglia sempre. Nel capitolo del 112 sono
decisivi tutti e due.

Le regole in fondo a ogni capitolo NON sono scritte qui: vengono prese, parola
per parola, da `libro_popup_dati.py`, dove sono già state verificate contro le
pagine del sito e le fonti istituzionali. `regole` indica la tavola e gli
indici delle frasi da mostrare. Se una regola cambia là, cambia anche qui.

Registro: lettura ad alta voce, dai 4 anni. Frasi corte, un ritornello che
insegna a fermarsi prima di agire — «Respiro. Guardo. So cosa fare.» — mai
un «non avere paura»: la paura non si vieta, si attraversa.
"""

TITOLO = "Flavia, Flavio e lo zaino rosso"
SOTTOTITOLO = "Un anno di piccole emergenze, dodici pop-up da alzare"
RITORNELLO = "Respiro. Guardo. So cosa fare."

CAPITOLI = [
    {
        "id": "cap1", "titolo": "Lo zaino rosso", "stagione": "settembre",
        "icona": ("alf-z-zaino.png", "Icona: zaino"),
        "testo": [
            "Un mattino, a scuola, arrivò Anna. Aveva la divisa ad alta visibilità dei "
            "volontari della Protezione Civile e, sul taschino, il suo nome.",
            "«Noi ci prepariamo prima», disse ai bambini. «Così, quando succede qualcosa, "
            "sappiamo già cosa fare.»",
            "Poi aprì uno zaino rosso: una bottiglia d'acqua, una torcia, una radio, una "
            "coperta, un foglio con i numeri importanti.",
            "«Si tiene vicino alla porta», disse Anna. «E si controlla ogni sei mesi, "
            "perché l'acqua scade e le pile si scaricano.»",
            "Flavia e Flavio si guardarono. Le cose da fare, loro le volevano sapere "
            "tutte.",
        ],
        "regole": [("tav1", [0]), ("tav12", [2])],
        "scena": "zaino",
    },
    {
        "id": "cap2", "titolo": "La terra trema", "stagione": "ottobre",
        "icona": ("alf-t-terremoto.png", "Icona: bambino accovacciato sotto un tavolo"),
        "testo": [
            "Una sera i due fratelli costruivano una torre sul tappeto. All'improvviso la "
            "torre tremò. Poi tremarono i bicchieri, la lampada, la casa intera.",
            "Flavio scattò verso la porta. «No!», disse Flavia. «Le cose cadono proprio lì "
            "davanti. Sotto il tavolo!»",
            "Respirarono. Guardarono. Sapevano cosa fare.",
            "Andarono sotto il tavolo grande della cucina e si coprirono la testa con le "
            "braccia, mentre la mamma li teneva vicini.",
            "Quando tutto fu fermo, uscirono con calma dalle scale, senza ascensore, fino "
            "allo spazio aperto davanti a casa.",
        ],
        "regole": [("tav2", [0, 1, 3])],
        "scena": "tavolo",
    },
    {
        "id": "cap3", "titolo": "La campanella strana", "stagione": "novembre",
        "icona": ("pop-sirena.png", "Icona: sirena di allarme"),
        "testo": [
            "A scuola, un giorno, suonò una campanella diversa: lunga, che non finiva mai. "
            "Era la prova di evacuazione.",
            "Flavio, che quel mese era chiudi-fila, controllò che nessuno restasse "
            "indietro. Flavia lasciò lo zaino sotto il banco: lo zaino resta, tu vai.",
            "Camminarono senza correre e senza parlare, per sentire la maestra.",
            "Al punto di raccolta, nel cortile, la maestra chiamò i nomi uno per uno. "
            "«Flavia?» «Presente!» «Flavio?» «Presente!»",
            "Nessuno tornò indietro a prendere niente.",
        ],
        "regole": [("tav11", [0, 2, 3, 4])],
        "scena": "scuola",
    },
    {
        "id": "cap4", "titolo": "Il cielo brontola", "stagione": "giugno",
        "icona": ("dis-temporale.png", "Icona: nuvola con fulmine"),
        "testo": [
            "Al campo, il cielo diventò grigio e cominciò a brontolare. Flavio era sotto "
            "un grande albero, solo in mezzo al prato, a ripararsi dalle prime gocce.",
            "«Via da lì!», chiamò il papà.",
            "Con i fulmini, un albero da solo non è un riparo, e nemmeno una tettoia "
            "leggera. Il posto sicuro è dentro: una casa, oppure la macchina con i "
            "finestrini chiusi.",
            "Flavio corse alla macchina, dove Flavia era già seduta, e tirò su il "
            "finestrino.",
            "Fuori il temporale fece tutto il suo spettacolo, e loro lo guardarono da "
            "dentro.",
        ],
        "regole": [("tav4", [0, 1, 2])],
        "scena": "temporale",
    },
    {
        "id": "cap5", "titolo": "Il vento porta via le cose", "stagione": "novembre",
        "icona": ("oca-albero.png", "Icona: albero piegato dal vento"),
        "testo": [
            "Un pomeriggio il vento si alzò fortissimo. Sul balcone un vaso cadde. Un "
            "cartellone volò via dalla strada come un aquilone.",
            "«Andiamo a far volare il nostro!», disse Flavio. «Non oggi», disse la nonna. "
            "«Il pericolo non è il vento: è quello che il vento fa volare.»",
            "Restarono in casa, lontani dalle finestre, con porte e finestre chiuse.",
            "Il giorno dopo, a vento finito, Flavia vide in strada un filo elettrico caduto a terra. Non lo toccò: lo "
            "disse alla nonna, e la nonna chiamò il 112.",
        ],
        "regole": [("tav5", [0, 3, 4])],
        "scena": "vento",
    },
    {
        "id": "cap6", "titolo": "Troppa acqua", "stagione": "dicembre",
        "icona": ("oca-pioggia.png", "Icona: nuvola con pioggia"),
        "testo": [
            "Piovve per due giorni. Il fosso dietro casa diventò un fiume marrone. "
            "L'acqua entrò nel garage e salì sulle scale della cantina.",
            "«Il mio libro è in garage!», disse Flavia. «Si sale, non si scende», disse "
            "il papà. «Il libro lo prendiamo dopo.»",
            "Salirono al piano di sopra con la nonna, senza scendere a prendere niente.",
            "Dalla finestra Flavio vide la strada allagata. Non si attraversa, né a piedi "
            "né in macchina: non si vede quanto è profonda.",
            "Aspettarono in alto, finché l'acqua non se ne andò.",
        ],
        "regole": [("tav3", [0, 1, 2])],
        "scena": "alluvione",
    },
    {
        "id": "cap7", "titolo": "Fumo sulla collina", "stagione": "agosto",
        "icona": ("alf-i-incendio.png", "Icona: fiamme"),
        "testo": [
            "In agosto, dalla collina dietro il paese, salì una colonna di fumo. Un "
            "incendio nel bosco.",
            "Il papà chiamò subito il 112.",
            "«Da che parte va il fumo?», chiese Flavia. «Verso il lago. Noi andiamo "
            "dall'altra parte», disse Flavio, che il nonno gliel'aveva insegnato.",
            "Nel bosco non ci si avvicina e non si prova a spegnere: si va via, dalla parte "
            "opposta al fumo, senza fermarsi nelle strade dove passa.",
            "Arrivati a casa chiusero porte, finestre e persiane, e aspettarono i vigili "
            "del fuoco.",
        ],
        "regole": [("tav6", [0, 1, 2])],
        "scena": "incendio",
    },
    {
        "id": "cap8", "titolo": "Fumo in cucina", "stagione": "gennaio",
        "icona": ("pop-strisciare.png", "Icona: bambino che avanza carponi"),
        "testo": [
            "Una domenica una padella dimenticata riempì il corridoio di fumo grigio. Il "
            "papà spense il fornello, ma il fumo era tanto e stava in alto, vicino al "
            "soffitto.",
            "«Giù, a carponi!»",
            "Flavia e Flavio si misero a quattro zampe: in basso l'aria si respira. "
            "Flavio arrivò per primo alla porta di casa e toccò la maniglia: era fredda, "
            "si poteva aprire.",
            "Uscirono per le scale, senza ascensore, fino in strada. Da fuori il papà "
            "chiamò il 112.",
            "Una volta fuori non si rientra: si aspetta che qualcuno dica che si può.",
        ],
        "regole": [("tav7", [0, 2, 4])],
        "scena": "fumo",
    },
    {
        "id": "cap9", "titolo": "La buca nel prato", "stagione": "aprile",
        "icona": ("alf-a-allerta.png", "Icona: triangolo di pericolo"),
        "testo": [
            "Una passeggiata ai Castelli, in primavera. In mezzo al prato c'era una buca "
            "profonda, con le pareti di terra. Flavia si sporse a guardare.",
            "«Ferma», disse Anna, che era con loro. «Ai Castelli Romani, sotto terra, c'è "
            "un gas che ogni tanto esce dal suolo. Non ha odore ed è pesante: si ferma nei "
            "posti bassi e chiusi, e chi entra non se ne accorge.»",
            "Nelle buche, nei pozzi e nelle cantine che non si conoscono non si entra.",
            "«E se qualcuno è dentro e non risponde?», chiese Flavio. «Non si entra a "
            "prenderlo. Si chiama un adulto e il 112, e si aspettano i vigili del fuoco.»",
        ],
        "regole": [("tav10", [0, 1, 2])],
        "scena": "buca",
    },
    {
        "id": "cap10", "titolo": "Via la luce", "stagione": "febbraio",
        "icona": ("oca-torcia.png", "Icona: torcia elettrica"),
        "testo": [
            "Una sera d'inverno la luce se ne andò. Tutto buio.",
            "La nonna prese la torcia dallo zaino rosso — non le candele, che possono dare "
            "fuoco alle cose.",
            "Lasciarono accesa una sola lampada, per accorgersi quando la corrente "
            "tornava. Il frigorifero restò chiuso: il cibo si conserva per ore.",
            "Flavio voleva scendere a vedere se il palazzo era tutto al buio. «Con le "
            "scale», disse Flavia, «non con l'ascensore.»",
            "La luce tornò dopo un'ora, e la lampada si accese da sola.",
        ],
        "regole": [("tav9", [0, 1, 2])],
        "scena": "blackout",
    },
    {
        "id": "cap11", "titolo": "Il giorno più caldo", "stagione": "luglio",
        "icona": ("dis-sole.png", "Icona: sole"),
        "testo": [
            "Il giorno più caldo dell'anno, alle due del pomeriggio, la nonna si sedette "
            "di colpo. Aveva il viso rosso e parlava piano.",
            "Respirarono. Guardarono. Sapevano cosa fare.",
            "Flavia prese il telefono e fece il 112. «Sono Flavia. Sono a Genzano.» Disse "
            "la via, il numero di casa e il nome del negozio all'angolo. «Mia nonna sta "
            "male: è rossa e parla piano. Siamo in tre.»",
            "Rispose a tutte le domande e non chiuse finché non glielo dissero.",
            "Intanto Flavio portò alla nonna un bicchiere d'acqua e tirò giù la "
            "tapparella.",
        ],
        "regole": [("tav13", [0, 2, 3])],
        "scena": "telefono",
    },
    {
        "id": "cap12", "titolo": "Il diploma", "stagione": "settembre, un anno dopo",
        "icona": ("alf-p-protezione-civile.png", "Icona: volontari di protezione civile con il furgone"),
        "testo": [
            "L'ambulanza arrivò poco dopo. La nonna tornò a casa la sera stessa, con "
            "una gran voglia di gelato.",
            "Il giorno dopo Anna venne a trovarli. «Hai detto dove eri, che cosa era "
            "successo, chi stava male, e non hai chiuso», disse a Flavia. «E tu hai "
            "portato l'acqua e fatto ombra», disse a Flavio. «È tutto quello che serve.»",
            "Diede a ciascuno un foglio con il bordo blu: il diploma di piccola protezione "
            "civile.",
            "Li attaccarono sopra i letti, accanto allo zaino rosso.",
            "Prima respiro. Poi guardo. Poi so cosa fare. E in emergenza si chiama il 112.",
        ],
        "regole": [("tav13", [4]), ("tav1", [0])],
        "scena": "diploma",
    },
]
