// Prova di nome e cognome sugli oggetti della stampa 3D: per ogni oggetto con la zona del nome
// (anteprima.nome in data/stampa_3d.yaml) crea, con lo stesso codice del sito, il file di ALFA 100
// con un nome lungo e lo scrive in una cartella; poi scripts/genera-stampa-3d.py --prova-nome
// controlla che ogni file sia un pezzo solo, chiuso, appoggiato sul piano e senza supporti.
// Uso: node scripts/prova-stampa3d-nome.mjs CARTELLA [testo]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const V = path.join(ROOT, 'themes/flavour-pcgenzano/static/vendor/stampa3d');
const { default: Module } = await import(pathToFileURL(path.join(V, 'manifold.js')).href);
const opentype = await import(pathToFileURL(path.join(V, 'opentype.min.mjs')).href);
const core = await import(pathToFileURL(path.join(ROOT, 'themes/flavour-pcgenzano/static/js/stampa3d-nome-core.js')).href);

const uscita = process.argv[2];
const testo = process.argv[3] || 'Maria Teresa Lucarelli';
if (!uscita) { console.error('Uso: node scripts/prova-stampa3d-nome.mjs CARTELLA [testo]'); process.exit(2); }
fs.mkdirSync(uscita, { recursive: true });

// data/stampa_3d.yaml letto da Python (nessuna libreria YAML in Node nel repository)
import { execFileSync } from 'node:child_process';
const dati = JSON.parse(execFileSync('python3', ['-c',
  'import json,yaml,sys; print(json.dumps(yaml.safe_load(open(sys.argv[1]))))', path.join(ROOT, 'data/stampa_3d.yaml')]).toString());

const M = await Module();
M.setup();
const ttf = fs.readFileSync(path.join(V, 'LiberationSans-Bold.ttf'));
const font = opentype.parse(ttf.buffer.slice(ttf.byteOffset, ttf.byteOffset + ttf.byteLength));
let errori = 0;
for (const o of dati.oggetti) {
  const a = o.anteprima || {};
  if (!a.nome) continue;
  const stl = fs.readFileSync(path.join(ROOT, 'static/stampa-3d', o.id, 'alfa-100.stl'));
  const buf = () => stl.buffer.slice(stl.byteOffset, stl.byteOffset + stl.byteLength);
  try {
    let r, usato = testo;
    try { r = core.conNome(buf(), a, testo, font, M); }
    catch (e) {
      // nelle zone più corte il sito chiede l'iniziale del nome: si prova come farebbe il volontario
      if (!/non entrano/.test(e.message)) throw e;
      usato = testo.replace(/^(\S)\S*\s+(?:(\S)\S*\s+)?/, (m, a1, a2) => a2 ? `${a1}. ${a2}. ` : `${a1}. `);
      r = core.conNome(buf(), a, usato, font, M);
    }
    fs.writeFileSync(path.join(uscita, `${o.id}.stl`), Buffer.from(r.stl));
    console.log(`${o.id}: ${r.lato}, misura ${r.size}${usato !== testo ? `, con l'iniziale («${usato}»)` : ''}`);
  } catch (e) {
    errori++;
    console.log(`${o.id}: ERRORE ${e.message}`);
  }
}
process.exit(errori ? 1 : 0);
