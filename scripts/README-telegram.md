# Notifica Telegram automatica

Sistema che invia messaggi al canale Telegram del Gruppo per **tre tipi di eventi**:

1. **Cambi di livello allerta meteo** (`data/allerta.json`)
2. **Attivazione/cessazione/aggiornamento emergenze** (`data/emergenza.json`)
3. **Pubblicazione di articoli con badge urgente** (`content/comunicazioni/`): solo Allerta, Avviso, Emergenza, Aggiornamento

I messaggi più gravi (allerta arancione/rossa, emergenza attiva, articolo Allerta o Emergenza) vengono **fissati in cima al canale** automaticamente. Quando l'evento cessa, il pin viene rimosso.

Per gli articoli con campo `image` nel frontmatter, il messaggio include la **copertina come anteprima** (sendPhoto). Se il sito non è ancora deployato e l'immagine non è raggiungibile, fallback graceful a messaggio testuale.

## Cosa fa

Quando uno degli eventi sopra si verifica, un messaggio formattato viene inviato automaticamente al canale Telegram. Il cittadino iscritto al canale riceve la notifica sul telefono **senza dover aprire il sito**.

**Esempi di trigger reali:**

- Allerta cambia da `verde` a `gialla` → notifica «🟡 ALLERTA GIALLA», nessun pin
- Allerta cambia da `gialla` a `arancione` → notifica «🟠 ALLERTA ARANCIONE» + **pin in cima al canale**
- Allerta cambia da `arancione` a `verde` → notifica «🟢 CESSATA ALLERTA» + **rimozione pin**
- `emergenza.json` attivato → notifica «🚨 EMERGENZA IN CORSO» + **pin**
- `emergenza.json` disattivato → notifica «✅ CESSATA EMERGENZA» + **rimozione pin**
- Pubblicato articolo nuovo con `badge: Allerta` → notifica con titolo + descrizione + cover + link sito + **pin**
- Pubblicato articolo nuovo con `badge: Aggiornamento` → notifica con cover + link sito (no pin)

**Cosa NON triggera notifica (anti-spam):**

- Aggiornamento di `ultimo_controllo` ogni 6 ore (workflow `check-allerta` senza cambio di livello): il livello è uguale, niente messaggio.
- Modifica di un articolo esistente (correzione di refusi, rinomine): solo articoli **aggiunti** ex novo vengono notificati.
- Articoli con `date` futura (calendarizzati): non vengono notificati al momento del commit. Per notificarli al go-live servirebbe un trigger giornaliero, non implementato.
- Articoli con badge non urgenti (Comunicazione, Formazione, Volontariato, Evento, Attività, Prevenzione, Esercitazione, Informazione, Radiocomunicazioni, ecc.).
- Articoli con `draft: true`.
- Modifiche al codice, alle schede stampabili, alla cartografia, ecc.

## Setup iniziale (10 minuti, da fare una sola volta)

### 1. Crea il bot

1. Apri Telegram, cerca **@BotFather**
2. Manda `/newbot`
3. Dagli un nome leggibile (es. *PC Genzano Allerte*)
4. Dagli un username univoco che finisca con `bot` (es. `pcgenzano_allerte_bot`)
5. **Copia il `BOT_TOKEN`** che ti ridà BotFather (è una stringa tipo `123456789:ABC-DEF...`). Tienilo da parte, ti serve dopo.

### 2. Aggiungi il bot al canale

1. Vai sul canale Telegram del Gruppo (es. `@pcalfagenzano` già esistente — vedi `data/social_links.yaml`)
2. Apri *Gestisci canale → Amministratori → Aggiungi amministratore*
3. Cerca il bot per username e aggiungilo
4. Dagli almeno il permesso **«Pubblica messaggi»**

### 3. Trova il chat_id del canale

1. Posta un messaggio test nel canale (es. *"Test bot"*)
2. Apri nel browser: `https://api.telegram.org/bot<TUO_BOT_TOKEN>/getUpdates`
   (sostituisci `<TUO_BOT_TOKEN>` con il token vero)
3. Cerca nel JSON: `"chat":{"id":-1001234567890,...` — il numero negativo (inizia con `-100`) è il **chat_id**
4. Tienilo da parte.

> Se `getUpdates` non mostra il canale: invia un altro messaggio dopo aver aggiunto il bot, e ricarica. Il bot deve "vedere" un messaggio per apparire negli aggiornamenti.

### 4. Configura i GitHub Secrets

