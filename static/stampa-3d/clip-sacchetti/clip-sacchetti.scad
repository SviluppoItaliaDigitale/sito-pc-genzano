// Clip chiudi-sacchetti con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Clip chiudi-sacchetti con il nominativo (volontari della Protezione Civile di Genzano di Roma).
// Due bracci uniti da una cerniera flessibile: si piega il bordo del sacchetto, lo si mette fra i bracci e si
// chiude finché il dente scatta. Il braccio largo porta bandiera, nominativo ed ente. Tocca solo l'esterno del
// sacchetto, non il cibo. Si stampa aperta e in piano, in un pezzo solo, senza supporti.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
tipo = "sacchetti"; // [sacchetti]
// tutto = pezzo unico; base e testo = pezzi separati per stampa a due colori
parte = "tutto"; // [tutto, base, testo]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
riga3 = "GENZANO DI ROMA";
font = "Liberation Sans:style=Bold";
// carattere stretto per le righe piccole: a 4 mm il tratto più sottile resta sopra 0,6 mm
font2 = "Liberation Sans Narrow:style=Bold";

/* [Bandiera italiana] */
bandiera = true;

/* [Spessori] */
// altezza delle scritte sopra la faccia (mm)
rilievo = 1.0;

$fn = 48;

// Misure: [lunghezza utile, larghezza del braccio con le scritte, raggio angoli, spessore (50 strati da 0,2 mm),
//          carattere riga1, y riga1, carattere righe piccole, y riga2, y riga3]
// La clip chiude sacchetti larghi fino a 12 cm. Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in
// su, tratti delle lettere da 0,6 mm in su. Liberation Sans Bold a 6,5 mm e Narrow Bold a 4 mm passano il controllo.
MISURE = [
    ["sacchetti", [125, 13, 1, 10, 6.5, -7.25, 4.0, -4.6, -10.2]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; LB = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8];

LA = 6;            // larghezza del braccio che preme
LUCE = 0.6;        // spazio fra i bracci chiusi, per le due pareti del sacchetto
DENTE = 1.5;       // rilievo lungo il braccio che preme: entra in un incavo dell'altro e fa fare una piega al sacchetto
CERN = 1.2;        // spessore della cerniera flessibile
CERN_O = [0, -1.7]; CERN_R = 5.3;
APERTA = 15;       // gradi di apertura con cui si stampa: chiudendola la cerniera lavora di poco
GAMBO = 1.6; SCATTO = 1.2;   // linguetta di chiusura e dente che aggancia sotto il braccio largo
CENTRO = [-62.5, 6.5];       // il pezzo è spostato così le scritte stanno intorno all'origine

SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}
// Bandiera e nominativo a sinistra, ente su due righe a destra
X_BAND = 8; X_NOM = X_BAND + 1.5 * S1 + 1.5 + 3.03 * S1; X_ENTE = 92;
module testi2d() {
    if (bandiera) translate([X_BAND, Y1]) bandiera2d(S1);
    translate([X_NOM, Y1]) text(riga1, size = S1, font = font, halign = "center", valign = "center");
    if (riga2 != "") translate([X_ENTE, Y2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    if (riga3 != "") translate([X_ENTE, Y3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
}

// Braccio largo, con le scritte: in alto ha l'incavo per il rilievo dell'altro braccio
module largo2d() {
    difference() {
        translate([R, -LB + R]) offset(r = R) square([L - 2 * R, LB - 2 * R]);
        translate([10 - 0.4, -DENTE]) square([105 + 0.8, DENTE + 1]);
        polygon([[L - 1.2, 0.1], [L + 0.1, 0.1], [L + 0.1, -1.2]]);          // invito per la linguetta
        polygon([[-0.1, 0.1], [2.5, 0.1], [-0.1, -2.5]]);                     // spazio per la cerniera
    }
}
// Braccio che preme, disegnato chiuso: rilievo, linguetta di chiusura con il dente e presa per riaprire
module stretto2d() {
    translate([0, LUCE]) square([L + 0.4 + GAMBO, LA]);
    translate([10, LUCE - DENTE]) square([105, DENTE + 0.01]);
    translate([L + 0.4, -LB - 3.2]) square([GAMBO, LB + 3.2 + LUCE + 0.01]);
    polygon([[L + 0.41, -LB - 0.3], [L + 0.4 - SCATTO, -LB - 0.3], [L + 0.4 - SCATTO, -LB - 0.9], [L + 0.41, -LB - 2.4]]);
    translate([L + 0.4, -LB - 4.8]) square([6, 1.6]);
}
function cern(a) = [CERN_O[0] + CERN_R * cos(a), CERN_O[1] + CERN_R * sin(a)];
module cerniera2d() {
    for (a = [90 + APERTA : 15 : 255]) hull() { translate(cern(a)) circle(d = CERN, $fn = 16); translate(cern(a + 15)) circle(d = CERN, $fn = 16); }
}
module clip2d() {
    largo2d();
    cerniera2d();
    translate(CERN_O) rotate(APERTA) translate(-CERN_O) stretto2d();
}

module base() { translate([CENTRO[0], CENTRO[1], 0]) linear_extrude(B) clip2d(); }
module testo() { translate([CENTRO[0], CENTRO[1], B - 0.01]) linear_extrude(rilievo + 0.01) testi2d(); }

if (parte == "tutto" || parte == "base") base();
if (parte == "tutto" || parte == "testo") testo();
