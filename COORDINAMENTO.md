# Bacheca di coordinamento — sito della Protezione Civile di Genzano di Roma

File interno, non pubblicato (Hugo non legge la cartella principale del repository). Lo usano Claude e ChatGPT per passarsi lavoro, istruzioni e avvisi. Nata l'8 ottobre 2026; dall'11 ottobre 2026 segue il protocollo comune a tutti i repository di Alessandro, qui sotto.

<!-- PROTOCOLLO-COMUNE:INIZIO — testo identico in tutti i repository di Alessandro. Copia di riferimento: assistente-personale/COORDINAMENTO.md. Se lo cambi, cambialo in tutti e cinque i repository nello stesso lavoro. -->

## Protocollo comune Claude ⇄ ChatGPT ⇄ Gemini (uguale in tutti i repository)

Valido dall'11/10/2026 in tutti i repository di Alessandro: `sito-pc-genzano`, `social-pc-genzano`, `sito-misericordia-ariccia`, `cooprimavera`, `assistente-personale`. Il file si chiama sempre `COORDINAMENTO.md` e sta sempre nella cartella principale del repository. Questa prima parte è identica ovunque; la seconda parte, «Questo repository», cambia da repository a repository.

### A che cosa serve

Claude (Claude Code) e ChatGPT (chat con connettore GitHub, Codex) lavorano sugli stessi repository. La bacheca è il posto dove si passano lavoro, istruzioni e avvisi, così Alessandro non deve copiare testi da una chat all'altra e il lavoro continua anche quando una delle due non è disponibile (per esempio quando Claude ha finito i crediti).

**Anche Gemini (dall'11/10/2026).** Gemini lavora sui repository (Jules chiude: sola lettura dall'11/11/2026, spento il 31/12/2026, avviso letto sul sito il 04/11/2026; non si usa più), sul PC con **Antigravity CLI** (`agy`, che dal 18/06/2026 sostituisce Gemini CLI: legge `AGENTS.md`, le skill di `.agents/skills/` e quelle di Alessandro in `~/.gemini/skills/`; si prepara con `scripts/installa-gemini-pc.sh` di `assistente-personale`, dal 04/11/2026). Dove questo protocollo dice «ChatGPT», vale allo stesso modo per Gemini: stesse regole, stessa autonomia, stesse eccezioni. Differenze: i suoi rami si chiamano `gemini/<argomento>-AAAAMMGG`; una richiesta indirizzata a «ChatGPT» la prende solo ChatGPT, una indirizzata a «Gemini» solo Gemini, una indirizzata a «chi è disponibile» la prende la prima che apre la bacheca, che scrive subito accanto «presa da …» con una PR in bozza, così l'altra non la riprende. Le revisioni automatiche fatte da Codex o da Gemini sulle PR sono pareri da verificare, non ordini.

### Chi dà le istruzioni

- **Alessandro**: in chat o scrivendo una richiesta qui. Le sue istruzioni prevalgono su tutto il resto.
- **Claude o ChatGPT**: con una voce nella sezione «Richieste» di questo file, indirizzata all'altra.
- Le regole del repository (`CLAUDE.md`, `.claude/rules/`, `AGENTS.md`) valgono per entrambe: chi lavora le segue anche quando l'altra non c'è.
- **Dubbi → domande** (istruzione di Alessandro del 13/10/2026: «se hai dubbi sei obbligato a fare domande a me per chiarimenti»). Quando una scelta cambia davvero l'esito e la risposta non è nei file, nelle regole o nelle fonti, non si indovina: si chiede ad Alessandro — in chat se c'è, altrimenti in «Domande» qui sotto — e intanto si fa il resto. Per le scelte ordinarie coperte dalle regole si procede e si riporta (regola `.claude/rules/autonomia.md`).

### Quando Claude è ferma: ChatGPT prende il suo posto (dal 21/10/2026)

Istruzioni di Alessandro del 21/10/2026, dopo tre giorni senza Claude per i crediti finiti: *«Se tu sei fuori servizio devo avere al 100% la stessa operatività con altra AI!»*, *«Utilizza ChatGPT come prima AI, e utilizza il cervello che abbiamo creato o il file coordinamento per le consegne dei lavori»*.

- **Chi fa che cosa.** Quando Claude non risponde o le sue routine falliscono, ChatGPT (Codex) è la prima riserva e lavora come Claude, con le stesse regole e la stessa autonomia fino alla pubblicazione (§ «Che cosa fa ChatGPT quando Alessandro scrive «guarda la bacheca»»): riprende i «Lavori in corso», prende anche le richieste indirizzate a Claude e, quando Alessandro lo chiede, fa le routine del giorno dai testi scritti nei repository (elenco in `assistente-personale/ROUTINE.md`). Gemini viene dopo, solo se anche ChatGPT è fermo. Le istruzioni operative per ChatGPT sono in `AGENTS.md`, § «Quando Claude è ferma, lavori tu al suo posto», uguale in tutti i repository.
- **Consegna continua.** I crediti finiscono senza preavviso e una sessione interrotta non può più scrivere la consegna. Per questo chi lavora (Claude o ChatGPT) scrive in «Lavori in corso» ogni lavoro che dura più di un passaggio **appena lo comincia**: che cosa, ramo, PR, prossimo passo, documenti del Cervello coinvolti. Lo aggiorna a ogni tappa e lo toglie quando il lavoro è pubblicato.
- **Dove passano le consegne.** Lavori sui repository: questa bacheca. Lavori fuori dai repository (lettere, email, appuntamenti, documenti degli enti): il Cervello su Google Drive, nel documento dell'ente o del progetto oppure in «Note rapide». ChatGPT lo legge e lo aggiorna con l'app Google Drive; Codex, che il Cervello non lo vede, lascia la nota in questa bacheca e chi ha l'accesso la riporta nel Cervello.
- **Firma e controlli non cambiano.** Valgono `.claude/rules/firma-dei-lavori.md` e `.claude/rules/qualita.md`: identità di Alessandro Cuollo, nessun nome di strumenti, tutti i controlli eseguiti, merge squash con messaggio scritto.
- **Quando Claude torna.** Per prima cosa legge questa bacheca e controlla il lavoro fatto da ChatGPT come controlla ogni consegna, correggendo sul ramo se serve. Poi riporta nel Cervello e nella memoria ciò che manca e riprende le routine. Chi prende un lavoro lo segna «preso da …» accanto alla voce, così nessuno rifà il lavoro dell'altro.

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

**Che cosa fa Alessandro: due gesti.** (1) **Avvio**: apre chatgpt.com/codex/cloud, sceglie l'ambiente del repository (per social-pc-genzano, «tutti-i-repository») e, se il selettore lo offre, il ramo `chatgpt/…` della pull request (altrimenti va bene il principale: il testo di avvio contiene già tutta la richiesta); incolla il testo di avvio e avvia. (2) **Consegna**: quando Codex ha finito, preme «Create PR» nel task. Niente altro: non scrive istruzioni, non controlla, non unisce.

