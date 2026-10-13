# Bacheca di coordinamento — sito della Protezione Civile di Genzano di Roma

File interno, non pubblicato (Hugo non legge la cartella principale del repository). Lo usano Claude e ChatGPT per passarsi lavoro, istruzioni e avvisi. Nata l'8 ottobre 2026; dall'11 ottobre 2026 segue il protocollo comune a tutti i repository di Alessandro, qui sotto.

<!-- PROTOCOLLO-COMUNE:INIZIO — testo identico in tutti i repository di Alessandro. Copia di riferimento: assistente-personale/COORDINAMENTO.md. Se lo cambi, cambialo in tutti e cinque i repository nello stesso lavoro. -->

## Protocollo comune Claude ⇄ ChatGPT ⇄ Gemini (uguale in tutti i repository)

Valido dall'11/10/2026 in tutti i repository di Alessandro: `sito-pc-genzano`, `social-pc-genzano`, `sito-misericordia-ariccia`, `cooprimavera`, `assistente-personale`. Il file si chiama sempre `COORDINAMENTO.md` e sta sempre nella cartella principale del repository. Questa prima parte è identica ovunque; la seconda parte, «Questo repository», cambia da repository a repository.

### A che cosa serve

Claude (Claude Code) e ChatGPT (chat con connettore GitHub, Codex) lavorano sugli stessi repository. La bacheca è il posto dove si passano lavoro, istruzioni e avvisi, così Alessandro non deve copiare testi da una chat all'altra e il lavoro continua anche quando una delle due non è disponibile (per esempio quando Claude ha finito i crediti).

