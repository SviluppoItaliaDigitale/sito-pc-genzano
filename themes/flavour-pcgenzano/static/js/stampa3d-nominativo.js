/*
  Oggetti da stampare con il nominativo (/stampa-3d/nominativi/): ricerca del numero, vista in 3D
  del file vero (si gira da ogni lato con dito, mouse, tastiera o pulsanti), scaricamento.
  Dati dallo shortcode stampa3d-nominativo (blocco JSON #s3d-dati, da data/stampa_3d.yaml).
  Vista con three.js (r160, copia locale in vendor/three, licenza MIT). Le scritte in rilievo
  si colorano dall'altezza: tutto ciò che sta sopra la base è del secondo colore.
  Nessuna richiesta fuori dal sito; nulla viene salvato.
*/
import * as THREE from '../vendor/three/three.module.min.js';
import { OrbitControls } from '../vendor/three/OrbitControls.js';

const DATI = JSON.parse(document.getElementById('s3d-dati').textContent);
const form = document.getElementById('s3d-form');
const campo = document.getElementById('s3d-numero');
const errore = document.getElementById('s3d-errore');
const esito = document.getElementById('s3d-esito');
const pannelli = {};
// Colori della bandiera nella vista (verde, bianco, rosso della bandiera italiana)
const TRICOLORE = ['#009246', '#ffffff', '#ce2b37'].map(c => new THREE.Color(c));

const nome3 = n => String(n).padStart(3, '0');
const percorso = (id, n, est) => `${DATI.base}${id}/${DATI.prefisso.toLowerCase()}-${nome3(n)}.${est}`;

function leggiNumero(testo) {
  const m = String(testo).match(/\d+/);
  if (!m) return null;
  const n = parseInt(m[0], 10);
  return n >= DATI.primo && n <= DATI.ultimo ? n : NaN;
}

function mostraErrore(msg) {
  errore.textContent = msg;
  campo.setAttribute('aria-invalid', msg ? 'true' : 'false');
}

function cerca(n, sposta) {
  const nominativo = `${DATI.prefisso} ${n}`;
  esito.querySelectorAll('[data-s3d="nominativo"]').forEach(e => { e.textContent = nominativo; });
  DATI.oggetti.forEach(o => {
    const sez = esito.querySelector(`[data-oggetto="${o.id}"]`);
    if (!sez) return;
    const file = `${DATI.prefisso}-${n}-${o.id}.stl`;
    const a = sez.querySelector('[data-s3d="scarica"]');
    a.href = percorso(o.id, n, 'stl');
    a.setAttribute('download', file);
    sez.querySelectorAll('[data-s3d="file"]').forEach(e => { e.textContent = file; });
    const img = sez.querySelector('[data-s3d="immagine"]');
    img.src = percorso(o.id, n, 'webp');
    img.alt = `${o.nome} blu con la scritta ${nominativo} e, sotto, Protezione Civile Genzano di Roma.`;
    pannello(o, sez).nuovoFile(percorso(o.id, n, 'stl'));
  });
  esito.hidden = false;
  scegliVisibile();
  try { history.replaceState(null, '', `#${DATI.prefisso.toLowerCase()}-${n}`); } catch (e) { /* indirizzo non modificabile */ }
  if (sposta) { esito.focus(); esito.scrollIntoView({ block: 'start' }); }
}

form.addEventListener('submit', ev => {
  ev.preventDefault();
  const n = leggiNumero(campo.value);
  if (n === null) { mostraErrore(`Scrivi il numero del tuo nominativo, per esempio 57.`); campo.focus(); return; }
  if (Number.isNaN(n)) { mostraErrore(`Non c'è questo numero. Scrivi un numero da ${DATI.primo} a ${DATI.ultimo}.`); campo.focus(); return; }
  mostraErrore('');
  cerca(n, true);
});

document.getElementById('s3d-altro').addEventListener('click', () => {
  campo.value = '';
  campo.focus();
  form.scrollIntoView({ block: 'center' });
});

/* ---------- Vista in 3D ---------- */

