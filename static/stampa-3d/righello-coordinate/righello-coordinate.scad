// Righello per le coordinate con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Strumenti con il nominativo per i volontari della Protezione Civile di Genzano di Roma:
// righello per leggere le coordinate sulle carte, segnalibro con l'alfabeto fonetico, porta tesserino,
// avvolgicavo per l'auricolare della radio, etichetta per il casco e fischietto di emergenza.
// Si cambiano solo i parametri qui sotto. Tutti si stampano senza supporti, nella posizione del file.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
tipo = "righello"; // [righello, segnalibro, tesserino, avvolgicavo, casco, fischietto]
// tutto = pezzo unico; base e testo = pezzi separati
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
// altezza delle scritte e delle tacche sopra la base (mm)
rilievo = 1.0;
// larghezza della cornice (mm), dove c'è
cornice = 1.2;

$fn = 48;

// Misure per tipo: [lunghezza, altezza, raggio angoli, spessore base, carattere riga1, y riga1,
//                   carattere righe piccole, y riga2, y riga3, x del centro del nominativo]
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, dettagli da 0,6 mm in su,
// rilievi alti e larghi almeno 0,5 mm.
MISURE = [
    ["righello",    [120, 70, 3.0, 2.5, 7.0, 12.0, 4.0,  3.5, -2.0, 6]],
    ["segnalibro",  [64, 150, 4.0, 1.6, 6.5, 58.0, 4.0, 49.0, 0, 5.65]],
    ["tesserino",   [94.2, 80, 4.0, 1.6, 6.5, -35.0, 4.0, -42.6, -48.0, 5.65]],
    ["avvolgicavo", [80, 32, 4.0, 3.0, 6.5, 6.5, 4.0, -1.8, -7.3, 5.65]],
    ["casco",       [80, 24, 4.0, 1.2, 8.0, 4.0, 4.0, -6.5, 0, 6.75]],
    ["fischietto",  [16, 56, 1.5, 0, 6.0, 0, 4.0, 0, 0, 0]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];
SMUSSO = tipo == "casco" ? 0.4 : 0.6;
CON_CORNICE = tipo == "segnalibro" || tipo == "avvolgicavo";

/* ---------- Forme in pianta ---------- */

// Avvolgicavo: due incavi alle estremità dove si avvolge il cavo, due fessure che lo trattengono
INCAVO = [18, 14]; FESSURA_CAVO = 2.2;
// Segnalibro: foro in alto per un nastro
FORO_NASTRO = 4;

module forma() {
    if (tipo == "righello") {
        // angoli in alto vivi: sono i punti da mettere sul punto da leggere
        translate([-L / 2, 0]) square([L, H / 2]);
        offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
    } else offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
}

module fori() {
    if (tipo == "avvolgicavo") {
        for (s = [-1, 1]) translate([s * L / 2, 0]) offset(r = 2) square(INCAVO - [4, 4], center = true);
        // fessure nelle linguette, una per parte, per bloccare le due estremità del cavo
        translate([L / 2 - 2.5, 11.5]) square([5.01, FESSURA_CAVO], center = true);
        translate([-L / 2 + 2.5, -11.5]) square([5.01, FESSURA_CAVO], center = true);
    }
    if (tipo == "segnalibro") translate([0, H / 2 - 7]) circle(d = FORO_NASTRO);
}

module sagoma(inset = 0) {
    difference() {
        offset(delta = -inset) forma();
        offset(delta = inset) fori();
    }
}

// Piastra con bordi smussati (gradini da 0,2 mm, uno strato di stampa ciascuno). Il righello non ha
// lo smusso in alto: il bordo da leggere deve arrivare fino allo spigolo.
module corpo() {
    sopra = tipo == "righello" ? 0 : SMUSSO;
    for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) sagoma(0.4 - i * 0.2);
    translate([0, 0, 0.4]) linear_extrude(B - 0.4 - sopra + 0.01) sagoma();
    n = round(sopra / 0.2);
    if (n > 0)
        for (i = [0:n - 1]) translate([0, 0, B - sopra + i * 0.2])
            linear_extrude(0.21 - (i == n - 1 ? 0.01 : 0)) sagoma(0.2 * (i + 1));
}

/* ---------- Scritte ---------- */

