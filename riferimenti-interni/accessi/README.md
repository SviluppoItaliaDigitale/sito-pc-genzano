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
| `FB_PAGE_TOKEN` + `FB_PAGE_ID` | repo social | pubblicare sulla Pagina, riscrivere il testo di un post uscito, **eliminare un post** | cambiare le immagini di un post uscito (la piattaforma non lo consente) |

**`instagram_manage_contents` concesso il 24/09/2026**, insieme al nuovo token
della Pagina (vedi sotto). Serve al workflow «🗑️ Elimina un contenuto
pubblicato» del repo social; non è ancora stato provato su un contenuto reale.

## Quando i token scadono e quando no

- **Token Instagram** (`IG_ACCESS_TOKEN`): dura 60 giorni, ma il workflow
  «🔑 Rinnovo token social» lo rinnova da solo il 1 e il 16 di ogni mese.
- **Token della Pagina** (`FB_PAGE_TOKEN`): ricavato da un token utente a lunga
  durata, **non scade**. La data di scadenza che mostra il debugger di Meta (60
  giorni) è quella del token utente intermedio, che dopo non serve più.
- **Entrambi si invalidano** se cambia la password dell'account Facebook o se
  Meta chiude le sessioni per sicurezza: errore `code 190` (sottocodice `460`
  sulla Pagina). Nessun rinnovo automatico li recupera: vanno rigenerati a mano.
  Successo il 23/09/2026, con tutta la pubblicazione ferma per una notte.

## Rigenerare i token a mano (procedura del 24/09/2026)

1. **Chrome**: consentire i popup a `[*.]facebook.com` e `[*.]instagram.com`
   (`chrome://settings/content/popups`). Senza, «Genera token» non fa nulla.
2. **Instagram**: developers.facebook.com → app **PC Genzano Publisher**
   (`1120754493711097`) → Instagram → *Configurazione dell'API con Business
   Login per Instagram* → riga `protezionecivilegenzano` → **Genera token** →
   accesso e consenso → segreto `IG_ACCESS_TOKEN` del repo social.
3. **Pagina Facebook**: Graph API Explorer → app PC Genzano Publisher → *Token
   utente* con `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`
   (più `instagram_basic`, `instagram_manage_contents`) → *Generate Access
   Token* → icona «i» → *Apri in Strumento token d'accesso* → **Extend Access
   Token** → incollare il token lungo nell'Explorer → `GET
   239709112708894?fields=access_token` → il valore è il token della Pagina →
   segreto `FB_PAGE_TOKEN`.
4. **Verifica**: workflow «🔑 Rinnovo token social» con `solo_verifica=true`,
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
**vuota**, pur avendo `pages_show_list` concesso. Il token della Pagina si
ricava invece chiedendolo alla Pagina per identificativo:

```bash
curl -s "https://graph.facebook.com/v23.0/239709112708894?fields=access_token&access_token=TOKEN_UTENTE_LUNGA_DURATA"
```