function leggiStl(buf) {
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

/* Quota della faccia su cui stanno le scritte: la superficie orizzontale rivolta in alto più ampia.
   Le scritte sono ciò che sta sopra di lei per l'altezza del rilievo; ganci e supporti, che salgono
   più in alto, restano del colore della base. */
function quotaBase(pos) {
  const aree = new Map();
  for (let t = 0; t < pos.length; t += 9) {
    const z0 = pos[t + 2], z1 = pos[t + 5], z2 = pos[t + 8];
    if (Math.abs(z0 - z1) > 1e-3 || Math.abs(z0 - z2) > 1e-3) continue;
    const ux = pos[t + 3] - pos[t], uy = pos[t + 4] - pos[t + 1], vx = pos[t + 6] - pos[t], vy = pos[t + 7] - pos[t + 1];
    const nz = ux * vy - uy * vx;            // doppia area con segno: positiva se la faccia guarda in alto
    if (nz <= 0) continue;
    const k = z0.toFixed(2);
    aree.set(k, (aree.get(k) || 0) + nz);
  }
  let best = 0, zb = 0;
  aree.forEach((a, k) => { if (a > best) { best = a; zb = parseFloat(k); } });
  return zb;
}

/* Una sola vista in 3D per tutta la pagina. Sette viste accese insieme (una per oggetto, ognuna
   ridisegnata 60 volte al secondo) esaurivano la memoria grafica dei telefoni e il browser chiudeva
   la pagina. Ora c'è un solo disegnatore: si sposta sull'oggetto che si sta guardando o toccando,
   disegna solo mentre l'oggetto si muove, e gli altri oggetti mostrano l'immagine. */
const tre = { renderer: null, scena: null, camera: null, controlli: null, mesh: null,
  attivo: null, rotto: false, gira: false, fermo: 0, forza: false };
const visibili = new Map();

function motore() {
  if (tre.renderer || tre.rotto) return !tre.rotto;
  try {
    tre.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
  } catch (e) { tre.rotto = true; return false; }
  const r = tre.renderer;
  r.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
  r.domElement.setAttribute('aria-hidden', 'true');
  r.domElement.className = 's3d-tela';
  r.domElement.addEventListener('webglcontextlost', ev => {
    ev.preventDefault();
    tre.rotto = true;
    ferma();
    Object.values(pannelli).forEach(q => soloImmagine(q, 'La vista in 3D si è fermata: guarda l\'immagine.'));
  });
  tre.scena = new THREE.Scene();
  tre.scena.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 1.6));
  const luce = new THREE.DirectionalLight(0xffffff, 1.6);
  luce.position.set(-40, 60, 120);
  tre.scena.add(luce);
  tre.camera = new THREE.PerspectiveCamera(30, 2, 1, 2000);
  tre.mesh = new THREE.Mesh(new THREE.BufferGeometry(),
    new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6, metalness: 0 }));
  tre.mesh.visible = false;
  tre.scena.add(tre.mesh);
  const c = new OrbitControls(tre.camera, r.domElement);
  c.enablePan = false;
  c.enableDamping = true;
  c.dampingFactor = 0.1;
  c.minPolarAngle = 0;
  c.maxPolarAngle = Math.PI;
  c.addEventListener('start', disegna);
  c.addEventListener('change', disegna);
  tre.controlli = c;
  document.addEventListener('visibilitychange', () => { if (!document.hidden) disegna(); });
  return true;
}

/* Disegna finché l'oggetto si muove (anche per l'inerzia), poi si ferma da solo. */
function passo() {
  if (document.hidden || esito.hidden || !tre.attivo || !tre.mesh.visible) { ferma(); return; }
  const mosso = tre.controlli.update();
  if (mosso || tre.forza) {
    tre.renderer.render(tre.scena, tre.camera);
    tre.forza = false;
    tre.fermo = 0;
  } else if (++tre.fermo > 30) ferma();
}
function disegna() {
  if (!tre.renderer || tre.rotto) return;
  tre.forza = true;
  if (!tre.gira) { tre.gira = true; tre.fermo = 0; tre.renderer.setAnimationLoop(passo); }
}
function ferma() {
  if (tre.renderer && tre.gira) tre.renderer.setAnimationLoop(null);
  tre.gira = false;
}

function soloImmagine(q, testo) {
  q.box.classList.remove('s3d-pronto');
  q.img.classList.remove('visually-hidden');
  q.comandi.hidden = true;
  q.stato.hidden = !testo;
  q.stato.textContent = testo || '';
}

function misura() {
  const q = tre.attivo;
  if (!q || !tre.renderer) return;
  const w = q.box.clientWidth, h = q.box.clientHeight;
  if (!w || !h) return;
  tre.renderer.setSize(w, h, false);
  tre.camera.aspect = w / h;
  tre.camera.updateProjectionMatrix();
  disegna();
}
const osservaMisure = typeof ResizeObserver === 'function' ? new ResizeObserver(misura) : null;

