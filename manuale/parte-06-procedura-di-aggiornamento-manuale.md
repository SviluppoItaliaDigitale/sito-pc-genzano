_[Indice manuale](README.md)_

# Parte 6 — Procedura di aggiornamento manuale

### Fonti da monitorare

| Fonte | URL | Cosa verificare |
|---|---|---|
| Manuale operativo design PA | [docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/) | Versione, data ultima modifica |
| Writing Toolkit | [designers.italia.it/risorse-per-il-design/writing-toolkit/](https://designers.italia.it/risorse-per-il-design/writing-toolkit/) | Nuove regole di scrittura |
| Linee guida design | [docs.italia.it/italia/designers-italia/design-linee-guida-docs/](https://docs.italia.it/italia/designers-italia/design-linee-guida-docs/) | Versione |
| Bootstrap Italia | [github.com/italia/bootstrap-italia/releases](https://github.com/italia/bootstrap-italia/releases) | Ultima versione stabile |
| AGID Accessibilità | [agid.gov.it/it/design-servizi/accessibilita](https://agid.gov.it/it/design-servizi/accessibilita) | Aggiornamenti normativi |
| Form AGID | [form.agid.gov.it](https://form.agid.gov.it/) | Procedura dichiarazione |

### Quando aggiornare

1. **Automaticamente ogni lunedì** — la GitHub Action settimanale apre un'Issue con i
   documenti da ricontrollare.
2. **Ogni 3 mesi** — in ogni caso, revisione periodica anche senza Issue.
3. **Ad ogni nuova versione** di Bootstrap Italia o del Manuale operativo.
4. **Ad ogni modifica normativa** su accessibilità, privacy, PA digitale.

### Come aggiornare manualmente

1. Apri Claude Code nella cartella del sito.
2. Dì: *"Verifica se le linee guida AGID sono aggiornate e aggiorna il manuale di stile se
   necessario."*
3. Claude Code:
   - Verifica le fonti online.
   - Confronta con le versioni nel manuale.
   - Aggiorna `MANUALE-SITO.md`.
   - Aggiorna le regole in `.claude/rules/02-content-design-pa.md`.
   - Aggiorna eventuali archetype o template.
   - Commit e push.

### Istruzioni per AI esterne (auto-aggiornamento assistito)

> **ISTRUZIONE:** Se questo file ti viene fornito per redigere un articolo, controlla la
> data "Ultimo check linee guida AGID" in cima. Se è più vecchia di 3 mesi rispetto alla data
> odierna, avvisa l'utente con questo messaggio:
>
> *"Il manuale di stile potrebbe essere obsoleto (ultimo aggiornamento: [data]). Ti consiglio
> di aggiornarlo tramite Claude Code o di attendere il prossimo check automatico settimanale.
> Vuoi che prosegua comunque con le regole attuali?"*
>
> Se l'utente conferma, prosegui. Altrimenti, attendi l'aggiornamento.

---

_[Indice manuale](README.md)_

[← Parte 05 — Checklist pre-pubblicazione](parte-05-checklist-pre-pubblicazione.md) · [↑ Indice](README.md) · [Parte 07 — Aggiornamento automatico settimanale →](parte-07-aggiornamento-automatico-settimanale.md)
