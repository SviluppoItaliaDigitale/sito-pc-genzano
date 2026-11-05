#!/usr/bin/env node
// Controlla che ogni JavaScript servito dal sito sia leggibile dai browser vecchi delle lavagne
// interattive (LIM) e dei PC di scuola: sintassi fino a ECMAScript 2018 (Chrome 64).
//
// Nasce l'01/11/2026 dalle segnalazioni delle scuole: su Chromium 69 Bootstrap Italia non si
// avviava (menu, finestre, accordion fermi) e due giochi dell'infanzia non partivano.
// Uso: node scripts/check-sintassi-js.cjs [--public CARTELLA]
//   senza --public: file .js e script inline delle pagine autonome in static/ e nel tema;
//   con --public: anche gli script inline di tutte le pagine costruite da Hugo.
// Richiede acorn (npm install --no-save acorn@8): validate-pr.yml lo installa.
const fs = require('fs'), path = require('path');
let acorn;
try { acorn = require('acorn'); } catch (e) {
  console.error('acorn mancante: npm install --no-save acorn@8 (oppure NODE_PATH verso una cartella che lo contiene)');
  process.exit(2);
}
const ROOT = path.resolve(__dirname, '..');
const VERSIONE = 2018;
// Eccezioni dichiarate: solo componenti che hanno già un'alternativa senza JavaScript moderno.
const ECCEZIONI = [
  // Libro che si esplora: la scena 3D richiede WebGL 2 e moduli ES2022 (three.js r160);
  // la versione testuale e le schede A4 dello stesso libro funzionano ovunque.
  /\/vendor\/three\//, /\/js\/libro-3d\.js$/,
  // Sala situazioni: strumento per la sala operativa, non per le scuole.
  /\/monitor\/index\.html$/,
  // Indice di ricerca generato da Pagefind: artefatto di build, non usato dalle pagine di scuola.
  /\/pagefind\//,
];
const SALTA_DIR = /^(node_modules|\.git|pagefind)$/;
const args = process.argv.slice(2);
const pub = args.includes('--public') ? args[args.indexOf('--public') + 1] : null;

function prova(code, mod) {
  try { acorn.parse(code, { ecmaVersion: VERSIONE, sourceType: mod ? 'module' : 'script', allowHashBang: true }); return null; }
  catch (e) { return e; }
}
function cammina(dir, fn) {
  if (!fs.existsSync(dir)) return;
  for (const f of fs.readdirSync(dir)) {
    if (SALTA_DIR.test(f)) continue;
    const p = path.join(dir, f), st = fs.statSync(p);
    if (st.isDirectory()) cammina(p, fn); else fn(p);
  }
}
const errori = [];
function controllaJs(p) {
  if (ECCEZIONI.some(r => r.test(p))) return;
  // Bootstrap Italia: oltre ai file usati, il pacchetto contiene moduli ES (esm, plugins) che il sito non carica
  if (/vendor\/bootstrap-italia\//.test(p) && !/bootstrap-italia\.bundle\.min\.js$/.test(p)) return;
  if (/\.min\.js\.map$|\.map$/.test(p)) return;
  const c = fs.readFileSync(p, 'utf8');
  const mod = /^\s*(import|export)\s/m.test(c);
  const e = prova(c, mod);
  if (e) errori.push(`${path.relative(ROOT, p)}:${e.loc ? e.loc.line + ':' + e.loc.column : ''} ${e.message} «${c.slice(Math.max(0, e.pos - 40), e.pos + 20).replace(/\s+/g, ' ')}»`);
}
function controllaHtml(p, base) {
  if (ECCEZIONI.some(r => r.test(p))) return;
  const h = fs.readFileSync(p, 'utf8');
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi; let m;
  while ((m = re.exec(h))) {
    const attr = m[1];
    if (/\bsrc\s*=/.test(attr) || /type\s*=\s*["']?(application\/(ld\+)?json|speculationrules|text\/template|text\/x-)/i.test(attr)) continue;
    if (!m[2].trim() || /\{\{/.test(m[2])) continue; // template Hugo non ancora costruito
    const e = prova(m[2], /type\s*=\s*["']?module/i.test(attr));
    if (e) {
      const riga = h.slice(0, m.index).split('\n').length + (e.loc ? e.loc.line - 1 : 0);
      errori.push(`${path.relative(base, p)}:${riga} (script nella pagina) ${e.message} «${m[2].slice(Math.max(0, e.pos - 40), e.pos + 20).replace(/\s+/g, ' ')}»`);
    }
  }
}
cammina(path.join(ROOT, 'static'), p => { if (p.endsWith('.js')) controllaJs(p); else if (p.endsWith('.html')) controllaHtml(p, ROOT); });
cammina(path.join(ROOT, 'themes/flavour-pcgenzano/static'), p => { if (p.endsWith('.js')) controllaJs(p); });
if (pub) cammina(path.resolve(pub), p => { if (p.endsWith('.html')) controllaHtml(p, path.resolve(pub)); });

const bi = fs.readFileSync(path.join(ROOT, 'static/vendor/bootstrap-italia/js/bootstrap-italia.bundle.min.js'), 'utf8');
if (!bi.slice(0, 200).includes('compatibile-lim')) errori.push('Bootstrap Italia non è la versione compatibile: esegui bash scripts/js-compatibile-lim.sh');

if (errori.length) {
  console.log(`❌ ${errori.length} script non leggibili dai browser delle LIM (sintassi oltre ECMAScript ${VERSIONE}, Chrome 64):`);
  errori.slice(0, 60).forEach(e => console.log('  - ' + e));
  console.log('Riscrivi la sintassi recente (?., ??, campi di classe, catch senza parametro…) in forma classica.');
  process.exit(1);
}
console.log(`✅ Tutti gli script sono leggibili dai browser delle LIM (ECMAScript ${VERSIONE}, Chrome 64)${pub ? ', comprese le pagine costruite' : ''}.`);
