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
- **Dubbi → domande** (istruzione di Alessandro del 13/10/2026: «se hai dubbi sei obbligato a fare domande a me per chiarimenti»). Quando una scelta cambia davvero l'esito e la risposta non è nei file, nelle regole o nelle fonti, non si indovina: si chiede ad Alessandro — in chat se c'è, altrimenti in «Domande» qui sotto — e intanto si fa il resto. Per le scelte ordinarie coperte dalle regole si procede e si riporta (regola `.claude/rules/autonomia.md`).

### Che cosa fa ChatGPT quando Alessandro scrive «guarda la bacheca» (o «continua il lavoro»)

ChatGPT lavora **in autonomia fino alla pubblicazione**, senza aspettare Claude:

1. **Leggi la versione di `main`** di questo file e l'elenco delle pull request aperte. Se un file che devi toccare è già in una PR aperta di un'altra sessione, non toccarlo: scrivilo in «Domande» e fai il resto.
2. **Prendi prima i lavori lasciati a metà** nella sezione «Lavori in corso», poi le richieste aperte indirizzate a ChatGPT (o a «chi è disponibile»), in ordine di data. Solo se entrambe le sezioni sono vuote rispondi in una riga: «Nessuna richiesta aperta per me in bacheca».
3. **Apri un ramo tuo** da `main` aggiornato: `chatgpt/<argomento>-AAAAMMGG` (o `codex/...`). Non riprendere il ramo di un'altra sessione, **salvo quando è indicato in «Lavori in corso»** o quando il lavoro ti arriva con un passaggio automatico (§ «Passaggio automatico a ChatGPT»): in quei casi il ramo, e la sua PR, sono passati a te e li continui lì.
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
- **Ogni lavoro è a firma di Alessandro Cuollo** — o del suo nominativo radioamatoriale **IU0QVW**, dove è d'uso — e in nessun caso deve apparire che sia stato fatto da un'intelligenza artificiale, «mai e poi mai» (istruzione del 13/10/2026, che estende a tutti i repository la regola nata in `sito-pc-genzano`). In pratica: identità git `Alessandro Cuollo <65465537+SviluppoItaliaDigitale@users.noreply.github.com>` su ogni commit (`bash scripts/imposta-identita-git.sh`, presente in ogni repository, la imposta e attiva l'hook `.githooks/commit-msg`, che toglie dal messaggio le righe `Co-authored-by` e quelle di sessione); nessun nome di strumenti nei messaggi di commit, nei titoli, nei testi e nei commenti delle PR, nei file pubblicati, nei metadati e nelle immagini; i commit arrivati su un ramo con un altro autore si riscrivono a nome di Alessandro prima di unire (`passa-a.py chiudi` lo fa da sé e toglie dalla PR i commenti di avvio e di risposta dello strumento); il merge è sempre squash con messaggio scritto a mano, così su `main` l'autore è Alessandro. Unica eccezione: i file di governo interni, non pubblicati (`CLAUDE.md`, `AGENTS.md`, `.claude/`, questa bacheca), che parlano necessariamente degli strumenti. Regola completa in `.claude/rules/firma-dei-lavori.md`, uguale in tutti i repository.
- **Italiano corretto e chiaro** in file, commit e PR.
- **Non cancellare quello che ha scritto l'altra**: si risponde sotto o si archivia con una riga di esito.

### Formato delle voci

- **Richiesta**: `- **AAAA-MM-GG — da <chi> a <chi> — <titolo>**` e sotto: che cosa serve, quali file, quali controlli, dove si pubblica. Chi la prende scrive accanto «presa da …, PR #N»; a lavoro pubblicato la sposta in «Archiviati» con l'esito.
- **Avviso**: `- **GG/MM/AAAA — <chi>.** testo`, in cima alla sezione «Avvisi». Serve quando un lavoro riguarda anche l'altra sessione (file rifatti, script cambiati, file generati da rigenerare).
- **Domanda**: in «Domande». Chi la legge risponde sotto, alla prima occasione.
- **Consegna di fine sessione**: chi chiude una sessione con lavoro a metà scrive in «Lavori in corso» che cosa resta, su quale ramo e in quale PR, così l'altra può riprenderlo: da quel momento il ramo passa all'altra sessione, e chi l'ha consegnato non ci fa più push finché non lo riceve indietro con una nuova consegna.

### Passaggio automatico a ChatGPT (dal 13/10/2026)

Claude non aspetta più che Alessandro scriva «guarda la bacheca»: quando decide che un lavoro va a ChatGPT, lo avvia da sola. Istruzione di Alessandro del 13/10/2026: «devi essere te in automatico a creare le istruzioni, aprire l'intelligenza artificiale idonea, fargli fare le cose e andare a pubblicare»; «valuta te i casi in cui deve essere utilizzato».

**Nessun passaggio a mano per Alessandro.** Istruzione del 13/10/2026: «io non devo fare nulla: devi fare tutto te in piena autonomia nel migliore dei modi»; «considera che hai un amico a disposizione a darti una mano, e tu gli devi dire esattamente cosa deve fare». Quindi: Claude decide, scrive la richiesta completa, la avvia, controlla il risultato, corregge o rifà da sola quando non va, e pubblica. Alessandro non copia testi, non apre chat, non incolla file. Se un lavoro non si può passare (sotto, «Che cosa non si passa») o non si può fare nel canale automatico (sotto, «Immagini»), lo fa Claude, se serve con più agenti in parallelo (regola `.claude/rules/autonomia.md`, uguale in tutti i repository: autonomia, lavoro diviso, agenti e skill creati quando servono, domande ad Alessandro nei dubbi).

**Come si avvia.** Claude scrive la richiesta in «Richieste» (formato di sempre, con la nota «passata in automatico»), apre un ramo `chatgpt/<argomento>-AAAAMMGG` da `main` aggiornato, apre una **pull request in bozza** con la stessa richiesta nella descrizione e lascia sulla PR il commento `@codex esegui la richiesta nella descrizione`. Codex, lo stesso che già rivede le pull request, parte da solo, lavora su quel ramo e fa push; il commento arriva dall'account di Alessandro, quindi vale come una sua istruzione. Chi lavora segue il protocollo di sempre (punti 4-6): controlli del repository, bacheca aggiornata sullo stesso ramo con «fatta da ChatGPT, PR #N», nessun'altra PR. Lo fa lo script `scripts/passa-a.py`, uguale in tutti i repository (`nuovo` avvia, `stato` controlla, `chiudi` unisce; `modello` stampa lo schema della richiesta). Se in un repository l'integrazione Codex non risponde, Claude fa il lavoro da sola e lo scrive in «Domande», una volta sola, perché Alessandro possa attivarla quando vuole.

**Che cosa contiene la richiesta, sempre.** ChatGPT lavora bene solo con istruzioni esatte, e nel canale automatico non può fare domande: tutto ciò che gli serve sta nella richiesta, verificato prima da Claude. Sette parti, nell'ordine (`passa-a.py modello` le stampa): (1) **obiettivo** in una frase, e a che cosa serve; (2) **file** da creare o modificare, con il percorso esatto; (3) **che cosa fare**, passo per passo, con i dati già verificati (numeri, nomi, date, misure, testi): niente da cercare, niente da indovinare; (4) **vincoli** del repository che valgono per quel lavoro (regole, licenze, misure, accessibilità, niente riferimenti allo strumento nei file e nei commit); (5) **controlli** da eseguire prima del push, con i comandi esatti; (6) **consegna**: commit sul ramo della PR, bacheca aggiornata sullo stesso ramo, un commento breve sulla PR con fatto / non fatto / perché; (7) **che cosa non fare**: non unire, non segnare pronta, non aprire altre PR, non toccare altri file. Una richiesta a cui manca una parte non si manda.

**Quando Claude lo fa da sola.** Lo decide caso per caso, con parsimonia: il piano ChatGPT ha crediti a consumo e ogni passaggio li usa (li usa anche la revisione automatica che Codex fa su ogni PR non in bozza, quindi la PR resta in bozza finché il lavoro non è finito, e più lavori piccoli si mettono in una richiesta sola). Si passa un lavoro quando:

- **serve andare live prima su più fronti**, soprattutto in emergenza o quando lo stesso contenuto esce su più siti: Claude tiene per sé la parte che richiede i gate editoriali e la comunicazione di allerta ed emergenza, e passa a ChatGPT le parti autonome che si possono specificare per iscritto (script e dati, controlli, audit, materiali di supporto, adattamenti di cose già fatte), così lavorano in parallelo invece che in fila;
- **è un lavoro che ChatGPT sa fare bene e che non ha bisogno del giudizio della sessione**: l'aggiornamento degli interventi dall'export del gestionale, gli audit del sito, i controlli ripetitivi;
- **una sessione finisce con un lavoro urgente a metà** (emergenza, uscita programmata entro un giorno, Alessandro ha chiesto di andare live): oltre alla consegna in «Lavori in corso», Claude passa il ramo a ChatGPT con lo stesso meccanismo. Se non è urgente, scrive solo la consegna.

**Immagini.** Le illustrazioni **SVG** le fa Claude (istruzione di Alessandro del 13/10/2026): sono codice, le rende e le guarda prima di pubblicarle; le passa a ChatGPT solo per lavorare in parallelo, con la richiesta completa (misure, contenuto riquadro per riquadro, testi, vincoli). Le **immagini raster** (foto, locandine, grafiche PNG o JPG) non passano dal canale automatico, perché Codex non ha il generatore di immagini: le fa Claude con i propri strumenti — i generatori del repository (cover, immagini social, fascia blu), gli SVG resi in PNG, i connettori grafici disponibili nella sessione quando ci sono, le foto con licenza libera — e le controlla prima del commit come ogni immagine. Se un'immagine non si può fare in nessuno di questi modi, Claude sceglie l'alternativa migliore (per esempio un'illustrazione al posto di una foto) e lo scrive nella PR. Nessun passaggio a mano per Alessandro.

**Che cosa non si passa.** Allerte ed emergenze vere, articoli nuovi che devono passare dai gate editoriali, pagine legali, lavori che richiedono credenziali, spese o invii a persone: restano a Claude o ad Alessandro, come in «Quando ChatGPT non unisce e si ferma».

**Chi chiude.** Codex avviato da un commento non unisce la PR e non la segna pronta. Chiude Claude: la sessione che ha fatto il passaggio ne controlla l'esito (`passa-a.py stato`), guarda il risultato (immagini rese e guardate, controlli del repository, niente dati inventati né riferimenti allo strumento), poi `passa-a.py chiudi`: riscrive a nome di Alessandro i commit del ramo che avessero un altro autore, segna la PR pronta, aspetta i controlli verdi, unisce (squash con messaggio scritto, un merge per volta), toglie dalla PR il commento di avvio e le risposte dello strumento e verifica la pubblicazione. Se la sessione è finita, lo fa la routine giornaliera. Se il risultato non va bene, Claude **continua direttamente** sullo stesso ramo e corregge o rifà, senza rimandare indietro (ogni giro costa crediti); se Codex risponde che i crediti sono finiti o non risponde entro un giorno, Claude fa il lavoro da sola e lo scrive in bacheca.

**Gemini.** Lo stesso schema varrà per Jules (etichetta `jules` su una issue) quando Alessandro avrà autorizzato l'app sui repository; fino ad allora i lavori che sarebbero andati a Gemini li fa Claude o passano a ChatGPT.

<!-- PROTOCOLLO-COMUNE:FINE -->

## Questo repository: sito-pc-genzano

Il merge su `main` pubblica il sito su Aruba e GitHub Pages in pochi minuti (`deploy.yml`). Le regole complete sono in `AGENTS.md` (punto d'ingresso per ChatGPT) e in `CLAUDE.md`.

### Controlli prima di unire una PR

- `hugo --minify` senza errori, e i controlli bloccanti della PR verdi (`validate-pr.yml`, `pa11y-ci.yml`).
- Articoli in `content/comunicazioni/`: il controllo di forma e dei fatti di `AGENTS.md` § 3.4 e § 3.5 (se Claude non c'è, usa come lista di controllo `.claude/agents/pc-article-reviewer.md`, `pc-fact-checker.md`, `pc-calendario-editoriale.md` per gli articoli programmati); cover generata con `python3 scripts/genera-cover.py <file>`; `python3 scripts/check-refusi.py <file>`; `python3 scripts/check-data-uscita.py`.
- Schede, kit e giochi: `.claude/agents/pc-didattica-reviewer.md` come lista di controllo; `python3 scripts/check-parita-schede.py`; i pacchetti si rigenerano con gli script, mai a mano.
- Illustrazioni: `python3 scripts/check-illustrazioni-udl.py` e il disegno guardato a 1200 px (a 720 px per i `-mobile.svg`).
- Identità dei commit: `bash scripts/imposta-identita-git.sh` (nome Alessandro Cuollo). Nessuna riga che citi lo strumento nei commit e nelle PR.

### Passaggi automatici in questo repository

- Li avvia Claude con `python3 scripts/passa-a.py nuovo` (ramo, voce in bacheca, PR in bozza, commento di avvio), li controlla con `passa-a.py stato` e li chiude con `passa-a.py chiudi --pr N` (commit riscritti a nome di Alessandro se serve, PR pronta, controlli verdi, squash merge, commenti dello strumento tolti dalla PR). Dettagli e criteri nel protocollo comune, § «Passaggio automatico a ChatGPT».
- Il commento `@codex …` è il solo riferimento allo strumento ammesso su GitHub, perché è il comando che avvia il lavoro, e `chiudi` lo toglie insieme alle risposte dello strumento. Titolo e descrizione della PR descrivono il lavoro senza nomi di strumenti (lo script si rifiuta di aprirla se ne trova uno); la richiesta per esteso sta in questa bacheca, che non è pubblicata. Le revisioni automatiche di Codex sulle PR pronte restano visibili (una revisione del bot non si può cancellare, a differenza dei commenti): dipendono da un'impostazione di Codex che solo Alessandro può cambiare, e per ora ha scelto di lasciarle (13/10/2026).
- Se la sessione che ha avviato il passaggio non lo chiude, lo chiude la routine giornaliera delle issue (14:00 italiane, rule 10 § «Lavorazione autonoma delle issue automatiche»).

### Quando qui ChatGPT non unisce

- Articoli che raccontano interventi o attività del Gruppo presi dalla stampa o da fonti non nostre: PR pronta ma **non unita**, perché i fatti vanno confrontati con il registro interventi (rule 10, punto 5-bis).
- Allerte ed emergenze vere (`data/allerta.json`, `data/emergenza.json`, articoli `Allerta`/`Emergenza`): solo su istruzione esplicita di Alessandro.
- Pagine legali (privacy, accessibilità, note legali): PR pronta, unisce Alessandro.

### Chi fa che cosa

Indicazioni dell'utente dell'8 ottobre 2026.

- **Illustrazioni SVG (Claude, dal 13/10/2026).** Le fa Claude (istruzione di Alessandro: «tu sei bravo a fare le immagini SVG»): le rende e le guarda a 1200 px e, per le versioni `-mobile.svg`, a 720 px, con `python3 scripts/check-illustrazioni-udl.py` verde. A ChatGPT solo in parallelo, quando serve andare live prima (protocollo comune, § «Passaggio automatico»): in quel caso arrivano su un ramo `chatgpt/…` con una PR, e Claude le guarda prima di unire. Fino al 12/10/2026 le faceva di solito ChatGPT, che le rendeva, le controllava e univa da sé a controlli verdi.
- **Immagini raster (Claude).** Foto, locandine e grafiche PNG o JPG non passano dal canale automatico (Codex non genera immagini): le fa Claude con gli strumenti del repository (`genera-cover.py`, `genera-immagini-social.py`, `applica-fascia-foto.sh`, gli SVG resi in PNG), con i connettori grafici della sessione quando ci sono, con le foto a licenza libera (`pc-image-fixer`); prima del commit valgono i controlli di rule 03 § «Illustrazioni fatte con strumenti esterni» (Read dell'immagine, gesti coerenti col DPC, `alt` e didascalia su ciò che si vede, nessun riferimento allo strumento) e la regola dei 4 loghi con il codice E10435833 dove vale. Nessun passaggio a mano per Alessandro.
- **Audit del sito (di solito ChatGPT).** Chi fa l'audit **non corregge**: scrive i rilievi in `riferimenti-interni/audit-esterni/AAAA-MM-GG-<argomento>.md` (formato nel README della cartella) e lascia un avviso qui. L'altra sessione verifica ogni rilievo, corregge quelli fondati con una PR e scrive l'esito accanto a ciascuno (corretto nella PR #N, non riprodotto, già a posto). Così l'utente non deve più copiare l'audit da una chat all'altra. Se Claude non è disponibile e Alessandro chiede a ChatGPT di correggere, ChatGPT verifica e corregge i rilievi fondati con una PR, seguendo il protocollo comune.
- **Pubblicazioni urgenti quando l'altra sessione non c'è.** Si pubblica con una PR e i controlli verdi; direttamente su `main` solo se l'utente lo chiede espressamente. In entrambi i casi un avviso qui: «pubblicato in urgenza: file …, motivo …, PR o commit …». Alla prima sessione utile l'altra lo ripassa e archivia l'avviso con l'esito.

## Domande

Domande fra le sessioni (o per Alessandro). Chi la legge risponde accanto, alla prima apertura della bacheca, e sposta la voce in «Archiviati» quando la risposta è applicata.

- Nessuna domanda aperta.

## Lavori in corso

Consegne di fine sessione: che cosa resta a metà, su quale ramo, in quale PR.


## Richieste

Lavori che una sessione (o Alessandro) chiede all'altra. Dal 13/10/2026 i passaggi a ChatGPT li avvia Claude da sola (protocollo comune, § «Passaggio automatico a ChatGPT»: voce qui sotto con la nota «passata in automatico» e PR in bozza); per le richieste a Gemini, e per quelle che Alessandro scrive qui a mano, resta l'avviso «guarda la bacheca». Formato nel protocollo comune.

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

