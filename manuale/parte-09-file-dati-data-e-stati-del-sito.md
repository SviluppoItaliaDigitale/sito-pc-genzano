_[Indice manuale](README.md)_

# Parte 9 — File dati `data/` e stati del sito

I file nella cartella `data/` pilotano comportamenti dinamici del sito **senza toccare i template**. Questa è la strada preferita per aggiornare card, banner, numeri di emergenza, canali social. Tutti i file sono letti da Hugo a build time: modifiche richiedono un nuovo build per comparire online (automatico al push).

### 9.1 — Panoramica dei file dati

| File | Formato | Scopo |
|---|---|---|
| `emergenza.json` | JSON | Attiva/disattiva modalità emergenza sulla home |
| `allerta.json` | JSON | Livello allerta meteo corrente (verde / giallo / arancione / rossa) |
| `risk_cards.yaml` | YAML | card della pagina Rischi e Prevenzione |
| `numeri_utili.yaml` | YAML | Numeri di emergenza mostrati in home, contatti, footer |
| `quick_links.yaml` | YAML | CTA del hero + "Cosa fare in caso di..." + servizi |
| `social_links.yaml` | YAML | Canali social + linktree |
| `codici_colore.yaml` | YAML | Descrizioni colori allertamento (pagina Allerte Meteo) |
| `glossario.yaml` | YAML | Voci del glossario inline (sigle PC sostituite da popover) |
| `aree_emergenza.yaml` | YAML | 16 punti del Piano Emergenza (10 AA + 2 AS + 4 AR) — coordinate verificate |
| `idranti.yaml` | YAML | Idranti antincendio sul territorio (template, da popolare con dati VVF) |
| `dae.yaml` | YAML | Defibrillatori semi-Automatici Esterni (template, registro IRC ai sensi L. 116/2021) |

Regola d'oro: **prima di creare un nuovo partial o template, verifica se la stessa cosa può essere fatta con un data file**. Questo mantiene il sito manutenibile da chi non conosce Hugo.

### 9.2 — `emergenza.json` (modalità emergenza home)

**Schema completo:**

```json
{
  "attiva": false,
  "tipo": "blu",
  "titolo": "",
  "descrizione": "",
  "link": "",
  "ultimo_aggiornamento": ""
}
```

**Campi:**
- `attiva` *(boolean, obbligatorio)*: `true` attiva la modalità emergenza; `false` la disattiva. Quando è `true` la homepage cambia layout: compare in alto il banner rosso e i numeri di emergenza, l'hero diventa compatto e le notizie scendono più in basso. Vedi `themes/flavour-pcgenzano/layouts/index.html`.
- `tipo` *(string)*: `blu` | `giallo` | `arancione` | `rosso`. Pilota il colore del banner. `rosso` = emergenza massima (terremoto, alluvione in corso, evacuazione). `blu` = informativa istituzionale.
- `titolo` *(string)*: breve, in maiuscoletto o frase istituzionale. Esempi accettabili: "EMERGENZA IN CORSO — RESTATE IN CASA", "EVENTO SISMICO — VERIFICHE IN CORSO".
- `descrizione` *(string)*: una o due frasi brevi. **Niente punto esclamativo**, niente allarmismo gratuito. Indica fonte e azione.
- `link` *(string, opzionale)*: URL a un articolo di dettaglio sul sito o a una pagina istituzionale. Se vuoto, il banner non mostra pulsante.
- `ultimo_aggiornamento` *(string)*: ISO date-time dell'ultimo aggiornamento del banner (compare in piccolo sul banner). Formato consigliato: `2026-04-21T14:30:00+02:00`.

#### Procedura — Attivare la modalità emergenza

