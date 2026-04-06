# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
  - Key front matter: `badge` (Allerta/Avviso/Comunicazione/Attività/Formazione/Evento/Volontariato), `priorita` (normale/urgente), `scadenza` (date), `allegati` (list of PDFs), `draft`
  - **IMPORTANTE**: nel frontmatter degli articoli usare sempre il formato data semplice `AAAA-MM-GG` (esempio: `2026-04-06`), MAI il formato con orario e timezone (esempio: `2026-04-06T03:32:00Z`). Il formato con timezone causa problemi di pubblicazione.
- All other folders are static pages (one `_index.md` per section)

### Theme (`themes/flavour-pcgenzano/`)

Custom theme, not an external dependency — edit freely. Structure:
- `layouts/partials/` — reusable components (navbar, footer, emergency-banner, allerta-card, etc.)
- `layouts/_default/` — base, list, single templates
- `layouts/index.html` — homepage template
- `static/css/` — custom CSS overrides on top of Bootstrap Italia

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

## Key operational notes

- **To activate emergency mode**: set `"attiva": true` in `data/emergenza.json` and fill `tipo`, `titolo`, `descrizione`. Reset to `false` when done.
- **To set weather alert**: edit `data/allerta.json` — change `livello` to `verde/giallo/arancione/rosso`.
- **Draft posts**: set `draft: true` in front matter. They appear locally with `hugo server -D` but are not published.
- **CI deploy**: pushing to `main` triggers `.github/workflows/deploy.yml` which builds twice (once per baseURL) and deploys via FTP to Aruba and via GitHub Pages API. Monitor at the Actions tab.
- **FTP credentials** are stored as GitHub secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).
