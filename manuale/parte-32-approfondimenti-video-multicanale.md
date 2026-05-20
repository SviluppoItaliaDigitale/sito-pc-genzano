# Parte 32 — "Approfondimenti video" multi-canale

> **Cos'è**: la sezione "Approfondimenti video" che appare in fondo a quasi tutte le pagine del sito (sfondo lavanda pastello AGID, border viola istituzionale) con 1-5 link a video YouTube pertinenti al contenuto della pagina. Il sistema è automatico: nessun intervento manuale richiesto al docente o all'editore quando si crea un nuovo articolo.
>
> **Pattern**: link puro, niente embed YouTube (privacy AGID, niente cookie di terze parti).
>
> **Aggiornamento**: ogni 1° del mese via workflow GitHub Actions `aggiorna-video-correlati.yml`.

---

## 32.1 Architettura in 4 pezzi

```
[YouTube] ──scrape──▶ data/video_dpc_catalogo.yaml ──cross-match──▶ data/video_correlati.yaml ──Hugo──▶ HTML
   12 canali IT        ~5000-15000 video                  mappa pagina→top-5 video           sezione in pagina
```

| Pezzo | File | Ruolo |
|---|---|---|
| 1 | `scripts/scrape-catalogo-video.py` | Interroga YouTube via `yt-dlp` per ciascun canale del dict `CANALI`, salva l'elenco completo dei video |
| 2 | `data/video_dpc_catalogo.yaml` | Catalogo grezzo. ID, titolo, URL, canale per ogni video |
| 3 | `scripts/genera-video-correlati.py` | Algoritmo IDF-weighted di cross-match titolo video ↔ contenuto pagina sito, con filtro lessicale per canali divulgativi |
| 4 | `data/video_correlati.yaml` | Mappa finale: ogni pagina del sito → max 5 video YouTube pertinenti ordinati per score |
| 5 | `themes/flavour-pcgenzano/layouts/partials/video-correlati.html` | Partial Hugo che legge la mappa e renderizza la sezione in fondo alla pagina |
| 6 | `themes/flavour-pcgenzano/static/css/custom.css` (sez. VIDEO CORRELATI v1.0) | Stile lavanda pastello AGID |
| 7 | `.github/workflows/aggiorna-video-correlati.yml` | Run mensile automatico |

---

## 32.2 Canali monitorati (al 2026-05-19)

### Tematici PC — nessun filtro (5 canali)

Sono canali la cui produzione è **tutta** pertinente alla Protezione Civile. Ogni video passa direttamente al cross-match.

| Canale | Handle YouTube | Tipico contenuto |
|---|---|---|
| **Dipartimento Protezione Civile** | `@DPCgov` | Comunicati ufficiali, esercitazioni nazionali, eventi PC |
| **Io non rischio** | `@io_non_rischio` | Campagna nazionale DPC + ANPAS + INGV + RELUIS + CIMA |
| **Abili a Proteggere** | `@abiliaproteggere4520` | Video LIS per persone sorde, Cooperativa Europe Consulting |
| **INGV terremoti** | `@INGVterremoti` | Sismologia, monitoraggio, divulgazione terremoti |
| **INGV vulcani** | `@INGVvulcani` | Vulcanologia (Vesuvio, Etna, Campi Flegrei, Stromboli) |

### Divulgativi qualificati — con filtro lessicale PC (7 canali, tutti italofoni)

Canali con produzione eterogenea. Solo i video il cui titolo contiene almeno una keyword PC (su ~250 keyword di `DIVULGATIVO_PC_KEYWORDS`) entra nel cross-match. **Policy editoriale 19 maggio 2026: solo canali in lingua italiana**, nessun canale in lingua straniera.

