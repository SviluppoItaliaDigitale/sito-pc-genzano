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
// Come lavora, come gli apribottiglie comuni: la punta dell'attrezzo appoggia sopra il tappo, la moneta, che sta
// fra l'appoggio e il manico a 22 mm dall'appoggio, entra sotto il bordo del tappo, e alzando il manico il tappo si
// piega e salta. (Nel primo disegno, del 25/11/2026, l'appoggio stava fra il dente e il manico: alzando il manico
// il dente sarebbe sceso. L'ha trovato la revisione prima della pubblicazione.)
// tre_in_uno: lo stesso attrezzo con, in fondo al manico, una linguetta a forma di moneta da 1 euro (23,25 mm di
// diametro, spessa 2,33 mm: stessa fonte) per sbloccare il carrello della spesa.
// Si stampa di taglio, in piedi su un lato lungo: così la tasca della moneta è una fessura verticale e
// l'apertura finisce in alto con un tetto a 45 gradi, e non servono supporti. Gli strati corrono per tutta la
// lunghezza del manico, che è il verso in cui lavora quando si fa leva.

/* [Pezzi] */
tipo = "apribottiglie"; // [apribottiglie, tre_in_uno]
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

LUNGO = 140; LARGO = 53; SPESSO = 10; SMUSSO = 6;   // spesso 10 mm: ai lati della tasca restano due pareti da 4 mm
MONETA_D = 21.25; MONETA_S = 1.67;
GIOCO_D = 0.4; GIOCO_S = 0.3;          // la tasca è 0,4 mm più larga e 0,3 mm più spessa della moneta
SPORGE = 4;                            // quanto la moneta esce dalla parete, dentro l'apertura (4 mm: la parete resta lontana dal collo)
APERTURA_R = 18; CZ = 25;              // apertura tonda: il tappo da 32,1 mm ci passa di sbieco
APPOGGIO_X = 20;                       // lato dell'apertura verso la punta: appoggia sopra il tappo
DENTE_X = APPOGGIO_X + 22;             // punta della moneta
PARETE_X = DENTE_X + SPORGE;           // dove finisce l'apertura e comincia la parete del manico
CX = PARETE_X - APERTURA_R;            // centro dell'apertura
MX = DENTE_X + MONETA_D / 2;           // centro della moneta
// occhiello per un cordino: in basso nell'apribottiglie; nel tre in uno in alto, perché in basso lo chiuderebbe la linguetta
CORDINO = tipo == "tre_in_uno" ? [132, 45] : [132, 8]; CORDINO_D = 5;
EURO_D = 23.25; LINGUA_S = 2.2; LINGUA_L = 28;   // linguetta per il carrello: un decimo più sottile della moneta
// Misure: [lunghezza, larghezza, smusso, spessore, carattere riga1, y riga1, carattere righe piccole, y riga2, y riga3,
//          x del centro del nominativo]. Con Liberation Sans Narrow Bold a 4,5 mm il tratto più sottile è di 0,70 mm.
MISURE = [
    ["apribottiglie", [140, 53, 6, 10, 8.0, 33, 4.5, 21, 14.5, 106]],
    ["tre_in_uno",    [168, 53, 6, 10, 8.0, 33, 4.5, 21, 14.5, 106]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9]; BAND = [69, 29]; XR = 100;   // XR = centro delle righe piccole

// profilo visto di fronte (x = lunghezza, y = larghezza): quattro angoli smussati a 45 gradi
module profilo() {
    polygon([[SMUSSO, 0], [LUNGO - SMUSSO, 0], [LUNGO, SMUSSO], [LUNGO, LARGO - SMUSSO],
             [LUNGO - SMUSSO, LARGO], [SMUSSO, LARGO], [0, LARGO - SMUSSO], [0, SMUSSO]]);
}

// apertura: un cerchio tagliato dal lato di appoggio, con un tetto a 45 gradi che finisce in un tratto piano
// di 4 mm (un ponte che si stampa senza supporti)
module apertura() {
    q = APERTURA_R / sqrt(2);
    // i due spigoli dove il lato di appoggio taglia il cerchio sono raccordati (3 mm): lì passano gli sforzi
    offset(r = 3) offset(delta = -3) intersection() {
        translate([CX, CZ]) circle(r = APERTURA_R);
        translate([APPOGGIO_X, -1]) square([LUNGO, LARGO + 2]);
    }
    intersection() {
        polygon([[CX - q, CZ + q], [CX + q, CZ + q], [CX + 2, CZ + 2 * q - 2], [CX - 2, CZ + 2 * q - 2]]);
        translate([APPOGGIO_X, -1]) square([LUNGO, LARGO + 2]);
    }
}

// goccia: un foro tondo con la punta in alto, che si stampa senza supporti
module goccia(d) { circle(d = d); polygon([[-d / 2 / sqrt(2), d / 2 / sqrt(2)], [d / 2 / sqrt(2), d / 2 / sqrt(2)], [0, d / sqrt(2)]]); }

// tasca della moneta: una fessura a metà spessore, aperta solo verso l'apertura; la moneta ci entra di lì
module tasca() {
    d = MONETA_D + GIOCO_D;
    translate([0, 0, -(MONETA_S + GIOCO_S) / 2]) linear_extrude(MONETA_S + GIOCO_S) {
        translate([MX, CZ]) goccia(d);      // a goccia: in stampa il lato alto della tasca è un tetto, non un arco
        translate([PARETE_X - 0.5, CZ - d / 2]) square([MX - PARETE_X + 0.5, d]);
    }
}

// smusso di 2 mm a 45 gradi sul bordo dell'apertura dal lato del dente, solo sulla faccia senza scritte, quella che
// guarda la bottiglia: quando l'attrezzo è inclinato di 30 gradi per infilare la moneta sotto il tappo, quello spigolo
// è l'unico punto che può toccare il collo
module smusso_dente() {
    intersection() {
        translate([0, 0, -SPESSO / 2 - 0.01]) hull() {
            linear_extrude(0.01) offset(delta = 2) apertura();
            translate([0, 0, 2]) linear_extrude(0.01) apertura();
        }
        translate([CX + 8, CZ - 13, -SPESSO]) cube([30, 26, SPESSO]);
    }
}

module tricolore() {
    for (i = [0:2]) translate([BAND[0] + i * 4 + (i > 0 ? 0.4 : 0), BAND[1]]) square([4 - (i == 1 ? 0.8 : 0.4), S1]);
}

module scritte2d() {
    if (bandiera) tricolore();
    translate([TX, Y1]) text(riga1, size = S1, font = font, halign = "center", valign = "center");
    translate([XR, Y2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    translate([XR, Y3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
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
        // il bordo che appoggia sul tappo è smussato di 1 mm sulle due facce: non ammacca il tappo e non si scheggia
        for (v = [-1, 1]) translate([APPOGGIO_X, CZ, v * SPESSO / 2]) rotate([0, 45, 0]) cube([1.42, 36, 1.42], center = true);
        smusso_dente();
    }
    // linguetta per il carrello, a metà spessore, con il lato basso sul piano di stampa
    if (tipo == "tre_in_uno") in_piedi() linear_extrude(LINGUA_S, center = true) hull() {
        translate([LUNGO - 8, 0]) square([8, EURO_D]);
        translate([LUNGO + LINGUA_L - EURO_D / 2, EURO_D / 2]) circle(d = EURO_D, $fn = 120);
    }
}

module testo() {
    in_piedi() translate([0, 0, SPESSO / 2 - 0.01]) linear_extrude(rilievo + 0.01) scritte2d();
}

if (parte == "tutto" || parte == "base") base();
if (parte == "tutto" || parte == "testo") testo();