1. Vai sul repository GitHub: **Settings → Secrets and variables → Actions**
2. Clicca **New repository secret** e aggiungi:
   - Nome: `TELEGRAM_BOT_TOKEN` · Valore: il token completo (incluso il numero davanti ai due punti)
   - Nome: `TELEGRAM_CHAT_ID` · Valore: il chat_id (con il segno meno davanti, es. `-1001234567890`)

### 5. Test

Per provare il sistema senza aspettare un'allerta vera:

1. Vai nella tab **Actions** del repository
2. Trova il workflow **📲 Notifica Telegram (allerta + emergenza)**
3. Clicca **Run workflow** → **Run**
4. Lo script gira: se le condizioni anti-spam non sono soddisfatte logga *"Nessun cambiamento significativo"* (normale al primo run con stato verde stabile)

Per forzare un test reale: modifica temporaneamente `data/allerta.json` con `livello: "gialla"`, committa, push. Il messaggio dovrebbe arrivare al canale entro 30 secondi. Poi rimetti `verde` per cessare.

## Architettura

| Componente | File | Cosa fa |
|---|---|---|
| Modulo condiviso | `scripts/telegram_lib.py` | Wrapper API Telegram: `send_message`, `send_photo`, `pin_message`, `unpin_all`, `get_credentials`, `trunc_caption`. Solo libreria standard Python, nessuna dipendenza |
| Workflow allerta/emergenza | `.github/workflows/notifica-telegram.yml` | Triggerato su `data/allerta.json` o `data/emergenza.json` |
| Script allerta/emergenza | `scripts/notifica-telegram.py` | Confronta stato corrente vs HEAD~1, decide categoria (critical/info/cessation), invia, applica pin/unpin |
| Workflow articoli | `.github/workflows/notifica-telegram-articolo.yml` | Triggerato su nuovi `content/comunicazioni/**.md` |
| Script articoli | `scripts/notifica-telegram-articolo.py` | Trova articoli aggiunti, filtra per badge/data/draft, attende deploy 3 min se ci sono immagini, invia con sendPhoto+caption (con fallback a sendMessage), pinna i critici |
| Secrets | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Configurati nei GitHub Secrets, mai committati nel repo |

I messaggi seguono la struttura ISO 22329 + CWA CEN/CENELEC della comunicazione di crisi: tipo evento, livello, area+tempo, cosa fare, fonte ufficiale, riferimento al 112.

## Logica pin/unpin

Telegram permette **un solo messaggio pinnato** per canale (più tecnicamente sì, ma per visibilità ne mostra uno solo). La logica è:

| Evento | Azione |
|---|---|
| Allerta gialla (livello attenzione) | Solo invio, no pin |
| Allerta arancione/rossa | Unpin precedente + invio + pin nuovo |
| Cessata allerta (verde) | Unpin precedente + invio (no nuovo pin) |
| Emergenza attivata | Unpin precedente + invio + pin nuovo |
| Emergenza aggiornata (durante attiva) | Unpin precedente + invio + pin nuovo |
| Cessata emergenza | Unpin precedente + invio (no nuovo pin) |
| Articolo `Allerta` o `Emergenza` | Invio + pin (sostituisce il pin precedente) |
| Articolo `Avviso` o `Aggiornamento` | Solo invio, no pin |
| Articolo altro badge | Niente notifica |

In questo modo il messaggio più recente di natura critica resta sempre fissato in cima al canale, finché un altro evento critico lo sostituisce o cessa lo stato.

## Sicurezza e privacy

- Il token bot non è mai committato nel repo (solo nei GitHub Secrets, criptati a riposo)
- Il bot pubblica **solo** sul canale specificato dal chat_id (whitelist hardcoded)
- Nessuna raccolta di dati degli iscritti: la lista degli iscritti è gestita da Telegram, non da noi (no GDPR pesante)
- Messaggi conformi alle regole di accessibilità social del Gruppo (max 2-3 emoji, niente Unicode decorativi, fonte sempre citata)

## Troubleshooting

**Il workflow gira ma non manda nulla** → controlla i log: probabilmente `TELEGRAM_BOT_TOKEN` o `TELEGRAM_CHAT_ID` mancano. Verifica i Secrets.

**HTTP 401 dal log Telegram** → token sbagliato o invalidato. Rigeneralo con BotFather (`/token`).

**HTTP 400 "chat not found"** → chat_id sbagliato. Riprova `getUpdates` per ottenerlo correttamente.

**HTTP 403 "bot is not a member"** → il bot non è admin del canale. Aggiungilo da *Gestisci canale → Amministratori*.

**Spam di messaggi** → se vedi notifiche per cambi non significativi, controlla `scripts/notifica-telegram.py` funzione `determina_messaggio()`: è dove vive la logica anti-spam.
