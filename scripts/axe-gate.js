#!/usr/bin/env node
/*
 * Gate accessibilità WCAG 2.2 AA con axe-core (runner ufficiale Deque).
 *
 * Perché non pa11y-ci: pa11y col runner axe conta anche i risultati
 * "incomplete" (casi che axe NON sa calcolare: testo su gradiente, contenuto
 * di pseudo-elementi, elementi sovrapposti) come errori, gonfiando il conteggio
 * con falsi positivi sulle "isole brand" del sito (hero blu in gradiente, ecc.).
 *
 * Questo gate fallisce SOLO sulle `violations` confermate. Gli `incomplete`
 * vengono stampati come informazione per revisione manuale, ma NON bloccano.
 *
 * Uso: node scripts/axe-gate.js  (server su http://127.0.0.1:8080)
 * Exit code 1 se ci sono violazioni confermate, 0 altrimenti.
 */
const puppeteer = require('puppeteer');
const axeSource = require('axe-core').source;

const BASE = process.env.AXE_BASE || 'http://127.0.0.1:8080';
const PATHS = [
  '/', '/cosa-fare-adesso/', '/emergenza/', '/allerte-meteo/', '/numeri-utili/',
  '/contatti/', '/accessibilita/', '/piano-familiare/', '/rischi-prevenzione/',
  '/comunicazioni/', '/cruscotto/',
];
// elementi esclusi (widget di terzi / mappe / dialog non pertinenti al gate)
const EXCLUDE = [['.leaflet-container'], ['iframe'], ['dialog']];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });
  let totalViol = 0, totalInc = 0;
  const failures = [];
  for (const p of PATHS) {
    const url = BASE + p;
    const page = await browser.newPage();
    try {
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
      await sleep(1500); // lascia girare il JS (glossario, widget)
      await page.evaluate(axeSource);
      const res = await page.evaluate(async (exclude) => {
        return await axe.run(
          { exclude },
          { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } }
        );
      }, EXCLUDE);
      const v = res.violations.reduce((s, x) => s + x.nodes.length, 0);
      const i = res.incomplete.reduce((s, x) => s + x.nodes.length, 0);
      totalViol += v; totalInc += i;
      console.log(`${p}  →  violazioni=${v}  incomplete=${i} (info)`);
      for (const viol of res.violations) {
        console.log(`   ✗ [${viol.id}] ${viol.help} — ${viol.nodes.length} nodi`);
        failures.push(`${p} [${viol.id}] ${viol.help} (${viol.nodes.length})`);
      }
    } catch (e) {
      console.log(`${p}  →  ERRORE caricamento: ${e.message}`);
      failures.push(`${p} ERRORE: ${e.message}`);
      totalViol += 1;
    } finally {
      await page.close();
    }
  }
  await browser.close();
  console.log('\n──────────────────────────────────────────');
  console.log(`TOTALE violazioni confermate: ${totalViol}`);
  console.log(`TOTALE incomplete (revisione manuale, non bloccanti): ${totalInc}`);
  if (totalViol > 0) {
    console.log('\nGate FALLITO — violazioni da correggere:');
    for (const f of failures) console.log('  · ' + f);
    process.exit(1);
  }
  console.log('Gate SUPERATO — nessuna violazione WCAG confermata.');
  process.exit(0);
})();
