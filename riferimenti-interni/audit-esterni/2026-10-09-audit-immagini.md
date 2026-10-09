# Verifica immagini del sito — 9 ottobre 2026

**Repository:** `SviluppoItaliaDigitale/sito-pc-genzano`. **Branch verificato per inventario:** `main`.

## Metodo e copertura (non sovrastimare)

L'inventario deriva da `git/trees/main?recursive=1`, non da una visita visiva a ogni pagina. Rilevati **5.468** file con estensione immagine in tutto il repository, di cui **3.888** nella directory pubblica `static/`; i restanti **1.580** sono soprattutto bozze, backup e risorse di sviluppo. Tra i file di `static/` figurano **1.076** codici QR SVG: sono codici funzionali, non illustrazioni narrative. Il conteggio delle immagini non coincide con quello delle illustrazioni da ridisegnare.

Sono stati letti i testi e i metadati XML delle **32** SVG nella directory `static/formazione/illustrazioni-udl/` presenti su `main`, controllando `title`, `desc` e dimensioni dei caratteri. Tutte e 32 hanno `title` e `desc`. **18** contengono almeno un testo con `font-size` inferiore a 18. Questo criterio è un *indicatore di rischio* e non dimostra da solo un'inosservanza delle WCAG. A parte le otto SVG oggetto della PR #1299, non risulta eseguita una revisione visiva a piena risoluzione dei rimanenti file da questo audit.

Le verifiche fatte **non** dimostrano che tutte le 3.888 immagini siano corrette, accessibili o comprensibili. Serve una revisione per uso (illustrazioni scolastiche, emergenze, grafici, fotografia documentale, pittogrammi, infografiche) e per pagina, con prova reale su smartphone e stampa.

### R1 — Illustrazioni con testi piccoli

- **Dove:** `static/formazione/illustrazioni-udl/`, 18 file della base `main` con almeno un testo sotto 18 (per esempio `co2-spazi-confinati.svg` con «NON SCENDERE» a 14, `siccita-risparmio-acqua.svg` con «POTABILE» a 12, altri con avvertenze a 17).
- **Che cosa non va:** testi relativamente minuti possono diventare difficili da leggere quando una SVG 1200×620 viene visualizzata a 360–720 px; la dimensione va controllata nella resa effettiva, insieme al contrasto e alla leggibilità in stampa.
- **Prova:** lettura degli attributi `font-size` nei nodi `text` delle 32 SVG.
- **Priorità:** P2; elevata per indicazioni operative.
- **Esito:** prime due correzioni nei file `co2-spazi-confinati.svg` e `siccita-risparmio-acqua.svg` nel branch `chatgpt/qualita-grafica-20261009`. Restano da verificare a vista gli altri 16 candidati.

### R2 — File fotografici identici con nomi editoriali differenti

- **Dove:** `static/images/dossier/`, fra gli altri:
  - `industriale-mappa-italia.webp`, `neve-sistema-allerta.webp`, `vento-hotspot-italia.webp` hanno lo **stesso SHA Git**.
  - `allertamento-dart-tsunami.webp` e `allertamento-indian-ocean-2004-top.webp` hanno lo **stesso SHA Git**.
  - `frane-hero.webp` e `frane-monte-toc.webp` hanno lo **stesso SHA Git**.
  - `maremoto-hero.webp` e `maremoto-onda-2004.webp` hanno lo **stesso SHA Git**.
- **Che cosa non va:** identità di file con nomi semantici diversi è una possibile incongruenza fra didascalia e contenuto; può anche trattarsi di un riutilizzo editoriale corretto. **Non cambiare la fotografia senza identificarne soggetto e fonte.**
- **Prova:** raggruppamento per SHA dei file pubblici; **20 gruppi** di contenuti byte-per-byte identici nell'intero `static/` (comprendono anche alias deliberati dei pittogrammi).
- **Priorità:** P2 per i dossier, P3 per gli alias pittogrammi.
- **Esito:** da verificare per ogni coppia, confrontando immagine, didascalia e fonte prima di sostituirla.

### R3 — Infografiche PNG di grandi dimensioni

- **Dove:** `static/infografiche/`: **16** PNG; numerosi file misurano circa **4–5 MB**. Per esempio `2026-04-17-kit-emergenza-infografica.png` pesa 5.019.418 byte.
- **Che cosa non va:** dimensioni elevate possono rallentare caricamento e consumo di dati; la compressione, il formato e il comportamento responsive vanno misurati prima di decidere l'intervento, senza peggiorare i testi.
- **Prova:** dimensioni dei blob riportate dall'albero Git.
- **Priorità:** P2.
- **Esito:** da verificare con anteprima, misure pixel e prove web; nessuna ricompressione cieca.

### R4 — Esperimento sul colino: composizione troppo vuota

- **Dove:** `static/formazione/illustrazioni-udl/esperimento-tombino-ostruito.svg` e variante mobile, proposte nella PR #1299.
- **Che cosa non va:** prima versione con oggetti disposti solo nella parte superiore e un piccolo elemento somigliante a un rubinetto anziché a una bottiglia; confronto visivo poco efficace.
- **Prova:** rendering desktop 1200×620 e mobile 720×1180, prima e dopo.
- **Priorità:** P2.
- **Esito:** migliorate entrambi i disegni nella PR #1299: contenitore graduato con livello raccolto decrescente nelle tre prove e bottiglia inclinata riconoscibile; da controllare i gate aggiornati dopo il commit.

### R5 — Controllo editoriale degli scenari a rischio

- **Dove:** tutte le immagini di comportamento in emergenza e attività scolastiche.
- **Che cosa non va:** validità XML e presenza di `alt` non sono prova di comprensibilità. Le immagini devono evitare gesti pericolosi, numeri inventati, ambiguità, testi deformati o inglesi, impaginazioni diverse tra schermo e stampa.
- **Prova:** il confronto tra la tavola SVG originale del tombino e il rendering corretto mostra un difetto non intercettato dal controllo formale.
- **Priorità:** P1 se il disegno insegna un comportamento errato; P2 per impaginazione o scarsa leggibilità.
- **Esito:** controllo visivo umano/editoriale ancora necessario, in particolare per le infografiche complesse; non è ragionevole dichiarare chiuso un audit visivo di migliaia di immagini con il solo inventario automatico.

## Regola di qualità per le successive correzioni

Ogni scena deve essere riconoscibile anche prima di leggere le parole. Titoli e descrizioni **solo in italiano**; testi fuori dalle figure, chiari e non sovrapposti. Per ogni modifica confrontare originale e sostituzione nel contesto della pagina, a 1200/720 px, su stampa A4 e con zoom 200%; verificare font leggibile, contrasti, fonti ufficiali, mantenimento delle didascalie, alternative testuali e assenza di regressioni. Le immagini di emergenza non vanno pubblicate se il significato appare ambiguo.

## Coordinamento

Le otto nuove SVG sono nella PR #1299; evitare modifiche parallele agli stessi file. I due interventi a testi piccoli su `main` sono nel branch `chatgpt/qualita-grafica-20261009`; nessun merge diretto su `main` senza controlli.
