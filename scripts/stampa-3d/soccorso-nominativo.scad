// Oggetti con il nominativo per l'intervento (volontari della Protezione Civile di Genzano di Roma): cuneo
// fermaporta, targhetta a sgancio rapido, scatola dei guanti con coperchio scorrevole e capsula a vite.
// Si cambiano solo i parametri qui sotto. Le idee vengono da ciò che si stampano da sé i vigili del fuoco;
// i disegni sono nostri. Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
// cuneo = fermaporta da tenere nello zaino; sgancio = targhetta che si aggancia a scatto a un anello o a un
// moschettone e si toglie con un colpo anche con i guanti; guanti = coperchio scorrevole con le scritte (la scatola
// è il secondo pezzo); capsula = corpo della capsula con le scritte (il tappo a vite è il secondo pezzo)
tipo = "cuneo"; // [cuneo, sgancio, guanti, capsula]
// tutto = pezzo con le scritte; base e testo = pezzi separati per stampa a due colori;
// scatola e tappo = secondo pezzo, uguale per tutti i nominativi
parte = "tutto"; // [tutto, base, testo, scatola, tappo]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
riga3 = "GENZANO DI ROMA";
font = "Liberation Sans:style=Bold";
// carattere stretto per le righe piccole: a 4 mm il tratto più sottile resta sopra 0,6 mm
font2 = "Liberation Sans Narrow:style=Bold";

/* [Bandiera italiana] */
bandiera = true;

/* [Misure] */
// diametro del filo dell'anello o del moschettone dove si aggancia la targhetta (mm): misuralo con un righello.
// La bocca è più stretta del filo di 0,8 mm: la targhetta entra con una leggera pressione. La tenuta va provata.
filo = 8;
// altezza delle scritte sopra la base (mm)
rilievo = 1.0;

$fn = 48;

// Misure per tipo: [lunghezza, altezza, raggio angoli, spessore base, carattere riga1, y riga1,
//                   carattere righe piccole, y riga2, y riga3, x del centro delle scritte]
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, tratti delle lettere da 0,6 mm in su,
// rilievi alti e larghi almeno 0,5 mm.
MISURE = [
    ["cuneo",   [130, 30, 2, 25, 6.5, 8.5, 4.0, 17.0, 0, 64]],
    ["sgancio", [70, 34, 4, 3.0, 6.5, 10.75, 4.0, -4.5, -10.0, 0]],
    ["guanti",  [122.2, 66.0, 3, 2.0, 6.5, 12.0, 4.0, -3.0, -8.5, -4]],
    ["capsula", [26, 70, 0, 2.0, 6.0, 0, 4.0, 0, 0, 0]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];
SMUSSO = 0.6;

/* ---------- Scritte ---------- */

SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}
// Nominativo con la bandiera a sinistra, centrato in x: posto fisso pensato per «ALFA 100»
function inizio_riga(s) = -(1.5 * s + 1.5 + 6.06 * s) / 2;
module nominativo2d(s) {
    xb = inizio_riga(s);
    if (bandiera) translate([xb, 0]) bandiera2d(s);
    translate([xb + 1.5 * s + 1.5 + 3.03 * s, 0]) text(riga1, size = s, font = font, halign = "center", valign = "center");
}
module riga(t, x, y, s = S2, f = font2) {
    translate([x, y]) text(t, size = s, font = f, halign = "center", valign = "center");
}
module testi2d() {
    translate([TX, Y1]) nominativo2d(S1);
    if (tipo == "cuneo") riga("PC GENZANO DI ROMA", TX + 19, Y2);
    else {
        if (riga2 != "") riga(riga2, TX, Y2);
        if (riga3 != "") riga(riga3, TX, Y3);
    }
}

/* ---------- Piastre (sgancio e coperchio dei guanti) ---------- */

