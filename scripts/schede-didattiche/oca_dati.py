# -*- coding: utf-8 -*-
"""Dati del Gioco dell'oca della protezione civile.

Il tabellone è una spirale di 56 caselle su griglia 7x8: si parte dall'angolo
in alto a sinistra e si arriva al centro. Le caselle speciali sono quattro:

  imprevisto  → si pesca una carta IMPREVISTO (cose che capitano)
  emergenza   → si pesca una carta EMERGENZA (si risponde per proseguire)
  avanti      → effetto fisso favorevole, scritto sulla casella
  fermo       → effetto fisso sfavorevole, scritto sulla casella

Le carte EMERGENZA portano la domanda davanti e la risposta capovolta in
fondo, come le altre schede del sito: si legge solo dopo aver risposto.

🔴 Le risposte seguono le indicazioni del Dipartimento della Protezione Civile
e le schede di autoprotezione già pubblicate sul sito. Chi aggiunge una carta
verifica lì, non a memoria: una regola di sicurezza sbagliata dentro un gioco
è più difficile da correggere di una scritta su una pagina.
"""

# (numero, tipo, etichetta breve, pittogramma opzionale)
# tipo: "via" normale · "imprevisto" · "emergenza" · "avanti" · "fermo"
CASELLE = [
 (1,  "partenza",  "Partenza",            "alf-p-protezione-civile"),
 (2,  "via",       "",                    None),
 (3,  "avanti",    "Hai lo zaino pronto: avanti di 2", "alf-z-zaino"),
 (4,  "via",       "",                    None),
 (5,  "imprevisto","Imprevisto",          None),
 (6,  "via",       "",                    None),
 (7,  "emergenza", "Emergenza",           None),
 (8,  "via",       "",                    None),
 (9,  "avanti",    "Sai il 112 a memoria: avanti di 3", "alf-n-telefono"),
 (10, "via",       "",                    None),
 (11, "imprevisto","Imprevisto",          None),
 (12, "via",       "",                    None),
 (13, "fermo",     "Ti fermi a legare la scarpa: stai fermo un giro", None),
 (14, "via",       "",                    None),
 (15, "emergenza", "Emergenza",           None),
 (16, "via",       "",                    None),
 (17, "avanti",    "Conosci l'uscita: avanti di 2", "alf-u-uscita"),
 (18, "via",       "",                    None),
 (19, "imprevisto","Imprevisto",          None),
 (20, "via",       "",                    None),
 (21, "via",       "",                    None),
 (22, "emergenza", "Emergenza",           None),
 (23, "via",       "",                    None),
 (24, "fermo",     "Ti fermi a guardare una vetrina: indietro di 3", None),
 (25, "via",       "",                    None),
 (26, "avanti",    "Hai fatto la prova di evacuazione: avanti di 3", "dis-scuola"),
 (27, "via",       "",                    None),
 (28, "imprevisto","Imprevisto",          None),
 (29, "via",       "",                    None),
 (30, "emergenza", "Emergenza",           None),
 (31, "via",       "",                    None),
 (32, "via",       "",                    None),
 (33, "avanti",    "Aiuti un compagno: avanti di 2", "dis-adulto-bambino"),
 (34, "via",       "",                    None),
 (35, "imprevisto","Imprevisto",          None),
 (36, "via",       "",                    None),
 (37, "fermo",     "Ti sei messo a correre: stai fermo un giro", None),
 (38, "via",       "",                    None),
 (39, "emergenza", "Emergenza",           None),
 (40, "via",       "",                    None),
 (41, "avanti",    "In fila con calma: avanti di 2", "alf-o-ordine"),
 (42, "via",       "",                    None),
 (43, "imprevisto","Imprevisto",          None),
 (44, "via",       "",                    None),
 (45, "emergenza", "Emergenza",           None),
 (46, "via",       "",                    None),
 (47, "avanti",    "Il piano di famiglia è appeso in cucina: avanti di 3", "dis-famiglia"),
 (48, "via",       "",                    None),
 (49, "imprevisto","Imprevisto",          None),
 (50, "via",       "",                    None),
 (51, "emergenza", "Emergenza",           None),
 (52, "via",       "",                    None),
 (53, "fermo",     "Ti sei distratto: indietro di 2", None),
 (54, "via",       "",                    None),
 (55, "via",       "",                    None),
 (56, "arrivo",    "Arrivo",              "alf-l-luogo-sicuro"),
]

