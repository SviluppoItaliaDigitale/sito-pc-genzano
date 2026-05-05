# Notifica Telegram automatica per allerte e emergenze

Sistema che invia messaggi al canale Telegram del Gruppo ogni volta che cambia lo stato di allerta meteo o di emergenza in corso.

## Cosa fa

Quando lo stato di `data/allerta.json` o `data/emergenza.json` cambia in modo significativo, un messaggio formattato viene inviato automaticamente al canale Telegram. Il cittadino iscritto al canale riceve la notifica sul telefono **senza dover aprire il sito**.

**Esempi di trigger reali:**

- Allerta cambia da `verde` a `gialla` → notifica «🟡 ALLERTA GIALLA — Lazio»
- Allerta cambia da `arancione` a `verde` → notifica «🟢 CESSATA ALLERTA»
- `emergenza.json` viene attivato → notifica «🚨 EMERGENZA IN CORSO»
- `emergenza.json` viene disattivato → notifica «✅ CESSATA EMERGENZA»

**Cosa NON triggera notifica (anti-spam):**

- Aggiornamento di `ultimo_controllo` ogni 6 ore (workflow `check-allerta` che verifica il bollettino senza che il livello sia cambiato): il livello è uguale, niente messaggio.
- Modifiche al codice, agli articoli, alle schede, alla cartografia, ecc.

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
| Workflow | `.github/workflows/notifica-telegram.yml` | Si triggera su push che modifica `data/allerta.json` o `data/emergenza.json`. Esegue lo script |
| Script | `scripts/notifica-telegram.py` | Confronta stato corrente vs HEAD~1, decide se notificare, costruisce messaggio HTML, invia via API Telegram |
| Secrets | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Configurati nei GitHub Secrets, mai committati nel repo |

Il messaggio segue la struttura ISO 22329 + CWA CEN/CENELEC della comunicazione di crisi: tipo evento, livello, area+tempo, cosa fare, fonte ufficiale, riferimento al 112.

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