// Targhetta a sgancio: anello aperto a sinistra, con il foro 0,6 mm più largo del filo e la bocca più stretta del
// filo di 0,8 mm, rivolta verso l'esterno (con 1,5 mm le ganasce corte si deformerebbero oltre il limite del PETG).
// Parete dell'anello 3,5 mm.
SG_FORO = filo + 0.6; SG_PARETE = 3.5; SG_BOCCA = filo - 0.8;
SG_X = -L / 2 - SG_FORO / 2 - SG_PARETE + 3;
module forma() {
    offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
    if (tipo == "sgancio")
        offset(r = 1) offset(delta = -1) hull() {
            translate([SG_X, 0]) circle(d = SG_FORO + 2 * SG_PARETE, $fn = 64);
            translate([-L / 2 + R, 0]) square([2 * R, SG_FORO + 2 * SG_PARETE], center = true);
        }
}
module fori() {
    if (tipo == "sgancio") translate([SG_X, 0]) {
        circle(d = SG_FORO, $fn = 64);
        offset(r = 0.6) offset(delta = -0.6)
            translate([-SG_FORO / 2 - SG_PARETE - 1, -SG_BOCCA / 2]) square([SG_FORO / 2 + SG_PARETE + 1, SG_BOCCA]);
    }
}
module sagoma(inset = 0) {
    difference() { offset(delta = -inset) forma(); offset(delta = inset) fori(); }
}
// Piastra con bordi smussati (gradini da 0,2 mm, uno strato di stampa ciascuno). Il coperchio dei guanti ha i
// bordi dritti, perché scorre nelle scanalature della scatola.
module piastra() {
    if (tipo == "guanti") linear_extrude(B) sagoma();
    else union() {
        for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) sagoma(0.4 - i * 0.2);
        translate([0, 0, 0.4]) linear_extrude(B - 0.4 - SMUSSO + 0.01) sagoma();
        for (i = [0:2]) translate([0, 0, B - SMUSSO + i * 0.2]) linear_extrude(0.21 - (i == 2 ? 0.01 : 0)) sagoma(0.2 * (i + 1));
    }
}

/* ---------- Cuneo fermaporta ---------- */

// Profilo visto di fianco: lungo 130 mm, alto 3 mm in punta e 30 mm in coda, con il tratto piano in coda
// (35 mm) dove sta il foro per il moschettone. Sotto ha cinque denti bassi che fanno presa sul pavimento.
// Si stampa sdraiato su un fianco: le scritte stanno sull'altro fianco, il profilo sale strato per strato.
CU_FORO = [121, 15];   // centro del foro per il moschettone, diametro 9 mm
module cuneo2d() {
    difference() {
        union() {
            polygon([[-L / 2, 1.2], [L / 2, 1.2], [L / 2, H], [L / 2 - 35, H], [-L / 2, 3]]);
            for (i = [0:4]) translate([-L / 2 + 25 + i * 22, 0])
                polygon([[0, 1.3], [10, 1.3], [12, 0], [2, 0]]);
        }
        translate([CU_FORO[0] - L / 2, CU_FORO[1]]) circle(d = 9);
    }
}
module cuneo_base() {
    // spigoli arrotondati di 1 mm sui fianchi: gradini da 0,2 mm in basso e in alto
    for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) offset(delta = -(0.4 - i * 0.2)) cuneo2d();
    translate([0, 0, 0.4]) linear_extrude(B - 0.4 - SMUSSO + 0.01) cuneo2d();
    for (i = [0:2]) translate([0, 0, B - SMUSSO + i * 0.2]) linear_extrude(0.21 - (i == 2 ? 0.01 : 0)) offset(delta = -0.2 * (i + 1)) cuneo2d();
}

/* ---------- Scatola dei guanti (secondo pezzo) ---------- */

// Interno 110 × 64 mm, alto 30 mm fino alle scanalature. Pareti da 3 mm, fondo da 2 mm. Il coperchio (2 mm, largo 66)
// scorre in due scanalature alte 3 mm e profonde 1,5 mm: 0,5 mm di gioco per lato, come la tolleranza dei servizi di stampa nei lati lunghi e nel lato in fondo; dal lato d'ingresso la
// parete è più bassa, così il coperchio entra e la sua linguetta (7,7 mm) resta fuori per tirarlo. Gli angoli in fondo
// alle scanalature sono arrotondati, così negli angoli della scatola restano 1,5 mm di parete.
G_IN = [110, 64]; G_P = 3; G_FONDO = 2; G_ALTO = 30; G_SCAN = [3.0, 1.5]; G_LABBRO = 1.6;
G_EST = G_IN + 2 * [G_P, G_P]; G_H = G_FONDO + G_ALTO + G_SCAN[0] + G_LABBRO;
module scatola() {
    z0 = G_FONDO + G_ALTO;
    difference() {
        linear_extrude(G_H) offset(r = 3) square(G_EST - [6, 6], center = true);
        translate([0, 0, G_FONDO]) linear_extrude(G_H) offset(r = 1) square(G_IN - [2, 2], center = true);
        // scanalature: dal lato d'ingresso (x positivo) fino a 1,5 mm dentro la parete in fondo
        translate([0, 0, z0]) linear_extrude(G_SCAN[0]) intersection() {
            translate([-G_IN[0] / 2 - G_SCAN[1], -G_IN[1] / 2 - G_SCAN[1]]) offset(r = 1.5) offset(delta = -1.5)
                square([G_IN[0] + G_SCAN[1] + G_P + 10, G_IN[1] + 2 * G_SCAN[1]]);
            translate([-G_EST[0], -G_EST[1]]) square(2 * G_EST);
        }
        // parete d'ingresso abbassata fino al fondo delle scanalature
        translate([G_IN[0] / 2 - 0.5, -G_IN[1] / 2 - G_SCAN[1], z0]) cube([G_P + 1, G_IN[1] + 2 * G_SCAN[1], G_H]);
    }
}

