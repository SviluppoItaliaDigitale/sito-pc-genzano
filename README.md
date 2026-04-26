# Sito Protezione Civile Genzano di Roma

Sito istituzionale del **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**.

- **Produzione**: https://www.protezionecivilegenzano.it/
- **Preview GitHub Pages**: https://sviluppoitaliadigitale.github.io/sito-pc-genzano/
- **Tecnologia**: [Hugo](https://gohugo.io/) (static site generator) + [Bootstrap Italia](https://italia.github.io/bootstrap-italia/) 2.x
- **Conformità**: AGID / Designers Italia, WCAG 2.2 AA
- **Deploy**: automatico a ogni push su `main` (GitHub Actions → Aruba via FTP + GitHub Pages)

---

## Guida ai file di documentazione (`.md`)

Questo repository contiene diversi file Markdown con ruoli diversi. Non vanno eliminati: ognuno ha una funzione operativa o di governance.

### File in root

| File | A cosa serve | Quando aprirlo |
|---|---|---|
| [`README.md`](README.md) | Panoramica del progetto, guida ai file, comandi principali. | Primo file da leggere. |
| [`MANUALE-SITO.md`](MANUALE-SITO.md) | **Manuale di stile v2.0** — guida passo-passo per scrivere articoli e pagine secondo AGID, specifiche immagini (fascia blu), checklist pre-pubblicazione. | Quando devi scrivere un articolo, una pagina o preparare un'immagine. |
| [`PIANO-EDITORIALE.md`](PIANO-EDITORIALE.md) | Fonti ufficiali da monitorare (DPC, INGV, ISPRA, Regione Lazio, ASL, Parco Castelli), calendario redazionale mensile e biblioteca di 250+ titoli evergreen. Obiettivo: tendere a un articolo al giorno (300-365/anno), minimo sostenibile 3-4 a settimana. | Quando devi proporre nuovi contenuti o cerchi ispirazione sulle fonti. |
| [`CLAUDE.md`](CLAUDE.md) | Istruzioni operative per Claude Code (o altra AI) — mandato, priorità, regole di qualità e sicurezza. Importa automaticamente le 6 regole in `.claude/rules/`. | Lettura automatica per ogni sessione AI. Va aggiornato solo se cambia la governance. |

### File in `.claude/rules/` (governance di dettaglio)

Questi 6 file sono importati automaticamente da `CLAUDE.md` e definiscono le regole operative per dominio. Non vanno eliminati.

| File | Dominio |
|---|---|
| [`01-governance-pa.md`](.claude/rules/01-governance-pa.md) | Riferimenti AGID, priorità, divieti assoluti. |
| [`02-content-design-pa.md`](.claude/rules/02-content-design-pa.md) | Scrittura PA, frontmatter articoli, fascia blu immagini, 13 categorie badge. |
| [`03-accessibility.md`](.claude/rules/03-accessibility.md) | Checklist WCAG 2.2 AA: HTML semantico, focus, alt text, contrasto. |
| [`04-hugo-architecture.md`](.claude/rules/04-hugo-architecture.md) | Struttura Hugo, data files, archetypes, homepage dual-mode. |
| [`05-github-aruba-deploy.md`](.claude/rules/05-github-aruba-deploy.md) | Deploy CI/CD su Aruba e GitHub Pages, rollback, divieti. |
| [`06-protezione-civile-scientifica.md`](.claude/rules/06-protezione-civile-scientifica.md) | Codici colore allerte, rischi territoriali, numeri emergenza, comunicazione del rischio. |

### File in `archetypes/` (template Hugo)

| File | A cosa serve |
|---|---|
| [`archetypes/comunicazioni.md`](archetypes/comunicazioni.md) | Template frontmatter per nuovi articoli (`hugo new comunicazioni/AAAA-MM-GG-titolo.md`). |
| [`archetypes/default.md`](archetypes/default.md) | Template minimale per pagine generiche. |

### File in `content/` (contenuti pubblicati)

- `content/comunicazioni/*.md` — articoli e news. Uno per file, frontmatter + corpo Markdown.
- `content/<sezione>/_index.md` — pagine statiche (una per sezione del sito).

---

## Struttura del progetto

```
sito-pc-genzano/
├── README.md                   ← sei qui
├── MANUALE-SITO.md             ← manuale di stile v2.0
├── PIANO-EDITORIALE.md         ← fonti e calendario redazionale
├── CLAUDE.md                   ← istruzioni per AI (importa .claude/rules/)
├── hugo.toml                   ← configurazione Hugo
│
├── .claude/rules/              ← 6 regole di governance (01-06)
├── .github/workflows/          ← automazioni CI/CD e controlli periodici
├── .manuale/sources-hashes.json ← stato hash fonti AGID (gestito dal workflow)
│
├── archetypes/                 ← template per nuovi contenuti
├── content/                    ← contenuti del sito
│   ├── comunicazioni/          ← articoli/news
│   └── <altre-sezioni>/        ← pagine statiche (chi-siamo, contatti, faq,
│                                  rischi-prevenzione, cosa-fare-adesso, ecc.)
├── data/                       ← file dati (JSON/YAML) per contenuti dinamici
│   ├── emergenza.json          ← modalità emergenza on/off
│   ├── allerta.json            ← livello allerta meteo
│   ├── risk_cards.yaml         ← 9 card rischi
│   ├── numeri_utili.yaml       ← numeri emergenza
│   ├── quick_links.yaml        ← CTA homepage
│   ├── social_links.yaml       ← link social
│   └── codici_colore.yaml      ← descrizioni codici allerta
├── scripts/                    ← script Python di automazione (genera-cover,
│                                  aggiorna-image-frontmatter)
├── static/                     ← asset statici (immagini, PDF, JS condivisi)
└── themes/flavour-pcgenzano/   ← tema custom (Bootstrap Italia 2.x)
    ├── layouts/shortcodes/     ← shortcode {{< foto >}} (click-per-ingrandire)
    └── static/css/custom.css   ← override CSS + regole @media print globali
```

---

## Comandi principali

```bash
# Dev server locale
hugo server              # solo contenuti pubblicati
hugo server -D           # anche bozze (draft: true)

# Build
hugo --minify            # build per GitHub Pages
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"  # build Aruba

# Nuovo articolo (usa l'archetype)
hugo new comunicazioni/AAAA-MM-GG-titolo-articolo.md

# Pubblicazione (triggera deploy automatico)
git add . && git commit -m "..." && git push

# Script interattivo di gestione (se installato)
bash ~/gestione-sito.sh

# Export contesto completo per altra AI (ChatGPT, Gemini, Claude web, ecc.)
bash scripts/export-contesto-ai.sh
# → Genera CONTESTO-AI.md nella root con TUTTA la documentazione del sito
#   in un unico file, pronto da copia-incollare in qualsiasi altra AI per
#   avere continuità di gestione senza perdere nulla.
```

---

## Continuità su altra AI o altra sessione

Per lavorare sul sito con un'AI diversa (ChatGPT, Gemini, Claude web) o in una
nuova sessione dove non si ha accesso automatico ai file del repo, esiste uno
**script di export** che raccoglie tutta la documentazione in un singolo file:

```bash
bash scripts/export-contesto-ai.sh
```

Produce `CONTESTO-AI.md` (~275 KB) contenente:
- README, CLAUDE.md, 6 regole di governance
- Manuale operativo completo (MANUALE-SITO.md)
- Piano editoriale (fonti + calendario + biblioteca evergreen)
- Archetype articoli, configurazione Hugo, shortcode `foto`
- Memorie utente (feedback durevoli salvati da Claude Code)

Basta copiare il contenuto di `CONTESTO-AI.md` e incollarlo come primo messaggio
nell'altra AI per avere continuità operativa senza perdere contesto.

Il file è `.gitignore`d perché si rigenera on-demand dallo stato corrente del repo.

---

## Automazioni attive (GitHub Actions)

Tutti i workflow di manutenzione girano **ogni lunedì** (primo giorno della settimana), scaglionati in orari diversi per ridurre il carico sul runner.

| Workflow | Frequenza | Scopo |
|---|---|---|
| `deploy.yml` | Ogni push su `main` | Build + deploy Aruba (FTP) + GitHub Pages |
| `check-allerta.yml` | Orario (min 12) | Verifica stato allerta meteo Regione Lazio |
| `pubblica-programmata.yml` | Giornaliero 06:00 UTC | Pubblica articoli programmati |
| `lighthouse-audit.yml` | Post-deploy | Audit performance/accessibilità/SEO |
| `smoke-test-post-deploy.yml` | Post-deploy | Smoke test live: status HTTP, marker JS, header sicurezza |
| `aggiorna-manuale.yml` | Lunedì 06:00 UTC | Hash fonti AGID/Designers Italia → issue se cambiano |
| `update-bootstrap-italia.yml` | Lunedì 06:00 UTC | Aggiornamenti Bootstrap Italia |
| `audit-sito.yml` | Lunedì 09:00 UTC | **Audit completo (38 sezioni)**: contenuti, codice/template, governance docs, audit aggiuntivo, link critici normativa (fuso `coerenza-docs.yml` + `check-normativa-links.yml` il 26 aprile 2026) |
| `check-links-sito.yml` | Lunedì 10:00 UTC | Crawl completo lychee: tutti i link (interni + esterni) |

Le issue generate automaticamente compaiono nella [tab Issues](https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/issues) con label `manutenzione`, `documentazione`, `link-rotti`, ecc.

---

## Flusso di lavoro tipico per pubblicare un articolo

1. Apri `MANUALE-SITO.md` (manuale operativo).
2. Identifica lo slug: `AAAA-MM-GG-titolo-breve`.
3. Esegui `hugo new comunicazioni/AAAA-MM-GG-titolo-breve.md`.
4. Compila il frontmatter (vedi Parte 1.5 del manuale).
5. Scrivi il corpo seguendo le regole AGID (Parte 2 del manuale).
6. Prepara l'immagine di copertina con fascia blu (Parte 3 del manuale).
7. Se hai foto evento, inseriscile nel corpo con lo shortcode `{{< foto >}}` (Parte 3.14 del manuale) — nome file diverso dallo slug così non vengono sovrascritte dal generatore di copertine.
8. Verifica con `hugo server` in locale.
9. Esegui la checklist pre-pubblicazione (Parte 5).
10. `git add . && git commit -m "Nuovo articolo: titolo" && git push`.
11. Controlla il deploy nella tab Actions.

---

## Contatti

- Repository: [github.com/SviluppoItaliaDigitale/sito-pc-genzano](https://github.com/SviluppoItaliaDigitale/sito-pc-genzano)
- Sito pubblico: [protezionecivilegenzano.it](https://www.protezionecivilegenzano.it/)
- Email istituzionale: vedi pagina [Contatti](https://www.protezionecivilegenzano.it/contatti/)

---

## Licenza e diritti

Contenuti testuali: © Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
Codice del tema: vedi `themes/flavour-pcgenzano/`.
Riferimenti normativi: AGID, Designers Italia, Dipartimento Protezione Civile.
