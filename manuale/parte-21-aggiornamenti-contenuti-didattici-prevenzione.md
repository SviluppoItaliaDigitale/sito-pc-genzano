# Parte 21 — Aggiornamenti contenuti didattici e prevenzione

Questa parte documenta gli aggiornamenti recenti ai contenuti didattici e di prevenzione del sito della Protezione Civile di Genzano di Roma.

## Nuove pagine informative pubblicate

### Scuole di Genzano e rischi locali

Percorso:

`content/rischi-prevenzione/scuole-genzano-rischi-locali.md`

Scopo:

- collegare scuola, famiglie, rischi principali e materiali didattici;
- fornire una pagina prudente, divulgativa e utile per docenti, studenti e genitori;
- rimandare sempre alle fonti ufficiali e ai piani interni delle scuole.

Regole editoriali:

- non inventare nomi di scuole, indirizzi, referenti, numeri o procedure interne;
- non indicare punti di raccolta scolastici non verificati;
- per procedure interne e punti di raccolta rimandare al piano di emergenza del singolo istituto, al Dirigente scolastico, al RSPP e agli addetti designati;
- per aree di attesa comunali e informazioni territoriali rimandare al Piano Comunale di Protezione Civile e alla cartografia operativa;
- usare linguaggio semplice, istituzionale, non allarmistico.

### Rischi principali in parole semplici

Percorso:

`content/rischi-prevenzione/rischi-in-parole-semplici.md`

Scopo:

- offrire una versione semplificata delle regole di autoprotezione;
- aiutare bambini, BES, persone con disabilità cognitive e persone con italiano L2;
- mantenere collegamenti alle pagine complete.

Regole editoriali:

- frasi brevi;
- verbi concreti;
- niente burocratese;
- istruzioni pratiche;
- evitare dettagli tecnici non necessari;
- non sostituire le fonti ufficiali e le pagine complete.

### Kit di emergenza economico e progressivo

Percorso:

`content/rischi-prevenzione/kit-emergenza-economico-progressivo.md`

Scopo:

- spiegare come costruire il kit poco alla volta;
- evitare spese inutili;
- indicare priorità progressive.

Regole editoriali:

- non citare marchi commerciali;
- non citare negozi;
- non suggerire prodotti sponsorizzati;
- non indicare prezzi inventati;
- usare solo categorie generiche di materiali utili in emergenza;
- mantenere una nota esplicita di neutralità commerciale.

## Schede didattiche aggiornate

### Lavaggio completo delle mani

Percorso:

`static/formazione/kit-calamita-bambini/10-routine-lavarsi-mani.html`

Regole:

- non usare più il titolo “Lavarsi le mani in 5 passi”, perché la scheda contiene una procedura più completa;
- usare formule come “Lavaggio completo delle mani” o “Procedura completa per l'igiene delle mani”;
- mantenere impaginazione A4 reale per la stampa;
- evitare testi incoerenti con il numero effettivo di passaggi presenti nell'immagine.

### Unisci i puntini: casco di Protezione Civile

Percorso:

`static/formazione/kit-calamita-bambini/12-unisci-puntini-casco.html`

Regole:

- usare il disegno fornito dall'utente;
- non ricostruire autonomamente l'immagine se è già stato fornito un disegno pronto;
- sostituire l'immagine solo se viene fornito un nuovo file definitivo;
- mantenere la scheda in formato A4 stampabile.

### Mandala del sole

Percorso:

`static/formazione/kit-calamita-bambini/07-mandala-sole.html`

Regole:

- mantenere il mandala semplice;
- evitare disegni troppo complessi per la fascia 3-5 anni;
- non trasformare l'attività in scheda troppo testuale.

## Mappa del sito

Quando vengono aggiunte nuove pagine informative importanti, aggiornare anche la pagina manuale:

`content/mappa-sito/_index.md`

Il file tecnico `sitemap.xml` è generato automaticamente da Hugo e non deve essere modificato a mano.

## Regola C.O.I.

Il riferimento corretto indicato dall'utente è:

**14° C.O.I.**

Non usare “15° C.O.I.” nei testi pubblici, nei manuali o nelle regole di governance.

## Regola generale sulle fonti

Ogni contenuto istituzionale deve distinguere chiaramente tra:

- dati verificati e pubblicati da fonti ufficiali;
- indicazioni generali di autoprotezione;
- contenuti didattici semplificati;
- materiali creativi o attività per bambini.

Non inserire dati territoriali, numeri, procedure, indirizzi, enti o responsabilità se non sono verificati da fonte ufficiale o già presenti nella documentazione comunale del sito.

## Sessione di consolidamento — 6 maggio 2026

Audit strutturale completo del sito (le 7 Fasi del modello di lavoro). Esiti principali:

