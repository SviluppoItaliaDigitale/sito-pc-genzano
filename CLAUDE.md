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
@.claude/rules/08-claude-code-setup.md

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

# Scarica/aggiorna la libreria di pittogrammi (ISO 7010 + ARASAAC)
bash scripts/scarica-pittogrammi.sh           # solo i mancanti
bash scripts/scarica-pittogrammi.sh --force   # ri-scarica tutto
# Output: static/pittogrammi/iso7010/*.svg + static/pittogrammi/arasaac/*.png
# Attribuzioni obbligatorie su /attribuzioni-pittogrammi/ (linkata dal footer).

# Scarica foto per articoli da fonti libere (con fascia blu istituzionale)
bash scripts/foto-da-wikipedia.sh "Titolo Pagina Wikipedia" slug-articolo [lang]
bash scripts/foto-da-nasa.sh      "search query"            slug-articolo
bash scripts/foto-da-usgs.sh      shakemap <eventid>        slug-articolo
# Output: static/images/<slug>.webp (1200px, fascia blu, max ~200 KB)
# Da mobile/cloud: vedi workflow scarica-foto-automatica.yml + marker frontmatter.
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
- `layouts/shortcodes/` — shortcode disponibili: `foto` (immagini articolo con click-per-ingrandire), `pittogramma` (ISO 7010/ARASAAC), `cosa-non-fare` (box rosso divieti per pagine rischio), `chi-chiamare` (tabella accessibile "chi chiamare" + chiarimento attivazione Gruppo, in coda alle pagine /rischi-prevenzione/*), `pagina-emergenza-lite` (contenuto pagina /emergenza/ ultra-leggera)
- `layouts/_default/_markup/` — render hook Markdown: `render-link.html` (link interni vs statici vs esterni) e `render-table.html` (tabelle accessibili: aggiunge `<th scope="col">` automatico a TUTTE le tabelle Markdown del sito + wrapping `.table-responsive` Bootstrap Italia + supporto `<caption>` per le tabelle convertite in HTML diretto). Hook universale: nessun editing manuale per pagina.
- `layouts/partials/` — include `article-cover.html` (copertina articolo con didascalia image_credit), `leggi-ad-alta-voce.html` (TTS Web Speech API per pagine essenziali), `accessibility-toolbar.html` (FAB strumenti a11y), `structured-data.html` (JSON-LD Organization NGO + ContactPoint + Article + Event + FAQPage + WebSite + BreadcrumbList)
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

**Convenzione posizionamento foto multiple negli articoli storici** (introdotta aprile 2026):
- **1ª foto**: dopo il **1° H2** dell'articolo, dopo il primo paragrafo di contenuto.
- **2ª foto**: dopo il **2° H2**, per aprire una seconda dimensione narrativa (ricostruzione, contesto, conseguenze).
- **3ª foto e oltre**: una per ogni H2 di **evento storico specifico citato** (es. negli articoli che raccontano sequenze di terremoti — Irpinia 1980, L'Aquila 2009, Centro Italia 2016, Emilia-Romagna 2023).
- **Mai a casaccio**: ogni foto va legata tematicamente alla sezione che la precede.

Lo script `scripts/foto-da-wikipedia.sh` filtra automaticamente bandiere/stemmi comunali (pattern `*Bandiera.svg`, `Flag_of_*`, `*-Stemma.svg`, `*Coat_of_arms*`) — exit code `4`. Non aggiungono valore narrativo; provare un titolo più specifico (un monumento, una piazza, una veduta). Specifiche complete in `MANUALE-SITO.md` Parte 14.9.

### Shortcode `pittogramma` (per supporto comprensione)

Per migliorare l'accessibilità cognitiva dei contenuti (bambini, anziani, persone con disabilità cognitive, parlanti italiano L2) si usa lo shortcode `pittogramma`, che inserisce simboli ISO 7010 (sicurezza standard) o ARASAAC (CC BY-NC-SA, comprensione cognitiva).

```go-html-template
{{< pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto" >}}
```

Uso inline (dentro una frase):
```go-html-template
Chiama il {{< pittogramma src="/pittogrammi/arasaac/112.png" alt="numero 112" inline="true" >}} 112.
```

Parametri: `src` (obbligatorio), `alt` (obbligatorio), `caption` (opzionale solo block), `inline="true"` per inserimento inline, `size` (small/medium/large/xlarge, default medium).

Produce `<img>` con `role="img"`, `loading="lazy"`, oppure `<figure>` con caption opzionale. CSS scoped in `custom.css` (sezione **PITTOGRAMMI v1.0**) con dimensioni fisse, override mobile, mantenimento colori in stampa (essenziale per i segnali di sicurezza). Compatibile con il toolbar di accessibilità: i pittogrammi sono marcati funzionali e restano visibili anche con preferenza "Nascondi immagini" attiva (selettori `html.a11y-hide-images img.pittogramma` e `html.a11y-grayscale img.pittogramma`).

**Libreria disponibile** (172 simboli, 3.3 MB):
- `static/pittogrammi/iso7010/*.svg` — 46 segnali standard (evacuazione, antincendio, divieto, obbligo, avvertimento). Fonte: Wikimedia Commons (PD-shape/CC0).
- `static/pittogrammi/arasaac/*.png` — 126 simboli (eventi, azioni autoprotezione, oggetti kit, persone, luoghi, segnali, veicoli). Fonte: ARASAAC (CC BY-NC-SA, autore Sergio Palao).

**Re-download della libreria**: `bash scripts/scarica-pittogrammi.sh` (idempotente, scarica solo i mancanti; `--force` ri-scarica tutto).

**Catalogo pubblico**: `/pittogrammi/` mostra l'intera libreria con anteprima, codice e licenza.

**Attribuzioni obbligatorie**: pagina `/attribuzioni-pittogrammi/` linkata dal footer. Le opere derivate (schede stampabili che includono ARASAAC) ereditano CC BY-NC-SA 4.0.

### Assistente guidato (`/assistente/`)

Pagina interattiva che guida il cittadino con domande semplici fino a una risposta di autoprotezione. È un **albero decisionale deterministico in JavaScript puro** (nessun LLM, nessuna API runtime), coerente con il vincolo di sito statico Hugo e con la responsabilità istituzionale di non dare indicazioni generate in emergenza.

- Contenuto in `content/assistente/_index.md` (solo frontmatter — `type: "assistente"`, `layout: "list"`).
- Logica e dati in `themes/flavour-pcgenzano/layouts/assistente/list.html`: oggetto `NODES` con 8 percorsi (terremoto, incendio, gas, allerta meteo, allagamento, volontario, numeri utili, IT-alert) e circa 30 nodi totali (domande e risposte). Struttura nodo: `{ kind: 'question'|'answer', title, prompt?, options?, body?, bullets?, emergency?, links? }`.
- I link interni usano `window.SITO_BASEURL` (iniettato via `{{ "" | relURL }}`) per essere compatibili sia con Aruba (root) sia con GitHub Pages (subpath `/sito-pc-genzano/`).
- Accessibilità: `aria-live="polite"` sul contenitore, focus management sul `<h2>` ad ogni render, navigazione tastiera nativa, banner rosso in cima con richiamo al 112, fallback `<noscript>` con link alle pagine istituzionali.
- Deep link: lo stato è riflesso in `location.hash` (es. `/assistente/#terremoto_casa`) per condividere una risposta.
- Homepage: card "Cosa devo fare?" in `data/quick_links.yaml` → `servizi[0]`.

Per aggiungere un nuovo percorso: aggiungere un nodo `question` collegato da `start.options`, poi le relative `answer` referenziate da `options[n].next`. Rispettare il criterio `emergency: true` solo per situazioni operative reali (coerenza con regola `06-protezione-civile-scientifica.md` sul tono di comunicazione del rischio). Ogni nodo `answer` può avere un `pittogramma` opzionale (es. `'arasaac/terremoto.png'`) renderizzato come `<figure>` accessibile sopra il corpo della risposta (vedi sezione pittogrammi).

### Pagina `/emergenza/` lite (per banda debole o emergenze)

Pagina ultra-leggera (44 KB vs 64 KB della homepage) per consultazione rapida quando la rete è satura/lenta. Aliases attivi: `/lite/`, `/emergenza-essenziale/`. Contenuto in ordine di priorità: banner emergenza dinamico (se `data/emergenza.json` attiva), 112 grande con call-to-action, stato allerta meteo dinamico colorato (legge `data/allerta.json` al build), 4 numeri essenziali, 6 azioni "cosa fare ora", 7 link rapidi al sito completo. Zero widget esterni (Windy/Meteoam/IT-alert), CSS inline nello shortcode `pagina-emergenza-lite.html`. Linkata dal footer di tutte le pagine.

### TTS "Leggi ad alta voce" (Web Speech API)

Pulsante che usa `window.speechSynthesis` browser nativo per leggere il contenuto delle pagine essenziali in italiano. Voce `it-IT` preferita, rate 0.95 per chiarezza, stati idle/reading/paused, fallback graceful (bottone nascosto) se browser senza Web Speech API. Esclude script/pittogrammi/code blocks dal testo letto. Componente in `partials/leggi-ad-alta-voce.html`. Opt-in via frontmatter `tts: true`. Attivo su 12 pagine: cosa-fare-adesso, numeri-utili, facile-da-leggere, allerte-meteo, piano-familiare + 7 sotto-pagine rischi-prevenzione. Caso d'uso: anziani con vista debole, persone in stress/emergenza, parlanti italiano L2, bambini.

### Box "Cosa NON fare" (shortcode `cosa-non-fare`)

Box rosso bordato con icona divieto che evidenzia visivamente i comportamenti DA EVITARE in caso di emergenza. Aumenta l'efficacia della comunicazione del rischio rispetto ai "non" dispersi nel testo. Attivo nelle 7 pagine `/rischi-prevenzione/*` (sismico, incendio, idrogeologico, vento, temporali, blackout, ondate calore). Contrasto WCAG AA garantito (testo `#7f1d1d` su `#fff5f5` = 7.7:1). Compatibile con toolbar a11y (contrasto invertito + scala grigi).

### Box "Chi chiamare" (shortcode `chi-chiamare`)

Sezione finale standardizzata delle 7 pagine `/rischi-prevenzione/*`: tabella accessibile (`<caption>` + `<th scope="col">`) con 3 livelli di gravità (vita in pericolo → 112; pericolo concreto → 112; segnalazione non urgente → 803 555) + nota istituzionale che chiarisce che il **Gruppo Comunale non è attivabile direttamente dai cittadini** (l'attivazione passa da Comune, Centro Funzionale Lazio, Prefettura). Coerente con `06-protezione-civile-scientifica.md` e con la pagina `/contatti/`. Uso senza parametri: `{{< chi-chiamare >}}`. Insieme al box `cosa-non-fare` chiude la struttura uniforme **Prima → Durante → Dopo → NON fare → Chi chiamare** delle pagine rischio.

### Tabelle accessibili (render hook `render-table.html`)

Tutte le tabelle Markdown del sito sono renderizzate con `<th scope="col">` automatico (WCAG 1.3.1 Info and Relationships) + wrapping in `.table-responsive` Bootstrap Italia + supporto allineamento colonne (left/center/right) preservato dal Markdown. **Nessun editing manuale per pagina**: il fix è sistemico (oltre 400 `<th>` gestiti dall'hook).

Il file è `themes/flavour-pcgenzano/layouts/_default/_markup/render-table.html`. Per le tabelle con `<caption>` esplicito (consigliato per tabelle landing critiche tipo `/contatti/`, `/numeri-utili/`, `/chi-siamo/`) si usa **HTML diretto** dentro Markdown — l'attribute syntax di Goldmark non si applica alle tabelle in Hugo. Esempio: `<table><caption>...</caption><thead><tr><th scope="col">...</th></tr></thead>...</table>` — vedi `content/contatti/_index.md` per il pattern di riferimento. CSS coordinato in `custom.css` sezione **TABLE CAPTION v1.0** (italico blu istituzionale, `.visually-hidden` helper per caption per screen reader-only).

### FAQ accordion (CSS `.faq-item`)

Per ridurre muri di testo in pagine informative con molte domande/risposte (es. `/allerte-meteo/`, `/faq/`), il sito ha una classe `.faq-item` che stilizza l'elemento HTML nativo `<details>`/`<summary>` come accordion accessibile. Vantaggi: semantica nativa (zero JS, zero ARIA hand-rolled), navigabile da tastiera, letta correttamente dagli screen reader, override stampa che apre tutti i `<details>` automaticamente. Esempio: `<details class="faq-item"><summary><strong>Domanda</strong></summary>Risposta…</details>`. Sezione **FAQ ACCORDION v1.0** in `custom.css`.

### Share buttons (`partials/page-tools.html` + `js/share.js`)

In fondo a ogni articolo e a tutte le pagine che includono `page-tools.html` c'è una riga di icone per **condividere il contenuto** su WhatsApp, Telegram, Facebook, X, LinkedIn, Email, oppure **copiare il link**, oppure usare la **condivisione nativa** del sistema operativo (Web Share API). Privacy-first: **solo link "share intent" HTML standard + Clipboard API + Web Share API**, nessuno script di terze parti, nessun tracker. Conforme AGID + GDPR senza necessità di consent banner. Bootstrap Italia ha un'utility `share` analoga ([italia.github.io/bootstrap-italia/docs/utilities/share/](https://italia.github.io/bootstrap-italia/docs/utilities/share/)). Il bottone "condividi nativo" si auto-nasconde se `navigator.share` non è supportato (desktop). Specifiche complete in regola `04-hugo-architecture.md` sezione "Share buttons".

### Striscia pittogrammi (CSS `.kit-pittogrammi-row`)

Riga visiva di pittogrammi ARASAAC inline per dare un colpo d'occhio immediato a una pagina di lista (es. `/rischi-prevenzione/kit-emergenza/`). Layout flex centrato, sfondo azzurrino istituzionale, gap responsive. Pattern: `<div class="kit-pittogrammi-row" role="img" aria-label="...">{{< pittogramma inline="true" >}} ...</div>`. Sezione **STRISCIA PITTOGRAMMI v1.0** in `custom.css`.

### Modal SOS-112 (`partials/sos-112.html`)

Bottone fisso "SOS 112" in basso a destra (FAB), apre un modal di conferma con **3 azioni**:
1. **Annulla** (focus iniziale, ENTER non chiama).
2. **Cosa devo fare?** → `/assistente/` (albero decisionale guidato): per chi non è sicuro che sia un'emergenza vera. Bottone outline blu istituzionale.
3. **Sì, chiama il 112** (`tel:112`): bottone rosso primario.

Il modal include nota informativa azzurra (`.sos-modal-alt`) che spiega l'alternativa "assistente guidato" prima dei pulsanti, e mantiene il warning legale (art. 658 c.p.). Focus trap JS riconosce automaticamente i 3 elementi via selettore `[href]`. Link verso assistente passa per `relURL` per essere compatibile sia con Aruba (root) sia con GitHub Pages (subpath).

### Dati strutturati JSON-LD (`partials/structured-data.html`)

**Importante**: l'Organization è marcata come `["Organization", "NGO"]`, **NON** `GovernmentOrganization` né `EmergencyService`. Il Gruppo è associazione di volontariato OdV, non ente pubblico né servizio di emergenza chiamabile direttamente — usare quei tipi indurrebbe Google/assistenti vocali a presentare il Gruppo come servizio chiamabile, contraddicendo la regola "in emergenza chiama il 112". Schema attivi: Organization+NGO, ContactPoint dedicato, WebSite (con SearchAction), BreadcrumbList, Article (per `/comunicazioni/`), Event (aggiuntivo per `badge: Evento` con location Place + organizer), FAQPage (per `/faq/`), WebPage (default), Question/Answer, ImageObject, PostalAddress, GeoCoordinates, City. Quando si aggiungono schema nuovi, prudenza su tipi che inducano confusione tra associazione di volontariato e ente pubblico/servizio di emergenza.

### Strumenti di Accessibilità (toolbar utente)

Bottone rotondo blu (FAB) in basso a sinistra su ogni pagina, apre un dialog modale con preferenze di lettura (dimensione testo, contrasto, scala di grigi, spaziatura, carattere ad alta leggibilità, evidenzia link, cursore grande, ecc.). Persistenza in `localStorage`. Inline early script in `<head>` per evitare il flash visivo al caricamento.

File:
- `themes/flavour-pcgenzano/layouts/partials/accessibility-toolbar.html` (markup)
- `themes/flavour-pcgenzano/static/css/a11y-toolbar.css` (FAB + dialog + classi `html.a11y-*` di preferenze)
- `themes/flavour-pcgenzano/static/js/a11y-toolbar.js` (logica)
- Pagina pubblica correlata: `content/accessibilita/_index.md`.

Regole estese in `.claude/rules/04-hugo-architecture.md` e `.claude/rules/03-accessibility.md`. **Mai sostituire** con widget commerciali tipo AccessiBe / UserWay (sconsigliati da W3C-WAI). Quando modifichi un componente del sito, verifica che funzioni anche con contrasto invertito, scala di grigi, immagini nascoste, pausa animazioni.

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

9. **FOTO FORNITE DALL'UTENTE**: quando l'utente fornisce foto per un articolo, **TUTTE vanno inserite nel corpo** (mai sostituite dalla sola copertina) usando lo shortcode `{{< foto >}}`. Ogni foto deve avere la fascia blu istituzionale e alt text significativo. Per il **posizionamento di foto multiple** in articoli storici (anniversari, memoria, eventi multipli), seguire la convenzione descritta nella sezione *"Shortcode foto"* qui sopra: 1ª foto dopo 1° H2, 2ª dopo 2° H2, foto successive sull'H2 di ogni evento storico specifico citato. Mai foto a casaccio.

10. **STAMPA**: il file `themes/flavour-pcgenzano/static/css/custom.css` contiene regole `@media print` globali che, quando l'utente clicca "Stampa" su una pagina, nascondono header/navbar/footer/banner/cookie/utility bar/page tools e stampano solo il contenuto della pagina (H1 + articolo + allegati) su A4 con margini standard. Non modificare questa sezione senza valutare l'impatto su tutti i layout.

11. **DATA ULTIMA REVISIONE (pagine legali/istituzionali)**: le pagine `privacy`, `note-legali`, `accessibilita`, `social-media-policy` hanno nel frontmatter il campo **`dataUltimaRevisione: "AAAA-MM-GG"`**. Il template `single.html` lo mostra come box evidente in cima al contenuto ("Pagina rivista il …"). Quando modifichi il contenuto sostanziale di una di queste pagine, aggiorna anche la data. Non usare stringhe tipo "Marzo 2026" nel corpo: il riferimento è unico e nel frontmatter. Il partial `page-tools.html` riconosce il campo e omette la `.Lastmod` automatica su queste pagine, per evitare date duplicate in conflitto.

12. **COMUNICAZIONE DI CRISI E DEL RISCHIO — gerarchia delle fonti**: il Gruppo si attiene a un quadro **gerarchico** di fonti normative e tecniche. In caso di conflitto teorico, prevale il livello superiore.
    1. **Italiano vincolante**: AGID (linee guida PA digitale) + DPC (Dipartimento Protezione Civile, riferimento settoriale: D.Lgs. 1/2018, Direttiva PCM 30 aprile 2021, linee guida sulla comunicazione del rischio, campagne "Io non rischio", bollettini di criticità, codici colore ufficiali). **Su un contenuto di Protezione Civile, DPC prevale su AGID** perché siamo Gruppo Comunale del Sistema Nazionale di PC.
    2. **Scientifico italiano**: CNR (CNR-IRPI per idrogeologico, CNR-INGV con INGV per sismologico-vulcanologico, CNR-IGAG per geologico) + ISPRA. Garantiscono la correttezza scientifica del merito. Su un dato scientifico vince CNR/ISPRA; sul *come* comunicarlo vince DPC.
    3. **Tecnico-operativo europeo**: EENA (European Emergency Number Association — è dietro lo sviluppo dell'app Where Are U) + CWA CEN/CENELEC (struttura messaggi di crisi sui social).
    4. **Standard internazionali**: ISO 22329:2021 (uso social media in emergenza) + WCAG 2.2 AA (accessibilità tecnica).
    5. **Normativa orizzontale**: DL 25/2025 (SMM PA), GDPR, L. 4/2004 (Stanca), CAD.

    Applicazione operativa nei post di allerta/emergenza: struttura standard del messaggio in 6 punti (tipo / livello-colore / area+tempo / cosa fare / fonte / prossimo aggiornamento), hashtag specifici e localizzati, monitoraggio della disinformazione (mai amplificare per smentire), accessibilità post (alt text, max 2 emoji, niente Unicode decorativi, non solo-colore per allerte). Specifiche complete in `MANUALE-SITO.md` Parte 13.7 e 13.9, e nelle regole `02-content-design-pa.md`, `03-accessibility.md`, `06-protezione-civile-scientifica.md`. La pagina pubblica `/social-media-policy/` espone questi principi al cittadino.

13. **CARTELLA `riferimenti-interni/`** (root del repo, NON deployata): contiene documentazione di lavoro per maintainer/AI di supporto che non va pubblicata sul sito (norme copyrighted, draft di consultazione, materiale interno). Hugo non la legge perché non rientra nelle cartelle native (`content/`, `static/`, `themes/`, `data/`, `assets/`, `layouts/`). Convenzione: 🟢 documenti pubblici → `static/manuali/`, 💶 copyrighted o riservati → `riferimenti-interni/<categoria>/`. Indice + stato accessibilità in `riferimenti-interni/README.md`. Specifiche complete nella regola `04-hugo-architecture.md`.

14. **SANDBOX CLAUDE CODE — sblocco per fonti immagini libere**: per scaricare foto da Wikipedia / Wikimedia / NASA / USGS senza essere bloccato dalla sandbox di sicurezza, il repo ha una configurazione predefinita in `.claude/settings.local.json` (in `.gitignore`, locale). Lo schema completo (allowlist `permissions` + `sandbox.network.allowedDomains` per i 9 domini delle nostre fonti foto) è in `MANUALE-SITO.md` Parte 14. Procedura: creare il file una volta sola, riavviare Claude Code (la sandbox legge il file all'avvio, non dinamicamente). Senza questo sblocco, le fonti immagini sono comunque accessibili al workflow `scarica-foto-automatica.yml` su GitHub Actions (rete libera): basta usare il marker `# TODO-foto-wikipedia` nel frontmatter dell'articolo. Specifiche in `MANUALE-SITO.md` Parte 14 e nella regola `08-claude-code-setup.md`.

14. **DATI ALLERTA METEO `data/allerta.json`**: due campi temporali distinti. `ultimo_aggiornamento` cambia **solo** quando il livello DPC cambia. `ultimo_controllo` cambia ogni volta che il workflow `check-allerta.yml` verifica il bollettino e committa (ogni ≥6 ore o cambio livello). Limite: max 4 commit/giorno + cambi di livello. Sia la barra allerta della homepage sia la pagina `/emergenza/` lite mostrano "Verificato: ..." sempre fresco. Il JS lato browser sulla homepage aggiorna ulteriormente il timestamp all'ora locale del client. Schema completo in `MANUALE-SITO.md` Parte 9.3.

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
| `audit-sito.yml` | Lunedì 09:00 UTC | **Audit completo (38 sezioni)**: contenuti pubblicati (COI, NUE 112, telefono, sede, CAP, placeholder, asset, badge, date, allegati, frasi AGID, draft `_index`, schede stampabili, modalità emergenza, pagine legali, widget) + codice/template (build Hugo, articoli `draft:true`, link a slug inesistenti, sintassi JS, validità YAML workflow, path assoluti template, residui CCV-MB/lombardo/`/index.html`) + governance docs (file presenti, import CLAUDE, badge list coerente, formato date, frontmatter, riferimenti incrociati, pagine obbligatorie, shortcode foto, script export, `dataUltimaRevisione`) + audit aggiuntivo (mixed content `http://`, `image_alt` accessibility WCAG 1.1.1, coerenza dati istituzionali nelle 7 traduzioni, divergenze `hugo.toml` ↔ `data/numeri_utili.yaml`, smoke test rendering H1 pagine critiche, **8 link critici normativa/PDF locali con messaggi dedicati**). Apre 1 issue settimanale con tutti i findings |
| `check-links-sito.yml` | Lunedì 10:00 UTC | Crawl completo del sito con **lychee**: verifica TUTTI i link (interni + esterni, tutte le pagine), apre issue automatica su 404/drift. Catch-all per mantenere aggiornati hub Strumenti, widget, Area Download, link esterni nei contenuti |
| `scarica-foto-automatica.yml` | Ogni push su `main` | **Step 1** — Scansiona articoli con marker `# TODO-foto-{wikipedia,nasa,usgs}: bash scripts/foto-da-XXX.sh "..." slug` (usato quando si scrive da mobile/cloud, dove la sandbox blocca i domini esterni). Fonti supportate (whitelist): **Wikipedia/Wikimedia** (PD/CC0/CC-BY/CC-BY-SA), **NASA Image Library** (Public Domain), **USGS Earthquake Hazards** (ShakeMap, Public Domain). Per ogni articolo: esegue lo script, scarica foto, applica fascia blu, aggiorna `image:` + `image_credit:` + `image_source_url:` nel frontmatter, rimuove il marker. **Step 2** — Genera cover tipografiche istituzionali (gradiente blu + titolo + fascia) per articoli rimasti con `image: ""` e SENZA marker (via `scripts/auto-cover-mancanti.py`, che chiama `genera-cover.py` + popola frontmatter solo se vuoto, mai sovrascrive foto utente). **Step 3** — Commit unico delle modifiche, ri-triggera `deploy.yml`. Apre issue se uno o più download foto falliscono. Skip-loop: i propri commit hanno `[skip-foto-wiki]` |

> **Storia merge**: il 26 aprile 2026 sono stati fusi 2 workflow dentro `audit-sito.yml` per consolidare le issue settimanali:
> - `coerenza-docs.yml` (lun 07:00) → sezioni 23-32 (governance docs)
> - `check-normativa-links.yml` (lun 08:00) → sezione 38 (link critici con messaggi dedicati)
>
> Risultato: -2 workflow, 1 issue settimanale invece di 3, stessa copertura.

## Key operational notes

- **To activate emergency mode**: set `"attiva": true` in `data/emergenza.json` and fill `tipo`, `titolo`, `descrizione`. Reset to `false` when done.
- **To set weather alert**: edit `data/allerta.json` — change `livello` to `verde/giallo/arancione/rosso`.
- **Draft posts**: set `draft: true` in front matter. They appear locally with `hugo server -D` but are not published.
- **CI deploy**: pushing to `main` triggers `.github/workflows/deploy.yml` which builds twice (once per baseURL) and deploys via FTP to Aruba and via GitHub Pages API. Monitor at the Actions tab.
- **FTP credentials** are stored as GitHub secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).
