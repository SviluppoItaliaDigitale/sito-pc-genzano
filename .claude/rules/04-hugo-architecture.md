# Hugo Architecture

Questo file contiene la **mappa generale** dell'architettura Hugo: struttura del progetto, regole fondamentali, comandi e divieti. Il dettaglio è suddiviso per area:

- **`04a-hugo-shortcode-partial.md`** — shortcode (`foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`, `pagina-emergenza-lite`), render hook (tabelle, link), partial (article-cover, leggi-ad-alta-voce, articolo-navigazione, articoli-correlati, share buttons, modal SOS-112, striscia pittogrammi, FAQ accordion).
- **`04b-hugo-template-css.md`** — menu di navigazione (mega-menu), TOC pagine lunghe, pagine legali con dataUltimaRevisione, regole stampa, tipografia `.article-body` v7.2, toolbar di accessibilità, sistema bozze social automatiche, pagina 404 istituzionale.
- **`04c-hugo-static-cartelle.md`** — cartelle `static/` canoniche, cartella `riferimenti-interni/` non deployata.

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
│   ├── auto-cover-mancanti.py       # Genera cover tipografiche banner per
│   │                                # articoli con image:"" o con file mancante
│   │                                # (sicuro: mai sovrascrive foto utente).
│   │                                # Chiama genera-cover.py + popola frontmatter.
│   ├── proponi-marker-foto.py       # DEPRECATO 2026-05-03: il marker TODO-foto-*
│   │                                # è bandito (CLAUDE.md punto 9). Lo script
│   │                                # resta per riferimento storico ma il suo
│   │                                # output non va più applicato. Per foto
│   │                                # inline usare l'agent pc-image-fixer.
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
- `"attiva": true` → layout emergenza (azioni → hero compatto → news)

Non modificare questa logica senza valutare l'impatto su entrambe le modalità.

**Banner emergenza SITE-WIDE (da 22 maggio 2026).** Il `partial "emergency-banner.html"` è chiamato in `_default/baseof.html` (subito dopo la navbar, **fuori** da `<main>` per non essere indicizzato da Pagefind), quindi quando `data/emergenza.json` ha `attiva: true` il banner compare su **ogni** pagina del sito, non solo in homepage — così chi atterra su una pagina interna durante un'emergenza vede comunque l'avviso. Esclusioni: la pagina lite `/emergenza/` (guard `{{ if ne .Type "emergenza" }}` in baseof, perché ha già la sua gestione interna del banner) e `/lanterna/` (standalone, non usa baseof). `index.html` **non** richiama più il partial (lo farebbe due volte). Il partial si auto-nasconde se l'emergenza non è attiva.

### Contenuti dinamici via data files

I file in `data/` sono la via principale per aggiornare contenuti senza toccare i template.
Aggiorna i data files al posto di modificare i template quando possibile.

### Output format custom (`hugo.toml [outputs] home`)

Oltre a `HTML`/`RSS`/`JSON`, la **home page** genera tre output format custom (definiti in `[outputFormats.*]` di `hugo.toml`, template `index.<suffix>.xml` nel tema):

- **`CAP`** → `/allerta-cap.xml` — feed **CAP 1.2** (Common Alerting Protocol, standard OASIS `urn:oasis:names:tc:emergency:cap:1.2`), machine-readable per aggregatori/app/bot. Template `index.cap.xml`, alimentato da `data/allerta.json`: un blocco `<info>` per pericolo concorrente (oggi sempre presente; domani/avviso meteo/incendi AIB Zona 9 solo se presenti nei rispettivi sotto-blocchi). L'`identifier` è **composito e byte-stabile** (derivato dai soli campi di contenuto mutabili, sanitizzato `replaceRE`): il documento non cambia tra i deploy orari finché lo stato allerta non cambia → niente "nuove" allerte spurie per i consumatori che deduplicano per `identifier`. `mediaType application/xml`, `baseName allerta-cap`, `rel alternate`, `notAlternative true`. Privacy-first (self-hosted, nessuna dipendenza esterna).
- **`NEWSSITEMAP`** → `/news-sitemap.xml` — sitemap **Google News** (`xmlns:news=…/sitemap-news/0.9`). Template `index.newssitemap.xml`: include **solo** gli articoli `comunicazioni` con `Date` nelle ultime **48h** (`now.AddDate 0 0 -2`), come richiesto da Google News; i `-facile` (A2) sono già esclusi via `build.list:never`. Dichiarata in `static/robots.txt` accanto alla `sitemap.xml` standard.
- **`BUILDINFO`** — endpoint di servizio con i metadati di build.

### Articoli (comunicazioni/)

- Usa sempre l'archetype: `hugo new comunicazioni/AAAA-MM-GG-titolo.md`
- Il frontmatter deve essere completo (vedi regola 02-content-design-pa.md)
- Il formato data nel frontmatter è SEMPRE `AAAA-MM-GG`, MAI con timezone
- `draft: true` esclude dalla build di produzione, visibile solo con `hugo server -D`

### Shortcode, render hook e partial

Vedi `04a-hugo-shortcode-partial.md` per: shortcode `foto` / `pittogramma` / `cosa-non-fare` / `chi-chiamare` / `pagina-emergenza-lite`, render hook tabelle e link, partial `article-cover` / `leggi-ad-alta-voce` / `articolo-navigazione` / `articoli-correlati` / share buttons / modal SOS-112 / striscia pittogrammi / FAQ accordion.

### Template, menu, CSS, UX

Vedi `04b-hugo-template-css.md` per: menu di navigazione mega-menu accorpato, TOC per articoli lunghi, pagine legali/istituzionali con `dataUltimaRevisione`, regole stampa, tipografia `.article-body` v7.2, toolbar di accessibilità (FAB), bozze social automatiche (Gemini API + Pillow), pagina 404 istituzionale.

### Cartelle statiche e riferimenti interni

Vedi `04c-hugo-static-cartelle.md` per: cartelle `static/` canoniche e cartella `riferimenti-interni/` non deployata.

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
