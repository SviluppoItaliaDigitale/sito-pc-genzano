// Custodia del pluviometro: ESP32 e due pressacavi (cavo del contatto e alimentazione)
// Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma - www.protezionecivilegenzano.it
// Licenza: CC BY-NC-SA 4.0. Misure in millimetri. Si apre con OpenSCAD (gratuito).
// Parti da esportare una per volta (OpenSCAD 2021.01 o successivo):
//   openscad -o custodia-pluviometro-scatola.stl -D 'parte="scatola"' custodia-pluviometro.scad
//   openscad -o custodia-pluviometro-coperchio.stl -D 'parte="coperchio"' custodia-pluviometro.scad
//   openscad -o custodia-pluviometro-guarnizione.stl -D 'parte="guarnizione"' custodia-pluviometro.scad
// Stampa: scatola con il fondo sul piatto, coperchio con la faccia piana sul piatto, guarnizione in TPU.

/* [Parte] */
// Parte da mostrare o esportare
parte_scelta = "tutto"; // [tutto, scatola, coperchio, guarnizione]

/* [Scheda] */
// Lunghezza della scheda (asse X)
pcb_lunghezza = 70; // [10:0.5:250]
// Larghezza della scheda (asse Y)
pcb_larghezza = 50; // [10:0.5:250]
// Spessore della scheda
pcb_spessore = 1.6; // [0.8:0.1:3]
// Spazio libero sopra la scheda (componenti, batteria, cavi)
spazio_sopra = 25; // [2:0.5:120]
// Altezza dei distanziali sotto la scheda
spazio_sotto = 5; // [2:0.5:20]

/* [Pareti e giochi] */
// Gioco tra scheda e pareti
gioco = 0.5; // [0.2:0.05:1.5]
// Spessore delle pareti
parete = 2.4; // [1.2:0.2:5]
// Spessore di fondo e coperchio
fondo = 2.4; // [1.2:0.2:5]
// Raggio degli spigoli esterni
raggio = 3; // [0:0.5:10]

/* [Coperchio] */
// Altezza del bordo che entra nella scatola
bordo_coperchio = 4; // [2:0.5:10]
// Spessore del bordo del coperchio
spessore_bordo = 1.6; // [1.2:0.2:3]
// Gioco tra il bordo del coperchio e le pareti
gioco_coperchio = 0.3; // [0.1:0.05:0.8]
// Coperchio avvitato agli angoli (altrimenti a incastro)
viti = true;
// Foro di passaggio della vite nel coperchio (M3: 3.4)
diametro_vite = 3.4; // [2:0.1:5]
// Foro della colonna per inserto a caldo o vite autofilettante (vedi la scheda dell'inserto)
diametro_foro_colonna = 4; // [2:0.1:6]
// Diametro esterno della colonna
diametro_colonna = 7.5; // [5:0.5:12]
// Guarnizione in TPU tra scatola e coperchio (solo con le viti)
guarnizione = true;
// Spessore della guarnizione
spessore_guarnizione = 1.2; // [0.6:0.2:3]

/* [Fori] */
// Numero di pressacavi sulla stessa parete
numero_pressacavi = 2; // [1, 2]
// Distanza fra i centri dei due pressacavi
distanza_pressacavi = 30; // [20:1:60]
// Foro del pressacavo (0 = nessuno)
foro_pressacavo = 12.7; // [0:0.1:30]
// Parete del pressacavo
lato_pressacavo = "davanti"; // [sinistra, destra, davanti, dietro]
// Foro per il connettore d'antenna sul coperchio (SMA: 6.5; 0 = nessuno)
foro_antenna = 0; // [0:0.1:20]
// Posizione del connettore d'antenna
posizione_antenna = "centro"; // [centro, sinistra, destra]
// Foro di scarico della condensa sul fondo (0 = nessuno)
foro_scarico = 2; // [0:0.5:5]

/* [Fissaggio] */
// Alette laterali con foro per viti o fascette
alette = true;
// Diametro del foro delle alette
foro_alette = 4.5; // [3:0.5:8]

/* [Qualità] */
// Segmenti dei cerchi (più alto = più liscio e più lento)
$fn = 48; // [16:8:96]

/* [Hidden] */
// Fori di fissaggio della scheda, misurati dal suo angolo (si modificano qui)
fori_scheda = [];
// Distanziali della scheda
diametro_distanziale = 6;
diametro_foro_distanziale = 2.5;
parte = parte_scelta; // copia, così -D 'parte="..."' funziona anche con i set di parametri
e = 0.01;
usa_guarnizione = guarnizione && viti;
ingombro_colonna = viti ? diametro_colonna + gioco : 0;
interno = [pcb_lunghezza + 2 * gioco + 2 * ingombro_colonna, pcb_larghezza + 2 * gioco,
           spazio_sotto + pcb_spessore + spazio_sopra];
esterno = [interno[0] + 2 * parete, interno[1] + 2 * parete, interno[2] + fondo];
origine_scheda = [parete + gioco + ingombro_colonna, parete + gioco];
sopra_colonne = usa_guarnizione ? 0.75 * spessore_guarnizione : 0; // la guarnizione si schiaccia del 25%
incastro = min(parete / 2, 1); // le colonne entrano nelle pareti: niente spigoli solo appoggiati
centri_colonne = [for (x = [parete + diametro_colonna / 2 - incastro, esterno[0] - parete - diametro_colonna / 2 + incastro])
                  for (y = [parete + diametro_colonna / 2 - incastro, esterno[1] - parete - diametro_colonna / 2 + incastro]) [x, y]];
