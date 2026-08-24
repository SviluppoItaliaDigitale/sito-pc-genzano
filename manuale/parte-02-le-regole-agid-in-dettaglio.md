_[Indice manuale](README.md)_

# Parte 2 — Le regole AGID in dettaglio

Queste regole derivano dal **Writing Toolkit di Designers Italia**, dal **Manuale operativo
di design della PA** e dalle integrazioni specifiche per la Protezione Civile.

> **Aggiornamento automatico**: le fonti AGID ufficiali sono monitorate dal workflow
> `.github/workflows/aggiorna-manuale.yml` ogni lunedì 06:00 UTC. Quando una fonte cambia
> (Writing Toolkit, Content Toolkit, UI Kit, Linee guida design PA, accessibilità AGID,
> Bootstrap Italia, DPC), il workflow apre automaticamente un'issue con checklist
> tripartita: aggiornare **(A)** questo file e gli altri della cartella `manuale/`,
> **(B)** in coerenza i file `.claude/rules/02-content-design-pa.md`, `.claude/rules/03-accessibility.md`,
> `CLAUDE.md` e gli agent custom letti da Claude Code in ogni sessione, **(C)** build
> Hugo + commit. Manuale e rules Claude devono dire la stessa cosa sulla stessa regola
> AGID, altrimenti il sito ha due fonti di verità divergenti e Claude applica regole
> obsolete in tutte le sessioni successive. Vedi `.claude/rules/02-content-design-pa.md`
> § "Sincronizzazione automatica con gli aggiornamenti AGID" per la procedura completa.

### 2.1 — I cinque principi del Writing Toolkit

1. **Scrivi per chi legge, non per chi ha scritto la norma.** L'utente non conosce il lessico
   interno della PA. Traduci.
2. **Dì prima le cose importanti.** La piramide rovesciata: conclusione in cima, dettagli
   dopo.
3. **Usa parole comuni.** "Casa" non "abitazione". "Paga" non "effettua il pagamento".
4. **Sii specifico.** "Entro il 15 giugno" non "prossimamente". "Piazza Tommaso Frasconi"
   non "nel centro cittadino".
5. **Rendi il testo scorrevole.** Frasi brevi, paragrafi brevi, titoli descrittivi,
   elenchi puntati.

### 2.2 — Lingua e tono

- **Lingua:** italiano corretto, contemporaneo, senza arcaismi ("ad uopo", "giusta delibera",
  "nelle more di").
- **Tono:** istituzionale, sobrio, rassicurante. Mai enfatico, mai minimizzante, mai
  commerciale.
- **Forma personale:** usa "tu" o "voi" quando ti rivolgi al cittadino, se il contesto lo
  permette. Evita "si prega di", "la S.V.", "il gentile utente".
- **Forma impersonale:** accettabile solo in comunicati ufficiali di routine (es. bandi,
  ordinanze).

### 2.3 — Lunghezza di frasi e paragrafi

| Regola | Dettaglio |
|---|---|
| Frase | Sotto le 20 parole (idealmente 12-15). |
| Paragrafo | 2-4 frasi, un concetto. |
| Testo totale | Articolo breve: 150-400 parole. Articolo lungo: 600-1200 parole. Oltre 1500: dividi in più articoli o sposta in pagina. |

**Come verificare la lunghezza media delle frasi** (opzionale):

Conta i punti nel testo, conta le parole, dividi. Se >20 parole/frase in media, accorcia.

### 2.4 — Voce attiva vs voce passiva

| Voce | Esempio | Quando usarla |
|---|---|---|
| Attiva | "**Scarica** il modulo" | Sempre preferita. Soggetto chiaro, verbo diretto. |
| Passiva | "Il modulo **può essere scaricato**" | Solo se il soggetto è irrilevante o sconosciuto. |

**Esercizio:** se puoi inserire "da [qualcuno]" dopo il verbo, è passiva. Trasformala in attiva.

