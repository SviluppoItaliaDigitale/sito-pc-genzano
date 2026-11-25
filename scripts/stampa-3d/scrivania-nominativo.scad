// Portapenne e porta foglietti da scrivania con il nominativo (Protezione Civile di Genzano di Roma).
// Davanti hanno una guida in cui scorre una targhetta con bandiera, nominativo ed ente: la targhetta si stampa a
// parte, con le scritte in alto, così possono avere un colore diverso dal fondo. Niente viti né colla.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
tipo = "penne"; // [penne, foglietti]
// tutto = targhetta con il nominativo; base e testo = la targhetta divisa per la stampa a due colori;
// corpo = il portapenne o il porta foglietti; montato = con la targhetta infilata, solo da guardare
parte = "tutto"; // [tutto, base, testo, corpo, montato]

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
// altezza delle scritte sopra la targhetta (mm)
rilievo = 1.0;

$fn = 48;

// Misure della targhetta: [lunghezza, larghezza in basso, raggio angoli, spessore (12 strati da 0,2 mm),
//                         carattere riga1, y riga1, carattere righe piccole, y riga2, y riga3]
// I due lati lunghi sono smussati a 45 gradi: in alto la targhetta è larga 14,2 mm ed è tenuta dalla guida.
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, tratti delle lettere da 0,6 mm in su.
// Liberation Sans Bold a 6,5 mm e Narrow Bold a 4 mm passano il controllo.
MISURE = [
    ["penne", [102, 19, 0, 2.4, 6.5, 0, 4.0, 3.0, -3.0]],
    ["foglietti", [102, 19, 0, 2.4, 6.5, 0, 4.0, 3.0, -3.0]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
T_L = M[0]; T_H = M[1]; T_S = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8];

SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}
// Bandiera e nominativo a sinistra, ente su due righe a destra
X_BAND = -48; X_NOM = X_BAND + 1.5 * S1 + 1.5 + 3.03 * S1; X_ENTE = 28.5;
module testi2d() {
    if (bandiera) translate([X_BAND, Y1]) bandiera2d(S1);
    translate([X_NOM, Y1]) text(riga1, size = S1, font = font, halign = "center", valign = "center");
    if (riga2 != "") translate([X_ENTE, Y2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    if (riga3 != "") translate([X_ENTE, Y3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
}
// profilo a coda di rondine: largo «larga» in basso, più stretto di due volte l'altezza in alto
module coda(lunga, larga, alta) {
    rotate([90, 0, 90]) linear_extrude(lunga)
        polygon([[-larga / 2, 0], [larga / 2, 0], [larga / 2 - alta, alta], [-larga / 2 + alta, alta]]);
}
module targhetta_base() { translate([-T_L / 2, 0, 0]) coda(T_L, T_H, T_S); }
module targhetta_testo() { translate([0, 0, T_S - 0.01]) linear_extrude(rilievo + 0.01) testi2d(); }

/* ---------- Corpi ---------- */

// Foglietti adesivi quadrati: 76 mm di lato (voce «Post-it» di it.wikipedia.org, consultata il 25/11/2026: il
// formato tipico è un quadrato di 7,6 cm; le pagine del produttore non si aprono da un programma). La sede è di
// 79 mm e alta quanto due blocchetti. Penne e matite: il portapenne è alto 92 mm, con due scomparti.
GIOCO = 0.2;                                   // gioco della targhetta nella guida, per parte
G_ALTA = 6;                                    // altezza del fondo della guida dal tavolo
G_L = 25;                                      // profondità del gradino davanti, con la guida
PARETE = 2.0; FONDO = 2.4; RA = 4;
P_LARGO = 110; P_FONDO = 70; P_ALTO = 92;      // portapenne
F_SEDE = 79; F_VANO = 30; F_ALTO = 24;         // porta foglietti: sede dei foglietti, vano per le graffette
F_LARGO = F_SEDE + F_VANO + 3 * 2.4; F_FONDO = F_SEDE + 2 * 2.4;

module tondo(l, f, r = RA) { translate([-l / 2 + r, r]) offset(r = r) square([l - 2 * r, f - 2 * r]); }
// Gradino con la guida: la targhetta entra da destra e si ferma a sinistra, centrata
module gradino(larga) {
    difference() {
        translate([0, -G_L / 2, 0]) linear_extrude(G_ALTA + T_S + GIOCO) tondo(larga, G_L + RA);
        translate([-T_L / 2 - 0.3, 0, G_ALTA]) coda(larga, T_H + 2 * GIOCO, T_S + GIOCO + 0.01);
        translate([-T_L / 2 - 0.3, -(T_H - 2 * T_S) / 2 - GIOCO, G_ALTA + T_S]) cube([larga, T_H - 2 * T_S + 2 * GIOCO, 2]);
    }
}
module portapenne() {
    gradino(P_LARGO);
    translate([0, G_L / 2, 0]) difference() {
        linear_extrude(P_ALTO) tondo(P_LARGO, P_FONDO);
        difference() {
            translate([0, PARETE, FONDO]) linear_extrude(P_ALTO) tondo(P_LARGO - 2 * PARETE, P_FONDO - 2 * PARETE, RA - PARETE);
            translate([16, 0, 0]) cube([PARETE, P_FONDO, P_ALTO]);     // divisorio: penne a sinistra, forbici e pennarelli a destra
        }
    }
}
module portafoglietti() {
    gradino(F_LARGO);
    translate([0, G_L / 2, 0]) difference() {
        linear_extrude(F_ALTO) tondo(F_LARGO, F_FONDO);
        translate([-F_LARGO / 2 + 2.4, 2.4, FONDO]) cube([F_SEDE, F_SEDE, F_ALTO]);
        translate([-F_LARGO / 2 + 2.4 + F_SEDE + 2.4, 2.4, FONDO]) linear_extrude(F_ALTO) translate([F_VANO / 2, 0]) tondo(F_VANO, F_SEDE, 2);
        // due inviti per prendere i foglietti con le dita: dietro e a sinistra
        translate([-F_LARGO / 2 + 2.4 + F_SEDE / 2 - 13, F_FONDO - 4, FONDO + 5]) cube([26, 8, F_ALTO]);
        translate([-F_LARGO / 2 - 2, 2.4 + F_SEDE / 2 - 13, FONDO + 5]) cube([6, 26, F_ALTO]);
    }
}
module corpo() { if (tipo == "penne") portapenne(); else portafoglietti(); }

if (parte == "tutto" || parte == "base") targhetta_base();
if (parte == "tutto" || parte == "testo") targhetta_testo();
if (parte == "corpo") corpo();
if (parte == "montato") translate([0, 0, -G_ALTA]) corpo();
