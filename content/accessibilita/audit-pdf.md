---
title: "Audit accessibilità dei PDF pubblicati"
description: "Stato di accessibilità (PDF/UA, ISO 14289-1) di tutti i documenti PDF pubblicati sul sito. Aggiornato periodicamente."
layout: "single"
toc: false
tts: true
dataUltimaRevisione: "2026-05-28"
---

Pubblichiamo lo **stato di accessibilità di ogni PDF presente sul sito** in modo trasparente, come previsto dalla nostra [Dichiarazione di accessibilità](/accessibilita/) e dall'art. 3 della Legge Stanca (L. 4/2004).

La scadenza che ci siamo dati per l'audit completo è il **31 dicembre 2026**.

## Come leggere la tabella

- ✅ **Accessibile** — il documento ha testo selezionabile, tag strutturali (intestazioni, paragrafi, alt text), lingua dichiarata. Lo screen reader lo legge bene.
- 🟡 **Parziale** — il documento ha testo selezionabile ma non i tag strutturali. Lo screen reader lo legge, ma in modo lineare senza riconoscere intestazioni, liste, tabelle.
- 🔴 **Non accessibile** — il documento è una scansione senza livello testuale (OCR mancante). Va rifatto.
- ⚪ **Terzo ente** — il documento è prodotto da un ente esterno (Dipartimento Protezione Civile, Regione Lazio, ministeri, Comune). L'accessibilità è responsabilità dell'ente emittente, come previsto dalla normativa.

## Cosa stiamo facendo

Per i documenti **del Gruppo** in stato 🔴 o 🟡, abbiamo un piano in quattro fasi:

1. **Inventario completo** (in corso) — questa pagina è l'output della Fase 1.
2. **OCR automatico** dei PDF scansionati senza livello testuale.
3. **Versioni HTML equivalenti** sul sito per i documenti più consultati: l'HTML è sempre più accessibile del PDF.
4. **Nuovi PDF prodotti già conformi PDF/UA** dal sistema di generazione automatico.

Per i documenti **di terzi enti** in stato 🟡 o 🔴, il Gruppo applica il principio del **testo equivalente**: se trovi un PDF che il tuo screen reader non legge bene, scrivi a **[segreteria@protezionecivilegenzano.it](mailto:segreteria@protezionecivilegenzano.it)** e ti forniremo una versione alternativa o un testo equivalente.

## Tabella completa

{{< audit-pdf-table >}}

## Riferimenti normativi

- **Legge 9 gennaio 2004 n. 4** ("Legge Stanca") — Disposizioni per favorire e semplificare l'accesso degli utenti, in particolare delle persone con disabilità, agli strumenti informatici.
- **D.Lgs. 10 agosto 2018 n. 106** — Adeguamento alla direttiva UE 2016/2102 sull'accessibilità dei siti web e applicazioni mobili degli enti pubblici.
- **ISO 14289-1:2014** (PDF/UA-1) — Standard internazionale di accessibilità per documenti PDF.
- **WCAG 2.2 livello AA** — Standard W3C per l'accessibilità dei contenuti web, applicabile anche ai documenti.

## Aggiornamento dell'audit

L'audit è generato automaticamente dallo script `audit-pdf-accessibilita.py` che analizza ogni PDF pubblicato e ne valuta:

- la presenza di un livello testuale (testo selezionabile);
- la presenza di tag strutturali (intestazioni, paragrafi, immagini con alt text);
- la dichiarazione di lingua nel catalog del PDF;
- la presenza di un titolo nei metadati.

Lo script viene rilanciato periodicamente per tenere aggiornato lo stato. Data dell'ultima esecuzione e numero di documenti analizzati sono mostrati in cima alla tabella.
