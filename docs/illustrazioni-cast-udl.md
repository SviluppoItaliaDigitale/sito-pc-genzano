# Illustrazioni didattiche e CAST UDL 3.0

Sistema grafico introdotto il 2026-10-08 sul ramo di revisione delle schede.

## Scopo
Usare un'immagine **quando aiuta a capire una relazione, una procedura o un pericolo**, non per decorare tutte le pagine. I materiali testuali già chiari non richiedono necessariamente una figura.

## Criteri CAST applicati
- **1.2 Percezione:** stessa informazione in forma visiva e testuale; alt significativo e didascalia, senza testo essenziale affidato soltanto all'SVG.
- **2.1 Lessico e simboli:** titoli leggibili e termini chiariti, niente simbologia ambigua.
- **2.5 Più media:** figure collegate al paragrafo esplicativo o alla procedura descritta.
- **3.2 Connessioni e idee essenziali:** colori al servizio delle differenze, passaggi numerati, niente distrazioni grafiche.
- **Principi di Mayer (apprendimento multimediale):** coerenza (niente elementi superflui), segnalazione, contiguità fra parola e figura, segmentazione delle procedure, termini spiegati prima. Dettagli in `.claude/rules/03-accessibility.md`.
- **Accessibilità WCAG:** descrizioni alternative, contrasto leggibile, messaggi non basati solo sul colore, testo vicino all'illustrazione.

## Asset
Gli SVG stanno in `static/formazione/illustrazioni-udl/`; il nome del file dice che cosa mostrano. Prima di disegnarne uno nuovo, guarda se ne esiste già uno riusabile.

Gli asset sono SVG statici locali, senza JavaScript o font esterni, con proporzioni 1200×620. Usare il shortcode `illustrazione-udl` con `src`, `alt` e `caption`. Il testo della pagina rimane sufficiente anche senza immagini.

## Illustrazioni preparate con strumenti esterni
Prima del commit: aprire e guardare l'immagine; verificare che gesto e scena coincidano con le indicazioni del DPC; scrivere `alt`, `caption`, `<title>` e `<desc>` su ciò che si vede davvero; togliere metadati, commenti o testi che citino lo strumento usato; controllare che le scritte restino dentro il `viewBox` e si leggano su telefono e su A4. Regola completa: `.claude/rules/03-accessibility.md` § «Progettazione universale per l'apprendimento».

## Regola di estensione
Per ogni nuova illustrazione: identificare un bisogno didattico, verificare contenuti e sicurezza con fonti ufficiali, inserire una descrizione alternativa non ridondante, verificare leggibilità su smartphone e carta A4, controllare la resa del sito. Non aggiungere una figura se non aumenta la comprensione.

**Nota:** l'adozione dei criteri CAST non equivale a certificazione CAST o verifica completa WCAG. È necessaria una revisione periodica con utenti reali, docenti e persone con disabilità.

Riferimento: https://udlguidelines.cast.org/representation/language-symbols/multiple-media/

## Leggibilità su smartphone e anteprime
- Una tavola orizzontale con più pannelli non deve essere usata come unica vista su telefono. Per le figure dense, creare una seconda versione SVG alta 720×1180/1440, con suffisso `-mobile.svg`; il shortcode la seleziona automaticamente.
- Non presentare collage di più tavole come anteprima principale: mostrare ogni illustrazione singolarmente, a dimensioni utili. I pannelli verticali devono avere numeri e titoli leggibili e indicazioni anche nel testo vicino.
- Un collegamento apre la figura originale ingrandita, anche in assenza di versione mobile. Su carta A4 controllare l'anteprima e la presenza di informazioni equivalenti nel corpo della pagina.
- Le immagini non sostituiscono la revisione pedagogica, la verifica della sicurezza né la prova con lettori di schermo e persone reali.
