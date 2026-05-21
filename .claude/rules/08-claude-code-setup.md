# Claude Code — Setup ambiente di sviluppo

Questo file documenta come configurare l'ambiente di Claude Code per lavorare sul sito senza essere bloccato dalla sandbox di sicurezza, in particolare per il download di foto da fonti libere e per la lettura di siti istituzionali con SPA JS o anti-bot.

## Firecrawl MCP — canale primario per siti SPA/anti-bot/SSL-CA-restricted

🟢 **Installato 19 maggio 2026** come MCP server stdio scope user (`firecrawl-mcp` v3.17.0 via `npx`, API key in env `FIRECRAWL_API_KEY`). Tier free: **500 pagine/mese**, 10 req/min.

**Quando usare Firecrawl al posto di WebFetch:**

- Siti **SPA JavaScript** (Next.js, React, Vue) dove WebFetch riceve solo "Loading..." o language selector
- Siti con **anti-bot WAF** (Cloudflare, Akamai) che restituiscono 403 a WebFetch
- Siti con **certificati SSL su CA non incluse nella sandbox** Claude Code (`.gov.it`/`.giustizia.it` con CA Sogei o simili) — Firecrawl gira su infra con CA store completo
- Pagine di **bollettini PDF** rese dinamicamente dietro JS

**Quando NON usare Firecrawl:**

- Siti **già leggibili via WebFetch** (Normattiva, GU, Camera, Regione Lazio, Wikipedia): risparmia pagine del tier.
- **Download diretto di file** (PDF, foto): usa `curl` con l'allowlist sandbox.
- Siti con **DNS failure/ECONNREFUSED**: il sito è realmente offline, nessun proxy lo risuscita.

**Quadro siti istituzionali al 19 maggio 2026 (test batch 13 URL):**

| Sito | Pre-Firecrawl | Post-Firecrawl |
|---|---|---|
| DPC `www.protezionecivile.gov.it` | SPA "Loading..." | ✅ 11.458 char markdown |
| EUR-Lex `eur-lex.europa.eu` | Contenuto vuoto | ✅ 6.085 char |
| DG ECHO `civil-protection-humanitarian-aid.ec.europa.eu` | Solo language selector | ✅ Leggibile (poche righe per home, ma pagine interne OK) |
| UNDRR `www.undrr.org` | 403 anti-bot | ✅ 13.204 char |
| OCHA `www.unocha.org` | 403 anti-bot | ✅ 25.285 char |
| Crusca `accademiadellacrusca.it` | 403 anti-bot | ✅ 12.386 char |
| Europeana `www.europeana.eu` | 403 anti-bot | ✅ 22.147 char |
| Library of Congress `www.loc.gov` | 403 anti-bot | ✅ 18.056 char |
| Senato `www.senato.it` | 403 anti-bot | ✅ 17.303 char |
| Quirinale `www.quirinale.it` | 403 anti-bot | ✅ 7.712 char |
| Giustizia Amministrativa `www.giustizia-amministrativa.it` | SSL CA error | ✅ 33.583 char (era problema CA store sandbox) |
| ENEA `www.enea.it` | SSL error | ✅ 36.086 char |
| INGV terremoti `terremoti.ingv.it` | SSL error | ✅ 34.419 char con lista terremoti realtime |

**Siti che restano inaccessibili anche con Firecrawl:**

| Sito | Motivo | Note |
|---|---|---|
| **Geoportale Nazionale MASE** (`gn.mase.gov.it`) | WAF aggressivo (Access Denied 207 byte) | Sicurezza lato server, non risolvibile lato client |
| **Cassazione SentenzeWeb** (`italgiure.giustizia.it`) | Timeout 30s (HTTP 408) | Sito raggiungibile ma lento; aumentare `timeout: 60000` nel JSON request o retry |
| **Comune Genzano** (`www.comune.genzanodiroma.rm.it`) | DNS resolution failed | Dominio davvero non risponde — sito offline o cambio URL |
| **USR Lazio** (`www.lazio.istruzione.it`) | ECONNREFUSED | Server offline; cercare endpoint alternativo |
| **protezionecivile.regione.lazio.it** | ECONNREFUSED | Sotto-sito offline; usare `www.regione.lazio.it` |

**Comando Firecrawl via MCP (sessione Claude Code):**

