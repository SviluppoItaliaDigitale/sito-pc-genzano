// Ganci con nominativo per i volontari della Protezione Civile di Genzano di Roma: appendiabiti da armadietto,
// gancio per l'anta, gancio da cintura e porta radio portatile. Si cambiano solo i parametri qui sotto.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
// appendiabiti = si avvita o si incolla nell'armadietto; anta = si appoggia sopra l'anta; cintura = clip da cintura;
// radio = supporto da parete su cui si aggancia la clip della radio portatile
tipo = "appendiabiti"; // [appendiabiti, anta, cintura, radio]
// tutto = pezzo unico; base e testo = pezzi separati per stampa a due colori
parte = "tutto"; // [tutto, base, testo]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
riga3 = "GENZANO DI ROMA";
font = "Liberation Sans:style=Bold";
// carattere stretto per le righe piccole, così il nome dell'ente entra tutto
font2 = "Liberation Sans Narrow:style=Bold";

/* [Bandiera italiana] */
// piccola bandiera in rilievo a sinistra del nominativo, alta quanto le lettere grandi (proporzioni 2:3)
bandiera = true;

/* [Misure] */
// spessore dell'anta su cui si appoggia il gancio (mm)
spessore_anta = 20;
// spazio per la cintura (mm)
spazio_cintura = 5;
// altezza delle scritte e della cornice sopra la base (mm)
rilievo = 1.0;
// larghezza della cornice (mm)
cornice = 1.2;

$fn = 48;

