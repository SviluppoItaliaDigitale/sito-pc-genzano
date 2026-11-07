# Audit del sito del 07/11/2026 — revisori del consulto

Materiale per i revisori dell'audit completo del 07/11/2026 che non possono aprire il sito da soli: lavorano su un fascicolo
del sito pubblicato e rispondono con una sola richiesta ciascuno. Le loro chiavi gratuite stanno solo sul PC di
Alessandro, quindi il giro parte da lì. Gli altri revisori dello stesso audit sono elencati in bacheca (`COORDINAMENTO.md`,
«Lavori in corso»).

| File | A che cosa serve |
|---|---|
| `fascicolo.md` | Il sito pubblicato il 07/11/2026 alle 11:13: misure di 35 pagine (codice, peso, tempo, lingua, titoli, immagini), intestazioni HTTP, `robots.txt`, menu, pagine della mappa del sito per sezione, ultimi articoli e testo delle pagine principali. Il JavaScript non è stato eseguito. |
| `richiesta.md` | La richiesta, uguale per tutti: sei sezioni, rilievi con prova presa dal fascicolo, vincoli del progetto. Al posto di `<LETTERA>` va la lettera del revisore. |
| `esegui.sh` | Il comando unico per il PC: fa lavorare i revisori insieme, ripulisce e controlla i rapporti, aggiorna l'esito in bacheca e apre una PR in bozza. |
| `rapporto.py` | Usato da `esegui.sh`: titolo esatto, sei sezioni, rilievi completi, nomi di strumenti da togliere; testo della PR ed esito per la bacheca. |

## Come si esegue

Dalla cartella del repository sul PC, con qualunque ramo aperto (il comando lavora in una cartella a parte, partendo da
`origin/main`):

```bash
cd ~/sito-pc-genzano && git fetch -q origin && bash <(git show origin/main:riferimenti-interni/audit-esterni/consulto-2026-11-07/esegui.sh)
```

Dura fino a mezz'ora. Per rifare solo alcuni revisori si aggiungono le loro lettere in fondo, per esempio `… esegui.sh) b j`.
Se un servizio non risponde, il suo rapporto manca e la bacheca lo dice; gli altri vanno avanti.

## Dopo

I rapporti arrivano in `riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-<lettera>.md` sul ramo
`claude/audit-consulto-revisori-20261107`, con ogni rilievo «Esito: da verificare». Claude verifica ogni rilievo sul sito
pubblicato e sul repository, scrive l'esito accanto, toglie i nomi di strumenti segnalati e unisce la PR; poi aggiorna il
confronto dei revisori per Alessandro.
