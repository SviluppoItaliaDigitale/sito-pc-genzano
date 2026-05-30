# Content Design PA

## Principi di scrittura

Scrivi sempre in italiano corretto, chiaro, sobrio e leggibile.
Evita burocratese, slogan vuoti, frasi troppo lunghe e tecnicismi inutili.
Scrivi pensando a cittadini reali: famiglie, anziani, volontari, scuole, persone fragili, utenti da mobile.
Ogni testo deve aiutare l'utente a capire cosa sta leggendo, cosa deve fare e dove trovare altre informazioni.

## Regole di struttura

- Titoli chiari e informativi (descrivono il contenuto, non lo pubblicizzano).
- Sottotitoli utili all'orientamento.
- Liste solo quando servono davvero, non per frammentare testo continuo.
- Call to action chiare, istituzionali, mai pressanti.
- Evita ripetizioni inutili tra titolo, occhiello e primo paragrafo.
- Mantieni coerenza tra titoli pagina, menu, breadcrumb e corpo del testo.

## Regole lessicali

- Voce attiva preferita alla passiva.
- Frasi brevi: tendenzialmente sotto le 20 parole.
- Usa "tu" o "voi" quando ti rivolgi direttamente al cittadino, se il contesto lo permette.
- Evita nominalizzazioni inutili ("effettuare il pagamento" → "pagare").
- Usa parole comuni al posto di tecnicismi quando possibile.
- Numeri di telefono: scrivi sempre in formato leggibile (es. 06 1234 5678).
- Date: scrivi in formato esteso quando rivolto ai cittadini (es. "martedì 6 aprile 2026"), usa AAAA-MM-GG solo nel frontmatter Hugo.

## Regola Quality Label ESC — logo + codice E10435833 sempre insieme

🔴 **Vincolo cogente UE** (Regolamento UE 2021/888 — European Solidarity Corps Visual Identity Guidelines): il **logo Quality Label** dell'European Solidarity Corps **deve essere sempre mostrato accompagnato dal codice di accreditamento dell'organizzazione**. Mai logo nudo, mai codice nudo, mai disgiunti.

- **Codice del Gruppo:** `E10435833`
- **Logo ufficiale:** `/images/quality-label-esc.png` (PNG, 400×400, fondo bianco)
- **Versione hi-res stampa:** `/images/logo-esc-quality-label-it.png` (4016×4016)
- **Loghi affiliazione del Gruppo = 2**: Quality Label ESC + SNPC Volontariato (`/images/logo-snpc-volontariato.png`). Il logo PC Genzano è la firma istituzionale, **non si conta come affiliazione**.

**Esposizione già attiva** (non duplicare):
- Footer site-wide (`themes/flavour-pcgenzano/layouts/partials/footer.html` + `static/app-shared/site-chrome.js`)
- Pagina `/chi-siamo/` § "Affiliazioni e riconoscimenti europei"
- Carosello social Instagram (slide finale "Affiliazioni" via `crea_slide_affiliazioni()` in `genera-immagini-social.py`)
- Schede stampabili A4 (banda piè pagina in `print.css` via `.scheda::after` + immagine `footer-print-affiliazioni.png`)
- Deck di presentazione (slide dedicata in `genera-presentazione.py`)

**Quando crei una nuova grafica/slide che ha un blocco affiliazioni**, ricontrolla sempre questi 3 punti:
1. Il logo ESC è accompagnato dal codice `E10435833` ben leggibile? → se no, non è conforme al Reg. UE 2021/888.
2. Hai aggiunto il logo PC Genzano tra gli "affiliati"? → se sì, sbagliato: rimuovilo, non è un'affiliazione esterna.
3. Hai aggiunto i 3 loghi al banner cover di un articolo? → se sì, sbagliato: il banner resta col solo titolo (vedi CLAUDE.md § "Affiliazioni e riconoscimenti europei").

### Composizione standard di ogni nuova grafica = ESATTAMENTE 4 LOGHI, MAI DOPPIONI

🔴 **Vincolo cogente: max 4 loghi totali per grafica, mai doppioni.** Vale per **tutte le grafiche istituzionali del Gruppo** prodotte in proprio o con strumenti esterni: cover articolo, slide social (carosello/post/storia), schede A4 stampabili (kit calamità, casi studio), locandine, deck di presentazione, infografiche, manifesti.

| # | Logo | Dove | File |
|---|---|---|---|
| 1 | **PC Genzano** (firma del Gruppo) | header/banner/intestazione | `/images/logo-pc-genzano.webp` (o `.png`/`-hires.png`) |
| 2 | **Quality Label ESC + codice `E10435833`** | footer/blocco affiliazioni | `/images/quality-label-esc.png` (web) o `/images/logo-esc-quality-label-it.png` (hi-res stampa) |
| 3 | **Coordinamento FE.PI.VOL.** | footer/blocco affiliazioni | `/images/logo-fepivol.png` |
| 4 | **SNPC Volontariato** | footer/blocco affiliazioni | `/images/logo-snpc-volontariato.png` |

**Regole di composizione, vietato deviare:**

