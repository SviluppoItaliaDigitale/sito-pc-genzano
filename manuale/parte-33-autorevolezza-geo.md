# Parte 35 — Autorevolezza (E-E-A-T), GEO/AI-SEO e microstampa

Raccoglie gli strumenti aggiunti per due obiettivi: (1) farsi **trovare e citare** da Google e dalle AI; (2) rafforzare la **credibilità** del sito. Sintesi operativa.

## 35.1 Pagina "Metodo editoriale"

`content/metodo-editoriale/_index.md` (`/metodo-editoriale/`) dichiara fonti, processo di verifica, frequenza di aggiornamento, chi scrive/rivede, cosa NON facciamo (no allerte ufficiali → 112), correzioni. È un segnale **E-E-A-T** (affidabilità) per cittadini, enti e AI. Linkata nel footer (Hugo + `site-chrome.js`).

## 35.2 "Pagina rivista il …" sulle guide

Il campo frontmatter `dataUltimaRevisione: "AAAA-MM-GG"` mostra il box "Pagina rivista il …". Già attivo su pagine legali e landing; esteso alle 10 pagine `rischi-prevenzione/*` (box aggiunto a `rischi-prevenzione/single.html`). Aggiornare la data quando si revisiona il contenuto.

## 35.3 `llms.txt`

`static/llms.txt` (formato llmstxt.org) → servito a `/llms.txt`. Sintesi del sito + pagine chiave con URL di produzione, perché ChatGPT/Perplexity/Google AI citino il sito con la fonte giusta. Aggiornarlo quando nascono nuove pagine pilastro.

## 35.4 Schema FAQPage opt-in

Una pagina con FAQ in accordion `<details class="faq-item">` espone lo schema **FAQPage** aggiungendo `faq_schema: true` nel frontmatter. Il partial `structured-data.html` estrae domanda/risposta e genera il JSON-LD. È opt-in per non marcare come FAQ accordion usati per altri scopi (es. moduli corso). Attivo: `/allerte-meteo/`, `/area-volontari/`. Lo schema **HowTo** è già su tutte le 8 pagine rischio via `howto_prima/durante/dopo`.

## 35.5 Analytics GoatCounter (anonimo, senza cookie)

- Attivazione: parametro `goatcounter` in `hugo.toml` (es. `goatcounter = "apicuollo"`). Vuoto = disattivo. Lo script viene iniettato da `baseof.html` solo se valorizzato.
- Privacy: cookieless, nessun dato personale → nessun banner aggiuntivo. Disclosure nella pagina Privacy § "Statistiche di visita anonime".
- Dashboard: `https://<codice>.goatcounter.com`. KPI utili: pagine più viste, provenienza, quota di traffico da fuori Genzano.
- Le pagine statiche dei giochi (`static/...` via `site-chrome.js`) non sono ancora incluse: da aggiungere se serve.

## 35.6 IndexNow (indicizzazione rapida)

- Chiave pubblica: `static/<KEY>.txt` (servita a `/<KEY>.txt`).
- Script: `scripts/indexnow-ping.py` — deduce le URL degli articoli dall'ultimo commit (esclude `-facile`), aggiunge home + archivio, POST a `api.indexnow.org`. Ping non bloccante.
- Workflow: `.github/workflows/indexnow.yml` — su push a `content/comunicazioni/**.md` attende il deploy (`sleep 180`) e invia il ping. Le notizie arrivano a Bing/Yandex in minuti.

## 35.7 Verifica proprietà (Search Console / Bing)

I file di verifica stanno nel repo per sopravvivere ai deploy: `static/google<...>.html` (Google Search Console) e `static/BingSiteAuth.xml` (Bing Webmaster). Serviti alla radice del sito.

## 35.8 Microtext / microstampa

`scripts/genera-microtext.py` (Python + Pillow): da lontano una parola o un'immagine normale, da vicino le linee sono **micro-testo personalizzato** (filigrana di sicurezza anti-falsificazione). Tre modalità:

```bash
python3 scripts/genera-microtext.py text  --macro "PROTEZIONE|CIVILE" --out static/images/microtext/banner.png
python3 scripts/genera-microtext.py image --in <foto>      --out <out.png>
python3 scripts/genera-microtext.py watermark --in <cover> --out <out.png> --opacity 0.18 --angle 30
```

Parametri utili: `--phrase` (default univoco col dominio), `--macro` (usa `|` per andare a capo), `--color`, `--microsize`, `--opacity`, `--angle`. Vettoriale per gli attestati: la microstampa resta nitida in stampa.

**Integrazione negli attestati** (filigrana già attiva): `static/giochi/assets/js/attestato.js` (SVG, copre anche `attestato-inclusivo.js`) e `static/js/quiz-preparazione.js` (canvas, attestato A4 + badge). Frase personalizzabile via `AttestatoPC.setMicroPhrase()`.

## 35.9 Cosa resta al di fuori del repo

Registrazione e invio sitemap su Google Search Console e Bing Webmaster Tools; costruzione di backlink/citazioni da fonti autorevoli. Non sono attività di codice.