**Anche Gemini (dall'11/10/2026).** Gemini lavora sui repository con **Jules** (jules.google, legge da solo `AGENTS.md`) o con Gemini CLI. Dove questo protocollo dice «ChatGPT», vale allo stesso modo per Gemini: stesse regole, stessa autonomia, stesse eccezioni. Differenze: i suoi rami si chiamano `gemini/<argomento>-AAAAMMGG`; una richiesta indirizzata a «ChatGPT» la prende solo ChatGPT, una indirizzata a «Gemini» solo Gemini, una indirizzata a «chi è disponibile» la prende la prima che apre la bacheca, che scrive subito accanto «presa da …» con una PR in bozza, così l'altra non la riprende. Le revisioni automatiche fatte da Codex o da Gemini sulle PR sono pareri da verificare, non ordini.

### Chi dà le istruzioni

- **Alessandro**: in chat o scrivendo una richiesta qui. Le sue istruzioni prevalgono su tutto il resto.
- **Claude o ChatGPT**: con una voce nella sezione «Richieste» di questo file, indirizzata all'altra.
- Le regole del repository (`CLAUDE.md`, `.claude/rules/`, `AGENTS.md`) valgono per entrambe: chi lavora le segue anche quando l'altra non c'è.

### Che cosa fa ChatGPT quando Alessandro scrive «guarda la bacheca» (o «continua il lavoro»)

ChatGPT lavora **in autonomia fino alla pubblicazione**, senza aspettare Claude:

1. **Leggi la versione di `main`** di questo file e l'elenco delle pull request aperte. Se un file che devi toccare è già in una PR aperta di un'altra sessione, non toccarlo: scrivilo in «Domande» e fai il resto.
2. **Prendi prima i lavori lasciati a metà** nella sezione «Lavori in corso», poi le richieste aperte indirizzate a ChatGPT (o a «chi è disponibile»), in ordine di data. Solo se entrambe le sezioni sono vuote rispondi in una riga: «Nessuna richiesta aperta per me in bacheca».
3. **Apri un ramo tuo** da `main` aggiornato: `chatgpt/<argomento>-AAAAMMGG` (o `codex/...`). Non riprendere il ramo di un'altra sessione, **salvo quando è indicato in «Lavori in corso»**: quel ramo, e la sua PR, sono passati a te e li continui lì.
4. **Fai il lavoro** seguendo le istruzioni della richiesta e le regole del repository. Leggi solo i file che servono a quel lavoro.
5. **Fai i controlli del repository** elencati in «Questo repository» (build, script di controllo). Se Claude non c'è, la revisione che di solito fa Claude la fai tu: usa come lista di controllo i file pertinenti di `.claude/agents/` se il repository li ha, altrimenti le regole di `CLAUDE.md`, `.claude/rules/` e i controlli di «Questo repository»; rendi e guarda le immagini, rileggi il testo.
6. **Apri la PR verso `main`** (anche in bozza), poi, **sullo stesso ramo**, aggiorna questa bacheca: accanto alla richiesta scrivi «fatta da ChatGPT, PR #N» con il numero appena assegnato e una riga su che cosa hai fatto; se una parte non si poteva fare, scrivi il motivo. Fai push: la PR si aggiorna da sola.
7. **Aspetta i controlli automatici e, se sono verdi, unisci tu la PR** (squash; se era in bozza, prima segnala che è pronta) e, dove il merge pubblica qualcosa (lo dice «Questo repository»), verifica che la pubblicazione parta e finisca (scheda Actions). Dove il merge non pubblica nulla, non lanciare a mano i workflow di pubblicazione. Questo vale salvo le eccezioni sotto e salvo quelle scritte in «Questo repository». Se il tuo strumento non può unire una PR, scrivi ad Alessandro una riga sola: «Unisci la PR #N: <link>».
8. **Un merge per volta**: se hai più lavori pronti, mettili in una sola PR, oppure aspetta che la pubblicazione precedente sia finita prima di unire la successiva.
9. **Rispondi ad Alessandro in breve**: che cosa hai fatto, numero della PR, link della pagina pubblicata, che cosa resta.

### Quando ChatGPT non unisce e si ferma

- I controlli automatici sono rossi e non sai correggerli: lascia la PR aperta e scrivi il problema in «Domande».
- Il lavoro richiede credenziali, spese, invii a persone o enti (email, messaggi), cancellazioni definitive o post sui social fuori dalle automazioni già previste.
- L'istruzione è ambigua su un fatto (dato, data, nome, norma): non indovinare, scrivi la domanda e fai il resto.
- Lo dice una regola di «Questo repository».

### Regole che valgono sempre

- **Mai commit diretti su `main`**: sempre ramo + PR, salvo che Alessandro lo chieda espressamente per quella modifica.
- **Mai dati inventati**: nomi, numeri, date, norme, recapiti si scrivono solo se verificati su una fonte. Se mancano, resta un campo «[da compilare]» o una domanda in bacheca.
- **Mai segreti nel repository** (password, token, chiavi).
- **Niente riferimenti all'intelligenza artificiale** nei contenuti pubblicati; nei repository della Protezione Civile (`sito-pc-genzano`, `social-pc-genzano`) nemmeno nei messaggi di commit, nei titoli e nei testi delle PR.
- **Italiano corretto e chiaro** in file, commit e PR.
- **Non cancellare quello che ha scritto l'altra**: si risponde sotto o si archivia con una riga di esito.

### Formato delle voci

- **Richiesta**: `- **AAAA-MM-GG — da <chi> a <chi> — <titolo>**` e sotto: che cosa serve, quali file, quali controlli, dove si pubblica. Chi la prende scrive accanto «presa da …, PR #N»; a lavoro pubblicato la sposta in «Archiviati» con l'esito.
- **Avviso**: `- **GG/MM/AAAA — <chi>.** testo`, in cima alla sezione «Avvisi». Serve quando un lavoro riguarda anche l'altra sessione (file rifatti, script cambiati, file generati da rigenerare).
- **Domanda**: in «Domande». Chi la legge risponde sotto, alla prima occasione.
- **Consegna di fine sessione**: chi chiude una sessione con lavoro a metà scrive in «Lavori in corso» che cosa resta, su quale ramo e in quale PR, così l'altra può riprenderlo: da quel momento il ramo passa all'altra sessione, e chi l'ha consegnato non ci fa più push finché non lo riceve indietro con una nuova consegna.

<!-- PROTOCOLLO-COMUNE:FINE -->

## Questo repository: sito-pc-genzano

Il merge su `main` pubblica il sito su Aruba e GitHub Pages in pochi minuti (`deploy.yml`). Le regole complete sono in `AGENTS.md` (punto d'ingresso per ChatGPT) e in `CLAUDE.md`.

### Controlli prima di unire una PR

- `hugo --minify` senza errori, e i controlli bloccanti della PR verdi (`validate-pr.yml`, `pa11y-ci.yml`).
- Articoli in `content/comunicazioni/`: il controllo di forma e dei fatti di `AGENTS.md` § 3.4 e § 3.5 (se Claude non c'è, usa come lista di controllo `.claude/agents/pc-article-reviewer.md`, `pc-fact-checker.md`, `pc-calendario-editoriale.md` per gli articoli programmati); cover generata con `python3 scripts/genera-cover.py <file>`; `python3 scripts/check-refusi.py <file>`; `python3 scripts/check-data-uscita.py`.
- Schede, kit e giochi: `.claude/agents/pc-didattica-reviewer.md` come lista di controllo; `python3 scripts/check-parita-schede.py`; i pacchetti si rigenerano con gli script, mai a mano.
- Illustrazioni: `python3 scripts/check-illustrazioni-udl.py` e il disegno guardato a 1200 px (a 720 px per i `-mobile.svg`).
- Identità dei commit: `bash scripts/imposta-identita-git.sh` (nome Alessandro Cuollo). Nessuna riga che citi lo strumento nei commit e nelle PR.

### Quando qui ChatGPT non unisce

- Articoli che raccontano interventi o attività del Gruppo presi dalla stampa o da fonti non nostre: PR pronta ma **non unita**, perché i fatti vanno confrontati con il registro interventi (rule 10, punto 5-bis).
- Allerte ed emergenze vere (`data/allerta.json`, `data/emergenza.json`, articoli `Allerta`/`Emergenza`): solo su istruzione esplicita di Alessandro.
- Pagine legali (privacy, accessibilità, note legali): PR pronta, unisce Alessandro.

### Chi fa che cosa

Indicazioni dell'utente dell'8 ottobre 2026.

- **Immagini e illustrazioni (di solito ChatGPT).** Si preparano su un ramo proprio e arrivano con una PR; nella bacheca un avviso «illustrazioni X pronte nella PR #N, da controllare». Chi le ha fatte le rende e le guarda a 1200 px e a 720 px, esegue i controlli e, se sono verdi, unisce la PR (protocollo comune, punto 7). Claude, quando c'è, le ripassa dopo.
- **Audit del sito (di solito ChatGPT).** Chi fa l'audit **non corregge**: scrive i rilievi in `riferimenti-interni/audit-esterni/AAAA-MM-GG-<argomento>.md` (formato nel README della cartella) e lascia un avviso qui. L'altra sessione verifica ogni rilievo, corregge quelli fondati con una PR e scrive l'esito accanto a ciascuno (corretto nella PR #N, non riprodotto, già a posto). Così l'utente non deve più copiare l'audit da una chat all'altra. Se Claude non è disponibile e Alessandro chiede a ChatGPT di correggere, ChatGPT verifica e corregge i rilievi fondati con una PR, seguendo il protocollo comune.
- **Pubblicazioni urgenti quando l'altra sessione non c'è.** Si pubblica con una PR e i controlli verdi; direttamente su `main` solo se l'utente lo chiede espressamente. In entrambi i casi un avviso qui: «pubblicato in urgenza: file …, motivo …, PR o commit …». Alla prima sessione utile l'altra lo ripassa e archivia l'avviso con l'esito.

## Domande

Domande fra le sessioni (o per Alessandro). Chi la legge risponde accanto, alla prima apertura della bacheca, e sposta la voce in «Archiviati» quando la risposta è applicata.

- Nessuna domanda aperta.

## Lavori in corso

Consegne di fine sessione: che cosa resta a metà, su quale ramo, in quale PR.


## Richieste

Lavori che una sessione (o Alessandro) chiede all'altra. Alessandro avvisa la sessione destinataria («guarda la bacheca»): nessuna delle due legge la bacheca da sola finché non viene aperta. Formato nel protocollo comune.

- **2026-10-11 — da Claude a ChatGPT — Procedura ricorrente: aggiornamento degli interventi dall'export del gestionale** (richiesta permanente: non si archivia, vale ogni volta che Alessandro manda il file)
  - **Quando**: Alessandro ti manda l'export del gestionale interventi (file `.xlsx`, di solito `gcpc-genzano-di-roma_global_reports_*.xlsx`) e scrive «aggiorna gli interventi» o simile. Lavora con **Codex** (serve eseguire gli script): il file va allegato al task.
  - **Mai nel repository il file `.xlsx`**: contiene i nomi dei volontari. Tienilo fuori dalla cartella del repository (per esempio `/tmp/`) e non fare `git add -A` senza guardare.
  - **1. Cumulativo o parziale?** Guarda la prima data dell'export e confrontala con `periodo.dal` di `static/open-data/statistiche-interventi.json` (oggi `2026-04-04`; ultimo intervento pubblicato `periodo.ultimo_numero`, oggi `178/2026` del `2026-10-06`).
    - prima data uguale o precedente **e** l'export contiene almeno l'intervento `periodo.ultimo_numero` (o numeri successivi), senza buchi nella numerazione → **cumulativo**: `python3 scripts/genera-open-data-interventi.py /tmp/<file>.xlsx`
    - prima data uguale o precedente ma l'export si ferma prima di `periodo.ultimo_numero` → è un export vecchio o incompleto: **fermati e chiedi ad Alessandro** un export più recente; non lanciare nessuno script, cancellerebbe gli interventi successivi.
    - prima data successiva → **parziale**: prima `python3 scripts/aggiorna-open-data-delta.py /tmp/<file>.xlsx --dry-run`, poi senza `--dry-run`. Mai il generatore su un export parziale: cancellerebbe i mesi precedenti.
    - Serve `pip install openpyxl`. Se lo script delta si ferma chiedendo `--volontari-nuovi N`: **fermati e chiedi ad Alessandro** quante persone sono nuove nel Gruppo; non stimare.
  - **1-bis. Interventi in Bozza e numeri mancanti** (regola di Alessandro dell'11/10/2026): gli interventi con stato **Bozza** non si pubblicano mai, perché possono ancora cambiare. Lavora su una copia del file senza quelle righe: se la bozza è l'ultimo numero, l'ultimo pubblicato resta il precedente e la bozza entra col prossimo export, una volta chiusa; se la bozza sta in mezzo a interventi chiusi, **fermati e chiedi**, perché il prossimo aggiornamento la salterebbe. Se nella numerazione manca un numero, chiedi ad Alessandro se è stato annullato prima di procedere. Nella copia riallinea anche gli aggregati dei volontari: il foglio «Interventi membri» può includere le presenze delle bozze, che vanno escluse dai conteggi pubblicati. Le bozze non entrano nemmeno negli articoli, nelle cover e nelle sintesi social.
  - **2. Controlla l'esito**: i file cambiati devono essere solo in `static/open-data/` (statistiche, tipologie, automezzi, volontari; CSV e JSON). Nessun nome, nessun indirizzo, nessun richiedente nei file: se ne vedi uno, fermati.
  - **3. Articoli**: per ogni **giornata di intervento non ancora raccontata** sul sito (cerca in `content/comunicazioni/` per data e argomento; non duplicare quelle già coperte, per esempio il 05/10 e il 06/10 hanno già un articolo), scrivi un articolo `content/comunicazioni/AAAA-MM-GG-<slug>.md` **retrodatato** alla data dell'intervento, con badge `Attività` (o `Aggiornamento` per un maltempo concluso). Regole: `AGENTS.md` § 3.4, § 3.5 e § 5.1; **orari arrotondati** («verso le 18»), **niente nomi, targhe, indirizzi privati o richiedenti**; vie e quartieri solo se servono a capire; il nome dei mezzi preso da `content/chi-siamo/_index.md` § «Mezzi e attrezzature principali»; se usi la stampa locale, solo fatti parafrasati e testate in fondo («Per approfondire»). Cover: `python3 scripts/genera-cover.py <file>` e poi `image:`/`image_alt:`. Interventi piccoli e simili della stessa giornata in un solo articolo; giornate senza nulla di raccontabile (solo servizi interni) si saltano e lo scrivi nella PR. Se nella stessa giornata esistono già altri articoli, usa il formato data con l'orario (`AGENTS.md` § 5.1): guarda gli orari già usati quel giorno e prendi il **primo minuto libero dopo il più alto** (se il 08/10 ha 00:01, 00:02 e 00:03, il nuovo va a `T00:04:00+02:00`); se l'articolo esistente ha la data semplice, portalo a `T00:01:00+02:00` e il nuovo a `T00:02:00+02:00`. Mai due articoli con lo stesso orario nello stesso giorno.
  - **4. Controlli**: `hugo --minify` senza errori, `python3 scripts/check-refusi.py <articoli>`, `python3 scripts/check-data-uscita.py`; poi i controlli della PR (`validate-pr.yml`, `pa11y-ci.yml`) verdi.
  - **5. Pubblica**: un solo ramo `chatgpt/interventi-AAAAMMGG`, **una sola PR** con open data e articoli insieme; nella descrizione elenca le giornate raccontate e quelle saltate. A controlli verdi **uniscila** e verifica che «🚀 Build e Deploy» finisca. Si unisce da sé solo se **tutti i fatti degli articoli vengono dall'export** (il registro del Gruppo). Se un articolo usa anche fatti presi dalla stampa che l'export non conferma, vale la regola delle notizie sull'attività del Gruppo: PR pronta ma **non unita**, con l'elenco dei dati da confermare nella descrizione, e il merge lo decide Alessandro. In alternativa togli quei fatti e unisci.
  - **6. Rispondi ad Alessandro**: periodo aggiornato (dal … al …, ultimo numero), quanti interventi aggiunti, articoli pubblicati con i link, giornate saltate. La issue «📊 Open data interventi da aggiornare», se aperta, si chiude da sola al controllo del lunedì.

Formato per una richiesta di immagine:

```markdown
- **AAAA-MM-GG — da Claude a ChatGPT — Illustrazione <nome-file>.svg**
  - Pagina: /percorso/della/pagina/ (sezione …)
  - Che cosa deve far capire: …
  - Che cosa deve mostrare: … (gesti e comportamenti come nelle indicazioni DPC citate nella pagina)
  - Testi nell'immagine: … (pochi, brevi, mai sopra i disegni)
  - Formato: SVG 1200×620 in static/formazione/illustrazioni-udl/, più la versione -mobile.svg 720×1180 se ci sono più riquadri
  - Vincoli: title e desc in italiano su ciò che si vede; nessun riferimento allo strumento usato; nessun logo
```


- **2026-10-09 — da Claude a ChatGPT — Promemoria sugli orari del caldo**
  - Nella figura ondate-di-calore-gesti ho corretto «esci dopo le 17» in «esci dopo le 18» (desktop e mobile): il decalogo del Ministero della Salute indica le ore più calde dalle 11 alle 18, e la pagina ora dice lo stesso. Nelle prossime figure sul caldo usare 11-18.


## Avvisi

- **13/10/2026 — Claude.** Tolto l'`aria-label="Torna alle storie"` dal link «← Storie e Racconti» in tutte le 20 storie (WCAG 2.5.3: il nome accessibile deve cominciare con il testo visibile): una storia nuova nasce senza quell'attributo. Riformulate in modo neutro le segnalazioni dell'articolo dell'8 ottobre e, con la PR successiva, di altri nove resoconti (niente «un cittadino ci ha chiesto/ha segnalato»: il Gruppo non si attiva su chiamata diretta dei cittadini, rule 06). Regola per i prossimi resoconti: la segnalazione si racconta senza indicare chi l'ha fatta («è arrivata la segnalazione di…»), anche se il rapportino di servizio scrive «cittadino».
- **13/10/2026 — Claude, PR #1360.** Dodici materiali di prevenzione (Biblioteca delle idee sbagliate, «Non è vero che» con `data/smentite.yaml`, calcolatore della scorta, laboratorio di dati reali, uscita sul territorio, scatola delle esercitazioni, cinque schede stampabili, due storie) e la sezione fissa **«Cosa impariamo»** nei resoconti degli interventi (archetype `comunicazioni.md`, rule 02, `pc-article-reviewer` § 7): da qui in poi ogni articolo con badge `Attività`, `Aggiornamento` o `Esercitazione` chiude con quella sezione prima di «Cosa puoi fare tu». Toccati anche i tre articoli dell'8, 9 e 12 ottobre (quello del 12 riallineato al testo della PR #1358), `grafico-csv` (decimali con la virgola), `tts-storia.js`, `custom.css`, la pagina privacy. Chi tocca quei file lo faccia dopo questa PR.
- **11/10/2026 — Aggiornamento interventi, fatto da ChatGPT, PR #1333.** Export cumulativo verificato: 204 rapporti approvati dal 04/04 al 09/10/2026, ultimo 205/2026, 26 aggiunti. Il 191/2026 è annullato (confermato da Alessandro); il 206/2026 resta escluso perché in Bozza, insieme alle sue tre presenze nei totali dei volontari. Originale invariato e XLSX fuori dal repository. Le giornate 7–9 ottobre erano già raccontate: corretto l'articolo del 9 da cinque a quattro interventi, tolta la bozza anche da cover e sintesi social. Regola sulle bozze precisata al punto 1-bis. Build, refusi, date, JSON-LD e verifica visiva della cover eseguiti; merge subordinato ai controlli della PR.
- **11/10/2026 — Aggiornamento interventi, fatto da Claude, PR #1339.** Nuovo export cumulativo: 205 rapporti tutti approvati, ultimo 206/2026 (ora chiuso), 191/2026 ancora assente. Open data rigenerati (205 interventi, 599,7 ore, 854 presenze) e 206 riaggiunto all'articolo del 9 ottobre (cinque interventi, cover rifatta con `--force`). Nessuna giornata nuova da raccontare. Tolto il promemoria sul 206.

- **11/10/2026 — Claude.** Scheda satellite del cruscotto ampliata (shortcode `dashboard-satellite.html`, script `genera-copernicus-sentinel{1,2,3}.py`, `immagini-meteo-release.py`, workflow `aggiorna-copernicus-sentinel3.yml`): livelli tematici NASA, indici Sentinel-2 con mappa dei cambiamenti, mappa dei cambiamenti radar a parità di orbita, qualità dell'acqua dei laghi. Chi tocca quei file o la release `immagini-meteo` lo faccia dopo questa PR: i nomi degli allegati della release ora li elencano i JSON in `static/open-data/`.

- **10/10/2026 — Claude.** Unite le PR #1319 (accessibilità di link e pulsanti: il nome letto dallo screen reader comincia dal testo visibile; regola in rule 03 § «Link e pulsanti») e #1322 (immagini meteo nella release `immagini-meteo` invece che in git; pulizia mensile delle immagini social vecchie). Nelle illustrazioni e nelle pagine nuove: niente `aria-label` che sostituisce il testo visibile di un link o di un pulsante.

- **09/10/2026 — Claude.** Verificate a vista le figure delle PR #1299, #1303 e #1304 (unita). Corretti a mano tre testi: orario del caldo (11-18) e «finché la scossa non finisce» nella versione per telefono dei tre gesti. Aggiunta la figura del triangolo all'esperimento 13. Per lampo e tuono c'è una richiesta qui sopra.
- **09/10/2026 — Pubblicazione immagini nelle pagine didattiche.** Modificate solo `content/rischi-prevenzione/ondate-di-calore.md` e `content/formazione/esperimenti.md` nel branch `chatgpt/pubblicazione-illustrazioni-20261009`: inseriti i cinque SVG già presenti nel repository. Non modificati altri template né asset. La revisione artistica dell'intera libreria resta un intervento separato.

- **09/10/2026 — Illustrazioni completate.** Preparati nel branch `chatgpt/illustrazioni-bacheca-20261009` gli otto SVG richiesti qui sotto, inclusi i tre layout verticali. I file non toccano le pagine: l'inserimento nelle sezioni indicate resta in carico alla sessione che gestisce i contenuti. Controllare `scripts/check-illustrazioni-udl.py` e il rendering delle immagini prima del merge.

- **08/10/2026, 21:45 — Claude.** Le illustrazioni in `static/formazione/illustrazioni-udl/` sono state controllate a vista e corrette (PR #1283, #1285, #1286, #1287, #1291). Prima di aggiungerne o modificarne una: rendila, guardala a 1200 px e, per le versioni `-mobile.svg`, a 720 px; nessun testo sopra un disegno; testo scuro solo su fondo chiaro; `<title>` e `<desc>` che descrivono ciò che si vede; `python3 scripts/check-illustrazioni-udl.py` verde.
- **08/10/2026, 21:45 — Claude.** I pittogrammi ARASAAC si scelgono guardandoli: il primo risultato della ricerca può mostrare tutt'altro (era successo con «scappare», «ospedale», «caldo», «frana»). In `scripts/scarica-pittogrammi.sh` un quarto campo fissa l'identificativo verificato.

## Archiviati

- **10/10/2026 — Correzione di `esperimento-lampo-tuono.svg` (richiesta di Claude del 09/10): unita con la PR #1321.** ChatGPT ha tolto il sole dalla finestra, disegnato le due frecce (lampo diritto, tuono a onde) e spostato il riquadro dei 9 secondi; dopo la revisione di Claude ha liberato il fulmine dall'etichetta e riposizionato le gocce. Figura controllata a 1200 px, controlli verdi.

- **09/10/2026 — Illustrazioni didattiche richieste dalla sessione di coordinamento: SVG prodotti e disponibili nel branch `chatgpt/illustrazioni-bacheca-20261009`.**
  - Ondate di calore: `ondate-di-calore-gesti.svg` + `-mobile.svg`, pagina `/rischi-prevenzione/ondate-di-calore/`.
  - Tombino ostruito: `esperimento-tombino-ostruito.svg` + `-mobile.svg`, esperimento 11.
  - Lampo e tuono: `esperimento-lampo-tuono.svg`, esperimento 19.
  - Maremoto: `esperimento-maremoto-fondale.svg`, esperimento 10.
  - Saturazione della spugna: `esperimento-spugna-saturazione.svg` + `-mobile.svg`, esperimento 6.
  - **09/10/2026: inserimento completato in una PR dedicata:** cinque shortcode `illustrazione-udl` con testo alternativo e didascalie esclusivamente in italiano, nelle pagine `content/rischi-prevenzione/ondate-di-calore.md` e `content/formazione/esperimenti.md`. Versioni mobili selezionate automaticamente dallo shortcode quando presenti. Verificare i controlli GitHub e il deploy della PR prima di considerare il sito aggiornato.

