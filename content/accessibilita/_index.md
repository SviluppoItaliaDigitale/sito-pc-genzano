---
title: "Dichiarazione di accessibilità"
description: "Dichiarazione di accessibilità conforme al modello AGID. Stato di conformità, contenuti non accessibili, modalità di valutazione, obiettivi annuali, feedback e contatti."
layout: "single"
toc: true
tts: true
dataUltimaRevisione: "2026-05-12"
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

- ingrandire il testo (quattro livelli, fino al 150 per cento);
- cambiare l'allineamento dei paragrafi (predefinito, a sinistra, giustificato);
- scegliere il **tipo di carattere**: predefinito, ad alta leggibilità (Verdana/Tahoma), oppure **OpenDyslexic** (carattere disegnato per persone con dislessia, opzionale);
- aumentare la spaziatura di righe e lettere;
- attivare la **Modalità lettura**: sfondo crema, riga di lettura ottimale (65 caratteri), spaziatura aumentata, allineamento a sinistra forzato. Pensata per ridurre la fatica visiva nelle letture lunghe;
- scegliere il **contrasto** tra cinque varianti: predefinito, alto (nero su bianco), invertito (bianco su nero), giallo su nero (stile Windows ad alto contrasto), blu su crema (stile BBC My Web My Way per dislessia e ipovisione);
- regolare la **velocità della lettura ad alta voce** (lenta, normale, veloce) direttamente dal pannello — la scelta si applica subito al bottone "Leggi ad alta voce";
- visualizzare il sito in scala di grigi;
- nascondere le immagini decorative;
- mettere in pausa le animazioni;
- evidenziare tutti i link;
- attivare un cursore grande;
- nascondere i pulsanti flottanti (Assistente virtuale, SOS 112, selettore lingua) se coprono il testo, soprattutto da telefono.

Le preferenze restano salvate sul dispositivo. Puoi cancellarle con il pulsante **Reimposta tutto**.

Il pannello è utilizzabile anche da tastiera: si apre con `Invio`, si naviga con `Tab` e si chiude con `Esc`.

## Font utilizzati

Il sito usa di base un carattere sans-serif moderno, leggibile su tutti i dispositivi. Dal pannello **Strumenti di accessibilità** puoi attivare due alternative:

- **Carattere ad alta leggibilità**: passa il testo a Verdana o Tahoma, due caratteri sans-serif considerati più leggibili da molte persone, in particolare anziani e ipovedenti. Sono già installati sul tuo dispositivo, non viene scaricato nulla.
- **Carattere OpenDyslexic** (in fase di attivazione): un carattere disegnato per persone con dislessia. Le lettere hanno una base più pesante, pensata per ridurre i ribaltamenti tipici (b/d, p/q). Le evidenze scientifiche sul beneficio sono **discusse**: alcuni studi non hanno trovato miglioramenti misurabili rispetto a Verdana o Arial, ma molte persone con dislessia ne apprezzano l'uso. Lo offriamo come scelta opzionale, mai come impostazione predefinita.

OpenDyslexic è rilasciato con **SIL Open Font License 1.1 (OFL)**, una licenza libera che ne consente l'uso anche su siti istituzionali. Il font è copiato sul nostro server (`/fonts/opendyslexic/`), il browser non lo richiede a domini esterni: nessun dato dell'utente lascia il sito.

