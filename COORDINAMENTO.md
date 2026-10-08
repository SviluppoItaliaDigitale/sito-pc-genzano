# Bacheca di coordinamento fra le sessioni che lavorano sul sito

File interno, non pubblicato (Hugo non legge la cartella principale del repository). Lo usano Claude e ChatGPT per lasciarsi avvisi quando lavorano sul sito nello stesso periodo. Regola dell'utente dell'8 ottobre 2026.

## Come si usa

1. **Prima di cominciare** un lavoro leggi questa bacheca **e l'elenco delle pull request aperte**: le PR dicono quali file stanno cambiando. Se un file che vuoi toccare è già in una PR aperta, non cambiarlo: aspetta che quella PR sia unita, oppure scrivi qui che cosa ti serve.
2. **Lascia un avviso** quando il tuo lavoro può riguardare l'altra sessione: file o cartelle che stai rifacendo, uno script o uno shortcode che hai cambiato, un file generato da rigenerare, un problema trovato nel lavoro dell'altra.
3. **Formato**: una voce in cima alla sezione «Avvisi», con data e ora italiana, chi scrive e il testo. Frasi brevi, file nominati per percorso.
4. **Quando un avviso non serve più**, chi lo ha scritto lo sposta in «Archiviati» con una riga su com'è finita.
5. La bacheca cambia, come ogni altro file, **solo con una pull request** (vedi il riquadro in cima ad `AGENTS.md`). Per un avviso urgente scrivilo anche nella descrizione della tua PR, che l'altra sessione vede subito.

Qui non vanno mai credenziali, dati personali o testi destinati al sito.

## Avvisi

- **08/10/2026, 21:45 — Claude.** Le illustrazioni in `static/formazione/illustrazioni-udl/` sono state controllate a vista e corrette (PR #1283, #1285, #1286, #1287, #1291). Prima di aggiungerne o modificarne una: rendila, guardala a 1200 px e, per le versioni `-mobile.svg`, a 720 px; nessun testo sopra un disegno; testo scuro solo su fondo chiaro; `<title>` e `<desc>` che descrivono ciò che si vede; `python3 scripts/check-illustrazioni-udl.py` verde.
- **08/10/2026, 21:45 — Claude.** I pittogrammi ARASAAC si scelgono guardandoli: il primo risultato della ricerca può mostrare tutt'altro (era successo con «scappare», «ospedale», «caldo», «frana»). In `scripts/scarica-pittogrammi.sh` un quarto campo fissa l'identificativo verificato.

## Archiviati

Nessuno.
