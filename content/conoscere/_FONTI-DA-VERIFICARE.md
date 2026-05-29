---
title: "Conoscere — Fonti da verificare (file di lavoro)"
description: "Checklist interna dei fatti da verificare prima di pubblicare la sezione Conoscere. NON pubblicato."
layout: "single"
date: 2026-05-29
build:
  render: never
  list: never
  publishResources: false
---

# Fonti da verificare — sezione `/conoscere/` (Onda 1)

> File di lavoro **non pubblicato** (`build: render: never`). È la checklist di revisione fattuale da chiudere **prima** del merge/deploy.
>
> Ogni voce corrisponde a un commento `<!-- FONTE-DA-VERIFICARE: ... -->` lasciato inline nei file. Cerca i marker con:
> `grep -rn "FONTE-DA-VERIFICARE" content/conoscere/`

## Legenda
- ⬜ da verificare · ✅ verificato · ✏️ corretto nel testo

---

## 1. `le-quattro-fasi/_index.md`

- ⬜ **Numero dell'articolo del D.Lgs 1/2018 che definisce le attività di protezione civile** (ritenuto **art. 2**) e relativo testo letterale.
  - Dove cercarlo: [Normattiva — D.Lgs. 1/2018](https://www.normattiva.it/) (testo consolidato); in alternativa [DPC — D.Lgs. 1/2018](https://www.protezionecivile.gov.it/it/normativa/decreto-legislativo-n-1-del-2-gennaio-2018/).
  - Nota: il DPC conferma la formula «previsione, prevenzione e mitigazione dei rischi, gestione delle emergenze e loro superamento». Resta da confermare **il numero d'articolo** prima di citarlo come tale.
- ⬜ **Fonte per la formula R = P × V × E** (Rischio = Pericolosità × Vulnerabilità × Esposizione).
  - Dove cercarlo: glossario [UNDRR](https://www.undrr.org/terminology) (Sendai); [ISPRA](https://www.isprambiente.gov.it/) (dissesto/rischio). Scegliere una fonte ufficiale e linkarla.

## 2. `servizio-nazionale.md`

- ⬜ **Articolo che elenca le COMPONENTI** del Servizio Nazionale (ritenuto **art. 4**).
  - Dove: Normattiva D.Lgs. 1/2018. (L'elenco Stato/Regioni/Province autonome/Città metropolitane/Province/Comuni è confermato dal DPC; manca solo il numero d'articolo.)
- ⬜ **Articolo che elenca le STRUTTURE OPERATIVE nazionali** (ritenuto **art. 13**) ed elenco aggiornato.
  - Dove: Normattiva D.Lgs. 1/2018. (Elenco confermato dal DPC.)
- ⬜ **Classificazione degli eventi/emergenze per livello** (tipo a/b/c) — articolo (ritenuto **art. 7**).
  - Dove: Normattiva D.Lgs. 1/2018.
- ⬜ **Articolo su funzioni dei Comuni e Sindaco autorità comunale di protezione civile** (ritenuto **art. 12**).
  - Dove: Normattiva D.Lgs. 1/2018.

## 3. `le-quattro-fasi/prevenzione.md`

- ⬜ **Articolo che definisce la prevenzione (strutturale e non strutturale)** (ritenuto **art. 2** e **art. 11**).
  - Dove: Normattiva D.Lgs. 1/2018.

## 4. `le-quattro-fasi/soccorso.md`

- ⬜ **Articolo che definisce la gestione dell'emergenza / assistenza alla popolazione**.
  - Dove: Normattiva D.Lgs. 1/2018.
- ⬜ **Definizioni e livello di COM, CCS, DiComaC** (Centro Operativo Misto, Centro Coordinamento Soccorsi, Direzione di Comando e Controllo).
  - Dove: [DPC](https://www.protezionecivile.gov.it/) e Direttive PCM sul modello di intervento. Verificare le definizioni esatte (la trattazione organica completa è rimandata a una sessione dedicata).
- ✅ Limite del volontariato sulla viabilità: già supportato da Codice della Strada artt. 11-12 (D.Lgs. 285/1992) + Circolare DPC 6/8/2018 (link nel testo). *Verificato come prassi consolidata del sito (rule 06).*

## 5. `le-quattro-fasi/superamento.md`

- ⬜ **Articoli su superamento dell'emergenza, dichiarazione dello stato di emergenza, ordinanze** (ritenuti **artt. 24-26**).
  - Dove: Normattiva D.Lgs. 1/2018.
- ⬜ **Durata massima dello stato di emergenza di rilievo nazionale e regole di proroga**; natura/limiti delle **OCDPC**.
  - Dove: Normattiva D.Lgs. 1/2018.
- ⬜ **Procedure AeDES e FAST** (denominazione esatta, descrizione, soggetti che le svolgono).
  - Dove: [DPC](https://www.protezionecivile.gov.it/) (sezione agibilità post-sisma).
- ⬜ **«Build back better» / Quadro di Sendai 2015-2030** — link alla fonte ufficiale.
  - Dove: [UNDRR — Sendai Framework](https://www.undrr.org/).

## 6. `telecomunicazioni-emergenza/_index.md`

- ⬜ **Descrizione tecnica di IT-alert** (tecnologia cell broadcast, soggetto gestore, scenari previsti).
  - Dove: sito ufficiale [IT-alert](https://www.it-alert.it/) e [DPC](https://www.protezionecivile.gov.it/).

## 7. `telecomunicazioni-emergenza/rete-zamberletti.md`

- ✅ **Frequenze radio** (VHF 144-146 MHz, UHF 430-440 MHz, HF, 145.500 MHz, CB 27 MHz canale 9): riusate **come da articolo già pubblicato** sul sito (verificate, come da istruzioni di sessione). Nessuna nuova frequenza inventata.
- ✅ **Slug degli articoli collegati** verificati e corretti al pattern con prefisso data (vedi sezione «Verifiche tecniche» qui sotto).

## 8. `rischio-vulcanico-colli-albani.md` (BOZZA, non pubblicata)

- ⬜ **Tutto il contenuto scientifico** è da scrivere in sessione dedicata, esclusivamente su fonti **INGV**. La pagina ha `build: render: never`: nessun fatto geologico è stato asserito in questa sessione, solo l'outline e i marker. Vedi i `<!-- FONTE-DA-VERIFICARE -->` nel file.

---

## Verifiche tecniche (non fattuali) da fare prima del merge

- ⬜ **Slug/URL degli articoli linkati**: confermare il pattern dei permalink di `content/comunicazioni/` (con o senza prefisso data) e che i link interni usati risolvano. Articoli citati:
  - `/comunicazioni/2026-04-29-nascita-dipartimento-protezione-civile-italia/` ✅ esiste
  - `/comunicazioni/2026-04-24-frane-movimenti-terreno-castelli-romani/` ✅ esiste
  - `/comunicazioni/2026-05-14-centro-operativo-comunale-coc/` ✅ esiste
  - `/comunicazioni/2026-04-13-frequenze-radio-emergenza-radioamatori-protezione-civile-1/` ✅ esiste
  - `/comunicazioni/2026-05-01-rete-zamberletti-499-esercitazione-radio/` ✅ esiste
  - `/comunicazioni/2026-05-02-rete-emergenza-metropolitana-roma-radioamatori/` ✅ esiste

  Tutti gli URL usano il **prefisso data** `AAAA-MM-GG-` (pattern dei permalink di `/comunicazioni/`, verificato in build). Risolti tutti in Hugo.
- ⬜ **Aggiungere il rimando reciproco** dagli articoli riusati verso le nuove pagine `/conoscere/` (rete-zamberletti, frane, COC, nascita-DPC). *Non fatto in Onda 1 per non modificare gli articoli datati senza revisione: valutare in fase di pubblicazione.*
- ⬜ **Build Hugo pulito** e **voce di menu** verificata visivamente (navbar Hugo + pagine statiche con `site-chrome.js`).
- ⬜ **Cache-bust FTP**: l'aggiunta di una voce di menu globale cambia l'HTML di tutte le pagine → al deploy verificare il re-upload (rule 05 § «File stantii su Aruba»).
