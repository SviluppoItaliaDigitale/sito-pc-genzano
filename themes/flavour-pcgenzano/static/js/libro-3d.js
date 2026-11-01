/*
  Libro 3D «Il libro che si esplora» (/formazione/libro-che-si-esplora/).
  Scena Three.js (r160, copia locale in vendor/three, licenza MIT) con un libro
  aperto: a sinistra testo e domanda, a destra un modellino interattivo; il
  lettore fa la sua previsione e alza il lembo per vedere la risposta.
  Testi: data/libro_3d.yaml e data/codici_colore.yaml, passati dallo shortcode
  libro-3d nel blocco JSON #lb-dati. Nessuna richiesta di rete.
*/
import * as THREE from '../vendor/three/three.module.min.js';
import { OrbitControls } from '../vendor/three/OrbitControls.js';

// Segnale per la rete di sicurezza dello shortcode: lo script è stato letto ed eseguito.
window.__libro3dAvviato = true;
const ROOT = document.getElementById('lb');
const DATI = JSON.parse(document.getElementById('lb-dati').textContent);
const BASE = DATI.base || '/';
const html = document.documentElement;
const mqRM = matchMedia('(prefers-reduced-motion: reduce)');
const RM = () => mqRM.matches || html.classList.contains('a11y-pause-anim') || html.classList.contains('a11y-pause-animations');

const LETTERE = 'ABCD';
const CH = DATI.capitoli.map(c => ({
  key:c.chiave, kicker:c.occhiello, title:c.titolo, intro:c.intro, q:c.domanda,
  opts:c.opzioni.map(o => ({t:o.testo, ok:!!o.giusta, why:o.perche || ''})),
  answer:c.risposta, short:c.breve, srcs:c.fonti.map(f => ({t:f.titolo, u:f.url}))
}));
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
const COLORI = DATI.colori.map(c => ({
  n:cap(c.livello), t:(c.titolo.split('—')[1] || c.titolo).trim(), s:c.significato, f:c.cosa_fare,
  c:parseInt(String(c.colore_bg).replace('#',''),16)
}));

const $ = id => document.getElementById('lb-' + id);
const stage = $('stage');
let chapter = 0, choice = -1, revealed = false, busy = false;

let renderer;
try { renderer = new THREE.WebGLRenderer({antialias:true}); }
catch (err) {
  // Senza WebGL (lavagne vecchie, schede grafiche disattivate): stesso messaggio della rete di
  // sicurezza dello shortcode, pannello nascosto, versione testuale aperta. Il modulo si ferma
  // qui in silenzio (un'eccezione lasciata uscire comparirebbe come errore della pagina).
  window.__libro3dAvviato = false;
  if (window.__libro3dNonParte) window.__libro3dNonParte();
  else $('loading').textContent = 'Il tuo browser non riesce a mostrare il libro in 3D. Trovi tutti i capitoli nella versione testuale qui sotto.';
  await new Promise(() => {});
}
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
stage.prepend(renderer.domElement);
renderer.domElement.setAttribute('aria-hidden','true');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xdfe6ee);
const camera = new THREE.PerspectiveCamera(34, 1, 0.05, 50);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enablePan = false; controls.enableDamping = true; controls.dampingFactor = .08;
controls.minPolarAngle = .35; controls.maxPolarAngle = 1.2;
controls.minAzimuthAngle = -.75; controls.maxAzimuthAngle = .75;
controls.target.set(0, .05, .02);

const hemi = new THREE.HemisphereLight(0xffffff, 0x9aa8bb, 1.6); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xffffff, 2.2);
sun.position.set(-1.6, 3.2, 1.4); sun.castShadow = true;
sun.shadow.mapSize.set(2048,2048);
Object.assign(sun.shadow.camera, {left:-1.6,right:1.6,top:1.6,bottom:-1.6,near:.5,far:8});
sun.shadow.bias = -0.0005; sun.shadow.radius = 4;
scene.add(sun);
const table = new THREE.Mesh(new THREE.PlaneGeometry(12,12), new THREE.MeshStandardMaterial({color:0xcdd6e1, roughness:1}));
table.rotation.x = -Math.PI/2; table.position.y = -0.001; table.receiveShadow = true; scene.add(table);
const mat = new THREE.Mesh(new THREE.PlaneGeometry(3.1,2.2), new THREE.MeshStandardMaterial({color:0xa9b9cb, roughness:1}));
mat.rotation.x = -Math.PI/2; mat.receiveShadow = true; scene.add(mat);

/* ---------- Materiali e pezzi in stile disegno tecnico ---------- */
const PAPER = 0xfbfaf5, INK = 0x24344d, BLUE = 0x003366;
const lineMat = new THREE.LineBasicMaterial({color:INK, transparent:true, opacity:.85});
function part(geo, color=PAPER, o={}){
  const m = new THREE.MeshStandardMaterial({color, roughness:o.rough ?? .92, metalness:0,
    transparent:o.opacity!=null, opacity:o.opacity ?? 1, emissive:o.emissive ?? 0x000000, emissiveIntensity:o.ei ?? 0,
    side:o.side ?? THREE.FrontSide, depthWrite:o.opacity!=null ? o.depthWrite ?? true : true});
  const mesh = new THREE.Mesh(geo, m);
  mesh.castShadow = o.shadow ?? true; mesh.receiveShadow = true;
  if (o.edges !== false) mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo, o.angle ?? 25), lineMat));
  return mesh;
}
const box = (w,h,d) => new THREE.BoxGeometry(w,h,d);
const at = (o,x,y,z) => (o.position.set(x,y,z), o);
function glow(obj, hex, k){ obj.traverse(c=>{ if(c.isMesh && c.material.emissive){ c.material.emissive.setHex(hex); c.material.emissiveIntensity = k; }}); }
function pick(obj, id){ obj.traverse(c=>{ if(c.isMesh) c.userData.pick = id; }); return obj; }

function textSprite(text, size=.045, color='#14223a', bg='rgba(255,255,255,.94)'){
  const c = document.createElement('canvas'), x = c.getContext('2d'), fs = 52;
  x.font = `700 ${fs}px "Titillium Web", Arial, sans-serif`;
  const w = Math.ceil(x.measureText(text).width) + 44; c.width = w; c.height = fs + 30;
  x.font = `700 ${fs}px "Titillium Web", Arial, sans-serif`;
  x.fillStyle = bg; x.beginPath(); x.roundRect(2,2,w-4,c.height-4,16); x.fill();
  x.strokeStyle = '#24344d'; x.lineWidth = 3; x.stroke();
  x.fillStyle = color; x.textBaseline = 'middle'; x.fillText(text, 22, c.height/2+2);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({map:t, depthTest:false, transparent:true}));
  s.renderOrder = 20; s.scale.set(size*c.width/c.height, size, 1); return s;
}
function pawn(color=0xe0a100){
  const g = new THREE.Group();
  g.add(at(part(new THREE.CylinderGeometry(.017,.026,.068,14), color),0,.034,0));
  g.add(at(part(new THREE.SphereGeometry(.02,14,10), color),0,.088,0));
  return g;
}

/* ---------- Animazioni ---------- */
const tweens = [];
function tween(dur, fn, done){ const tw = {t:0, dur:RM() ? Math.min(dur,.25) : dur, fn, done}; tweens.push(tw); return tw; }
const ease = p => p<.5 ? 2*p*p : 1-Math.pow(-2*p+2,2)/2;
/* uscita con un piccolo rimbalzo, come la carta di un libro pop-up */
const easeBack = p => 1 + 2.2*Math.pow(p-1,3) + 1.2*Math.pow(p-1,2);
function moveTo(obj, target, dur=.9, hop=.05, done){
  const a = obj.position.clone();
  tween(dur, p=>{ const e = ease(p); obj.position.lerpVectors(a,target,e); obj.position.y += Math.sin(Math.PI*e)*hop; }, done);
}
const say = t => { $('status').textContent = t; };

/* ---------- Il libro ---------- */
const book = new THREE.Group(); scene.add(book);
book.add(at(part(box(2.26,.04,1.58), BLUE, {edges:false, rough:.7}),0,.02,0));
const block = (x) => at(part(box(1.05,.05,1.47), 0xf1eee4, {edges:false}), x, .065, 0);
book.add(block(-.545), block(.545));
const PW = 1.04, PD = 1.46, PY = .0915;

function pageCanvas(){ const c = document.createElement('canvas'); c.width = 2080; c.height = 2920; return c; }
const leftCv = pageCanvas(), rightCv = pageCanvas();
const leftTex = new THREE.CanvasTexture(leftCv), rightTex = new THREE.CanvasTexture(rightCv);
for (const t of [leftTex,rightTex]){ t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; }
function pageMesh(tex, x){
  const m = new THREE.Mesh(new THREE.PlaneGeometry(PW,PD), new THREE.MeshStandardMaterial({map:tex, roughness:1}));
  m.rotation.x = -Math.PI/2; m.position.set(x, PY, 0); m.receiveShadow = true; return m;
}
const leftPage = pageMesh(leftTex, -.545), rightPage = pageMesh(rightTex, .545);
book.add(leftPage, rightPage);
const gutter = new THREE.Mesh(new THREE.PlaneGeometry(.06, PD), new THREE.MeshBasicMaterial({color:0x000000, transparent:true, opacity:.12}));
gutter.rotation.x = -Math.PI/2; gutter.position.set(0, PY+.0005, 0); book.add(gutter);

function wrap(x, text, maxW){
  const words = text.split(' '), lines = []; let line = '';
  for (const w of words){ const t = line ? line+' '+w : w; if (x.measureText(t).width > maxW && line){ lines.push(line); line = w; } else line = t; }
  if (line) lines.push(line); return lines;
}
function paperBase(x){
  x.setTransform(2,0,0,2,0,0);
  x.fillStyle = '#fbfaf5'; x.fillRect(0,0,1040,1460);
  x.fillStyle = 'rgba(36,52,77,.07)';
  for (let yy=40; yy<1460; yy+=40) for (let xx=40; xx<1040; xx+=40){ x.beginPath(); x.arc(xx,yy,1.6,0,7); x.fill(); }
}
const F = (w,s) => `${w} ${s}px "Titillium Web", Arial, sans-serif`;
function drawLeft(i){
  const c = CH[i], x = leftCv.getContext('2d'); paperBase(x);
  x.fillStyle = '#003366'; x.font = F(700,24); x.letterSpacing = '3px';
  x.fillText(c.kicker.toUpperCase(), 80, 110); x.letterSpacing = '0px';
  x.fillStyle = '#14223a'; x.font = F(700,70); x.fillText(c.title, 80, 190);
  x.fillStyle = '#003366'; x.fillRect(80, 214, 90, 6);
  x.font = F(400,31); x.fillStyle = '#2a3a52'; let y = 280;
  for (const l of wrap(x, c.intro, 880)){ x.fillText(l, 80, y); y += 44; }
  y += 30; x.font = F(700,22); x.fillStyle = '#4a5a72'; x.letterSpacing = '3px'; x.fillText('LA TUA PREVISIONE', 80, y); x.letterSpacing = '0px';
  y += 46; x.font = F(600,34); x.fillStyle = '#14223a';
  for (const l of wrap(x, c.q, 880)){ x.fillText(l, 80, y); y += 44; }
  y += 14; x.font = F(400,29);
  c.opts.forEach((o,k)=>{
    x.strokeStyle = '#24344d'; x.lineWidth = 2; x.beginPath(); x.arc(98, y-10, 17, 0, 7); x.stroke();
    x.fillStyle = '#14223a'; x.font = F(700,20); x.fillText(LETTERE[k], 91, y-3);
    x.font = F(400,29); x.fillText(o.t, 132, y); y += 50;
  });
  // area sotto il lembo
  x.fillStyle = '#eef4ea'; x.fillRect(60, 1120, 920, 280);
  x.strokeStyle = '#16723a'; x.lineWidth = 3; x.strokeRect(60, 1120, 920, 280);
  x.fillStyle = '#16723a'; x.font = F(700,22); x.letterSpacing = '3px'; x.fillText('RISPOSTA', 90, 1170); x.letterSpacing = '0px';
  x.fillStyle = '#14223a'; x.font = F(600,28); y = 1218;
  for (const l of wrap(x, c.short, 860)){ x.fillText(l, 90, y); y += 38; }
  x.fillStyle = '#4a5a72'; x.font = F(400,22); x.fillText(String(i*2+1), 80, 1440);
  leftTex.needsUpdate = true;
}
function drawRight(i){
  const x = rightCv.getContext('2d'); paperBase(x);
  x.fillStyle = '#4a5a72'; x.font = F(400,22);
  x.fillText('Tocca gli oggetti · usa i comandi «Prova sulla pagina»', 80, 1400);
  x.textAlign = 'right'; x.fillText(String(i*2+2), 960, 1440); x.textAlign = 'left';
  rightTex.needsUpdate = true;
}

