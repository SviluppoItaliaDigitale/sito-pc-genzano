# Accessi e permessi — che cosa possiamo fare davvero

Elenco di ogni credenziale del progetto, di che cosa abilita e — soprattutto —
di **che cosa non abilita**. Serve a non scoprire un permesso mancante nel
momento in cui serve, come è successo il 21 settembre 2026: un post era uscito
due volte e non si poteva cancellarlo, perché il giorno prima erano stati
chiesti i permessi per pubblicare e nessuno aveva pensato ad annullare.

Regola operativa: **quando si chiede un accesso, si chiede per l'intero ciclo di
vita di ciò che si va a gestire** — creare, correggere, annullare — non solo per
il passo che serve quel giorno.

Questa cartella non è deployata (vedi rule 04c).

## Canali social

| Credenziale | Dove | Abilita | NON abilita |
|---|---|---|---|
| `IG_ACCESS_TOKEN` + `IG_USER_ID` | repo social | pubblicare post, caroselli e storie su Instagram; chiudere i commenti | **eliminare un contenuto** (serve `instagram_manage_contents`); modificare la didascalia di un post uscito (la piattaforma non lo consente a nessuno) |
| `FB_PAGE_TOKEN` + `FB_PAGE_ID` | repo social | sulla Pagina: pubblicare, riscrivere il testo di un post uscito, **eliminare un post**, commenti, messaggi Messenger, statistiche, impostazioni. Su Instagram (API con login Facebook): **eliminare contenuti**, commenti, messaggi diretti, statistiche | cambiare le immagini di un post uscito (la piattaforma non lo consente); gestire amministratori, persone e risorse del portfolio (manca `business_management`, di proposito); inserzioni |

**Dal 03/10/2026 `FB_PAGE_TOKEN` viene dall'utente di sistema `sito-web`**
(ID 61594965425134, Admin) del portfolio «Protezione Civile Genzano»: Pagina e
account Instagram in accesso completo, app «PC Genzano Publisher»
(`1120754493711097`) con ruolo «Sviluppa l'app». Non dipende più dal profilo
personale di Alessandro.

Permessi concessi: `pages_show_list`, `pages_read_engagement`,
`pages_read_user_content`, `pages_manage_posts`, `pages_manage_engagement`,
`pages_manage_metadata`, `pages_messaging`, `read_insights`,
`instagram_basic`, `instagram_content_publish`, `instagram_manage_contents`,
`instagram_manage_comments`, `instagram_manage_insights`,
`instagram_manage_messages`.

Esclusi di proposito: `business_management` (aggiungere o togliere
amministratori, persone e risorse del portfolio resta solo ad Alessandro), i
permessi pubblicitari (`ads_*`, `pages_manage_ads`) e quelli di negozio e
contenuti sponsorizzati.

## Quando i token scadono e quando no

- **Token Instagram** (`IG_ACCESS_TOKEN`): dura 60 giorni, ma il workflow
  «🔑 Rinnovo token social» lo rinnova da solo il 1 e il 16 di ogni mese.
  Serve a pubblicare; non è stato toccato il 03/10/2026.
- **Token della Pagina** (`FB_PAGE_TOKEN`): token dell'utente di sistema con
  scadenza «Mai», **non scade**. Non essendo legato a un profilo personale,
  non si invalida se cambia la password dell'account Facebook di Alessandro
  (era successo il 23/09/2026 con il vecchio token, con la pubblicazione ferma
  per una notte). Si invalida solo se il token viene revocato o se sito-web
  perde l'accesso alla Pagina o all'app.

## Rigenerare i token a mano

1. **Pagina Facebook** (procedura del 03/10/2026): business.facebook.com →
   portfolio «Protezione Civile Genzano» → Impostazioni → Utenti → **Utenti di
   sistema** → sito-web → **Genera token** → app PC Genzano Publisher →
   scadenza **Mai** → i permessi elencati sopra (senza `business_management`)
   → Genera token → Copia. Poi si ricava il token della Pagina (vedi «Il token
   della Pagina non si ottiene da /me/accounts») e si aggiorna il segreto
   `FB_PAGE_TOKEN` del repo social. Il token non va mai incollato in chat né
   nei file.
2. **Instagram** (procedura del 24/09/2026): Chrome deve consentire i popup a
   `[*.]facebook.com` e `[*.]instagram.com`
   (`chrome://settings/content/popups`), altrimenti «Genera token» non fa
   nulla. developers.facebook.com → app **PC Genzano Publisher** → Instagram →
   *Configurazione dell'API con Business Login per Instagram* → riga
   `protezionecivilegenzano` → **Genera token** → accesso e consenso → segreto
   `IG_ACCESS_TOKEN` del repo social.
