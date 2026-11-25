// Porta posate con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Oggetti con il nominativo per il campo, la mensa, i kit e la sede (volontari della Protezione Civile di
// Genzano di Roma): segna tazza, etichette per borraccia, gavetta e brandina, porta posate, porta pile, porta schede,
// segnalibro per il registro e cartellino per l'armadietto. Si cambiano solo i parametri qui sotto.
// Ogni oggetto lascia libera, sulla faccia delle scritte, una fascia per una riga con nome e cognome.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
// tazza = clip per il manico della tazza; borraccia = etichetta con occhiello per moschettone; posate = astuccio per
// posate di metallo; gavetta = etichetta con foro per cordino; brandina = targhetta con due asole per fascette o velcro;
// pile_aa e pile_aaa = porta 4 pile; schede = vassoio per schede SD, microSD e nano SIM;
// registro = segnalibro per il registro di sala operativa; armadietto = cartellino da biadesivo o da due viti
tipo = "posate"; // [tazza, borraccia, posate, gavetta, brandina, pile_aa, pile_aaa, schede, registro, armadietto]
// tutto = pezzo unico; base e testo = pezzi separati per stampa a due colori;
// controllo_viti = solo le parti delle scritte che finirebbero sotto le teste delle viti (deve risultare vuoto)
parte = "tutto"; // [tutto, base, testo, controllo_viti]

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

/* [Manico della tazza] */
// Per i manici delle tazze non c'è una norma: le misure cambiano da tazza a tazza. Misura con un righello la parte
// del manico dove va la clip: larghezza (da un lato all'altro) e spessore (dall'interno all'esterno). Le misure qui
// sotto sono un'ipotesi per un manico medio; il foro ha 0,5 mm di gioco per lato e la bocca è più stretta del manico
// di 1,5 mm, così la clip si apre un poco, entra e resta ferma. Prima stampa di prova consigliata.
manico_largo = 12;
manico_spesso = 8;

/* [Spessori] */
// altezza delle scritte e della cornice sopra la base (mm)
rilievo = 1.0;
// larghezza della cornice (mm), dove c'è
cornice = 1.2;

$fn = 48;

