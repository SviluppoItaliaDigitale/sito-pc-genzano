// Vassoio porta piatto, bicchiere e posate con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Vassoio porta piatto, bicchiere e posate con il nominativo (volontari della Protezione Civile di Genzano di Roma).
// Il piatto e il bicchiere si infilano in due fori più stretti del loro bordo: restano appesi e non scivolano.
// La bottiglietta d'acqua da mezzo litro scende in un pozzetto. Vicino a ogni posto una scritta appena incisa dice
// che cosa ci va. Le posate stanno sotto una clip a molla. Il vassoio è rialzato su dodici piedini, perché piatto e bicchiere
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
// sinistra3, centro3, destra3 = terza versione, con le sedi sagomate: si stampa diritta, con il fondo sul piatto;
// montato3 = terza versione montata, solo da guardare
parte = "tutto"; // [tutto, base, testo, sinistra, centro, destra, sinistra180, centro180, clip, montato, sinistra3, centro3, destra3, montato3, sinistra_i, centro_i, destra_i, sinistra180_i, centro180_i, sinistra3_i, centro3_i, destra3_i, farfalle, farfalle3, provino, rivetti_targhetta, rivetti_targhetta3, controllo_viti]
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
// consultate il 25/11/2026). Il foro del piatto è di 180 mm nella versione principale (dal 25/11/2026, richiesta di
// Alessandro: il piatto non deve poter cadere dal vassoio) e di 200 mm nella versione per soli piatti rigidi: più
// stretto del bordo dei due piatti (che quindi non passano) e più largo della loro base (che quindi scende nel foro).
// Con il foro da 180 mm un piatto con il bordo sotto i 185 mm cade; con quello da 200 mm, sotto i 205 mm.
// Bicchiere usa e getta da 200 ml: 70 mm alla bocca (scheda tecnica Euronda Monoart mod. 80, rev. 11/2024), 46 mm
// alla base e 70 mm alla bocca, alto 97 mm (bicchieri in polipropilene Semadeni, scheda su avantorsciences.com);
// fonti consultate il 25/11/2026. Il foro del bicchiere è di 56 mm: il bicchiere scende di circa 40 mm e si
// ferma. Un bicchiere con la base più larga di 56 mm non entra: si appoggia sul piano.
// Piedini: il piano sta a 48 mm dal tavolo, 6 mm più di quanto scende quel bicchiere (42 mm, contando lo smusso).
// Il PETG comincia a deformarsi a 68 gradi (temperatura di inflessione sotto carico, scheda tecnica Prusament PETG
// di Prusa Polymers, consultata il 25/11/2026): niente stoviglie o bevande bollenti.
// Versione principale (foro da 180 mm): il piatto appoggia più in basso, sulla parete, e sotto il bordo restano
// 22 mm di vassoio per parte con il piatto piano e 20 mm con il fondo (con il foro da 200 mm sono 12 e 10 mm).
// La base dei due piatti (165 e 145 mm) entra comunque. Per piatti leggeri, pieni o molli è la più sicura.
// Bottiglietta d'acqua da mezzo litro: tonda, 68 mm di diametro, alta 172,5 mm (bottiglia rPET da 500 ml, scheda
// del produttore su berlinpackaging.eu, consultata il 25/11/2026). Il pozzetto è largo 70 mm e profondo 44 mm: la
// bottiglia scende di circa 35 mm e si ferma su un cono che in fondo lascia un'apertura di 54 mm. Una bottiglia
// più larga di 70 mm non entra; una più stretta di 55 mm cadrebbe.
BOTT = 70; B_PROF = 44; B_CONO = 9; B_FONDO = 54;
STRETTO = parte == "montato" || parte == "sinistra180" || parte == "centro180" || parte == "sinistra180_i" || parte == "centro180_i";
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
// Le sedi dei dadi sono larghe 7,5 mm: un foro stampato esce un po' più stretto del disegno.
FORO = 4.5; SVASO_D = 9.4; SVASO_H = 2.45; DADO = 7.5; DADO_H = 3.4;