/* lembo di carta incernierato sul bordo superiore dell'area risposta */
const flapCv = document.createElement('canvas'); flapCv.width = 1840; flapCv.height = 560;
(function(){ const x = flapCv.getContext('2d'); x.setTransform(2,0,0,2,0,0);
  x.fillStyle = '#f4efe1'; x.fillRect(0,0,920,280);
  x.strokeStyle = '#24344d'; x.setLineDash([10,8]); x.lineWidth = 2; x.strokeRect(10,10,900,260);
  x.setLineDash([]); x.fillStyle = '#003366'; x.font = F(700,34); x.textAlign = 'center';
  x.fillText('Alza il lembo', 460, 128); x.font = F(400,26); x.fillStyle = '#2a3a52';
  x.fillText('dopo aver fatto la tua previsione', 460, 172);
  x.beginPath(); x.moveTo(460,210); x.lineTo(440,240); x.lineTo(480,240); x.closePath(); x.fill(); })();
const flapTex = new THREE.CanvasTexture(flapCv); flapTex.colorSpace = THREE.SRGBColorSpace;
const flapPivot = new THREE.Group();
flapPivot.position.set(-.545, PY+.002, 1.12-.73); book.add(flapPivot);
const flap = new THREE.Mesh(new THREE.PlaneGeometry(.92,.28), new THREE.MeshStandardMaterial({map:flapTex, roughness:1}));
flap.rotation.x = -Math.PI/2; flap.position.set(0, 0, .14); flap.castShadow = true; flap.userData.pick = 'flap';
const flapBack = new THREE.Mesh(new THREE.PlaneGeometry(.92,.28), new THREE.MeshStandardMaterial({color:0xf4efe1, roughness:1}));
flapBack.rotation.x = Math.PI/2; flapBack.position.set(0, -.0005, .14); flapBack.userData.pick = 'flap';
flapPivot.add(flap, flapBack);
function setFlap(open){
  const a = flapPivot.rotation.x, b = open ? -2.35 : 0;
  tween(open ? .9 : .6, p=>{ flapPivot.rotation.x = a + (b-a)*(open && !RM() ? easeBack(p) : ease(p)); });
}

/* foglio che gira quando cambi capitolo */
const sheetPivot = new THREE.Group(); sheetPivot.position.set(0, PY+.003, 0); book.add(sheetPivot);
const sheet = new THREE.Mesh(new THREE.PlaneGeometry(PW,PD), new THREE.MeshStandardMaterial({color:0xfbfaf5, roughness:1, side:THREE.DoubleSide}));
sheet.rotation.x = -Math.PI/2; sheet.position.x = .52; sheet.castShadow = true; sheet.visible = false; sheetPivot.add(sheet);

function casetta(w,h,d){
  const g = new THREE.Group(); g.add(at(part(box(w,h,d)),0,h/2,0));
  const sh = new THREE.Shape(); sh.moveTo(-w/2-.01,0); sh.lineTo(w/2+.01,0); sh.lineTo(0,h*.45); sh.closePath();
  g.add(at(part(new THREE.ExtrudeGeometry(sh,{depth:d+.02,bevelEnabled:false}), 0xb24a35),0,h,-d/2-.01));
  g.add(at(part(box(.04,.07,.006), 0x6b4f33),0,.035,d/2+.003)); return g;
}
function carro(color){
  const c = new THREE.Group();
  c.add(at(part(box(.11,.035,.2), color),0,.04,0), at(part(box(.095,.035,.1), 0xdfe8f2),0,.075,.01));
  for (const [wx,wz] of [[-.058,-.065],[.058,-.065],[-.058,.065],[.058,.065]]){ const w = part(new THREE.CylinderGeometry(.022,.022,.018,14), 0x222831); w.rotation.z = Math.PI/2; at(w,wx,.022,wz); c.add(w); }
  return c;
}

/* ---------- Le scene della pagina di destra ---------- */
const anchor = new THREE.Group(); anchor.position.set(.545, PY, -.04); book.add(anchor);

/* ---------- Effetti ----------
   Pop-up dei modellini, luce e colore del cielo per ogni capitolo, polvere
   luminosa, scintille sulla previsione giusta, ingresso della telecamera.
   Con «Pausa animazioni» o movimento ridotto restano solo i cambi immediati. */
function popUp(g){
  if (RM()) return;
  [...g.children].forEach((c,k)=>{
    const piv = new THREE.Group(); g.add(piv); piv.add(c);   /* il perno è sulla pagina: il pezzo «si alza» dalla carta */
    piv.scale.set(1,.001,1); piv.rotation.x = -.5;
    const d = .08*k, dur = .7;
    tween(dur + d, p=>{ const q = Math.max(0, Math.min(1, (p*(dur+d) - d)/dur)); const e = easeBack(q);
      piv.scale.set(1, Math.max(.001, e), 1); piv.rotation.x = -.5*(1-Math.min(1,e)); },
      ()=>{ piv.scale.set(1,1,1); piv.rotation.x = 0; });
  });
}
const TINTA = { sisma:0xe3dccf, alluvione:0xcfdbe6, sottopasso:0xcbd6e0, incendio:0xead6c8, allerta:0xdfe3ee,
  kit:0xdfe6ee, caldo:0xf0dfc4, temporale:0xbfc8d6, vento:0xd3dde6, blackout:0x9aa3b4, gas:0xd8d6cc,
  maremoto:0xc9dfe8, industriale:0xd5d6d2, radiologico:0xd9dde2, siccita:0xeedfc2 };
const SOLE = { caldo:0xfff0d0, incendio:0xffe2c8, temporale:0xdfe7ff, blackout:0xc8d2ff, siccita:0xfff1d6 };
const cielo = new THREE.Color(0xdfe6ee), cieloA = new THREE.Color(), sunCol = new THREE.Color(0xffffff), sunA = new THREE.Color();
function atmosfera(key){
  const bg = new THREE.Color(TINTA[key] ?? 0xdfe6ee), sc = new THREE.Color(SOLE[key] ?? 0xffffff);
  if (RM()){ scene.background.copy(bg); sun.color.copy(sc); return; }
  cieloA.copy(scene.background); sunA.copy(sun.color);
  tween(1.2, p=>{ const e = ease(p); scene.background.copy(cieloA).lerp(bg,e); sun.color.copy(sunA).lerp(sc,e); });
}
/* punto rotondo e sfumato per polvere e scintille (i Points sono quadrati senza texture) */
const puntoTex = (()=>{ const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
  const g = x.createRadialGradient(32,32,0,32,32,32); g.addColorStop(0,'rgba(255,255,255,1)'); g.addColorStop(.45,'rgba(255,255,255,.85)'); g.addColorStop(1,'rgba(255,255,255,0)');
  x.fillStyle = g; x.fillRect(0,0,64,64); return new THREE.CanvasTexture(c); })();
/* polvere luminosa nel fascio di luce: si muove solo senza «Pausa animazioni» */
const POLVERE = 140, pv = new Float32Array(POLVERE*3), pvVel = [];
for (let k=0;k<POLVERE;k++){ pv[k*3] = (Math.random()-.5)*2.6; pv[k*3+1] = .1+Math.random()*1.2; pv[k*3+2] = (Math.random()-.5)*1.8;
  pvVel.push([(Math.random()-.5)*.02, .01+Math.random()*.02, (Math.random()-.5)*.02]); }
const pvGeo = new THREE.BufferGeometry(); pvGeo.setAttribute('position', new THREE.BufferAttribute(pv,3));
const polvere = new THREE.Points(pvGeo, new THREE.PointsMaterial({color:0xfff6d8, size:.02, map:puntoTex, transparent:true, opacity:.6, depthWrite:false}));
scene.add(polvere);
function muoviPolvere(dt, t){
  if (!dt) return;
  for (let k=0;k<POLVERE;k++){ const v = pvVel[k];
    pv[k*3] += (v[0] + .006*Math.sin(t*.7+k))*dt; pv[k*3+1] += v[1]*dt; pv[k*3+2] += v[2]*dt;
    if (pv[k*3+1] > 1.4){ pv[k*3+1] = .08; pv[k*3] = (Math.random()-.5)*2.6; pv[k*3+2] = (Math.random()-.5)*1.8; } }
  pvGeo.attributes.position.needsUpdate = true;
}
/* scintille quando la previsione è giusta */
const scintille = [];
function festa(){
  if (RM()) return;
  const o = new THREE.Vector3(); flapPivot.getWorldPosition(o); o.y += .05; o.z += .1;
  const N = 90, pos = new Float32Array(N*3), col = new Float32Array(N*3), vel = [];
  const tinte = [new THREE.Color(0xffbe2e), new THREE.Color(0x16a34a), new THREE.Color(0x3b82f6), new THREE.Color(0xffffff)];
  for (let k=0;k<N;k++){ pos.set([o.x+(Math.random()-.5)*.6, o.y, o.z+(Math.random()-.5)*.1], k*3);
    const c = tinte[k%4]; col.set([c.r,c.g,c.b], k*3);
    vel.push(new THREE.Vector3((Math.random()-.5)*.9, .9+Math.random()*1.1, (Math.random()-.5)*.6)); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos,3)); geo.setAttribute('color', new THREE.BufferAttribute(col,3));
  const pts = new THREE.Points(geo, new THREE.PointsMaterial({size:.045, map:puntoTex, vertexColors:true, transparent:true, opacity:1, depthWrite:false}));
  scene.add(pts); scintille.push({pts, vel, t:0});
}
function muoviScintille(dt, ferme){
  /* con «Pausa animazioni» attivata a scintille in volo, le scintille spariscono subito invece di continuare a muoversi */
  if (ferme) dt = 9;
  for (let i=scintille.length-1;i>=0;i--){ const s = scintille[i]; s.t += dt;
    const a = s.pts.geometry.attributes.position;
    s.vel.forEach((v,k)=>{ v.y -= 2.2*dt; a.array[k*3] += v.x*dt; a.array[k*3+1] += v.y*dt; a.array[k*3+2] += v.z*dt; });
    a.needsUpdate = true; s.pts.material.opacity = Math.max(0, 1 - s.t/1.6);
    if (s.t > 1.6){ scene.remove(s.pts); s.pts.geometry.dispose(); s.pts.material.dispose(); scintille.splice(i,1); } }
}
/* scossa leggera del libro quando la previsione non è quella sicura */
function scuoti(){
  if (RM()) return;
  tween(.45, p=>{ book.rotation.z = .025*Math.sin(p*Math.PI*6)*(1-p); }, ()=>{ book.rotation.z = 0; });
}
/* ingresso: la telecamera scende sul libro e il libro ruota verso chi guarda */
function ingresso(){
  if (RM()) return;
  const fine = camera.position.clone(), inizio = fine.clone().multiplyScalar(2.1).add(new THREE.Vector3(1.4,.9,0));
  camera.position.copy(inizio); book.rotation.y = -.55; controls.enabled = false;
  tween(2.4, p=>{ const e = 1-Math.pow(1-p,3); camera.position.lerpVectors(inizio, fine, e); book.rotation.y = -.55*(1-e); camera.lookAt(controls.target); },
    ()=>{ book.rotation.y = 0; controls.enabled = true; });
}
const clampP = v => (v.x = Math.max(-.42, Math.min(.42, v.x)), v.z = Math.max(-.55, Math.min(.5, v.z)), v);