| Passiva (da evitare) | Attiva (preferita) |
|---|---|
| "Il corso è tenuto dai volontari" | "I volontari tengono il corso" |
| "L'emergenza è gestita dal sindaco" | "Il sindaco gestisce l'emergenza" |
| "Il modulo deve essere compilato" | "Compila il modulo" |

### 2.5 — Nominalizzazioni

Le nominalizzazioni trasformano un verbo in sostantivo ("pagare" → "effettuare il pagamento"):
**evitale**.

| Nominalizzazione (evita) | Verbo diretto (usa) |
|---|---|
| "Effettuare il pagamento" | "Pagare" |
| "Procedere all'iscrizione" | "Iscriversi" |
| "Provvedere alla compilazione" | "Compilare" |
| "Dare comunicazione" | "Comunicare" |
| "Fare richiesta" | "Chiedere" |
| "Prendere visione" | "Leggere", "guardare" |

### 2.6 — Parole comuni vs tecnicismi

| Complesso (evita) | Semplice (usa) |
|---|---|
| Abitazione | Casa |
| Automezzo | Auto, furgone |
| Autorizzare | Permettere |
| Documentazione | Documenti |
| Fruire | Usare, avere |
| Inoltrare | Inviare |
| Modalità | Come, modo |
| Nominativo | Nome |
| Presentarsi | Venire, andare |
| Procedere | Fare, andare |
| Recarsi | Andare |
| Terapia | Cura |
| Ulteriore | Altro |

**Tecnicismi necessari:** ammessi se indispensabili, spiegati alla prima occorrenza.

Esempio:

> La trasmissione usa la modalità **NVIS** (Near Vertical Incidence Skywave, propagazione
> quasi verticale delle onde radio), utile per comunicazioni locali senza ripetitori.

### 2.7 — Parole straniere

- **Ammesse** se entrate nell'uso comune (computer, email, online, email, web, chat).
- **In corsivo** se tecniche o poco comuni (*briefing*, *debriefing*, *workshop*).
- **Non declinare** al plurale italiano: "i tablet" non "i tablets", "i file" non "i files".

### 2.8 — Acronimi e sigle

Principio: **evitali se puoi**. Se sono necessari:

1. Prima occorrenza: nome per esteso + acronimo tra parentesi.
2. Da lì in poi: solo l'acronimo.

**Esempio:**

> Il Centro Operativo Comunale (COC) è attivato dal sindaco.
> Il COC coordina le squadre operative sul territorio.

**Sigle senza scioglimento** (ammesse): PA, UE, IVA, SPID, PEC, RC auto.

**Sigle interne** (richiedono scioglimento): DPC (Dipartimento della Protezione Civile),
COC, NUE 112, VVF, CRI, AIB.

### 2.9 — Maiuscole e minuscole

**Regola generale AGID:** uso restrittivo delle maiuscole.

| Categoria | Corretto | Evitare |
|---|---|---|
| Cariche istituzionali | sindaco, assessore, ministro | Sindaco, Assessore, Ministro |
| Eccezioni (tradizione) | Presidente della Repubblica | presidente della Repubblica |
| Ministeri | Ministero della difesa | Ministero della Difesa |
| Dipartimenti | Dipartimento della protezione civile | Dipartimento della Protezione Civile |
| Giorni della settimana | lunedì, martedì | Lunedì, Martedì |
| Mesi | gennaio, febbraio | Gennaio, Febbraio |
| Nomi propri | Regione Lazio | REGIONE LAZIO |
| Nomi di legge | Legge 4/2004, Codice di Protezione Civile | LEGGE 4/2004 |

**Nel dubbio, minuscola.**

### 2.10 — Numeri

| Regola | Esempio |
|---|---|
| Da 1 a 9 nel testo | in lettere ("tre volontari") |
| Da 10 in su | in cifre ("25 volontari") |
| All'inizio di frase | sempre in lettere ("Venti volontari sono arrivati") |
| Grandi numeri | separatore puntuale ("1.200" non "1,200" né "1 200") |
| Separatore decimale | virgola ("2,5 metri") |
| Numeri romani | per leggi e secoli ("Titolo V", "XXI secolo") |

### 2.11 — Date e orari

**Date nel testo (rivolto al cittadino):**

