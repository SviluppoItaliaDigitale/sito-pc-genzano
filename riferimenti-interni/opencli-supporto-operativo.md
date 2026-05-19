# opencli — supporto operativo per Claude Code

**File interno** (non deployato sul sito). Documenta cosa è opencli, quando posso usarlo, quando devo chiedere, e quali sono i confini operativi inviolabili.

**Stato al 19 maggio 2026**: 🟡 **STANDBY**. Script preparati ma non attivi. Documentazione codificata per consentire un'attivazione futura sicura, senza effetti collaterali sui canali pubblicati del Gruppo.

---

## 1. Cos'è opencli

**opencli** è una CLI Node.js che permette di guidare un browser locale (Chrome/Firefox) tramite comandi shell. È un wrapper sopra Chrome DevTools Protocol (CDP), simile a Puppeteer/Playwright ma orientato all'uso da riga di comando interattiva, non al test automation.

Si installa una volta sola con:

```bash
npm install -g @jackwener/opencli
```

E richiede un'**estensione browser** companion che apre il canale di comunicazione fra CLI e finestra del browser. Verifica:

```bash
opencli doctor
# Output atteso:
#   ✓ CLI installed (version x.y.z)
#   ✓ Extension installed
#   ✓ Connectivity: connected
```

---

## 2. Comandi principali (sottoinsieme operativo)

| Comando | Effetto |
|---|---|
| `opencli browser open <url>` | Apre l'URL nella scheda attiva del browser |
| `opencli browser wait --selector <css> --timeout <ms>` | Attende che un elemento CSS appaia, oppure fallisce dopo timeout |
| `opencli browser fill --selector <css> --value <text>` | Imposta il `value` di un input/textarea (sovrascrive contenuto) |
| `opencli browser type --selector <css> --value <text>` | Digita testo dentro un elemento (preserva contenuto + eventi keystroke) |
| `opencli browser click --selector <css>` | Clic singolo su un elemento |
| `opencli browser upload --file <path>` | Carica un file nel prossimo `<input type=file>` attivato |
| `opencli browser screenshot --output <path>` | Salva screenshot della pagina visibile |
| `opencli browser eval --js '<expr>'` | Valuta JavaScript nel contesto della pagina (RISCHIOSO: vedi § 6) |

