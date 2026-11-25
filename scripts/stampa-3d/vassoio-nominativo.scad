// Vassoio porta piatto, bicchiere e posate con il nominativo (volontari della Protezione Civile di Genzano di Roma).
// Il piatto e il bicchiere si infilano in due fori più stretti del loro bordo: restano appesi e non scivolano.
// Le posate stanno sotto una clip a molla. Il vassoio è rialzato su dodici piedini, perché piatto e bicchiere
// scendono sotto il piano; ai due lati corti ha un'asola per le dita, che fa da manico. È in tre pezzi uniti da
// cinque viti, perché intero (456 × 240 mm) non entra nel piatto
// di una stampante da tavolo: ogni pezzo sta in 250 × 210 mm (Original Prusa MK4S: scheda su prusa3d.com,
// consultata il 25/11/2026). Le scritte stanno su una targhetta avvitata sopra il piano: si stampa a parte, con le
// lettere in alto, così possono avere un colore diverso dal fondo.
// Il vassoio porta le stoviglie: non è un oggetto per alimenti e il cibo non va appoggiato sulla plastica stampata.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Pezzo] */
// tutto = targhetta con il nominativo; base e testo = la targhetta divisa per la stampa a due colori;
// sinistra, centro, destra = i tre pezzi del vassoio, già capovolti per la stampa (il piano sta sul piatto);
// clip = clip per le posate, coricata per la stampa; montato = vassoio montato, solo da guardare;
// controllo_viti = solo le parti delle scritte che finirebbero sotto una vite (deve risultare vuoto)
// sinistra180 e centro180 = seconda versione dei due pezzi del piatto, con il foro da 180 mm
parte = "tutto"; // [tutto, base, testo, sinistra, centro, destra, sinistra180, centro180, clip, montato, controllo_viti]
tipo = "vassoio"; // [vassoio]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
riga3 = "GENZANO DI ROMA";
font = "Liberation Sans:style=Bold";
// carattere stretto per le righe piccole: a 4 mm il tratto più sottile resta sopra 0,6 mm
font2 = "Liberation Sans Narrow:style=Bold";

/* [Bandiera italiana] */
// piccola bandiera in rilievo a sinistra del nominativo, alta quanto le lettere grandi (proporzioni 2:3)
bandiera = true;

/* [Spessori] */
// altezza delle scritte sopra la targhetta (mm)
rilievo = 1.0;

$fn = 64;

/* ---------- Stoviglie: misure (con la fonte) ---------- */

// Piatto piano usa e getta «da 22 cm»: 225 mm in alto, 165 mm alla base, alto 20 mm. Piatto fondo «da 22 cm»:
// 220 mm in alto, 145 mm alla base, alto 27 mm (Dopla Green, schede del rivenditore office.centrolibri.it,
// consultate il 25/11/2026). Il foro del piatto è di 200 mm: più stretto del bordo dei due piatti (che quindi non
// passano) e più largo della loro base (che quindi scende nel foro). Un piatto con il bordo sotto i 205 mm cade.
// Bicchiere usa e getta da 200 ml: 70 mm alla bocca (scheda tecnica Euronda Monoart mod. 80, rev. 11/2024), 46 mm
// alla base e 70 mm alla bocca, alto 97 mm (bicchieri in polipropilene Semadeni, scheda su avantorsciences.com);
// fonti consultate il 25/11/2026. Il foro del bicchiere è di 56 mm: il bicchiere scende di circa 40 mm e si
// ferma. Un bicchiere con la base più larga di 56 mm non entra: si appoggia sul piano.
// Piedini: il piano sta a 48 mm dal tavolo, 6 mm più di quanto scende quel bicchiere (42 mm, contando lo smusso).
// Il PETG comincia a deformarsi a 68 gradi (temperatura di inflessione sotto carico, scheda tecnica Prusament PETG
// di Prusa Polymers, consultata il 25/11/2026): niente stoviglie o bevande bollenti.
// Seconda versione (foro da 180 mm): il piatto appoggia più in basso, sulla parete, e sotto il bordo restano
// 22 mm di vassoio per parte con il piatto piano e 20 mm con il fondo (con il foro da 200 mm sono 12 e 10 mm).
// La base dei due piatti (165 e 145 mm) entra comunque. Per piatti leggeri, pieni o molli è la più sicura.
STRETTO = parte == "sinistra180" || parte == "centro180";
FORO_PIATTO = STRETTO ? 180 : 200; FORO_BICCHIERE = 56;
PIANO = 3.0;                  // spessore del piano (15 strati da 0,2 mm)
NERV = 15;                    // fin dove scendono le nervature sotto il piano (12 mm oltre il piano)
FLANGIA = 26;                 // fin dove scendono le pareti di giunzione (23 mm oltre il piano)
PIEDE = 48;                   // altezza del piano dal tavolo
SM = 1.5;                     // smusso dei fori sul lato dove si infilano piatto e bicchiere

