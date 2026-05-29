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

## Verifica fattuale — COMPLETATA (29 maggio 2026)

Tutti i fatti normativi puntuali sono stati **verificati su fonte primaria/istituzionale** e i marker `<!-- FONTE-DA-VERIFICARE -->` delle pagine pubblicabili sono stati chiusi. Dettaglio in `content/conoscere/_FONTI-DA-VERIFICARE.md`. In sintesi:

- **D.Lgs. 1/2018 verificato verbatim su Normattiva**: attività di PC = **art. 2** (con prevenzione strutturale/non strutturale ai commi 3-5, NON art. 11); componenti = **art. 4**; classificazione eventi a/b/c = **art. 7**; funzioni dei Comuni/Sindaco = **art. 12**; strutture operative = **art. 13**; stato di emergenza = **art. 24** (**durata max 12 mesi + proroga max 12**); ordinanze = **art. 25**.
- **DPC**: componenti, strutture operative, scheda **AeDES** ("Agibilità e Danno nell'Emergenza Sismica").
- **Ministero dell'Interno**: definizioni di **CCS / COM / DiComaC** (Metodo Augustus).
- **UNDRR**: Quadro di **Sendai 2015-2030** + *build back better*.
- **IT-alert**: sistema nazionale DPC, cell broadcast, operativo dal 2024.
- Citazioni e link aggiunti in ogni pagina; ogni numero d'articolo è ora sostanziato.

🔴 **Correzione collaterale**: in fase di verifica si è scoperto che **3 URL DPC inizialmente citati erano 404**. Corretti in tutte le pagine e ri-verificati 200:
- Codice → `…/normativa/decreto-legislativo-n1-del-2-gennaio-2018-codice-della-protezione-civile/`
- Legge 225/1992 → `…/normativa/legge-n225-del-24-febbraio-1992-0/`
- Servizio Nazionale → nuovo sottodominio `https://servizio-nazionale.protezionecivile.gov.it/`

## Rimandi reciproci — FATTI

Aggiunto un link alle pagine `/conoscere/` in fondo (sezione "Sul nostro sito") di **6 articoli `/comunicazioni/` riusati**, senza toccare `image:` né altro (solo +1 bullet ciascuno):
- nascita-DPC → `/conoscere/servizio-nazionale/`
- frane Castelli Romani → `/conoscere/le-quattro-fasi/prevenzione/`
- COC → `/conoscere/le-quattro-fasi/soccorso/`
- frequenze radio → `/conoscere/telecomunicazioni-emergenza/`
- Rete Zamberletti 499ª → `/conoscere/telecomunicazioni-emergenza/rete-zamberletti/`
- rete metropolitana Roma → `/conoscere/telecomunicazioni-emergenza/`

## Deploy / cache-bust — PREDISPOSTO

Il pattern cache-bust della rule 05 è stato **applicato preventivamente**: comment `<!-- cache-bust: 2026-05-29 … -->` aggiornato/aggiunto sugli 11 `_index.md` di sezione canonici. Così, quando la PR verrà mergiata, il re-upload FTP dei file di sezione è non ambiguo (il byte-content dei sorgenti cambia → il minifier rimuove il comment, quindi è invisibile agli utenti ma forza il diff). **Non è un blocco**: il rischio "file stantii" si materializza solo se un deploy resta bloccato per ore da fallimenti non correlati; il cache-bust è la rete di sicurezza già documentata. **Il deploy non è eseguito in questa PR** (nessun merge, nessun push su `main`): la verifica live post-deploy resta a carico dell'operatore umano.

## Da decidere PRIMA del merge (umano)

1. **Rischio vulcanico Colli Albani** (`rischio-vulcanico-colli-albani.md`): resta **bozza non pubblicata** (`render: never`), da completare in sessione INGV dedicata. I suoi 7 marker `FONTE-DA-VERIFICARE` sono volutamente ancora aperti.
2. **File di lavoro** (`_FONTI-DA-VERIFICARE.md`, `_PR-DESCRIPTION.md`, stub vulcano): decidere se rimuoverli prima del merge o lasciarli — sono comunque esclusi dal sito (`build: render: never`).
