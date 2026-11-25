// Segnaposto per la tavola con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.
// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.
// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».
// Oggetti con nominativo: targhetta da petto, portachiavi ed etichetta per lo zaino (volontari della
// Protezione Civile di Genzano di Roma), targhe da tavolo e da parete. Si cambiano solo i parametri qui sotto.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Tipo di targhetta] */
// petto = da divisa; portachiavi = con foro per l'anello; zaino = con fessura per laccio o cinghia;
// tavolo = da scrivania (targa + piede); parete = con fori per le viti
// Natale (25/11/2026): addobbo = disco da appendere all'albero; stella = stella da appendere; pacco = etichetta per
// i regali; segnaposto = targa piccola con il suo piede, per la tavola
// Feste dell'anno (25/11/2026), tutte da appendere, con la stessa disposizione delle scritte dell'addobbo:
// uovo = Pasqua; fiore = Infiorata e primavera; coccarda = 2 giugno e feste nazionali; cuore = «Grazie»
// carrello (25/11/2026) = portachiavi con una linguetta a forma di moneta da 1 euro, per sbloccare il carrello della spesa
tipo = "segnaposto"; // [petto, portachiavi, zaino, tavolo, parete, addobbo, stella, pacco, segnaposto, uovo, fiore, coccarda, cuore, carrello]
// tutto = pezzo unico; base e testo = pezzi separati per stampa a due colori; piede = supporto della versione da tavolo
parte = "tutto"; // [tutto, base, testo, piede]

/* [Testi] */
riga1 = "ALFA 1";
riga2 = "PROTEZIONE CIVILE";
// terza riga (petto, portachiavi, zaino): vuota per non usarla
riga3 = "GENZANO DI ROMA";
// riga in alto degli oggetti di Natale («BUON NATALE», «AUGURI DA»): vuota per non usarla
riga0 = "";
font = "Liberation Sans:style=Bold";
// carattere stretto per la riga piccola, così il nome dell'ente entra tutto
font2 = "Liberation Sans Narrow:style=Bold";

/* [Fissaggio della targhetta da petto] */
// balia = canale per una spilla da balia di metallo, da fissare con una goccia di colla; spilla = incavo per barretta adesiva da 30 mm; magneti = due sedi per magneti 10x1 mm
fissaggio = "balia"; // [balia, spilla, magneti, nessuno]
// lunghezza della spilla da balia (mm)
balia_lunghezza = 45;
// larghezza del canale per il filo della spilla (mm): largo apposta, perché i servizi di stampa garantiscono ±0,5 mm
balia_canale = 1.6;

/* [Bandiera italiana] */
// piccola bandiera in rilievo a sinistra del nominativo, alta quanto le lettere grandi (proporzioni 2:3)
bandiera = true;

/* [Spessori] */
// altezza delle scritte e della cornice sopra la base (mm): 1 mm resiste all'uso e si legge anche al tatto
rilievo = 1.0;
// larghezza della cornice (mm), 0 per toglierla
cornice = 1.2;

$fn = 48;

