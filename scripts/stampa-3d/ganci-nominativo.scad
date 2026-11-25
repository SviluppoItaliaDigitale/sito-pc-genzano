// Ganci con nominativo per i volontari della Protezione Civile di Genzano di Roma: appendiabiti da armadietto,
// gancio per l'anta, gancio da cintura, porta radio portatile, supporto per torcia e clip da parasole. Si cambiano solo i parametri qui sotto.
// Licenza: CC BY-NC-SA 4.0 — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.

/* [Oggetto] */
// appendiabiti = si avvita o si incolla nell'armadietto; anta = si appoggia sopra l'anta; cintura = clip da cintura;
// radio = supporto da parete su cui si aggancia la clip della radio portatile;
// microfono = supporto da parete o da cruscotto per il microfono altoparlante della radio;
// torcia = supporto da parete per una torcia tonda;
// parasole = clip da infilare sull'aletta parasole del mezzo, con l'occhiello per il telecomando o le chiavi
tipo = "appendiabiti"; // [appendiabiti, anta, cintura, radio, microfono, torcia, parasole]
// tutto = pezzo unico; base e testo = pezzi separati per stampa a due colori;
// controllo_viti = solo le parti delle scritte che finirebbero sulle teste delle viti (deve risultare vuoto)
parte = "tutto"; // [tutto, base, testo, controllo_viti]

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
// spessore del ponte che passa sopra l'anta (mm): sta nella fessura fra anta chiusa e mobile, di pochi millimetri
spessore_ponte = 2;
// spazio per la cintura (mm): cinture spesse fino a 5 mm, il dentino lascia passare 3,5 mm e la linguetta si piega
spazio_cintura = 5.5;
// altezza utile per la cintura fra il ponte e il dentino (mm): entrano le cinture alte fino a 4 cm
altezza_cintura = 44;
// diametro del corpo della torcia (mm). Maglite a 2 o 3 pile D: 39,67 mm (classiche) e 38,1 mm (ML300LX),
// dalle schede del produttore su maglite.com (consultate il 24/11/2026). Per un'altra torcia misura il corpo.
diametro_torcia = 39.7;
// spessore dell'aletta parasole del mezzo (mm): misuralo con un righello prima di stampare, cambia da mezzo a mezzo
spessore_parasole = 20;
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
    ["radio",        [80, 34, 4, 5.0, 8.5, 6.0, 4.5, -2.3, -8.0, 6]],
    ["microfono",    [66, 30, 4, 5.0, 7.5, 6.0, 4.0, -2.0, -7.0, 6]],
    ["torcia",       [80, 34, 4, 5.0, 8.5, 6.0, 4.5, -2.3, -8.0, 6]],
    ["parasole",     [80, 34, 4, 4.0, 8.5, 6.0, 4.5, -2.3, -8.0, 6]]
];
M = MISURE[search([tipo], MISURE)[0]][1];
L = M[0]; H = M[1]; R = M[2]; B = M[3];
S1 = M[4]; Y1 = M[5]; S2 = M[6]; Y2 = M[7]; Y3 = M[8]; TX = M[9];
SMUSSO = 0.6;

// Anello del supporto torcia (spiegato più sotto): serve già qui per la posizione della terza vite
TOR_D = diametro_torcia + 0.6; TOR_T = 3.5; TOR_R = TOR_D / 2 + TOR_T; TOR_Y = -10 - TOR_R - 12;   // 22 mm sotto la piastra: le viti in alto restano libere
TOR_Z = B - 0.5 + TOR_R;                     // centro dell'anello: l'anello tocca la piastra
TOR_BOCCA = diametro_torcia * 0.92;

// Viti per legno o truciolare a testa svasata piana da 4 mm: testa larga da 7,64 a 8 mm e alta fino a 2,35 mm
// (manuale tecnico di viteria, capitolo 19, tabella a pagina 19.3, consultato il 25/11/2026). La svasatura dei fori
// è di 8,8 mm, profonda 2,2 mm: la testa resta a filo. Nei fori da 4,4 mm passa anche una vite M4.
// Fori per le viti (testa svasata da 4 mm), dove servono: sotto le scritte, perché la testa della vite
// non copra la bandiera o il nominativo (parte = "controllo_viti" lo verifica)
VITI = tipo == "appendiabiti" ? [[-33, -11], [33, -11]]
     : tipo == "radio" ? [[-33, -11], [33, -11], [-30, -74], [30, -74]]
     : tipo == "microfono" ? [[-25, -21.5], [25, -21.5]]
     : tipo == "torcia" ? [[-33, -11], [33, -11], [0, TOR_Y - TOR_R - 8]]
     : [];

