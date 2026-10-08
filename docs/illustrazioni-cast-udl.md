# Illustrazioni didattiche e CAST UDL 3.0

Sistema grafico introdotto il 2026-10-08 sul ramo di revisione delle schede.

## Scopo
Usare un'immagine **quando aiuta a capire una relazione, una procedura o un pericolo**, non per decorare tutte le pagine. I materiali testuali già chiari non richiedono necessariamente una figura.

## Criteri CAST applicati
- **1.2 Percezione:** stessa informazione in forma visiva e testuale; alt significativo e didascalia, senza testo essenziale affidato soltanto all'SVG.
- **2.1 Lessico e simboli:** titoli leggibili e termini chiariti, niente simbologia ambigua.
- **2.5 Più media:** figure collegate al paragrafo esplicativo o alla procedura descritta.
- **3.2 Connessioni e idee essenziali:** colori al servizio delle differenze, passaggi numerati, niente distrazioni grafiche.
- **Accessibilità WCAG:** descrizioni alternative, contrasto leggibile, messaggi non basati solo sul colore, testo vicino all'illustrazione.

## Asset consegnati
- `terremoto-tre-gesti.svg`: sequenza abbassati-riparati-tieniti; riuso nella pagina facile da leggere e rischio sismico.
- `allagamento-luoghi-sicuri.svg`: luogo alto contro cantina/strada allagata; testo esplicativo affiancato.
- `temporale-effetti-cascata.svg`: successione di conseguenze **possibili**, non inevitabili.
- `esperimento-viscosita-gas.svg`: modello didattico dei gas in fluidi di viscosità diversa.
- `co2-spazi-confinati.svg`: accumulo possibile di CO₂, con avviso esplicito sui limiti del modello.

Gli asset sono SVG statici locali, senza JavaScript o font esterni, con proporzioni 1200×620. Usare il shortcode `illustrazione-udl` con `src`, `alt` e `caption`. Il testo della pagina rimane sufficiente anche senza immagini.

## Regola di estensione
Per ogni nuova illustrazione: identificare un bisogno didattico, verificare contenuti e sicurezza con fonti ufficiali, inserire una descrizione alternativa non ridondante, verificare leggibilità su smartphone e carta A4, controllare la resa del sito. Non aggiungere una figura se non aumenta la comprensione.

**Nota:** l'adozione dei criteri CAST non equivale a certificazione CAST o verifica completa WCAG. È necessaria una revisione periodica con utenti reali, docenti e persone con disabilità.

Riferimento: https://udlguidelines.cast.org/representation/language-symbols/multiple-media/
