# Hugo Architecture

## Struttura del progetto

```
sito-pc-genzano/
├── content/
│   ├── comunicazioni/       # Articoli/news (archetype: comunicazioni.md)
│   │   └── AAAA-MM-GG-titolo.md
│   └── [sezioni statiche]/  # Pagine statiche (accessibilita, allerte-meteo,
│                            # area-download, cartografia, cerca, chi-siamo,
│                            # contatti, cosa-fare-adesso, diventa-volontario,
│                            # faq, formazione, note-legali, numeri-utili,
│                            # piano-emergenza, piano-familiare, privacy,
│                            # rischi-prevenzione, siti-utili, social-media-policy)
│                            # con _index.md
├── data/
│   ├── emergenza.json       # Modalità emergenza on/off
│   ├── allerta.json         # Livello allerta meteo (verde/giallo/arancione/rosso)
│   ├── risk_cards.yaml      # Card rischi e prevenzione
│   ├── numeri_utili.yaml    # Numeri di emergenza
│   ├── quick_links.yaml     # CTA homepage hero
│   ├── social_links.yaml    # Link social
│   └── codici_colore.yaml   # Descrizioni codici colore allerte
├── themes/flavour-pcgenzano/
│   ├── layouts/
│   │   ├── index.html       # Homepage (dual-mode: normale / emergenza)
│   │   ├── 404.html         # Pagina errore 404
│   │   ├── _default/        # baseof.html, list.html, single.html
│   │   ├── partials/        # navbar, footer, emergency-banner, allerta-card,
│   │   │                    # cookie-banner, breadcrumb, page-tools,
│   │   │                    # accessibility-toolbar.html (FAB strumenti a11y), ecc.
│   │   ├── shortcodes/      # foto.html (click-per-ingrandire accessibile)
│   │   │                    # pittogramma.html (ISO 7010 + ARASAAC)
│   │   ├── comunicazioni/   # list.html con filtri per badge
│   │   └── cerca/           # list.html con motore di ricerca JS
│   └── static/
│       ├── css/custom.css   # Override CSS su Bootstrap Italia + regole
│       │                    # @media print globali (stampa solo l'articolo)
│       ├── css/a11y-toolbar.css  # Stili FAB + dialog Strumenti di Accessibilità
│       │                         # + classi html.a11y-* per le preferenze utente
│       ├── js/a11y-toolbar.js    # Logica del toolbar di accessibilità
│       │                         # (apri/chiudi, focus trap, persistenza
│       │                         # localStorage, applicazione classi su <html>)
│       └── images/          # Asset statici
├── archetypes/
│   ├── comunicazioni.md     # Archetype completo per news
│   └── default.md           # Archetype minimale
├── scripts/
│   ├── genera-cover.py              # Genera copertine tipografiche automatiche
│   ├── aggiorna-image-frontmatter.py # Aggiorna il campo image negli articoli
│   ├── applica-fascia-foto.sh       # Applica fascia blu istituzionale a una
│   │                                # foto sorgente fornita dall'utente e la
│   │                                # converte in WebP 1200px pronta per l'uso
│   │                                # via shortcode {{< foto >}}
│   ├── scarica-pittogrammi.sh       # Scarica/aggiorna libreria pittogrammi
│   │                                # ISO 7010 (Wikimedia) + ARASAAC.
│   │                                # Output: static/pittogrammi/...
│   ├── auto-cover-mancanti.py       # Genera cover tipografiche per articoli
│   │                                # con image:"" e senza marker TODO-foto-*
│   │                                # (sicuro: mai sovrascrive foto utente).
│   │                                # Chiama genera-cover.py + aggiorna
│   │                                # frontmatter solo se vuoto.
│   ├── proponi-marker-foto.py       # Scansiona articoli con image:"" e
│   │                                # propone marker TODO-foto-wikipedia da
│   │                                # incollare manualmente. Output testuale
│   │                                # o CSV. Sicuro: non modifica file.
│   └── export-contesto-ai.sh        # Export di tutta la documentazione in
│                                    # un unico CONTESTO-AI.md per altra AI
├── .claude/rules/           # Regole di governance (questo file)
└── CLAUDE.md                # Istruzioni per Claude Code
```