/* ---------- Pianta (vista da sopra, vassoio in uso) ---------- */

LARGO = 456; FONDO = 240;                      // ingombro del vassoio montato
G1 = 148; G2 = 328;                            // giunzioni: sinistra | centro | destra
PX = 148;                                      // centro del piatto: la prima giunzione taglia il foro a metà
CX = 381; CY = 78;                             // centro del bicchiere
BX = 381; BY = -8;                             // centro della bottiglietta
NX = 381; NY = -84;                            // centro della targhetta
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
// Davanti a ogni testa di vite restano almeno 25 mm liberi per la chiave: per questo il secondo piedino sta a x = 105
PIEDI = [[22, 98], [105, 109], [168, 109], [312, 107], [340, 110], [434, 98]];

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
    if (i == 4) translate([BX, BY]) circle(d = BOTT + 2 * extra, $fn = 120);
    if (i == 2 || i == 3) hull() for (v = [-1, 1]) translate([MAN_X[i - 2], v * (MAN_L - MAN_W) / 2]) circle(d = MAN_W + 2 * extra, $fn = 48);
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
    anello2d([BX, BY], BOTT, 2.6);
    difference() { manici2d(SM + 3.2); manici2d(SM - 0.01); }                       // bordo delle asole dei manici
    translate([NERV_X, -FONDO / 2]) square([2.4, FONDO]);                           // fra il piatto e le posate
    for (y = [-75, 25]) translate([NERV_X, y - 1.2]) square([G2 - NERV_X, 2.4]);    // sotto la corsia delle posate
    for (y = [38, -57]) translate([G2, y - 1.2]) square([MAN_X[1] - MAN_W / 2 - G2, 2.4]);   // pezzo di destra
}
// Scritte incise di 0,4 mm sulla faccia del piano, accanto a ogni posto: si vedono appena e dicono che cosa ci va
INCISO = 0.4;
module etichetta(t, p) { translate(p) text(t, size = 5, font = font2, halign = "center", valign = "center"); }
module etichette2d() {
    etichetta("PIATTO", [95, -104]);
    etichetta("POSATE", [POS_X, -106]);
    etichetta("BICCHIERE", [CX, 38.5]);
    etichetta("BOTTIGLIA", [BX, -51.5]);
}
// parete di giunzione: da y0 a y1, spessa s, con il lato sulla giunzione g (verso = -1 a sinistra, 1 a destra)
module parete(g, verso, s, y0, y1) {
    translate([verso < 0 ? g - s : g, y0, PIANO - 0.01]) cube([s, y1 - y0, FLANGIA - PIANO]);
}
module piede(p) {
    translate([p[0], p[1], PIANO - 0.01]) cylinder(d1 = 20, d2 = 13, h = PIEDE - PIANO, $fn = 48);
}
/* ---------- Giunzioni senza viti: pezzi «a incastro» con chiavette a farfalla ---------- */

// Chi non vuole viti e dadi stampa i pezzi «a incastro» (parti che finiscono per _i): al posto di fori e sedi dei
// dadi hanno, a cavallo di ogni giunzione, sedi a coda di rondine alte quanto la parete. In ogni sede si preme una
// chiavetta a farfalla: collo largo 6 mm, ali larghe 12 mm, lunga 14 mm. Lavora a trazione per tutta l'altezza,
// quindi tiene sia quando il vassoio si porta dai manici sia quando si prende dal centro. Sulle facce inclinate ha
// otto cordoncini che sporgono 0,3 mm: nella sede (0,2 mm di gioco) si schiacciano e la tengono ferma. Il gioco e i
// cordoncini sono ipotesi di progetto: il provino (parte «provino») serve a provarli sulla propria stampante.
// Un dente a V lungo la giunzione (sporge 1,8 mm, facce a più di 45 gradi, quindi si stampa senza supporti) entra
// in una gola del pezzo accanto e impedisce ai pezzi di scorrere in altezza uno sull'altro.
// Le sedi e i pezzi pieni intorno prendono il posto delle viti: i pezzi a incastro non hanno fori per le viti.
// Alla seconda giunzione restano anche le due costole di allineamento dei pezzi con le viti.
INC_PARTI = ["sinistra_i", "centro_i", "destra_i", "sinistra180_i", "centro180_i", "sinistra3_i", "centro3_i",
             "destra3_i", "interferenze", "interferenze3"];