const BUILD = {
 sisma(){
  const g = new THREE.Group(), room = new THREE.Group(); g.add(room);
  room.add(at(part(box(.84,.02,.9), 0xe9e4d6),0,.01,-.05));
  room.add(at(part(box(.84,.5,.02)),0,.26,-.49), at(part(box(.02,.5,.9)),-.41,.26,-.05));
  const win = new THREE.Group(); at(win,.17,.3,-.475);
  win.add(at(part(box(.24,.2,.015), 0xdfe8f2),0,0,0));
  const glass = part(box(.2,.16,.01), 0x9cc6ea, {opacity:.6, edges:false}); win.add(at(glass,0,0,.008));
  win.add(at(part(box(.012,.16,.012)),0,0,.012), at(part(box(.2,.012,.012)),0,0,.012));
  room.add(pick(win,1));
  const tbl = new THREE.Group(); at(tbl,-.1,0,.02);
  tbl.add(at(part(box(.32,.02,.22), 0xc79a63),0,.165,0));
  for (const [lx,lz] of [[-.14,-.09],[.14,-.09],[-.14,.09],[.14,.09]]) tbl.add(at(part(new THREE.CylinderGeometry(.01,.01,.155,8), 0xb08654),lx,.08,lz));
  room.add(pick(tbl,0));
  const shelf = new THREE.Group(); at(shelf,-.33,0,-.3);
  shelf.add(at(part(box(.14,.4,.09), 0xd8cdb6),0,.2,0));
  const books = [];
  [0x5d7fb3,0xb85a3c,0x6c9a5f,0xd9a441].forEach((c,k)=>{ const b = at(part(box(.022,.06,.06), c), -.045+k*.03, .43, 0); shelf.add(b); books.push({m:b, home:b.position.clone()}); });
  room.add(shelf);
  const stairs = new THREE.Group();
  for (let k=0;k<5;k++){ const h = .03*(k+1); stairs.add(at(part(box(.12,h,.07), 0xe1d7c3),.32,h/2+.02,.3-k*.07)); }
  room.add(pick(stairs,2));
  const p = pawn(); at(p,.08,.02,.32); room.add(p);
  const T = [new THREE.Vector3(-.1,.02,.02), new THREE.Vector3(.17,.02,-.36), new THREE.Vector3(.32,.11,.16)];
  const groups = [tbl, win, stairs];
  let shake = 0;
  return { g,
    tools:[ {label:'Fai tremare la stanza', fn(){ if (RM()){ say('Con le animazioni in pausa la stanza non trema. In una scossa vera mobili, libri e vetri possono cadere: per questo ci si ripara sotto il tavolo.'); } else { shake = 3; say('La stanza trema per qualche secondo: guarda che cosa si muove e che cosa cade.'); }
              books.forEach((b,k)=>{ const to = new THREE.Vector3(.11+k*.045, .012, .14+k*.025); setTimeout(()=>{ const a=b.m.position.clone(); tween(.6,q=>{ b.m.position.lerpVectors(a,to,ease(q)); b.m.position.y += Math.sin(Math.PI*q)*.06; b.m.rotation.z = q*1.4; }); }, 400+k*350); }); } },
            {label:'Rimetti a posto', fn(){ books.forEach(b=>{ b.m.position.copy(b.home); b.m.rotation.set(0,0,0); }); say('I libri sono tornati sullo scaffale.'); } } ],
    choose(i){ groups.forEach((o,k)=>glow(o, 0xffb000, k===i ? .45 : 0)); moveTo(p, T[i]); },
    update(dt,t){ if (shake>0){ shake -= dt; const a = Math.min(1, shake)*.012;
      room.position.set(Math.sin(t*57)*a, 0, Math.cos(t*43)*a*.8); shelf.rotation.z = Math.sin(t*31)*a*5; glass.material.opacity = .45+.25*Math.sin(t*40); }
      else { room.position.set(0,0,0); shelf.rotation.z = 0; } }
  };
 },
 alluvione(){
  const g = new THREE.Group(), EARTH = 0x9c8461;
  g.add(at(part(box(.2,.12,.5), EARTH),-.32,.06,-.2), at(part(box(.18,.12,.5), EARTH),.33,.06,-.2));
  g.add(at(part(box(.84,.12,.1), EARTH),.0,.06,-.4));
  for (const [x,w] of [[-.32,.2],[.33,.18]]) g.add(at(part(box(w,.008,.5), 0x7fa35a, {edges:false}),x,.124,-.2));
  const H = new THREE.Group(); g.add(H);
  H.add(at(part(box(.46,.015,.36), 0xe6dfcf),.02,.0075,-.17));
  H.add(at(part(box(.46,.5,.015)),.02,.25,-.35), at(part(box(.015,.5,.36)),-.21,.25,-.17), at(part(box(.015,.5,.36)),.245,.25,-.17));
  H.add(at(part(box(.015,.12,.36)),.03,.06,-.17));
  H.add(at(part(box(.46,.015,.36), 0xe6dfcf),.02,.127,-.17), at(part(box(.46,.015,.36), 0xe6dfcf),.02,.31,-.17));
  const sh = new THREE.Shape(); sh.moveTo(-.25,0); sh.lineTo(.25,0); sh.lineTo(0,.15); sh.closePath();
  const roof = part(new THREE.ExtrudeGeometry(sh,{depth:.38,bevelEnabled:false}), 0xb24a35); at(roof,.02,.5,-.36); H.add(roof);
  const cant = new THREE.Group(), gar = new THREE.Group(), alto = new THREE.Group();
  cant.add(at(part(box(.08,.05,.06), 0xc9a86b),-.15,.04,-.25)); gar.add(at(part(box(.14,.045,.08), 0x5d7fb3),.14,.035,-.22));
  alto.add(at(part(box(.12,.04,.08), 0x8aa7cf),.15,.338,-.26));
  H.add(pick(cant,0), pick(gar,2), pick(alto,1));
  const L1 = textSprite('Cantina',.034), L2 = textSprite('Garage',.034), L3 = textSprite('Piano alto',.034), L4 = textSprite('Piano terra',.034);
  at(L1,-.09,.1,-.04); at(L2,.13,.1,-.04); at(L3,.02,.44,-.04); at(L4,.02,.26,-.04); g.add(L1,L2,L3,L4);
  const wMat = {opacity:.55, edges:false, shadow:false, depthWrite:false};
  const inside = part(box(1,1,1), 0x3f86c9, wMat), outL = part(box(1,1,1), 0x3f86c9, wMat), outR = part(box(1,1,1), 0x3f86c9, wMat);
  g.add(inside, outL, outR);
  const p = pawn(); at(p,.02,.135,-.05); g.add(p);
  let lvl = 0;
  function setLevel(v){ lvl = v; const h = .008 + v*.27;
    inside.scale.set(.43,h,.34); inside.position.set(.02,h/2+.01,-.17);
    const o = Math.max(.001, h-.12); outL.scale.set(.2,o,.5); outL.position.set(-.32,.13+o/2,-.2); outR.scale.set(.18,o,.5); outR.position.set(.33,.13+o/2,-.2);
    outL.visible = outR.visible = h > .121;
    const m = h < .03 ? 'L’acqua comincia a entrare dal basso.' : h < .118 ? 'Cantina e garage si stanno riempiendo.' : h < .3 ? 'Cantina e garage sono pieni. L’acqua sale al piano terra.' : 'L’acqua ha superato il piano terra.';
    say(m);
  }
  setLevel(.15);
  const T = [new THREE.Vector3(-.09,.015,-.12), new THREE.Vector3(.0,.318,-.14), new THREE.Vector3(.13,.015,-.12)];
  const groups = [cant, alto, gar];
  return { g, tools:[{range:true, label:'Livello dell’acqua', min:0, max:100, value:15, fn(v){ setLevel(v/100); }}],
    choose(i){ groups.forEach((o,k)=>glow(o,0xffb000,k===i?.5:0)); moveTo(p, T[i], 1.1, .08); },
    update(){} };
 },
 sottopasso(){
  const g = new THREE.Group(), EARTH = 0x9c8461, ROAD = 0x5b6270;
  const yRoad = z => z>=.22 ? .14 : z>=.06 ? .02+(z-.06)/.16*.12 : z>=-.11 ? .02 : z>=-.27 ? .02+(-.11-z)/.16*.12 : .14;
  g.add(at(part(box(.84,.14,.3), EARTH),0,.07,.37), at(part(box(.84,.14,.3), EARTH),0,.07,-.43));
  g.add(at(part(box(.84,.02,.86), EARTH),0,.01,-.03));
  g.add(at(part(box(.2,.01,.28), ROAD),0,.145,.37), at(part(box(.2,.01,.28), ROAD),0,.145,-.42), at(part(box(.2,.01,.17), ROAD),0,.025,-.025));
  const L = Math.hypot(.16,.12), A = Math.atan2(.12,.16);
  const r1 = part(box(.2,.01,L), ROAD); at(r1,0,.085,.14); r1.rotation.x = -A;
  const r2 = part(box(.2,.01,L), ROAD); at(r2,0,.085,-.19); r2.rotation.x = A; g.add(r1,r2);
  g.add(at(part(box(.84,.03,.07), 0xd8d2c4),0,.27,-.13));
  for (const px of [-.16,.16]) g.add(at(part(box(.035,.25,.05), 0xd8d2c4),px,.14,-.13));
  const hole = new THREE.Mesh(new THREE.CircleGeometry(.024,20), new THREE.MeshBasicMaterial({color:0x111111}));
  hole.rotation.x = -Math.PI/2; at(hole,.035,.031,-.03); g.add(hole);
  const lid = part(new THREE.CylinderGeometry(.026,.026,.006,20), 0x444a55); at(lid,-.03,.034,-.06); lid.rotation.z = .5; g.add(lid);
  const water = part(box(1,1,1), 0x8a744c, {opacity:.9, edges:false, shadow:false, depthWrite:false}); g.add(water);
  let murky = true, lvl = .4;
  function setLevel(v){ lvl = v; const h = .008 + v*.08, d = .17 + 2*(h/.12*.16);
    water.scale.set(.2,h,d); water.position.set(0,.03+h/2,-.025); }
  setLevel(lvl);
  const car = new THREE.Group();
  car.add(at(part(box(.11,.035,.2), 0x2f6fb5),0,.04,0), at(part(box(.095,.035,.1), 0xdfe8f2),0,.075,.01));
  for (const [wx,wz] of [[-.058,-.065],[.058,-.065],[-.058,.065],[.058,.065]]){ const w = part(new THREE.CylinderGeometry(.022,.022,.018,14), 0x222831); w.rotation.z = Math.PI/2; at(w,wx,.022,wz); car.add(w); }
  const carHome = () => { car.position.set(0, yRoad(.38)+.005, .38); car.rotation.set(0,0,0); };
  carHome(); g.add(car);
  function drive(toZ, dur, after){ const z0 = car.position.z;
    tween(dur, q=>{ const z = z0 + (toZ-z0)*ease(q); car.position.z = z; car.position.y = yRoad(z)+.005;
      const s = (yRoad(z+.01)-yRoad(z-.01))/.02; car.rotation.x = Math.atan(s); }, after); }
  return { g, tools:[
      {range:true, label:'Livello dell’acqua', min:0, max:100, value:40, fn(v){ setLevel(v/100); say(v<25 ? 'Il velo d’acqua sembra sottile, ma da qui non si vede il fondo.' : 'L’acqua copre il fondo del sottopassaggio.'); }},
      {label:'Guarda sotto la superficie', fn(){ murky = !murky; water.material.color.setHex(murky ? 0x8a744c : 0x6fa8dc); water.material.opacity = murky ? .9 : .28;
        this.textContent = murky ? 'Guarda sotto la superficie' : 'Rendi l’acqua torbida';
        say(murky ? 'L’acqua è torbida: buche e tombini non si vedono.' : 'Sotto la superficie c’è un tombino aperto. Dall’auto non lo vedresti.'); }},
      {label:'Riporta l’auto in cima', fn(){ carHome(); say('L’auto è di nuovo davanti al sottopassaggio.'); }} ],
    choose(i){ carHome();
      if (i===2){ tween(1.0, q=>{ car.rotation.y = Math.PI*ease(q); car.position.z = .38 + .08*ease(q); }); say('Torni indietro e cerchi un’altra strada.'); }
      else drive(.08, i===0 ? 1.8 : .9, ()=>{ tween(.5,q=>{ car.rotation.z = .06*Math.sin(q*Math.PI*3); }); say('L’auto entra nell’acqua e si ferma: il motore si è spento.'); }); },
    update(){} };
 },
 incendio(){
  const g = new THREE.Group();
  const hill = part(new THREE.CylinderGeometry(.12,.34,.14,9), 0x8f9a5e); at(hill,-.14,.07,-.27); g.add(hill);
  const tree = (x,z,y=0,burnt=false) => { const t = new THREE.Group();
    t.add(at(part(new THREE.CylinderGeometry(.006,.008,.04,6), 0x6b4f33),0,.02,0));
    t.add(at(part(new THREE.ConeGeometry(.032,.09,7), burnt ? 0x3c3c3c : 0x3f7a45),0,.08,0)); at(t,x,y,z); g.add(t); };
  [[-.3,-.15,0],[-.05,-.45,0],[-.36,-.38,0],[.05,-.2,0],[-.25,.0,0],[.3,-.4,0],[-.06,-.13,.06],[-.22,-.3,.1]].forEach(a=>tree(...a));
  const F = new THREE.Vector3(-.14,.15,-.27);
  const flames = [];
  for (let k=0;k<6;k++){ const f = part(new THREE.ConeGeometry(.025,.08,7), k%2 ? 0xf07f1a : 0xd23a2f, {emissive:0xff5a1f, ei:.9, edges:false});
    const a = k/6*Math.PI*2; at(f, F.x+Math.cos(a)*.05, F.y+.03, F.z+Math.sin(a)*.04); g.add(f); flames.push(f); }
  const house = new THREE.Group(); at(house,.22,0,.22);
  house.add(at(part(box(.14,.1,.12)),0,.05,0));
  const sh = new THREE.Shape(); sh.moveTo(-.08,0); sh.lineTo(.08,0); sh.lineTo(0,.06); sh.closePath();
  house.add(at(part(new THREE.ExtrudeGeometry(sh,{depth:.13,bevelEnabled:false}), 0xb24a35),0,.1,-.065)); g.add(house);
  const H = new THREE.Vector3(.22,0,.34);
  const p = pawn(); at(p,H.x,.0,H.z); g.add(p);
  const smoke = []; const smokeMat = new THREE.MeshStandardMaterial({color:0x8c8f96, transparent:true, opacity:.5, depthWrite:false, roughness:1});
  for (let k=0;k<44;k++){ const s = new THREE.Mesh(new THREE.SphereGeometry(.022,8,6), smokeMat.clone()); s.userData.age = Math.random()*3; g.add(s); smoke.push(s); }
  const WINDS = [{v:[.5,.86], n:'verso la casa, cioè verso di te'}, {v:[1,0], n:'verso destra'}, {v:[-1,0], n:'verso sinistra'}, {v:[0,-1], n:'lontano dalla casa'}];
  let wi = 0, W = new THREE.Vector3(), E = new THREE.Vector3();
  const windArrow = new THREE.ArrowHelper(new THREE.Vector3(1,0,0), F.clone().setY(.34), .2, 0x6b7280, .05, .035);
  const escArrow = new THREE.ArrowHelper(new THREE.Vector3(1,0,0), H.clone().setY(.012), .2, 0x16a34a, .05, .04);
  g.add(windArrow, escArrow);
  function setWind(i){ wi = i; W.set(WINDS[i].v[0],0,WINDS[i].v[1]).normalize();
    const away = H.clone().sub(F).setY(0).normalize();
    E.copy(away).addScaledVector(W,-.9);
    if (E.length() < .3){ E.set(-W.z,0,W.x); if (E.dot(away) < 0) E.negate(); }
    E.normalize(); windArrow.setDirection(W); escArrow.setDirection(E);
    say(`Il vento spinge il fumo ${WINDS[i].n}. La freccia verde indica da che parte allontanarti.`); }
  setWind(0);
  return { g, tools:[
      {label:'Cambia il vento', fn(){ setWind((wi+1)%WINDS.length); }},
      {label:'Riporta la pedina a casa', fn(){ p.position.set(H.x,0,H.z); say('La pedina è tornata davanti a casa.'); }} ],
    choose(i){ p.position.set(H.x,0,H.z); let T;
      if (i===0) T = F.clone().addScaledVector(W,.28).setY(0);
      else if (i===1) T = H.clone().addScaledVector(E,.24).setY(0);
      else T = F.clone().lerp(H,.35).setY(.03);
      moveTo(p, clampP(T), 1.2, .06); },
    update(dt,t){
      flames.forEach((f,k)=>{ const s = 1+.25*Math.sin(t*9+k*1.7); f.scale.set(1,s,1); });
      const sp = RM() ? .35 : 1;
      smoke.forEach(s=>{ let a = s.userData.age += dt*sp; if (a>3){ a = s.userData.age = 0; s.userData.j = Math.random()-.5; }
        const j = s.userData.j||0; s.position.set(F.x + W.x*a*.12 + j*.03, F.y + .05 + a*.07, F.z + W.z*a*.12 + j*.02);
        s.scale.setScalar(.8 + a*.9); s.material.opacity = .5*(1-a/3); }); }
  };
 },
 allerta(){
  const g = new THREE.Group();
  g.add(at(part(box(.8,.03,.22), 0xd8cdb6),0,.015,0), at(part(box(.8,.02,.22), 0xd8cdb6),0,.07,0));
  for (const px of [-.39,.39]) g.add(at(part(box(.02,.06,.2), 0xd8cdb6),px,.05,0));
  const tubes = [];
  COLORI.forEach((c,k)=>{
    const t = new THREE.Group(); at(t,-.285+k*.19,0,0);
    const glass = part(new THREE.CylinderGeometry(.05,.05,.34,24,1,true), 0xdfeaf5, {opacity:.35, side:THREE.DoubleSide, depthWrite:false, shadow:false});
    at(glass,0,.2,0); t.add(glass);
    const h = .1 + k*.07; const liq = part(new THREE.CylinderGeometry(.044,.044,h,24), c.c, {emissive:c.c, ei:.08, angle:40});
    at(liq,0,.035+h/2,0); t.add(liq);
    const lab = textSprite(c.n,.038); at(lab,0,.44,0); t.add(lab);
    pick(t, 'tubo'+k); g.add(t); tubes.push({t, liq});
  });
  function sel(k){ tubes.forEach((o,j)=>{ const y0 = o.t.position.y, y1 = j===k ? .05 : 0; tween(.4,q=>{ o.t.position.y = y0+(y1-y0)*ease(q); }); o.liq.material.emissiveIntensity = j===k ? .35 : .08; });
    const c = COLORI[k]; say(`Allerta ${c.n.toLowerCase()}. ${c.s} Cosa fare: ${c.f}`); }
  return { g, tools: COLORI.map((c,k)=>({label:`Allerta ${c.n.toLowerCase()}`, fn(){ sel(k); }})),
    onPick(id){ if (String(id).startsWith('tubo')) sel(+String(id).slice(4)); },
    choose(){ sel(2); }, update(){} };
 },
 kit(){
  const g = new THREE.Group(), BAG = new THREE.Vector3(.2,.33,-.2);
  const bag = new THREE.Group(); at(bag,.2,0,-.2);
  bag.add(at(part(box(.22,.28,.13), 0xc0392b),0,.14,0), at(part(box(.16,.1,.035), 0xa93226),0,.09,.08), at(part(box(.22,.04,.15), 0xa93226),0,.29,0));
  const strap = part(new THREE.TorusGeometry(.05,.008,6,16,Math.PI), 0x3b3b3b); strap.rotation.x = -Math.PI/2; at(strap,0,.31,0); bag.add(strap);
  g.add(bag);
  const items = []; const mk = (name, obj, x, z, bad) => { at(obj,x,0,z); pick(obj,'item'+items.length); items.push({name, obj, home:obj.position.clone(), bad, in:false}); g.add(obj); };
  const torch = new THREE.Group(); { const b = part(new THREE.CylinderGeometry(.018,.018,.11,14), 0x2c3e50); b.rotation.z = Math.PI/2; at(b,0,.02,0);
    const h = part(new THREE.CylinderGeometry(.028,.02,.035,14), 0x7f8c8d); h.rotation.z = Math.PI/2; at(h,.07,.026,0); torch.add(b,h); }
  const bottle = new THREE.Group(); bottle.add(at(part(new THREE.CylinderGeometry(.026,.026,.11,16), 0x9cc6ea, {opacity:.7}),0,.055,0), at(part(new THREE.CylinderGeometry(.012,.012,.02,10), 0x2f6fb5),0,.12,0));
  const docs = new THREE.Group(); docs.add(at(part(box(.1,.012,.07), 0x2f5aa8),0,.006,0), at(part(box(.09,.006,.065), 0xf4efe1),0,.015,0));
  const meds = new THREE.Group(); meds.add(at(part(box(.07,.04,.05), 0xf6f6f2),0,.02,0), at(part(box(.03,.008,.008), 0x16a34a, {edges:false}),0,.042,0), at(part(box(.008,.008,.03), 0x16a34a, {edges:false}),0,.042,0));
  const bank = new THREE.Group(); bank.add(at(part(box(.05,.02,.1), 0x30353d),0,.01,0));
  const whistle = new THREE.Group(); { const w = part(new THREE.CylinderGeometry(.014,.014,.05,12), 0xf07f1a); w.rotation.z = Math.PI/2; at(w,0,.016,0); whistle.add(w, at(part(box(.02,.02,.02), 0xf07f1a),-.03,.016,0)); }
  const candle = new THREE.Group(); candle.add(at(part(new THREE.CylinderGeometry(.02,.02,.09,14), 0xf3e6c4),0,.045,0));
  const flame = part(new THREE.ConeGeometry(.01,.03,8), 0xffb000, {emissive:0xff8a00, ei:1, edges:false}); at(flame,0,.11,0); candle.add(flame);
  mk('torcia', torch, -.28,.16); mk('bottiglia d’acqua', bottle, -.08,.33); mk('documenti', docs, -.3,-.1);
  mk('farmaci', meds, -.1,-.02); mk('power bank', bank, .08,.32); mk('fischietto', whistle, .3,.28); mk('candela', candle, -.32,.38, true);
  const good = items.filter(o=>!o.bad).length;
  const count = () => items.filter(o=>o.in).length;
  function put(o){
    if (o.in) return;
    if (o.bad){ const x0 = o.obj.position.x; tween(.6,q=>{ o.obj.position.x = x0 + Math.sin(q*Math.PI*6)*.015*(1-q); }); glow(o.obj,0xd23a2f,.6); setTimeout(()=>glow(o.obj,0,0),900);
      say('La candela resta fuori: per fare luce usa la torcia, le candele possono provocare un incendio.'); return; }
    o.in = true; const a = o.obj.position.clone();
    tween(.8,q=>{ o.obj.position.lerpVectors(a,BAG,ease(q)); o.obj.position.y += Math.sin(Math.PI*q)*.18; o.obj.scale.setScalar(1-.6*q); }, ()=>{ o.obj.visible = false; });
    const n = count(); say(n===good ? `Zaino pronto: ${n} oggetti su ${good}. La candela è rimasta fuori.` : `Nello zaino: ${o.name}. Oggetti messi: ${n} su ${good}.`);
  }
  const map = {0:items[0], 1:items[6], 2:items[5]};
  return { g, tools:[
      {label:'Prepara lo zaino', fn(){ items.filter(o=>!o.bad).forEach((o,k)=>setTimeout(()=>put(o), k*250)); }},
      {label:'Svuota lo zaino', fn(){ items.forEach(o=>{ o.in = false; o.obj.visible = true; o.obj.position.copy(o.home); o.obj.scale.setScalar(1); }); say('Lo zaino è vuoto. Tocca gli oggetti per metterli dentro.'); }} ],
    onPick(id){ if (String(id).startsWith('item')) put(items[+String(id).slice(4)]); },
    choose(i){ Object.values(map).forEach((o,k)=>glow(o.obj,0xffb000,k===i?.55:0)); },
    update(dt,t){ flame.scale.y = 1+.2*Math.sin(t*12); }
  };
 },
 caldo(){
  const g = new THREE.Group();
  g.add(at(part(box(.84,.012,.95), 0xd9cfb4),0,.006,-.03));
  g.add(at(part(box(.84,.004,.16), 0x8d8f94, {edges:false}),0,.014,.22));
  const h1 = casetta(.36,.22,.2), h2 = casetta(.3,.2,.2); at(h1,-.2,0,-.2); at(h2,.22,0,-.22); g.add(h1, h2);
  const shut = []; [-.28,-.12].forEach(x=>{ const s = at(part(box(.09,.01,.012), 0x6b7c93),x,.205,-.093); g.add(s); shut.push(s); });
  const tree = new THREE.Group(); tree.add(at(part(new THREE.CylinderGeometry(.01,.014,.1,8), 0x6b4f33),0,.05,0), at(part(new THREE.SphereGeometry(.07,12,9), 0x3f7a45),0,.14,0)); at(tree,.05,0,.05); g.add(tree);
  const sunM = part(new THREE.SphereGeometry(.05,20,14), 0xffc107, {emissive:0xffb000, ei:.9, edges:false, shadow:false}); g.add(sunM);
  const thermo = new THREE.Group(); at(thermo,.36,0,.32); g.add(thermo);
  thermo.add(at(part(new THREE.CylinderGeometry(.02,.02,.3,14,1,true), 0xdfeaf5, {opacity:.35, side:THREE.DoubleSide, depthWrite:false, shadow:false}),0,.17,0));
  const liq = part(new THREE.CylinderGeometry(.014,.014,1,14), 0xd23a2f, {edges:false}); thermo.add(liq);
  thermo.add(at(part(new THREE.SphereGeometry(.026,14,10), 0xd23a2f, {edges:false}),0,.025,0));
  const lab = textSprite('Ore 9', .04); g.add(lab);
  const p = pawn(); at(p,-.2,0,.0); g.add(p);
  let hour = 9, closed = false;
  function setHour(h){ hour = h; const t = (h-6)/15;
    sunM.position.set(-.45+.9*t, .15+.42*Math.sin(Math.PI*t), -.42);
    const hot = h>=11 && h<18; sunM.material.color.setHex(hot ? 0xff7a1a : 0xffd54a); sunM.material.emissive.setHex(hot ? 0xff5a00 : 0xffb000);
    const lv = .05 + .2*Math.sin(Math.PI*Math.min(1,Math.max(0,(h-6)/14))); liq.scale.y = lv; liq.position.y = .04 + lv/2;
    lab.material.map.dispose(); const n = textSprite('Ore ' + h, .04); lab.material = n.material; lab.scale.copy(n.scale); lab.position.set(sunM.position.x, sunM.position.y+.08, sunM.position.z);
    say(hot ? `Ore ${h}: sono le ore più calde, dalle 11 alle 18. Resta al fresco ed evita gli sforzi.` : `Ore ${h}: fuori dalle ore più calde. Se esci, porta acqua e cappello.`);
    const inp = document.getElementById('r-caldo-0'); if (inp) inp.value = h; }
  setHour(9);
  return { g, tools:[
      {range:true, label:'Ora del giorno', min:6, max:21, value:9, fn(v){ setHour(v); }},
      {label:'Abbassa le tapparelle', fn(){ closed = !closed; shut.forEach(s=>{ const a = s.scale.y, b = closed ? 9 : 1; tween(.5,q=>{ s.scale.y = a+(b-a)*ease(q); s.position.y = .205 - (s.scale.y-1)*.005; }); });
        this.textContent = closed ? 'Alza le tapparelle' : 'Abbassa le tapparelle';
        say(closed ? 'Tapparelle abbassate: nelle ore di sole diretto la casa resta più fresca.' : 'Tapparelle alzate.'); }} ],
    choose(i){ setHour([13,9,15][i]); moveTo(p, new THREE.Vector3([-.05,-.1,.15][i], 0, .22), 1, .04); },
    update(){} };
 },
 temporale(){
  const g = new THREE.Group();
  g.add(at(part(box(.84,.012,.95), 0x8fae6a),0,.006,-.03));
  const tree = new THREE.Group(); tree.add(at(part(new THREE.CylinderGeometry(.012,.016,.16,8), 0x6b4f33),0,.08,0), at(part(new THREE.ConeGeometry(.07,.2,9), 0x3f7a45),0,.24,0)); at(tree,-.25,0,-.2); g.add(pick(tree,0));
  const roof = new THREE.Group(); at(roof,.25,0,-.25);
  for (const [x,z] of [[-.08,-.05],[.08,-.05],[-.08,.05],[.08,.05]]) roof.add(at(part(box(.008,.14,.008), 0x9aa0a8),x,.07,z));
  roof.add(at(part(box(.2,.008,.14), 0x9aa0a8),0,.145,0)); g.add(pick(roof,1));
  const safe = new THREE.Group(); const hs = casetta(.2,.16,.16); at(hs,.2,0,.18); safe.add(hs);
  safe.add(at(carro(0x2f6fb5),-.2,0,.28)); g.add(pick(safe,2));
  const cloud = new THREE.Group(); [[0,0,0,.11],[.1,.01,.03,.09],[-.1,0,.02,.08],[.04,.04,-.04,.08]].forEach(([x,y,z,r])=>cloud.add(at(part(new THREE.SphereGeometry(r,14,10), 0x6b7280, {edges:false, shadow:false}),x,y,z)));
  at(cloud,-.15,.62,-.25); g.add(cloud);
  const bolt = new THREE.Group(); const pts = [[-.15,.55],[-.2,.45],[-.17,.44],[-.23,.33],[-.2,.32],[-.25,.25]];
  for (let k=0;k<pts.length-1;k++){ const [x1,y1]=pts[k],[x2,y2]=pts[k+1]; const L = Math.hypot(x2-x1,y2-y1);
    const s = part(box(.012,L,.012), 0xfff3a0, {emissive:0xffe066, ei:1, edges:false, shadow:false}); at(s,(x1+x2)/2,(y1+y2)/2,-.2); s.rotation.z = Math.atan2(x2-x1,y2-y1)*-1; bolt.add(s); }
  bolt.visible = false; g.add(bolt);
  const flash = new THREE.PointLight(0xfff6c8, 0, 2); at(flash,-.2,.5,-.2); g.add(flash);
  const p = pawn(); at(p,0,0,.05); g.add(p);
  const T = [new THREE.Vector3(-.21,0,-.15), new THREE.Vector3(.25,0,-.25), new THREE.Vector3(.2,0,.32)];
  return { g, tools:[{label:'Arriva il fulmine', fn(){ bolt.visible = true; tween(.5,q=>{ flash.intensity = 6*(1-q); }, ()=>{ bolt.visible = false; });
      say('Il fulmine colpisce l’albero isolato: è il punto più alto del prato. Al riparo si sta nella casa o in auto con i finestrini chiusi.'); }}],
    choose(i){ [tree,roof,safe].forEach((o,k)=>glow(o,0xffb000,k===i?.45:0)); moveTo(p, T[i], 1, .05); },
    update(dt,t){ cloud.position.x = -.15 + Math.sin(t*.4)*.03; } };
 },
 vento(){
  const g = new THREE.Group();
  g.add(at(part(box(.84,.012,.95), 0xb9b4a8),0,.006,-.03));
  const pal = new THREE.Group(); pal.add(at(part(box(.3,.42,.2), 0xe6dfcf),0,.21,0));
  const cornice = at(part(box(.34,.025,.06), 0xc9bfa8),0,.43,.12); pal.add(cornice);
  pal.add(at(part(box(.06,.1,.01), 0x6b4f33),.08,.05,.101));
  for (const x of [-.08,.04]) for (const y of [.18,.32]) pal.add(at(part(box(.06,.06,.01), 0x9cc6ea),x,y,.101));
  at(pal,-.2,0,-.28); g.add(pal);
  const corniceZone = new THREE.Group(); g.add(pick(corniceZone,0));
  pick(cornice,0);
  const door = new THREE.Group(); g.add(door);
  const scaf = new THREE.Group(); at(scaf,.25,0,-.3);
  for (const x of [-.08,.08]) for (const z of [-.04,.04]) scaf.add(at(part(box(.006,.34,.006), 0x8a8f99),x,.17,z));
  for (const y of [.12,.24,.34]) scaf.add(at(part(box(.18,.01,.09), 0xc9a86b),0,y,0)); g.add(scaf);
  const bill = new THREE.Group(); at(bill,.24,0,.16);
  for (const x of [-.08,.08]) bill.add(at(part(box(.01,.18,.01), 0x5b6270),x,.09,0));
  const panel = at(part(box(.24,.12,.01), 0xf2c12e),0,.22,0); bill.add(panel); g.add(pick(bill,2));
  const tree = new THREE.Group(); tree.add(at(part(new THREE.CylinderGeometry(.01,.014,.12,8), 0x6b4f33),0,.06,0), at(part(new THREE.SphereGeometry(.07,12,9), 0x3f7a45),0,.16,0)); at(tree,-.28,0,.22); g.add(tree);
  const leaves = []; for (let k=0;k<18;k++){ const l = part(box(.014,.003,.01), 0x5e8d43, {edges:false, shadow:false}); l.userData.o = Math.random(); g.add(l); leaves.push(l); }
  const p = pawn(); at(p,0,0,.25); g.add(p);
  let wind = .7;
  const T = [new THREE.Vector3(-.2,0,-.13), new THREE.Vector3(-.12,0,-.17), new THREE.Vector3(.24,0,.22)];
  return { g, tools:[{range:true, label:'Forza del vento', min:0, max:100, value:70, fn(v){ wind = v/100; say(v>60 ? 'Raffiche forti: cartelloni, impalcature e alberi possono cedere o perdere pezzi.' : 'Vento moderato.'); }}],
    choose(i){ [cornice,null,bill].forEach((o,k)=>o && glow(o,0xffb000,k===i?.5:0)); moveTo(p, T[i], 1, .04, ()=>{ if (i===1) say('Sei dentro l’edificio: resta lontano dalle finestre.'); }); },
    update(dt,t){ const s = RM() ? .3 : 1;
      bill.rotation.z = Math.sin(t*6)*.05*wind*s; tree.rotation.z = Math.sin(t*3.3)*.12*wind*s; scaf.rotation.z = Math.sin(t*5)*.015*wind*s;
      leaves.forEach(l=>{ l.userData.o = (l.userData.o + dt*(.08+.5*wind)*s) % 1; const o = l.userData.o; l.position.set(-.42+.84*o, .05+.25*Math.abs(Math.sin(o*9+l.id)), -.45+((l.id*37)%90)/100); l.rotation.set(o*20,o*13,0); l.visible = wind>.15; }); } };
 },
 blackout(){
  const g = new THREE.Group(), room = new THREE.Group(); g.add(room);
  room.add(at(part(box(.84,.02,.9), 0xe9e4d6),0,.01,-.05), at(part(box(.84,.5,.02)),0,.26,-.49), at(part(box(.02,.5,.9)),-.41,.26,-.05));
  const tbl = new THREE.Group(); tbl.add(at(part(box(.26,.02,.18), 0xc79a63),0,.14,0));
  for (const [x,z] of [[-.11,-.07],[.11,-.07],[-.11,.07],[.11,.07]]) tbl.add(at(part(new THREE.CylinderGeometry(.008,.008,.13,8), 0xb08654),x,.07,z));
  at(tbl,-.05,0,.05); room.add(tbl);
  const candle = new THREE.Group(); candle.add(at(part(new THREE.CylinderGeometry(.016,.016,.06,12), 0xf3e6c4),0,.03,0));
  const flame = part(new THREE.ConeGeometry(.008,.024,8), 0xffb000, {emissive:0xff8a00, ei:1, edges:false}); at(flame,0,.075,0); flame.visible = false; candle.add(flame);
  at(candle,-.12,.15,.06); room.add(pick(candle,0));
  const torch = new THREE.Group(); { const b = part(new THREE.CylinderGeometry(.014,.014,.08,12), 0x2c3e50); b.rotation.z = Math.PI/2; at(b,0,.014,0); torch.add(b, at(part(new THREE.CylinderGeometry(.02,.015,.02,12), 0x7f8c8d),.05,.016,0)); torch.children[1].rotation.z = Math.PI/2; }
  at(torch,.03,.15,.06); room.add(pick(torch,1));
  const beam = new THREE.SpotLight(0xfff2cc, 0, 1.4, .45, .5); at(beam,.08,.17,.06); beam.target.position.set(.4,0,-.3); room.add(beam, beam.target);
  const fridge = new THREE.Group(); fridge.add(at(part(box(.14,.32,.13), 0xf4f6f8),0,.16,0));
  const fdoor = part(box(.14,.32,.01), 0xe9edf1); const hinge = new THREE.Group(); at(hinge,-.07,.16,.07); at(fdoor,.07,0,0); hinge.add(fdoor); fridge.add(hinge);
  at(fridge,.3,.02,-.38); room.add(pick(fridge,2));
  const tv = at(part(box(.2,.12,.02), 0x22262e),-.1,.3,-.475); room.add(tv);
  const lamp = part(new THREE.SphereGeometry(.03,14,10), 0xfff4c2, {emissive:0xffe9a0, ei:1, edges:false, shadow:false}); at(lamp,0,.47,-.1); room.add(lamp);
  const p = pawn(); at(p,.12,.02,.25); room.add(p);
  let dark = false;
  function setDark(on){ dark = on; hemi.intensity = on ? .25 : 1.6; sun.intensity = on ? .25 : 2.2; lamp.material.emissiveIntensity = on ? 0 : 1; tv.material.color.setHex(on ? 0x111317 : 0x22262e);
    say(on ? 'È andata via la corrente: la stanza è al buio.' : 'La corrente è tornata.'); }
  return { g, tools:[{label:'Va via la corrente', fn(){ setDark(!dark); this.textContent = dark ? 'Torna la corrente' : 'Va via la corrente'; }}],
    choose(i){ if (!dark){ setDark(true); const b = document.getElementById('t-blackout-0'); if (b) b.textContent = 'Torna la corrente'; }
      flame.visible = i===0; beam.intensity = i===1 ? 6 : 0; [candle,torch,fridge].forEach((o,k)=>glow(o,0xffb000,k===i?.4:0));
      const a = hinge.rotation.y, b = i===2 ? -1.3 : 0; tween(.6,q=>{ hinge.rotation.y = a+(b-a)*ease(q); });
      if (i===0) say('Una candela accesa al buio può provocare un incendio.'); else if (i===1) say('Con la torcia vedi senza rischi. Ora scollega gli elettrodomestici.'); else say('Aprendo il frigorifero il freddo esce: tienilo chiuso.'); },
    update(dt,t){ if (flame.visible) flame.scale.y = 1+.2*Math.sin(t*12); },
    dispose(){ hemi.intensity = 1.6; sun.intensity = 2.2; } };
 },
 gas(){
  const g = new THREE.Group(), EARTH = 0x9c8461;
  g.add(at(part(box(.2,.16,.5), EARTH),-.32,.08,-.2), at(part(box(.18,.16,.5), EARTH),.33,.08,-.2), at(part(box(.84,.16,.1), EARTH),0,.08,-.4));
  for (const [x,w] of [[-.32,.2],[.33,.18]]) g.add(at(part(box(w,.008,.5), 0x7fa35a, {edges:false}),x,.164,-.2));
  g.add(at(part(box(.84,.008,.3), 0x7fa35a, {edges:false}),0,.004,.3));
  const H = new THREE.Group(); g.add(H);
  H.add(at(part(box(.46,.015,.36), 0xe6dfcf),.02,.0075,-.17), at(part(box(.46,.36,.015)),.02,.18,-.35), at(part(box(.015,.36,.36)),-.21,.18,-.17), at(part(box(.015,.36,.36)),.245,.18,-.17));
  H.add(at(part(box(.3,.015,.36), 0xe6dfcf),-.06,.167,-.17));
  for (let k=0;k<5;k++) H.add(at(part(box(.08,.012,.05), 0xd8cdb6),.19,.03+k*.03,-.3+k*.05));
  const animal = new THREE.Group(); animal.add(at(part(box(.06,.022,.03), 0x8a6d4b),0,.012,0), at(part(new THREE.SphereGeometry(.016,10,8), 0x8a6d4b),.04,.014,0)); at(animal,-.1,.015,-.2); animal.rotation.y = .4; H.add(animal);
  const co2 = part(box(1,1,1), 0x7d8fa8, {opacity:.0, edges:false, shadow:false, depthWrite:false}); H.add(co2);
  const lab = textSprite('CO₂: non si vede', .03); at(lab,-.06,.08,-.04); lab.visible = false; g.add(lab);
  const L1 = textSprite('Cantina', .03); at(L1,.02,.135,-.02); g.add(L1);
  const p = pawn(); at(p,.19,.17,-.08); g.add(p);
  let show = false, lvl = .5;
  function setLvl(v){ lvl = v; const h = .01 + v*.12; co2.scale.set(.43,h,.34); co2.position.set(.02,.015+h/2,-.17); }
  setLvl(.5);
  function vis(){ co2.material.opacity = show ? .5 : 0; lab.visible = show; }
  return { g, tools:[
      {label:'Mostra il gas', fn(){ show = !show; vis(); this.textContent = show ? 'Nascondi il gas' : 'Mostra il gas';
        say(show ? 'Così si vedrebbe la CO₂: pesante, si raccoglie in basso nella cantina. Nella realtà è invisibile e senza odore.' : 'Nella realtà la CO₂ non si vede e non ha odore.'); }},
      {range:true, label:'Gas accumulato in cantina', min:0, max:100, value:50, fn(v){ setLvl(v/100); if (!show){ show = true; vis(); } }} ],
    choose(i){ const T = [new THREE.Vector3(-.06,.015,-.18), new THREE.Vector3(.1,.004,.32), new THREE.Vector3(.12,.015,-.2)];
      moveTo(p, T[i], 1.1, .06, ()=>{ glow(p, i===1 ? 0 : 0xd23a2f, i===1 ? 0 : .5); });
      say(i===1 ? 'Sei all’aria aperta. Ora chiama il 112 e tieni lontane le altre persone.' : 'Sei rimasto dove si accumula il gas: è il punto più pericoloso.'); },
    update(){} };
 },
 maremoto(){
  const g = new THREE.Group();
  g.add(at(part(box(.84,.02,.95), 0xe8d7a8),0,.01,-.03));
  const wet = at(part(box(.84,.004,.3), 0xc6b48a, {edges:false}),0,.022,-.25); g.add(wet);
  const sea = part(box(.84,.04,1), 0x3f86c9, {opacity:.8, edges:false, shadow:false}); g.add(sea);
  const hill = part(new THREE.CylinderGeometry(.1,.2,.2,8), 0x8f9a5e); at(hill,.26,.1,.28); g.add(hill);
  const hut = casetta(.12,.1,.1); at(hut,-.25,0,.3); g.add(hut);
  const umb = new THREE.Group(); umb.add(at(part(new THREE.CylinderGeometry(.004,.004,.12,6), 0x8a8f99),0,.06,0), at(part(new THREE.ConeGeometry(.06,.03,10), 0xd23a2f),0,.13,0)); at(umb,-.05,0,0); g.add(umb);
  const p = pawn(); at(p,.0,.02,.05); g.add(p);
  let zFront = -.15;
  function setSea(front){ zFront = front; const back = -.5, d = front-back; sea.scale.z = d; sea.position.set(0,.03,(front+back)/2); }
  setSea(-.15);
  function to(front, dur, after){ const a = zFront; tween(dur, q=>setSea(a+(front-a)*ease(q)), after); }
  return { g, tools:[
      {label:'Il mare si ritira', fn(){ to(-.42, 2); say('Il mare si ritira all’improvviso e scopre la spiaggia: è un segnale naturale di maremoto. Allontanati subito.'); }},
      {label:'Arriva l’onda', fn(){ to(.24, 1.6); say('L’acqua invade la spiaggia. Chi è sulla collina è al sicuro; la prima onda può non essere la più grande.'); }},
      {label:'Ricomincia', fn(){ setSea(-.15); p.position.set(0,.02,.05); say('La spiaggia è tornata com’era.'); }} ],
    choose(i){ const T = [new THREE.Vector3(.02,.02,-.3), new THREE.Vector3(0,.02,.05), new THREE.Vector3(.26,.2,.28)]; moveTo(p, T[i], 1.3, .05); },
    update(){} };
 },
 industriale(){
  const g = new THREE.Group();
  g.add(at(part(box(.84,.012,.95), 0xc9cfb8),0,.006,-.03));
  const fab = new THREE.Group(); fab.add(at(part(box(.26,.12,.16), 0xbfc5cc),0,.06,0));
  for (const x of [-.06,.06]) fab.add(at(part(new THREE.CylinderGeometry(.018,.022,.22,10), 0x9aa0a8),x,.17,-.03));
  fab.add(at(part(new THREE.CylinderGeometry(.05,.05,.1,16), 0xd8dce1),.18,.05,.03)); at(fab,-.25,0,-.32); g.add(fab);
  const home = new THREE.Group(); const hc = casetta(.2,.16,.16); home.add(hc);
  const wins = []; [-.05,.05].forEach(x=>{ const w = at(part(box(.045,.05,.01), 0x9cc6ea),x,.1,.081); w.rotation.y = -1.2; home.add(w); wins.push(w); });
  at(home,.22,0,.18); g.add(pick(home,1));
  const school = new THREE.Group(); school.add(at(part(box(.2,.12,.12), 0xf0d9b5),0,.06,0), at(part(box(.004,.12,.004), 0x8a8f99),.12,.06,0), at(part(box(.04,.025,.003), 0x2f6fb5),.14,.11,0));
  at(school,-.2,0,.28); g.add(pick(school,2));
  const cloudMat = new THREE.MeshStandardMaterial({color:0xb7c45a, transparent:true, opacity:.4, depthWrite:false, roughness:1});
  const puffs = []; for (let k=0;k<30;k++){ const s = new THREE.Mesh(new THREE.SphereGeometry(.03,8,6), cloudMat.clone()); s.userData.age = Math.random()*4; s.userData.j = Math.random()-.5; g.add(s); puffs.push(s); }
  const p = pawn(); at(p,.05,0,.05); g.add(p);
  let shut = false;
  const W = new THREE.Vector3(.55,0,.6).normalize(), F = new THREE.Vector3(-.25,.26,-.35);
  return { g, tools:[{label:'Chiudi porte e finestre', fn(){ shut = !shut; wins.forEach(w=>{ const a = w.rotation.y, b = shut ? 0 : -1.2; tween(.5,q=>{ w.rotation.y = a+(b-a)*ease(q); }); });
      this.textContent = shut ? 'Riapri le finestre' : 'Chiudi porte e finestre';
      say(shut ? 'Finestre chiuse e ventilazione spenta: la casa ti ripara dalla nube.' : 'Finestre aperte: con una nube in arrivo vanno chiuse.'); }}],
    choose(i){ const T = [new THREE.Vector3(-.1,0,-.12), new THREE.Vector3(.22,0,.18), new THREE.Vector3(-.2,0,.4)];
      moveTo(p, T[i], 1.3, .04, ()=>{ if (i===1){ p.visible = false; if (!shut){ document.getElementById('t-industriale-0')?.click(); } } });
      p.visible = true; [null,home,school].forEach((o,k)=>o && glow(o,0xffb000,k===i?.4:0)); },
    update(dt){ const sp = RM() ? .35 : 1;
      puffs.forEach(s=>{ let a = s.userData.age += dt*sp; if (a>4){ a = s.userData.age = 0; s.userData.j = Math.random()-.5; }
        s.position.set(F.x + W.x*a*.15 + s.userData.j*.08, F.y + a*.015, F.z + W.z*a*.15 - s.userData.j*.06);
        s.scale.setScalar(.8+a*.7); s.material.opacity = .45*(1-a/4); }); } };
 },
 radiologico(){
  const g = new THREE.Group(), room = new THREE.Group(); g.add(room);
  room.add(at(part(box(.6,.02,.6), 0xe9e4d6),-.08,.01,-.15), at(part(box(.6,.4,.02)),-.08,.21,-.44), at(part(box(.02,.4,.6)),-.37,.21,-.15), at(part(box(.02,.4,.6)),.21,.21,-.15));
  const win = new THREE.Group(); win.add(at(part(box(.16,.12,.012), 0xdfe8f2),0,0,0)); const pane = at(part(box(.07,.1,.01), 0x9cc6ea),.04,0,.01); win.add(pane); at(win,-.1,.25,-.43); room.add(win);
  const fan = new THREE.Group(); for (let k=0;k<3;k++){ const b = part(box(.08,.004,.018), 0xb8c0ca); b.position.x = .04; const r = new THREE.Group(); r.rotation.y = k*2.09; r.add(b); fan.add(r); }
  at(fan,-.08,.395,-.15); room.add(fan);
  const tbl = new THREE.Group(); tbl.add(at(part(box(.2,.015,.14), 0xc79a63),0,.12,0)); for (const [x,z] of [[-.08,-.05],[.08,-.05],[-.08,.05],[.08,.05]]) tbl.add(at(part(new THREE.CylinderGeometry(.007,.007,.11,8), 0xb08654),x,.06,z)); at(tbl,-.15,0,-.1); room.add(tbl);
  const radio = at(part(box(.06,.035,.03), 0x30353d),-.18,.145,-.1); room.add(radio);
  const iodio = new THREE.Group(); iodio.add(at(part(box(.03,.04,.02), 0xf6f6f2),0,.02,0)); at(iodio,-.1,.128,-.08); room.add(pick(iodio,2));
  const rings = []; for (let k=0;k<3;k++){ const r = new THREE.Mesh(new THREE.TorusGeometry(.03,.002,6,24), new THREE.MeshBasicMaterial({color:0x2f6fb5, transparent:true})); r.rotation.x = Math.PI/2; at(r,-.18,.17,-.1); r.userData.o = k/3; room.add(r); rings.push(r); }
  const car = carro(0x2f6fb5); at(car,.33,0,.25); g.add(pick(car,0));
  const p = pawn(); at(p,.0,.02,.2); g.add(p);
  let closed = false, spin = 1;
  return { g, tools:[{label:'Chiudi le finestre e spegni la ventilazione', fn(){ closed = !closed; spin = closed ? 0 : 1; const a = pane.position.x, b = closed ? -.04 : .04; tween(.5,q=>{ pane.position.x = a+(b-a)*ease(q); });
      this.textContent = closed ? 'Riapri e riaccendi' : 'Chiudi le finestre e spegni la ventilazione';
      say(closed ? 'Finestre chiuse e ventilazione spenta. Ora resta in un locale interno e ascolta la radio.' : 'Finestre aperte e ventilazione accesa.'); }}],
    choose(i){ [car,null,iodio].forEach((o,k)=>o && glow(o,0xffb000,k===i?.5:0));
      const T = [new THREE.Vector3(.33,0,.4), new THREE.Vector3(-.05,.02,-.25), new THREE.Vector3(-.08,.02,-.02)]; moveTo(p, T[i], 1.1, .05);
      say(['Mettersi in viaggio espone di più: con il riparo al chiuso si resta in casa.','Sei al chiuso, in un locale interno. Segui la radio e i canali ufficiali.','Lo iodio si prende solo se lo dispongono le autorità sanitarie.'][i]); },
    update(dt,t){ fan.rotation.y += dt*8*spin*(RM() ? .3 : 1); rings.forEach(r=>{ r.userData.o = (r.userData.o + dt*.5) % 1; const o = r.userData.o; r.scale.setScalar(1+o*2.5); r.material.opacity = .6*(1-o); }); } };
 },
 siccita(){
  const g = new THREE.Group();
  g.add(at(part(box(.84,.012,.95), 0xc9b48a),0,.006,-.03));
  const crack = new THREE.Group(); for (let k=0;k<14;k++){ const c = part(box(.08,.003,.004), 0x7a6646, {edges:false, shadow:false}); c.rotation.y = k*1.3; at(c,-.3+((k*29)%60)/100,.013,.1+((k*17)%30)/100); crack.add(c); } g.add(crack);
  const basin = new THREE.Group(); at(basin,-.15,0,-.3);
  basin.add(at(part(box(.4,.015,.26), 0xb8b0a0),0,.008,0)); for (const [x,z,w,d] of [[0,-.13,.4,.012],[0,.13,.4,.012],[-.2,0,.012,.26],[.2,0,.012,.26]]) basin.add(at(part(box(w,.12,d), 0xd8d2c4),x,.06,z));
  const water = part(box(.38,1,.24), 0x3f86c9, {opacity:.7, edges:false, shadow:false}); basin.add(water); g.add(basin);
  const home = casetta(.18,.15,.15); at(home,.25,0,-.25); g.add(pick(home,1));
  const car = carro(0x2f6fb5); at(car,.25,0,.22); g.add(pick(car,0));
  const hose = new THREE.Mesh(new THREE.TorusGeometry(.05,.005,6,16,Math.PI*1.4), new THREE.MeshStandardMaterial({color:0x2e9e4f})); hose.rotation.x = Math.PI/2; at(hose,.14,.01,.22); g.add(hose);
  const font = new THREE.Group(); font.add(at(part(new THREE.CylinderGeometry(.02,.025,.12,10), 0x8a8f99),0,.06,0), at(part(box(.04,.008,.008), 0x8a8f99),.02,.11,0)); at(font,-.3,0,.3); g.add(pick(font,2));
  const p = pawn(); at(p,.05,0,.05); g.add(p);
  function setLvl(v){ const h = .005 + v*.1; water.scale.y = h; water.position.y = .015+h/2;
    say(v<.25 ? 'Il serbatoio è quasi vuoto: ogni litro risparmiato serve per bere e cucinare.' : v<.6 ? 'Il livello scende: è il momento delle ordinanze e del risparmio.' : 'Il serbatoio è ancora pieno.'); }
  setLvl(.35);
  return { g, tools:[{range:true, label:'Livello del serbatoio', min:0, max:100, value:35, fn(v){ setLvl(v/100); }}],
    choose(i){ [car,home,font].forEach((o,k)=>glow(o,0xffb000,k===i?.45:0)); const T = [new THREE.Vector3(.13,0,.3), new THREE.Vector3(.2,0,-.1), new THREE.Vector3(-.26,0,.36)]; moveTo(p, T[i], 1, .04); },
    update(){} };
 }
};

