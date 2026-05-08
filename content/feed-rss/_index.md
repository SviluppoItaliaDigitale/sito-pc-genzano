---
title: "Feed RSS — ricevi le notizie del Gruppo come preferisci"
description: "Tutti i feed RSS del sito del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma. Iscriviti per ricevere le novità del sito direttamente nel tuo aggregatore o nella tua casella email."
layout: "single"
toc: true
---

I **feed RSS** sono un modo semplice e gratuito per **ricevere automaticamente** le novità del nostro sito senza dover passare ogni giorno a controllarle. Il sito del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma pubblica feed RSS per ogni sezione, generati automaticamente a ogni aggiornamento.

## Cos'è un feed RSS, in pratica

Un feed RSS è un **file XML** che il nostro sito pubblica automaticamente, con la lista degli ultimi articoli (titolo, data, breve descrizione, link). Quando pubblichiamo un nuovo articolo, il feed si aggiorna **subito**.

Tu, dal tuo aggregatore (un programma o un'app), **chiedi al feed** se ci sono novità. Se ce ne sono, ti arrivano. Niente registrazione, niente email da darci, niente cookie, **nessun dato tuo che esca dal tuo dispositivo**.

È una tecnologia nata negli anni Duemila per i blog ed è ancora oggi lo **standard più affidabile** per il monitoraggio di un sito istituzionale: nessun social-network in mezzo, nessun algoritmo di selezione, nessuna pubblicità.

## Come iscriversi (3 modi)

### 1. Aggregatore web (il più semplice per chi non vuole installare nulla)

- **[Feedly](https://feedly.com/)** — gratuito, funziona dal browser e da app smartphone
- **[Inoreader](https://www.inoreader.com/)** — gratuito, anche con notifiche push
- **[NewsBlur](https://newsblur.com/)** — gratuito, open source

Ti registri (con un'email a tua scelta), incolli l'URL di uno dei feed qui sotto, e da quel momento le nostre notizie compaiono nel tuo aggregatore.

### 2. Programma desktop o mobile

- **[Thunderbird](https://www.thunderbird.net/)** (Windows/Mac/Linux) — gratuito, open source. Da menu *Conti → Nuovo account → Feed*.
- **[NetNewsWire](https://netnewswire.com/)** (Mac/iOS) — gratuito, open source.
- **[Read You](https://github.com/Ashinch/ReadYou)** (Android) — gratuito, open source.

### 3. Auto-discovery del browser

Se usi **Firefox** con l'estensione "RSS Preview" o **Edge** con l'estensione "Feedbro", l'icona RSS del feed compare automaticamente quando visiti una pagina del nostro sito che ha un feed associato.

## I nostri feed

| Argomento | URL del feed |
|---|---|
| **🏠 Tutto il sito (sintesi homepage)** | [`https://www.protezionecivilegenzano.it/index.xml`](https://www.protezionecivilegenzano.it/index.xml) |
| **📰 Comunicazioni e notizie** (il più consultato) | [`https://www.protezionecivilegenzano.it/comunicazioni/index.xml`](https://www.protezionecivilegenzano.it/comunicazioni/index.xml) |
| **🌧️ Allerte meteo** | [`https://www.protezionecivilegenzano.it/allerte-meteo/index.xml`](https://www.protezionecivilegenzano.it/allerte-meteo/index.xml) |
| **⚠️ Rischi e prevenzione** | [`https://www.protezionecivilegenzano.it/rischi-prevenzione/index.xml`](https://www.protezionecivilegenzano.it/rischi-prevenzione/index.xml) |
| **📋 Piano di emergenza** | [`https://www.protezionecivilegenzano.it/piano-emergenza/index.xml`](https://www.protezionecivilegenzano.it/piano-emergenza/index.xml) |
| **👨‍👩‍👧 Piano familiare** | [`https://www.protezionecivilegenzano.it/piano-familiare/index.xml`](https://www.protezionecivilegenzano.it/piano-familiare/index.xml) |
| **📞 Numeri utili** | [`https://www.protezionecivilegenzano.it/numeri-utili/index.xml`](https://www.protezionecivilegenzano.it/numeri-utili/index.xml) |
| **🎓 Formazione** | [`https://www.protezionecivilegenzano.it/formazione/index.xml`](https://www.protezionecivilegenzano.it/formazione/index.xml) |
| **🤝 Diventa volontario** | [`https://www.protezionecivilegenzano.it/diventa-volontario/index.xml`](https://www.protezionecivilegenzano.it/diventa-volontario/index.xml) |
| **🗺️ Cartografia** | [`https://www.protezionecivilegenzano.it/cartografia/index.xml`](https://www.protezionecivilegenzano.it/cartografia/index.xml) |
| **📖 Glossario PC** | [`https://www.protezionecivilegenzano.it/glossario/index.xml`](https://www.protezionecivilegenzano.it/glossario/index.xml) |
| **📚 Standard ISO per la PC** | [`https://www.protezionecivilegenzano.it/standard-iso/index.xml`](https://www.protezionecivilegenzano.it/standard-iso/index.xml) |
| **❓ Domande frequenti (FAQ)** | [`https://www.protezionecivilegenzano.it/faq/index.xml`](https://www.protezionecivilegenzano.it/faq/index.xml) |
| **💼 Area download** | [`https://www.protezionecivilegenzano.it/area-download/index.xml`](https://www.protezionecivilegenzano.it/area-download/index.xml) |

Per chi cerca **una sola iscrizione**: il feed [Comunicazioni e notizie](https://www.protezionecivilegenzano.it/comunicazioni/index.xml) è il più aggiornato e contiene allerte, attività, comunicazioni istituzionali e tutto ciò che pubblicheremo nel sito.

## Cosa NON troverai nei feed

I feed RSS sono pensati per le **novità del sito** (articoli, comunicazioni, nuove pagine). Non comprendono:

- I dati dinamici di **stato allerta** (quelli sono in `data/allerta.json` e nella barra di stato della homepage);
- Lo stato di **modalità emergenza** (in `data/emergenza.json` e nel banner emergenza);
- I **commenti dei social** o aggiornamenti istantanei (per quelli, segui i nostri canali Facebook, Instagram, X, Telegram).

Per le **emergenze in corso** il feed RSS non è il canale primario: usa l'app **IT-alert** del Dipartimento di Protezione Civile, le **allerte meteo** della Regione Lazio, e in caso di **pericolo immediato** chiama il **112**.

## Tecnologia e privacy

I nostri feed sono generati da **[Hugo](https://gohugo.io/)** (motore statico open source) come parte normale della build del sito. Sono **standard RSS 2.0** + auto-discovery via `<link rel="alternate" type="application/rss+xml">` nell'`<head>` di tutte le pagine.

Da un punto di vista **privacy**:
- I feed sono **file statici pubblici**: non c'è registrazione, non c'è tracciamento, non c'è cookie.
- Quando il tuo aggregatore scarica il feed, il nostro server vede solo l'IP e l'user-agent (come per qualsiasi visita al sito) — i log standard del server, gestiti come da [Privacy Policy](/privacy/).
- I feed **non contengono mai dati personali** dei lettori del sito.

## Per altri Comuni e Gruppi PC

Se gestisci un Gruppo di Volontariato di Protezione Civile e vuoi monitorare le nostre attività per condividere o riusare i materiali (i nostri [Kit Calamità](/formazione/kit-calamita/) e i contenuti formativi sono **rilasciati liberamente**), il feed [Comunicazioni](https://www.protezionecivilegenzano.it/comunicazioni/index.xml) è il modo più ordinato per restare aggiornato.

## Aiuto

Se non riesci a configurare l'iscrizione o se uno dei link sopra non funziona, scrivici dalla pagina [Contatti](/contatti/). Risponderemo nei tempi indicati nella [Social Media Policy](/social-media-policy/).