/* Accende la vista sull'oggetto più visibile dello schermo. */
function scegliVisibile() {
  let meglio = null, quota = 0.55;
  visibili.forEach((r, id) => { if (r > quota) { quota = r; meglio = pannelli[id]; } });
  if (meglio && (!tre.attivo || (visibili.get(tre.attivo.o.id) || 0) < 0.3)) attiva(meglio);
}
const osservaSchermo = typeof IntersectionObserver === 'function'
  ? new IntersectionObserver(voci => {
      voci.forEach(v => visibili.set(v.target.dataset.s3dId, v.intersectionRatio));
      if (!esito.hidden) scegliVisibile();
    }, { threshold: [0, 0.3, 0.55, 0.8, 1] })
  : null;

function posiziona(dir) {
  const q = tre.attivo;
  tre.camera.position.set(0, 0, dir * q.distanza);
  tre.camera.up.set(0, 1, 0);
  tre.controlli.target.set(0, 0, 0);
  tre.controlli.update();
  disegna();
}

function ruota(verso) {
  const c = tre.controlli;
  const off = tre.camera.position.clone().sub(c.target);
  const s = new THREE.Spherical().setFromVector3(off);
  if (verso === 'sinistra') s.theta -= Math.PI / 6;
  if (verso === 'destra') s.theta += Math.PI / 6;
  if (verso === 'su') s.phi = Math.max(0.01, s.phi - Math.PI / 9);
  if (verso === 'giu') s.phi = Math.min(Math.PI - 0.01, s.phi + Math.PI / 9);
  tre.camera.position.copy(c.target).add(new THREE.Vector3().setFromSpherical(s));
  c.update();
  disegna();
}

function attiva(q, poi) {
  if (!motore()) { soloImmagine(q, 'Il tuo browser non mostra la vista in 3D: guarda l\'immagine.'); return; }
  if (tre.attivo === q) { if (poi && q.geo) poi(); return; }
  const prima = tre.attivo;
  if (prima) {
    prima.cam = { pos: tre.camera.position.clone(), up: tre.camera.up.clone() };
    if (prima.geo) prima.geo.dispose();            // libera la memoria grafica; i dati restano
    soloImmagine(prima, '');
    if (!tre.rotto) prima.comandi.hidden = false;  // i pulsanti accendono di nuovo la vista
    if (osservaMisure) osservaMisure.unobserve(prima.box);
  }
  tre.attivo = q;
  tre.mesh.visible = false;
  q.box.appendChild(tre.renderer.domElement);
  if (osservaMisure) osservaMisure.observe(q.box);
  if (q.geo) mostra(q, poi); else carica(q, poi);
}

function mostra(q, poi) {
  tre.mesh.geometry = q.geo;
  tre.mesh.visible = true;
  const c = tre.controlli;
  c.minDistance = q.distanza * 0.4;
  c.maxDistance = q.distanza * 2.5;
  misura();
  if (q.cam) {
    tre.camera.position.copy(q.cam.pos);
    tre.camera.up.copy(q.cam.up);
    c.target.set(0, 0, 0);
    c.update();
  } else posiziona(1);
  q.img.classList.add('visually-hidden');          // resta per i lettori di schermo
  q.stato.hidden = true;
  q.comandi.hidden = false;
  q.box.classList.add('s3d-pronto');
  disegna();
  if (poi) poi();
}

async function carica(q, poi) {
  const mia = ++q.richiesta;
  const url = q.url;
  q.stato.hidden = false;
  q.stato.textContent = 'Sto preparando la vista in 3D…';
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(r.status);
    const pos = leggiStl(await r.arrayBuffer());
    const fianco = q.o.anteprima && q.o.anteprima.fianco;
    if (typeof fianco === 'number')                // file girato per la stampa di fianco: si rimette dritto
      for (let i = 0; i < pos.length; i += 3) { const xs = pos[i]; pos[i] = pos[i + 2] + fianco; pos[i + 2] = -xs; }
    if (mia !== q.richiesta || url !== q.url) return;
    q.geo = geometria(q.o, pos, q);
    q.geoUrl = url;
    q.cam = null;
    if (tre.attivo === q && !tre.rotto) mostra(q, poi);
  } catch (e) {
    if (mia !== q.richiesta) return;
    soloImmagine(q, 'La vista in 3D non si è caricata: guarda l\'immagine.');
  }
}

/* Targa da tavolo: la piastra con le scritte è inclinata; per riconoscere le scritte dall'altezza si
   riporta in piano (inclina = [angolo, taglio alla base, mezza altezza della piastra], dal modello). */
