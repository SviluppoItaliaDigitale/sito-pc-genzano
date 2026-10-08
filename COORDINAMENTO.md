# Bacheca di coordinamento fra le sessioni che lavorano sul sito

File interno, non pubblicato (Hugo non legge la cartella principale del repository). Lo usano Claude e ChatGPT per lasciarsi avvisi quando lavorano sul sito nello stesso periodo. Regola dell'utente dell'8 ottobre 2026.

## Come si usa

1. **Prima di cominciare** un lavoro leggi questa bacheca **e l'elenco delle pull request aperte**: le PR dicono quali file stanno cambiando. Se un file che vuoi toccare è già in una PR aperta, non cambiarlo: aspetta che quella PR sia unita, oppure scrivi qui che cosa ti serve.
2. **Lascia un avviso** quando il tuo lavoro può riguardare l'altra sessione: file o cartelle che stai rifacendo, uno script o uno shortcode che hai cambiato, un file generato da rigenerare, un problema trovato nel lavoro dell'altra.
3. **Formato**: una voce in cima alla sezione «Avvisi», con data e ora italiana, chi scrive e il testo. Frasi brevi, file nominati per percorso.
4. **Quando un avviso non serve più**, chi lo ha scritto lo sposta in «Archiviati» con una riga su com'è finita.
5. La bacheca cambia, come ogni altro file, **solo con una pull request** (vedi il riquadro in cima ad `AGENTS.md`). Per un avviso urgente scrivilo anche nella descrizione della tua PR, che l'altra sessione vede subito.

Qui non vanno mai credenziali, dati personali o testi destinati al sito.

## Chi fa che cosa

Indicazioni dell'utente dell'8 ottobre 2026.

- **Immagini e illustrazioni (di solito ChatGPT).** Si preparano su un ramo proprio e arrivano con una PR; nella bacheca un avviso «illustrazioni X pronte nella PR #N, da controllare». Prima dell'unione l'altra sessione le guarda renderizzate (vedi l'avviso sulle illustrazioni qui sotto). Se l'altra sessione non è disponibile, chi le ha fatte le rende e le guarda da sé, a 1200 px e a 720 px.
- **Audit del sito (di solito ChatGPT).** Chi fa l'audit **non corregge**: scrive i rilievi in `riferimenti-interni/audit-esterni/AAAA-MM-GG-<argomento>.md` (formato nel README della cartella) e lascia un avviso qui. L'altra sessione verifica ogni rilievo, corregge quelli fondati con una PR e scrive l'esito accanto a ciascuno (corretto nella PR #N, non riprodotto, già a posto). Così l'utente non deve più copiare l'audit da una chat all'altra.
- **Pubblicazioni urgenti quando l'altra sessione non c'è.** Si pubblica con una PR e i controlli verdi; direttamente su `main` solo se l'utente lo chiede espressamente. In entrambi i casi un avviso qui: «pubblicato in urgenza: file …, motivo …, PR o commit …». Alla prima sessione utile l'altra lo ripassa e archivia l'avviso con l'esito.

## Richieste

Lavori che una sessione chiede all'altra. L'utente avvisa la sessione destinataria («guarda le richieste in bacheca»): nessuna delle due legge la bacheca da sola finché non viene aperta. Chi prende in carico una richiesta scrive accanto «presa da …, PR #N»; a lavoro unito la sposta in «Archiviati».

Formato per una richiesta di immagine:

```markdown
- **AAAA-MM-GG — da Claude a ChatGPT — Illustrazione <nome-file>.svg**
  - Pagina: /percorso/della/pagina/ (sezione …)
  - Che cosa deve far capire: …
  - Che cosa deve mostrare: … (gesti e comportamenti come nelle indicazioni DPC citate nella pagina)
  - Testi nell'immagine: … (pochi, brevi, mai sopra i disegni)
  - Formato: SVG 1200×620 in static/formazione/illustrazioni-udl/, più la versione -mobile.svg 720×1180 se ci sono più riquadri
  - Vincoli: title e desc in italiano su ciò che si vede; nessun riferimento allo strumento usato; nessun logo
```

Nessuna richiesta aperta.

## Avvisi

- **08/10/2026, 21:45 — Claude.** Le illustrazioni in `static/formazione/illustrazioni-udl/` sono state controllate a vista e corrette (PR #1283, #1285, #1286, #1287, #1291). Prima di aggiungerne o modificarne una: rendila, guardala a 1200 px e, per le versioni `-mobile.svg`, a 720 px; nessun testo sopra un disegno; testo scuro solo su fondo chiaro; `<title>` e `<desc>` che descrivono ciò che si vede; `python3 scripts/check-illustrazioni-udl.py` verde.
- **08/10/2026, 21:45 — Claude.** I pittogrammi ARASAAC si scelgono guardandoli: il primo risultato della ricerca può mostrare tutt'altro (era successo con «scappare», «ospedale», «caldo», «frana»). In `scripts/scarica-pittogrammi.sh` un quarto campo fissa l'identificativo verificato.

## Archiviati

Nessuno.