Documentazione completa upstream: [github.com/jackwener/opencli](https://github.com/jackwener/opencli) (verificare attualità).

---

## 3. Casi d'uso autorizzati nel nostro contesto

| Caso d'uso | Stato | Note |
|---|---|---|
| **Verifica handle YouTube** di un canale di cui non si conosce l'URL esatto (ricerca veloce sul sito di YouTube) | 🟢 OK senza chiedere | Letto pubblicamente, no modifiche. Più rapido di tentativi yt-dlp ciechi |
| **Anteprima rendering** di una pagina del sito locale dopo un build (es. controllo header, screenshot di una sezione nuova) | 🟢 OK senza chiedere | Pagina locale, no modifiche persistenti |
| **Recupero metadati YouTube** difficili (numero iscritti canale, ultima data video, descrizione) per arricchire `data/video_dpc_catalogo.yaml` | 🟢 OK senza chiedere | Solo lettura |
| **Test di rendering social** (apri il preview generato della pagina su X/Facebook/LinkedIn debugger pubblici per vedere l'Open Graph) | 🟢 OK senza chiedere | Strumenti pubblici, no login richiesto |
| **Compilazione bozze social Livello B** (apri X/Facebook compose, riempi campi, NON cliccare Pubblica) | 🟡 Chiedere prima | Richiede login utente attivo nel browser; fragile ai cambi DOM social |
| **Verifica accessibilità rendering** (apri sito locale e screenshot per controllare contrasto/layout) | 🟢 OK senza chiedere | Solo lettura visiva |
| **Backup contenuti del proprio account** (es. export DM, export post propri, archivio thread) | 🟡 Chiedere prima | Coinvolge dati personali dell'utente |
| **Click "Pubblica" / "Invia" / "Conferma"** sui social/Mail/SaaS | 🔴 **VIETATO** | Inviolabile: la pubblicazione è SEMPRE atto umano |
| **Transazioni** (carrello, pagamento, acquisto) | 🔴 **VIETATO** | Inviolabile |
| **Modifiche account** (cambio password, eliminazione, impostazioni privacy) | 🔴 **VIETATO** | Inviolabile |
| **Iscrizione/disiscrizione** servizi | 🔴 **VIETATO** | Inviolabile |
| **Eval JS arbitrario** su domini terzi | 🔴 **VIETATO** | Vedi § 6 — pattern di sicurezza |

---

## 4. Pattern di uso "no side effect" (preferito)

L'unico modo per garantire zero effetti collaterali è far rispettare a Claude un protocollo di lavoro disciplinato:

### 4.1 Preflight obbligatorio

Prima di ogni sequenza opencli, Claude deve:

1. Stampare un **piano** sintetico: cosa apre, cosa legge, cosa scrive, cosa NON tocca.
2. Identificare il **massimo effetto possibile** del comando peggiore della sequenza.
3. Se il piano include `click` / `type` / `fill` / `upload` su domini fuori dal sito del Gruppo, **chiedere conferma esplicita** all'utente.

### 4.2 Sequenza tipica autorizzata

```bash
# 1. Apre una pagina pubblica
opencli browser open "https://www.youtube.com/@CICAP_it/videos"

# 2. Attende che la lista video sia caricata
opencli browser wait --selector "ytd-rich-item-renderer" --timeout 10000

# 3. Estrae info (read-only via DOM)
opencli browser eval --js "
  Array.from(document.querySelectorAll('a#video-title-link'))
       .slice(0, 5)
       .map(a => ({title: a.textContent.trim(), url: a.href}))
"
```

Questo flusso non scrive nulla. È il pattern preferito.

### 4.3 Sequenza con `fill` (richiede conferma)

```bash
# Solo dopo conferma esplicita dell'utente "ok riempi le bozze social"
opencli browser open "https://x.com/compose/post"
opencli browser wait --selector "div[data-testid='tweetTextarea_0']"
opencli browser fill --selector "div[data-testid='tweetTextarea_0']" --value "$(cat bozza-x.txt)"
echo "→ Bozza X compilata. Verifica e clicca 'Posta' manualmente."
```

Il `fill` modifica DOM ma NON conferma l'azione. L'utente deve cliccare manualmente.

---

## 5. Vincoli inviolabili

Sono regole che Claude non può violare **anche se l'utente le autorizza**:

1. **Mai cliccare** bottoni etichettati "Pubblica" / "Posta" / "Invia" / "Conferma" / "Acquista" / "Salva modifiche".
2. **Mai inviare** messaggi DM, email, SMS, chiamate via opencli.
3. **Mai modificare** impostazioni di account (privacy, password, 2FA, notifiche).
4. **Mai accedere** a sezioni autenticate dei social per scopi diversi dalla compilazione bozze (che ha vincolo umano sul Publish).
5. **Mai estrarre** dati personali di terzi (DM altrui, profili privati, contenuti riservati).
6. **Mai disinstallare/installare** estensioni browser senza richiesta esplicita.
7. **Mai eseguire** `opencli browser eval` con codice che modifica `localStorage`, `cookies`, `IndexedDB` di domini terzi.

Se l'utente chiede una violazione di queste regole, Claude **rifiuta motivando** e propone un'alternativa sicura.

---

## 6. Pattern di sicurezza — `eval` JS

Il comando `opencli browser eval --js '<expr>'` è il più pericoloso: esegue codice arbitrario nel contesto del dominio aperto. Pattern di sicurezza:

| Pattern | Verdetto |
|---|---|
| `document.querySelectorAll(...).map(...)` (read-only) | 🟢 OK |
| `JSON.stringify(window.__PRELOADED_STATE__)` (legge state pubblico) | 🟢 OK |
| `document.title` o `location.href` (read-only) | 🟢 OK |
| `document.cookie = ...` (scrittura cookie) | 🔴 VIETATO |
| `fetch(...)` con metodo POST/PUT/DELETE | 🔴 VIETATO |
| `localStorage.setItem(...)` o `sessionStorage` write | 🔴 VIETATO |
| `window.location = ...` (redirect) | 🟡 OK solo verso domini sicuri della stessa origine |
| `document.body.innerHTML = ...` (modifica DOM persistente) | 🔴 VIETATO |
| `element.click()` programmaticamente | 🟡 OK solo se NON è un bottone di conferma/pubblicazione |

In dubbio: **non eseguire**. Chiedere all'utente.

---

## 7. Workflow tipici nel contesto del sito PC Genzano

### 7.1 Trovare l'handle YouTube di un canale

```bash
# 1. Apre la ricerca YouTube
opencli browser open "https://www.youtube.com/results?search_query=Vigili+del+Fuoco+canale+ufficiale&sp=EgIQAg%253D%253D"  # filtro Channel

# 2. Estrae i primi 5 canali risultanti
opencli browser eval --js "
  Array.from(document.querySelectorAll('ytd-channel-renderer'))
       .slice(0, 5)
       .map(c => ({
         name: c.querySelector('#text')?.textContent?.trim(),
         handle: c.querySelector('#subscribers')?.textContent?.trim(),
         url: c.querySelector('a#main-link')?.href
       }))
"
```

Output: lista di canali candidati con URL. Da lì Claude sceglie quello plausibile e lo aggiunge a `scripts/scrape-catalogo-video.py`.

### 7.2 Anteprima Open Graph di un articolo

```bash
# Apre il Facebook Sharing Debugger con l'URL del nostro articolo
opencli browser open "https://developers.facebook.com/tools/debug/?q=https://www.protezionecivilegenzano.it/comunicazioni/2026-05-19-it-alert-tecnologia-accessibilita-falsi-miti/"
# Lettura visiva del rendering. Nessun click su "Aggiorna debug" se richiede login.
```

### 7.3 Compilare bozze social (Livello B) — solo dopo OK utente

Vedi `scripts/pubblica-social-livello-b.sh` (oggi in standby). L'attivazione richiede:

1. Selettori CSS aggiornati (verificare ogni 3-6 mesi).
2. Sessione browser dell'utente già loggata sui 4 social.
3. Conferma esplicita prima di partire.
4. Stop **prima** del click "Pubblica" su ogni piattaforma.

---

## 8. Quando opencli **non** serve (alternative migliori)

| Compito | Alternativa | Perché |
|---|---|---|
| Scaricare lista video da un canale YouTube | `yt-dlp --flat-playlist <url>` | Più veloce, no browser, no estensione |
| Validare HTML di una pagina del sito | `hugo --quiet` + grep / lighthouse CLI | Più affidabile, niente rendering JS necessario |
| Inviare richieste HTTP (GET/POST API REST) | `curl` con sandbox cloud allowlist | Più trasparente, no DOM |
| Estrarre metadati da pagine statiche | `WebFetch` (sandbox cloud) o `curl` + `grep` | Più leggero |
| Pubblicare articoli sul sito | `git push` + workflow Hugo | È la nostra pipeline |
| Generare immagini social | `scripts/genera-immagini-social.py` (Pillow) | Più affidabile, niente rendering JS |

Usa opencli **solo** quando l'azione richiede DOM JS (es. infinite scroll YouTube), una sessione autenticata, o un test visivo che gli altri strumenti non possono dare.

---

## 9. Sandbox cloud — opencli non disponibile

In **sandbox cloud** (Claude Code app mobile/web/agent GitHub-integrato) opencli **non è installato** e non lo sarà: la sandbox è isolata, niente browser locale, niente estensioni.

Quando lavoro in cloud:
- Per cercare handle YouTube → uso yt-dlp con probe multipli (limit 1) sui candidati plausibili.
- Per verificare rendering pagina → uso `hugo --quiet` + lettura di file HTML generati in `public/`.
- Per anteprima social → uso solo strumenti che accettano URL pubblici via API (Facebook Debugger non funziona da CLI cloud).

opencli è uno strumento **locale-only**, attivabile dal Claude Code CLI del PC dell'utente.

---

## 10. Attivazione

Quando l'utente vuole attivare opencli per davvero:

1. Sul **PC desktop** dell'utente: `npm install -g @jackwener/opencli` + installa l'estensione browser companion.
2. Verifica: `opencli doctor` → `Connectivity: connected`.
3. Apri sessione Claude Code CLI **locale** (non cloud).
4. Rimuovi il blocco `STANDBY GUARD` da `scripts/pubblica-social-livello-b.sh` (4 righe `echo` + `exit 0`).
5. Aggiorna i selettori CSS della sezione `SEL_*` in quel file (data ultima verifica → oggi).
6. Test in dry-run con un articolo già pubblicato (deve compilare e fermarsi prima del click "Pubblica").
7. Solo se il test va a buon fine: workflow operativo.

L'attivazione richiede passaggi manuali dell'utente. Claude non li compie in autonomia.

---

## 11. Disattivazione di emergenza

Se opencli inizia a comportarsi in modo anomalo (timeout strani, eval con effetti imprevisti, modifiche non richieste a DOM):

```bash
# 1. Chiudi il browser controllato
pkill -f chromium
pkill -f firefox

# 2. Disinstalla l'estensione browser (manuale dalla pagina estensioni)

# 3. Disinstalla la CLI
npm uninstall -g @jackwener/opencli

# 4. Reinserisci STANDBY GUARD in scripts/pubblica-social-livello-b.sh
```

Nessuna parte del sito o del repo è influenzata da opencli, è uno strumento puramente di automazione browser locale.

---

## 12. Riferimenti

- **Script preparato**: `scripts/pubblica-social-livello-b.sh` (oggi in STANDBY GUARD).
- **Script attivo equivalente Livello A**: `scripts/pubblica-social-assistito.sh` (manuale, niente opencli — vedi Parte 13 del manuale).
- **Manuale operativo Parte 13**: Social Media Policy + workflow di pubblicazione.
- **Manuale operativo Parte 14**: Configurazione ambiente di sviluppo Claude Code.
- **Memoria Claude `feedback_workflow_ai_esterne_validato.md`**: validazione test 9 maggio 2026 (ChatGPT 9.5/10 con drag-drop, opencli Livello B in standby).

---

**Ultima revisione**: 19 maggio 2026.
**Autore**: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
**Stato**: documentazione operativa preparata; opencli stesso in standby fino ad attivazione esplicita dell'utente.