// Misure per tipo: [lunghezza, altezza, raggio angoli, spessore base, carattere riga1, y riga1,
//                   carattere righe 2-3, y riga2, y riga3, x del centro del testo]
// Regole dei servizi di stampa FDM (Craftcloud): pareti da 1 mm in su, dettagli e tratti delle lettere da 0,6 mm in su,
// rilievi alti e larghi almeno 0,5 mm. Con Liberation Sans Narrow Bold a 4,5 mm il tratto più sottile è di 0,70 mm.
MISURE = [
    ["petto",       [80, 30, 3, 2.4, 8.5,  6.0, 4.5,  -2.3,  -8.0, 6]],
    ["portachiavi", [64, 26, 4, 4.0, 6.5,  5.7, 4.5,  -1.2,  -6.7, 3]],
    ["carrello",    [64, 26, 4, 4.0, 6.5,  5.7, 4.5,  -1.2,  -6.7, 3]],
    ["zaino",       [80, 42, 4, 4.0, 8.5,  2.0, 4.5,  -6.3, -12.0, 6]],
    ["tavolo",      [150, 45, 4, 4.0, 20,  5.5, 6.0, -13.5,     0, 0]],
    ["parete",      [150, 45, 4, 4.0, 20,  5.5, 6.0, -13.5,     0, 0]],
    ["addobbo",     [76, 76, 4, 2.4, 8.0,  4.0, 4.5,  -7.5, -13.5, 7]],
    ["stella",      [112, 112, 3, 2.4, 8.0, 1.0, 4.5, -8.5, -14.5, 8]],
    ["pacco",       [86, 40, 3, 2.4, 8.0,  5.0, 4.5,  -5.0, -11.5, 9.5]],
    ["segnaposto",  [100, 46, 4, 3.0, 9.0, 13.0, 4.5, -4.0, -10.5, 7]],
    // feste: la lunghezza è quella della zona delle scritte (un disco di 76 mm), non l'ingombro del pezzo
    ["uovo",        [76, 76, 4, 2.4, 8.0,  4.0, 4.5,  -7.5, -13.5, 7]],
    ["fiore",       [76, 76, 4, 2.4, 8.0,  4.0, 4.5,  -7.5, -13.5, 7]],
    ["coccarda",    [76, 76, 4, 2.4, 8.0,  4.0, 4.5,  -7.5, -13.5, 7]],
    ["cuore",       [76, 76, 4, 2.4, 8.0,  7.0, 4.5,  -4.5, -10.5, 7]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];
FESTA = tipo == "uovo" || tipo == "fiore" || tipo == "coccarda" || tipo == "cuore";
NATALE = tipo == "addobbo" || tipo == "stella" || tipo == "pacco" || tipo == "segnaposto" || FESTA;
CHIAVI = tipo == "portachiavi" || tipo == "carrello";
TRE_RIGHE = tipo == "petto" || CHIAVI || tipo == "zaino" || NATALE;
// Oggetti di Natale: quota della riga in alto, distanza della bandiera dal bordo sinistro, foro per il nastro
Y0 = tipo == "cuore" ? 20 : tipo == "addobbo" || FESTA ? 17 : tipo == "stella" ? 11 : 14.2;
BAND_DA = tipo == "addobbo" || FESTA ? 5 : tipo == "stella" ? 25 : tipo == "pacco" ? 12 : CHIAVI ? 3 : 3.5;
NASTRO_D = 4.5;
NASTRO = tipo == "addobbo" || tipo == "coccarda" ? [0, L / 2 + 2] : tipo == "stella" ? [0, 45] : tipo == "uovo" ? [0, 43]
       : tipo == "fiore" ? [0, 42] : tipo == "cuore" ? [0, 28.5] : [-L / 2 + 6.5, 0];
// stella a cinque punte: raggio delle punte e delle rientranze; rientranze larghe, per farci stare le scritte
ST_R = 56 - R; ST_r = 34 - R;

// Portachiavi: occhiello tondo a sinistra con il foro per l'anello (5,5 mm di plastica intorno al foro)
OCCHIELLO_D = 16; FORO_D = 5;
OCCHIELLO_X = -L / 2 - OCCHIELLO_D / 2 + 3;
// Zaino: fessura in alto per laccio o cinghia
FESSURA = [26, 5.5]; FESSURA_Y = 13.5;

module forma() {
    if (tipo == "addobbo") {
        circle(d = L, $fn = 120);
        hull() { translate(NASTRO) circle(d = 14); translate([0, L / 2 - 8]) circle(d = 14); }
    }
    else if (tipo == "uovo")          // uovo: un cerchio largo in basso e uno stretto in alto
        hull() { translate([0, -4]) circle(r = 39, $fn = 120); translate([0, 19]) circle(r = 31, $fn = 120); }
    else if (tipo == "fiore") {       // fiore: dieci petali tondi intorno al disco delle scritte
        circle(d = L, $fn = 120);
        for (i = [0:9]) rotate(90 + i * 36) translate([36, 0]) circle(r = 13, $fn = 60);
    }
    else if (tipo == "coccarda") {    // coccarda: bordo pieghettato, due nastri in basso, occhiello in alto
        polygon([for (i = [0:63]) let (a = i * 360 / 64, q = i % 2 == 0 ? 42 : 39.5) [q * cos(a), q * sin(a)]]);
        hull() { translate(NASTRO) circle(d = 14); translate([0, L / 2 - 8]) circle(d = 14); }
        for (v = [-1, 1]) scale([v, 1]) polygon([[4, -30], [21, -30], [26, -64], [18, -59], [11, -66]]);
    }
    else if (tipo == "cuore") {       // cuore: due lobi che scendono a una punta arrotondata; foro sotto l'incavo
        for (v = [-1, 1]) hull() { translate([v * 19, 18]) circle(r = 26, $fn = 120); translate([0, -50]) circle(r = 3); }
        // l'incavo fra i due lobi: senza, l'inviluppo lo chiuderebbe e il cuore non si riconoscerebbe
    }
    else if (tipo == "stella")
        offset(r = R) polygon([for (i = [0:9]) let (a = 90 + i * 36, q = i % 2 == 0 ? ST_R : ST_r) [q * cos(a), q * sin(a)]]);
    else if (tipo == "pacco")
        offset(r = R) polygon([[-L / 2 + R + 9, -H / 2 + R], [L / 2 - R, -H / 2 + R], [L / 2 - R, H / 2 - R],
                               [-L / 2 + R + 9, H / 2 - R], [-L / 2 + R, H / 2 - R - 9], [-L / 2 + R, -H / 2 + R + 9]]);
    else
    offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
    if (CHIAVI)
        hull() {
            translate([OCCHIELLO_X, 0]) circle(d = OCCHIELLO_D);
            translate([-L / 2 + R, 0]) square([2 * R, OCCHIELLO_D], center = true);
        }
}

module fori() {
    if (CHIAVI) translate([OCCHIELLO_X, 0]) circle(d = FORO_D);
    if (tipo == "zaino") translate([0, FESSURA_Y]) offset(r = 1.5) square(FESSURA - [3, 3], center = true);
    if (tipo == "addobbo" || tipo == "stella" || tipo == "pacco" || FESTA) translate(NASTRO) circle(d = NASTRO_D);
}

module sagoma(inset = 0) {
    difference() {
        offset(delta = -inset) forma();
        offset(delta = inset) fori();
    }
}

// Tricolore: tre fasce verticali separate da solchi di 0,8 mm (sopra il minimo di 0,5 mm dei servizi di stampa),
// così si riconosce anche stampato in un solo colore. Posizione fissa a sinistra, il nominativo si sposta di TX.
BAND_H = S1; BAND_W = S1 * 1.5; SOLCO = 0.8;
BAND_X = TX - L / 2 + BAND_DA;
module bandiera2d() {
    for (i = [0:2])
        translate([BAND_X - TX + i * BAND_W / 3 + (i > 0 ? SOLCO / 2 : 0), Y1 - BAND_H / 2])
            square([BAND_W / 3 - (i == 1 ? SOLCO : SOLCO / 2), BAND_H]);
}

module testi2d() {
    if (bandiera && TRE_RIGHE) bandiera2d();
    translate([bandiera && TRE_RIGHE ? TX : 0, riga2 == "" ? 0 : Y1])
        text(riga1, size = S1, font = font, halign = "center", valign = "center");
    if (riga2 != "")
        translate([0, Y2])
            text(riga2, size = S2, font = font2, halign = "center", valign = "center");
    if (TRE_RIGHE && riga3 != "")
        translate([0, Y3])
            text(riga3, size = S2, font = font2, halign = "center", valign = "center");
    if (NATALE && riga0 != "") {
        translate([0, Y0]) text(riga0, size = S2, font = font2, halign = "center", valign = "center");
        // due stelline ai lati della riga in alto (addobbo e stella)
        if (tipo == "addobbo" || tipo == "stella" || FESTA) for (v = [-1, 1]) translate([v * (len(riga0) > 10 ? 27 : len(riga0) < 7 ? 17 : 21), Y0])
            polygon([for (i = [0:9]) let (a = 90 + i * 36, q = i % 2 == 0 ? 3.2 : 1.5) [q * cos(a), q * sin(a)]]);
    }
}

// Bordi smussati: tre gradini da 0,2 mm in alto e due in basso (uno strato di stampa ciascuno).
// Danno un bordo rifinito che non si scheggia e tolgono la «zampa d'elefante» del primo strato.
SMUSSO = 0.6;

module corpo() {
    for (i = [0:1]) translate([0, 0, i * 0.2]) linear_extrude(0.21) sagoma(0.4 - i * 0.2);
    translate([0, 0, 0.4]) linear_extrude(B - 0.4 - SMUSSO + 0.01) sagoma();
    for (i = [0:2]) translate([0, 0, B - SMUSSO + i * 0.2]) linear_extrude(0.21 - (i == 2 ? 0.01 : 0)) sagoma(0.2 * (i + 1));
}

module rilievo2d() {
    testi2d();
    if (cornice > 0) difference() { sagoma(SMUSSO); sagoma(SMUSSO + cornice); }
}

// Chiave per il carrello: una linguetta con la punta tonda come una moneta da 1 euro (23,25 mm di diametro,
// spessa 2,33 mm: Banca centrale europea, «Facce comuni», ecb.europa.eu, letta il 25/11/2026). È spessa 2,2 mm,
// un decimo meno della moneta, perché una stampa può uscire più spessa del disegno; esce di 28 mm dal manico,
// più del diametro della moneta, così la punta arriva dove arriverebbe la moneta.
EURO_D = 23.25; LINGUA_S = 2.2; LINGUA_L = 28;
module lingua() {
    linear_extrude(LINGUA_S) hull() {
        translate([L / 2 - 4, -EURO_D / 2]) square([4, EURO_D]);
        translate([L / 2 + LINGUA_L - EURO_D / 2, 0]) circle(d = EURO_D, $fn = 120);
    }
}

module base() {
    if (tipo == "carrello") lingua();
    difference() {
        corpo();
        if (tipo == "petto" && fissaggio == "spilla")
            translate([0, 0, -0.01]) linear_extrude(0.81) square([32, 7], center = true);
        if (tipo == "petto" && fissaggio == "balia") balia();
        if (tipo == "petto" && fissaggio == "magneti")
            for (x = [-22, 22]) translate([x, 0, -0.01]) cylinder(d = 10.3, h = 1.21);
        if (tipo == "parete")
            for (x = [-(L / 2 - 9), L / 2 - 9]) translate([x, 0, 0]) {
                translate([0, 0, -0.01]) cylinder(d = 4.2, h = B + 0.02);
                translate([0, 0, B - 2.1]) cylinder(d1 = 4.2, d2 = 8.6, h = 2.11);
            }
    }
}

// Canale sul retro: la gamba fissa della spilla ci si appoggia dentro e si ferma con una goccia di colla;
// la gamba con la punta resta libera. Le due sedi alle estremità accolgono molla e testa.
// Profondità 1,3 mm e sedi da 1,4 mm: sopra resta almeno 1 mm di plastica, il minimo per le pareti FDM.
module balia() {
    l = balia_lunghezza - 7;    // tratto di canale tra le due sedi
    translate([0, 4, 0]) {
        translate([0, 0, -0.01]) linear_extrude(1.31) square([l + 1, balia_canale], center = true);
        for (x = [-balia_lunghezza / 2 + 2, balia_lunghezza / 2 - 2])
            translate([x, 0, -0.01]) linear_extrude(1.41) square([6.5, 6.5], center = true);
    }
}

module testo3d() {
    translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) rilievo2d();
}

// Piede per la versione da tavolo: la targa si infila nella fessura, inclinata di 15 gradi
module piede() {
    fessura = B + rilievo + 1.0;               // mezzo millimetro di gioco per parte: la tolleranza di una stampa a filo
    pl = tipo == "segnaposto" ? 35 : 50;       // mezza lunghezza del piede
    difference() {
        hull() {
            translate([-pl, -14, 0]) cube([2 * pl, 28, 2]);
            translate([-pl, -8, 0]) cube([2 * pl, 16, 14]);
        }
        translate([0, -2, 6]) rotate([-15, 0, 0])
            translate([-(L / 2 + 5), -fessura / 2, 0]) cube([L + 10, fessura, 30]);
    }
}

if (parte == "piede") piede();
else {
    if (parte == "tutto" || parte == "base") base();
    if (parte == "tutto" || parte == "testo") testo3d();
}
