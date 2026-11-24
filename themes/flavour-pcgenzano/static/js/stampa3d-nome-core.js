/*
  Nome e cognome sugli oggetti della stampa 3D: calcolo puro, senza pagina (lo usano il sito,
  stampa3d-nome.js, e la prova scripts/prova-stampa3d-nome.mjs).
  Prende il file STL del nominativo, aggiunge una riga con nome e cognome nella zona libera indicata
  in data/stampa_3d.yaml (anteprima.nome: zona [x0, y0, x1, y1] e lato "fronte" o "retro") e restituisce
  il file STL nuovo, in un solo pezzo chiuso. Sul fronte la riga è in rilievo come le altre scritte; sul
  retro è incisa e scritta a specchio, così si legge girando l'oggetto. Le coordinate della zona sono
  quelle della vista (oggetto con le scritte verso l'alto), come per la bandiera.
  Carattere: Liberation Sans Bold, lo stesso dei modelli OpenSCAD («size» di OpenSCAD = corpo × 0,72).
  Sintassi entro ECMAScript 2018.
*/

export const ALTEZZE = [5.5, 5, 4.5, 4];        // «size» di OpenSCAD, dalla più grande alla più piccola
export const MAX_CARATTERI = 32;
const PROFONDITA_RETRO = 0.6;                    // incisione sul retro, in mm (3 strati da 0,2 mm)

/* ---------- STL ---------- */

export function leggiStl(buf) {
  const dv = new DataView(buf);
  const n = dv.getUint32(80, true);
  if (84 + n * 50 !== buf.byteLength) throw new Error('file STL non binario');
  const pos = new Float32Array(n * 9);
  for (let i = 0; i < n; i++) {
    const o = 84 + i * 50 + 12;
    for (let k = 0; k < 9; k++) pos[i * 9 + k] = dv.getFloat32(o + k * 4, true);
  }
  return pos;
}

export function scriviStl(vert, tri) {
  const n = tri.length / 3;
  const buf = new ArrayBuffer(84 + n * 50);
  const dv = new DataView(buf);
  const intest = 'Protezione Civile Genzano di Roma - stampa 3D';
  for (let i = 0; i < intest.length && i < 80; i++) dv.setUint8(i, intest.charCodeAt(i));
  dv.setUint32(80, n, true);
  for (let t = 0; t < n; t++) {
    const o = 84 + t * 50;
    const p = [0, 1, 2].map(k => [vert[tri[t * 3 + k] * 3], vert[tri[t * 3 + k] * 3 + 1], vert[tri[t * 3 + k] * 3 + 2]]);
    const u = [p[1][0] - p[0][0], p[1][1] - p[0][1], p[1][2] - p[0][2]];
    const v = [p[2][0] - p[0][0], p[2][1] - p[0][1], p[2][2] - p[0][2]];
    let nx = u[1] * v[2] - u[2] * v[1], ny = u[2] * v[0] - u[0] * v[2], nz = u[0] * v[1] - u[1] * v[0];
    const l = Math.hypot(nx, ny, nz) || 1;
    nx /= l; ny /= l; nz /= l;
    dv.setFloat32(o, nx, true); dv.setFloat32(o + 4, ny, true); dv.setFloat32(o + 8, nz, true);
    for (let k = 0; k < 3; k++) for (let c = 0; c < 3; c++) dv.setFloat32(o + 12 + k * 12 + c * 4, p[k][c], true);
  }
  return buf;
}

/* ---------- Dalla posizione di stampa alla vista e ritorno ---------- */
// fianco: pezzo stampato in piedi sul lato sinistro; assi: rotazione che porta le scritte in alto.

export function versoVista(p, a) {
  let x = p[0], y = p[1], z = p[2];
  if (typeof a.fianco === 'number') { const xs = x; x = z + a.fianco; z = -xs; }
  if (Array.isArray(a.assi)) {
    const q = [x, y, z];
    x = a.assi[0][0] * q[0] + a.assi[0][1] * q[1] + a.assi[0][2] * q[2];
    y = a.assi[1][0] * q[0] + a.assi[1][1] * q[1] + a.assi[1][2] * q[2];
    z = a.assi[2][0] * q[0] + a.assi[2][1] * q[1] + a.assi[2][2] * q[2];
  }
  return [x, y, z];
}

