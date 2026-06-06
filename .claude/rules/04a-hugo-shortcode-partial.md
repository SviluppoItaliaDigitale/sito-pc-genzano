# Hugo — Shortcode, Render Hook, Partial

Questo file raccoglie gli **shortcode**, i **render hook Markdown** e i **partial** del tema. Per la struttura del progetto, le regole Hugo fondamentali e i comandi vedi `04-hugo-architecture.md`. Per template, CSS, menu di navigazione e UX vedi `04b-hugo-template-css.md`.

## Shortcode `foto` (immagini nel corpo degli articoli)

Il tema definisce due shortcode: `foto` (foto evento) e `pittogramma` (simboli).

```go-html-template
{{< foto src="/images/AAAA-MM-GG-descrizione.webp"
         alt="Testo alternativo per screen reader"
         caption="Didascalia opzionale" >}}
```

Produce `<figure>` con:
- immagine cliccabile che apre a dimensione intera in nuova scheda
- `aria-label` descrittivo sul link ("Apri a dimensione intera: {alt}")
- `<figcaption>` opzionale che accetta markdown inline
- `loading="lazy"` e responsive (Bootstrap Italia `img-fluid`)
- Funziona senza JavaScript (progressive enhancement)

`src` e `alt` sono **obbligatori**: la mancanza causa errore di build Hugo.

## Shortcode `pittogramma` (simboli ISO 7010 e ARASAAC)

Inserisce pittogrammi standardizzati per supportare la comprensione del testo a bambini, anziani, persone con disabilità cognitive e parlanti italiano L2 (regola 03 — accessibilità cognitiva).

Uso block (figure centrata con caption opzionale):
```go-html-template
{{< pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto"
                size="large" >}}
```

Uso inline (dentro una frase):
```go-html-template
Chiama il {{< pittogramma src="/pittogrammi/arasaac/112.png" alt="numero 112" inline="true" >}} 112.
```

Parametri:
- `src` (obbligatorio) — percorso pittogramma in `/pittogrammi/iso7010/` o `/pittogrammi/arasaac/`
- `alt` (obbligatorio) — testo alternativo significativo per screen reader (mai stringa vuota: il pittogramma non è decorativo, è esplicativo)
- `caption` (opzionale, solo block) — didascalia visibile sotto
- `inline="true"` — inserimento inline dentro una frase (default: block)
- `size` — `small` (48px) | `medium` (96px, default) | `large` (160px) | `xlarge` (240px)