| Canale | Handle YouTube | Tipico contenuto rilevante |
|---|---|---|
| **Geopop** | `@geopop` | Ricostruzioni 3D di disastri geologici (Vajont, Sarno, Pompei, Bhopal) |
| **National Geographic Italia** | `@natgeoit` | Documentari ambiente, climate, disastri storici (edizione italiana, voce italiana) |
| **Rai Cultura** | `@raicultura` | Documentari storici (eventi memoria) |
| **Rai News** | `@RaiNews` | Notizie italiane, emergenze attuali |
| **CICAP** | `@CICAP_it` | Fact-checking scientifico, fake news scientifiche |
| **Link4Universe** | `@link4universe` | Astronomia, asteroidi, impatti cosmici |
| **Wired Italia** | `@WiredItalia` | Tech, climate, disastri nucleari (Chernobyl) |

**Canali rimossi nell'ottimizzazione 19 maggio 2026:**

| Canale rimosso | Motivo |
|---|---|
| **Sky TG24** (`@SkyTG24`) | Eccesso di rumore (notizie politiche/economiche non pertinenti) anche col filtro lessicale; rapporto segnale/rumore basso |
| **TGCom24** (`@TgCom24`) | Stesso pattern: troppe notizie generiche che attraversavano il filtro lessicale come falsi positivi |

### Tentati e scartati

Canali che **non hanno** un canale YouTube attivo, o l'handle non corrisponde a un canale ricco di video pertinenti: ISPRA, Vigili del Fuoco (nazionale), Croce Rossa Italiana, CNR, Focus, CMCC, EuroNews Italiano, Rai Documentari, TG1, Corriere, La Repubblica.

Questi enti pubblicano principalmente su **siti istituzionali**, **social non-video** (Twitter/X, Facebook), **archivi web** custom. Aggiungere scraper HTML personalizzati è fragile e poco mantenibile; salto.

---

## 32.3 Logica di filtro lessicale (`DIVULGATIVO_PC_KEYWORDS`)

La whitelist è in `scripts/genera-video-correlati.py`, ~250 keyword italiane e inglesi su 17 categorie tematiche:

1. **Sismico**: terremoto/i, sisma, magnitudo, faglia, epicentro, tettonica, earthquake, seismic...
2. **Vulcanico**: vulcano, eruzione, lava, magma, Vesuvio, Etna, Stromboli, Campi Flegrei, Krakatoa, Pompei...
3. **Tsunami**: tsunami, maremoto, onda anomala
4. **Idrogeologico**: frana, alluvione, dissesto, esondazione, valanga, sinkhole, nubifragio
5. **Incendi**: incendio, AIB, antincendio, wildfire, bushfire
6. **Meteo estremo**: ondata di caldo, heatwave, tempesta, uragano, tornado, vento forte, nubifragio
7. **Blackout/infrastrutture**: blackout, diga, Vajont, ponte crollato, Morandi
8. **Chimico/nucleare**: chimico, radioattivo, nucleare, Chernobyl, Fukushima, Seveso, Bhopal, dioxin
9. **Disastri**: disastro, calamità, catastrofe, emergenza, disaster
10. **Eventi storici Italia**: Aquila, Amatrice, Sarno, Irpinia, Friuli, Belice, Vajont, Vermicino, Torri Gemelle...
11. **Climate change**: clima, climate change, global warming, siccità, El Niño
12. **Pandemie**: pandemia, epidemia, Covid, SARS, Spagnola, peste nera
13. **Protezione civile**: protezione civile, civil protection, soccorso, evacuazione, rescue
14. **PC europea**: UCPM, ERCC, rescEU, Copernicus EMS
15. **Primo soccorso**: primo soccorso, BLS, BLSD, DAE, RCP, defibrillator, Heimlich
16. **Inclusione/disabilità**: disabilità, accessibilità, persone vulnerabili, DiDRR, Sendai
17. **Comunicazione di crisi**: fake news, IT-alert, Cell Broadcast, ISO 22324/22329/22361/22395

Il match è **substring case-insensitive**. Es. "terremot" cattura "terremoto", "terremoti", "terremoteggiato" (raro).

---

## 32.4 Algoritmo IDF-weighted di cross-match

Per ogni pagina del sito:

