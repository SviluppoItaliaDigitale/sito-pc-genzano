# Claude Code — Setup ambiente di sviluppo

Questo file documenta come configurare l'ambiente di Claude Code per lavorare sul sito senza essere bloccato dalla sandbox di sicurezza, in particolare per il download di foto da fonti libere.

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