- Esteso: "lunedì 15 maggio 2026"
- Medio: "15 maggio 2026"
- Mese in **minuscolo**.
- Niente "il gg/mm/aaaa".

**Date nei dati tecnici (tabelle, liste):**

- ISO: "2026-05-15"

**Orari:**

- Formato 24 ore: "09:30", "23:45"
- Senza zero iniziale nel parlato: "le 9", "le 23"
- "Dalle 9 alle 12" (niente trattino spaziato: "dalle 9 – alle 12")

### 2.12 — Numeri di telefono

Formato leggibile, a gruppi:

- Fisso italiano: **06 9362 600** o **06 9362600** (non "069362600")
- Cellulare: **+39 333 123 4567**
- Numero unico: **112** (tre cifre, nessun prefisso)

**Nel link `tel:`** (HTML): `tel:+39069362600` (senza spazi, con prefisso internazionale).

### 2.13 — Indirizzi

- Via/Piazza con iniziale maiuscola: "Via Sicilia", "Piazza Tommaso Frasconi"
- Civico con cifra: "Via Sicilia, 13-15"
- CAP e città: "00045 Genzano di Roma (RM)"
- Completo: "Via Sicilia, 13-15 — 00045 Genzano di Roma (RM)"

### 2.14 — Unità di misura

- Ambito tecnico: cifra + simbolo SI con spazio: "3 km", "25 °C", "100 kg"
- Ambito discorsivo: in lettere per quantità piccole: "tre chilometri", "venticinque gradi"
- Simbolo °C (Celsius): niente spazio prima del °, spazio prima della cifra: "25 °C" non
  "25°C" né "25 ° C"

### 2.15 — Link

**Regola d'oro:** il testo del link deve essere **descrittivo anche fuori contesto**.

| Buono | Cattivo |
|---|---|
| "Consulta il [bollettino del Centro Funzionale Regionale Lazio](url)" | "Consulta il bollettino [qui](url)" |
| "Scarica il [modulo di iscrizione (PDF, 120 KB)](url)" | "Scarica il modulo [cliccando qui](url)" |
| "Leggi l'[ordinanza sindacale 42/2026](url)" | "[Leggi di più](url)" |

**Link a documenti:** sempre indicare tipo e dimensione: `(PDF, 120 KB)`, `(DOCX, 50 KB)`.

**Link esterni:** segnalare se aprono nuova finestra (il render hook del sito lo fa automaticamente).

### 2.16 — Grassetto, corsivo, sottolineato

| Formato | Quando |
|---|---|
| **Grassetto** | Parola chiave o frase breve (max una riga) che vuoi risaltare. Mai paragrafi interi. |
| *Corsivo* | Titoli di opere, parole straniere non comuni, termini tecnici alla prima occorrenza, citazioni brevi. |
| Sottolineato | **Mai.** Online indica un link. Usa altri formati. |
| MAIUSCOLO | Mai in testo corrente. Solo sigle ammesse (PA, UE). |

### 2.17 — Elenchi puntati e numerati

**Puntati** (`-` o `*`): quando l'ordine non conta.

- Voci parallele (tutte sostantivi, o tutte azioni, o tutte descrizioni).
- Frasi brevi: niente punto finale se sono frammenti, punto finale se sono frasi complete.
- Almeno voci. Sotto le 3 scrivi un paragrafo.

**Numerati** (`1.`, `2.`): quando l'ordine **conta** (procedure, passaggi, priorità).

**Divieti:**

