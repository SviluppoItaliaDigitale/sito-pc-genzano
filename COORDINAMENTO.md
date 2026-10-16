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
3. **Apri un ramo tuo** da `main` aggiornato: `chatgpt/<argomento>-AAAAMMGG` (o `codex/...`). Non riprendere il ramo di un'altra sessione, **salvo quando è indicato in «Lavori in corso»** o quando il lavoro ti arriva con un passaggio preparato da Claude (§ «Passaggio a ChatGPT»): in quei casi il ramo, e la sua PR, sono passati a te e li continui lì.
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
- **Ogni lavoro è a firma di Alessandro Cuollo** — o del suo nominativo radioamatoriale **IU0QVW**, dove è d'uso — e in nessun caso deve apparire che sia stato fatto da un'intelligenza artificiale, «mai e poi mai» (istruzione del 13/10/2026, che estende a tutti i repository la regola nata in `sito-pc-genzano`). In pratica: identità git `Alessandro Cuollo <65465537+SviluppoItaliaDigitale@users.noreply.github.com>` su ogni commit (`bash scripts/imposta-identita-git.sh`, presente in ogni repository, la imposta e attiva l'hook `.githooks/commit-msg`, che toglie dal messaggio le righe `Co-authored-by` e quelle di sessione); nessun nome di strumenti nei messaggi di commit, nei titoli, nei testi e nei commenti delle PR, nei file pubblicati, nei metadati e nelle immagini; i commit arrivati su un ramo con un altro autore si riscrivono a nome di Alessandro prima di unire (`passa-a.py chiudi` lo fa da sé e toglie dalla PR gli eventuali commenti dello strumento); il merge è sempre squash con messaggio scritto a mano, così su `main` l'autore è Alessandro. Unica eccezione: i file di governo interni, non pubblicati (`CLAUDE.md`, `AGENTS.md`, `.claude/`, questa bacheca), che parlano necessariamente degli strumenti. Regola completa in `.claude/rules/firma-dei-lavori.md`, uguale in tutti i repository.
- **Italiano corretto e chiaro** in file, commit e PR.
- **Non cancellare quello che ha scritto l'altra**: si risponde sotto o si archivia con una riga di esito.

### Formato delle voci

- **Richiesta**: `- **AAAA-MM-GG — da <chi> a <chi> — <titolo>**` e sotto: che cosa serve, quali file, quali controlli, dove si pubblica. Chi la prende scrive accanto «presa da …, PR #N»; a lavoro pubblicato la sposta in «Archiviati» con l'esito (per i passaggi preparati da Claude lo fa `passa-a.py chiudi`).
- **Avviso**: `- **GG/MM/AAAA — <chi>.** testo`, in cima alla sezione «Avvisi». Serve quando un lavoro riguarda anche l'altra sessione (file rifatti, script cambiati, file generati da rigenerare).
- **Domanda**: in «Domande». Chi la legge risponde sotto, alla prima occasione.
- **Consegna di fine sessione**: chi chiude una sessione con lavoro a metà scrive in «Lavori in corso» che cosa resta, su quale ramo e in quale PR, così l'altra può riprenderlo: da quel momento il ramo passa all'altra sessione, e chi l'ha consegnato non ci fa più push finché non lo riceve indietro con una nuova consegna.

### Passaggio a ChatGPT — preparato da Claude, avviato da Alessandro, chiuso da Claude (dal 13/10/2026)

Claude non aspetta che Alessandro scriva «guarda la bacheca»: quando decide che un lavoro va a ChatGPT, lo prepara da sola e lo richiude da sola. Istruzioni di Alessandro del 13/10/2026: «devi essere te in automatico a creare le istruzioni, aprire l'intelligenza artificiale idonea, fargli fare le cose e andare a pubblicare»; «valuta te i casi in cui deve essere utilizzato»; «considera che hai un amico a disposizione a darti una mano, e tu gli devi dire esattamente cosa deve fare».

**Perché ci sono due gesti a mano, e solo quelli.** Il canale automatico — il commento `@codex esegui la richiesta nella descrizione` sulla pull request in bozza — per l'account di Alessandro non funziona: con gli ambienti cloud pubblicati per tutti e cinque i repository, Codex risponde comunque «To use Codex here, create an environment for this repo» (difetto aperto di OpenAI sul canale delle pull request, openai/codex #20093, verificato il 13/10/2026 su pull request nuove in tre repository; la documentazione di Codex descrive ormai quel comando come avvio di una chat cloud «legacy»). Le vie a pagamento (azione GitHub con chiave API) sono escluse: decisione di Alessandro dello stesso giorno, «zero spese». Resta Codex Cloud, dove il lavoro lo avvia chi lo chiede e, a lavoro finito, chi lo ha avviato apre la pull request («Review changes and test results before committing or opening a pull request», documentazione ufficiale). Quindi i gesti a mano sono due, entrambi di Alessandro: **l'avvio** (un copia-incolla) e **la consegna** (il pulsante «Create PR» del task). Sono l'eccezione dichiarata alla regola `.claude/rules/autonomia.md` («io non devo fare nulla»); tutto il resto — richiesta, ramo, pull request, testo di avvio, controllo del risultato, firma, merge, deploy, bacheca — resta a Claude. Quando il canale automatico tornerà a funzionare si torna all'avvio dal commento senza cambiare nient'altro: `passa-a.py nuovo --con-codex` lascia anche il commento di avvio, e serve a riprovarlo senza spendere nulla.

**Che cosa fa Claude, prima.** Decide che il lavoro va a ChatGPT (criteri sotto), scrive la richiesta completa (sette parti, sotto) e lancia `python3 scripts/passa-a.py nuovo --argomento <slug> --titolo "…" --brief <file>` (script uguale in tutti i repository; `modello` stampa lo schema): apre il ramo `chatgpt/<argomento>-AAAAMMGG` da `main` aggiornato, scrive la voce in «Richieste» (nota «preparata da Claude, da avviare a mano in Codex Cloud», numero della pull request, ramo, la nota sull'avvio a mano e la richiesta), apre la **pull request in bozza** con la stessa richiesta nella descrizione (senza nomi di strumenti: lo script si rifiuta di aprirla se ne trova uno) e stampa il **testo di avvio**: un'intestazione di poche righe (repository, pull request, ramo, «non toccare la bacheca, non unire, riassumi alla fine») seguita dalla richiesta intera. Claude lo riporta ad Alessandro in chat, pronto da copiare; se la sessione finisce, `passa-a.py riavvia --pr N` lo ristampa quando serve. Intanto Claude fa il resto del lavoro.

**Che cosa fa Alessandro: due gesti.** (1) **Avvio**: apre chatgpt.com/codex, sceglie l'ambiente del repository e, se il selettore lo offre, il ramo `chatgpt/…` della pull request (altrimenti va bene il principale: il testo di avvio contiene già tutta la richiesta); incolla il testo di avvio e avvia. (2) **Consegna**: quando Codex ha finito, preme «Create PR» nel task. Niente altro: non scrive istruzioni, non controlla, non unisce.

**Che cosa fa Codex, durante.** Lavora sul ramo da cui è partito il task, esegue la richiesta punto per punto, fa i controlli indicati e alla fine riassume che cosa ha fatto, che cosa resta e perché. Non tocca `COORDINAMENTO.md` (l'esito in bacheca lo scrive chi chiude, così il lavoro non entra in conflitto con la voce) e non unisce nulla. Il suo contenitore non legge la pull request e la sua rete può essere limitata: per questo il testo di avvio porta la richiesta intera e non rimanda né alla bacheca né a pagine esterne.

**Che cosa fa Claude, dopo.** `passa-a.py stato` dice che cosa è arrivato: «CONSEGNA NELLA PR #M» (la pull request aperta dal task dopo la preparazione, riconosciuta dal ramo di base, dal nome del ramo preparato o dal numero della pull request), «POSSIBILE CONSEGNA NELLA PR #M» (aperta dopo la preparazione con il solo titolo della richiesta, che può coincidere per caso, o da un ramo `codex/…` senza altri segni: si riconosce guardandola) oppure «HA FATTO PUSH» se il lavoro arriva direttamente sul ramo. Claude controlla il risultato (immagini rese e guardate, controlli del repository, niente dati inventati né riferimenti allo strumento); se non va bene **continua direttamente** sul ramo e corregge o rifà, senza rimandare indietro (ogni giro costa crediti): per correggere il lavoro arrivato in una pull request di consegna, prima lo porta nel ramo con `passa-a.py chiudi --pr N --consegna M --senza-merge`, che non unisce, lascia la pull request in bozza e la voce in «Richieste», aggiorna la copia locale del ramo e stampa i passi per correggere. Poi `passa-a.py chiudi --pr N --consegna M`: porta il lavoro della pull request #M nel ramo preparato e la chiude come assorbita con un titolo neutro; riscrive a nome di Alessandro i commit con un altro autore e toglie i trailer; porta nel ramo le novità di `main` con un commit di merge (mai rebase; un conflitto ferma lo script e si risolve a mano); sposta la voce di bacheca in «Archiviati» con la riga di esito; segna la pull request pronta, aspetta i controlli verdi, unisce (squash con messaggio scritto, un merge per volta), toglie dalle due pull request gli eventuali commenti dello strumento (i rapporti di `github-actions[bot]` restano; dalle sessioni cloud, dove il canale di GitHub non lascia cancellare, commenti e ramo li toglie il workflow `rimuovi-firma-strumento.yml` alla chiusura della pull request) e, dove il repository ha `deploy.yml`, aspetta che il deploy del merge finisca bene: un deploy fallito ferma lo script, perché il sito non è aggiornato. Se la sessione è finita, chiude la routine giornaliera. Se dopo un giorno dalla preparazione non è arrivato nulla, Claude chiede ad Alessandro se l'ha avviata o se manca solo «Create PR»; se l'ha avviata e Codex non ha consegnato, o se ha risposto che i crediti sono finiti, Claude fa il lavoro da sola e lo scrive in bacheca.

**Ambienti cloud.** Gli ambienti di Codex Cloud (chatgpt.com/codex/cloud/settings/environments: uno per repository, creati e pubblicati da Alessandro dal PC, visibili «Solo io», l'unica scelta che l'account personale offre) esistono per tutti e cinque i repository dal 13/10/2026: Codex Cloud ci lavora dentro. Non serve altro; `passa-a.py stato` segnala comunque come «CANALE AUTOMATICO MUTO» la risposta «create an environment», se arriva a un commento di avvio.

**Che cosa contiene la richiesta, sempre.** ChatGPT lavora bene solo con istruzioni esatte, e in Codex Cloud non può fare domande: tutto ciò che gli serve sta nella richiesta, verificato prima da Claude. Sette parti, nell'ordine (`passa-a.py modello` le stampa): (1) **obiettivo** in una frase, e a che cosa serve; (2) **file** da creare o modificare, con il percorso esatto; (3) **che cosa fare**, passo per passo, con i dati già verificati (numeri, nomi, date, misure, testi): niente da cercare, niente da indovinare; (4) **vincoli** del repository che valgono per quel lavoro (regole, licenze, misure, accessibilità, niente riferimenti allo strumento nei file e nei commit); (5) **controlli** da eseguire prima di consegnare, con i comandi esatti; (6) **consegna**: solo le modifiche ai file del punto 2, messaggi di commit in italiano senza nomi di strumenti, un riassunto finale con fatto / non fatto / perché, `COORDINAMENTO.md` non si tocca; (7) **che cosa non fare**: non unire, non segnare pronta nessuna pull request, non toccare altri file, non inventare dati mancanti. Una richiesta a cui manca una parte non si manda.

**Quando si passa un lavoro a ChatGPT.** Lo decide Claude caso per caso, con parsimonia: il piano ChatGPT ha crediti a consumo e ogni passaggio li usa (li usa anche la revisione automatica che Codex fa sulle pull request non in bozza, quindi la pull request preparata resta in bozza finché il lavoro non è finito, e più lavori piccoli si mettono in una richiesta sola). Si passa un lavoro quando:

- **serve andare live prima su più fronti**, soprattutto in emergenza o quando lo stesso contenuto esce su più siti: Claude tiene per sé la parte che richiede i gate editoriali e la comunicazione di allerta ed emergenza, e passa a ChatGPT le parti autonome che si possono specificare per iscritto (script e dati, controlli, audit, materiali di supporto, adattamenti di cose già fatte), così lavorano in parallelo invece che in fila;
- **è un lavoro che ChatGPT sa fare bene e che non ha bisogno del giudizio della sessione**: l'aggiornamento degli interventi dall'export del gestionale, gli audit del sito, i controlli ripetitivi;
- **una sessione finisce con un lavoro urgente a metà** (emergenza, uscita programmata entro un giorno, Alessandro ha chiesto di andare live): oltre alla consegna in «Lavori in corso», Claude passa il ramo a ChatGPT con lo stesso meccanismo. Se non è urgente, scrive solo la consegna.

Se un lavoro non si può passare (sotto, «Che cosa non si passa»), o non si può fare in Codex Cloud (sotto, «Immagini»), lo fa Claude, se serve con più agenti in parallelo (regola `.claude/rules/autonomia.md`, uguale in tutti i repository: autonomia, lavoro diviso, agenti e skill creati quando servono, domande ad Alessandro nei dubbi).

**Immagini.** Le illustrazioni **SVG** le fa Claude (istruzione di Alessandro del 13/10/2026): sono codice, le rende e le guarda prima di pubblicarle; le passa a ChatGPT solo per lavorare in parallelo, con la richiesta completa (misure, contenuto riquadro per riquadro, testi, vincoli). Le **immagini raster** (foto, locandine, grafiche PNG o JPG) non si passano a ChatGPT, perché Codex non ha il generatore di immagini: le fa Claude con i propri strumenti — i generatori del repository (cover, immagini social, fascia blu), gli SVG resi in PNG, i connettori grafici disponibili nella sessione quando ci sono, le foto con licenza libera — e le controlla prima del commit come ogni immagine. Se un'immagine non si può fare in nessuno di questi modi, Claude sceglie l'alternativa migliore (per esempio un'illustrazione al posto di una foto) e lo scrive nella pull request. Nessun passaggio a mano per Alessandro.

**Che cosa non si passa.** Allerte ed emergenze vere, articoli nuovi che devono passare dai gate editoriali, pagine legali, lavori che richiedono credenziali, spese o invii a persone: restano a Claude o ad Alessandro, come in «Quando ChatGPT non unisce e si ferma».

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

### Passaggi a ChatGPT in questo repository

- Li prepara Claude con `python3 scripts/passa-a.py nuovo` (ramo `chatgpt/…`, voce in bacheca, PR in bozza, testo di avvio con la richiesta intera); li avvia Alessandro in Codex Cloud incollando il testo di avvio e, a lavoro finito, premendo «Create PR» nel task (i soli due gesti a mano); li controlla Claude con `passa-a.py stato` e li chiude con `passa-a.py chiudi --pr N --consegna M` (pull request di consegna portata nel ramo e chiusa con titolo neutro, commit riscritti a nome di Alessandro se serve, voce di bacheca archiviata con l'esito, PR pronta, controlli verdi, squash merge). Dettagli e criteri nel protocollo comune, § «Passaggio a ChatGPT».
- Titolo e descrizione della PR descrivono il lavoro senza nomi di strumenti (lo script si rifiuta di aprirla se ne trova uno); la richiesta per esteso sta in questa bacheca e nel testo di avvio. Codex non tocca la bacheca: l'esito lo scrive `chiudi`. Il commento `@codex …` resta solo per riprovare il canale automatico (`nuovo --con-codex`, `riavvia --con-codex`): `chiudi` lo toglie insieme alle risposte dello strumento. Le revisioni automatiche di Codex sulle PR pronte restano visibili (una revisione del bot non si può cancellare, a differenza dei commenti): dipendono da un'impostazione di Codex che solo Alessandro può cambiare, e per ora ha scelto di lasciarle (13/10/2026).
- Se la sessione che ha preparato il passaggio non lo chiude, lo chiude la routine giornaliera delle issue (14:00 italiane, rule 10 § «Lavorazione autonoma delle issue automatiche»).

### Quando qui ChatGPT non unisce

- Articoli che raccontano interventi o attività del Gruppo presi dalla stampa o da fonti non nostre: PR pronta ma **non unita**, perché i fatti vanno confrontati con il registro interventi (rule 10, punto 5-bis).
- Allerte ed emergenze vere (`data/allerta.json`, `data/emergenza.json`, articoli `Allerta`/`Emergenza`): solo su istruzione esplicita di Alessandro.
- Pagine legali (privacy, accessibilità, note legali): PR pronta, unisce Alessandro.

### Chi fa che cosa

Indicazioni dell'utente dell'8 ottobre 2026.

- **Illustrazioni SVG (Claude, dal 13/10/2026).** Le fa Claude (istruzione di Alessandro: «tu sei bravo a fare le immagini SVG»): le rende e le guarda a 1200 px e, per le versioni `-mobile.svg`, a 720 px, con `python3 scripts/check-illustrazioni-udl.py` verde. A ChatGPT solo in parallelo, quando serve andare live prima (protocollo comune, § «Passaggio a ChatGPT»): in quel caso arrivano su un ramo `chatgpt/…` con una PR, e Claude le guarda prima di unire. Fino al 12/10/2026 le faceva di solito ChatGPT, che le rendeva, le controllava e univa da sé a controlli verdi.
- **Immagini raster (Claude).** Foto, locandine e grafiche PNG o JPG non si passano a ChatGPT (Codex non genera immagini): le fa Claude con gli strumenti del repository (`genera-cover.py`, `genera-immagini-social.py`, `applica-fascia-foto.sh`, gli SVG resi in PNG), con i connettori grafici della sessione quando ci sono, con le foto a licenza libera (`pc-image-fixer`); prima del commit valgono i controlli di rule 03 § «Illustrazioni fatte con strumenti esterni» (Read dell'immagine, gesti coerenti col DPC, `alt` e didascalia su ciò che si vede, nessun riferimento allo strumento) e la regola dei 4 loghi con il codice E10435833 dove vale. Nessun passaggio a mano per Alessandro.
- **Audit del sito (di solito ChatGPT).** Chi fa l'audit **non corregge**: scrive i rilievi in `riferimenti-interni/audit-esterni/AAAA-MM-GG-<argomento>.md` (formato nel README della cartella) e lascia un avviso qui. L'altra sessione verifica ogni rilievo, corregge quelli fondati con una PR e scrive l'esito accanto a ciascuno (corretto nella PR #N, non riprodotto, già a posto). Così l'utente non deve più copiare l'audit da una chat all'altra. Se Claude non è disponibile e Alessandro chiede a ChatGPT di correggere, ChatGPT verifica e corregge i rilievi fondati con una PR, seguendo il protocollo comune.
- **Pubblicazioni urgenti quando l'altra sessione non c'è.** Si pubblica con una PR e i controlli verdi; direttamente su `main` solo se l'utente lo chiede espressamente. In entrambi i casi un avviso qui: «pubblicato in urgenza: file …, motivo …, PR o commit …». Alla prima sessione utile l'altra lo ripassa e archivia l'avviso con l'esito.

## Domande

Domande fra le sessioni (o per Alessandro). Chi la legge risponde accanto, alla prima apertura della bacheca, e sposta la voce in «Archiviati» quando la risposta è applicata.

- Nessuna domanda aperta.

## Lavori in corso

Consegne di fine sessione: che cosa resta a metà, su quale ramo, in quale PR.


## Richieste

Lavori che una sessione (o Alessandro) chiede all'altra. Dal 13/10/2026 i passaggi a ChatGPT li prepara Claude da sola (protocollo comune, § «Passaggio a ChatGPT»: voce qui sotto con la nota «preparata da Claude, da avviare a mano in Codex Cloud» e PR in bozza) e li avvia Alessandro in Codex Cloud con il testo di avvio; per le richieste a Gemini, e per quelle che Alessandro scrive qui a mano, resta l'avviso «guarda la bacheca». Formato nel protocollo comune.

- **2026-10-16 — da Claude a ChatGPT — Appunti illustrati: modelli di pagina e tre pagine di prova** (preparata da Claude, da avviare a mano in Codex Cloud; PR #1439; ramo `chatgpt/appunti-illustrati-20261016`)
  - **Avvio a mano (Alessandro).** In Codex Cloud: ambiente del repository, ramo `chatgpt/appunti-illustrati-20261016` se il selettore lo offre, poi il testo di avvio (intestazione più le sette parti qui sotto: lo stampa `passa-a.py nuovo`, lo ristampa `passa-a.py riavvia --pr 1439`). A lavoro finito, «Create PR» dal task: la pull request di consegna la porta nel ramo e la chiude `passa-a.py chiudi --pr 1439 --consegna M`.
  - **1. Obiettivo.**
    Costruire il modello degli «Appunti illustrati di protezione civile» (proposta 93): schede A4 di ripasso, una per argomento, che riprendono lo schema di pagina di due libri di appunti illustrati per le superiori. Insieme al modello, le prime tre pagine di prova per la secondaria di secondo grado: «Il terremoto» (pagina-concetto), «Come si chiama il 112» (pagina-procedura) e «Come si legge l'allerta» (pagina-procedura). Le tre pagine servono ad Alessandro per approvare l'aspetto prima dei circa 27 argomenti che seguiranno con lo stesso generatore.
  - **2. File.**
    Da creare:
    - `data/appunti_illustrati.json` — testi e struttura delle tre pagine
    - `scripts/genera-appunti-illustrati.py` — generatore, solo libreria standard di Python
    - `static/formazione/schede-stampabili/assets/appunti.css` — stile comune delle pagine
    - `static/formazione/schede-stampabili/appunti-terremoto-secondaria2/index.html` (generato) e `disegno-apertura.svg`
    - `static/formazione/schede-stampabili/appunti-chiamata-112-secondaria2/index.html` (generato) e `disegno-apertura.svg`
    - `static/formazione/schede-stampabili/appunti-leggere-allerta-secondaria2/index.html` (generato) e `disegno-apertura.svg`

    Da modificare:
    - `static/formazione/schede-stampabili/index.html` — tre schede nella sezione della secondaria di secondo grado
    - `content/formazione/kit-scuola-secondaria-secondo-grado.md` — tre voci nel blocco «Schede già pronte per la stampa»
    - `static/formazione/schede-stampabili/pacchetti/*.html` e `data/materiali_lezione.json` — solo come li riscrivono `scripts/genera-pacchetti-schede.py` e `scripts/genera-materiali-lezione.py`
    - `.github/workflows/validate-pr.yml` — un passo nel job `pacchetti-schede`

    Nessun altro file. Nessun file binario (ZIP, PNG, PDF): lo ZIP del kit lo rigenera chi chiude il lavoro.
  - **3. Che cosa fare.**
    1. Leggi prima le regole del repository (cartella `rules/` della configurazione nascosta, trovale con `find . -name '09-regole-contenuti-qualita.md'`): `09-regole-contenuti-qualita.md` § 15-ter (come si fanno le schede stampabili e perché la stampa si rompe), `03-accessibility.md` § «Progettazione universale per l'apprendimento», `02-content-design-pa.md` § «Umanizzazione della scrittura», e la lista di controllo `pc-didattica-reviewer.md` (cartella `agents/` accanto a `rules/`). Modello tecnico: `static/formazione/schede-stampabili/caso-amatrice-secondaria2/index.html` (intestazione, `scheda-print.css`, barra `.scheda-toolbar`, `<article class="scheda-page">`, `.scheda-footer`, URL canonico) e `static/formazione/schede-stampabili/assets/scheda-print.css` (variabili di colore, classe `.soluzione-capovolta`, banda delle affiliazioni aggiunta in stampa).

    2. Due modelli di pagina, ciascuno su un solo foglio A4. Dei due libri si riprende lo schema della pagina; etichette, testi e disegni sono nostri.

       **Pagina-concetto** (per rischi, storia, organizzazione; modello «quaderno di appunti a colori»):
       - testata: etichetta «Appunti illustrati · Protezione civile · Secondaria di II grado», titolo in lettering (punto 3) e, sotto, la **domanda guida** a cui la pagina risponde;
       - **disegno d'apertura** accanto alla testata;
       - **In breve**: 3 frasi;
       - **La sequenza**: 4-5 passaggi numerati, ognuno con una piccola icona e una riga di testo;
       - **Cause e conseguenze**: 2-3 coppie unite da una freccia disegnata;
       - **Chi fa cosa**: 4-5 ruoli (enti e cittadino, mai persone con nome), un compito per riga, con una piccola icona;
       - **Punto chiave**: la frase da ricordare, in un riquadro;
       - **Occhio all'errore**: 2 idee sbagliate corrette, prese dalla Biblioteca delle idee sbagliate, con il link alla voce;
       - **Parole chiave**: 4-5 termini evidenziati, con la definizione breve del glossario del sito;
       - **Per l'interrogazione**: 3 domande;
       - **Controlla a casa**: 3 caselle da spuntare;
       - piede: fonti (le pagine del sito usate), capitolo del Manuale e pagina del rischio per approfondire, «Testi e disegni: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma, licenza CC BY 4.0», `.scheda-footer` come nelle altre schede.

       **Pagina-procedura** (per le cose da saper fare; modello «appunti illustrati di matematica»):
       - testata come sopra, con titolo in lettering e 1-2 **note adesive** (foglietti leggermente ruotati) che portano il concetto chiave in due-tre parole;
       - **La teoria**: 4-5 punti con le parole importanti evidenziate in tre colori secondo una legenda fissa, scritta in piccolo nel riquadro (giallo = azioni, azzurro = numeri e luoghi, rosa = attenzione);
       - **Le regole**: riquadro con 2-4 regole;
       - **Esempio guidato**: il caso di partenza, poi 3-4 passi numerati, ognuno con una riga di spiegazione e una riga in riquadro (che cosa si dice o si fa);
       - **Lo schema**: 4 pastiglie colorate unite da frecce, dal primo all'ultimo gesto;
       - **Occhio all'errore**: riquadro rosa con triangolo di avvertimento, 1-2 errori tipici con la correzione;
       - **Prova tu**: un caso nuovo, con **Indizio** (icona della lampadina) e **Soluzione** stampata capovolta in fondo con la classe `.soluzione-capovolta`;
       - piede come nella pagina-concetto.

       In entrambi i modelli ogni riquadro ha bordo tratteggiato e una **linguetta** colorata in alto a sinistra con il nome del riquadro, come le schede di un raccoglitore.

    3. Aspetto e lettering. Direzione: «quaderno di appunti a colori fatto a mano»: carta chiara, righe o quadretti leggerissimi sullo sfondo dei riquadri, evidenziatori, frecce e cerchi disegnati.
       - Titolo in lettering con il carattere a mano `edu-cursive` (file `static/formazione/schede-stampabili/assets/edu-cursive-400.woff2`, licenza OFL in `OFL-edu-cursive.txt`, da dichiarare con `@font-face` in `appunti.css`): grande (30-34 pt in stampa), colore pieno con un'ombra spostata in un secondo colore e una sottolineatura a pennello disegnata in SVG sotto la parola principale; al massimo due colori per titolo.
       - Il carattere a mano solo per titoli, linguette, note adesive e domanda guida. Il testo continuo resta nel carattere di `scheda-print.css`, almeno 9,5 pt in stampa.
       - Colori: le variabili di `scheda-print.css` (`--scheda-blu`, `--scheda-oro`, `--scheda-verde`, `--scheda-rosso`) e i tre evidenziatori; ogni testo con contrasto almeno 4,5:1 sul suo fondo, calcolato.
       - Leggibile anche stampata in bianco e nero: le parole evidenziate sono anche in grassetto, i riquadri si riconoscono da linguetta e bordo, nessuna informazione affidata al solo colore.
       - Icone, frecce e sottolineature: SVG in linea scritti a mano, semplici, con `aria-hidden="true"` quando sono decorativi.
       - Niente pittogrammi ARASAAC (cambierebbero la licenza), niente foto, niente emoji.
       - Tutto lo stile comune sta in `appunti.css`, caricato dopo `scheda-print.css`; niente stili in linea nelle pagine.

    4. Generatore `scripts/genera-appunti-illustrati.py`, con due righe di spiegazione in testa. Legge `data/appunti_illustrati.json` (un elenco di pagine, ognuna con `slug`, `modello` = `concetto` o `procedura`, titolo, domanda guida, disegno con percorso e testo alternativo, i campi dei riquadri del suo modello, `fonti`, `manuale`, `approfondisci`) e scrive `static/formazione/schede-stampabili/appunti-<slug>-secondaria2/index.html`. Escape HTML di tutti i testi, output identico a ogni esecuzione. Con `--check` non scrive nulla ed esce con errore se un file generato è diverso da quello sul disco. In `.github/workflows/validate-pr.yml`, job `pacchetti-schede`, aggiungi dopo il passo dei pacchetti un passo «📒 Appunti illustrati allineati ai dati» che esegue `python3 scripts/genera-appunti-illustrati.py --check`.

    5. Contenuti: solo fatti scritti in queste pagine del sito, già verificate. Se un fatto non c'è, non scriverlo e dillo nel riassunto. Registro per ragazzi di 14-19 anni: frasi brevi e concrete, mai la paura come leva.
       - **Il terremoto** (pagina-concetto): `content/rischi-prevenzione/rischio-sismico.md`, `content/manuale/711-rischio-sismico.md`, `content/rischi-prevenzione/idee-sbagliate.md` (voci `#correre-fuori`, `#ascensore`, `#tornare-in-casa`, `#prevedere-terremoti`), glossario `data/glossario.yaml` (`magnitudo`, `intensita-sismica`, `epicentro`, `ipocentro`, `area-attesa`, `ingv`). La sequenza riprende che cosa fare prima, durante e dopo la scossa come lo scrive la pagina del rischio sismico, con icone di oggetti (tavolo, scala, porta, area di attesa), senza figure umane.
       - **Come si chiama il 112** (pagina-procedura): `content/comunicazioni/2026-10-08-segnalare-emergenze-112-come-fare.md`, `content/comunicazioni/2026-02-11-giornata-europea-112-numero-unico.md`, `content/numeri-utili/_index.md`, `static/formazione/schede-stampabili/chiamo-112-secondaria2/index.html`, idee sbagliate `#numero-unico` e `#chiamare-gruppo`, glossario `nue`, `where-are-u`, `sala-operativa-lazio`. Esempio guidato e Prova tu: due situazioni diverse e concrete (per esempio un malore in casa e un fuoco di sterpaglie visto dalla strada), senza indirizzi reali; se servono personaggi, si chiamano Flavio, Silvia o Marco.
       - **Come si legge l'allerta** (pagina-procedura): `content/allerte-meteo/_index.md`, `content/allerte-meteo/cosa-significa-a-genzano.md`, `data/codici_colore.yaml`, `content/manuale/714-rischio-meteo-idrologico.md`, idee sbagliate `#allerta-gialla` e `#allerta-tutti`, glossario `allerta`, `allertamento`, `bollettino-criticita`, `cfr`, `zona-allerta`, `coc`. Esempio guidato: l'allerta gialla del 10-11 settembre 2026 come la riporta `data/registro_prevenzione.yaml` (solo zona, tipo e date scritti lì). Prova tu: un caso dichiarato come esempio, con la scritta «Esempio per esercitarsi, non è un bollettino vero». Lo schema: trova la zona → leggi il colore → guarda il tipo di rischio → controlla quando vale.
       - Dati che restano identici alle fonti: nel Lazio l'unico numero per qualsiasi emergenza è il 112 (mai 115, 118 o 1515 come numeri da chiamare); le segnalazioni non urgenti vanno alla Sala Operativa della Protezione Civile del Lazio, 803 555; il Gruppo Comunale non si attiva chiamandolo direttamente; i codici colore con le parole esatte di `data/codici_colore.yaml` (verde: nessuna allerta; giallo: criticità ordinaria; arancione: criticità moderata; rosso: criticità elevata); Genzano di Roma è nella zona di allerta F «Bacini Costieri Sud».

    6. Disegni d'apertura, uno per pagina, SVG scritti a mano nella cartella della scheda (`disegno-apertura.svg`). Pensati per stare larghi circa 9 cm sul foglio: `viewBox` di circa 600×360, al massimo 6 scritte, ciascuna di almeno 22 unità e tutta dentro il `viewBox`; `role="img"` con `<title>` e `<desc>` in italiano su ciò che si vede; nessun logo, nessun metadato. Nella pagina, `alt` uguale nel senso a `<desc>`.
       - Terremoto: sezione del terreno con la faglia, l'ipocentro in profondità, l'epicentro in superficie proprio sopra e le onde che arrivano a una casa; scritte «ipocentro», «epicentro», «faglia», «onde sismiche», coerenti con le definizioni del glossario.
       - 112: un telefono con il 112 sullo schermo e attorno le quattro cose da dire (chi sei, che cosa succede, dove, quante persone), come nell'articolo dell'8 ottobre.
       - Allerta: la scala dei quattro colori, con accanto a ogni colore la parola del livello.

    7. Indice e kit. Nella sezione della secondaria di secondo grado di `static/formazione/schede-stampabili/index.html` aggiungi tre `scheda-card` come quelle vicine (`scheda-card-icon secondaria2`, fascia «Secondaria II · 14-19 anni · appunti», meta «1 foglio · ripasso», descrizione di una riga, pulsante «Apri e stampa»). In `content/formazione/kit-scuola-secondaria-secondo-grado.md`, blocco «Schede già pronte per la stampa», tre voci nello stesso formato delle altre. Poi rigenera con gli script, mai a mano: `python3 scripts/genera-appunti-illustrati.py`, `python3 scripts/genera-pacchetti-schede.py`, `python3 scripts/genera-materiali-lezione.py`.
  - **4. Vincoli.**
    - Un argomento, un foglio A4: l'area stampabile è alta 28,7 cm (margini di `@page` in `scheda-print.css`); `.scheda-page` è un contenitore flex, quindi niente `float`; in fondo `scheda-print.css` aggiunge la banda delle affiliazioni, a cui va lasciato spazio. Se il contenuto non entra si accorciano i testi, non si scende sotto i 9,5 pt.
    - Accessibilità WCAG 2.2 AA: `lang="it"`, un solo h1, un h2 per ogni riquadro, `alt` su ogni immagine, elenchi veri per passaggi e caselle, ordine di lettura uguale a quello visivo; a schermo la pagina si legge anche da telefono (riquadri in colonna sotto i 700 px). La soluzione capovolta viene dopo il testo del Prova tu anche nell'ordine di lettura.
    - Italiano corretto, frasi sotto le 20 parole, voce attiva, niente tic da testo scritto in automatico (rule 02 § «Umanizzazione»).
    - Nessun riferimento a strumenti automatici nei file, nei commenti, nei metadati e nei messaggi di commit.
    - Schede senza JavaScript, come le altre; URL canonico `https://www.protezionecivilegenzano.it/formazione/schede-stampabili/<cartella>/`.
    - Nessun dato, luogo, nome o fonte inventati.
  - **5. Controlli.**
    - `python3 scripts/genera-appunti-illustrati.py --check` → nessuna differenza.
    - `python3 scripts/genera-materiali-lezione.py --check` → nessun errore.
    - `python3 scripts/aggiungi-canonical-statiche.py --check` → nessun errore.
    - `python3 scripts/check-parita-schede.py` → nessun errore, salvo la parità con lo ZIP della secondaria di secondo grado (lo ZIP lo rigenera chi chiude): riporta nel riassunto i messaggi che restano.
    - `python3 -c "import sys, xml.dom.minidom as m; [m.parse(f) for f in sys.argv[1:]]" static/formazione/schede-stampabili/appunti-*/disegno-apertura.svg` → nessun errore.
    - `git status --short` → solo i file del punto 2.
    - Se `hugo` è installato: `hugo --minify --quiet`, poi `python3 scripts/check-qualita-pagine.py public` e `python3 scripts/check-ancore.py public --base-path ""` → nessun errore.
    - Se c'è un browser Chromium: `python3 scripts/check-fogli-stampa.py --da-git origin/main` → ogni pagina su un solo foglio.
    - Un controllo che nell'ambiente non si può eseguire si scrive nel riassunto: lo esegue chi chiude.
  - **6. Consegna.**
    Solo le modifiche ai file del punto 2, con messaggi di commit in italiano e senza nomi di strumenti (per esempio «Appunti illustrati: modelli di pagina e tre pagine di prova»). Alla fine un riassunto breve: fatto, non fatto e perché, fatti non trovati nelle fonti, controlli non eseguiti. `COORDINAMENTO.md` non si tocca.
  - **7. Che cosa non fare.**
    Non unire nulla e non segnare pronta nessuna pull request. Non toccare file fuori dall'elenco del punto 2, non creare file binari, non scrivere gli altri argomenti, non inventare fatti, numeri, nomi o fonti: se manca qualcosa, scrivilo nel riassunto finale.

    Nota per chi chiude (istruzione di Alessandro del 16/10/2026): nulla va online senza il suo ok. La consegna si porta nel ramo con `chiudi --senza-merge`, si rigenera lo ZIP del kit, si fanno i controlli, si mandano ad Alessandro le tre pagine in PDF e si unisce solo dopo il suo «pubblica».

- **2026-10-11 — da Claude a ChatGPT — Procedura ricorrente: aggiornamento degli interventi dall'export del gestionale** (richiesta permanente: non si archivia, vale ogni volta che Alessandro manda il file)
  - **Quando**: Alessandro ti manda l'export del gestionale interventi (file `.xlsx`, di solito `gcpc-genzano-di-roma_global_reports_*.xlsx`) e scrive «aggiorna gli interventi» o simile. Lavora con **Codex** (serve eseguire gli script): il file va allegato al task.
  - **Mai nel repository il file `.xlsx`**: contiene i nomi dei volontari. Tienilo fuori dalla cartella del repository (per esempio `/tmp/`) e non fare `git add -A` senza guardare.
  - **1. Cumulativo o parziale?** Guarda la prima data dell'export e confrontala con `periodo.dal` di `static/open-data/statistiche-interventi.json` (oggi `2026-04-04`; ultimo intervento pubblicato `periodo.ultimo_numero`, oggi `178/2026` del `2026-10-06`).
    - prima data uguale o precedente **e** l'export contiene almeno l'intervento `periodo.ultimo_numero` (o numeri successivi), senza buchi nella numerazione → **cumulativo**: `python3 scripts/genera-open-data-interventi.py /tmp/<file>.xlsx`
    - prima data uguale o precedente ma l'export si ferma prima di `periodo.ultimo_numero` → è un export vecchio o incompleto: **fermati e chiedi ad Alessandro** un export più recente; non lanciare nessuno script, cancellerebbe gli interventi successivi.
    - prima data successiva → **parziale**: prima `python3 scripts/aggiorna-open-data-delta.py /tmp/<file>.xlsx --dry-run`, poi senza `--dry-run`. Mai il generatore su un export parziale: cancellerebbe i mesi precedenti.
    - Serve `pip install openpyxl`. Se lo script delta si ferma chiedendo `--volontari-nuovi N`: **fermati e chiedi ad Alessandro** quante persone sono nuove nel Gruppo; non stimare.
    - Se uno dei due script si ferma con «Data di inizio non leggibile negli interventi …», **fermati e chiedi ad Alessandro** di correggere quegli interventi nel gestionale e di riesportare. Se il delta si ferma perché `data/open_data_interventi.json` non si legge o non conta gli stessi interventi dei dataset, serve un export **cumulativo**: chiedilo ad Alessandro. In tutti e due i casi gli script non hanno scritto nessun file (dal 16/10/2026 controllano tutto prima di scrivere, anche con `--dry-run`).
  - **1-bis. Interventi in Bozza e numeri mancanti** (regola di Alessandro dell'11/10/2026): gli interventi con stato **Bozza** non si pubblicano mai, perché possono ancora cambiare. Lavora su una copia del file senza quelle righe: se la bozza è l'ultimo numero, l'ultimo pubblicato resta il precedente e la bozza entra col prossimo export, una volta chiusa; se la bozza sta in mezzo a interventi chiusi, **fermati e chiedi**, perché il prossimo aggiornamento la salterebbe. Se nella numerazione manca un numero, chiedi ad Alessandro se è stato annullato prima di procedere. Nella copia riallinea anche gli aggregati dei volontari: il foglio «Interventi membri» può includere le presenze delle bozze, che vanno escluse dai conteggi pubblicati. Le bozze non entrano nemmeno negli articoli, nelle cover e nelle sintesi social.
  - **2. Controlla l'esito**: i file cambiati devono essere solo in `static/open-data/` (statistiche, tipologie, automezzi, volontari; CSV e JSON) e `data/open_data_interventi.json` (i dati dei grafici interattivi della pagina Open data, dal 15/10/2026: per giorno solo numero di interventi e ore, per mese tipologie, ore di inizio e mezzi). Nessun nome, nessun indirizzo, nessun richiedente nei file: se ne vedi uno, fermati.
  - **3. Articoli**: per ogni **giornata di intervento non ancora raccontata** sul sito (cerca in `content/comunicazioni/` per data e argomento; non duplicare quelle già coperte, per esempio il 05/10 e il 06/10 hanno già un articolo), scrivi un articolo `content/comunicazioni/AAAA-MM-GG-<slug>.md` **retrodatato** alla data dell'intervento, con badge `Attività` (o `Aggiornamento` per un maltempo concluso). Regole: `AGENTS.md` § 3.4, § 3.5 e § 5.1; **orari arrotondati** («verso le 18»), **niente nomi, targhe, indirizzi privati o richiedenti**; vie e quartieri solo se servono a capire; il nome dei mezzi preso da `content/chi-siamo/_index.md` § «Mezzi e attrezzature principali»; se usi la stampa locale, solo fatti parafrasati e testate in fondo («Per approfondire»). Cover: `python3 scripts/genera-cover.py <file>` e poi `image:`/`image_alt:`. Interventi piccoli e simili della stessa giornata in un solo articolo; giornate senza nulla di raccontabile (solo servizi interni) si saltano e lo scrivi nella PR. Per ogni giornata raccontata aggiungi in `data/racconti_interventi.json` la riga `"AAAA-MM-GG": ["comunicazioni/<slug>"]` (in ordine di data; più articoli sulla stessa giornata in una lista): il calendario della pagina Open data mostra così il link all'articolo. Solo se l'articolo racconta gli interventi di quel giorno, non se lo cita di passaggio. Il generatore elenca alla fine le giornate ancora senza racconto. Se nella stessa giornata esistono già altri articoli, usa il formato data con l'orario (`AGENTS.md` § 5.1): guarda gli orari già usati quel giorno e prendi il **primo minuto libero dopo il più alto** (se il 08/10 ha 00:01, 00:02 e 00:03, il nuovo va a `T00:04:00+02:00`); se l'articolo esistente ha la data semplice, portalo a `T00:01:00+02:00` e il nuovo a `T00:02:00+02:00`. Mai due articoli con lo stesso orario nello stesso giorno.
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

- **16/10/2026 — Claude, ramo `claude/correzioni-grafici-aprilia`.** Correzioni dopo la PR #1428: (1) gli script degli open data interventi calcolano e controllano tutto prima di scrivere, anche con `--dry-run`, e si fermano su date illeggibili o conti che non tornano (punto 1 della procedura qui sopra); (2) nei grafici, scegliendo un mese il giorno selezionato passa dentro quel mese e su telefono il mese entra in vista; (3) «Pausa animazioni» del pannello mette su `<html>` sia `a11y-pause-animations` sia `a11y-pause-anim`: nessuna delle due va rinominata nell'altra (rule 03); (4) l'incendio di Aprilia raccontato nell'articolo del 23 giugno è di domenica 21 giugno (registro, intervento 33/2026): corretti articolo, testi social e collegamento nei due calendari.
- **16/10/2026 — Claude, ramo `claude/open-data-grafici-interattivi`.** Grafici interattivi nella pagina Open data, con le stesse funzioni di quelli del bilancio antincendio (PR #1427): `scripts/genera-open-data-interventi.py` e `scripts/aggiorna-open-data-delta.py` scrivono anche `data/open_data_interventi.json`, con per ogni giorno solo il numero di interventi e le ore, e tipologie, ore di inizio e mezzi solo per mese. Lo shortcode `grafico-interattivo` ora accetta i valori per mese (`per_mese`), le parole del periodo intero (`testi`) e i racconti presi da un altro file: quelli dei giorni stanno in `data/racconti_interventi.json`, curato a mano (punto 3 della procedura qui sopra). Toccati anche `grafico-interattivo.js`, la pagina `/open-data/`, il promemoria `promemoria-export-interventi.yml`, rule 04a e 10, manuale parte 29 e l'agente `pc-dati-e-feed`. Il prossimo aggiornamento degli interventi rigenera i grafici da solo: a mano restano solo le righe dei racconti.
- **15/10/2026 — Claude, ramo `claude/manuali-agid-controllo-settimanale`.** Il controllo settimanale `aggiorna-manuale.yml` era cieco sulle regole di scrittura dal 4 maggio: le pagine di Writing Toolkit, Content Toolkit, UI Kit e Linee guida AGID non si scaricavano più e il workflow lo ignorava. Ora il testo dei manuali (Fondamenti del design system, Guida alle parole della PA, Linee guida di design, Manuale operativo di design) si legge dai repository ufficiali su GitHub con `scripts/manuali-agid.py`, la copia aggiornata sta in `.manuale/manuali-agid/` e l'issue di revisione riporta le righe cambiate; le fonti che non si leggono vanno nell'issue «⚠️ Fonti del manuale operativo non raggiungibili», che si chiude da sola. Per sapere che cosa dicono oggi i manuali AgID, leggere `.manuale/manuali-agid/` (non modificarla a mano). Correzioni dello stesso giorno (ramo `claude/manuali-agid-correzioni`): nel repository lo script usa da solo quella copia (`python3 scripts/manuali-agid.py testo content/…` controlla una pagina senza `--manuali`), scrive le ore in ora italiana anche su GitHub, e l'issue delle fonti si chiude solo dopo un controllo arrivato in fondo.
- **14/10/2026 — Claude, ramo `claude/mappe-laboratorio-e-social`.** Dati climatici di Genzano rifatti su una serie omogenea: `scripts/genera-clima-castelli.py` e il Laboratorio meteo chiedono sempre a Open-Meteo `models=era5_seamless` (senza, dal 2017 l'archivio passa al modello IFS e i decenni non si confrontano più). Nuovo dataset `clima-giorni-30-gradi-genzano.json`; i grafici del dossier «Il clima che cambia i rischi» si rigenerano con `scripts/genera-grafici-clima-dossier.py`. Sotto ogni grafico del Laboratorio c'è la spiegazione a parole (gruppo `laboratorio` di `data/mappe_raccontate.yaml`, partial `mappa-raccontata.html` comune con il cruscotto, controllo `check-mappe-raccontate.py`). I social ricevono solo gli articoli aggiunti da un push, non quelli modificati (`genera-social-bozze.yml`). La foto `vento-castelli-locale.webp` è di Barga, in Toscana: non va descritta come dei Castelli.
- **14/10/2026 — Claude, ramo `claude/cinque-proposte-rapide`.** Cinque proposte della roadmap: Settimana della protezione civile a scuola (`/formazione/settimana-protezione-civile/`), Sala stampa (`/sala-stampa/`), Accordo di aiuto fra vicini (scheda stampabile `accordo-vicini`), «Vivo qui da poco» (`/vivo-qui-da-poco/`) e Calendario della prevenzione (`/calendario-prevenzione/`, shortcode `calendario-prevenzione`, dati in `data/calendario_prevenzione.yaml`, file `.ics` generato da `scripts/genera-calendario-prevenzione.py` e controllato da `validate-pr.yml`). Toccati anche mappa del sito, «Da dove comincio», contatti, «Per gli enti», scuole, formazione, percorsi didattici, piano familiare, kit di emergenza, persone con necessità specifiche, indice delle schede, deck di presentazione e i due articoli sull'ora solare (usciranno il 24 e il 25 ottobre, con le date del cambio, gli orari del sole e le regole sulle luci corretti). Il file `.ics` non si modifica a mano: si cambia il YAML e si rigenera.
- **14/10/2026 — Claude.** Protocollo aggiornato in tutti e cinque i repository (§ «Passaggio a ChatGPT» del protocollo comune): il passaggio è «preparato da Claude, avviato da Alessandro, chiuso da Claude», perché il canale `@codex` sulle pull request resta muto per il suo account. `passa-a.py nuovo` non manda più il commento di avvio (resta con `--con-codex`, per riprovare il canale senza spese) e stampa il testo di avvio, con la richiesta intera, da incollare in Codex Cloud; a lavoro finito Alessandro preme «Create PR» nel task; `stato` riconosce la pull request di consegna, `chiudi --consegna M` la porta nel ramo e la chiude, e `chiudi` archivia da sé la voce di bacheca con l'esito. Codex non tocca più la bacheca.
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

- **2026-10-13 — da Claude ad Alessandro — Ambienti Codex per i passaggi automatici.** La prima richiesta automatica (PR #1365) non è partita: il bot ha risposto «To use Codex here, create an environment for this repo». Serve, una volta sola e solo dal tuo account ChatGPT: https://chatgpt.com/codex/cloud/settings/environments → «Create environment» → repository `SviluppoItaliaDigitale/sito-pc-genzano` (impostazioni predefinite), poi lo stesso per `sito-misericordia-ariccia`, `cooprimavera`, `social-pc-genzano` e `assistente-personale`. Fino ad allora i lavori che partirebbero verso ChatGPT li fa Claude da sola, come previsto dal protocollo. Quando è fatto, Claude rilancia la prova e archivia questa voce.
  - **Esito (14/10/2026).** Ambienti creati e pubblicati da Alessandro il 13/10/2026 per tutti e cinque i repository. Il canale `@codex` sulle pull request è rimasto muto (difetto di OpenAI, openai/codex #20093): dal 14/10/2026 i passaggi si avviano a mano in Codex Cloud con il testo di avvio (protocollo comune, § «Passaggio a ChatGPT»).

- **2026-10-13 — da Claude a ChatGPT — Illustrazione del temporale: versione verticale per telefono** (passata in automatico; PR #1365; ramo `chatgpt/illustrazione-temporale-mobile-20261013`) — **fatta, PR #1365**
  - **Esito (14/10/2026).** Unita il 13/10/2026 con la PR #1365: il file l'ha fatto Claude sul ramo preparato, perché il canale automatico non partiva. Voce archiviata il 14/10/2026, con il passaggio al protocollo «preparato da Claude, avviato da Alessandro, chiuso da Claude».
  - **Esito (13/10/2026, Claude).** Codex non ha potuto lavorare: sul repository non esiste ancora un ambiente Codex nell'account ChatGPT di Alessandro (risposta del bot sulla PR: «create an environment for this repo»); finché non viene creato, nessun passaggio automatico parte. Il file l'ha fatto Claude sullo stesso ramo (disegni del sorgente riusati a scala 0,68, resa controllata a 720 px, controlli dello script e build eseguiti) e la PR si chiude con `passa-a.py chiudi`.
  - **1. Obiettivo.**
    Creare la versione verticale per telefono dell'illustrazione didattica «Come un temporale può provocare altri problemi», così che sulla pagina `/rischi-prevenzione/` chi legge da smartphone veda i quattro riquadri impilati, con testi leggibili, invece della tavola orizzontale rimpicciolita.
  - **2. File.**
    - `static/formazione/illustrazioni-udl/temporale-effetti-cascata-mobile.svg` (nuovo; nessun altro file va toccato)
    - Sorgente da cui partire, da non modificare: `static/formazione/illustrazioni-udl/temporale-effetti-cascata.svg`
  - **3. Che cosa fare.**
    1. Aprire il sorgente `temporale-effetti-cascata.svg` (1200×620): contiene quattro riquadri affiancati, ciascuno con una testata colorata, un disegno e una didascalia su due righe, tre frecce fra i riquadri, un titolo in alto e una nota in basso.
    2. Scrivere il nuovo file con `width="720" height="1180" viewBox="0 0 720 1180"`, `role="img"`, `aria-labelledby="tit desc"`, e gli stessi `<title id="tit">` e `<desc id="desc">` del sorgente, parola per parola.
    3. Sfondo: lo stesso rettangolo con gradiente `paper` (`#ffffff` → `#eff5f8`, `rx="24"`) a tutta tela e la stessa fascia blu `#126084` alta 14 px in testa.
    4. Titolo «Come un temporale può provocare altri problemi» in alto, Arial grassetto, dimensione 30, colore `#123957`, su due righe se non sta in 720 px di larghezza (spezzare dopo «temporale»).
    5. I quattro riquadri impilati in colonna, nell'ordine 1 → 4, ciascuno largo 640 px (margine 40 px a sinistra e a destra), con la stessa testata colorata del sorgente (`#17678e`, `#5e6476`, `#9c5b26`, `#087d80`) e gli stessi testi di testata: «1. TEMPORALE», «2. DANNI ALLE LINEE», «3. BLACKOUT», «4. ALTRI EFFETTI». Testata alta 56 px, testo Arial grassetto 24, bianco.
    6. Dentro ogni riquadro, a sinistra, il disegno del sorgente riusato tale e quale: copiare i `<path>`, `<circle>` e `<rect>` del gruppo corrispondente (quelli dentro i `<g transform="translate(… 0)">` che seguono i quattro riquadri), senza ridisegnarli, applicando solo una traslazione e, se serve, una scala 0,85 perché stiano in un'area di circa 230×200 px. A destra del disegno la didascalia del sorgente, su due righe, Arial 24, colore `#123957`, allineata a sinistra: «Pioggia e vento / intensi», «Alberi o infrastrutture / possono danneggiarsi», «Possibile interruzione / della corrente», «Acqua e apparecchi / possono risentirne».
    7. Fra un riquadro e il successivo una freccia verticale verso il basso, stesso tratto del sorgente (`#9aabb5`, spessore 5, estremi arrotondati), centrata orizzontalmente.
    8. In fondo la nota del sorgente, Arial 20, colore `#3b5363`, centrata, su due righe: «Sono conseguenze POSSIBILI, non una catena inevitabile.» / «Prepararsi aiuta a ridurre gli effetti.»
    9. Tutto deve stare dentro il `viewBox`: nessuna scritta tagliata ai bordi, nessun elemento sotto il fondo della tela; testi mai più piccoli di 20 px.
  - **4. Vincoli.**
    - Solo SVG statico: niente `<script>`, niente `<foreignObject>`, niente font esterni né risorse remote (`href` con `http`); font `Arial,sans-serif` come nel sorgente.
    - Nessun logo e nessuna scritta aggiuntiva oltre a quelle elencate; nessun riferimento a strumenti nei commenti, nei metadati e nei messaggi di commit.
    - Stessi colori e stesse parole del sorgente: è la stessa figura in formato verticale, non una figura nuova.
    - Accessibilità: `<title>` e `<desc>` presenti e non vuoti, `role="img"` sulla radice.
    - Identità dei commit: `Alessandro Cuollo <65465537+SviluppoItaliaDigitale@users.noreply.github.com>` (eseguire `bash scripts/imposta-identita-git.sh` prima del commit); messaggio di commit in italiano, per esempio «Illustrazione del temporale: versione verticale per telefono».
  - **5. Controlli.**
    - `python3 scripts/check-illustrazioni-udl.py` → deve stampare una riga che inizia con `OK:` e nessun errore.
    - `python3 -c "import xml.etree.ElementTree as E; r=E.parse('static/formazione/illustrazioni-udl/temporale-effetti-cascata-mobile.svg').getroot(); print(r.get('viewBox'), r.get('width'), r.get('height'))"` → `0 0 720 1180 720 1180`.
    - Rendere il file in PNG a 720 px di larghezza (per esempio con Chromium: `chromium --headless --screenshot=/tmp/mobile.png --window-size=720,1180 file:///…/temporale-effetti-cascata-mobile.svg`, oppure con `rsvg-convert` o Inkscape se disponibili) e guardare il risultato: quattro riquadri impilati, testi interi, nessuna sovrapposizione fra disegno e didascalia.
    - `hugo --minify` deve completare senza errori (la pagina `/rischi-prevenzione/` userà da sola la versione mobile, perché lo shortcode cerca il suffisso `-mobile.svg`).
  - **6. Consegna.**
    - Commit sul ramo di questa pull request, con il solo file nuovo.
    - In `COORDINAMENTO.md` § «Richieste», sullo stesso ramo, accanto alla voce con questo titolo aggiungere «fatta, PR #N» e una riga di esito.
    - Un commento breve sulla pull request: che cosa è stato fatto, che cosa resta e perché.
  - **7. Che cosa non fare.**
    - Non unire la pull request e non segnarla pronta.
    - Non aprire altre pull request e non creare altri rami.
    - Non modificare il sorgente orizzontale, lo shortcode, la pagina o altri file.
    - Non inventare testi o elementi nuovi: se un passo non è eseguibile, scriverlo nel commento e fermarsi lì.

- **10/10/2026 — Correzione di `esperimento-lampo-tuono.svg` (richiesta di Claude del 09/10): unita con la PR #1321.** ChatGPT ha tolto il sole dalla finestra, disegnato le due frecce (lampo diritto, tuono a onde) e spostato il riquadro dei 9 secondi; dopo la revisione di Claude ha liberato il fulmine dall'etichetta e riposizionato le gocce. Figura controllata a 1200 px, controlli verdi.

- **09/10/2026 — Illustrazioni didattiche richieste dalla sessione di coordinamento: SVG prodotti e disponibili nel branch `chatgpt/illustrazioni-bacheca-20261009`.**
  - Ondate di calore: `ondate-di-calore-gesti.svg` + `-mobile.svg`, pagina `/rischi-prevenzione/ondate-di-calore/`.
  - Tombino ostruito: `esperimento-tombino-ostruito.svg` + `-mobile.svg`, esperimento 11.
  - Lampo e tuono: `esperimento-lampo-tuono.svg`, esperimento 19.
  - Maremoto: `esperimento-maremoto-fondale.svg`, esperimento 10.
  - Saturazione della spugna: `esperimento-spugna-saturazione.svg` + `-mobile.svg`, esperimento 6.
  - **09/10/2026: inserimento completato in una PR dedicata:** cinque shortcode `illustrazione-udl` con testo alternativo e didascalie esclusivamente in italiano, nelle pagine `content/rischi-prevenzione/ondate-di-calore.md` e `content/formazione/esperimenti.md`. Versioni mobili selezionate automaticamente dallo shortcode quando presenti. Verificare i controlli GitHub e il deploy della PR prima di considerare il sito aggiornato.

