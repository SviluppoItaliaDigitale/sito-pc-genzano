#!/usr/bin/env node
/**
 * smoke-test-playwright.js — smoke test interattivi post-deploy.
 *
 * Esegue con Chromium headless una manciata di scenari che HTTP-only
 * non può catturare: clic veri sul FAB accessibilità, apertura modal
 * ricerca Pagefind (Ctrl+K), link tel:112 su /numeri-utili/, presenza
 * dei bottoni TTS/reading-time sull'articolo.
 *
 * Uso:
 *   node scripts/smoke-test-playwright.js [URL_BASE]
 *
 * URL_BASE default: https://www.protezionecivilegenzano.it
 * Variante test in locale: http://localhost:1313
 *
 * Exit code 0 se tutti i test passano, !=0 altrimenti.
 *
 * Setup una-tantum:
 *   npm install --no-save playwright@1.60.0
 *   npx playwright install chromium
 */

const { chromium } = require('playwright');

const BASE = process.argv[2] || 'https://www.protezionecivilegenzano.it';

// Dismiss del cookie banner (compare su prima visita). Riusato dai test che
// devono fare clic veri sotto al banner.
async function dismissCookieBanner(page) {
  const accept = page.locator('#cookie-banner button:has-text("OK")').first();
  if (await accept.isVisible({ timeout: 1500 }).catch(() => false)) {
    await accept.click();
    await page.waitForTimeout(300);
  }
}

const TESTS = [
  {
    nome: 'Home — page load + H1 visibile',
    path: '/',
    check: async (page) => {
      const title = await page.title();
      if (!/Protezione Civile.*Genzano/i.test(title)) {
        throw new Error(`title inatteso: "${title}"`);
      }
      const h1 = await page.locator('h1').first().textContent();
      if (!h1 || h1.length < 5) throw new Error('H1 mancante o vuoto');
      return { title, h1: h1.trim().slice(0, 80) };
    },
  },
  {
    nome: 'Home — FAB accessibilità apre/chiude dialog',
    path: '/',
    check: async (page) => {
      await dismissCookieBanner(page);
      const fab = page.locator('#a11yToolbarOpen');
      await fab.waitFor({ state: 'visible', timeout: 5000 });
      await fab.click();
      const dialog = page.locator('#a11yDialog');
      await dialog.waitFor({ state: 'visible', timeout: 3000 });
      await page.locator('#a11yDialogClose').click();
      await dialog.waitFor({ state: 'hidden', timeout: 3000 });
      return { ok: true };
    },
  },
  {
    nome: 'Home — ricerca Pagefind si apre con Ctrl+K',
    path: '/',
    check: async (page) => {
      await dismissCookieBanner(page);
      await page.keyboard.press('Control+k');
      const modal = page.locator('#pcg-ricerca-dialog');
      const visible = await modal.isVisible({ timeout: 4000 }).catch(() => false);
      if (!visible) throw new Error('Modal #pcg-ricerca-dialog non aperto entro 4s');
      await page.keyboard.press('Escape');
      return { ok: true };
    },
  },
  {
    nome: 'Articolo recente — strumenti lettura (TTS + reading-time)',
    path: '/comunicazioni/',
    check: async (page) => {
      // Prima card articolo del'archivio (esclude la card della pagina stessa)
      const firstArticleLink = page.locator(
        'main a[href*="/comunicazioni/2026-"], main a[href*="/comunicazioni/2025-"]'
      ).first();
      const href = await firstArticleLink.getAttribute('href', { timeout: 8000 });
      if (!href) throw new Error('Nessun link articolo trovato');
      const targetUrl = href.startsWith('http') ? href : BASE + href;
      await page.goto(targetUrl, { waitUntil: 'domcontentloaded' });
      await dismissCookieBanner(page);
      const tts = await page.locator('.tts-wrapper button, button:has-text("Leggi ad alta voce")').first()
        .isVisible({ timeout: 5000 }).catch(() => false);
      const readingTime = await page.locator('.reading-time:has-text("min")').first()
        .isVisible({ timeout: 2000 }).catch(() => false);
      if (!tts) throw new Error('Bottone TTS non trovato');
      if (!readingTime) throw new Error('Pill .reading-time con "min" non trovata');
      return { article: href, tts, readingTime };
    },
  },
  {
    nome: '/numeri-utili/ — almeno 5 link tel: visibili, encoding corretto',
    path: '/numeri-utili/',
    check: async (page) => {
      const tels = await page.locator('a[href^="tel:"]:visible').all();
      if (tels.length < 5) {
        throw new Error(`Solo ${tels.length} link tel: visibili (atteso >=5)`);
      }
      // Verifica che almeno 1 sia un numero di emergenza (3 cifre) o COC (069...)
      let coc = null, has112 = false;
      for (const t of tels) {
        const href = await t.getAttribute('href');
        if (href && /tel:\+39069362600/.test(href)) coc = href; // COC Genzano
        if (href === 'tel:112') has112 = true;
      }
      if (!coc) throw new Error('COC Genzano tel:+39069362600 non trovato');
      // Verifica anti-pattern: niente "tel:+39 069..." con spazio encoded
      const allHrefs = await Promise.all(tels.map(t => t.getAttribute('href')));
      const encodingBug = allHrefs.find(h => h && /tel:\+39%20|tel:\+39 /.test(h));
      if (encodingBug) throw new Error(`tel: encoding bug: ${encodingBug}`);
      return { count: tels.length, coc, has112 };
    },
  },
  {
    nome: 'Footer — link feed RSS presente',
    path: '/',
    check: async (page) => {
      await dismissCookieBanner(page);
      const rss = page.locator('footer a[href*="/feed-rss/"], footer a[href*="/index.xml"]').first();
      const visible = await rss.isVisible({ timeout: 4000 }).catch(() => false);
      if (!visible) throw new Error('Link RSS nel footer non trovato');
      return { ok: true };
    },
  },
];

(async () => {
  console.log(`\n🎭 Playwright smoke test — base: ${BASE}\n`);
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (PC-Genzano smoke-test) Playwright',
    viewport: { width: 1280, height: 800 },
  });
  const page = await ctx.newPage();

  let passed = 0;
  let failed = 0;
  const results = [];

  for (const t of TESTS) {
    process.stdout.write(`  · ${t.nome} ... `);
    const t0 = Date.now();
    try {
      await page.goto(BASE + t.path, { waitUntil: 'domcontentloaded', timeout: 15000 });
      const detail = await t.check(page);
      const dt = ((Date.now() - t0) / 1000).toFixed(1);
      console.log(`✅ (${dt}s) ${JSON.stringify(detail).slice(0, 100)}`);
      results.push({ nome: t.nome, status: 'pass', dt: +dt, detail });
      passed++;
    } catch (e) {
      const dt = ((Date.now() - t0) / 1000).toFixed(1);
      console.log(`❌ (${dt}s) ${e.message.split('\n')[0]}`);
      results.push({ nome: t.nome, status: 'fail', dt: +dt, error: e.message.split('\n')[0] });
      failed++;
    }
  }

  await browser.close();
  console.log(`\n📊 Risultato: ${passed}/${TESTS.length} pass, ${failed} fail\n`);
  if (process.env.SMOKE_OUT) {
    require('fs').writeFileSync(process.env.SMOKE_OUT, JSON.stringify({
      base: BASE,
      timestamp: new Date().toISOString(),
      passed,
      failed,
      results,
    }, null, 2));
  }
  process.exit(failed === 0 ? 0 : 1);
})();
