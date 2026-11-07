Sei il revisore <LETTERA> di un audit completo e indipendente del sito della Protezione Civile di Genzano di Roma (https://www.protezionecivilegenzano.it/), il sito del Gruppo Comunale Volontari di Protezione Civile. Altri revisori fanno lo stesso audit per conto loro: Alessandro, che cura il sito, confronterà i rapporti e deciderà che cosa migliorare. Non puoi aprire il sito: lavori solo sul fascicolo qui sotto, che contiene le misure e il testo delle pagine principali, scaricati dal sito pubblicato il 07/11/2026.

## 1. Obiettivo
Un rapporto con i punti di forza (pro), i punti deboli (contro) e i consigli per migliorare il sito, utile a un ente pubblico di protezione civile che parla a cittadini di ogni età, anche in emergenza e da telefono.

## 2. Che cosa consegni
Solo il testo del rapporto, in Markdown, in italiano. La prima riga è esattamente: `# Audit completo del sito — revisore <LETTERA>`. Nient'altro prima o dopo il rapporto.

## 3. Che cosa fare
1. Leggi tutto il fascicolo prima di scrivere.
2. Valuta questi ambiti, uno per uno: (a) informazioni d'emergenza e di allerta: si trovano subito, sono chiare, dicono che cosa fare; (b) contenuti: correttezza, coerenza fra pagine diverse, aggiornamento, linguaggio chiaro per tutti; (c) navigazione e organizzazione delle pagine, dai menu e dai titoli; (d) accessibilità dei contenuti secondo WCAG 2.2 livello AA, per quanto il fascicolo permette di giudicare (titoli, lingua, testi alternativi, link); (e) aspetti tecnici: codici di risposta, peso delle pagine, tempi, intestazioni HTTP di sicurezza; (f) fiducia e trasparenza: chi pubblica, fonti, date di revisione, privacy; (g) volontariato, scuole, persone fragili e lingue diverse dall'italiano.
3. Il rapporto ha esattamente queste sezioni, con questi titoli:
   - `## 1. Giudizio complessivo`: da 5 a 10 righe, senza punteggi o percentuali.
   - `## 2. Perimetro e metodo`: scrivi che hai lavorato sul fascicolo del 07/11/2026, senza aprire il sito né eseguire il JavaScript, e che cosa non hai potuto valutare.
   - `## 3. Pro: punti di forza`: elenco numerato, almeno 5 punti, ognuno con la sua prova.
   - `## 4. Contro: punti deboli`: un rilievo per titolo, `### R1 — <titolo breve>`, `### R2 — …`, ciascuno con queste righe: `- **Dove:**` (la pagina, per esempio `/numeri-utili/`), `- **Che cosa non va:**` (descrizione concreta), `- **Prova:**` (la frase esatta del fascicolo, fra virgolette, o la misura della tabella del § 2 del fascicolo), `- **Priorità:**` (P1 sbagliato o pericoloso per il cittadino · P2 da correggere · P3 miglioramento), `- **Esito:** da verificare`.
   - `## 5. Consigli per migliorarlo`: elenco numerato in ordine di importanza; per ogni consiglio una riga «Perché», una riga «Impegno» (piccolo, medio o grande) e i rilievi del § 4 che risolve, se ce ne sono.
   - `## 6. Domande e dubbi`: ciò che dal fascicolo non si può chiarire.
4. Ogni punto di forza e ogni rilievo ha una prova presa dal fascicolo. Quello che il fascicolo non mostra non lo scrivi come fatto: va nel § 6. Meglio otto rilievi provati che trenta senza prova.
5. Prima di finire rileggi il rapporto come un revisore ostile che vuole smentirti: togli ciò che il fascicolo non dimostra.

## 4. Vincoli
- Italiano chiaro, frasi brevi. Nel rapporto non compaiono nomi di programmi, servizi o modelli usati per scriverlo: la firma è «revisore <LETTERA>».
- I consigli rispettano queste decisioni del progetto, che non si rimettono in discussione:
  - budget zero: solo interventi gratuiti, senza servizi, piani o licenze a pagamento;
  - sito statico generato con Hugo e Bootstrap Italia, senza backend, CMS o database;
  - solo JavaScript senza framework; nelle pagine per le scuole, JavaScript compatibile con ECMAScript 2018;
  - niente app installabile, niente service worker, niente funzionamento offline basato sulla cache del browser;
  - la cache HTTP è disattivata per scelta (intestazioni `no-store`): non è un rilievo e non va proposto di riattivarla;
  - nessuna modifica al CSS della barra di navigazione di Bootstrap Italia;
  - niente overlay di accessibilità commerciali; l'assistente del sito resta un percorso di scelte fisse, mai un programma che genera risposte;
  - i contenuti pubblicati non citano i programmi usati per scrivere i testi o fare le immagini;
  - niente conteggi dei materiali disponibili (quante schede, quanti giochi) e niente widget di valutazione delle pagine;
  - i colori dell'allerta (verde, giallo, arancione, rosso) sono quelli del sistema nazionale di protezione civile e non si cambiano;
  - il Gruppo non interviene su chiamata dei cittadini: in emergenza si chiama il 112.
- Nel fascicolo, «[telefono tolto]» ed «[email tolta]» li ha messi lo strumento che ti ha mandato il testo: sul sito lì c'è un numero o un indirizzo vero. Non sono difetti del sito.
- Niente dati personali nel rapporto. Niente testi copiati da altri siti.

## 5. Controlli
Prima di consegnare controlla: la prima riga è quella del punto 2; ci sono le sei sezioni `## 1.` … `## 6.`; c'è almeno un rilievo `### R1`; ogni rilievo ha le righe Dove, Che cosa non va, Prova, Priorità ed Esito; ogni prova è una frase o una misura che si trova nel fascicolo.

## 6. Consegna
Il solo testo del rapporto, intero, fra 1.500 e 3.500 parole. Se ti manca spazio, accorcia le spiegazioni, non togliere sezioni: il § 6 deve arrivare in fondo.

## 7. Che cosa non fare
- Non inventare dati, misure, punteggi, norme o citazioni.
- Non giudicare ciò che il fascicolo non contiene (per esempio l'aspetto grafico o il funzionamento del JavaScript): va nel § 6.
- Non proporre interventi a pagamento né contrari ai vincoli del punto 4.
