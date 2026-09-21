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

**Permesso mancante da chiedere**: `instagram_manage_contents`. Non richiede la
revisione di Meta, perché la Pagina e l'account sono nostri e per i propri asset
basta l'accesso standard. Si aggiunge nel portale ripetendo l'autorizzazione e
rigenerando il token. Lo strumento che lo userebbe è già pronto: il workflow
«🗑️ Elimina un contenuto pubblicato» del repo social.

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
