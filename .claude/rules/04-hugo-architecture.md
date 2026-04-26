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
Il tema definisce un unico shortcode: `foto`, usato per inserire foto evento nel corpo degli articoli.

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

### Menu di navigazione principale (mega-menu accorpato)

Il menu è definito in `hugo.toml` sotto `[[menus.main]]` e renderizzato in `themes/flavour-pcgenzano/layouts/partials/navbar.html`. Struttura a **6 voci di primo livello**, di cui 3 dropdown:

| Voce | Tipo | Contenuto |
|---|---|---|
| Home | diretta | `/` |
| Per il Cittadino ▾ | dropdown | Cosa Fare Adesso, Allerte Meteo, Rischi e Prevenzione, Cartografia, Numeri Utili, Piano Familiare |
| Formazione ▾ | dropdown | Corsi e percorsi, Giochi, Glossario, Schede Stampabili |
| Volontariato ▾ | dropdown | Diventa Volontario, Chi Siamo |
| Comunicazioni | diretta | `/comunicazioni/` |
| Contatti | diretta | `/contatti/` |

Razionale: 10 voci flat erano troppe per mobile e per l'utente in emergenza. L'accorpamento mantiene tutte le pagine raggiungibili in 2 click ma riduce il rumore visivo.

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

**Non** usare `static/documenti/` per contenuto nuovo: resta esclusa dal deploy perché contiene materiale ereditato dal sito precedente gestito direttamente sul server Aruba.

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
