# Claude Code — Setup ambiente di sviluppo

Questo file documenta come configurare l'ambiente di Claude Code per lavorare sul sito senza essere bloccato dalla sandbox di sicurezza, in particolare per il download di foto da fonti libere.

## Sandbox: cos'è e come funziona

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
      "Bash(curl:*.wikipedia.org/*)",
      "Bash(curl:commons.wikimedia.org/*)",
      "Bash(curl:upload.wikimedia.org/*)",
      "Bash(curl:images-api.nasa.gov/*)",
      "Bash(curl:images-assets.nasa.gov/*)",
      "Bash(curl:earthquake.usgs.gov/*)"
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
        "*.usgs.gov"
      ]
    }
  }
}
```

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

Il workflow `.github/workflows/scarica-foto-automatica.yml` gira su un runner GitHub Actions con rete libera. Se un articolo nuovo include il marker `# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Titolo Pagina" slug-articolo` nel frontmatter, al push il runner scarica la foto, applica la fascia blu istituzionale, popola `image:` + `image_credit:` + `image_source_url:` e rimuove il marker. **Per la sola copertina di un articolo nuovo, lo sblocco locale non è necessario.**

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
- `scripts/foto-da-wikipedia.sh`, `foto-da-nasa.sh`, `foto-da-usgs.sh`, `foto-da-noaa.sh` — gli script che usano questi domini.
- `.github/workflows/scarica-foto-automatica.yml` — il workflow CI che fa lo stesso lavoro su GitHub Actions (rete libera, niente sandbox).
