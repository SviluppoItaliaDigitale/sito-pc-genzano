---
title: "PR — Conoscere la Protezione Civile (Onda 1)"
description: "Bozza descrizione PR. File di lavoro non pubblicato."
date: 2026-05-29
build:
  render: never
  list: never
  publishResources: false
---

# PR — Sezione "Conoscere la Protezione Civile" (Onda 1)

> File di lavoro, non pubblicato (`build: render: never`). Bozza della descrizione di Pull Request `feat/conoscere-protezione-civile-onda1` → `main`.

## Cosa fa questa PR

Avvia un nuovo livello **dottrinale** del sito: la protezione civile spiegata come materia, organizzata sulle quattro attività del Codice (D.Lgs. 1/2018). È un lavoro **additivo**: nessun contenuto esistente è stato modificato o spostato.

## File creati (`content/conoscere/`)

| File | URL | Contenuto |
|---|---|---|
| `_index.md` | `/conoscere/` | Landing: cos'è il livello, indice delle fasi, backlog futuro |
| `servizio-nazionale.md` | `/conoscere/servizio-nazionale/` | Componenti, strutture operative, livelli Stato/Regioni/Comuni, Sindaco |
| `le-quattro-fasi/_index.md` | `/conoscere/le-quattro-fasi/` | Panoramica + modello del rischio **R = P × V × E** |
| `le-quattro-fasi/previsione.md` | `…/previsione/` | Fase 1 |
| `le-quattro-fasi/prevenzione.md` | `…/prevenzione/` | Fase 2 |
| `le-quattro-fasi/soccorso.md` | `…/soccorso/` | Fase 3 (catena COC→COM→CCS→DiComaC) |
| `le-quattro-fasi/superamento.md` | `…/superamento/` | Fase 4 |
| `telecomunicazioni-emergenza/_index.md` | `/conoscere/telecomunicazioni-emergenza/` | Reti radio, radioamatori, IT-alert |
| `telecomunicazioni-emergenza/rete-zamberletti.md` | `…/rete-zamberletti/` | Consolida le frequenze già pubblicate |
| `rischio-vulcanico-colli-albani.md` | — | **STUB bozza** (`build: render: never`): solo outline + fonti INGV |
| `_FONTI-DA-VERIFICARE.md` | — | **Checklist non pubblicata** dei fatti da verificare |
| `_PR-DESCRIPTION.md` | — | Questo file (non pubblicato) |

## File modificati (navigazione)

- `hugo.toml` — nuova voce di primo livello "Conoscere la Protezione Civile" (dropdown, peso 2, subito dopo Home). Nessuna modifica al CSS della navbar.
- `static/app-shared/site-chrome.js` — stessa voce sincronizzata per le pagine statiche fuori da Hugo (`navDropdown-conoscere`), come richiesto dalla regola di coerenza menu.
- `content/mappa-sito/_index.md` — sezione "Conoscere la Protezione Civile" nella mappa del sito.

## Collisioni evitate

- `/storia/` (Storia del territorio) **non** toccata: la futura storia della PC userà uno slug diverso.
- `/normativa/`, `/strumenti/`, `/rischi-prevenzione/` non ricreate: le nuove pagine vi rimandano.
- La pagina operativa `/rischi-prevenzione/rischio-vulcanico/` resta separata dallo stub dottrinale.

## Verifiche fatte

- `hugo --minify` pulito; le 9 pagine pubblicabili rese; stub e file di lavoro **esclusi** dal build (`render: never`).
- Zero link interni rotti sulle pagine `/conoscere/` (nessuno span "Contenuto non ancora disponibile").
- Link agli articoli `/comunicazioni/` corretti al pattern reale con prefisso data.
- Voce di menu presente in homepage (Hugo) e in `site-chrome.js` (statiche), nell'ordine corretto.
- Disclaimer resi con il pattern `alert` già in uso sul sito (markdown→`<strong>` verificato nell'HTML).

## ⚠️ Da fare PRIMA del merge/pubblicazione (umano)

1. **Chiudere `content/conoscere/_FONTI-DA-VERIFICARE.md`**: verificare su Normattiva i numeri d'articolo del D.Lgs. 1/2018 e le fonti UNDRR/DPC marcate. I marker inline sono `<!-- FONTE-DA-VERIFICARE -->`.
2. **Rimandi reciproci**: valutare se aggiungere, dagli articoli `/comunicazioni/` riusati, un link alle nuove pagine `/conoscere/` (non fatto in Onda 1 per non modificare articoli datati senza revisione).
3. **Decidere se rimuovere i 3 file di lavoro** (`_FONTI-DA-VERIFICARE.md`, `_PR-DESCRIPTION.md`, lo stub vulcano) prima del merge, o lasciarli: sono comunque esclusi dal sito generato (`build: render: never`).

## ⚠️ Nota deploy (NON risolvere in questa PR)

L'aggiunta di una **voce di menu globale** cambia l'HTML renderizzato di **tutte** le pagine. Al momento del deploy va verificato che `FTP-Deploy-Action` ricarichi correttamente i file (scenario "file stantii su Aruba", rule `05-github-aruba-deploy.md`). Se necessario, applicare il pattern cache-bust sugli `_index.md` di sezione documentato nella rule 05. **Il deploy non è eseguito in questa PR** (nessun merge, nessun push su `main`).
