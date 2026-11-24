/*
  Vista in 3D degli oggetti da stampare (/stampa-3d/<oggetto>/): mostra il file STL vero, che si gira
  da ogni lato con dito, mouse, tastiera o pulsanti. Il file da mostrare lo dice stampa3d.js
  (window.pcgzS3dFile e l'evento «s3d:file»), che va caricato prima di questo.
  three.js r160 (copia locale in vendor/three, licenza MIT). La vista parte quando entra nello schermo
  e disegna solo mentre l'oggetto si muove. Le scritte in rilievo si colorano dall'altezza.
*/
import * as THREE from '../vendor/three/three.module.min.js';
import { OrbitControls } from '../vendor/three/OrbitControls.js';

const DATI = JSON.parse(document.getElementById('s3d-dati').textContent);
const O = DATI.oggetto;
const vista = {
  box: document.querySelector('.s3d-visore'),
  img: document.querySelector('[data-s3d="immagine"]'),
  carica: document.querySelector('[data-s3d="caricamento"]'),
  comandi: document.querySelector('[data-s3d="comandi"]'),
};


// Colori della bandiera nella vista (verde, bianco, rosso della bandiera italiana)
const TRICOLORE_HEX = ['#009246', '#ffffff', '#ce2b37'];

const tre = {
  renderer: null, scena: null, camera: null, controlli: null, mesh: null,
  url: '', geoUrl: '', richiesta: 0, distanza: 200, rotto: false, gira: false, fermo: 0, forza: false,
  visibile: false, avviato: false,
  nuovoFile(url) {
    this.url = url;
    if (this.avviato && !this.rotto && this.geoUrl !== url) carica();
  },
};

function soloImmagine(testo) {
  vista.box.classList.remove('s3d-pronto');
  vista.img.classList.remove('visually-hidden');
  vista.comandi.hidden = true;
  vista.carica.hidden = !testo;
  vista.carica.textContent = testo || '';
}

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

/* Quota della faccia su cui stanno le scritte: la superficie orizzontale rivolta in alto più ampia,
   salvo quando il modello la indica (quota_scritte, per esempio il porta tesserino, dove la superficie
   più ampia è il fondo della tasca). */
function quotaBase(pos) {
  const a = O.anteprima || {};
  if (typeof a.quota_scritte === 'number') return a.quota_scritte;
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
  aree.forEach((v, k) => { if (v > best) { best = v; zb = parseFloat(k); } });
  return zb;
}

/* Il file è nella posizione di stampa: si rimette come lo si guarda. fianco = pezzo stampato in piedi
   sul lato sinistro; assi = rotazione che porta le scritte verso l'alto (fischietto). */
function orienta(pos) {
  const a = O.anteprima || {};
  if (typeof a.fianco === 'number')
    for (let i = 0; i < pos.length; i += 3) { const xs = pos[i]; pos[i] = pos[i + 2] + a.fianco; pos[i + 2] = -xs; }
  if (Array.isArray(a.assi))
    for (let i = 0; i < pos.length; i += 3) {
      const p = [pos[i], pos[i + 1], pos[i + 2]];
      for (let k = 0; k < 3; k++) pos[i + k] = a.assi[k][0] * p[0] + a.assi[k][1] * p[1] + a.assi[k][2] * p[2];
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

function geometria(pos) {
  const a = O.anteprima || { base: '#1d4f9a', rilievo: '#f07d00' };
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.computeBoundingBox();
  const b = geo.boundingBox, c = new THREE.Vector3();
  b.getCenter(c);
  const ril = a.rilievo_mm || 1;
  const pc = coordinatePiastra(pos, a.inclina);
  const zb = quotaBase(pc);
  const tri = TRICOLORE_HEX.map(h => new THREE.Color(h));
  const cb = new THREE.Color(a.base), cr = new THREE.Color(a.rilievo);
  const colori = new Float32Array(pos.length);
  // Nome e cognome incisi sul retro (stampa3d-nome.js): fondo e pareti dell'incisione si colorano come le scritte
  const retro = a.nome && a.nome.lato === 'retro' && Array.isArray(a.nome.zona) ? a.nome.zona : null;
  const zmin = b.min.z;
  for (let t = 0; t < pos.length; t += 9) {
    const zm = Math.max(pc[t + 2], pc[t + 5], pc[t + 8]);
    const alto = zm > zb + 0.01 && zm <= zb + ril + 0.02;
    let cc = alto ? cr : cb;
    if (retro && zm > zmin + 0.01 && zm <= zmin + 0.7) {
      const cx = (pc[t] + pc[t + 3] + pc[t + 6]) / 3, cy = (pc[t + 1] + pc[t + 4] + pc[t + 7]) / 3;
      if (cx >= retro[0] - 0.5 && cx <= retro[2] + 0.5 && cy >= retro[1] - 0.5 && cy <= retro[3] + 0.5) cc = cr;
    }
    if (alto && a.bandiera) {
      const cx = (pc[t] + pc[t + 3] + pc[t + 6]) / 3, cy = (pc[t + 1] + pc[t + 4] + pc[t + 7]) / 3;
      const [x0, y0, x1, y1] = a.bandiera;
      if (cx >= x0 - 0.1 && cx <= x1 + 0.1 && cy >= y0 - 0.1 && cy <= y1 + 0.1)
        cc = tri[Math.max(0, Math.min(2, Math.floor((cx - x0) / (x1 - x0) * 3)))];   // il bordo sinistro può cadere poco prima di x0
    }
    for (let k = 0; k < 9; k += 3) { colori[t + k] = cc.r; colori[t + k + 1] = cc.g; colori[t + k + 2] = cc.b; }
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colori, 3));
  geo.translate(-c.x, -c.y, -c.z);
  geo.computeVertexNormals();
  const lato = Math.max(b.max.x - b.min.x, (b.max.y - b.min.y) * 1.6);
  tre.distanza = lato * 0.5 / Math.tan(THREE.MathUtils.degToRad(15)) * 1.25;
  return geo;
}

/* Disegna solo mentre l'oggetto si muove (anche per l'inerzia), poi si ferma da solo: così la pagina
   non consuma batteria e memoria grafica quando nessuno la tocca. */
function passo() {
  if (document.hidden || !tre.mesh.visible) { ferma(); return; }
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

function misura() {
  if (!tre.renderer) return;
  const w = vista.box.clientWidth, h = vista.box.clientHeight;
  if (!w || !h) return;
  tre.renderer.setSize(w, h, false);
  tre.camera.aspect = w / h;
  tre.camera.updateProjectionMatrix();
  disegna();
}

function posiziona(dir) {
  tre.camera.position.set(0, 0, dir * tre.distanza);
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

function motore() {
  if (tre.renderer || tre.rotto) return !tre.rotto;
  try {
    tre.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
    const r = tre.renderer;
    r.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
    r.domElement.setAttribute('aria-hidden', 'true');
    r.domElement.className = 's3d-tela';
    r.domElement.addEventListener('webglcontextlost', ev => {
      ev.preventDefault();
      tre.rotto = true;
      ferma();
      soloImmagine('La vista in 3D si è fermata: guarda l\'immagine.');
    });
    tre.scena = new THREE.Scene();
    tre.scena.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 1.6));
    const luce = new THREE.DirectionalLight(0xffffff, 1.6);
    luce.position.set(-40, 60, 120);
    tre.scena.add(luce);
    tre.camera = new THREE.PerspectiveCamera(30, 2, 1, 4000);
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
    vista.box.appendChild(r.domElement);
    if (typeof ResizeObserver === 'function') new ResizeObserver(misura).observe(vista.box);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) disegna(); });
    return true;
  } catch (e) {
    tre.rotto = true;
    return false;
  }
}

