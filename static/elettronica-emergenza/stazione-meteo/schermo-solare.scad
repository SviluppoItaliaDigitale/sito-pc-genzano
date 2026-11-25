// Schermo solare per il sensore BME280: piatti conici impilati su tre barre filettate
// Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma - www.protezionecivilegenzano.it
// Licenza: CC BY-NC-SA 4.0. Misure in millimetri. Si apre con OpenSCAD (gratuito).
// Parti da esportare una per volta (OpenSCAD 2021.01 o successivo):
//   openscad -o schermo-solare-piatto.stl -D 'parte="piatto"' schermo-solare.scad
//   openscad -o schermo-solare-cappello.stl -D 'parte="cappello"' schermo-solare.scad
//   openscad -o schermo-solare-base.stl -D 'parte="base"' schermo-solare.scad
// Stampa: ogni parte cosi' come esce dal file, con la faccia piana sul piatto.
// Pareti coniche a 45 gradi: si stampano senza supporti.
// Montaggio: base, poi i piatti (di solito 5), poi il cappello, infilati su tre
// barre filettate M5 in acciaio inox con un dado sopra e uno sotto.

/* [Parte] */
// Parte da mostrare o esportare
parte_scelta = "tutto"; // [tutto, piatto, cappello, base]

/* [Piatti] */
// Raggio esterno dei piatti e del cappello
raggio_esterno = 60; // [40:1:90]
// Raggio dell'apertura centrale dei piatti
raggio_apertura = 34; // [20:1:60]
// Spessore della parete conica, misurato perpendicolare alla parete
spessore_parete = 2; // [1.2:0.2:4]
// Altezza dei distanziali sopra le linguette (spazio d'aria fra i piatti)
altezza_distanziale = 15; // [8:1:30]
// Numero di piatti (solo per l'anteprima "tutto"; si stampano uno per volta)
numero_piatti = 5; // [2:1:8]

/* [Linguette e barre] */
// Spessore delle linguette
spessore_linguetta = 3; // [2:0.5:6]
// Foro per la barra filettata (M5: 5.5 di partenza, si regola con la prova)
foro_barra = 5.5; // [3:0.1:8]
// Diametro esterno dei distanziali
diametro_distanziale = 11; // [8:0.5:16]

/* [Base] */
// Spessore della base
spessore_base = 4; // [3:0.5:8]
// Altezza del tubo centrale che porta il cavo e il sensore
altezza_tubo = 40; // [10:1:80]
// Diametro esterno del tubo centrale
diametro_tubo = 12; // [8:0.5:20]
// Diametro interno del tubo (passaggio del cavo a 4 fili)
foro_tubo = 7; // [4:0.5:15]
// Lunghezza della staffa di fissaggio
lunghezza_staffa = 60; // [30:1:120]
// Foro delle viti della staffa
foro_staffa = 5.5; // [3:0.5:8]

/* [Qualità] */
// Segmenti dei cerchi (più alto = più liscio e più lento)
$fn = 96; // [32:8:160]

/* [Hidden] */
parte = parte_scelta; // copia, così -D 'parte="..."' funziona anche con i set di parametri
e = 0.01;
altezza_cono = raggio_esterno - raggio_apertura;          // 45 gradi
spessore_orizzontale = spessore_parete * sqrt(2);          // parete a 45 gradi
raggio_barre = raggio_esterno + diametro_distanziale / 2 + 1;
passo = spessore_linguetta + altezza_distanziale;          // distanza fra due piatti
angoli = [90, 210, 330];

// Parete conica: dal bordo esterno sul piatto sale verso il centro a 45 gradi.
module cono_aperto(r_basso, r_alto) {
  h = r_basso - r_alto;
  rotate_extrude() polygon([
    [r_basso - spessore_orizzontale, 0], [r_basso, 0],
    [r_alto, h], [r_alto - spessore_orizzontale, h]]);
}