Una volta riavviata la sessione dopo l'install, i tool MCP `mcp__firecrawl__scrape` (e `_crawl`, `_map`, `_search`) sono direttamente invocabili. Esempio in conversazione: *"usa Firecrawl per leggere la homepage DPC e estrarre allerta meteo nazionale"*.

**Comando Firecrawl via curl (qualsiasi sessione, anche cloud-side):**

```bash
curl -s -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "<URL>", "formats": ["markdown"], "onlyMainContent": true, "timeout": 30000}'
```

**Costo per pagina:** 1 page del tier free. Funzionalità avanzate (`crawl` multi-pagina, `search`, `extract` LLM-powered) consumano da 1 a 5 pagine per chiamata.

**Workflow editoriale aggiornato:**

1. **Lettura singola URL nota** (es. circolare DPC specifica, sentenza Corte Costituzionale): Firecrawl `scrape` → 1 page.
2. **Sweep multi-pagina dello stesso dominio** (es. tutti i comunicati DPC del mese): Firecrawl `crawl` con `maxDepth: 2` e `limit: 20` → ~20 page.
3. **Ricerca trasversale tematica** (es. "circolari volontariato PC 2026"): Firecrawl `search` → 5 page.
4. **Estrazione strutturata** (es. tutti i numeri di articolo + data di un atto): Firecrawl `extract` con schema JSON → 1-5 page.

**Aggiornamenti workflow CI futuri**: il workflow `.github/workflows/normativa-watcher.yml` può aggiungere il DPC come fonte monitorata (oggi è in whitelist `08-claude-code-setup.md` ma resta inutilizzabile via WebFetch). Costo stimato: ~10 page/mese sul tier free.

## Playwright MCP — browser automation per smoke test post-deploy

🟢 **Installato 19 maggio 2026** come MCP server stdio scope user. Niente API key.

⚠️ **Riconfigurato 21 maggio 2026 — usa il Google Chrome di sistema (non il browser-bundle).** Su **Ubuntu 26.04** il browser-bundle di Playwright NON è installabile: `npx playwright install chromium` fallisce con `ERROR: Playwright does not support chromium on ubuntu26.04-x64` (vale anche per playwright 1.60). Per questo il vecchio server `@executeautomation/playwright-mcp-server` andava in `✗ Failed to connect`. Fix applicato (persistente in `~/.claude.json`, scope user):

```bash
claude mcp remove playwright -s user
claude mcp add playwright -s user -- npx -y @playwright/mcp@latest --browser chrome --no-sandbox
claude mcp list   # deve mostrare: playwright ... ✓ Connected
```