INC = len([for (q = INC_PARTI) if (q == parte) 1]) > 0;
K_L = 14; K_COLLO = 6; K_ALA = 12; K_GIOCO = 0.2; K_BORDO = 3;
KY1 = 110; KY2 = [-85, 0, 85];                 // chiavette della prima e della seconda giunzione
D_SPORGE = 1.8; D_MEZZA = 2.2;                 // dente a V: sporgenza e mezza altezza
module chiave2d(e = 0) {
    offset(delta = e) polygon([[-K_L / 2, -K_ALA / 2], [0, -K_COLLO / 2], [K_L / 2, -K_ALA / 2],
                               [K_L / 2, K_ALA / 2], [0, K_COLLO / 2], [-K_L / 2, K_ALA / 2]]);
}
// La chiavetta come si stampa: in piedi, così gli strati hanno la forma della farfalla e la trazione corre dentro
// ogni strato. «testa» è lo spessore di una base più larga, che resta fuori dalla sede: fa da battuta e da presa.
module chiavetta(alta, testa = 0) {
    translate([0, 0, testa]) {
        linear_extrude(alta - 3) {
            chiave2d();
            for (sx = [-1, 1], sy = [-1, 1], t = [0.3, 0.75])
                translate([sx * t * K_L / 2, sy * (K_COLLO / 2 + t * (K_ALA - K_COLLO) / 2)]) circle(r = 0.3, $fn = 12);
        }
        // invito: negli ultimi 3 mm la chiavetta si restringe a gradini, fino a 0,45 mm per parte
        for (i = [0:2]) translate([0, 0, alta - 3.01 + i]) linear_extrude(1.01) chiave2d(-0.15 * (i + 1));
    }
    // la base ha una linguetta che sporge 3 mm dall'ingrossamento della parete: da lì si fa leva per toglierla
    if (testa > 0) linear_extrude(testa) { offset(r = 2, $fn = 24) chiave2d(); translate([-13, -4]) square([6, 8]); }
}
module sede_chiave(g, y, z0, alta) { translate([g, y, z0]) linear_extrude(alta) chiave2d(K_GIOCO); }
module rinforzo(g, y, z0, alta) {
    translate([g - K_L / 2 - K_BORDO, y - K_ALA / 2 - K_BORDO, z0]) cube([K_L + 2 * K_BORDO, K_ALA + 2 * K_BORDO, alta]);
}
// dente a V sulla faccia di giunzione, sporge verso sinistra; «e» allarga la gola del pezzo accanto
module dente(g, tratti, zc, e = 0) {
    for (t = tratti) translate([g, t[0] - e, zc]) rotate([-90, 0, 0]) linear_extrude(t[1] - t[0] + 2 * e)
        polygon([[0.01, -D_MEZZA - 1.3 * e], [-D_SPORGE - e, 0], [0.01, D_MEZZA + 1.3 * e]]);
}
// tratti del dente: stanno lontani 5,5 mm dal centro di ogni chiavetta, per non entrare nelle sedi
function tratti1(ys) = [[ys + 1.4, KY1 - 5.5], [KY1 + 5.5, 118.4], [-KY1 + 5.5, -ys - 1.4], [-118.4, -KY1 - 5.5]];
TRATTI2 = [[-118, -90.5], [-79.5, -5.5], [5.5, 79.5], [90.5, 118]];
D_Z = 14.5; D_Z3 = 8;                          // quota del dente nei due vassoi
// Tutto il vassoio pieno, senza i tagli delle giunzioni
module corpo() {
    if (INC) {
        for (v = [-1, 1]) rinforzo(G1, v * KY1, PIANO - 0.01, FLANGIA - PIANO);
        for (y = KY2) rinforzo(G2, y, PIANO - 0.01, FLANGIA - PIANO);
    }
    linear_extrude(PIANO) contorno2d();
    translate([0, 0, PIANO - 0.01]) linear_extrude(NERV - PIANO) nervature2d();
    for (p = PIEDI, v = [-1, 1]) piede([p[0], v * p[1]]);
    translate([BX, BY, PIANO - 0.01]) cylinder(d = BOTT + 4.8, h = B_PROF - PIANO, $fn = 120);   // pozzetto della bottiglia
    // sedi dei dadi della targhetta
    for (p = T_VITI) translate([NX + p[0], NY + p[1], PIANO - 0.01]) cylinder(d = 15, h = 4, $fn = 48);
}
module scavi() {
    // fori di piatto e bicchiere, con lo smusso dal lato delle stoviglie
    translate([0, 0, -1]) linear_extrude(PIEDE) { fori2d(); manici2d(); }
    // lo smusso si fa foro per foro: un solo inviluppo li unirebbe tutti
    translate([0, 0, -0.01]) linear_extrude(INCISO + 0.01) etichette2d();
    // pezzi a incastro: sedi delle chiavette, alte quanto la parete e chiuse dal piano
    if (INC) {
        for (v = [-1, 1]) sede_chiave(G1, v * KY1, PIANO, FLANGIA);
        for (y = KY2) sede_chiave(G2, y, PIANO, FLANGIA);
    }
    // pozzetto della bottiglia: diritto, poi un cono su cui la bottiglia si ferma, poi aperto
    translate([BX, BY, 0]) {
        translate([0, 0, -1]) cylinder(d = BOTT, h = B_PROF - B_CONO + 1, $fn = 120);
        translate([0, 0, B_PROF - B_CONO - 0.01]) cylinder(d1 = BOTT, d2 = B_FONDO, h = B_CONO + 0.02, $fn = 120);
        cylinder(d = B_FONDO, h = PIEDE, $fn = 120);
    }
    for (i = [0:4]) hull() {
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
module viti_teste(g, viti, vz = VITE_Z) {    // nel pezzo a sinistra della giunzione
    for (y = viti) translate([g, y, vz]) rotate([0, -90, 0]) {
        translate([0, 0, -0.01]) cylinder(d = FORO, h = FL_A + 0.02, $fn = 32);
        translate([0, 0, FL_A - SVASO_H]) cylinder(d1 = FORO, d2 = SVASO_D, h = SVASO_H + 0.02, $fn = 32);
    }
}
module viti_dadi(g, viti, vz = VITE_Z, fine = FLANGIA + 6) {   // nel pezzo a destra della giunzione
    for (y = viti) {
        translate([g - 0.01, y, vz]) rotate([0, 90, 0]) cylinder(d = FORO, h = 7.6, $fn = 32);
        hull() for (z = [vz, fine]) translate([g + 2, y, z]) rotate([0, 90, 0])
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
        if (INC) dente(G1, tratti1(Y1A), D_Z, 0.2);
        else { viti_teste(G1, VITI_1); costole(G1, COST_1, 0.2); }
    }
}
module pezzo_centro() {
    difference() {
        union() {
            intersection() { corpo(); translate([G1, -200, -1]) cube([G2 - G1, 400, 100]); }
            for (v = [-1, 1]) parete(G1, 1, FL_B, v > 0 ? Y1A : -FONDO / 2, v > 0 ? FONDO / 2 : -Y1A);
            parete(G2, -1, FL_A, -FONDO / 2, FONDO / 2);
            if (INC) dente(G1, tratti1(Y1A), D_Z);
            else intersection() { costole(G1, COST_1); translate([G1 - 5, -200, 0]) cube([5, 400, 100]); }
        }
        scavi();
        if (INC) dente(G2, TRATTI2, D_Z, 0.2);
        else { viti_dadi(G1, VITI_1); viti_teste(G2, VITI_2); }
        costole(G2, COST_2, 0.2);
    }
}
module pezzo_destra() {
    difference() {
        union() {
            intersection() { corpo(); translate([G2, -200, -1]) cube([LARGO - G2 + 1, 400, 100]); }
            parete(G2, 1, FL_B, -FONDO / 2, FONDO / 2);
            intersection() { costole(G2, COST_2); translate([G2 - 5, -200, 0]) cube([5, 400, 100]); }
            if (INC) dente(G2, TRATTI2, D_Z);
        }
        scavi();
        if (!INC) viti_dadi(G2, VITI_2);
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

/* ---------- Terza versione: sedi sagomate ---------- */

// Qui le stoviglie non restano appese: appoggiano sul fondo, dentro sedi con la loro forma. Il piatto sta in una
// conca chiusa da un anello alto 8 mm, che si allarga più della parete del piatto (così il piatto tocca il fondo e
// non l'anello): base fino a 166 mm. Il bicchiere scende in un bicchierino alto 45 mm, circa metà dei 97 mm del
// bicchiere, così resta facile da prendere: 49 mm in basso, 61 mm in alto. La bottiglietta sta in un anello largo
// 70 mm e alto 45 mm. Le posate appoggiano su due ponticelli alti 9 mm e la clip si aggancia a uno dei due.
// Il vassoio non ha piedini: si stampa diritto, con il fondo sul piatto della stampante, e per prenderlo dal tavolo
// i due lati corti salgono inclinati verso l'esterno. Coordinate vere: z verso l'alto, z = 0 è il tavolo.
W3 = 420; D3 = 240;                            // fondo del vassoio (in alto, con i due bordi inclinati, è largo 454)
F3 = 2.4; H3 = 18; LAB = 17; MURO = 2.4;       // fondo, altezza dei bordi, sporgenza dei bordi inclinati, pareti
J1 = 115; J2 = 296;                            // giunzioni
P3 = [115, 0];                                 // centro del piatto
A_R = 84; A_H = 8; A_PEND = 1.6; A_S = 2.4;    // anello del piatto: raggio interno in basso, altezza, pendenza, spessore
A_FUORI = A_R + A_PEND * A_H + A_S;
C3 = [360, 75]; B3 = [360, -6]; N3 = [360, -80];   // bicchiere, bottiglietta, targhetta
BIC_H = 45; BIC_D1 = 49; BIC_D2 = 61;
POS3_X = 253; CLIP3_Y = [-35, 45];             // corsia delle posate e i due ponticelli
PONTE = 9;                                     // altezza dei ponticelli: 3 mm di tetto, sotto il dente della clip
N_ALTO = 10.6;                                 // altezza degli appoggi della targhetta: la vite M4 × 10 si ferma
                                               // a 4 mm dal tavolo, anche con una testa che affonda un po' di più
V3_Z = 10;                                     // quota delle viti di giunzione
Y3A = A_FUORI + 1.3;                           // la prima giunzione passa per il piatto: le pareti stanno fuori dall'anello
V3_1 = [-109, 109]; V3_2 = [-85, 0, 85];
module xz(t) { rotate([90, 0, 0]) linear_extrude(t) children(); }
module vasca3() {
    translate([0, -D3 / 2, 0]) cube([W3, D3, F3]);
    // bordi lunghi, diritti, e bordi corti inclinati: sotto ci passano le dita
    for (y = [D3 / 2, -D3 / 2 + MURO]) translate([0, y, 0]) xz(MURO) polygon([[0, 0], [W3, 0], [W3 + LAB, H3], [-LAB, H3]]);
    translate([0, D3 / 2, 0]) xz(D3) {
        polygon([[0, 0], [3.4, 0], [3.4 - LAB, H3], [-LAB, H3]]);
        polygon([[W3, 0], [W3 - 3.4, 0], [W3 + LAB - 3.4, H3], [W3 + LAB, H3]]);
    }
    translate([P3[0], P3[1], F3 - 0.01]) rotate_extrude($fn = 180)
        polygon([[A_R, 0], [A_R + A_PEND * A_H, A_H], [A_FUORI, A_H], [A_FUORI, 0]]);
    translate([C3[0], C3[1], F3 - 0.01]) cylinder(d1 = BIC_D1 + 4, d2 = BIC_D2 + 4, h = BIC_H, $fn = 120);
    translate([B3[0], B3[1], F3 - 0.01]) cylinder(d = BOTT + 4.8, h = 45, $fn = 120);
    // pareti di giunzione
    for (v = [-1, 1]) {
        translate([J1 - FL_A, v > 0 ? Y3A : -D3 / 2 + 1, F3 - 0.01]) cube([FL_A + FL_B, D3 / 2 - 1 - Y3A, H3 - F3]);
    }
    translate([J2 - FL_A, -D3 / 2 + 1, F3 - 0.01]) cube([FL_A + FL_B, D3 - 2, H3 - F3]);
    if (INC) {
        for (v = [-1, 1]) rinforzo(J1, v * KY1, F3 - 0.01, H3 - F3);
        for (y = KY2) rinforzo(J2, y, F3 - 0.01, H3 - F3);
    }
    // ponticelli delle posate
    for (y = CLIP3_Y) translate([POS3_X - 33, y - 9.2, F3 - 0.01]) cube([66, 18.4, PONTE - F3]);
    // appoggi della targhetta: due con il dado, due semplici
    for (p = T_VITI) {
        translate([N3[0] + p[0] - 7.5, N3[1] + p[1] - 6.5, F3 - 0.01]) cube([15, 13, N_ALTO - F3]);
        translate([N3[0] + p[0], N3[1] + 14, F3 - 0.01]) cylinder(d = 10, h = N_ALTO - F3, $fn = 48);
    }
}
module etichette3() {
    etichetta("PIATTO", [30, -100]);
    etichetta("POSATE", [POS3_X, -106]);
    // bicchiere e bottiglietta: sul fondo della loro sede, perché fra due sedi alte la scritta non si vedrebbe
    etichetta("BICCHIERE", C3);
    etichetta("BOTTIGLIA", B3);
}
// Le pareti della prima giunzione stanno sotto il bordo del piatto: il loro spigolo interno è tagliato lungo una
// linea parallela alla parete del piatto piano (base 165 mm, bordo 225 mm, alto 20 mm, presa diritta fra base e
// bordo: è un'ipotesi, il profilo vero non è nella scheda del produttore), 2,5 mm più in basso.
function sotto_il_piatto(y) = F3 + (y - 82.5) / 1.5 - 2.5;
module scavi3() {
    for (v = [0, 1]) mirror([0, v, 0]) translate([J1 - (INC ? 11 : FL_A + 1), 0, 0]) rotate([90, 0, 90]) linear_extrude(INC ? 22 : FL_A + FL_B + 2)
        polygon([[Y3A - 1, sotto_il_piatto(Y3A - 1)], [113, sotto_il_piatto(113)], [113, 30], [Y3A - 1, 30]]);
    // pezzi a incastro: sedi delle chiavette, aperte in alto, e sotto ognuna un foro da 3,2 mm nel fondo per
    // spingerla fuori; con la chiavetta al suo posto il foro è chiuso
    if (INC) for (c = concat([for (v = [-1, 1]) [J1, v * KY1]], [for (y = KY2) [J2, y]])) {
        sede_chiave(c[0], c[1], F3, H3);
        translate([c[0] - 3.5, c[1], -1]) cylinder(d = 3.2, h = F3 + 1.5, $fn = 24);
    }
    translate([0, 0, F3 - INCISO]) linear_extrude(1) etichette3();
    translate([C3[0], C3[1], F3]) cylinder(d1 = BIC_D1, d2 = BIC_D2 + 0.02, h = BIC_H + 0.02, $fn = 120);
    translate([B3[0], B3[1], F3]) cylinder(d = BOTT, h = 50, $fn = 120);
    // Fessure della clip: un pozzetto per la gamba e, verso l'esterno, la tasca dove aggancia il dente. La tasca
    // esce dal fianco del ponticello con una finestrella alta 2,8 mm: da lì, con un cacciavite piccolo, si spinge
    // il dente per togliere la clip. Il fondo della tasca è rialzato di 1,2 mm e segue il dente, che è smussato.
    // Sopra il dente restano 0,65 mm: il tetto della tasca è un ponte di 10 mm, che in stampa può calare un po'.
    for (y = CLIP3_Y, v = [-1, 1]) translate([POS3_X + v * POS_L / 2, y, 0]) {
        translate([-FESSURA / 2, -5.2, F3]) cube([FESSURA, 10.4, PONTE]);
        translate([v > 0 ? FESSURA / 2 - 0.01 : -FESSURA / 2 - 0.5, -5.2, F3]) cube([0.51, 10.4, PONTE - PIANO - F3 + 0.4]);
        translate([v > 0 ? FESSURA / 2 + 0.49 : -FESSURA / 2 - 0.49 - 6, -5.2, F3 + 1.2]) cube([6, 10.4, PONTE - PIANO - F3 - 0.8]);
    }
    // viti della targhetta: il dado entra di lato in un canale a T, sotto 2 mm di tetto
    for (p = T_VITI) translate([N3[0] + p[0], N3[1] + p[1], 0]) {
        v = p[0] > 0 ? 1 : -1;
        translate([0, 0, F3 + 0.2]) cylinder(d = FORO, h = 20, $fn = 32);
        translate([v > 0 ? -DADO / 2 - 0.8 : -8, -DADO / 2, N_ALTO - 2 - DADO_H]) cube([8 + DADO / 2 + 0.8, DADO, DADO_H]);
        translate([v > 0 ? -DADO / 2 - 0.8 : -8, -FORO / 2, N_ALTO - 2 - 0.01]) cube([8 + DADO / 2 + 0.8, FORO, 3]);
    }
}
module costole3(gioco = 0) {
    for (y = COST_2) translate([J2, y, F3 - 0.01]) cylinder(r = 1.5 + gioco, h = H3 - F3 + (gioco > 0 ? 1 : 0), $fn = 24);
}
module sinistra3() {
    difference() {
        intersection() { vasca3(); translate([-50, -200, -1]) cube([J1 + 50, 400, 100]); }
        scavi3();
        if (INC) dente(J1, tratti1(Y3A), D_Z3, 0.2);
        else viti_teste(J1, V3_1, V3_Z);
    }
}
module centro3() {
    difference() {
        union() {
            intersection() { vasca3(); translate([J1, -200, -1]) cube([J2 - J1, 400, 100]); }
            if (INC) dente(J1, tratti1(Y3A), D_Z3);
        }
        scavi3();
        if (INC) dente(J2, TRATTI2, D_Z3, 0.2);
        else { viti_dadi(J1, V3_1, V3_Z, H3 + 6); viti_teste(J2, V3_2, V3_Z); }
        costole3(0.2);
    }
}
module destra3() {
    difference() {
        union() {
            intersection() { vasca3(); translate([J2, -200, -1]) cube([W3, 400, 100]); }
            intersection() { costole3(); translate([J2 - 5, -200, 0]) cube([5, 400, 100]); }
            if (INC) dente(J2, TRATTI2, D_Z3);
        }
        scavi3();
        if (!INC) viti_dadi(J2, V3_2, V3_Z, H3 + 6);
    }
}
module montato3() {
    translate([-N3[0], -N3[1], -N_ALTO]) {
        sinistra3(); centro3(); destra3();
        translate([POS3_X, CLIP3_Y[0] + C_LARGA / 2, PONTE]) rotate([90, 0, 0]) clip();
    }
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
if (parte == "sinistra" || parte == "sinistra180" || parte == "sinistra_i" || parte == "sinistra180_i") per_la_stampa() pezzo_sinistra();
if (parte == "centro" || parte == "centro180" || parte == "centro_i" || parte == "centro180_i") per_la_stampa() pezzo_centro();
if (parte == "destra" || parte == "destra_i") per_la_stampa() pezzo_destra();
if (parte == "clip") clip();
if (parte == "montato") montato();
if (parte == "sinistra3" || parte == "sinistra3_i") sinistra3();
if (parte == "centro3" || parte == "centro3_i") centro3();
if (parte == "destra3" || parte == "destra3_i") destra3();
if (parte == "montato3") montato3();
// chiavette delle giunzioni e rivetti della targhetta (7,2 mm sul vassoio con i piedini, 5,6 mm su quello sagomato)
// Chiavette: cinque con la base per il vassoio con i piedini (si premono da sotto); per quello sagomato due basse,
// per la giunzione sotto il bordo del piatto, e tre alte, che si premono dall'alto
K_ALTA = FLANGIA - PIANO - 0.4; K3_BASSA = 11.0; K3_ALTA = H3 - F3 - 0.4;
// Una barretta bassa le tiene unite in stampa (più stabili sul piatto): si taglia a filo. Sta dal lato che resta fuori.
if (parte == "farfalle") { for (i = [0:4]) translate([i * 22, 0, 0]) chiavetta(K_ALTA, 3); translate([0, -0.5, 0]) cube([88, 1, 0.6]); }
if (parte == "farfalle3") { for (i = [0:4]) translate([i * 18, 0, 0]) chiavetta(i < 2 ? K3_BASSA : K3_ALTA); translate([0, -0.5, 0]) cube([72, 1, 0.6]); }
// Provino: un blocchetto con una sede e una chiavetta alta 9 mm, per provare l'incastro prima di stampare il vassoio
if (parte == "provino") {
    difference() { rinforzo(0, 0, 0, 10); sede_chiave(0, 0, 1, 10); }
    translate([22, 0, 0]) chiavetta(8.8);
    translate([9, -0.5, 0]) cube([8, 1, 0.6]);
}
// Controlli: i pezzi a incastro montati con le chiavette non devono compenetrarsi (queste parti devono uscire vuote)
if (parte == "interferenze") {
    intersection() { pezzo_sinistra(); pezzo_centro(); }
    intersection() { pezzo_centro(); pezzo_destra(); }
    intersection() {
        union() { pezzo_sinistra(); pezzo_centro(); pezzo_destra(); }
        union() { for (v = [-1, 1]) translate([G1, v * KY1, PIANO + 0.2]) linear_extrude(K_ALTA) chiave2d();
                  for (y = KY2) translate([G2, y, PIANO + 0.2]) linear_extrude(K_ALTA) chiave2d(); }
    }
}
if (parte == "interferenze3") {
    intersection() { sinistra3(); centro3(); }
    intersection() { centro3(); destra3(); }
    intersection() {
        union() { sinistra3(); centro3(); destra3(); }
        union() { for (v = [-1, 1]) translate([J1, v * KY1, F3 + 0.05]) linear_extrude(K3_BASSA) chiave2d();
                  for (y = KY2) translate([J2, y, F3 + 0.05]) linear_extrude(K3_ALTA) chiave2d(); }
    }
}
if (parte == "rivetti_targhetta") rivetti(7.2, 2);
if (parte == "rivetti_targhetta3") rivetti(5.6, 2);
// Le due viti della targhetta stanno ai lati delle righe piccole: qui si controlla che resti così (cerchi da 10 mm)
if (parte == "controllo_viti")
    linear_extrude(1) intersection() { testi2d(); union() for (v = T_VITI) translate(v) circle(d = 10); }
