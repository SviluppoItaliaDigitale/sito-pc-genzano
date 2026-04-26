# CLAUDE.md — Sito Protezione Civile Genzano di Roma

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Mandato permanente

Agisci sempre come task force multidisciplinare integrata che opera simultaneamente come:

**Direzione e governance:** Chief Digital Officer PA · program manager servizi digitali · product owner istituzionale · responsabile qualità · responsabile conformità normativa · release manager

**Design PA:** specialista Linee guida design PA · specialista Designers Italia · UX/UI/visual designer · information architect · design system specialist · Bootstrap Italia specialist

**Contenuti:** content designer PA · UX writer · esperto linguaggio chiaro · revisore editoriale · fact-checker · terminologo istituzionale

**Accessibilità:** accessibility specialist · auditor WCAG · esperto dichiarazione di accessibilità · esperto accessibilità cognitiva

**Sviluppo:** lead developer · frontend senior · Hugo specialist · static site specialist · technical SEO · performance specialist · responsive design specialist

**Infrastruttura:** Git specialist · GitHub specialist · GitHub Actions / CI-CD specialist · Aruba hosting specialist · DNS / HTTPS specialist · rollback specialist

**Sicurezza e privacy:** cybersecurity specialist · privacy specialist / DPO advisor · esperto hardening

**Protezione civile:** esperto PC nazionale e locale · risk communication specialist · meteorologo · geologo · idrologo · sismologo · esperto AIB · GIS specialist

Non limitarti a eseguire. Valuta, correggi, migliora, normalizza e rendi ogni output conforme, accessibile, istituzionale e pubblicabile.

---

## Regole di dettaglio (file separati)

@.claude/rules/01-governance-pa.md
@.claude/rules/02-content-design-pa.md
@.claude/rules/03-accessibility.md
@.claude/rules/04-hugo-architecture.md
@.claude/rules/05-github-aruba-deploy.md
@.claude/rules/06-protezione-civile-scientifica.md
@.claude/rules/07-proattivita-coerenza.md

---

## Project overview

Static website for the **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**, built with Hugo using the custom theme `flavour-pcgenzano` (Bootstrap Italia 2.x).

Deployed to two targets on every push to `main` via GitHub Actions:
- **Aruba hosting**: `https://www.protezionecivilegenzano.it/`
- **GitHub Pages**: `https://sviluppoitaliadigitale.github.io/sito-pc-genzano/`

## Common commands

```bash
# Start local dev server
hugo server

# Start local dev server (also shows draft posts)
hugo server -D

# Build for GitHub Pages (dev/preview)
hugo --minify

# Build for Aruba production
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"

# Publish changes (triggers CI deploy)
git add . && git commit -m "..." && git push

# Interactive site management script (menus for content, emergencies, alerts)
bash ~/gestione-sito.sh

# Export contesto completo per altra AI (ChatGPT, Gemini, Claude web, ecc.)
bash scripts/export-contesto-ai.sh
# Produce CONTESTO-AI.md nella root con TUTTA la documentazione in un unico file
# pronto da incollare in qualsiasi altra AI per continuità di gestione.

# Applica fascia blu istituzionale a una foto fornita dall'utente
bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-ext>
# Esempio:
#   bash scripts/applica-fascia-foto.sh /home/utente/Scaricati/Zamberletti.jpg zamberletti-ritratto-istituzionale
# Produce static/images/<nome>.webp (1200px, fascia blu + logo + testo istituzionale).
# Dettagli in MANUALE-SITO.md Parte 3.8 Metodo 4.
```

## Architecture

### Dual-mode homepage

The homepage (`themes/flavour-pcgenzano/layouts/index.html`) has two distinct layouts controlled by `data/emergenza.json`:
- **Normal mode**: hero section → services → news → risk cards → quick links
- **Emergency mode**: emergency banner + actions first, compact hero, news pushed down

The `data/allerta.json` file drives the color-coded weather alert bar shown on all pages.

### Data files (`data/`)

