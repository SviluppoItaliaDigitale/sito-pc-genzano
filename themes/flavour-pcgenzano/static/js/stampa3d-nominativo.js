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
const viste = {};
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
    vista(o, sez).carica(percorso(o.id, n, 'stl'));
  });
  esito.hidden = false;
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

function vista(o, sez) {
  if (viste[o.id]) return viste[o.id];
  const box = sez.querySelector('.s3d-visore');
  const img = sez.querySelector('[data-s3d="immagine"]');
  const stato = sez.querySelector('[data-s3d="caricamento"]');
  const comandi = sez.querySelector('[data-s3d="comandi"]');
  const col = o.anteprima || { base: '#1d4f9a', rilievo: '#f07d00' };
  const v = { carica() {} };
  viste[o.id] = v;

  let renderer;
  try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); }
  catch (e) { stato.textContent = 'Il tuo browser non mostra la vista in 3D: guarda l\'immagine.'; return v; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.domElement.setAttribute('aria-hidden', 'true');
  renderer.domElement.className = 's3d-tela';
  box.appendChild(renderer.domElement);

  const scena = new THREE.Scene();
  scena.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 1.6));
  const luce = new THREE.DirectionalLight(0xffffff, 1.6);
  luce.position.set(-40, 60, 120);
  scena.add(luce);
  const camera = new THREE.PerspectiveCamera(30, 2, 1, 2000);
  const controlli = new OrbitControls(camera, renderer.domElement);
  controlli.enablePan = false;
  controlli.enableDamping = true;
  controlli.dampingFactor = 0.1;
  controlli.minPolarAngle = 0;
  controlli.maxPolarAngle = Math.PI;
  let mesh = null, distanza = 200;

  const misura = () => {
    const w = box.clientWidth, h = box.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(misura).observe(box);

  function posiziona(dir) {
    camera.position.set(0, 0, dir * distanza);
    camera.up.set(0, 1, 0);
    controlli.target.set(0, 0, 0);
    controlli.update();
  }

  function ruota(verso) {
    const off = camera.position.clone().sub(controlli.target);
    const s = new THREE.Spherical().setFromVector3(off);
    if (verso === 'sinistra') s.theta -= Math.PI / 6;
    if (verso === 'destra') s.theta += Math.PI / 6;
    if (verso === 'su') s.phi = Math.max(0.01, s.phi - Math.PI / 9);
    if (verso === 'giu') s.phi = Math.min(Math.PI - 0.01, s.phi + Math.PI / 9);
    camera.position.copy(controlli.target).add(new THREE.Vector3().setFromSpherical(s));
    controlli.update();
  }

  comandi.addEventListener('click', ev => {
    const b = ev.target.closest('button');
    if (!b || !mesh) return;
    if (b.dataset.ruota) ruota(b.dataset.ruota);
    if (b.dataset.vista) posiziona(b.dataset.vista === 'retro' ? -1 : 1);
  });

  renderer.setAnimationLoop(() => {
    if (!mesh || esito.hidden) return;
    controlli.update();
    renderer.render(scena, camera);
  });

  let richiesta = 0;
  v.carica = async url => {
    const mia = ++richiesta;
    stato.hidden = false;
    stato.textContent = 'Sto preparando la vista in 3D…';
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error(r.status);
      const pos = leggiStl(await r.arrayBuffer());
      if (mia !== richiesta) return;
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      geo.computeBoundingBox();
      const b = geo.boundingBox, c = new THREE.Vector3();
      b.getCenter(c);
      const ril = o.anteprima && o.anteprima.rilievo_mm ? o.anteprima.rilievo_mm : 1;
      const zb = quotaBase(pos);
      const band = o.anteprima && o.anteprima.bandiera;
      const cb = new THREE.Color(col.base), cr = new THREE.Color(col.rilievo);
      const colori = new Float32Array(pos.length);
      for (let t = 0; t < pos.length; t += 9) {
        const zm = Math.max(pos[t + 2], pos[t + 5], pos[t + 8]);
        const alto = zm > zb + 0.01 && zm <= zb + ril + 0.02;
        let cc = alto ? cr : cb;
        if (alto && band) {
          const cx = (pos[t] + pos[t + 3] + pos[t + 6]) / 3, cy = (pos[t + 1] + pos[t + 4] + pos[t + 7]) / 3;
          const [x0, y0, x1, y1] = band;
          if (cx >= x0 - 0.1 && cx <= x1 + 0.1 && cy >= y0 - 0.1 && cy <= y1 + 0.1)
            cc = TRICOLORE[Math.min(2, Math.floor((cx - x0) / (x1 - x0) * 3))];
        }
        for (let k = 0; k < 9; k += 3) { colori[t + k] = cc.r; colori[t + k + 1] = cc.g; colori[t + k + 2] = cc.b; }
      }
      geo.setAttribute('color', new THREE.BufferAttribute(colori, 3));
      geo.translate(-c.x, -c.y, -c.z);
      geo.computeVertexNormals();
      if (mesh) { scena.remove(mesh); mesh.geometry.dispose(); }
      mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6, metalness: 0 }));
      scena.add(mesh);
      const larg = b.max.x - b.min.x;
      distanza = larg * 0.5 / Math.tan(THREE.MathUtils.degToRad(15)) * 1.25;
      controlli.minDistance = distanza * 0.4;
      controlli.maxDistance = distanza * 2.5;
      misura();
      posiziona(1);
      img.classList.add('visually-hidden'); // resta per i lettori di schermo
      stato.hidden = true;
      comandi.hidden = false;
      box.classList.add('s3d-pronto');
    } catch (e) {
      if (mia !== richiesta) return;
      img.classList.remove('visually-hidden');
      comandi.hidden = true;
      box.classList.remove('s3d-pronto');
      stato.textContent = 'La vista in 3D non si è caricata: guarda l\'immagine.';
    }
  };
  return v;
}

/* Indirizzo con il nominativo (#alfa-57): la pagina lo cerca subito, così si può condividere. */
const daIndirizzo = location.hash.match(new RegExp(`^#${DATI.prefisso.toLowerCase()}-(\\d+)$`));
if (daIndirizzo) {
  const n = leggiNumero(daIndirizzo[1]);
  if (n && !Number.isNaN(n)) { campo.value = String(n); cerca(n, false); }
}
