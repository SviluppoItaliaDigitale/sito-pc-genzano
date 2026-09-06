---
title: "Dichiarazione di accessibilità"
description: "Dichiarazione di accessibilità AGID: stato di conformità, contenuti non accessibili, modalità di valutazione, obiettivi annuali, feedback e contatti."
layout: "single"
toc: true
tts: true
dataUltimaRevisione: "2026-09-06"
aliases:
  - /dichiarazione-accessibilita.html
---

Questa pagina contiene la dichiarazione di accessibilità del sito della Protezione Civile di Genzano di Roma, redatta secondo il modello AGID e conforme alla **Direttiva (UE) 2016/2102**, alla **Legge 9 gennaio 2004 n. 4** ("Stanca") e al **D.Lgs. 10 agosto 2018 n. 106**.

La dichiarazione si applica al sito **www.protezionecivilegenzano.it**.

## Stato di conformità

Il sito è **parzialmente conforme** ai requisiti dello standard europeo armonizzato **EN 301 549 v3.2.1** (basato sulle **WCAG 2.1 livello AA**), con **tendenza esplicita alla piena conformità**. Il sito adotta inoltre come obiettivo ulteriore le **WCAG 2.2 livello AA**, che estendono le 2.1 con nuovi criteri: le 2.2 non sostituiscono la base normativa europea finché non saranno recepite in una versione armonizzata dello standard, ma sono già il riferimento dei nostri controlli interni.

**Cosa risulta conforme nelle verifiche effettuate.** Ogni voce indica come e quando è stata verificata: i risultati valgono per le pagine e le date indicate, non come garanzia assoluta e permanente sull'intero sito.

- **Lighthouse Accessibilità: 100/100** — mediana su 9 run × 3 URL campione (home, archivio comunicazioni, numeri utili), verifica del 10 maggio 2026; il punteggio è ricontrollato dall'audit automatico 2 volte al giorno (`lighthouse-audit.yml`).
- **Best Practices: 100/100** e **SEO: 100/100** — stesse condizioni di test.
- **Performance: 95/100** — mediana (LCP 2,3 s, TBT 70-130 ms, CLS 0,024-0,058), stesse condizioni di test.
- **Gate axe-core su ogni modifica** — dal luglio 2026 ogni proposta di modifica al sito passa un controllo automatico axe-core (WCAG 2.2 AA) su 11 pagine campione prima della pubblicazione: al 15 luglio 2026 il gate risulta superato con **0 violazioni confermate**; restano segnalati controlli "da revisione manuale" (non violazioni accertate) che vengono esaminati progressivamente.
- **Contrasto colore WCAG AA**: nei test (automatici axe-core + calcoli manuali sui componenti del tema) non risultano testi sotto la soglia 4,5:1 sulle pagine campione; le regressioni note emerse in passato sono state corrette e sono documentate nel repository pubblico.
- **Navigazione da tastiera**: percorsi Tab/Shift+Tab/Enter/Esc verificati manualmente sulle pagine campione (elenco più sotto), senza trappole da tastiera riscontrate. Sulle mini-app interattive (giochi, quiz, schede stampabili) la navigazione completa richiede JavaScript attivo.
- **Focus visibile**: ogni elemento interattivo ha outline visibile (3px) al focus.
- **Skip link**: "Vai al contenuto principale" presente in cima alle pagine generate dal sito; sulle mini-app interattive è fornito via JavaScript insieme al resto dell'intestazione.
- **Landmark ARIA**: header/nav/main/footer presenti nativamente sulle pagine generate dal sito; sulle mini-app interattive (giochi, quiz, schede stampabili) sono iniettati via JavaScript e richiedono quindi JavaScript attivo.
- **Alt text**: le immagini informative hanno descrizione testuale e le decorative `alt=""`; la copertura è controllata da una verifica automatica settimanale sull'intero repository (`audit-sito.yml`, check `image_alt`) e a campione in revisione editoriale.
- **Lingua dichiarata**: ogni pagina dichiara `<html lang>` correttamente, anche per le 7 traduzioni.
- **`<th scope="col">` automatico**: tutte le 400+ tabelle Markdown del sito sono rese con intestazioni accessibili.
- **Pittogrammi standardizzati**: 46 segnali ISO 7010 + 125 ARASAAC integrati per supportare comprensione cognitiva (bambini, anziani, italiano L2, persone con disabilità cognitive).
- **TTS "Leggi ad alta voce"** nativo (Web Speech API) attivo sulle pagine editoriali del sito (escluse le pagine legali e puramente funzionali).
- **Toolbar di accessibilità** utente con 11 preferenze persistenti (dimensione testo, contrasto invertito, scala di grigi, font ad alta leggibilità, spaziatura, animazioni, evidenza link, cursore grande, ecc.). È uno **strumento di supporto opzionale** che si aggiunge all'accessibilità nativa delle pagine: non è, e non va inteso come, una prova di conformità del sito.
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

