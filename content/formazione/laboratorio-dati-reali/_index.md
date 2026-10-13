---
title: "Piccolo laboratorio di dati reali"
description: "Un'estate di temperature e piogge a Genzano di Roma, in un file da aprire in classe: ipotesi da mettere alla prova, un metodo in cinque passi e la differenza fra osservazione, correlazione e conclusione."
date: 2026-10-13
draft: false
type: "page"
layout: "single"
toc: true
dataUltimaRevisione: "2026-10-13"
tts: true
---

Questo laboratorio dà alla classe un **insieme di dati veri**: le temperature massime e minime e la pioggia di ogni giorno dal **1° giugno al 30 settembre 2026** per la zona di Genzano di Roma, 122 righe in tutto. Con questi dati gli studenti formulano ipotesi, le verificano e imparano a dire che cosa un numero dimostra e che cosa no. Vengono dalla stessa fonte del [Laboratorio meteo](/laboratorio-meteo/) del sito, fermati in un file per poterci lavorare con calma.

## I dati

<div class="table-responsive">
<table>
<caption>File del laboratorio, scaricabili e riusabili con licenza CC BY 4.0</caption>
<thead>
<tr><th scope="col">File</th><th scope="col">Contenuto</th><th scope="col">Scarica</th></tr>
</thead>
<tbody>
<tr><td><strong>Dati giornalieri</strong></td><td>Una riga per giorno: data, temperatura massima (°C), temperatura minima (°C), pioggia (mm). 122 righe.</td><td><a href="/open-data/laboratorio-genzano-estate-2026.csv">CSV</a> · <a href="/open-data/laboratorio-genzano-estate-2026.json">JSON con i metadati</a></td></tr>
<tr><td><strong>Pioggia per settimana</strong></td><td>La pioggia sommata a blocchi di sette giorni a partire dal 1° giugno (l'ultimo blocco ha tre giorni). Serve per il grafico qui sotto.</td><td><a href="/open-data/laboratorio-genzano-estate-2026-settimane.csv">CSV</a></td></tr>
</tbody>
</table>
</div>

**Da dove vengono.** Dalla rianalisi climatica **ERA5** del programma europeo Copernicus (Copernicus Climate Change Service, gestito dal Centro europeo per le previsioni meteorologiche a medio termine, ECMWF), scaricata con il servizio Open-Meteo (licenza CC BY 4.0), lo stesso usato dal Laboratorio meteo. Il punto richiesto è il centro di Genzano (41,706° N, 12,690° E, quota 444 m secondo il modello di quota di Open-Meteo); i valori restituiti sono quelli della **cella di griglia** della rianalisi che lo contiene, con centro a 41,72° N, 12,76° E, e descrivono un'area di diversi chilometri di lato. Il file è un'**istantanea** estratta il 13 ottobre 2026: non si aggiorna da solo.

<div class="alert alert-info" role="note">
<p class="mb-0"><i class="bi bi-info-circle me-2" aria-hidden="true"></i><strong>La prima cosa da discutere in classe:</strong> questi numeri non sono il termometro di una via di Genzano. Sono il risultato di un modello che combina osservazioni e calcolo su una griglia. Un termometro in cortile può segnare un grado in più o in meno, e in un temporale estivo può piovere forte in un quartiere e niente in quello accanto. Sapere <em>che cosa misura</em> un dato è il primo passo per usarlo bene.</p>
</div>

### La pioggia settimana per settimana

{{< grafico-csv file="static/open-data/laboratorio-genzano-estate-2026-settimane.csv" tipo="barre" titolo="Pioggia a blocchi di sette giorni, estate 2026, cella ERA5 di Genzano di Roma" unita="mm" >}}

### I mesi in sintesi

Questa tabella è calcolata dal file giornaliero: ogni numero si può rifare a mano o con un foglio di calcolo, ed è il primo esercizio consigliato.

<div class="table-responsive" tabindex="0" role="region" aria-labelledby="cap-sintesi-mensile">
<table>
<caption id="cap-sintesi-mensile">Sintesi mensile, estate 2026, cella ERA5 di Genzano di Roma (medie arrotondate al decimo; la tabella scorre in orizzontale sugli schermi stretti)</caption>
<thead>
<tr><th scope="col">Mese</th><th scope="col">Massima media (°C)</th><th scope="col">Massima più alta</th><th scope="col">Minima media (°C)</th><th scope="col">Giorni con massima ≥ 30 °C</th><th scope="col">Giorni ≥ 35 °C</th><th scope="col">Pioggia totale (mm)</th><th scope="col">Giorni con almeno 1 mm</th><th scope="col">Pioggia massima in un giorno</th></tr>
</thead>
<tbody>
<tr><td>giugno</td><td>28,0</td><td>34,0 (28 giugno)</td><td>18,2</td><td>13</td><td>0</td><td>26,6</td><td>7</td><td>8,5 mm (3 giugno)</td></tr>
<tr><td>luglio</td><td>31,5</td><td>35,8 (31 luglio)</td><td>20,6</td><td>24</td><td>2</td><td>15,8</td><td>7</td><td>4,1 mm (2 luglio)</td></tr>
<tr><td>agosto</td><td>32,3</td><td>36,4 (28 agosto)</td><td>21,6</td><td>25</td><td>3</td><td>36,9</td><td>9</td><td>11,7 mm (21 agosto)</td></tr>
<tr><td>settembre</td><td>27,5</td><td>33,9 (1° settembre)</td><td>17,2</td><td>8</td><td>0</td><td>49,8</td><td>9</td><td>13,7 mm (10 settembre)</td></tr>
</tbody>
</table>
</div>

In tutta l'estate: **129,1 mm** di pioggia, **32 giorni** con almeno 1 mm, **70 giorni** con massima di almeno 30 °C e **5 giorni** oltre i 35 °C; la serie più lunga senza pioggia (meno di 1 mm al giorno) è durata **15 giorni**, dal 4 giugno.

Un dettaglio da discutere quando rifate i conti: la minima media di giugno è esattamente **18,15 °C**. Arrotondata al decimo fa 18,2, ma alcuni programmi la mostrano come 18,1, perché nei calcolatori i numeri con la virgola sono approssimati. Non è un errore di nessuno: è un buon motivo per scrivere sempre quante cifre si tengono.

## Il metodo in cinque passi

{{< passi titolo="Dalla domanda alla conclusione" >}}
1. **La domanda.** Una sola, chiara, a cui i dati possono rispondere: «luglio è stato più caldo di agosto?» va bene; «l'estate è stata brutta?» no, perché «brutta» non si misura.
2. **L'ipotesi.** Che cosa mi aspetto di trovare, scritto prima di guardare i numeri. Serve proprio a scoprire se avevo torto.
3. **Che cosa misuro e come.** Quale colonna, quale calcolo (media, totale, conteggio, massimo), su quale periodo. Si decide prima, non dopo aver visto il risultato.
4. **Il risultato.** Il numero, con l'unità di misura e il periodo: «agosto: massima media 32,3 °C; luglio: 31,5 °C».
5. **Che cosa posso dire.** È un'osservazione, una correlazione o una conclusione? È il passo più importante e il più difficile: vedi il riquadro.
{{< /passi >}}

### Osservazione, correlazione, conclusione

- **Osservazione:** descrive i dati, senza spiegarli. «Nei quattro mesi ci sono stati 32 giorni con almeno 1 mm di pioggia.» Un'osservazione è vera o falsa: si controlla rifacendo il conto.
- **Correlazione:** due cose variano insieme. «I giorni con pioggia hanno avuto massime più basse dei giorni senza pioggia (28,6 °C contro 30,3 °C).» È vero nei dati, ma non dice ancora *perché*. Prima di spiegarlo bisogna controllare le altre variabili: il mese, per esempio, cambia la temperatura da solo (fra agosto e settembre ci sono quasi cinque gradi di massima media). Il controllo si fa confrontando giorni con e senza pioggia **dentro lo stesso mese**.
- **Conclusione:** una spiegazione che regge perché ha escluso le altre. Per sostenere che «la pioggia abbassa la temperatura» bisognerebbe anche sapere dalla fisica che cosa succede davvero (nuvole e pioggia riducono il sole al suolo, l'aria che porta la pioggia è spesso più fresca) e misurare quelle cose, che in questo file non ci sono. Con questi dati si può al massimo dire: «è compatibile con», «suggerisce», «andrebbe verificato con…». Dire «dimostra» è quasi sempre troppo.

**L'esempio da fare insieme.** Rifate il confronto mese per mese: a giugno i giorni con pioggia hanno la stessa massima media degli altri (28,1 °C contro 28,0 °C); a luglio sono più freschi di 3,0 °C, ad agosto di 2,3 °C, a settembre di 1,4 °C. La differenza quindi **non sparisce** quando si tiene fermo il mese: resta, tranne che a giugno. Poi provate con i sei giorni in cui sono caduti almeno 5 mm: la massima del giorno dopo, confrontata con quella dei giorni vicini dello stesso periodo, è più bassa in tutti e sei i casi, ma di quantità molto diverse: da 0,2 a 2,8 °C. Con sette-nove giorni di pioggia al mese, però, queste medie ballano molto: un giorno in più o in meno le sposta. Che cosa si può dire alla fine? Che i dati sono *compatibili* con «quando piove fa più fresco», che il mese da solo non basta a spiegarlo, e che per capire il perché servirebbero misure che qui mancano (nuvolosità, vento, origine dell'aria). La discussione su che cosa manca vale più del numero.

## Sei ipotesi da mettere alla prova

Ogni gruppo ne sceglie una, segue i cinque passi e presenta il risultato alla classe in tre minuti: domanda, numero, che cosa si può dire.

<div class="table-responsive">
<table>
<caption>Ipotesi di partenza, con il calcolo suggerito e la trappola da evitare</caption>
<thead>
<tr><th scope="col">Ipotesi</th><th scope="col">Che cosa calcolare</th><th scope="col">Attenzione a</th></tr>
</thead>
<tbody>
<tr><td>«Luglio è il mese più caldo dell'estate.»</td><td>Massima media e numero di giorni con massima ≥ 30 °C per ogni mese.</td><td>Nei dati di quest'anno agosto supera luglio: un'estate sola non dice qual è «il» mese più caldo in generale. Per quello serve il <a href="/laboratorio-meteo/">Laboratorio meteo</a>, che ha molti anni.</td></tr>
<tr><td>«D'estate a Genzano non piove mai.»</td><td>Totale di pioggia, giorni con almeno 1 mm, serie più lunga senza pioggia.</td><td>«Mai» e «sempre» sono quasi sempre falsi: 32 giorni su 122 hanno avuto pioggia. La domanda migliore è «quanto e quando».</td></tr>
<tr><td>«Quando piove fa più fresco.»</td><td>Massima media dei giorni con e senza pioggia; poi lo stesso confronto mese per mese.</td><td>La correlazione c'è e resta anche a parità di mese (tranne a giugno), ma il file non contiene le misure che spiegherebbero il perché: è l'esercizio sulla differenza fra correlazione e conclusione.</td></tr>
<tr><td>«Ci sono stati molti giorni da allerta caldo.»</td><td>Giorni con massima ≥ 35 °C e serie di giorni consecutivi sopra i 30 °C.</td><td>I bollettini sul caldo usano criteri diversi dalla sola massima (temperatura percepita, durata, notti calde). Il conteggio è un indizio, non il bollettino: vedi <a href="/rischi-prevenzione/ondate-di-calore/">Ondate di calore</a>.</td></tr>
<tr><td>«Il 10 settembre è stato un giorno di pioggia eccezionale.»</td><td>Confronto dei 13,7 mm con la pioggia totale del mese e con gli altri giorni più piovosi.</td><td>13,7 mm in un giorno è il massimo di quest'estate, ma non è un valore estremo in assoluto: in un temporale intenso possono cadere decine di millimetri in un'ora. «Eccezionale» rispetto a che cosa? Cercate nelle <a href="/comunicazioni/">comunicazioni</a> del sito che cosa è successo quel giorno.</td></tr>
<tr><td>«Il dato del modello è uguale a quello del termometro.»</td><td>Confronto di una settimana di massime del file con le misure di un termometro a scuola o di una stazione meteo amatoriale della zona.</td><td>Lo scarto che trovate non è un errore di nessuno: è la differenza fra una cella di modello e un punto. Da registrare come osservazione.</td></tr>
</tbody>
</table>
</div>

## La scheda di lavoro

Si compila una per gruppo (anche su carta, copiando la tabella).

<div class="table-responsive">
<table>
<caption>Scheda di lavoro del laboratorio: un passo per riga</caption>
<thead>
<tr><th scope="col">Passo</th><th scope="col">La nostra risposta</th></tr>
</thead>
<tbody>
<tr><td>1. La domanda (una sola, misurabile)</td><td></td></tr>
<tr><td>2. L'ipotesi, scritta prima di guardare i dati</td><td></td></tr>
<tr><td>3. Colonna, calcolo e periodo</td><td></td></tr>
<tr><td>4. Il risultato, con unità e periodo</td><td></td></tr>
<tr><td>5. È un'osservazione, una correlazione o una conclusione? Perché?</td><td></td></tr>
<tr><td>6. Che cosa ci servirebbe per esserne più sicuri</td><td></td></tr>
<tr><td>7. Che cosa cambia per la protezione civile (una riga)</td><td></td></tr>
</tbody>
</table>
</div>

Il passo 7 chiude il cerchio: quanti giorni molto caldi ci sono stati dice quanto conta sapere [che cosa fare con il caldo](/rischi-prevenzione/ondate-di-calore/); quanta pioggia cade in un giorno dice perché [una strada allagata non si attraversa](/rischi-prevenzione/rischio-idrogeologico/).

## Come aprire i dati

- **Foglio di calcolo** (anche gratuito): si apre il CSV, si ordina per colonna, si usano le funzioni media, somma, conta.se, max.
- **Carta e penna**, per la primaria: si scelgono dieci giorni, si disegnano le massime come colonne colorate e la pioggia come gocce; le domande restano le stesse.
- **Il Laboratorio meteo** del sito, per la secondaria: la stessa fonte, ma su molti anni; gli esempi pronti coprono le stagioni passate, e per l'estate 2026 si usano i dati di questo file.

## Per il docente

- **Età:** dalla classe 4ª della primaria (osservazioni e conteggi) alla secondaria di secondo grado (correlazioni, confronti fra mesi, medie mobili).
- **Discipline:** matematica, scienze, geografia, educazione civica; tecnologia per il foglio di calcolo.
- **Che cosa si valuta:** la correttezza del calcolo e, soprattutto, la frase del passo 5: chi distingue un'osservazione da una conclusione ha capito il laboratorio, anche se il suo numero era sbagliato.
- **Bisogni educativi speciali:** le tabelle si possono ridurre a dieci giorni scelti insieme; per chi fatica con le cifre vale il lavoro su carta con colonne colorate e gocce; il foglio di calcolo, con i filtri e le funzioni già pronte, è uno strumento compensativo e non un ostacolo. La scheda di lavoro si compila anche a voce, con il docente che scrive.
- **Fonti:** Copernicus Climate Change Service, rianalisi ERA5; [Open-Meteo, Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api); le pagine del sito citate sopra per i comportamenti di protezione civile.
- **Collegamenti:** [Esperimenti e attività](/formazione/esperimenti/) (il pluviometro e la spugna che si satura), [Dalla carta al territorio](/formazione/dalla-carta-al-territorio/) (dove va l'acqua nel quartiere), [Biblioteca delle idee sbagliate](/rischi-prevenzione/idee-sbagliate/) (per allenare lo stesso sguardo sui luoghi comuni).
