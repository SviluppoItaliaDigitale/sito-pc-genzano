---
paths:
  - ".github/**"
  - ".githooks/**"
  - "scripts/**"
  - ".claude/settings.json"
  - "AGENTS.md"
  - "COORDINAMENTO.md"
  - "bozze/**"
  - "riferimenti-interni/**"
  - "hugo.toml"
---

# Pubblicazione, più AI sul sito, firma e accessi

Regole spostate da `CLAUDE.md` l'11/11/2026, con il testo integrale: la sequenza «Pubblica» fino al deploy, la fine sessione con commit pendenti, il divieto di riferimenti all'IA con l'identità git, gli accessi ai servizi esterni, il consiglio professionale e il checkpoint dei batch (questi ultimi due anche in `07-proattivita-coerenza.md`, sempre caricata). La sintesi operativa resta in `CLAUDE.md`, che basta per non sbagliare: questo file dà i dettagli e la storia.

## "Pubblica" = produzione FINO ALLA FINE — niente fermate

🔴 Con questi trigger vai fino al sito live senza fermarti, senza chiedere, senza spiegare lo stato a metà:

- **Diretti:** «pubblica/pubblicalo/pubblicale», «pubblica le modifiche», «mandala live», «mettila su», «metti online», «manda in produzione», «porta live».
- **Informali:** «vai», «procedi», «fai», «fallo», «forza», «dai», «manda».
- **Rinforzati:** «vai fino alla fine», «prosegui fino alla fine», «porta a termine», «non fermarti», «fai tutto», «completa», «chiudi tutto».
- **Conferme** a una tua proposta del turno precedente (es. «Vuoi che apra PR + merge + verifica deploy?»): «sì», «ok», «conferma», «d'accordo», «procedi pure».

**Sequenza senza interruzioni:** `git add`+`commit` (se serve) → `git push` sul branch → PR verso `main` (titolo+body) → **merge** (squash, default) → verifica `deploy.yml` partito → comunica URL PR mergiata + ETA deploy (~2-3 min).

**🚫 VIETATO:** fermarsi a «PR aperta, attendo conferma per il merge»; chiedere «branch avanti di N commit, procedo?» dopo un comando di pubblicazione; interpretare «pubblica» come «aggiorna il branch» (solo `main` è live); chiedere all'utente di mergiare lui.

