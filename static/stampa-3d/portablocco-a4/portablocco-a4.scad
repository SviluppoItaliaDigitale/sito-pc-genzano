// Portablocco A4 con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Portablocco con il nominativo, per fogli A4 e B5 (volontari della Protezione Civile di Genzano di Roma).
// Una tavoletta rigida con una molla che ferma i fogli in alto e, dietro la molla, un incavo a scatto per la penna.
// La tavoletta è in due metà unite sul retro da una piastra con quattro viti, perché intera non entra nel piatto
// di una stampante da tavolo (250 × 210 mm la Original Prusa MK4S: scheda su prusa3d.com, consultata il
// 25/11/2026). Le due metà si stampano capovolte: la faccia su cui si scrive nasce liscia sul piatto di stampa e le
// nervature salgono sul retro. Le scritte stanno su una targhetta avvitata in alto, stampata a parte con le lettere
// in su: così possono avere un colore diverso dal fondo.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
// a4 = fogli A4 (210 × 297 mm); b5 = fogli B5 (176 × 250 mm)
tipo = "a4"; // [a4, b5]
// tutto = targhetta con il nominativo; base e testo = la targhetta divisa per la stampa a due colori;
// alta e bassa = le due metà della tavoletta, capovolte per la stampa; piastra = piastra di giunzione;
// molla = fermafogli con il porta penna, coricato per la stampa; montato = portablocco montato, solo da guardare;
// controllo_viti = solo le parti delle scritte che finirebbero sotto una vite (deve risultare vuoto)
parte = "tutto"; // [tutto, base, testo, alta, bassa, piastra, molla, montato, rivetti, controllo_viti]

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