function coordinatePiastra(pos, inclina) {
  if (!inclina) return pos;
  const [gradi, calo, meta] = inclina, a = gradi * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
  const pc = new Float32Array(pos.length);
  for (let i = 0; i < pos.length; i += 3) {
    const y = pos[i + 1], z = pos[i + 2] + calo;
    pc[i] = pos[i]; pc[i + 1] = y * c + z * s - meta; pc[i + 2] = -y * s + z * c;
  }
  return pc;
}

function geometria(o, pos, q) {
  const col = o.anteprima || { base: '#1d4f9a', rilievo: '#f07d00' };
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.computeBoundingBox();
  const b = geo.boundingBox, c = new THREE.Vector3();
  b.getCenter(c);
  const ril = o.anteprima && o.anteprima.rilievo_mm ? o.anteprima.rilievo_mm : 1;
  // Coordinate per colorare le scritte: per la targa da tavolo, piastra davanti riportata in piano
  const pc = coordinatePiastra(pos, o.anteprima && o.anteprima.inclina);
  const zb = quotaBase(pc);
  const band = o.anteprima && o.anteprima.bandiera;
  const cb = new THREE.Color(col.base), cr = new THREE.Color(col.rilievo);
  const colori = new Float32Array(pos.length);
  for (let t = 0; t < pos.length; t += 9) {
    const zm = Math.max(pc[t + 2], pc[t + 5], pc[t + 8]);
    const alto = zm > zb + 0.01 && zm <= zb + ril + 0.02;
    let cc = alto ? cr : cb;
    if (alto && band) {
      const cx = (pc[t] + pc[t + 3] + pc[t + 6]) / 3, cy = (pc[t + 1] + pc[t + 4] + pc[t + 7]) / 3;
      const [x0, y0, x1, y1] = band;
      if (cx >= x0 - 0.1 && cx <= x1 + 0.1 && cy >= y0 - 0.1 && cy <= y1 + 0.1)
        cc = TRICOLORE[Math.min(2, Math.floor((cx - x0) / (x1 - x0) * 3))];
    }
    for (let k = 0; k < 9; k += 3) { colori[t + k] = cc.r; colori[t + k + 1] = cc.g; colori[t + k + 2] = cc.b; }
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colori, 3));
  geo.translate(-c.x, -c.y, -c.z);
  geo.computeVertexNormals();
  q.distanza = (b.max.x - b.min.x) * 0.5 / Math.tan(THREE.MathUtils.degToRad(15)) * 1.25;
  return geo;
}

function pannello(o, sez) {
  if (pannelli[o.id]) return pannelli[o.id];
  const q = {
    o, sez, url: '', geo: null, geoUrl: '', cam: null, distanza: 200, richiesta: 0,
    box: sez.querySelector('.s3d-visore'),
    img: sez.querySelector('[data-s3d="immagine"]'),
    stato: sez.querySelector('[data-s3d="caricamento"]'),
    comandi: sez.querySelector('[data-s3d="comandi"]'),
  };
  pannelli[o.id] = q;
  q.box.dataset.s3dId = o.id;
  q.box.addEventListener('pointerdown', () => { if (tre.attivo !== q && !tre.rotto) attiva(q); });
  q.comandi.addEventListener('click', ev => {
    const b = ev.target.closest('button');
    if (!b || tre.rotto) return;
    attiva(q, () => {
      if (b.dataset.ruota) ruota(b.dataset.ruota);
      if (b.dataset.vista) posiziona(b.dataset.vista === 'retro' ? -1 : 1);
    });
  });
  if (osservaSchermo) osservaSchermo.observe(q.box);
  q.nuovoFile = url => {
    q.url = url;
    if (q.geoUrl === url) return;
    if (q.geo) { q.geo.dispose(); q.geo = null; q.geoUrl = ''; }
    q.cam = null;
    if (tre.attivo === q) { tre.mesh.visible = false; carica(q); }
    else if (tre.rotto) soloImmagine(q, '');
    else {
      soloImmagine(q, '');
      q.comandi.hidden = false;
    }
  };
  return q;
}

/* Indirizzo con il nominativo (#alfa-57): la pagina lo cerca subito, così si può condividere. */
const daIndirizzo = location.hash.match(new RegExp(`^#${DATI.prefisso.toLowerCase()}-(\\d+)$`));
if (daIndirizzo) {
  const n = leggiNumero(daIndirizzo[1]);
  if (n && !Number.isNaN(n)) { campo.value = String(n); cerca(n, false); }
}