- Non spezzare una frase continua in un elenco puntato (es. "Il gruppo è composto da: -
  volontari - autisti - responsabili"). Scrivi la frase.
- Niente elenchi a mezza pagina di una-parola.

### 2.18 — Tabelle

- Poche colonne (2-4 massimo su mobile).
- Poco testo per cella (sotto le 15 parole).
- Intestazioni di colonna chiare (prima riga in `**grassetto**`).
- Niente tabelle solo per "impaginare" (usa liste o sezioni).

### 2.19 — Citazioni e riferimenti normativi

**Citazioni testuali:** blockquote Markdown (`>`):

```markdown
> «Grazie all'acquisto e la consegna dei nuovi defibrillatori la Regione Lazio porta
> a compimento l'importante percorso avviato per rafforzare le competenze dei nostri
> volontari in materia di primo soccorso.»
>
> — *Pasquale Ciacciarelli, Assessore alla Protezione Civile della Regione Lazio*
```

**Riferimenti normativi:**

- **Spiega il contenuto** della norma in linguaggio semplice.
- Non citare articoli/commi nel corpo ("art. 20 comma 2...").
- Linka sempre a Normattiva o Gazzetta Ufficiale.

Esempio:

> La legge 4/2004 (Legge Stanca) stabilisce che i siti della pubblica amministrazione
> devono essere accessibili a tutte le persone, comprese quelle con disabilità.

Non:

> Ai sensi dell'art. 3, comma 1, lettera c) della Legge 9 gennaio 2004, n. 4 e ss.mm.ii.,
> in combinato disposto con il D.Lgs. 106/2018...

**Quadro normativo aggiornato (verifica 24/08/2026).** Il portale AGID sull'accessibilità è stato ristrutturato (nuovo URL `agid.gov.it/it/ambiti-intervento/accessibilita-usabilita`, il vecchio `/it/design-servizi/accessibilita` reindirizza). Il riferimento resta la **Legge Stanca (L. 4/2004)** + **D.Lgs. 106/2018** per la dichiarazione di accessibilità dei siti PA — da compilare/aggiornare **entro il 23 settembre** di ogni anno, con **obiettivi di accessibilità** pubblicati **entro il 31 marzo**, sempre tramite `form.agid.gov.it`. AGID è anche Autorità di vigilanza sull'accessibilità digitale ai sensi del **D.Lgs. 82/2022** (recepimento dell'European Accessibility Act, Direttiva UE 2019/882): riguarda soprattutto operatori privati di grandi dimensioni, non introduce nuovi obblighi per la dichiarazione del nostro sito.

### 2.20 — Linguaggio inclusivo

- Evita il maschile "neutro" quando puoi: "le persone" > "gli uomini"; "chi si iscrive" >
  "l'iscritto".
- Niente asterischi, schwa (ə) o altre sperimentazioni grafiche: non accessibili agli
  screen reader e non previsti dalle linee guida AGID.
- Se devi nominare esplicitamente entrambi i generi, alterna o usa forme ellittiche:
  "volontari e volontarie", "chi è interessato".

### 2.21 — Accessibilità cognitiva

- **Titoli e sottotitoli** che descrivono il contenuto della sezione.
- **Prima le informazioni importanti**, poi i dettagli.
- **Feedback comprensibili** senza esperienza tecnica.
- **Consistenza**: usa sempre gli stessi nomi per le stesse cose (es. "squadra operativa"
  sempre, non alternato con "team operativo" o "gruppo operativo").

### 2.22 — Regole specifiche Protezione Civile

| Regola | Dettaglio |
|---|---|
| Allerte meteo | Solo dati del Centro Funzionale Regionale Lazio. Fonte sempre citata. |
| Codici colore | Verde, gialla, arancione, rossa. Non usare "massima allerta" per fenomeni ordinari. |
| Previsto vs in corso | "È previsto" (futuro) vs "è in corso" (presente). Non confondere. |
| Allerta vs emergenza | Allerta = preavviso, emergenza = evento in atto. |
| Numeri | Nel Lazio il cittadino chiama **solo il 112** (NUE). Altri riferimenti: 803 555 (Sala Operativa PC Lazio), 1530 (Guardia Costiera). |
| Tono | Calmo, informativo, rassicurante. Mai allarmistico. Mai minimizzante. |
| Autoprotezione | Per i comportamenti, cita sempre fonti ufficiali (DPC, Regione, Comune). |

### 2.23 — Livello qualitativo atteso quando rivedi un articolo (qualità ChatGPT 9.5/10)

Quando rileggi un articolo prima della pubblicazione (tuo o di Claude Code) il livello atteso è quello di un Caporedattore PA con 18 anni di esperienza: la stessa cura del migliore strumento esterno di riferimento (test del 9 maggio 2026: ChatGPT 9.5/10).

Vale per **tutti i contesti** in cui Claude Code lavora: CLI desktop sul PC, app mobile, sessione cloud, agent GitHub-integrato. Nessuno dei tre delega ad AI esterne — l'utente ha chiesto esplicitamente che la stessa qualità sia raggiunta in tutte le sessioni.

**Cosa significa nella pratica:**

| Aspetto | Livello atteso |
|---|---|
| Lede (primo paragrafo) | Concreto, non retorico. "La Festa della Mamma è una buona occasione per mettere ordine nelle cose pratiche di casa" sì, "è un'occasione per pensare alla cura delle persone a cui vogliamo bene" no. |
| Frasi >20 parole | Spezzate sistematicamente in 2-3 frasi più corte. |
| Nominalizzazioni | Sostituite con verbi attivi. "Effettuare il pagamento" → "pagare". "Procedere alla compilazione" → "compilare". |
| Voce passiva | Ridotta dove ne aumenta solo la formalità senza aiutare la chiarezza. |
| Burocratese | Eliminato anche se presente nel testo originale. "Ad uopo", "giusta delibera", "nelle more di", "si prega di", "la S.V." sono fuori. |
| Fonti istituzionali | Ogni claim tecnico ha fonte verificabile (DPC, CFR Lazio, ISPRA, INGV, ASL Roma 6, MIM, IFRC, WHO, …). |
| Linkografia interna | Sempre verificata e valorizzata prima delle fonti esterne. Sezione "Per approfondire" strutturata in due blocchi: *Sul nostro sito* + *Fonti istituzionali*. |
| Bullet uniformi | In una stessa lista tutti i bullet iniziano con la stessa parte del discorso (verbi all'imperativo, oppure sostantivi). |
| H2 senza enfasi | Niente `**bold**` dentro l'H2, niente emoji decorative. L'H2 è già visivamente forte. |
| `image:` del frontmatter | **Mai modificato durante una revisione testuale.** Pre-commit check `git diff <file> \| grep -E '^[+-]image' \| head -5` obbligatorio. |
| Esito legittimo "nessuna modifica" | Quando un articolo è già conforme AGID, dichiararlo esplicitamente. Inventare modifiche per dimostrare attività è un anti-pattern. |

**Workflow di revisione su singolo articolo:**

1. Leggi il file integralmente.
2. Identifica 0-15 problemi reali (non inventati).
3. Applica `Edit` puntuali con razionale AGID per ogni modifica.
4. **Pre-commit check obbligatorio**: `git diff <file> | grep -E '^[+-]image' | head -5` — se trovi diff su `image:` non richiesto, ripristina (anti-pattern banner intoccabile).
5. Mostra il diff con tabella delle modifiche e dichiara cosa hai *lasciato intatto* e perché.
6. Commit + push solo dopo conferma utente o se è già stato autorizzato un batch.

**Per batch di revisione ≥5 articoli**: applicare il checkpoint pre-batch (`.claude/rules/07-proattivita-coerenza.md`), ottenere conferma esplicita, lavorare in serie con commit a tappe (≈30-50 articoli per commit) per mantenere la cronologia git navigabile.

### 2.24 — Umanizzazione della scrittura (prosa naturale, senza tic da IA)

Regola introdotta il 19 agosto 2026, speculare a `.claude/rules/02-content-design-pa.md` § "Umanizzazione della scrittura" (regola di coerenza manuale ↔ rules: i due file dicono la stessa cosa). Fonti: la pagina [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) del WikiProject AI Cleanup, che cataloga i pattern statistici ricorrenti nei testi prodotti dai modelli linguistici, e le linee guida di prompting di Anthropic (istruzioni positive + esempi rappresentativi dello stile desiderato).

**Subordinazione ad AGID.** Questa regola è un livello di rifinitura *sotto* le regole AGID di questa Parte 2, mai una deroga. Se un consiglio stilistico confligge con una regola AGID, WCAG o di comunicazione del rischio, vince la regola. Restano ferme in particolare: frasi sotto le ~20 parole (§ 2.3), bullet uniformi con punto fermo (§ 2.17), struttura fissa delle pagine rischio, struttura a 6 punti dei post di crisi.

**Obiettivo**: prosa editoriale italiana concreta e specifica, con ritmo naturale entro il registro breve. Non è una direttiva "inganna gli AI detector" (strumenti inaffidabili, come avverte la stessa pagina Wikipedia): è una direttiva di qualità.

**I 10 tic da evitare:**

1. Copule semplici, non perifrasi: «è», non «rappresenta / costituisce / si configura come / funge da / si pone come / vanta» in serie.
2. Niente grappoli di lessico da IA: «cruciale», «fondamentale», «significativo», «panorama», «testimonianza», «dinamico», «un ruolo chiave»… Il segnale è la **densità** (3+ nello stesso testo), non la singola parola.
3. Non attribuire importanza a tutto: niente «momento fondamentale» / «svolta significativa» / «a testimonianza di» su fatti ordinari. Il fatto si racconta con nomi, date, luoghi, numeri.
4. Niente pseudoanalisi decorative al gerundio: «evidenziando così…», «sottolineando l'importanza…», «contribuendo a…», «riflettendo un più ampio…». Se l'analisi serve, ha una fonte; altrimenti si taglia.
5. Niente consenso inventato: «secondo molti esperti», «gli osservatori ritengono», «ampiamente riconosciuto» solo con fonte reale citata (principio NO INVENZIONI).
6. Parallelismi negativi col contagocce: «non solo X, ma anche Y» / «non è X, è Y» al massimo una volta per articolo, e solo se il contrasto è reale.
7. Spezzare la regola del tre: niente terne automatiche di aggettivi («chiaro, efficace e accessibile»). Si elencano le cose che servono: due, quattro, una.
8. Niente conclusioni prefabbricate: «in conclusione», «in sintesi», «guardando al futuro», «nonostante le sfide» come chiusa automatica. Un articolo può finire sul suo ultimo fatto utile.
9. Struttura al servizio del contenuto: non ogni articolo è una mini-presentazione con intro + 3 sezioni + elenco + considerazioni finali. H2, liste, grassetti ed emoji solo con funzione (la struttura fissa delle pagine rischio non si tocca).
10. Niente frasi da assistente virtuale nel contenuto: «Ecco una panoramica…», «Speriamo sia utile», «Non esitate a…».

**Le due regole positive:** (a) variare il ritmo entro il registro breve — frasi brevissime alternate a frasi medie, mai sequenze di periodi identici; (b) privilegiare il concreto — il dettaglio specifico e pertinente (la via, il modello del mezzo, l'orario reale) è ciò che rende il testo credibile e che la prosa generica «leviga via».

**Italiano impeccabile, sempre.** Umanizzare non autorizza sciatterie: grammatica, ortografia, punteggiatura e accenti restano perfetti. In caso di dubbio fa fede la Treccani (in subordine l'Accademia della Crusca). Spell-check `scripts/check-refusi.py` obbligatorio sui file toccati.

**Eccezioni:** versioni facili `-facile.md` (le frasi corte e ripetitive lì sono intenzionali), pagine rischio e contenuti operativi di emergenza, registri di genere su richiesta esplicita, testi legali/tecnici.

**In revisione**: metodo conservativo del § 2.23 — solo i tic reali, giudizio caso per caso (un «diritto fondamentale» non è un tic), mai sostituzioni cieche via `sed`, mai toccare `image:`. Il check è integrato nel gate `pc-article-reviewer` (checklist § 10) e, per le AI esterne, in `AGENTS.md` § "Umanizzazione della scrittura".

---

_[Indice manuale](README.md)_

[← Parte 01 — Scrivere un articolo passo per passo](parte-01-scrivere-un-articolo-passo-per-passo.md) · [↑ Indice](README.md) · [Parte 03 — Immagini per gli articoli →](parte-03-immagini-per-gli-articoli.md)