// Cono chiuso in punta (cappello): stessa pendenza, finisce in un vertice.
module cono_chiuso(r_basso) {
  h = r_basso;
  rotate_extrude() polygon([
    [r_basso - spessore_orizzontale, 0], [r_basso, 0],
    [0, h], [0, h - spessore_orizzontale]]);
}

module linguette(con_distanziali) {
  for (a = angoli) rotate([0, 0, a]) difference() {
    union() {
      hull() {
        translate([raggio_esterno - spessore_orizzontale - 1, -diametro_distanziale / 2, 0])
          cube([e, diametro_distanziale, spessore_linguetta]);
        translate([raggio_barre, 0, 0]) cylinder(d = diametro_distanziale, h = spessore_linguetta);
      }
      if (con_distanziali) translate([raggio_barre, 0, 0])
        cylinder(d = diametro_distanziale, h = passo);
    }
    translate([raggio_barre, 0, -e]) cylinder(d = foro_barra, h = passo + 2 * e);
  }
}

module piatto() {
  difference() {
    union() {
      cono_aperto(raggio_esterno, raggio_apertura);
      linguette(true);
    }
    // i fori delle barre restano liberi anche dove il distanziale tocca il cono
    for (a = angoli) rotate([0, 0, a]) translate([raggio_barre, 0, -e]) cylinder(d = foro_barra, h = passo + 2 * e);
  }
}

module cappello() {
  difference() {
    union() {
      cono_chiuso(raggio_esterno);
      linguette(false);
    }
    for (a = angoli) rotate([0, 0, a]) translate([raggio_barre, 0, -e]) cylinder(d = foro_barra, h = passo + 2 * e);
  }
}

module base() {
  difference() {
    union() {
      // anello con la stessa apertura dei piatti e una traversa al centro
      difference() {
        cylinder(r = raggio_esterno, h = spessore_base);
        translate([0, 0, -e]) cylinder(r = raggio_apertura, h = spessore_base + 2 * e);
      }
      translate([-raggio_apertura - 1, -diametro_tubo / 2, 0])
        cube([2 * raggio_apertura + 2, diametro_tubo, spessore_base]);
      // tubo centrale: il cavo sale dentro, il sensore si lega in cima con una fascetta
      cylinder(d = diametro_tubo, h = spessore_base + altezza_tubo);
      // linguette con distanziali per il primo piatto
      for (a = angoli) rotate([0, 0, a]) {
        hull() {
          translate([raggio_esterno - 6, -diametro_distanziale / 2, 0]) cube([e, diametro_distanziale, spessore_base]);
          translate([raggio_barre, 0, 0]) cylinder(d = diametro_distanziale, h = spessore_base);
        }
        translate([raggio_barre, 0, 0]) cylinder(d = diametro_distanziale, h = spessore_base + altezza_distanziale);
      }
      // staffa per fissare lo schermo a un supporto con due viti
      translate([raggio_apertura, -15, 0]) cube([raggio_esterno - raggio_apertura + lunghezza_staffa, 30, spessore_base]);
    }
    translate([0, 0, -e]) cylinder(d = foro_tubo, h = spessore_base + altezza_tubo + 2 * e);
    for (a = angoli) rotate([0, 0, a])
      translate([raggio_barre, 0, -e]) cylinder(d = foro_barra, h = spessore_base + altezza_distanziale + 2 * e);
    for (x = [raggio_esterno + lunghezza_staffa * 0.35, raggio_esterno + lunghezza_staffa * 0.8])
      translate([x, 0, -e]) cylinder(d = foro_staffa, h = spessore_base + 2 * e);
  }
}

if (parte == "piatto") piatto();
if (parte == "cappello") cappello();
if (parte == "base") base();
if (parte == "tutto") {
  color("white") base();
  z0 = spessore_base + altezza_distanziale;
  for (i = [0 : numero_piatti - 1]) translate([0, 0, z0 + i * passo]) color("lightgray") piatto();
  translate([0, 0, z0 + numero_piatti * passo]) color("white") cappello();
}
