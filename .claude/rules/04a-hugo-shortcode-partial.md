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

**Libreria disponibile** (171 simboli, 3.3 MB):
- `static/pittogrammi/iso7010/*.svg` — 46 segnali standard (E* evacuazione, F* antincendio, W* avvertimento, M* obbligo, P* divieto). Vettoriali, scalabili senza perdita.
- `static/pittogrammi/arasaac/*.png` — 125 simboli (eventi/rischi, azioni autoprotezione, oggetti kit emergenza, persone, luoghi, segnali, veicoli, numeri utili). Bitmap 500px.

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

- **Link interno `/...` che termina con estensione di file statico** (`.pdf`, `.webp`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.zip`, `.mp3`, `.mp4`, `.csv`, `.txt`, `.rtf`, `.html`, `.htm`): reso come `<a>` diretto. Serve per linkare file in `static/manuali/`, `static/allegati/`, `static/images/` e micro-siti HTML autonomi in `static/quizpc/`, `static/formazionepc/`, `static/giochi/` senza che il controllo `site.GetPage` li marchi come "non disponibili".
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

**Quando viene popolato `image_credit`**: il workflow `scarica-foto-automatica.yml` lo popola automaticamente per gli articoli con marker `# TODO-foto-wikipedia` (e analoghi NASA/USGS). Per articoli con foto utente o foto evento personali, il campo si compila manualmente nel frontmatter.

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

2. **`partials/articoli-correlati.html`** — sezione «Leggi anche» con 3 card di articoli con stesso `badge` dell'articolo corrente, ordinate per data decrescente. Esclude l'articolo corrente. Mostra immagine cover + data + titolo + descrizione.

CSS in `custom.css` (sezioni "ARTICOLO PREV/NEXT v1.0" e "ARTICOLI CORRELATI v1.0"):
- Hover lift `translateY(-2px)`, ombra blu istituzionale
- Focus visibile `outline: 3px solid #ffbe2e` (WCAG 2.4.7)
- Nascosti in stampa via `@media print`

Quando aggiungi una nuova sezione paginata (es. `/news-tecniche/`), nel suo `single.html` (o aggiornando la condizione in `_default/single.html`) basta chiamare i 2 partial — funzionano automaticamente.

## Assistente guidato (`/assistente/`)

Pagina interattiva che guida il cittadino con domande semplici fino a una risposta di autoprotezione. È un **albero decisionale deterministico in JavaScript puro** (nessun LLM, nessuna API runtime), coerente con il vincolo di sito statico Hugo e con la responsabilità istituzionale di non dare indicazioni generate in emergenza.

- **Contenuto**: `content/assistente/_index.md` (solo frontmatter — `type: "assistente"`, `layout: "list"`).
- **Logica e dati**: `themes/flavour-pcgenzano/layouts/assistente/list.html`. Oggetto `NODES` con 8 percorsi (terremoto, incendio, gas, allerta meteo, allagamento, volontario, numeri utili, IT-alert) e circa 30 nodi totali. Struttura nodo: `{ kind: 'question'|'answer', title, prompt?, options?, body?, bullets?, emergency?, links? }`.
- **Compatibilità subpath**: i link interni usano `window.SITO_BASEURL` (iniettato via `{{ "" | relURL }}`) per essere compatibili sia con Aruba (root) sia con GitHub Pages (subpath `/sito-pc-genzano/`).
- **Accessibilità**: `aria-live="polite"` sul contenitore, focus management sul `<h2>` ad ogni render, navigazione tastiera nativa, banner rosso in cima con richiamo al 112, fallback `<noscript>` con link alle pagine istituzionali.
- **Deep link**: lo stato è riflesso in `location.hash` (es. `/assistente/#terremoto_casa`) per condividere una risposta.
- **Homepage**: card "Cosa devo fare?" in `data/quick_links.yaml` → `servizi[0]`.

**Per aggiungere un nuovo percorso**: aggiungere un nodo `question` collegato da `start.options`, poi le relative `answer` referenziate da `options[n].next`. Rispettare il criterio `emergency: true` solo per situazioni operative reali (coerenza con regola `06-protezione-civile-scientifica.md` sul tono di comunicazione del rischio). Ogni nodo `answer` può avere un `pittogramma` opzionale (es. `'arasaac/terremoto.png'`) renderizzato come `<figure>` accessibile sopra il corpo della risposta.

## Partial `structured-data` (JSON-LD Schema.org)

`themes/flavour-pcgenzano/layouts/partials/structured-data.html` inietta il blocco `<script type="application/ld+json">` con i dati strutturati Schema.org per i motori di ricerca e gli assistenti vocali.

**Schema attivi:** Organization+NGO, ContactPoint, WebSite (con SearchAction), BreadcrumbList, Article (per `/comunicazioni/`), Event (aggiuntivo per `badge: Evento` con location Place + organizer), FAQPage (per `/faq/`), WebPage (default), Question/Answer, ImageObject, PostalAddress, GeoCoordinates, City.

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