Produce `<img>` con `role="img"` e `loading="lazy"`, oppure `<figure>` con caption opzionale. CSS scoped in `custom.css` (sezione **PITTOGRAMMI v1.0**) con dimensioni fisse, override mobile (large/xlarge ridotti su <576px), mantenimento colori in stampa (i colori dei segnali ISO 7010 sono parte dell'informazione di sicurezza e non devono essere convertiti in scala di grigi).

**Libreria disponibile** (simboli, 3.3 MB):
- `static/pittogrammi/iso7010/*.svg` — 46 segnali standard (E* evacuazione, F* antincendio, W* avvertimento, M* obbligo, P* divieto). Vettoriali, scalabili senza perdita.
- `static/pittogrammi/arasaac/*.png` — simboli (eventi/rischi, azioni autoprotezione, oggetti kit emergenza, persone, luoghi, segnali, veicoli, numeri utili). Bitmap 500px.

**Re-download della libreria**: `bash scripts/scarica-pittogrammi.sh` (idempotente, scarica solo i mancanti; `--force` ri-scarica tutto). Lo script ha rate-limit 1s tra le richieste Wikimedia per evitare ban temporaneo.

**Regole di attribuzione (obbligatorie):**
- Pagina `/attribuzioni-pittogrammi/` linkata dal footer di tutte le pagine.
- ARASAAC è CC BY-NC-SA 4.0: le opere derivate (ad esempio le **schede stampabili PDF** dei kit didattici) che includono pittogrammi ARASAAC ereditano la stessa licenza CC BY-NC-SA 4.0.
- ISO 7010 da Wikimedia: prevalentemente PD-shape/CC0, attribuzione di cortesia su pagina dedicata.

**Regole di uso editoriale:**
- Non sostituire il testo con il solo pittogramma: il pittogramma è di **supporto** alla comprensione, mai sostituto. WCAG 1.4.5 (Images of Text) e principio di leggibilità per L2.
- Usare un pittogramma per concetto chiave, non come "decorazione visiva" continua: la sovrabbondanza riduce l'efficacia comunicativa per gli utenti che ne hanno davvero bisogno.
- Per segnali di sicurezza (ISO 7010 di tipo P/W/M/F): preferire i simboli standard a quelli ARASAAC quando si comunica un obbligo o un divieto formale.
- Per situazioni narrative o didattiche destinate a bambini: preferire ARASAAC per il colore e il tratto più riconoscibile.

## Shortcode `cosa-non-fare` (box divieti per pagine rischio)

Box rosso bordato (`#c1121f`) con icona divieto che evidenzia visivamente i comportamenti DA EVITARE. Aumenta l'efficacia della comunicazione del rischio rispetto ai "non" dispersi nel testo. Usato sulle 7 pagine `/rischi-prevenzione/*`.

```go-html-template
{{< cosa-non-fare titolo="Cosa NON fare in caso di terremoto" >}}
- **Non correre fuori durante la scossa**
- **Non usare gli ascensori**
- **Non usare il telefono per curiosità**
{{< /cosa-non-fare >}}
```

Parametro `titolo` opzionale (default: "Cosa NON fare"). Contenuto Markdown standard. Output: `<div role="region" aria-label="...">` con header colorato + body in lista. Contrasto WCAG AA: testo `#7f1d1d` su `#fff5f5` = 7.7:1. CSS scoped sezione **COSA NON FARE v1.0** in `custom.css`. In stampa diventa nero su bianco mantenendo gerarchia visiva con `page-break-inside: avoid`.

## Shortcode `chi-chiamare` (chiusura standard pagine rischio)

Sezione finale uniforme delle 7 pagine `/rischi-prevenzione/*`: tabella accessibile (`<caption>` + `<th scope="col">`) con i numeri da chiamare per livello di gravità + nota istituzionale che chiarisce la modalità di attivazione del Gruppo.

```go-html-template
{{< chi-chiamare >}}
```

Nessun parametro. Produce un `<section aria-labelledby>` con:
- `<h2>` "Chi chiamare"
- Tabella `caption + thead + tbody`: 3 righe (vita in pericolo → 112, pericolo concreto → 112, segnalazione non urgente → 803 555 Sala Operativa PC Lazio)
- `<a href="tel:112">` su ogni occorrenza del 112 con stile `.chi-chiamare-call` rosso istituzionale + focus visibile (WCAG 2.4.7)
- Alert role=note che chiarisce: *"Il Gruppo Comunale Volontari di PC Genzano non può essere attivato direttamente dai cittadini"* — coerente con regola `06-protezione-civile-scientifica.md` e con le pagine `/contatti/` e `/numeri-utili/`.

CSS scoped sezione **CHI CHIAMARE BOX v1.0** in `custom.css`. In stampa il numero 112 resta nero con underline.

**Struttura uniforme finale delle pagine rischio**: dopo l'introduzione "Perché è rilevante sul nostro territorio" e gli eventuali "Segnali e situazioni tipiche", ogni pagina ha l'ordine fisso **Cosa fare PRIMA → Cosa fare DURANTE → Cosa fare DOPO → `cosa-non-fare` → `chi-chiamare`**. Modello di riferimento per nuovi rischi che dovessero essere aggiunti in futuro.

## Shortcode `link-card` (griglia di card link nei contenuti)

Card link visibile (icona + titolo + descrizione) per griglie di consultazione dentro le pagine markdown, in alternativa all'elenco puntato anonimo. Nato per la sezione "Pagine di consultazione rapida" dell'hub `/rischi-prevenzione/` (la scheda scuolabus non si trovava in un bullet — maggio 2026).

```go-html-template
<div class="consulta-rapida">
{{</* link-card url="/rischi-prevenzione/sicurezza-scuolabus/" icon="bi-bus-front" titolo="Sicurezza sullo scuolabus" desc="Cosa fare in emergenza durante il tragitto." */>}}
... altre card ...
</div>
```

- Parametri: `url` (path interno), `icon` (classe Bootstrap Icons), `titolo`, `desc`. Tutti obbligatori.
- **Subpath GitHub Pages**: il template fa `.Get "url" | strings.TrimPrefix "/" | relURL` (stesso pattern del render-link hook), così i link funzionano sia su Aruba (root) sia su GitHub Pages (`/sito-pc-genzano/`). Scrivere `url` con leading slash.
- Le card vanno avvolte in `<div class="consulta-rapida">` (raw HTML nel markdown), senza righe vuote tra gli shortcode. CSS scoped sezione **CARD CONSULTAZIONE RAPIDA v1.0** in `custom.css` (hover lift, focus visibile `#ffbe2e`, `prefers-reduced-motion` + `a11y-pause-anim`, stampa).

## Componenti Bootstrap Italia — `callout`, `passi`, `timeline`, `galleria` (maggio 2026)

Quattro shortcode di contenuto, AGID/WCAG, applicabili a contenuto già esistente per migliorarne lettura e orientamento.

- **`callout`** — box nota del design system: **usa il componente NATIVO Bootstrap Italia** (`.callout .note/.warning/.danger/.success` + `.callout-inner` + `.callout-title` con icona dallo sprite BI `vendor/bootstrap-italia/svg/sprites.svg`). API autore: `{{</* callout tipo="info|avviso|pericolo|ok" titolo="…" */>}} testo markdown {{</* /callout */>}}` (mappa: info→note, avviso→warning, pericolo→danger, ok→success). 🔴 **Non creare CSS `.callout` custom**: collide col bundle BI (incidente: titolo con `margin-bottom:2.222rem` ereditato). Nessuna CSS custom per il callout.
- **`passi`** (stepper) — avvolge una **lista ordinata Markdown** e la rende con pallini numerati (CSS counter su `<ol>` reale → ordine annunciato dagli screen reader). `{{</* passi titolo="…" */>}}` … lista `1. 2. 3.` … `{{</* /passi */>}}`. CSS sezione **PASSI / STEPPER v1.0**.
- **`timeline`** — avvolge una **lista Markdown** (un evento per voce, di norma `**data/titolo** — testo`) e la rende come linea del tempo verticale con marcatori. CSS sezione **TIMELINE v1.0**.
- **`galleria`** (carosello) — per articoli con **≥4 foto**: avvolge più `{{</* foto */>}}` in un carosello accessibile, **solo avanzamento manuale** (mai autoplay — WCAG 2.2.2), scroll-snap + pulsanti prev/next con `aria-label` disabilitati ai bordi, `static/js/galleria.js` idempotente. CSS sezione **GALLERIA v1.0**.

Utility correlate in `custom.css`: **`.pc-spinner`** (indicatore di caricamento, rispetta `prefers-reduced-motion` + `a11y-pause-anim`; cablato negli stati di caricamento del Laboratorio meteo) e **`.table-sticky`** (intestazione tabella sticky per tabelloni lunghi, `max-height:70vh`).

## Shortcode `scheda-terremoto` (scheda dettaglio evento sismico)

`themes/flavour-pcgenzano/layouts/shortcodes/scheda-terremoto.html` rende la **scheda di dettaglio di un singolo terremoto** sul modello della pagina evento di `terremoti.ingv.it`. Usato dalla pagina `content/cruscotto/terremoto.md` (URL `/cruscotto/terremoto/`), che riceve l'ID evento via **hash** (`#46107472`) o query (`?event=46107472`).

- **Dati live INGV FDSN** (CORS aperto, fetch dal browser, niente widget di terzi): GeoJSON (`?eventid=<id>&format=geojson`) per il riepilogo; QuakeML (`&includeallmagnitudes=true&includeallorigins=true&includearrivals=false`) per le magnitudo/origini multiple. L'ID evento INGV è in `properties.eventId`; coordinate GeoJSON `[lon, lat, prof]`.
- **Tab accessibili** (pattern ARIA tablist, frecce/Home/End, roving tabindex): Dati evento (mappa epicentro **a piena larghezza** Leaflet self-hosted + griglia parametri `.eq-dati-grid` sotto) · Localizzazioni e magnitudo · Meccanismo di sorgente · Impatto · Sismicità (FDSN bbox ~50 km, ultimi 30 gg) · Cosa fare (autoprotezione sismica + link a `/rischi-prevenzione/rischio-sismico/`) · Download.
- **Prodotti scientifici INGV non ricalcolati** (vincolo: siamo associazione di volontariato, non ente sismologico — coerente con lo schema `Organization`): ShakeMap e meccanismo focale sono **embed ufficiali con attribuzione CC BY-SA** se esistono (img con `onerror` → fallback), altrimenti **deep-link** alla scheda INGV. Per eventi profondi/offshore questi prodotti spesso non esistono.
- **Condivisione/stampa/QR** dal chrome standard di pagina (`page-tools.html`); il tab Download offre QuakeML/GeoJSON + scheda ufficiale INGV.
- CSS scoped in un blocco `<style>` interno allo shortcode (sezione **SCHEDA TERREMOTO v1.0**). La pagina ha `tts: false`, `indice: false`, `build.list: never` (non in liste/RSS/sitemap: è una pagina-strumento che richiede l'hash).
- **Collegamento dal cruscotto**: `dashboard-terremoti.html` cattura `properties.eventId` e linka ogni riga (cella "Zona") e popup mappa a `/cruscotto/terremoto/#<id>` (URL via `relURL | jsonify`).

🔴 **Filtro eventi italiani (`isItaliano`) in `dashboard-terremoti.html`**: l'API INGV chiude il `place` con la provincia tra parentesi, a volte come **sigla** `(CS)`, a volte come **nome esteso** `(Cosenza)`/`(Reggio Calabria)` (tipico degli eventi offshore). Il filtro accetta entrambi (set `PROVINCE_IT` sigle + `PROVINCE_NOMI` nomi estesi) + mari/coste italiane. **Non restringere a sole sigle**: il 1° giugno 2026 un M6.2 "Costa Calabra nord-occidentale (Cosenza)" non compariva perché il filtro accettava solo `(CS)`.

## Partial `indice-pagina` — indice di pagina con scrollspy (site-wide)

`themes/flavour-pcgenzano/layouts/partials/indice-pagina.html` produce l'**indice "In questa pagina"** (navscroll Bootstrap Italia semplificato): elenco da `.TableOfContents`, sticky a sinistra su desktop (colonna 2-col in `_default/single.html` e `_default/list.html`), accordion collassabile su mobile. `static/js/indice-pagina.js` evidenzia la sezione corrente mentre si scorre (scrollspy → `.active` + `aria-current` sui link). CSS sezione **INDICE DI PAGINA v1.0**.

- **Gate site-wide**: compare automaticamente sulle pagine con `len .Fragments.Identifiers >= 3` (≥3 heading). ⚠️ Non usare `len .Fragments.Headings` (top-level): in Hugo 0.154 risultava inaffidabile (tornava 1).
- **Opt-out**: `indice: false` oppure `toc: false` nel frontmatter.
- **Escluse** (pagine-strumento): `cruscotto`, `laboratorio-meteo`, `cerca`, `emergenza`, `lanterna`, `mappa-sito`, `attribuzioni-pittogrammi` (più `comunicazioni` su list.html).
- Sostituisce il vecchio TOC in `<details>` (rimosso da single.html/list.html). Mantiene `id="indice"` per il back-to-top contestuale.

## Render hook tabelle (`_markup/render-table.html`)

Tutte le tabelle Markdown del sito sono rese dal hook `themes/flavour-pcgenzano/layouts/_default/_markup/render-table.html`. Comportamento:

- **`<th scope="col">` automatico** su ogni cella di intestazione (riga in `<thead>`). Migliora il riconoscimento da screen reader e rispetta WCAG 1.3.1 (Info and Relationships). Nessun editing manuale per pagina: si applica a tutte le tabelle Markdown del sito (oltre 400 `<th>` gestiti automaticamente).
- **Wrapping automatico in `.table-responsive`** Bootstrap Italia per scroll orizzontale su mobile sulle tabelle larghe.
- **Allineamento colonne** preservato dal Markdown (`:---`, `---:`, `:---:`) → reso come `style="text-align: ..."` sulle celle.
- **`<caption>` opzionale** via `Attributes.caption` o `Attributes.title`. **Importante**: la sintassi attribute block di Goldmark `{caption="..."}` **non si applica** alle tabelle Markdown in Hugo (limitazione del parser). Per aggiungere una caption a una tabella specifica, **convertire la tabella in HTML diretto** dentro Markdown:

```html
<div class="table-responsive">
<table>
<caption>Testo descrittivo della tabella</caption>
<thead>
<tr><th scope="col">Colonna A</th><th scope="col">Colonna B</th></tr>
</thead>
<tbody>
<tr><td>...</td><td>...</td></tr>
</tbody>
</table>
</div>
```

Tabelle landing già convertite con caption: `/contatti/` ("Quando contattarci"), `/numeri-utili/` (numeri emergenza), `/chi-siamo/` (consiglio direttivo, con `caption.visually-hidden` perché c'è già un card-header sopra). Per le altre 50+ tabelle Markdown del sito la caption non è necessaria: il `<th scope="col">` automatico è sufficiente per la conformità WCAG, perché ogni tabella è preceduta da un `<h2>` o `<h3>` che ne descrive il contenuto.

CSS scoped sezione **TABLE CAPTION v1.0** in `custom.css`: italico blu istituzionale, allineato a sinistra; helper `.visually-hidden` per caption screen reader-only (nasconde visivamente ma resta accessibile).

**Aggiornamento `hugo.toml`**: il render hook richiede Hugo ≥ 0.142.0. Il file `hugo.toml` ora ha `[markup.goldmark.parser.attribute]` con `block = true` e `title = true` abilitati per uso futuro su altri block element (le tabelle non li usano).

## Render-link hook (link Markdown nel corpo)

Il tema personalizza il rendering dei link Markdown tramite `layouts/_default/_markup/render-link.html` (copia speculare in `themes/flavour-pcgenzano/layouts/_default/_markup/render-link.html`). Comportamento:

- **Link interno `/...` che termina con estensione di file statico** (`.pdf`, `.webp`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.zip`, `.mp3`, `.mp4`, `.csv`, `.json`, `.txt`, `.rtf`, `.html`, `.htm`): reso come `<a>` diretto. Serve per linkare file in `static/manuali/`, `static/allegati/`, `static/images/`, `static/open-data/` e micro-siti HTML autonomi in `static/quizpc/`, `static/formazionepc/`, `static/giochi/` senza che il controllo `site.GetPage` li marchi come "non disponibili".
- **Link interno `/.../` (path che termina con `/`) verso cartella con `static/<path>/index.html`**: il hook fa `fileExists "static/<path>/index.html"` e se esiste lo tratta come statico. Serve per scrivere `[Giochi](/giochi/)` senza dover specificare `/index.html`.
- **Link interno `/...` verso pagina Hugo esistente**: `<a>` normale.
- **Link interno `/...` verso pagina non trovata** (e non file statico): `<span class="text-muted" title="Contenuto non ancora disponibile">` — consente di linkare articoli non ancora pubblicati che si attiveranno automaticamente al deploy successivo.
- **Link esterno `http(s)://`**: `<a target="_blank" rel="noopener noreferrer">`.
- **`mailto:` / `tel:`**: `<a>` con `safeURL`.

**Subpath GitHub Pages e `relURL`**: il hook strippa il leading `/` dal link prima di passarlo a `relURL`. Hugo `relURL` **non** aggiunge il subpath del baseURL ai path che iniziano con `/`: `relURL "/foo"` resta `/foo`, mentre `relURL "foo"` diventa `/sito-pc-genzano/foo`. Senza questo strip, tutti i link interni del markdown (che per convenzione scriviamo con leading `/`) funzionerebbero su Aruba (baseURL root) ma sarebbero rotti su GitHub Pages (baseURL con subpath `/sito-pc-genzano/`). Se modifichi il hook, mantieni la riga `$relLink := strings.TrimPrefix "/" $link` e usa `$relLink | relURL` in tutti i branch interni.

Se estendi la lista di estensioni statiche o modifichi il comportamento di `relURL`, aggiorna **entrambi** i file `render-link.html` (progetto e tema) per mantenere la coerenza.

## FAQ accordion (`.faq-item` su `<details>`)

Per ridurre muri di testo in pagine con molte domande/risposte (es. `/allerte-meteo/`, `/faq/`), il sito ha una classe `.faq-item` che stilizza l'elemento HTML nativo `<details>`/`<summary>` come accordion accessibile.

```html
<details class="faq-item">
<summary><strong>Domanda concisa</strong></summary>

Risposta in Markdown standard. Bullet, link, **enfasi**.

</details>
```

Caratteristiche:
- **Semantica nativa**: zero JS, zero ARIA hand-rolled. Lettura corretta da screen reader, navigazione tastiera nativa (Enter/Space su `<summary>`).
- **Chevron CSS-only** (border + transform): nessuna icona da caricare, nessun JS di animazione.
- **Focus visibile WCAG 2.4.7** (outline `#ffbe2e` 3px su `<summary>`).
- **Override stampa**: tutti i `<details>` aperti automaticamente con `display: block !important`, niente icona chevron — il documento stampato include sempre tutto il contenuto.
- **Override mobile** (≤576px): padding ridotto.

CSS scoped sezione **FAQ ACCORDION v1.0** in `custom.css`. Quando si introduce un nuovo accordion FAQ, riutilizzare questa classe: non servono varianti nuove.

## Share buttons (`partials/page-tools.html` + `js/share.js`)

Riga di icone in fondo a ogni articolo e a tutte le pagine che includono il partial `page-tools.html` (cioè: `_default/single.html`, `rischi-prevenzione/single.html`, `pittogrammi/single.html`). Permette al cittadino di condividere il contenuto su WhatsApp, Telegram, Facebook, X (Twitter), LinkedIn, Email, oppure di copiare il link, oppure di usare la condivisione nativa del sistema operativo (Web Share API).

**Architettura privacy-first:**

- **Solo link "share intent" HTML standard** (`https://wa.me/?text=...`, `https://t.me/share/url?url=...`, ecc.): nessun JavaScript SDK delle piattaforme social. Niente tracker, niente cookie di terze parti. Conforme **AGID** + **GDPR** senza necessità di consent banner aggiuntivo.
- **Web Share API nativa** (`navigator.share()`) per il bottone "Altre app": apre il selettore di app del sistema operativo. Il bottone si auto-nasconde via JS se l'API non è disponibile (desktop senza supporto).
- **Clipboard API** (`navigator.clipboard.writeText()`) per "Copia link", con fallback a `document.execCommand('copy')` per vecchi browser. Feedback visivo: classe `.copied` + icona check + aria-label "Link copiato negli appunti" per 2 secondi.

**Bottoni in ordine** (HTML in `page-tools.html`):

1. WhatsApp — `bi-whatsapp` — colore brand al hover (`#25d366`)
2. Telegram — `bi-telegram` — colore brand al hover (`#229ed9`)
3. Facebook — `bi-facebook` — colore brand al hover (`#1877f2`)
4. X (Twitter) — `bi-twitter-x` — nero al hover (`#000`)
5. LinkedIn — `bi-linkedin` — colore brand al hover (`#0a66c2`)
6. Email — `bi-envelope` — `mailto:?subject=...&body=...`
7. Copia link — `bi-link-45deg` — Clipboard API + feedback verde
8. Condividi nativo — `bi-three-dots` — Web Share API mobile (auto-nascosto su desktop)

**Accessibilità:**
- Ogni `<a>` o `<button>` ha `aria-label` descrittivo (es. "Condividi su WhatsApp").
- Testo nascosto per screen reader (`<span class="visually-hidden">WhatsApp</span>`) accanto all'icona — gli screen reader leggono entrambi.
- `target="_blank" rel="noopener noreferrer"` sui link esterni.
- Focus visibile con outline `#ffbe2e` (giallo PA) di 3px.
- `prefers-reduced-motion`: disattiva l'animazione `translateY(-2px)` al hover.

**Stampa:** la riga share è nascosta automaticamente da `@media print` (sia globale sia locale per ridondanza).

**Mobile:** bottoni rimpiccioliti a 36px e label "Condividi:" su riga propria. Il bottone "Condividi nativo" è particolarmente utile su mobile.

CSS scoped sezione **SHARE BUTTONS v1.0** in `custom.css`. JS in `static/js/share.js` (caricato `defer` da `baseof.html`). Quando si modifica la lista delle piattaforme, aggiornare entrambi i blocchi (HTML + CSS hover colors).

## Striscia pittogrammi (`.kit-pittogrammi-row`)

Riga visiva di pittogrammi inline ARASAAC per dare un colpo d'occhio immediato a una pagina lista (es. `/rischi-prevenzione/kit-emergenza/`). Layout flex centrato, gap responsive, sfondo azzurrino istituzionale.

```html
<div class="kit-pittogrammi-row" role="img" aria-label="Componenti essenziali del kit di emergenza: zaino, acqua, cibo, torcia, radio, medicine, documenti, fischietto">
{{< pittogramma src="/pittogrammi/arasaac/zaino.png" alt="Zaino" size="small" inline="true" >}}
{{< pittogramma src="/pittogrammi/arasaac/acqua.png" alt="Acqua" size="small" inline="true" >}}
{{< pittogramma src="/pittogrammi/arasaac/cibo.png" alt="Cibo" size="small" inline="true" >}}
{{< pittogramma src="/pittogrammi/arasaac/torcia.png" alt="Torcia" size="small" inline="true" >}}
</div>
```

Regole:
- **`role="img"` + `aria-label` complessivo** sul wrapper: gli screen reader leggono la striscia come **una sola immagine descrittiva** invece di leggere ogni `alt` singolo. WCAG 1.1.1 conforme.
- Pittogrammi all'interno con `size="small"` (48px) e `inline="true"` per evitare il layout `<figure>` block default.
- Su mobile (≤576px) gap ridotto + padding ridotto.
- In stampa lo sfondo diventa bianco e il bordo nero, `page-break-inside: avoid`.

CSS scoped sezione **STRISCIA PITTOGRAMMI v1.0** in `custom.css`.

## Modal SOS-112 esteso (`partials/sos-112.html`)

Vedi `CLAUDE.md` sezione "Modal SOS-112" per la sintesi. Il modal di conferma chiamata 112 ha **3 azioni**: Annulla (focus iniziale, ENTER sicuro), "Cosa devo fare?" (link a `/assistente/`, bottone outline blu istituzionale), "Sì, chiama il 112" (bottone rosso primario, `<a href="tel:112">`).

Note operative:
- L'href dell'assistente passa per `{{ "assistente/" | relURL }}` per compatibilità Aruba/GitHub Pages.
- Il focus trap JS rileva tutti i `[href]` e bottoni: il nuovo `<a id="sos-modal-guide">` viene incluso automaticamente nel ciclo Tab/Shift+Tab.
- CSS scoped: `.sos-modal-btn-guide` (outline blu) + `.sos-modal-alt` (nota informativa azzurra prima dei bottoni). Sezione esistente del modal in `custom.css`.

Se un domani serve aggiungere una **quarta azione** (ipotesi: "Numeri utili"), aggiungere prima del bottone "Cosa devo fare?" — non distruggere l'ordine: sequenza visiva column-reverse su mobile (Call → Cosa fare → Annulla dall'alto al basso) e row su desktop (Annulla → Cosa fare → Call da sinistra a destra), che è la gerarchia di azione corretta.

## Shortcode `pagina-emergenza-lite` (pagina `/emergenza/`)

Contiene tutto il rendering della pagina `/emergenza/` (pagina **ultra-leggera** per banda debole o emergenze: 44 KB vs 64 KB della homepage). Usa `data/allerta.json` e `data/emergenza.json` letti al build. Zero widget esterni (Windy/Meteoam/IT-alert), CSS inline minimale (~3KB), niente Bootstrap né JS aggiuntivo. Usato solo dalla pagina `content/emergenza/_index.md`.

**Contenuto in ordine di priorità:**
1. Banner emergenza dinamico (se `data/emergenza.json` attiva).
2. 112 grande con call-to-action `tel:112`.
3. Stato allerta meteo dinamico colorato (legge `data/allerta.json` al build).
4. 4 numeri essenziali.
5. 6 azioni "cosa fare ora".
6. 7 link rapidi al sito completo.

Aliases pagina: `/lite/`, `/emergenza-essenziale/`. Linkata dal footer di tutte le pagine. Caso d'uso: rete satura/lenta durante un'emergenza, dispositivi vecchi, consultazione rapida da mobile.

## Partial `leggi-ad-alta-voce` (TTS Web Speech API)

Vedi regola `03-accessibility.md` sezione TTS per dettagli. Sintesi: opt-in via frontmatter `tts: true`, attivo su 12 pagine essenziali, voce italiana di default, fallback graceful, accessibile da tastiera. Componente in `partials/leggi-ad-alta-voce.html`, CSS in `custom.css` sezione **TTS v1.0**.

## Partial `article-cover` (copertina con didascalia credit)

Le copertine degli articoli sono renderizzate dal partial `themes/flavour-pcgenzano/layouts/partials/article-cover.html`, chiamato da `_default/single.html` per `content/comunicazioni/*.md`.

Comportamento del partial:
- Se `.Params.image` presente: produce un `<figure>` con `<img>` e (opzionale) `<figcaption>`.
- Se `.Params.image` assente: fallback su `images/notizia-default.svg` (no caption, `aria-hidden="true"`).
- Se `.Params.image_credit` o `.Params.image_source_url` presenti: aggiunge la `<figcaption class="article-cover-credit">` con icona camera, testo credit e link "Fonte originale" (target=_blank, rel=noopener, aria-label esplicito).

Stile in `custom.css` sezione **ARTICLE COVER v1.0**: testo piccolo (0.82rem), italic, allineato a destra, link blu istituzionale. Su mobile: text-align left, font 0.78rem. In stampa: colori convertiti in nero, link che si espande con URL completo (per la riproducibilità del documento stampato).

**Quando viene popolato `image_credit`**: a maggio 2026 lo popolava automaticamente il workflow `scarica-foto-automatica.yml` per gli articoli con marker `# TODO-foto-wikipedia`. Dal 3 maggio 2026 il marker è bandito (CLAUDE.md punto 9): le foto da fonti ufficiali vanno inline nel corpo come `{{< foto >}}` con caption che cita autore + licenza, NON nel banner. Quindi `image_credit` resta usato solo per casi storici e per articoli che (eccezionalmente) hanno una foto utente custom come `image:` — sconsigliato. La cover tipografica generata da `auto-cover-mancanti.py` non popola `image_credit` (la cover è opera nostra).

Esempio frontmatter completo:
```yaml
image: "/images/2026-11-23-irpinia-1980.webp"
image_alt: "ShakeMap del terremoto dell'Irpinia 1980"
image_credit: "USGS — Public domain — via Wikimedia Commons"
image_source_url: "https://commons.wikimedia.org/wiki/File:USGS_..."
```

Compatibilità retroattiva: gli articoli pre-esistenti senza `image_credit` continuano a funzionare normalmente (il `<figcaption>` non viene reso).

## Articoli prev/next + correlati (partials)

Due partial standardizzati che `_default/single.html` chiama automaticamente per ogni articolo della sezione `/comunicazioni/`:

1. **`partials/articolo-navigazione.html`** — riga «Articolo più recente / Articolo precedente» basata su `.PrevInSection` / `.NextInSection`. Niente parametri: si attiva su qualsiasi pagina `.IsPage` con un `.Section` >= 2 articoli. Riusabile su nuove sezioni archivio future.

2. **`partials/articoli-correlati.html`** — sezione «Leggi anche» con card di articoli con stesso `badge` dell'articolo corrente, ordinate per data decrescente. Esclude l'articolo corrente. Mostra immagine cover + data + titolo + descrizione.

CSS in `custom.css` (sezioni "ARTICOLO PREV/NEXT v1.0" e "ARTICOLI CORRELATI v1.0"):
- Hover lift `translateY(-2px)`, ombra blu istituzionale
- Focus visibile `outline: 3px solid #ffbe2e` (WCAG 2.4.7)
- Nascosti in stampa via `@media print`

Quando aggiungi una nuova sezione paginata (es. `/news-tecniche/`), nel suo `single.html` (o aggiornando la condizione in `_default/single.html`) basta chiamare i 2 partial — funzionano automaticamente.

## Assistente guidato (`/assistente/`)

Pagina interattiva che guida il cittadino con domande semplici fino a una risposta di autoprotezione. È un **albero decisionale deterministico in JavaScript puro** (nessun LLM, nessuna API runtime), coerente con il vincolo di sito statico Hugo e con la responsabilità istituzionale di non dare indicazioni generate in emergenza.

- **Contenuto**: `content/assistente/_index.md` (solo frontmatter — `type: "assistente"`, `layout: "list"`).
- **Logica e dati**: `themes/flavour-pcgenzano/layouts/assistente/list.html`. Oggetto `NODES` con percorsi (terremoto, incendio, gas, allerta meteo, allagamento, volontario, numeri utili, IT-alert) e circa 30 nodi totali. Struttura nodo: `{ kind: 'question'|'answer', title, prompt?, options?, body?, bullets?, emergency?, links? }`.
- **Compatibilità subpath**: i link interni usano `window.SITO_BASEURL` (iniettato via `{{ "" | relURL }}`) per essere compatibili sia con Aruba (root) sia con GitHub Pages (subpath `/sito-pc-genzano/`).
- **Accessibilità**: `aria-live="polite"` sul contenitore, focus management sul `<h2>` ad ogni render, navigazione tastiera nativa, banner rosso in cima con richiamo al 112, fallback `<noscript>` con link alle pagine istituzionali.
- **Deep link**: lo stato è riflesso in `location.hash` (es. `/assistente/#terremoto_casa`) per condividere una risposta.
- **Homepage**: card "Cosa devo fare?" in `data/quick_links.yaml` → `servizi[0]`.

**Per aggiungere un nuovo percorso**: aggiungere un nodo `question` collegato da `start.options`, poi le relative `answer` referenziate da `options[n].next`. Rispettare il criterio `emergency: true` solo per situazioni operative reali (coerenza con regola `06-protezione-civile-scientifica.md` sul tono di comunicazione del rischio). Ogni nodo `answer` può avere un `pittogramma` opzionale (es. `'arasaac/terremoto.png'`) renderizzato come `<figure>` accessibile sopra il corpo della risposta.

## Partial `structured-data` (JSON-LD Schema.org)

`themes/flavour-pcgenzano/layouts/partials/structured-data.html` inietta il blocco `<script type="application/ld+json">` con i dati strutturati Schema.org per i motori di ricerca e gli assistenti vocali.

**Schema attivi:** Organization+NGO, ContactPoint, WebSite (con SearchAction), BreadcrumbList, Article (per `/comunicazioni/`), Event (aggiuntivo per `badge: Evento` con location Place + organizer), FAQPage (per `/faq/` **e** per qualunque pagina con frontmatter `faq_schema: true`, vedi sotto), HowTo (per pagine `/rischi-prevenzione/*` con frontmatter `howto_prima` / `howto_durante` / `howto_dopo` — vedi sotto), WebPage (default), Question/Answer, HowToStep, ImageObject, PostalAddress, GeoCoordinates, City.

**HowTo per pagine rischio — 8 pagine già coperte.** Da maggio 2026 le 8 pagine `/rischi-prevenzione/*` con struttura uniforme PRIMA/DURANTE/DOPO sono **tutte** coperte da markup `HowTo` (`rischio-sismico`, `rischio-idrogeologico`, `rischio-incendio`, `rischio-vulcanico`, `ondate-di-calore`, `blackout`, `vento-forte`, `temporali-intensi`). Il pattern è documentato qui per chi aggiungerà nuove pagine rischio in futuro. Il blocco HowTo si attiva aggiungendo nel frontmatter 3 campi stringa:

```yaml
howto_prima: "Riassunto in 1-3 frasi delle azioni preventive da fare prima dell'evento."
howto_durante: "Riassunto in 1-3 frasi delle azioni immediate da fare durante l'evento."
howto_dopo: "Riassunto in 1-3 frasi delle azioni di recupero da fare dopo l'evento."
```

Il partial controlla `if and .Params.howto_prima .Params.howto_durante .Params.howto_dopo` — il blocco HowTo viene emesso **solo** se tutti e tre i campi sono presenti. Pagine senza i campi continuano ad avere solo `WebPage` + `BreadcrumbList` (nessuna regressione).

**`totalTime`** calcolato come `ReadingTime × 1.5` minuti (lettura → applicazione pratica), minimo 5 minuti. **`url` di ciascun HowToStep** punta al frammento `#cosa-fare-prima` / `#cosa-fare-durante` / `#cosa-fare-dopo` della pagina, ancore presenti su tutte le pagine rischio per la struttura uniforme già documentata in `rule 06-protezione-civile-scientifica.md`.

⚠️ **Sintassi obbligatoria `| jsonify | safeJS`** per ogni campo testuale dentro `<script type="application/ld+json">`. Hugo applica un **secondo escape JS contestuale** alle stringhe dentro `<script>`, e il solo `| jsonify` produce doppio escape (es. `name: "\"Foo\""`). Aggiungere `| safeJS` dopo `| jsonify` impedisce il secondo escape e produce JSON valido. Vale anche per gli apostrofi italiani (es. "L'unica difesa"). Testato con `validator.schema.org` post-fix del 12 maggio 2026.

**FAQPage opt-in dagli accordion (oltre a `/faq/`).** Le pagine con FAQ in accordion `<details class="faq-item">` possono esporre lo schema **FAQPage** aggiungendo `faq_schema: true` nel frontmatter: il partial estrae con `findRESubmatch` la domanda (`<summary>`) e la risposta da ogni accordion e genera il JSON-LD (`| plainify | htmlUnescape | jsonify | safeJS`). È **opt-in** apposta, per non marcare come FAQ gli accordion usati per altri contenuti (es. moduli corso in `/formazione/percorsi-didattici/`). Attivo su `/allerte-meteo/` e `/area-volontari/`; la `/faq/` mantiene la sua lista FAQPage curata a mano.

**Importante — vincolo di tipo Organization:** l'Organization è marcata come `["Organization", "NGO"]`, **NON** `GovernmentOrganization` né `EmergencyService`. Il Gruppo è associazione di volontariato OdV, non ente pubblico né servizio di emergenza chiamabile direttamente — usare quei tipi indurrebbe Google/assistenti vocali a presentare il Gruppo come servizio chiamabile, contraddicendo la regola "in emergenza chiama il 112".

**Quando estendi gli schema**: prudenza su tipi che inducano confusione tra associazione di volontariato e ente pubblico/servizio di emergenza. Verifica con [Google Rich Results Test](https://search.google.com/test/rich-results) e [Schema.org validator](https://validator.schema.org/).

## Partial `meta-social` (Open Graph + Twitter Card)

Tutti i meta tag che controllano l'**anteprima** dei link quando vengono condivisi su WhatsApp, Telegram, Facebook, X, LinkedIn, Slack, ecc. sono in `themes/flavour-pcgenzano/layouts/partials/meta-social.html` (chiamato da `baseof.html`). Include:

- **Open Graph base**: `og:title`, `og:description`, `og:type` (`article` per `.IsPage`, `website` per liste e pagine), `og:url`, `og:locale=it_IT`, `og:site_name`.
- **Open Graph image avanzato**: `og:image`, `og:image:secure_url`, `og:image:type` (calcolato da estensione: `.webp`/`.png`/`.svg`/`.gif`/default `.jpg`), `og:image:width=1200`, `og:image:height=630`, `og:image:alt` (da `image_alt` o titolo).
- **Article-specific** (solo `.IsPage`): `article:published_time` (ISO 8601), `article:modified_time`, `article:author`, `article:section` (dal badge), `article:tag` (range sui tags).
- **Twitter Card**: `twitter:card=summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt`. Opzionale `twitter:site` se in `[params] twitterSite = "@..."` di `hugo.toml`.

Default per pagine senza copertina: `static/images/og-default.png` 1200×630 nel tema.

**Cache delle anteprime**: le piattaforme social cachano le anteprime (Facebook/X possono cachare per ore o giorni). Se modifichi la copertina di un articolo, l'anteprima si aggiorna **solo dopo che la piattaforma ricontrolla**. Per forzare il refresh: [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) e [Twitter Card Validator](https://cards-dev.twitter.com/validator).

## Partial della roadmap (maggio 2026)

Partial aggiunti con le iniziative della roadmap. Tutti auto-protettivi (renderizzano solo quando hanno senso) e inclusi dai template `_default`.

- **`qr-articolo.html`** (idea #6) — bottone "Scarica QR" + `<dialog>` con il QR dell'articolo. Si attiva solo se esiste `static/qr/<slug>.png|svg` (generati da `scripts/genera-qr-articoli.py`). Incluso in `page-tools.html`. CSS § QR ARTICOLO v1.0.
- **`ricerca-modal.html`** (idea #24) — modal di ricerca full-text Pagefind, apertura da icona navbar e da `Ctrl+K`. `pagefind-ui` caricato in lazy alla prima apertura. Incluso in `baseof.html`. Indice in `static/pagefind/` generato da `scripts/genera-indice-ricerca.sh`. CSS § RICERCA PAGEFIND v1.0. La pagina `/cerca/` (`layouts/cerca/list.html`) usa lo stesso motore.
- **`lis-badge.html`** (idea #10) — badge "Disponibile in LIS" sulle pagine del sito. **Due modalità** (v2.0, maggio 2026):
  - **Modalità preferita: `lis_section: "<famiglia>"`** nel frontmatter → mostra badge *"N video LIS disponibili"* che linka a `/lis/#<famiglia>` (anchor della sezione corrispondente sull'hub). Funziona con il registro `data/lis.yaml` v2.0 che cataloga 59 video LIS dei canali "Io non rischio" (DPC) e "Abili a Proteggere" (Cooperativa Europe Consulting) suddivisi in 10 famiglie tematiche. Privacy-first: niente embed YouTube, ogni video apre il canale del produttore in nuova scheda. Incluso in `_default/single.html`, `_default/list.html` e `rischi-prevenzione/single.html`. Famiglie attive: `rischio-sismico`, `rischio-vulcanico`, `rischio-idrogeologico`, `rischio-incendio`, `maremoto`, `allerte-meteo`, `gestione-emergenza`, `pianificazione`, `aree-emergenza`, `kit-emergenza`. Pagine target: `/rischi-prevenzione/rischio-{sismico,vulcanico,idrogeologico,incendio}/`, `/rischi-prevenzione/kit-emergenza/`, `/allerte-meteo/`, `/piano-emergenza/`, `/cartografia/`.
  - **Modalità legacy: `lis_video: "<id>"`** → dialog popup con video self-hosted o link YouTube + trascrizione. Mantenuta per retrocompatibilità con eventuali video futuri prodotti in proprio. CSS § LIS v2.0.
  - **Aggiornamento periodico**: workflow `.github/workflows/check-video-lis.yml` (cron settimanale lunedì 11:23 UTC) gira `scripts/check-nuovi-video-lis.py` che confronta i feed RSS/HTML dei 2 canali con `data/lis.yaml` e apre issue automatica se trova nuovi video LIS da integrare, con suggerimento famiglia tematica.

Layout di pagina aggiunti dalla roadmap (non partial, ma `layouts/<sezione>/`): `stato-sistema/list.html` (#25), `storia/list.html` (#8), `lis/list.html` (#10), `lanterna/list.html` (#4, standalone — NON usa `baseof.html`), `quiz-preparazione/list.html` (#7), `podcast/{list,single,rss.xml}` (#22), `articoli-da-ascoltare/list.html` (#22, ex `podcast/`), `allerta-stato/list.json` (#2, endpoint JSON puro).

Script asset associati: `genera-qr-articoli.py`, `genera-indice-ricerca.sh`, `backup-documenti-aruba.py`. JS statici: `notifiche-allerta.js` (#2), `glossario-pagina.js` (#21), `quiz-preparazione.js` (#7), `static/giochi/assets/js/arena.js` (#11).

## Dossier interattivi — sezione `/dossier/` + 9 shortcode `dossier-*`

I **dossier interattivi** (`content/dossier/`, URL `/dossier/`) sono racconti visivi *scrollytelling* a tema scuro "spazio", **full-bleed** e accessibili (WCAG 2.2 AA). Sono un **"motore" riusabile**: l'impianto è scritto una volta, **ogni nuovo dossier è un singolo file Markdown** in `content/dossier/<slug>.md`. Guida operativa completa: `manuale/parte-39-dossier-interattivi.md`.

**Architettura:** layout `layouts/dossier/single.html` (definisce `main`, carica `static/css/dossier.css`, rende barra di avanzamento + pallini dai `sezioni` del frontmatter + `{{ .Content }}` + sezione condivisione, poi `static/js/dossier.js`); landing `layouts/dossier/list.html` (griglia card, CSS `static/css/dossier-list.css`); box homepage `partials/dossier-home.html` (dossier più recente, CSS `static/css/dossier-home.css`, inserito in `index.html` modalità normale fra `cruscotto-home` e `services`). Il full-bleed si ottiene con `main:has(> .dossier){padding:0}` in `dossier.css`.

**I 9 shortcode** (`layouts/shortcodes/dossier-*.html`):

- `dossier-hero` — apertura a tutto schermo (`id`, `image`, `alt`, `eyebrow`, `title` con `<br>`, `sub`, `credito`).
- `dossier-scena` — sezione con sfondo immagine + pannello in vetro; `align="left|right|top"` (con `top` immagine grande centrata); `id`/`image`/`alt`/`kicker`/`title`/`credito` + corpo Markdown. Il pannello ha classe `reveal` (comparsa al viewport).
- `dossier-dati` + `dossier-dato` — numeri che si animano (count-up). `dossier-dato`: `to`/`unita`/`label`, oppure `da="ANNO"` per anni **dinamici** (`{{ sub now.Year (int ...) }}`) — evita dati che invecchiano.
- `dossier-confronto` — slider prima/dopo (due immagini, cursore trascinabile, tastiera): `titolo`/`testo`/`base`/`baseAlt`/`baseLab`/`top`/`topAlt`/`topLab`/`ratio`/`cap`.
- `dossier-hotspot` + `dossier-punto` — immagine grande con punti cliccabili (popover). `dossier-punto`: `x`/`y` (% sull'immagine) + `titolo` + corpo Markdown. I popover si **capovolgono** da soli (alto/basso/sinistra/destra, logica in `dossier.js`) per non uscire dallo schermo; i punti compaiono "a cascata" quando l'immagine entra (`.dossier-hotspot.is-revealed`).
- `dossier-chiusura` — finale con titolo + testo + fino a 2 CTA (`cta1`/`cta1url`, `cta2`/`cta2url`).
- `dossier-fonti` — crediti/fonti (Markdown).

🔴 **Subpath GitHub Pages:** ogni immagine passa per `strings.TrimPrefix "/" | relURL` (vale per gli shortcode, per `dossier-home.html` e per `dossier/list.html`). Non usare `relURL` su path con leading slash: romperebbe su GitHub Pages.

🔴 **Animazioni:** sono molte (Ken Burns, parallasse, ingresso direzionale dei pannelli, cascata dei punti hotspot, cielo stellato + nebulosa dietro le sezioni scure, stelle cadenti, anelli orbitanti, riflesso sui numeri, micro-interazioni). **Tutte** disattivate da `@media (prefers-reduced-motion: reduce)` **e** da `html.a11y-pause-anim` (toggle "Pausa animazioni" del toolbar). Il dossier resta leggibile e usabile senza animazioni (popover da tastiera Invio/Spazio/Esc, slider `input[type=range]` nativo). Sezioni CSS: `dossier.css` v1.0→v1.3.

🔴 **Immagini:** solo con **licenza chiara** (NASA pubblico dominio, Copernicus/ESA CC BY, autori con CC) e **credito onesto** in `credito`/`cap`/`fonti`. Mai attribuire un'immagine al satellite sbagliato né spacciarla per un'altra. Asset in `static/images/dossier/` (WebP).

**Frontmatter di un dossier:** `type: "dossier"`, `title`, `description`, `image` (cover per social/landing), `tts: false`, `indice: false`, `sezioni: [{ id, label }, ...]` (un punto per `id` di sezione, per la navigazione a pallini). **Menu:** voce "Dossier interattivi" → `/dossier/` sotto **Risorse** in `hugo.toml` **e** `static/app-shared/site-chrome.js` (tenere sincronizzati).
