// Gruccia per la divisa con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Oggetti grandi con il nominativo, in due pezzi uniti da viti (volontari della Protezione Civile di Genzano di
// Roma): gruccia per la divisa e gli abiti, vassoio per piatto, posate e bicchiere. Sono in due pezzi perché interi
// non entrano nel piatto di una stampante da tavolo: per esempio 250 × 210 mm la Original Prusa MK4S, 250 × 220 mm
// la CORE One, 360 × 360 mm la XL (schede su prusa3d.com, consultate il 25/11/2026). I pezzi della gruccia stanno in
// 250 × 210 mm; il pezzo più grande del vassoio chiede un piatto di almeno 250 × 250 mm. Il pezzo con le scritte
// cambia con il nominativo, il secondo è uguale per tutti. Si cambiano solo i parametri qui sotto.
// Ogni oggetto lascia libera, accanto alle scritte, una fascia per una riga con nome e cognome.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
// gruccia = gruccia larga 40 cm con la barra per i pantaloni; vassoio = vassoio a scomparti con due manici
tipo = "gruccia"; // [gruccia, vassoio]
// tutto = il pezzo con il nominativo; base e testo = lo stesso pezzo diviso per la stampa a due colori;
// braccio = secondo pezzo della gruccia (già capovolto per la stampa); modulo = secondo pezzo del vassoio;
// insieme = i due pezzi montati, solo da guardare: non si stampa così
parte = "tutto"; // [tutto, base, testo, braccio, modulo, insieme]

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
// Per la gruccia lunghezza × altezza è l'oggetto montato e lo spessore è quello del pezzo; per il vassoio sono le
// misure del pezzo con il nominativo, «spessore» è l'altezza del bordo con le scritte e le tre righe stanno in fila.
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, tratti delle lettere da 0,6 mm in su,
// rilievi alti e larghi almeno 0,5 mm. Liberation Sans Bold da 6 mm in su e Narrow Bold a 4 mm passano il controllo.
MISURE = [
    ["gruccia", [400, 188, 6, 10.8, 8.0, 31.0, 4.0, 13.0, 6.5, 0]],
    ["vassoio", [249, 250, 4, 15.0, 6.0, 120.0, 4.0, 120.0, 120.0, -188]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];

/* ---------- Viti e dadi (uguali per i due oggetti) ---------- */

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
// Gancio: occhio di 40 mm e apertura di 36 mm, per tubi appendiabiti fino a 35 mm. Un tubo ovale per armadi misura
// 30 × 15 mm (kit Emuca, articolo 7061611: scheda su emuca.com, consultata il 25/11/2026). Non c'è una misura unica:
// chi ha un tubo più grosso lo misura prima di stampare.
// Spessore 10,8 mm (54 strati da 0,2 mm): due linguette da 5,4 mm, una vite da 10 mm che non esce dal retro.
// Carico: giacca e pantaloni di una divisa, cioè qualche chilo. Con 3 kg appesi, la flessione nel gancio (sezione di
// 14 × 10,8 mm, braccio di 27 mm) dà circa 2,5 MPa, contro i 47 MPa a cui cede il PETG stampato in piano (scheda
// tecnica Prusament PETG di Prusa Polymers, consultata il 25/11/2026). È un calcolo, non una prova di carico.
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

/* ---------- Vassoio: misure (con la fonte) ---------- */

// Scomparto del piatto: largo 237 mm; lungo 217 mm sul fondo e 229 mm all'altezza del bordo, perché la parete del
// manico è inclinata di 45 gradi. Un piatto piano usa e getta «da 22 cm» misura 225 mm in alto, 165 mm alla base ed
// è alto 20 mm (Dopla Green, scheda del rivenditore office.centrolibri.it, consultata il 25/11/2026): entra con il
// bordo sopra la parete inclinata. Regola per gli altri piatti: fino a 217 mm entrano sempre; più larghi, fino a
// 235 mm, entrano se il bordo esterno è più alto, in millimetri, del diametro meno 217.
// Corsia delle posate lunga 244 mm: coltello 210-245 mm, forchetta e cucchiaio 190-210 mm (guida Lusini «Posate»,
// consultata il 24/11/2026). Scomparto del bicchiere 84 × 84 mm, per bicchieri e tazze larghi fino a 8 cm.
// Fondo 2,4 mm (12 strati), bordi alti 15 mm, parete fra i due pezzi alta 24 mm, manici alti 26 mm.
// Il vassoio porta le stoviglie e non tocca il cibo. Si lava a mano: il PETG comincia a deformarsi a 68 gradi
// (temperatura di inflessione sotto carico, scheda tecnica Prusament PETG, consultata il 25/11/2026).
V_LARGO = 250; V_FONDO = 2.4; V_BORDO_H = 15; V_BORDO = 3; V_DIETRO = 10;
V_R = 4; V_RI = 6;                             // raggi degli angoli in fondo: fuori e dentro
V_GA = 4; V_GB = 8; V_GH = 24;                 // pareti di giunzione dei due pezzi e loro altezza
V_PIANO_A = 217;                               // fondo piano dello scomparto del piatto
V_POSATE = 52; V_DIV = 2; V_BICCHIERE = 84;    // corsia delle posate, divisori bassi, scomparto del bicchiere
V_DIV_H = 8.4;                                 // altezza dei divisori bassi (6 mm sopra il fondo)
V_MAN_H = 26; V_MAN_S = 5; V_MAN_L = 120;      // manico: altezza, spessore in orizzontale, larghezza alla base
V_VITE_Z = 9.5; V_VITI_Y = [-85, 0, 85];       // viti della giunzione: altezza da terra e posizioni
V_NOME_X = [-160, -98];                        // fascia libera per nome e cognome, sul bordo dietro
V_ENTE_X = -50.2;                              // centro della riga con l'ente: finisce 6 mm prima della giunzione

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

// Gruccia: nominativo, fascia libera per nome e cognome, poi l'ente su due righe.
// Vassoio: tutto su una riga lungo il bordo dietro: nominativo, fascia libera, poi l'ente per intero (a 4 mm
// «PROTEZIONE CIVILE GENZANO DI ROMA» è lungo 88 mm).
module testi2d() {
    translate([TX, Y1]) nominativo2d(S1);
    if (tipo == "vassoio") riga(str(riga2, riga2 != "" && riga3 != "" ? " " : "", riga3), V_ENTE_X, Y2);
    else {
        if (riga2 != "") riga(riga2, TX, Y2);
        if (riga3 != "") riga(riga3, TX, Y3);
    }
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

/* ---------- Vassoio ---------- */

// Ogni pezzo è mezzo vassoio: la giunzione sta sul piano x = 0, il fondo va verso le x negative e finisce con una
// parete inclinata di 45 gradi, che sopra il bordo prosegue e fa da manico: le dita entrano sotto, il pollice sta
// sopra. Inclinata così la parete si stampa senza supporti, e il bordo rialzato del piatto le passa sopra.
function v_xi(xb, z) = xb - (z - V_FONDO);       // faccia interna della parete inclinata, alla quota z
function v_xo(xb, z) = v_xi(xb, z) - V_MAN_S;    // faccia esterna

// Rettangolo da x0 a x1: angoli arrotondati in fondo (x0), vivi sulla giunzione (x1)
module v_pianta(x0, x1, y0, y1, r) {
    hull() {
        translate([x0 + r, y0 + r]) circle(r);
        translate([x0 + r, y1 - r]) circle(r);
        translate([x1 - 0.01, y0]) square([0.01, y1 - y0]);
    }
}

module v_manico(xb) {
    z0 = V_BORDO_H - 0.01; z1 = V_MAN_H; zs = z1 - 6;       // in cima il manico è largo 11 mm: ci sta il pollice
    intersection() {
        translate([0, V_MAN_L / 2, 0]) rotate([90, 0, 0]) linear_extrude(V_MAN_L)
            polygon([[v_xo(xb, z0), z0], [v_xo(xb, z1), z1], [v_xi(xb, zs), z1], [v_xi(xb, zs), zs], [v_xi(xb, z0), z0]]);
        // i fianchi del manico salgono a 45 gradi verso il centro
        hull() {
            translate([-500, -V_MAN_L / 2, z0]) cube([500, V_MAN_L, 0.01]);
            translate([-500, -V_MAN_L / 2 + (z1 - z0), z1]) cube([500, V_MAN_L - 2 * (z1 - z0), 0.01]);
        }
    }
}

// piano = lunghezza del fondo piano; pg = spessore della parete di giunzione; dietro = spessore del bordo dietro
module v_meta(piano, pg, dietro) {
    xb = -(pg + piano);
    ya = -V_LARGO / 2; yb = V_LARGO / 2;
    zs = V_BORDO_H - 1.5; c = 1.5;
    difference() {
        union() {
            // guscio: fondo, bordi e parete inclinata; sotto i lati lunghi uno smusso di 1,5 mm
            hull() {
                linear_extrude(0.01) v_pianta(v_xo(xb, 0), 0, ya + c, yb - c, V_R);
                translate([0, 0, c]) linear_extrude(0.01) v_pianta(v_xo(xb, c), 0, ya, yb, V_R);
                translate([0, 0, V_BORDO_H - 0.01]) linear_extrude(0.01) v_pianta(v_xo(xb, V_BORDO_H), 0, ya, yb, V_R);
            }
            // parete di giunzione, più alta dei bordi: fa da divisorio
            translate([-pg, ya, c]) cube([pg, V_LARGO, V_GH - c]);
            v_manico(xb);
        }
        // vano
        hull() {
            translate([0, 0, V_FONDO]) linear_extrude(0.01) v_pianta(v_xi(xb, V_FONDO), -pg, ya + V_BORDO, yb - dietro, V_RI);
            translate([0, 0, zs]) linear_extrude(0.01) v_pianta(v_xi(xb, zs), -pg, ya + V_BORDO, yb - dietro, V_RI);
        }
        translate([0, 0, zs - 0.01]) linear_extrude(V_GH) v_pianta(v_xi(xb, zs), -pg, ya + V_BORDO, yb - dietro, V_RI);
    }
}

// Pezzo con il nominativo: scomparto del piatto. Il bordo dietro è largo 10 mm e porta le scritte sulla faccia in
// alto; nella parete di giunzione passano tre viti, con la testa svasata dal lato del piatto.
module v_base() {
    difference() {
        v_meta(V_PIANO_A, V_GA, V_DIETRO);
        for (y = V_VITI_Y) translate([0, y, V_VITE_Z]) rotate([0, -90, 0]) {
            translate([0, 0, -0.01]) cylinder(d = FORO, h = V_GA + 0.02);
            translate([0, 0, V_GA - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.02);
        }
    }
}

// Secondo pezzo: corsia delle posate, scomparto del bicchiere e spazio per pane o tovagliolo. La parete di
// giunzione è spessa 8 mm: dentro ha tre asole aperte in alto, dove si lasciano cadere i dadi, e tre fori ciechi per
// le viti, che non sbucano dal lato delle posate.
module v_modulo() {
    piano = V_POSATE + V_DIV + V_BICCHIERE;
    xb = -(V_GB + piano);
    xd = -(V_GB + V_POSATE);                                // divisorio fra posate e bicchiere
    yb = V_LARGO / 2 - V_BORDO;
    mirror([1, 0, 0]) difference() {
        union() {
            v_meta(piano, V_GB, V_BORDO);
            translate([xd - V_DIV, -yb - 0.01, V_FONDO - 0.01]) cube([V_DIV, 2 * yb + 0.02, V_DIV_H - V_FONDO]);
            // chiusura dello scomparto del bicchiere: segue la parete inclinata
            translate([0, yb - V_BICCHIERE, 0]) rotate([90, 0, 0]) linear_extrude(V_DIV)
                polygon([[xd - V_DIV + 0.01, V_FONDO - 0.01], [xd - V_DIV + 0.01, V_DIV_H],
                         [v_xi(xb, V_DIV_H) - 2, V_DIV_H], [v_xi(xb, V_FONDO) - 2, V_FONDO - 0.01]]);
        }
        for (y = V_VITI_Y) {
            // foro cieco della vite: 7 mm, resta 1 mm di parete dal lato delle posate
            translate([0.01, y, V_VITE_Z]) rotate([0, -90, 0]) cylinder(d = FORO, h = 7.01);
            // asola del dado, con il fondo a V che lo tiene all'altezza della vite
            hull() for (z = [V_VITE_Z, V_GH + 6]) translate([-2 - DADO_H, y, z]) rotate([0, 90, 0])
                cylinder(d = DADO / cos(30), h = DADO_H, $fn = 6);
        }
    }
}

/* ---------- Montaggio dei pezzi ---------- */

module base() {
    if (tipo == "gruccia") gr_base(); else v_base();
}
module testo() {
    translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) testi2d();
}

if (parte == "tutto" || parte == "base" || parte == "insieme") base();
if (parte == "tutto" || parte == "testo" || parte == "insieme") testo();
if (parte == "braccio") gr_braccio_stampa();
if (parte == "modulo") v_modulo();
if (parte == "insieme") { if (tipo == "gruccia") gr_braccio_montato(); else v_modulo(); }
