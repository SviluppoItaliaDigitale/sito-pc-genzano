// Altri oggetti con il nominativo dei volontari della Protezione Civile di Genzano di Roma:
// tessera multiuso (formato carta di credito, con righello e numero di emergenza), etichetta per
// l'attrezzatura (si fissa con due fascette a radio, torce, borse, maniglie) e targa da tavolo per
// la postazione in sala operativa o al COC. Si cambiano solo i parametri qui sotto.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Tipo di oggetto] */
tipo = "tessera"; // [tessera, etichetta, tavolo]
// tutto = pezzo unico; base e testo = pezzi separati
parte = "tutto"; // [tutto, base, testo]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
riga3 = "GENZANO DI ROMA";
font = "Liberation Sans:style=Bold";
// carattere stretto per le righe piccole: con 4,5 mm il tratto più sottile è di 0,70 mm
font2 = "Liberation Sans Narrow:style=Bold";

/* [Bandiera italiana] */
bandiera = true;

/* [Spessori] */
// altezza delle scritte e della cornice sopra la base (mm)
rilievo = 1.0;
// larghezza della cornice (mm)
cornice = 1.2;

$fn = 48;

// Misure per tipo: [lunghezza, altezza, raggio angoli, spessore base, carattere riga1, y riga1,
//                   carattere righe 2-3, y riga2, y riga3, x del centro del nominativo]
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, dettagli da 0,6 mm in su,
// rilievi e incisioni alti e larghi almeno 0,5 mm.
MISURE = [
    ["tessera",   [86, 54, 3.5, 3.0, 8.5, 15.5, 4.5, 6.5, 0.5, -1]],
    ["etichetta", [76, 24, 3.0, 3.0, 6.5, 5.6, 4.0, -1.4, -6.4, 4.5]],
    ["tavolo",    [140, 46, 4.0, 3.5, 16, 8.5, 5.5, -7.5, -15.0, 14]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];
SMUSSO = 0.6;

// Tessera: asola a destra per cordino o moschettone, riga del numero di emergenza, righello sul retro
ASOLA = [3.6, 14]; ASOLA_X = L / 2 - 6;
// Etichetta: due fessure per fascette fino a 5 mm di larghezza
FESSURA = [2.4, 6.5]; FESSURA_X = L / 2 - 4.5;
// Targa da tavolo: due piastre a «tetto» inclinate di 65 gradi, aperte sotto
INCLINA = 65;

module forma() { offset(r = R) square([L - 2 * R, H - 2 * R], center = true); }

module fori() {
    if (tipo == "tessera") translate([ASOLA_X, 7]) offset(r = ASOLA[0] / 2 - 0.01) square(ASOLA - [ASOLA[0] - 0.02, ASOLA[0] - 0.02], center = true);
    if (tipo == "etichetta") for (s = [-1, 1]) translate([s * FESSURA_X, 0]) offset(r = 1) square(FESSURA - [2, 2], center = true);
}

module sagoma(inset = 0) {
    difference() {
        offset(delta = -inset) forma();
        offset(delta = inset) fori();
    }
}

// Tricolore a sinistra del nominativo: tre fasce separate da solchi di 0,8 mm
BAND_H = S1; BAND_W = S1 * 1.5; SOLCO = 0.8;
// bordo sinistro della bandiera: posto per il nominativo più lungo («ALFA 100») senza toccarla
BAND_X = tipo == "tessera" ? -39.5 : tipo == "etichetta" ? -27 : -57;
module bandiera2d() {
    for (i = [0:2])
        translate([BAND_X - TX + i * BAND_W / 3 + (i > 0 ? SOLCO / 2 : 0), Y1 - BAND_H / 2])
            square([BAND_W / 3 - (i == 1 ? SOLCO : SOLCO / 2), BAND_H]);
}

module testi2d() {
    translate([TX, 0]) {
        if (bandiera) bandiera2d();
        translate([0, Y1]) text(riga1, size = S1, font = font, halign = "center", valign = "center");
    }
    sposta = tipo == "tessera" ? -3 : 0;   // nella tessera le righe piccole lasciano posto all'asola
    if (riga2 != "") translate([sposta, Y2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    if (riga3 != "") translate([sposta, Y3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
    if (tipo == "tessera") {
        translate([sposta, -10]) text("EMERGENZA 112", size = 6.5, font = font, halign = "center", valign = "center");
        // righello in rilievo lungo il bordo basso: tacche ogni 5 mm, numeri ogni centimetro
        for (i = [0:14]) translate([-38 + i * 5 - 0.4, -H / 2 + SMUSSO + cornice - 0.01])
            square([0.8, i % 2 == 0 ? 4.5 : 2.8]);
        for (i = [0:7]) translate([-38 + i * 10, -H / 2 + 9.3]) text(str(i), size = 4.5, font = font2, halign = "center", valign = "center");
        translate([40.5, -H / 2 + 5]) text("cm", size = 4.5, font = font2, halign = "right", valign = "center");
    }
}

module corpo() {
    for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) sagoma(0.4 - i * 0.2);
    translate([0, 0, 0.4]) linear_extrude(B - 0.4 - SMUSSO + 0.01) sagoma();
    for (i = [0:2]) translate([0, 0, B - SMUSSO + i * 0.2]) linear_extrude(0.21 - (i == 2 ? 0.01 : 0)) sagoma(0.2 * (i + 1));
}

module rilievo2d() {
    testi2d();
    if (cornice > 0) difference() { sagoma(SMUSSO); sagoma(SMUSSO + cornice); }
}

module piastra(parte) {
    if (parte == "tutto" || parte == "base") corpo();
    if (parte == "tutto" || parte == "testo") translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) rilievo2d();
}

// Targa da tavolo: la piastra con le scritte davanti e una piastra liscia dietro, unite in alto.
// Le facce interne sono inclinate di 65 gradi: si stampa in piedi, senza supporti.
CALO = 2;   // si taglia la base per avere un appoggio piatto
module tavolo(parte) {
    D = H * cos(INCLINA);                      // sporgenza in pianta di ciascuna piastra
    intersection() {
        translate([0, 0, -CALO]) union() {
            rotate([INCLINA, 0, 0]) translate([0, H / 2, 0]) piastra(parte);
            // la piastra dietro, uguale ma senza scritte, si incrocia con quella davanti in alto:
            // il colmo è a V anche dentro, quindi niente soffitti piatti da sostenere
            if (parte != "testo") translate([0, 2 * D - 2 * B, 0]) mirror([0, 1, 0]) rotate([INCLINA, 0, 0]) translate([0, H / 2, 0]) corpo();
        }
        translate([-L, -L, 0]) cube([2 * L, 3 * L, 2 * L]);
    }
}

if (tipo == "tavolo") tavolo(parte);
else piastra(parte);
