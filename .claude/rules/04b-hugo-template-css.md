# Hugo — Template, CSS, Menu, UX

Questo file raccoglie le regole su **template** principali, **menu di navigazione**, **toolbar di accessibilità**, **tipografia**, **stampa**, **404** e sistema **bozze social**. Per la struttura del progetto e le regole Hugo fondamentali vedi `04-hugo-architecture.md`. Per shortcode, render hook e partial vedi `04a-hugo-shortcode-partial.md`. Per cartelle statiche e deploy vedi `04c-hugo-static-cartelle.md`.

## Menu di navigazione principale (mega-menu accorpato)

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

## Indice della pagina (TOC) per articoli lunghi

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

## Pagine legali/istituzionali con data di revisione

Le pagine `privacy`, `note-legali`, `accessibilita`, `social-media-policy` usano il campo frontmatter `dataUltimaRevisione: "AAAA-MM-GG"`.

Il template `_default/single.html` mostra questa data in un box evidente (`alert alert-light`) in cima al contenuto, subito dopo il titolo, con il testo "Pagina rivista il …".

Il partial `partials/page-tools.html` verifica la presenza del campo: se è impostato, omette la `.Lastmod` automatica per evitare due date sulla stessa pagina. Questo garantisce che ci sia un'unica fonte di verità per la data di revisione delle pagine legali, sotto il controllo editoriale esplicito del redattore (non automatica da git).

Non usare date di revisione hard-coded nel corpo (tipo "Ultimo aggiornamento: Marzo 2026"): la data è unica e vive nel frontmatter.

## Regole stampa

Il file `themes/flavour-pcgenzano/static/css/custom.css` contiene un blocco `@media print` globale che nasconde tutto il chrome del sito (header, navbar, footer, banner, cookie, utility bar, page tools, breadcrumb) e stampa solo il contenuto della pagina su formato A4 con margini standard. Esiste anche un blocco specifico per il piano familiare stampabile (`body.piano-printing`). Non duplicare queste regole; se servono modifiche, lavora sui blocchi esistenti.

## Tipografia del corpo articolo (`.article-body` v7.2)

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

## Strumenti di Accessibilità (toolbar utente)

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

## Bozze social automatiche (Gemini API + Pillow)

Sistema completo per generare bozze post social (X, Facebook, Instagram, Telegram) e immagini Instagram (post 1080×1080 + carosello + story 1080×1920) a partire dagli articoli del sito. Usa il **tier gratuito Gemini 2.5 Flash** (1500 req/giorno = costo zero).

**Componenti operativi:**
- `scripts/genera-social.py` — motore Python: legge le rules `.claude/rules/02|03|06.md` e le inietta nel system prompt di Gemini, ottiene 4 testi via JSON strutturato, salva in `social-bozze/<slug>/`.
- `scripts/genera-immagini-social.py` — Pillow: template istituzionale per Instagram con auto-rilevamento carosello (estrae le foto inline `{{< foto >}}` dal body).
- `scripts/genera-social.sh` — wrapper bash sequenziale.
- `.github/workflows/genera-social-bozze.yml` — automazione CI a ogni push articolo.

**Cartelle:**
- `social-bozze/<slug>/` — fuori da Hugo (non deployata sul sito), visibile solo nel repo per copia/incolla.
- `static/images-social/<slug>-instagram-{post,post-N,story}.webp` — deployata sul sito (URL pubblico Aruba).

**Setup chiave:**
- Locale: `export GEMINI_API_KEY="..."` in `~/.bashrc` (chiave gratuita da `aistudio.google.com/apikey`).
- CI: GitHub Secret `GEMINI_API_KEY`.

**3 scenari auto-rilevati** (zero configurazione frontmatter aggiuntiva):

| Scenario | `image:` | Foto inline `{{< foto >}}` | Output IG |
|---|---|---|---|
| A | vuoto | assenti | cover tipografica + story |
| B | path | assenti | post + story |
| C | path | 2-9 nel body | carosello (max 10) + story |

**Regole della scrittura sociale**: caricate dinamicamente dalle rules `02-content-design-pa.md` (linguaggio AGID, hashtag stabili, struttura post crisi), `03-accessibility.md` (a11y social: alt text, max 2 emoji, no Unicode decorativi), `06-protezione-civile-scientifica.md` (codici colore, struttura 6 punti per allerte).

