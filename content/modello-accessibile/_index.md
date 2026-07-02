---
title: "Un modello replicabile: comunicare l'emergenza a tutti"
description: "Come il Gruppo di Genzano ha costruito una piattaforma d'informazione accessibile per progettazione e privacy-first per la protezione civile."
layout: "single"
language: "it"
hreflang:
  - lang: "it"
    url: "/modello-accessibile/"
  - lang: "en"
    url: "/english/about-this-practice/"
  - lang: "fr"
    url: "/francais/about-this-practice/"
  - lang: "de"
    url: "/deutsch/about-this-practice/"
sitemap:
  priority: 0.6
  changefreq: yearly
---

**Una nota di buona pratica per la comunità della protezione civile e della riduzione del rischio.**

Il **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma** è un'organizzazione di volontariato (OdV) del Comune di Genzano di Roma, parte del Servizio Nazionale della Protezione Civile. Come ogni gruppo comunale, il nostro lavoro principale è sul campo: prevenzione, monitoraggio e assistenza alla popolazione prima, durante e dopo le emergenze — terremoti, alluvioni, incendi, maltempo.

Questa pagina racconta qualcosa di meno comune: la **piattaforma pubblica d'informazione** che abbiamo costruito attorno a quel lavoro, e le scelte di progettazione che ne fanno un **modello trasferibile**, non solo un sito.

## Il problema che volevamo risolvere

L'informazione d'emergenza spesso raggiunge chi ne ha meno bisogno e manca chi ne ha di più: anziani, persone con disabilità, persone con bassa alfabetizzazione, chi non parla italiano, chiunque sia sotto stress. Abbiamo trattato l'**accessibilità non come un adempimento finale, ma come il punto di partenza** della progettazione: se un messaggio non raggiunge *tutti*, non è davvero pubblicato.

## Come funziona

La piattaforma è un **sito statico, privacy-first** (nessun tracciamento, nessun cookie per i contenuti, nessun video di terze parti incorporato), con l'accessibilità costruita in ogni livello:

- **Accessibilità tecnica — WCAG 2.2 AA.** HTML semantico, navigazione da tastiera, focus visibile, contrasto calcolato e una **barra degli strumenti di accessibilità** nativa (dimensione del testo, spaziatura, alto contrasto e contrasto invertito, carattere ad alta leggibilità e per dislessia, riduzione delle animazioni). Evitiamo di proposito gli *overlay* commerciali, sconsigliati dal W3C-WAI e dalle associazioni delle persone con disabilità.
- **Lettura ad alta voce ovunque.** Un pulsante di sintesi vocale nativo del browser (Web Speech API, senza costi né servizi esterni) su ogni pagina di contenuto, con tempo di lettura stimato e sillabazione automatica.
- **Accesso cognitivo.** Versioni in **linguaggio facile da leggere**, **pittogrammi** standardizzati (ISO 7010 + ARASAAC) e un glossario che spiega le sigle alla prima occorrenza.
- **Comunicazione Aumentativa Alternativa (CAA).** **Tabelle di comunicazione** stampabili con pittogrammi ARASAAC, perché chi in emergenza non riesce a parlare — per afasia, disabilità cognitiva, stress o perché non parla italiano — possa **indicare** ciò di cui ha bisogno.
- **Lingua dei Segni.** Un catalogo di contenuti in **Lingua dei Segni Italiana (LIS)**.
- **Braille.** Per ogni notizia viene generato automaticamente, nella nostra pipeline di pubblicazione, un **file Braille (BRF)** pronto per la stampa (libreria open source *liblouis*): un canale reale verso le persone cieche e ipovedenti, complementare allo screen reader.
- **Accesso linguistico.** Le informazioni essenziali sono disponibili in **otto lingue** (italiano più inglese, francese, tedesco, spagnolo, portoghese, rumeno ed esperanto), con gestione corretta di `lang`/`hreflang`; i contenuti in linguaggio facile sono offerti anche in altre lingue, incluso l'arabo.

Attorno a questo nucleo di accessibilità stanno gli strumenti di preparazione: pagine sui rischi con struttura costante *prima / durante / dopo*, **kit di emergenza dedicati alle categorie vulnerabili**, un **piano familiare salvabile offline**, giochi e quiz per le scuole, un **cruscotto in tempo reale** (dati sismici, meteo, qualità dell'aria e del mare da fonti ufficiali come INGV e Open-Meteo) e **dossier interattivi** sulla storia dei rischi del territorio.

## Standard e fonti

Ogni affermazione è riconducibile a una fonte istituzionale primaria. La nostra gerarchia di riferimento: Dipartimento della Protezione Civile (DPC) e linee guida AgID per prime; enti scientifici nazionali (CNR, ISPRA, INGV); riferimenti operativi europei (EENA e il numero unico di emergenza **112**); standard internazionali — **WCAG 2.2 AA**, **ISO 22329** (social media nelle emergenze) e riferimenti umanitari come **Sphere** e **IFRC** per i kit delle categorie vulnerabili.

## Perché è replicabile

L'intera piattaforma gira su **tecnologia aperta, standard e a basso costo**: un generatore di siti statici, un design system aperto, API native del browser e strumenti open source (liblouis per il Braille, pittogrammi ARASAAC). Nessun CMS proprietario, nessun server a runtime, nessun costo di licenza, hosting semplicissimo. Qualunque ente locale o organizzazione di volontariato può riprodurre il modello: la parte difficile non è la tecnologia, ma la **disciplina editoriale** di trattare l'accessibilità come requisito di partenza.

## Riconoscimenti

Il Gruppo è organizzazione accreditata dal **Corpo europeo di solidarietà** (Quality Label, codice organizzazione **E10435833**, Regolamento (UE) 2021/888), ed è affiliato a **SNPC Volontariato** e al coordinamento **FE.PI.VOL.**

---

**Contatti.** Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma — Via Sicilia 13-15, 00045 Genzano di Roma (RM) · segreteria@protezionecivilegenzano.it · [www.protezionecivilegenzano.it](https://www.protezionecivilegenzano.it/)

*Siamo lieti di condividere il nostro approccio e i nostri materiali con altre organizzazioni di protezione civile e con chi si occupa di riduzione del rischio.*
