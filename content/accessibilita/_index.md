---
title: "Dichiarazione di accessibilità"
description: "Dichiarazione di accessibilità conforme al modello AGID. Stato di conformità, contenuti non accessibili, modalità di valutazione, obiettivi annuali, feedback e contatti."
layout: "single"
toc: true
tts: true
dataUltimaRevisione: "2026-05-10"
aliases:
  - /dichiarazione-accessibilita.html
---

Questa pagina contiene la dichiarazione di accessibilità del sito della Protezione Civile di Genzano di Roma, redatta secondo il modello AGID e conforme alla **Direttiva (UE) 2016/2102**, alla **Legge 9 gennaio 2004 n. 4** ("Stanca") e al **D.Lgs. 10 agosto 2018 n. 106**.

La dichiarazione si applica al sito **www.protezionecivilegenzano.it**.

## Stato di conformità

Il sito è **parzialmente conforme** ai requisiti previsti dalla **WCAG 2.2 livello AA** e dallo standard **EN 301 549**, con **tendenza esplicita alla piena conformità**.

**Cosa è conforme al 100%** (verificato il 2026-05-10 con audit automatico Lighthouse + axe-core):

- **Accessibilità: 100/100** mediana stabile su 9 run × 3 URL rappresentative (home, archivio comunicazioni, numeri utili).
- **Best Practices: 100/100** mediana stabile.
- **SEO: 100/100** mediana stabile.
- **Performance: 95/100** mediana stabile (LCP 2.3 s, TBT 70-130 ms, CLS 0.024-0.058 — Web Vitals tutti "Good").
- **Contrasto colore WCAG AA**: tutti gli elementi testuali del sito hanno contrasto ≥ 4.5:1 verificato.
- **Navigazione da tastiera**: l'intero sito è navigabile con Tab/Shift+Tab/Enter/Esc, nessuna trappola da tastiera.
- **Focus visibile**: ogni elemento interattivo ha outline visibile (3px) al focus.
- **Skip link**: "Vai al contenuto principale" presente in cima a tutte le pagine.
- **Landmark ARIA**: header/nav/main/footer presenti su tutte le pagine.
- **Alt text**: tutte le immagini informative hanno descrizione testuale, le decorative hanno `alt=""`.
- **Lingua dichiarata**: ogni pagina dichiara `<html lang>` correttamente, anche per le 7 traduzioni.
- **`<th scope="col">` automatico**: tutte le 400+ tabelle Markdown del sito sono rese con intestazioni accessibili.
- **Pittogrammi standardizzati**: 46 segnali ISO 7010 + 125 ARASAAC integrati per supportare comprensione cognitiva (bambini, anziani, italiano L2, persone con disabilità cognitive).
- **TTS "Leggi ad alta voce"** nativo (Web Speech API) attivo su tutte le pagine non legali e funzionali.
- **Toolbar di accessibilità** utente con 11 preferenze persistenti (dimensione testo, contrasto invertito, scala di grigi, font ad alta leggibilità, spaziatura, animazioni, evidenza link, cursore grande, ecc.).
- **Selettore velocità TTS** (lento/normale/veloce) persistito in `localStorage`.
- **Hreflang + `<html lang>` dinamico**: le 7 traduzioni dichiarano correttamente la lingua nel markup.
- **Sillabazione automatica** (`hyphens: auto`) per dislessici e parlanti italiano L2.
- **Glossario inline** con popover accessibili per sigle tecniche (DPC, COC, IT-alert, ecc.).
- **Bottoni share social** privacy-first senza tracker, con `aria-label` descrittivi.

## Contenuti non accessibili

Le seguenti aree del sito **non sono pienamente accessibili** per i motivi indicati. Il Gruppo si impegna a migliorare progressivamente.