**Cosa NON fa** (intenzionalmente):
- Non pubblica automaticamente sui social (le bozze sono per copia/incolla manuale).
- Non aggiunge informazioni che non sono nell'articolo.
- Non sostituisce la rilettura umana.

**Documentazione operativa completa** in `scripts/README-social.md`. **Workflow mobile-first** in `MANUALE-MOBILE.md` (root).

## Pagina 404 istituzionale

`themes/flavour-pcgenzano/layouts/404.html` è una **pagina di atterraggio del recupero**, non un vicolo cieco. Contiene:
- Form ricerca interna integrato (action su `/cerca/`)
- 8 card di link rapidi alle pagine più consultate (Numeri Utili, Allerte Meteo, Cosa fare, Assistente, Diventa Volontario, Comunicazioni, Cartografia, Mappa Sito)
- Alert «in caso di emergenza chiama il 112»
- Script JS di redirect URL legacy (Joomla `*.html`) che si attiva solo se nessuna regola `.htaccess` server-side ha già intercettato l'URL

**Importante**: NON c'è un override `layouts/404.html` nella root del progetto (è stato rimosso aprile 2026). Vince quello del tema. Se in futuro qualcuno crea `layouts/404.html`, scavalca il template del tema e l'utente non vede più questa pagina.

## Homepage enhancements v1.0 (aprile 2026)

Quattro micro-miglioramenti grafici applicati alla **sola homepage** (scoped via `body.home-page`), tutti AGID-compliant, tutti con copertura `prefers-reduced-motion` + `@media print` + toolbar a11y "pausa animazioni" + supporto mobile (nessuna `@media (hover: hover)` o esclusione touch — funzionano identico su iOS/Android).

1. **Live dot pulse** (`.live-dot` + `@keyframes livePulse`) — cerchio blu istituzionale `#003366` accanto al titolo "Notizie in Evidenza", animazione box-shadow espansiva 2.5s. Ricalca il pattern `sosPulse` del bottone SOS-112 in chiave informativa anziché di emergenza. Markup: `<span class="live-dot" aria-hidden="true"></span>` davanti al testo del titolo, in `partials/latest-news.html`.

2. **Reveal-on-scroll** (`.reveal-on-scroll.is-revealed` + `js/homepage-reveal.js`) — IntersectionObserver puro stdlib applicato ai selettori `.quick-action-card`, `.card-servizio`, `.card-notizia-hero`, `section .card.border-danger`, `.stat-hero-item`, `.card-numero-utile`. Le card appaiono con `opacity 0→1 + translateY(15px→0)` quando entrano nel viewport (threshold 0.15, rootMargin -50px). Auto-disable se reduced-motion o IntersectionObserver assente. Script caricato `defer` solo per `.IsHome`.

3. **Hero pattern + gradiente animato** (`@keyframes heroGradientShift` + `body.home-page .hero-section::after`) — pattern di linee oblique sottili (`opacity: 0.045`) via `repeating-linear-gradient` (zero data:URL) sovrapposto al gradiente blu esistente. Il gradiente shifta cromaticamente in 35s loop con `background-size: 180%`. Il movimento è quasi impercettibile ma dà profondità.

4. **Hover lift card + freccia CTA** — `translateY(-3px)` + ombra blu istituzionale al `:hover` o `:focus-within`. La `bi-arrow-right` delle CTA scivola di 4px a destra. Stessa estetica già usata in articoli prev/next + correlati. Su mobile si attiva al `:focus-within` (touch).

CSS scoped sezione **HOMEPAGE ENHANCEMENTS v1.0** in `custom.css` (~150 righe). Body class `home-page` aggiunta condizionalmente in `baseof.html`: `<body{{ if .IsHome }} class="home-page"{{ end }}>` — necessaria per scope CSS, evita leak su altre pagine.

**Per disattivare tutto** (homepage piatta come pre-v1.0): rimuovi la condizione `.IsHome` dal body class in `baseof.html` — niente regole CSS si applicheranno (sono tutte scoped).

**Per estendere a un'altra pagina** (es. archivio comunicazioni): cambia la condizione in `baseof.html` o aggiungi una nuova body class, poi modifica i selettori CSS coerentemente.

Specifiche operative complete in `MANUALE-SITO.md` Parte 15.
