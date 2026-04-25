# Proattività e Coerenza — Verifica di Pattern Simili

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
Sono stati fatti 4 file con `sed` su `/quizpc/index.html` e `/formazionepc/index.html`, ma è stato lasciato `/abili-a-proteggere/index.html` (stessa categoria di bug) e `/giochi/index.html` (stessa categoria di bug, in 3 punti diversi del repo). I contatori dei giochi nella tabella della pagina Formazione sono rimasti a 8/9/30 anche se la prosa sopra parlava già di 33 giochi. L'utente ha dovuto chiedere a parte la sistemazione e ha detto: "se non te lo avessi chiesto, avremmo avuto un sito con errori". Questa regola nasce da quell'incidente.

## Vincolo correlato

La regola "Aggiornamento automatico docs dopo modifiche strutturali" (CLAUDE.md, MANUALE-SITO, archetype, README) è un **caso particolare** di questa regola più generale. Anche docs, manuale e archetype rientrano nella passata di verifica.