let current = null;
function mount(i){
  if (current){ current.dispose?.(); anchor.remove(current.g); current.g.traverse(o=>{ o.geometry?.dispose(); if (o.material){ o.material.map?.dispose(); o.material.dispose(); } }); }
  current = BUILD[CH[i].key](); anchor.add(current.g);
  popUp(current.g); atmosfera(CH[i].key);
}

/* ---------- Pannello ---------- */
const dots = $('dots');
CH.forEach((c,k)=>{ const b = document.createElement('button'); b.className = 'dot'; b.textContent = k+1; b.setAttribute('aria-label',`Capitolo ${k+1}: ${c.title}`); b.onclick = ()=>goTo(k); dots.append(b); });

function renderPanel(i){
  const c = CH[i];
  $('kicker').textContent = c.kicker; $('titolo').textContent = c.title; $('intro').textContent = c.intro; $('question').textContent = c.q;
  [...dots.children].forEach((d,k)=> k===i ? d.setAttribute('aria-current','step') : d.removeAttribute('aria-current'));
  $('prev').disabled = i===0; $('next').disabled = i===CH.length-1;
  const tools = $('tools'); tools.replaceChildren();
  current.tools.forEach((t,k)=>{
    if (t.range){ const w = document.createElement('div'); w.className = 'range';
      const id = `r-${c.key}-${k}`; w.innerHTML = `<label for="${id}">${t.label}</label><input type="range" id="${id}" min="${t.min}" max="${t.max}" value="${t.value}">`;
      w.querySelector('input').addEventListener('input', e=>t.fn(+e.target.value)); tools.append(w); }
    else { const b = document.createElement('button'); b.type = 'button'; b.textContent = t.label; b.id = `t-${c.key}-${k}`; b.addEventListener('click', function(){ t.fn.call(this); }); tools.append(b); }
  });
  const opts = $('opts'); opts.replaceChildren();
  c.opts.forEach((o,k)=>{ const b = document.createElement('button'); b.type = 'button'; b.className = 'opt'; b.id = `o-${c.key}-${k}`;
    b.setAttribute('aria-pressed','false'); b.innerHTML = `<b aria-hidden="true">${LETTERE[k]}</b><span></span>`; b.querySelector('span').textContent = o.t;
    b.onclick = ()=>choose(k); opts.append(b); });
  $('answer').hidden = true; $('flapBtn').textContent = 'Alza il lembo e scopri la risposta';
  $('src').replaceChildren('Per saperne di più: ');
  c.srcs.forEach((f,k)=>{ const a = document.createElement('a'); a.href = BASE + f.u.replace(/^\//,''); a.textContent = f.t; if (k) $('src').append('; '); $('src').append(a); });
  $('src').append('.');
  say(''); voceStop(); disegnaConta();
}
function choose(k){
  choice = k; [...$('opts').children].forEach((b,j)=>b.setAttribute('aria-pressed', String(j===k)));
  current.choose?.(k); if (revealed) showAnswer();
}
function showAnswer(){
  const c = CH[chapter], right = c.opts.findIndex(o=>o.ok);
  $('answer').hidden = false; $('answerText').textContent = c.answer;
  const v = $('verdict');
  if (choice < 0){ v.textContent = 'Non hai fatto una previsione: scegli una risposta e confrontala.'; v.className = 'verdict'; }
  else if (choice === right){ v.textContent = 'Previsione giusta.'; v.className = 'verdict ok'; }
  else { v.textContent = `Non è la scelta sicura. ${c.opts[choice].why}`; v.className = 'verdict ko'; }
  [...$('opts').children].forEach((b,j)=>b.classList.toggle('right', j===right));
  segnaVisto(c.key);
}
function toggleFlap(){
  revealed = !revealed; setFlap(revealed);
  $('flapBtn').textContent = revealed ? 'Abbassa il lembo' : 'Alza il lembo e scopri la risposta';
  if (revealed){ showAnswer(); const right = CH[chapter].opts.findIndex(o=>o.ok); if (choice === right) festa(); else if (choice >= 0) scuoti(); } else { $('answer').hidden = true; [...$('opts').children].forEach(b=>b.classList.remove('right')); }
}
$('flapBtn').onclick = toggleFlap;
$('prev').onclick = ()=>goTo(chapter-1);
$('next').onclick = ()=>goTo(chapter+1);
addEventListener('hashchange', ()=>{ const m = /^#capitolo-(\d{1,2})$/.exec(location.hash); if (m) goTo(Math.min(CH.length, Math.max(1,+m[1]))-1); });
ROOT.addEventListener('keydown', e=>{
  if (e.target.closest('input,textarea,select')) return;
  if (e.key==='ArrowRight') goTo(chapter+1); else if (e.key==='ArrowLeft') goTo(chapter-1);
});

function goTo(i){
  if (busy || i<0 || i>=CH.length || i===chapter) return;
  const dir = i > chapter ? 1 : -1; busy = true;
  if (revealed){ revealed = false; setFlap(false); }
  choice = -1;
  const swap = ()=>{ chapter = i; drawLeft(i); drawRight(i); mount(i); renderPanel(i); try{ history.replaceState(null,'','#capitolo-'+(i+1)); }catch(_){} };
  if (RM()){ swap(); busy = false; return; }
  sheet.visible = true;
  const from = dir>0 ? 0 : Math.PI, to = dir>0 ? Math.PI : 0; let swapped = false;
  tween(.85, p=>{ sheetPivot.rotation.z = from + (to-from)*ease(p);
      if (!swapped && p>=.5){ swapped = true; swap(); }
      current.g.scale.setScalar(p<.5 ? Math.max(.001, 1-p*2) : 1); },
    ()=>{ sheet.visible = false; busy = false; current.g.scale.setScalar(1); });
}

/* ---------- Strumenti per la classe ----------
   Lettura ad alta voce (Web Speech API, voce italiana, velocità condivisa con
   il resto del sito), conteggio delle previsioni della classe (solo in
   memoria), avanzamento salvato nel browser e attestato da stampare. */
const voce = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
const btnVoce = $('ascolta');
function voceStop(){ if (voce){ speechSynthesis.cancel(); } btnVoce.setAttribute('aria-pressed','false'); }
function testoDaLeggere(){
  const c = CH[chapter], parti = [c.kicker + '.', c.title + '.', c.intro, c.q];
  c.opts.forEach((o,k)=>parti.push(`Risposta ${LETTERE[k]}: ${o.t}.`));
  if (revealed) parti.push($('verdict').textContent, c.answer);
  return parti.join(' ');
}
if (voce){
  btnVoce.hidden = false;
  btnVoce.onclick = ()=>{
    if (btnVoce.getAttribute('aria-pressed')==='true'){ voceStop(); return; }
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(testoDaLeggere()); u.lang = 'it-IT';
    let rate = .95; try { rate = parseFloat(localStorage.getItem('pcgenzano-tts-rate')) || .95; } catch(_){}
    u.rate = rate;
    const v = speechSynthesis.getVoices().find(x=>x.lang==='it-IT') || speechSynthesis.getVoices().find(x=>x.lang && x.lang.startsWith('it'));
    if (v) u.voice = v;
    u.onend = u.onerror = ()=>btnVoce.setAttribute('aria-pressed','false');
    btnVoce.setAttribute('aria-pressed','true'); speechSynthesis.speak(u);
  };
  addEventListener('pagehide', ()=>speechSynthesis.cancel());
}

const conti = {};
const btnClasse = $('classe');
btnClasse.onclick = ()=>{
  const on = btnClasse.getAttribute('aria-pressed')!=='true';
  btnClasse.setAttribute('aria-pressed', String(on)); $('conta').hidden = !on; disegnaConta();
};
let contaDi = null;
/* Le righe si creano una volta per capitolo; i clic aggiornano solo i numeri,
   così il fuoco da tastiera resta sul pulsante premuto. */
function disegnaConta(){
  const c = CH[chapter], n = conti[c.key] || (conti[c.key] = c.opts.map(()=>0));
  const righe = $('conta-righe');
  if (contaDi !== c.key){
    contaDi = c.key; righe.replaceChildren();
    c.opts.forEach((o,k)=>{
      const L = LETTERE[k], r = document.createElement('div'); r.className = 'lb-conta-riga';
      r.innerHTML = `<span class="lb-conta-lettera" aria-hidden="true">${L}</span><button type="button" aria-label="Togli una mano alla risposta ${L}">−</button><output aria-label="Mani per la risposta ${L}">0</output><button type="button" aria-label="Aggiungi una mano alla risposta ${L}">+</button>`;
      const [meno, piu] = r.querySelectorAll('button');
      meno.onclick = ()=>{ n[k] = Math.max(0, n[k]-1); aggiornaConta(); };
      piu.onclick = ()=>{ n[k]++; aggiornaConta(); };
      righe.append(r);
    });
  }
  aggiornaConta();
}
function aggiornaConta(){
  const c = CH[chapter], n = conti[c.key];
  [...$('conta-righe').querySelectorAll('output')].forEach((o,k)=>{ o.textContent = n[k]; });
  const tot = n.reduce((a,b)=>a+b,0);
  $('conta-tot').textContent = tot ? 'Mani alzate: ' + n.map((x,k)=>`${LETTERE[k]} ${x}`).join(', ') + '.' : '';
}
$('conta-azzera').onclick = ()=>{ conti[CH[chapter].key].fill(0); aggiornaConta(); };

const CHIAVE = 'pcgenzano-libro3d-' + (DATI.variante || 'libro_3d');
function leggiVisti(){ try { return new Set(JSON.parse(localStorage.getItem(CHIAVE) || '[]')); } catch(_){ return new Set(); } }
let visti = leggiVisti();
function mostraAvanzamento(){
  const n = CH.filter(c=>visti.has(c.key)).length;
  $('progresso').textContent = n ? `Risposte che hai già scoperto: ${n} su ${CH.length}.` : '';
  $('fine').hidden = n < CH.length;
}
function segnaVisto(k){
  if (visti.has(k)) return; visti.add(k);
  try { localStorage.setItem(CHIAVE, JSON.stringify([...visti])); } catch(_){}
  mostraAvanzamento();
}
$('ricomincia').onclick = ()=>{ visti = new Set(); try { localStorage.removeItem(CHIAVE); } catch(_){} mostraAvanzamento(); };
$('stampa-attestato').onclick = ()=>{
  const nome = $('nome').value.trim();
  document.getElementById('lb-att-nome').textContent = nome || '______________________________';
  document.getElementById('lb-att-data').textContent = 'Genzano di Roma, ' + new Date().toLocaleDateString('it-IT', {day:'numeric', month:'long', year:'numeric'});
  const att = document.getElementById('lb-attestato'); if (att.parentNode !== document.body) document.body.append(att);
  html.classList.add('stampa-attestato-libro');
  const via = ()=>{ html.classList.remove('stampa-attestato-libro'); removeEventListener('afterprint', via); };
  addEventListener('afterprint', via);
  print();
  setTimeout(via, 60000); /* ripiego se il browser non segnala la fine della stampa */
};
mostraAvanzamento();

/* ---------- Selezione con puntatore ---------- */
const ray = new THREE.Raycaster(), ptr = new THREE.Vector2(); let down = null;
renderer.domElement.addEventListener('pointerdown', e=>{ down = [e.clientX, e.clientY]; $('hint').classList.add('off'); });
function hitAt(e){
  const r = renderer.domElement.getBoundingClientRect();
  ptr.set(((e.clientX-r.left)/r.width)*2-1, -((e.clientY-r.top)/r.height)*2+1);
  ray.setFromCamera(ptr, camera);
  const hits = ray.intersectObjects([flap, flapBack, ...(current ? [current.g] : [])], true);
  for (const h of hits){ let o = h.object; while (o && o.userData.pick===undefined) o = o.parent; if (o && o.visible !== false) return o.userData.pick; }
  return undefined;
}
renderer.domElement.addEventListener('pointerup', e=>{
  if (!down || Math.hypot(e.clientX-down[0], e.clientY-down[1]) > 6) return; down = null;
  const id = hitAt(e); if (id===undefined) return;
  if (id==='flap') toggleFlap();
  else if (typeof id==='number') choose(id);
  else current.onPick?.(id);
});
renderer.domElement.addEventListener('pointermove', e=>{ if (e.buttons) return; renderer.domElement.style.cursor = hitAt(e)!==undefined ? 'pointer' : 'grab'; });

/* ---------- Dimensioni e ciclo ---------- */
function resize(){
  const w = stage.clientWidth, h = stage.clientHeight; if (!w || !h) return;
  renderer.setSize(w,h,false); camera.aspect = w/h; camera.updateProjectionMatrix();
  const k = Math.pow(Math.max(1, 1.5/camera.aspect), .85);
  const dist = 3.05*k; camera.position.set(0, dist*.78, dist*.62); controls.maxDistance = dist*1.6; controls.minDistance = .9; controls.update();
}
new ResizeObserver(resize).observe(stage);

const clock = new THREE.Clock(); let animT = 0;
function loop(){
  const dt = Math.min(clock.getDelta(), .1);
  /* «Pausa animazioni» o movimento ridotto: i movimenti continui (fiamme, fumo, nube, vento, ventola) si fermano; restano solo le transizioni brevi dei comandi. RM() si rilegge a ogni fotogramma, quindi vale anche se la preferenza cambia a pagina aperta. */
  const still = RM(); if (!still) animT += dt;
  for (let k=tweens.length-1; k>=0; k--){ const tw = tweens[k]; tw.t += dt; const p = Math.min(1, tw.t/tw.dur); tw.fn(p); if (p>=1){ tweens.splice(k,1); tw.done?.(); } }
  current?.update(still ? 0 : dt, animT); muoviPolvere(still ? 0 : dt, animT); muoviScintille(dt, still);
  if (controls.enabled) controls.update(); renderer.render(scene, camera);
  requestAnimationFrame(loop);
}

/* ---------- Avvio ---------- */
(async()=>{
  try{ await Promise.race([Promise.all([document.fonts.load(F(700,40)), document.fonts.load(F(400,40)), document.fonts.load(F(600,40))]), new Promise(r=>setTimeout(r,2500))]); }catch(_){}
  const m = /^#capitolo-(\d{1,2})$/.exec(location.hash); chapter = m ? Math.min(CH.length, Math.max(1,+m[1]))-1 : 0;
  drawLeft(chapter); drawRight(chapter); mount(chapter); renderPanel(chapter);
  $('loading').remove(); resize(); ingresso(); loop();
  setTimeout(()=>$('hint').classList.add('off'), 9000);
})();
