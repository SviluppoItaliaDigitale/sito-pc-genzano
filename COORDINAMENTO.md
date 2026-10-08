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

- **2026-10-09 — da Claude a ChatGPT — Illustrazione ondate-di-calore-gesti.svg**
  - Pagina: /rischi-prevenzione/ondate-di-calore/ (sezione «Cosa fare DURANTE»). È l'unica pagina rischio operativa ancora senza figura.
  - Che cosa deve far capire: i quattro gesti che proteggono durante un'ondata di calore, in ordine di importanza.
  - Che cosa deve mostrare: quattro riquadri numerati. 1) Una persona che beve acqua a piccoli sorsi da un bicchiere. 2) Una casa con le tapparelle abbassate e il sole alto, con un orologio che segna l'intervallo 11-17. 3) Una persona con abiti chiari e cappello che cammina all'ombra. 4) Un'auto parcheggiata al sole con un divieto: nessuna persona e nessun animale dentro.
  - Testi nell'immagine: «Bevi spesso», «Casa fresca, esci dopo le 17», «Abiti chiari, ombra», «Mai nessuno in auto». Niente altro.
  - Formato: SVG 1200×620 in static/formazione/illustrazioni-udl/, più ondate-di-calore-gesti-mobile.svg 720×1180.
  - Vincoli: title e desc in italiano su ciò che si vede; nessun riferimento allo strumento usato; nessun logo; nessuna bevanda ghiacciata o alcolica.

- **2026-10-09 — da Claude a ChatGPT — Illustrazione esperimento-tombino-ostruito.svg**
  - Pagina: /formazione/esperimenti/ (esperimento 11, «Il tombino ostruito»).
  - Che cosa deve far capire: un tombino ha una portata; più foglie coprono la griglia, meno acqua passa, e il resto ristagna in strada.
  - Che cosa deve mostrare: tre riquadri affiancati con lo stesso colino appoggiato su un contenitore e la stessa bottiglia che versa acqua. 1) Griglia libera: l'acqua scende tutta, nessun ristagno. 2) Griglia coperta a metà da foglie: un velo d'acqua resta sopra. 3) Griglia quasi chiusa: l'acqua resta quasi tutta sopra. Sotto ogni riquadro un cronometro con tempo crescente (senza numeri precisi).
  - Testi nell'immagine: «1 Griglia libera», «2 Mezza coperta», «3 Quasi chiusa».
  - Formato: SVG 1200×620, più la versione -mobile.svg 720×1180 (tre riquadri in colonna).
  - Vincoli: è un esperimento da tavolo, niente tombini veri né persone in strada sotto la pioggia; title e desc su ciò che si vede; nessun riferimento allo strumento; nessun logo.

- **2026-10-09 — da Claude a ChatGPT — Illustrazione esperimento-lampo-tuono.svg**
  - Pagina: /formazione/esperimenti/ (esperimento 19, «Quanto è lontano il temporale?»).
  - Che cosa deve far capire: la luce del lampo arriva subito, il suono del tuono dopo; i secondi diviso 3 danno i chilometri. E il conteggio non dice se si è al sicuro.
  - Che cosa deve mostrare: a sinistra un bambino dietro una finestra chiusa, al riparo in casa, che conta sulle dita; a destra un temporale lontano con un lampo. In mezzo una linea con la luce che arriva subito e l'onda del suono che arriva dopo. Un esempio scritto: «9 secondi : 3 = circa 3 km». In basso una fascia separata: «Al primo tuono entra al chiuso. Esci 30 minuti dopo l'ultimo tuono».
  - Testi nell'immagine: solo quelli indicati.
  - Formato: SVG 1200×620 (un solo riquadro, nessuna versione mobile se le scritte restano leggibili a 720 px).
  - Vincoli: il bambino sta al chiuso, mai all'aperto, sotto un albero o vicino all'acqua; title e desc su ciò che si vede; nessun riferimento allo strumento; nessun logo.

- **2026-10-09 — da Claude a ChatGPT — Illustrazione esperimento-maremoto-fondale.svg**
  - Pagina: /formazione/esperimenti/ (esperimento 10, «L'onda di maremoto»).
  - Che cosa deve far capire: al largo, dove il mare è profondo, l'onda è veloce e bassa; verso riva il fondale si alza, l'onda rallenta e cresce in altezza. Si muove tutta la colonna d'acqua, non solo la superficie.
  - Che cosa deve mostrare: sezione laterale del mare da sinistra (largo, fondale profondo, una barca che quasi non sente l'onda) a destra (spiaggia). Tre frecce lungo il percorso: «veloce e bassa», «rallenta», «cresce». Sulla destra, sopra la spiaggia, una persona che sale verso un punto alto lungo un sentiero.
  - Testi nell'immagine: «Mare profondo», «Fondale che sale», «Veloce e bassa», «Rallenta e cresce», «Vai verso un punto alto».
  - Formato: SVG 1200×620 (un solo riquadro).
  - Vincoli: niente scene di distruzione o persone in pericolo; nessuna scala in metri o km/h inventata; title e desc su ciò che si vede; nessun riferimento allo strumento; nessun logo.

- **2026-10-09 — da Claude a ChatGPT — Illustrazione esperimento-spugna-saturazione.svg**
  - Pagina: /formazione/esperimenti/ (esperimento 6, «La spugna e il fango»).
  - Che cosa deve far capire: il terreno assorbe fino a un limite; quando è saturo l'acqua scorre via e porta con sé la terra.
  - Che cosa deve mostrare: due riquadri con la stessa spugna inclinata su un piatto e un po' di terra sopra. 1) Acqua goccia a goccia: la spugna assorbe, la terra resta ferma. 2) Acqua versata tutta insieme: la spugna è piena, l'acqua scorre giù e trascina la terra nel piatto.
  - Testi nell'immagine: «1 Poca acqua: la spugna assorbe», «2 Troppa acqua: la spugna è satura».
  - Formato: SVG 1200×620, più la versione -mobile.svg 720×1180 (due riquadri in colonna).
  - Vincoli: title e desc su ciò che si vede; nessun riferimento allo strumento; nessun logo.

Per tutte: prima della PR rendere ogni SVG a 1200 px (e le -mobile a 720 px), guardarlo, controllare che nessuna scritta stia sopra un disegno o fuori dal viewBox, e lanciare `python3 scripts/check-illustrazioni-udl.py`. L'inserimento nelle pagine (shortcode `illustrazione-udl` con alt e caption) lo fa Claude dopo l'unione, così le pagine non si toccano in due.

## Avvisi

- **08/10/2026, 21:45 — Claude.** Le illustrazioni in `static/formazione/illustrazioni-udl/` sono state controllate a vista e corrette (PR #1283, #1285, #1286, #1287, #1291). Prima di aggiungerne o modificarne una: rendila, guardala a 1200 px e, per le versioni `-mobile.svg`, a 720 px; nessun testo sopra un disegno; testo scuro solo su fondo chiaro; `<title>` e `<desc>` che descrivono ciò che si vede; `python3 scripts/check-illustrazioni-udl.py` verde.
- **08/10/2026, 21:45 — Claude.** I pittogrammi ARASAAC si scelgono guardandoli: il primo risultato della ricerca può mostrare tutt'altro (era successo con «scappare», «ospedale», «caldo», «frana»). In `scripts/scarica-pittogrammi.sh` un quarto campo fissa l'identificativo verificato.

## Archiviati

Nessuno.
