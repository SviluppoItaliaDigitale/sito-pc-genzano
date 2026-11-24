// Cover rinforzata per iPhone 16 con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Cover rinforzata per il telefono con il nominativo inciso sul retro (volontari della Protezione Civile di
// Genzano di Roma). Misure dai disegni dimensionali pubblicati da Apple per chi progetta accessori
// (developer.apple.com, «Accessory Design Guidelines», disegni di settembre 2025 e marzo 2026, consultati il
// 24/11/2026); iPhone è un marchio di Apple Inc. Si stampa in TPU, con il retro sul piano: le scritte sono
// incise e a specchio, così si leggono dal retro. Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di
// Protezione Civile di Genzano di Roma.

/* [Telefono] */
// modello del telefono: la cover entra solo nel suo
tipo = "iphone16"; // [iphone17, iphone17pro, iphone17promax, iphone17e, iphone16]
// tutto = cover con le scritte incise; base = cover senza scritte; testo = solo le scritte (per incidere)
parte = "tutto"; // [tutto, base, testo]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
riga3 = "GENZANO DI ROMA";
font = "Liberation Sans:style=Bold";
// carattere stretto per le righe piccole
font2 = "Liberation Sans Narrow:style=Bold";

/* [Bandiera italiana] */
bandiera = true;

/* [Misure] */
// gioco fra telefono e cover per lato (mm): il TPU si allarga se la stampa viene più stretta
gioco = 0.3;
// spessore delle pareti (mm)
parete = 2.0;
// spessore del retro (mm): Apple chiede al massimo 2,1 mm perché la ricarica senza fili e MagSafe funzionino
fondo = 2.0;
// bordo rialzato sopra lo schermo (mm)
bordo = 1.2;
// profondità delle scritte incise (mm), detta «rilievo» per lo script che fa le anteprime
rilievo = 0.6;

$fn = 24;

// Caratteri delle scritte: [_, _, _, _, nominativo, _, righe piccole, _, _, _] (posizioni lette dallo script
// che controlla il tratto minimo delle lettere, come negli altri modelli)
MISURE = [
    ["iphone17",       [0, 0, 0, 0, 7.0, 0, 4.5, 0, 0, 0]],
    ["iphone17pro",    [0, 0, 0, 0, 7.0, 0, 4.5, 0, 0, 0]],
    ["iphone17promax", [0, 0, 0, 0, 7.0, 0, 4.5, 0, 0, 0]],
    ["iphone17e",      [0, 0, 0, 0, 7.0, 0, 4.5, 0, 0, 0]],
    ["iphone16",       [0, 0, 0, 0, 7.0, 0, 4.5, 0, 0, 0]]
];
S1 = MISURE[search([tipo], MISURE)[0]][1][4];
S2 = MISURE[search([tipo], MISURE)[0]][1][6];