### Widget di terze parti
- **Strumenti meteo embed**: Windy.com, INGV mappa sismica, Radar DPC, MeteoAM, Blitzortung. Sono caricati con sistema **click-to-load** (l'utente sceglie esplicitamente di attivarli). L'interfaccia interna dei widget dipende dal fornitore esterno e non è sotto il nostro controllo.
- **Motivazione**: contenuto di terze parti (art. 3, comma 6, Direttiva UE 2016/2102 — esenzione per contenuti di terzi non sviluppati né finanziati né controllati).
- **Mitigazione**: per ogni widget è disponibile un link al sito ufficiale del fornitore, dove il cittadino può accedere ai contenuti con le opzioni di accessibilità del fornitore stesso.

### Documenti PDF storici nell'Area Download
- **Alcuni PDF pre-2022** nell'Area Download (vecchi piani comunali, carte tematiche scansionate, ordinanze d'archivio) potrebbero non avere OCR completo e non rispettare PDF/UA.
- **Motivazione**: documenti scansionati ricevuti da enti terzi (Comune, Regione, Prefettura), non rigenerabili dal Gruppo.
- **Mitigazione**: per ogni PDF storico critico, il sito offre una pagina HTML equivalente accessibile. È in corso un audit progressivo per rigenerare i PDF con OCR completo e tag PDF/UA.

### Mappe interattive
- Le mappe Leaflet/MapLibre eventualmente integrate hanno limiti di interazione da sola tastiera per il pan/zoom (limite intrinseco delle librerie SVG-based).
- **Mitigazione**: ogni mappa è sempre affiancata da una versione testuale equivalente (lista dei punti raduno, indirizzi, coordinate).

## Redazione della dichiarazione

