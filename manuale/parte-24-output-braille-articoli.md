# Parte 24 — Output Braille-ready per gli articoli (BRF)

Aggiunta a maggio 2026 nell'ambito del **Punto 19 della roadmap accessibilità**.

Il sito genera automaticamente una versione **BRF** (Braille Ready Format) di ogni articolo pubblicato in `content/comunicazioni/`. Il file è ASCII puro, conforme allo standard internazionale BRF/ICEB, pronto per **display braille** e **stampanti braille** (UICI Roma e Biblioteca Italiana per Ciechi di Monza ne usano).

L'utente cieco o ipovedente può scaricare il `.brf` dal bottone "Scarica versione braille" presente sopra ogni articolo, aprirlo sul proprio display braille collegato al PC, o stamparlo su carta braille con una stampante Index, ViewPlus o equivalente.

---

## 24.1 Perché esiste

Lo screen reader è uno strumento eccellente per chi legge col tatto, ma ha tre limiti per un sito istituzionale di Protezione Civile:

1. **Richiede una connessione attiva**: in emergenza, con la rete satura, l'utente potrebbe non riuscire a navigare il sito.
2. **Non è portabile**: un foglio braille stampato si può tenere in tasca, sul comodino, in casa accanto al telefono.
3. **L'audio non è sempre praticabile**: in ambienti rumorosi, in luoghi pubblici, in situazioni di privacy ridotta.

Il file `.brf` colma questi tre limiti: scarica una volta, stampa in casa o in associazione (UICI Roma offre il servizio), conservalo come riferimento permanente. Inoltre apre il sito a un canale di comunicazione **vero** verso ciechi e ipovedenti, non solo "compatibile con screen reader".

## 24.2 Standard tecnici adottati

| Parametro | Valore | Motivazione |
|---|---|---|
| Tabella di traduzione | `it-it-comp6.utb` | Braille italiano a 6 punti standard. Output ASCII puro. È quello che UICI Italia raccomanda per testi correnti. |
| Line width | 40 celle | Standard ICEB per stampanti braille comuni (Index Basic-D, Tiger Cub, ViewPlus Emprint). |
| Page length | 25 righe | Standard ICEB per pagine A4 braille. |
| Form feed | `0x0C` | Carattere ASCII standard delimitatore pagine in BRF. |
| Numerazione | `#N` destra-allineato | Standard braille (cifra preceduta da `#`). |
| Header pagina | Titolo articolo (troncato) + `#N` | Riconoscibilità immediata, ICEB-compliant. |
| Encoding output | ASCII puro (`0x20-0x7E` + `0x0A` + `0x0C`) | Universalmente supportato da stampanti braille. |

**Perché NON `it-it-g1.utb`**: questa tabella è citata in molta documentazione internazionale come "Italian Grade 1", ma NON esiste effettivamente nel pacchetto liblouis upstream. La tabella canonica italiana di liblouis è `it-it-comp6.utb` (6 punti standard, lettera-per-lettera, uncontracted). Comp6 corrisponde di fatto a quello che gli anglofoni chiamano "Grade 1".

**Perché NON `it-it-comp8.utb`** (8 punti, computer braille): produce output Unicode, non ASCII. Non valido come BRF. Adatto solo a display elettronici a 8 punti (usati per programmazione e matematica), non a stampa.

## 24.3 Architettura

Tre componenti, introdotti in tre serate successive:

| Sera | Componente | File toccati |
|---|---|---|
| Sera 1 (12 maggio 2026) | **Script Python** `scripts/genera-braille.py` standalone, esecuzione locale, idempotente, CLI con `--force`/`--limit`/`--article`/`--verbose`. | `scripts/genera-braille.py`, `.gitignore` |
| Sera 2 (futura) | **Integrazione `deploy.yml`**: step apt-install liblouis + esecuzione script prima di `hugo --minify`, output `.brf` finisce in `public/braille/comunicazioni/` e viene deployato su Aruba e GitHub Pages. | `.github/workflows/deploy.yml` |
| Sera 3 (futura) | **Partial HTML** `partials/scarica-braille.html` + integrazione `_default/single.html`: bottone "Scarica versione braille" sopra il corpo articolo, vicino al pulsante "Leggi ad alta voce". | `themes/.../partials/scarica-braille.html`, `themes/.../_default/single.html` |

Questo manuale documenta lo **stato a fine Sera 1** + roadmap per le serate successive.