// Misure dei telefoni, in mm, dai disegni di Apple. Distanze lungo il telefono misurate dal bordo in alto.
// [[larghezza, lunghezza, spessore],
//  [profilo degli angoli: distanze dal bordo dei punti della curva, uguali sui due lati],
//  [[centro, mezza lunghezza] dei tasti a sinistra (azione, volume su, volume giù); spessore dei tasti],
//  [[centro, mezza lunghezza] del tasto laterale a destra; spessore], [centro del Controllo fotocamera, 0 se non c'è],
//  [apertura della fotocamera vista dal retro: x0, y0, x1, y1, raggio; con x1 = 0 è tutta la fascia in alto fino a y1],
//  [distanza dal centro dei fori di altoparlanti e microfoni in basso: dal più vicino al più lontano],
//  [larghezza della zona del ricevitore e del microfono frontale in alto]]
TELEFONI = [
    ["iphone17", [[71.45, 149.61, 7.95],
        [0, 0.02, 0.48, 2.26, 5.56, 9.87, 14.53, 19.23],
        [[34.08, 3.45], [48.23, 5.60], [62.43, 5.60], 2.66],
        [[55.32, 8.85], 2.66], [98.20],
        [0.4, 0.5, 34.8, 44.6, 10],
        [11.5, 20.6],
        [14.02]]],
    ["iphone17pro", [[71.85, 150.01, 8.75],
        [0, 0.04, 0.92, 3.80, 8.46, 13.90, 19.43],
        [[34.28, 3.45], [48.43, 5.60], [62.63, 5.60], 2.66],
        [[55.53, 8.85], 2.66], [98.40],
        [0, 0, 0, 46.0, 8],
        [11.5, 20.6],
        [28.85]]],
    ["iphone17promax", [[77.98, 163.43, 8.75],
        [0, 0.04, 0.92, 3.80, 8.46, 13.90, 19.43],
        [[34.28, 3.45], [48.43, 5.60], [62.63, 5.60], 2.66],
        [[55.53, 8.85], 2.66], [111.82],
        [0, 0, 0, 46.0, 8],
        [12.3, 23.6],
        [28.85]]],
    ["iphone17e", [[71.52, 146.71, 7.80],
        [0, 0.06, 0.95, 3.30, 7.10, 11.50, 16.00],
        [[31.28, 3.77], [45.43, 5.92], [59.63, 5.92], 3.31],
        [[52.53, 9.17], 3.31], [0],
        [4.3, 4.3, 33.0, 22.4, 8],
        [10.9, 21.5],
        [11.95]]],
    ["iphone16", [[71.63, 147.64, 7.81],
        [0, 0.04, 0.59, 2.29, 5.24, 9.06, 13.21, 17.40],
        [[34.08, 3.45], [48.23, 5.60], [62.43, 5.60], 2.66],
        [[55.33, 8.85], 2.66], [96.23],
        [0.4, 0.4, 34.2, 44.6, 10],
        [11.5, 20.6],
        [14.02]]]
];
P = TELEFONI[search([tipo], TELEFONI)[0]][1];
W = P[0][0]; L = P[0][1]; T = P[0][2];
CURVA = P[1];
TASTI_SX = [P[2][0], P[2][1], P[2][2]]; SP_SX = P[2][3];
TASTO_DX = P[3][0]; SP_DX = P[3][1];
CC = P[4][0];
CAM = P[5];
FORI = P[6];
RICEVITORE = P[7][0];

ZC = fondo + T / 2;                    // quota del centro dei tasti e dei fori: a metà spessore del telefono
H = fondo + T + bordo;                 // altezza della cover
K = gioco + parete;                    // dal profilo del telefono al fuori della cover
LABBRO = 0.6;                          // il bordo copre 0,6 mm del telaio, mai il vetro (che inizia 1 mm più in dentro)
CORNICE = 0.9;                         // altezza dello scivolo sotto il bordo: 0,9 mm in 1 mm, si stampa senza supporti
PARACOLPI = 1.0;                       // angoli rinforzati: 1 mm più larghi delle pareti

/* ---------- Profilo del telefono ---------- */

// Curva degli angoli: i punti del disegno uniti con una spline di Catmull-Rom, così la curva resta liscia
function cr(p0, p1, p2, p3, t) = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                                       + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t);
N = len(CURVA);
// punti (distanza dal lato, distanza dal bordo in alto), con due punti in più lungo i lati per la tangente
PUNTI = concat([[0, CURVA[N - 1] + 5]], [for (i = [0:N - 1]) [CURVA[i], CURVA[N - 1 - i]]], [[CURVA[N - 1] + 5, 0]]);
ANGOLO = [for (i = [1:N - 1]) for (t = [0:3]) if (!(i == N - 1 && t > 0))
              cr(PUNTI[i - 1], PUNTI[i], PUNTI[i + 1], PUNTI[min(i + 2, N + 1)], t / 4)];
function angolo(sx, sy) = [for (q = (sx * sy > 0 ? ANGOLO : [for (i = [len(ANGOLO) - 1:-1:0]) ANGOLO[i]]))
                              [sx * (W / 2 - q[0]), sy * (L / 2 - q[1])]];
module telefono2d() {
    polygon(concat(angolo(1, 1), angolo(-1, 1), angolo(-1, -1), angolo(1, -1)));
}
module profilo(d) { offset(delta = d) telefono2d(); }

// Fuori della cover: pareti e angoli rinforzati
module esterno2d(d) {
    profilo(d);
    intersection() {
        profilo(d + PARACOLPI);
        difference() {
            square([W + 20, L + 20], center = true);
            square([W - 24, L + 30], center = true);
            square([W + 30, L - 24], center = true);
        }
    }
}

/* ---------- Corpo ---------- */