1. **Verifica la fonte**: la decisione di attivare la modalità emergenza è del responsabile del Gruppo o del COC, non del redattore. Non attivare mai di propria iniziativa.
2. Apri `data/emergenza.json`.
3. Compila i campi:

   ```json
   {
     "attiva": true,
     "tipo": "arancione",
     "titolo": "ALLERTA METEO ARANCIONE SUI CASTELLI ROMANI",
     "descrizione": "Il Centro Funzionale Regionale prevede piogge intense fino alle 24:00 di mercoledi. Limitare gli spostamenti.",
     "link": "/comunicazioni/2026-04-21-allerta-arancione-castelli/",
     "ultimo_aggiornamento": "2026-04-21T09:15:00+02:00"
   }
   ```

4. Commit: `Attivazione modalità emergenza — allerta arancione`.
5. Push: il sito si aggiorna in 2–3 minuti.
6. **In parallelo**: pubblica l'articolo linkato (vedi Parte 1).

#### Procedura — Disattivare la modalità emergenza

1. Verifica con il responsabile che l'evento sia chiuso.
2. Apri `data/emergenza.json`.
3. Riporta `attiva` a `false`. Svuota gli altri campi (lascia `""` o `"blu"`), per non lasciare residui in repository:

   ```json
   {
     "attiva": false,
     "tipo": "blu",
     "titolo": "",
     "descrizione": "",
     "link": "",
     "ultimo_aggiornamento": ""
   }
   ```

4. Commit: `Chiusura modalità emergenza — allerta rientrata`.
5. Pubblica in parallelo un articolo di aggiornamento operativo ("allerta rientrata, nessuna criticità rilevata").

### 9.3 — `allerta.json` (banner allerta meteo + pre-allerta domani + avvisi meteo + rischio incendi)

Dal 13 maggio 2026 il file `data/allerta.json` è diventato il **bus unico di stato meteo del sito**: raccoglie il livello attuale di criticità idrogeologica, la pre-allerta di domani, gli avvisi di condizioni meteorologiche avverse (vento, neve, calore) e il rischio incendi boschivi (campagna AIB Lazio). Ogni blocco è opzionale e popolato dal workflow `check-allerta.yml` con tre script Python specializzati.

**Schema completo (esempio "tutto attivo"):**

```json
{
  "livello": "gialla",
  "titolo": "ALLERTA GIALLA",
  "descrizione": "Criticità per temporali. Prestare attenzione.",
  "ultimo_aggiornamento": "2026-05-13T05:43:55+02:00",
  "ultimo_controllo": "2026-05-13T05:43:55+02:00",
  "domani": {
    "livello": "gialla",
    "titolo": "Previsto giallo",
    "rischi": ["temporali"],
    "data": "2026-05-14"
  },
  "avviso_meteo": {
    "tipo": "vento",
    "livello": "gialla",
    "descrizione": "Venti da forti a burrasca dai quadranti settentrionali",
    "validita_inizio": "2026-05-13T00:00:00+02:00",
    "validita_fine": "2026-05-14T12:00:00+02:00",
    "url": "https://protezionecivile.regione.lazio.it/.../allertamento_13_05_2026.pdf",
    "fonte_data": "2026-05-12"
  },
  "rischio_incendi": {
    "livello": "gialla",
    "livello_aib": "MEDIO",
    "titolo": "Pericolosità MEDIA",
    "zona_aib": 9,
    "data": "2026-05-13",
    "fonte": "Regione Lazio — Centro Funzionale (modello RISICOLazio + Fondazione CIMA)",
    "domani": {"livello": "gialla", "livello_aib": "MEDIO", "data": "2026-05-14"}
  }
}
```

**Campi del livello principale (criticità idrogeologica/idraulica):**
- `livello` *(string, obbligatorio)*: `verde` | `gialla` | `arancione` | `rossa`. Pilota il colore della barra allerta in cima a ogni pagina.
- `titolo` *(string)*: es. "ALLERTA GIALLA".
- `descrizione` *(string)*: frase sintetica conforme palette messaggi DPC.
- `ultimo_aggiornamento` *(ISO 8601)*: timestamp dell'**ultimo cambio livello**. Suffisso `+02:00` o `+01:00` automatico in base alla data (fuso Europe/Rome dinamico).
- `ultimo_controllo` *(ISO 8601)*: timestamp dell'**ultima verifica**. Cambia ogni volta che il workflow committa.