## 24.4 Path canonici

```
content/comunicazioni/<slug>.md        ← sorgente Markdown (input)
                  ↓
scripts/genera-braille.py              ← generatore Python
                  ↓
static/braille/comunicazioni/<slug>.brf  ← output BRF (ASCII puro)
                  ↓
public/braille/comunicazioni/<slug>.brf  ← copiato da Hugo al build
                  ↓
https://www.protezionecivilegenzano.it/braille/comunicazioni/<slug>.brf
                                       ← URL pubblico (Sera 2+)
```

**`.gitignore`** include `static/braille/` perché i `.brf` sono **rigenerati** ad ogni esecuzione dello script, mai committati.

## 24.5 Preprocessing Markdown → testo piano

La traduzione braille parte da testo piano. Lo script implementa un parser che gestisce:

**Frontmatter YAML**: rimosso completamente (`---` ... `---`). Il titolo viene riusato come intestazione del primo paragrafo del BRF + come header di ogni pagina.

**Shortcode noti**:
- `{{< foto src="..." alt="X" caption="Y" >}}` → `[Foto: X. Didascalia: Y.]`. Alt text e caption preservano l'informazione narrativa dell'immagine.
- `{{< pittogramma src="..." alt="X" >}}` → `[Pittogramma: X.]`.
- `{{< cosa-non-fare >}}body{{< /cosa-non-fare >}}` → `[COSA NON FARE]` come heading + il body interno riprocessato dal pipeline Markdown.
- `{{< chi-chiamare >}}` → testo statico "Chi chiamare in caso di pericolo: 112 (NUE), 115 (VVF), 1515 (CC Forestali)" (lo shortcode genera contenuti dinamici via template Hugo, qui usiamo il testo equivalente).

**Shortcode sconosciuti**: WARNING log + rimozione del tag. Il summary finale stampa l'elenco con conteggio occorrenze, per scoperta incrementale.