// Misure per tipo: [lunghezza, altezza, raggio angoli, spessore base, carattere riga1, y riga1,
//                   carattere righe piccole, y riga2, y riga3, x del centro delle scritte]
// Nei porta pile «lunghezza × altezza» è la faccia davanti con le scritte e le y sono quote da terra;
// nel porta posate lunghezza = astuccio, altezza = larghezza, spessore = spessore totale.
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, tratti delle lettere da 0,6 mm in su,
// rilievi alti e larghi almeno 0,5 mm. Liberation Sans Bold da 6 mm in su e Narrow Bold a 4 mm passano il controllo.
MISURE = [
    ["tazza",      [56, 32, 3, 2.5, 6.0, 9.5, 4.0, -5.5, -11.0, 0]],
    ["borraccia",  [70, 34, 4, 3.5, 6.5, 10.75, 4.0, -4.5, -10.0, 0]],
    ["posate",     [214.5, 50, 3, 26, 6.5, 13.5, 4.0, -4.0, -11.0, -30]],
    ["gavetta",    [70, 34, 4, 3.0, 6.5, 10.75, 4.0, -4.5, -10.0, 0]],
    ["brandina",   [90, 34, 4, 3.0, 6.5, 10.75, 4.0, -4.5, -10.0, 0]],
    ["pile_aa",    [72, 36, 3, 2.0, 6.5, 30.25, 4.0, 15.0, 9.5, 0]],
    ["pile_aaa",   [64, 34, 3, 2.0, 6.5, 28.25, 4.0, 13.0, 7.5, 0]],
    ["schede",     [117, 64, 4, 3.5, 6.5, 25.25, 4.0, 10.0, 0, 0]],
    ["registro",   [60, 200, 4, 2.0, 6.5, 91.5, 4.0, 75.5, 70.0, 0]],
    ["armadietto", [90, 36, 4, 3.0, 6.5, 9.75, 4.0, -5.5, -11.0, 0]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];
SMUSSO = 0.6;
CON_CORNICE = tipo == "registro";
// righe 2 e 3 unite in una riga sola, dove c'è spazio in larghezza
UNA_RIGA = tipo == "schede";

/* ---------- Misure degli oggetti veri (con la fonte) ---------- */

// Pile stilo AA (LR6): diametro 13,7-14,5 mm, altezza 49,5-50,5 mm (IEC 60086-2:2021, riportata da
// en.wikipedia.org/wiki/AA_cell; Panasonic LR6XW: 14,5 × 50,5 mm, consultati il 24/11/2026).
// Pile ministilo AAA (LR03): diametro 9,5-10,5 mm, altezza 43,3-44,5 mm (scheda Energizer EN92, IEC LR03,
// data.energizer.com/pdfs/EN92EU0126.pdf, consultata il 24/11/2026).
// Le sedi si fanno sul massimo più 0,5 mm per lato.
PILA = tipo == "pile_aa" ? [14.5, 50.5] : [10.5, 44.5];      // [diametro massimo, altezza massima]
SEDE = PILA[0] + 1.0;                                          // 15,5 mm (AA) e 11,5 mm (AAA)
SEDE_FONDA = tipo == "pile_aa" ? 34 : 32;                      // la pila sporge di 16,5 mm (AA) e 12,5 mm (AAA)
PROF = SEDE + 4;                                               // profondità del porta pile: pareti da 2 mm

// Schede: SD 24 × 32 × 2,1 mm e microSD 11 × 15 × 1,0 mm (SD Association, misure riportate dalle schede
// Kingston SDCS2 e Sony SF-16N4); nano SIM (4FF) 12,3 × 8,8 × 0,67 mm (ETSI TS 102 221, comunicato ETSI
// del 1° giugno 2012). Consultate il 24/11/2026. Sedi con 0,5 mm di gioco per lato.
// [larghezza, altezza, profondità della sede, diametro dell'incavo per il dito]
SCHEDE = [[25, 33, 2.2, 10], [25, 33, 2.2, 10], [12, 16, 1.2, 10], [12, 16, 1.2, 10],
          [9.8, 13.3, 0.9, 8], [9.8, 13.3, 0.9, 8]];
SCHEDE_Y0 = -28;            // bordo basso delle sedi
INCAVO_FONDO = 1.0;          // plastica che resta sotto l'incavo per il dito

// Posate da tavola: coltello 210-245 mm, forchetta e cucchiaio 190-210 mm (guida Lusini «Posate», consultata il
// 24/11/2026); un cucchiaio da tavola sta in una confezione di 40 × 30 × 200 mm (IKEA MARTORP, 19 cm).
// Dentro l'astuccio: 212 × 46 × 22 mm; il coltello più lungo sporge di qualche centimetro.
POS_UTILE = 212; POS_FONDO = 2.5; POS_PARETE = 2.0;

// Etichette: occhiello per moschettone (foro 8 mm, anello largo 7 mm) e foro per cordino (4,5 mm)
OCCHIELLO = tipo == "borraccia" ? [22, 8] : [14, 4.5];       // [diametro esterno, foro]
OCCHIELLO_X = -L / 2 - OCCHIELLO[0] / 2 + 4;
// Brandina: due asole da 4,5 × 22 mm, per fascette fino a 4 mm di spessore o velcro largo fino a 2 cm
ASOLA = [4.5, 22]; ASOLA_X = L / 2 - 6.5;

// Viti per legno o truciolare a testa svasata piana da 4 mm: testa larga da 7,64 a 8 mm e alta fino a 2,35 mm
// (manuale tecnico di viteria, capitolo 19, tabella a pagina 19.3, consultato il 25/11/2026). La svasatura dei fori
// è di 8,8 mm, profonda 2,2 mm: la testa resta a filo. Nei fori da 4,4 mm passa anche una vite M4.
// Fori per le viti (testa svasata da 4 mm) lontani dalle scritte (parte = "controllo_viti" lo verifica)
VITI = tipo == "armadietto" ? [[-39, 0], [39, 0]] : [];

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

// Le scritte della faccia: nominativo, poi la fascia libera per nome e cognome, poi l'ente
module testi2d() {
    translate([TX, Y1]) nominativo2d(S1);
    if (UNA_RIGA) riga(str(riga2, " ", riga3), TX, Y2);
    else {
        if (riga2 != "") riga(riga2, TX, Y2);
        if (riga3 != "") riga(riga3, TX, Y3);
    }
}

/* ---------- Forme in pianta delle piastre ---------- */

module forma() {
    if (tipo == "tazza") {
        offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
        clip2d(true);
    } else if (tipo == "registro") translate([0, 0]) offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
    else if (tipo == "schede") offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
    else {
        offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
        if (tipo == "borraccia" || tipo == "gavetta")
            hull() {
                translate([OCCHIELLO_X, 0]) circle(d = OCCHIELLO[0]);
                translate([-L / 2 + R, 0]) square([2 * R, OCCHIELLO[0]], center = true);
            }
    }
}

module fori() {
    if (tipo == "borraccia" || tipo == "gavetta") translate([OCCHIELLO_X, 0]) circle(d = OCCHIELLO[1]);
    if (tipo == "brandina") for (s = [-1, 1]) translate([s * ASOLA_X, 0]) offset(r = 1) square(ASOLA - [2, 2], center = true);
    if (tipo == "tazza") clip2d(false);
}

module sagoma(inset = 0) {
    difference() {
        offset(delta = -inset) forma();
        offset(delta = inset) fori();
    }
}

// Piastra con bordi smussati (gradini da 0,2 mm, uno strato di stampa ciascuno)
module piastra(h = B) {
    difference() {
        union() {
            for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) sagoma(0.4 - i * 0.2);
            translate([0, 0, 0.4]) linear_extrude(h - 0.4 - SMUSSO + 0.01) sagoma();
            for (i = [0:2]) translate([0, 0, h - SMUSSO + i * 0.2]) linear_extrude(0.21 - (i == 2 ? 0.01 : 0)) sagoma(0.2 * (i + 1));
        }
        for (v = VITI) translate(v) {
            translate([0, 0, -0.01]) cylinder(d = 4.4, h = h + 0.02);
            translate([0, 0, h - 2.2]) cylinder(d1 = 4.4, d2 = 8.8, h = 2.21);
        }
    }
}

