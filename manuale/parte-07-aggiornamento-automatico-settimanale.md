_[Indice manuale](README.md)_

# Parte 7 — Aggiornamento automatico settimanale

Il repository include una **GitHub Action** (`.github/workflows/aggiorna-manuale.yml`)
che ogni **lunedì alle 08:00** (ora italiana) verifica lo stato delle fonti ufficiali e
apre un'**Issue** sul repository con la checklist dei punti da controllare.

### Come funziona

1. La Action fetcha:
   - Le pagine principali di Designers Italia e AGID.
   - L'ultimo release tag di Bootstrap Italia via API GitHub.
2. Calcola un hash SHA-256 del contenuto.
3. Confronta con gli hash memorizzati in `.manuale/sources-hashes.json`.
4. Se qualche hash è cambiato (o se l'Issue settimanale non esiste), apre un'Issue con:
   - Lista delle fonti cambiate.
   - Nuova versione di Bootstrap Italia (se disponibile).
   - Checklist di punti da controllare nel manuale.
5. Aggiorna il file `.manuale/sources-hashes.json` con i nuovi hash.
6. Commit automatico del file hashes (solo quel file).

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

1. Vai su GitHub → Actions → "Aggiorna manuale di stile".
2. Clicca "Run workflow" → "Run workflow".
3. Attendi ~1 minuto. Se ci sono novità, apparirà una nuova Issue.

---

_[Indice manuale](README.md)_

[← Parte 06 — Procedura di aggiornamento manuale](parte-06-procedura-di-aggiornamento-manuale.md) · [↑ Indice](README.md) · [Parte 08 — Modificare e cancellare contenuti →](parte-08-modificare-e-cancellare-contenuti.md)
