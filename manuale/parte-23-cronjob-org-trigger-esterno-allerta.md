_[Indice manuale](README.md)_

# Parte 23 — Trigger esterno cron-job.org per allerta meteo

Questa parte documenta l'architettura del sistema di polling allerta meteo introdotta il **10 maggio 2026**, basata su un trigger esterno gratuito (cron-job.org) che chiama l'API GitHub `workflow_dispatch` per garantire latenza reale di **~15 secondi** al cambio livello DPC.

> **Aggiornamento 13 maggio 2026**: dietro a questo trigger gira ora una **pipeline a tre script** che copre tre fonti distinte: criticità idrogeologica (CSV opendatasicilia + fallback PDF Regione Lazio), avvisi meteo avversi (PDF Regione Lazio), rischio incendi AIB (PDF Regione Lazio Zona 9). Il trigger esterno descritto in questa parte resta invariato: gli script aggiuntivi vengono semplicemente eseguiti in sequenza all'interno del workflow `check-allerta.yml`. Specifiche dei tre script in `parte-10-github-actions-e-automazioni.md` § 10.3.

## 23.1 — Perché un trigger esterno

GitHub Actions schedule (`cron:` nel file `.yml`) è **best effort**, non garantito. Verifica empirica del 10 maggio 2026:

- `cron: '*/5 * * * *'` → 0 run scheduled in 42 minuti
- `cron: '7,22,37,52 * * * *'` → 0 run scheduled in 20 minuti

Documentazione GitHub conferma esplicitamente: *"Schedule events can be delayed during periods of high loads of GitHub Actions workflow runs. High-load times include the start of every hour."*

Per un sistema di Protezione Civile, la latenza imprevedibile non è accettabile. Soluzione: separare il timer (esterno, affidabile) dall'esecuzione (GitHub Actions, gratis e funzionante).

## 23.2 — Architettura "doppio trigger fail-safe"

```
┌─────────────────────────────────────────────────────────────┐
│  Trigger PRIMARIO — cron-job.org                            │
│  ──────────────────────────────                             │
│  Server: Germania, 3 cluster ridondanti, SLA 99,9%           │
│  Frequenza: ogni 5 minuti puntuale                          │
│  Aderenza: <30 secondi di drift osservato                   │
│  Cosa fa: HTTP POST a api.github.com/.../dispatches         │
│  Latenza al lancio workflow: ~5 secondi                     │
│  Costo: gratis (free tier illimitato)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│  Trigger FAIL-SAFE — GitHub schedule '17 * * * *'           │
│  ───────────────────────────────────────────────             │
│  Frequenza: 1 run/h al minuto 17                             │
│  Aderenza: variabile (drift fino a 30+ min documentato)      │
│  Scopo: paracadute se cron-job.org va giù                   │
│  Worst case: ricontrollo DPC entro 60 min                   │
└────────────────────────┬────────────────────────────────────┘
                         │ workflow_dispatch o schedule
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions runner (Ubuntu virtuale, monouso)           │
│  Esegue check-allerta.yml:                                   │
│  1. Scarica CSV DPC da opendatasicilia                      │
│  2. Cerca riga "Genzano di Roma"                            │
│  3. Estrae livello (verde/gialla/arancione/rossa)           │
│  4. Confronta con data/allerta.json                          │
│  5. Se cambio livello → commit + push (anti-spam: max 4/g)  │
└────────────────────────┬────────────────────────────────────┘
                         │ git push
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Trigger automatico notifica-telegram.yml                   │
│  Manda push al canale Telegram t.me/pcalfagenzano           │
│  Pin automatico per Allerta arancione/rossa                  │
│  Latenza: ~5 secondi                                         │
└─────────────────────────────────────────────────────────────┘

TOTALE end-to-end al cambio livello DPC: ~15-30 secondi.
```

L'**anti-spam** interno (`stale_check` 5h45min) impedisce commit duplicati anche se i due trigger sparano ravvicinati: il secondo run trova `ultimo_controllo` recente e salta il commit.

