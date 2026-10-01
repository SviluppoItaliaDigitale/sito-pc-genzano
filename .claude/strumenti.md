# Registro degli strumenti del progetto

Regola in `.claude/rules/strumenti.md`: ogni strumento che resta nel repo si annota qui (nome, scopo, data, origine).

| Nome | Scopo | Data | Origine |
|---|---|---|---|
| `.claude/agents/pc-calendario-editoriale.md` | Gate del calendario: la data di uscita di un articolo programmato deve essere coerente con la data che annuncia | 28/09/2026 | scritto nel repo, su richiesta dell'utente dopo l'articolo AIB uscito fuori data |
| `scripts/check-data-uscita.py` | Controllo deterministico usato dall'agente, da `validate-pr.yml` e da `controllo-data-uscita.yml` (solo stdlib) | 28/09/2026 | scritto nel repo |
| `.github/workflows/controllo-data-uscita.yml` | Controllo serale degli articoli in uscita nei prossimi 10 giorni, issue in-place | 28/09/2026 | scritto nel repo |
| `data/dati_canonici.yaml` | Registro dei dati che devono essere uguali in tutto il sito: valore, fonte ufficiale, varianti sbagliate da cercare | 01/10/2026 | scritto nel repo, su richiesta dell'utente («dati unici e ufficiali») |
| `scripts/check-dati-canonici.py` | Cerca le varianti sbagliate del registro in content/, data/, static/ e layout; bloccante in `validate-pr.yml` (stdlib + PyYAML) | 01/10/2026 | scritto nel repo |