1. **Tokenizza** il titolo, la description (frontmatter), il corpo (primi 3000 caratteri + headings H2/H3).
2. **Calcola peso IDF** di ogni keyword: parola comune nel sito → peso 0.2, parola moderatamente frequente → 0.6, parola rara/tecnica → 1.0.
3. **Confronta** le keyword della pagina con le keyword del titolo di ogni video del catalogo.
4. **Score posizionale**: keyword nel titolo della pagina × 3, in description × 2, nel corpo × 1.
5. **Filtri qualità**:
   - **Anchor**: almeno una keyword in overlap deve essere nel titolo o description della pagina (non solo nel corpo).
   - **Anchor IDF >= 0.5**: l'anchor non deve essere una parola super-generica.
   - **🔴 Gate tematico (difesa strutturale, 20/05/2026)**: almeno una parola-ancora dev'essere **PC-tematica e specifica**. Si verifica con `_anchor_is_topical_specific()`, che usa gli stem topici derivati da `DIVULGATIVO_PC_KEYWORDS` + `TOPICAL_ANCHOR_SHORT` (sigle: coc, dae, 112…) + luoghi-disastro (`emilia`, `genova`, `nemi`…). I termini PC **troppo astratti** (`TOPICAL_BROAD_STEMS`: crisi, disastro, ricostruzione, tragedia, emergency…) **non bastano da soli**: servono con un co-aggancio specifico. Questo impedisce gli agganci su parole generiche che, essendo rare nel corpus del sito, prendevano peso IDF pieno e diventavano "ancore forti" pur non c'entrando nulla (l'IDF è calcolato solo sul sito). La sola whitelist `STOPWORDS_IT` era whack-a-mole.
   - **Per canali divulgativi non-tematici**: vincolo extra `IDF >= 0.7` sull'anchor (parola tecnica, non comune).
   - **Denylist video** (`DENY_VIDEO_IDS`): esclusione per ID YouTube dei falsi positivi di ultimo miglio (parola topica ma contesto non-PC: "palle di neve", "Masai Kenya"…).
   - **Score >= 2.0**.
6. **Ordina** i video per score decrescente, prende i **top 5**.

> **Principio editoriale (regola permanente, 20/05/2026): video pertinente o niente sezione.** Se nessun video del catalogo condivide con la pagina un'ancora PC-tematica specifica, la pagina **non ha** la sezione "Approfondimenti video". Vale per tutti gli articoli, passati e futuri: meglio nessun video che un video sbagliato. È il motivo per cui la copertura è scesa da ~494 a ~125 pagine il 20/05/2026 (le pagine non-topiche — auguri, bilanci, ricorrenze — correttamente non hanno video).

Risultato: la mappa `data/video_correlati.yaml` ha per ogni `key` (path della pagina) la lista dei top 5 video con score, overlap, anchor.

---

## 32.5 Stile UI — "Approfondimenti video" pastello AGID

La sezione è renderizzata dal partial `partials/video-correlati.html` chiamato in fondo ai template `_default/single.html`, `_default/list.html`, `rischi-prevenzione/single.html`, `risorse-pronte/list.html`.

Stile (CSS sezione "VIDEO CORRELATI v1.0" in `custom.css`):

- **Sfondo**: `#f5f0fb` (lavanda chiarissima, contrasto AAA con testo nero 16:1)
- **Border-left**: 5px solido `#6b21a8` (viola istituzionale, palette nuclei Ed. Civica)
- **Border esterno**: `#d9c7e8`
- **Border radius**: 12px
- **Watermark**: icona `bi-play-circle-fill` in alto a destra, opacità 18%
- **H2**: `#4a1d96` per contrasto AAA su sfondo
- **Card video**: sfondo bianco, hover viola con ombra
- **Focus outline**: `#ffbe2e` 3px (WCAG 2.4.7)

Coerente con il sistema pastello AGID del sito (`.strumenti-articolo` azzurro pastello blu, `.cosa-non-fare` rosato pastello rosso).

---

## 32.6 Pagine escluse dal cross-match

`scripts/genera-video-correlati.py` ha un `SKIP_PAGE_PATTERNS` che esclude:

- **Pagine legali**: `/privacy/`, `/note-legali/`, `/accessibilita/`, `/social-media-policy/`
- **Pagine di servizio**: `/mappa-sito/`, `/cerca/`, `/feed-rss/`, `/siti-utili/`, `/trasparenza/`, `/open-data/`, `/stato-sistema/`
- **Hub audio**: `/podcast/`, `/articoli-da-ascoltare/`, `/audio-e-podcast/` (hanno già contenuti audio)
- **Hub LIS**: `/lis/` (ha già tutti i video LIS)
- **Assistente**: `/assistente/`
- **Traduzioni**: `/english/`, `/francais/`, `/deutsch/`, `/espanol/`, `/portugues/`, `/romana/`, `/esperanto/`
- **Hub formazione**: `/formazione/` (root)

---

## 32.7 Come aggiungere un nuovo canale

```python
# In scripts/scrape-catalogo-video.py, nel dict CANALI:

"mio-nuovo-canale": {
    "nome": "Nome leggibile del canale",
    "url": "https://www.youtube.com/@mioHandle/videos",
    "tematico_pc": True,  # True se ogni video è già pertinente PC
                          # False se è un canale divulgativo generale
                          # (in tal caso si applica il filtro lessicale)
},
```

Poi:

```bash
# Test locale (limitato a 5 video per evitare attese):
python3 scripts/scrape-catalogo-video.py --limit 5 --output /tmp/test.yaml

# Se OK, lancia scrape completo:
python3 scripts/scrape-catalogo-video.py

# Rigenera mappa:
python3 scripts/genera-video-correlati.py

# Build Hugo + commit:
hugo --quiet --minify --baseURL "https://www.protezionecivilegenzano.it/"
git add scripts/ data/
git commit -m "Aggiunge canale Nome al cross-match video"
git push origin main
```

Il workflow mensile poi mantiene il canale aggiornato.

### Verifica handle YouTube

YouTube ha 3 forme di URL canale che yt-dlp accetta:

- `https://www.youtube.com/@handle` (formato moderno, preferito)
- `https://www.youtube.com/c/legacy-name` (formato legacy)
- `https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxxxxx` (channel ID, sempre stabile)

Per verificare se un handle esiste prima di committarlo:

```bash
yt-dlp --flat-playlist --playlist-end 1 --print "%(title)s" "https://www.youtube.com/@HANDLE/videos"
```

Se la risposta è `ERROR ... 404` o `does not have videos tab`, l'handle non funziona. Provare varianti, oppure cercare il channel ID dal canale aprendo il sito in browser → impostazioni → "Avanzato" → channel ID.

---

## 32.8 Come escludere un falso positivo

🔴 **Regola: meglio nulla che un video sbagliato.** Se un match non è chiaramente pertinente, va tolto; se una pagina non ha video pertinenti, resta senza sezione. Niente "riempitivi".

⚠️ **NON** usare `data/video_correlati.yaml` come unico punto di fix: è **rigenerato** ogni mese dal workflow, quindi una rimozione manuale dal file viene **persa**. I fix vanno nel **generatore** (`scripts/genera-video-correlati.py`), così persistono.

**Opzione A — denylist del singolo video (preferita per il falso positivo "di ultimo miglio")**

Quando un video ha una parola topica ma un contesto non-PC (es. "Una battaglia di palle di neve" su `neve`, "Una giornata con i Masai" su `siccità`), nessun filtro a keyword lo distingue. Si esclude per ID YouTube:

```python
# In scripts/genera-video-correlati.py:
DENY_VIDEO_IDS = {
    "A1QE73885gQ",  # palle di neve (svago, non emergenza)
    # ...aggiungi qui l'ID del video fuori tema.
}
```

L'ID è nel campo `url: https://youtu.be/<ID>` della voce nel file YAML.

**Opzione B — parola generica che ancora troppo: aggiungila a `STOPWORDS_IT`**

Solo per parole **davvero non-topiche** (astratte/comuni: "presenta", "fatta", "europa", "storia"). ⚠️ **Mai** mettere in stopword un termine PC o un luogo-disastro (es. `aquila`, `emilia`, `vajont`): serve come ancora topica legittima.

**Opzione C — termine PC troppo astratto che aggancia tutto: spostalo in `TOPICAL_BROAD_STEMS`**

Se un termine PC reale ma generico (es. `crisi`, `disastro`, `ricostruzione`) aggancia pagine non correlate, va in `TOPICAL_BROAD_STEMS`: resta valido solo con un co-aggancio specifico, mai da solo.

**Opzione D — keyword di vocabolario troppo larga: restringila in `DIVULGATIVO_PC_KEYWORDS`**

Per i canali divulgativi, sostituisci keyword generiche con forme contestualizzate (es. `"nuclear"` → `"incidente nucleare"`, `"chernobyl"`, `"fukushima"`).

Dopo ogni fix: `python3 scripts/genera-video-correlati.py` → verifica il diff → commit. Il fix si propaga automaticamente ai rigeneri mensili successivi.

---

## 32.9 Soglie editoriali (`--min-score`, `--max-per-page`)

Default:

- `--min-score 2.0` — score minimo per accettare un match
- `--max-per-page 5` — max 5 video correlati per pagina

Per **più copertura** (più match, meno qualità):

```bash
python3 scripts/genera-video-correlati.py --min-score 1.5 --max-per-page 6
```

Per **meno copertura** (meno match, alta qualità):

```bash
python3 scripts/genera-video-correlati.py --min-score 3.0 --max-per-page 3
```

La scelta editoriale attuale (`2.0 / 5`) bilancia 90% di copertura del sito con qualità accettabile dei match.

---

## 32.10 Numeri di riferimento (2026-05-19)

| Metrica | Valore |
|---|---|
| Canali monitorati | 13 |
| Video totali catalogati | ~5000-15000 (dipende dal periodo) |
| Video divulgativi scartati dal filtro PC | ~70% del catalogo divulgativi |
| Pagine del sito analizzate | 538 |
| Pagine con almeno 1 video correlato | ~490 (91%) |
| Video unici usati | ~600 |
| Link video totali distribuiti | ~1900 |
| Distribuzione canali (% link) | Geopop 33%, DPCgov 22%, AaP 13%, INGV-terr 9%, Io non rischio 6%, CICAP 5%, INGV-vulc 4%, Wired 3%, Link4U 2%, NatGeo 1% + altri |

---

## 32.11 Privacy e licenze

- **Niente embed**: la sezione mostra solo **link** (target=_blank, rel="noopener noreferrer") al video su YouTube. Nessun iframe, nessuna chiamata JS a YouTube, niente cookie di terze parti.
- **AGID conforme**: nessuna richiesta di consenso cookie addizionale è necessaria (i link sono HTML standard).
- **Copyright**: i video restano sul canale del produttore; il sito linka soltanto. Non si pubblicano trascrizioni dei video se non disponibili pubblicamente.
- **Attribuzione**: ogni link mostra il **nome del canale** accanto al titolo del video (es. "Il disastro del Vajont — Geopop").

---

## 32.12 Riferimenti incrociati

- **Workflow GitHub Actions**: `.github/workflows/aggiorna-video-correlati.yml`
- **Rule rilevante**: `.claude/rules/10-automazioni-github-actions.md` § `aggiorna-video-correlati.yml`
- **CSS sezione**: `themes/flavour-pcgenzano/static/css/custom.css` § VIDEO CORRELATI v1.0
- **Partial Hugo**: `themes/flavour-pcgenzano/layouts/partials/video-correlati.html`
- **Companion check video DPC eventi**: `.github/workflows/check-video-dpc-eventi.yml` (bi-mensile, segnala video DPC nuovi via issue)
- **Companion check video LIS**: `.github/workflows/check-video-lis.yml` (settimanale, gestisce video LIS in `data/lis.yaml`)
- **Architettura statica**: `.claude/rules/04-hugo-architecture.md`

---

**Ultimo aggiornamento**: 19 maggio 2026.