## 23.3 — Setup iniziale (una sola volta, già fatto il 10 maggio 2026)

### Step 1 — Personal Access Token GitHub fine-grained

URL: <https://github.com/settings/personal-access-tokens/new>

Configurazione:

| Campo | Valore |
|---|---|
| Token name | `cron-job-org-pc-genzano` |
| Resource owner | `SviluppoItaliaDigitale` |
| Description | `Trigger esterno per check-allerta.yml ogni 5 min via cron-job.org` |
| Expiration | 1 anno (massimo consentito sui fine-grained) |
| Repository access | **Only select repositories** → `sito-pc-genzano` |
| Repository permissions | Actions: **Read and write** + Contents: **Read-only** + Metadata: **Read-only** (automatico) |

Il token va copiato **una sola volta** (GitHub non lo mostra più dopo). Inizia con `github_pat_`.

### Step 2 — Configurazione cron-job.org

Account gratuito su <https://cron-job.org/it/signup/>. Poi `Cronjobs → Crea cronjob`:

**Tab BASE:**

| Campo | Valore |
|---|---|
| Title | `PC Genzano — Allerta meteo polling` |
| URL | `https://api.github.com/repos/SviluppoItaliaDigitale/sito-pc-genzano/actions/workflows/check-allerta.yml/dispatches` |
| Attiva cronjob | ON |
| Salva risposte cronologia | ON (utile per debug) |
| Esecuzione programmata | Ogni 5 minuti |
| Espressione Crontab | `*/5 * * * *` (auto) |

**Tab AVANZATE:**

| Campo | Valore |
|---|---|
| Richiede autenticazione HTTP | OFF (autenticazione via Bearer header) |
| Fuso orario | Europe/Rome |
| Metodo HTTP richiesta | POST |
| Body della richiesta | `{"ref":"main"}` |
| Timeout | 30 secondi |

**Headers (5 righe):**

| Nome | Valore |
|---|---|
| `Content-Type` | `application/json` |
| `Accept` | `application/vnd.github+json` |
| `Authorization` | `Bearer github_pat_xxxxxxxxxxxxxxxxxxxx` (il PAT) |
| `X-GitHub-Api-Version` | `2022-11-28` |
| `User-Agent` | `cron-job.org-PC-Genzano-Bot` |

Test di esecuzione: deve restituire `204 No Content` con header `x-accepted-github-permissions: actions=write`.

### Step 3 — GitHub Secret per il workflow di controllo scadenza

Path: `Settings → Secrets and variables → Actions → New repository secret`

| Campo | Valore |
|---|---|
| Name | `CRONJOB_GH_PAT` |
| Secret | il valore del PAT (solo `github_pat_xxxxx...`, senza `Bearer`) |

Questo secret è usato **solo** dal workflow `controllo-scadenza-pat.yml` per leggere la scadenza del PAT via API. NON è usato per il trigger primario (quello è gestito da cron-job.org).

## 23.4 — Workflow di controllo scadenza PAT

File: `.github/workflows/controllo-scadenza-pat.yml`

Frequenza: 1° del mese alle 09:00 UTC (`cron: '0 9 1 * *'`).

Logica:

1. Chiama `https://api.github.com/user` con il PAT autenticato.
2. L'header di risposta `github-authentication-token-expiration` contiene la data di scadenza (i fine-grained la rivelano sempre).
3. Calcola giorni mancanti.
4. Se ≤30 giorni: apre/aggiorna issue `manutenzione`. Se ≤7 giorni: aggiunge label `urgente`.
5. Se PAT scaduto o invalido: issue immediata urgente.
6. Se >30 giorni: silenzioso (nessuna issue, nessun rumore).

Idempotenza: se esiste già una issue aperta sulla scadenza PAT, aggiunge un commento di update invece di duplicare.

Procedura di rinnovo (incollata automaticamente nel body della issue):

