// Oggetti grandi con il nominativo, in due pezzi uniti da viti (volontari della Protezione Civile di Genzano di
// Roma): gruccia per la divisa e gli abiti. È in due pezzi perché intera non entra nel piatto di una stampante da
// tavolo: per esempio 250 × 210 mm la Original Prusa MK4S, 250 × 220 mm la CORE One, 360 × 360 mm la XL (schede su
// prusa3d.com, consultate il 25/11/2026). Il pezzo più grande della gruccia misura 238 × 188 mm: serve un piatto
// di almeno 250 × 200 mm, per lasciare il margine del bordo di adesione. Il pezzo con le scritte cambia con il
// nominativo, il secondo è uguale per tutti. Si cambiano solo i parametri qui sotto.
// Accanto alle scritte resta libera una fascia per una riga con nome e cognome.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
// gruccia = gruccia larga 40 cm con la barra per i pantaloni
tipo = "gruccia"; // [gruccia]
// tutto = il pezzo con il nominativo; base e testo = lo stesso pezzo diviso per la stampa a due colori;
// braccio = secondo pezzo della gruccia (già capovolto per la stampa);
// insieme = i due pezzi montati, solo da guardare: non si stampa così;
// controllo_viti = solo le parti delle scritte che finirebbero sopra una vite (deve risultare vuoto)
parte = "tutto"; // [tutto, base, testo, braccio, insieme, rivetti, controllo_viti]

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
// altezza delle scritte sopra la faccia (mm)
rilievo = 1.0;

$fn = 48;

