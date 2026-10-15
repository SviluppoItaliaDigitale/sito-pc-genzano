_[Indice manuale](README.md)_

# Parte 7 — Aggiornamento automatico settimanale

Il repository include una **GitHub Action** (`.github/workflows/aggiorna-manuale.yml`)
che ogni **lunedì alle 08:00** (ora italiana) verifica lo stato delle fonti ufficiali e
apre un'**Issue** sul repository con la checklist dei punti da controllare.

### Come funziona

1. Scarica dai repository ufficiali su GitHub il testo dei manuali di scrittura: Fondamenti del
   design system .italia (Contenuti, Linguaggio, Microtesti, Tono di voce), Guida alle parole
   della PA, Linee guida di design, Manuale operativo di design (`scripts/manuali-agid.py`).
   La copia sta in `.manuale/manuali-agid/` e si rinnova da sola.
2. Legge le pagine web di Designers Italia, AGID, Bootstrap Italia e DPC e calcola un hash
   SHA-256 del testo visibile, confrontandolo con `.manuale/sources-hashes.json`.
3. Se un manuale o una pagina è cambiato, apre un'Issue con:
   - i documenti cambiati, con le righe cambiate e il confronto dei commit;
   - le pagine web cambiate;
   - la checklist di punti da controllare nel manuale, nelle regole e nella skill dei testi.
4. Se una fonte non si legge (pagina spostata, sito che rifiuta le richieste, pagina senza
   testo leggibile), lo scrive nell'Issue «⚠️ Fonti del manuale operativo non raggiungibili»,
   che si aggiorna ogni settimana e si chiude da sola alla prima settimana in cui tutte le fonti si
   leggono (un controllo interrotto a metà non la chiude).
5. Commit automatico degli hash e della copia dei manuali (solo `.manuale/`).

### Come agire sull'Issue

Quando ricevi la notifica dell'Issue settimanale:

1. Apri l'Issue: contiene link e checklist.
2. Apri Claude Code nella cartella del sito.
3. Dì: *"Aggiorna il manuale di stile con le novità dell'Issue #XX."*
4. Claude legge l'Issue, verifica le fonti, propone le modifiche.
5. Approva le modifiche.
6. Commit e push: l'Issue viene chiusa automaticamente se referenziata nel commit
   (`closes #XX`).

### Come disabilitare temporaneamente

Se non vuoi ricevere Issue settimanali per un periodo:

1. Apri `.github/workflows/aggiorna-manuale.yml`.
2. Commenta la sezione `schedule:` o rimuovi il trigger `schedule`.
3. Commit e push.

Per riattivare: ripristina la sezione.

### Esecuzione manuale

Puoi triggerare la Action a mano:

1. Vai su GitHub → Actions → "Aggiornamento MANUALE-SITO.md".
2. Clicca "Run workflow" → "Run workflow".
3. Attendi ~1 minuto. Se ci sono novità, apparirà una nuova Issue.

---

_[Indice manuale](README.md)_

[← Parte 06 — Procedura di aggiornamento manuale](parte-06-procedura-di-aggiornamento-manuale.md) · [↑ Indice](README.md) · [Parte 08 — Modificare e cancellare contenuti →](parte-08-modificare-e-cancellare-contenuti.md)