export function versoStampa(p, a) {
  let x = p[0], y = p[1], z = p[2];
  if (Array.isArray(a.assi)) {                   // matrice di rotazione: l'inversa è la trasposta
    const q = [x, y, z];
    x = a.assi[0][0] * q[0] + a.assi[1][0] * q[1] + a.assi[2][0] * q[2];
    y = a.assi[0][1] * q[0] + a.assi[1][1] * q[1] + a.assi[2][1] * q[2];
    z = a.assi[0][2] * q[0] + a.assi[1][2] * q[1] + a.assi[2][2] * q[2];
  }
  if (typeof a.fianco === 'number') { const xv = x; x = -z; z = xv - a.fianco; }
  return [x, y, z];
}

/* Quota della faccia con le scritte (vista): quella indicata nel modello o la faccia in alto più ampia. */
export function quotaScritte(posVista, a) {
  if (typeof a.quota_scritte === 'number') return a.quota_scritte;
  const aree = new Map();
  for (let t = 0; t < posVista.length; t += 9) {
    const z0 = posVista[t + 2];
    if (Math.abs(z0 - posVista[t + 5]) > 1e-3 || Math.abs(z0 - posVista[t + 8]) > 1e-3) continue;
    const nz = (posVista[t + 3] - posVista[t]) * (posVista[t + 7] - posVista[t + 1]) - (posVista[t + 4] - posVista[t + 1]) * (posVista[t + 6] - posVista[t]);
    if (nz <= 0) continue;
    const k = z0.toFixed(2);
    aree.set(k, (aree.get(k) || 0) + nz);
  }
  let best = 0, zb = 0;
  aree.forEach((v, k) => { if (v > best) { best = v; zb = parseFloat(k); } });
  return zb;
}

/* ---------- Testo ---------- */

export function pulisci(testo) {
  return String(testo || '').replace(/\s+/g, ' ').trim();
}

/* Contorni del testo in mm, centrati in (0, 0), y verso l'alto, a specchio se richiesto. */
function contorni(font, testo, size, specchio) {
  const corpo = size / 0.72;
  const path = font.getPath(testo, 0, 0, corpo);
  const poligoni = [];
  let cur = null, px = 0, py = 0;
  const passi = 8;
  const punto = (x, y) => { cur.push([x, -y]); px = x; py = y; };
  path.commands.forEach(c => {
    if (c.type === 'M') { cur = []; poligoni.push(cur); punto(c.x, c.y); }
    else if (c.type === 'L') punto(c.x, c.y);
    else if (c.type === 'Q') {
      const x0 = px, y0 = py;
      for (let i = 1; i <= passi; i++) {
        const t = i / passi, u = 1 - t;
        punto(u * u * x0 + 2 * u * t * c.x1 + t * t * c.x, u * u * y0 + 2 * u * t * c.y1 + t * t * c.y);
      }
    } else if (c.type === 'C') {
      const x0 = px, y0 = py;
      for (let i = 1; i <= passi; i++) {
        const t = i / passi, u = 1 - t;
        punto(u * u * u * x0 + 3 * u * u * t * c.x1 + 3 * u * t * t * c.x2 + t * t * t * c.x,
          u * u * u * y0 + 3 * u * u * t * c.y1 + 3 * u * t * t * c.y2 + t * t * t * c.y);
      }
    }
  });
  const validi = poligoni.filter(p => p.length >= 3);
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
  validi.forEach(p => p.forEach(q => { x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]); }));
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const out = validi.map(p => {
    const q = p.map(v => [specchio ? -(v[0] - cx) : v[0] - cx, v[1] - cy]);
    return specchio ? q.reverse() : q;            // a specchio il verso dei contorni si inverte
  });
  return { poligoni: out, larghezza: x1 - x0, altezza: y1 - y0 };
}

/* Sceglie la misura più grande che entra nella zona (con 0,5 mm di margine per lato). */
export function misuraTesto(font, testo, zona) {
  const w = zona[2] - zona[0] - 1, h = zona[3] - zona[1] - 1;
  for (const size of ALTEZZE) {
    const c = contorni(font, testo, size, false);
    if (c.larghezza <= w && c.altezza <= h) return size;
  }
  return 0;
}

/* ---------- Oggetto con il nome ---------- */