**Markdown**:
- `# H1` / `## H2` → testo MAIUSCOLO + righe vuote sopra e sotto
- `### H3+` → Title Case + righe vuote
- `- lista` → `* elemento` (l'asterisco è cella braille standard)
- `1. lista` → preservata letterale
- `**bold**` / `*italic*` → marker rimossi, solo testo (Grade 1 italiano non ha standard di enfasi)
- `[testo](url)` assoluto → `testo (url)`; relativo → solo `testo` (link interni non hanno senso su carta braille)
- Tabelle Markdown pipe-delimited → lasciate così per MVP (resa tabella 2-D ICEB rimandata a future iterazioni)
- ```` ``` code block ``` ```` → prefisso `CODICE:` + body letterale
- `--- ` separatore orizzontale → linea di asterischi

## 24.6 Idempotenza

Lo script confronta `mtime` del `.md` sorgente con quello del `.brf` di destinazione:

```python
if brf_file.exists() and brf_file.stat().st_mtime >= md_file.stat().st_mtime:
    log.debug(f"SKIP-UPTODATE {slug}")
    continue
```

Risultato:
- Primo run su 388 articoli: ~2 minuti totali (parsing + traduzione + scrittura).
- Run successivi (solo articoli modificati): ~0.3 sec × N nuovi articoli. Per un push tipico di 1-2 articoli: <5 sec.

Override con `--force` per rigenerare tutto (es. dopo modifica della tabella di traduzione o del parser).

## 24.7 CLI

```bash
# Tutti gli articoli (idempotente)
python3 scripts/genera-braille.py

# Solo primi N articoli (test)
python3 scripts/genera-braille.py --limit 10

# Forza rigenerazione completa
python3 scripts/genera-braille.py --force

# Solo un articolo specifico (slug)
python3 scripts/genera-braille.py --article 2026-05-12-iso-22324-codici-colore-allerta

# DEBUG logging
python3 scripts/genera-braille.py --verbose
```

Combinabili: `--limit 30 --verbose --force` per test mirati.

## 24.8 Dipendenze sistema

```bash
sudo apt-get install -y python3-louis liblouis-data python3-yaml
```

Verifica:

```bash
python3 -c "import louis; print(louis.version())"   # → 3.x
ls /usr/share/liblouis/tables/it-it-comp6.utb       # → file presente
```

Nessuna installazione `pip install` necessaria. Il pacchetto `python3-louis` Ubuntu/Debian è il binding ufficiale di liblouis mantenuto dalla communità.

## 24.9 Verifica output

Un file `.brf` ben formato:

```bash
# 1. Purezza ASCII: deve dare 0
python3 -c "
data = open('static/braille/comunicazioni/<slug>.brf','rb').read()
bad = sum(1 for b in data if not (0x20 <= b <= 0x7E or b == 0x0A or b == 0x0C))
print(f'Byte non-validi: {bad}')
"

# 2. Ispezione visiva con xxd
xxd static/braille/comunicazioni/<slug>.brf | head -10
# Atteso: bytes ASCII visibili (lettere, simboli braille codificati ASCII,
# spazi 0x20, newline 0x0A, eventualmente form-feed 0x0C tra pagine).

# 3. Anteprima con BRF viewer online (es. https://brltranslator.com)
# Caricare il file e leggere il testo italiano risultante.
```

## 24.10 Caratteri italiani — mappa braille comp6

| Carattere | Cella braille (ASCII) |
|---|---|
| `a-z` | minuscole | `a-z` |
| `A-Z` (maiuscole) | prefisso `.` (singola) o `\`,` (parola intera) |
| `é` | `=` |
| `è` | `!` |
| `à` | `(` |
| `ì` | `/` |
| `ò` | `9` |
| `ù` | `)` |
| Cifre `0-9` | prefisso `#` + lettere `a-j` (es. `12` → `#ab`) |
| Punteggiatura `.,;:?!` | varianti ASCII standard |

Test rapido in Python:

```python
import louis
samples = ['perché', 'qualità', 'città', 'è', "l'allerta", 'così', 'più']
for s in samples:
    print(f"{s!r:20} → {louis.translateString(['it-it-comp6.utb'], s)!r}")
```

## 24.11 Cosa NON entra nell'MVP (rimandato)

Coerente con l'assessment Punto 19:

1. **Tabelle complesse**: resa 2-D ICEB richiederebbe `liblouisutdml` (XML→braille con styling). Per ora le tabelle Markdown restano pipe-delimited.
2. **Multilingua**: le 7 traduzioni (`/english/`, `/francais/`, ...) usano tabelle diverse (`en-us-g1.ctb`, `fr-bfu-comp8.utb`, ecc.). Fuori MVP.
3. **Indice generale `.brf`** di tutti gli articoli (catalogo navigabile): possibile Versione 2.
4. **Opzione utente "Grade 1 / Comp 8 / Grade 2"** via dropdown sulla pagina: MVP genera solo comp6.
5. **Output PEF** (Portable Embosser Format, XML moderno): BRF è universalmente supportato dalle stampanti esistenti.
6. **Pagine non-comunicazioni** (rischi/prevenzione, FAQ, kit calamità): hanno shortcode complessi che richiederebbero handler dedicati.
7. **Anteprima braille a schermo** con font Unicode braille (`U+2800-U+28FF`): valutabile dopo MVP.

## 24.12 Test di accettazione UICI

Per validare la qualità reale del BRF prima di pubblicizzarlo come servizio:

1. Stampare 3 articoli campione (uno breve, uno medio, uno lungo) su carta braille con stampante UICI Roma.
2. Far leggere a un lettore braille esperto (volontario UICI o operatore della Biblioteca Italiana per Ciechi).
3. Raccogliere feedback su: leggibilità, gestione delle sigle (NUE, COC, DPC), corretto rendering accenti, paginazione, intestazione.
4. Se serve, calibrare le scelte di preprocessing (es. espandere le sigle in chiaro la prima volta, formato date più verboso, ecc.).

Test pianificato per **giugno 2026** (post-Sera 2 + Sera 3, quando il bottone download è pubblicamente disponibile).

## 24.13 Riferimenti

- **Liblouis** — libreria di traduzione braille open source, mantenuta da Sebastian Andersson e community: <https://liblouis.io/>
- **Standard ICEB** — International Council on English Braille per BRF/embosser conventions: <http://www.iceb.org/>
- **UICI Roma** — Unione Italiana Ciechi e Ipovedenti, sede di Roma: <https://www.uicilazio.it/>
- **Biblioteca Italiana per Ciechi "Regina Margherita"** — Monza, sede storica della trascrizione braille italiana: <https://www.bibciechi.it/>
- **Assessment Punto 19 della roadmap** — documentato nelle conversazioni Claude Code maggio 2026.