// Misure per tipo: [lunghezza, altezza, raggio angoli, spessore base, carattere riga1, y riga1,
//                   carattere righe piccole, y riga2, y riga3, x del centro delle scritte]
// Lunghezza × altezza è l'oggetto montato e lo spessore è quello del pezzo.
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, tratti delle lettere da 0,6 mm in su,
// rilievi alti e larghi almeno 0,5 mm. Liberation Sans Bold da 6 mm in su e Narrow Bold a 4 mm passano il controllo.
MISURE = [
    ["gruccia", [400, 188, 6, 10.8, 8.0, 31.0, 4.0, 13.0, 6.5, 0]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];

/* ---------- Viti e dadi ---------- */

// Viti M4 × 10 a testa svasata con esagono incassato (ISO 10642) e dadi esagonali M4 (ISO 4032).
// Testa della vite: cono a 90 gradi, diametro teorico fino a 8,96 mm (reale da 7,53 mm), alta fino a 2,48 mm:
// tabella della norma BS EN ISO 10642 riportata da engineersedge.com. Dado: 7 mm fra le facce piane, alto fino a
// 3,2 mm (ISO 4032:1979, estratto su standards.iteh.ai; scheda Fabory dell'articolo 01103040001). Foro di passaggio
// di 4,5 mm: serie media della ISO 273:1979, ripresa dalla norma indiana IS 1821:1987 (law.resource.org).
// Fonti consultate il 25/11/2026.
// La svasatura è larga 9,4 mm e profonda 2,45 mm: la testa resta circa 0,2 mm sotto la superficie, così non tocca
// i tessuti né il piatto. La sede del dado è larga 7,2 mm e profonda 3,4 mm: il dado entra giusto e non gira
// mentre si stringe la vite. La vite da 10 mm prende quasi tutto il dado e non esce dall'altra parte.
FORO = 4.5; SVASO_D = 9.4; SVASO_H = 2.45; DADO = 7.2; DADO_H = 3.4;

/* ---------- Gruccia: misure (con la fonte) ---------- */

// Larghezza 400 mm: una gruccia di legno per adulti del commercio è larga 43 cm e spessa 14 mm (IKEA BUMERANG,
// articolo 702.385.41: scheda su ikea.com/it, consultata il 25/11/2026).
// Gancio: occhio di 40 mm e apertura di 36,5 mm fra la punta e la piastra. Con la tolleranza di stampa (±0,5 mm
// per superficie) si dichiara per tubi appendiabiti fino a 33 mm. Un tubo ovale per armadi misura 30 × 15 mm (kit
// Emuca, articolo 7061611: scheda su emuca.com, consultata il 25/11/2026). Non c'è una misura unica: chi ha un tubo
// più grosso lo misura prima di stampare.
// Spessore 10,8 mm (54 strati da 0,2 mm): due linguette da 5,4 mm, una vite da 10 mm che non esce dal retro.
// Carico: giacca e pantaloni di una divisa, cioè qualche chilo. Con 3 kg appesi, la flessione nel gancio (sezione di
// 14 × 10,8 mm, braccio di 27 mm) dà circa 2,5 MPa, contro i 47 MPa a cui cede il PETG stampato in piano (scheda
// tecnica Prusament PETG di Prusa Polymers, consultata il 25/11/2026). Giunzioni: il braccio destro porta metà del
// carico (circa 15 N) attraverso linguette da 5,4 mm e due viti M4 per giunzione; taglio e pressione sui fori restano
// di pochi MPa. Sono calcoli, non una prova di carico: per questo la scheda dice «valore di calcolo».
T = 10.8;                     // spessore della gruccia
MEZZO = T / 2;                // piano su cui si toccano le linguette dei due pezzi
SM = 2.0;                     // smusso a 45 gradi di tutti gli spigoli: niente bordi vivi sui tessuti
GIOCO = 0.3;                  // gioco in testa alle linguette

GR_COLLO = 30; GR_SY = -11; GR_SD = 22;        // fascia delle spalle: mezza larghezza, linea di mezzo, altezza
GR_PUNTA = [191, -58]; GR_PD = 18;             // punta del braccio (centro) e sua altezza
GR_BX = 183; GR_BY = -75; GR_BD = 14;          // barra dei pantaloni: mezza lunghezza, linea di mezzo, altezza
GR_PW = 76; GR_PY0 = 0.4; GR_PY1 = 42;         // piastra con le scritte: larghezza, bordo basso, bordo alto
GR_GC = [0, 72]; GR_GR = 27; GR_GW = 14;       // gancio: centro, raggio della linea di mezzo, larghezza
GR_GA0 = -70; GR_GA1 = 150;                    // gancio: angolo del piede e angolo della punta
GR_X0 = 6; GR_X1 = 38;                         // giunzione delle spalle: da x0 a x1 i due pezzi si sovrappongono
GR_XB = 17;                                    // giunzione della barra: da -17 a +17
GR_VITI = [[14, GR_SY], [30, GR_SY], [-8.5, GR_BY], [8.5, GR_BY]];
GR_TACCA_X = 165;                              // tacche per le spalline e i passanti

/* ---------- Scritte ---------- */

// Tricolore: tre fasce separate da solchi di 0,8 mm, alto quanto le lettere grandi (proporzioni 2:3)
SOLCO = 0.8;
module bandiera2d(h) {
    w = h * 1.5;
    for (i = [0:2])
        translate([i * w / 3 + (i > 0 ? SOLCO / 2 : 0), -h / 2])
            square([w / 3 - (i == 1 ? SOLCO : SOLCO / 2), h]);
}

// Nominativo con la bandiera a sinistra, il tutto centrato in x: la bandiera ha un posto fisso, pensato per
// «ALFA 100» (largo circa 6,06 volte la dimensione del carattere), 1,5 mm prima del nominativo.
function inizio_riga(s) = -(1.5 * s + 1.5 + 6.06 * s) / 2;
module nominativo2d(s) {
    xb = inizio_riga(s);
    if (bandiera) translate([xb, 0]) bandiera2d(s);
    translate([xb + 1.5 * s + 1.5 + 3.03 * s, 0]) text(riga1, size = s, font = font, halign = "center", valign = "center");
}

module riga(t, x, y, s = S2, f = font2) {
    translate([x, y]) text(t, size = s, font = f, halign = "center", valign = "center");
}

// Nominativo, fascia libera per nome e cognome, poi l'ente su due righe.
module testi2d() {
    translate([TX, Y1]) nominativo2d(S1);
    if (riga2 != "") riga(riga2, TX, Y2);
    if (riga3 != "") riga(riga3, TX, Y3);
}

/* ---------- Gruccia ---------- */

// Tutta la gruccia è fatta di dischi con gli spigoli smussati, uniti a due a due: così ogni bordo, anche quello del
// gancio, ha lo smusso di 2 mm senza gradini.
module disco(d, h = T, s = SM) {
    rotate_extrude($fn = 40) polygon([[0, 0], [d / 2 - s, 0], [d / 2, s], [d / 2, h - s], [d / 2 - s, h], [0, h]]);
}
module tratto(p, q, dp, dq) {
    hull() { translate(p) disco(dp); translate(q) disco(dq); }
}

function gr_gp(a) = [GR_GC[0] + GR_GR * cos(a), GR_GC[1] + GR_GR * sin(a)];
// Gancio aperto verso sinistra: dal piede, a destra, gira sopra il tubo e finisce con la punta arrotondata.
// Il piede scende dentro la piastra.
module gr_gancio() {
    for (a = [GR_GA0 : 10 : GR_GA1 - 10]) tratto(gr_gp(a), gr_gp(a + 10), GR_GW, GR_GW);
    tratto(gr_gp(GR_GA0), [gr_gp(GR_GA0)[0] - 3, GR_PY1 - 8], GR_GW, GR_GW);
}
module gr_piastra() {
    hull() for (x = [-1, 1], y = [GR_PY0 + 6, GR_PY1 - 6]) translate([x * (GR_PW / 2 - 6), y, 0]) disco(12);
}
module gr_fascia() {
    tratto([-GR_COLLO, GR_SY], [GR_COLLO, GR_SY], GR_SD, GR_SD);
}
module gr_braccio(v) {                       // v = -1 braccio sinistro, 1 braccio destro
    tratto([v * GR_COLLO, GR_SY], [v * GR_PUNTA[0], GR_PUNTA[1]], GR_SD, GR_PD);
    tratto([v * GR_PUNTA[0], GR_PUNTA[1]], [v * GR_BX, GR_BY], GR_PD, GR_BD);
}
module gr_barra() {
    tratto([-GR_BX, GR_BY], [GR_BX, GR_BY], GR_BD, GR_BD);
}

// Tacche: una per braccio sul bordo alto, per spalline e passanti (larga 7 mm, con gli spigoli smussati), e una
// fila di incavi bassi (0,8 mm) sul bordo alto della barra, perché i pantaloni non scivolino.
function gr_bordo_alto(x) = GR_SY + (x - GR_COLLO) * (GR_PUNTA[1] - GR_SY) / (GR_PUNTA[0] - GR_COLLO)
    + (GR_SD - (GR_SD - GR_PD) * (x - GR_COLLO) / (GR_PUNTA[0] - GR_COLLO)) / 2 / cos(atan((GR_SY - GR_PUNTA[1]) / (GR_PUNTA[0] - GR_COLLO)));
module gr_asola(d0, d1, h) {
    hull() for (dy = [0, 14]) translate([0, dy, 0]) cylinder(d1 = d0, d2 = d1, h = h, $fn = 24);
}
module gr_tacche() {
    for (v = [-1, 1]) translate([v * GR_TACCA_X, gr_bordo_alto(GR_TACCA_X) - 2, 0]) {
        translate([0, 0, -1]) gr_asola(7, 7, T + 2);
        translate([0, 0, -0.01]) gr_asola(7 + 2.4, 7, 1.2);
        translate([0, 0, T - 1.2 + 0.01]) gr_asola(7, 7 + 2.4, 1.2);
    }
    for (x = [-150 : 10 : 150]) if (abs(x) > GR_XB + 8)
        translate([x, GR_BY + GR_BD / 2 + 2.2, -1]) cylinder(d = 6, h = T + 2, $fn = 16);
}

// Pezzo con il nominativo: gancio, piastra, braccio sinistro, metà sinistra della barra. Nelle due giunzioni tiene
// la metà dietro (da 0 a 5,4 mm), con le sedi dei dadi sul retro: così si stampa con le scritte in alto e niente
// resta sospeso.
module gr_base() {
    difference() {
        union() {
            gr_gancio();
            gr_piastra();
            gr_braccio(-1);
            intersection() { gr_fascia(); translate([-100, -40, -1]) cube([100 + GR_X1, 80, T + 2]); }
            intersection() { gr_barra(); translate([-250, GR_BY - 20, -1]) cube([250 + GR_XB, 40, T + 2]); }
            // la piastra e la fascia delle spalle fanno corpo unico: si riempie il solco fra i loro smussi
            translate([-GR_PW / 2 + 4, -3, 0]) cube([GR_PW / 2 - 4 + GR_X0, GR_PY0 + 6, T]);
            translate([GR_X0 - 0.01, -3, 0]) cube([GR_PW / 2 - 4 - GR_X0, GR_PY0 + 6, MEZZO]);
        }
        // metà davanti tolta dove si appoggiano le linguette del braccio
        translate([GR_X0, -40, MEZZO]) cube([100, 40 + GR_PY0 / 2, T]);
        translate([-GR_XB, GR_BY - 20, MEZZO]) cube([100, 40, T]);
        // viti: foro di passaggio e sede esagonale del dado, sul retro
        for (p = GR_VITI) translate([p[0], p[1], -0.01]) {
            cylinder(d = FORO, h = T);
            cylinder(d = DADO / cos(30), h = DADO_H + 0.01, $fn = 6);
        }
        gr_tacche();
    }
}

// Secondo pezzo, nella posizione di montaggio: braccio destro e metà destra della barra, con due linguette che
// stanno davanti a quelle del pezzo con il nominativo. Le teste delle viti affondano nella faccia davanti.
module gr_braccio_montato() {
    difference() {
        union() {
            gr_braccio(1);
            intersection() { gr_fascia(); translate([GR_X0 + GIOCO, -40, -1]) cube([100, 80, T + 2]); }
            intersection() { gr_barra(); translate([-GR_XB + GIOCO, GR_BY - 20, -1]) cube([300, 40, T + 2]); }
        }
        // metà dietro tolta sopra le linguette del pezzo con il nominativo
        translate([-100, -40, -1]) cube([100 + GR_X1 + GIOCO, 45, MEZZO + 1]);
        translate([-100, GR_BY - 20, -1]) cube([100 + GR_XB + GIOCO, 40, MEZZO + 1]);
        for (p = GR_VITI) translate([p[0], p[1], 0]) {
            translate([0, 0, MEZZO - 1]) cylinder(d = FORO, h = T);
            translate([0, 0, T - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.01);
        }
        gr_tacche();
    }
}
// Per la stampa il braccio è capovolto: la faccia davanti sta sul piano, con le linguette e le svasature.
module gr_braccio_stampa() {
    translate([0, 0, T]) rotate([0, 180, 0]) gr_braccio_montato();
}

/* ---------- Montaggio dei pezzi ---------- */

module base() {
    gr_base();
}
module testo() {
    translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) testi2d();
}

/* ---------- Ferramenta stampata: rivetti al posto di viti e dadi ---------- */

// Chi non vuole comprare viti e dadi stampa questi rivetti: entrano negli stessi fori da 4,5 mm. La testa svasata
// si appoggia nella svasatura; il gambo è tagliato in due per il lungo e in punta ha due denti che sporgono 0,4 mm
// dal foro:
// passano nel foro stringendosi e si riaprono nella sede del dado. «presa» è la distanza fra la superficie dove
// sta la testa e la parete su cui appoggerebbe il dado. Si stampano coricati, uniti da una barretta che si spezza:
// così gli strati corrono lungo il gambo. Non stringono come una vite: tengono uniti i pezzi con un po' di gioco.
R_GAMBO = 2.05; R_TESTA = 4.3; R_SPESSO = 3.0; R_TAGLIO = 2.0; R_PUNTA = 3.0;
// Dente: 0,4 mm oltre il foro; nei rivetti corti 0,25 mm, perché le gambe corte si piegano meno senza cedere
function r_dente(presa) = presa < 6.5 ? 2.5 : 2.65;
module rivetto_mezzo(presa) {                  // metà profilo: [raggio, distanza dalla testa]
    lh = presa - 0.4 + 0.15;                   // la testa affonda 0,4 mm nella svasatura; 0,15 mm di gioco
    polygon([[0, 0], [R_TESTA, 0], [R_GAMBO, R_TESTA - R_GAMBO], [R_GAMBO, lh], [r_dente(presa), lh], [r_dente(presa), lh + 0.8],
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
            translate([1.4, 0, -3]) cylinder(d = R_TAGLIO, h = 6, $fn = 24);   // il taglio comincia dentro la testa: gambe più lunghe, più elastiche
            translate([lh + R_PUNTA + 1, 0, -3]) cylinder(d = R_TAGLIO, h = 6, $fn = 24);
        }
    }
}
// «quanti» rivetti uguali, uniti da una barretta sul fianco delle teste: si taglia a filo con un tronchesino
module rivetti(presa, quanti) {
    for (i = [0 : quanti - 1]) translate([0, i * 11, 0]) rivetto(presa);
    translate([0.3, 0, 0]) cube([1.0, (quanti - 1) * 11, 0.8]);
}

if (parte == "tutto" || parte == "base" || parte == "insieme") base();
// quattro rivetti con la presa di 7,4 mm, per le due giunzioni
if (parte == "rivetti") rivetti(7.4, 4);
if (parte == "tutto" || parte == "testo" || parte == "insieme") testo();
if (parte == "braccio") gr_braccio_stampa();
if (parte == "insieme") gr_braccio_montato();
// Le viti stanno sotto la piastra, lontane dalle scritte: qui si controlla che resti così (cerchi da 10 mm).
if (parte == "controllo_viti")
    linear_extrude(1) intersection() { testi2d(); union() for (v = GR_VITI) translate(v) circle(d = 10); }