// Misure della piastra con le scritte: [lunghezza, altezza, raggio angoli, spessore base, carattere riga1, y riga1,
//                                       carattere righe 2-3, y riga2, y riga3, x del centro del testo]
// Stesse regole di stampa delle targhette (Craftcloud, FDM): pareti da 1 mm in su, tratti delle lettere da 0,6 mm in su.
// Lo spessore è di 5 mm perché i ganci portano peso; con PETG pieno al 100% reggono giacche, zaini e radio.
MISURE = [
    ["appendiabiti", [80, 34, 4, 5.0, 8.5, 6.0, 4.5, -2.3, -8.0, 6]],
    ["anta",         [80, 34, 4, 5.0, 8.5, 6.0, 4.5, -2.3, -8.0, 6]],
    ["cintura",      [80, 34, 4, 5.0, 8.5, 6.0, 4.5, -2.3, -8.0, 6]],
    ["radio",        [80, 34, 4, 5.0, 8.5, 6.0, 4.5, -2.3, -8.0, 0]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];
SMUSSO = 0.6;

// Fori per le viti (testa svasata da 4 mm), dove servono
VITI = tipo == "appendiabiti" ? [[-33, 0], [33, 0]]
     : tipo == "radio" ? [[-33, 0], [33, 0], [-33, -60], [33, -60]]
     : [];

// Contorno visto di fronte
module forma() {
    offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
    if (tipo == "appendiabiti" || tipo == "anta")        // linguetta sotto la piastra, dove nasce il gancio
        translate([-13, -46]) offset(r = 4) offset(delta = -4) square([26, 40]);
    if (tipo == "radio")                                   // pannello sotto la piastra per il supporto
        translate([-L / 2, -76]) offset(r = R) offset(delta = -R) square([L, 66]);
    if (tipo == "cintura")                                 // occhiello a destra per un moschettone
        hull() {
            translate([L / 2 + 6, 0]) circle(d = 18);
            translate([L / 2 - R, 0]) square([2 * R, 18], center = true);
        }
}

module fori() {
    if (tipo == "cintura") translate([L / 2 + 6, 0]) circle(d = 8);
}

module sagoma(inset = 0) {
    difference() {
        offset(delta = -inset) forma();
        offset(delta = inset) fori();
    }
}

// Tricolore: tre fasce verticali separate da solchi di 0,8 mm, riconoscibile anche stampato in un solo colore
BAND_H = S1; BAND_W = S1 * 1.5; SOLCO = 0.8; BAND_X = -L / 2 + 3.5;
module bandiera2d() {
    for (i = [0:2])
        translate([BAND_X + i * BAND_W / 3 + (i > 0 ? SOLCO / 2 : 0), Y1 - BAND_H / 2])
            square([BAND_W / 3 - (i == 1 ? SOLCO : SOLCO / 2), BAND_H]);
}

module testi2d() {
    if (bandiera) bandiera2d();
    translate([bandiera ? TX : 0, Y1]) text(riga1, size = S1, font = font, halign = "center", valign = "center");
    if (riga2 != "") translate([0, Y2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    if (riga3 != "") translate([0, Y3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
}

module rilievo2d() {
    difference() {
        union() {
            testi2d();
            if (cornice > 0) difference() { sagoma(SMUSSO); sagoma(SMUSSO + cornice); }
        }
        for (v = VITI) translate(v) circle(d = 10);   // niente rilievo dove appoggia la testa della vite
    }
}

// Piastra con bordi smussati (gradini da 0,2 mm, uno strato di stampa ciascuno)
module piastra() {
    difference() {
        union() {
            for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) sagoma(0.4 - i * 0.2);
            translate([0, 0, 0.4]) linear_extrude(B - 0.4 - SMUSSO + 0.01) sagoma();
            for (i = [0:2]) translate([0, 0, B - SMUSSO + i * 0.2]) linear_extrude(0.21 - (i == 2 ? 0.01 : 0)) sagoma(0.2 * (i + 1));
        }
        for (v = VITI) translate(v) {
            translate([0, 0, -0.01]) cylinder(d = 4.4, h = B + 0.02);
            translate([0, 0, B - 2.2]) cylinder(d1 = 4.4, d2 = 8.8, h = 2.21);
        }
    }
}

// Blocco con spigoli arrotondati lungo l'asse x (per ganci e alette): da [x0,y0,z0] a [x1,y1,z1]
module blocco(a, b, r = 1.5) {
    hull() for (y = [a[1] + r, b[1] - r], z = [a[2] + r, b[2] - r])
        translate([a[0], y, z]) rotate([0, 90, 0]) cylinder(r = r, h = b[0] - a[0]);
}

// Gancio davanti alla linguetta: braccio che esce, punta che risale e rinforzo alla radice
module gancio() {
    blocco([-11, -45, B - 0.5], [11, -35, B + 28]);                 // braccio, 10 mm di spessore
    blocco([-11, -45, B + 21], [11, -23, B + 28]);                  // punta, 7 mm di spessore
    hull() {                                                         // rinforzo a 45 gradi alla radice
        translate([-11, -35, B - 0.5]) cube([22, 0.01, 7]);
        translate([-11, -35, B - 0.5]) cube([22, 7, 0.01]);
    }
}

// Ponte sopra l'anta e aletta che scende dietro
module ponte_anta() {
    D = spessore_anta;
    blocco([-15, H / 2 - 5, -(D + 5)], [15, H / 2, 0.5]);
    blocco([-15, H / 2 - 28, -(D + 5)], [15, H / 2, -D]);
}

// Clip da cintura: ponte in alto e lingua che scende dietro la piastra, con un dentino che trattiene la cintura
module clip_cintura() {
    G = spazio_cintura;
    blocco([-20, H / 2 - 5, -(G + 4)], [20, H / 2, 0.5]);
    blocco([-20, -30, -(G + 4)], [20, H / 2, -G]);
    blocco([-20, -30, -G - 0.5], [20, -25, -G + 1.5], 0.8);
}

// Supporto radio: «cinturone» finto su cui si aggancia la clip della radio, libero in alto
module supporto_radio() {
    blocco([-26, -72, B - 0.5], [26, -62, B + 12]);                // piede che lo tiene staccato dalla parete
    blocco([-26, -72, B + 8], [26, -28, B + 12]);                  // lingua da 4 mm, 7,5 mm davanti alla piastra
}

SPOSTA = tipo == "anta" ? spessore_anta + 5 : tipo == "cintura" ? spazio_cintura + 4 : 0;

translate([0, 0, SPOSTA]) {
    if (parte == "tutto" || parte == "base") {
        piastra();
        if (tipo == "appendiabiti" || tipo == "anta") gancio();
        if (tipo == "anta") ponte_anta();
        if (tipo == "cintura") clip_cintura();
        if (tipo == "radio") supporto_radio();
    }
    if (parte == "tutto" || parte == "testo")
        translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) rilievo2d();
}