/* ---------- Viti e dadi ---------- */

// Viti M4 × 10 a testa svasata con esagono incassato (ISO 10642) e dadi esagonali M4 (ISO 4032).
// Testa della vite: cono a 90 gradi, diametro teorico fino a 8,96 mm, alta fino a 2,48 mm (tabella della norma BS EN
// ISO 10642 riportata da engineersedge.com). Dado: 7 mm fra le facce piane, alto fino a 3,2 mm (ISO 4032:1979,
// estratto su standards.iteh.ai; scheda Fabory dell'articolo 01103040001). Foro di passaggio di 4,5 mm: serie media
// della ISO 273:1979, ripresa dalla norma indiana IS 1821:1987 (law.resource.org). Fonti consultate il 25/11/2026.
FORO = 4.5; SVASO_D = 9.4; SVASO_H = 2.45; DADO = 7.2; DADO_H = 3.4;

/* ---------- Pianta (vista da sopra, vassoio in uso) ---------- */

LARGO = 456; FONDO = 240;                      // ingombro del vassoio montato
G1 = 148; G2 = 328;                            // giunzioni: sinistra | centro | destra
PX = 148;                                      // centro del piatto: la prima giunzione taglia il foro a metà
CX = 381; CY = 62;                             // centro del bicchiere
NX = 381; NY = -62;                            // centro della targhetta
POS_X = 291; POS_L = 55;                       // corsia delle posate: centro e distanza fra le gambe della clip
NERV_X = 256;                                  // nervatura fra il piatto e le posate
// Manici: un'asola di 92 × 22 mm per le dita a ogni lato corto; fuori dall'asola resta una barra larga 7 mm
MAN_X = [18, LARGO - 18]; MAN_L = 92; MAN_W = 22;
CLIP_Y = [-20, 60];                            // due posti per la clip (se ne usa una, o due)
RA = 10;                                       // raggio degli angoli del vassoio
FL_A = 4; FL_B = 8;                            // pareti di giunzione: quella con le teste delle viti, quella con i dadi
VITE_Z = 14.5;                                 // quota delle viti di giunzione sotto il piano
VITI_1 = [-110, 110]; VITI_2 = [-85, 0, 85];   // viti della prima e della seconda giunzione
// Piedini: quattro per pezzo, così ogni pezzo sta in piedi anche da solo
PIEDI = [[22, 98], [130, 109], [168, 109], [312, 107], [348, 107], [434, 98]];

/* ---------- Targhetta ---------- */