## Regole Hugo fondamentali

- Non proporre soluzioni pensate per CMS tradizionali: Hugo genera HTML statico.
- Ogni modifica deve rispettare la logica nativa di Hugo (template lookup order, data cascade, archetypes).
- Non rompere il build di Hugo: testa mentalmente ogni modifica prima di proporla.
- Se una modifica può essere fatta a livello di partial o template comune, preferisci quella strada rispetto a duplicare codice.
- Evita logica complessa nei template: usa data files o front matter per i contenuti variabili.

## Regole specifiche per questo progetto

### Homepage dual-mode
La homepage ha due layout distinti controllati da `data/emergenza.json`:
- `"attiva": false` → layout normale (hero → servizi → news → card rischi → link rapidi)
- `"attiva": true` → layout emergenza (banner emergenza + azioni → hero compatto → news)

Non modificare questa logica senza valutare l'impatto su entrambe le modalità.

### Contenuti dinamici via data files
I file in `data/` sono la via principale per aggiornare contenuti senza toccare i template.
Aggiorna i data files al posto di modificare i template quando possibile.

### Articoli (comunicazioni/)
- Usa sempre l'archetype: `hugo new comunicazioni/AAAA-MM-GG-titolo.md`
- Il frontmatter deve essere completo (vedi regola 02-content-design-pa.md)
- Il formato data nel frontmatter è SEMPRE `AAAA-MM-GG`, MAI con timezone
- `draft: true` esclude dalla build di produzione, visibile solo con `hugo server -D`

### Shortcode `foto` (immagini nel corpo degli articoli)
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

### Shortcode `pittogramma` (simboli ISO 7010 e ARASAAC)

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

### Shortcode `cosa-non-fare` (box divieti per pagine rischio)

Box rosso bordato (`#c1121f`) con icona divieto che evidenzia visivamente i comportamenti DA EVITARE. Aumenta l'efficacia della comunicazione del rischio rispetto ai "non" dispersi nel testo. Usato sulle 7 pagine `/rischi-prevenzione/*`.

```go-html-template
{{< cosa-non-fare titolo="Cosa NON fare in caso di terremoto" >}}
- **Non correre fuori durante la scossa**
- **Non usare gli ascensori**
- **Non usare il telefono per curiosità**
{{< /cosa-non-fare >}}
```

Parametro `titolo` opzionale (default: "Cosa NON fare"). Contenuto Markdown standard. Output: `<div role="region" aria-label="...">` con header colorato + body in lista. Contrasto WCAG AA: testo `#7f1d1d` su `#fff5f5` = 7.7:1. CSS scoped sezione **COSA NON FARE v1.0** in `custom.css`. In stampa diventa nero su bianco mantenendo gerarchia visiva con `page-break-inside: avoid`.

### Shortcode `chi-chiamare` (chiusura standard pagine rischio)

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

### Render hook tabelle (`_markup/render-table.html`)

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

### FAQ accordion (`.faq-item` su `<details>`)

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

### Share buttons (`partials/page-tools.html` + `js/share.js`)

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

### Striscia pittogrammi (`.kit-pittogrammi-row`)

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

### Modal SOS-112 esteso (`partials/sos-112.html`)

Vedi `CLAUDE.md` sezione "Modal SOS-112" per la sintesi. Il modal di conferma chiamata 112 ha **3 azioni**: Annulla (focus iniziale, ENTER sicuro), "Cosa devo fare?" (link a `/assistente/`, bottone outline blu istituzionale), "Sì, chiama il 112" (bottone rosso primario, `<a href="tel:112">`).

Note operative:
- L'href dell'assistente passa per `{{ "assistente/" | relURL }}` per compatibilità Aruba/GitHub Pages.
- Il focus trap JS rileva tutti i `[href]` e bottoni: il nuovo `<a id="sos-modal-guide">` viene incluso automaticamente nel ciclo Tab/Shift+Tab.
- CSS scoped: `.sos-modal-btn-guide` (outline blu) + `.sos-modal-alt` (nota informativa azzurra prima dei bottoni). Sezione esistente del modal in `custom.css`.