/* ---------- Capsula a vite ---------- */

// Corpo diametro 26 mm, alto 60 mm più il collo filettato di 10 mm; interno diametro 18 mm e profondo 68 mm.
// Filetto a un principio con passo 5 mm, disegnato come un cerchio fuori centro che ruota salendo: i fianchi
// restano sotto i 45 gradi, quindi il filetto si stampa senza supporti. Il tappo ha 0,5 mm di gioco, come la
// tolleranza dei servizi di stampa.
CA_R = 13; CA_IN = 9; CA_DRITTO = 60; CA_COLLO = 10; CA_PASSO = 5; CA_R0 = 10.8; CA_E = 0.7;
module filetto(h, r) {
    linear_extrude(h, twist = -360 * h / CA_PASSO, slices = 4 * h, convexity = 4)
        translate([CA_E, 0]) circle(r = r, $fn = 64);
}
module capsula_corpo() {
    difference() {
        union() {
            for (i = [0:1]) translate([0, 0, i * 0.2]) cylinder(r = CA_R - 0.4 + i * 0.2, h = 0.21, $fn = 96);
            translate([0, 0, 0.4]) cylinder(r = CA_R, h = CA_DRITTO - 0.4, $fn = 96);
            translate([0, 0, CA_DRITTO - 0.01]) filetto(CA_COLLO, CA_R0);
        }
        translate([0, 0, B]) cylinder(r = CA_IN, h = CA_DRITTO + CA_COLLO, $fn = 64);
    }
}
// Tappo: diametro 29 mm, alto 12,5 mm (10,5 di filetto e 2 di cielo), con un'aletta forata (4 mm) per il cordino.
// I 0,5 mm in più lasciano gioco fra il cielo e la cima del collo, così il tappo chiude sulla spalla del corpo.
// Nel file è capovolto, con il cielo sul piano.
CA_TAPPO_FONDO = CA_COLLO + 0.5;
module tappo() {
    translate([0, 0, CA_TAPPO_FONDO + 2]) rotate([180, 0, 0]) difference() {
        union() {
            cylinder(r = 14.5, h = CA_TAPPO_FONDO + 2, $fn = 96);
            hull() {
                translate([14.5 + 3, 0, CA_COLLO - 1]) cylinder(d = 10, h = 3);
                translate([10, 0, CA_COLLO - 1]) cylinder(d = 10, h = 3);
            }
        }
        translate([0, 0, -0.01]) filetto(CA_TAPPO_FONDO + 0.01, CA_R0 + 0.5);
        translate([14.5 + 3, 0, CA_COLLO - 2]) cylinder(d = 4, h = 6);
    }
}
// Scritte in rilievo sul fianco del corpo, lette dal basso verso l'alto: nominativo e, accanto, l'ente.
module capsula_testo() {
    for (k = [0:1]) rotate([0, 0, k == 0 ? 0 : 28]) intersection() {
        difference() {
            cylinder(r = CA_R + rilievo, h = CA_DRITTO, $fn = 96);
            translate([0, 0, -1]) cylinder(r = CA_R - 0.01, h = CA_DRITTO + 2, $fn = 96);
        }
        translate([0, 0, 1 + CA_DRITTO / 2]) rotate([90, 0, 0]) linear_extrude(CA_R + 2) rotate(90)
            if (k == 0) nominativo2d(S1);
            else riga("PC GENZANO DI ROMA", 0, 0);
    }
}

/* ---------- Montaggio ---------- */

module base() {
    if (tipo == "cuneo") cuneo_base();
    else if (tipo == "capsula") capsula_corpo();
    else piastra();
}
module testo() {
    if (tipo == "capsula") capsula_testo();
    else translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01)
        if (tipo == "cuneo") translate([-L / 2, 0]) testi2d(); else testi2d();
}

if (parte == "tutto" || parte == "base") base();
if (parte == "tutto" || parte == "testo") testo();
if (parte == "scatola") scatola();
if (parte == "tappo") tappo();
