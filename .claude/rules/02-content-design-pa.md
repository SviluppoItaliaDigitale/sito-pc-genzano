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
4. Ogni foto deve comunque avere la **fascia blu istituzionale** (vedi regola sopra). Per trattare in modo uniforme le foto fornite dall'utente, usa lo script `scripts/applica-fascia-foto.sh`:
   ```bash
   bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-ext>
   ```
   Ridimensiona a 1200 px, sovrappone logo + testo istituzionale, esporta WebP qualità 85 (ricompresso a 75 se >200 KB) in `static/images/<nome>.webp`. Evita passaggi manuali in Canva/GIMP. Dettagli in `MANUALE-SITO.md` Parte 3.8, Metodo 4.
5. Lo shortcode produce `<figure>`/`<figcaption>` accessibili, immagine cliccabile per ingrandire (apre in nuova scheda), `aria-label` descrittivo, `loading="lazy"`. La tipografia `.article-body` v7.2 (`custom.css`) applica automaticamente cornice con ombra morbida e didascalia in corsivo blu — non serve CSS inline.

6. **Posizionamento di foto multiple in articoli storici** (convenzione adottata aprile 2026 dopo arricchimento di 35 foto su 30+ articoli memoria/anniversario):
   - **1ª foto**: dopo il **1° H2** dell'articolo, dopo il primo paragrafo di contenuto.
   - **2ª foto**: dopo il **2° H2**, per aprire una seconda dimensione narrativa (ricostruzione, contesto, conseguenze).
   - **3ª foto e oltre**: una per ogni H2 di **evento storico specifico citato** (es. articoli che raccontano sequenze di terremoti — Irpinia 1980, L'Aquila 2009, Centro Italia 2016).
   - **Mai foto a casaccio**: ogni foto va legata tematicamente alla sezione che la precede.
   - **Quando aggiungere foto multiple**: l'articolo deve avere ≥5 H2, raccontare eventi storici specifici, e le foto candidate devono avere valore narrativo (luoghi, persone, mappe, satellite — non bandiere o stemmi). Non per articoli di servizio quotidiano o dottrinali.
   - **Filtro automatico bandiere/stemmi comunali**: lo script `scripts/foto-da-wikipedia.sh` scarta i risultati con pattern `*Bandiera.svg`, `Flag_of_*`, `*-Stemma.svg`, `*Coat_of_arms*`, `*Stemma_di_*` (exit code `4`). Se capita, provare un titolo più specifico (un monumento, una piazza, una veduta).

Specifiche complete in `MANUALE-SITO.md` Parte 14.9. Questa regola nasce dopo un incidente in cui una foto fornita dall'utente era stata sostituita dalla sola copertina automatica — comportamento non accettabile.

### Divieto: foto stock generiche ripetute per macro-tema

**Mai** generare batch di foto inline che assegnano la **stessa foto stock** (Pexels/Pixabay/Unsplash) a gruppi di articoli accomunati solo da un macro-tema (es. "tutti gli articoli sul volontariato" → stessa foto di volontari generici, "tutti gli articoli sul calore" → stessa foto di sole). Mai usare query generiche tipo `"italian civil defense"`, `"volunteers"`, `"heat wave"` per popolare automaticamente decine di articoli: le API stock restituiscono sempre la stessa prima immagine, e il sito si riempie di foto duplicate non pertinenti.

**Why:** ad aprile 2026 un batch automatico ha aggiunto 289 foto inline a 278 articoli usando solo 43 immagini distinte (74 articoli avevano la stessa foto della Croce Rossa con la stessa caption *"Il sistema italiano di Protezione Civile in azione"*). Ripetizione massiccia di foto stock generiche danneggia l'autorità istituzionale del sito e contraddice il principio AGID di sobrietà ("no foto è meglio di foto sbagliata"). I 14 commit batch sono stati ripuliti.

**How to apply:**
- Foto inline `{{< foto >}}` solo se realmente pertinente al **singolo** articolo, mai per macro-tema.
- Fonti accettabili per la foto inline: foto fornita dall'utente, foto Wikipedia/NASA/USGS/NOAA con query specifica all'evento o al soggetto dell'articolo (es. `"Terremoto dell'Aquila 2009"`, non `"earthquake italy"`), foto stock **solo** se l'articolo lo richiede in modo non sostituibile e con query specifica al contenuto.
- **Mai** scrivere script o workflow che iterano su un elenco di articoli e cercano una foto stock con la stessa query categoriale.
- Caption e alt text vanno scritti **per ogni singola foto**, mai riusati su più articoli.
- Se un articolo non ha una foto evidente da inserire, lasciarlo senza foto inline: la sola cover tipografica con titolo è sufficiente.

### Foto utente — banner pulito (sito) vs carosello (social)

Le foto fornite dall'utente **non vanno mai nel banner/copertina** del sito (campo `image:` del frontmatter). Il banner deve restare pulito col solo titolo dell'articolo e il page-hero blu istituzionale: è una scelta di design istituzionale che non si tocca.

**Regola sito (web):**
- `image:` resta `""` o viene popolato solo dalla **cover tipografica** automatica (gradiente blu + titolo, generata dal workflow `auto-cover-mancanti.py`) oppure dalle **foto da fonti ufficiali** (Wikipedia/NASA/USGS via marker `# TODO-foto-*`).
- Le foto utente vanno **tutte dentro il corpo articolo** come `{{< foto >}}`:
  - 1 foto → punto narrativamente sensato (dopo l'apertura o sotto un H2 pertinente).
  - 2-3 foto → 1ª dopo 1° H2, 2ª dopo 2° H2, ecc. (convenzione articoli storici).
  - **≥4 foto → galleria/carosello dentro l'articolo** (CSS scoped, immagini cliccabili, riga responsive o slider accessibile).

**Regola social (Instagram/Facebook/X/Telegram):**
- Stesse foto che stanno nel corpo articolo diventano automaticamente **carosello Instagram**: lo script `genera-immagini-social.py` rileva i blocchi `{{< foto src="..." >}}` nel body e li combina con la cover tipografica (max 10 immagini). Story sempre 1 sola.
- **Niente da configurare**: stessa fonte (foto nel corpo), due usi distinti.

**Riassunto pratico:** quando l'utente dice "ecco una foto" o "queste foto", `image:` resta vuoto, le foto vanno tutte nel corpo, e i social pescano da lì in automatico al prossimo workflow.

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

**Caso A — un solo articolo nella giornata** (default, ~85% dei casi)
Usa il formato semplice `AAAA-MM-GG` (esempio: `date: 2026-04-06`). Hugo lo interpreta automaticamente come mezzanotte ora italiana grazie alla `timeZone = "Europe/Rome"` configurata in `hugo.toml`.

**Caso B — due o più articoli nella stessa giornata**
Usa il formato ISO 8601 con orario crescente per ogni articolo, in ordine di pubblicazione (ultimo scritto = orario maggiore = finisce in cima all'archivio).

```yaml
# 1° articolo del giorno:
date: 2026-04-30T00:01:00+02:00

# 2° articolo (ultimo scritto, in cima):
date: 2026-04-30T00:02:00+02:00
```

**Perché orari minimi (00:01, 00:02, …) e non semantici (08:00, 14:00, 18:00):**
L'orario non viene mai mostrato all'utente (il template formatta solo la data lunga "30 aprile 2026"). Serve esclusivamente come tie-break per l'ordering Hugo `Date desc`. Orari minimi garantiscono che gli articoli del **giorno corrente** non risultino "futuri" per Hugo (cosa che li escluderebbe dal build fino al rebuild successivo del workflow `pubblica-programmata.yml`, alle 06:00 UTC).

**Perché esiste questa regola:**
Ad aprile 2026 si è scoperto che Hugo, con due articoli a `date: AAAA-MM-GG` identico, applica come tie-break l'ordine alfabetico del filename, non l'ordine di pubblicazione: 47 giornate del sito avevano articoli renderizzati in ordine arbitrario rispetto a quando erano stati scritti. Aggiungere orario crescente risolve.

**Cosa NON usare:**
- `date: 2026-04-06T03:32:00Z` (timezone UTC esplicita in fondo): comportamento meno chiaro, rischio di "articolo futuro" se l'utente è in Europa pre-tz-fix. Usa sempre `+02:00` (italiana).
- `date: "2026-04-06"` (con virgolette): tecnicamente accettato da Hugo ma sconsigliato per coerenza con tutti gli articoli del sito.

**Workflow operativo per l'utente:**
- Quando scrivi un articolo nuovo con `hugo new comunicazioni/AAAA-MM-GG-titolo.md`, l'archetype produce `date: {{ .Date }}` che si espande automaticamente al timestamp completo. Va bene per il caso B.
- Per il caso A (singolo articolo giorno) lo riduci a `date: AAAA-MM-GG` semplice.
- Se ti accorgi a posteriori di aver pubblicato 2 articoli nello stesso giorno con `date` solo-data, lancia `python3 scripts/fix-ordering-articoli-stesso-giorno.py` (idempotente, riassegna orari `00:01, 00:02, ...` basati su git first-commit asc).

## Regole editoriali

- Nessun contenuto ambiguo o non verificato.
- Nessun testo "che sembra giusto": deve essere realmente pubblicabile.
- Correggi i testi proposti dall'utente in modo conservativo, senza tradirne il significato.
- Verifica sempre ortografia, grammatica, punteggiatura e accenti.
- Se il testo originale non rispetta queste regole, riscrivilo prima di proporre pubblicazione.

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
| Informazione | `#0284c7` | Azzurro — notizia di servizio |
| Prevenzione | `#15803d` | Verde — contenuti di auto-protezione |
| Esercitazione | `#ea580c` | Arancione — addestramento operativo |
| Aggiornamento | `#4338ca` | Indaco — stato avanzamento |
| Formazione | `#7c3aed` | Viola — corsi e didattica |
| Volontariato | `#b45309` | Ambra scuro — reclutamento e attività volontari |
| Attività | `#0891b2` | Turchese — operatività ordinaria |

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