### Documenti PDF pubblicati sul sito
- **Stato al 6 settembre 2026** (verifica esterna sui 50 PDF presenti nel repository del sito): 41 documenti non hanno una struttura di tag (PDF/UA, ISO 14289-1); di questi, 17 non contengono testo estraibile perché esportati come immagine: gli 8 poster di emergenza multilingue e le 9 presentazioni tematiche. Lo screen reader può quindi leggere in modo lineare, o non leggere affatto, questi file.
- **Motivazione**: parte dei documenti sono scansioni o file ricevuti da enti terzi (Comune, Regione, Prefettura), non rigenerabili dal Gruppo; i poster e le presentazioni sono stati esportati da strumenti che rasterizzano il testo.
- **Mitigazione**: per ogni documento esiste l'equivalente HTML accessibile sul sito. Il Manuale di Protezione Civile ha il reader online in [/manuale/](/manuale/); le presentazioni tematiche corrispondono alle pagine dei rischi e delle allerte; i poster multilingue corrispondono alle pagine tradotte (inglese, francese, tedesco, spagnolo, portoghese, rumeno, esperanto). Se un PDF non è leggibile con la tua tecnologia assistiva, scrivi a [segreteria@protezionecivilegenzano.it](mailto:segreteria@protezionecivilegenzano.it): forniamo una versione alternativa o un testo equivalente.
- **Piano**: rigenerazione con struttura di tag, in ordine di priorità, per il Manuale, i materiali per le scuole, i documenti di emergenza e la modulistica; la presenza dei tag sarà verificata documento per documento e non presentata come conformità PDF/UA finché non sia stata controllata con lettore di schermo.
- **Stato per documento**: consulta la pagina [Audit accessibilità dei PDF pubblicati](/accessibilita/audit-pdf/) per il quadro documento per documento.

### Mappe interattive
- Le mappe Leaflet/MapLibre eventualmente integrate hanno limiti di interazione da sola tastiera per il pan/zoom (limite intrinseco delle librerie SVG-based).
- **Mitigazione**: ogni mappa è sempre affiancata da una versione testuale equivalente (lista dei punti raduno, indirizzi, coordinate).

## Redazione della dichiarazione