**Blocco `domani` (pre-allerta criticità idrogeologica):** popolato solo quando il bollettino-domani del DPC ha `data_validita_inizio` **strettamente futura** rispetto a oggi (filtro che evita la falsa pre-allerta tra 00:00 e ~14:00 quando il CSV "domani" copre ancora il giorno corrente). Mostrato in homepage come fascia "Previsto domani: …" solo se `livello ≥ gialla`.

**Blocco `avviso_meteo` (vento, neve, calore, gelate, mareggiate):** popolato dal parser PDF degli "Allertamenti" Regione Lazio quando rileva un avviso di condizioni meteorologiche avverse **non già coperto** dal bollettino di criticità idrogeologica. Frequenza tipica: 1-3 emissioni al mese (a evento). Cessazione automatica quando l'avviso scade. Campo `tipo` può essere composito (es. `"vento, neve"`).

**Blocco `rischio_incendi` (campagna AIB Lazio):** popolato dal parser PDF del "Bollettino di Pericolosità da Incendi Boschivi" durante la campagna giugno-ottobre. Genzano di Roma è in **Zona AIB 9** (confermato dal PDF ufficiale "Tabelle Comuni_Zone Allerta AIB" 2019). Mapping: BASSO→verde (nascosto), MEDIO→gialla, MODERATO→arancione, ELEVATO→rossa. Fuori stagione il blocco non esiste (cessazione automatica quando i PDF AIB non sono più pubblicati).

**Aggiornamento automatico** (architettura doppio trigger fail-safe, 10 maggio 2026):

1. **Trigger primario — cron-job.org ogni 5 min** (free tier, SLA 99.9%): chiama l'API GitHub `workflow_dispatch` con un Personal Access Token fine-grained (permessi Actions: write sul solo `sito-pc-genzano`). **Latenza end-to-end osservata: ~15 secondi** al cambio livello DPC. Setup gestito su [console.cron-job.org](https://console.cron-job.org/).
2. **Trigger fail-safe — GitHub schedule orario** (`cron: '17 * * * *'`, 1 run/h al minuto 17): paracadute minimale se cron-job.org va giù.

A ogni run vengono eseguiti **in sequenza** tre script:

| Script | Cosa fa | Fonte |
|---|---|---|
| `scripts/check-allerta.py` | Criticità idrogeologica + pre-allerta `domani` | CSV opendatasicilia (primaria) → fallback PDF Regione Lazio se entrambi i CSV non rispondono |
| `scripts/check-avvisi-meteo.py` | Avvisi meteo avversi (vento/neve/calore) | Parser PDF pagina `/bollettini/allertamenti` Regione Lazio |
| `scripts/check-rischi-incendi.py` | Rischio incendi AIB Zona 9 | Parser PDF pagina `/bollettini/rischi-incendi` Regione Lazio (solo in campagna AIB) |

Ogni script aggiorna **solo il proprio blocco** in `allerta.json` (anti-spam per blocco). Lo script committa **solo se almeno uno** dei tre ha modificato il file. Messaggio commit combinato:

```
Allerta meteo: livello verde → gialla + avviso meteo: vento gialla + rischio incendi: MODERATO
```

**Anti-flicker JS lato client:** la funzione `checkAllertaDPC()` in homepage rilegge il CSV opendatasicilia ad ogni page-load e ogni 30 minuti. Per evitare lo sfarfallio visivo del banner, il JS sovrascrive titolo/descrizione **solo se il livello calcolato è diverso** da quello già renderizzato server-side. Se i livelli combaciano, il banner resta intatto.

**Fallback PDF Regione Lazio** (attivato solo se opendatasicilia non risponde): lo script `check-allerta.py` scarica il PDF firmato di criticità idrogeologica del giorno corrente (`tbl_bollettini_criticita/bollettino_DD_MM_YYYY.pdf`), parsa con `pdftotext -layout` ed estrae la Zona F (Bacini Costieri Sud = Genzano) per le due sezioni "Valutazioni per OGGI" e "Valutazioni per DOMANI". Output GH Actions estende il campo `source` a `opendatasicilia | pdf-regione-lazio | misto`.

