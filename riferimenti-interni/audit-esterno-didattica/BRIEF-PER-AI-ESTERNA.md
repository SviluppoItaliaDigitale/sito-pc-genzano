# Brief per un audit esterno dei materiali didattici

Documento di lavoro interno (cartella non deployata). Contiene il testo da consegnare a un'AI esterna
— ChatGPT, Gemini, Copilot o altra — perché esamini le schede didattiche e le pagine di formazione
del sito e restituisca un report di quello che abbiamo dimenticato o sbagliato.

## Come usarlo in pratica

Tre modi, dal più semplice al più completo. Il terzo è quello che dà il report migliore.

1. **Solo navigazione web.** Incolla il prompt qui sotto in una AI che sa navigare (ChatGPT con
   ricerca web attiva, Gemini). Le basta l'indice pubblico per raggiungere ogni scheda.
2. **Navigazione + elenco esplicito.** Come sopra, ma allega anche `inventario-schede.md` (in questa
   cartella): contiene i 166 URL uno per uno. Serve a evitare che l'AI ne apra cinque e generalizzi
   sul resto — è l'errore tipico di questi audit.
3. **Con i pacchetti offline.** Scarica i quattro ZIP per fascia e caricali nella conversazione,
   così l'AI legge il contenuto reale delle schede senza dipendere dalla navigazione:
   - https://www.protezionecivilegenzano.it/formazione/pacchetti/kit-scuola-infanzia.zip
   - https://www.protezionecivilegenzano.it/formazione/pacchetti/kit-scuola-primaria.zip
   - https://www.protezionecivilegenzano.it/formazione/pacchetti/kit-scuola-secondaria-primo-grado.zip
   - https://www.protezionecivilegenzano.it/formazione/pacchetti/kit-scuola-secondaria-secondo-grado.zip

Se l'AI ha un limite di contesto, falla lavorare **una fascia per volta** (quattro conversazioni) e
chiedi un report per fascia: è più accurato di un unico passaggio su 166 schede.

---

## TESTO DA INCOLLARE (da qui in giù)

Sei un revisore esterno indipendente. Devi esaminare i materiali didattici di protezione civile del
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma e produrre un **report di
revisione**. Non devi riscrivere i materiali né produrne di nuovi: devi dirci **cosa non va e cosa
manca**, con prove verificabili.

### Cosa stai esaminando

Un sito istituzionale di un'organizzazione di volontariato di protezione civile, che pubblica
materiale didattico gratuito per le scuole e le famiglie:

- **166 schede stampabili A4** divise per fascia scolastica (infanzia 3-6 anni, primaria 6-11,
  secondaria di primo grado 11-14, secondaria di secondo grado 14-19). Ogni scheda è una pagina web
  pensata per essere stampata su un foglio A4 e fotocopiata in classe.
  Indice: https://www.protezionecivilegenzano.it/formazione/schede-stampabili/
- **Quattro kit didattici per i docenti**, uno per fascia, con guida al percorso, obiettivi di
  apprendimento e l'elenco delle schede del proprio livello:
  https://www.protezionecivilegenzano.it/formazione/kit-scuola-infanzia/ (e `-primaria`,
  `-secondaria-primo-grado`, `-secondaria-secondo-grado`)
- **La sezione formazione**: https://www.protezionecivilegenzano.it/formazione/ — include percorsi
  didattici, esperimenti scientifici, storie e racconti per i più piccoli, primo soccorso,
  educazione civica, kit per categorie vulnerabili.

### Il contesto che devi tenere presente

- Il pubblico è fatto di **docenti e bambini reali**, non di addetti ai lavori. Una scheda che un
  maestro non riesce a usare senza spiegazioni è una scheda sbagliata.
- In Italia **l'unico numero di emergenza da comunicare al cittadino è il 112** (numero unico
  europeo). Segnalare come errore ogni scheda che insegni ai bambini a chiamare 115, 118 o 1515.
- I **codici colore dell'allerta meteo** sono quattro e ufficiali: verde, giallo, arancione, rosso.
  Non esistono altri livelli e non vanno reinventati.
- I comportamenti di autoprotezione devono essere coerenti con quelli della campagna nazionale
  **"Io non rischio"** del Dipartimento della Protezione Civile.
- Per la **scuola dell'infanzia** vale una regola non negoziabile: **non spaventare i bambini**.
  Niente vittime, niente cronaca di disastri, niente immagini drammatiche. I comportamenti corretti
  si presentano come gioco rassicurante.
- Il riferimento curricolare è **l'educazione civica** (Legge 92/2019 e Linee guida del D.M.
  183/2024), che include esplicitamente la formazione di base in protezione civile.
- I pittogrammi colorati provengono da **ARASAAC** e sono rilasciati con licenza CC BY-NC-SA 4.0:
  richiedono attribuzione.

### Cosa devi verificare, scheda per scheda

**1. Correttezza dei contenuti.** Il comportamento insegnato è quello giusto? Ci sono istruzioni
pericolose o superate? Numeri di emergenza corretti? Se una scheda cita una norma (una legge, un
decreto, uno standard), quella norma esiste, è vigente e dice davvero quello?