**Crediti:** OpenDyslexic — Abbie Gonzalez, [opendyslexic.org](https://opendyslexic.org), SIL OFL 1.1.

## Lettura ad alta voce

In molte pagine trovi il pulsante **Leggi ad alta voce**. Il browser legge il contenuto con la voce italiana disponibile sul tuo dispositivo.

La funzione:

- è gratuita;
- non invia il testo a server esterni;
- usa le funzionalità del browser e del sistema operativo;
- permette di scegliere la velocità di lettura (lenta, normale, veloce).

Può essere utile per anziani, persone con dislessia, bambini, persone che leggono lentamente o persone sotto stress durante un'emergenza.

La pagina [Podcast](/podcast/) raccoglie l'elenco di tutti gli articoli ascoltabili, con la **durata stimata** della lettura ad alta voce.

## Versioni alternative degli articoli

Ogni articolo nella sezione [Comunicazioni](/comunicazioni/) può essere letto in modi diversi, a seconda delle esigenze. Sopra il testo dell'articolo trovi un piccolo gruppo di bottoni che danno accesso a queste versioni alternative.

### 1. Audio — Leggi ad alta voce

Già descritto sopra. Il browser legge il contenuto ad alta voce con la voce italiana del dispositivo. Niente account, niente costi, niente dati inviati a server esterni.

### 2. Braille — Scarica versione braille (BRF)

Su ogni articolo è disponibile un bottone **Scarica versione braille**. Apre un file in formato **BRF** (Braille Ready Format), uno standard internazionale ASCII universalmente supportato da:

- **display braille** (Index, ViewPlus, HumanWare BrailleNote, Tiger Cub e altri lettori tattili);
- **stampanti braille** (UICI Roma e Biblioteca Italiana per Ciechi di Monza leggono nativamente questo formato).

Il file è generato automaticamente per ogni articolo pubblicato. La traduzione usa la tabella **braille italiano standard a 6 punti** (uncontracted, lettera per lettera). Il file è scaricabile gratuitamente, senza account.

La generazione è automatica con la libreria open source **liblouis** (raccomandata da W3C-WAI), nessun servizio esterno coinvolto. Specifiche tecniche complete sul nostro [manuale tecnico interno](/manuali/) (Parte 24).

### 3. PDF — Scarica trascrizione

Su ogni articolo è disponibile un bottone **Scarica trascrizione PDF**. Apre la finestra di stampa del tuo browser, dove puoi scegliere **"Salva come PDF"** come destinazione: ottieni il testo dell'articolo formattato A4, senza il chrome del sito (niente menu, navbar, banner, cookie). Utile per:

- conservare l'articolo offline;
- portarlo a una riunione, stamparlo, mandarlo via email;
- consultarlo in emergenza con la rete satura.

Niente generazione PDF lato server, niente librerie pesanti: usiamo la funzione di stampa nativa del browser, che è gratuita e funziona su tutti i sistemi operativi.

### 4. Italiano semplice — Versione facile da leggere (A2 CEFR)

Su alcuni articoli — i più densi o tecnici (allerte, autoprotezione, standard ISO, normativa) — trovi un **banner giallo** in cima con il bottone **"Leggi in italiano semplice [A2]"**. Porta a una versione semplificata dello stesso articolo, scritta in italiano L2 livello **A2** del Quadro Europeo (CEFR):

- frasi corte (8-12 parole);
- parole comuni, niente burocratese;
- sigle spiegate la prima volta (es. "il 112, il numero unico europeo");
- niente subordinate concatenate;
- numeri scritti in cifre.

Pensata per **parlanti italiano L2** (chi non ha l'italiano come prima lingua), **persone con disabilità cognitive lievi**, **anziani con esperienza scolastica limitata** e **chi legge in fretta** durante un'emergenza.

La versione facile è opt-in per articolo: se non vedi il banner giallo, significa che per quell'articolo non c'è ancora una versione semplificata. La redazione la produce on-demand per i contenuti più importanti.

## Versioni in altre lingue

### Otto versioni curate dal Gruppo

Il sito offre **otto versioni curate** delle pagine essenziali (numeri utili, cosa fare in emergenza, piano familiare, accessibilità), tradotte e revisionate dai volontari del Gruppo:

- 🇮🇹 italiano (lingua principale)
- 🇬🇧 english
- 🇫🇷 français
- 🇩🇪 deutsch
- 🇪🇸 español
- 🇵🇹 português
- 🇷🇴 română
- 🌍 esperanto

Ogni pagina dichiara correttamente la lingua nel markup HTML (`<html lang>`) e nei meta Open Graph (`og:locale`), così screen reader, motori di ricerca e crawler la riconoscono.

### Traduzione automatica del browser

Per le altre lingue il sito è compatibile con la **traduzione automatica del browser** (Chrome, Edge, Safari mobile, Firefox con estensione). Quando arrivi sul sito con una lingua di sistema diversa dall'italiano, il browser ti propone in alto una barra: clicca per tradurre la pagina nella tua lingua. La traduzione è gratuita ed elaborata sul tuo dispositivo o dal traduttore del browser (Google Translate per Chrome, Bing per Edge, Apple Translate per Safari).

**Privacy:** la traduzione del browser invia il testo della pagina al servizio di traduzione del fornitore (Google, Microsoft, Apple). Se per te è un problema, leggi prima la nostra [privacy policy](/privacy/) o consulta solo le versioni curate sopra.

**Come tornare all'italiano:** clicca di nuovo sulla barra di traduzione del browser e scegli "Mostra originale", oppure ricarica la pagina con `Ctrl+Shift+R` (Cmd+Shift+R su Mac).

## Supporto in emergenza

Quando ti serve aiuto subito, il sito offre tre strumenti pensati per ridurre attrito:

### Versione leggera `/emergenza/`

La pagina [Cosa fare adesso](/emergenza/) è una versione **ultra-leggera** del sito (44 KB totali) pensata per:

- **rete satura** o lenta (durante un'emergenza l'infrastruttura può essere sovraccarica);
- **dispositivi vecchi** o con poca memoria;
- **consultazione rapida** in stress, senza distrazioni.

Mostra solo i numeri di emergenza, le azioni immediate e i link essenziali. Niente JavaScript pesante, niente immagini decorative, niente widget esterni. Carica in meno di 1 secondo anche su 3G.

### Modal "Chiama il 112"

Su tutte le pagine, in basso a destra, c'è un piccolo bottone rosso **SOS 112**. Cliccandolo si apre una finestra di conferma con tre opzioni: **Annulla** (ENTER, scelta sicura iniziale), **Cosa devo fare?** (guida ragionata se non sai descrivere l'emergenza), **Sì, chiama il 112**. La finestra serve per **prevenire chiamate accidentali** al numero di emergenza e per orientare chi non ha mai chiamato il 112 prima.

Puoi nascondere il bottone dal pannello **Strumenti di accessibilità** se lo trovi invadente. In quel caso il **112** resta sempre componibile dalla tastiera del telefono.

### Assistente virtuale

In basso a sinistra, accanto al pannello accessibilità, trovi un bottone **Assistente virtuale**. Apre una pagina che ti guida con **domande semplici** fino alla risposta giusta sulla tua emergenza: terremoto in casa, incendio, allerta meteo, evacuazione, IT-alert ricevuto, dubbio sui numeri da chiamare, ecc.

L'assistente è un **albero decisionale deterministico in JavaScript**: niente intelligenza artificiale, niente cloud, nessuna risposta inventata. Tutte le indicazioni sono pre-scritte dal Gruppo e validate sulle linee guida del Dipartimento di Protezione Civile.

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

Questi contenuti sono caricati con un sistema **click-to-load**: prima compare un riquadro informativo con titolo, descrizione e fonte. Il widget esterno viene **scaricato e attivato solo se scegli esplicitamente** di cliccare il bottone "Carica la mappa", "Apri il radar", ecc.

### Perché click-to-load è una scelta di accessibility-aware design

È una scelta deliberata, non un'ottimizzazione casuale. Caricare automaticamente widget esterni avrebbe **quattro effetti negativi** sull'accessibilità:

1. **Cookie di terze parti involontari**: ogni widget Windy/INGV/Radar carica risorse JavaScript e cookie del fornitore. Se l'utente non vuole quei cookie, dovrebbe rifiutarli pagina per pagina.
2. **Performance hit involontario**: i widget pesano centinaia di KB, allungano i tempi di caricamento e impattano Largest Contentful Paint. Su rete mobile lenta è notevole.
3. **Focus trap inattesi**: alcuni widget catturano il focus della tastiera in modi non standard. Per chi naviga con Tab/Shift+Tab è disorientante.
4. **Audio/video automatici**: alcuni widget riproducono audio o animazioni senza preavviso. Per chi usa screen reader o ha epilessia fotosensibile è un rischio reale.

Con click-to-load **l'utente sceglie quando attivare il widget**, conosce in anticipo cosa caricherà (titolo, fonte) e può decidere consapevolmente. È coerente con il principio **WCAG 2.2 — 3.2.5 (Change on Request)**: le modifiche significative al contesto avvengono solo su richiesta esplicita.

### Alternative testuali

Per ogni widget esterno il sito offre anche **un link diretto al sito ufficiale del fornitore**, dove il cittadino può consultare il contenuto con le opzioni di accessibilità del fornitore stesso (di solito più complete di quelle del widget embed). Esempi:

- Mappa meteo Windy → link a [windy.com centrato su Genzano](https://www.windy.com/41.692/12.693)
- Mappa terremoti INGV → link a [terremoti.ingv.it](https://terremoti.ingv.it/)
- Radar DPC → link al [portale Dipartimento di Protezione Civile](https://dpc-radar.ingv.it/)

La pagina [Strumenti in tempo reale](/strumenti/) elenca gli strumenti usati e distingue le **fonti istituzionali** (DPC, INGV, ARPA, MeteoAM) dagli **strumenti di consultazione** di terze parti.

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

<!-- cache-bust: 2026-05-12 forza re-upload FTP per allineare header/footer dopo audit -->