module rilievo2d() {
    difference() {
        union() {
            testi2d();
            if (CON_CORNICE && cornice > 0) difference() { sagoma(SMUSSO); sagoma(SMUSSO + cornice); }
        }
        for (v = VITI) translate(v) circle(d = 10);   // niente rilievo dove appoggia la testa della vite
    }
}

/* ---------- Segna tazza: clip per il manico ---------- */

// Anello aperto a sinistra della piastra, alto 8 mm: il manico passa nel foro ovale, la bocca è più stretta
// del manico di 1,5 mm. Parete dell'anello 2,4 mm. Si stampa in piano: anello e piastra partono dal piatto.
CLIP_FORO = [manico_spesso + 1, manico_largo + 1];   // [x, y]: 0,5 mm di gioco per lato
CLIP_PARETE = 2.4; CLIP_ALTO = 8; CLIP_BOCCA = manico_spesso - 1.5;
CLIP_X = -L / 2 - CLIP_FORO[0] / 2 - CLIP_PARETE + 1.5;
module clip2d(pieno) {
    translate([CLIP_X, 0])
        if (pieno) offset(r = 1) offset(delta = -1) difference() {
            hull() {
                resize(CLIP_FORO + 2 * [CLIP_PARETE, CLIP_PARETE]) circle(d = 10, $fn = 64);
                translate([CLIP_FORO[0] / 2, 0]) square([CLIP_PARETE * 2, 14], center = true);
            }
        }
        else union() {
            resize(CLIP_FORO) circle(d = 10, $fn = 64);
            // bocca verso sinistra, con gli spigoli arrotondati
            translate([-CLIP_FORO[0] / 2 - CLIP_PARETE - 1, -CLIP_BOCCA / 2]) square([CLIP_FORO[0] / 2 + CLIP_PARETE + 1, CLIP_BOCCA]);
        }
}
module tazza_base() {
    piastra();
    // l'anello sale fino a 8 mm, con gli stessi gradini sul fondo
    intersection() {
        union() {
            for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) sagoma(0.4 - i * 0.2);
            translate([0, 0, 0.4]) linear_extrude(CLIP_ALTO - 0.4) sagoma();
        }
        translate([CLIP_X - 20, -20, -1]) cube([20 + CLIP_FORO[0] / 2 + CLIP_PARETE, 40, CLIP_ALTO + 2]);
    }
}