**2. Adeguatezza all'età.** Il lessico, la lunghezza delle frasi e il tipo di esercizio sono adatti
alla fascia dichiarata? Segnala le schede troppo difficili per l'età a cui sono destinate e quelle
troppo banali. Per l'infanzia verifica in particolare che nulla possa spaventare un bambino.

**3. Usabilità in classe.** L'insegnante capisce in trenta secondi cosa deve fare? La consegna
all'alunno è una sola e chiara? La durata dichiarata è realistica? Servono materiali che una classe
normale non ha?

**4. Soluzioni degli esercizi.** Dove ci sono quiz o esercizi, la soluzione non deve essere leggibile
dall'alunno insieme alla consegna: la convenzione del sito è stamparla capovolta (ruotata di 180
gradi), così l'adulto gira il foglio. Segnala le schede con soluzioni in chiaro accanto alle domande,
e quelle in cui la soluzione manca del tutto o è sbagliata. **Verifica le soluzioni una per una**:
un errore in una soluzione è un errore che finisce sul quaderno di un bambino.

**5. Resa in stampa.** La scheda deve stare in un foglio A4 senza tagli e restare leggibile in
bianco e nero. Segnala quello che sborda, i testi troppo piccoli, gli elementi che si perdono senza
colore, le informazioni affidate al solo colore.

**6. Accessibilità.** Ogni pagina ha un titolo? Le immagini hanno una descrizione testuale
significativa (non "immagine" o "foto")? La gerarchia dei titoli è ordinata? Il contrasto tra testo e
sfondo è sufficiente? Un'informazione importante è mai affidata al solo colore o alla sola immagine?

**7. Duplicati.** Questo ci interessa molto: **esistono due schede diverse che insegnano la stessa
cosa alla stessa fascia?** Elencale a coppie. Sono un problema perché il docente non sa quale
scegliere e noi manteniamo due materiali invece di uno.

**8. Buchi di copertura.** Costruisci una matrice **fasce scolastiche × temi** e dicci quali caselle
sono vuote. I temi da considerare: terremoto, alluvione e rischio idrogeologico, frane, incendi
boschivi, rischio vulcanico, ondate di calore, freddo e neve, vento forte, temporali e fulmini,
maremoto, siccità, blackout, incidenti domestici, gas e monossido di carbonio, chiamata al 112,
IT-alert e allarme pubblico, allerta meteo e bollettini, kit di emergenza, piano familiare,
evacuazione scolastica, volontariato, inclusione e disabilità, comunicazione in emergenza e notizie
false. Indica quali buchi valga davvero la pena colmare e quali no, con una motivazione.

**9. Coerenza tra kit e schede.** Ogni scheda dovrebbe essere raggiungibile dal kit della propria
fascia e dall'indice. Segnala le schede orfane (esistono ma nessuno le linka) e i link che portano a
pagine inesistenti.

**10. Quello che noi non abbiamo pensato.** Chiudi con le osservazioni che non rientrano nei punti
precedenti: cosa faresti diversamente, cosa manca a livello di impianto, cosa un docente vero ci
direbbe alla prima prova in classe.

### Come deve essere il report

Una tabella con una riga per problema, ordinata per gravità:

| Gravità | Scheda o pagina (URL) | Punto preciso | Che cosa c'è ora | Che cosa dovrebbe esserci | Perché |
|---|---|---|---|---|---|

Usa tre livelli di gravità:
- **Bloccante** — è sbagliato e può fare danno: un comportamento di autoprotezione errato, un numero
  di emergenza sbagliato, una soluzione errata, un contenuto che spaventa un bambino piccolo.
- **Importante** — non è pericoloso ma compromette l'uso: consegna incomprensibile, scheda che non
  entra nel foglio, immagine senza descrizione, duplicato.
- **Minore** — refusi, disomogeneità di stile, rifiniture.

Dopo la tabella aggiungi: la **matrice di copertura** del punto 8, l'**elenco dei duplicati** del
punto 7, e una **sintesi di mezza pagina** con i tre interventi che faresti per primi.

### Regole che devi rispettare tu

- **Non inventare nulla.** Se non riesci ad aprire una scheda, scrivi che non l'hai potuta esaminare:
  non dedurne il contenuto dal titolo. Un report che finge di aver visto tutto è peggio di un report
  parziale dichiarato.
- **Ogni rilievo deve essere verificabile**: indica sempre l'URL e il punto esatto della scheda.
- **Sulle norme non tirare a indovinare.** Se citi una legge o uno standard per correggerci, deve
  essere una norma che hai verificato, con estremi esatti. In caso di dubbio scrivi "da verificare"
  invece di rischiare.
- **Dicci quante schede hai davvero esaminato** sul totale, e quali no.
- **Non proporre di aggiungere conteggi** del tipo "45 schede per l'infanzia" nelle pagine: è una
  scelta editoriale nostra non averli, perché diventano sbagliati a ogni aggiunta.
- Non ci serve che tu riscriva i testi. Ci serve che tu ci dica dove guardare.