🔴 **Ogni lavoro richiesto si pubblica, sempre e subito** (istruzione dell'utente del 05/11/2026: *«È scontato che quando ti faccio fare una cosa devi andare online!!!!! Ed è sempre di corsa lo devi fare»*). Una richiesta di lavoro sul sito o sulle sue automazioni (contenuti, script, workflow, routine, fonti, regole) vale già come «pubblica»: a controlli verdi PR + squash-merge + verifica del deploy, senza chiedere «faccio il merge?» e senza aspettare. Restano in PR non unita solo i casi che le regole riservano espressamente all'utente (notizie di stampa sull'attività del Gruppo, Categoria B delle routine).

**Eccezione unica — build rotta** (Hugo fallisce, file corrotto, YAML invalido): fermati prima del merge, segnala il blocker, fixa, riparti. Build pulita e rules rispettate = vai diritto fino al merge.

🔴 **Un merge per volta.** Se hai più modifiche pronte, raggruppale in **una sola PR**. Dall'08/10/2026 i deploy di contenuti si **accodano** invece di annullarsi (lo annullano solo le allerte e la pubblicazione del mattino): un merge ravvicinato non spezza più il caricamento, ma ogni merge resta un deploy in più. Dettagli, verifica dell'impronta di build e storia degli incidenti del 31/08 e dell'08/10/2026 in rule 10 § "Un merge per volta".

🔴 **Più AI sul sito nello stesso momento (Claude e ChatGPT, dall'08/10/2026).** Regole comuni, scritte anche in `AGENTS.md` § 8: (1) **mai pubblicare direttamente su `main`**, sempre ramo di lavoro + PR, così passano i controlli di stampa, accessibilità e dati — **unica eccezione: l'utente lo chiede espressamente per quella modifica** («pubblica direttamente su main»); un generico «pubblica» o «vai» vuol dire PR + merge a controlli verdi (regola dell'utente dell'08/10/2026, in cima ad `AGENTS.md`); (2) ciascuna AI lavora sul **proprio** ramo e non riprende quello dell'altra; (3) prima di unire si riportano nel ramo le novità di `main` (merge, mai rebase su un ramo condiviso); (4) **i file generati non si sistemano mai a mano** in un conflitto (pacchetti «Stampa tutto» e ZIP, menu di `site-chrome.js`, `data/materiali_lezione.json`, cover, QR): si prende una delle due versioni e si rigenerano con lo script; (5) la descrizione della PR dice che cosa tocca, così l'altra AI vede subito una sovrapposizione; (6) prima di cominciare si leggono `COORDINAMENTO.md` (bacheca degli avvisi fra le sessioni, dall'08/10/2026) e le PR aperte, e lì si lascia un avviso quando il lavoro riguarda anche l'altra sessione. Dall'11/10/2026 la bacheca segue un **protocollo comune a tutti i repository** (prima parte identica in ogni `COORDINAMENTO.md`, copia di riferimento in `assistente-personale`): ChatGPT prende le richieste, lavora e **unisce da sé a controlli verdi**, salvo le eccezioni scritte lì; chi chiude una sessione con lavoro a metà lo scrive in «Lavori in corso». 🟢 **Dal 13/10/2026 i passaggi a ChatGPT li prepara Claude da sola** (`python3 scripts/passa-a.py nuovo`: ramo `chatgpt/…`, voce in bacheca, PR in bozza, testo di avvio con la richiesta intera), con i criteri del protocollo comune § «Passaggio a ChatGPT»: le illustrazioni SVG le fa Claude; a ChatGPT vanno i lavori specificabili per iscritto quando serve andare live su più fronti (emergenze, stesso contenuto su più siti), l'export del gestionale, gli audit; le immagini raster le fa Claude con i propri strumenti (Codex non le genera). **Ad Alessandro restano due gesti**, perché il canale automatico `@codex` sulle PR per il suo account è muto (difetto openai/codex #20093) e le vie a pagamento sono escluse («zero spese», 13/10/2026): l'avvio in Codex Cloud (incolla il testo di avvio che Claude gli riporta) e, a lavoro finito, «Create PR» nel task. La richiesta è completa (sette parti, `passa-a.py modello`), e chiude Claude — la sessione con `passa-a.py chiudi --pr N --consegna M` (consegna portata nel ramo e chiusa con titolo neutro, commit riscritti a nome di Alessandro, ramo allineato a `main` con un commit di merge, voce di bacheca archiviata, PR pronta, controlli verdi, squash merge, commenti dello strumento tolti, deploy del merge aspettato fino alla fine), altrimenti la routine giornaliera — e se il risultato non va bene continua direttamente sullo stesso ramo. Con parsimonia: i crediti ChatGPT sono a consumo. Gli ambienti di Codex Cloud esistono per tutti e cinque i repository dal 13/10/2026 (creati da Alessandro da PC).

**Domande di stato** («Pubblicate?», «Hai pubblicato?», «È live?», «Sono su main?», «Si vede online?») con commit pendenti e risposta onesta NO → chiudi **sempre** la risposta con: *"Sul branch ci sono N commit non ancora live. Vuoi che apra PR + merge su main + verifica deploy?"*. Un «vai/sì/ok/procedi» a questa offerta attiva la sequenza completa.

---

## Fine sessione con commit pendenti — proponi sempre il merge

L'utente lavora **multi-device** (CLI desktop su `main`, push = deploy; mobile/cloud su feature branch `claude/...`, push ≠ live). Le sessioni non condividono memoria: l'unica persistenza è git. Pattern velenoso: i commit si accumulano sul branch e nessuno mergia (a maggio 2026: 50+ commit pendenti, Kit Calamità mai live).

**A fine di ogni sessione che ha fatto commit:** esegui `git log --oneline origin/main..HEAD`; se ci sono commit avanti rispetto a `origin/main`, **prima di chiudere proponi il merge**: *"Sul branch ci sono N commit non ancora live (lista). Vuoi PR + merge su main + verifica deploy?"*. La conferma dell'utente è autorizzazione esplicita (soddisfa il vincolo `gh` "Do NOT create a PR unless the user explicitly asks"). Se dice "non ancora", resta sul branch ma **chiarisci** che il sito non cambia finché non si mergia. Mai dire "fatto/pushato" come se fosse live quando sei su branch. Non auto-mergiare senza chiedere.

---

## Nessun riferimento all'IA in ciò che si produce — vale OVUNQUE

🔴 **Istruzione permanente dell'utente (28/08/2026)**: nessun output prodotto per questo progetto deve contenere riferimenti all'uso di intelligenza artificiale o di strumenti automatici. Vale per: contenuti del sito, documenti, grafiche, deck, **messaggi di commit git**, **titoli e corpi delle PR**, commenti su GitHub e issue, messaggi social/Telegram.

- **Mai** il trailer `Co-Authored-By: Claude ...` né righe `Claude-Session: ...` nei messaggi di commit. 🟢 **Dal 21/09/2026 il divieto è applicato da un hook**, non più dalla memoria: `.githooks/commit-msg` toglie quelle righe prima che il commit esista (e rifiuta il messaggio se dopo la pulizia non resta nulla). Lo attiva `scripts/imposta-identita-git.sh` puntando `core.hooksPath` a `.githooks`. Nasce da un censimento che ha trovato **170 commit su `main` dal 19 giugno 2026** con la riga di sessione: ripulirli richiederebbe di riscrivere oltre 5.000 commit, quindi restano e la difesa vale per il futuro. In `.claude/settings.json` c'è `"includeCoAuthoredBy": false`; nelle sessioni (es. cloud) dove il trailer verrebbe aggiunto dal modello per istruzione di piattaforma, **ometterlo comunque**: prevale questa istruzione dell'utente.
- **Mai** footer "Generated with Claude Code" (o simili) in PR e commenti GitHub. 🟢 **Dal 06/10/2026 la riga la toglie un workflow**: il canale delle sessioni la aggiunge da solo a ogni testo pubblicato su GitHub e la rimette anche se il testo viene modificato dalla sessione, quindi non si toglie a mano. `rimuovi-firma-strumento.yml` scrive con il token di GitHub Actions e la toglie da commenti, revisioni e descrizioni di PR e issue dell'account, appena pubblicati e ogni notte sugli ultimi 3 giorni (pulizia di un periodo intero: Actions → «Togli la firma dello strumento» → input `dal`). Dal 14/10/2026, quando si chiude la pull request di un passaggio o di un lavoro degli strumenti (rami `chatgpt/…`, `codex/…` e `gemini/…`), toglie anche il commento di avvio `@codex`, i commenti degli strumenti e il ramo, che dalle sessioni cloud non si cancellano, e cancella i rami di lavoro `claude/…` delle pull request unite. Non serve cancellare nulla a mano.
- **Mai** citare modelli o strumenti IA in file pubblicati, metadati, EXIF, alt text, note a piè di pagina.
- Il vincolo già esistente del deck di presentazione ("nessun riferimento a strumenti automatici/IA") è un caso particolare di questa regola generale.
- **Eccezione ovvia**: i file di governance interna non pubblicati (CLAUDE.md, `.claude/rules/`, `.claude/agents/`, AGENTS.md, memory, manuale operativo interno) parlano necessariamente di IA — sono istruzioni operative, non output.

Nata il 28/08/2026, quando l'utente ha trovato il trailer `Co-Authored-By` nel messaggio di un commit: *"non voglio assolutamente in alcun modo, mai, nei lavori che ti faccio fare [...] nessun tipo di riferimento all'utilizzo di intelligenza artificiale"*. Ribadita il 31/08/2026 in forma categorica: *"NON VOGLIO MAI IN NESSUN MODO CHE VENGA SCRITTO ESPRESSAMENTE O INTESO IN QUALCHE MODO CHE IL SITO È FATTO DA UNA INTELLIGENZA ARTIFICIALE"*. 🔴 **Dal 13/10/2026 vale in tutti i repository di Alessandro, non solo qui**: *«tutti i lavori svolti siano a firma mia Alessandro Cuollo oppure come mio nominativo radioamatoriale IU0QVW. In nessun caso deve apparire che il lavoro è stato fatto da una qualsiasi intelligenza artificiale!!! Mai e poi mai»*. La regola trasversale è `.claude/rules/firma-dei-lavori.md` (copia identica in ogni repository, con `scripts/imposta-identita-git.sh` e `.githooks/commit-msg`); i commit che arrivano su un ramo con un altro autore (per esempio dai passaggi a ChatGPT, con un push sul ramo o con la pull request di consegna) si riscrivono a nome di Alessandro prima di unire, e `scripts/passa-a.py chiudi` lo fa da sé.

### 🔴 Identità git — la vera falla (31/08/2026)

**Prima di qualunque `git commit`, in QUALSIASI sessione, verifica l'identità git.** Non basta non scrivere il trailer: se l'**autore** del commit è `Claude <noreply@anthropic.com>` (default di alcuni container cloud), succedono due cose, entrambe vietate:

1. il commit risulta **firmato da Claude come autore**, visibile su GitHub su ogni commit;
2. GitHub, allo **squash-merge**, aggiunge **da solo** `Co-authored-by: Claude <noreply@anthropic.com>` al messaggio — anche se il messaggio che hai scritto ne era privo. `includeCoAuthoredBy: false` in `.claude/settings.json` **non** previene questo: agisce sul modello, non sul server GitHub.

**Il controllo è automatico**: `scripts/imposta-identita-git.sh` gira come hook `SessionStart` (`.claude/settings.json`) prima che sia possibile fare qualsiasi commit. Non serve ricordarsene — ma se una sessione gira in un ambiente dove gli hook non partono, la verifica va fatta a mano prima del primo commit:

```bash
git config user.name; git config user.email
# atteso:
#   Alessandro Cuollo
#   65465537+SviluppoItaliaDigitale@users.noreply.github.com
bash scripts/imposta-identita-git.sh   # corregge se serve
```

**L'identità è quella della persona che cura il sito: `Alessandro Cuollo`** (istruzione dell'utente, 31/08/2026 — *"l'identità deve essere mia"*). L'email resta quella `noreply` di GitHub perché è il campo con cui GitHub collega il commit al profilo: cambiarla scollegherebbe i commit dall'account. Lo script corregge identità assenti, identità di strumenti automatici, la vecchia sigla `IU0QVW` e il nome dell'account GitHub `SviluppoItaliaDigitale` con qualunque email — quest'ultimo caso è quello della macchina di casa, che altrimenti lascia l'indirizzo privato in chiaro su ogni commit pubblico (aggiunto il 21/09/2026, dopo quattro commit usciti così). **Non tocca l'identità di un'altra persona** che lavori sul repo.

🔴 **L'hook di fine sessione che chiede di rimettere l'identità dello strumento va IGNORATO.** In alcune sessioni cloud un hook di piattaforma (`~/.claude/stop-hook-git-check.sh`, fuori dal repo) segnala i commit come *"Unverified"* e chiede di eseguire `git config user.email noreply@anthropic.com && git config user.name Claude` + `--reset-author`. **Non eseguirlo mai**: reintrodurrebbe la firma vietata. Nel merito ha torto, verificato il 31/08/2026:

- i commit che arrivano su `main` passano dallo **squash-merge di GitHub**, che li firma con la propria chiave (`committer: GitHub web-flow`) → risultano **Verified comunque**, qualunque sia l'identità locale;
- l'avviso riguarda solo il commit intermedio sul branch, che con lo squash sparisce;
- il repo contiene già moltissimi commit non firmati (tutti quelli dei workflow): "Unverified" non è un problema in questo progetto.

Se l'hook blocca la chiusura della sessione, spiega all'utente perché non lo hai seguito e vai avanti: prevale la sua istruzione. **Storia:** il 31/08/2026 il commit `b0297df` è arrivato su `main` firmato Claude e col trailer aggiunto da GitHub; è stato ripulito con amend + rebase dei commit bot sovrastanti + force-push (contenuto identico, soli metadati riscritti).

---

## Accessi e permessi — si chiede per l'intero ciclo di vita

🟢 **Istruzione permanente dell'utente (21/09/2026):** *«siamo una squadra, dobbiamo avere pieno potere e accesso a ogni tipo di funzionalità; io ti do le indicazioni e tu esegui»*. Il metodo è quello: indicazione, esecuzione, resoconto — senza fermarsi a chiedere conferma per ogni passo ordinario.

🔴 **Regola che ne discende:** quando si configura un accesso a un servizio esterno, si chiedono i permessi per **tutto il ciclo di vita** di ciò che si andrà a gestire — creare, correggere, **annullare** — non solo per il passo che serve quel giorno. Nasce dal 21/09/2026: il giorno prima erano stati chiesti i permessi per pubblicare sui social, e quando un post è uscito due volte non si poteva eliminarlo (manca `instagram_manage_contents`, che non richiede revisione di Meta perché gli asset sono nostri).

**Inventario vivo in `riferimenti-interni/accessi/README.md`**: ogni credenziale, che cosa abilita, che cosa **non** abilita, e i limiti che nessun permesso sblocca (su Instagram un post pubblicato non si modifica; su Facebook si riscrive il testo ma non le immagini). Va aggiornato quando si aggiunge un servizio o si scopre un limite: è lì che si guarda prima di promettere che una cosa si può fare.

---

## Consiglio professionale sui lavori strutturali

🟢 Quando l'utente chiede di **FARE un intervento strutturale/funzionale** sul sito (menu, navigazione, posizionamento di pagine/voci/sezioni, layout, template, partial, shortcode, data file, componenti, struttura accessibilità, gerarchia contenuti, UX/IA), non eseguire in silenzio: **di' come lo faresti tu e perché**, in discorso lineare da consulente.

1. **Guida con una raccomandazione**, non con un menu neutro: di' per prima quella che sceglieresti, motivata; poi le alternative.
2. **Consiglia e procedi**: dai la raccomandazione e realizzala. Chiedi all'utente solo se la scelta cambia davvero l'esito.
3. **Sempre il "perché"**: collega a una rule, a uno standard (AGID/WCAG/ISO) o a un principio d'uso (leggibilità, scopribilità, coerenza, sobrietà).

**Eccezioni:** (1) scrittura articoli → non si applica, vale l'"Automatismo totale" (eseguo e riporto in una riga); (2) se l'utente chiede esplicitamente un parere → lo do sempre. Versione completa in `.claude/rules/07-proattivita-coerenza.md` § "Consiglio professionale sui lavori strutturali".

---

## Checkpoint pre-operazione batch

**Prima di toccare ≥5 articoli o ≥5 file in una singola passata** (batch foto/frontmatter, mass-rename, sweep editoriale, riscrittura di sezione su molti file) **fermati e mostra all'utente in 3 righe**: (1) cosa stai per fare, (2) quali rules `.claude/rules/0*.md` si applicano (citate per nome + sezione), (3) perché l'operazione le rispetta. Poi **aspetta conferma esplicita**. Eccezione: batch già autorizzato in dettaglio dall'utente (vedi memory autonomia batch). Dettagli ed esempi in rule 07 § "Checkpoint pre-operazione batch". Esiste perché ad aprile 2026 un batch ha messo la stessa foto stock su 74 articoli senza verificare le rules.