3. **Verifica**: workflow «🔑 Rinnovo token social» con `solo_verifica=true`,
   poi un giro di «📣 Pubblicazione automatica social»: la coda riparte da sola.

## Pubblicazione del sito

| Credenziale | Dove | Abilita | NON abilita |
|---|---|---|---|
| `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` | repo sito | caricare il sito su Aruba | cancellare la cartella `/documenti/`, esclusa dal deploy per scelta (rule 05) |
| `SOCIAL_REPO_PAT` | repo sito | chiamare i workflow del repo social (la sveglia) | scrivere nel repo social |
| `REPO_SECRETS_PAT` | repo social | riscrivere il token Instagram nei segreti dopo il rinnovo | altro |
| `CRONJOB_GH_PAT` | repo sito | il trigger esterno che tiene reattiva l'allerta meteo | — |

## Servizi di supporto

| Credenziale | Abilita | Limite |
|---|---|---|
| `GEMINI_API_KEY` | testi delle bozze social | tier gratuito, ampiamente sufficiente |
| `FIRECRAWL_API_KEY` | lettura di siti istituzionali con JavaScript o anti-bot | 500 pagine al mese |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | avvisi sul canale: allerta e nuovi articoli | — |
| `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `UNSPLASH_ACCESS_KEY` | foto stock, usate di rado per scelta editoriale | — |
| `CDSE_S3_ACCESS_KEY` + `CDSE_S3_SECRET_KEY` (dal 10/10/2026) | lettura dell'archivio del Copernicus Data Space Ecosystem via S3 (`eodata.dataspace.copernicus.eu`, bucket `eodata`): Sentinel-1/2/3/5P e prodotti CLMS, per gli snapshot `copernicus-*.json` del cruscotto | sola lettura: niente elaborazioni sul loro server (openEO e Sentinel Hub vogliono un client OIDC a parte); quota gratuita 10 TB/mese e 4 scarichi in parallelo; le chiavi si rigenerano dal gestore chiavi S3 dell'account (dataspace.copernicus.eu, «S3 keys manager»), la segreta si vede una volta sola |

## Limiti che non dipendono da un permesso

Alcune cose non si possono fare e nessuna credenziale le sblocca. Vale la pena
saperle prima di prometterle:

- **Instagram**: una volta pubblicato, non si cambiano né il testo né le
  immagini. Si può solo eliminare (col permesso giusto) e ripubblicare.
- **Facebook**: il testo si riscrive, le immagini no.
- **Aruba**: non c'è modo di fare redirect lato server oltre a `.htaccess`, e la
  cartella `/documenti/` resta gestita a mano.

## Ambiente di lavoro

Il mio ambiente blocca da sé i comandi git che riscrivono la storia
(`rebase`, `--amend`, `push --force`). È il motivo per cui i 170 commit con il
rimando di sessione sono ancora lì: la pulizia richiede proprio quei comandi.
Si sblocca dalle impostazioni di Claude Code, con una regola di permesso per
Bash.

## Instagram: due API, due spazi di identificativi

Scoperto il 21/09/2026 provando a cancellare un doppione. Le due API di
Instagram non sono intercambiabili, e la differenza non è documentata in modo
evidente:

- **Con login Instagram** (`graph.instagram.com`, il nostro `IG_ACCESS_TOKEN`):
  serve a pubblicare. Gli identificativi dei contenuti che restituisce **non
  valgono** sull'altra API.
- **Con login Facebook** (`graph.facebook.com`, token derivato dalla Pagina):
  è l'unica che accetta l'eliminazione, e vuole gli identificativi del **suo**
  spazio, che si ottengono da `/{instagram_business_account}/media`.

Quindi per cancellare un contenuto: dalla Pagina si ricava l'account Instagram
collegato, da quello l'elenco dei contenuti con gli identificativi giusti, e su
quelli si chiama la cancellazione. Cercare l'identificativo con l'API sbagliata
porta a *Unsupported delete request*, che sembra un problema di permessi e non
lo è.

**L'account Instagram collegato alla Pagina**: `17841449011648440`
(Pagina `239709112708894`).

## Il token della Pagina non si ottiene da /me/accounts

Su questo portafoglio business `GET /me/accounts` risponde con una lista
**vuota**, pur avendo `pages_show_list` concesso (anche con il token
dell'utente di sistema). Il token della Pagina si
ricava invece chiedendolo alla Pagina per identificativo:

```bash
curl -s "https://graph.facebook.com/v23.0/239709112708894?fields=access_token&access_token=TOKEN_UTENTE_DI_SISTEMA"
```