// Misure della targhetta: [larghezza, altezza, raggio angoli, spessore base (18 strati), carattere riga1, y riga1,
//                         carattere righe piccole, y riga2, y riga3]
// Regole dei servizi di stampa FDM (Craftcloud): tratti delle lettere da 0,6 mm in su, rilievi alti e larghi almeno
// 0,5 mm. Liberation Sans Bold a 8 mm e Narrow Bold a 4 mm passano il controllo.
MISURE = [
    ["vassoio", [76, 50, 4, 3.6, 8.0, 14, 4.0, -7, -13.5]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
T_L = M[0]; T_H = M[1]; T_R = M[2]; T_S = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8];
T_VITI = [[-31, -11], [31, -11]];

// Tricolore: tre fasce separate da solchi di 0,8 mm, alto quanto le lettere grandi (proporzioni 2:3)
SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}
// Nominativo con la bandiera a sinistra, il tutto centrato: la bandiera ha un posto fisso, pensato per «ALFA 100»
// (largo circa 6,06 volte la dimensione del carattere), 1,5 mm prima del nominativo.
function inizio_riga(s) = -(1.5 * s + 1.5 + 6.06 * s) / 2;
module nominativo2d(s) {
    xb = inizio_riga(s);
    if (bandiera) translate([xb, 0]) bandiera2d(s);
    translate([xb + 1.5 * s + 1.5 + 3.03 * s, 0]) text(riga1, size = s, font = font, halign = "center", valign = "center");
}
module riga(t, y) {
    translate([0, y]) text(t, size = S2, font = font2, halign = "center", valign = "center");
}
// Nominativo, fascia libera per nome e cognome, poi l'ente su due righe
module testi2d() {
    translate([0, Y1]) nominativo2d(S1);
    if (riga2 != "") riga(riga2, Y2);
    if (riga3 != "") riga(riga3, Y3);
}
module targhetta_base() {
    difference() {
        hull() {
            linear_extrude(0.01) offset(r = T_R) square([T_L - 2 * T_R, T_H - 2 * T_R], center = true);
            translate([0, 0, T_S - 1]) linear_extrude(0.01) offset(r = T_R) square([T_L - 2 * T_R, T_H - 2 * T_R], center = true);
            translate([0, 0, T_S - 0.01]) linear_extrude(0.01) offset(r = T_R - 1) square([T_L - 2 * T_R, T_H - 2 * T_R], center = true);
        }
        for (p = T_VITI) translate([p[0], p[1], 0]) {
            translate([0, 0, -1]) cylinder(d = FORO, h = T_S + 2, $fn = 32);
            translate([0, 0, T_S - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.01, $fn = 32);
        }
    }
}
module targhetta_testo() {
    translate([0, 0, T_S - 0.01]) linear_extrude(rilievo + 0.01) testi2d();
}

/* ---------- Vassoio: spazio di progetto ---------- */

// Qui il vassoio è disegnato visto da sopra, con z = profondità sotto il piano (z = 0 è la faccia dove si
// appoggiano le stoviglie). Per la stampa i pezzi si specchiano in y: così il piano sta sul piatto della stampante
// e nervature, pareti e piedini salgono senza parti sospese.
module contorno2d() {
    translate([RA, -FONDO / 2 + RA]) offset(r = RA) square([LARGO - 2 * RA, FONDO - 2 * RA]);
}
module foro2d(i, extra) {
    if (i == 0) translate([PX, 0]) circle(d = FORO_PIATTO + 2 * extra, $fn = 180);
    if (i == 1) translate([CX, CY]) circle(d = FORO_BICCHIERE + 2 * extra, $fn = 96);
    if (i > 1) hull() for (v = [-1, 1]) translate([MAN_X[i - 2], v * (MAN_L - MAN_W) / 2]) circle(d = MAN_W + 2 * extra, $fn = 48);
}
module fori2d(extra = 0) {
    translate([PX, 0]) circle(d = FORO_PIATTO + 2 * extra, $fn = 180);
    translate([CX, CY]) circle(d = FORO_BICCHIERE + 2 * extra, $fn = 96);
}
// fessure per le gambe della clip: 2,8 × 10,4 mm
FESSURA = 2.8;
module fessure2d() {
    for (y = CLIP_Y, v = [-1, 1]) translate([POS_X + v * POS_L / 2, y]) square([FESSURA, 10.4], center = true);
}
module manici2d(extra = 0) {
    for (x = MAN_X) hull() for (v = [-1, 1]) translate([x, v * (MAN_L - MAN_W) / 2]) circle(d = MAN_W + 2 * extra, $fn = 48);
}
module anello2d(c, d, s) {
    translate(c) difference() { circle(d = d + 2 * SM + 2 * s, $fn = 180); circle(d = d + 2 * SM - 0.02, $fn = 180); }
}
module nervature2d() {
    difference() { contorno2d(); offset(delta = -2.4) contorno2d(); }               // bordo
    anello2d([PX, 0], FORO_PIATTO, 2.6);
    anello2d([CX, CY], FORO_BICCHIERE, 2.4);
    difference() { manici2d(SM + 3.2); manici2d(SM - 0.01); }                       // bordo delle asole dei manici
    translate([NERV_X, -FONDO / 2]) square([2.4, FONDO]);                           // fra il piatto e le posate
    for (y = [-75, 25]) translate([NERV_X, y - 1.2]) square([G2 - NERV_X, 2.4]);    // sotto la corsia delle posate
    translate([G2, -1.2]) square([CX - FORO_BICCHIERE / 2 - G2, 2.4]);              // pezzo di destra
    translate([G2, NY + 22]) square([MAN_X[1] - MAN_W / 2 - G2, 2.4]);
}
// parete di giunzione: da y0 a y1, spessa s, con il lato sulla giunzione g (verso = -1 a sinistra, 1 a destra)
module parete(g, verso, s, y0, y1) {
    translate([verso < 0 ? g - s : g, y0, PIANO - 0.01]) cube([s, y1 - y0, FLANGIA - PIANO]);
}
module piede(p) {
    translate([p[0], p[1], PIANO - 0.01]) cylinder(d1 = 20, d2 = 13, h = PIEDE - PIANO, $fn = 48);
}
// Tutto il vassoio pieno, senza i tagli delle giunzioni
module corpo() {
    linear_extrude(PIANO) contorno2d();
    translate([0, 0, PIANO - 0.01]) linear_extrude(NERV - PIANO) nervature2d();
    for (p = PIEDI, v = [-1, 1]) piede([p[0], v * p[1]]);
    // sedi dei dadi della targhetta
    for (p = T_VITI) translate([NX + p[0], NY + p[1], PIANO - 0.01]) cylinder(d = 15, h = 4, $fn = 48);
}
module scavi() {
    // fori di piatto e bicchiere, con lo smusso dal lato delle stoviglie
    translate([0, 0, -1]) linear_extrude(PIEDE) { fori2d(); manici2d(); }
    // lo smusso si fa foro per foro: un solo inviluppo li unirebbe tutti
    for (i = [0:3]) hull() {
        translate([0, 0, -0.01]) linear_extrude(0.01) foro2d(i, SM);
        translate([0, 0, SM]) linear_extrude(0.01) foro2d(i, -0.02);
    }
    translate([0, 0, -1]) linear_extrude(PIANO + 2) fessure2d();
    // viti della targhetta: foro e sede esagonale del dado, aperta verso il basso
    for (p = T_VITI) translate([NX + p[0], NY + p[1], 0]) {
        translate([0, 0, -1]) cylinder(d = FORO, h = 10, $fn = 32);
        translate([0, 0, PIANO + 0.6]) cylinder(d = DADO / cos(30), h = DADO_H + 1, $fn = 6);
    }
}
// Giunzione: sulla parete sottile passano le viti, con la testa svasata; nella parete spessa il foro è cieco e il
// dado scende in un'asola aperta. Una costola verticale sulla parete spessa entra in una scanalatura dell'altra:
// tiene allineati i pezzi mentre si stringono le viti.
module viti_teste(g, viti) {                 // nel pezzo a sinistra della giunzione
    for (y = viti) translate([g, y, VITE_Z]) rotate([0, -90, 0]) {
        translate([0, 0, -0.01]) cylinder(d = FORO, h = FL_A + 0.02, $fn = 32);
        translate([0, 0, FL_A - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.02, $fn = 32);
    }
}
module viti_dadi(g, viti) {                  // nel pezzo a destra della giunzione
    for (y = viti) {
        translate([g - 0.01, y, VITE_Z]) rotate([0, 90, 0]) cylinder(d = FORO, h = 7.01, $fn = 32);
        hull() for (z = [VITE_Z, FLANGIA + 6]) translate([g + 2, y, z]) rotate([0, 90, 0])
            cylinder(d = DADO / cos(30), h = DADO_H, $fn = 6);
    }
}
module costole(g, ys, gioco = 0) {
    for (y = ys) translate([g, y, PIANO - 0.01]) cylinder(r = 1.5 + gioco, h = FLANGIA - PIANO + (gioco > 0 ? 1 : 0), $fn = 24);
}
COST_1 = [-105, 105]; COST_2 = [-45, 45];
Y1A = FORO_PIATTO / 2 + 0.6;                   // le pareti della prima giunzione cominciano oltre il foro del piatto

module pezzo_sinistra() {
    difference() {
        union() {
            intersection() { corpo(); translate([-1, -200, -1]) cube([G1 + 1, 400, 100]); }
            for (v = [-1, 1]) parete(G1, -1, FL_A, v > 0 ? Y1A : -FONDO / 2, v > 0 ? FONDO / 2 : -Y1A);
        }
        scavi();
        viti_teste(G1, VITI_1);
        costole(G1, COST_1, 0.2);
    }
}
module pezzo_centro() {
    difference() {
        union() {
            intersection() { corpo(); translate([G1, -200, -1]) cube([G2 - G1, 400, 100]); }
            for (v = [-1, 1]) parete(G1, 1, FL_B, v > 0 ? Y1A : -FONDO / 2, v > 0 ? FONDO / 2 : -Y1A);
            parete(G2, -1, FL_A, -FONDO / 2, FONDO / 2);
            intersection() { costole(G1, COST_1); translate([G1 - 5, -200, 0]) cube([5, 400, 100]); }
        }
        scavi();
        viti_dadi(G1, VITI_1);
        viti_teste(G2, VITI_2);
        costole(G2, COST_2, 0.2);
    }
}
module pezzo_destra() {
    difference() {
        union() {
            intersection() { corpo(); translate([G2, -200, -1]) cube([LARGO - G2 + 1, 400, 100]); }
            parete(G2, 1, FL_B, -FONDO / 2, FONDO / 2);
            intersection() { costole(G2, COST_2); translate([G2 - 5, -200, 0]) cube([5, 400, 100]); }
        }
        scavi();
        viti_dadi(G2, VITI_2);
    }
}

/* ---------- Clip per le posate ---------- */

// Un ponte sopra le posate, con due gambe che entrano nelle fessure del piano e si agganciano sotto con un dente.
// Sotto il ponte una linguetta a molla, spessa 2 mm, preme le posate: da libera scende a circa 1 mm dal piano e
// sotto il ponte restano 6 mm. Le posate si infilano dal manico. Si stampa coricata, così gli strati corrono lungo le gambe e la molla, che devono flettere.
C_LARGA = 10; C_ALTO = 6; C_PONTE = 3; C_GAMBA = 1.6; C_DENTE = 0.8;
// La faccia esterna della gamba sta a 0,1 mm dal bordo esterno della fessura; il dente sporge 0,8 mm oltre e si
// aggancia sotto il piano. Per entrare, la gamba flette verso l'interno, dove la fessura (2,8 mm) lascia 1,1 mm.
C_FUORI = POS_L / 2 + FESSURA / 2 - 0.1;
module clip2d() {                              // x lungo il ponte, y verso l'alto; y = 0 è la faccia del piano
    h = C_ALTO + C_PONTE;
    translate([-C_FUORI, C_ALTO]) square([2 * C_FUORI, C_PONTE]);
    for (v = [-1, 1]) {
        // gamba: 0,3 mm di gioco nella fessura da 3,2 mm, dente verso l'esterno sotto il piano
        translate([v > 0 ? C_FUORI - C_GAMBA : -C_FUORI, -PIANO - 3.2]) square([C_GAMBA, C_ALTO + PIANO + 3.2 + 0.01]);
        polygon([for (p = [[-0.01, -PIANO - 0.25], [C_DENTE, -PIANO - 0.25], [C_DENTE, -PIANO - 1.2], [-0.01, -PIANO - 3.2]])
            [v * (C_FUORI + p[0]), p[1]]]);
    }
    // molla: parte da sotto il ponte, a sinistra, e scende fino a 1,5 mm dal piano
    hull() { translate([-20, C_ALTO + 0.2]) circle(d = 2.0, $fn = 16); translate([-17, C_ALTO - 0.4]) circle(d = 2.0, $fn = 16); }
    hull() { translate([-17, C_ALTO - 0.4]) circle(d = 2.0, $fn = 16); translate([12, 2.1]) circle(d = 2.0, $fn = 16); }
    hull() { translate([12, 2.1]) circle(d = 2.0, $fn = 16); translate([17, 3.2]) circle(d = 2.0, $fn = 16); }
}
module clip() { linear_extrude(C_LARGA) clip2d(); }

/* ---------- Uscite ---------- */

module per_la_stampa() { mirror([0, 1, 0]) children(); }
// Vassoio montato come si usa, con la targhetta nell'origine: il piano sta a z = 0, i piedini scendono a -48 mm
module montato() {
    translate([-NX, -NY, 0]) {
        scale([1, 1, -1]) { pezzo_sinistra(); pezzo_centro(); pezzo_destra(); }
        translate([POS_X, CLIP_Y[0] + C_LARGA / 2, 0]) rotate([90, 0, 0]) clip();
    }
}

if (parte == "tutto" || parte == "base") targhetta_base();
if (parte == "tutto" || parte == "testo") targhetta_testo();
if (parte == "sinistra" || parte == "sinistra180") per_la_stampa() pezzo_sinistra();
if (parte == "centro" || parte == "centro180") per_la_stampa() pezzo_centro();
if (parte == "destra") per_la_stampa() pezzo_destra();
if (parte == "clip") clip();
if (parte == "montato") montato();
// Le due viti della targhetta stanno ai lati delle righe piccole: qui si controlla che resti così (cerchi da 10 mm)
if (parte == "controllo_viti")
    linear_extrude(1) intersection() { testi2d(); union() for (v = T_VITI) translate(v) circle(d = 10); }