Se un domani serve aggiungere una **quarta azione** (ipotesi: "Numeri utili"), aggiungere prima del bottone "Cosa devo fare?" — non distruggere l'ordine: sequenza visiva column-reverse su mobile (Call → Cosa fare → Annulla dall'alto al basso) e row su desktop (Annulla → Cosa fare → Call da sinistra a destra), che è la gerarchia di azione corretta.

### Shortcode `pagina-emergenza-lite`

Contiene tutto il rendering della pagina `/emergenza/` (pagina ultra-leggera per banda debole). Usa `data/allerta.json` e `data/emergenza.json` letti al build. Zero widget esterni, CSS inline minimale (~3KB), niente Bootstrap né JS aggiuntivo. Usato solo dalla pagina `content/emergenza/_index.md`. Aliases pagina: `/lite/`, `/emergenza-essenziale/`. Linkata dal footer di tutte le pagine.

### Partial `leggi-ad-alta-voce` (TTS Web Speech API)

Vedi regola `03-accessibility.md` sezione TTS per dettagli. Sintesi: opt-in via frontmatter `tts: true`, attivo su 12 pagine essenziali, voce italiana di default, fallback graceful, accessibile da tastiera. Componente in `partials/leggi-ad-alta-voce.html`, CSS in `custom.css` sezione **TTS v1.0**.

### Partial `article-cover` (copertina con didascalia credit)

Vedi sezione "Copertina articolo con didascalia di credit" più sotto. Sintesi: gestisce `<figure>` + `<img>` + `<figcaption>` con `image_credit` e `image_source_url` quando presenti nel frontmatter (popolati dal workflow `scarica-foto-automatica.yml` per articoli con marker `# TODO-foto-*`).

### Menu di navigazione principale (mega-menu accorpato)

Il menu è definito in `hugo.toml` sotto `[[menus.main]]` e renderizzato in `themes/flavour-pcgenzano/layouts/partials/navbar.html`. Struttura a **7 voci di primo livello**, di cui 4 dropdown:

| Voce | Tipo | Contenuto |
|---|---|---|
| Home | diretta | `/` |
| Per il Cittadino ▾ | dropdown | Cosa Fare Adesso, Allerte Meteo, Rischi e Prevenzione, Cartografia, Numeri Utili, Piano Familiare |
| Educazione e Inclusione ▾ | dropdown | Kit per le scuole, Schede Stampabili, Giochi della Sicurezza, **Abili a Proteggere**, **Facile da Leggere**, Glossario |
| Volontariato ▾ | dropdown | Diventa Volontario, Chi Siamo |
| Risorse ▾ | dropdown | FAQ, Strumenti in Tempo Reale, Area Download, Normativa, Mappa del Sito |
| Comunicazioni | diretta | `/comunicazioni/` |
| Contatti | diretta | `/contatti/` |

Razionale: 10 voci flat erano troppe per mobile e per l'utente in emergenza. L'accorpamento mantiene tutte le pagine raggiungibili in ≤ 2 click ma riduce il rumore visivo.

**Storia del riordino (aprile 2026):** dopo audit di usabilità, la prima versione "6 voci con Formazione" lasciava 4 buchi gravi:
- `/abili-a-proteggere/` e `/facile-da-leggere/` raggiungibili solo in 3+ click — paradosso, visto che servono a chi ha più difficoltà;
- `/strumenti/`, `/area-download/`, `/normativa/`, `/faq/` visibili solo in homepage o footer, perse da chi entra dal motore di ricerca.

Il dropdown "Formazione" è stato rinominato **"Educazione e Inclusione"** e ha accolto le 2 pagine accessibili. È stato aggiunto un nuovo dropdown **"Risorse"** per le 5 pagine di servizio. Il numero totale di voci di primo livello è salito da 6 a 7, ancora dentro il limite Miller 7±2.

**Convenzioni TOML per i dropdown:**
- Il "padre" ha solo `name`, `identifier` e `weight` (nessun `url`).
- I "figli" hanno `parent = "<identifier-del-padre>"` e `weight` per l'ordine.

```toml
[[menus.main]]
  name = "Per il Cittadino"
  identifier = "per-il-cittadino"
  weight = 2

[[menus.main]]
  name = "Cosa Fare Adesso"
  url = "/cosa-fare-adesso/"
  parent = "per-il-cittadino"
  weight = 1
```