- La **firma (1) è separata** dalle affiliazioni (2-4): mai mescolare PC Genzano tra le card affiliazione (sarebbe doppione — è già la firma istituzionale visibile come header/banner).
- **Mai inserire lo stesso logo due volte** nella stessa grafica (es. PC Genzano nell'header E ancora in una card affiliazione = doppione, vietato).
- **Mai inserire un 5° logo** nelle grafiche del Gruppo (es. PC Lazio, Comune di Genzano, Croce Rossa, ANPAS, VVF, INGV, ecc.). Quei loghi sono di **enti coordinatori/operatori del Sistema Nazionale di PC** e vanno citati nei **contenuti testuali** o nel **footer site-wide del sito** (chrome del portale), MAI dentro la grafica istituzionale del Gruppo.
- **Vincolo cogente Quality Label:** il logo ESC va SEMPRE con il codice `E10435833` accanto, mai disgiunti (Reg. UE 2021/888). Le altre 3 affiliazioni non hanno codici obbligatori.

**Vale anche per grafiche realizzate con AI esterne** (ChatGPT, Gemini, Midjourney, Canva, Adobe Express, DALL-E, Stable Diffusion, ecc.): quando dai un brief a un'AI esterna per generare una locandina/infografica/banner/post per il Gruppo, includi sempre nel prompt la regola **"esattamente 4 loghi, mai doppioni"** + fornisci i 4 file ufficiali del repo. Esempio di pattern brief da incollare in coda al prompt AI:

> *Vincolo loghi (cogente): la grafica deve riportare ESATTAMENTE 4 loghi (1) PC Genzano in alto come firma; (2) Quality Label ESC + codice E10435833 accanto, (3) Coordinamento FE.PI.VOL., (4) SNPC Volontariato nel footer come blocco affiliazioni. Mai doppioni. Mai 5° logo. Mai logo ESC senza codice E10435833. File ufficiali: \[allegare i 4 PNG dal repo\].*

Vedi `CONTESTO-AI.md` / `CONTESTO-AI-slim.md` per il prompt completo da incollare alle AI esterne (rigenera con `bash scripts/export-contesto-ai.sh` dopo qualsiasi modifica a CLAUDE.md o `.claude/rules/`).

**Why:** richiesta utente del 27 maggio 2026 + verifica retroattiva che footer Hugo + site-chrome.js già hanno il blocco dal 18 maggio. La regola codifica il vincolo legale UE per impedire grafiche future che mostrino il logo Quality Label senza codice (sarebbero non conformi al Reg. UE 2021/888).

## Regola immagini — fascia blu istituzionale

Ogni immagine di copertina degli articoli DEVE avere una fascia blu in basso con:
- Sfondo: `#003366` (--pc-primary), opacità 85-90%, altezza ~15-18% dell'immagine
- Logo: `logo-pc-genzano.png` a sinistra (~75px di altezza)
- Riga 1: "PROTEZIONE CIVILE" — bianco, bold, ~30px
- Riga 2: "Gruppo Comunale Volontari — Genzano di Roma" — bianco, regular, ~15px
- Formato: WebP, 1200px di larghezza, max 200 KB
- Nome file: `AAAA-MM-GG-descrizione-breve.webp` in `static/images/`
- Alt text: sempre significativo, mai "Immagine di..."

Riferimento visivo: `static/images/zamberletti-protezione-civile-genzano.webp`
Specifiche complete: `MANUALE-SITO.md`, Parte 3.

## Regola foto evento — quando l'utente fornisce foto reali

**Quando l'utente fornisce foto** di un intervento, esercitazione, attività o evento, vale la **regola rigida**:

1. **TUTTE** le foto fornite vanno **inserite nel corpo dell'articolo** (mai sostituite dalla sola copertina).
2. Ogni foto deve essere inserita con lo shortcode `{{< foto >}}` — mai con markdown `![...]()` diretto:
   ```go-html-template
   {{< foto src="/images/AAAA-MM-GG-descrizione-specifica.webp"
            alt="Descrizione significativa per screen reader"
            caption="Didascalia opzionale." >}}
   ```
3. Il **nome del file foto** deve essere **diverso dallo slug dell'articolo** (es. `2026-04-20-incendio-cecchina-casolare.webp`), così lo script `genera-cover.py` non sovrascrive la foto reale con una copertina tipografica.
4. Ogni foto deve avere la **fascia blu istituzionale** (regola sopra). Usa lo script `scripts/applica-fascia-foto.sh`:
   ```bash
   bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-ext>
   ```
   Ridimensiona a 1200 px, sovrappone logo + testo, esporta WebP qualità 85 (ricompresso a 75 se >200 KB) in `static/images/<nome>.webp`. Niente passaggi manuali Canva/GIMP. Dettagli in `MANUALE-SITO.md` Parte 3.8, Metodo 4.
5. Lo shortcode produce `<figure>`/`<figcaption>` accessibili, immagine cliccabile (apre in nuova scheda), `aria-label` descrittivo, `loading="lazy"`. La tipografia `.article-body` v7.2 (`custom.css`) applica cornice con ombra morbida e didascalia in corsivo blu — niente CSS inline.

6. **Posizionamento di foto multiple in articoli storici** (convenzione aprile 2026):
   - **1ª foto**: dopo il **1° H2**, dopo il primo paragrafo di contenuto.
   - **2ª foto**: dopo il **2° H2** (seconda dimensione narrativa: ricostruzione, contesto, conseguenze).
   - **3ª foto e oltre**: una per ogni H2 di **evento storico specifico citato** (es. Irpinia 1980, L'Aquila 2009, Centro Italia 2016).
   - **Mai foto a casaccio**: ogni foto legata tematicamente alla sezione che la precede.
   - **Quando**: articolo con ≥5 H2, eventi storici specifici, foto con valore narrativo (luoghi, persone, mappe, satellite — non bandiere/stemmi). Non per servizio quotidiano o articoli dottrinali.
   - **Filtro bandiere/stemmi**: `scripts/foto-da-wikipedia.sh` scarta i pattern `*Bandiera.svg`, `Flag_of_*`, `*-Stemma.svg`, `*Coat_of_arms*`, `*Stemma_di_*` (exit code `4`). Provare un titolo più specifico (monumento, piazza, veduta).

7. **Idempotenza della fascia blu (no doppia fascia)** — incident 16 maggio 2026 "Giro d'Italia Formia":
   - **Mai applicare la fascia su una foto che ce l'ha già** (risultato: 2 bande blu sovrapposte con lo stesso testo).
   - `scripts/applica-fascia-foto.py` da **v2 (16 maggio 2026) è idempotente**: rileva fasce esistenti (sample pixel a 98% h centro fascia + 80% h zona foto, confronto `#003366 ± 30`) e va in **skip**. Output `[skip] La foto ha già una fascia...`.
   - **Override** con `--force` (solo casi edge, mai automatico). Un `--force` passato senza richiesta utente è un bug.
   - **Pattern "foto aggiunte dopo la pubblicazione"** (workflow legittimo ricorrente): backup in `/tmp/`, applica fascia via script, rigenera carosello IG via `genera-immagini-social.py --force`. Vedi `manuale/parte-03-immagini-per-gli-articoli.md` § "Aggiungere foto dopo la pubblicazione" e agent `pc-image-fixer.md`.

Specifiche complete in `MANUALE-SITO.md` Parte 14.9. Questa regola nasce dopo un incidente in cui una foto fornita dall'utente era stata sostituita dalla sola copertina automatica — comportamento non accettabile.

### Divieto: foto stock generiche ripetute per macro-tema

**Mai** generare batch di foto inline che assegnano la **stessa foto stock** (Pexels/Pixabay/Unsplash) a gruppi di articoli accomunati solo da un macro-tema (es. "tutti gli articoli sul volontariato" → stessa foto di volontari generici, "tutti gli articoli sul calore" → stessa foto di sole). Mai usare query generiche tipo `"italian civil defense"`, `"volunteers"`, `"heat wave"` per popolare automaticamente decine di articoli: le API stock restituiscono sempre la stessa prima immagine, e il sito si riempie di foto duplicate non pertinenti.

**Why:** ad aprile 2026 un batch ha aggiunto 289 foto inline a 278 articoli con solo 43 immagini distinte (74 articoli con la stessa foto Croce Rossa e la stessa caption *"Il sistema italiano di Protezione Civile in azione"*). Danneggia l'autorità del sito e contraddice la sobrietà AGID ("no foto è meglio di foto sbagliata"). I 14 commit batch sono stati ripuliti.

**How to apply:**
- Foto inline `{{< foto >}}` solo se pertinente al **singolo** articolo, mai per macro-tema.
- Fonti accettabili: foto utente; Wikipedia/NASA/USGS/NOAA con query specifica all'evento/soggetto (es. `"Terremoto dell'Aquila 2009"`, non `"earthquake italy"`); foto stock **solo** se non sostituibile e con query specifica.
- **Mai** script/workflow che iterano su una lista cercando una foto stock con la stessa query categoriale.
- Caption e alt **per ogni singola foto**, mai riusati.
- Se non c'è una foto evidente, lasciare l'articolo senza foto inline: la cover tipografica col titolo basta.

### Foto utente — banner pulito (sito) vs carosello (social)

Le foto utente **non vanno mai nel banner/copertina** del sito (campo `image:`). Il banner resta pulito col solo titolo + page-hero blu istituzionale: scelta di design che non si tocca.

**Regola sito (web):**
- `image:` resta `""` o viene popolato solo dalla **cover tipografica** automatica (gradiente blu + titolo, da `auto-cover-mancanti.py`). MAI da foto utente/Wikipedia/NASA/USGS — quelle vanno **sempre inline** come `{{< foto >}}`. Il marker `# TODO-foto-*` è bandito (CLAUDE.md punto 9).
- Foto utente **tutte nel corpo** come `{{< foto >}}`: 1 foto → punto narrativamente sensato; 2-3 foto → 1ª dopo 1° H2, 2ª dopo 2° H2; **≥4 foto → galleria/carosello inline** (CSS scoped, immagini cliccabili, riga responsive o slider accessibile).

**Regola social (Instagram/Facebook/X/Telegram):** le stesse foto del corpo diventano automaticamente **carosello Instagram** — `genera-immagini-social.py` rileva i blocchi `{{< foto src="..." >}}` e li combina con la cover (max 10 immagini). Story sempre 1 sola. Niente da configurare.

**Riassunto:** quando l'utente dice "ecco una foto", `image:` resta vuoto, le foto vanno tutte nel corpo, i social pescano da lì al prossimo workflow.

**🔴 ANTI-PATTERN — modifica del campo `image:` durante una revisione testuale.** Quando il task è *"rivedi questo articolo"*, *"riscrivi secondo AGID"*, *"correggi i refusi"*, *"miglioralo"* o simile, **il campo `image:` non deve cambiare** rispetto al valore originale. Anche se trovi una foto pertinente su Wikimedia/NASA/altro, la foto va inline nel corpo come `{{< foto >}}`, non nel banner. **Check pre-commit obbligatorio:**

```bash
git diff <file.md> | grep -E '^[+-]image' | head -5
```

Se il diff contiene righe `+image:` / `-image:` (anche solo `image_alt:`) e l'utente non ha richiesto esplicitamente un cambio di copertina, **stop**: ripristina il valore originale prima del commit.

**Why:** il 9 maggio 2026 ChatGPT-cloud, in revisione AGID dell'articolo "Giornata Europa — Meccanismo UCPM", ha sostituito `image: ""` con una foto reale Wikimedia ERCC. Il banner è andato live con la foto invece della cover tipografica col titolo — identità visiva rotta fino al fix manuale.

## Nomi dei nostri mezzi, attrezzature e dotazioni — verifica dalla fonte canonica

🔴 **Regola cogente** quando un articolo cita un **mezzo, un'attrezzatura o una dotazione in uso al Gruppo Comunale** (autocarro, autobotte, modulo AIB, fuoristrada, tenda sociale, generatore, radio, DPI, attrezzature manuali): **prima di scrivere il nome, verifica la denominazione tecnica ufficiale in `content/chi-siamo/_index.md` § "I nostri mezzi"** (sezione card con `<i class="bi bi-truck">`).

**Why:** la scritta sulla **livrea** è quasi sempre una **classificazione di sistema** del Servizio Nazionale/Regionale di PC (es. *"Regione Lazio - Protezione Civile - Colonna Mobile - Volontariato"*), **non** il modello tecnico. Confonderli produce un articolo tecnicamente sbagliato anche se "letterale" rispetto alla foto.

**Incident 26 maggio 2026 — visita scout AGESCI:** la foto davanti a un mezzo con scritta *"Colonna Mobile - Volontariato"* è andata live citando *"l'autocarro Colonna Mobile della Regione Lazio"*. Il modello reale è il **Mercedes Actros — autobotte antincendio da 14.000 litri** (`content/chi-siamo/_index.md` riga 105). Fix a posteriori (caption + corpo H2 + `social_punti`), ma il primo deploy era live col nome sbagliato.

**Procedura pre-articolo:**

1. Prima di nominare un mezzo, fai:
   ```bash
   grep -in "<nome-presunto>\|autocarro\|autobotte\|modulo\|fuoristrada" content/chi-siamo/_index.md
   ```
2. Se non compare, allarga:
   ```bash
   grep -iE "actros|atego|cabstar|vm90|nissan|iveco|mercedes|tenda" content/chi-siamo/_index.md
   ```
3. Usa il **modello tecnico** come identificazione primaria (*"Mercedes Actros"*, *"Iveco VM90"*, *"Nissan Cabstar"*) + funzione (autobotte 14.000 l, fuoristrada 4×4 con modulo 800 l, piattaforma aerea).
4. Le scritte sulla livrea si possono citare nell'`alt` (descrivono il visibile, WCAG 1.1.1) ma **non sostituiscono il nome tecnico** nel corpo, caption e `social_punti`.

**Estensione:** stessa logica per ogni dotazione (radio, generatori, DPI, attrezzature AIB, kit, tende). Se `/chi-siamo/` non basta, controlla `data/dotazioni_*.yaml` (se esistono), articoli passati con badge `Attività`/`Esercitazione` sullo stesso mezzo, e `/area-volontari/`.

## Regola pittogrammi — supporto comprensione (bambini, anziani, L2)

Il sito ha una libreria di **Pittogrammi standardizzati** (46 ISO 7010 + 125 ARASAAC) in `static/pittogrammi/` per supportare la comprensione del testo a bambini, anziani, persone con disabilità cognitive e parlanti italiano L2 (regola di accessibilità cognitiva).

Si usano con lo shortcode `pittogramma`:

```go-html-template
{{< pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto" >}}
```

Per uso inline dentro una frase: `inline="true"`. Per dimensione: `size="small|medium|large|xlarge"` (default: medium).

**Regole d'uso editoriale:**
1. Il pittogramma è **supporto** alla comprensione, mai sostituto del testo (WCAG 1.4.5).
2. Un pittogramma per concetto chiave, non come decorazione visiva continua.
3. Per segnali di sicurezza formali (obblighi, divieti, avvertimenti): preferire **ISO 7010**.
4. Per situazioni narrative/didattiche per bambini: preferire **ARASAAC**.
5. **`alt` sempre descrittivo**, mai stringa vuota o "Immagine di...". Esempio: `alt="Persona che si nasconde sotto al tavolo in caso di terremoto"`.

**Attribuzioni — obbligatorie:**
- Pagina `/attribuzioni-pittogrammi/` linkata dal footer di tutte le pagine.
- ARASAAC è CC BY-NC-SA 4.0: ogni opera derivata (in particolare le **schede stampabili PDF** dei kit didattici) che include pittogrammi ARASAAC eredita la stessa licenza CC BY-NC-SA 4.0. Indica esplicitamente la licenza nel piè di pagina della scheda.

Specifiche complete in `MANUALE-SITO.md` Parte 3.16.

## Regola critica — formato data nel frontmatter Hugo

Lo schema dipende da quanti articoli condividono la giornata.

**Caso A — un solo articolo nella giornata** (default, ~85% dei casi): formato semplice `AAAA-MM-GG` (es. `date: 2026-04-06`). Hugo lo interpreta come mezzanotte ora italiana (`timeZone = "Europe/Rome"` in `hugo.toml`).

**Caso B — due o più articoli nella stessa giornata**: formato ISO 8601 con orario crescente per ordine di pubblicazione (ultimo scritto = orario maggiore = in cima all'archivio).

```yaml
# 1° articolo del giorno:
date: 2026-04-30T00:01:00+02:00

# 2° articolo (ultimo scritto, in cima):
date: 2026-04-30T00:02:00+02:00
```

**Perché orari minimi (00:01, 00:02…) e non semantici:** l'orario non è mai mostrato (il template formatta solo "30 aprile 2026"), serve solo come tie-break per l'ordering `Date desc`. Orari minimi evitano che gli articoli del **giorno corrente** risultino "futuri" per Hugo (esclusi dal build fino al rebuild di `pubblica-programmata.yml`, 06:00 UTC).

**Perché la regola esiste:** ad aprile 2026 si è scoperto che con due articoli a `date: AAAA-MM-GG` identico Hugo usa come tie-break l'ordine alfabetico del filename, non quello di pubblicazione: 47 giornate avevano articoli in ordine arbitrario. L'orario crescente risolve.

**Cosa NON usare:** `date: ...Z` (UTC esplicita: rischio "articolo futuro", usa sempre `+02:00`); `date: "2026-04-06"` (con virgolette: accettato ma sconsigliato per coerenza).

**Workflow operativo:** `hugo new comunicazioni/AAAA-MM-GG-titolo.md` produce `date: {{ .Date }}` → timestamp completo (va bene per il caso B); per il caso A riducilo a `AAAA-MM-GG`. Se ti accorgi a posteriori di 2 articoli stesso giorno con `date` solo-data, lancia `python3 scripts/fix-ordering-articoli-stesso-giorno.py` (idempotente, riassegna `00:01, 00:02, ...` da git first-commit asc).

## Regole editoriali

- Nessun contenuto ambiguo o non verificato.
- Nessun testo "che sembra giusto": deve essere realmente pubblicabile.
- Correggi i testi proposti dall'utente in modo conservativo, senza tradirne il significato.
- Verifica sempre ortografia, grammatica, punteggiatura e accenti.
- Se il testo originale non rispetta queste regole, riscrivilo prima di proporre pubblicazione.

## Programmi di eventi — disclaimer obbligatorio "fai riferimento al sito ufficiale"

🔴 **Ogni articolo che riporta il programma, il calendario o gli orari di un evento organizzato da un ente terzo** (Comune di Genzano di Roma, Comune di Marino, parrocchie, associazioni, ecc.) **DEVE includere un disclaimer** che:

1. invita a fare **sempre riferimento al sito ufficiale dell'ente organizzatore** per eventuali variazioni al programma;
2. chiarisce che il Gruppo riporta il programma **a titolo informativo** e **non risponde di modifiche** decise dall'organizzazione.

**Formato** (callout blockquote, posizionato vicino al programma/calendario):

```markdown
> ⚠️ **Per eventuali variazioni fai sempre riferimento al [sito ufficiale del Comune di <organizzatore>](URL).** Il Gruppo riporta il programma a titolo informativo e **non risponde di modifiche** decise dall'organizzazione.
```

**Il riferimento è il sito dell'ente che ORGANIZZA l'evento**: Comune di Genzano (`https://www.comune.genzanodiroma.roma.it/`) per gli eventi di Genzano, Comune di Marino (`https://www.comune.marino.rm.it/`) per quelli di Marino, ecc. Non il nostro sito.

**Why:** i programmi degli eventi cambiano spesso fino all'ultimo momento e non sono sotto il controllo del Gruppo. Il Gruppo non deve assumersi responsabilità per cambi che non gestisce. Richiesto dall'utente il 22/05/2026 dopo l'integrazione dei programmi delle Infiorate. Vale anche quando il programma è "in aggiornamento" sul sito dell'ente.

## Sincronizzazione automatica con gli aggiornamenti AGID

Le linee guida AGID/Designers Italia si aggiornano nel tempo. Il workflow `.github/workflows/aggiorna-manuale.yml` (lunedì 06:00 UTC) monitora le 10 fonti ufficiali (Linee guida design PA, Designers Italia + Writing/Content Toolkit + UI Kit, Bootstrap Italia, Accessibilità AGID, Dichiarazione accessibilità, DPC) via hash SHA-256 (BeautifulSoup).

Quando una fonte cambia, apre un'issue (label `manuale + documentazione + revisione`) con checklist a 3 sezioni: **(A)** aggiornare il manuale operativo (`manuale/parte-02`, `03`, `11`, `12`, `MANUALE-SITO.md`); **(B)** aggiornare in coerenza `.claude/rules/`, `CLAUDE.md` e gli agent `pc-article-reviewer`/`pc-social-publisher`/`pc-deploy-validator`; **(C)** verifica finale (build, grep date, chiusura issue).

**Regola di coerenza obbligatoria**: il manuale operativo (rivolto all'utente) e le rules `.claude/` (lette dall'AI in tutte le sessioni: CLI desktop, mobile, cloud) devono dire **la stessa cosa** sulla stessa regola AGID. Se aggiorni l'uno senza l'altro, il sito ha due fonti di verità divergenti e Claude continua ad applicare regole obsolete in tutte le sessioni successive.

**Why**: punto sollevato dall'utente il 9 maggio 2026 — la regola "Claude redige come ChatGPT 9.5/10" non sopravvive se, quando AGID si aggiorna, le rules restano alla baseline iniziale. Questa sezione documenta il vincolo di applicazione speculare.

**How to apply** quando trovi un'issue del workflow:
1. Apri ogni URL e identifica le novità.
2. Aggiorna **simultaneamente** il manuale (`manuale/`) e le rules (`02`, `03`, `CLAUDE.md` punti 2-4, agent rilevanti).
3. Se introduce un nuovo principio, citalo come fonte ufficiale in entrambi i posti.
4. `grep -rn "<data-modifica>" manuale/ .claude/rules/ CLAUDE.md` per verificare la sincronia.
5. Build Hugo pulito + commit "Aggiornamento AGID DD/MM/AAAA — manuale + rules Claude in sincronia" + push.
6. Chiudi l'issue citando il commit.

## Livello qualitativo della redazione — qualità ChatGPT 9.5/10

**Vale per ogni contesto Claude Code** (CLI desktop, mobile, cloud, agent GitHub): **nessuno delega ad AI esterne** la redazione/revisione, tutti applicano integralmente AGID con la cura del miglior strumento di riferimento (test 9 maggio 2026: ChatGPT 9.5/10, vedi `feedback_workflow_ai_esterne_validato.md`).

**Cosa significa in revisione:**

1. **Lettura UX writer**: ogni paragrafo "il cittadino lo capisce in 30 secondi?". Frasi >20 parole spezzate, nominalizzazioni → verbi attivi, passive ridotte.
2. **Lede concreto, non retorico**: il primo paragrafo dice cosa l'articolo fa per l'utente, niente formule generiche ("è un'occasione per pensare a...").
3. **Fonti istituzionali sempre citate**: ogni claim tecnico (numeri, codici colore, regole) ha fonte verificabile (DPC, CFR Lazio, ISPRA, INGV, ASL Roma 6, MIM). Niente "secondo gli esperti".
4. **Linkografia interna valorizzata**: prima delle fonti esterne, verifica se il sito ha già contenuti pertinenti (kit-calamita, schede, articoli correlati, glossario, ISO). Pattern `[Sul nostro sito:] / [Fonti istituzionali:]`.
5. **Bullet uniformi**: in una lista tutti i bullet iniziano con la stessa parte del discorso (tutti imperativi, o tutti sostantivi).
6. **H2 senza enfasi ridondante**: niente `**bold**` o "🔥 ATTENZIONE 🔥" nell'H2 (è già forte).
7. **Punto fermo a fine bullet** (Designers Italia): frase compiuta = punto fermo; bullet di una parola = nessun punto.
8. **Distinzione `Allerta`/`Emergenza`/`Aggiornamento`** sempre rispettata (vedi `06-protezione-civile-scientifica.md`).
9. **Niente burocratese residuo**: "ad uopo", "giusta delibera", "nelle more di", "si prega di", "la S.V." — eliminare anche se presenti nel testo originale dell'utente.

**Workflow di revisione su singolo articolo:**

```
1. Read del file.
2. Lettura come UX writer: identifica 0-15 problemi reali (non inventati).
3. Edit puntuali con razionale AGID per ogni modifica.
4. Pre-commit check OBBLIGATORIO: git diff <file> | grep -E '^[+-]image' | head -5
   → se trovi diff su `image:` non richiesto, ripristina (anti-pattern banner).
5. Mostra diff all'utente con tabella delle modifiche e cosa hai LASCIATO INTATTO e perché.
6. Commit + push solo dopo conferma o se l'utente ha già autorizzato un batch.
```

**Quando un articolo non ha modifiche**, dichiara *"Articolo conforme AGID, nessuna modifica necessaria"* — esito legittimo. Inventare modifiche per dimostrare attività è anti-pattern.

**Per batch ≥5 articoli**: applica il checkpoint pre-batch (`07-proattivita-coerenza.md`), conferma esplicita, commit a tappe (≈30-50 articoli per commit).

### Auto-gate AGID prima del commit (sintesi operativa)

La regola completa è in `CLAUDE.md` § "Auto-gate AGID prima del commit di un nuovo articolo". Sintesi:

1. **Quando generi un articolo nuovo** in `content/comunicazioni/`, **prima del `git add`** invochi `pc-article-reviewer` su quel file.
2. Solo dopo il via libera dell'agent (o dopo aver applicato i suoi fix) procedi al commit.
3. Il gate è **obbligato**, non opzionale. Vale anche su singolo articolo.

**Eccezione — registro non-AGID solo su richiesta esplicita dell'utente.** Se l'utente chiede un registro diverso (comunicato stampa, lettera istituzionale, paper, relazione tecnica, memoria, bando, delibera, ordinanza, scheda accademica, **o altro genere esplicito**), sospendi il gate per quel documento e applica le **convenzioni di genere** (piramide rovesciata + 5W per il comunicato; intestazione + protocollo per la lettera; IMRaD per il paper; ecc.). Vale solo per quel documento; il prossimo articolo ricade nel gate standard. **L'eccezione la decide l'utente, non tu.**

## Frontmatter obbligatorio per gli articoli (comunicazioni/)

Ogni articolo deve avere tutti i campi previsti dall'archetipo:
- `title`: titolo chiaro e informativo
- `date`: formato AAAA-MM-GG
- `description`: breve sommario (massimo 160 caratteri, utile anche per SEO)
- `badge`: Allerta | Avviso | Comunicazione | Attività | Formazione | Evento | Volontariato | Radiocomunicazioni | Prevenzione | Esercitazione | Aggiornamento | Informazione | Emergenza (categorie nuove ricevono colore automatico da palette in `themes/flavour-pcgenzano/layouts/partials/badge.html`)

**Palette ufficiale delle categorie** (contrasto WCAG AA ≥ 4.5:1 su bianco):

| Categoria | Hex | Note |
|---|---|---|
| Allerta | `#d9364f` | Rosso allerta — richiede attenzione immediata |
| Emergenza | `#7f1d1d` | Rosso scuro — evento in corso di gravità massima |
| Avviso | `#b45309` | Ambra scuro — segnalazione operativa non urgente |
| Evento | `#c026d3` | Magenta — iniziativa pubblica |
| Comunicazione | `#003366` | Blu istituzionale — informazione ordinaria |
| Radiocomunicazioni | `#0369a1` | Blu radio — attività HF/VHF/UHF |
| Informazione | `#075985` | Blu petrolio — notizia di servizio (WCAG AA 7.56:1) |
| Prevenzione | `#15803d` | Verde — contenuti di auto-protezione |
| Esercitazione | `#c2410c` | Arancione bruciato — addestramento operativo (WCAG AA 5.18:1) |
| Aggiornamento | `#4338ca` | Indaco — stato avanzamento |
| Formazione | `#7c3aed` | Viola — corsi e didattica |
| Volontariato | `#b45309` | Ambra scuro — reclutamento e attività volontari |
| Attività | `#0e7490` | Turchese scuro — operatività ordinaria (WCAG AA 5.36:1) |

Queste tinte sono applicate in `custom.css` in due gruppi coordinati: le classi `.notizia-categoria.<categoria>` (badge nelle card) e i selettori `.filter-pill[data-filter="<categoria>"]` (pulsanti filtro nell'archivio). Qualsiasi modifica alla palette va replicata in **entrambi** i gruppi per mantenere la coerenza visiva.

**Criterio d'uso `Allerta` vs `Emergenza`:** i due badge non sono sinonimi e hanno colori distinti perché coprono fasi diverse del ciclo del rischio (previsione vs evento in corso). I criteri operativi e gli esempi sono definiti in `.claude/rules/06-protezione-civile-scientifica.md`, sezione "Quando usare il badge 'Allerta' e quando 'Emergenza'". Non scegliere tra i due per varietà editoriale: il badge `Emergenza` è intenzionalmente raro.
- `priorita`: normale | urgente
- `autore`: "Gruppo Comunale Volontari PC Genzano" (default)
- `image`: percorso immagine o stringa vuota
- `scadenza`: data di scadenza o stringa vuota
- `area`: zona geografica o stringa vuota
- `allegati`: lista di PDF o array vuoto `[]`. Ogni voce è un oggetto con `titolo`, `url` e `dimensione` opzionale ma raccomandata (WCAG 3.3.5 Help):
  ```yaml
  allegati:
    - titolo: "Ordinanza sindacale"
      url: "/documenti/ordinanza.pdf"
      dimensione: "120 KB"
  ```
- `draft`: false (per articoli pubblicati)

## Comunicazione di crisi sui social — struttura standard

Per i post di **allerta** o **emergenza** sui canali social istituzionali (Instagram, Facebook, X, Telegram), il messaggio deve avere — **in quest'ordine** — tutti i sei elementi della struttura ISO 22329 + CWA CEN/CENELEC:

1. **Tipo di evento** (allerta meteo, vento forte, temporali, evacuazione, ecc.) — concreto, non vago.
2. **Livello e codice colore** (giallo/arancione/rosso) — solo dal Centro Funzionale Regionale Lazio, mai inventato.
3. **Area geografica + finestra temporale** in chiaro.
4. **Cosa fare** — 2-3 azioni di autoprotezione, voce attiva, frasi brevi.
5. **Fonte ufficiale** con link verificabile (CFR, DPC, Comune).
6. **Prossimo aggiornamento**: quando e su quale canale.

Mai mescolare allerta, prevenzione e attività ordinaria nello stesso post in fase di rischio in corso.

### Hashtag — policy del Gruppo

- Uno per evento, **specifico e localizzato**, coerente fra tutti i canali.
- Stabili: `#PCGenzano`, `#Genzano`, `#AllertaLazio`, `#NUE112`.
- Mai hashtag virali, ironici, politici o generici svuotati (`#italia`, `#news`).
- Per evento specifico in corso: hashtag dedicato univoco, coordinato con Comune e Regione (es. `#AllagamentiGenzano2026`), mai più varianti per lo stesso evento.

### Disinformazione — risposta

- **Mai amplificare per smentire**: non condividere il post falso (nemmeno in critica). Niente screenshot leggibili.
- Risposta breve **citando la fonte ufficiale** (CFR, DPC, Comune). Senza polemica, senza nominare l'autore della fake news.
- La **fonte unica di verità** è il sito istituzionale: ogni post social rilevante linka un articolo del sito.

Le specifiche complete sono in `MANUALE-SITO.md` Parte 13.7. La pagina pubblica `/social-media-policy/` espone questi principi al cittadino.

## Frontmatter per le pagine legali / istituzionali

Le pagine `content/privacy/_index.md`, `content/note-legali/_index.md`, `content/accessibilita/_index.md` e `content/social-media-policy/_index.md` devono avere il campo:

- **`dataUltimaRevisione: "AAAA-MM-GG"`** — data dell'ultima revisione sostanziale della pagina.

Il template `themes/flavour-pcgenzano/layouts/_default/single.html` mostra questo valore come box evidente (`<div class="alert alert-light">`) in cima al contenuto con il testo "Pagina rivista il …". Il partial `page-tools.html` disattiva la `.Lastmod` automatica se il campo è presente, per evitare date duplicate o in conflitto.

**Regole operative:**
- Aggiorna `dataUltimaRevisione` ogni volta che modifichi contenuto sostanziale (non refusi o link morti).
- Non scrivere date di revisione nel corpo del testo (stringhe tipo "Marzo 2026", "Ultimo aggiornamento: …"): il riferimento è unico e nel frontmatter.
- Il workflow `audit-sito.yml` (sezione 32) verifica settimanalmente che le 4 pagine legali abbiano il campo `dataUltimaRevisione` impostato in formato `AAAA-MM-GG`.

## Coerenza kit didattici ↔ schede stampabili

I kit didattici per le scuole (`content/formazione/kit-scuola-{infanzia,primaria,secondaria-primo-grado,secondaria-secondo-grado}.md`) devono **tutti** rimandare alle schede stampabili della loro fascia in `static/formazione/schede-stampabili/`. La regola è simmetrica: ogni scheda fisica deve essere linkata almeno una volta dal kit del proprio livello.

**Convenzione di naming delle schede stampabili:**

| Kit | Suffisso scheda |
|---|---|
| Infanzia | `-infanzia` (es. `tartaruga-saggia-infanzia`, `colorare-terremoto-infanzia`) o nome generico (`labirinto-uscita`, `chiamo-112`) |
| Primaria | `-primaria` (es. `cruciverba-primaria`, `piano-familiare-primaria`) o generico |
| Secondaria 1° grado | `-secondaria` (es. `decodifica-bollettino-secondaria`, `mappa-rischi-secondaria`) |
| Secondaria 2° grado | `-secondaria2` (es. `caso-amatrice-secondaria2`, `traccia-esame-secondaria2`) |

**Cosa deve avere ogni kit:** un blocco "Schede già pronte per la stampa" che elenca con bullet point e link diretto **tutte** le schede del proprio livello, prima della sezione "Compito di realtà" o "Schede fotocopiabili".

**Verifica rapida:**
```bash
for f in content/formazione/kit-scuola-*.md; do
  echo "$(basename "$f"): $(grep -oE 'schede-stampabili/[a-z0-9-]+' "$f" | sort -u | wc -l) schede linkate"
done
```

Ogni kit deve linkarne almeno tante quante ne contiene la cartella per il suo livello. Un kit con zero link verso le schede del proprio livello è un bug — è successo una volta a entrambi i kit secondaria, scoperto solo quando un docente ha segnalato che non trovava le schede dal proprio kit.

## Versione "italiano semplice" (A2 CEFR) — file affiancato

Da maggio 2026 (Punto 16 roadmap) gli articoli possono avere una **versione semplificata** in italiano L2 A2 CEFR, per parlanti L2, disabilità cognitive, anziani con poca scuola, chi legge in fretta. Guida completa: `manuale/parte-25-italiano-l2-versione-facile.md`.

**Convenzione di naming:**

```
content/comunicazioni/<slug>.md          ← versione completa AGID
content/comunicazioni/<slug>-facile.md   ← versione italiano L2 A2
```

**Frontmatter incrociato:**
- Versione completa: `versione_facile: "<slug>-facile"`
- Versione facile: `versione_facile_di: "<slug>"` + **`build: { list: never, render: always, publishResources: true }` OBBLIGATORIO**

Hugo renderizza entrambi come pagine distinte. Il partial `partials/versione-facile-toggle.html` aggiunge un banner giallo in cima a ciascuna pagina che linka all'altra.

🔴 **VINCOLO HIDE DALLE LISTE.** Ogni file `<slug>-facile.md` DEVE includere nel frontmatter:

```yaml
build:
  list: never              # esclude da Site.RegularPages, Site.AllPages,
                           # quindi da homepage, archivio, RSS, sitemap,
                           # podcast list, articoli correlati, index.json
  render: always           # ma resta renderizzata come pagina HTML
  publishResources: true   # gli asset Page Resources sono pubblicati
```

⚠️ **CRITICO**: la chiave del frontmatter è `build:` (senza underscore). La vecchia sintassi `_build:` (con underscore) è stata **rimossa** da Hugo 0.145.0 e causa **ERROR error building site** su Hugo 0.161+, bloccando completamente il deploy. Storia: 12 maggio 2026 le PR #186/#187/#188/#190 hanno introdotto `_build:` per errore, causando 3 deploy falliti consecutivi prima del fix in PR #191.

Senza questa config la versione facile compare in homepage, `/comunicazioni/`, `/podcast/`, RSS, sitemap, index.json e correlati — due card quasi identiche. Con `build.list: never` è raggiungibile **solo** dal bottone "Leggi in italiano semplice" sull'articolo madre.

**Storia:** regola aggiunta il 12 maggio 2026 dopo che la prima P16 fece comparire la versione facile in homepage come doppia "ultima notizia" (fix PR #186/#187/#188). Specifiche: `manuale/parte-25 § 25.11`.

**Eccezione gate AGID obbligata.** La versione facile NON segue il linguaggio AGID standard. Usa le **regole CEFR A2**:
- frasi corte (8-12 parole massimo),
- lessico delle 2000 parole più frequenti dell'italiano,
- verbi al presente indicativo,
- sigle spiegate la prima volta (es. "il 112, il numero unico europeo"),
- numeri in cifre, mai in lettere,
- niente subordinate concatenate, niente metafore, niente retorica.

Formalizzazione del registro non-AGID già coperto da `CLAUDE.md § "Auto-gate AGID"` come eccezione. **Non invocare `pc-article-reviewer` sui file `<slug>-facile.md`** (rigetterebbe frasi "troppo corte"): il review va fatto secondo i criteri CEFR A2, non AGID.

**Workflow on-demand** (per articolo): Parte 25 § 25.6. Non automatico, scelta editoriale per contenuti ad alta priorità (bollettini allerta, autoprotezione, numeri emergenza, articoli normativi densi).

**Articolo campione live**: `content/comunicazioni/2026-05-12-iso-22324-codici-colore-allerta-facile.md` (associato alla versione completa `2026-05-12-iso-22324-codici-colore-allerta.md`).