lung_aletta = foro_alette * 2.5;
larg_aletta = min(foro_alette * 3, esterno[1]);
sp_aletta = max(fondo, 3);
z_pressacavo = fondo + spazio_sotto + pcb_spessore + spazio_sopra / 2;
x_antenna = posizione_antenna == "sinistra" ? parete + ingombro_colonna + foro_antenna
          : posizione_antenna == "destra" ? esterno[0] - parete - ingombro_colonna - foro_antenna : esterno[0] / 2;

module blocco(dim, r) {
  if (r <= 0) cube(dim);
  else hull() for (x = [r, dim[0] - r]) for (y = [r, dim[1] - r]) translate([x, y, 0]) cylinder(r = r, h = dim[2]);
}

module aletta(foro) {
  if (foro) translate([lung_aletta - larg_aletta / 2, 0, -e]) cylinder(d = foro_alette, h = sp_aletta + 2 * e);
  else hull() {
    translate([-raggio - e, -larg_aletta / 2, 0]) cube([raggio + e, larg_aletta, sp_aletta]);
    translate([lung_aletta - larg_aletta / 2, 0, 0]) cylinder(d = larg_aletta, h = sp_aletta);
  }
}

module alette_tutte(foro) {
  translate([esterno[0], esterno[1] / 2, 0]) aletta(foro);
  translate([0, esterno[1] / 2, 0]) mirror([1, 0, 0]) aletta(foro);
}

module foro_laterale() {
  spostamenti = numero_pressacavi == 2 ? [-distanza_pressacavi / 2, distanza_pressacavi / 2] : [0];
  if (foro_pressacavo > 0) for (d = spostamenti) {
    if (lato_pressacavo == "sinistra") translate([-e, esterno[1] / 2 + d, z_pressacavo]) rotate([0, 90, 0]) cylinder(d = foro_pressacavo, h = parete + 2 * e);
    if (lato_pressacavo == "destra") translate([esterno[0] - parete - e, esterno[1] / 2 + d, z_pressacavo]) rotate([0, 90, 0]) cylinder(d = foro_pressacavo, h = parete + 2 * e);
    if (lato_pressacavo == "davanti") translate([esterno[0] / 2 + d, -e, z_pressacavo]) rotate([-90, 0, 0]) cylinder(d = foro_pressacavo, h = parete + 2 * e);
    if (lato_pressacavo == "dietro") translate([esterno[0] / 2 + d, esterno[1] - parete - e, z_pressacavo]) rotate([-90, 0, 0]) cylinder(d = foro_pressacavo, h = parete + 2 * e);
  }
}

module scatola() {
  difference() {
    union() {
      blocco(esterno, raggio);
      if (alette) alette_tutte(false);
    }
    translate([parete, parete, fondo]) blocco([interno[0], interno[1], interno[2] + 1], max(raggio - parete, 0));
    foro_laterale();
    if (foro_scarico > 0) translate([origine_scheda[0] / 2 + parete / 2, esterno[1] / 2, -e]) cylinder(d = foro_scarico, h = fondo + 2 * e);
    if (alette) alette_tutte(true);
  }
  for (p = fori_scheda) translate([origine_scheda[0] + p[0], origine_scheda[1] + p[1], fondo - e])
    difference() {
      cylinder(d = diametro_distanziale, h = spazio_sotto + e);
      translate([0, 0, 1]) cylinder(d = diametro_foro_distanziale, h = spazio_sotto);
    }
  if (viti) intersection() {
    translate([0, 0, fondo - e]) blocco([esterno[0], esterno[1], interno[2] + sopra_colonne + e], raggio);
    for (c = centri_colonne) translate([c[0], c[1], fondo - e])
      difference() {
        cylinder(d = diametro_colonna, h = interno[2] + sopra_colonne + e);
        translate([0, 0, interno[2] + sopra_colonne - min(10, interno[2] - 1)]) cylinder(d = diametro_foro_colonna, h = min(10, interno[2] - 1) + 2 * e);
      }
  }
}

module coperchio() {
  r_bordo = max(raggio - parete - gioco_coperchio, 0);
  dim_bordo = [interno[0] - 2 * gioco_coperchio, interno[1] - 2 * gioco_coperchio];
  difference() {
    union() {
      blocco([esterno[0], esterno[1], fondo], raggio);
      translate([parete + gioco_coperchio, parete + gioco_coperchio, fondo - e]) difference() {
        blocco([dim_bordo[0], dim_bordo[1], bordo_coperchio + e], r_bordo);
        translate([spessore_bordo, spessore_bordo, -e])
          blocco([dim_bordo[0] - 2 * spessore_bordo, dim_bordo[1] - 2 * spessore_bordo, bordo_coperchio + 3 * e], max(r_bordo - spessore_bordo, 0));
      }
    }
    if (viti) for (c = centri_colonne) {
      translate([c[0], c[1], fondo]) cylinder(d = diametro_colonna + 2 * gioco_coperchio, h = bordo_coperchio + 1);
      translate([c[0], c[1], -e]) cylinder(d = diametro_vite, h = fondo + 2 * e);
    }
    if (foro_antenna > 0) translate([x_antenna, esterno[1] / 2, -e]) cylinder(d = foro_antenna, h = fondo + 2 * e);
  }
}

module guarnizione_tpu() {
  difference() {
    blocco([esterno[0], esterno[1], spessore_guarnizione], raggio);
    translate([parete, parete, -e]) blocco([interno[0], interno[1], spessore_guarnizione + 2 * e], max(raggio - parete, 0));
  }
}

if (parte == "scatola" || parte == "tutto") scatola();
if (parte == "coperchio") coperchio();
if (parte == "tutto") translate([esterno[0] + lung_aletta + 10, 0, 0]) coperchio();
if (usa_guarnizione && parte == "guarnizione") guarnizione_tpu();
if (usa_guarnizione && parte == "tutto") translate([0, esterno[1] + 10, 0]) guarnizione_tpu();