/* Mostra una forma già pronta (posizione di stampa): il file STL scaricato o quello con nome e cognome. */
function mostra(pos, chi) {
  orienta(pos);
  const geo = geometria(pos);
  if (tre.mesh.geometry) tre.mesh.geometry.dispose();
  tre.mesh.geometry = geo;
  tre.mesh.visible = true;
  tre.geoUrl = chi;
  const c = tre.controlli;
  c.minDistance = tre.distanza * 0.4;
  c.maxDistance = tre.distanza * 2.5;
  misura();
  posiziona(1);
  vista.img.classList.add('visually-hidden');          // resta per i lettori di schermo
  vista.carica.hidden = true;
  vista.comandi.hidden = false;
  vista.box.classList.add('s3d-pronto');
  disegna();
}

async function carica() {
  const mia = ++tre.richiesta;
  const url = tre.url;
  vista.carica.hidden = false;
  vista.carica.textContent = 'Sto preparando la vista in 3D…';
  try {
    const r = await fetch(url);
    if (!r.ok) throw new Error(r.status);
    const pos = leggiStl(await r.arrayBuffer());
    if (mia !== tre.richiesta) return;
    mostra(pos, url);
  } catch (e) {
    if (mia !== tre.richiesta) return;
    soloImmagine('La vista in 3D non si è caricata: guarda l\'immagine.');
  }
}

function avvia() {
  if (tre.avviato) return;
  tre.avviato = true;
  if (!motore()) { soloImmagine('Il tuo browser non mostra la vista in 3D: guarda l\'immagine.'); return; }
  carica();
}

{
  vista.comandi.addEventListener('click', ev => {
    const b = ev.target.closest('button');
    if (!b || tre.rotto || !tre.mesh || !tre.mesh.visible) return;
    if (b.dataset.ruota) ruota(b.dataset.ruota);
    if (b.dataset.vista) posiziona(b.dataset.vista === 'retro' ? -1 : 1);
  });
  // La vista in 3D parte quando entra nello schermo, o al primo tocco
  vista.box.addEventListener('pointerdown', avvia, { once: true });
  if (typeof IntersectionObserver === 'function') {
    const oss = new IntersectionObserver(voci => {
      if (voci.some(v => v.isIntersecting)) { oss.disconnect(); avvia(); }
    }, { rootMargin: '100px' });
    oss.observe(vista.box);
  } else avvia();
}


tre.nuovoFile(window.pcgzS3dFile || '');
document.addEventListener('s3d:file', ev => tre.nuovoFile(ev.detail));
// Forma con nome e cognome, preparata da stampa3d-nome.js: si mostra senza scaricare nulla
document.addEventListener('s3d:geometria', ev => {
  const pos = ev.detail && ev.detail.pos;
  if (!pos) return;
  if (!tre.avviato) avvia();
  tre.richiesta++;                       // un caricamento in corso non la sovrascrive
  if (tre.rotto || !tre.mesh) return;    // senza vista 3D resta l'immagine: il file si scarica lo stesso
  mostra(pos, 'nome');
  if (ev.detail.lato === 'retro') posiziona(-1);
});