**Render nel template:** la `partials/navbar.html` itera su `.Site.Menus.main`. Per ogni voce con `.HasChildren` produce il pattern Bootstrap Italia `nav-item dropdown` con `dropdown-toggle` + `dropdown-menu` contenente `link-list`. Il dropdown è marcato `.active` se uno qualsiasi dei figli è la pagina corrente (controllo via `IsMenuCurrent` / `HasMenuCurrent`).

**Aggiungere/spostare una voce:**
1. Modifica `[[menus.main]]` in `hugo.toml`.
2. Decidi se è di primo livello (rara: solo se è un'azione fondamentale) o sotto un dropdown esistente.
3. Niente modifiche al template: rendering automatico.
4. Verifica con `hugo --quiet --minify` che la build resti pulita.

Non aggiungere voci di primo livello senza valutarne l'impatto sul mobile: il limite di sicurezza è 6-7 voci visibili contemporaneamente.

### Indice della pagina (TOC) per articoli lunghi

Le pagine con frontmatter `toc: true` mostrano in cima un **indice cliccabile** (Table of Contents) generato automaticamente da Hugo a partire dalle intestazioni H2/H3 del Markdown. Si applica solo a pagine che usano `_default/single.html` (Hugo richiede `layout: "single"` nel frontmatter, già usato dai kit didattici).

Pagine attualmente con TOC attivo: `/formazione/`, `/formazione/kit-scuola-infanzia/`, `/formazione/kit-scuola-primaria/`, `/formazione/kit-scuola-secondaria-primo-grado/`, `/formazione/kit-scuola-secondaria-secondo-grado/`. Sono pagine da 500-950 righe con 15-20 sezioni: navigarle senza un indice è proibitivo.

**Cosa rende:** un `<details open>` Bootstrap-Italia-flavoured con icona elenco, titolo "In questa pagina", chevron animato e una griglia `auto-fill minmax(260px, 1fr)` che su desktop dispone le voci in 2-3 colonne, su mobile (≤768px) in colonna singola. La sezione è dentro un wrapper `<div id="indice">` per consentire il salto diretto.

**Back-to-top contestuale:** il bottone `#backToTop` in `baseof.html` rileva la presenza di `#indice` con `getElementById`. Se presente, lo scroll punta lì invece che a `scrollY=0`, e l'`aria-label` diventa "Torna all'indice della pagina". Backward compatible: senza TOC, comportamento standard.

**Quando attivare `toc: true`:**
- Pagina con almeno 8-10 H2 OPPURE
- Pagina molto lunga (>500 righe Markdown) anche con meno H2

**Regole operative:**
- Non duplicare l'indice nel corpo Markdown.
- Mantenere intestazioni H2 chiare e brevi: appariranno come voci di indice.
- L'indice è nascosto in stampa (`@media print { .article-toc { display: none } }`).
- Non serve aggiungere ID manuali: Hugo li genera dallo slug del titolo.

### Copertina articolo con didascalia di credit (`partials/article-cover.html`)

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

### Pagine legali/istituzionali con data di revisione
Le pagine `privacy`, `note-legali`, `accessibilita`, `social-media-policy` usano il campo frontmatter `dataUltimaRevisione: "AAAA-MM-GG"`.

Il template `_default/single.html` mostra questa data in un box evidente (`alert alert-light`) in cima al contenuto, subito dopo il titolo, con il testo "Pagina rivista il …".

Il partial `partials/page-tools.html` verifica la presenza del campo: se è impostato, omette la `.Lastmod` automatica per evitare due date sulla stessa pagina. Questo garantisce che ci sia un'unica fonte di verità per la data di revisione delle pagine legali, sotto il controllo editoriale esplicito del redattore (non automatica da git).

Non usare date di revisione hard-coded nel corpo (tipo "Ultimo aggiornamento: Marzo 2026"): la data è unica e vive nel frontmatter.

### Regole stampa
Il file `themes/flavour-pcgenzano/static/css/custom.css` contiene un blocco `@media print` globale che nasconde tutto il chrome del sito (header, navbar, footer, banner, cookie, utility bar, page tools, breadcrumb) e stampa solo il contenuto della pagina su formato A4 con margini standard. Esiste anche un blocco specifico per il piano familiare stampabile (`body.piano-printing`). Non duplicare queste regole; se servono modifiche, lavora sui blocchi esistenti.

### Tipografia del corpo articolo (`.article-body` v7.2)
Il template `themes/flavour-pcgenzano/layouts/_default/single.html` avvolge il contenuto in `<article class="article-body">`. Il blocco CSS **v7.2** in `themes/flavour-pcgenzano/static/css/custom.css` applica a questo wrapper una tipografia istituzionale curata scoped — non influisce su homepage, liste, card o widget.

Cosa applica:
- Base `font-size: 1.05rem`, `line-height: 1.75`, colore testo `#1a1a1a`.
- **Lede** (primo paragrafo): `1.15rem`, colore `#003366`, peso 500.
- **Capolettera** sulla prima lettera del primo paragrafo: `3rem`, blu, float left.
- **`<h2>`**: barra blu `3px` a sinistra, `margin-top: 2.5rem`, colore `#003366`.
- **`<h3>` / `<h4>`**: colore `#003366`, peso 600, spaziatura ridotta.
- **`<ul>` / `<ol>`**: `::marker` blu, spaziatura voci `0.4rem`.
- **`<blockquote>`**: bordo sinistro blu `4px`, sfondo `#f4f7fb`, corsivo.
- **`<figure>`** (shortcode `foto`): max-width `640px`, ombra morbida, cornice sottile; `<figcaption>` in corsivo blu centrato.
- **`<a>` non `.btn`**: underline `1px` → `2px` al hover/focus.
- **`<table>`**: header blu `#003366`, zebra leggera `#f8f9fb`.
- **`<hr>`**: sfumatura orizzontale blu (decorativa).
- **`<code>`** inline: sfondo `#f4f7fb`, colore blu.

Override integrati:
- `@media (max-width: 768px)`: riduce capolettera, spaziature H2 e dimensione lede.
- `@media (prefers-reduced-motion: reduce)`: disattiva transizioni sui link.
- `@media print`: azzera capolettera, ombre, gradienti e sfondi; mantiene gerarchia in bianco e nero.

Regole operative:
- La tipografia si applica automaticamente a qualsiasi articolo in `content/comunicazioni/` e a ogni pagina che usa `_default/single.html`.
- Non introdurre stili inline nel Markdown (`<span style="color:...">`): il tema li sovrascriverebbe.
- Non usare `<h1>` nel corpo: il titolo pagina è già `<h1>`, il corpo parte da `<h2>`.
- Il primo paragrafo deve avere senso compiuto (min. 2 frasi) per sfruttare lede + capolettera.
- Se serve modificare la tipografia, lavora sul blocco v7.2 esistente in `custom.css` — non duplicare.
- Dettagli e tabella completa in `MANUALE-SITO.md` Parte 3.15.

### Render-link hook (link Markdown nel corpo)
Il tema personalizza il rendering dei link Markdown tramite `layouts/_default/_markup/render-link.html` (copia speculare in `themes/flavour-pcgenzano/layouts/_default/_markup/render-link.html`). Comportamento:

- **Link interno `/...` che termina con estensione di file statico** (`.pdf`, `.webp`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.zip`, `.mp3`, `.mp4`, `.csv`, `.txt`, `.rtf`, `.html`, `.htm`): reso come `<a>` diretto. Serve per linkare file in `static/manuali/`, `static/allegati/`, `static/images/` e micro-siti HTML autonomi in `static/quizpc/`, `static/formazionepc/`, `static/giochi/` senza che il controllo `site.GetPage` li marchi come "non disponibili".
- **Link interno `/.../` (path che termina con `/`) verso cartella con `static/<path>/index.html`**: il hook fa `fileExists "static/<path>/index.html"` e se esiste lo tratta come statico. Serve per scrivere `[Giochi](/giochi/)` senza dover specificare `/index.html`.
- **Link interno `/...` verso pagina Hugo esistente**: `<a>` normale.
- **Link interno `/...` verso pagina non trovata** (e non file statico): `<span class="text-muted" title="Contenuto non ancora disponibile">` — consente di linkare articoli non ancora pubblicati che si attiveranno automaticamente al deploy successivo.
- **Link esterno `http(s)://`**: `<a target="_blank" rel="noopener noreferrer">`.
- **`mailto:` / `tel:`**: `<a>` con `safeURL`.

**Subpath GitHub Pages e `relURL`**: il hook strippa il leading `/` dal link prima di passarlo a `relURL`. Hugo `relURL` **non** aggiunge il subpath del baseURL ai path che iniziano con `/`: `relURL "/foo"` resta `/foo`, mentre `relURL "foo"` diventa `/sito-pc-genzano/foo`. Senza questo strip, tutti i link interni del markdown (che per convenzione scriviamo con leading `/`) funzionerebbero su Aruba (baseURL root) ma sarebbero rotti su GitHub Pages (baseURL con subpath `/sito-pc-genzano/`). Se modifichi il hook, mantieni la riga `$relLink := strings.TrimPrefix "/" $link` e usa `$relLink | relURL` in tutti i branch interni.

Se estendi la lista di estensioni statiche o modifichi il comportamento di `relURL`, aggiorna **entrambi** i file `render-link.html` (progetto e tema) per mantenere la coerenza.

### Strumenti di Accessibilità (toolbar utente)

In ogni pagina del sito, in basso a sinistra, è presente un **bottone rotondo blu istituzionale** (FAB) con icona `bi-universal-access` che apre un **dialog modale** con preferenze di lettura: dimensione testo (4 livelli), allineamento, carattere ad alta leggibilità, spaziatura ampia, contrasto (default/alto/invertito), scala di grigi, nascondi immagini decorative, pausa animazioni, evidenzia link, cursore grande.

**File coinvolti** (tutti nel tema, modificabili liberamente):

- `themes/flavour-pcgenzano/layouts/partials/accessibility-toolbar.html` — markup del FAB + dialog (~150 righe).
- `themes/flavour-pcgenzano/static/css/a11y-toolbar.css` — stili del FAB + dialog + le classi `html.a11y-*` che applicano le preferenze al sito.
- `themes/flavour-pcgenzano/static/js/a11y-toolbar.js` — logica (apri/chiudi, focus trap, Esc, persistenza localStorage, sync UI ↔ stato).
- `themes/flavour-pcgenzano/layouts/_default/baseof.html` — include il partial e linka CSS+JS. Contiene anche un **inline early script** nel `<head>` che applica le preferenze salvate **prima del rendering**, evitando il flash visivo (FOUC) quando l'utente ha contrasto invertito o testo grande.

**Persistenza:** chiave `pcgenzano-a11y-prefs` in `localStorage`. Il bottone "Reimposta tutto" del dialog ripulisce stato e storage.

**Cosa va NON fatto:**

- Non sostituirlo con widget commerciali tipo AccessiBe / UserWay / Equally AI: il W3C-WAI e le associazioni delle persone con disabilità sconsigliano questi "overlay" che mascherano problemi di accessibilità invece di risolverli.
- Non rimuovere l'inline early script in `<head>`: senza quello, ogni ricarica produce un flash di testo non scalato o sfondo non invertito.
- Non spostare il FAB in basso a destra: c'è già il `back-to-top` (e su mobile anche il SOS-112), si crea sovrapposizione.
- Non aggiungere preferenze complesse "alla overlay" (modalità autismo, modalità ADHD, ecc.): sono pseudo-scientifiche. Se vuoi estendere, aggiungi solo controlli di **preferenza di lettura** misurabili (font, contrasto, spaziatura, animazioni).

**Cosa si può estendere senza problemi:**

- Aggiungere nuovi livelli di dimensione testo (oggi 100/110/125/150%).
- Aggiungere nuove palette di contrasto.
- Aggiungere link nel dialog verso risorse interne (es. Glossario, FAQ).

**Pagina pubblica correlata:** `content/accessibilita/_index.md` descrive il toolbar al cittadino e dà istruzioni complementari sugli strumenti di sistema (zoom OS, screen reader NVDA/VoiceOver/TalkBack, contrasto OS, riconoscimento vocale). Mantenere allineate le due descrizioni se modifichi le funzioni del toolbar.

### Cartelle `static/` canoniche per file depositati via git
Per evitare che nuovi file finiscano in cartelle escluse dal deploy FTP (vedi regola `05-github-aruba-deploy.md`), usa queste cartelle:

| Contenuto | Cartella | URL pubblico |
|---|---|---|
| Manuali tecnici permanenti citati da più articoli | `static/manuali/` | `/manuali/nome.pdf` |
| Allegati specifici di un articolo | `static/allegati/AAAA/` | `/allegati/AAAA/nome.pdf` |
| Comunicati stampa firmati | `static/comunicati/AAAA/` | `/comunicati/AAAA/nome.pdf` |
| Segnaletica aree di emergenza | `static/cartelli/` | `/cartelli/nome.png` |
| Copertine e foto evento | `static/images/` | `/images/nome.webp` |
| Archivio storico immagini | `static/images/archivio-storico/` | `/images/archivio-storico/nome.ext` |
| Pittogrammi ISO 7010 | `static/pittogrammi/iso7010/` | `/pittogrammi/iso7010/nome.svg` |
| Pittogrammi ARASAAC | `static/pittogrammi/arasaac/` | `/pittogrammi/arasaac/nome.png` |

**Non** usare `static/documenti/` per contenuto nuovo: resta esclusa dal deploy perché contiene materiale ereditato dal sito precedente gestito direttamente sul server Aruba.

### Cartella `riferimenti-interni/` — documentazione di lavoro NON deployata

Per la **documentazione di lavoro** che il Gruppo deve poter consultare ma **non può/non vuole pubblicare** (norme tecniche copyrighted, draft di consultazione, materiale a uso interno) il repo ha una cartella di livello root:

```
riferimenti-interni/
├── README.md                              ← elenco documenti + stato accessibilità
├── comunicazione-emergenze/
│   ├── iso-22329-2021-social-media-emergencies.pdf       (copyrighted ISO)
│   └── cwa-cen-cenelec-draft-social-media-messages.pdf   (draft consultazione)
└── ...                                    ← futura espansione tematica
```

**Caratteristiche:**
- **Resta nel repo git**, sincronizzata fra maintainer e visibile alle AI di supporto (Claude Code).
- **Non viene deployata**: Hugo costruisce solo da `content/`, `static/`, `themes/`, `data/`, `assets/`, `layouts/`. Una cartella estranea a queste rimane fuori dal sito.
- **Nessun link** dal contenuto pubblico (`content/`, `static/`, `themes/`) verso questa cartella.

**Quando aggiungere un documento qui invece che in `static/manuali/`:**

| Status del documento | Destinazione |
|---|---|
| Pubblico dominio / *approved for public release* / Creative Commons | `static/manuali/` (link pubblico) |
| Copyrighted con copia legittima del Gruppo | `riferimenti-interni/<categoria>/` |
| Draft in fase di consultazione pubblica con scadenza | `riferimenti-interni/<categoria>/` |
| Verbali interni, note di redazione, riferimenti normativi pre-pubblicazione | `riferimenti-interni/<categoria>/` |

**Verifica che non sia esposta**: il workflow `audit-sito.yml` non include `riferimenti-interni/` perché Hugo non la legge. Se in futuro il workflow viene esteso, escluderla esplicitamente. La directory `static/documenti/` è esclusa dal deploy FTP per ragioni storiche (vedi regola 05); `riferimenti-interni/` invece non rientra proprio nelle cartelle Hugo, quindi non serve esclusione FTP.

### Tema personalizzato
Il tema `flavour-pcgenzano` è una dipendenza interna, non esterna: modificalo liberamente.
Si basa su Bootstrap Italia 2.x: usa le classi e i componenti nativi del design system.

## Comandi

```bash
hugo server          # Dev server locale (solo pubblicati)
hugo server -D       # Dev server locale (anche bozze)
hugo --minify        # Build per GitHub Pages
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"  # Build per Aruba
```

## Divieti

- Non introdurre dipendenze esterne non necessarie (npm, node_modules, ecc.).
- Non usare shortcodes non definiti nel tema.
- Non modificare il `baseURL` nella configurazione senza aggiornare anche il workflow CI/CD.
- Non lasciare front matter incompleto o con campi mancanti rispetto all'archetype.
- Non toccare il template lookup order di Hugo senza verificare le conseguenze sull'intera build.