- **Dichiarazione redatta il**: 10 maggio 2026.
- **Metodo di redazione**: **autovalutazione** condotta dal soggetto pubblico ai sensi dell'art. 3, comma 1, della Decisione di esecuzione (UE) 2018/1523.
- **Data ultima revisione**: 10 maggio 2026.
- **Prossimo riesame previsto**: 10 maggio 2027 (riesame annuale obbligatorio ai sensi della normativa italiana ed europea sull'accessibilità).
- **Frequenza dei test automatici**: settimanale (workflow `audit-sito.yml` ogni lunedì) + post-deploy (workflow `lighthouse-audit.yml` dopo ogni pubblicazione).

## Informazioni sul sito

- **URL**: <https://www.protezionecivilegenzano.it/>
- **Editore**: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
- **Tecnologie utilizzate**: Hugo 0.161+ (generatore statico), Bootstrap Italia 2.x (design system AGID/Designers Italia), HTML5, CSS3, JavaScript ES6 (Web Speech API per TTS, IntersectionObserver per lazy-load).
- **Hosting**: Aruba S.p.A. (HTTPS forzato, HSTS attivo, header di sicurezza X-Content-Type-Options/X-Frame-Options/Referrer-Policy/Permissions-Policy/HSTS).
- **Compatibilità browser**: Chrome ≥ 88, Firefox ≥ 78, Safari ≥ 14, Edge ≥ 88, browser mobili moderni. Su browser legacy il sito resta utilizzabile con degradazione progressiva.
- **Compatibilità tecnologie assistive**: testato con **NVDA** (Windows), **VoiceOver** (macOS/iOS), **TalkBack** (Android), screen reader integrati Chrome/Firefox.

## Modalità di valutazione

L'autovalutazione è stata condotta combinando strumenti automatici e test manuali:

### Strumenti automatici
- **Google Lighthouse 12** (Chrome DevTools + GitHub Actions), audit Performance / Accessibilità / Best Practices / SEO con configurazione `lighthouserc.json` (3 run × 3 URL, mediana, mobile).
- **axe-core** (integrato in Lighthouse) per validazione WCAG 2.2 AA.
- **Workflow GitHub Actions**: audit settimanale `audit-sito.yml` (oltre 40 sezioni di controllo), audit post-deploy `lighthouse-audit.yml`, link checker `check-links-sito.yml` (lychee).

### Test manuali
- **Navigazione completa da tastiera**: percorsi di Tab/Shift+Tab/Enter/Esc su home, articoli, archivio, mappa, assistente guidato, modulo cerca, toolbar accessibilità, modale SOS-112.
- **Test contrasto colore**: verifica WCAG AA (≥ 4.5:1) per testo normale e (≥ 3:1) per testo grande.
- **Test focus visibile**: ogni elemento interattivo ha outline ≥ 3 px e `outline-offset` adeguato.
- **Test gerarchia titoli**: un solo H1 per pagina, H2/H3 in ordine logico senza salti di livello.

### Test con tecnologie assistive
- **NVDA** (Windows) — letture full-page e percorsi narrazione.
- **VoiceOver** (macOS/iOS) — gesture rotor, lettura per landmark.
- **TalkBack** (Android) — gesture esplora-tocca, lettura strutturata.

### Pagine campione testate
Home, archivio comunicazioni, articolo singolo, numeri utili, contatti, accessibilità, privacy, assistente guidato, mappa cartografia, almeno una pagina per ognuna delle 7 traduzioni.

## Obiettivi di accessibilità (2026-2027)

Il Gruppo si impegna a raggiungere la **piena conformità WCAG 2.2 AA** entro il 10 maggio 2027 attraverso i seguenti obiettivi:

1. **Audit completo dei PDF storici** dell'Area Download: rigenerazione con OCR completo e tag PDF/UA per i documenti pre-2022 che lo richiedano. Scadenza: 31 dicembre 2026.
2. **Trascrizione testuale** di eventuali video YouTube/Vimeo embed presenti nel sito. Scadenza: continua, all'atto della pubblicazione.
3. **Mantenimento Lighthouse A11y = 100/100** verificato dall'audit automatico settimanale; in caso di regressione, intervento entro 7 giorni.
4. **Sostituzione progressiva dei widget di terze parti** non accessibili con alternative native quando disponibili (es. mappe self-hosted con tile OpenStreetMap per ridurre dipendenza da Windy/altri).
5. **Formazione annuale** dei volontari redattori su scrittura inclusiva AGID, WCAG 2.2 e linguaggio della PA. Riferimenti: Designers Italia, Writing Toolkit, Content Toolkit.
6. **Audit di accessibilità di terzi qualificati** entro il 31 dicembre 2027 per validare l'autovalutazione.

## Criteri adottati

Il sito è progettato per facilitare la consultazione da computer, tablet e smartphone. In particolare:

- struttura le pagine con titoli ordinati;
- usa testi alternativi per le immagini significative;
- mantiene colori e contrasti leggibili (WCAG AA verificato, ≥ 4.5:1);
- permette la navigazione da tastiera completa, senza trappole;
- usa link descrittivi (mai "clicca qui" o "leggi di più" senza contesto);
- segnala dimensione e tipo dei file scaricabili (es. "PDF, 120 KB");
- evita, dove possibile, testi troppo lunghi o tecnici;
- rispetta le preferenze di sistema per movimento ridotto e tema colore (`prefers-reduced-motion`, `prefers-color-scheme`).

## Strumenti di accessibilità del sito

In ogni pagina, in basso a sinistra, trovi un pulsante rotondo blu con l'icona di accessibilità. Aprendo il pannello puoi:

- ingrandire il testo;
- cambiare l'allineamento dei paragrafi;
- attivare un carattere ad alta leggibilità;
- aumentare spaziatura di righe e lettere;
- attivare contrasto alto o contrasto invertito;
- visualizzare il sito in scala di grigi;
- nascondere immagini decorative;
- mettere in pausa le animazioni;
- evidenziare i link;
- attivare un cursore grande;
- nascondere i pulsanti flottanti, se coprono il testo su telefono.

Le preferenze restano salvate sul dispositivo. Puoi cancellarle con il pulsante **Reimposta tutto**.

Il pannello è utilizzabile anche da tastiera: si apre con `Invio`, si naviga con `Tab` e si chiude con `Esc`.

## Lettura ad alta voce

In molte pagine trovi il pulsante **Leggi ad alta voce**. Il browser legge il contenuto con la voce italiana disponibile sul tuo dispositivo.

La funzione:

- è gratuita;
- non invia il testo a server esterni;
- usa le funzionalità del browser e del sistema operativo;
- permette di scegliere la velocità di lettura.

Può essere utile per anziani, persone con dislessia, bambini, persone che leggono lentamente o persone sotto stress durante un'emergenza.

## Glossario e supporti alla lettura

Il sito usa anche strumenti di supporto cognitivo:

- tempo di lettura stimato negli articoli;
- definizioni brevi per alcune sigle e parole tecniche;
- link al [glossario completo](/glossario/);
- sillabazione automatica del browser, dove disponibile;
- pagina [Facile da leggere](/facile-da-leggere/) con frasi brevi e indicazioni essenziali.

## Browser e lettura vocale

La lettura vocale funziona con i principali browser, tra cui Chrome, Firefox, Safari, Edge e browser mobili moderni.

In alcuni browser orientati alla privacy, come Tor Browser o configurazioni molto restrittive di Brave e LibreWolf, la lettura vocale può essere disattivata. Non è un errore del sito: è una scelta del browser per ridurre il rischio di tracciamento tramite le voci installate sul dispositivo.

## Strumenti del dispositivo

Per esigenze avanzate, usa anche gli strumenti del sistema operativo o del browser.

### Zoom della pagina

- **Windows / Linux:** `Ctrl` + `+`, `Ctrl` + `-`, `Ctrl` + `0`.
- **macOS:** `Cmd` + `+`, `Cmd` + `-`, `Cmd` + `0`.
- **Tablet e smartphone:** usa il gesto con due dita per ingrandire.

### Lettori di schermo

- **Windows:** NVDA o JAWS.
- **macOS, iPhone e iPad:** VoiceOver.
- **Android:** TalkBack.

### Contrasto e tema scuro

Puoi impostare contrasto elevato, tema scuro, dimensione testo e riduzione animazioni dalle impostazioni di accessibilità del tuo dispositivo.

## Contenuti di terze parti

Alcune pagine includono widget e strumenti esterni, per esempio Windy.com, INGV, Radar DPC, MeteoAM e Blitzortung.

Questi contenuti sono caricati con un sistema **click-to-load**: prima compare un riquadro informativo e il contenuto esterno viene caricato solo se scegli di aprirlo.

Quando carichi un widget, l'interfaccia interna del servizio esterno dipende dal fornitore. Quando possibile, il sito offre anche un link alternativo al sito ufficiale del servizio.

La pagina [Strumenti in tempo reale](/strumenti/) elenca gli strumenti usati e distingue le fonti istituzionali dagli strumenti di consultazione.

## Feedback e segnalazioni

Se trovi un problema che ti impedisce di usare il sito o di accedere a un contenuto, puoi segnalarlo con questi recapiti:

- **Email:** [segreteria@protezionecivilegenzano.it](mailto:segreteria@protezionecivilegenzano.it)
- **Telefono:** [+39 06 9362600](tel:+39069362600)

Nella segnalazione indica, se possibile:

- pagina interessata;
- problema riscontrato;
- dispositivo usato;
- browser usato;
- eventuale tecnologia assistiva utilizzata.

Cercheremo di rispondere entro 30 giorni.

## Procedura di attuazione

Ai sensi dell'art. 3-quinquies della Legge 9 gennaio 2004 n. 4, in caso di risposta assente o insoddisfacente entro 30 giorni dalla segnalazione, puoi rivolgerti al **Difensore civico per il digitale** dell'Agenzia per l'Italia Digitale (AGID), che è l'autorità di vigilanza preposta al monitoraggio della conformità all'accessibilità delle pubbliche amministrazioni italiane.

- **Sito ufficiale**: [agid.gov.it — Difensore civico per il digitale](https://www.agid.gov.it/it/design-servizi/accessibilita/difensore-civico-digitale)
- **Modulo di reclamo**: disponibile sul portale AGID con istruzioni per il deposito.

## Risorse utili

- [AGID — Accessibilità](https://www.agid.gov.it/it/design-servizi/accessibilita)
- [Designers Italia](https://designers.italia.it/)
- [W3C Web Accessibility Initiative](https://www.w3.org/WAI/)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

## Vedi anche

- [Privacy e cookie policy](/privacy/) — dati, cookie e widget esterni
- [Facile da leggere](/facile-da-leggere/) — istruzioni essenziali in linguaggio semplice
- [Glossario](/glossario/) — sigle e termini tecnici spiegati
- [Strumenti in tempo reale](/strumenti/) — servizi esterni e fonti di consultazione