Ora usa il **Google Chrome di sistema** (`/usr/bin/google-chrome-stable`, Chrome 141; headless verificato su Normattiva). Browser disponibili sulla macchina: `google-chrome-stable` (deb) e `chromium` (snap). **I tool `mcp__playwright__*` (e `mcp__firecrawl__*`) compaiono nella sessione solo dopo un riavvio di Claude Code** (gli MCP si agganciano all'avvio). Insieme a Firecrawl (JS-render + anti-bot + SSL) coprono la lettura *verbatim* dei siti istituzionali, incluse le pagine dinamiche con click (es. scheda "Aggiornamenti all'atto" di Normattiva) — utile per la verifica normativa anti-allucinazione.

**Quando usare Playwright al posto di WebFetch/Firecrawl:**

- **Smoke test live post-deploy**: clic veri sui bottoni, scroll fino a certi elementi, verifica che JS lato client esegua, screenshot di pagine specifiche.
- **Test interattivi del FAB accessibilità**: aprire il dialog, cambiare contrasto, verificare che il sito si ridipinga.
- **Verifica funzionamento moduli JS** (assistente, Pagefind, glossario inline) con browser reale.
- **Reproduce bug visual-only** che `pc-deploy-validator` (HTTP-only) e Lighthouse non catturano.

**Quando NON usare Playwright:**

- Per leggere contenuto testuale di una pagina (usa WebFetch o Firecrawl, molto più veloci).
- Per audit accessibility (usa Lighthouse + axe-core, sono specifici).

**Integrazione con agent esistenti:**
- `pc-deploy-validator` (Bash-only oggi) può aggiungere uno step opzionale di smoke test interattivo prima dell'OK al merge.
- `browser-qa` skill globale ECC trova qui il backend operativo concreto.

---



## Sandbox CLOUD vs sandbox LOCALE — non sono la stessa cosa

⚠️ **Distinzione critica scoperta il 9 maggio 2026** (test diretto sui domini di rete dalla sessione cloud):

Tutto quanto descritto sopra (file `.claude/settings.local.json` + tabella delle 7 fonti foto) **vale solo per la sandbox LOCALE** — quella di Claude Code CLI eseguito sul PC dell'utente. Le sessioni di Claude Code **CLOUD** (mobile, web, agent GitHub-integrato) hanno una whitelist di rete **completamente diversa**, gestita lato Anthropic, **non modificabile dall'utente**, indipendente dal `.claude/settings.local.json` (che è in `.gitignore` e quindi non viene letto in cloud).

### Whitelist effettiva sandbox CLOUD (testata 2026-05-09)

| Dominio | Stato cloud | Note |
|---|---|---|
| `github.com` | ✅ 200 | clone, push (ma il push avviene via GitHub MCP server interno, non curl) |
| `raw.githubusercontent.com` | ✅ 301 | lettura file singoli da repo pubblici |
| `pypi.org`, `files.pythonhosted.org` | ✅ 200 | `pip install` funziona |
| `registry.npmjs.org` | ✅ 200 | `npm install` funziona |
| `archive.ubuntu.com` | ✅ 200 | `apt update` funziona (ma serve sudo) |
| `api.github.com` | ❌ 403 | bloccato — usare i tool MCP `mcp__github__*` |
| **TUTTE le 14 sorgenti foto** (Wikimedia, NASA, USGS, NOAA, Pexels, Pixabay, Unsplash) | ❌ 403 `host_not_allowed` | **non scaricabili dalla sessione cloud** |
| `deb.debian.org` | ❌ 403 | bloccato |

### Conseguenza operativa

Le foto inline `{{< foto >}}` da fonti esterne (Wikimedia/NASA/USGS/NOAA/stock) **non possono essere scaricate dalle sessioni cloud**. La procedura `pc-image-fixer` (WebFetch + curl + applica-fascia) funziona **solo** dal Claude Code CLI sul PC dell'utente con `.claude/settings.local.json` configurato.

Tre flussi praticabili:

1. **Locale (PC)**: l'utente apre Claude Code CLI sul PC → l'agent `pc-image-fixer` fa tutto. Sandbox sbloccata via `.claude/settings.local.json`.
2. **Cloud + utente che fornisce la foto**: l'utente carica/incolla un file immagine già scaricato → la sessione cloud lo legge dal filesystem temporaneo, applica fascia blu (Pillow è installabile via pip che è whitelistato), inserisce shortcode. Niente download esterno richiesto.
3. **Workflow CI**: il workflow `scarica-foto-automatica.yml` su GitHub Actions ha **rete libera** (runner Ubuntu standard) e può scaricare da qualsiasi fonte. Lo step 2 (`auto-cover-mancanti.py`) genera comunque la cover tipografica banner per ogni articolo con `image: ""`. Lo step 1 (download foto inline) era basato sui marker `# TODO-foto-*` che sono **banditi** dal 3 maggio 2026 (CLAUDE.md punto 9): non c'è quindi un meccanismo CI per le foto inline.

### Cosa funziona dalla sandbox cloud

- Lettura/scrittura file del repo (Read, Edit, Write, Bash su file locali).
- Build Hugo (se Hugo è preinstallato) o test sintassi.
- Tool MCP per GitHub (`mcp__github__create_pull_request`, `merge_pull_request`, ecc.).
- `pip install <pacchetto>` e `npm install <pacchetto>` per dipendenze toolchain.
- Pillow installabile al volo per applicare la fascia blu **se la foto sorgente è già nel filesystem**.

### Cosa NON funziona dalla sandbox cloud

- `curl` o `WebFetch` verso Wikimedia/NASA/USGS/NOAA/Pexels/Pixabay/Unsplash → `403 host_not_allowed`.
- `git push` di file `.claude/settings.local.json` per sbloccare la rete: il file resterà comunque ignorato dalla sandbox cloud (la whitelist è di sistema, non di repo).
- Modificare la whitelist di rete della sessione cloud: non è esposta al codice utente.

### Cosa NON fare

- **Non promettere all'utente cloud-side che si possono scaricare foto da fonti esterne** in questa sessione: causa frustrazione (è successo il 9 maggio 2026 con l'articolo Giornata dell'Europa, da cui questa sezione).
- **Non aggiungere domini di sorgenti foto a `.claude/settings.local.json` come "fix per il cloud"**: il file non viene letto in cloud, resta utile solo in locale.

---

## Sandbox LOCALE — sblocco per fonti foto (configurazione descritta sopra)

Quanto segue vale solo per **Claude Code CLI eseguito sul PC dell'utente**. Per la sandbox cloud vedi sezione precedente.

Claude Code esegue in una sandbox di sicurezza che, di default, blocca:

- chiamate di rete verso domini non in allowlist;
- scrittura file fuori dalla working directory;
- comandi considerati rischiosi (`rm -rf`, `dd`, ecc.).

Per il nostro flusso editoriale serve **rete libera verso le fonti foto** (Wikipedia, Wikimedia Commons, NASA Image Library, USGS) e basta. Tutto il resto resta sandboxato.

## File `.claude/settings.local.json`

In `.gitignore` (preferenza locale, non di repo). Schema completo:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "WebFetch(domain:*.wikipedia.org)",
      "WebFetch(domain:commons.wikimedia.org)",
      "WebFetch(domain:upload.wikimedia.org)",
      "WebFetch(domain:*.nasa.gov)",
      "WebFetch(domain:earthquake.usgs.gov)",
      "WebFetch(domain:*.usgs.gov)",
      "WebFetch(domain:*.noaa.gov)",
      "WebFetch(domain:weather.gov)",
      "WebFetch(domain:api.pexels.com)",
      "WebFetch(domain:images.pexels.com)",
      "WebFetch(domain:pixabay.com)",
      "WebFetch(domain:cdn.pixabay.com)",
      "WebFetch(domain:api.unsplash.com)",
      "WebFetch(domain:images.unsplash.com)",
      "Bash(curl:*.wikipedia.org/*)",
      "Bash(curl:commons.wikimedia.org/*)",
      "Bash(curl:upload.wikimedia.org/*)",
      "Bash(curl:images-api.nasa.gov/*)",
      "Bash(curl:images-assets.nasa.gov/*)",
      "Bash(curl:earthquake.usgs.gov/*)",
      "Bash(curl:*.noaa.gov/*)",
      "Bash(curl:weather.gov/*)",
      "Bash(curl:api.pexels.com/*)",
      "Bash(curl:images.pexels.com/*)",
      "Bash(curl:pixabay.com/*)",
      "Bash(curl:cdn.pixabay.com/*)",
      "Bash(curl:api.unsplash.com/*)",
      "Bash(curl:images.unsplash.com/*)"
    ]
  },
  "sandbox": {
    "network": {
      "allowedDomains": [
        "*.wikipedia.org",
        "commons.wikimedia.org",
        "upload.wikimedia.org",
        "*.wikimedia.org",
        "images-api.nasa.gov",
        "images-assets.nasa.gov",
        "*.nasa.gov",
        "earthquake.usgs.gov",
        "*.usgs.gov",
        "*.noaa.gov",
        "weather.gov",
        "api.pexels.com",
        "images.pexels.com",
        "pixabay.com",
        "cdn.pixabay.com",
        "api.unsplash.com",
        "images.unsplash.com"
      ]
    }
  }
}
```

**Domini delle 7 fonti foto:**

| Fonte | Domini necessari | API key |
|---|---|---|
| Wikipedia/Wikimedia | `*.wikipedia.org`, `commons.wikimedia.org`, `upload.wikimedia.org` | no |
| NASA | `images-api.nasa.gov`, `images-assets.nasa.gov`, `*.nasa.gov` | no |
| USGS | `earthquake.usgs.gov`, `*.usgs.gov` | no |
| NOAA | `*.noaa.gov`, `weather.gov` | no |
| Pexels | `api.pexels.com`, `images.pexels.com` | sì (gratuita) |
| Pixabay | `pixabay.com`, `cdn.pixabay.com` | sì (gratuita) |
| Unsplash | `api.unsplash.com`, `images.unsplash.com` | sì (gratuita) |

**Servono entrambe le sezioni.** `permissions.allow` autorizza il tool, `sandbox.network.allowedDomains` autorizza la connessione di rete sottostante.

## Fonti istituzionali normative (aggiunta 8 maggio 2026)

Oltre alle fonti foto, l'allowlist include i siti istituzionali italiani ed europei per il **reperimento di normativa, atti, sentenze, ordinanze**, testati e funzionanti via WebFetch. Servono per supportare la stesura di articoli su novità normative e giurisprudenziali della Protezione Civile.

| Categoria | Sito | Domini | Note |
|---|---|---|---|
| Normativa nazionale (testo consolidato) | **Normattiva** | `www.normattiva.it` | Ottimo — ricerca per data/atto/parola |
| Normativa nazionale (Gazzetta Ufficiale) | **GU** | `www.gazzettaufficiale.it` | Ottimo — sommari per data, atti per ELI |
| Atti parlamentari | **Camera dei Deputati** | `www.camera.it` | Ottimo — banca dati ddl, leggi, decreti |
| Atti governativi | **Governo** | `www.governo.it` | Ottimo — comunicati CdM, provvedimenti |
| Normativa regionale Lazio | **Regione Lazio** | `www.regione.lazio.it`, `*.regione.lazio.it` | Ottimo — atti, BURL (settimanali) |
| Normativa regionale Lazio | **Consiglio regionale Lazio** | `www.consiglio.regione.lazio.it` | Ottimo — leggi regionali, atti del Consiglio |
| Giurisprudenza costituzionale | **Corte Costituzionale** | `www.cortecostituzionale.it` | Ottimo — sentenze, archivio storico |
| Giurisprudenza contabile | **Corte dei Conti** | `www.corteconti.it` | Ottimo — sentenze contabili, controllo |
| Giurisprudenza UE | **CURIA** (CGUE) | `curia.europa.eu` | Ottimo — sentenze CGUE + Tribunale UE |
| Giurisprudenza diritti umani | **HUDOC** (CEDU) | `hudoc.echr.coe.int` | Accessibile (JS-heavy, risposta più generica) |
| Diritto UE (sommario) | **EUR-Lex** | `eur-lex.europa.eu` | In allowlist ma SPA JS — solo URL specifiche |
| Normativa PC nazionale | **DPC** | `www.protezionecivile.gov.it` | In allowlist ma SPA JS — non funziona ora |

## Fonti scientifico-tecniche, salute, locali, ministeri (aggiunta 8 maggio 2026, secondo giro test)

Estensione della whitelist con 25 ulteriori siti istituzionali testati e funzionanti, organizzati per area di lavoro tipica della redazione PC.

### Scientifico (rischi naturali, clima, ambiente)

| Sito | Dominio | Uso tipico |
|---|---|---|
| **ISPRA** | `www.isprambiente.gov.it` | Cartografia rischio idrogeologico/sismico, dati ambientali nazionali |
| **CNR-IRPI** | `www.irpi.cnr.it` | Frane, alluvioni, dissesti — rilevante per Castelli |
| **CMCC** | `www.cmcc.it` | Centro euro-Mediterraneo cambiamenti climatici, scenari Lazio |
| **ARPA Lazio** | `www.arpalazio.it` | Qualità aria, allerte ambientali Lazio |
| **ARSIAL** | `www.arsial.it` | Agenzia regionale agricoltura Lazio (fonti agricole + ambientali) |

### Meteo, osservazione Terra, emergenze satellitari

| Sito | Dominio | Uso tipico |
|---|---|---|
| **Copernicus EMS** | `emergency.copernicus.eu` | Mappe satellitari emergenze UE in tempo reale (incendi, alluvioni, siccità) |
| **ECMWF** | `www.ecmwf.int` | Centro europeo previsioni meteo (modelli ensemble) |
| **WMO** | `wmo.int` | Organizzazione Meteorologica Mondiale (severe weather) |

### Salute pubblica e gruppi vulnerabili

| Sito | Dominio | Uso tipico |
|---|---|---|
| **Istituto Superiore di Sanità** | `www.iss.it` | Sorveglianza sanitaria, Piano caldo, autorevole su salute pubblica |
| **ECDC** | `www.ecdc.europa.eu` | Centro europeo controllo malattie, allerte epidemiche |

### Media istituzionali UE (uso editoriale per articoli)

| Sito | Dominio | Uso tipico |
|---|---|---|
| **Commissione Europea — Audiovisual** | `audiovisual.ec.europa.eu` | Foto e video ufficiali della Commissione UE per uso editoriale (Schuman Day, ERCC, rescEU, Canadair, vertici, sedi istituzionali). Termini di riuso "Commission reuse policy" — citare sempre © European Union + anno + autore. Whitelist aggiunta 2026-05-09 dopo articolo Giornata dell'Europa. **Nota**: spesso le stesse foto sono già su Wikimedia Commons con licenze esplicite (CC/PD), preferirle quando disponibili (es. foto VOA in PD o foto EU rilasciate CC BY 4.0). |

### Forze operative del Sistema PC

| Sito | Dominio | Uso tipico |
|---|---|---|
| **Vigili del Fuoco** | `www.vigilfuoco.it`, `opendata.vigilfuoco.it` | VVF nazionale, statistiche interventi, comunicati; portale Open Data (dataset aperti su interventi di soccorso) |
| **ANPAS** | `www.anpas.org` | Pubbliche assistenze, partner DPC su "Io non rischio" |
| **Carabinieri** | `www.carabinieri.it` | Arma dei Carabinieri (Carabinieri Forestali, ordine pubblico in emergenza) |

### Enti territoriali area Genzano

| Sito | Dominio | Uso tipico |
|---|---|---|
| **Città Metropolitana Roma** | `www.cittametropolitanaroma.it` | Atti CM Roma (PC area metropolitana) |
| **ASL Roma 6** | `www.aslroma6.it` | ASL competente Genzano (118, ondate calore, sanità locale) |

### Ministeri

| Sito | Dominio | Uso tipico |
|---|---|---|
| **Min. Istruzione e Merito (MIM)** | `www.mim.gov.it` | Ed. civica, D.M. 183/2024, sicurezza scolastica |
| **Min. Cultura** | `www.cultura.gov.it` | Tutela patrimonio in emergenza |
| **Min. Infrastrutture e Trasporti** | `www.mit.gov.it` | Infrastrutture critiche, dighe, sicurezza trasporti |

### Statistiche, open data, cartografia

| Sito | Dominio | Uso tipico |
|---|---|---|
| **ISTAT** | `www.istat.it` | Demografia, popolazione vulnerabile per Comune |
| **dati.gov.it** | `www.dati.gov.it` | Portale nazionale open data PA |
| **dati.lazio.it** | `dati.lazio.it` | Open data Regione Lazio (406 dataset) |
| **OpenCoesione** | `opencoesione.gov.it` | Monitoraggio fondi pubblici (PNRR, fondi europei PC) |
| **Geoportale Lazio** | `geoportale.regione.lazio.it` | Cartografia regionale (256 layer, WMS/WFS/WCS) |
| **OpenStreetMap** | `www.openstreetmap.org` | Mappa libera, base per mappe del sito |

### Educazione e ricerca didattica

| Sito | Dominio | Uso tipico |
|---|---|---|
| **INDIRE** | `www.indire.it` | Ricerca educativa, materiali didattici PC per scuole |

**Nessuna API key richiesta** per nessuna di queste fonti.

### Siti testati che NON funzionavano via WebFetch (status aggiornato 19 maggio 2026)

🟢 **Aggiornamento maggio 2026**: dopo l'installazione di Firecrawl MCP, **13 dei 18 siti** precedentemente bloccati sono ora leggibili tramite il canale Firecrawl (vedi sezione "Firecrawl MCP" in cima al file). Vincolo: 1 pagina del tier free (500/mese) per richiesta. Lista completa:

| Sito | Causa originale (WebFetch) | Status ora |
|---|---|---|
| **DPC** (`www.protezionecivile.gov.it`) | Solo "Loading..." (SPA JS) | 🟢 Firecrawl OK (11.458 char) |
| **EUR-Lex** (`eur-lex.europa.eu`) | Contenuto vuoto (SPA JS) | 🟢 Firecrawl OK (6.085 char) |
| **DG ECHO** (`civil-protection-humanitarian-aid.ec.europa.eu`) | Solo language selector (SPA JS) | 🟢 Firecrawl OK (pagine interne) |
| **UNDRR** (`www.undrr.org`) | HTTP 403 Forbidden anti-bot | 🟢 Firecrawl OK (13.204 char) |
| **OCHA** (`www.unocha.org`) | HTTP 403 Forbidden anti-bot | 🟢 Firecrawl OK (25.285 char) |
| **Crusca** (`accademiadellacrusca.it`) | HTTP 403 Forbidden anti-bot | 🟢 Firecrawl OK (12.386 char) |
| **Europeana** (`www.europeana.eu`) | HTTP 403 Forbidden anti-bot | 🟢 Firecrawl OK (22.147 char) |
| **Library of Congress** (`www.loc.gov`) | HTTP 403 Forbidden anti-bot | 🟢 Firecrawl OK (18.056 char) |
| **Senato** (`www.senato.it`) | HTTP 403 Forbidden anti-bot | 🟢 Firecrawl OK (17.303 char) |
| **Quirinale** (`www.quirinale.it`) | HTTP 403 Forbidden anti-bot | 🟢 Firecrawl OK (7.712 char) |
| **Giustizia Amministrativa** (`www.giustizia-amministrativa.it`) | SSL CA error (CA giustizia non in sandbox) | 🟢 Firecrawl OK (33.583 char) — era problema CA store sandbox locale, non server |
| **ENEA** (`www.enea.it`) | SSL CA error | 🟢 Firecrawl OK (36.086 char) |
| **terremoti.ingv.it** | SSL CA error | 🟢 Firecrawl OK (34.419 char, lista terremoti realtime) |
| **Cassazione SentenzeWeb** (`www.italgiure.giustizia.it`) | SSL CA error | 🟡 Firecrawl raggiunge ma va in timeout 30s (HTTP 408). Possibile con `timeout: 60000` + retry |
| **Geoportale Nazionale MASE** (`gn.mase.gov.it`) | HTTP 403 Forbidden anti-bot | ❌ Firecrawl bloccato da WAF aggressivo (Access Denied 207 byte). Server-side hard-block |
| **Parco Castelli Romani** (`www.parcocastelliromani.it`) | SSL CA error | ❓ Non testato post-Firecrawl, probabilmente OK come gli altri SSL CA |
| **Comune Genzano** (`www.comune.genzanodiroma.rm.it`) | ECONNREFUSED | ❌ DNS resolution failed anche via Firecrawl — sito offline o cambio URL |
| **USR Lazio** (`www.lazio.istruzione.it`) | ECONNREFUSED | ❌ Server offline; cercare endpoint alternativo |
| **protezionecivile.regione.lazio.it** | ECONNREFUSED | ❌ Sotto-sito offline; usare `www.regione.lazio.it` |

**Pattern interpretativi:**
- **SPA JS** (DPC, EUR-Lex, DG ECHO): risolto da Firecrawl che renderizza Chromium headless lato server.
- **403 anti-bot**: risolto da pool di proxy + browser fingerprint reali di Firecrawl.
- **SSL CA error**: era problema della sandbox locale Claude Code (CA store incompleto), non del server. Firecrawl ha CA store completo.
- **DNS failure / ECONNREFUSED**: il server è davvero down o ha cambiato URL — nessun canale lo risuscita.
- **WAF aggressivo** (MASE Geoportale): firewall server-side che blocca anche Firecrawl. Hard-block, niente da fare lato client.

### Cosa funziona bene via WebFetch

- Aprire un **atto specifico** se si ha l'URL diretta (Normattiva URN, GU ELI, sentenza per anno+numero).
- Aprire il **sommario di una GU per data nota** (`https://www.gazzettaufficiale.it/gazzetta/serie_generale/caricaDettaglio?dataPubblicazioneGazzetta=AAAA-MM-GG&numeroGazzetta=NNN`).
- Aprire un **numero specifico di BURL Lazio** (già usato per il regolamento SAFOR-PROCIV, BURL 36 e 37 di maggio 2026).
- Aprire la **homepage tematica** del Consiglio regionale Lazio o della Corte Costituzionale per scorrere le ultime delibere/sentenze.