/* ---------- Porta posate ---------- */

// Astuccio piatto lungo x, chiuso a sinistra e aperto a destra, con un incavo per le dita all'apertura e un foro
// di scolo nel fondo. Si stampa in piedi sul lato chiuso (genera-stampa-3d.py lo ruota: «fianco»), così le pareti
// salgono dritte senza supporti. Le scritte stanno sulla faccia di sopra (z = B).
module profilo_x(x0, x1) {     // profilo disegnato nel piano y-z ed esteso lungo x da x0 a x1
    translate([x0, 0, 0]) rotate([90, 0, 90]) linear_extrude(x1 - x0) children();
}
module posate_base() {
    W = H; T = B; P = POS_PARETE;
    difference() {
        profilo_x(-L / 2, L / 2) translate([0, T / 2]) offset(r = R) square([W - 2 * R, T - 2 * R], center = true);
        profilo_x(-L / 2 + POS_FONDO, L / 2 + 0.01) translate([0, T / 2]) offset(r = 1.5) square([W - 2 * P - 3, T - 2 * P - 3], center = true);
        translate([L / 2, 0, -0.01]) cylinder(r = 10, h = T + 0.02, $fn = 64);     // incavo per le dita
        translate([-L / 2 - 0.01, 0, T / 2]) rotate([0, 90, 0]) cylinder(d = 6, h = POS_FONDO + 0.02);   // scolo
    }
}

/* ---------- Porta pile ---------- */

// Blocco con 4 sedi in fila, aperte in alto. Si stampa in piedi, come si usa: le scritte stanno sulla faccia
// davanti (y = -PROF/2) e nella vista l'oggetto si sdraia con quella faccia verso l'alto («assi»).
PASSO = (L - 2 * 2) / 4;
module pile_base() {
    difference() {
        union() {
            for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21)
                offset(delta = -(0.4 - i * 0.2)) offset(r = R) square([L - 2 * R, PROF - 2 * R], center = true);
            translate([0, 0, 0.4]) linear_extrude(H - 0.4) offset(r = R) square([L - 2 * R, PROF - 2 * R], center = true);
        }
        for (i = [0:3]) translate([-L / 2 + 2 + PASSO * (i + 0.5), 0, H - SEDE_FONDA]) cylinder(d = SEDE, h = SEDE_FONDA + 0.01, $fn = 64);
    }
}
module pile_testo() {
    translate([0, -PROF / 2 + 0.01, 0]) rotate([90, 0, 0]) linear_extrude(rilievo + 0.01) testi2d();
}

/* ---------- Porta schede ---------- */

// Vassoio con le sedi in fila in basso, ognuna con un incavo per il dito sul bordo basso, e le scritte in alto.
function schede_x(i) = i == 0 ? -L / 2 + 4 : schede_x(i - 1) + SCHEDE[i - 1][0] + 3;
module schede_base() {
    difference() {
        piastra();
        for (i = [0:len(SCHEDE) - 1]) {
            s = SCHEDE[i];
            translate([schede_x(i), SCHEDE_Y0, B - s[2]]) cube([s[0], s[1], s[2] + 0.01]);
            translate([schede_x(i) + s[0] / 2, SCHEDE_Y0, INCAVO_FONDO]) cylinder(d = s[3], h = B);
        }
    }
}

/* ---------- Montaggio dei pezzi ---------- */

module base() {
    if (tipo == "tazza") tazza_base();
    else if (tipo == "posate") posate_base();
    else if (tipo == "pile_aa" || tipo == "pile_aaa") pile_base();
    else if (tipo == "schede") schede_base();
    else piastra();
}
module testo() {
    if (tipo == "pile_aa" || tipo == "pile_aaa") pile_testo();
    else translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) rilievo2d();
}

if (parte == "tutto" || parte == "base") base();
if (parte == "tutto" || parte == "testo") testo();
if (parte == "controllo_viti" && len(VITI) > 0)
    linear_extrude(1) intersection() { testi2d(); union() for (v = VITI) translate(v) circle(d = 10); }