// Tricolore: tre fasce separate da solchi di 0,8 mm, alto quanto le lettere grandi (proporzioni 2:3)
SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}

// Nominativo con la bandiera a sinistra, centrato in x: la bandiera ha un posto fisso, pensato per «ALFA 100»
module nominativo2d(size, xb) {
    if (bandiera) translate([xb, 0]) bandiera2d(size);
    translate([TX, 0]) text(riga1, size = size, font = font, halign = "center", valign = "center");
}

module riga(t, x, y, s = S2, f = font2, h = "center") {
    translate([x, y]) text(t, size = s, font = f, halign = h, valign = "center");
}

/* ---------- Righello per le coordinate ---------- */

// Due «angoli di lettura» (romer) negli angoli in alto e una scala lineare in basso.
// 1:25.000 → 100 m = 4 mm; 1:50.000 → 100 m = 2 mm; 1:10.000 → 100 m = 10 mm.
TACCA = 0.8;
module tacche_angolo(x0, verso, passo) {   // verso = +1 (angolo sinistro) o -1 (angolo destro)
    for (k = [0:10]) {
        lunga = k % 5 == 0 ? 6 : 3.5;
        // tacche sul bordo alto, dall'angolo verso il centro
        translate([x0 + verso * k * passo - TACCA / 2, H / 2 - lunga]) square([TACCA, lunga + 0.01]);
        // tacche sul bordo laterale, dall'angolo verso il basso
        translate([verso > 0 ? x0 - 0.01 : x0 - lunga, H / 2 - k * passo - TACCA / 2]) square([lunga + 0.01, TACCA]);
    }
    // sulla scala 1:50.000 le tacche sono fitte: si scrive solo il chilometro
    if (passo > 2) riga("500 m", x0 + verso * 5 * passo, H / 2 - 9);
    riga("1 km", x0 + verso * 10 * passo, H / 2 - 9);
}
module righello2d() {
    intersection() {
        union() {
            // in alto a destra la scala 1:25.000, la più usata, che si legge con il righello dritto;
            // in alto a sinistra la 1:50.000, che si legge girando il righello di un quarto di giro
            tacche_angolo(L / 2, -1, 4);
            tacche_angolo(-L / 2, 1, 2);
            for (k = [0:20]) {     // scala 1:10.000 lungo il bordo basso, una tacca ogni 50 m (5 mm)
                lunga = k % 10 == 0 ? 6 : k % 2 == 0 ? 4.5 : 3;
                translate([-50 + 5 * k - TACCA / 2, -H / 2 - 0.01]) square([TACCA, lunga + 0.01]);
            }
        }
        forma();
    }
    for (k = [0:4]) riga(str(k * 200), -50 + 20 * k, -H / 2 + 9);
    riga("1 km", 50, -H / 2 + 9);
    riga("SCALA 1:50.000", -34, H / 2 - 15.5);
    riga("SCALA 1:25.000", 34, H / 2 - 15.5);
    riga("SCALA 1:10.000", 0, -H / 2 + 15.5);
    translate([0, Y1]) nominativo2d(S1, -27.2);
    riga(riga2, 0, Y2);
    riga(riga3, 0, Y3);
}

/* ---------- Segnalibro con l'alfabeto fonetico ---------- */

// Alfabeto ortografico internazionale per le radiocomunicazioni (ICAO/ITU, «alfabeto NATO»),
// con le grafie ufficiali Alfa e Juliett.
ALFABETO = ["Alfa", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India",
            "Juliett", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", "Romeo",
            "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"];
module segnalibro2d() {
    translate([0, Y1]) nominativo2d(S1, -25.3);
    riga("ALFABETO FONETICO", 0, Y2);
    for (i = [0:25]) {
        col = floor(i / 13); r = i % 13;
        x = col == 0 ? -29 : -0.5;
        y = 41 - r * 8;
        riga(chr(65 + i), x, y, S2, font, "left");
        riga(ALFABETO[i], x + 6.9, y, S2, font2, "left");
    }
    riga(riga2, 0, -H / 2 + 11.5);
    riga(riga3, 0, -H / 2 + 5.8);
}

/* ---------- Avvolgicavo ---------- */
module avvolgicavo2d() {
    translate([0, Y1]) nominativo2d(S1, -25.3);
    riga(riga2, 0, Y2);
    riga(riga3, 0, Y3);
}