**Che cosa fa Codex, durante.** Lavora sul ramo da cui è partito il task, esegue la richiesta punto per punto, fa i controlli indicati e alla fine riassume che cosa ha fatto, che cosa resta e perché. Non tocca `COORDINAMENTO.md` (l'esito in bacheca lo scrive chi chiude, così il lavoro non entra in conflitto con la voce) e non unisce nulla. Il suo contenitore non legge la pull request e la sua rete può essere limitata: per questo il testo di avvio porta la richiesta intera e non rimanda né alla bacheca né a pagine esterne.

**Che cosa fa Claude, dopo.** `passa-a.py stato` dice che cosa è arrivato: «CONSEGNA NELLA PR #M» (la pull request aperta dal task dopo la preparazione, riconosciuta dal ramo di base, dal nome del ramo preparato o dal numero della pull request), «POSSIBILE CONSEGNA NELLA PR #M» (aperta dopo la preparazione con il solo titolo della richiesta, che può coincidere per caso, o da un ramo `codex/…` senza altri segni: si riconosce guardandola) oppure «HA FATTO PUSH» se il lavoro arriva direttamente sul ramo. Claude controlla il risultato (immagini rese e guardate, controlli del repository, niente dati inventati né riferimenti allo strumento); se non va bene **continua direttamente** sul ramo e corregge o rifà, senza rimandare indietro (ogni giro costa crediti): per correggere il lavoro arrivato in una pull request di consegna, prima lo porta nel ramo con `passa-a.py chiudi --pr N --consegna M --senza-merge`, che non unisce, lascia la pull request in bozza e la voce in «Richieste», aggiorna la copia locale del ramo e stampa i passi per correggere. Poi `passa-a.py chiudi --pr N --consegna M`: porta il lavoro della pull request #M nel ramo preparato e la chiude come assorbita con un titolo neutro; riscrive a nome di Alessandro i commit con un altro autore e toglie i trailer; porta nel ramo le novità di `main` con un commit di merge (mai rebase; un conflitto ferma lo script e si risolve a mano); sposta la voce di bacheca in «Archiviati» con la riga di esito; segna la pull request pronta, aspetta i controlli verdi, unisce (squash con messaggio scritto, un merge per volta), toglie dalle due pull request gli eventuali commenti dello strumento (i rapporti di `github-actions[bot]` restano; dalle sessioni cloud, dove il canale di GitHub non lascia cancellare, commenti e ramo li toglie il workflow `rimuovi-firma-strumento.yml` alla chiusura della pull request) e, dove il repository ha `deploy.yml`, aspetta che il deploy del merge finisca bene: un deploy fallito ferma lo script, perché il sito non è aggiornato. Se la sessione è finita, chiude la routine giornaliera. Se dopo un giorno dalla preparazione non è arrivato nulla, Claude chiede ad Alessandro se l'ha avviata o se manca solo «Create PR»; se l'ha avviata e Codex non ha consegnato, o se ha risposto che i crediti sono finiti, Claude fa il lavoro da sola e lo scrive in bacheca. In fondo `stato` elenca anche le pull request di ChatGPT o Gemini che non sono passaggi («NON È UN PASSAGGIO»: rami `chatgpt/…` che non sono passaggi preparati, rami `codex/…` e `gemini/…` che nessun passaggio riconosce come consegna certa; una consegna solo possibile compare anche lì e, se non è la consegna, si tratta così), cioè lavoro fatto in riserva o da una richiesta della bacheca: Claude lo controlla come ogni consegna e lo unisce con `passa-a.py chiudi --pr N --titolo "…" --messaggio "…"` (con `--qualsiasi` per i rami `codex/…` e `gemini/…`), che riscrive gli autori, segna la pull request pronta, aspetta i controlli e unisce con squash.

**Ambienti cloud.** Gli ambienti di Codex Cloud (chatgpt.com/settings/codex-cloud, scheda «Ambienti»: creati da Alessandro, visibili «Solo io», l'unica scelta che l'account personale offre) esistono per tutti e cinque i repository dal 13/10/2026, uno per repository, e Codex Cloud ci lavora dentro. Fa eccezione social-pc-genzano, che sta solo in «tutti-i-repository»: l'ambiente con tutti e cinque i repository e le skill di Alessandro, quello da usare quando Claude è ferma (nome dato il 21/10/2026; a un ambiente già creato non si aggiunge un repository). Non serve altro; `passa-a.py stato` segnala comunque come «CANALE AUTOMATICO MUTO» la risposta «create an environment», se arriva a un commento di avvio.

**Che cosa contiene la richiesta, sempre.** ChatGPT lavora bene solo con istruzioni esatte, e in Codex Cloud non può fare domande: tutto ciò che gli serve sta nella richiesta, verificato prima da Claude. Sette parti, nell'ordine (`passa-a.py modello` le stampa): (1) **obiettivo** in una frase, e a che cosa serve; (2) **file** da creare o modificare, con il percorso esatto; (3) **che cosa fare**, passo per passo, con i dati già verificati (numeri, nomi, date, misure, testi): niente da cercare, niente da indovinare; (4) **vincoli** del repository che valgono per quel lavoro (regole, licenze, misure, accessibilità, niente riferimenti allo strumento nei file e nei commit); (5) **controlli** da eseguire prima di consegnare, con i comandi esatti; (6) **consegna**: solo le modifiche ai file del punto 2, messaggi di commit in italiano senza nomi di strumenti, un riassunto finale con fatto / non fatto / perché, `COORDINAMENTO.md` non si tocca; (7) **che cosa non fare**: non unire, non segnare pronta nessuna pull request, non toccare altri file, non inventare dati mancanti. Una richiesta a cui manca una parte non si manda.

**Quando si passa un lavoro a ChatGPT.** Lo decide Claude caso per caso, con parsimonia: il piano ChatGPT ha crediti a consumo e ogni passaggio li usa (li usa anche la revisione automatica che Codex fa sulle pull request non in bozza, quindi la pull request preparata resta in bozza finché il lavoro non è finito, e più lavori piccoli si mettono in una richiesta sola). Si passa un lavoro quando:

- **serve andare live prima su più fronti**, soprattutto in emergenza o quando lo stesso contenuto esce su più siti: Claude tiene per sé la parte che richiede i gate editoriali e la comunicazione di allerta ed emergenza, e passa a ChatGPT le parti autonome che si possono specificare per iscritto (script e dati, controlli, audit, materiali di supporto, adattamenti di cose già fatte), così lavorano in parallelo invece che in fila;
- **è un lavoro che ChatGPT sa fare bene e che non ha bisogno del giudizio della sessione**: l'aggiornamento degli interventi dall'export del gestionale, gli audit del sito, i controlli ripetitivi;
- **una sessione finisce con un lavoro urgente a metà** (emergenza, uscita programmata entro un giorno, Alessandro ha chiesto di andare live): oltre alla consegna in «Lavori in corso», Claude passa il ramo a ChatGPT con lo stesso meccanismo. Se non è urgente, scrive solo la consegna.

Se un lavoro non si può passare (sotto, «Che cosa non si passa»), o non si può fare in Codex Cloud (sotto, «Immagini»), lo fa Claude, se serve con più agenti in parallelo (regola `.claude/rules/autonomia.md`, uguale in tutti i repository: autonomia, lavoro diviso, agenti e skill creati quando servono, domande ad Alessandro nei dubbi).

**Immagini.** Le illustrazioni **SVG** le fa Claude (istruzione di Alessandro del 13/10/2026): sono codice, le rende e le guarda prima di pubblicarle; le passa a ChatGPT solo per lavorare in parallelo, con la richiesta completa (misure, contenuto riquadro per riquadro, testi, vincoli). Le **immagini raster** (foto, locandine, grafiche PNG o JPG) non si passano a ChatGPT, perché Codex non ha il generatore di immagini: le fa Claude con i propri strumenti — i generatori del repository (cover, immagini social, fascia blu), gli SVG resi in PNG, i connettori grafici disponibili nella sessione quando ci sono, le foto con licenza libera — e le controlla prima del commit come ogni immagine. Se un'immagine non si può fare in nessuno di questi modi, Claude sceglie l'alternativa migliore (per esempio un'illustrazione al posto di una foto) e lo scrive nella pull request. Nessun passaggio a mano per Alessandro.

**Che cosa non si passa.** Allerte ed emergenze vere, articoli nuovi che devono passare dai gate editoriali, pagine legali, lavori che richiedono credenziali, spese o invii a persone: restano a Claude o ad Alessandro, come in «Quando ChatGPT non unisce e si ferma».

**Gemini.** Jules chiude il 31/12/2026 e non si usa. Gemini lavora con Antigravity: sul PC con `agy`; dal cellulare comandando il PC acceso (Remote Control, antigravity.google.com), e a PC spento con i Remote Agents di Antigravity, quando Google li avrà attivati per l'account di Alessandro (distribuzione graduale, non ancora attivi il 04/11/2026). Fino ad allora, a PC spento, i lavori che sarebbero andati a Gemini li fa Claude o passano a ChatGPT, oppure a «Gemini automatico» (sotto).

### AI automatiche e consulto fra AI (dal 05/11/2026)

Istruzioni di Alessandro del 05/11/2026: *«Fai in modo che tra AI si parlino in autonomia»*, *«Parlino e aiutino»*, *«Dobbiamo fare cose gratuite»*, *«Non riesci a forzare l'avvio di codex di chatgpt?»*, *«le istruzioni che andrai a passare in automatico, devono essere chiare precise a prova di errore»*.

- **Chi sono.** AI che lavorano da sole su GitHub, gratis o nei limiti degli abbonamenti già pagati: «ChatGPT automatico» (Codex con l'accesso ChatGPT di Alessandro), «Gemini automatico» (Gemini CLI con la chiave gratuita della Gemini API; solo nei repository pubblici, vedi sotto «Che cosa non si passa»), «DeepSeek automatico», «GLM automatico», «Kimi automatico» e «Qwen automatico» (Claude Code con i modelli gratuiti di Ollama Cloud). Le fa partire il workflow `.github/workflows/lavoratore-ai.yml`, uguale in tutti i repository, con `scripts/lavoratore-ai.py`.
- **Come si passa loro un lavoro.** Una voce in «Richieste» indirizzata a una di loro (per esempio `- **2026-11-05 — da Claude a ChatGPT automatico — Titolo**`), con sotto la richiesta nelle sette parti di `passa-a.py modello`, rientrate di due spazi, portata su `main`. Da una sessione lo fa da solo `python3 scripts/lavoratore-ai.py richiedi --a "ChatGPT automatico" --titolo "…" --brief FILE`: controlla le sette parti, scrive la voce, apre la PR della bacheca, aspetta i controlli e la unisce. L'AI parte appena la voce arriva su `main` e, come rete, ogni mattina (09:23 con l'ora solare, 10:23 con quella legale: le quote giornaliere gratuite di Gemini, che si azzerano a mezzanotte del Pacifico, sono già nuove). Una richiesta senza le sette parti compilate non parte: il run diventa rosso con il motivo, e si corregge la voce.
- **Che cosa fa l'AI.** Segna la voce «presa da …», lavora su un ramo `auto/<ai>-<argomento>-AAAAMMGG` con istruzioni fisse (regole del repository, la richiesta punto per punto, divieti, controlli, verifica finale da revisore ostile, riassunto) e consegna sul ramo; nella voce scrive l'esito, i file toccati e il riassunto. Se il repository permette a GitHub Actions di aprire pull request, apre anche la PR in bozza e la voce dice «PR #N»; se no, la voce dice «ramo …, pull request da aprire» e il run resta verde. Il programma dell'AI lavora in un job che può solo leggere, senza il token di GitHub che scrive: non può fare push, unire o aprire PR. Consegna il lavoro come pacchetto a un job separato, che riparte da un checkout pulito, non si fida del pacchetto e lo ricontrolla: le modifiche a `COORDINAMENTO.md`, `.github/` e `.githooks/` vengono annullate; collegamenti simbolici, sottomoduli e percorsi fuori dal repository bloccano la consegna. Un lavoro o un riassunto con un testo simile a una chiave d'accesso, o con il valore vero di una chiave del job, non si pubblica; un lavoro bloccato fa diventare rosso il run e il ramo resta, con il motivo nella voce. `passa-a.py stato` dice per ogni ramo `auto/…` che cosa ha scritto la consegna (lavoro consegnato, a metà, nessun file, non riuscito, bloccato, interrotto), e `chiudi` si ferma su un tentativo non riuscito o bloccato che non ha lavoro sul ramo.
- **Se il servizio è occupato.** L'AI prova fino a tre modelli, dal più nuovo. Se il programma risponde «occupato» tre volte prima di toccare un file, passa al modello successivo; se sono tutti occupati riprova dopo cinque minuti, al massimo per due giri. Se la quota gratuita di un modello è finita, passa subito al successivo, senza secondo giro, perché la quota non torna in cinque minuti. Se nessun modello lavora, il ramo si toglie insieme alla sua PR e la richiesta, ancora aperta su `main`, riparte da sola al giro dopo: al prossimo aggiornamento della bacheca su `main`, al giro del mattino o con l'avvio a mano del workflow. Si toglie da solo anche il ramo rimasto da un giro che non ha lavorato (solo la bacheca, con «lavoro non riuscito» e nessun file toccato, oppure senza esito da più di tre ore); un ramo con del lavoro resta a chi controlla.
- **Chi unisce.** Claude, alla prima sessione o routine sul repository, anche dal cellulare: controlla il lavoro come ogni consegna (`passa-a.py stato` lo elenca fra le PR che non sono passaggi, oppure fra i rami senza PR) e lo chiude con `passa-a.py chiudi --pr N --qualsiasi --titolo "…" --messaggio "…"`; se la PR non c'è, con `passa-a.py chiudi --ramo auto/… --titolo "…" --messaggio "…"`, che la apre a nome di Alessandro e prosegue uguale. `chiudi` archivia la voce, aspetta i controlli e unisce; un tentativo non riuscito non si chiude (lo script si rifiuta) e lo riprende il giro dopo. Un lavoro rimasto a metà (per esempio quota finita dopo aver toccato i file) resta sul ramo con «lavoro non riuscito» e i file toccati: chi unisce lo rifà passare dai controlli della richiesta, lo chiude se è completo e, se non lo è, lo completa sul ramo prima di chiudere. Quando la PR è segnata pronta, la revisione automatica di ChatGPT la legge. Quando Claude è ferma, la chiude ChatGPT con le stesse regole.
- **Consulto.** Chi lavora (Claude, ChatGPT, Gemini e le AI automatiche) può chiedere un parere alle altre: `python3 scripts/consulto-ai.py deepseek|qwen|glm|kimi|gptoss|gemini "domanda"`, oppure `tutti`, che le fa parlare fra loro (rispondono, leggono le risposte delle altre, si correggono, e una sintesi dice dove concordano e dove no; `elenco` dice chi risponde adesso). Su Claude anche `scripts/chiedi-a.sh`. Il parere si verifica sulla fonte, non si esegue a occhi chiusi. Mai dati personali, sanitari, di minori o riservati nelle domande: lo script toglie comunque email, telefoni, codici fiscali, IBAN e numeri di carta. Ollama dichiara di non usare i testi per addestrare i modelli. Per la Gemini API la pagina dei prezzi dice che sul piano gratuito i testi servono a migliorare i prodotti di Google; le condizioni (versione del 17/10/2025, l'ultima che si è potuta leggere) aggiungono che possono leggerli dei revisori, chiedono di non mandare dati sensibili, riservati o personali e fanno eccezione per chi è nello Spazio economico europeo, in Svizzera e nel Regno Unito. Per questo Gemini non riceve i file (`--file`) di un repository privato, o di cui non si sa se lo sia, e con `tutti` resta fuori da solo.
- **Chiavi.** Nei segreti di ogni repository: `GEMINI_API_KEY` e `OLLAMA_API_KEY` (gratuite) e `CHATGPT_ACCESSO` (un accesso ChatGPT separato per ogni repository, perché i rinnovi automatici non si pestino i piedi; la copia rinnovata si salva cifrata nella cache e ogni 6 giorni il giro del mattino la tiene viva). Le mette dal PC `scripts/collega-ai-automatiche.sh`, che all'avvio delle sessioni sul PC aggiunge da solo le chiavi gratuite anche ai repository nuovi, permette a GitHub Actions di aprire le PR in bozza e dice se manca un accesso ChatGPT. Dalle sessioni cloud GitHub non lascia toccare segreti e impostazioni di Actions: lì lo script lo dice ed esce, e le consegne senza PR si chiudono lo stesso con `chiudi --ramo`. Senza la chiave che serve la richiesta resta aperta e il run è rosso: lo vede la sorveglianza dei guasti.
- **Che cosa non si passa.** Quello che non si passa a ChatGPT (§ «Che cosa non si passa»): allerte ed emergenze, articoli che passano dai gate editoriali, pagine legali, credenziali, spese, invii a persone o enti, pubblicazioni sui social. A nessuna di loro lavori che chiedono di leggere o scrivere dati personali di terzi (anagrafiche, contatti, verbali con nomi): «Non esporre dati personali di terzi fuori da questo workspace» (`CLAUDE.md` di assistente-personale). E a «Gemini automatico» nessun lavoro in un repository privato, o di cui GitHub non dice se lo sia: lì l'AI può leggere dati personali e riservati, che a Gemini non vanno. Lo controlla lo script: `richiedi` non pubblica la richiesta, una voce già in bacheca non parte e rende rosso il run finché non si riscrive per DeepSeek, GLM, Kimi o Qwen automatico, e lì le AI automatiche lavorano senza la chiave di Gemini, quindi nemmeno il loro consulto la raggiunge.

<!-- PROTOCOLLO-COMUNE:FINE -->

## Questo repository: sito-pc-genzano

Il merge su `main` pubblica il sito su Aruba e GitHub Pages in pochi minuti (`deploy.yml`). Le regole complete sono in `AGENTS.md` (punto d'ingresso per ChatGPT) e in `CLAUDE.md`.

### Routine di questo repository

I testi delle routine di Claude che lavorano qui sono in `riferimenti-interni/routine-prompts/` (indice con orari in `riferimenti-interni/routine-prompts/README.md`); l'elenco di tutte le routine di Alessandro è in `ROUTINE.md` del repository `assistente-personale`. Se Claude è ferma, ChatGPT le esegue da quei testi (§ «Quando Claude è ferma: ChatGPT prende il suo posto»).

### Controlli prima di unire una PR

- `hugo --minify` senza errori, e i controlli bloccanti della PR verdi (`validate-pr.yml`, `pa11y-ci.yml`).
- Articoli in `content/comunicazioni/`: il controllo di forma e dei fatti di `AGENTS.md` § 3.4 e § 3.5 (se Claude non c'è, usa come lista di controllo `.claude/agents/pc-article-reviewer.md`, `pc-fact-checker.md`, `pc-calendario-editoriale.md` per gli articoli programmati); cover generata con `python3 scripts/genera-cover.py <file>`; `python3 scripts/check-refusi.py <file>`; `python3 scripts/check-data-uscita.py`.
- Schede, kit e giochi: `.claude/agents/pc-didattica-reviewer.md` come lista di controllo; `python3 scripts/check-parita-schede.py`; i pacchetti si rigenerano con gli script, mai a mano.
- Illustrazioni: `python3 scripts/check-illustrazioni-udl.py` e il disegno guardato a 1200 px (a 720 px per i `-mobile.svg`).
- Identità dei commit: `bash scripts/imposta-identita-git.sh` (nome Alessandro Cuollo). Nessuna riga che citi lo strumento nei commit e nelle PR.

### Passaggi a ChatGPT in questo repository

- Li prepara Claude con `python3 scripts/passa-a.py nuovo` (ramo `chatgpt/…`, voce in bacheca, PR in bozza, testo di avvio con la richiesta intera); li avvia Alessandro in Codex Cloud incollando il testo di avvio e, a lavoro finito, premendo «Create PR» nel task (i soli due gesti a mano); li controlla Claude con `passa-a.py stato` e li chiude con `passa-a.py chiudi --pr N --consegna M` (pull request di consegna portata nel ramo e chiusa con titolo neutro, commit riscritti a nome di Alessandro se serve, voce di bacheca archiviata con l'esito, PR pronta, controlli verdi, squash merge). Dettagli e criteri nel protocollo comune, § «Passaggio a ChatGPT».
- Titolo e descrizione della PR descrivono il lavoro senza nomi di strumenti (lo script si rifiuta di aprirla se ne trova uno); la richiesta per esteso sta in questa bacheca e nel testo di avvio. Codex non tocca la bacheca: l'esito lo scrive `chiudi`. Il commento `@codex …` resta solo per riprovare il canale automatico (`nuovo --con-codex`, `riavvia --con-codex`): `chiudi` lo toglie insieme alle risposte dello strumento. Le revisioni automatiche di Codex sulle PR pronte restano visibili (una revisione del bot non si può cancellare, a differenza dei commenti): dipendono da un'impostazione di Codex che solo Alessandro può cambiare, e per ora ha scelto di lasciarle (13/10/2026).
- **Avvio con una riga (dal 05/11/2026).** Istruzione di Alessandro: «Devi scrivere sul file coordinamento altrimenti è troppo complicato così copiare». Dopo `passa-a.py nuovo`, Claude porta la voce del passaggio anche sul ramo principale, con una PR della sola bacheca unita a controlli verdi, prima di dare il via ad Alessandro. Il testo da incollare in Codex Cloud diventa una riga: «Leggi COORDINAMENTO.md ed esegui la richiesta della PR #N.», con l'ambiente «sito-pc-genzano» e il ramo principale. Ogni voce porta il riquadro «Per chi la esegue» (non toccare la bacheca, non unire, riassunto finale). Prima di `chiudi`, il ramo `chatgpt/…` si allinea a `main` prendendo la bacheca di `main`. Finché `passa-a.py` non lo fa da sé, questi passi li fa Claude.
- Se la sessione che ha preparato il passaggio non lo chiude, lo chiude la routine giornaliera delle issue (14:07 italiane, rule 10 § «Lavorazione autonoma delle issue automatiche»).

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

- **07/11/2026 — Claude, audit completo del sito con più revisori.** Richiesta di Alessandro: «Fai fare un audit completo del sito ... a tutte le intelligenze artificiali che abbiamo collegato. Ogni intelligenza fa il suo audit. Pro e contro del sito. Consigli per migliorarlo». Stessa richiesta in sette parti per ogni revisore; ognuno scrive il proprio file `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-<lettera>.md`: A Claude (fatto: PR #1751, unita il 07/11/2026), B Gemini automatico (primo tentativo fermo dopo lo scheletro per la quota gratuita finita, ramo `auto/gemini-audit-completo-del-sito-revisore-b-20261107`, da togliere dal PC o dalla pagina del ramo; secondo tentativo del 07/11 alle 9:07 fermo senza file per il servizio occupato, errore 503 su gemini-3.8-flash e 3.7-flash e limite al minuto su 3.6-flash: la richiesta è stata spostata dopo quelle di D, E, F e G, così non le blocca, e riparte quando tocca a lei; il lavoratore legge il limite al minuto come quota del giorno finita e non rifà quel modello nel secondo giro, da correggere nel kit comune di `assistente-personale`), C ChatGPT (passaggio, PR #1749, avvio a mano in Codex Cloud), D DeepSeek, E GLM, F Kimi e G Qwen automatici. Dalle 9:06 del 07/11/2026 nei segreti del repository c'è anche `OLLAMA_API_KEY` (nel run del lavoratore `HA_OLLAMA_API_KEY: true`); manca ancora `CHATGPT_ACCESSO`. Le richieste D, E, F e G partono una per giro del lavoratore, nell'ordine della bacheca: dopo ogni consegna si rilancia «AI automatiche» (Actions o `gh workflow run lavoratore-ai.yml`). Prossimo passo: Claude verifica ogni rilievo, scrive l'esito accanto e chiude ogni consegna con `passa-a.py chiudi`; il confronto dei revisori va ad Alessandro.

## Richieste

- **2026-11-07 — da Claude a DeepSeek automatico — Audit completo del sito, revisore D**
  ## 1. Obiettivo
  Un audit completo e indipendente del sito della Protezione Civile di Genzano di Roma (https://www.protezionecivilegenzano.it/) e del suo repository, con i punti di forza (pro), i punti deboli (contro) e i consigli per migliorarlo, scritto in un solo file. Serve ad Alessandro per confrontare il parere di più revisori, ognuno con il proprio audit, e decidere che cosa migliorare.

  ## 2. File
  - `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-d.md` (da creare). Nessun altro file si crea o si modifica.

  ## 3. Che cosa fare
  1. Per prima cosa crea il file con lo scheletro delle sezioni del passo 6 e riempilo man mano: se il lavoro si interrompe, ciò che hai già scritto resta.
  2. Raccogli le prove solo da queste fonti:
     - il sito pubblicato, con richieste vere: `curl -sS -L -A "Mozilla/5.0" -o /tmp/pagina.html -w "%{http_code} %{size_download}\n" URL` per pagina e peso, `curl -sSI URL` per le intestazioni HTTP; l'elenco delle pagine è in https://www.protezionecivilegenzano.it/sitemap.xml;
     - il repository: template in `themes/flavour-pcgenzano/layouts/`, CSS e JavaScript in `themes/flavour-pcgenzano/static/` e `static/`, contenuti in `content/`, dati in `data/`, script in `scripts/`, automazioni in `.github/workflows/`;
     - i rapporti già fatti in `riferimenti-interni/audit-esterni/` e `riferimenti-interni/audit-interni/`: non ripetere un rilievo già segnato come corretto, salvo che tu lo ritrovi ancora sul sito pubblicato (in quel caso scrivilo).
  3. Guarda almeno queste pagine del sito pubblicato: `/`, `/emergenza/`, `/cosa-fare-adesso/`, `/allerte-meteo/`, `/numeri-utili/`, `/rischi-prevenzione/rischio-sismico/`, `/piano-emergenza/`, `/aree-attesa/`, `/cruscotto/`, `/monitor/`, `/assistente/`, `/comunicazioni/` e l'articolo più recente che trovi lì, `/formazione/`, `/giochi/`, `/lim/`, `/diventa-volontario/`, `/chi-siamo/`, `/contatti/`, `/accessibilita/`, `/privacy/`, `/open-data/`, `/cerca/`, `/english/`, `/facile-da-leggere/`, `/mappa-sito/`. Puoi aggiungerne altre. Fai al massimo 200 richieste al sito, una al secondo: è su un hosting condiviso.
  4. Valuta questi ambiti, uno per uno: (a) informazioni d'emergenza e allerta, chiare per il cittadino; (b) contenuti: correttezza, fonti, coerenza fra pagine diverse, aggiornamento; (c) navigazione, ricerca, organizzazione delle pagine; (d) accessibilità secondo WCAG 2.2 livello AA (titoli, testi alternativi, etichette, contrasti, uso da tastiera, nomi accessibili dei comandi); (e) peso e velocità delle pagine su rete mobile; (f) motori di ricerca e dati strutturati; (g) sicurezza (HTTPS, intestazioni HTTP, Content-Security-Policy) e privacy; (h) materiali per le scuole e uso sulla lavagna interattiva; (i) affidabilità tecnica: build, automazioni, controlli; (j) grafica e identità.
  5. Se nel tuo ambiente puoi aprire le pagine con un browser, provale anche lì (per esempio con un controllo di accessibilità automatico); se non puoi, controlla l'HTML e scrivi nel § 2 del file che la prova nel browser non è stata fatta. Se il sito non risponde dal tuo ambiente, fai l'audit sul solo repository e scrivilo nel § 2.
  6. Il file ha esattamente queste sezioni, con questi titoli:
     - `# Audit completo del sito — revisore D`
     - `## 1. Giudizio complessivo`: da 5 a 10 righe, senza punteggi o percentuali che non hai misurato.
     - `## 2. Perimetro e metodo`: data e ora italiane delle misure, pagine e file guardati, comandi usati, che cosa non hai potuto verificare e perché.
     - `## 3. Pro: punti di forza`: elenco numerato, almeno 5 punti, ognuno con la sua prova.
     - `## 4. Contro: punti deboli`: un rilievo per titolo `### R1 — <titolo breve>`, `### R2 — …`, ciascuno con le cinque voci del formato di `riferimenti-interni/audit-esterni/README.md`: «Dove», «Che cosa non va», «Prova», «Priorità» (P1 sbagliato o pericoloso per il cittadino · P2 da correggere · P3 miglioramento) ed «Esito», dove scrivi «(da compilare da chi verifica)».
     - `## 5. Consigli per migliorarlo`: elenco numerato in ordine di importanza; per ogni consiglio una riga «Perché», una riga «Impegno» (piccolo, medio o grande) e i rilievi del § 4 che risolve, se ce ne sono. Solo consigli gratuiti e compatibili con i vincoli del punto 4.
     - `## 6. Domande e dubbi`: ciò che non hai potuto chiarire.
  7. Ogni punto di forza e ogni rilievo ha una prova verificabile: l'URL con il risultato della richiesta (codice HTTP, misura, frase esatta copiata dalla pagina), oppure il percorso del file con il numero di riga. Quello che non hai verificato non si scrive. Meglio otto rilievi provati che trenta senza prova.
  8. Prima di finire rileggi il file come un revisore ostile che vuole smentirti: ricontrolla ogni prova, togli ciò che non regge, controlla che i consigli rispettino i vincoli del punto 4.

  ## 4. Vincoli
  - Il file è in italiano chiaro, con frasi brevi. Nel file non compaiono nomi di programmi o di servizi usati per fare il lavoro: la firma è «revisore D».
  - I consigli rispettano queste decisioni del progetto, che non si rimettono in discussione:
    - budget zero: solo interventi gratuiti, senza servizi, piani o licenze a pagamento;
    - sito statico generato con Hugo e Bootstrap Italia, senza backend, CMS o database;
    - solo JavaScript senza framework; nelle pagine per le scuole, JavaScript compatibile con ECMAScript 2018;
    - niente app installabile, niente service worker, niente funzionamento offline basato sulla cache del browser;
    - la cache HTTP è disattivata per scelta (intestazioni `no-store`): non proporre di riattivarla; se un controllo automatico la segnala, è una conseguenza nota, non un rilievo;
    - nessuna modifica al CSS della barra di navigazione di Bootstrap Italia;
    - niente overlay di accessibilità commerciali; l'assistente del sito resta un percorso di scelte fisse, mai un programma che genera risposte;
    - i contenuti pubblicati non citano i programmi usati per scrivere i testi o fare le immagini;
    - niente conteggi dei materiali disponibili (quante schede, quanti giochi) e niente widget di valutazione delle pagine;
    - i colori dell'allerta (verde, giallo, arancione, rosso) sono quelli del sistema nazionale di protezione civile e non si cambiano;
    - il Gruppo non interviene su chiamata dei cittadini: in emergenza si chiama il 112.
  - Niente dati personali nel file. Niente testi copiati da siti di terzi: si citano solo frasi brevi del sito che si sta valutando, come prova.

  ## 5. Controlli
  - `test -f riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-d.md && echo presente` stampa «presente».
  - `grep -cE "^## [1-6]\. " riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-d.md` stampa 6.
  - `grep -c "^### R[0-9]" riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-d.md` stampa un numero maggiore di 0, e ogni rilievo ha le righe «Dove», «Che cosa non va», «Prova», «Priorità» ed «Esito».
  - `python3 -c "import importlib.util as u; s=u.spec_from_file_location('l','scripts/lavoratore-ai.py'); m=u.module_from_spec(s); s.loader.exec_module(m); t=open('riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-d.md',encoding='utf-8').read(); print(len(m.VIETATE.findall(t))+len(m.VIETATE_SIGLE.findall(t)))"` stampa 0 (nessun nome di strumento nel file).
  - `git status --porcelain` elenca solo il file del punto 2.

  ## 6. Consegna
  Solo il file del punto 2. Alla fine un riassunto breve: fatto, non fatto e perché, controlli eseguiti con l'esito. `COORDINAMENTO.md` non si tocca: l'esito in bacheca lo scrive chi chiude il lavoro.

  ## 7. Che cosa non fare
  - Non correggere nulla del sito né del repository: chi fa l'audit non corregge, le correzioni le fa chi verifica i rilievi.
  - Non toccare file fuori dall'elenco del punto 2; non unire nulla, non aprire e non segnare pronta nessuna pull request.
  - Non inventare dati, misure, punteggi, norme o citazioni: se una cosa non si può verificare, va nel § 6 del file.
  - Non mandare dati del repository o del sito a servizi esterni, salvo le richieste al sito pubblicato del passo 3.

- **2026-11-07 — da Claude a Kimi automatico — Audit completo del sito, revisore F**
  ## 1. Obiettivo
  Un audit completo e indipendente del sito della Protezione Civile di Genzano di Roma (https://www.protezionecivilegenzano.it/) e del suo repository, con i punti di forza (pro), i punti deboli (contro) e i consigli per migliorarlo, scritto in un solo file. Serve ad Alessandro per confrontare il parere di più revisori, ognuno con il proprio audit, e decidere che cosa migliorare.

  ## 2. File
  - `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-f.md` (da creare). Nessun altro file si crea o si modifica.

  ## 3. Che cosa fare
  1. Per prima cosa crea il file con lo scheletro delle sezioni del passo 6 e riempilo man mano: se il lavoro si interrompe, ciò che hai già scritto resta.
  2. Raccogli le prove solo da queste fonti:
     - il sito pubblicato, con richieste vere: `curl -sS -L -A "Mozilla/5.0" -o /tmp/pagina.html -w "%{http_code} %{size_download}\n" URL` per pagina e peso, `curl -sSI URL` per le intestazioni HTTP; l'elenco delle pagine è in https://www.protezionecivilegenzano.it/sitemap.xml;
     - il repository: template in `themes/flavour-pcgenzano/layouts/`, CSS e JavaScript in `themes/flavour-pcgenzano/static/` e `static/`, contenuti in `content/`, dati in `data/`, script in `scripts/`, automazioni in `.github/workflows/`;
     - i rapporti già fatti in `riferimenti-interni/audit-esterni/` e `riferimenti-interni/audit-interni/`: non ripetere un rilievo già segnato come corretto, salvo che tu lo ritrovi ancora sul sito pubblicato (in quel caso scrivilo).
  3. Guarda almeno queste pagine del sito pubblicato: `/`, `/emergenza/`, `/cosa-fare-adesso/`, `/allerte-meteo/`, `/numeri-utili/`, `/rischi-prevenzione/rischio-sismico/`, `/piano-emergenza/`, `/aree-attesa/`, `/cruscotto/`, `/monitor/`, `/assistente/`, `/comunicazioni/` e l'articolo più recente che trovi lì, `/formazione/`, `/giochi/`, `/lim/`, `/diventa-volontario/`, `/chi-siamo/`, `/contatti/`, `/accessibilita/`, `/privacy/`, `/open-data/`, `/cerca/`, `/english/`, `/facile-da-leggere/`, `/mappa-sito/`. Puoi aggiungerne altre. Fai al massimo 200 richieste al sito, una al secondo: è su un hosting condiviso.
  4. Valuta questi ambiti, uno per uno: (a) informazioni d'emergenza e allerta, chiare per il cittadino; (b) contenuti: correttezza, fonti, coerenza fra pagine diverse, aggiornamento; (c) navigazione, ricerca, organizzazione delle pagine; (d) accessibilità secondo WCAG 2.2 livello AA (titoli, testi alternativi, etichette, contrasti, uso da tastiera, nomi accessibili dei comandi); (e) peso e velocità delle pagine su rete mobile; (f) motori di ricerca e dati strutturati; (g) sicurezza (HTTPS, intestazioni HTTP, Content-Security-Policy) e privacy; (h) materiali per le scuole e uso sulla lavagna interattiva; (i) affidabilità tecnica: build, automazioni, controlli; (j) grafica e identità.
  5. Se nel tuo ambiente puoi aprire le pagine con un browser, provale anche lì (per esempio con un controllo di accessibilità automatico); se non puoi, controlla l'HTML e scrivi nel § 2 del file che la prova nel browser non è stata fatta. Se il sito non risponde dal tuo ambiente, fai l'audit sul solo repository e scrivilo nel § 2.
  6. Il file ha esattamente queste sezioni, con questi titoli:
     - `# Audit completo del sito — revisore F`
     - `## 1. Giudizio complessivo`: da 5 a 10 righe, senza punteggi o percentuali che non hai misurato.
     - `## 2. Perimetro e metodo`: data e ora italiane delle misure, pagine e file guardati, comandi usati, che cosa non hai potuto verificare e perché.
     - `## 3. Pro: punti di forza`: elenco numerato, almeno 5 punti, ognuno con la sua prova.
     - `## 4. Contro: punti deboli`: un rilievo per titolo `### R1 — <titolo breve>`, `### R2 — …`, ciascuno con le cinque voci del formato di `riferimenti-interni/audit-esterni/README.md`: «Dove», «Che cosa non va», «Prova», «Priorità» (P1 sbagliato o pericoloso per il cittadino · P2 da correggere · P3 miglioramento) ed «Esito», dove scrivi «(da compilare da chi verifica)».
     - `## 5. Consigli per migliorarlo`: elenco numerato in ordine di importanza; per ogni consiglio una riga «Perché», una riga «Impegno» (piccolo, medio o grande) e i rilievi del § 4 che risolve, se ce ne sono. Solo consigli gratuiti e compatibili con i vincoli del punto 4.
     - `## 6. Domande e dubbi`: ciò che non hai potuto chiarire.
  7. Ogni punto di forza e ogni rilievo ha una prova verificabile: l'URL con il risultato della richiesta (codice HTTP, misura, frase esatta copiata dalla pagina), oppure il percorso del file con il numero di riga. Quello che non hai verificato non si scrive. Meglio otto rilievi provati che trenta senza prova.
  8. Prima di finire rileggi il file come un revisore ostile che vuole smentirti: ricontrolla ogni prova, togli ciò che non regge, controlla che i consigli rispettino i vincoli del punto 4.

  ## 4. Vincoli
  - Il file è in italiano chiaro, con frasi brevi. Nel file non compaiono nomi di programmi o di servizi usati per fare il lavoro: la firma è «revisore F».
  - I consigli rispettano queste decisioni del progetto, che non si rimettono in discussione:
    - budget zero: solo interventi gratuiti, senza servizi, piani o licenze a pagamento;
    - sito statico generato con Hugo e Bootstrap Italia, senza backend, CMS o database;
    - solo JavaScript senza framework; nelle pagine per le scuole, JavaScript compatibile con ECMAScript 2018;
    - niente app installabile, niente service worker, niente funzionamento offline basato sulla cache del browser;
    - la cache HTTP è disattivata per scelta (intestazioni `no-store`): non proporre di riattivarla; se un controllo automatico la segnala, è una conseguenza nota, non un rilievo;
    - nessuna modifica al CSS della barra di navigazione di Bootstrap Italia;
    - niente overlay di accessibilità commerciali; l'assistente del sito resta un percorso di scelte fisse, mai un programma che genera risposte;
    - i contenuti pubblicati non citano i programmi usati per scrivere i testi o fare le immagini;
    - niente conteggi dei materiali disponibili (quante schede, quanti giochi) e niente widget di valutazione delle pagine;
    - i colori dell'allerta (verde, giallo, arancione, rosso) sono quelli del sistema nazionale di protezione civile e non si cambiano;
    - il Gruppo non interviene su chiamata dei cittadini: in emergenza si chiama il 112.
  - Niente dati personali nel file. Niente testi copiati da siti di terzi: si citano solo frasi brevi del sito che si sta valutando, come prova.

  ## 5. Controlli
  - `test -f riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-f.md && echo presente` stampa «presente».
  - `grep -cE "^## [1-6]\. " riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-f.md` stampa 6.
  - `grep -c "^### R[0-9]" riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-f.md` stampa un numero maggiore di 0, e ogni rilievo ha le righe «Dove», «Che cosa non va», «Prova», «Priorità» ed «Esito».
  - `python3 -c "import importlib.util as u; s=u.spec_from_file_location('l','scripts/lavoratore-ai.py'); m=u.module_from_spec(s); s.loader.exec_module(m); t=open('riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-f.md',encoding='utf-8').read(); print(len(m.VIETATE.findall(t))+len(m.VIETATE_SIGLE.findall(t)))"` stampa 0 (nessun nome di strumento nel file).
  - `git status --porcelain` elenca solo il file del punto 2.

  ## 6. Consegna
  Solo il file del punto 2. Alla fine un riassunto breve: fatto, non fatto e perché, controlli eseguiti con l'esito. `COORDINAMENTO.md` non si tocca: l'esito in bacheca lo scrive chi chiude il lavoro.

  ## 7. Che cosa non fare
  - Non correggere nulla del sito né del repository: chi fa l'audit non corregge, le correzioni le fa chi verifica i rilievi.
  - Non toccare file fuori dall'elenco del punto 2; non unire nulla, non aprire e non segnare pronta nessuna pull request.
  - Non inventare dati, misure, punteggi, norme o citazioni: se una cosa non si può verificare, va nel § 6 del file.
  - Non mandare dati del repository o del sito a servizi esterni, salvo le richieste al sito pubblicato del passo 3.

- **2026-11-07 — da Claude a GLM automatico — Audit completo del sito, revisore E**
  ## 1. Obiettivo
  Un audit completo e indipendente del sito della Protezione Civile di Genzano di Roma (https://www.protezionecivilegenzano.it/) e del suo repository, con i punti di forza (pro), i punti deboli (contro) e i consigli per migliorarlo, scritto in un solo file. Serve ad Alessandro per confrontare il parere di più revisori, ognuno con il proprio audit, e decidere che cosa migliorare.

  ## 2. File
  - `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-e.md` (da creare). Nessun altro file si crea o si modifica.

  ## 3. Che cosa fare
  1. Per prima cosa crea il file con lo scheletro delle sezioni del passo 6 e riempilo man mano: se il lavoro si interrompe, ciò che hai già scritto resta.
  2. Raccogli le prove solo da queste fonti:
     - il sito pubblicato, con richieste vere: `curl -sS -L -A "Mozilla/5.0" -o /tmp/pagina.html -w "%{http_code} %{size_download}\n" URL` per pagina e peso, `curl -sSI URL` per le intestazioni HTTP; l'elenco delle pagine è in https://www.protezionecivilegenzano.it/sitemap.xml;
     - il repository: template in `themes/flavour-pcgenzano/layouts/`, CSS e JavaScript in `themes/flavour-pcgenzano/static/` e `static/`, contenuti in `content/`, dati in `data/`, script in `scripts/`, automazioni in `.github/workflows/`;
     - i rapporti già fatti in `riferimenti-interni/audit-esterni/` e `riferimenti-interni/audit-interni/`: non ripetere un rilievo già segnato come corretto, salvo che tu lo ritrovi ancora sul sito pubblicato (in quel caso scrivilo).
  3. Guarda almeno queste pagine del sito pubblicato: `/`, `/emergenza/`, `/cosa-fare-adesso/`, `/allerte-meteo/`, `/numeri-utili/`, `/rischi-prevenzione/rischio-sismico/`, `/piano-emergenza/`, `/aree-attesa/`, `/cruscotto/`, `/monitor/`, `/assistente/`, `/comunicazioni/` e l'articolo più recente che trovi lì, `/formazione/`, `/giochi/`, `/lim/`, `/diventa-volontario/`, `/chi-siamo/`, `/contatti/`, `/accessibilita/`, `/privacy/`, `/open-data/`, `/cerca/`, `/english/`, `/facile-da-leggere/`, `/mappa-sito/`. Puoi aggiungerne altre. Fai al massimo 200 richieste al sito, una al secondo: è su un hosting condiviso.
  4. Valuta questi ambiti, uno per uno: (a) informazioni d'emergenza e allerta, chiare per il cittadino; (b) contenuti: correttezza, fonti, coerenza fra pagine diverse, aggiornamento; (c) navigazione, ricerca, organizzazione delle pagine; (d) accessibilità secondo WCAG 2.2 livello AA (titoli, testi alternativi, etichette, contrasti, uso da tastiera, nomi accessibili dei comandi); (e) peso e velocità delle pagine su rete mobile; (f) motori di ricerca e dati strutturati; (g) sicurezza (HTTPS, intestazioni HTTP, Content-Security-Policy) e privacy; (h) materiali per le scuole e uso sulla lavagna interattiva; (i) affidabilità tecnica: build, automazioni, controlli; (j) grafica e identità.
  5. Se nel tuo ambiente puoi aprire le pagine con un browser, provale anche lì (per esempio con un controllo di accessibilità automatico); se non puoi, controlla l'HTML e scrivi nel § 2 del file che la prova nel browser non è stata fatta. Se il sito non risponde dal tuo ambiente, fai l'audit sul solo repository e scrivilo nel § 2.
  6. Il file ha esattamente queste sezioni, con questi titoli:
     - `# Audit completo del sito — revisore E`
     - `## 1. Giudizio complessivo`: da 5 a 10 righe, senza punteggi o percentuali che non hai misurato.
     - `## 2. Perimetro e metodo`: data e ora italiane delle misure, pagine e file guardati, comandi usati, che cosa non hai potuto verificare e perché.
     - `## 3. Pro: punti di forza`: elenco numerato, almeno 5 punti, ognuno con la sua prova.
     - `## 4. Contro: punti deboli`: un rilievo per titolo `### R1 — <titolo breve>`, `### R2 — …`, ciascuno con le cinque voci del formato di `riferimenti-interni/audit-esterni/README.md`: «Dove», «Che cosa non va», «Prova», «Priorità» (P1 sbagliato o pericoloso per il cittadino · P2 da correggere · P3 miglioramento) ed «Esito», dove scrivi «(da compilare da chi verifica)».
     - `## 5. Consigli per migliorarlo`: elenco numerato in ordine di importanza; per ogni consiglio una riga «Perché», una riga «Impegno» (piccolo, medio o grande) e i rilievi del § 4 che risolve, se ce ne sono. Solo consigli gratuiti e compatibili con i vincoli del punto 4.
     - `## 6. Domande e dubbi`: ciò che non hai potuto chiarire.
  7. Ogni punto di forza e ogni rilievo ha una prova verificabile: l'URL con il risultato della richiesta (codice HTTP, misura, frase esatta copiata dalla pagina), oppure il percorso del file con il numero di riga. Quello che non hai verificato non si scrive. Meglio otto rilievi provati che trenta senza prova.
  8. Prima di finire rileggi il file come un revisore ostile che vuole smentirti: ricontrolla ogni prova, togli ciò che non regge, controlla che i consigli rispettino i vincoli del punto 4.

  ## 4. Vincoli
  - Il file è in italiano chiaro, con frasi brevi. Nel file non compaiono nomi di programmi o di servizi usati per fare il lavoro: la firma è «revisore E».
  - I consigli rispettano queste decisioni del progetto, che non si rimettono in discussione:
    - budget zero: solo interventi gratuiti, senza servizi, piani o licenze a pagamento;
    - sito statico generato con Hugo e Bootstrap Italia, senza backend, CMS o database;
    - solo JavaScript senza framework; nelle pagine per le scuole, JavaScript compatibile con ECMAScript 2018;
    - niente app installabile, niente service worker, niente funzionamento offline basato sulla cache del browser;
    - la cache HTTP è disattivata per scelta (intestazioni `no-store`): non proporre di riattivarla; se un controllo automatico la segnala, è una conseguenza nota, non un rilievo;
    - nessuna modifica al CSS della barra di navigazione di Bootstrap Italia;
    - niente overlay di accessibilità commerciali; l'assistente del sito resta un percorso di scelte fisse, mai un programma che genera risposte;
    - i contenuti pubblicati non citano i programmi usati per scrivere i testi o fare le immagini;
    - niente conteggi dei materiali disponibili (quante schede, quanti giochi) e niente widget di valutazione delle pagine;
    - i colori dell'allerta (verde, giallo, arancione, rosso) sono quelli del sistema nazionale di protezione civile e non si cambiano;
    - il Gruppo non interviene su chiamata dei cittadini: in emergenza si chiama il 112.
  - Niente dati personali nel file. Niente testi copiati da siti di terzi: si citano solo frasi brevi del sito che si sta valutando, come prova.

  ## 5. Controlli
  - `test -f riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-e.md && echo presente` stampa «presente».
  - `grep -cE "^## [1-6]\. " riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-e.md` stampa 6.
  - `grep -c "^### R[0-9]" riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-e.md` stampa un numero maggiore di 0, e ogni rilievo ha le righe «Dove», «Che cosa non va», «Prova», «Priorità» ed «Esito».
  - `python3 -c "import importlib.util as u; s=u.spec_from_file_location('l','scripts/lavoratore-ai.py'); m=u.module_from_spec(s); s.loader.exec_module(m); t=open('riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-e.md',encoding='utf-8').read(); print(len(m.VIETATE.findall(t))+len(m.VIETATE_SIGLE.findall(t)))"` stampa 0 (nessun nome di strumento nel file).
  - `git status --porcelain` elenca solo il file del punto 2.

  ## 6. Consegna
  Solo il file del punto 2. Alla fine un riassunto breve: fatto, non fatto e perché, controlli eseguiti con l'esito. `COORDINAMENTO.md` non si tocca: l'esito in bacheca lo scrive chi chiude il lavoro.

  ## 7. Che cosa non fare
  - Non correggere nulla del sito né del repository: chi fa l'audit non corregge, le correzioni le fa chi verifica i rilievi.
  - Non toccare file fuori dall'elenco del punto 2; non unire nulla, non aprire e non segnare pronta nessuna pull request.
  - Non inventare dati, misure, punteggi, norme o citazioni: se una cosa non si può verificare, va nel § 6 del file.
  - Non mandare dati del repository o del sito a servizi esterni, salvo le richieste al sito pubblicato del passo 3.

- **2026-11-07 — da Claude a Qwen automatico — Audit completo del sito, revisore G**
  ## 1. Obiettivo
  Un audit completo e indipendente del sito della Protezione Civile di Genzano di Roma (https://www.protezionecivilegenzano.it/) e del suo repository, con i punti di forza (pro), i punti deboli (contro) e i consigli per migliorarlo, scritto in un solo file. Serve ad Alessandro per confrontare il parere di più revisori, ognuno con il proprio audit, e decidere che cosa migliorare.

  ## 2. File
  - `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-g.md` (da creare). Nessun altro file si crea o si modifica.

  ## 3. Che cosa fare
  1. Per prima cosa crea il file con lo scheletro delle sezioni del passo 6 e riempilo man mano: se il lavoro si interrompe, ciò che hai già scritto resta.
  2. Raccogli le prove solo da queste fonti:
     - il sito pubblicato, con richieste vere: `curl -sS -L -A "Mozilla/5.0" -o /tmp/pagina.html -w "%{http_code} %{size_download}\n" URL` per pagina e peso, `curl -sSI URL` per le intestazioni HTTP; l'elenco delle pagine è in https://www.protezionecivilegenzano.it/sitemap.xml;
     - il repository: template in `themes/flavour-pcgenzano/layouts/`, CSS e JavaScript in `themes/flavour-pcgenzano/static/` e `static/`, contenuti in `content/`, dati in `data/`, script in `scripts/`, automazioni in `.github/workflows/`;
     - i rapporti già fatti in `riferimenti-interni/audit-esterni/` e `riferimenti-interni/audit-interni/`: non ripetere un rilievo già segnato come corretto, salvo che tu lo ritrovi ancora sul sito pubblicato (in quel caso scrivilo).
  3. Guarda almeno queste pagine del sito pubblicato: `/`, `/emergenza/`, `/cosa-fare-adesso/`, `/allerte-meteo/`, `/numeri-utili/`, `/rischi-prevenzione/rischio-sismico/`, `/piano-emergenza/`, `/aree-attesa/`, `/cruscotto/`, `/monitor/`, `/assistente/`, `/comunicazioni/` e l'articolo più recente che trovi lì, `/formazione/`, `/giochi/`, `/lim/`, `/diventa-volontario/`, `/chi-siamo/`, `/contatti/`, `/accessibilita/`, `/privacy/`, `/open-data/`, `/cerca/`, `/english/`, `/facile-da-leggere/`, `/mappa-sito/`. Puoi aggiungerne altre. Fai al massimo 200 richieste al sito, una al secondo: è su un hosting condiviso.
  4. Valuta questi ambiti, uno per uno: (a) informazioni d'emergenza e allerta, chiare per il cittadino; (b) contenuti: correttezza, fonti, coerenza fra pagine diverse, aggiornamento; (c) navigazione, ricerca, organizzazione delle pagine; (d) accessibilità secondo WCAG 2.2 livello AA (titoli, testi alternativi, etichette, contrasti, uso da tastiera, nomi accessibili dei comandi); (e) peso e velocità delle pagine su rete mobile; (f) motori di ricerca e dati strutturati; (g) sicurezza (HTTPS, intestazioni HTTP, Content-Security-Policy) e privacy; (h) materiali per le scuole e uso sulla lavagna interattiva; (i) affidabilità tecnica: build, automazioni, controlli; (j) grafica e identità.
  5. Se nel tuo ambiente puoi aprire le pagine con un browser, provale anche lì (per esempio con un controllo di accessibilità automatico); se non puoi, controlla l'HTML e scrivi nel § 2 del file che la prova nel browser non è stata fatta. Se il sito non risponde dal tuo ambiente, fai l'audit sul solo repository e scrivilo nel § 2.
  6. Il file ha esattamente queste sezioni, con questi titoli:
     - `# Audit completo del sito — revisore G`
     - `## 1. Giudizio complessivo`: da 5 a 10 righe, senza punteggi o percentuali che non hai misurato.
     - `## 2. Perimetro e metodo`: data e ora italiane delle misure, pagine e file guardati, comandi usati, che cosa non hai potuto verificare e perché.
     - `## 3. Pro: punti di forza`: elenco numerato, almeno 5 punti, ognuno con la sua prova.
     - `## 4. Contro: punti deboli`: un rilievo per titolo `### R1 — <titolo breve>`, `### R2 — …`, ciascuno con le cinque voci del formato di `riferimenti-interni/audit-esterni/README.md`: «Dove», «Che cosa non va», «Prova», «Priorità» (P1 sbagliato o pericoloso per il cittadino · P2 da correggere · P3 miglioramento) ed «Esito», dove scrivi «(da compilare da chi verifica)».
     - `## 5. Consigli per migliorarlo`: elenco numerato in ordine di importanza; per ogni consiglio una riga «Perché», una riga «Impegno» (piccolo, medio o grande) e i rilievi del § 4 che risolve, se ce ne sono. Solo consigli gratuiti e compatibili con i vincoli del punto 4.
     - `## 6. Domande e dubbi`: ciò che non hai potuto chiarire.
  7. Ogni punto di forza e ogni rilievo ha una prova verificabile: l'URL con il risultato della richiesta (codice HTTP, misura, frase esatta copiata dalla pagina), oppure il percorso del file con il numero di riga. Quello che non hai verificato non si scrive. Meglio otto rilievi provati che trenta senza prova.
  8. Prima di finire rileggi il file come un revisore ostile che vuole smentirti: ricontrolla ogni prova, togli ciò che non regge, controlla che i consigli rispettino i vincoli del punto 4.

  ## 4. Vincoli
  - Il file è in italiano chiaro, con frasi brevi. Nel file non compaiono nomi di programmi o di servizi usati per fare il lavoro: la firma è «revisore G».
  - I consigli rispettano queste decisioni del progetto, che non si rimettono in discussione:
    - budget zero: solo interventi gratuiti, senza servizi, piani o licenze a pagamento;
    - sito statico generato con Hugo e Bootstrap Italia, senza backend, CMS o database;
    - solo JavaScript senza framework; nelle pagine per le scuole, JavaScript compatibile con ECMAScript 2018;
    - niente app installabile, niente service worker, niente funzionamento offline basato sulla cache del browser;
    - la cache HTTP è disattivata per scelta (intestazioni `no-store`): non proporre di riattivarla; se un controllo automatico la segnala, è una conseguenza nota, non un rilievo;
    - nessuna modifica al CSS della barra di navigazione di Bootstrap Italia;
    - niente overlay di accessibilità commerciali; l'assistente del sito resta un percorso di scelte fisse, mai un programma che genera risposte;
    - i contenuti pubblicati non citano i programmi usati per scrivere i testi o fare le immagini;
    - niente conteggi dei materiali disponibili (quante schede, quanti giochi) e niente widget di valutazione delle pagine;
    - i colori dell'allerta (verde, giallo, arancione, rosso) sono quelli del sistema nazionale di protezione civile e non si cambiano;
    - il Gruppo non interviene su chiamata dei cittadini: in emergenza si chiama il 112.
  - Niente dati personali nel file. Niente testi copiati da siti di terzi: si citano solo frasi brevi del sito che si sta valutando, come prova.

  ## 5. Controlli
  - `test -f riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-g.md && echo presente` stampa «presente».
  - `grep -cE "^## [1-6]\. " riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-g.md` stampa 6.
  - `grep -c "^### R[0-9]" riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-g.md` stampa un numero maggiore di 0, e ogni rilievo ha le righe «Dove», «Che cosa non va», «Prova», «Priorità» ed «Esito».
  - `python3 -c "import importlib.util as u; s=u.spec_from_file_location('l','scripts/lavoratore-ai.py'); m=u.module_from_spec(s); s.loader.exec_module(m); t=open('riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-g.md',encoding='utf-8').read(); print(len(m.VIETATE.findall(t))+len(m.VIETATE_SIGLE.findall(t)))"` stampa 0 (nessun nome di strumento nel file).
  - `git status --porcelain` elenca solo il file del punto 2.

  ## 6. Consegna
  Solo il file del punto 2. Alla fine un riassunto breve: fatto, non fatto e perché, controlli eseguiti con l'esito. `COORDINAMENTO.md` non si tocca: l'esito in bacheca lo scrive chi chiude il lavoro.

  ## 7. Che cosa non fare
  - Non correggere nulla del sito né del repository: chi fa l'audit non corregge, le correzioni le fa chi verifica i rilievi.
  - Non toccare file fuori dall'elenco del punto 2; non unire nulla, non aprire e non segnare pronta nessuna pull request.
  - Non inventare dati, misure, punteggi, norme o citazioni: se una cosa non si può verificare, va nel § 6 del file.
  - Non mandare dati del repository o del sito a servizi esterni, salvo le richieste al sito pubblicato del passo 3.

- **2026-11-07 — da Claude a Gemini automatico — Audit completo del sito, revisore B, secondo tentativo**
  ## 1. Obiettivo
  Un audit completo e indipendente del sito della Protezione Civile di Genzano di Roma (https://www.protezionecivilegenzano.it/) e del suo repository, con i punti di forza (pro), i punti deboli (contro) e i consigli per migliorarlo, scritto in un solo file. Serve ad Alessandro per confrontare il parere di più revisori, ognuno con il proprio audit, e decidere che cosa migliorare.

  ## 2. File
  - `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-b.md` (da creare). Nessun altro file si crea o si modifica.

  ## 3. Che cosa fare
  Prima di cominciare: la quota gratuita del tuo servizio è di circa 20 richieste al giorno per modello, e il primo tentativo del 7 novembre si è fermato dopo lo scheletro. Lavora quindi a blocchi grandi, con pochi passi: un solo comando scarica in `/tmp/audit/` tutte le pagine del passo 3 con le loro intestazioni e stampa per ognuna codice HTTP, peso, titolo, h1 e descrizione; un secondo comando legge insieme i file del repository che ti servono; scrivi il file intero in una o due volte; esegui tutti i controlli della parte 5 in un solo comando.
  1. Per prima cosa crea il file con lo scheletro delle sezioni del passo 6 e riempilo man mano: se il lavoro si interrompe, ciò che hai già scritto resta.
  2. Raccogli le prove solo da queste fonti:
     - il sito pubblicato, con richieste vere: `curl -sS -L -A "Mozilla/5.0" -o /tmp/pagina.html -w "%{http_code} %{size_download}\n" URL` per pagina e peso, `curl -sSI URL` per le intestazioni HTTP; l'elenco delle pagine è in https://www.protezionecivilegenzano.it/sitemap.xml;
     - il repository: template in `themes/flavour-pcgenzano/layouts/`, CSS e JavaScript in `themes/flavour-pcgenzano/static/` e `static/`, contenuti in `content/`, dati in `data/`, script in `scripts/`, automazioni in `.github/workflows/`;
     - i rapporti già fatti in `riferimenti-interni/audit-esterni/` e `riferimenti-interni/audit-interni/`: non ripetere un rilievo già segnato come corretto, salvo che tu lo ritrovi ancora sul sito pubblicato (in quel caso scrivilo).
  3. Guarda almeno queste pagine del sito pubblicato: `/`, `/emergenza/`, `/cosa-fare-adesso/`, `/allerte-meteo/`, `/numeri-utili/`, `/rischi-prevenzione/rischio-sismico/`, `/piano-emergenza/`, `/aree-attesa/`, `/cruscotto/`, `/monitor/`, `/assistente/`, `/comunicazioni/` e l'articolo più recente che trovi lì, `/formazione/`, `/giochi/`, `/lim/`, `/diventa-volontario/`, `/chi-siamo/`, `/contatti/`, `/accessibilita/`, `/privacy/`, `/open-data/`, `/cerca/`, `/english/`, `/facile-da-leggere/`, `/mappa-sito/`. Puoi aggiungerne altre. Fai al massimo 200 richieste al sito, una al secondo: è su un hosting condiviso.
  4. Valuta questi ambiti, uno per uno: (a) informazioni d'emergenza e allerta, chiare per il cittadino; (b) contenuti: correttezza, fonti, coerenza fra pagine diverse, aggiornamento; (c) navigazione, ricerca, organizzazione delle pagine; (d) accessibilità secondo WCAG 2.2 livello AA (titoli, testi alternativi, etichette, contrasti, uso da tastiera, nomi accessibili dei comandi); (e) peso e velocità delle pagine su rete mobile; (f) motori di ricerca e dati strutturati; (g) sicurezza (HTTPS, intestazioni HTTP, Content-Security-Policy) e privacy; (h) materiali per le scuole e uso sulla lavagna interattiva; (i) affidabilità tecnica: build, automazioni, controlli; (j) grafica e identità.
  5. Se nel tuo ambiente puoi aprire le pagine con un browser, provale anche lì (per esempio con un controllo di accessibilità automatico); se non puoi, controlla l'HTML e scrivi nel § 2 del file che la prova nel browser non è stata fatta. Se il sito non risponde dal tuo ambiente, fai l'audit sul solo repository e scrivilo nel § 2.
  6. Il file ha esattamente queste sezioni, con questi titoli:
     - `# Audit completo del sito — revisore B`
     - `## 1. Giudizio complessivo`: da 5 a 10 righe, senza punteggi o percentuali che non hai misurato.
     - `## 2. Perimetro e metodo`: data e ora italiane delle misure, pagine e file guardati, comandi usati, che cosa non hai potuto verificare e perché.
     - `## 3. Pro: punti di forza`: elenco numerato, almeno 5 punti, ognuno con la sua prova.
     - `## 4. Contro: punti deboli`: un rilievo per titolo `### R1 — <titolo breve>`, `### R2 — …`, ciascuno con le cinque voci del formato di `riferimenti-interni/audit-esterni/README.md`: «Dove», «Che cosa non va», «Prova», «Priorità» (P1 sbagliato o pericoloso per il cittadino · P2 da correggere · P3 miglioramento) ed «Esito», dove scrivi «(da compilare da chi verifica)».
     - `## 5. Consigli per migliorarlo`: elenco numerato in ordine di importanza; per ogni consiglio una riga «Perché», una riga «Impegno» (piccolo, medio o grande) e i rilievi del § 4 che risolve, se ce ne sono. Solo consigli gratuiti e compatibili con i vincoli del punto 4.
     - `## 6. Domande e dubbi`: ciò che non hai potuto chiarire.
  7. Ogni punto di forza e ogni rilievo ha una prova verificabile: l'URL con il risultato della richiesta (codice HTTP, misura, frase esatta copiata dalla pagina), oppure il percorso del file con il numero di riga. Quello che non hai verificato non si scrive. Meglio otto rilievi provati che trenta senza prova.
  8. Prima di finire rileggi il file come un revisore ostile che vuole smentirti: ricontrolla ogni prova, togli ciò che non regge, controlla che i consigli rispettino i vincoli del punto 4.

  ## 4. Vincoli
  - Il file è in italiano chiaro, con frasi brevi. Nel file non compaiono nomi di programmi o di servizi usati per fare il lavoro: la firma è «revisore B».
  - I consigli rispettano queste decisioni del progetto, che non si rimettono in discussione:
    - budget zero: solo interventi gratuiti, senza servizi, piani o licenze a pagamento;
    - sito statico generato con Hugo e Bootstrap Italia, senza backend, CMS o database;
    - solo JavaScript senza framework; nelle pagine per le scuole, JavaScript compatibile con ECMAScript 2018;
    - niente app installabile, niente service worker, niente funzionamento offline basato sulla cache del browser;
    - la cache HTTP è disattivata per scelta (intestazioni `no-store`): non proporre di riattivarla; se un controllo automatico la segnala, è una conseguenza nota, non un rilievo;
    - nessuna modifica al CSS della barra di navigazione di Bootstrap Italia;
    - niente overlay di accessibilità commerciali; l'assistente del sito resta un percorso di scelte fisse, mai un programma che genera risposte;
    - i contenuti pubblicati non citano i programmi usati per scrivere i testi o fare le immagini;
    - niente conteggi dei materiali disponibili (quante schede, quanti giochi) e niente widget di valutazione delle pagine;
    - i colori dell'allerta (verde, giallo, arancione, rosso) sono quelli del sistema nazionale di protezione civile e non si cambiano;
    - il Gruppo non interviene su chiamata dei cittadini: in emergenza si chiama il 112.
  - Niente dati personali nel file. Niente testi copiati da siti di terzi: si citano solo frasi brevi del sito che si sta valutando, come prova.

  ## 5. Controlli
  - `test -f riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-b.md && echo presente` stampa «presente».
  - `grep -cE "^## [1-6]\. " riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-b.md` stampa 6.
  - `grep -c "^### R[0-9]" riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-b.md` stampa un numero maggiore di 0, e ogni rilievo ha le righe «Dove», «Che cosa non va», «Prova», «Priorità» ed «Esito».
  - `python3 -c "import importlib.util as u; s=u.spec_from_file_location('l','scripts/lavoratore-ai.py'); m=u.module_from_spec(s); s.loader.exec_module(m); t=open('riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-b.md',encoding='utf-8').read(); print(len(m.VIETATE.findall(t))+len(m.VIETATE_SIGLE.findall(t)))"` stampa 0 (nessun nome di strumento nel file).
  - `git status --porcelain` elenca solo il file del punto 2.

  ## 6. Consegna
  Solo il file del punto 2. Alla fine un riassunto breve: fatto, non fatto e perché, controlli eseguiti con l'esito. `COORDINAMENTO.md` non si tocca: l'esito in bacheca lo scrive chi chiude il lavoro.

  ## 7. Che cosa non fare
  - Non correggere nulla del sito né del repository: chi fa l'audit non corregge, le correzioni le fa chi verifica i rilievi.
  - Non toccare file fuori dall'elenco del punto 2; non unire nulla, non aprire e non segnare pronta nessuna pull request.
  - Non inventare dati, misure, punteggi, norme o citazioni: se una cosa non si può verificare, va nel § 6 del file.
  - Non mandare dati del repository o del sito a servizi esterni, salvo le richieste al sito pubblicato del passo 3.

- **2026-11-07 — da Claude a ChatGPT — Audit completo del sito, revisore C** (preparata da Claude, da avviare a mano in Codex Cloud; PR #1749; ramo `chatgpt/audit-completo-revisore-c-20261107`)
  - **Avvio a mano (Alessandro).** In Codex Cloud, ambiente «sito-pc-genzano», ramo principale, incolla una riga: «Leggi COORDINAMENTO.md ed esegui la richiesta della PR #1749.». A lavoro finito, «Create PR» dal task: la pull request di consegna la porta nel ramo e la chiude `passa-a.py chiudi --pr 1749 --consegna M`.
  - **Per chi la esegue.** Esegui le sette parti qui sotto, punto per punto. Non toccare `COORDINAMENTO.md`, non unire e non segnare pronta nessuna pull request; alla fine scrivi un riassunto: fatto, non fatto e perché, controlli eseguiti con l'esito.
  - **1. Obiettivo.**
    Un audit completo e indipendente del sito della Protezione Civile di Genzano di Roma (https://www.protezionecivilegenzano.it/) e del suo repository, con i punti di forza (pro), i punti deboli (contro) e i consigli per migliorarlo, scritto in un solo file. Serve ad Alessandro per confrontare il parere di più revisori, ognuno con il proprio audit, e decidere che cosa migliorare.
  - **2. File.**
    - `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-c.md` (da creare). Nessun altro file si crea o si modifica.
  - **3. Che cosa fare.**
    1. Per prima cosa crea il file con lo scheletro delle sezioni del passo 6 e riempilo man mano: se il lavoro si interrompe, ciò che hai già scritto resta.
    2. Raccogli le prove solo da queste fonti:
       - il sito pubblicato, con richieste vere: `curl -sS -L -A "Mozilla/5.0" -o /tmp/pagina.html -w "%{http_code} %{size_download}\n" URL` per pagina e peso, `curl -sSI URL` per le intestazioni HTTP; l'elenco delle pagine è in https://www.protezionecivilegenzano.it/sitemap.xml;
       - il repository: template in `themes/flavour-pcgenzano/layouts/`, CSS e JavaScript in `themes/flavour-pcgenzano/static/` e `static/`, contenuti in `content/`, dati in `data/`, script in `scripts/`, automazioni in `.github/workflows/`;
       - i rapporti già fatti in `riferimenti-interni/audit-esterni/` e `riferimenti-interni/audit-interni/`: non ripetere un rilievo già segnato come corretto, salvo che tu lo ritrovi ancora sul sito pubblicato (in quel caso scrivilo).
    3. Guarda almeno queste pagine del sito pubblicato: `/`, `/emergenza/`, `/cosa-fare-adesso/`, `/allerte-meteo/`, `/numeri-utili/`, `/rischi-prevenzione/rischio-sismico/`, `/piano-emergenza/`, `/aree-attesa/`, `/cruscotto/`, `/monitor/`, `/assistente/`, `/comunicazioni/` e l'articolo più recente che trovi lì, `/formazione/`, `/giochi/`, `/lim/`, `/diventa-volontario/`, `/chi-siamo/`, `/contatti/`, `/accessibilita/`, `/privacy/`, `/open-data/`, `/cerca/`, `/english/`, `/facile-da-leggere/`, `/mappa-sito/`. Puoi aggiungerne altre. Fai al massimo 200 richieste al sito, una al secondo: è su un hosting condiviso.
    4. Valuta questi ambiti, uno per uno: (a) informazioni d'emergenza e allerta, chiare per il cittadino; (b) contenuti: correttezza, fonti, coerenza fra pagine diverse, aggiornamento; (c) navigazione, ricerca, organizzazione delle pagine; (d) accessibilità secondo WCAG 2.2 livello AA (titoli, testi alternativi, etichette, contrasti, uso da tastiera, nomi accessibili dei comandi); (e) peso e velocità delle pagine su rete mobile; (f) motori di ricerca e dati strutturati; (g) sicurezza (HTTPS, intestazioni HTTP, Content-Security-Policy) e privacy; (h) materiali per le scuole e uso sulla lavagna interattiva; (i) affidabilità tecnica: build, automazioni, controlli; (j) grafica e identità.
    5. Se nel tuo ambiente puoi aprire le pagine con un browser, provale anche lì (per esempio con un controllo di accessibilità automatico); se non puoi, controlla l'HTML e scrivi nel § 2 del file che la prova nel browser non è stata fatta. Se il sito non risponde dal tuo ambiente, fai l'audit sul solo repository e scrivilo nel § 2.
    6. Il file ha esattamente queste sezioni, con questi titoli:
       - `# Audit completo del sito — revisore C`
       - `## 1. Giudizio complessivo`: da 5 a 10 righe, senza punteggi o percentuali che non hai misurato.
       - `## 2. Perimetro e metodo`: data e ora italiane delle misure, pagine e file guardati, comandi usati, che cosa non hai potuto verificare e perché.
       - `## 3. Pro: punti di forza`: elenco numerato, almeno 5 punti, ognuno con la sua prova.
       - `## 4. Contro: punti deboli`: un rilievo per titolo `### R1 — <titolo breve>`, `### R2 — …`, ciascuno con le cinque voci del formato di `riferimenti-interni/audit-esterni/README.md`: «Dove», «Che cosa non va», «Prova», «Priorità» (P1 sbagliato o pericoloso per il cittadino · P2 da correggere · P3 miglioramento) ed «Esito», dove scrivi «(da compilare da chi verifica)».
       - `## 5. Consigli per migliorarlo`: elenco numerato in ordine di importanza; per ogni consiglio una riga «Perché», una riga «Impegno» (piccolo, medio o grande) e i rilievi del § 4 che risolve, se ce ne sono. Solo consigli gratuiti e compatibili con i vincoli del punto 4.
       - `## 6. Domande e dubbi`: ciò che non hai potuto chiarire.
    7. Ogni punto di forza e ogni rilievo ha una prova verificabile: l'URL con il risultato della richiesta (codice HTTP, misura, frase esatta copiata dalla pagina), oppure il percorso del file con il numero di riga. Quello che non hai verificato non si scrive. Meglio otto rilievi provati che trenta senza prova.
    8. Prima di finire rileggi il file come un revisore ostile che vuole smentirti: ricontrolla ogni prova, togli ciò che non regge, controlla che i consigli rispettino i vincoli del punto 4.
  - **4. Vincoli.**
    - Il file è in italiano chiaro, con frasi brevi. Nel file non compaiono nomi di programmi o di servizi usati per fare il lavoro: la firma è «revisore C».
    - I consigli rispettano queste decisioni del progetto, che non si rimettono in discussione:
      - budget zero: solo interventi gratuiti, senza servizi, piani o licenze a pagamento;
      - sito statico generato con Hugo e Bootstrap Italia, senza backend, CMS o database;
      - solo JavaScript senza framework; nelle pagine per le scuole, JavaScript compatibile con ECMAScript 2018;
      - niente app installabile, niente service worker, niente funzionamento offline basato sulla cache del browser;
      - la cache HTTP è disattivata per scelta (intestazioni `no-store`): non proporre di riattivarla; se un controllo automatico la segnala, è una conseguenza nota, non un rilievo;
      - nessuna modifica al CSS della barra di navigazione di Bootstrap Italia;
      - niente overlay di accessibilità commerciali; l'assistente del sito resta un percorso di scelte fisse, mai un programma che genera risposte;
      - i contenuti pubblicati non citano i programmi usati per scrivere i testi o fare le immagini;
      - niente conteggi dei materiali disponibili (quante schede, quanti giochi) e niente widget di valutazione delle pagine;
      - i colori dell'allerta (verde, giallo, arancione, rosso) sono quelli del sistema nazionale di protezione civile e non si cambiano;
      - il Gruppo non interviene su chiamata dei cittadini: in emergenza si chiama il 112.
    - Niente dati personali nel file. Niente testi copiati da siti di terzi: si citano solo frasi brevi del sito che si sta valutando, come prova.
  - **5. Controlli.**
    - `test -f riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-c.md && echo presente` stampa «presente».
    - `grep -cE "^## [1-6]\. " riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-c.md` stampa 6.
    - `grep -c "^### R[0-9]" riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-c.md` stampa un numero maggiore di 0, e ogni rilievo ha le righe «Dove», «Che cosa non va», «Prova», «Priorità» ed «Esito».
    - `python3 -c "import importlib.util as u; s=u.spec_from_file_location('l','scripts/lavoratore-ai.py'); m=u.module_from_spec(s); s.loader.exec_module(m); t=open('riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-c.md',encoding='utf-8').read(); print(len(m.VIETATE.findall(t))+len(m.VIETATE_SIGLE.findall(t)))"` stampa 0 (nessun nome di strumento nel file).
    - `git status --porcelain` elenca solo il file del punto 2.
  - **6. Consegna.**
    Solo il file del punto 2. Alla fine un riassunto breve: fatto, non fatto e perché, controlli eseguiti con l'esito. `COORDINAMENTO.md` non si tocca: l'esito in bacheca lo scrive chi chiude il lavoro.
  - **7. Che cosa non fare.**
    - Non correggere nulla del sito né del repository: chi fa l'audit non corregge, le correzioni le fa chi verifica i rilievi.
    - Non toccare file fuori dall'elenco del punto 2; non unire nulla, non aprire e non segnare pronta nessuna pull request.
    - Non inventare dati, misure, punteggi, norme o citazioni: se una cosa non si può verificare, va nel § 6 del file.
    - Non mandare dati del repository o del sito a servizi esterni, salvo le richieste al sito pubblicato del passo 3.

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

- **05/11/2026 — Claude.** AI automatiche a prova di guasto (protocollo comune, § «AI automatiche e consulto fra AI»), dopo la prima prova vera in `sito-pc-genzano`: Gemini occupato per otto minuti e mezzo, nessun file toccato, e GitHub Actions senza il permesso di aprire la PR. Ora l'AI prova fino a tre modelli in due giri, toglie il ramo se nessuno lavora (la richiesta riparte da sola), riprende i rami dei tentativi falliti, consegna sul ramo anche senza PR con il run verde; la PR la apre chi controlla con `passa-a.py chiudi --ramo auto/…`, da qualunque sessione, anche dal cellulare. In serata la seconda prova: Gemini ha scritto la riga richiesta e poi ha finito la quota gratuita del giorno, con il riassunto rifiutato perché fuori dalle sue cartelle di lavoro; Claude ha rifatto i sei controlli della richiesta e ha chiuso con `chiudi --ramo` da una sessione nel cloud (PR #1726 di `sito-pc-genzano`). Da qui ogni programma può scrivere il riassunto, una quota finita fa passare subito al modello successivo senza secondo giro, e il giro del mattino parte alle 08:23 UTC, dopo l'azzeramento delle quote di Gemini (mezzanotte del Pacifico). Uguale in tutti e cinque i repository.
- **25/10/2026 — ChatGPT, interventi e Memorial Giordano Funari, PR [#1586](https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/pull/1586).** Contenuti approvati da Alessandro in chat il 25 ottobre, inclusi data, terza edizione, piazza Frasconi e presenza del Gruppo al Memorial. Export aggiornato al 22 ottobre, ultimo 212/2026: 211 rapporti approvati, 618,3 ore, 10.642 km, 870 presenze e 33 volontari attivi. Bozze 213 e 214 escluse con le sei presenze. Resoconto unico Genzano/Latina, data del servizio a Latina allineata al registro, tutti gli allegati conservati; Memorial con foto ritagliata, fuori dai conteggi. Controlli locali e automatici superati. Pubblicazione autorizzata con questa sola PR; esito del deploy e verifica live riportati nella descrizione della PR.


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

- **2026-11-05 — da Claude a Gemini automatico — Tabella delle automazioni: riga del lavoratore della bacheca** — presa da Gemini automatico, PR #1726
  - **Esito (05/11/2026).** Lavoro consegnato e unito in `main` con la pull request #1726.
  ## 1. Obiettivo
  Nella tabella dei workflow della regola delle automazioni deve esserci la riga di `lavoratore-ai.yml`, il workflow arrivato con la PR #1721: così la tabella torna a elencare tutti i workflow del repository.

  ## 2. File
  .claude/rules/10-automazioni-github-actions.md

  ## 3. Che cosa fare
  1. Apri `.claude/rules/10-automazioni-github-actions.md` e trova la riga della tabella che comincia con `` | `rimuovi-firma-strumento.yml` | ``: nel file ce n'è una sola.
  2. Subito dopo quella riga, senza righe vuote in mezzo, inserisci la riga che sta fra le due righe `RIGA-INIZIO` e `RIGA-FINE` qui sotto, identica carattere per carattere (apici inversi, virgolette basse «», puntini …, apostrofi e spazi compresi). Le due righe `RIGA-INIZIO` e `RIGA-FINE` non vanno nel file. Nel file la riga comincia con il carattere `|` in prima colonna, come le altre righe della tabella.
  RIGA-INIZIO
  | `lavoratore-ai.yml` | Push su `main` che tocca `COORDINAMENTO.md` + ogni giorno 05:23 UTC + `workflow_dispatch` | **AI automatiche della bacheca** (05/11/2026, kit comune a tutti i repository): `scripts/lavoratore-ai.py` prende da sé le voci di «Richieste» di `COORDINAMENTO.md` indirizzate a «ChatGPT automatico» (Codex con l'accesso ChatGPT di Alessandro), «Gemini automatico» (chiave gratuita della Gemini API) o «DeepSeek/GLM/Kimi/Qwen automatico» (modelli gratuiti di Ollama Cloud) e scritte nelle sette parti di `scripts/passa-a.py modello`; segna la voce presa, fa lavorare il programma dell'AI senza il token di GitHub su un ramo `auto/<ai>-<argomento>-AAAAMMGG` e consegna sul ramo, con esito e riassunto nella voce, più una PR in bozza se il repository permette a GitHub Actions di aprirla. Se il servizio è occupato prova fino a tre modelli, in due giri; se nessun modello lavora toglie il ramo e la richiesta riparte da sola al giro dopo. Le modifiche a `COORDINAMENTO.md` e `.github/` si annullano e un lavoro con un testo simile a una chiave d'accesso non si pubblica. Il lavoro lo controlla e lo chiude Claude con `python3 scripts/passa-a.py chiudi --pr N --qualsiasi --titolo "…" --messaggio "…"` oppure, se la PR non c'è, con `python3 scripts/passa-a.py chiudi --ramo auto/… --titolo "…" --messaggio "…"`, che la apre. I segreti `CHATGPT_ACCESSO`, `GEMINI_API_KEY` e `OLLAMA_API_KEY` e il permesso di aprire PR li mette dal PC `scripts/collega-ai-automatiche.sh` di `assistente-personale`: senza la chiave che serve la richiesta resta aperta e il run è rosso. Ogni 6 giorni il giro del mattino tiene vivo l'accesso ChatGPT. Protocollo comune di `COORDINAMENTO.md`, § «AI automatiche e consulto fra AI». |
  RIGA-FINE
  3. Non cambiare nient'altro: nessun'altra riga del file, nessuno spazio, nessun a capo in più o in meno, nemmeno in fondo al file.

  ## 4. Vincoli
  - Il file è un file di governo interno, non pubblicato sul sito: lì i nomi delle intelligenze artificiali sono ammessi, ma solo quelli già scritti nella riga del punto 3. Non aggiungerne altri.
  - La riga resta una sola riga di tabella con tre celle: nessun carattere «|» dentro le celle, nessun a capo dentro la riga.
  - Niente riformulazioni, correzioni di stile o «miglioramenti» della riga: va copiata così com'è. Se ti sembra che contenga un errore, copiala comunque e scrivilo nel riassunto.

  ## 5. Controlli
  Ogni controllo è un comando di una riga, da eseguire dalla cartella principale del repository.
  1. `git diff --numstat` deve stampare una sola riga, con i numeri `1` e `0` e il nome `.claude/rules/10-automazioni-github-actions.md` (una riga aggiunta, nessuna tolta, un solo file).
  2. `git status --porcelain` deve stampare una sola riga, che finisce con `.claude/rules/10-automazioni-github-actions.md`.
  3. `grep -c '^| `lavoratore-ai.yml` |' .claude/rules/10-automazioni-github-actions.md` deve stampare `1`.
  4. `grep -B1 '^| `lavoratore-ai.yml` |' .claude/rules/10-automazioni-github-actions.md | head -1 | cut -c1-33` deve stampare `` | `rimuovi-firma-strumento.yml` | `` (la riga nuova sta subito dopo quella).
  5. `grep '^| `lavoratore-ai.yml` |' .claude/rules/10-automazioni-github-actions.md | tr -cd '|' | wc -c` deve stampare `4` (tre celle).
  6. `grep -c 'consulto fra AI». |$' .claude/rules/10-automazioni-github-actions.md` deve stampare `1` (la riga finisce come nella richiesta).

  ## 6. Consegna
  Solo la modifica del file del punto 2. Alla fine il riassunto che chiede il sistema: fatto, non fatto e perché, controlli eseguiti con il loro esito, dubbi.

  ## 7. Che cosa non fare
  Non toccare altri file (né `COORDINAMENTO.md`, né `.github/`, né `CLAUDE.md`, né il manuale); non riordinare la tabella; non aggiungere date, numeri di PR o righe diverse da quella del punto 3; non fare commit, push, rami o pull request; non eseguire build del sito o altri controlli lunghi: per questo file bastano i sei controlli del punto 5.
  - **Esito del 05/11/2026, 22:49** — Gemini automatico, modello gemini-3.6-flash: lavoro non riuscito (servizio occupato (modelli provati: gemini-3.8-flash, gemini-3.7-flash, gemini-3.6-flash)); i file toccati fin lì sono nella PR #1726. File toccati: .claude/rules/10-automazioni-github-actions.md.
    ## Fatto
    - Inserita la riga per lavoratore-ai.yml nella tabella dei workflow in .claude/rules/10-automazioni-github-actions.md, subito dopo la riga di rimuovi-firma-strumento.yml.
    ## Non fatto e perché
    - Nessuna voce omessa: la modifica è stata completata esattamente come richiesto.
    ## Controlli eseguiti ed esito
    - git diff --numstat: 1 riga aggiunta, 0 tolte, 1 file modificato (.claude/rules/10-automazioni-github-actions.md). OK.
    - git status --porcelain: solo .claude/rules/10-automazioni-github-actions.md risulta modificato. OK.
    - grep -c ^| lavoratore-ai.yml |: ha restituito 1. OK.
    - grep -B1 ^| lavoratore-ai.yml |: ha restituito | rimuovi-firma-strumento.yml |. OK.
    - Conteggio pipe nella nuova riga: 4 (tre celle). OK.
    - grep -c consulto fra AI». |$: ha restituito 1. OK.
    ## Dubbi e domande per chi controlla
    - Nessun dubbio.

Lavori che una sessione (o Alessandro) chiede all'altra. Dal 13/10/2026 i passaggi a ChatGPT li prepara Claude da sola (protocollo comune, § «Passaggio a ChatGPT»: voce qui sotto con la nota «preparata da Claude, da avviare a mano in Codex Cloud» e PR in bozza) e li avvia Alessandro in Codex Cloud con il testo di avvio; per le richieste a Gemini, e per quelle che Alessandro scrive qui a mano, resta l'avviso «guarda la bacheca». Formato nel protocollo comune. Dal 05/11/2026 la voce di ogni passaggio sta anche qui sul ramo principale, e per avviarla in Codex Cloud basta una riga: «Leggi COORDINAMENTO.md ed esegui la richiesta della PR #N.» (§ «Passaggi a ChatGPT in questo repository»).

- **2026-11-05 — da Claude a ChatGPT — Schede sui residuati bellici nel percorso «Oggetti sconosciuti»** (preparata da Claude, da avviare a mano in Codex Cloud; PR #1703; ramo `chatgpt/schede-residuati-bellici-20261105`)
  - **Esito (05/11/2026).** Lavoro consegnato e unito in `main` con la pull request #1703.
  - **Avvio (Alessandro): una riga.** In Codex Cloud, ambiente «sito-pc-genzano», ramo principale (non serve sceglierne un altro). Incolla: «Leggi COORDINAMENTO.md ed esegui la richiesta della PR #1703.» A lavoro finito, «Create PR» dal task. La pull request di consegna la porta nel ramo e la chiude Claude (`passa-a.py chiudi --pr 1703 --consegna M`).
  - **Per chi la esegue.** Esegui le sette parti qui sotto, punto per punto, con i controlli che indicano. Parti dal ramo principale; se il task è partito dal ramo `chatgpt/schede-residuati-bellici-20261105`, va bene lo stesso. Non modificare COORDINAMENTO.md: l'esito lo scrive chi chiude il lavoro. Messaggi di commit in italiano, senza nomi di strumenti. Non unire nulla e non segnare pronta nessuna pull request. Alla fine riassumi in poche righe che cosa hai fatto, che cosa resta e perché.
  - **1. Obiettivo.**
    Due schede stampabili nuove sui residuati bellici (ordigni della seconda guerra mondiale rimasti inesplosi), una per la primaria (8–11 anni) e una per la secondaria di primo grado (11–14 anni), inserite nel percorso «Oggetti sconosciuti» già pubblicato e collegate dai due kit per le scuole. Nessun annuncio: niente articoli, niente homepage, niente social, nessuna data sulla scheda.
  - **2. File.**
    Nuovi:
    - static/formazione/schede-stampabili/oggetti-un-oggetto-della-guerra-primaria/index.html
    - static/formazione/schede-stampabili/oggetti-residuati-bellici-secondaria1/index.html

    Da modificare:
    - content/formazione/kit-scuola-primaria.md (elenco del percorso «Oggetti sconosciuti», subito dopo «Una segnalazione chiara»)
    - content/formazione/kit-scuola-secondaria-primo-grado.md (elenco del percorso «Oggetti sconosciuti», subito dopo «Segnali e supposizioni»)
    - static/formazione/schede-stampabili/index.html (una scheda nel blocco «Oggetti sconosciuti — Primaria», una nel blocco «Oggetti sconosciuti — Secondaria I»)
    - static/formazione/schede-stampabili/oggetti-sconosciuti-guida-adulti/index.html (le due schede nell'elenco del percorso e le loro risposte)

    Generati dagli script, mai a mano: static/formazione/schede-stampabili/pacchetti/*.html, gli ZIP dei kit prodotti da scripts/genera-pacchetti-kit.py, data/materiali_lezione.json, il collegamento «Pronto per la LIM» e l'URL canonico che gli script aggiungono alle due schede nuove.
  - **3. Che cosa fare.**
    1. Leggi per intero queste pagine del percorso e usale come modello: oggetti-una-segnalazione-chiara-primaria, oggetti-prima-di-raccogliere-primaria, oggetti-petardi-e-oggetti-metallici-secondaria1, oggetti-segnali-e-supposizioni-secondaria1, oggetti-sconosciuti-guida-adulti. Le schede nuove ne copiano struttura, fogli di stile, classi, intestazione, nota per l'adulto dentro la scheda, soluzione capovolta (classe `soluzione-capovolta`), riquadro delle fonti numerate e piè di pagina.
    2. Stessi principi del percorso, scritti nella guida per gli adulti: ai ragazzi non si chiede di riconoscere un ordigno; si insegna a fermarsi, non toccare, non calciare, non spostare, non raccogliere, allontanarsi, ricordare il posto guardandolo da lontano e avvisare un adulto; l'adulto chiama il 112 da un luogo sicuro, dopo essersi allontanato e prima di usare telefono o radio; non esiste una distanza unica da insegnare; i disegni non rappresentano distanze di sicurezza; nessuna paura come leva; gli esempi sono inventati e lo si dice.
    3. Scheda primaria «Un oggetto della guerra» (8–11 anni, circa 20 minuti):
       - spiegazione breve: durante la seconda guerra mondiale in Italia caddero bombe e proiettili; alcuni non sono esplosi e possono trovarsi ancora nel terreno, nei boschi, nei campi, nei cantieri, nei laghi o in mare; anche dopo tanti anni possono essere pericolosi; li possono toccare solo gli artificieri delle Forze armate;
       - racconto inventato: Flavio e Silvia passeggiano con il nonno Pasquale; nel terreno smosso vedono un oggetto di metallo arrugginito che non conoscono; Silvia vorrebbe portarlo a scuola, Flavio la ferma; si allontanano e il nonno, da lontano, chiama il 112 e spiega dove si trovano;
       - attività 1: mettere in ordine 4–5 azioni;
       - attività 2: vero o falso con il perché (per esempio «Se è arrugginito non è più pericoloso»: falso; «Lo porto ai Carabinieri per farlo vedere»: falso; «Lo dico subito a un adulto»: vero; «Mi avvicino per fotografarlo»: falso);
       - attività 3: completare una segnalazione chiara (dove sei, che cosa vedi da lontano, chi è con te), senza avvicinarsi;
       - nota per l'adulto e soluzione capovolta, come nelle altre schede.
    4. Scheda secondaria I «Residuati bellici: che cosa fare se li trovi» (11–14 anni, circa 30 minuti):
       - che cosa sono i residuati bellici e perché si trovano ancora oggi (scavi e lavori, terreni smossi, acque che si abbassano, mare);
       - chi fa che cosa: chi trova si allontana e chiama il 112; intervengono le forze dell'ordine; la bonifica e il disinnesco li fanno gli artificieri delle Forze armate (in mare la Marina Militare); per gli ordigni più grandi, durante il disinnesco, le autorità possono disporre l'evacuazione dell'area. Scrivi solo i passaggi confermati dalle fonti del punto 5;
       - cinque idee sbagliate da smontare, ognuna con il perché: «È vecchio, non esplode più»; «Lo sposto in un posto sicuro»; «Lo porto io in caserma»; «Faccio un video da vicino»; «Se è piccolo non è pericoloso»;
       - attività: una notizia inventata (dichiarata inventata) di un ritrovamento in un cantiere, da analizzare (chi ha fatto bene, che cosa cambieresti); una segnalazione chiara al 112 (dove, che cosa si vede da lontano, se ci sono persone vicine), senza avvicinarsi;
       - nota per l'adulto e soluzione capovolta.
    5. Fonti: ogni fatto delle due schede ha una fonte primaria che hai letto, citata nel riquadro numerato delle fonti con ente, titolo e link: Ministero della Difesa e Forze armate (difesa.it, esercito.difesa.it, marina.difesa.it) per chi fa bonifica e disinnesco; Normattiva, solo sul testo vigente, se citi una norma (per esempio il Codice dell'ordinamento militare, decreto legislativo 15 marzo 2010, n. 66, per la bonifica da ordigni bellici); siti delle Prefetture (prefettura.it) per le evacuazioni durante i disinneschi; Treccani per i fatti storici. Per il 112 usa la stessa fonte della guida per gli adulti. Ciò che non trovi confermato non si scrive, e lo elenchi nel riassunto. Nessuna cifra senza fonte.
    6. Nessuna data nelle due schede: niente «aggiornata al», «fonti consultate il», «nuovo» (istruzione di Alessandro: queste schede non si datano oggi). Le date delle verifiche scrivile solo nel riassunto finale.
    7. Kit: aggiungi una voce per scheda negli elenchi del percorso, nello stesso formato delle voci vicine: `- [Titolo](/formazione/schede-stampabili/<cartella>/) — <età>. <obiettivo in una frase>.`
    8. Indice delle schede: una scheda per blocco, copiando il markup delle schede vicine (icona Bootstrap Icons, fascia, durata, descrizione che finisce con «Con nota per l'adulto e soluzione capovolta.», pulsante «Apri e stampa» con il suo aria-label).
    9. Guida per gli adulti: aggiungi le due schede dove la guida elenca le schede del percorso e le loro risposte nella sezione delle risposte, con la stessa numerazione progressiva e lo stesso stile.
    10. Rigenera i file generati: `python3 scripts/genera-pacchetti-schede.py`, `python3 scripts/genera-pacchetti-kit.py`, `python3 scripts/genera-materiali-lezione.py`, `python3 scripts/segno-lim-statiche.py`, `python3 scripts/aggiungi-canonical-statiche.py` (prima leggi `--help` di ciascuno).
  - **4. Vincoli.**
    - Leggi prima AGENTS.md e, nella cartella delle regole del repository, lim-scuole.md, 02-content-design-pa.md (§ «Personaggi delle storie per bambini») e 09-regole-contenuti-qualita.md (§ 15-ter, stampa).
    - Italiano corretto e semplice, frasi brevi, voce attiva, del tu ai ragazzi; nessun divieto o garanzia assoluti senza scenario.
    - Personaggi: protagonista Flavio; altri nomi solo fra Silvia, Maria, Elio, Pasquale, Lina, Alessandro, Christian, Marco.
    - Stampa A4: ogni scheda senza fogli bianchi né fogli quasi vuoti con le tre serie di caratteri del controllo; se serve, scala di stampa della sola scheda (`html { font-size: N% }`), al massimo il 12% in meno, poi si stringono gli spazi.
    - Niente JavaScript nuovo. Licenza come le altre schede (CC BY-NC-SA 4.0).
    - Nessun nome di strumenti o servizi automatici nei file, nei metadati e nei messaggi di commit. Prima del primo commit: `bash scripts/imposta-identita-git.sh` (autore Alessandro Cuollo).
    - Uno strumento che manca si installa (`apt-get update` e `apt-get install`, poi pip o npm); se non ci riesci, scrivi nel riassunto che cosa hai provato e con quale errore.
  - **5. Controlli.**
    Tutti con esito senza errori:
    - `hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"` (nessun ERROR nel log)
    - `python3 scripts/check-refusi.py` sui file del punto 2
    - `python3 scripts/check-parita-schede.py`
    - `python3 scripts/genera-materiali-lezione.py --check`
    - `python3 scripts/segno-lim-statiche.py --check`
    - `python3 scripts/aggiungi-canonical-statiche.py --check --sitemap public/sitemap.xml`
    - `python3 scripts/check-qualita-pagine.py public`
    - `python3 scripts/check-fogli-stampa.py --da-git origin/main`
    - `python3 scripts/check-lim.py --da-git origin/main`
    - `python3 scripts/check-dati-canonici.py` e `python3 scripts/cerca-incongruenze.py --da-git origin/main`
  - **6. Consegna.**
    Solo i file del punto 2, con messaggi di commit in italiano e senza nomi di strumenti. Alla fine un riassunto breve: fatto / non fatto / perché, le fonti lette con la data della lettura, i controlli eseguiti con l'esito. `COORDINAMENTO.md` non si tocca.
  - **7. Che cosa non fare.**
    Non unire nulla, non segnare pronta nessuna pull request, non toccare file fuori dall'elenco del punto 2, non scrivere articoli né pagine nuove, non inventare dati: se manca qualcosa, scrivilo nel riassunto finale.

- **2026-11-05 — da Claude a ChatGPT — Tre articoli d'archivio sugli interventi del Gruppo riportati dalle cronache locali** (preparata da Claude, da avviare a mano in Codex Cloud; PR #1704; ramo `chatgpt/articoli-cronache-interventi-20261105`)
  - **Esito (05/11/2026).** Consegna della PR #1706 portata nel ramo e unita con la PR #1704 su ordine di Alessandro («pubblica la PR #1706»). Fatti ricontrollati sulle quattro pagine di cronaca: il lavoro al sottopasso dell'Appia è del 7 gennaio (articolo spostato a quella data, nuova cover); tombino con orario e dettagli dalla cronaca, link all'esperimento corretto dopo la rinumerazione; gate AGID applicato.
  - **Avvio (Alessandro): una riga.** In Codex Cloud, ambiente «sito-pc-genzano», ramo principale (non serve sceglierne un altro). Incolla: «Leggi COORDINAMENTO.md ed esegui la richiesta della PR #1704.» A lavoro finito, «Create PR» dal task. La pull request di consegna la porta nel ramo e la chiude Claude (`passa-a.py chiudi --pr 1704 --consegna M`); la unisce Alessandro, dopo il confronto con il registro interventi.
  - **Per chi la esegue.** Esegui le sette parti qui sotto, punto per punto, con i controlli che indicano. Parti dal ramo principale; se il task è partito dal ramo `chatgpt/articoli-cronache-interventi-20261105`, va bene lo stesso. Non modificare COORDINAMENTO.md: l'esito lo scrive chi chiude il lavoro. Messaggi di commit in italiano, senza nomi di strumenti. Non unire nulla e non segnare pronta nessuna pull request. Alla fine riassumi in poche righe che cosa hai fatto, che cosa resta e perché.
  - **1. Obiettivo.**
    Tre articoli d'archivio, datati al giorno dei fatti, sugli interventi del Gruppo riportati dalle cronache locali. Restano in questa pull request: la unisce Alessandro dopo averli confrontati con il registro interventi.
  - **2. File.**
    - content/comunicazioni/2026-01-06-maltempo-albero-croce-santa-squadra-ciampino.md
    - content/comunicazioni/2026-01-08-sottopasso-appia-ciampino-idrovore.md
    - content/comunicazioni/2026-07-20-chiavi-tombino-centro-storico.md
    - static/images/ con le tre cover prodotte da `scripts/genera-cover.py` (un file per articolo, nome uguale allo slug)
  - **3. Che cosa fare.**
    1. Leggi le pagine di cronaca qui sotto e verifica ogni fatto. Nel corpo entrano solo i fatti confermati dalla pagina, riscritti con parole tue.
       - Articolo del 6 gennaio 2026. Fatti da verificare: dopo giorni di pioggia un albero cade vicino alla Croce Santa e danneggia due auto; i volontari del Gruppo fanno i rilievi e lo rimuovono, insieme a Carabinieri e Polizia Locale (https://www.castellinotizie.it/2026/01/06/genzano-cade-albero-vicino-la-croce-santa-danneggiate-due-auto-fratelli-ditalia-allattacco-ancora-una-tragedia-sfiorata/); dopo un intervento su un albero in centro, una squadra del Gruppo parte per Ciampino con un'idrovora, su disposizione della Sala Operativa regionale (https://www.ilmamilio.it/wp/2026/01/maltempo-la-protezione-civile-di-genzano-in-azione-squadra-inviata-a-ciampino/); lungo via Montegiove il sottopasso ferroviario al confine fra Genzano e Ariccia torna percorribile grazie al lavoro delle squadre del Gruppo (https://www.ilmamilio.it/wp/2026/01/castelli-roma-e-provincia-nella-morsa-del-maltempo-175-interventi-dei-vigili-del-fuoco-tra-allagamenti-e-alberi-caduti/).
       - Articolo dell'8 gennaio 2026. Fatti da verificare: nei giorni dopo il maltempo i Gruppi di Genzano e di Albano svuotano con le idrovore il sottopasso dell'Appia a Ciampino, ancora allagato (https://www.castellinotizie.it/2026/01/08/ciampino-protezione-civile-di-genzano-e-albano-in-azione-per-liberare-il-sottopasso-dellappia-ancora-allagato-dopo-il-maltempo/).
       - Articolo del 20 luglio 2026. Fatti da verificare: su richiesta della Polizia Locale, i volontari recuperano da un tombino del centro storico le chiavi cadute a una persona, dopo una lunga ricerca (https://www.castellinotizie.it/2026/07/20/genzano-perde-le-chiavi-nel-tombino-interviene-la-protezione-civile-e-gliele-restituisce-dopo-una-lunga-ricerca/).
       Se una pagina non si apre o non conferma un fatto, quel fatto non si scrive e lo elenchi nel riassunto.
    2. Frontmatter di ogni articolo, in quest'ordine:
       ```
       title: "<titolo informativo, senza enfasi>"
       date: <vedi punto 6>
       description: "<massimo 160 caratteri>"
       badge: "Attività"
       priorita: "normale"
       autore: "Gruppo Comunale Volontari PC Genzano"
       image: "/images/<slug>.webp"
       image_alt: "Cover dell'articolo: <titolo>"
       scadenza: ""
       area: "Genzano di Roma"   (per l'articolo dell'8 gennaio: "Ciampino (RM)")
       allegati: []
       social: false
       social_citazione: ""
       social_punti: []
       draft: false
       ```
       `social: false` resta anche se oggi gli script dei social non lo conoscono ancora: lo riconosceranno con un altro lavoro già in corso. Gli articoli d'archivio non vanno sui social.
    3. Struttura del corpo: un primo paragrafo concreto (giorno con la data estesa, luogo, che cosa è successo); una o due sezioni `##` con il racconto; la sezione `## Cosa impariamo` con 2–4 punti di prevenzione ricavati solo dai fatti raccontati, ognuno collegato a una pagina del sito che esiste (per esempio /rischi-prevenzione/rischio-idrogeologico/, /rischi-prevenzione/temporali-intensi/, /rischi-prevenzione/vento-forte/, /numeri-utili/); la frase «Il Gruppo Comunale non può essere attivato direttamente dai cittadini: in emergenza chiama il 112.»; infine `## Per approfondire` con «Sul nostro sito:» (pagine del sito) e «Le cronache locali:» (nome della testata, titolo e link di ogni pagina usata).
    4. Regole sulle cronache: parafrasi sempre, mai frasi copiate o virgolettati, nessun nome di testata nel corpo (se serve, «secondo le cronache locali»), testate solo in fondo. Orari arrotondati («nel pomeriggio», «in serata»), mai al minuto. Niente nomi di privati, targhe, indirizzi privati, condizioni di salute. Chi ha chiesto l'intervento: si nomina solo un ente (Polizia Locale, Carabinieri, Sala Operativa regionale); per un cittadino si scrive in forma neutra («dopo una segnalazione»). Nessuna polemica politica: il titolo della prima pagina di Castelli Notizie riporta l'attacco di un partito e non va ripreso in nessun modo.
    5. Un mezzo o un'attrezzatura si nominano solo come li chiama content/chi-siamo/_index.md, § «Mezzi e attrezzature principali»; «idrovora» va bene come nome generico.
    6. Date: `date: 2026-01-06` e `date: 2026-01-08` in formato semplice. Il 20 luglio ha già due articoli con `T00:01:00+02:00` e `T00:02:00+02:00`: il nuovo prende `date: 2026-07-20T00:03:00+02:00` e gli altri due non si toccano.
    7. Cover: per ogni articolo `python3 scripts/genera-cover.py content/comunicazioni/<file>.md`, poi apri l'immagine e controlla che mostri titolo e fascia.
  - **4. Vincoli.**
    - Leggi prima AGENTS.md e, nella cartella delle regole del repository, 02-content-design-pa.md (§ «Fonti giornalistiche negli articoli», § «Resoconti degli interventi»).
    - Italiano corretto, frasi sotto le 20 parole, voce attiva, niente burocratese e niente tic da testo generato (vedi AGENTS.md § 3.5).
    - Badge «Attività». Nessuna versione facile per questi tre articoli.
    - Nessun nome di strumenti o servizi automatici nei file, nei metadati e nei messaggi di commit. Prima del primo commit: `bash scripts/imposta-identita-git.sh` (autore Alessandro Cuollo).
    - Uno strumento che manca si installa (`apt-get update` e `apt-get install`, poi pip); se non ci riesci, scrivi nel riassunto che cosa hai provato.
  - **5. Controlli.**
    Tutti senza errori:
    - `hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"` (nessun ERROR nel log)
    - `python3 scripts/check-refusi.py` sui tre articoli
    - `python3 scripts/check-grafiche-social.py` sui tre articoli
    - `python3 scripts/cerca-incongruenze.py --da-git origin/main`
    - `python3 scripts/check-dati-canonici.py`
    - `git diff --name-only origin/main` deve mostrare solo i file del punto 2
  - **6. Consegna.**
    Solo i file del punto 2, con messaggi di commit in italiano e senza nomi di strumenti. Alla fine un riassunto breve: fatto / non fatto / perché, e per ogni articolo l'elenco dei dati presi dalla stampa che Alessandro deve confermare con il registro interventi (giorno, luogo, che cosa, chi ha attivato il Gruppo, mezzi). `COORDINAMENTO.md` non si tocca.
  - **7. Che cosa non fare.**
    Non unire nulla, non segnare pronta la pull request (la unisce Alessandro dopo il confronto con il registro), non toccare file fuori dall'elenco del punto 2, non inventare fatti: se manca qualcosa, scrivilo nel riassunto finale.

- **2026-11-05 — Claude — Articoli d'archivio del 2026, un articolo per evento, senza social** (ramo `claude/archivio-2026-articoli-20261105`; PR #1712)
  - **Esito (05/11/2026).** Unita con la PR #1712, con l'ok di Alessandro: i 26 articoli ricontrollati sulle fonti primarie, con le copertine col titolo e gli orari nei giorni con più uscite; nessun materiale social.
  - Che cosa: 26 articoli datati al giorno dell'evento (ricorrenze, eventi nazionali, norme, atti del Comune), tutti con `social: false`; gli script dei social imparano a saltare gli articoli con `social: false`.
  - File: gli articoli nuovi in `content/comunicazioni/` (dal 2 gennaio al 3 ottobre 2026) con le loro cover; `archetypes/comunicazioni.md`; `scripts/genera-social.py`, `genera-immagini-social.py`, `check-grafiche-social.py`, `social-pronti.py`, `social_comune.py`, `README-social.md`; rule 04b e 10; `CLAUDE.md`.

- **2026-11-05 — Claude — Correzione delle informazioni su IT-alert** (ramo `claude/correzioni-it-alert-20261105`; PR #1710)
  - **Esito (05/11/2026).** Unita con la PR #1710 alle 06:45: testi su IT-alert allineati alle fonti ufficiali in tutto il sito, quattro voci nuove in `data/dati_canonici.yaml`, puntate del podcast sospese finché non saranno rifatte. Online e verificata alle 07:28.
  - Che cosa: l'articolo del 19 maggio è riscritto sulle pagine ufficiali di IT-alert e del Dipartimento; restano la sua versione facile, le frasi su IT-alert e «precipitazioni intense» negli altri contenuti, le nuove voci del registro dei dati, i controlli e la pubblicazione.
  - File: articoli e versioni facili su IT-alert del 15 maggio, 19 maggio, 11 giugno, 10 luglio e 27 agosto; dossier «Il messaggio che salva»; traccia d'esame della secondaria di secondo grado e indice delle schede, con i pacchetti rigenerati; articoli su Soverato, Marche e Livorno; gioco «Scelte difficili»; assistente; percorsi didattici; `a11y-toolbar.css`; `data/dati_canonici.yaml`. Se un altro lavoro tocca l'indice delle schede o `data/materiali_lezione.json`, dopo il merge i file generati si rigenerano con gli script.

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

