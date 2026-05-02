_[Indice manuale](README.md)_

# Parte 19 — Agenti specializzati Claude Code (maggio 2026)

A maggio 2026 sono stati installati nel repo cinque **agenti specializzati**
in `.claude/agents/`. Sono profili professionali virtuali con cui Claude Code
ti aiuta nei compiti ricorrenti del Gruppo, ognuno con un'expertise mirata
(redazione AGID, art direction, gestione issue, deploy engineering,
comunicazione di crisi).

**La parte importante:** non devi ricordare nessun nome tecnico. **Scrivi a
Claude in italiano normale**, dicendo cosa vuoi fare, e Claude attiva da solo
l'agente giusto.

---

## 19.1 I cinque agenti e quando si attivano

### 1. Caporedattore (revisione articoli)

**Quando lo attivi**: hai scritto un articolo nuovo o ne hai modificato uno
sostanziale e vuoi un controllo prima di pubblicare.

**Frasi naturali che lo attivano automaticamente**:

- *"Mi rivedi questo articolo prima di pubblicare?"*
- *"Controlla l'articolo `<nome-file>.md`, va bene?"*
- *"Mi dici se ci sono errori in questo articolo?"*
- *"Verifica frontmatter e linguaggio AGID dell'articolo che ho scritto."*

**Cosa fa**: legge il file, applica le 13 categorie di badge, verifica formato
data, lunghezza description (≤160 char per SEO), sezioni rigide delle pagine
rischio, foto secondo convenzione, link interni esistenti, niente conteggi
inventario, niente burocratese, NUE 112 unico numero emergenza Lazio.

**Cosa NON fa**: non riscrive l'articolo da solo. Ti dà una lista di cose da
sistemare e tu decidi.

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