module strato(z0, z1, d) { translate([0, 0, z0]) linear_extrude(z1 - z0) esterno2d(K + d); }

module guscio() {
    // spigolo in basso smussato a gradini sopra i primi 0,7 mm, che restano dritti (lì ci sono le scritte)
    strato(0, 0.7, -0.9);
    strato(0.7, 1.0, -0.6);
    strato(1.0, 1.3, -0.3);
    strato(1.3, H - 0.6, 0);
    strato(H - 0.6, H - 0.3, -0.3);
    strato(H - 0.3, H, -0.6);
}

module vano() {
    // il telefono con il gioco
    translate([0, 0, fondo]) linear_extrude(T - CORNICE + 0.001) profilo(gioco);
    // scivolo sotto il bordo: da +0,3 a -0,6 mm in 0,9 mm di altezza
    hull() {
        translate([0, 0, fondo + T - CORNICE]) linear_extrude(0.001) profilo(gioco);
        translate([0, 0, fondo + T - 0.001]) linear_extrude(0.001) profilo(-LABBRO);
    }
    // finestra dello schermo
    translate([0, 0, fondo + T - 0.01]) linear_extrude(bordo + 1) profilo(-LABBRO);
    // ricevitore e microfono frontale in alto: lì il bordo non sporge sul telefono
    translate([0, 0, fondo + T - CORNICE]) linear_extrude(bordo + CORNICE + 1)
        intersection() {
            profilo(gioco);
            translate([-(RICEVITORE / 2 + 1.5), L / 2 - 6]) square([RICEVITORE + 3, 10]);
        }
}

// Apertura della fotocamera nel retro. I disegni la danno vista dal retro, con l'origine in alto a sinistra:
// dal davanti quell'angolo è in alto a destra.
module fotocamera2d() {
    if (CAM[2] == 0)
        intersection() {
            profilo(-0.4);
            translate([0, L / 2 - CAM[3] / 2 + 5]) offset(r = CAM[4]) square([W - 0.8 - 2 * CAM[4], CAM[3] + 10 - 2 * CAM[4]], center = true);
        }
    else
        translate([W / 2 - CAM[2], L / 2 - CAM[3]])
            offset(r = CAM[4]) offset(delta = -CAM[4]) square([CAM[2] - CAM[0], CAM[3] - CAM[1]]);
}

// asola lungo x (tasti, fori) e lungo y
module asola(lung, alta) {
    hull() for (s = [-1, 1]) translate([s * (lung - alta) / 2, 0]) circle(d = alta);
}

// Tasti protetti: sul fuori un cuscinetto da premere, con la parete intorno assottigliata a 1,2 mm perché ceda
// I tasti sporgono 0,45 mm dal telaio (disegni di Apple): dentro la parete c'è una tasca che arriva a 0,1 mm
// dalla punta del tasto, così il tasto non resta premuto; fuori la parete si assottiglia a 1,2 mm
SPORGE = 0.45;
TASCA = SPORGE + 0.1;                  // dal telaio del telefono al fondo della tasca
module tasca_tasto(yb, mezzo, sp, verso) {
    translate([verso * (W / 2 + TASCA / 2), L / 2 - yb, ZC])
        cube([TASCA + 0.02, 2 * mezzo + 1, sp + 1], center = true);
}
INCAVO = K - TASCA - 1.2;              // profondità dell'incavo esterno
module incavo_tasto(yb, mezzo, sp, verso) {
    translate([verso * (W / 2 + K - INCAVO + 1.5), L / 2 - yb, ZC])
        cube([3, 2 * mezzo + 3, sp + 3.2], center = true);
}
module cuscinetto(yb, mezzo, sp, verso) {
    translate([verso * (W / 2 + K - INCAVO + (INCAVO + 0.6) / 2 - 0.01), L / 2 - yb, ZC])
        cube([INCAVO + 0.6, 2 * mezzo - 1, sp], center = true);
}

// Righe in rilievo sui fianchi per la presa (tra i tasti), alte quanto il telefono
module righe(y_da, y_a, verso) {
    n = floor((y_a - y_da) / 3);
    if (n >= 2)
        for (i = [0:n - 1])
            translate([verso * (W / 2 + K + 0.3), L / 2 - (y_da + 1.5 + i * 3), fondo + 0.8])
                linear_extrude(T - 1.5) square([0.6 + 0.6, 1.2], center = true);
}

