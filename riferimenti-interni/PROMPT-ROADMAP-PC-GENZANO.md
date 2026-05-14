# Prompt di avvio Claude Code — Roadmap PC Genzano

Libreria dei 25 prompt rimanenti per la roadmap di evoluzione del sito.
L'idea #6 (QR articoli) è già in lavorazione e non è inclusa qui.

---

## Come si usano

1. Apri il terminale, vai nella root del repo: `cd ~/sito-pc-genzano`
2. Lancia Claude Code: `claude`
3. Copia integralmente il prompt dell'iniziativa che vuoi attaccare
4. Incolla nella sessione, premi Invio
5. Claude Code legge `CLAUDE.md` + `.claude/rules/0*.md` in automatico e decide
   il piano. Confermi/correggi quando ti chiede. Alla fine pubblica.

I prompt sono **deliberatamente alto-livello**: dichiarano *cosa* costruire
e *perché*, lasciando a Claude Code architettura, stack e dettagli implementativi.
I vincoli generali del progetto (Hugo, Bootstrap Italia, AGID, WCAG, divieto PWA,
anti-pattern image, banner-titolo intoccabile, niente articoli draft, no API a
pagamento, dangerous-clean-slate del deploy.yml) sono nel `CLAUDE.md` e
Claude Code li applica da sé — non serve ripeterli.

---

## Indice per livello di difficoltà

