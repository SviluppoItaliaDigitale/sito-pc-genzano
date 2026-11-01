#!/usr/bin/env node
// Apre le pagine per le scuole con un Chromium del 2018 (versione 69, quella delle lavagne
// interattive con Android 9 e dei PC di scuola non aggiornati) e blocca gli errori che lì
// fermano il sito: script che non si avviano, Bootstrap Italia assente, menu che non si aprono.
//
// Nasce l'01/11/2026 dalle segnalazioni delle scuole: su quel browser Bootstrap Italia 2.x non
// partiva (101 pagine su 165) e due giochi dell'infanzia non si avviavano. Gira ogni settimana
// in controllo-lim.yml; il controllo veloce sulle PR è scripts/check-sintassi-js.cjs.
//
// Uso: node scripts/check-lim-browser-vecchio.cjs --chrome PERCORSO/chrome --public public
// Richiede il pacchetto ws (npm install --no-save ws@8). Esce 1 se trova problemi, 2 se manca qualcosa.
'use strict';
const { spawn } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
let WebSocket;
try { WebSocket = require('ws'); } catch (e) { console.error('ws mancante: npm install --no-save ws@8'); process.exit(2); }

const args = process.argv.slice(2);
const opt = n => (args.includes(n) ? args[args.indexOf(n) + 1] : null);
const CHROME = opt('--chrome'), PUBLIC = path.resolve(opt('--public') || 'public');
if (!CHROME || !fs.existsSync(CHROME)) { console.error('Indica il Chromium vecchio con --chrome'); process.exit(2); }
if (!fs.existsSync(path.join(PUBLIC, 'index.html'))) { console.error('Build mancante in ' + PUBLIC); process.exit(2); }

// Errori attesi: il libro 3D richiede WebGL 2 e moduli recenti, e su questi browser
// mostra da solo la versione testuale (rete di sicurezza nello shortcode libro-3d).
const ATTESI = [/\/js\/libro-3d\.js/, /vendor\/three\//];
const PAGINE_HUGO = ['/', '/formazione/', '/formazione/crea-la-mia-lezione/', '/formazione/percorsi-didattici/',
  '/formazione/kit-scuola-primaria/', '/formazione/kit-calamita/', '/formazione/esperimenti/',
  '/formazione/libro-che-si-esplora/', '/giochi/', '/laboratorio-meteo/', '/quiz-preparazione/',
  '/tabelle-comunicazione/', '/assistente/', '/cosa-fare-adesso/', '/numeri-utili/'];

function trova(dir, filtro, out) {
  if (!fs.existsSync(dir)) return out;
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    if (fs.statSync(p).isDirectory()) { if (f !== 'pacchetti') trova(p, filtro, out); }
    else if (filtro(p)) out.push('/' + path.relative(PUBLIC, p).split(path.sep).join('/').replace(/index\.html$/, ''));
  }
  return out;
}
const pagine = PAGINE_HUGO.slice();
trova(path.join(PUBLIC, 'giochi'), p => p.endsWith('index.html'), pagine);
for (const d of ['quizpc', 'formazionepc', 'scuole', 'formazione/storie-e-racconti'])
  trova(path.join(PUBLIC, d), p => p.endsWith('index.html'), pagine);
// un campione stabile di schede e kit (le loro pagine condividono gli stessi script)
const schede = trova(path.join(PUBLIC, 'formazione/schede-stampabili'), p => p.endsWith('index.html'), []);
pagine.push(...schede.filter((_, i) => i % 15 === 0));
const kit = [];
for (const d of fs.readdirSync(path.join(PUBLIC, 'formazione')).filter(d => d.startsWith('kit-calamita-')))
  trova(path.join(PUBLIC, 'formazione', d), p => p.endsWith('.html'), kit);
pagine.push(...kit.filter((_, i) => i % 15 === 0));

const TIPI = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.json': 'application/json',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon', '.mp3': 'audio/mpeg' };
const srv = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  let f = path.join(PUBLIC, p);
  if (!f.startsWith(PUBLIC)) { res.writeHead(403); return res.end(); }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TIPI[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

const sleep = ms => new Promise(r => setTimeout(r, ms));
const getJson = u => new Promise((r, j) => http.get(u, res => { let d = ''; res.on('data', c => d += c); res.on('end', () => { try { r(JSON.parse(d)); } catch (e) { j(e); } }); }).on('error', j));

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const base = 'http://127.0.0.1:' + srv.address().port;
  const porta = 9200 + Math.floor(Math.random() * 600);
  const ch = spawn(CHROME, ['--headless', '--no-sandbox', '--disable-gpu', '--remote-debugging-port=' + porta,
    '--window-size=1366,768', 'about:blank'], { stdio: 'ignore' });
  let elenco;
  for (let i = 0; i < 60 && !elenco; i++) { try { elenco = await getJson(`http://127.0.0.1:${porta}/json`); } catch (e) { await sleep(250); } }
  if (!elenco) { console.error('Il Chromium vecchio non si è avviato'); ch.kill(); process.exit(2); }
  const ws = new WebSocket(elenco.find(x => x.type === 'page').webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));
  let id = 0; const attese = {}; let cur = null;
  ws.on('message', m => {
    const d = JSON.parse(m);
    if (d.id && attese[d.id]) { attese[d.id](d.result || d); delete attese[d.id]; }
    if (d.method === 'Runtime.exceptionThrown' && cur) {
      const e = d.params.exceptionDetails;
      cur.push(((e.exception && e.exception.description) || e.text).split('\n')[0].slice(0, 150) + ' @' + (e.url || '').replace(base, ''));
    }
  });
  const invia = (method, params) => new Promise(r => { const i = ++id; attese[i] = r; ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
  await invia('Runtime.enable'); await invia('Page.enable');
  const SONDA = `(function(){
    var usaBI=!!document.querySelector('script[src*="bootstrap-italia.bundle"]');
    var dd=document.querySelector('.navbar .dropdown-toggle'), menu='';
    if(dd){dd.click();var m=dd.parentElement.querySelector('.dropdown-menu');menu=(m&&m.classList.contains('show'))?'ok':'fermo';dd.click();}
    return JSON.stringify({bi:usaBI?typeof window.bootstrap:'', menu:menu});})()`;
  const problemi = [];
  for (const u of pagine) {
    cur = [];
    await invia('Page.navigate', { url: base + u });
    await sleep(2500);
    const r = await invia('Runtime.evaluate', { expression: SONDA, returnByValue: true });
    let s = {}; try { s = JSON.parse(r.result.value); } catch (e) { }
    const errori = cur.filter(e => !ATTESI.some(a => a.test(e)));
    errori.forEach(e => problemi.push(`${u}: errore JavaScript: ${e}`));
    if (s.bi && s.bi !== 'object') problemi.push(`${u}: Bootstrap Italia non si avvia (menu, finestre e accordion fermi)`);
    if (s.menu === 'fermo') problemi.push(`${u}: il menu a tendina non si apre`);
    process.stdout.write('.');
  }
  process.stdout.write('\n');
  ws.close(); ch.kill(); srv.close();
  if (problemi.length) {
    console.log(`❌ ${problemi.length} problemi con il browser delle LIM non aggiornate (Chromium 69):`);
    problemi.forEach(p => console.log('  - ' + p));
    process.exit(1);
  }
  console.log(`✅ ${pagine.length} pagine funzionano anche con Chromium 69 (LIM e PC di scuola non aggiornati).`);
  process.exit(0);
})();