// Misure: [larghezza targhetta, altezza targhetta, raggio angoli, spessore targhetta (18 strati), carattere riga1,
//          y riga1, carattere righe piccole, y riga2, y riga3, larghezza del foglio, altezza del foglio]
// Formati dei fogli: A4 210 × 297 mm, B5 176 × 250 mm (serie A e B della norma ISO 216, tabella riportata dalla
// voce «ISO 216» di it.wikipedia.org, consultata il 25/11/2026).
// Regole dei servizi di stampa FDM (Craftcloud): tratti delle lettere da 0,6 mm in su, rilievi alti e larghi almeno
// 0,5 mm. Liberation Sans Bold a 6,5 mm e Narrow Bold a 4 mm passano il controllo.
MISURE = [
    ["a4", [126, 15, 3, 3.6, 6.5, 0, 4.0, 3.1, -3.1, 210, 297]],
    ["b5", [126, 15, 3, 3.6, 6.5, 0, 4.0, 3.1, -3.1, 176, 250]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
T_L = M[0]; T_H = M[1]; T_R = M[2]; T_S = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8];
FW = M[9]; FH = M[10];

/* ---------- Viti e dadi ---------- */

// Viti M4 × 10 a testa svasata con esagono incassato (ISO 10642) e dadi esagonali M4 (ISO 4032).
// Testa della vite: cono a 90 gradi, diametro teorico fino a 8,96 mm, alta fino a 2,48 mm (tabella della norma BS EN
// ISO 10642 riportata da engineersedge.com). Dado: 7 mm fra le facce piane, alto fino a 3,2 mm (ISO 4032:1979,
// estratto su standards.iteh.ai; scheda Fabory dell'articolo 01103040001). Foro di passaggio di 4,5 mm: serie media
// della ISO 273:1979, ripresa dalla norma indiana IS 1821:1987 (law.resource.org). Fonti consultate il 25/11/2026.
// Le sedi dei dadi sono larghe 7,5 mm: un foro stampato esce un po' più stretto del disegno.
FORO = 4.5; SVASO_D = 9.4; SVASO_H = 2.45; DADO = 7.5; DADO_H = 3.4;

/* ---------- Tavoletta: misure ---------- */

// Vista dal davanti: x in larghezza, y verso l'alto, la targhetta è nell'origine.
LARGA = FW + 10;                               // 5 mm di margine per lato
ALTO = 10.5;                                   // bordo in alto, sopra la targhetta
STOP = -37.5;                                  // dove si ferma il bordo alto del foglio (contro la base della molla)
BASSO = STOP - FH - 3;                         // bordo in basso
GIUNTO = (ALTO + BASSO) / 2;                   // le due metà sono uguali in altezza
PELLE = 2.4;                                   // spessore della faccia su cui si scrive (12 strati)
SPESSA = 12.4;                                 // spessore in tutto, con le nervature
FASCIA = 7.8;                                  // spessore delle due fasce accanto alla giunzione
P_S = 4.6; P_L = LARGA - 12; P_H = 40;         // piastra di giunzione: spessore, larghezza, altezza
P_VX = LARGA / 2 - 40; P_VY = 10;              // viti della piastra: due per metà
RA = 6;
T_VX = 56;                                     // viti della targhetta
M_VX = 20; M_VY = -31.5;                       // viti della molla

/* ---------- Targhetta ---------- */

SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}
// Tutto su una fascia: bandiera, nominativo e, a destra, l'ente su due righe
X_BAND = -49.3; X_NOM = X_BAND + 1.5 * S1 + 1.5 + 3.03 * S1; X_ENTE = 27.4;
module testi2d() {
    if (bandiera) translate([X_BAND, Y1]) bandiera2d(S1);
    translate([X_NOM, Y1]) text(riga1, size = S1, font = font, halign = "center", valign = "center");
    if (riga2 != "") translate([X_ENTE, Y2]) text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    if (riga3 != "") translate([X_ENTE, Y3]) text(riga3, size = S2, font = font2, halign = "center", valign = "center");
}
module targhetta_base() {
    difference() {
        hull() {
            linear_extrude(0.01) offset(r = T_R) square([T_L - 2 * T_R, T_H - 2 * T_R], center = true);
            translate([0, 0, T_S - 0.8]) linear_extrude(0.01) offset(r = T_R) square([T_L - 2 * T_R, T_H - 2 * T_R], center = true);
            translate([0, 0, T_S - 0.01]) linear_extrude(0.01) offset(r = T_R - 0.8) square([T_L - 2 * T_R, T_H - 2 * T_R], center = true);
        }
        for (v = [-1, 1]) translate([v * T_VX, 0, 0]) {
            translate([0, 0, -1]) cylinder(d = FORO, h = T_S + 2, $fn = 32);
            translate([0, 0, T_S - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.01, $fn = 32);
        }
    }
}
module targhetta_testo() {
    translate([0, 0, T_S - 0.01]) linear_extrude(rilievo + 0.01) testi2d();
}

/* ---------- Tavoletta: spazio di progetto ---------- */

// Qui z è la profondità dietro la faccia su cui si scrive (z = 0 è quella faccia). Per la stampa le metà si
// specchiano in y: la faccia sta sul piatto e nervature, fasce e sedi salgono senza parti sospese.
module contorno2d() {
    translate([-LARGA / 2 + RA, BASSO + RA]) offset(r = RA) square([LARGA - 2 * RA, ALTO - BASSO - 2 * RA]);
}
module nervature2d() {
    difference() { contorno2d(); offset(delta = -3) contorno2d(); }
    for (x = [-LARGA / 4, 0, LARGA / 4]) translate([x - 1, BASSO]) square([2, ALTO - BASSO]);
    for (y = [BASSO + 55 : 55 : ALTO - 50]) if (abs(y - GIUNTO) > P_H / 2 + 8) translate([-LARGA / 2, y - 1]) square([LARGA, 2]);
    translate([-LARGA / 2, -18]) square([LARGA, 2]);                                  // sotto la targhetta
}
module corpo() {
    linear_extrude(PELLE) contorno2d();
    translate([0, 0, PELLE - 0.01]) linear_extrude(SPESSA - PELLE) nervature2d();
    // fasce accanto alla giunzione: ci appoggia la piastra
    intersection() {
        linear_extrude(FASCIA) contorno2d();
        translate([-LARGA / 2, GIUNTO - P_H / 2, 0]) cube([LARGA, P_H, FASCIA]);
    }
    // sedi dei dadi della targhetta e delle teste delle viti della molla
    for (v = [-1, 1]) {
        translate([v * T_VX, 0, PELLE - 0.01]) cylinder(d = 15, h = 6.6 - PELLE);
        translate([v * M_VX, M_VY, PELLE - 0.01]) cylinder(d = 15, h = 5 - PELLE);
    }
}
module scavi() {
    // posto per la piastra, sopra le fasce
    translate([-P_L / 2 - 0.3, GIUNTO - P_H / 2 - 0.3, FASCIA]) cube([P_L + 0.6, P_H + 0.6, SPESSA]);
    // Viti della piastra. Il dado non sta in una sede aperta verso la piastra (stringendo tirerebbe solo la piastra):
    // scorre in un canale a T che parte dalla giunzione, sotto 2,4 mm di fascia. Così la vite stringe la piastra
    // contro la fascia. Si infila prima di accostare le due metà. Sopra il dado il canale è largo quanto la vite:
    // i due bordi sporgono 1,35 mm e si stampano senza supporti. La vite M4 × 10 entra per 12,2 mm al massimo
    // (testa affondata di 0,2 mm): la punta si ferma a 2,2 mm dalla faccia; il foro arriva a 1 mm dalla faccia, per
    // le teste più piccole del massimo, che affondano di più.
    for (vx = [-1, 1]) translate([vx * P_VX, GIUNTO, 0]) {
        for (vy = [-1, 1]) translate([0, vy * P_VY, 1.0]) cylinder(d = FORO, h = SPESSA, $fn = 32);
        translate([-DADO / 2, -P_VY - DADO / 2 - 0.8, FASCIA - 2.4 - DADO_H]) cube([DADO, 2 * P_VY + DADO + 1.6, DADO_H]);
        translate([-FORO / 2, -P_VY - DADO / 2 - 0.8, FASCIA - 2.4 - 0.01]) cube([FORO, 2 * P_VY + DADO + 1.6, 2.42]);
    }
    for (v = [-1, 1]) {
        // targhetta: la vite scende dal davanti, il dado sta in una sede aperta sul retro
        translate([v * T_VX, 0, -1]) cylinder(d = FORO, h = SPESSA + 2, $fn = 32);
        translate([v * T_VX, 0, 6.6 - DADO_H]) cylinder(d = DADO / cos(30), h = DADO_H + 0.01, $fn = 6);
        translate([v * T_VX, 0, 6.6]) cylinder(d = 13, h = SPESSA);
        // molla: la vite sale dal retro, con la testa svasata nella sede
        translate([v * M_VX, M_VY, -1]) cylinder(d = FORO, h = SPESSA + 2, $fn = 32);
        translate([v * M_VX, M_VY, 5 - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.01, $fn = 32);
        translate([v * M_VX, M_VY, 5]) cylinder(d = 13, h = SPESSA);
    }
}
module meta_alta() {
    difference() {
        intersection() { corpo(); translate([-LARGA, GIUNTO, -1]) cube([2 * LARGA, ALTO - GIUNTO + 1, 50]); }
        scavi();
    }
}
module meta_bassa() {
    difference() {
        intersection() { corpo(); translate([-LARGA, BASSO - 1, -1]) cube([2 * LARGA, GIUNTO - BASSO + 1, 50]); }
        scavi();
    }
}
// Piastra di giunzione: si appoggia sulle due fasce, con le teste svasate delle viti verso il retro
module piastra() {
    difference() {
        linear_extrude(P_S) offset(r = 3) square([P_L - 6, P_H - 6], center = true);
        for (vx = [-1, 1], vy = [-1, 1]) translate([vx * P_VX, vy * P_VY, 0]) {
            translate([0, 0, -1]) cylinder(d = FORO, h = P_S + 2, $fn = 32);
            translate([0, 0, P_S - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.01, $fn = 32);
        }
    }
}

/* ---------- Molla fermafogli con porta penna ---------- */

// Profilo (u verso il basso del foglio, w sopra la faccia): una base avvitata alla tavoletta, dietro la base un
// incavo a C per la penna (per fusti da 8,5 a 9,5 mm: l'apertura è di 8,4 mm, l'interno di 10,2 mm; entra a scatto) e davanti una lamina che preme sui
// fogli. La lamina è spessa 2,4 mm e da libera scende 1 mm sotto la faccia: montata, preme già. Sotto la lamina
// passano circa 20 fogli (2 mm). Si stampa coricata su un fianco: gli strati corrono lungo la lamina.
M_L = 70;                                      // larghezza della molla
M_BASE = 5.4;
LAM = [[11, 4.2], [16.5, 8.6], [38, 0.2], [46, 6.0]];
module molla2d() {
    difference() {
        union() {
            translate([-16, 0]) square([28, M_BASE]);
            translate([-8, 11]) circle(r = 6.4, $fn = 64);
        }
        translate([-8, 11]) circle(r = 5.1, $fn = 64);
        translate([-8 - 4.2, 11]) square([8.4, 10]);
    }
    // radice della lamina: si assottiglia dalla base, senza spigoli dove flette
    hull() { translate([9, 2.7]) circle(d = 5.4, $fn = 32); translate(LAM[1]) circle(d = 2.4, $fn = 24); }
    for (i = [0 : len(LAM) - 2]) hull() { translate(LAM[i]) circle(d = 2.4, $fn = 24); translate(LAM[i + 1]) circle(d = 2.4, $fn = 24); }
}
module molla() {
    difference() {
        linear_extrude(M_L) molla2d();
        for (z = [M_L / 2 - M_VX, M_L / 2 + M_VX]) {
            translate([6, -1, z]) rotate([-90, 0, 0]) cylinder(d = FORO, h = 10, $fn = 32);
            translate([6, M_BASE - DADO_H, z]) rotate([-90, 0, 0]) cylinder(d = DADO / cos(30), h = DADO_H + 2, $fn = 6);
        }
    }
}

/* ---------- Ferramenta stampata: rivetti al posto di viti e dadi ---------- */

// Chi non vuole comprare viti e dadi stampa questi rivetti: entrano negli stessi fori da 4,5 mm. La testa svasata
// si appoggia nella svasatura; il gambo è tagliato in due per il lungo e in punta ha due denti che sporgono 0,4 mm
// dal foro:
// passano nel foro stringendosi e si riaprono nella sede del dado. «presa» è la distanza fra la superficie dove
// sta la testa e la parete su cui appoggerebbe il dado. Si stampano coricati, uniti da una barretta che si spezza:
// così gli strati corrono lungo il gambo. Non stringono come una vite: tengono uniti i pezzi con un po' di gioco.
R_GAMBO = 2.1; R_TESTA = 4.3; R_DENTE = 2.65; R_SPESSO = 3.0; R_TAGLIO = 2.0; R_PUNTA = 3.0;
module rivetto_mezzo(presa) {                  // metà profilo: [raggio, distanza dalla testa]
    lh = presa - 0.4 + 0.15;                   // la testa affonda 0,4 mm nella svasatura; 0,15 mm di gioco
    polygon([[0, 0], [R_TESTA, 0], [R_GAMBO, R_TESTA - R_GAMBO], [R_GAMBO, lh], [R_DENTE, lh], [R_DENTE, lh + 0.8],
             [1.7, lh + R_PUNTA], [0, lh + R_PUNTA]]);
}
module rivetto(presa) {
    lh = presa - 0.4 + 0.15;
    translate([0, 0, R_SPESSO / 2]) difference() {
        intersection() {
            rotate([0, 90, 0]) rotate_extrude($fn = 64) rivetto_mezzo(presa);
            translate([-1, -6, -R_SPESSO / 2]) cube([lh + R_PUNTA + 2, 12, R_SPESSO]);
        }
        hull() {
            translate([1.8, 0, -3]) cylinder(d = R_TAGLIO, h = 6, $fn = 24);   // il taglio comincia dentro la testa: gambe più lunghe, più elastiche
            translate([lh + R_PUNTA + 1, 0, -3]) cylinder(d = R_TAGLIO, h = 6, $fn = 24);
        }
    }
}
// «quanti» rivetti uguali, uniti dalla barretta sotto le teste
module rivetti(presa, quanti) {
    for (i = [0 : quanti - 1]) translate([0, i * 11, 0]) rivetto(presa);
    translate([-0.9, 0, 0]) cube([1.2, (quanti - 1) * 11, 0.8]);
}

/* ---------- Uscite ---------- */

module per_la_stampa() { mirror([0, 1, 0]) children(); }
module montato() {
    scale([1, 1, -1]) {
        meta_alta(); meta_bassa();
        translate([0, GIUNTO, FASCIA]) piastra();
    }
    // la base della molla comincia 2 mm sotto la targhetta e finisce dove si ferma il foglio
    multmatrix([[0, 0, 1, -M_L / 2], [-1, 0, 0, STOP + 12], [0, 1, 0, 0]]) molla();
}

if (parte == "tutto" || parte == "base") targhetta_base();
if (parte == "tutto" || parte == "testo") targhetta_testo();
if (parte == "alta") per_la_stampa() translate([0, -GIUNTO, 0]) meta_alta();
if (parte == "bassa") per_la_stampa() translate([0, -GIUNTO, 0]) meta_bassa();
if (parte == "piastra") piastra();
if (parte == "molla") molla();
if (parte == "montato") montato();
// otto rivetti con la presa di 7 mm: quattro per la piastra, due per la molla, due per la targhetta
if (parte == "rivetti") rivetti(7.0, 8);
// Le due viti della targhetta stanno alle estremità, fuori dalle scritte: qui si controlla (cerchi da 10 mm)
if (parte == "controllo_viti")
    linear_extrude(1) intersection() { testi2d(); union() for (v = [-1, 1]) translate([v * T_VX, 0]) circle(d = 10); }
