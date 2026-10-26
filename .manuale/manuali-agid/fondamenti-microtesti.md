# Microtesti

> Testo ufficiale di Designers Italia, «Fondamenti del design system .italia: Microtesti» (https://designers.italia.it/design-system/fondamenti/microtesti/), licenza CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/deed.it). Convertito in Markdown senza cambiare il testo dal file src/data/content/design-system/fondamenti/microtesti.yaml del repository https://github.com/italia/designers.italia.it (commit 8aca4c5 del 20/10/2026). Non modificarlo a mano: si aggiorna con `python3 scripts/manuali-agid.py aggiorna`.
<!-- fine intestazione -->

I microtesti rendono l'interazione fluida e coerente con l'ecosistema di un servizio digitale. Scopri come scrivere testi di interfaccia utili, che facilitano il raggiungimento degli obiettivi e che ispirano fiducia.

## Migliora il rapporto tra utenti e interfaccia

I microtesti sono brevi testi strategici presenti nelle interfacce dei servizi digitali che **guidano, informano e rassicurano gli utenti durante l’interazione**: call-to-action, etichette di navigazione, messaggi di errore, messaggi di conferma, testi delle notifiche, testi segnaposto. 

I microtesti migliorano notevolmente l’esperienza utente, l'usabilità dell'interfaccia e, più in generale, l'accessibilità di un servizio digitale. Quando ben progettati, **favoriscono il raggiungimento di un obiettivo**, **aiutano a evitare errori** e, di conseguenza, **contribuiscono ad aumentare la fiducia negli utenti**.

## Scrivi per facilitare e orientare l’interazione

### Tieni presente l'obiettivo dell'utente

I microtesti efficaci sono **focalizzati**, **contestuali** e **guidano l'utente verso l'obiettivo**. Ogni parola dovrebbe aiutare l’utente a compiere un’unica azione in modo semplice, chiaro e sicuro. Aggiungere informazioni non pertinenti rischia di creare confusione, rallentare il flusso e aumentare il carico cognitivo. **Orienta quindi l'utente sempre verso l’azione primaria**, segnalando chiaramente come secondarie o collaterali altre possibilità di interazione.

### Usa azioni specifiche

**Inizia le call-to-action con un verbo** che indichi chiaramente l’azione da svolgere e consenta all'utente di prevedere l'effetto dell'interazione.

| VA BENE | NON VA BENE |
|---|---|
| Invia | OK |
| Aggiungi un nuovo provider | Nuovo provider |

### Usa un linguaggio semplice e conciso

**Vai dritto al punto** ed **evita il più possibile nominalizzazioni, negazioni e forme passive**: rendono il testo difficile da comprendere. Considera anche il limite massimo di caratteri che un componente specifico può contenere. A parità di significato, è sempre preferibile ridurre la quantità di testo piuttosto che incrementarla.

→ [Approfondisci il tema nel fondamento Linguaggio](https://designers.italia.it/design-system/fondamenti/linguaggio)

| VA BENE | NON VA BENE |
|---|---|
| Cerca un documento | Fai una ricerca fra i documenti |
| I campi con asterisco sono obbligatori | Questo campo non è opzionale |
| Hai salvato il documento. Vai alla sezione "..." per visualizzarlo | Il documento è stato salvato con successo nella sezione "..." |

### Usa un tono di voce appropriato al contesto

Una Pubblica Amministrazione che mette le persone al centro sa parlare con una voce empatica. Quando progetti i microtesti, **tieni conto il più possibile degli stati d’animo in cui potrebbe trovarsi l’utente** che interagisce con l’interfaccia e adatta il tono al contesto.

→ [Approfondisci il tema nel fondamento Tono di voce](https://designers.italia.it/design-system/fondamenti/tono-di-voce)

| VA BENE | NON VA BENE |
|---|---|
| (Immagine: Hai ricevuto una multa di 60 euro per divieto di sosta. Hai tempo fino al 12 gennaio 2025 per pagare senza costi aggiuntivi. Puoi pagare online o tramite bollettino postale. Paga online.) Tono di voce autorevole, istruttivo e orientato all'azione | (Immagine: È ora di pagare! Hai ricevuto una multa di 60 euro perchè hai parcheggiato dove non si poteva. Se non paghi entro il 12 gennaio 2025 ti addebiteremo costi aggiuntivi. Paga adesso.) Tono di voce colpevolizzante |

### Includi aiuti contestuali di valore

(Immagine: Esempi di aiuti contestuali)

Gli aiuti contestuali sono microtesti aggiuntivi che **guidano l'utente su come interagire con l’interfaccia**, **compilare campi** e **interpretare alcuni elementi UI**. Rappresentano un'opportunità per rendere l'interazione intuitiva e fluida.

- Usa i testi segnaposto per suggerire agli utenti come interagire con campi liberi senza validazione, come le barre di ricerca (ad esempio: "Cerca servizi e uffici", "Inizia a digitare un indirizzo"). Ricorda che questi suggerimenti scompaiono quando l'utente inizia a digitare.

- Per indicare istruzioni di compilazione, come ad esempio per i [campi input](https://designers.italia.it/design-system/componenti/input/) dei [form](https://designers.italia.it/design-system/componenti/form/), usa invece l'helper text fisso posto sotto il componente, così il suggerimento non scompare. Scrivi istruzioni utili e specifiche, come "Inserisci una password di almeno 8 caratteri e con almeno una maiuscola" e non "Inserisci una password sicura".

- Nei [dropdown](https://designers.italia.it/design-system/componenti/dropdown/) di selezione, specifica cosa bisogna selezionare (ad esempio, "Seleziona una regione", "Seleziona una sede") e non usare il generico "Seleziona un'opzione".

- Usa i [tooltip](https://designers.italia.it/design-system/componenti/tooltip/) solo per indicazioni secondarie o accessorie, poichè saranno visibili solo al clic, tap o al passaggio del mouse. Usali con moderazione e valuta se l’aiuto contestuale è davvero necessario.

### Aiuta nella risoluzione degli errori

(Immagine: Un esempio microcopy per un messaggio di errore)

Un messaggio di errore utile **aiuta a riconoscere il problema e dà indicazioni per correggerlo**, supportando l'utente in un momento di frustrazione.

1. Scrivi un titolo che descrive chiaramente qual è il problema, senza incolpare l'utente.

2. Spiega la causa dell'errore, nella descrizione.

3. Continua la descrizione spiegando in che modo risolvere.

4. Fornisci, se possibile, una call-to-action per una soluzione immediata o una via d'uscita alternativa.

### Chiedi conferma prima di azioni importanti

Prima di azioni con conseguenze rilevanti o irreversibili, **dai all'utente possibilità di assicurarsi che voglia effettivamente procedere**. Le persone possono commettere errori, soprattutto in contesti complessi, sotto pressione o quando sono di fretta.

(Immagine: Un esempio microcopy per una modale di conferma)

Quando chiedi conferma a un'utente:

1. Scrivi un titolo sotto forma di domanda che esplicita chiaramente l'azione che si sta per compiere. Preferisci la forma *Vuoi* + *[Verbo dell'azione]*, evitando generici "Attenzione!" o "Sei sicuro di voler...?" che non danno contesto o nascondono l'informazione principale alla fine della frase.

2. Fornisci una descrizione completa dell’azione e delle sue conseguenze, cercando di non ripetere le parole del titolo. Offri un suggerimento per evitare errori prima di procedere o una spiegazione di come rimediare all'azione successivamente.

3. Usa lo stesso verbo che hai usato nel titolo come call-to-action principale, per evitare ambiguità.

4. Usa "Annulla" come call-to-action secondaria per annullare l'azione.

Nei casi di forte ambiguità tra la call-to-action principale e quella secondaria, puoi cambiare verbi, includere sostantivi e aggiungere Sì/No. Ad esempio:

Per esempio: Vuoi annullare la pratica? No, mantieni pratica / Sì, annulla pratica

### Comunica l'esito positivo di un'azione

I messaggi di conferma comunicano all'utente che un'azione è stata completata con successo, fornendo dettagli rilevanti e rassicurazioni. Sono fondamentali per migliorare l'esperienza utente e aumentare la fiducia nel servizio.

(Immagine: Un esempio microcopy per un messaggio di conferma)

Quando progetti messaggi di conferma:

1. Scrivi un titolo che descrive chiaramente l'azione che è stata appena conclusa.

2. Spiega gli effetti dell'azione e includi eventuali numeri di riferimento (come nel caso di richieste).

3. Includi informazioni su cosa succede dopo ed eventuali tempi di attesa.

4. Se rilevante, aggiungi una call-to-action per far continuare l'utente nell'interazione del servizio. Ad esempio, puoi invitare l'utente a navigare un'altra sezione, approfondire informazioni aggiuntive, ripetere la stessa azione appena conclusa, scaricare una ricevuta.

### Sfrutta gli stati vuoti per incentivare le interazioni

(Immagine: Un esempio di microcopy per uno stato vuoto)

Gli stati vuoti, in inglese *empty states*, sono quei testi che appaiono in sezioni temporaneamente vuote, prima che il sistema o l'utente aggiungano informazioni, oppure quando una ricerca non restituisce risultati. Scrivere un microtesto per uno stato vuoto è un’opportunità per **far comprendere all’utente come iniziare a interagire con l’interfaccia**, perché questa sia davvero di valore per la sua esperienza, senza perdite di tempo.

1. Includi un messaggio principale che spiega lo stato vuoto, evitando parole e tono di voce “negativi”.

2. Suggerisci come **avviare l’interazione che annulla lo stato vuoto** e il tipo di esperienza offrirà la sezione una volta avviata la prima interazione.

3. Se possibile, aggiungi una call-to-action per annullare lo stato vuoto immediatamente.

## Rispetta la consistenza delle tue scelte di scrittura

La progettazione di schemi ricorrenti d’interazione a livello di UX e UI implica anche definire **scelte** e **pattern di contenuto** ricorrenti e consistenti nell’ambito dello stesso servizio. Oltre alle buone pratiche generali quindi, è buona norma definire e applicare in interfaccia, e **in maniera consistente**, la terminologia usata, gli ingombri di testo, i copy delle call to action.

Per facilitare l’aggiornamento consistente dei testi durante tutte le fasi di progettazione di un servizio, sono disponibili strumenti e integrazioni per i principali software di prototipazione che permettono di **creare e gestire librerie di microtesti**.

## Fai ricerca e testa i microtesti del tuo servizio

Prima di scrivere microtesti, è importante **conoscere il linguaggio che gli utenti usano** in relazione a un determinato servizio. Alcune possibili attività di ricerca sono: **conversation mining** (analisi del linguaggio usato in conversazioni su social network e forum), **focus group** e **interviste utente**.
  
Per valutare se i microtesti progettati sono comprensibili agli utenti e corrispondono al loro linguaggio e alle loro aspettative, puoi svolgere principalmente **[test di usabilità](https://designers.italia.it/risorse-per-progettare/validare/test-di-usabilita/)**, ma anche **test di leggibilità** (tramite formula di Flesch-Vacca e l’indice Gulpease), **test di comprensione**, **cloze test** (o cloze deletion test), **test dell'evidenziatore** e **test A/B**.
