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
│   │   │                    # cookie-banner, breadcrumb, page-tools, ecc.
│   │   ├── shortcodes/      # foto.html (click-per-ingrandire accessibile)
│   │   ├── comunicazioni/   # list.html con filtri per badge
│   │   └── cerca/           # list.html con motore di ricerca JS
│   └── static/
│       ├── css/custom.css   # Override CSS su Bootstrap Italia + regole
│       │                    # @media print globali (stampa solo l'articolo)
│       └── images/          # Asset statici
├── archetypes/
│   ├── comunicazioni.md     # Archetype completo per news
│   └── default.md           # Archetype minimale
├── scripts/
│   ├── genera-cover.py              # Genera copertine tipografiche automatiche
│   ├── aggiorna-image-frontmatter.py # Aggiorna il campo image negli articoli
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

### Pagine legali/istituzionali con data di revisione
Le pagine `privacy`, `note-legali`, `accessibilita`, `social-media-policy` usano il campo frontmatter `dataUltimaRevisione: "AAAA-MM-GG"`.

Il template `_default/single.html` mostra questa data in un box evidente (`alert alert-light`) in cima al contenuto, subito dopo il titolo, con il testo "Pagina rivista il …".

Il partial `partials/page-tools.html` verifica la presenza del campo: se è impostato, omette la `.Lastmod` automatica per evitare due date sulla stessa pagina. Questo garantisce che ci sia un'unica fonte di verità per la data di revisione delle pagine legali, sotto il controllo editoriale esplicito del redattore (non automatica da git).

Non usare date di revisione hard-coded nel corpo (tipo "Ultimo aggiornamento: Marzo 2026"): la data è unica e vive nel frontmatter.

### Regole stampa
Il file `themes/flavour-pcgenzano/static/css/custom.css` contiene un blocco `@media print` globale che nasconde tutto il chrome del sito (header, navbar, footer, banner, cookie, utility bar, page tools, breadcrumb) e stampa solo il contenuto della pagina su formato A4 con margini standard. Esiste anche un blocco specifico per il piano familiare stampabile (`body.piano-printing`). Non duplicare queste regole; se servono modifiche, lavora sui blocchi esistenti.

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
