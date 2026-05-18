_[Indice manuale](README.md)_

# Parte 19 — Agenti specializzati Claude Code (maggio 2026)

A maggio 2026 sono stati installati nel repo **agenti specializzati**
in `.claude/agents/` (**quindici al 18 maggio 2026**). Sono profili professionali
virtuali con cui Claude Code ti aiuta nei compiti ricorrenti del Gruppo,
ognuno con un'expertise mirata. La progressione:

- **8 agent dell'apertura** (maggio 2026): redazione AGID, art direction, gestione issue, deploy engineering, comunicazione di crisi, QA schede stampabili, audit di sistema, **gate visivo foto** (aggiunto il 15 maggio dopo l'incidente "Giro d'Italia 2026 a Formia": caption fabbricate dai testi di terzi invece che dalle foto reali).
- **5 agent professionisti aggiuntivi** (15 maggio 2026, in risposta alla richiesta utente *"assumi le migliori professionalità per essere perfetti"*): accessibility auditor IAAP CPACC, content strategist editoriale (Repubblica.it/ANSA), glottologa italiano L2 (Univ. Stranieri Siena), SEO editor (La Stampa/Sole 24 Ore Digital), avvocato amministrativista (Camera Deputati). Ognuno con CV credibile e responsabilità chiara nel ciclo editoriale.
- **2 agent aggiunti il 16-18 maggio 2026**: `pc-photo-caption-verifier` (gate visivo Read multimodale foto, codificato dopo l'incidente Formia), `pc-notebooklm-publisher` (publishing engineer dei materiali multimediali NotebookLM su `/risorse-pronte/`).

**La parte importante:** non devi ricordare nessun nome tecnico. **Scrivi a
Claude in italiano normale**, dicendo cosa vuoi fare, e Claude attiva da solo
l'agente giusto.

> ⚠️ **Da leggere insieme a questa Parte**: la **[Parte 31](parte-31-skill-globali-invocazione.md)** sulle **skill globali Claude Code** invocate col tool `Skill`. Gli agent `pc-*` e le ~100 skill globali sono **complementari**: gli agent sono profili professionali editoriali specifici del sito, le skill sono pattern tecnici trasversali (accessibilità, SEO, audit, ricerca, ecc.). Spesso vanno invocati in sequenza (es. revisione articolo: `pc-article-reviewer` → `pc-photo-caption-verifier` → skill `accessibility` → skill `seo-audit`).

---

## 19.1 I quindici agenti e quando si attivano

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
che IG rifiuta), verifica peso file e dimensioni 1080×1080 / 1080×1920.

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

**Quando lo attivi**: vuoi sapere se le norme citate in un articolo sono ancora vigenti — utile per articoli vecchi e per nuovi articoli che citano normativa specifica.

**Frasi naturali che lo attivano automaticamente**:
- *"Le norme citate qui sono ancora vigenti?"*
- *"Controlla i riferimenti di legge."*
- *"La L. 225/1992 vale ancora?"* (no, è abrogata dal D.Lgs. 1/2018)

**Cosa fa**: estrae citazioni normative dal corpo (D.Lgs., L., L.R., DGR, DPCM, D.M.), verifica via WebFetch su **Normattiva** / **Gazzetta Ufficiale** / **Consiglio regionale Lazio** / **BURL Lazio** se ogni norma è vigente, abrogata o modificata. Conoscenza pregressa di norme PC fondamentali (D.Lgs. 1/2018 vigente, L. 225/1992 abrogata, L.R. Lazio 9/2017 vigente, ecc.) per evitare WebFetch inutili. Suggerisce sostituzioni dove abrogata.

**Identità tecnica**: `pc-normative-verifier`.

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