/* ---------- Etichetta per il casco ---------- */
module casco2d() {
    translate([0, Y1]) nominativo2d(S1, -30.95);
    riga(str(riga2, " ", riga3 == "GENZANO DI ROMA" ? "GENZANO" : riga3), 0, Y2);
}

module rilievo2d() {
    if (tipo == "righello") righello2d();
    if (tipo == "segnalibro") segnalibro2d();
    if (tipo == "avvolgicavo") avvolgicavo2d();
    if (tipo == "casco") casco2d();
    if (CON_CORNICE && cornice > 0) difference() { sagoma(SMUSSO); sagoma(SMUSSO + cornice); }
}

module piastra(parte) {
    if (parte == "tutto" || parte == "base") corpo();
    if (parte == "tutto" || parte == "testo") translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) rilievo2d();
}

/* ---------- Porta tesserino ---------- */

// Tasca per una tessera formato carta di credito (ISO/IEC 7810 ID-1: 85,6 × 54 mm, spessa 0,76 mm),
// aperta in alto: la tessera scivola sopra la linguetta e si infila sotto i bordi. I bordi hanno il
// lato di sotto inclinato di 46 gradi, così si stampano senza supporti. In basso una fascia con il
// nominativo, in alto una linguetta con l'asola per la clip da badge.
CARTA = [87.2, 55.4]; CANALE = 1.4; FONDO = 1.6; LABBRO = 2.0;
TS_ALTO = FONDO + CANALE + LABBRO * tan(46) + 1.0;      // spessore della cornice: 6,1 mm
TASCA_Y1 = 27; TASCA_Y0 = TASCA_Y1 - CARTA[1];
TS_GIU = TASCA_Y0 - 3.5 - 20;                           // bordo basso della fascia con il nominativo
LINGUETTA = [40, 13]; ASOLA_BADGE = [15, 4];

module ts_contorno() {      // cornice e fascia, senza la linguetta
    translate([0, (TASCA_Y1 + TS_GIU) / 2])
        offset(r = R) square([L - 2 * R, TASCA_Y1 - TS_GIU - 2 * R], center = true);
}
module ts_linguetta() {
    difference() {
        hull() {
            translate([-LINGUETTA[0] / 2, TASCA_Y1 - 5]) square([LINGUETTA[0], 1]);
            for (s = [-1, 1]) translate([s * (LINGUETTA[0] / 2 - 5), TASCA_Y1 + LINGUETTA[1] - 5]) circle(r = 5);
        }
        translate([0, TASCA_Y1 + 7]) offset(r = 2) square(ASOLA_BADGE - [4, 4], center = true);
    }
}
module ts_tasca(dentro = 0) {   // ingombro della tessera, aperto in alto; dentro = quanto coprono i bordi
    translate([-CARTA[0] / 2 + dentro, TASCA_Y0 + dentro]) square([CARTA[0] - 2 * dentro, CARTA[1] + 40]);
}
module tesserino(parte) {
    if (parte == "tutto" || parte == "base") {
        // fondo: tutta la pianta più la linguetta, con i due gradini in basso
        for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21)
            offset(delta = -(0.4 - i * 0.2)) union() { ts_contorno(); ts_linguetta(); }
        translate([0, 0, 0.4]) linear_extrude(FONDO - 0.4 + 0.01) union() { ts_contorno(); ts_linguetta(); }
        // cornice con il canale per la tessera e i bordi inclinati
        difference() {
            translate([0, 0, FONDO]) linear_extrude(TS_ALTO - FONDO)
                difference() { ts_contorno(); ts_tasca(LABBRO); }
            translate([0, 0, FONDO - 0.01]) linear_extrude(CANALE + 0.01) ts_tasca();
            hull() {
                translate([0, 0, FONDO + CANALE - 0.01]) linear_extrude(0.01) ts_tasca();
                translate([0, 0, FONDO + CANALE + LABBRO * tan(46)]) linear_extrude(0.01) ts_tasca(LABBRO);
            }
        }
    }
    if (parte == "tutto" || parte == "testo")
        translate([0, 0, TS_ALTO - 0.01]) linear_extrude(rilievo + 0.01) {
            translate([0, Y1]) nominativo2d(S1, -25.3);
            riga(riga2, 0, Y2);
            riga(riga3, 0, Y3);
        }
}

