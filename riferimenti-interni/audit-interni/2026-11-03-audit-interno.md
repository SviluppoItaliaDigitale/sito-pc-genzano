# Audit interno del sito — 3 novembre 2026 — snapshot `98a2326`

Esito: **7 rilievi** (P1: 2 · P2: 3 · P3: 2) · corretti in questo run (Categoria A): **5** · da validare o decidere: **2**.

Audit mensile (routine `trig_01RMQwDs5Ku2mRfkwkDZnKmx`). Perimetro eseguito: build Hugo 0.154.5 pulita (con e senza le modifiche), integrità asset (5.330 file), ancore (5.230), JSON-LD, qualità pagine (1.647), navigazione, parità schede (4 kit), dati vs dataset, dati canonici (52 voci), incongruenze (10 famiglie), menu, calendario prevenzione, catalogo lezioni, mappe raccontate, libro 3D, ruoli ARIA, inventario PDF (73), comunicati, data di uscita, refusi e grammatica (0 errori reali), freschezza, fonti del cruscotto, 60 workflow (YAML, timeout, pin SHA), scansione segreti, feed CAP/sitemap, stato allerta (verde, controllo di 0,5 h fa), pagine critiche live (HTTP 200; live sulla stessa build di `main`). Revisione dei fatti sugli articoli di anniversario in uscita fra il 4 e il 17 novembre.
**Non eseguiti in questa sessione** (limite dell'ambiente, dichiarato): axe-core nel browser, esercitazione completa della catena di allerta, collaudo interattivo del sito pubblicato, confronto dell'intero manifesto col sito live (la richiesta verso il sito ha superato il tempo massimo; verificate a campione le pagine critiche e lo SHA di build).

## Rilievi

### F01 · Firenze 1966, Genova 2011, Piemonte 1994, Versilia 1996 (in uscita 4-8/11): dati e cause senza fonte o smentiti  P1
Tipo: difetto confermato — **corretto**
Prova: confronto con DPC, Arpae, ISPRA, Vigili del Fuoco, ACI-ISTAT. Fra gli altri: Firenze «sei metri» e «alle sei Santa Croce allagata» (targa 4,92 m, notte 3-4 novembre); Genova «500 mm in 6 ore» (ARPAL: fino a 400 mm in 12 ore) e causa attribuita alla manutenzione dei tombini (nessuna fonte); Piemonte «decine di vittime» (DPC: 68); Versilia «notte del 19 giugno» (VVF: temporale dalle 6, massimo alle 13:50) e cause attribuite alle cave di marmo (nessuna fonte).
Impatto: errori su tragedie con vittime, la categoria del gate dei fatti.
Correzione: testi riallineati alle fonti, affermazioni non verificabili tolte o riformulate (anche nei campi social). Versione facile dei maremoti inclusa.
Verifica: `check-dati-canonici.py` OK, `check-data-uscita.py` OK, build pulita.
Fonti: servizio-nazionale.protezionecivile.gov.it (Firenze, Genova, Piemonte), aggiornati.arpae.it (Ecoscienza 5-6/2011), ISPRA, scheda VVF Versilia, Università di Pisa.

### F02 · Versilia 1996: l'articolo del 19/06 contraddiceva quello di novembre sull'ora dell'evento  P1
Tipo: difetto confermato — **corretto**
Prova: `2026-06-19-versilia-1996-alluvione-cardoso-stazzema.md` diceva «pioggia dal 18 giugno, picco tra le 2 e le 4 del mattino, la popolazione dormiva», «470 mm», «decine di dispersi mai ritrovati», «mille senzatetto, 250 miliardi di lire».
Impatto: due articoli del sito davano versioni diverse e la più forte non aveva fonte.
Correzione: allineato ai Vigili del Fuoco (19 giugno, dalle 6, circa 480 mm in circa 12 ore, massimo alle 13:50); dati senza fonte tolti.
Verifica: grep delle frasi vecchie vuoto.

### F03 · Casco in bicicletta «obbligatorio per i minori»: 4 articoli (2 versioni facili)  P2
Tipo: difetto confermato — **corretto**
Prova: `grep -rn "casco.*obbligator" content`. Il Codice della Strada (art. 182) non prevede il casco in bicicletta. Gli articoli del 30/04 e del 03/06 (con le facili) lo davano obbligatorio.
Correzione: «non obbligatorio per legge, ma raccomandato», coerente con l'articolo del 6/12 e del 17/11.
Verifica: grep. **Da confermare** con `pc-normative-verifier` sul testo vigente su Normattiva alla prossima sessione (non riletto qui).

### F04 · Giornata vittime della strada: dati ACI-ISTAT 2024 imprecisi e articolo che esce dopo la giornata  P2
Tipo: difetto confermato — **corretto** (dati) / **da decidere** (data)
Prova: feriti 233.853 (non «oltre 220.000»), incidenti 173.364 (non «165.000»), ciclisti 185 in calo del 12,7% (non «in crescita»). La giornata cade domenica 15/11/2026, l'articolo esce il 17/11: testo reso neutro («in occasione della Giornata»).
Raccomandazione: anticipare l'uscita al 14-15 novembre (`pc-calendario-editoriale`); non fatto perché sposta l'ordine di tre articoli.

### F05 · Articoli Halloween con scadenza 31/10 non archiviati (issue #1676)  P3
Tipo: difetto confermato — **corretto** (`archiviato: true` su articolo e versione facile).

### F06 · Registrazione del dominio protezionecivilegenzano.it in scadenza il 30/12/2026 (issue #1666)  P2
Tipo: da validare — responsabile: Alessandro/Aruba. Rinnovo da verificare sul pannello Aruba; se scade si spengono sito, feed e QR stampati.

### F07 · CSP con `unsafe-inline`/`unsafe-eval`; scheda di fonti non raggiungibili da questo ambiente  P3
Tipo: raccomandazione ereditata (stretta della CSP in Report-Only, già nota). I feed YouTube (404 su 17 canali) e CelesTrak non rispondono da questo ambiente: nessun run fallito nelle ultime 100 esecuzioni CI, quindi si ritiene un limite del proxy; da ricontrollare al prossimo giro di `controllo-fonti-cruscotto`.

## Dati non verificabili lasciati (con avvertenza)
Genova: data 2019 dello scolmatore del Fereggiano (da dichiarazione, da ricontrollare); maremoti: equivalenza calendario lunare del 5 novembre 1854 (calcolo, da ricontrollare). Firenze: scout, diga di Levane, origine dei Gruppi comunali; Piemonte: Ceva; Strada: paragrafi su fasce d'età e citazione AIFVS.
