# Hugo Architecture

## Struttura del progetto

```
sito-pc-genzano/
├── content/
│   ├── comunicazioni/       # Articoli/news (archetype: comunicazioni.md)
│   │   └── AAAA-MM-DD-titolo.md
│   └── [sezioni statiche]/  # Pagine statiche con _index.md
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
│   │   ├── _default/        # base.html, list.html, single.html
│   │   └── partials/        # navbar, footer, emergency-banner, allerta-card, ecc.
│   └── static/css/          # Override CSS su Bootstrap Italia
├── archetypes/
│   ├── comunicazioni.md     # Archetype completo per news
│   └── default.md           # Archetype minimale
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
- Usa sempre l'archetype: `hugo new comunicazioni/AAAA-MM-DD-titolo.md`
- Il frontmatter deve essere completo (vedi regola 02-content-design-pa.md)
- Il formato data nel frontmatter è SEMPRE `AAAA-MM-GG`, MAI con timezone
- `draft: true` esclude dalla build di produzione, visibile solo con `hugo server -D`

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
