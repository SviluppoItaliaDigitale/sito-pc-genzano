# Contenuti

> Testo ufficiale di Designers Italia, «Fondamenti del design system .italia: Contenuti» (https://designers.italia.it/design-system/fondamenti/contenuti/), licenza CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/deed.it). Convertito in Markdown senza cambiare il testo dal file src/data/content/design-system/fondamenti/contenuti.yaml del repository https://github.com/italia/designers.italia.it (commit 373215d del 05/10/2026). Non modificarlo a mano: si aggiorna con `python3 scripts/manuali-agid.py aggiorna`.
<!-- fine intestazione -->

I contenuti sono un elemento cruciale dell’esperienza utente di un sito o servizio digitale. Scopri come strutturare e presentare i contenuti in modo efficace, accessibile e sulla base delle esigenze informative delle persone.

## Progetta contenuti adatti alla consultazione su schermo

I contenuti influenzano direttamente l’esperienza d’uso, l’accessibilità e la percezione di un servizio digitale.  

Su schermo, **consultiamo solo il 20-28% di una pagina** e la **scansioniamo velocemente seguendo la forma di una F** ([F-pattern](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/it/versione-corrente/doc/progettazione-dei-contenuti/scrittura-e-linguaggio.html#come-leggono-le-persone-sul-web)), spesso da uno smartphone in mobilità o usando tecnologie assistive. È quindi importante che i contenuti siano strutturati secondo specifiche caratteristiche, evitando la cattiva pratica di riportare in interfaccia contenuti concepiti per supporti analogici.

## Definisci un obiettivo per ogni contenuto

Prima di progettare qualsiasi contenuto, chiediti di che cosa hanno bisogno gli utenti, imposta un obiettivo e **disponi i contenuti in base alle loro esigenze informative**. Quando spieghi qualcosa, cerca sempre di rispondere alle domande chiave: chi, cosa, dove, come e quando. 

**Parti dalle informazioni principali** e, solo successivamente, aggiungi eventuali informazioni secondare o accessorie, seguendo l'[approccio della piramide inversa](https://www.nngroup.com/articles/inverted-pyramid/)). Puoi mettere in risalto informazioni principali con componenti come [callout](https://designers.italia.it/design-system/componenti/callout) e [dimmer](https://designers.italia.it/design-system/componenti/dimmer).

## Organizza le informazioni su pagina

Aiuta le persone a trovare ciò che cercano sul tuo sito o servizio impostando una **struttura intuitiva e accessibile**.

### Titoli

I titoli devono essere chiari e descrittivi dei contenuti della pagina, in massimo 70 caratteri (inclusi spazi). È possibile scrivere un testo più lungo solo se essenziale per rendere il titolo chiaro, ma deve essere un’eccezione in quanto:
- Google taglia i testi che superano i 70 caratteri;  
- titoli troppo lunghi sono difficili da capire.

### Sommari

Il sommario è un testo breve che riassume in modo chiaro il contenuto della pagina ed è ciò che gli utenti vedono nei risultati di ricerca.  

Il sommario dovrebbe: 
- essere presente in tutte le pagine; 
- non superare i 160 caratteri;
- finire con il punto, per aiutare le persone che usano tecnologie assistive;
- non ripetere il contenuto del titolo e non contenere parole introduttive ridondanti.

### Corpo di pagina

- Dividi il contenuto in [sezioni](https://designers.italia.it/design-system/componenti/sections) e il testo in paragrafi, con titoletti descrittivi. I paragrafi non dovrebbero avere più di 5 frasi ognuno.  
- Non ripetere il sommario nel primo paragrafo.  
- Usa un [linguaggio semplice e naturale](https://designers.italia.it/design-system/fondamenti/linguaggio) e mantieni i testi brevi, rimandando ad altri contenuti di approfondimento tramite link. 
- Usa sempre degli esempi concreti per spiegare meglio le informazioni. Un esempio è un ottimo modo per spiegare un concetto e rendere il testo più chiaro, senza dilungarsi in lunghe spiegazioni.

Non ci sono indicazioni specifiche sulla lunghezza del corpo di pagina, ma ricorda che:  
- le persone leggono solo tra il 20 e il 28% del testo su una pagina; 
- il carico cognitivo aumenta ogni 100 parole che aggiungi su una pagina. 

### Intestazioni

Usa le intestazioni per dividere il contenuto e dargli una struttura di navigazione, usando i relativi tag semantici nel codice HTML. Ogni titolo di pagina è un H1, quindi parti con gli H2 per i contenuti di pagina.   

Usa i livelli di intestazione (da H2 a H4) in maniera ordinata e non usare il grassetto come sostitutivo. Gli utenti di tecnologie assistive spesso navigano le pagine tramite liste di intestazioni.

### Indice di pagina

Per pagine lunghe, includi un [indice di pagina navigabile](https://designers.italia.it/design-system/componenti/navscroll/). L'indice di pagina mostra le intestazioni H2 della pagina, riportando gli stessi titoli usati sul corpo di pagina.

Assicurati che l’indice sia ben fruibile anche su dispositivi mobili, utilizzando menu a tendina accessibili e icone chiare.

### Elenchi puntati e numerati

Usa elenchi puntati per rendere più leggibile il testo. Verifica che i punti dell’elenco siano:
- coerenti, se sono parte integrante della frase che introduce la lista: in questo caso, inoltre l’iniziale del punto elenco è minuscola e la frase si chiude col punto e virgola (se è l’ultimo punto dell’elenco con il punto fermo);  
- sintetici e chiari;  
- correttamente allineati.  

Usa un elenco numerato quando devi guidare le persone in un processo. In questo caso non serve avere una frase introduttiva.  

1. Assicurati di mettere il punto fermo alla fine di ogni frase.  
2. Scrivi frasi brevi, semplici e chiare per far capire l’azione da compiere.  
3. Segnala con dei link i documenti eventualmente necessari per completare l’azione.  
4. Evita sottoelenchi puntati. Se necessario, crea piuttosto un nuovo elenco puntato.

### Link

L’utilizzo dei link è molto utile per rendere i contenuti brevi e rimandare ad altri contenuti per ulteriori approfondimenti:
- assicurati che sia chiara la destinazione di ogni link o lo scopo del collegamento;
- inserisci solo collegamenti a contenuti che abbiano un’effettiva pertinenza e utilità con il contenuto;
- apri il link nella stessa scheda del browser se la pagina di destinazione è interna allo stesso sito o servizio, in una nuova scheda se il link rimanda a un altro sito o servizio.

### Tabelle

Le [tabelle](https://designers.italia.it/design-system/componenti/table) possono essere utili per spiegare facilmente dei concetti. Ricorda però: 
- di non inserire troppo testo all’interno della tabella: otterresti il risultato opposto; 
- di usare tabelle con poche colonne, per non rendere difficile la lettura con dispositivi mobili.

Per presentare i contenuti suddivisi in temi logici, senza bisogno di comparazione tra elementi, potrebbe essere più appropriato usare le [tab](https://designers.italia.it/design-system/componenti/tabs).

### Dati e grafici

Per rendere comprensibili i dati da parte degli utenti, cerca di presentarli in forma visiva, sotto forma di grafici o mappe (data visualization).

A seconda del tipo di dati che devi rappresentare, puoi usare strumenti come:
- [Metabase](https://www.metabase.com/), per dashboard dinamiche;
- [Rawgraphs](https://app.rawgraphs.io/), per grafici;
- [QGIS](https://qgis.org/), per mappe interattive.

### Immagini e video

Usa contenuti multimediali solo se aiutano a comprendere meglio le informazioni che vuoi veicolare. Assicurati che siano di qualità (alta risoluzione) e di [presentarli in modo accessibile](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/it/versione-corrente/doc/progettazione-dei-contenuti/immagini-e-video.html): in particolare, ricorda di includere **alt-text** per le immagini, **sottotitoli** e **trascrizioni** per i video.

### Didascalie
Accompagna sempre le immagini, i grafici o i dati con delle didascalie sintetiche (non più di due righe). Ricorda, quando necessario, di [citare l’autore e riportare la licenza di pubblicazione](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/it/versione-corrente/doc/progettazione-dei-contenuti/proprieta-intellettuale-e-privacy.html).

## Imposta una struttura uniforme per i contenuti della stessa tipologia

Le pagine della stessa tipologia di contenuto (in inglese, *content type*) - ad esempio, le pagine degli uffici, i servizi, le notizie, i bandi, ecc. - dovrebbero presentare la stessa organizzazione dei contenuti su pagina, in un ordine fisso. Così, lo stesso utente, quando navigherà altri contenuti dello stesso o di altri servizi, saprà già dove trovare in pagina le informazioni che cerca.

I [modelli di Designers Italia](https://designers.italia.it/modelli) presentano content type pronti all'uso per varie tipologie di ente.

→ [Approfondisci l'argomento Content type](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/it/versione-corrente/doc/progettazione-dei-contenuti/architettura-dell-informazione.html#tipologie-di-contenuto-content-type)

## Usa un linguaggio semplice e un tono di voce appropriato

Una Pubblica Amministrazione che mette le persone al centro sa parlare con una voce semplice, chiara ed empatica. Scrivi i contenuti con l’obiettivo primario di farti capire ed essere efficace, tenendo conto il più possibile degli stati d’animo in cui potrebbe trovarsi l’utente che interagisce con l’interfaccia.

→ [Vai al fondamento Linguaggio](https://designers.italia.it/design-system/fondamenti/linguaggio/)

→ [Vai al fondamento Tono di voce](https://designers.italia.it/design-system/fondamenti/tono-di-voce/)

## Testa e ottimizza i contenuti

I contenuti dovrebbero sempre essere progettati e ottimizzati in maniera iterativa e continua. Per valutare se i contenuti corrispondono alle attese e alle esigenze informative delle persone che utilizzano il servizio, puoi svolgere [test di usabilità](https://designers.italia.it/risorse-per-progettare/validare/test-di-usabilita/) moderati, preparando attività da svolgere con domande aperte.