// Contorno visto di fronte
module forma() {
    offset(r = R) square([L - 2 * R, H - 2 * R], center = true);
    if (tipo == "appendiabiti" || tipo == "anta")        // pannello sotto la piastra, largo quanto lei, dove nasce il gancio
        translate([-L / 2, -46]) offset(r = R) offset(delta = -R) square([L, 40]);
    if (tipo == "radio")                                   // pannello sotto la piastra per il supporto
        translate([-L / 2, -84]) offset(r = R) offset(delta = -R) square([L, 74]);
    if (tipo == "microfono")                               // pannello sotto la piastra per il supporto
        translate([-L / 2, -60]) offset(r = R) offset(delta = -R) square([L, 50]);
    if (tipo == "torcia")                                  // pannello sotto la piastra per le due mezzelune
        translate([-L / 2, TOR_Y - TOR_R - 15]) offset(r = R) offset(delta = -R) square([L, -TOR_Y + TOR_R + 15 - 10]);
    if (tipo == "cintura" || tipo == "parasole")           // occhiello a destra per un moschettone
        hull() {
            translate([L / 2 + 6, 0]) circle(d = 18);
            translate([L / 2 - R, 0]) square([2 * R, 18], center = true);
        }
}

module fori() {
    if (tipo == "cintura" || tipo == "parasole") translate([L / 2 + 6, 0]) circle(d = 8);
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

// Profilo disegnato nel piano y-z ed esteso per tutta la larghezza della piastra, con gli angoli
// arrotondati come la piastra. I pezzi «di fianco» si stampano in piedi sul lato sinistro: ogni strato
// poggia su quello sotto, senza supporti dentro le fessure (genera-stampa-3d.py li ruota).
module profilo_x(y0, y1, z0, z1) {
    intersection() {
        rotate([90, 0, 90]) linear_extrude(L, center = true) children();
        translate([0, (y0 + y1) / 2, z0])
            linear_extrude(z1 - z0) offset(r = R) square([L - 2 * R, y1 - y0 - 2 * R], center = true);
    }
}

// Clip da cintura: ponte in alto, linguetta che scende dietro la piastra e dentino con lo scivolo
// in basso. La cintura entra dal basso, il dentino la trattiene; per toglierla si solleva la linguetta.
// La linguetta lavora come una molla: 3,5 mm di PETG per 49 mm, si apre di 1,5 mm con circa 2 kg.
module clip_cintura() {
    G = spazio_cintura; T = 3.5; Y0 = H / 2 - 5 - altezza_cintura - 5;
    profilo_x(Y0, H / 2, -(G + T), 0.5)
        offset(r = 0.8) offset(delta = -0.8) union() {
            translate([H / 2 - 5, -(G + T)]) square([5, G + T + 0.5]);           // ponte in alto
            translate([Y0, -(G + T)]) square([H / 2 - Y0, T]);                    // linguetta
            polygon([[Y0, -G - 0.1], [Y0, -G + 0.6], [Y0 + 2, -G + 2],            // dentino: scivolo sotto,
                     [Y0 + 4, -G + 2], [Y0 + 5.5, -G - 0.1]]);                    // fermo sopra
        }
}

// Gancio davanti al pannello, largo quanto la piastra: braccio che esce, punta che risale e rinforzo
// alla radice. Fra la piastra e la punta restano 21 mm per giacche, zaini e caschi.
module gancio() {
    profilo_x(-45, -23, B - 0.5, B + 28)
        offset(r = 1.5) offset(delta = -1.5) union() {
            translate([-45, B - 0.5]) square([10, 28.5]);                     // braccio, 10 mm di spessore
            translate([-45, B + 21]) square([22, 7]);                         // punta, 7 mm di spessore
            polygon([[-35.1, B - 0.5], [-35.1, B + 7], [-28, B - 0.5]]);      // rinforzo a 45 gradi
        }
}

// Ponte sopra l'anta e aletta che scende dietro, larghi quanto la piastra
module ponte_anta() {
    D = spessore_anta;
    P = spessore_ponte;
    profilo_x(H / 2 - 28, H / 2, -(D + 5), 0.5)
        offset(r = 0.8) offset(delta = -0.8) union() {
            translate([H / 2 - P, -(D + 5)]) square([P, D + 5.5]);
            translate([H / 2 - 28, -(D + 5)]) square([28, 5]);
        }
}

// Supporto radio: barra spessa 4 mm e alta 38 mm, come una cintura, staccata 8 mm dalla parete e
// tenuta solo dai due appoggi alle estremità. La clip della radio passa dietro la barra e scende
// libera sotto, come su una cintura vera: la radio appoggia con la curva della clip sul bordo alto.
// Y0-Y1 = altezza della barra, G = spazio fra piastra e barra, T = spessore della barra.
module supporto_radio(Y0 = -64, Y1 = -26, G = 8, T = 4) {
    A = 6; Z = G + T;
    profilo_x(Y0, Y1, B - 0.5, B + Z) translate([Y0, B + G]) square([Y1 - Y0, T]);
    for (s = [-1, 1])                    // appoggi con il lato interno a scivolo (45°): di fianco si stampano senza supporti
        intersection() {
            hull() {
                translate([s * (L / 2 - A / 2), (Y0 + Y1) / 2, B + (Z - 0.5) / 2]) cube([A, Y1 - Y0, Z + 0.5], center = true);
                translate([s * (L / 2 - (A + Z + 1) / 2), (Y0 + Y1) / 2, B - 0.25]) cube([A + Z + 1, Y1 - Y0, 0.5], center = true);
            }
            translate([0, (Y0 + Y1) / 2, B - 0.5])
                linear_extrude(Z + 1) offset(r = R) square([L - 2 * R, Y1 - Y0 - 2 * R], center = true);
        }
}

// Supporto torcia: anello a scatto largo quanto la piastra, con la torcia in orizzontale. L'anello è spesso 3,5 mm e
// ha il foro 0,6 mm più largo del corpo; la bocca davanti è stretta il 92% del diametro, così la torcia si spinge
// dentro, l'anello si apre un poco e la trattiene (con l'85% servirebbe una spinta troppo forte). La terza vite sta sotto l'anello, nel pannello.
module supporto_torcia() {
        profilo_x(TOR_Y - TOR_R, TOR_Y + TOR_R, B - 0.5, B - 0.5 + 2 * TOR_R)
            offset(r = 0.8) offset(delta = -0.8) difference() {
                union() {
                    translate([TOR_Y, TOR_Z]) circle(r = TOR_R, $fn = 96);
                    translate([TOR_Y - TOR_R, B - 0.5]) square([2 * TOR_R, TOR_R]);      // base piena contro la piastra
                }
                translate([TOR_Y, TOR_Z]) circle(d = TOR_D, $fn = 96);
                translate([TOR_Y - TOR_BOCCA / 2, TOR_Z]) square([TOR_BOCCA, TOR_R + 1]);  // bocca davanti
            }
}

// Clip da parasole: ponte sopra l'aletta e linguetta che scende dietro, come il gancio per l'anta, con il ponte
// spesso 3 mm. Lo spazio è lo spessore dell'aletta più 0,5 mm; la linguetta scende di 24 mm.
module clip_parasole() {
    D = spessore_parasole + 0.5; P = 3;
    profilo_x(H / 2 - 24, H / 2, -(D + 4), 0.5)
        offset(r = 0.8) offset(delta = -0.8) union() {
            translate([H / 2 - P, -(D + 4)]) square([P, D + 4.5]);
            translate([H / 2 - 24, -(D + 4)]) square([24, 4]);
        }
}

SPOSTA = tipo == "anta" ? spessore_anta + 5 : tipo == "cintura" ? spazio_cintura + 3.5
       : tipo == "parasole" ? spessore_parasole + 4.5 : 0;

translate([0, 0, SPOSTA]) {
    if (parte == "tutto" || parte == "base") {
        piastra();
        if (tipo == "appendiabiti" || tipo == "anta") gancio();
        if (tipo == "anta") ponte_anta();
        if (tipo == "cintura") clip_cintura();
        if (tipo == "radio") supporto_radio();
        // microfono: barra alta 24 mm e spessa 3,5 mm, a 4,5 mm dalla piastra, per la clip a molla del microfono
        if (tipo == "microfono") supporto_radio(-54, -30, 4.5, 3.5);
        if (tipo == "torcia") supporto_torcia();
        if (tipo == "parasole") clip_parasole();
    }
    if (parte == "controllo_viti")
        linear_extrude(1) intersection() { testi2d(); for (v = VITI) translate(v) circle(d = 10); }
    if (parte == "tutto" || parte == "testo")
        translate([0, 0, B - 0.01]) linear_extrude(rilievo + 0.01) rilievo2d();
}