/* ---------- Fischietto ---------- */

// Fischietto senza pallina, come la testa di un flauto dolce: si soffia nella fessura in basso, il getto
// d'aria passa davanti alla finestra e si rompe sullo spigolo (labbro); la canna chiusa sopra risuona.
// Si stampa in piedi, con la bocca sul piano: la canna finisce con un tetto a punta (più di 45 gradi),
// la finestra ha sopra solo lo spigolo, quindi niente supporti. Le misure seguono le proporzioni dei
// fischietti a canna chiusa: fessura 8 × 1,2 mm, finestra alta 3 mm, canna lunga 22 mm.
FW = [-8, 8]; FD = [-6, 6]; FH = H;
FESSURA_ARIA = [8, 1.2]; FESSURA_Y = 3.4;   // fessura dove si soffia: y da 3,4 a 4,6
FINESTRA = [12, 15]; CANNA_TOP = 34; PARETE_Y = 4.0;
module fs_pianta(d) { offset(r = R) offset(delta = -R - d) translate([FW[0], FD[0]]) square([FW[1] - FW[0], FD[1] - FD[0]]); }
module fischietto(parte) {
    if (parte == "tutto" || parte == "base")
        difference() {
            // corpo con gli spigoli verticali arrotondati e il bordo alto smussato
            union() {
                linear_extrude(FH - 0.8) fs_pianta(0);
                hull() { translate([0, 0, FH - 0.81]) linear_extrude(0.01) fs_pianta(0); translate([0, 0, FH - 0.01]) linear_extrude(0.01) fs_pianta(0.6); }
            }
            // fessura per l'aria, aperta sotto
            translate([-FESSURA_ARIA[0] / 2, FESSURA_Y, -0.01]) cube([FESSURA_ARIA[0], FESSURA_ARIA[1], FINESTRA[0] + 0.02]);
            // canna che risuona, con il tetto a punta
            translate([-4.5, -4.4, FINESTRA[0]]) cube([9, PARETE_Y + 4.4, CANNA_TOP - FINESTRA[0]]);
            hull() {
                translate([-4.5, -4.4, CANNA_TOP - 0.01]) cube([9, PARETE_Y + 4.4, 0.01]);
                translate([-0.2, -0.4, CANNA_TOP + 5.6]) cube([0.4, 0.4, 0.01]);
            }
            // finestra davanti
            translate([-FESSURA_ARIA[0] / 2, FESSURA_Y, FINESTRA[0]]) cube([FESSURA_ARIA[0], FD[1] - FESSURA_Y + 0.01, FINESTRA[1] - FINESTRA[0]]);
            // labbro: la parete sopra la finestra si assottiglia verso il basso fino allo spigolo
            translate([-FESSURA_ARIA[0] / 2, 0, 0]) rotate([90, 0, 90]) linear_extrude(FESSURA_ARIA[0])
                polygon([[PARETE_Y, FINESTRA[1] - 0.01], [FD[1] + 0.01, FINESTRA[1] - 0.01], [FD[1] + 0.01, FINESTRA[1] + 3]]);
            // foro per il cordino, a goccia per stamparlo senza supporti
            translate([FW[0] - 0.01, 0, FH - 4.5]) rotate([0, 90, 0]) rotate([0, 0, 0])
                linear_extrude(FW[1] - FW[0] + 0.02) hull() { circle(d = 3.6); translate([-2.55, 0]) square(0.01, center = true); }
        }
    // scritte sul retro (y = -6), che si leggono dal basso verso l'alto
    if (parte == "tutto" || parte == "testo")
        translate([0, FD[0] + 0.01, 0]) rotate([90, 0, 0]) linear_extrude(rilievo + 0.01) {
            if (bandiera) translate([-3, 3]) rotate(90) bandiera2d(S1);
            translate([-3, 13.5]) rotate(90) text(riga1, size = S1, font = font, halign = "left", valign = "center");
            translate([3.5, 5]) rotate(90) text(str(riga2 == "PROTEZIONE CIVILE" ? "PC" : riga2, " ", riga3), size = S2, font = font2, halign = "left", valign = "center");
        }
}

if (tipo == "tesserino") tesserino(parte);
else if (tipo == "fischietto") fischietto(parte);
else piastra(parte);
