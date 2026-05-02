# Proattività e Coerenza — Verifica di Pattern Simili

## Checkpoint pre-operazione batch (precede tutto il resto)

**Prima di iniziare** qualsiasi operazione che tocca **≥5 articoli o ≥5 file in una singola passata** (batch foto, batch frontmatter, mass-rename, sweep editoriale, riscrittura di sezione su molti file, ecc.) **fermati e fai un check visibile all'utente** in 3 righe:

1. **Cosa stai per fare** (il pattern dell'operazione: "modificare il campo X su N file Y").
2. **Quali rules si applicano** (cita per nome i file `.claude/rules/0*.md` pertinenti e la sezione/divieto specifico — non basta dire "le rules", devi citarli).
3. **Perché stai per rispettarle** (collegamento esplicito tra l'operazione e ogni rule citata).

Poi **chiedi conferma** all'utente con un messaggio del tipo *"Confermi questi parametri prima che proceda?"* e **aspetta l'OK esplicito**. Non far partire l'operazione di propria iniziativa.

### Esempio corretto

> Sto per scaricare una foto inline su 60 articoli usando il marker `# TODO-foto-pexels`.
> Rules pertinenti:
> - `02-content-design-pa.md` sezione **"Divieto: foto stock generiche ripetute per macro-tema"** → vieta di assegnare la stessa foto stock a articoli accomunati solo da macro-tema.
> - `02-content-design-pa.md` sezione **"Foto utente — banner pulito vs carosello"** → la foto inline va nel corpo, mai nel campo `image:` del frontmatter.
>
> Per rispettarle proporrei: query specifica per ogni singolo articolo (non query categoriale), preferenza per Wikipedia/NASA/USGS dove possibile. Confermi?

### Esempio errato (proibito)

> Procedo a scaricare le foto sui 60 articoli...
> *(senza checkpoint, senza citare rules, senza conferma — è il pattern che ha generato l'incidente di aprile 2026)*

### Quando il checkpoint NON serve

- Operazione singola (1 articolo, 1 file, 1 fix mirato).
- Operazione esplicitamente già autorizzata in dettaglio dall'utente nel turno precedente con parametri concreti ("modifica i frontmatter di questi 8 articoli specifici e basta").
- Build, test, hugo --quiet, audit read-only.

### Perché esiste questa regola

Ad aprile 2026 un batch di 14 commit ha messo la stessa foto stock (Croce Rossa) su 74 articoli con caption identica. L'incidente è nato perché l'agent ha categorizzato gli articoli per macro-tema e ha lanciato il batch **senza fermarsi a citare le rules**. Il checkpoint pre-batch è il safety-net che impedisce il riprodursi del pattern: rendere il ragionamento sull'applicabilità delle rules **visibile all'utente prima dell'azione**, non dopo.

## Principio

Quando completi un fix, una correzione o un cambio strutturale, **prima di concludere il lavoro** esegui sempre una passata di verifica per cercare lo stesso pattern in altre parti del sito e proponi i fix correlati senza aspettare che l'utente li chieda.

L'utente gestisce il sito da solo e si affida alla tua qualità complessiva, non solo al singolo task. Un fix incompleto che lascia lo stesso problema in altre pagine è un debito tecnico che si trasforma in un bug visibile al cittadino.

## Quando applicare la regola

In modo automatico, dopo ogni:

- **Fix di link o path** (es. `/foo/index.html` → `/foo/`): grep di tutti gli altri pattern simili nel `content/`, nei `themes/`, nelle pagine HTML statiche.
- **Aggiornamento di un contatore** (numero di articoli, schede, giochi, kit, allegati): verifica ogni occorrenza dello stesso contatore in pagine, partial, archetype, MANUALE-SITO, FAQ, hub, sitemap.
- **Modifica di una stringa istituzionale** (numero di telefono, COI, sede, denominazione del Gruppo): grep dell'intero repo, incluso `static/` e `themes/`.
- **Aggiunta o rimozione di contenuti** (scheda, gioco, articolo, pagina): verifica che sia linkata coerentemente da kit, hub, partial, sitemap, archetype, MANUALE.
- **Modifica a uno shortcode, partial o template**: cerca tutti gli usi e verifica che restino coerenti.
- **Bulk replace via sed o grep -l + xargs**: dopo l'esecuzione, fai sempre una passata di controllo per assicurarti che il pattern sia completamente esaurito.
- **Rinomina di file, cartelle, slug**: verifica i link entranti e uscenti.
- **Cambio di convenzione** (badge, naming, struttura frontmatter, schema dati): allinea ogni occorrenza esistente.

## Come applicare la regola

1. Mentre stai leggendo un file per modificarlo, se vedi altre incongruenze evidenti (numeri sbagliati, link rotti, frasi obsolete) **segnalale subito** invece di limitarti al task richiesto. Anche se non rientrano nel "letterale" della richiesta dell'utente.

2. Quando finisci un task complesso, non chiudere con un semplice "fatto" — concludi con un mini-audit che dichiara cosa hai verificato:

   > "Ho controllato anche A, B, C: coerenti. Ho notato anche D: vuoi che lo sistemi?"

3. Per i fix di pattern (link, path, stringhe ricorrenti), prima di committare esegui una grep mirata che dimostra l'assenza di residui:

   ```bash
   grep -rn "<vecchio-pattern>" content/ themes/ static/ 2>/dev/null
   ```

   Se la grep restituisce ancora occorrenze, il task non è completo.

4. Quando crei nuovi contenuti, verifica anche i punti di **riferimento incrociato**: un nuovo articolo va aggiunto agli "Approfondimenti" pertinenti? Una nuova scheda va linkata dal kit della sua fascia? Un nuovo gioco va aggiunto al partial `games-cta.html` e alla mappa del sito?

## Distinzione importante

Questa regola **non autorizza** ad aggiungere feature non richieste o ad espandere lo scope arbitrariamente. La regola del progetto dice: "Don't add features, refactor, or introduce abstractions beyond what the task requires."

Il criterio di confine:

- Se il pattern non corretto è **dello stesso tipo** del bug appena risolto → va sistemato (è completare il fix, non espandere lo scope).
- Se è una **feature nuova o un refactor** → no, va proposto e atteso il via libera dell'utente.

## Casi storici

**25 aprile 2026 — fix Chrome cache `/quizpc/index.html` → `/quizpc/`.**
Sono stati fatti 4 file con `sed` su `/quizpc/index.html` e `/formazionepc/index.html`, ma è stato lasciato `/abili-a-proteggere/index.html` (stessa categoria di bug) e `/giochi/index.html` (stessa categoria di bug, in 3 punti diversi del repo). I contatori dei giochi nella tabella della pagina Formazione sono rimasti a 8/9/30 anche se la prosa sopra parlava già di giochi. L'utente ha dovuto chiedere a parte la sistemazione e ha detto: "se non te lo avessi chiesto, avremmo avuto un sito con errori". Questa regola nasce da quell'incidente.

**25 aprile 2026 — falso allarme su 8 articoli "non ancora scritti".**
Subito dopo aver scritto questa regola, durante un sweep proattivo ho trovato 8 link interni che il render-link hook mostrava come "Contenuto non ancora disponibile" e ho proposto all'utente di scriverli. Era falso: tutti e 8 erano già scritti, `draft: false`, ma con `date` futura — Hugo li escludeva correttamente dalla build fino al raggiungimento della data. Lo span grigio era il graceful degradation di design, **non** un bug. Lezione: prima di proporre di scrivere/creare/aggiungere qualunque cosa che sembra mancante, **verificare l'esistenza fisica del file** (`ls content/...`, `find static/...`). Un link rotto in pagina può significare "manca", "futuro", "rinominato", "draft". Sono cose diverse, e l'azione corretta dipende dalla causa.

## Vincolo correlato

La regola "Aggiornamento automatico docs dopo modifiche strutturali" (CLAUDE.md, MANUALE-SITO, archetype, README) è un **caso particolare** di questa regola più generale. Anche docs, manuale e archetype rientrano nella passata di verifica.
