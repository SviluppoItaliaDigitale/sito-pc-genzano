_[Indice manuale](README.md)_

# Parte 19 — Agenti specializzati Claude Code (maggio 2026)

A maggio 2026 sono stati installati nel repo **agenti specializzati**
in `.claude/agents/` (**sedici a maggio 2026, trentaquattro dal 6 settembre 2026**). Sono profili professionali
virtuali con cui Claude Code ti aiuta nei compiti ricorrenti del Gruppo,
ognuno con un'expertise mirata. La progressione:

- **8 agent dell'apertura** (maggio 2026): redazione AGID, art direction, gestione issue, deploy engineering, comunicazione di crisi, QA schede stampabili, audit di sistema, **gate visivo foto** (aggiunto il 15 maggio dopo l'incidente "Giro d'Italia 2026 a Formia": caption fabbricate dai testi di terzi invece che dalle foto reali).
- **5 agent professionisti aggiuntivi** (15 maggio 2026, in risposta alla richiesta utente *"assumi le migliori professionalità per essere perfetti"*): accessibility auditor IAAP CPACC, content strategist editoriale (Repubblica.it/ANSA), glottologa italiano L2 (Univ. Stranieri Siena), SEO editor (La Stampa/Sole 24 Ore Digital), avvocato amministrativista (Camera Deputati). Ognuno con CV credibile e responsabilità chiara nel ciclo editoriale.
- **2 agent aggiunti il 16-18 maggio 2026**: `pc-photo-caption-verifier` (gate visivo Read multimodale foto, codificato dopo l'incidente Formia), `pc-materiali-publisher` (publishing engineer dei materiali multimediali NotebookLM su `/risorse-pronte/`).
- **1 agent aggiunto ad agosto 2026**: `pc-revisore-linguistico` (gate linguistico obbligato: script deterministici + lettura sintattica per articoli mancanti, accordi e reggenze — nasce il 19/08/2026 dopo che «L'Italia ha rete ben strutturata», «nella immagine» e «superficiale.Il» erano andati live superando tutti i controlli).
- **1 agent aggiunto a maggio 2026**: `pc-correttore-bozze` (correttore di bozze deterministico — caccia refusi e errori ortografici/grammaticali su QUALSIASI contenuto, incluse le schede statiche HTML, il punto cieco da cui era passato "cuoperti"→"copriti").
- **17 agent aggiunti il 6 settembre 2026 — il sistema di affidabilità interno.** Un audit esterno aveva trovato 24 rilievi (11 P1) tutti fondati con i gate del sito tutti verdi: fatti sbagliati su Rigopiano, istruzioni per bambini da correggere, rubriche che valutavano la paura, esercizi che spacciavano ipotesi per legge, dati diversi dal dataset, note perse in stampa, pacchetti non paritari, ZIP inutilizzabili offline, privacy e accessibilità da riallineare, favicon vuota, ancore rotte. L'istruzione dell'utente: *«queste cose non devono mai più capitare: non devo più rivolgermi ad altre intelligenze artificiali per fare un audit»*. Da qui i gate dei **fatti** (`pc-fact-checker`), dei **materiali scolastici** (`pc-didattica-reviewer`), della **scienza** (`pc-revisore-scientifico`), della **cronaca** (`pc-desk-giornalistico`), della **conformità legale**, dell'**integrità tecnica**, della **coerenza trasversale**, del **codice**, delle **automazioni**, della **sicurezza**, delle **traduzioni**, dei **dati e feed**, dell'**esercitazione di emergenza**, della **verifica visiva**, dell'**usabilità**, della **documentazione**, e il direttore dell'**audit interno mensile** (`pc-audit-completo`). Sezioni 18-34 di questa Parte.

**La parte importante:** non devi ricordare nessun nome tecnico. **Scrivi a
Claude in italiano normale**, dicendo cosa vuoi fare, e Claude attiva da solo
l'agente giusto.

> ⚠️ **Da leggere insieme a questa Parte**: la **[Parte 31](parte-31-skill-globali-invocazione.md)** sulle **skill globali Claude Code** invocate col tool `Skill`. Gli agent `pc-*` e le ~100 skill globali sono **complementari**: gli agent sono profili professionali editoriali specifici del sito, le skill sono pattern tecnici trasversali (accessibilità, SEO, audit, ricerca, ecc.). Spesso vanno invocati in sequenza (es. revisione articolo: `pc-article-reviewer` → `pc-photo-caption-verifier` → skill `accessibility` → skill `seo-audit`).

---

## 19.1 Gli agenti e quando si attivano

### 1. Caporedattore (revisione articoli) — 🔴 GATE OBBLIGATO

**Da maggio 2026 questo agent è il gate obbligato pre-commit.** Quando Claude Code (in qualunque sessione: CLI desktop, app mobile, sessione cloud, agent GitHub-integrato) genera o modifica sostanzialmente un articolo in `content/comunicazioni/`, **prima del `git add`** invoca questo agent. Non è "proattivo a discrezione": è obbligatorio. Regola codificata in `CLAUDE.md` § *"Auto-gate AGID prima del commit di un nuovo articolo"* e in `.claude/rules/02-content-design-pa.md` § *"Auto-gate AGID prima del commit"*. Esiste perché il 9 maggio 2026 abbiamo dovuto rivedere retroattivamente 43 articoli storici per ripianare il debito accumulato dalle sessioni che non lo invocavano spontaneamente.

**Quando lo attivi tu manualmente**: hai scritto un articolo a mano o ne hai modificato uno sostanziale e vuoi un controllo prima di pubblicare. (Se l'articolo lo ha generato Claude, l'agent è già passato per il gate prima del commit.)

**Frasi naturali che lo attivano automaticamente**:

- *"Mi rivedi questo articolo prima di pubblicare?"*
- *"Controlla l'articolo `<nome-file>.md`, va bene?"*
- *"Mi dici se ci sono errori in questo articolo?"*
- *"Verifica frontmatter e linguaggio AGID dell'articolo che ho scritto."*
- *"Fai una revisione AGID di tutti gli articoli del mese di X"* (batch retrospettivo).

**Cosa fa**: legge il file, applica le 13 categorie di badge, verifica formato data, lunghezza description (≤160 char per SEO), sezioni rigide delle pagine rischio, foto secondo convenzione, link interni esistenti, niente conteggi inventario, niente burocratese, NUE 112 unico numero emergenza Lazio. Quando lo si invoca con istruzione esplicita di edit (come nel pre-commit gate), applica i fix direttamente con razionale AGID per ogni modifica.

**🔴 Eccezione — registro non-AGID:** se l'utente ha chiesto esplicitamente un documento in registro diverso (comunicato stampa, lettera istituzionale, paper scientifico, relazione tecnica, memoria, bando, delibera, ordinanza, scheda accademica, **o qualsiasi altro genere a richiesta esplicita**), il gate è sospeso per quel documento. Claude applica le convenzioni del genere (vedi **Parte 12** per i comunicati stampa). L'eccezione la attivi tu chiedendo esplicitamente quel registro: in assenza di richiesta esplicita, il default è AGID.

**Identità tecnica** (se proprio ti serve): `pc-article-reviewer`.

---

### 2. Art Director (foto e immagini)

**Quando lo attivi**: hai foto da inserire in un articolo, devi applicare la
fascia blu istituzionale, vuoi sistemare la cover.

**Frasi naturali che lo attivano automaticamente**:

- *"Ecco una foto dell'intervento, mettila nell'articolo."*
- *"Queste immagini vanno nell'articolo X, applica la fascia."*
- *"La cover di questo articolo va sistemata, ha solo image vuoto."*
- *"Mi prepari le foto per l'articolo dell'esercitazione di domani?"*

**Cosa fa**: applica fascia blu (1200px, ≤200 KB, WebP), inserisce shortcode
`{{< foto >}}` nel corpo (mai sostituisce il banner col titolo), posiziona
foto multiple con la convenzione storica (1ª dopo 1° H2, 2ª dopo 2° H2…),
fa partire la galleria automatica se ≥4 foto.

**Cosa NON fa**: non sostituisce mai il banner dell'articolo con una foto
utente. Il banner = sempre cover tipografica con titolo, è la regola
istituzionale del Gruppo che non si negozia.

**Identità tecnica**: `pc-image-fixer`.

---

### 3. Project Manager (pulizia issue GitHub)

**Quando lo attivi**: vuoi vedere se ci sono issue aperte da chiudere, fare
pulizia del tracker.

**Frasi naturali che lo attivano automaticamente**:

- *"Controlla le issue aperte sul repo."*
- *"Si possono chiudere le issue?"*
- *"Fammi pulizia del tracker."*
- *"Quante issue abbiamo aperte? Sono ancora valide?"*

**Cosa fa**: usa `gh CLI` per listare le issue aperte, le categorizza per
tipo, verifica nello stato attuale del repo se i problemi che le hanno
generate sono ancora presenti. Distingue issue obsolete (chiuse) da issue
reali (chiede conferma o agisce sulla causa-radice).

**Cosa NON fa**: non chiude issue create manualmente da umani senza chiedere.
Non chiude issue dove la causa-radice non è stata risolta (perché si
ricreerebbero al run successivo del workflow).

**Richiede**: `gh` CLI installato e autenticato. La prima volta che lo
attivi, ti guida a installarlo e a fare login (5 minuti).

**Identità tecnica**: `pc-issue-triage`.

---

### 4. Release Engineer (verifica pre-push)

**Quando lo attivi**: stai per pubblicare e vuoi una verifica preventiva che
nulla rompa il sito live.

**Frasi naturali che lo attivano automaticamente**:

- *"Verifica prima del push, va tutto bene?"*
- *"Posso pubblicare in sicurezza?"*
- *"Controlla il deploy."*
- *"Build OK? Niente regressioni?"*

**Cosa fa**: build Hugo a baseURL Aruba e GitHub Pages, validazione YAML
workflow, controllo `.htaccess` integro (Permissions-Policy con
`geolocation=(self)`), verifica che nessun articolo nuovo abbia `draft: true`,
nessun riferimento a 115/118/1515 come "numero da chiamare", nessun nuovo
conteggio inventario hardcoded, frontmatter completo per articoli modificati.

**Cosa NON fa**: non fa il push. La decisione è sempre tua. Restituisce un
GO/NO-GO motivato con elenco di blocchi e warning.

**Identità tecnica**: `pc-deploy-validator`.

---

### 5. Risk Communication Specialist (revisione bozze social)

**Quando lo attivi**: il workflow ha generato le bozze social per un articolo
e tu vuoi un'ultima revisione prima di copia/incollare sui canali.

**Frasi naturali che lo attivano automaticamente**:

- *"Mi rivedi le bozze social per l'articolo X?"*
- *"Sono pronte per pubblicare le bozze?"*
- *"Controlla i testi e le immagini Instagram di questo articolo."*
- *"Le immagini per Instagram sono nel formato giusto?"*

**Cosa fa**: applica le regole del CWA CEN/CENELEC sui post di crisi
(struttura 6 punti per allerte: tipo, livello, area+tempo, cosa fare, fonte,
prossimo aggiornamento), verifica accessibilità social (alt text, max 2
emoji, niente Unicode decorativi, niente maiuscole continue, niente solo
colore per allerta), verifica hashtag policy del Gruppo (no virali, no
generici svuotati), verifica formato JPG delle immagini Instagram (no WebP
che IG rifiuta), verifica peso file e dimensioni feed 1080×1350 (4:5) / storia 1080×1920 (9:16).

**Cosa NON fa**: non pubblica mai sui social. La pubblicazione è sempre
manuale, è una scelta del Gruppo.

**Identità tecnica**: `pc-social-publisher`.

---

### 6. Print Quality Engineer (QA schede stampabili)

**Quando lo attivi**: hai creato o modificato una scheda A4 stampabile in
`static/formazione/kit-calamita-*/` e vuoi un controllo prima di pubblicarla.

**Frasi naturali che lo attivano automaticamente**:

- *"Controlla le schede stampabili del kit bambini."*
- *"Fai il QA del kit calamità anziani."*
- *"I puzzle di questa scheda sono giocabili davvero?"*
- *"Il labirinto ha una via d'uscita? Il cruciverba ha le celle giuste?"*

**Cosa fa**: verifica struttura HTML, conformità al `print.css`, esistenza
delle immagini referenziate, **giocabilità reale dei puzzle** (labirinti con
percorso valido, parole effettivamente nascoste nel word search, celle
corrette nei cruciverba, sudoku risolvibile), accessibilità (alt text,
contrasto, dimensione font). Restituisce una punch list di problemi.

**Cosa NON fa**: non valuta il rendering visivo finale (serve un occhio umano
o un test browser) e non genera contenuto creativo — verifica solo l'esistente.

**Identità tecnica**: `pc-print-card-qa`.

---

### 7. Auditor di Sistema (audit completo del sito)

**Quando lo attivi**: vuoi una fotografia onesta dello stato del sito —
bug, incongruenze, cosa funziona — su tutto il repo, non solo sull'ultimo
commit.

**Frasi naturali che lo attivano automaticamente**:

- *"Fammi un audit approfondito del sito."*
- *"Controlla tutto il sito, ci sono incongruenze?"*
- *"Pro e contro, dimmi che bug ci sono."*
- *"Il sito è in ordine? Fai una verifica seria."*

**Cosa fa**: build Hugo, integrità dei link interni (distinguendo i link
realmente rotti dai link verso articoli calendarizzati, che NON sono bug),
ordering degli articoli pubblicati lo stesso giorno, completezza del
frontmatter, anti-pattern banditi, coerenza tra file (menu, sigla COI,
pagine legali, documentazione agenti), peso delle immagini. Produce un
report tabellare con PRO / bug per gravità / raccomandazioni.

**Cosa NON fa**: non corregge niente, non committa, non pusha, non apre
PR né issue. È un auditor in sola lettura — le correzioni le autorizzi tu.
È diverso dal **Release Engineer** (che controlla solo il diff prima di un
push) e dall'audit settimanale automatico `audit-sito.yml`.

**Identità tecnica**: `pc-site-auditor`.

---

### 8. Verificatore Visivo Foto (gate caption/alt) — 🔴 GATE OBBLIGATO

**Da maggio 2026 questo agent è il gate visivo obbligato** richiamato automaticamente da **pc-article-reviewer** ogni volta che un articolo contiene `{{< foto >}}`. Esiste dopo l'incidente del 15 maggio 2026 (articolo "Giro d'Italia 2026 a Formia"): l'AI aveva scritto caption fabbricate dai testi FEPIVOL — *"briefing davanti alla Colonna Mobile"* su foto che mostrava due volontari in auto, *"marea di volontari accorsi"* su tre ragazzi in posa. Caption sciolte dalla realtà visiva, attribuzioni sbagliate (foto nostre attribuite al FEPIVOL).

**Cosa fa**: per ogni `{{< foto >}}`, esegue **Read multimodale** della foto sorgente (Claude vede l'immagine), confronta con alt e caption dichiarati, applica fix se trova incoerenze. Verifica anche l'attribuzione: foto utente (file da `~/Scaricati/IMG-*` o `~/Immagini/*`) = "Foto: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma" come default. Mai attribuirle a soggetti terzi solo perché il task cita testi di quei soggetti.

**Identità tecnica**: `pc-photo-caption-verifier`.

---

### 9. Accessibility Designer IAAP CPACC (audit WCAG contenuti)

**CV**: certificazione IAAP CPACC, 15 anni audit WCAG su PA italiana (INPS, INAIL, Min. Salute, Agenzia Entrate). Membro gruppo AGID per la "Dichiarazione di accessibilità". Autore manuali pratici Designers Italia su accessibilità contenuti.

**Quando lo attivi**: vuoi un check WCAG sui CONTENUTI di un articolo o di una pagina — non solo sul rendering HTML (che è il lavoro di Lighthouse).

**Frasi naturali che lo attivano automaticamente**:
- *"Audit accessibilità di questo articolo, va bene per WCAG?"*
- *"Controlla alt e contrasto."*
- *"Sigle sciolte alla prima occorrenza?"*

**Cosa fa**: verifica alt foto significativi (no "Immagine di…"), gerarchia heading H2→H3 senza salti, link descrittivi (no "clicca qui"), sigle PC sciolte alla prima occorrenza, lingua dichiarata per pagine tradotte, tabelle con scope + caption dove serve, contrasto badge custom. Report con riferimento puntuale ai success criteria WCAG (1.1.1, 1.3.1, 1.4.3, 2.4.4, 3.1.1, 3.1.4).

**Identità tecnica**: `pc-accessibility-auditor`.

---

### 10. Content Strategist Editoriale (freschezza articoli)

**CV**: 18 anni ex-vicedirettore Repubblica.it (cronaca + sicurezza), ex-caporedattore web ANSA.it, Master Content Strategy SDA Bocconi. Cura di 3 progetti AGID sulla freschezza dei contenuti PA.

**Quando lo attivi**: vuoi sapere quali articoli sono scaduti, vecchi con dati obsoleti, o da aggiornare prima di una revisione editoriale.

**Frasi naturali che lo attivano automaticamente**:
- *"Ci sono articoli vecchi da aggiornare?"*
- *"Fai un audit della freschezza degli articoli."*
- *"Articoli con scadenza passata da archiviare?"*

**Cosa fa**: sweep articoli con `scadenza:` superata (proponi ARCHIVIA/AGGIORNA/PROROGA), audit articoli > 18 mesi su topic time-sensitive, verifica norme citate (per check vigenza puntuale rinvia all'agent giuridico), telefoni/URL che possono essere cambiati, conteggi cristallizzati banditi dalla regola "niente conteggi inventario sul sito" (maggio 2026).

**Si integra con il workflow `gestione-scadenze.yml`** (lunedì 09:37 UTC), che apre issue automatica con elenco articoli scaduti.

**Identità tecnica**: `pc-content-freshness`.

---

### 11. Glottologa Italiano L2 (versione facile A2 CEFR)

**CV**: dottorato in Linguistica Applicata all'**Università per Stranieri di Siena**, 8 anni glottologa CILS, esperienza didattica con migranti in CPIA Roma/Milano/Bologna, membro gruppo AGID "Versione facile da leggere" 2024.

**Quando lo attivi**: vuoi creare la versione facile da leggere di un articolo (rivolta a parlanti italiano L2, persone con disabilità cognitive, anziani con poca scolarizzazione).

**Frasi naturali che lo attivano automaticamente**:
- *"Genera la versione facile di questo articolo."*
- *"Versione italiano L2 di questa pagina."*
- *"Riscrivi in italiano semplice per A2."*

**Cosa fa**: produce `<slug>-facile.md` con regole **CEFR A2** rigorose — frasi 8-12 parole, lessico delle 2000 parole più frequenti, sigle sempre sciolte, verbi al presente, voce attiva, niente subordinate concatenate, niente metafore. Aggiunge il cross-frontmatter (`versione_facile:` sull'originale, `versione_facile_di:` + `build:list:never` sulla versione facile per escluderla da homepage/archivio/RSS).

**Eccezione gate AGID**: il file `*-facile.md` NON segue il linguaggio AGID standard ma le regole CEFR A2; `pc-article-reviewer` NON viene invocato su di esso (vedi CLAUDE.md § "Auto-gate AGID — eccezione registro").

**Identità tecnica**: `pc-italian-l2-writer`.

---

### 12. SEO Editor / Internal Linker (linkografia interna)

**CV**: 12 anni content editor digitale a **La Stampa** + **Il Sole 24 Ore Digital**, Master Information Architecture al **Royal College of Art** di Londra, autore del libro "Linkografia delle PA" (Designers Italia, 2024).

**Quando lo attivi**: vuoi rivedere la linkografia interna di un articolo prima della pubblicazione.

**Frasi naturali che lo attivano automaticamente**:
- *"Suggerisci link interni per questo articolo."*
- *"L'articolo ha abbastanza link al glossario e ai kit?"*
- *"Quali articoli correlati metterei in fondo?"*

**Cosa fa**: scansiona il corpo per sigle e entità (rischi, kit calamità, standard ISO, categorie vulnerabili), mappa ciascuna alla pagina madre del sito (glossario, `/rischio-sismico/`, `/formazione/kit-calamita-anziani/`, ecc.), propone una sezione "Sul nostro sito" con 4-6 link interni prima delle "Fonti istituzionali" (regola AGID: prima rispondi sul tuo sito, poi rinvia a fonti esterne). Massimo 1 link per concetto, prima occorrenza.

**Identità tecnica**: `pc-internal-linker`.

---

### 13. SEO Technical Specialist (meta / OG / structured data)

**CV**: certificazione **Google Search Central** 2023, 10 anni SEO technical lead in agenzie digital per portali PA (Min. Cultura, Min. Salute campagne, INPS sezione Sostegni). Cura del toolkit Designers Italia "SEO per servizi pubblici digitali".

**Quando lo attivi**: vuoi verificare che un articolo sia ottimizzato per Google e per le anteprime social prima della pubblicazione.

**Frasi naturali che lo attivano automaticamente**:
- *"Controlla il SEO di questo articolo."*
- *"Meta description OK?"*
- *"L'anteprima OG su Facebook funziona?"*

**Cosa fa**: verifica meta description ≤160 char, title ≤60, slug SEO-friendly, OG image esiste 1200×630, Twitter Card, JSON-LD Article (Schema.org), canonical, presenza in sitemap.xml, inclusione in RSS feed, lang attribute. Report PASS/WARN/FAIL per ciascun check.

**Identità tecnica**: `pc-seo-checker`.

---

### 14. Avvocato Amministrativista (vigenza norme citate)

**CV**: laurea Giurisprudenza LUISS con dottorato Diritto Amministrativo Sapienza, 14 anni consulente legislativo **Camera dei Deputati** (Ufficio Studi e Documentazione, specializzazione PC + ambiente), autore manuale **"La Protezione Civile dopo il D.Lgs. 1/2018"** (Giuffrè, 2023).

**Quando lo attivi**: vuoi sapere se le norme citate in un articolo sono ancora vigenti — utile per articoli vecchi e per nuovi articoli che citano normativa specifica. Verifica anche la **fedeltà strutturale** delle pagine che *riproducono* una norma articolo per articolo (tabelle Capo/articoli, sintesi per articolo): Capi, intervalli e rubriche devono combaciare con la fonte primaria.

**Frasi naturali che lo attivano automaticamente**:
- *"Le norme citate qui sono ancora vigenti?"*
- *"Controlla i riferimenti di legge."*
- *"La L. 225/1992 vale ancora?"* (no, è abrogata dal D.Lgs. 1/2018)
- *"La struttura del Codice (Capi/articoli) è corretta?"*

**Cosa fa**: estrae citazioni normative dal corpo (D.Lgs., L., L.R., DGR, DPCM, D.M.), verifica via WebFetch/Firecrawl su **Normattiva** / **Gazzetta Ufficiale** / **Consiglio regionale Lazio** / **BURL Lazio** se ogni norma è vigente, abrogata o modificata. Conoscenza pregressa di norme PC fondamentali (D.Lgs. 1/2018 vigente, L. 225/1992 abrogata, **L.R. Lazio 2/2014 = legge regionale PC vigente**, ecc.) per evitare WebFetch inutili. Per le pagine che riproducono una norma confronta Capi/articoli/rubriche con la fonte primaria (Normattiva per le statali, Consiglio regionale per le L.R. — Normattiva non contiene le regionali). Suggerisce sostituzioni dove abrogata o **riallinea le strutture fabbricate**.

**Identità tecnica**: `pc-normative-verifier`.

---

### 15. Correttore di bozze (refusi e ortografia)

**Quando lo attivi**: vuoi una rilettura mirata a refusi ed errori ortografici/grammaticali su uno o più file, una cartella, o le schede statiche. Diverso dal Caporedattore (`pc-article-reviewer`, che fa revisione AGID degli articoli in `content/comunicazioni/`): questo agent caccia **refusi** ed **errori ortografici/grammaticali** su QUALSIASI contenuto, incluse le **schede statiche HTML** in `static/formazione/` e `static/giochi/` (il punto cieco da cui era passato "cuoperti"→"copriti").

**Frasi naturali che lo attivano automaticamente**:
- *"Controlla i refusi in questo articolo."*
- *"Cerca errori di battitura/ortografia."*
- *"Rileggi per refusi questa scheda."*
- *"Bonifica il legacy una sezione per volta."*

**Cosa fa**: usa il correttore deterministico `scripts/check-refusi.py` (hunspell it_IT via spylls + allowlist `scripts/dizionario-pc.txt`) come prima passata, poi giudica ogni parola sospetta (refuso vs nome proprio/sigla/termine tecnico) e applica le correzioni o aggiorna l'allowlist. Restituisce: refusi corretti, parole valide aggiunte al dizionario, e una passata di lettura per errori grammaticali/di accordo che il correttore non vede. Complementare al workflow settimanale `controllo-refusi.yml`.

**Identità tecnica**: `pc-correttore-bozze`.

---


### 18. Fact-checker (gate dei fatti e delle fonti) — 🔴 GATE OBBLIGATO

**Da settembre 2026 è il gate obbligato** su ogni contenuto con dati verificabili (date, orari, bilanci di vittime e superstiti, quantità, cause, norme, citazioni, dati da dataset), richiamato anche da `pc-article-reviewer` (§ 12). Esiste dopo l'audit del 6 settembre 2026: la scheda Rigopiano contava 4 bambini fra le vittime (erano fra i superstiti), attribuiva la valanga al terremoto (nesso non dimostrato) e riportava un orario diverso dalla ricostruzione INGV.

**Frasi naturali**: *"verifica i dati di questo articolo"*, *"le fonti sono giuste?"*, *"controlla che i numeri tornino"*, *"questo caso studio è affidabile?"*.

**Cosa fa**: estrae ogni affermazione verificabile, la confronta con la fonte primaria (INGV, DPC, VVF, ISPRA, Normattiva, MIM, dataset del sito) e produce una tabella affermazione → fonte → verdetto; corregge ciò che è smentito in tutti i file che ripetono il dato, riformula in modo prudente ciò che non è verificabile, blocca il commit se un dato sensibile resta senza fonte.

**Identità tecnica**: `pc-fact-checker`.

---

### 19. Revisore didattico e della sicurezza (materiali scolastici) — 🔴 GATE OBBLIGATO

**Gate obbligato** su ogni scheda stampabile, kit scuola, kit calamità, rubrica, gioco o percorso nuovo o modificato. Esiste perché la filastrocca della Tartaruga saggia consigliava il divano come riparo e «non avere paura» come regola, le note per l'adulto sparivano dal foglio stampato e un esercizio presentava come legge un limite di 5 minuti.

**Frasi naturali**: *"controlla questa scheda prima di darla ai docenti"*, *"va bene per l'infanzia?"*, *"la rubrica è corretta?"*, *"il kit per le scuole è a posto?"*.

**Cosa fa**: verifica sicurezza delle istruzioni (allineamento DPC), assenza di divieti assoluti senza scenario, adeguatezza all'età, rubriche senza emozioni come livelli, normativa scolastica vigente (OM 3/2025, D.M. 183/2024, Accordo 17/4/2025), esercizi e soluzioni che tornano, avvertenze dentro il wrapper stampabile, parità dei quattro formati (script `check-parita-schede.py`, `check-dati-schede.py`), licenze ARASAAC/ISO 7010; delega i fatti al fact-checker.

**Identità tecnica**: `pc-didattica-reviewer`.

---

### 20. Comitato scientifico interno

**Quando lo attivi**: contenuti che spiegano un fenomeno, una causa, una scala, un codice colore o un comportamento di autoprotezione. Esiste perché una scheda presentava il terremoto come innesco della valanga di Rigopiano.

**Frasi naturali**: *"è scientificamente corretto?"*, *"stiamo spiegando bene il rischio?"*, *"magnitudo o intensità?"*.

**Cosa fa**: controlla il ragionamento (cause sostenute dalle fonti primarie, scale e unità, pericolosità/vulnerabilità/rischio, previsione vs evento in corso), il tono della comunicazione del rischio e la gerarchia delle fonti (DPC → CNR/ISPRA/INGV → EENA → ISO).

**Identità tecnica**: `pc-revisore-scientifico`.

---

### 21. Caposervizio di cronaca e deontologia

**Quando lo attivi**: articoli su eventi reali, anniversari di tragedie, vicende giudiziarie, contenuti che citano persone, minori, vittime, indagati.

**Frasi naturali**: *"questo articolo di cronaca è corretto?"*, *"possiamo scrivere così?"*, *"stiamo tutelando i minori?"*.

**Cosa fa**: 5W nel lede, titolo che non eccede i fatti, attribuzione di ogni informazione, presunzione di non colpevolezza e fasi processuali, Carta di Treviso, tutela delle vittime, niente dati personali, orari arrotondati, ruolo del Gruppo secondo la Circolare DPC 6/8/2018, note di aggiornamento datate.

**Identità tecnica**: `pc-desk-giornalistico`.

---

### 22. Responsabile della conformità legale

**Quando lo attivi**: modifiche a privacy, accessibilità, note legali, trasparenza, social media policy, `hugo.toml`; nuovi trattamenti di dati; scadenze del 23 settembre e del 31 marzo.

**Frasi naturali**: *"la privacy è a posto?"*, *"la dichiarazione di accessibilità è aggiornata?"*, *"chi è il nostro RPD?"*.

**Cosa fa**: coerenza titolare/RPD/basi giuridiche per un ente pubblico, modello AgID della dichiarazione, calendario degli adempimenti, corrispondenza fra ciò che le pagine dichiarano e ciò che il sito fa, licenze. Non certifica: prepara il testo corretto e indica cosa deve confermare il Comune o il RPD. Il calendario è tenuto dal workflow `scadenze-conformita.yml`.

**Identità tecnica**: `pc-conformita-legale`.

---

### 23. Ingegnere dell'integrità tecnica

**Frasi naturali**: *"il sito è integro?"*, *"gli ZIP funzionano offline?"*, *"le ancore sono a posto?"*, *"i PDF sono leggibili?"*.

**Cosa fa**: esegue e interpreta `check-integrita-asset.py` (file vuoti o corrotti, inventario PDF), `check-ancore.py` (frammenti e mailto), `check-parita-schede.py`, `check-jsonld.py`, smoke test e fingerprint live; controlla a mano gli stati dell'interfaccia (caricamento, vuoto, errore). Esiste dopo favicon vuota, PNG corrotto, 17 ancore rotte, 234 link assoluti negli ZIP, e-mail codificata due volte.

**Identità tecnica**: `pc-integrita-tecnica`.

---

### 24. Revisore della coerenza trasversale

**Frasi naturali**: *"il sito si contraddice da qualche parte?"*, *"kit e pagine rischio dicono la stessa cosa?"*.

**Cosa fa**: inventario delle informazioni ripetute (comportamenti, kit, numeri, dati istituzionali, eventi, norme, definizioni) e allineamento di ogni copia alla fonte canonica (pagine rischio, chi-siamo, numeri_utili.yaml, Normattiva). Esiste perché la checklist del kit elencava le candele che la pagina blackout vieta.

**Identità tecnica**: `pc-coerenza-trasversale`.

---

### 25. Revisore del codice

**Quando lo attivi**: ogni modifica non banale a template, partial, shortcode, CSS, JavaScript, script Python; bug di interfaccia.

**Cosa fa**: legge il diff riga per riga con la checklist Hugo (subpath, escape, guardie), JavaScript (stati, sicurezza, tastiera), CSS (scoped, isole brand, stampa), Python (idempotenza, fail-safe); esegue build, `node --check`, `py_compile`, `check-jsonld`, `check-ancore`, menu-sync.

**Identità tecnica**: `pc-revisore-codice`.

---

### 26. Responsabile delle automazioni

**Quando lo attivi**: creazione o modifica di un workflow, run falliti, job lenti, nuove fonti dati, routine.

**Cosa fa**: YAML validi, `timeout-minutes`, permessi minimi, pin a SHA, anti-loop, trigger, modello di priorità del deploy (un merge per volta), copertura del watchdog, dipendenze installate, documentazione in rule 10 e manuale.

**Identità tecnica**: `pc-revisore-automazioni`.

---

### 27. Responsabile della sicurezza

**Quando lo attivi**: modifiche a `.htaccess`, CSP, workflow con segreti, nuovi widget o fonti, allarmi.

**Cosa fa**: segreti e dati personali, CSP e header coerenti con ciò che il sito carica, supply chain (pin, vendor senza CDN), superficie JavaScript, catena allerta, risposta agli incidenti; hardening progressivo in Report-Only prima dell'enforcing.

**Identità tecnica**: `pc-sicurezza`.

---

### 28. Responsabile delle versioni multilingue

**Frasi naturali**: *"le traduzioni sono aggiornate?"*, *"l'inglese è corretto?"*.

**Cosa fa**: ogni traduzione (7 lingue, facile-da-leggere multilingua, poster) dice esattamente ciò che dice l'italiano canonico; lingua naturale per un lettore in stress; markup `language`/hreflang/lang; equivalente HTML dei poster.

**Identità tecnica**: `pc-revisore-traduzioni`.

---

### 29. Responsabile dei dati aperti e dei feed

**Cosa fa**: validità (JSON, XML, CAP OASIS, RSS, sitemap), coerenza fra formati e copie (CSV ↔ JSON ↔ pagine), metadati e licenze, freschezza, regole di aggiornamento per delta, identificatori stabili, nessun dato personale.

**Identità tecnica**: `pc-dati-e-feed`.

---

### 30. Direttore delle esercitazioni della catena di emergenza

**Frasi naturali**: *"se scatta un'allerta rossa adesso, funziona tutto?"*, *"facciamo un'esercitazione"*.

**Cosa fa**: simula in locale (mai su `main`) un'allerta e un'emergenza dal bollettino alla home, alla pagina lite, al CAP, al Telegram, con degradazioni e ritorno al verde; produce un verbale anello per anello.

**Identità tecnica**: `pc-esercitazione-emergenza`.

---

### 31. Verificatore visivo del rendering

**Quando lo attivi**: markup HTML custom nei contenuti, nuovi componenti, schede stampabili, mini-app, CSS strutturale.

**Cosa fa**: server Hugo locale, screenshot con Playwright a 375/768/1280 px e in stampa A4, letti davvero (Read multimodale) per trovare testo schiacciato, immagini giganti, contrasto, note mancanti sul foglio, pagine che sbordano.

**Identità tecnica**: `pc-verifica-visiva`.

---

### 32. Responsabile dell'usabilità e dell'architettura dell'informazione

**Frasi naturali**: *"il sito si naviga bene?"*, *"un anziano trova i numeri utili?"*, *"dove metto questa pagina?"*.

**Cosa fa**: percorsi critici per profilo (cittadino in emergenza, genitore, docente, anziano, volontario, giornalista, straniero) con soglie di click, coerenza delle etichette, pagine orfane, vicoli ciechi, Miller sui menu, priorità mobile; raccomanda e procede (rule 07).

**Identità tecnica**: `pc-usabilita`.

---

### 33. Custode della documentazione

**Quando lo attivi**: dopo ogni modifica strutturale (agenti, script, workflow, shortcode, sezioni, routine, regole).

**Cosa fa**: ogni componente reale è documentato e ogni documentazione descrive un componente reale (CLAUDE.md, rules, agenti, manuale, AGENTS.md, CONTESTO-PROGETTO.md); manuale e rules dicono la stessa cosa; incidenti con la loro lezione.

**Identità tecnica**: `pc-documentazione`.

---

### 34. Direttore dell'audit interno

**Quando lo attivi**: audit mensile (routine `trig_01RMQwDs5Ku2mRfkwkDZnKmx`, il 3 del mese alle 06:00), prima di una distribuzione importante, dopo un incidente, o *"fammi l'audit completo"*.

**Cosa fa**: esegue tutti gli script deterministici, invoca tutti gli specialisti, consolida i rilievi nel formato dell'audit esterno (prova, impatto, correzione, verifica, P1/P2/P3), corregge la Categoria A fino a live, lascia in PR la Categoria B, apre issue con responsabile per ciò che va validato da Comune, RPD, RSPP o docenti; rapporto in `riferimenti-interni/audit-interni/`.

**Identità tecnica**: `pc-audit-completo`.

---

## 19.2 Esempi di workflow tipici

### Pubblicare un articolo nuovo (sequenza ideale)

1. Scrivi l'articolo (con Claude o da solo).
2. *"Mi rivedi questo articolo prima di pubblicare?"* → **Caporedattore** ti
   dice cosa sistemare.
3. Sistemi gli appunti.
4. *"Verifica prima del push, va tutto bene?"* → **Release Engineer** ti
   dice GO/NO-GO.
5. Pubblichi (`git push` o "pubblica" in chat).
6. Aspetti che il workflow `genera-social-bozze.yml` finisca (~5 minuti).
7. *"Mi rivedi le bozze social?"* → **Risk Communication Specialist** ti
   prepara i testi finali.

### Aggiungere foto a un articolo

1. Hai l'articolo aperto e una o più foto da mettere.
2. *"Ecco le foto dell'intervento, mettile nell'articolo."* →
   **Art Director** applica fascia blu, posiziona inline, scrive il
   shortcode `{{< foto >}}`.
3. *"Verifica prima del push?"* → **Release Engineer** controlla.
4. Pubblichi.

### Pulire le issue

1. *"Controlla le issue aperte."* → **Project Manager** (la prima volta
   guida a installare `gh`).
2. L'agent ti propone una tabella: quali sono obsolete, quali da fixare.
3. Confermi le chiusure batch.

---

## 19.3 Domande frequenti

**D: E se Claude non capisce e attiva l'agent sbagliato?**

R: Riformula la richiesta in modo più esplicito. Esempio: invece di *"controlla
questo"* (ambiguo), scrivi *"controlla l'articolo prima di pubblicare"* (attiva
il Caporedattore) o *"verifica il deploy prima di pubblicare"* (attiva il
Release Engineer).

In casi rari puoi anche scrivere il nome tecnico: *"usa pc-issue-triage per
pulire le issue"*.

**D: Posso usare più agent insieme?**

R: Sì. Esempio: *"controlla l'articolo + verifica il deploy + rivedi le bozze
social"* — Claude li attiva uno dopo l'altro o in parallelo se sono
indipendenti.

**D: Gli agent funzionano anche da mobile?**

R: Sì, da app Claude Android. La conversazione è identica a quella desktop.
La differenza è solo che da mobile non puoi installare/autenticare `gh`
locale, quindi l'agent **Project Manager (issue)** funziona solo da PC.

**D: Posso modificare un agent o crearne uno nuovo?**

R: Sì, sono file `.md` in `.claude/agents/`. Ogni file ha un frontmatter
con `name`, `description` (la frase da cui Claude capisce quando attivare),
`tools` (allowlist), e poi il system prompt che lo specializza. Per crearne
uno nuovo, copia uno esistente come template e modifica.

**D: Cosa succede se l'agent fa un errore?**

R: Tutti gli agent hanno divieti espliciti: non pubblicano sui social, non
fanno push, non chiudono issue senza verifica, non sostituiscono il banner
articolo. Il rischio è limitato. Ma se vedi qualcosa di anomalo nei suoi
output, basta dirglielo: *"hai sbagliato, l'articolo non aveva quel
problema"* — e Claude corregge.

---

## 19.4 File degli agent (riferimento tecnico)

| File | Ruolo | Background dichiarato |
|---|---|---|
| `.claude/agents/pc-article-reviewer.md` | Caporedattore | 18 anni Content Designer PA, formazione Crusca |
| `.claude/agents/pc-image-fixer.md` | Art Director | 14 anni visual design PA, AIAP |
| `.claude/agents/pc-issue-triage.md` | Project Manager | 16 anni Engineering Manager OSS/CNCF |
| `.claude/agents/pc-deploy-validator.md` | Release Engineer | 15 anni SRE per PA italiana |
| `.claude/agents/pc-social-publisher.md` | Risk Communication | 12 anni Comunication Officer PC, contributor CWA CEN/CENELEC |
| `.claude/agents/pc-print-card-qa.md` | Print Quality Engineer | 10 anni Print Production Specialist per editori didattici |
| `.claude/agents/pc-site-auditor.md` | Auditor di Sistema | 17 anni QA Lead e auditor tecnico per portali PA |
| `.claude/agents/pc-fact-checker.md` | Fact-checker | 15 anni verifica dei fatti in quotidiani e agenzia, desk scientifico |
| `.claude/agents/pc-didattica-reviewer.md` | Revisore didattico e sicurezza | 20 anni insegnamento, coordinamento ed. civica, RSPP di istituto, «Io non rischio» |
| `.claude/agents/pc-revisore-scientifico.md` | Comitato scientifico interno | voce collettiva: meteorologo, geologo, idrologo, sismologo, vulcanologo, AIB, climatologo, sanità pubblica |
| `.claude/agents/pc-desk-giornalistico.md` | Caposervizio di cronaca | 22 anni in redazione, formatore OdG su deontologia e cronaca giudiziaria |
| `.claude/agents/pc-conformita-legale.md` | Conformità legale | 16 anni giurista e RPD per enti locali, docente ANCI |
| `.claude/agents/pc-integrita-tecnica.md` | Integrità tecnica | 14 anni release engineer e QA di portali statici e pacchetti offline |
| `.claude/agents/pc-coerenza-trasversale.md` | Coerenza trasversale | 12 anni redattore capo di portale istituzionale e knowledge manager PC |
| `.claude/agents/pc-revisore-codice.md` | Revisore del codice | 15 anni frontend senior e code review su design system italiano |
| `.claude/agents/pc-revisore-automazioni.md` | Automazioni | 12 anni ingegnere di piattaforma e CI/CD per servizi con vincoli di continuità |
| `.claude/agents/pc-sicurezza.md` | Sicurezza | 14 anni sicurezza applicativa e risposta agli incidenti per PA |
| `.claude/agents/pc-revisore-traduzioni.md` | Versioni multilingue | 15 anni traduttore istituzionale (UE, DG ECHO) e localization manager |
| `.claude/agents/pc-dati-e-feed.md` | Dati aperti e feed | 12 anni data steward open data e integratore CAP |
| `.claude/agents/pc-esercitazione-emergenza.md` | Esercitazioni catena emergenza | 18 anni sala operativa e responsabile esercitazioni di centro funzionale |
| `.claude/agents/pc-verifica-visiva.md` | Verifica visiva | 12 anni QA visuale e regressione grafica, stampa A4 |
| `.claude/agents/pc-usabilita.md` | Usabilità e IA | 14 anni UX researcher e information architect, kit Designers Italia |
| `.claude/agents/pc-documentazione.md` | Documentazione | 13 anni technical writer e knowledge base docs-as-code |
| `.claude/agents/pc-audit-completo.md` | Direttore audit interno | 20 anni audit di sistemi pubblici (ISO 19011/27001/22301) e verifiche accessibilità |

I background sono "personae" usati per ancorare le valutazioni a standard
verificabili (linee guida AGID, ISO 22329, WCAG, CWA, ecc.). Non sono persone
reali: sono profili professionali che il modello AI usa per ragionare con la
giusta lente.

---

## 19.5 Manutenzione futura

- Quando aggiungi un nuovo agent in `.claude/agents/`, **aggiorna anche
  questa Parte 19** con frasi naturali di attivazione + identità tecnica.
- Quando modifichi la `description` di un agent (la frase che Claude usa per
  capire quando attivarlo), assicurati che le frasi naturali documentate qui
  continuino a fare match. Test pratico: scrivi una di queste frasi a Claude
  in una nuova sessione e verifica che l'agent giusto si attivi.
- Non rimuovere agent senza prima rimuovere i riferimenti nel manuale.
