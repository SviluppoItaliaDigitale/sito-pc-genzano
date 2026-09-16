# Generatori delle schede didattiche a più fogli

Nove schede stampabili di `static/formazione/schede-stampabili/` non si
scrivono a mano: hanno decine di fogli quasi identici, e un refuso corretto su
un foglio solo resterebbe sugli altri venticinque. Qui vivono i generatori e i
dati da cui nascono.

| Genera | Scheda prodotta | Fogli |
|---|---|---|
| `genera-alfabetiere-quaderno.py` | `alfabetiere-az-infanzia/` | 26 (una lettera per foglio) |
| `genera-alfabetiere-tabella.py` | `alfabetiere-pc-infanzia/` | 1 (le 26 lettere in tabella) |
| `genera-album-disegni.py` | `disegni-mezzi-infanzia/`, `disegni-persone-infanzia/`, `disegni-momenti-infanzia/` | 12 ciascuno |
| `genera-memory.py` | `memory-protezione-civile-infanzia/` | 3 (tessere, retro, regole) |
| `genera-gioco-oca.py` | `gioco-oca-protezione-civile/` | 4 (tabellone, imprevisti, emergenze, regole e pedine) |
| `genera-libro-popup.py` | `libro-popup-protezione-civile/` | 16 (copertina, guida, tredici tavole con la scelta di stampa, diploma) |
| `genera-storia-popup.py` | `flavia-libro-popup/` | 14 fogli A4 **orizzontali** (copertina e retro, guida, dodici capitoli con la storia) |

I testi stanno nei due moduli di dati, non nei generatori:

- `alfabeto_dati.py` — le 26 lettere: parola, disegno, didascalia, e i flag
  `ospite` (lettera fuori dall'alfabeto italiano di 21 lettere: J, K, W, X, Y)
  e `muta` (la H, che nell'alfabeto italiano c'è ma non ha un suono proprio).
- `disegni_dati.py` — i tre album, con titolo, disegno, testo alternativo e
  didascalia di ogni foglio.
- `libro_popup_dati.py` — le tredici tavole del quaderno pop-up: titolo, testo,
  regole «che cosa si fa» (le stesse delle pagine sui rischi del sito) e
  pittogramma di ciascuna emergenza.
- `storia_popup_dati.py` — il libro con la storia: i dodici capitoli di «Flavia,
  Flavio e lo zaino rosso», con il testo da leggere ad alta voce e i rimandi
  alle regole di `libro_popup_dati.py` (una regola sta scritta in un posto solo).
  I disegni delle scene sono tracciati dal generatore, non sono pittogrammi.
- `oca_dati.py` — il gioco dell'oca: le 56 caselle del percorso, le 12 carte
  imprevisto (fatto, effetto, disegno e descrizione del disegno), le 12 carte
  emergenza (domanda, risposta e pagina del sito da cui viene) e le 6 pedine.
  Il percorso a spirale e la posizione delle caselle li calcola il generatore,
  che verifica anche che le caselle disegnate siano tante quante i testi.

## Come si rigenera

```bash
cd scripts/schede-didattiche
python3 genera-alfabetiere-quaderno.py
python3 genera-alfabetiere-tabella.py
python3 genera-album-disegni.py
python3 genera-memory.py
python3 genera-gioco-oca.py
python3 genera-libro-popup.py
python3 genera-storia-popup.py
cd ../..
python3 scripts/genera-pacchetti-schede.py   # rifà "Stampa tutto"
python3 scripts/genera-pacchetti-kit.py      # rifà gli ZIP offline
python3 scripts/check-parita-schede.py       # deve chiudere in verde
```

I due passaggi finali non sono facoltativi: senza di loro la scheda cambia
sulla pagina singola ma resta vecchia in «Stampa tutto» e nello ZIP, ed è
esattamente il disallineamento che `check-parita-schede.py` esiste per vietare.

## Le illustrazioni

Sono pittogrammi **ARASAAC** nella variante in bianco e nero, quella pensata
per essere colorata: autore Sergio Palao, origine ARASAAC, proprietà del
Governo di Aragona, licenza **CC BY-NC-SA 4.0**. Stanno in
`static/pittogrammi/arasaac-bn/`, con `registro.json` che per ogni file dice da
quale pittogramma ARASAAC viene, e si riscaricano con
`bash scripts/scarica-pittogrammi.sh`.

Ogni foglio che contiene pittogrammi porta l'attribuzione stampata, non solo
il primo: queste schede si stampano anche una pagina alla volta, e il foglio
che finisce in classe deve portarla con sé. Se aggiungi disegni a un foglio che
prima non ne aveva — è successo con le carte imprevisto del gioco dell'oca —
ricordati di aggiungere l'attribuzione anche lì.

I file che servono a una sola scheda portano il prefisso del suo generatore
(`alf-` l'alfabetiere, `dis-` gli album, `oca-` il gioco dell'oca); i disegni
già presenti si riusano invece di scaricarne un doppione.

## Se aggiungi un disegno

1. Scegli il pittogramma su [arasaac.org](https://arasaac.org) e **guardalo**:
   serve un contorno pulito, non una figura riempita di nero, altrimenti non si
   può colorare.
2. Aggiungi `nome-file: id` a `static/pittogrammi/arasaac-bn/registro.json` e
   lancia `bash scripts/scarica-pittogrammi.sh`.
3. Aggiungi la voce nel modulo di dati, con un `alt` che descrive **ciò che si
   vede davvero** e una didascalia che dà un nome alla cosa senza trasformarsi
   in un'istruzione di autoprotezione: quelle stanno nelle schede dedicate.
4. Rigenera, ricontrolla il numero di fogli in stampa, rifà pacchetti e parità.