### Cosa NON funziona via WebFetch

- **Riempire form di ricerca** dinamici (Normattiva, GU, BURL hanno motori di ricerca client-side che WebFetch non sa azionare). Il workaround è aprire URL specifiche o scorrere sommari per data.
- **Renderizzare SPA JavaScript** (DPC, EUR-Lex). Il workaround è cercare endpoint REST/API o pagine HTML statiche alternative.
- **Senato** (`www.senato.it`) e **Quirinale** (`www.quirinale.it`): rispondono **HTTP 403 Forbidden** (anti-bot lato server, non risolvibile dall'allowlist client).
- **Giustizia Amministrativa** (`www.giustizia-amministrativa.it`) e **Cassazione SentenzeWeb** (`www.italgiure.giustizia.it`): **errore certificato SSL** (CA della giustizia italiana non riconosciuta). Non risolvibile da allowlist; servirebbe `curl --insecure` o un browser reale.

### Workflow tipico per "ultime N normative PC"

1. **Identificare la finestra temporale** (es. ultime 5 GU, ultimo BURL Lazio, ultimo trimestre di sentenze CC).
2. **Aprire i sommari** in parallelo (URL stabili — una WebFetch per numero).
3. **Filtrare gli atti PC** dai sommari (titolo + ente emanante).
4. **Restituire la lista** con titolo, fonte, data, link diretto.
5. Se servono i **testi completi**, aprire le URL specifiche dei singoli atti.

⚠️ **Affidabilità**: WebFetch passa il contenuto a un modello fast che lo riassume. Per atti dove **ogni parola conta** (numeri di articolo, date, importi, soglie), conviene **verificare il testo originale** sul link riportato. La trascrizione è un punto di partenza, non la fonte di verità finale.

## Procedura iniziale (una sola volta per repo)

1. Verifica se il file esiste: `cat .claude/settings.local.json 2>/dev/null`.
2. Se non esiste, crealo con il contenuto sopra.
3. Se esiste con altri contenuti, aggiungi i due blocchi mantenendo il resto.
4. **Riavvia Claude Code**: la sandbox legge il file all'avvio della sessione, non dinamicamente. Senza riavvio le modifiche non hanno effetto.

Una volta riavviato, dura per tutte le sessioni successive in questo repo.

## Quando lo sblocco serve

- Vuoi vedere l'immagine **prima del push** per verificare la fascia blu istituzionale.
- Vuoi inserire **più immagini nel corpo** di un articolo (il workflow `scarica-foto-automatica.yml` gestisce solo la copertina via marker).
- Stai facendo una **passata di revisione** di articoli precedenti per arricchirli.

## Quando NON serve

Il workflow `.github/workflows/scarica-foto-automatica.yml` step 2 (`auto-cover-mancanti.py`) gira sempre al push e genera la cover tipografica banner per articoli con `image: ""`. Niente sandbox locale richiesta per la cover banner.

Il marker `# TODO-foto-*` (ex meccanismo step 1 del workflow) è **bandito dal 3 maggio 2026** (CLAUDE.md punto 9): per inserire foto inline nel corpo articolo da fonti ufficiali si usa l'agent `pc-image-fixer` (procedura WebFetch + curl + applica-fascia + shortcode `{{< foto >}}`). Da Claude Code locale serve l'allowlist domini in `.claude/settings.local.json` per WebFetch + curl.

## Aggiungere un nuovo dominio

Quando si introduce uno script `foto-da-NUOVA.sh` (es. Copernicus, NOAA, EUMETSAT — vedi regola `05-github-aruba-deploy.md` "Aggiungere una nuova fonte"):

1. Aggiungi i domini in **entrambi** i blocchi (`permissions.allow` e `sandbox.network.allowedDomains`).
2. Aggiorna la tabella in `MANUALE-SITO.md` Parte 14.3 con il nuovo dominio.
3. Aggiorna `ALLOWED_SCRIPTS` del workflow `scarica-foto-automatica.yml` con il nuovo script.
4. Riavvia Claude Code.

## Cosa NON mettere

- **Token, credenziali, API key**: il file è in `.gitignore` ma per disciplina non ci mettiamo segreti. Vanno in variabili d'ambiente OS o GitHub secrets.
- **Domini privati** (intranet, gestionali del Comune): la sandbox è uno strato di difesa, non si apre "tanto perché".
- **`*` come allowlist generica**: meglio aggiungere domini specifici man mano che servono.

## Troubleshooting

**"Host not in allowlist" da `curl`**: hai modificato il file ma non hai riavviato Claude Code. La sandbox legge il file solo all'avvio.

**`WebFetch` chiede ancora il permesso ogni volta**: hai messo il dominio solo in `sandbox.network.allowedDomains`, manca in `permissions.allow`. Aggiungilo in entrambi.

**Il file non viene letto**: verifica il path. Deve essere `.claude/settings.local.json` nella **root del repo**, non in sottocartelle. Verifica anche che il JSON sia valido: `python3 -m json.tool .claude/settings.local.json`.

## Riferimenti

- `MANUALE-SITO.md` Parte 14 — versione lunga della stessa documentazione, in italiano operativo.
- `CLAUDE.md` regola 14 — sintesi.
- `scripts/foto-da-wikipedia.sh`, `foto-da-nasa.sh`, `foto-da-usgs.sh`, `foto-da-noaa.sh`, `foto-da-pexels.sh`, `foto-da-pixabay.sh`, `foto-da-unsplash.sh` — gli script che usano questi domini (7 fonti totali).
- `.github/workflows/scarica-foto-automatica.yml` — il workflow CI che fa lo stesso lavoro su GitHub Actions (rete libera, niente sandbox).