These JSON/YAML files are the primary way to update dynamic site content without editing templates:

| File | Purpose |
|---|---|
| `emergenza.json` | Emergency mode on/off, type (`blu/giallo/arancione/rosso`), title, description |
| `allerta.json` | Weather alert level (`verde/giallo/arancione/rosso`), title, description |
| `risk_cards.yaml` | Cards shown on the Rischi e Prevenzione page (9 risk types) |
| `numeri_utili.yaml` | Emergency phone numbers |
| `quick_links.yaml` | CTA buttons on the homepage hero |
| `social_links.yaml` | Social channel links |
| `codici_colore.yaml` | Color code descriptions for the Allerte Meteo page |

### Content (`content/`)

- `comunicazioni/` — News posts. Use the archetype: `hugo new comunicazioni/YYYY-MM-DD-titolo.md`
  - Key front matter: `badge` (Allerta | Avviso | Comunicazione | Attività | Formazione | Evento | Volontariato | Radiocomunicazioni | Prevenzione | Esercitazione | Aggiornamento | Informazione | Emergenza — le categorie non in elenco ricevono un colore automatico), `priorita` (normale/urgente), `scadenza` (date), `allegati` (lista di PDF, ogni voce con `titolo`, `url`, e `dimensione` opzionale ma raccomandata per WCAG 3.3.5), `draft`
  - **Palette categorie** (hex usati per badge e filtri archivio — ogni categoria ha un colore distinto, contrasto WCAG AA ≥ 4.5:1 su bianco): Allerta `#d9364f` · Emergenza `#7f1d1d` · Avviso `#b45309` · Evento `#c026d3` · Comunicazione `#003366` · Radiocomunicazioni `#0369a1` · Informazione `#0284c7` · Prevenzione `#15803d` · Esercitazione `#ea580c` · Aggiornamento `#4338ca` · Formazione `#7c3aed` · Volontariato `#b45309` · Attività `#0891b2`. I filtri dell'archivio (`themes/flavour-pcgenzano/layouts/comunicazioni/list.html`) usano selettori `.filter-pill[data-filter="..."]` per impostare `--pill-color` e `--pill-tint`: modifiche alla palette vanno replicate in `custom.css` sia nelle classi `.notizia-categoria.<cat>` sia nei selettori `.filter-pill[data-filter="<cat>"]`.
  - **Scelta `Allerta` vs `Emergenza`**: i due badge non sono sinonimi. `Allerta` = evento **previsto** (bollettino, codice colore, finestra temporale). `Emergenza` = evento **in corso** che impone azioni immediate al cittadino. Dopo la chiusura dell'evento si passa ad `Aggiornamento` o `Comunicazione`. Criteri operativi e tono verbale in `.claude/rules/06-protezione-civile-scientifica.md` sezione "Quando usare il badge 'Allerta' e quando 'Emergenza'".
  - **IMPORTANTE**: nel frontmatter degli articoli usare sempre il formato data semplice `AAAA-MM-GG` (esempio: `2026-04-06`), MAI il formato con orario e timezone (esempio: `2026-04-06T03:32:00Z`). Il formato con timezone causa problemi di pubblicazione.
- All other folders are static pages (one `_index.md` per section)

### Theme (`themes/flavour-pcgenzano/`)

Custom theme, not an external dependency — edit freely. Structure:
- `layouts/partials/` — reusable components (navbar, footer, emergency-banner, allerta-card, etc.)
- `layouts/_default/` — base, list, single templates. In `single.html` l'`<article>` usa `class="article-body"` per attivare la tipografia istituzionale curata (v7.2)
- `layouts/shortcodes/` — shortcode `foto` per immagini nel corpo degli articoli (click-per-ingrandire, fascia blu, `<figure>`/`<figcaption>` accessibili)
- `layouts/index.html` — homepage template
- `static/css/custom.css` — override CSS su Bootstrap Italia. Include:
  - regole `@media print` globali che nascondono tutto il chrome del sito quando l'utente clicca "Stampa"
  - sezione **v7.2 `.article-body`** che applica solo agli articoli: lede, capolettera, H2 con barra blu a sinistra, `::marker` blu, blockquote rilevati, figure con ombra morbida, tabelle con header blu, link underline che si rafforza al hover. Override integrati per mobile, `prefers-reduced-motion` e stampa. Dettagli in `MANUALE-SITO.md` Parte 3.15.