**Timezone Europe/Rome dinamica:** tutti i timestamp di `allerta.json` usano `ZoneInfo("Europe/Rome")` che gestisce automaticamente CEST (+02:00, ora legale) e CET (+01:00, ora solare) senza intervento al cambio del fuso.

Nella maggior parte dei casi **non serve intervenire manualmente**.

> **Storia tecnica (13 maggio 2026)**: la versione iniziale leggeva solo `bollettino-oggi-comuni-latest.csv`, causando un gap di ~14 ore notturne (00:00-14:00) durante il quale il CSV "oggi" era già scaduto e il CSV "domani" non veniva consultato. Il bug si è manifestato il 13/05: l'utente leggeva sul sito "NESSUNA ALLERTA" mentre la Regione Lazio aveva già emesso allerta gialla per temporali per il giorno corrente. Fix: lettura di entrambi i CSV con filtro `data_validita_inizio ≤ now ≤ data_validita_fine` e MAX dei livelli tra i validi.

**Aggiornamento manuale**: serve solo se l'automazione fallisce o se si vuole forzare un messaggio istituzionale specifico. Modifica il file, commit, push. **Nota**: al successivo ciclo il workflow sovrascriverà il tuo intervento col valore letto dalle fonti DPC. Per evitarlo, disabilita temporaneamente il workflow (vedi 10.9).

**Fonti dati ufficiali:**
- Criticità idrogeologica/idraulica (primaria): `https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/refs/heads/main/data/bollettini/bollettino-{oggi,domani}-comuni-latest.csv`
- Criticità idrogeologica (fallback PDF): `https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini/criticita-idrogeologica-idraulica`
- Allertamenti / avvisi meteo: `https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini/allertamenti`
- Rischi incendi AIB: `https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini/rischi-incendi`

### 9.4 — `risk_cards.yaml` (Rischi e Prevenzione)

Contiene le card mostrate nella pagina hub "Rischi e Prevenzione" e nella homepage. Ogni card rimanda a una sottopagina di `content/rischi-prevenzione/`.

**Schema di ogni card:**

```yaml
- id: "rischio-sismico"
  titolo: "Rischio Sismico"
  icona: "bi-tsunami"
  colore: "warning"
  classe_icona: "si-orange"
  descrizione_breve: "Cosa fare prima, durante e dopo un terremoto."
  peso: 1
```

