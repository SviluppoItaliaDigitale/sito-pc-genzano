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

const ROOT = document.getElementById('lb');
const DATI = JSON.parse(document.getElementById('lb-dati').textContent);
const BASE = DATI.base || '/';
const html = document.documentElement;
const mqRM = matchMedia('(prefers-reduced-motion: reduce)');
const RM = () => mqRM.matches || html.classList.contains('a11y-pause-anim') || html.classList.contains('a11y-pause-animations');

const CH = DATI.capitoli.map(c => ({
  key:c.chiave, kicker:c.occhiello, title:c.titolo, intro:c.intro, q:c.domanda,
  opts:c.opzioni.map(o => ({t:o.testo, ok:!!o.giusta, why:o.perche || ''})),
  answer:c.risposta, short:c.breve, src:{t:c.fonte.titolo, u:c.fonte.url}
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
catch (err) { $('loading').textContent = 'Il tuo browser non riesce a mostrare il libro in 3D. Trovi tutti i capitoli nella versione testuale qui sotto.'; throw err; }
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

scene.add(new THREE.HemisphereLight(0xffffff, 0x9aa8bb, 1.6));
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
    x.fillStyle = '#14223a'; x.font = F(700,20); x.fillText('ABC'[k], 91, y-3);
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
  tween(.7, p=>{ flapPivot.rotation.x = a + (b-a)*ease(p); });
}

/* foglio che gira quando cambi capitolo */
const sheetPivot = new THREE.Group(); sheetPivot.position.set(0, PY+.003, 0); book.add(sheetPivot);
const sheet = new THREE.Mesh(new THREE.PlaneGeometry(PW,PD), new THREE.MeshStandardMaterial({color:0xfbfaf5, roughness:1, side:THREE.DoubleSide}));
sheet.rotation.x = -Math.PI/2; sheet.position.x = .52; sheet.castShadow = true; sheet.visible = false; sheetPivot.add(sheet);

/* ---------- Le scene della pagina di destra ---------- */
const anchor = new THREE.Group(); anchor.position.set(.545, PY, -.04); book.add(anchor);
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
    tools:[ {label:'Fai tremare la stanza', fn(){ shake = RM() ? 1.2 : 3; say('La stanza trema per qualche secondo: guarda che cosa si muove e che cosa cade.');
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
    const c = COLORI[k]; say(`${c.n}: ${c.t}. ${c.s} Cosa fare: ${c.f}`); }
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
 }
};

let current = null;
function mount(i){
  if (current){ anchor.remove(current.g); current.g.traverse(o=>{ o.geometry?.dispose(); if (o.material){ o.material.map?.dispose(); o.material.dispose(); } }); }
  current = BUILD[CH[i].key](); anchor.add(current.g);
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
    b.setAttribute('aria-pressed','false'); b.innerHTML = `<b aria-hidden="true">${'ABC'[k]}</b><span></span>`; b.querySelector('span').textContent = o.t;
    b.onclick = ()=>choose(k); opts.append(b); });
  $('answer').hidden = true; $('flapBtn').textContent = 'Alza il lembo e scopri la risposta';
  $('src').innerHTML = ''; const a = document.createElement('a'); a.href = BASE + c.src.u.replace(/^\//,''); a.target = '_blank'; a.rel = 'noopener';
  a.textContent = c.src.t; $('src').append('Per saperne di più: ', a, ' (sito del Gruppo, si apre in una nuova scheda).');
  say('');
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
}
function toggleFlap(){
  revealed = !revealed; setFlap(revealed);
  $('flapBtn').textContent = revealed ? 'Abbassa il lembo' : 'Alza il lembo e scopri la risposta';
  if (revealed) showAnswer(); else { $('answer').hidden = true; [...$('opts').children].forEach(b=>b.classList.remove('right')); }
}
$('flapBtn').onclick = toggleFlap;
$('prev').onclick = ()=>goTo(chapter-1);
$('next').onclick = ()=>goTo(chapter+1);
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
      const s = p<.5 ? 1-p*2 : (p-.5)*2;
      current.g.scale.setScalar(Math.max(.001, s)); },
    ()=>{ sheet.visible = false; busy = false; current.g.scale.setScalar(1); });
}

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

const clock = new THREE.Clock();
function loop(){
  const dt = Math.min(clock.getDelta(), .1), t = clock.elapsedTime;
  for (let k=tweens.length-1; k>=0; k--){ const tw = tweens[k]; tw.t += dt; const p = Math.min(1, tw.t/tw.dur); tw.fn(p); if (p>=1){ tweens.splice(k,1); tw.done?.(); } }
  current?.update(dt,t); controls.update(); renderer.render(scene, camera);
  requestAnimationFrame(loop);
}

/* ---------- Avvio ---------- */
(async()=>{
  try{ await Promise.race([Promise.all([document.fonts.load(F(700,40)), document.fonts.load(F(400,40)), document.fonts.load(F(600,40))]), new Promise(r=>setTimeout(r,2500))]); }catch(_){}
  const m = /^#capitolo-(\d)$/.exec(location.hash); chapter = m ? Math.min(CH.length, Math.max(1,+m[1]))-1 : 0;
  drawLeft(chapter); drawRight(chapter); mount(chapter); renderPanel(chapter);
  $('loading').remove(); resize(); loop();
  setTimeout(()=>$('hint').classList.add('off'), 9000);
})();