1. Genera nuovo PAT (1 anno) con stessi permessi
2. Aggiorna `Authorization` header su cron-job.org (Bearer + nuovo token)
3. Test di esecuzione (deve dare 204)
4. Aggiorna secret `CRONJOB_GH_PAT`
5. Elimina vecchio token
6. Chiudi issue

## 23.5 — Diagnostica e troubleshooting

### Sintomo: cron-job.org dà errori 401 o 403

- **401 Unauthorized**: il token è scaduto o errato. Genera nuovo PAT.
- **403 Forbidden**: il token non ha permessi sufficienti. Verifica:
  - Resource owner = `SviluppoItaliaDigitale`
  - Repository access = `sito-pc-genzano` selezionato
  - Permissions = Actions: Read and write
- **404 Not Found**: il workflow_dispatch non esiste. Verifica:
  - URL contiene `actions/workflows/check-allerta.yml/dispatches`
  - Il workflow ha la riga `workflow_dispatch:` in `on:`

### Sintomo: cron-job.org dà 204 ma il workflow non parte

- Verifica nel tab "Actions" GitHub se compare un run con event `workflow_dispatch`.
- Se compare ma rimane in coda: GitHub ha alto carico, attendi.
- Se non compare: il branch nel body è sbagliato (deve essere `{"ref":"main"}`).

### Sintomo: cron-job.org silenzioso, nessun trigger

- Verifica su <https://console.cron-job.org/jobs> che il cronjob sia "Attivo".
- Controlla la cronologia: se ci sono fallimenti consecutivi, cron-job.org può sospendere il job.
- In caso di sospensione, il fail-safe orario `17 * * * *` continua a fungere da paracadute.

### Sintomo: il workflow controllo-scadenza-pat.yml non apre issue anche con PAT scaduto

- Verifica che il secret `CRONJOB_GH_PAT` sia configurato (Settings → Secrets and variables → Actions).
- Se assente, il workflow logga warning ed esce pulito senza errori.
- Trigger manuale via Actions tab → "Controllo scadenza PAT" → "Run workflow".

## 23.6 — Storia tecnica

| Data | Evento |
|---|---|
| 2026-04-30 | Workflow `check-allerta.yml` creato con cron `0 * * * *` (orario, latenza fino a 60 min) |
| 2026-05-05 | Bot Telegram operativo (notifica-telegram.yml + secret BOT_TOKEN/CHAT_ID configurati) |
| 2026-05-10 09:33 | Tentativo cron `*/5 * * * *` per ridurre latenza |
| 2026-05-10 11:18 | Verifica empirica: 0 run scheduled in 42 minuti col `*/5` |
| 2026-05-10 11:33 | Tentativo cron espliciti `7,22,37,52 * * * *` |
| 2026-05-10 11:53 | Verifica: anche cron espliciti non onorati (0 run in 20 min) |
| 2026-05-10 14:10 | Decisione architettura: trigger esterno cron-job.org |
| 2026-05-10 14:18 | Primo test 403 (token con repository access vuoto) |
| 2026-05-10 14:22 | Token corretto: Repository access = sito-pc-genzano + Actions: write |
| 2026-05-10 14:27 | Test di esecuzione: **204 No Content**, latenza 1.36 sec |
| 2026-05-10 14:30 | Primo run automatico cron-job.org: workflow #397 lanciato puntuale |
| 2026-05-10 14:35 | Architettura doppio trigger fail-safe + workflow controllo scadenza |

## 23.7 — Riferimenti

- Workflow: `.github/workflows/check-allerta.yml`, `.github/workflows/controllo-scadenza-pat.yml`
- Configurazione cron-job.org: <https://console.cron-job.org/jobs>
- Token GitHub: <https://github.com/settings/personal-access-tokens>
- Secret GitHub: `Settings → Secrets and variables → Actions`
- Memoria Claude: `feedback_github_cron_explicit_better.md` nella memoria di sessione
- API GitHub: <https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event>
- Documentazione cron-job.org: <https://docs.cron-job.org/>
