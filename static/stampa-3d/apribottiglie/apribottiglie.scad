// Apribottiglie per tappi a corona con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Apribottiglie per tappi a corona con il nominativo dei volontari della Protezione Civile di Genzano di Roma.
// Il dente che solleva il tappo è il bordo di una moneta da 5 centesimi infilata in una tasca: la plastica
// stampata da sola si consumerebbe dopo pochi tappi. Si cambiano solo i parametri qui sotto.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
//
// Misure di partenza, con fonte e data:
// - moneta da 5 centesimi di euro: diametro 21,25 mm, spessore 1,67 mm (Banca centrale europea, «Facce comuni»,
//   ecb.europa.eu, letta il 25/11/2026);
// - tappo a corona da 26 mm: diametro esterno 32,1 mm (± 0,2), altezza 6,0 mm (± 0,15), norma DIN EN 17177 come
//   riportata dalla voce «Kronkorken» di de.wikipedia.org, letta il 25/11/2026 (la norma è a pagamento).
// Come lavora: la moneta entra sotto il bordo del tappo, il lato opposto dell'apertura appoggia sopra il tappo,
// a 22 mm dal dente, e alzando il manico il tappo si piega e salta.
// Si stampa di taglio, in piedi su un lato lungo: così la tasca della moneta è una fessura verticale e
// l'apertura finisce in alto con un tetto a 45 gradi, e non servono supporti. Gli strati corrono per tutta la
// lunghezza del manico, che è il verso in cui lavora quando si fa leva.

/* [Pezzi] */
tipo = "apribottiglie"; // [apribottiglie]
// tutto = pezzo unico; base e testo = pezzi separati
parte = "tutto"; // [tutto, base, testo]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
riga3 = "GENZANO DI ROMA";
font = "Liberation Sans:style=Bold";
font2 = "Liberation Sans Narrow:style=Bold";
bandiera = true;
// altezza delle scritte sopra la faccia (mm)
rilievo = 1.0;

$fn = 96;

LUNGO = 132; LARGO = 53; SPESSO = 8; SMUSSO = 6;
MONETA_D = 21.25; MONETA_S = 1.67;
GIOCO_D = 0.4; GIOCO_S = 0.3;          // la tasca è 0,4 mm più larga e 0,3 mm più spessa della moneta
SPORGE = 3;                            // quanto la moneta esce dalla parete, dentro l'apertura
APERTURA_R = 18; CZ = 25;              // apertura tonda: il tappo da 32,1 mm ci passa di sbieco
PARETE_X = 24;                         // dove finisce la parete della punta e comincia l'apertura
DENTE_X = PARETE_X + SPORGE;           // punta della moneta
APPOGGIO_X = DENTE_X + 22;             // lato dell'apertura che appoggia sopra il tappo
CX = PARETE_X + APERTURA_R;            // centro dell'apertura
MX = DENTE_X - MONETA_D / 2;           // centro della moneta
CORDINO = [124, 8]; CORDINO_D = 5;     // occhiello per un cordino
// Misure: [lunghezza, larghezza, smusso, spessore, carattere riga1, y riga1, carattere righe piccole, y riga2, y riga3,
//          x del centro del nominativo]. Con Liberation Sans Narrow Bold a 4,5 mm il tratto più sottile è di 0,70 mm.
MISURE = [
    ["apribottiglie", [132, 53, 6, 8, 8.0, 33, 4.5, 21, 14.5, 99]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9]; BAND = [60, 29];

// profilo visto di fronte (x = lunghezza, y = larghezza): quattro angoli smussati a 45 gradi
module profilo() {
    polygon([[SMUSSO, 0], [LUNGO - SMUSSO, 0], [LUNGO, SMUSSO], [LUNGO, LARGO - SMUSSO],
             [LUNGO - SMUSSO, LARGO], [SMUSSO, LARGO], [0, LARGO - SMUSSO], [0, SMUSSO]]);
}

// apertura: un cerchio tagliato dal lato di appoggio, con un tetto a 45 gradi che finisce in un tratto piano
// di 6 mm (un ponte che si stampa senza supporti)
module apertura() {
    q = APERTURA_R / sqrt(2);
    intersection() {
        union() {
            translate([CX, CZ]) circle(r = APERTURA_R);
            polygon([[CX - q, CZ + q], [CX + q, CZ + q], [CX + 3, CZ + 2 * q - 3], [CX - 3, CZ + 2 * q - 3]]);
        }
        translate([0, -1]) square([APPOGGIO_X, LARGO + 2]);
    }
}

// goccia: un foro tondo con la punta in alto, che si stampa senza supporti
module goccia(d) { circle(d = d); polygon([[-d / 2 / sqrt(2), d / 2 / sqrt(2)], [d / 2 / sqrt(2), d / 2 / sqrt(2)], [0, d / sqrt(2)]]); }

// tasca della moneta: una fessura a metà spessore, aperta solo verso l'apertura; la moneta ci entra di lì
module tasca() {
    d = MONETA_D + GIOCO_D;
    translate([0, 0, -(MONETA_S + GIOCO_S) / 2]) linear_extrude(MONETA_S + GIOCO_S) {
        translate([MX, CZ]) goccia(d);      // a goccia: in stampa il lato alto della tasca è un tetto, non un arco
        translate([MX, CZ - d / 2]) square([PARETE_X + 0.5 - MX, d]);
    }
}

module tricolore() {
    for (i = [0:2]) translate([BAND[0] + i * 4 + (i > 0 ? 0.4 : 0), BAND[1]]) square([4 - (i == 1 ? 0.8 : 0.4), S1]);
}

module scritte2d() {
    if (bandiera) tricolore();
    translate([TX, Y1]) text(riga1, size = S1, font = font, halign = "center", valign = "center");
    translate([92, Y2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    translate([92, Y3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
}

// Il pezzo esce già in piedi: x = lunghezza, z = larghezza, y = spessore; le scritte sono sulla faccia y = -4.
module in_piedi() { rotate([90, 0, 0]) children(); }

module base() {
    in_piedi() difference() {
        linear_extrude(SPESSO, center = true) difference() {
            profilo();
            apertura();
            translate(CORDINO) goccia(CORDINO_D);
        }
        tasca();
    }
}

module testo() {
    in_piedi() translate([0, 0, SPESSO / 2 - 0.01]) linear_extrude(rilievo + 0.01) scritte2d();
}

if (parte == "tutto" || parte == "base") base();
if (parte == "tutto" || parte == "testo") testo();
