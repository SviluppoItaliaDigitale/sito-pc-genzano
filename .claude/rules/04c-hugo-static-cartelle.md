# Hugo — Cartelle Statiche e Riferimenti Interni

Questo file raccoglie le convenzioni sulle **cartelle statiche** (`static/`) e sulla cartella di livello root **`riferimenti-interni/`** non deployata. Per la struttura del progetto vedi `04-hugo-architecture.md`. Per shortcode/partial vedi `04a-hugo-shortcode-partial.md`. Per template/CSS/UX vedi `04b-hugo-template-css.md`.

## Cartelle `static/` canoniche per file depositati via git

Per evitare che nuovi file finiscano in cartelle escluse dal deploy FTP (vedi regola `05-github-aruba-deploy.md`), usa queste cartelle:

| Contenuto | Cartella | URL pubblico |
|---|---|---|
| Manuali tecnici permanenti citati da più articoli | `static/manuali/` | `/manuali/nome.pdf` |
| Allegati specifici di un articolo | `static/allegati/AAAA/` | `/allegati/AAAA/nome.pdf` |
| Comunicati stampa firmati | `static/comunicati/AAAA/` | `/comunicati/AAAA/nome.pdf` |
| Segnaletica aree di emergenza | `static/cartelli/` | `/cartelli/nome.png` |
| Copertine e foto evento | `static/images/` | `/images/nome.webp` |
| Dataset aperti CSV/JSON (da `scripts/genera-open-data.py`) | `static/open-data/` | `/open-data/nome.csv` · `/open-data/nome.json` |
| Archivio storico immagini | `static/images/archivio-storico/` | `/images/archivio-storico/nome.ext` |
| Pittogrammi ISO 7010 | `static/pittogrammi/iso7010/` | `/pittogrammi/iso7010/nome.svg` |
| Pittogrammi ARASAAC | `static/pittogrammi/arasaac/` | `/pittogrammi/arasaac/nome.png` |

**Non** usare `static/documenti/` per contenuto nuovo: resta esclusa dal deploy perché contiene materiale ereditato dal sito precedente gestito direttamente sul server Aruba.

## Cartella `riferimenti-interni/` — documentazione di lavoro NON deployata

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

## Cartella `bozze/` — articoli in lavorazione NON deployati

Per la **stesura di articoli con calma** prima della pubblicazione, il repo ha una cartella di livello root `bozze/` (creata 22 maggio 2026, gestita dallo script `gestione-sito.sh` voci 5-8: Crea / Modifica / Pubblica / Elimina bozza). Funziona con lo **stesso meccanismo** di `riferimenti-interni/`: è una cartella estranea alle directory native di Hugo (`content/`, `static/`, `themes/`, `data/`, `assets/`, `layouts/`), quindi **non viene mai costruita né deployata** — una bozza non può finire online per sbaglio.

**Perché qui e non in `content/comunicazioni/` con `draft: true`:** la regola di progetto vieta gli articoli `draft: true` dentro `content/` (vedi `09-regole-contenuti-qualita.md` punto e memoria `feedback_no_draft_in_revisione.md`) perché le bozze dimenticate si accumulavano e rischiavano di andare live. La cartella `bozze/` fuori da `content/` **rispetta** quella regola: zero file `draft: true` in `content/`, le bozze vivono in un'area separata che Hugo non vede.

**Ciclo di vita:**
1. **Crea bozza** → file `bozze/<slug>.md` con frontmatter completo e `draft: false` (la `date` è un placeholder, scelta alla pubblicazione).
2. **Pubblica bozza** → lo script chiede la data (oggi o futura per calendarizzare), allinea il campo `date:`, garantisce `draft: false`, e **sposta** il file in `content/comunicazioni/<data>-<slug>.md`. Da quel momento è un articolo normale (gate AGID, cover, ecc. valgono come per ogni articolo).
3. Le bozze sono **tracciate da git** (sincronizzate fra desktop/mobile/cloud), ma restano fuori dal sito finché non vengono pubblicate.

Indice e spiegazione anche in `bozze/README.md`. **Non considerare la presenza di "bozze" in `gestione-sito.sh` una regressione della regola no-draft**: è il pattern fuori-da-content, conforme.
