# Audit esterni — rilievi da verificare

Cartella interna, non pubblicata. Qui chi fa un audit del sito (di solito ChatGPT, su richiesta dell'utente) scrive i rilievi **senza correggere nulla**. La verifica e le correzioni le fa l'altra sessione, con una PR, e annota l'esito accanto a ogni rilievo. Regola in `COORDINAMENTO.md` § «Chi fa che cosa».

## Nome del file

`AAAA-MM-GG-<argomento>.md`, per esempio `2026-10-09-schede-infanzia.md`. Un file per audit; dopo averlo creato, un avviso in `COORDINAMENTO.md`.

## Formato di ogni rilievo

```markdown
### R1 — <titolo breve>
- **Dove:** URL della pagina e, se lo sai, file del repository
- **Che cosa non va:** descrizione concreta, con la frase o il dato esatto
- **Prova:** come lo hai verificato (fonte, misura, schermata descritta)
- **Priorità:** P1 (sbagliato o pericoloso) · P2 (da correggere) · P3 (miglioramento)
- **Esito:** (lo compila chi verifica: corretto nella PR #N · non riprodotto · già a posto · da decidere con l'utente)
```

Niente dati personali, credenziali o contenuti copiati da siti di terzi.
