# Parte 41 — Le schede didattiche a più fogli, e come si rigenerano

Quattro schede stampabili non si scrivono a mano. Hanno decine di fogli quasi
identici, e chi corregge un refuso su un foglio lo lascia sugli altri
venticinque. Per queste, la fonte di verità non è l'HTML ma un piccolo
generatore in `scripts/schede-didattiche/`, e l'HTML è il suo prodotto.

| Scheda | Cartella | Fogli | Generatore |
|---|---|---|---|
| A come Allerta, Z come Zaino | `alfabetiere-az-infanzia/` | 26 | `genera-alfabetiere-quaderno.py` |
| L'alfabetiere della sicurezza | `alfabetiere-pc-infanzia/` | 1 | `genera-alfabetiere-tabella.py` |
| I mezzi della protezione civile | `disegni-mezzi-infanzia/` | 12 | `genera-album-disegni.py` |
| Le persone che aiutano | `disegni-persone-infanzia/` | 12 | `genera-album-disegni.py` |
| Le giornate insieme | `disegni-momenti-infanzia/` | 12 | `genera-album-disegni.py` |
| Memory della protezione civile | `memory-protezione-civile-infanzia/` | 3 | `genera-memory.py` |

## Non modificare l'HTML a mano

Una correzione scritta direttamente nell'`index.html` sopravvive fino alla
prossima rigenerazione e poi sparisce, senza avviso. I testi vivono nei due
moduli di dati:

- `scripts/schede-didattiche/alfabeto_dati.py` — le 26 lettere;
- `scripts/schede-didattiche/disegni_dati.py` — i tre album.

Il memory tiene le sue dieci coppie dentro al generatore, perché sono poche e
l'ordine sul foglio fa parte del gioco.

## La sequenza completa

```bash
cd scripts/schede-didattiche
python3 genera-alfabetiere-quaderno.py
python3 genera-alfabetiere-tabella.py
python3 genera-album-disegni.py
python3 genera-memory.py
cd ../..
python3 scripts/genera-pacchetti-schede.py
python3 scripts/genera-pacchetti-kit.py
python3 scripts/check-parita-schede.py
```

Gli ultimi tre comandi non sono un di più. Senza di loro la scheda cambia sulla
pagina singola e resta vecchia in «Stampa tutto» e nello ZIP offline: è
esattamente il disallineamento che `check-parita-schede.py` esiste per vietare,
e che fa fallire la pull request.

## Contare i fogli prima di pubblicare

Una scheda che in stampa sborda su una pagina in più è un difetto che il
browser non segnala. Il controllo si fa rendendo la pagina in media `print` e
contando le pagine del PDF: il quaderno deve dare **26** pagine, la tabella
**1**, ogni album **12**, il memory **3**. Se il numero cresce, il colpevole di
solito è l'immagine: si riduce di un paio di millimetri e si ricontrolla.

## Le illustrazioni

Sono pittogrammi **ARASAAC** nella variante in bianco e nero, quella con il solo
contorno, pensata per essere colorata. Stanno in
`static/pittogrammi/arasaac-bn/`, e `registro.json` dice per ogni file da quale
pittogramma ARASAAC viene. Si riscaricano con `bash scripts/scarica-pittogrammi.sh`:
la sezione dedicata legge il registro e scarica **per identificativo**, non per
parola chiave, così il risultato non cambia se ARASAAC riordina i risultati di
ricerca.

Licenza **CC BY-NC-SA 4.0**, autore Sergio Palao, origine ARASAAC, proprietà del
Governo di Aragona. Le schede che li contengono ereditano la stessa licenza.

🔴 **L'attribuzione va su ogni foglio, non solo sul primo.** Queste schede
invitano esplicitamente a stampare una pagina alla volta: il foglio che finisce
in classe deve portare la licenza con sé. Se aggiungi un foglio, controlla che
il paragrafo della licenza ci sia anche lì.

## Scegliere un pittogramma nuovo

1. Cercalo su [arasaac.org](https://arasaac.org) e **guardalo davvero**. Serve un
   contorno pulito: le figure riempite di nero non si possono colorare, e sono
   la metà abbondante dei risultati di ricerca.
2. Aggiungi `nome-file: id` a `static/pittogrammi/arasaac-bn/registro.json`,
   poi `bash scripts/scarica-pittogrammi.sh`.
3. Nel modulo di dati scrivi un `alt` che descrive **ciò che si vede davvero**,
   non ciò che vorresti significasse.
4. La didascalia dà un nome alla cosa. Non è il posto per le istruzioni di
   autoprotezione: quelle stanno nelle schede dedicate, dove sono complete e
   allineate al Dipartimento della Protezione Civile. Una riga a metà, su un
   foglio da colorare, è peggio di nessuna riga.

## Le lettere dell'alfabetiere

L'alfabeto italiano tradizionale ha **21 lettere**. J, K, W, X e Y non ne fanno
parte: si incontrano nelle parole venute da altre lingue, e nei dati portano il
flag `ospite`. La **H** invece c'è, ma non ha un suono proprio — si scrive in
*ho, hai, ha, hanno* e nei gruppi *ch* e *gh* — e porta il flag `muta`.

La distinzione non è pedanteria: la scheda la stampa un insegnante e la legge un
bambino di cinque anni. Scrivere che «la H non è una lettera italiana» insegna
una cosa falsa a tutti e due.
