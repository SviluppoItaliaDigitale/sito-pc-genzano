# Registro degli strumenti del progetto

Regola in `.claude/rules/strumenti.md`: ogni strumento che resta nel repo si annota qui (nome, scopo, data, origine).

| Nome | Scopo | Data | Origine |
|---|---|---|---|
| `.claude/agents/pc-calendario-editoriale.md` | Gate del calendario: la data di uscita di un articolo programmato deve essere coerente con la data che annuncia | 28/09/2026 | scritto nel repo, su richiesta dell'utente dopo l'articolo AIB uscito fuori data |
| `scripts/check-data-uscita.py` | Controllo deterministico usato dall'agente, da `validate-pr.yml` e da `controllo-data-uscita.yml` (solo stdlib) | 28/09/2026 | scritto nel repo |
| `.github/workflows/controllo-data-uscita.yml` | Controllo serale degli articoli in uscita nei prossimi 10 giorni, issue in-place | 28/09/2026 | scritto nel repo |