### Fix di drift documentale e fact errors

- **C.O.I. 14°** allineato in 4 file che avevano l'asserzione invertita (`README.md`, `audit-sito.yml`, `pc-article-reviewer`, `pc-deploy-validator`).
- **Bandiera SPQR di Reggio Emilia** rimossa dall'articolo 1996: era spacciata come "foto storica del terremoto del 15 ottobre 1996". Pubblicata prima che il filtro anti-bandiere fosse aggiunto a `foto-da-wikipedia.sh`.
- **Caption ShakeMap INGV** corrette in 5 articoli (Emilia 2012 + Amatrice 2016): la stessa foto md5-identica era usata in più articoli con caption diverse che dichiaravano "capannone industriale crollato a Mirandola" o "Amatrice in macerie", mentre la foto è una mappa di intensità macrosismica INGV.
- **Duplicato editoriale 24 agosto** sul decimo anniversario di Amatrice 2016: due articoli con stessa data, stesso evento, badge diversi. Tenuto `2026-08-24-amatrice-2016-centro-italia-decimo-anniversario.md` (Comunicazione, taglio narrativo cronologico). Aliases nel file mantenuto preserva l'URL del file rimosso per SEO.

### Pulizia template-injection

- **Box "Kit consigliato per questo rischio"** rimosso da 17 hub di sezione di servizio (`/contatti/`, `/numeri-utili/`, `/cartografia/`, `/allerte-meteo/`, `/area-download/`, `/piano-familiare/`, `/faq/`, `/cosa-fare-adesso/`, `/formazione/`, `/siti-utili/`, `/strumenti/`, `/glossario/`, `/assistente/`, `/attribuzioni-pittogrammi/`, `/pittogrammi/`, `/social-media-policy/`, `/san-pio-da-pietrelcina/`). Il box appariva in 342 file totali in 7 varianti di testo, spesso con messaggio incoerente con il tema della pagina (es. `/contatti/` con "Per vento forte..."). Sostituito con `## Vedi anche` contestuale.
- **Pagine rischio specifico** (`rischi-prevenzione/*.md`) e articoli di comunicazioni: lasciati intatti, il box è coerente lì.

### Asset e performance

- **-2.85 MB di asset** ottimizzati: `favicon.png` 932→10 KB (era duplicato del logo, ridimensionato a 64×64), `logo-pc-genzano.png` 932→237 KB (480×480 sufficiente), 2 webp ricompressi sotto i 200 KB, 8+3 webp duplicati md5 consolidati al filename canonico, articoli ridiretti.
- **Bootstrap Italia bundle**: tentato switch a slim (-750 KB), **rollback** dopo che la navbar custom Italia ha smesso di rispondere. Decisione registrata in memoria: lasciare sempre il bundle 995 KB. Vedi `feedback_bs_italia_no_slim.md`.
- **CSS unused audit**: rimosse 11 classi morte (-66 righe su `custom.css`). Bug fixato: selettore `html.a11y-pause-anim` (troncato) → `html.a11y-pause-animations` (full nome generato dal JS toolbar a11y).

### Card uniformate al pattern v1.0

8 card del sito allineate al pattern hover-lift v1.0 (homepage): `transform: translateY(-3px) + box-shadow: 0 10px 22px rgba(0, 51, 102, 0.14)`. Card a "lift laterale" (`.card-notizia-small`, `.card-social-link`) lasciate invariate per coerenza col layout orizzontale.

### Navigazione

3 nuove pagine prevenzione (`scuole-genzano-rischi-locali`, `rischi-in-parole-semplici`, `kit-emergenza-economico-progressivo`) integrate nell'hub `/rischi-prevenzione/_index.md` (sezione "Pagine di consultazione rapida") e nella mappa sito principale (sezione "Cosa fare in caso di…"). Voci di menu navbar **non toccate** per scelta editoriale ("Rischi in parole semplici" non promosso a primo livello, "Kit pronti per situazioni vulnerabili" lasciato dov'era).

### Fasi NON eseguite (decisione)

- **Description >160 char** su 115 articoli: scelta editoriale del Gruppo, articoli storici lunghi richiedono description ricca. Non riscritti.
- **Foto stock duplicate** scartate dalla pulizia: tra i 9 cluster di duplicati md5 ne restano 1 (3 file Centro Italia 2016 con caption divergenti — risolto col fix Amatrice ShakeMap) e archivio-storico. Decisione: archivio-storico preservato come tale.
- **Verifiche browser** (mobile 320/375/768/1024 px, stampa A4 reale, Lighthouse score, regressioni JS interattive): da fare quando l'utente è davanti al sito live, fuori scope autonomia CLI.