**Campi:**
- `id`: slug della pagina di dettaglio (`/rischi-prevenzione/<id>/`). Deve esistere in `content/rischi-prevenzione/<id>/_index.md` o `<id>.md`.
- `titolo`: titolo card, coerente con l'H1 della pagina di dettaglio.
- `icona`: nome icona Bootstrap Italia (prefisso `bi-`). Vedi [icons.getbootstrap.com](https://icons.getbootstrap.com/).
- `colore`: variante Bootstrap (`primary`, `warning`, `danger`, `info`, `success`, `dark`). Pilota il bordo/sfondo della card.
- `classe_icona`: classe custom per colorare l'icona (`si-orange`, `si-blue`, `si-teal`, `si-green`, `si-dark`). Definite in `custom.css`.
- `descrizione_breve`: una frase max 100 caratteri.
- `peso`: intero, determina l'ordine di visualizzazione (1 = prima, 9 = ultima).

**Modifiche tipiche:**
- Aggiungere una card nuova: aggiungi blocco YAML + crea la pagina di dettaglio in `content/rischi-prevenzione/<id>.md`. Ricorda di aggiornare l'archivio e il menu se serve.
- Togliere una card: rimuovi il blocco + considera di lasciare la pagina di dettaglio come archivio (vedi 8.4 scenario B) o rimuoverla.
- Riordinare: modifica solo i `peso`.

### 9.5 — `numeri_utili.yaml` (numeri di emergenza)

**Regola chiave**: nel Lazio il **solo numero da comunicare al cittadino è il 112** (NUE). 115, 118, 1515 non sono più il riferimento. Qualunque AI che proponga di aggiungerli come "numeri da chiamare" va corretta.

**Struttura:**

```yaml
emergenza:      # Numeri in evidenza massima
  - numero: "112"
    nome: "Numero Unico Emergenza (NUE)"
    descrizione: "..."
    icona: "bi-telephone-fill"
    principale: true

utili:          # Numeri utili secondari
  - numero: "1530"
    nome: "Guardia Costiera"
    ...

locale:         # Numeri del Gruppo (MAI per emergenze)
  - numero: "+39 06 9362600"
    nome: "Segreteria Gruppo PC Genzano"
    ...
    nota: "NON per emergenze"
```

**Campi:**
- `numero`: formato leggibile con spaziature (`112`, `803 555`, `+39 06 9362600`).
- `nome`: ufficiale del servizio.
- `descrizione`: a cosa serve, una frase.
- `icona`: classe Bootstrap Italia.
- `principale`: se `true`, la card è in evidenza grafica maggiore.
- `nota` (opzionale): testo di avviso (tipicamente "NON per emergenze" per i numeri del Gruppo).

### 9.6 — `quick_links.yaml` (CTA hero + servizi)

sezioni distinte:
- `principali`: pulsanti del hero homepage (tipicamente 3).
- `cosa_fare`: card "Cosa fare in caso di..." in homepage.
- `servizi`: card "Servizi per il cittadino".

Campi comuni: `titolo`, `url`, `icona` (Bootstrap Italia icon), `classe` o `classe_icona`, `descrizione`, opzionalmente `azione` (testo sul pulsante).

Regole:
- Ogni URL deve esistere come pagina nel sito (altrimenti il render-link hook mostra testo inerte solo in contenuti markdown, ma in questi partial i link sono generati direttamente: qui un URL inesistente produce un 404 vero).
- Mantieni numero card coerente con il layout (3 principali, 4 cosa_fare, 4 servizi è la configurazione testata).

### 9.7 — `social_links.yaml`

Lista `canali:` + singolo `linktree:`. Campi per canale: `nome`, `url`, `icona`, `classe_btn`, `aria_label`, `descrizione`.

Aggiungere un canale nuovo: aggiungi blocco + verifica che l'icona Bootstrap Italia esista (`bi-whatsapp`, `bi-youtube`, ecc.). Rimuovere un canale: togli il blocco; i partial che usano `range canali` si adattano.

### 9.8 — `codici_colore.yaml`

Pilota la pagina "Allerte Meteo" sezione "Significato dei colori". Ogni livello ha: `livello` (slug), `titolo`, `colore_bg`, `colore_testo`, `significato`, `cosa_fare`, `icona`. I colori sono coordinati con la palette ufficiale del sistema di allertamento nazionale.

**Non modificare** `colore_bg` e `colore_testo` senza ricontrollare il contrasto WCAG (≥ 4.5:1 testo normale).

### 9.9 — Validazione data files

Prima di commit, verifica:

- **JSON** (`emergenza.json`, `allerta.json`): formato valido. Errori di virgola o virgolette rompono il build. Usa un linter o `python3 -m json.tool < data/emergenza.json`.
- **YAML**: indentazione a 2 spazi, niente tab. Stringhe con caratteri speciali tra virgolette doppie. Usa `python3 -c "import yaml; yaml.safe_load(open('data/risk_cards.yaml'))"`.
- **Caratteri accentati**: sempre UTF-8, mai entità HTML (`è`, non `&egrave;`).

Un `data` rotto blocca `hugo --minify` e il deploy fallisce: il sito resta sulla versione precedente e il monitoring Actions mostra un fallimento rosso.

---

_[Indice manuale](README.md)_

[← Parte 08 — Modificare e cancellare contenuti](parte-08-modificare-e-cancellare-contenuti.md) · [↑ Indice](README.md) · [Parte 10 — GitHub Actions e automazioni →](parte-10-github-actions-e-automazioni.md)