### Livello 1 — velocissime (1-3 ore)
- [#19 Calendario eventi `.ics` sottoscrivibile](#19--calendario-eventi-ics-sottoscrivibile)
- [#24 Pagefind search interna full-text](#24--pagefind-search-interna-full-text)

### Livello 2 — facili (mezza giornata - 1 giornata)
- [#21 Glossario interattivo PC](#21--glossario-interattivo-pc)
- [#27 Toolbar accessibilità v2](#27--toolbar-accessibilità-v2)
- [#25 Pagina "Stato del sistema"](#25--pagina-stato-del-sistema)
- [#22 Podcast pubblico con RSS](#22--podcast-pubblico-con-rss)
- [#9 Versione FALC linguaggio facile](#9--versione-falc-linguaggio-facile)

### Livello 3 — medie (1-3 giorni)
- [#18 Dashboard trasparenza ETS RUNTS](#18--dashboard-trasparenza-ets-runts)
- [#20 Wiki tecnica volontari](#20--wiki-tecnica-volontari)
- [#8 Timeline storica Castelli Romani](#8--timeline-storica-castelli-romani)
- [#5 Assistente vocale di emergenza](#5--assistente-vocale-di-emergenza)
- [#4 Modalità "Lanterna" sopravvivenza](#4--modalità-lanterna-sopravvivenza)
- [#23 Newsletter Buttondown](#23--newsletter-buttondown)
- [#11 Hub "Arena PC Genzano"](#11--hub-arena-pc-genzano)

### Livello 4 — impegnative (3-7 giorni)
- [#3 Mappa interattiva del territorio](#3--mappa-interattiva-del-territorio)
- [#7 Quiz "Quanto sei preparato?"](#7--quiz-quanto-sei-preparato)
- [#26 Mappa rischi DPC zone Lazio](#26--mappa-rischi-dpc-zone-lazio)
- [#10 Sistematizzazione contenuti in LIS](#10--sistematizzazione-contenuti-in-lis)
- [#2 Notifiche allerta browser (no Service Worker)](#2--notifiche-allerta-browser-no-service-worker)

### Livello 5 — grandi progetti gaming (1-3 settimane cadauno)
- [#15 "Codice Colore Rapido"](#15--codice-colore-rapido)
- [#16 "Memory Calamità" 3D](#16--memory-calamità-3d)
- [#14 "Kit dello Zaino" 2.0 con fisica](#14--kit-dello-zaino-20-con-fisica)
- [#17 "Cronaca dell'Emergenza" adventure](#17--cronaca-dellemergenza-adventure)
- [#12 "Centrale Operativa 112" tycoon](#12--centrale-operativa-112-tycoon)
- [#13 "Evacua Genzano" RTS](#13--evacua-genzano-rts)

---

# LIVELLO 1 — Velocissime

## #19 — Calendario eventi `.ics` sottoscrivibile

```
Devi implementare l'idea #19 della roadmap PC Genzano.

COSA È:
Calendario eventi pubblico del sito con export in formato iCalendar (.ics)
sottoscrivibile. Pubblica esercitazioni, sessioni formative, riunioni pubbliche,
ricorrenze "Io non rischio", attività ETS RUNTS e ogni altra attività che il
Gruppo organizza in calendario fisso.

OBIETTIVO:
Permettere a cittadini e volontari di sottoscrivere il calendario una sola
volta dal proprio Google/Apple/Outlook Calendar e ricevere automaticamente
ogni nuovo evento a ogni aggiornamento del sito. Niente API esterne, tutto
generato a build-time da Hugo. Trasparenza ETS senza calendari mantenuti
a mano.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md di questo
repo. Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, frontmatter, UX della pagina indice e integrazione
con menu/mappa-sito/assistente. Quando hai un piano chiaro, eseguilo.
```

---

## #24 — Pagefind search interna full-text

```
Devi implementare l'idea #24 della roadmap PC Genzano.

COSA È:
Motore di ricerca interno full-text del sito, indicizzato a build-time da
Pagefind (https://pagefind.app), con interfaccia moderna a modal alla
Algolia DocSearch, che copra le 7 traduzioni (it/en/fr/de/es/pt/ro/eo)
e mostri snippet evidenziati, filtri per sezione e scorciatoia da tastiera
(Ctrl+K / ⌘+K).

OBIETTIVO:
Sostituire la search attuale con uno strumento che trovi davvero quello che
l'utente cerca anche dentro il corpo degli articoli, non solo nei titoli.
Cruciale per chi entra cercando "scossa" o "evacuazione" durante un evento
e non sa orientarsi nel menu. Zero costi ricorrenti: Pagefind è open source
e gira interamente client-side, indice statico generato a build-time.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md di questo
repo. NON modificare deploy.yml (vincolo permanente): se serve uno step
Pagefind nel CI, usa un workflow separato o uno script invocato manualmente
prima del commit. Modal accessibile WCAG 2.2 AA (focus trap, aria-live per
risultati, navigabile da sola tastiera).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, integrazione col theme, UX della modal e dei filtri.
Quando hai un piano chiaro, eseguilo.
```

---

# LIVELLO 2 — Facili

## #21 — Glossario interattivo PC

```
Devi implementare l'idea #21 della roadmap PC Genzano.

COSA È:
Glossario terminologico della Protezione Civile italiana: COC, ROS, SOI, COI,
NRBC, AIB, codice colore DPC, livelli idranti UNI, sigle frequenze radio,
acronimi normativi, eccetera. Ogni voce ha definizione in linguaggio chiaro
AGID, eventualmente esempi, fonte istituzionale e link a contenuti correlati
del sito. Dev'essere navigabile come pagina dedicata (con filtri alfabetici
e ricerca) E inline negli articoli: quando un termine del glossario compare
in un articolo, deve mostrare un tooltip accessibile al passaggio del cursore
o al focus da tastiera.

OBIETTIVO:
Abbattere la barriera del gergo tecnico per il cittadino comune. Permettere
al volontario in formazione di avere un riferimento ufficiale unico. Dare ai
giornalisti locali una fonte rapida quando ci citano. Migliorare l'accessibilità
cognitiva del sito senza appesantire il testo degli articoli.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md di questo
repo. Le definizioni testuali passano dal gate AGID (qualità 9.5/10).
I tooltip devono funzionare anche con sola tastiera (focus + Esc per chiudere)
e con screen reader. Niente librerie pesanti per tooltip: la soluzione deve
essere leggera e degradare bene se JS è disabilitato.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu data structure (YAML/JSON in data/, page bundle, o altro), render
hook Markdown per il match inline, e UX della pagina indice. Quando hai un
piano chiaro, eseguilo.
```

---

## #27 — Toolbar accessibilità v2

```
Devi implementare l'idea #27 della roadmap PC Genzano.

COSA È:
Evoluzione del partial accessibility-toolbar.html già esistente: aggiunta di
font OpenDyslexic (open source) come alternativa, controlli per
spaziatura caratteri / interlinea / dimensione testo persistenti, override
prefers-reduced-motion (blocco animazioni globale forzato), modalità "lettura
focalizzata" che riduce la pagina a barra-essenziale + colonna lettura
centrale per chi soffre di affollamento visivo o ADHD.

OBIETTIVO:
Spingere l'accessibilità del sito oltre il minimo richiesto da WCAG 2.2 AA,
verso il livello che lo standard EN 301 549 e la prassi PA migliore considerano
"inclusivo per disabilità cognitive". Recuperare utenti dislessici, con ADHD,
con ridotta visione, anziani, italiano L2. Tutte le preferenze in localStorage,
niente account, niente tracking.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md, in
particolare 03-accessibility.md. Mantieni compatibilità con la toolbar v1
esistente: chi aveva già impostato qualcosa non deve perdere le sue scelte.
OpenDyslexic va auto-ospitato (no Google Fonts), font-display: swap, peso
totale del set ragionato. Niente librerie esterne pesanti.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu UX, CSS variables, eventuali nuovi controlli e icone. Quando hai
un piano chiaro, eseguilo.
```

---

## #25 — Pagina "Stato del sistema"

```
Devi implementare l'idea #25 della roadmap PC Genzano.

COSA È:
Pagina pubblica "/stato-sistema/" stile statuspage. Mostra in tempo quasi
reale (build-time + dati JSON aggiornati dai workflow esistenti): stato
allerta meteo corrente, ultimo check DPC (timestamp), ultimo deploy del sito,
ultimo audit Lighthouse con punteggio, ultime esercitazioni svolte, prossime
esercitazioni calendarizzate, conformità AGID, stato workflow critici
(check-allerta, audit-sito, smoke-test) con semaforo verde/giallo/rosso.

OBIETTIVO:
Dare un cruscotto pubblico unico di trasparenza tecnica e operativa, sia
verso cittadini (che vedono che il sistema funziona) sia verso istituzioni
e media (che hanno un riferimento credibile). Demistificare il backend del
sito mostrando con orgoglio gli automatismi messi in piedi.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md. I dati
vanno letti dai data files JSON/YAML esistenti (data/allerta.json, eventuali
artifacts dei workflow). NON aggiungere nuove API esterne. NON modificare
deploy.yml: se servono nuovi dati, generali da un workflow separato che
committa un nuovo file in data/. Tono istituzionale ma comprensibile.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, partial, badge SVG generati o icon set Bootstrap
Italia, layout dei pannelli. Quando hai un piano chiaro, eseguilo.
```

---

## #22 — Podcast pubblico con RSS

```
Devi implementare l'idea #22 della roadmap PC Genzano.

COSA È:
Sezione podcast "Voci dalla PC Genzano": episodi audio di 10-20 minuti su
divulgazione rischi locali, racconti esercitazioni, ospiti tecnici, interviste
volontari. Hugo deve generare la pagina indice degli episodi e un feed RSS
iTunes-compatible (con tag itunes:* corretti) auto-distribuibile su Spotify,
Apple Podcasts, Google Podcasts, Pocket Casts. I file MP3 stanno su
GitHub Releases del repo (2 GB gratis per release).

OBIETTIVO:
Aprire un canale di comunicazione alternativo per chi preferisce ascoltare a
leggere: pendolari, ipovedenti, anziani che usano smart speaker, giovani con
abitudini podcast. Zero costi ricorrenti: niente piattaforme paid, niente
hosting dedicato. Il feed sostituisce qualsiasi servizio di terze parti.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md. Episodi
con trascrizione completa accessibile in pagina (per accessibilità + SEO).
Frontmatter degli episodi con campi minimi per RSS podcast (titolo, durata,
descrizione lunga, descrizione breve, data, link MP3, eventuale immagine
copertina con fascia blu). Niente articoli draft.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu output format Hugo per RSS podcast, architettura della sezione,
shortcode player audio. Predisponi tutto pronto per il primo episodio (che
non includere: lo registreremo in seguito). Quando hai un piano chiaro,
eseguilo.
```

---

## #9 — Versione FALC linguaggio facile

```
Devi implementare l'idea #9 della roadmap PC Genzano.

COSA È:
Sistema di "versione facile da leggere e capire" (FALC, standard europeo
IFLA / Inclusion Europe) per le pagine chiave: ogni contenuto rilevante può
avere una versione semplificata con frasi corte, lessico base, supporto
pittografico, una nozione per frase, font ad alta leggibilità. Si attiva
da toggle nel partial o da accessibility-toolbar. Le pagine candidate sono
i 12 Kit Calamità, la /emergenza/, la /assistente/ e le pagine "Cosa fare se".

OBIETTIVO:
Includere fra i destinatari del sito le persone con disabilità cognitive
lievi/moderate, italiano L2 (immigrati, turisti), anziani con declino
cognitivo, ragazzi delle scuole medie. Le linee guida ufficiali italiane
FALC sono dell'Anffas e UE — vanno seguite alla lettera. Anche cinque
pagine convertite cambiano l'esperienza di centinaia di utenti reali.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
I testi FALC passano dal gate AGID + criteri FALC specifici (frasi ≤15 parole,
lessico Vocabolario di Base di De Mauro, una nozione per frase, niente
metafore, niente sigle non sciolte). Pittogrammi ARASAAC o ISO 7010
(libreria già scaricata da scripts/scarica-pittogrammi.sh).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu meccanismo di switch (frontmatter facile_da_leggere: true? pagina
gemella .it.md / .it-facile.md? render hook?), UX e layout. Inizia
predisponendo l'infrastruttura tecnica e UN solo esempio funzionante
(es. /emergenza/ in versione FALC), il resto delle pagine le convertiremo
gradualmente. Quando hai un piano chiaro, eseguilo.
```

---

# LIVELLO 3 — Medie

## #18 — Dashboard trasparenza ETS RUNTS

```
Devi implementare l'idea #18 della roadmap PC Genzano.

COSA È:
Dashboard pubblica con i numeri del Gruppo Comunale: ore di servizio annuali
e cumulative, interventi suddivisi per tipologia (AIB, idraulico, ricerca,
assistenza), ore formazione erogata e ricevuta, esercitazioni svolte,
volontari attivi (numero aggregato, non nominativi), fondi ricevuti/spesi
in forma aggregata. Grafici interattivi con Chart.js. Dati storici dei
3-5 anni precedenti per mostrare crescita / serie temporale.

OBIETTIVO:
Trasparenza obbligatoria per gli ETS RUNTS trasformata in vetrina di fiducia
civica. Mostrare con dati concreti il lavoro del volontariato del Gruppo,
attirare nuovi volontari, dare alle istituzioni comunali e regionali una
fonte ufficiale facilmente consultabile, motivare i donatori (5x1000).

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md. Tutti i
dati nominativi sono off-limits (GDPR + privacy volontari): solo numeri
aggregati. Chart.js è una dipendenza già accettabile (libreria diffusa,
gratis, build-time inclusion). Grafici accessibili: tabella dati equivalente
fornita sotto ogni grafico per screen reader (WCAG 2.2 1.4.5 + 1.1.1).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu data structure (YAML annuale in data/bilancio-sociale.yaml?),
componenti grafici, layout. Iniziamo con dati di esempio realistici (mock-up),
poi li popoleremo coi numeri reali in commit successivi. Quando hai un piano
chiaro, eseguilo.
```

---

## #20 — Wiki tecnica volontari

```
Devi implementare l'idea #20 della roadmap PC Genzano.

COSA È:
Sezione pubblica /formazione/manuali-tecnici/ destinata a volontari del
Gruppo (e di altri Gruppi PC che ci leggono): SOP (Standard Operating
Procedures) operative, schede tecniche attrezzature (mezzi, gruppi
elettrogeni, motopompe, radio), procedure CRI/DPC adattate al territorio,
frequenze radio pubbliche autorizzate, glossario radio (Q-codes,
abbreviazioni), checklist mezzo pre-uscita, schede primo soccorso secondo
linee guida IRC. Ogni scheda ha versione PDF stampabile.

OBIETTIVO:
Avere un riferimento unico e aggiornato delle procedure operative del Gruppo,
disponibile anche da mobile in intervento. Condividere esperienza con altri
Gruppi PC del territorio (effetto rete). Rendere replicabili le esercitazioni.
Tutto pubblico: la trasparenza operativa è valore, non rischio.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
Contenuti tecnici scritti in registro professionale (non "linguaggio per il
cittadino": qui i destinatari sono volontari). Gate AGID applicato in
modalità "documentazione tecnica" (vedi punto 4 del CLAUDE.md, eccezione
non-AGID). Niente informazioni sensibili (numeri privati volontari, mappe
operative riservate, dati personali). Frequenze radio: solo quelle pubblicate
e autorizzate.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura sezione, template scheda, generatore PDF, indice
navigabile. Predisponi infrastruttura + 2-3 schede esempio (es. checklist
mezzo, SOP attivazione COC, scheda radio portatile). Le altre le scriveremo
insieme in commit successivi. Quando hai un piano chiaro, eseguilo.
```

---

## #8 — Timeline storica Castelli Romani

```
Devi implementare l'idea #8 della roadmap PC Genzano.

COSA È:
Pagina /storia/eventi-castelli-romani/ con timeline interattiva degli eventi
storici di Protezione Civile della zona: alluvione storica del Tevere,
sciami sismici dei Colli Albani, frane storiche di Rocca di Papa e Ariccia,
fenomeno gas Lago Albano, incendi AIB rilevanti, alluvioni di Genzano,
evento Vesuvio del 1944 visto dai Castelli. Ogni evento ha data, luogo,
descrizione, fonte primaria (INGV, CNR-IRPI, archivio storico comunale,
ISPRA), foto d'epoca dove possibile, lezioni apprese. Animazione di scroll
verticale moderna con CSS Scroll-Driven Animations.

OBIETTIVO:
Costruire memoria collettiva del territorio. Mostrare ai cittadini che gli
eventi non sono "una volta ogni mai", aiutare la prevenzione attraverso la
conoscenza storica. Dare a scuole, giornalisti, ricercatori una fonte
divulgativa ma rigorosa. Posizionare il sito come autorità divulgativa
locale, non solo comunicazione operativa.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
Tutte le fonti devono essere citate con link permanenti (Normattiva, archivio
INGV, repository CNR, archivio comunale). Foto d'epoca: solo da fonti
liberamente riusabili (Wikimedia Commons, archivio comunale rilasciato in
licenza libera, archivio INGV). Niente Getty / agenzie a pagamento.
Animazioni rispettano prefers-reduced-motion. Gate AGID applicato sui testi.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu data structure (JSON in data/eventi-storici.yaml?), template
timeline, illustrazioni vettoriali aggiuntive, navigazione anchor. Inizia
con infrastruttura + 4-5 eventi documentati (ricerca fonti inclusa). Quando
hai un piano chiaro, eseguilo.
```

---

## #5 — Assistente vocale di emergenza

```
Devi implementare l'idea #5 della roadmap PC Genzano.

COSA È:
Evoluzione dell'assistente guidato esistente in /assistente/: aggiunta di un
modulo di riconoscimento vocale via Web Speech API SpeechRecognition (gratuita,
built-in nei browser, niente backend) che permette al cittadino di porre
domande a voce ("Cosa devo fare se vedo un incendio?", "Come mi preparo per
un terremoto?") e ricevere risposte vocali tramite il TTS già esistente
(leggi-ad-alta-voce). Il matching domanda → risposta è basato su intent
keyword precompilati (non IA esterna).

OBIETTIVO:
Servire utenti che non possono leggere (anziani con vista compromessa,
ipovedenti, dislessici gravi, italiano L2 con bassa alfabetizzazione,
mani occupate in emergenza). Modalità hands-free in scenari critici.
Tutto offline-friendly (Web Speech API funziona client-side anche se l'API
di rete fa il riconoscimento server-side, dipende dal browser).

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
NESSUNA chiamata ad API a pagamento, NESSUN backend, NESSUN tracking della
voce. Esplicito disclaimer di privacy (alcuni browser inviano l'audio ai
loro server Google/Apple/Microsoft per il riconoscimento — l'utente deve
saperlo). Fallback testuale completo: tutto ciò che si può chiedere a voce
deve essere fattibile anche da tastiera. Skip se browser non supporta Web
Speech (Firefox storicamente limitato — graceful degradation).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, mappa intent → risposte, integrazione con assistente.
Quando hai un piano chiaro, eseguilo.
```

---

## #4 — Modalità "Lanterna" sopravvivenza

```
Devi implementare l'idea #4 della roadmap PC Genzano.

COSA È:
Evoluzione della pagina lite /emergenza/ esistente verso una vera "modalità
sopravvivenza" da usare con poca batteria, scarsa connessione, di notte,
sotto stress: torcia accendibile via getUserMedia + ImageCapture flash
controls (dove supportato, principalmente Chrome Android), bussola
DeviceOrientation con freccia nord, Wake Lock API per impedire spegnimento
schermo, alto contrasto fisso, font 24pt minimo, numero 112 sempre in alto
in viewport sticky, link rapidi ai 5 contenuti più critici. Tutto in <60 KB
totali, niente JS bloccante.

OBIETTIVO:
Rendere il sito uno strumento attivo di sopravvivenza, non solo di
informazione. In una situazione critica (terremoto notturno, alluvione,
blackout) il cittadino ha già il sito aperto sul telefono e accede a
funzioni essenziali con un solo tap.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md. La
torcia funziona SOLO su Android Chrome (limite browser noto): graceful
degradation chiara, no errori a video. Wake Lock API in opt-in con messaggio
informativo (consuma batteria). Bussola può richiedere permesso esplicito
(iOS 13+). Test su rete 2G simulata (Chrome DevTools): deve essere
utilizzabile entro 3 secondi.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu UI, layout, fallback, integrazione con la /emergenza/ esistente
(modulo aggiuntivo o pagina parallela?). Quando hai un piano chiaro,
eseguilo.
```

---

## #23 — Newsletter Buttondown

```
Devi implementare l'idea #23 della roadmap PC Genzano.

COSA È:
Sistema newsletter pubblica con archivio sul sito. Form di iscrizione embed
di Buttondown free tier (1000 iscritti gratis, poi 9$/mese — soglia da
monitorare). Archivio delle uscite settimanali/mensili come pagina statica
del sito generata da Hugo. Tema: riepilogo articoli della settimana,
avvisi importanti, prossimi eventi, una "rubrica" su un rischio specifico
ogni numero.

OBIETTIVO:
Canale di comunicazione diretto e proprietario (no algoritmi social) verso
cittadini che vogliono restare informati senza dover venire attivamente sul
sito. Soprattutto utile per fasce 50+ che leggono le email più
frequentemente dei social.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
Trasparenza GDPR completa: cosa salviamo, dove, quanto, come ci si cancella.
Aggiornare le pagine /privacy/ e /note-legali/ di conseguenza
(dataUltimaRevisione obbligatorio — vedi punto 11 del CLAUDE.md).
Form di iscrizione accessibile WCAG 2.2 AA + double opt-in obbligatorio.
Aggiungere monitoraggio interno: quando ci avviciniamo al limite 1000 iscritti,
issue automatica per decidere se passare a piano paid o migrare a Listmonk
self-hosted.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu integrazione (form embed vs API Buttondown), template archivio,
frequenza (settimanale? mensile?). Quando hai un piano chiaro, eseguilo.
```

---

## #11 — Hub "Arena PC Genzano"

```
Devi implementare l'idea #11 della roadmap PC Genzano.

COSA È:
Pagina hub /giochi/ ridisegnata come launcher in stile videogioco moderno
(ispirazione: Steam Library, Xbox Hub, PlayStation home). Griglia di card
animate (entrance + hover) con copertine illustrate, badge progressi
sbloccati per ciascun gioco, indicatore "continua dove avevi lasciato",
tutorial integrato per nuovi utenti. Doppia skin attivabile: "Arena"
(look gaming pieno di animazioni e colori) e "Classica AGID" (Bootstrap
Italia puro, zero animazioni — toggle nella accessibility-toolbar v2).
Progressi gestiti via localStorage, niente account, niente cloud.

OBIETTIVO:
Fare da contenitore unitario e accattivante per i 6 nuovi giochi che
costruiremo nei Livelli 5. Migliorare l'esperienza dei giochi esistenti
nella stessa identità visiva. Trasformare la sezione giochi da accessorio
secondario a vetrina educativa che attira ragazzi e famiglie.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
La skin "Arena" non deve essere il default per chi ha prefers-reduced-motion
attivo: in quel caso si parte automaticamente con skin "Classica". Animazioni
mai >3Hz. Localstorage minimal: solo nome utente opzionale + progressi giochi
(esposto in modo trasparente, cancellabile con un click). Coerente con coach
giochi esistente.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, design system gaming (palette declinata, font
secondario eventuale, micro-animazioni), data structure progressi. Per ora
il launcher mostrerà i giochi esistenti — i 6 nuovi li aggiungeremo via
via. Quando hai un piano chiaro, eseguilo.
```

---

# LIVELLO 4 — Impegnative

## #3 — Mappa interattiva del territorio

```
Devi implementare l'idea #3 della roadmap PC Genzano.

COSA È:
Mappa interattiva del territorio di Genzano e Castelli Romani con punti di
interesse rilevanti per la Protezione Civile: aree di raccolta evacuazione
(D.M. 13/2/2014), sedi PC, idranti UNI conformi, defibrillatori AED (mappa
DAE-RespondER), punti acqua, zone a rischio frana (CARG), zone allagamento
storico, confini zona F DPC, sedi VVF e CRI più vicine. Filtri per categoria.
Geolocalizzazione opt-in per centrare la mappa sulla posizione utente.
Stack consigliato: Leaflet + OpenStreetMap (entrambi gratis, no API key).

OBIETTIVO:
Dare al cittadino uno strumento autonomo per orientarsi nell'emergenza,
prima e durante. Riferimento ufficiale che mancava sul territorio
(ogni comune dei Castelli ha mappe statiche PDF nascoste, noi facciamo una
mappa interattiva di tutti i comuni vicini). Trasparenza sull'infrastruttura
di protezione esistente: dove sono i defibrillatori, dove sono gli idranti
funzionanti, dove sono le aree di raccolta ufficiali.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
Dati GeoJSON statici nel repo (data/mappa/*.geojson). Marker accessibili:
tabella equivalente "tutti i punti di interesse in lista" come alternativa
testuale (WCAG 2.2 1.1.1). Layer attivabili separatamente. Geolocalizzazione
in opt-in esplicito con messaggio chiaro. Niente tile premium: solo
OpenStreetMap o tile gratuiti. Nominare le fonti dati (Comune, Regione,
DAE-RespondER, CARG, ecc.) sotto la mappa.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, organizzazione dei layer, UX dei filtri, fonte dei
dati di partenza (per ora dati di esempio sintetici per Genzano, poi li
arricchiamo coi dati reali in commit successivi). Quando hai un piano chiaro,
eseguilo.
```

---

## #7 — Quiz "Quanto sei preparato?"

```
Devi implementare l'idea #7 della roadmap PC Genzano.

COSA È:
Quiz adattivo "Quanto sei preparato a un'emergenza?". 12-15 domande
ramificate (l'utente sceglie la propria situazione iniziale, le domande
successive si adattano: vive solo / con famiglia / con anziani / con animali,
abita in casa o in appartamento, ha auto o no, eccetera). Alla fine: badge
personalizzato con il profilo di preparazione + PDF stampabile generato
client-side (jsPDF) con piano d'azione su misura. Tutto in localStorage,
niente backend, niente raccolta dati.

OBIETTIVO:
Far emergere all'utente cosa gli manca per essere davvero preparato, in modo
non giudicante e personalizzato. Generare contenuto pratico ("ecco il piano
per te") invece di astratto ("ecco il decalogo generale"). Stimolare
condivisione social del badge (effetto rete senza sacrificare la privacy).

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
Quiz accessibile da sola tastiera, lettore di schermo, prefers-reduced-motion
rispettato. Domande in linguaggio AGID, niente giudizio morale ("Sei
impreparato!" → no; "Ecco le 3 cose che ti aiuterebbero" → sì). PDF generato
client-side con jsPDF: nessun dato esce dal browser dell'utente. Badge
condivisibile come immagine PNG generata localmente (canvas → toBlob).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu state machine del quiz, struttura albero domande, design del badge
finale, template PDF. Quando hai un piano chiaro, eseguilo.
```

---

## #26 — Mappa rischi DPC zone Lazio

```
Devi implementare l'idea #26 della roadmap PC Genzano.

COSA È:
Widget integrato nella homepage e nella pagina /emergenza/ che mostra in
forma amichevole lo stato delle zone di allerta meteo del Lazio (con focus
sulla zona F, la nostra). Dati presi dal bollettino DPC Regione Lazio. Se
il DPC pubblica un endpoint JSON aperto, usarlo direttamente; altrimenti
estendere il workflow check-allerta.yml esistente per scraping settimanale
di tutte le zone Lazio e generazione di un file data/zone-lazio.json.

OBIETTIVO:
Dare al cittadino contesto sulla nostra allerta: se la zona F è gialla ma
le zone limitrofe sono arancioni, è utile saperlo per pianificare spostamenti.
Migliorare la comprensione del sistema codice colore mostrandolo applicato
in concreto.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
Non sostituire il pannello allerta esistente: integrarlo come pannello
"contesto regionale" complementare. Aggiornamento massimo ogni 6 ore
(coerente con check-allerta.yml). Mappa SVG vettoriale del Lazio nel repo
(disegno semplificato delle zone, non confini amministrativi precisi: si
tratta di una mappa schematica). Legenda accessibile con tabella equivalente.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu se chiedere al DPC un'API ufficiale o ricorrere a scraping pulito,
architettura del widget, posizionamento. Quando hai un piano chiaro, eseguilo.
```

---

## #10 — Sistematizzazione contenuti in LIS

```
Devi implementare l'idea #10 della roadmap PC Genzano.

COSA È:
Sistema strutturato per video LIS (Lingua Italiana dei Segni) sui contenuti
critici del sito: pagina /emergenza/, 12 Kit Calamità, /assistente/, principali
articoli "Cosa fare se". Video brevi (15-60 secondi), MP4 H.264 ottimizzati,
ospitati su GitHub Releases del repo (gratis fino a 2 GB per release).
Badge "Disponibile in LIS" cliccabile su ogni pagina che ha il video, che
apre lightbox con player accessibile, sottotitoli, trascrizione testuale
estesa. Sezione indice /lis/ con elenco di tutti i video disponibili.

OBIETTIVO:
Rendere accessibili in LIS i contenuti vitali del sito alle persone sorde
segnanti (~70.000 in Italia). Posizionare il sito come PA all'avanguardia
sull'inclusione comunicativa. Stabilire un format replicabile da altri
Gruppi PC.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md.
I video LIS richiedono un interprete LIS qualificato: tecnicamente costruiamo
l'infrastruttura, i video stessi li produrremo in collaborazione con
ENS sezione Roma in tempi successivi. Player video con controlli tastiera
completi, captions track WebVTT (non solo "sottotitoli stampati": tracce
selezionabili). Trascrizione testuale completa sotto ogni video (WCAG 2.2
1.2.1 + 1.2.2). Niente YouTube embed (privacy: niente cookie terzi):
self-hosted via GitHub Releases.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, partial player, frontmatter badge, indice. Per ora
predisponi infrastruttura completa + UN video segnaposto (placeholder con
trascrizione testuale di esempio). I video reali li gireremo dopo. Quando
hai un piano chiaro, eseguilo.
```

---

## #2 — Notifiche allerta browser (no Service Worker)

```
Devi implementare l'idea #2 della roadmap PC Genzano, nella variante senza
Service Worker (la PWA è vietata per scelta utente: vincolo permanente).

COSA È:
Sistema di notifiche allerta meteo via Notification API nativa del browser,
SENZA Service Worker (limite: funziona solo finché la tab del sito è aperta).
Quando l'utente attiva l'opt-in, una piccola routine JavaScript polla
data/allerta.json ogni 5 minuti tramite fetch + If-Modified-Since: se il
livello sale a arancione/rosso, si lancia una notifica nativa (con
vibrazione mobile dove supportata via Vibration API).

OBIETTIVO:
Avvisare il cittadino quando l'allerta peggiora, senza chiedergli di
ricaricare la pagina o controllare i social. È un palliativo rispetto a una
push notification completa (che richiederebbe Service Worker = vietato),
ma copre un caso d'uso reale: utenti che lasciano la nostra pagina aperta
in background sul telefono.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md e delle .claude/rules/0*.md, in
particolare il DIVIETO PWA / Service Worker (motivo: cache aggressiva non
gestibile, gli utenti vedono versioni stale del sito). Opt-in con messaggio
chiaro che spiega il limite "funziona solo se tieni la tab aperta".
Privacy: nessun tracking, nessun ID utente, polling solo del JSON pubblico
allerta. Frequenza polling configurabile, default 5 minuti, max 1 minuto in
fascia rossa.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu UX di opt-in, dove posizionare il toggle, come gestire fallback
per browser senza Notification API o senza Vibration. Quando hai un piano
chiaro, eseguilo.
```

---

# LIVELLO 5 — Grandi progetti gaming

NOTA TRASVERSALE PER TUTTI I GIOCHI: ognuno deve rispettare la rule
03-accessibility.md "Coach dei giochi" del CLAUDE.md, avere skin "classica
AGID" alternativa attivabile da accessibility-toolbar, pausa universale,
controlli tastiera completi, no flash >3Hz, soluzione raggiungibile senza
audio. Progressi in localStorage, niente cloud. Estetica "videogioco moderno"
con palette istituzionale (#003366 blu PC) declinata in chiave gaming.

---

## #15 — "Codice Colore Rapido"

```
Devi implementare l'idea #15 della roadmap PC Genzano: il primo dei nuovi
giochi in stile videogioco moderno.

COSA È:
Mini-gioco a tempo "Codice Colore Rapido". Compare in scena una mini-
situazione testuale ("Pioggia forte sui Castelli Romani per le prossime
12 ore", "Vento moderato in pianura", ecc.) e quattro pulsanti colorati
(verde / giallo / arancione / rosso): vince chi tocca quello corretto entro
3 secondi. Modalità "carriera 30 livelli a difficoltà crescente" +
modalità "infinita".

OBIETTIVO:
Insegnare il sistema codice-colore DPC in forma giocosa a bambini, ragazzi
e cittadini adulti, con un'estetica da videogioco moderno (animazioni fluide,
palette istituzionale declinata in chiave gaming, micro-feedback visivi e
sonori opzionali). Deve invogliare anche un quattordicenne, non sembrare un
quiz didattico anni '90.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md, delle .claude/rules/0*.md e la nota
trasversale sui giochi sopra. Le situazioni di scenario devono essere
realistiche e didatticamente corrette: ognuna corrisponde a una vera
combinazione "evento meteo → livello DPC" secondo la classificazione
ufficiale. Niente librerie a pagamento, niente leaderboard cloud.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu stack (canvas vanilla / Pixi / Phaser / pure CSS+JS), illustrazioni,
animazioni, struttura livelli. Quando hai un piano chiaro, eseguilo.
```

---

## #16 — "Memory Calamità" 3D

```
Devi implementare l'idea #16 della roadmap PC Genzano: secondo gioco gaming.

COSA È:
Memory match con flip 3D delle carte (CSS 3D transforms + GSAP gratuito).
Tre mazzi tematici: rischio idraulico (oggetti del kit alluvione), rischio
sismico (oggetti del kit terremoto), rischio AIB (oggetti del kit incendio).
Difficoltà progressive 8 / 16 / 24 / 32 carte. Particle effect al match,
suoni di conferma opzionali. Al completamento, mini-scheda informativa
sull'oggetto della coppia trovata.

OBIETTIVO:
Memorizzare per associazione gli oggetti dei kit emergenza. Adatto a
bambini elementari e primi anni medie. Estetica giocattolo moderno
(non clip-art anni 2000).

VINCOLI:
Rispetta tutte le regole del CLAUDE.md, delle .claude/rules/0*.md e la nota
trasversale sui giochi sopra. Illustrazioni vettoriali coerenti (stile
unico), non emoji né foto stock. Animazioni disattivabili (prefers-reduced-
motion). Senza GSAP se possibile (vediamo se animazioni CSS native bastano:
è più leggero, ma se serve GSAP è dipendenza accettabile gratis).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu stack, illustrazioni (commissionate o vettoriali tue), data
structure del mazzo, UX. Quando hai un piano chiaro, eseguilo.
```

---

## #14 — "Kit dello Zaino" 2.0 con fisica

```
Devi implementare l'idea #14 della roadmap PC Genzano: refactor totale del
gioco "Kit dello Zaino" esistente.

COSA È:
Refresh completo del gioco esistente. Engine fisica Matter.js (gratuito):
drag and drop con peso e ingombro realistico, animazioni di rimbalzo, zaino
che si riempie in modo 3D-like (CSS transform / canvas 2D), timer 3 minuti,
feedback sonori opzionali. Spiegazione contestuale per ogni oggetto: perché
la pila va prima della radio? Perché l'acqua va in bottiglie PET e non
vetro? Punteggio basato su completezza + ordine ottimale.

OBIETTIVO:
Trasformare un gioco didattico esistente in un'esperienza ludicamente
soddisfacente. Insegnare non solo COSA mettere nel kit ma anche PERCHÉ e
COME (ordine di accesso prioritario). Adatto a famiglie con bambini in fase
di preparazione kit casa.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md, delle .claude/rules/0*.md e la nota
trasversale sui giochi sopra. Matter.js è una dipendenza accettabile gratis.
La fisica deve essere disattivabile (chi non la vuole, modalità "kit
classico" drag&drop semplice senza simulazione fisica). Tutte le info sugli
oggetti del kit aggiornate alle linee guida ufficiali DPC e Sphere 2018.
Preservare i contenuti educativi del gioco attuale (non perdere niente di
quanto già funziona).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura, integrazione Matter.js, illustrazioni oggetti, UX.
Quando hai un piano chiaro, eseguilo.
```

---

## #17 — "Cronaca dell'Emergenza" adventure

```
Devi implementare l'idea #17 della roadmap PC Genzano: avventura testuale
moderna stile Reigns / 80 Days.

COSA È:
Avventura testuale a scelta multipla con presentazione modernissima (swipe
left/right su mobile, frecce/tasti su desktop). Quattro scenari realistici
sui Castelli Romani: alluvione lampo a Genzano, sciame sismico Colli
Albani, incendio AIB estivo, blackout esteso con anziano in casa.
Ogni scenario è una catena di 15-25 scelte con conseguenze, ogni partita
dura 5-8 minuti, finali multipli (positivo, parziale, negativo) con
spiegazione di cosa sarebbe stato meglio fare. Tipografia editoriale,
foto bianco/nero virate blu istituzionale, suono ambientale opzionale.

OBIETTIVO:
Trasferire competenza attraverso narrazione esperienziale. La differenza
fra leggere "evita ascensori in terremoto" e VIVERLO in una storia dove
hai scelto l'ascensore e ne paghi le conseguenze è enorme. Adatto a
ragazzi delle superiori e adulti.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md, delle .claude/rules/0*.md e la nota
trasversale sui giochi sopra. Gate AGID applicato sui testi narrativi (lo
storytelling deve essere di qualità professionale). Niente toni catastrofisti
o traumatizzanti: gli scenari devono educare, non spaventare per spaventare.
Ogni "finale negativo" si chiude con una nota costruttiva ("ecco cosa
sarebbe stato meglio"). State machine pura (niente engine d'avventura
esterni se non strettamente necessari).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura state machine, struttura dei rami narrativi (YAML/JSON?),
UX swipe/keyboard, design del finale. Quando hai un piano chiaro, eseguilo.
```

---

## #12 — "Centrale Operativa 112" tycoon

```
Devi implementare l'idea #12 della roadmap PC Genzano: simulatore tycoon
della centrale operativa.

COSA È:
Simulatore in cui l'utente è dispatcher di una mini-centrale operativa.
Riceve "chiamate" (clip audio TTS o file MP3 brevi con voci diverse), legge
il caso, assegna codice triage (rosso/giallo/verde/bianco), decide quali
mezzi mandare (CRI, VVF, ambulanza, PC volontaria) tenendo conto di risorse
limitate (X ambulanze, Y squadre PC), gestisce flussi simultanei. Stile HUD
futuristico con palette istituzionale, font monospace tipo terminale,
mappa Genzano stilizzata vettoriale come sfondo dinamico. Phaser 3 come
engine consigliato (gratis, HTML5).

OBIETTIVO:
Insegnare la logica triage e la gestione risorse alla cittadinanza con un
gioco serio. Sensibilizzare sull'importanza dei codici colore, sul perché
"chiamo il 118 e poi attendo" significa una decisione informata altrove.
Funziona anche come strumento di reclutamento volontari interessati alla
parte operativa.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md, delle .claude/rules/0*.md e la nota
trasversale sui giochi sopra. Triage e protocolli realistici (riferimenti
linee guida SIS 118 e EENA). Audio chiamate: se TTS browser, fallback con
testo. Niente situazioni eccessivamente cruente o realistiche-traumatiche:
è un serious game, non un horror.
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura Phaser, design HUD, scenari, audio, progressione
difficoltà. Quando hai un piano chiaro, eseguilo.
```

---

## #13 — "Evacua Genzano" RTS

```
Devi implementare l'idea #13 della roadmap PC Genzano: il gioco più
ambizioso, RTS di gestione evacuazione.

COSA È:
Real-time strategy in cui l'utente gestisce l'evacuazione dei cittadini di
Genzano da una zona colpita verso le aree di raccolta ufficiali. Mappa
stilizzata della città (SVG vettoriale), sprite cittadini-puntini animati
da guidare lungo percorsi sicuri, ondate progressive di scenario: sisma,
alluvione, incendio AIB, incidente chimico su via Anagnina. Sistema
punteggio basato su % popolazione in salvo + tempo + risorse utilizzate
(volontari, mezzi, comunicazioni). PixiJS come engine consigliato (gratis,
WebGL renderer per performance fluide anche con centinaia di sprites).

OBIETTIVO:
Trasmettere la complessità reale della gestione evacuazione in PC. Far
comprendere alla cittadinanza perché le esercitazioni sono importanti, cosa
fanno i volontari durante un'emergenza vera. Strumento divulgativo top-level,
adatto a ragazzi delle superiori, universitari, adulti curiosi.

VINCOLI:
Rispetta tutte le regole del CLAUDE.md, delle .claude/rules/0*.md e la nota
trasversale sui giochi sopra. Mappa Genzano stilizzata, non realistica al
millimetro (evita di sembrare strumento operativo: è un serious game).
Niente vittime visualizzate esplicitamente (un puntino che non arriva
diventa grigio, non c'è sangue). Tutti gli scenari hanno una soluzione
ottimale dimostrabile (non frustrazione gratuita).
Sei su CLI desktop, vai fino in fondo: push diretto su main quando finito.

Decidi tu architettura PixiJS, pathfinding, design ondate, balance economy,
UX. Quando hai un piano chiaro, eseguilo. Questo è il gioco più grande:
considera di spalmarlo su più sessioni con commit incrementali (es. prima
solo lo scenario "alluvione", poi gli altri tre via via). Apri una issue
"epic" sul repo per tracciare l'avanzamento.
```

---

## Note di chiusura

I prompt si possono usare in qualsiasi ordine, ma il consiglio è:
1. Partire dal Livello 1-2 per accumulare slancio e abituare il workflow.
2. Affrontare il Livello 3 a blocchi tematici (es. accessibilità: #27 + #9 + #5 + #10).
3. Il Livello 4 va affrontato uno alla volta, con tempo dedicato.
4. Il Livello 5 (giochi) può andare in parallelo al Livello 11 (hub) — il
   primo a essere pronto è "Codice Colore Rapido" che fa da template stilistico
   per gli altri.

Se durante un'iniziativa Claude Code propone deviazioni o scopre vincoli che
non avevamo previsto, ascoltalo: il prompt è alto livello apposta per lasciarli
emergere. Le sue domande di chiarimento valgono oro per affinare il piano.
