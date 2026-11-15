# Podcast automatico (dal 15/11/2026)

Due puntate a settimana (martedì e venerdì), fatte con NotebookLM nel Chrome del PC
e pubblicate solo dopo la trascrizione e il controllo dei fatti. Nessun passaggio a mano.

Istruzione di Alessandro del 15/11/2026: *«dobbiamo automatizzare la creazione di podcast
per la protezione civile e lo devi fare TU in automatico senza nessun mio intervento»*;
scelte: puntate online da sole solo se superano il controllo, due a settimana.

## Dove gira

Sul PC, senza nessuno davanti: la crontab dell'utente lancia `scripts/podcast-auto/giro-automatico.sh`
ogni ora dalle 8:31 alle 21:31. Il lanciatore parte davvero una volta al giorno e solo se in
calendario ci sono meno di 8 puntate (controllo gratuito su `origin/main`); avvia Claude Code
senza finestra con Chrome (`claude -p --chrome --permission-mode auto`) in una copia di lavoro
separata (`~/podcast-lavoro/copia-sito`), e scrive i log in `~/podcast-lavoro/log/`.
Servono: PC acceso e non in sospensione, Chrome aperto con l'estensione di Claude e l'accesso a
Google in NotebookLM (`notebook.google.com`). Prova del collegamento: `giro-automatico.sh --prova`.

Le puntate già in calendario escono da sole anche a PC spento (rebuild di ogni mattina su
GitHub). Se il magazzino scende sotto una settimana o un'uscita salta, `controllo-podcast.yml`
apre una issue che arriva per email.

## Il giro, passo per passo

Una puntata alla volta (istruzione di Alessandro del 15/11/2026): si chiude fino alla messa
in calendario prima di cominciare la successiva.

1. **Prossima puntata**: prima voce `da-fare` di `coda.yaml`.
   `python3 scripts/podcast-auto/trova-fonti.py <id>` cerca tutte le pagine pubblicate del sito
   sul tema (pagine, articoli, dossier, kit, schede, materiali per le scuole: parola nel titolo),
   aggiunge le fonti ufficiali di `ufficiali` e scrive `~/podcast-lavoro/<id>/fonti.txt`
   (indirizzi per NotebookLM) e `fonte.md` (testo di tutte, per il controllo dei fatti).
   `~/.podcast-venv/bin/python scripts/podcast-auto/prepara-fonte.py <id>` scrive `istruzioni.txt`.
   Se le fonti sono poche, si aggiungono a `ufficiali` pagine istituzionali verificate con una
   richiesta reale (mai indirizzi indovinati); se ce ne sono di fuori tema, si mettono in `escludi`.
2. **NotebookLM** (Chrome, scheda nuova): «Nuovo notebook» → «Aggiungi fonte» → «Siti web»
   → tutti gli indirizzi di `fonti.txt` separati da uno spazio → «Inserisci». Poi «Overview audio» → formato Approfondimento, lingua Italiano, lunghezza
   Predefinita → nel campo «Su cosa dovrebbero concentrarsi…» il testo di `istruzioni.txt`
   → «Genera ora». Attendere (5-20 minuti). Cercare i pulsanti per nome (strumento `find`),
   non per coordinate: la posizione dei riquadri cambia.
   **Scaricare senza «Scarica»**: Chrome chiede dove salvare e quella finestra di sistema non
   si comanda. Si avvia `~/.podcast-venv/bin/python scripts/podcast-auto/ricevitore.py <id>`
   (in background, ascolta su 127.0.0.1:8799), si preme «Riproduci» sull'audio pronto e nella
   pagina si esegue:
   ```js
   performance.setResourceTimingBufferSize(5000);
   document.querySelectorAll('audio,video').forEach(x => x.pause());
   const u = performance.getEntriesByType('resource').map(e => e.name)
     .filter(n => n.includes('googlevideo.com/videoplayback')).pop();
   const b = await (await fetch(u.replace(/&range=[^&]*/, ''))).blob();
   (await fetch('http://127.0.0.1:8799/', {method: 'POST', body: b})).status
   ```
   Se `u` è vuoto (scheda aperta da molto), si ricarica la pagina e si preme di nuovo
   «Riproduci». Il file arriva in `~/podcast-lavoro/<id>/audio.m4a`.
3. **Trascrizione**: `~/.podcast-venv/bin/python scripts/podcast-auto/trascrivi.py ~/podcast-lavoro/<id>/audio.m4a`.
4. **Controllo dei fatti** (agente `pc-materiali-publisher` § «Niente si pubblica senza
   verifica», più `pc-fact-checker`): leggere tutta la trascrizione e confrontarla frase per
   frase con le pagine fonte e con `data/dati_canonici.yaml`. Errore = un'affermazione che le
   fonti non contengono o contraddicono, un numero diverso, un «sempre/mai» non nelle fonti,
   un nome di strumento o di intelligenza artificiale, il Gruppo indicato come chiamabile in
   emergenza. Se c'è anche un solo errore la puntata **non si pubblica**: si rigenera una volta
   (stesse fonti, istruzioni rafforzate sul punto sbagliato); al secondo errore la voce va in
   `stato: scartata` con il motivo e si passa alla successiva al giro dopo.
5. **Trascrizione pulita**: correggere solo gli errori di riconoscimento (non il contenuto),
   dare paragrafi leggibili, in `~/podcast-lavoro/<id>/trascrizione.md`.
6. **Pubblicazione**: `~/.podcast-venv/bin/python scripts/podcast-auto/pubblica-puntata.py <id> AUDIO TRASCRIZIONE --descrizione "…"`
   (≤160 caratteri, dice di che cosa parla, niente «verificato» o «interviste»). Poi
   `python3 scripts/check-dati-canonici.py`, `python3 scripts/check-refusi.py content/podcast/<file>`,
   build Hugo, ramo `claude/podcast-<id>`, PR, squash merge, verifica del deploy e
   ascolto della pagina pubblicata (il player carica l'audio).
7. **Resoconto** ad Alessandro con notifica: puntata uscita (link) o scartata (motivo).

## Regole fisse

- Fonti solo pagine del sito già pubblicate e verificate; mai siti esterni come fonte.
- Nessun riferimento a strumenti o all'intelligenza artificiale nella pagina, nel file audio
  (metadati tolti dalla ricodifica) e nei testi (`firma-dei-lavori.md`).
- Non si dichiara nulla che non è vero per quel file (CLAUDE.md, «Nessuna dichiarazione non misurata»).
- Il notebook di NotebookLM resta nell'account; non si condivide.