- **Dichiarazione redatta il**: 10 maggio 2026.
- **Metodo di redazione**: **autovalutazione** condotta dal soggetto ai sensi dell'art. 3, comma 1, della Decisione di esecuzione (UE) 2018/1523.
- **Data ultima revisione**: 15 luglio 2026 (revisione del linguaggio: le affermazioni di conformità sono ora accompagnate da data, metodo e ambito della verifica).
- **Dichiarazione sul portale AGID**: la pubblicazione della dichiarazione tramite la procedura ufficiale ([form.agid.gov.it](https://form.agid.gov.it/)) è a carico del referente del Gruppo; il collegamento sarà aggiunto qui e nel piè di pagina appena disponibile.
- **Riesame annuale**: secondo il calendario AgID, la dichiarazione va riesaminata e, se necessario, aggiornata **entro il 23 settembre di ogni anno**. Prossimo riesame: entro il 23 settembre 2026, poi entro il 23 settembre 2027.
- **Frequenza dei test automatici**: settimanale (workflow `audit-sito.yml` ogni lunedì) + post-deploy (workflow `lighthouse-audit.yml` dopo ogni pubblicazione).

## Informazioni sul sito

- **URL**: <https://www.protezionecivilegenzano.it/>
- **Editore**: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
- **Tecnologie utilizzate**: Hugo 0.154 (generatore statico, versione fissata nella pipeline di pubblicazione), Bootstrap Italia 2.x (design system AGID/Designers Italia), HTML5, CSS3, JavaScript ES6 (Web Speech API per TTS, IntersectionObserver per lazy-load).
- **Hosting**: Aruba S.p.A. (HTTPS forzato, HSTS attivo, header di sicurezza X-Content-Type-Options/X-Frame-Options/Referrer-Policy/Permissions-Policy/HSTS).
- **Compatibilità browser**: Chrome ≥ 88, Firefox ≥ 78, Safari ≥ 14, Edge ≥ 88, browser mobili moderni. Su browser legacy il sito resta utilizzabile con degradazione progressiva.
- **Compatibilità tecnologie assistive**: verifiche a campione con **NVDA** (Windows), **VoiceOver** (macOS/iOS) e **TalkBack** (Android) sulle pagine campione elencate più sotto (sessioni di autovalutazione di maggio 2026). Non si tratta di una certificazione: segnalazioni di problemi con tecnologie assistive sono benvenute tramite il meccanismo di feedback in fondo a questa pagina.

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

## Criteri AAA soddisfatti oltre l'obbligo

Il livello di conformità richiesto per i siti della Pubblica Amministrazione è **WCAG 2.2 AA**, ed è quello che il sito persegue. Il livello **AAA** non è un obbligo di legge e — come precisa lo stesso W3C — non è raccomandato come requisito per un intero sito, perché alcuni criteri AAA non sono soddisfacibili per certi tipi di contenuto. Tuttavia il sito **soddisfa già diversi criteri di livello AAA**, che dichiariamo qui per trasparenza. Non costituiscono una dichiarazione di conformità AAA complessiva.

**Criteri AAA verificati come soddisfatti:**

- **2.4.8 Posizione** — ogni pagina mostra un percorso di navigazione (breadcrumb) che indica dove ci si trova nel sito.
- **2.4.10 Intestazioni di sezione** — i contenuti sono organizzati con intestazioni di sezione ordinate (H2/H3).
- **3.1.3 Parole inusuali** — il glossario inline con finestra di approfondimento spiega i termini tecnici alla prima occorrenza.
- **3.1.4 Abbreviazioni** — lo stesso glossario scioglie le sigle (DPC, COC, IT-alert, NUE, ecc.).
- **2.3.2 Tre lampi** — nessun contenuto del sito lampeggia.
- **2.5.6 Meccanismi di input simultanei** — il sito si usa indifferentemente con mouse, tastiera o touch, senza vincolare a un solo metodo.

**Criteri AAA soddisfatti in parte (oltre l'AA, ma non sull'intero sito):**

- **1.4.6 Contrasto migliorato (7:1)** — il **testo principale di lettura** è già ben oltre i 7:1: corpo del testo 17,4:1, blu istituzionale di titoli e link 12,6:1, testo informativo 7,56:1. Restano sotto la soglia 7:1 — pur rispettando l'AA 4,5:1 — solo elementi accessori: alcuni badge di categoria, le barre di allerta colorate e il testo secondario.
- **1.4.8 Presentazione visiva** — la *Modalità lettura* e i cinque contrasti selezionabili del pannello di accessibilità coprono la maggior parte dei requisiti (sfondo/testo scelti dall'utente, riga di ~65 caratteri, interlinea aumentata, allineamento a sinistra).
- **3.1.5 Livello di lettura** — i contenuti più critici (allerte, autoprotezione, procedure) hanno una **versione in italiano semplice (A2 CEFR)** affiancata; non ancora su tutti gli articoli.

**Criteri AAA che il sito sceglie consapevolmente di non perseguire** (per non confliggere con l'identità istituzionale o per limiti oggettivi):

- **1.4.6 Contrasto 7:1 su tutti gli elementi** — la palette istituzionale dei badge e delle allerte è calibrata sull'AA (4,5:1); portarla a 7:1 ne snaturerebbe i colori riconoscibili.
- **1.4.9 Immagini di testo (nessuna eccezione)** — le copertine degli articoli riportano il titolo come immagine tipografica, scelta di identità visiva. Il titolo è comunque sempre presente anche come testo reale nella pagina.
- **2.5.5 Dimensione target (44px)** — alcuni controlli secondari (filtri dell'archivio, bottoni compatti) sono sotto i 44px; è invece soddisfatto il criterio AA 2.5.8 (24px minimo).
- **1.2.6 Lingua dei segni (LIS) per tutti i contenuti** — il sito offre un hub dedicato di video in LIS, ma non un'interpretazione LIS per ogni contenuto audio/video.

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

La pagina [Articoli da ascoltare](/articoli-da-ascoltare/) raccoglie l'elenco di tutti gli articoli ascoltabili, con la **durata stimata** della lettura ad alta voce.

## Versioni alternative degli articoli

Ogni articolo nella sezione [Comunicazioni](/comunicazioni/) può essere letto in modi diversi, a seconda delle esigenze. Sopra il testo dell'articolo trovi un piccolo gruppo di bottoni che danno accesso a queste versioni alternative.

### 1. Audio — Leggi ad alta voce

Già descritto sopra. Il browser legge il contenuto ad alta voce con la voce italiana del dispositivo. Niente account, niente costi, niente dati inviati a server esterni.

### 2. Braille — Scarica versione braille (BRF)

Su ogni articolo è disponibile un bottone **Scarica versione braille**. Apre un file in formato **BRF** (Braille Ready Format), uno standard internazionale ASCII universalmente supportato da:

- **display braille** (Index, ViewPlus, HumanWare BrailleNote, Tiger Cub e altri lettori tattili);
- **stampanti braille** (UICI Roma e Biblioteca Italiana per Ciechi di Monza leggono nativamente questo formato).

Il file è generato automaticamente per ogni articolo pubblicato. La traduzione usa la tabella **braille italiano standard a 6 punti** (uncontracted, lettera per lettera). Il file è scaricabile gratuitamente, senza account.

La generazione è automatica con la libreria open source **liblouis** (raccomandata da W3C-WAI), nessun servizio esterno coinvolto.

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

- Mappa meteo Windy → link a [windy.com centrato su Genzano di Roma](https://www.windy.com/41.692/12.693)
- Mappa terremoti INGV → link a [terremoti.ingv.it](https://terremoti.ingv.it/)
- Radar DPC → link al [portale Dipartimento di Protezione Civile](https://radar.protezionecivile.it/)

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

<!-- cache-bust: 2026-05-29 forza re-upload FTP dopo aggiunta voce di menu globale "Conoscere la Protezione Civile" -->

<!-- cache-bust: 2026-06-10 forza re-upload FTP per loghi footer WebP + cookie banner early-paint -->