module base() {
    difference() {
        union() {
            guscio();
            // righe sui fianchi: a sinistra sotto il volume, a destra sotto il tasto laterale
            righe(TASTI_SX[2][0] + TASTI_SX[2][1] + 6, TASTI_SX[2][0] + TASTI_SX[2][1] + 30, -1);
            righe(TASTO_DX[0] + TASTO_DX[1] + 6,
                  CC > 0 ? CC - 21 : TASTO_DX[0] + TASTO_DX[1] + 30, 1);
        }
        vano();
        translate([0, 0, -1]) linear_extrude(fondo + 1.01) fotocamera2d();
        // tasti: incavo sul fuori (la parete resta di 1,2 mm)
        for (t = TASTI_SX) incavo_tasto(t[0], t[1], SP_SX, -1);
        incavo_tasto(TASTO_DX[0], TASTO_DX[1], SP_DX, 1);
        // Controllo fotocamera: aperto fino in cima, 30 mm. Apple chiede 4,2 mm liberi sopra e sotto il centro sul
        // telaio e un cono di 55 gradi verso l'esterno: il fondo dell'apertura scende a 55 gradi attraverso la parete
        if (CC > 0)
            hull() {
                translate([W / 2, L / 2 - CC - 15, ZC - 4.2]) cube([0.01, 30, H]);
                translate([W / 2 + K + PARACOLPI + 1, L / 2 - CC - 15, ZC - 4.2 - (K + PARACOLPI + 1) / tan(55)]) cube([0.01, 30, H]);
            }
        // tasche dei tasti
        for (t = TASTI_SX) tasca_tasto(t[0], t[1], SP_SX, -1);
        tasca_tasto(TASTO_DX[0], TASTO_DX[1], SP_DX, 1);
        // porta USB-C: aperta fino in cima, 14 mm per tutto lo spazio della spina (12,45 × 6,60 mm), 0,5 mm di margine sotto
        translate([-7, -L / 2 - K - 3, ZC - 3.8]) cube([14, K + 4, H]);
        // altoparlante e microfoni: un'asola alta 2,4 mm per i fori più vicini al centro e un foro da 1,8 mm a
        // parte per il più lontano, perché con pareti oltre 2,25 mm Apple chiede canali separati per i microfoni
        for (s = [-1, 1]) {
            translate([s * (FORI[0] + FORI[1] - 2.8) / 2, -L / 2 + 1, ZC]) rotate([90, 0, 0])
                linear_extrude(K + 4) asola(FORI[1] - FORI[0] - 0.4, 2.4);   // da 1,2 mm prima del foro più vicino a 0,7 mm dal foro a parte
            translate([s * FORI[1], -L / 2 + 1, ZC]) rotate([90, 0, 0]) linear_extrude(K + 4) circle(d = 1.8);
        }
    }
    // cuscinetti e dentini dei tasti
    for (t = TASTI_SX) cuscinetto(t[0], t[1], SP_SX, -1);
    cuscinetto(TASTO_DX[0], TASTO_DX[1], SP_DX, 1);
}

/* ---------- Scritte incise sul retro ---------- */

SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}
function inizio_riga(s) = -(1.5 * s + 1.5 + 6.06 * s) / 2;
module nominativo2d(s) {
    xb = inizio_riga(s);
    if (bandiera) translate([xb, 0]) bandiera2d(s);
    translate([xb + 1.5 * s + 1.5 + 3.03 * s, 0]) text(riga1, size = s, font = font, halign = "center", valign = "center");
}
// posizioni dal fondo del telefono, sotto MagSafe; più in basso resta la riga per nome e cognome
Y_NOM = -L / 2 + 47;
Y_R2 = -L / 2 + 37;
Y_R3 = -L / 2 + 30;
module testi2d() {
    translate([0, Y_NOM]) nominativo2d(S1);
    if (riga2 != "") translate([0, Y_R2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    if (riga3 != "") translate([0, Y_R3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
}
module testo() {
    // a specchio: si stampa con il retro sul piano e si legge girando la cover
    translate([0, 0, -0.01]) linear_extrude(rilievo + 0.01) mirror([1, 0]) testi2d();
}

if (parte == "base") base();
else if (parte == "testo") testo();
else difference() { base(); testo(); }