/*
  stl: ArrayBuffer del file del nominativo; a: anteprima dell'oggetto (data/stampa_3d.yaml);
  testo: nome e cognome; font: carattere di opentype.js; M: modulo manifold-3d già pronto (setup fatto).
  Restituisce { stl: ArrayBuffer, pos: Float32Array (posizione di stampa), size, lato }.
*/
export function conNome(stl, a, testo, font, M) {
  const cfg = a.nome;
  if (!cfg || !Array.isArray(cfg.zona)) throw new Error('Questo oggetto non ha lo spazio per nome e cognome.');
  testo = pulisci(testo);
  if (!testo) throw new Error('Scrivi nome e cognome.');
  if (testo.length > MAX_CARATTERI) throw new Error(`Scrivi al massimo ${MAX_CARATTERI} caratteri.`);
  const mancanti = Array.from(testo).filter(ch => ch !== ' ' && font.charToGlyphIndex(ch) === 0);
  if (mancanti.length) throw new Error(`Questi caratteri non si possono stampare: ${Array.from(new Set(mancanti)).join(' ')}`);
  const zona = cfg.zona, retro = cfg.lato === 'retro';
  const size = misuraTesto(font, testo, zona);
  if (!size) throw new Error('Nome e cognome non entrano: scrivi solo l\'iniziale del nome, per esempio «M. Rossi».');

  const pos = leggiStl(stl);
  // posizione di vista, per la quota della faccia
  const vista = new Float32Array(pos.length);
  for (let i = 0; i < pos.length; i += 3) {
    const v = versoVista([pos[i], pos[i + 1], pos[i + 2]], a);
    vista[i] = v[0]; vista[i + 1] = v[1]; vista[i + 2] = v[2];
  }
  let zmin = Infinity;
  for (let i = 2; i < vista.length; i += 3) zmin = Math.min(zmin, vista[i]);
  const ril = a.rilievo_mm || 1;
  const z0 = retro ? zmin - 0.01 : quotaScritte(vista, a) - 0.01;
  const altezza = retro ? PROFONDITA_RETRO + 0.01 : ril + 0.01;

  // il testo, estruso nella vista e riportato nella posizione di stampa
  const c = contorni(font, testo, size, retro);
  const cx = (zona[0] + zona[2]) / 2, cy = (zona[1] + zona[3]) / 2;
  const sezione = new M.CrossSection(c.poligoni, 'NonZero').translate([cx, cy]);
  const solido = sezione.extrude(altezza).translate([0, 0, z0]);
  const tm = solido.getMesh();
  const tv = tm.vertProperties, np = tm.numProp;
  const tvs = new Float32Array(tv.length / np * 3);
  for (let i = 0, j = 0; i < tv.length; i += np, j += 3) {
    const p = versoStampa([tv[i], tv[i + 1], tv[i + 2]], a);
    tvs[j] = p[0]; tvs[j + 1] = p[1]; tvs[j + 2] = p[2];
  }
  // il versoStampa può invertire l'orientamento solo con assi impropri: le rotazioni lo conservano
  const testoM = new M.Manifold(new M.Mesh({ numProp: 3, vertProperties: tvs, triVerts: tm.triVerts }));

  // l'oggetto: triangoli del file con i vertici uniti
  const mappa = new Map(), vert = [], triV = new Uint32Array(pos.length / 3);
  for (let i = 0; i < pos.length; i += 3) {
    const k = `${pos[i].toFixed(4)},${pos[i + 1].toFixed(4)},${pos[i + 2].toFixed(4)}`;
    let idx = mappa.get(k);
    if (idx === undefined) { idx = vert.length / 3; mappa.set(k, idx); vert.push(pos[i], pos[i + 1], pos[i + 2]); }
    triV[i / 3] = idx;
  }
  const mesh = new M.Mesh({ numProp: 3, vertProperties: new Float32Array(vert), triVerts: triV });
  mesh.merge();
  const base = new M.Manifold(mesh);
  const unito = retro ? base.subtract(testoM) : base.add(testoM);
  if (unito.status && unito.status() !== 'NoError' && unito.status() !== 0) throw new Error('Il file non si è potuto preparare.');
  const r = unito.getMesh();
  const rv = r.vertProperties, rn = r.numProp;
  const v3 = new Float32Array(rv.length / rn * 3);
  for (let i = 0, j = 0; i < rv.length; i += rn, j += 3) { v3[j] = rv[i]; v3[j + 1] = rv[i + 1]; v3[j + 2] = rv[i + 2]; }
  const fuori = scriviStl(v3, r.triVerts);
  [sezione, solido, testoM, base, unito].forEach(o => { try { o.delete(); } catch (e) { /* già liberato */ } });
  return { stl: fuori, pos: leggiStl(fuori), size, lato: retro ? 'retro' : 'fronte' };
}
