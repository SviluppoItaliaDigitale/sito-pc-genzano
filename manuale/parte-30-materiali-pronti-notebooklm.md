_[Indice manuale](README.md)_

# Parte 30 — Materiali pronti NotebookLM (`/risorse-pronte/`)

Da maggio 2026 il sito ha una sezione `/risorse-pronte/` che raccoglie **materiali multimediali pronti da scaricare e condividere** (podcast, infografiche, presentazioni) divisi per tema di Protezione Civile. Sono generati con [Google NotebookLM](https://notebooklm.google.com) partendo dalle fonti istituzionali del sito e pubblicati con licenza **CC BY-NC-SA 4.0**.

Questa parte del manuale spiega il workflow completo, dall'apertura di NotebookLM alla pubblicazione live sul sito.

---

## 30.1 Cosa contiene la pagina `/risorse-pronte/`

Hub pubblico con i materiali divisi in **5 temi** (al 16/05/2026):

- 🏠 Rischio sismico nei Castelli Romani
- 🌧️ Rischio idrogeologico
- 🔥 Rischio incendi boschivi (AIB)
- ⛈️ Allerta meteo
- 🎒 Kit emergenza famiglia

Per ogni tema, **fino a 4 tipi di materiali**:

| Tipo | Formato | Durata/Dimensione tipica | Uso |
|---|---|---|---|
| Podcast audio | M4A (AAC) | 20-25 min, 30-50 MB | Ascolto offline su telefono, auto, podcast app |
| Infografica | PNG 1080×1080 | 1-5 MB | Condivisione WhatsApp, stampa A4, affissione bacheca |
| Presentazione PPTX | PowerPoint | 5-20 MB | Docenti che modificano per uso in classe |
| Presentazione PDF | PDF | 5-20 MB | Apertura su qualsiasi dispositivo senza PowerPoint |

Quiz e flashcard sono temporaneamente esclusi: NotebookLM li condivide solo come link al notebook proprietario, e ogni visita consumerebbe quota PRO. Saranno gestiti in futuro come HTML statico nativo del sito.

---

## 30.2 Architettura tecnica

### Sul Desktop dell'utente

```
~/Scrivania/
├── GUIDA-NOTEBOOKLM-PC-GENZANO.md       ← guida didattica completa
├── notebooklm-pacchetti/                ← 📥 INPUT: cosa caricare in NotebookLM
│   ├── 00-LEGGIMI.md
│   ├── rischio-sismico/
│   │   ├── 00-INDICE.md                 ← passi 1-4 della procedura
│   │   ├── 02-prompt-podcast.md         ← copia-incolla in NotebookLM
│   │   ├── 03-prompt-infografica.md
│   │   ├── 04-prompt-presentazione.md
│   │   ├── AAA-FONTI-SITO-AGGREGATE-rischio-sismico.md  ← carica come fonte file
│   │   └── LINKS-DA-INCOLLARE.txt       ← URL da incollare come fonti link
│   ├── rischio-idrogeologico/...
│   ├── rischio-incendio/...
│   ├── allerta-meteo/...
│   └── kit-emergenza/...
└── notebooklm-output/                   ← 📤 OUTPUT: dove trascini i file scaricati
    ├── 00-LEGGIMI.md
    ├── rischio-sismico/                 ← (vuoto finché non lavori sul tema)
    ├── rischio-idrogeologico/
    ├── rischio-incendio/
    ├── allerta-meteo/
    └── kit-emergenza/
```

I file dei pacchetti sono generati da `scripts/prepara-pacchetto-notebooklm.py`. La drop zone resta vuota finché l'utente non vi trascina i file scaricati da NotebookLM.

### Nel repo

```
sito-pc-genzano/
├── content/
│   ├── risorse-pronte/_index.md           ← pagina hub pubblica
│   └── podcast/
│       ├── _index.md                      ← pagina podcast list
│       └── <data>-<tema>.md               ← episodio per ogni podcast pubblicato
├── data/
│   └── risorse_pronte.yaml                ← catalogo materiali (auto-popolato)
├── static/
│   ├── podcast/episodi/                   ← file MP3/M4A
│   ├── infografiche/                      ← PNG/JPG/WebP
│   └── presentazioni/                     ← PPTX + PDF
├── themes/flavour-pcgenzano/layouts/
│   ├── risorse-pronte/list.html           ← hub layout con chip indice
│   └── partials/materiali-correlati.html  ← cross-link auto su pagine rischio
└── scripts/
    ├── prepara-pacchetto-notebooklm.py    ← genera pacchetti su Desktop
    └── pubblica-notebooklm-output.py      ← pubblica drop zone sul sito
```

---

## 30.3 Workflow operativo per nuovo tema

### Passo 1 — Lancia il preparatore (una sola volta o quando aggiungi temi)

```bash
python3 scripts/prepara-pacchetto-notebooklm.py
```

Genera tutti i pacchetti per i 5 temi su `~/Scrivania/notebooklm-pacchetti/`. Idempotente: rilancia ogni volta che hai modificato lo script o vuoi aggiornare i prompt.

### Passo 2 — Apri NotebookLM e crea il notebook

1. Vai su <https://notebooklm.google.com> con il tuo account Google **PRO** (badge visibile in alto a destra).
2. Clicca "Crea notebook".
3. Titolo: il nome del tema (es. "Rischio sismico nei Castelli Romani").

### Passo 3 — Carica le fonti (5-6 click totali)

Nel pacchetto del tema sul Desktop apri `00-INDICE.md`. Trovi 2 file fonti:

**3A — Carica 1 file aggregato**:
- Apri NotebookLM → "Aggiungi fonti" → "Carica file"
- Seleziona `AAA-FONTI-SITO-AGGREGATE-<tema>.md` (contiene 145-267 articoli del nostro sito sul tema)
- 1 upload, ~30 sec di lettura da parte di NotebookLM

**3B — Incolla 3-5 URL esterni**:
- Apri `LINKS-DA-INCOLLARE.txt` (un URL per riga)
- Per ognuno: copia → in NotebookLM "Aggiungi fonti" → "Link" → incolla → conferma
- ~4 incoll, ~1 min di fetch totale

A questo punto NotebookLM ha tutto il materiale: aspetta che ogni voce abbia la spunta verde.

### Passo 4 — Imposta italiano (una sola volta)

Ingranaggio ⚙️ in alto a destra → Impostazioni → Output language → **Italiano** → Salva.

Questa impostazione è persistente per il tuo account.

### Passo 5 — Genera i 3 output

Per ognuno dei 3 prompt copia il contenuto del file `.md` corrispondente e incollalo nel campo "Personalizza" del bottone Studio.

| Bottone Studio | File prompt | Output scaricato (nome auto-generato) |
|---|---|---|
| Overview audio | `02-prompt-podcast.md` | File `.m4a` (es. `La_realtà_dietro_un_allerta_meteo.m4a`) |
| Infografica | `03-prompt-infografica.md` | File `.png` o `.jpg` |
| Presentazione | `04-prompt-presentazione.md` | File `.pptx` E `.pdf` (2 bottoni separati per scaricare entrambi i formati) |

Ogni generazione richiede 1-5 minuti. **Scarica tutti i file** nella cartella Downloads del browser.

### Passo 6 — Trascina i file nella drop zone

Sposta tutti i file scaricati in `~/Scrivania/notebooklm-output/<tema>/`. **Non rinominare nulla**: lo script li classifica automaticamente per estensione.

Esempio drop zone dopo trascinamento:

```
~/Scrivania/notebooklm-output/kit-emergenza/
├── La_protezione_civile_inizia_dal_frigorifero.m4a    (38 MB)
├── unnamed.png                                         (4 MB)
├── Resilience_Operational_Blueprint.pptx               (21 MB)
└── Resilience_Operational_Blueprint.pdf                (17 MB)
```

### Passo 7 — Scrivi a Claude

> *"Pubblica gli output di NotebookLM per il tema `<tema-slug>`"*

Esempi: *"Pubblica gli output di NotebookLM per il tema rischio-sismico"*, *"Pronti i file per allerta-meteo"*, *"Pubblica kit-emergenza"*.

L'agent [`pc-notebooklm-publisher`](../.claude/agents/pc-notebooklm-publisher.md) prende il comando, lancia lo script, verifica, committa, pusha.

### Passo 8 — Cosa succede in automatico

Claude esegue:

1. `python3 scripts/pubblica-notebooklm-output.py <tema>`
2. I file vengono **classificati per estensione** (M4A → podcast, PNG → infografica, PPTX → presentazione, PDF → presentazione-pdf)
3. Vengono **rinominati** in formato canonico: `<data>-<tema>-<tipo>.<ext>` (es. `2026-05-16-kit-emergenza-podcast.m4a`)
4. Vengono **copiati** nelle cartelle giuste: `static/podcast/episodi/`, `static/infografiche/`, `static/presentazioni/`
5. **Aggiunte voci** a `data/risorse_pronte.yaml`
6. Per il podcast, **creato anche** `content/podcast/<data>-<tema>.md` con frontmatter `episodio: N`, `audio: <url>`, descrizione standard, licenza CC BY-NC-SA 4.0
7. **Cross-link automatico**: il partial `materiali-correlati.html` mostra "Materiali pronti su questo tema" in fondo alla pagina rischio/sezione corrispondente
8. `hugo --quiet --minify` verifica build pulito
9. Commit + push
10. **Deploy.yml** parte automaticamente: ~3 min e tutto è live su Aruba + GitHub Pages

---

## 30.4 Verifica post-pubblicazione

Dopo che Claude ti dice "fatto, pushato", controlla:

1. **Pagina hub**: <https://www.protezionecivilegenzano.it/risorse-pronte/>
   - L'indice chip in cima deve mostrare il tuo tema cliccabile con il conteggio (es. "Rischio sismico · 4")
   - La sezione del tema mostra le 4 card materiali con anteprima infografica, player audio HTML5, bottoni Scarica
2. **Pagina podcast**: <https://www.protezionecivilegenzano.it/podcast/>
   - L'episodio nuovo appare in cima alla lista con numero progressivo
   - Feed RSS aggiornato: <https://www.protezionecivilegenzano.it/podcast/index.xml> (controlla con un aggregatore tipo Inoreader)
3. **Cross-link sulla pagina rischio**: es. <https://www.protezionecivilegenzano.it/rischi-prevenzione/rischio-sismico/>
   - In fondo (sopra il box "Condividi e scarica") trovi la sezione "Materiali pronti su questo tema"

Se uno di questi 3 punti fallisce, segnalalo a Claude per debug.

---

## 30.5 Aggiungere un tema nuovo

Per aggiungere un sesto tema (es. `rischio-vulcanico`):

### 1. Aggiorna lo script preparatore

Edita `scripts/prepara-pacchetto-notebooklm.py`:

```python
TEMI = {
    # ... temi esistenti ...
    "rischio-vulcanico": {
        "titolo": "Rischio vulcanico nei Colli Albani",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/rischio-vulcanico/",
        "articoli_correlati": [
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "INGV Osservatorio Vesuviano: https://www.ov.ingv.it",
            "DPC Rischio vulcanico: https://www.protezionecivile.gov.it/it/pagina/rischio-vulcanico",
        ],
        "focus_podcast": [
            "I Colli Albani come distretto vulcanico quiescente (non estinto)",
            "Crateri del Lago Albano e del Lago di Nemi",
            "Sistema di monitoraggio INGV",
            "Cosa fare in caso di ripresa attività",
        ],
        "icona_emoji": "🌋",
    },
}

KEYWORDS_TEMA = {
    # ... esistenti ...
    "rischio-vulcanico": [
        "vulcan", "vulcanic", "Vesuvio", "Colli Albani", "INGV",
        "Lago Albano", "Lago Nemi", "caldera", "magma",
    ],
}
```

### 2. Aggiorna `data/risorse_pronte.yaml`

Aggiungi il nuovo tema all'array `temi:`:

```yaml
temi:
  # ... esistenti ...
  - slug: rischio-vulcanico
    titolo: "Rischio vulcanico"
    icona: "bi-fire"
    descrizione: "Distretto vulcanico dei Colli Albani: monitoraggio, scenari, comportamenti."
```

### 3. Crea la cartella drop zone

```bash
mkdir -p ~/Scrivania/notebooklm-output/rischio-vulcanico
```

### 4. Rigenera i pacchetti

```bash
python3 scripts/prepara-pacchetto-notebooklm.py
```

Lo script crea automaticamente la cartella `notebooklm-pacchetti/rischio-vulcanico/` con tutti i file pronti.

### 5. (Opzionale) Aggiungi alias in `materiali-correlati.html`

Se la pagina rischio sul sito ha un nome diverso dal slug tema, aggiungi un alias nel partial:

```go
{{- $aliases := dict
    "allerte-meteo" "allerta-meteo"
    "rischio-vulcani" "rischio-vulcanico"
-}}
```

### 6. Procedi col passo 2 del workflow standard sopra.

---

## 30.6 Gestione re-pubblicazione (aggiornamento materiale)

Quando vuoi rifare un podcast/infografica perché le fonti sono cambiate o vuoi una versione nuova:

1. **Apri lo stesso notebook NotebookLM esistente** (non crearlo nuovo). Aggiorna le fonti (rimuovi vecchie, carica nuove).
2. Genera nuovamente i 3 output (Overview audio + Infografica + Presentazione).
3. Trascina i nuovi file nella drop zone `~/Scrivania/notebooklm-output/<tema>/`. **I file vecchi della drop zone non importa se ci sono, ma è più pulito svuotare prima**.
4. Scrivi a Claude *"ripubblica gli output di NotebookLM per X"*.

Claude:
- Pubblica i nuovi file con la **data odierna** nel naming (es. `2026-08-15-rischio-sismico-podcast.m4a` invece di `2026-05-16-...`)
- Aggiunge nuove voci in `risorse_pronte.yaml` (le vecchie restano come archivio)
- Decide insieme a te se rimuovere le versioni vecchie (`git rm static/podcast/episodi/2026-05-16-...m4a` + rimozione voci yaml)

Storicamente i podcast NotebookLM hanno breve emivita (max 6 mesi prima che le fonti istituzionali si aggiornino). Ri-generazione ogni 6 mesi è una cadenza ragionevole.

---

## 30.7 Troubleshooting

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Il chip "Tema · N" è muted ("—") dopo che ho pubblicato | Build Hugo non aggiornata, oppure tema slug yaml ≠ slug pagina | Aspetta il deploy (~3 min), poi hard refresh (Ctrl+Shift+R). Se persiste, verifica `data/risorse_pronte.yaml` `temi:` ↔ `materiali:` slug |
| "Materiali pronti su questo tema" non appare sulla pagina rischio | Auto-discovery del tema sbagliato (vedi sezione 30.5 punto 5) | Aggiungi alias in `materiali-correlati.html` |
| Il podcast non appare nel feed RSS | Manca `content/podcast/<slug>.md` oppure `audio:` non popolato | Verifica che lo script abbia creato il content file; se no, crealo manualmente prendendo modello dagli episodi esistenti |
| Player audio inline non funziona su Safari | M4A senza atoms moov spostato all'inizio (faststart) | Esporta da NotebookLM o ri-encode con `ffmpeg -i in.m4a -movflags +faststart out.m4a` |
| Errore "Push fallito" dopo 3 retry | Conflitto concorrenza forte con altri workflow | Lancia manualmente `git pull --rebase origin main && git push` |
| File con estensione non riconosciuta (es. `.docx`) nella drop zone | NotebookLM ha esportato la trascrizione | Rinominalo a mano con estensione adeguata (`.txt`) e lo script lo classifica come trascrizione, oppure ignoralo |

---

## 30.8 Licenza e attribuzione

Tutti i materiali pubblicati su `/risorse-pronte/` sono **Creative Commons CC BY-NC-SA 4.0**:

- **BY**: chi li riusa deve citare "Protezione Civile Genzano di Roma" come fonte
- **NC**: solo uso non commerciale (didattica, formazione interna, divulgazione)
- **SA**: opere derivate devono usare la stessa licenza

Per uso commerciale o istituzionale fuori dal contesto della Protezione Civile, contattare segreteria@protezionecivilegenzano.it.

I materiali generati con NotebookLM **non hanno restrizioni Google** sui contenuti generati: l'output è tuo (vedi <https://policies.google.com/terms/generative-ai>). Le **fonti** caricate restano dei rispettivi titolari (DPC, INGV, ISPRA, ecc.) ma sono opere della PA italiana liberamente riusabili (art. 5 L. 633/1941).

---

## 30.9 Riferimenti

- Script: `scripts/prepara-pacchetto-notebooklm.py`, `scripts/pubblica-notebooklm-output.py`
- Agent: [`.claude/agents/pc-notebooklm-publisher.md`](../.claude/agents/pc-notebooklm-publisher.md)
- Layout hub: `themes/flavour-pcgenzano/layouts/risorse-pronte/list.html`
- Partial cross-link: `themes/flavour-pcgenzano/layouts/partials/materiali-correlati.html`
- Pagina pubblica: <https://www.protezionecivilegenzano.it/risorse-pronte/>
- Feed RSS podcast: <https://www.protezionecivilegenzano.it/podcast/index.xml>
- Guida utente standalone: `~/Scrivania/GUIDA-NOTEBOOKLM-PC-GENZANO.md` (su Desktop)
- NotebookLM: <https://notebooklm.google.com>
- Documentazione NotebookLM: <https://support.google.com/notebooklm>