IMPREVISTI = [
 ("Manca la luce in tutta la via.", "Accendi la torcia, non le candele. Stai fermo un giro."),
 ("Piove forte e la strada si allaga.", "Aspetti al piano di sopra: stai fermo un giro."),
 ("Il cane di casa si è spaventato.", "Lo cerchi e lo tieni vicino: indietro di 2."),
 ("Hai lasciato lo zaino in camera.", "La prossima volta lo prepari la sera prima: indietro di 3."),
 ("Un albero caduto blocca la strada.", "Fai il giro dall'altra parte: indietro di 2."),
 ("La radio dà una notizia utile.", "Ora sai dove andare: avanti di 3."),
 ("Hai imparato a memoria il numero della mamma o del papà.", "Avanti di 2."),
 ("Trovi per terra una bottiglia sconosciuta.", "Non la tocchi, ti allontani e lo dici a un adulto: avanti di 2."),
 ("Hai messo l'acqua nello zaino.", "Avanti di 2."),
 ("Ti sei ricordato dov'è il punto di raccolta.", "Avanti di 3."),
 ("Vuoi filmare quello che succede.", "Metti via il telefono e ascolti l'adulto: stai fermo un giro."),
 ("Aiuti un vicino anziano a scendere le scale.", "Avanti di 3."),
]

# domanda, risposta (capovolta sulla carta), fonte interna da cui viene la risposta
EMERGENZE = [
 ("La terra trema mentre sei in classe. Che cosa fai?",
  "Ti ripari sotto il banco, ti proteggi la testa con le braccia e aspetti che la scossa finisca. Poi esci in fila con l'insegnante.",
  "/rischi-prevenzione/rischio-sismico/"),
 ("Senti odore di gas in cucina. Che cosa fai?",
  "Non accendi e non spegni niente, nemmeno la luce. Chiami subito un adulto, che apre le finestre e chiude il gas. Poi si esce.",
  "/formazione/schede-stampabili/odore-gas-infanzia/"),
 ("Suona l'allarme della scuola. Che cosa fai?",
  "Lasci tutto dov'è, ti metti in fila senza spingere e segui l'insegnante fino al punto di raccolta. Non torni indietro per nessun motivo.",
  "/formazione/schede-stampabili/labirinto-evacuazione-primaria/"),
 ("Vedi del fumo uscire da una porta chiusa. Che cosa fai?",
  "Non apri quella porta. Ti allontani, avvisi subito un adulto e uscite insieme dalla via più lontana dal fumo.",
  "/kit-organizzazioni/condominio/"),
 ("Arriva un temporale forte mentre sei al parco. Che cosa fai?",
  "Vai al coperto in un edificio con un adulto. Non stai sotto gli alberi e lontano da pali e tettoie.",
  "/rischi-prevenzione/temporali-intensi/"),
 ("Ti accorgi di esserti perso in un posto affollato. Che cosa fai?",
  "Ti fermi dove sei e non corri via. Cerchi un adulto con la divisa e gli dici il tuo nome e cognome. Resti lì e aspetti: non vai via con nessun altro.",
  "/formazione/schede-stampabili/se-mi-perdo-infanzia/"),
 ("Un compagno si fa male e non riesce ad alzarsi. Che cosa fai?",
  "Non lo sposti, a meno che non sia in pericolo immediato, per esempio il fuoco o il traffico. Chiami subito un adulto e resti lì con lui finché non arriva.",
  "/formazione/primo-soccorso/emorragie-ustioni-traumi/"),
 ("Devi chiamare il 112. Che cosa dici?",
  "Dici dove ti trovi, che cosa è successo e se ci sono feriti o persone in pericolo. Poi rispondi con calma: non chiudi la chiamata finché non te lo dice chi risponde.",
  "/numeri-utili/"),
 ("L'acqua sta salendo nella strada davanti a casa tua. Che cosa fai?",
  "Sali al piano di sopra con un adulto. Non scendi in cantina e non entri in garage.",
  "/rischi-prevenzione/rischio-idrogeologico/"),
 ("Trovi una siringa o un oggetto sconosciuto per terra. Che cosa fai?",
  "Non lo tocchi e non lo sposti. Ti allontani e lo dici subito a un adulto.",
  "/formazione/schede-stampabili/oggetti-prima-di-raccogliere-primaria/"),
 ("Fa molto caldo e ti gira la testa. Che cosa fai?",
  "Ti metti all'ombra o al fresco, bevi acqua e lo dici a un adulto: se non ti passa, l'adulto chiama il 112.",
  "/rischi-prevenzione/ondate-di-calore/"),
 ("Squilla il telefono di casa e non c'è nessun adulto. Che cosa fai?",
  "Non rispondi se non sai chi chiama. Chiami un familiare al numero che sai a memoria, quello scritto nel piano della tua famiglia.",
  "/piano-familiare/"),
]