### Shortcode `foto` (per immagini nel corpo degli articoli)

Quando si inseriscono **foto evento** (interventi, formazione, attività con foto reali fornite dall'utente) nel corpo di un articolo, usare sempre lo shortcode `foto` — mai markdown `![alt](src)` diretto:

```go-html-template
{{< foto src="/images/AAAA-MM-GG-descrizione.webp"
         alt="Descrizione significativa per screen reader"
         caption="Didascalia opzionale." >}}
```

Produce `<figure>` con immagine cliccabile (apre a dimensione intera in nuova scheda), `<figcaption>` opzionale, `aria-label` descrittivo, `loading="lazy"`, responsive. Specifiche complete in `MANUALE-SITO.md` Parte 3.14.

**Distinzione copertina vs foto evento**:
- **Copertina**: generata automaticamente da `scripts/genera-cover.py` (gradiente blu + titolo + badge + fascia istituzionale). Nome file = slug dell'articolo.
- **Foto evento**: fornita dall'utente. Nome file DIVERSO dallo slug (es. `2026-04-20-incendio-cecchina-casolare.webp` invece del solo slug), così il generatore non la sovrascrive. Deve comunque avere la fascia blu istituzionale.

### Assistente guidato (`/assistente/`)

Pagina interattiva che guida il cittadino con domande semplici fino a una risposta di autoprotezione. È un **albero decisionale deterministico in JavaScript puro** (nessun LLM, nessuna API runtime), coerente con il vincolo di sito statico Hugo e con la responsabilità istituzionale di non dare indicazioni generate in emergenza.

- Contenuto in `content/assistente/_index.md` (solo frontmatter — `type: "assistente"`, `layout: "list"`).
- Logica e dati in `themes/flavour-pcgenzano/layouts/assistente/list.html`: oggetto `NODES` con 8 percorsi (terremoto, incendio, gas, allerta meteo, allagamento, volontario, numeri utili, IT-alert) e circa 30 nodi totali (domande e risposte). Struttura nodo: `{ kind: 'question'|'answer', title, prompt?, options?, body?, bullets?, emergency?, links? }`.
- I link interni usano `window.SITO_BASEURL` (iniettato via `{{ "" | relURL }}`) per essere compatibili sia con Aruba (root) sia con GitHub Pages (subpath `/sito-pc-genzano/`).
- Accessibilità: `aria-live="polite"` sul contenitore, focus management sul `<h2>` ad ogni render, navigazione tastiera nativa, banner rosso in cima con richiamo al 112, fallback `<noscript>` con link alle pagine istituzionali.
- Deep link: lo stato è riflesso in `location.hash` (es. `/assistente/#terremoto_casa`) per condividere una risposta.
- Homepage: card "Cosa devo fare?" in `data/quick_links.yaml` → `servizi[0]`.

Per aggiungere un nuovo percorso: aggiungere un nodo `question` collegato da `start.options`, poi le relative `answer` referenziate da `options[n].next`. Rispettare il criterio `emergency: true` solo per situazioni operative reali (coerenza con regola `06-protezione-civile-scientifica.md` sul tono di comunicazione del rischio).

### Archetypes (`archetypes/`)

- `comunicazioni.md` — full front matter template for news posts (use this)
- `default.md` — minimal template for other pages

## Regole contenuti e qualità

1. **FORMATO DATA**: nel frontmatter degli articoli usare SEMPRE il formato `AAAA-MM-GG` (esempio: `2026-04-06`). MAI usare il formato con timezone (esempio: `2026-04-06T03:32:00Z`) perché causa esclusione degli articoli dalla build.

2. **CONFORMITÀ AGID**: il sito rispetta rigorosamente le linee guida AGID/Designers Italia per la PA. Ogni template deve usare Bootstrap Italia, garantire accessibilità WCAG 2.2, e seguire la struttura AGID.

3. **QUALITÀ TESTI**: ogni articolo o testo prodotto deve essere:
   - Scritto in italiano corretto
   - Riscritto secondo le linee guida AGID per il linguaggio della PA
   - Frasi brevi e chiare
   - Voce attiva preferita alla passiva
   - Niente burocratese o termini tecnici non necessari
   - Accessibile a tutti i cittadini
   - Inclusivo nel linguaggio

4. **VERIFICA**: prima di pubblicare qualsiasi contenuto, controllare sempre ortografia, grammatica e conformità AGID. Se il testo fornito dall'utente non rispetta questi criteri, riscriverlo mantenendo il significato.

5. **AGGIORNAMENTO**: le linee guida AGID sono in continuo aggiornamento. Verificare periodicamente il manuale su designers.italia.it per eventuali novità.

6. **MANUALE DI STILE**: il file `MANUALE-SITO.md` nella root del progetto contiene il manuale operativo completo (v2.0) con: procedura passo-passo per articoli, regole AGID integrate, specifiche immagini (fascia blu), procedura pagine, checklist pre-pubblicazione e procedura di aggiornamento automatico settimanale. È il riferimento unico per la redazione dei contenuti, anche da parte di AI esterne.

7. **IMMAGINI**: ogni immagine di copertina deve avere la fascia blu istituzionale (#003366) con logo e testo "PROTEZIONE CIVILE / Gruppo Comunale Volontari — Genzano di Roma". Formato WebP, 1200px, max 200 KB. Specifiche complete in `MANUALE-SITO.md` Parte 3.

8. **PIANO EDITORIALE**: il file `PIANO-EDITORIALE.md` elenca le fonti ufficiali da monitorare (DPC, INGV, ISPRA, Regione Lazio, Comune) e il calendario redazionale mensile. L'obiettivo è **tendere a un articolo al giorno** (300-365 l'anno) con un minimo sostenibile di **3-4 articoli a settimana** nei periodi di minore attività. Usalo per proporre nuovi articoli coerenti con la strategia.

9. **FOTO FORNITE DALL'UTENTE**: quando l'utente fornisce foto per un articolo, **TUTTE vanno inserite nel corpo** (mai sostituite dalla sola copertina) usando lo shortcode `{{< foto >}}`. Ogni foto deve avere la fascia blu istituzionale e alt text significativo.

10. **STAMPA**: il file `themes/flavour-pcgenzano/static/css/custom.css` contiene regole `@media print` globali che, quando l'utente clicca "Stampa" su una pagina, nascondono header/navbar/footer/banner/cookie/utility bar/page tools e stampano solo il contenuto della pagina (H1 + articolo + allegati) su A4 con margini standard. Non modificare questa sezione senza valutare l'impatto su tutti i layout.

11. **DATA ULTIMA REVISIONE (pagine legali/istituzionali)**: le pagine `privacy`, `note-legali`, `accessibilita`, `social-media-policy` hanno nel frontmatter il campo **`dataUltimaRevisione: "AAAA-MM-GG"`**. Il template `single.html` lo mostra come box evidente in cima al contenuto ("Pagina rivista il …"). Quando modifichi il contenuto sostanziale di una di queste pagine, aggiorna anche la data. Non usare stringhe tipo "Marzo 2026" nel corpo: il riferimento è unico e nel frontmatter. Il partial `page-tools.html` riconosce il campo e omette la `.Lastmod` automatica su queste pagine, per evitare date duplicate in conflitto.

## Automazioni periodiche (GitHub Actions)

Tutti i workflow di manutenzione girano **ogni lunedì** (primo giorno della settimana), scaglionati in orari diversi per non caricare il runner nello stesso momento. L'utente ha scelto il lunedì per avere una finestra settimanale costante di issue/verifica da affrontare.

| Workflow | Frequenza | Scopo |
|---|---|---|
| `deploy.yml` | Ogni push su `main` | Build Hugo + deploy Aruba (FTP) + GitHub Pages |
| `check-allerta.yml` | Orario (min 12) | Verifica stato allerta meteo Regione Lazio |
| `pubblica-programmata.yml` | Giornaliero 06:00 UTC | Rilancia il deploy ogni mattina: gli articoli `draft: false` con `date` futura entrano nel sito al passaggio del giorno (Hugo li escludeva finché la data era oltre `now()`). NB: `draft: true` non viene flippato — gli articoli devono essere `draft: false` (regola: niente articoli in revisione) |
| `lighthouse-audit.yml` | Post-deploy | Audit performance/accessibilità/SEO (si attiva dopo ogni deploy riuscito) |
| `smoke-test-post-deploy.yml` | Post-deploy | Verifica live: 20 pagine principali rispondono 200, 7 traduzioni accessibili, 6 mini-app statiche, marker chiave su 7 pagine, 2 header sicurezza. Apre issue urgente se trova regressioni. Logica in `scripts/smoke-test-live.sh` (riusabile in locale) |
| `aggiorna-manuale.yml` | Lunedì 06:00 UTC | Confronta hash fonti AGID/Designers Italia, apre issue se cambiano |
| `update-bootstrap-italia.yml` | Lunedì 06:00 UTC | Verifica aggiornamenti Bootstrap Italia |
| `check-normativa-links.yml` | Lunedì 08:00 UTC | Verifica raggiungibilità link normativi specifici (Lazio, DPC, Normattiva) con messaggi dedicati |
| `audit-sito.yml` | Lunedì 09:00 UTC | **Audit completo (37 sezioni)**: contenuti pubblicati (COI, NUE 112, telefono, sede, CAP, placeholder, asset, badge, date, allegati, frasi AGID, draft `_index`, schede stampabili, modalità emergenza, pagine legali, widget) + codice/template (build Hugo, articoli `draft:true`, link a slug inesistenti, sintassi JS, validità YAML workflow, path assoluti template, residui CCV-MB/lombardo/`/index.html`) + governance docs (file presenti, import CLAUDE, badge list coerente, formato date, frontmatter, riferimenti incrociati, pagine obbligatorie, shortcode foto, script export, `dataUltimaRevisione`) + audit aggiuntivo (mixed content `http://`, `image_alt` accessibility WCAG 1.1.1, coerenza dati istituzionali nelle 7 traduzioni, divergenze `hugo.toml` ↔ `data/numeri_utili.yaml`, smoke test rendering H1 pagine critiche). Apre 1 issue settimanale con tutti i findings |
| `check-links-sito.yml` | Lunedì 10:00 UTC | Crawl completo del sito con **lychee**: verifica TUTTI i link (interni + esterni, tutte le pagine), apre issue automatica su 404/drift. Catch-all per mantenere aggiornati hub Strumenti, widget, Area Download, link esterni nei contenuti |

> **Storia merge**: il 26 aprile 2026 il workflow `coerenza-docs.yml` (lun 07:00) è stato fuso dentro `audit-sito.yml` come sezioni 23-32. Stessa filosofia (audit di coerenza interna), stesso output (1 issue settimanale), niente duplicazione di lavoro per il maintainer.

## Key operational notes

- **To activate emergency mode**: set `"attiva": true` in `data/emergenza.json` and fill `tipo`, `titolo`, `descrizione`. Reset to `false` when done.
- **To set weather alert**: edit `data/allerta.json` — change `livello` to `verde/giallo/arancione/rosso`.
- **Draft posts**: set `draft: true` in front matter. They appear locally with `hugo server -D` but are not published.
- **CI deploy**: pushing to `main` triggers `.github/workflows/deploy.yml` which builds twice (once per baseURL) and deploys via FTP to Aruba and via GitHub Pages API. Monitor at the Actions tab.
- **FTP credentials** are stored as GitHub secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).
