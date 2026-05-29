# Proposta di architettura — Livello dottrinale «Conoscere la Protezione Civile»

> **Documento di lavoro, non pubblicato.** Vive in `.claude/planning/`, fuori da `content/`: Hugo non lo costruisce e non finisce mai online. Prodotto nella sessione di Fase 0 (discovery), branch `claude/pc-doctrinal-discovery-phase0-U192V`. **Non contiene contenuto di sito**: è un progetto da approvare prima di costruire.
>
> Data: 29 maggio 2026 · Stato: **in attesa di approvazione delle decisioni del §C**.

---

## Premessa onesta: NON siamo a un punto zero

Il brief è scritto come una Fase 0 a campo libero, ma git racconta una storia diversa, e la riporto subito perché cambia tutto il resto del documento.

**Il livello «Conoscere la Protezione Civile» esiste già ed è live su `main`.** È stato costruito e mergiato con la PR **#418 — «Conoscere la Protezione Civile (Onda 1)»**. Le sessioni non condividono memoria: l'unica persistenza è git, e git dice che l'Onda 1 è stata fatta, verificata sulle fonti primarie, e pubblicata.

Quindi questa Fase 0 **non progetta da zero**: fotografa cosa c'è, lo riconosce come **base di qualità di riferimento**, e progetta la costruzione del **resto** (Onde 2 e successive). Alcune decisioni che il brief mi chiede di sottoporti (slug radice, etichetta, struttura sulle quattro fasi) **sono già state prese dall'Onda 1**: te le ripropongo non come scelte aperte ma come «confermi o revisioni?», con la storia di come sono state decise.

---

## A. Sintesi della discovery

### A.1 — Cosa ha già consegnato l'Onda 1 (live su `main`)

Sezione `content/conoscere/`, 9 pagine pubblicate + 2 file di lavoro non pubblicati:

| URL | File | Stato |
|---|---|---|
| `/conoscere/` | `_index.md` | ✅ Landing: cos'è il livello, indice fasi, backlog dichiarato |
| `/conoscere/le-quattro-fasi/` | `le-quattro-fasi/_index.md` | ✅ Panoramica + modello del rischio **R = P × V × E** |
| `…/previsione/` | `le-quattro-fasi/previsione.md` | ✅ Fase 1 |
| `…/prevenzione/` | `le-quattro-fasi/prevenzione.md` | ✅ Fase 2 |
| `…/soccorso/` | `le-quattro-fasi/soccorso.md` | ✅ Fase 3 (catena COC→COM→CCS→DiComaC, in sintesi) |
| `…/superamento/` | `le-quattro-fasi/superamento.md` | ✅ Fase 4 (stato emergenza art. 24, AeDES, Sendai) |
| `/conoscere/servizio-nazionale/` | `servizio-nazionale.md` | ✅ Componenti (art. 4), strutture operative (art. 13), Comuni e Sindaco (art. 12) |
| `/conoscere/telecomunicazioni-emergenza/` | `telecomunicazioni-emergenza/_index.md` | ✅ **Differenziatore #1**: reti radio, radioamatori, IT-alert |
| `…/rete-zamberletti/` | `telecomunicazioni-emergenza/rete-zamberletti.md` | ✅ Frequenze verificate (riuso dell'articolo già pubblicato) |
| `/conoscere/rischio-vulcanico-colli-albani/` | `rischio-vulcanico-colli-albani.md` | ✅ **Differenziatore #2**: Vulcano Laziale, fonti INGV+DPC (completata, `render:never` rimosso) |
| — | `_FONTI-DA-VERIFICARE.md` | 🔒 file di lavoro (`build: render: never`) — checklist verifica fonti |
| — | `_PR-DESCRIPTION.md` | 🔒 file di lavoro (`build: render: never`) — bozza descrizione PR |

**Verifica fattuale dell'Onda 1: già completata e tracciata.** `_FONTI-DA-VERIFICARE.md` documenta che ogni numero d'articolo è stato controllato verbatim su Normattiva (attività di PC = **art. 2**, non art. 11; componenti art. 4; eventi a/b/c art. 7; Comuni/Sindaco art. 12; strutture operative art. 13; stato di emergenza art. 24 con durata max 12+12 mesi; ordinanze art. 25), e che **3 URL DPC inizialmente errati (404) sono stati corretti e ri-verificati 200**. Questo è il livello di rigore già stabilito: è il pavimento, non il soffitto.

### A.2 — Il template editoriale già consolidato (da riusare integralmente)

Le 9 pagine condividono una struttura **identica**. È il modello di qualità da replicare in ogni pagina futura:

- **Front-matter (7 campi):** `title`, `description` (140-180 char), `layout: "single"`, `toc: true`, `image: ""` (riservato, non usato), `date`, `dataUltimaRevisione`. Nessuna chiave `build:` sulle pagine pubblicate.
- **Paragrafo di apertura** che definisce il tema in lingua piana, con i concetti chiave in **grassetto**.
- **Disclaimer obbligatorio** subito dopo l'apertura, pattern fisso:
  ```html
  <div class="alert alert-info" role="note">
  <p class="mb-0"><i class="bi bi-info-circle me-2" aria-hidden="true"></i><strong>Una guida divulgativa.</strong> … Il Gruppo … <strong>non parla a nome</strong> del Dipartimento della Protezione Civile né della Regione Lazio. In emergenza il riferimento resta sempre il <strong>numero unico 112</strong> e i canali ufficiali.</p>
  </div>
  ```
- **3-7 sezioni H2** con titoli ricorrenti («Che cosa significa…», «Gli strumenti…», «Cosa fa il volontariato in questa fase», «Approfondimenti sul nostro sito»).
- **Citazioni a tre livelli:** (1) link inline alla norma (Normattiva o protezionecivile.gov.it), (2) etichetta `Fonte:` dopo le affermazioni fattuali, (3) sezione finale **«Per approfondire — fonti istituzionali»** con elenco puntato e attribuzione dell'ente. **Nessuna nota a piè di pagina, nessuna bibliografia separata, nessun BibTeX.**
- **Cross-link** sia in-testo sia nel footer verso `/rischi-prevenzione/`, `/strumenti/`, `/allerte-meteo/`, `/cartografia/`, `/piano-emergenza/`, `/normativa/`, `/glossario/`, `/diventa-volontario/`, articoli `/comunicazioni/`.
- **Zero shortcode, zero immagini, zero CSS nuovo.** Solo Markdown nativo + `div.alert` di Bootstrap Italia + tabelle pipe.
- **Lunghezza tipica: 600–1.100 parole/pagina.**

### A.3 — Contenuti dottrinali ancora «sepolti» nelle notizie (candidati al consolidamento)

| Articolo `/comunicazioni/` | Valore dottrinale | Azione proposta |
|---|---|---|
| `2026-04-29-nascita-dipartimento-protezione-civile-italia` | Storia DPC, Vajont→Codice | **Fonte** per la futura pagina «Storia della PC». Resta come notizia; già cross-linkato da `/conoscere/servizio-nazionale/`. |
| `2026-04-16-catena-comunicazioni-…-dpc-cor-com-coc` | Catena DPC/COR/COM/COC | **Fonte primaria interna** per la pagina dedicata «Modello di intervento» (approfondimento di `soccorso/`). |
| `2026-05-14-centro-operativo-comunale-coc` | COC in dettaglio | **Fonte** per «Modello di intervento»; già cross-linkato da `soccorso/`. |
| `2026-05-01-rete-zamberletti-499-esercitazione-radio` | Frequenze verificate | Già consolidato in `rete-zamberletti.md`. Nessuna azione. |
| `2026-04-24-frane-movimenti-terreno-castelli-romani` | Idrogeologia territoriale | **Fonte** per scheda dottrinale «rischio idrogeologico» + territorio. Già cross-linkato da `prevenzione/`. |
| `2026-06-19-microzonazione-sismica-castelli-romani` | Microzonazione sismica | **Fonte** per scheda dottrinale «rischio sismico». |
| `2026-10-06-sismicita-castelli-romani-zona-2b` | Classificazione sismica territorio | **Fonte** per scheda «rischio sismico» (sezione territoriale). |
| `2026-06-02-iso-31000-gestione-rischio` | Norma ISO 31000 risk management | **Fonte/cross-link** per «Scienza del rischio». |
| `2026-01-31-neve-castelli-romani-organizzazione` | Rischio neve/gelo | **Fonte** per la scheda «neve e gelo» del catalogo rischi. |

> **Principio di consolidamento (proposto):** le notizie **non si cancellano e non si spostano** (sono datate, vivono nell'archivio). Le pagine dottrinali permanenti *citano e sintetizzano* le notizie come fonti interne, e le notizie ricevono +1 bullet «Sul nostro sito» verso la pagina dottrinale (esattamente il pattern già usato in Onda 1 su 6 articoli).

> **Piano pandemico 2025-2029:** *non esiste* un articolo dedicato (solo menzioni di passaggio). La futura scheda «rischio sanitario-pandemico» va scritta **da fonti primarie** (Ministero della Salute — Piano Pandemico Nazionale; ISS), non consolidando materiale interno inesistente. Segnalato come gap reale al §F.

### A.4 — Mappa delle collisioni (cosa NON duplicare né scavalcare)

| Slug/sezione esistente | Natura | Regola per il nuovo livello |
|---|---|---|
| **`/conoscere/`** | ⚠️ **già occupato da noi** (Onda 1) | Lo slug radice proposto dal brief è già il nostro. Si **estende**, non si ricrea. |
| `/storia/` | «Storia del **rischio nei Castelli Romani**» (territoriale, `type: storia`, `layout: list`) | **Non toccare.** La futura «Storia della **protezione civile italiana**» ha bisogno di uno slug diverso → decisione §C.4. |
| `/normativa/` | Guida normativa esistente (`dataUltimaRevisione 2026-05-06`) | **Rimando**, non ricreazione. Il backlog «quadro normativo annotato» è un *potenziamento* di questa pagina. |
| `/strumenti/` | Strumenti real-time + cruscotto | **Rimando** dalle pagine «previsione» e dalle schede rischio. |
| `/glossario/` | Glossario sigle (popover inline attivo) | **Rimando**; il backlog «lessico referenziato» è un *potenziamento* di questa pagina + voci nuove in `data/glossario.yaml`. |
| `/metodo-editoriale/` | Pagina «come scriviamo/verifichiamo», ancora `#fonti` | **Casa naturale dello standard di citazione** del livello dottrinale (vedi §C.7). |
| `/rischi-prevenzione/rischio-vulcanico/` | Pagina **operativa** «cosa fare» | Separata e cross-linkata dalla pagina **«materia»** `/conoscere/rischio-vulcanico-colli-albani/`. Modello da replicare per ogni rischio: *materia* in `/conoscere/`, *cosa fare* in `/rischi-prevenzione/`. |
| `/rischi-prevenzione/` (7 pagine operative PRIMA/DURANTE/DOPO) | Operativo-cittadino | Le schede dottrinali del «catalogo rischi» **non** duplicano: spiegano il fenomeno e la scienza, e rimandano alla pagina operativa per l'autoprotezione. |
| `/esercitazioni/`, `/scuole/`, `/schede-1-minuto/` | Operativo/didattico | Solo cross-link, nessuna sovrapposizione. |

### A.5 — Meccanismo di menu e front-matter (convenzioni rilevate)

- **Menu:** definito in `hugo.toml` come `[[menus.main]]` (voce padre con `identifier`, figli con `parent`). **Va sempre replicato in `static/app-shared/site-chrome.js`** (regola di coerenza, rule 04b). La voce «Conoscere la Protezione Civile» **oggi è figlia del dropdown «Risorse»** (`parent = "risorse"`, `weight = 0`) — **non** voce di primo livello. Il commento in `hugo.toml` documenta il perché: il 29/05/2026 collocarla al primo livello causava **overflow orizzontale della navbar** (etichetta troppo lunga). Questo vincolo pesa sulla decisione §C.1/§C.2.
- **Front-matter pagine dottrinali:** vedi §A.2 (7 campi). Coerente con `/normativa/`, `/strumenti/`, `/glossario/` (tutte `layout: single`, `toc`, `tts`, `dataUltimaRevisione`). Le pagine `/conoscere/` **non** dichiarano `tts:` esplicito → ereditano il default-ON (corretto: vogliamo la lettura ad alta voce su contenuto educativo).
- **Skill assenti:** le skill `audit-pcgenzano` e `bootstrap-italia-agid` citate nel brief **non sono installate** in questo ambiente (è presente 1 sola skill). Il controllo qualità si appoggia agli **agent del repo** già disponibili: `pc-article-reviewer` (gate AGID), `pc-normative-verifier` (vigenza norme — centrale qui), `pc-accessibility-auditor`, `pc-internal-linker`, `pc-seo-checker`, `pc-deploy-validator`.

---

## B. Architettura informativa proposta

### B.1 — L'albero (esistente ✅ + proposto 🔲)

```
/conoscere/                                    ✅ landing (hub del livello-materia)
├── le-quattro-fasi/                           ✅ panoramica + R = P × V × E
│   ├── previsione/                            ✅
│   ├── prevenzione/                           ✅
│   ├── soccorso/                              ✅ (sintesi della catena)
│   │   └── modello-di-intervento/             🔲 approfondimento: COC→COM→CCS→DiComaC,
│   │                                              catena soccorsi sanitari, triage/PMA
│   │                                              (consolida art. catena-comunicazioni + COC)
│   └── superamento/                           ✅ (sintesi)
│       └── dopo-l-emergenza/                  🔲 approfondimento: stato emergenza, ordinanze
│                                                  art. 25, AeDES/FAST, ricostruzione, lezioni apprese
├── servizio-nazionale/                        ✅ chi-fa-cosa
│   └── scienza-del-rischio/                   🔲 Centri di competenza, INGV/CNR/ISPRA,
│                                                  catena modello→bollettino→allerta
├── catalogo-dei-rischi/                       🔲 HUB nuovo: indice delle schede-rischio «materia»
│   ├── rischio-sismico/                       🔲 (consolida microzonazione + zona 2b)
│   ├── rischio-idrogeologico/                 🔲 (consolida frane Castelli)
│   ├── rischio-incendio/                      🔲
│   ├── rischio-maremoto/                      🔲  ← gap nazionale, fonti INGV/ISPRA/DPC
│   ├── rischio-sanitario/                     🔲  ← gap, fonti Min. Salute/ISS (no materiale interno)
│   ├── rischio-chimico-industriale/           🔲  ← Seveso, fonti ISPRA/MASE
│   ├── rischio-nucleare-radiologico/          🔲  ← Piano naz. emergenze radiologiche
│   ├── rischio-neve-gelo/                     🔲  (consolida neve Castelli)
│   └── rischio-siccita/                       🔲
│   (NB: rischio-vulcanico «materia» vive già a /conoscere/rischio-vulcanico-colli-albani/)
├── rischio-vulcanico-colli-albani/            ✅ DIFFERENZIATORE #2
├── telecomunicazioni-emergenza/               ✅ DIFFERENZIATORE #1
│   ├── rete-zamberletti/                      ✅
│   └── (eventuale) reti-e-protocolli/         🔲 approfondimento tecnico opzionale
├── storia-della-protezione-civile/            🔲 ← risolve collisione /storia/ (vedi §C.4)
└── dimensione-internazionale/                 🔲 UCPM, rescEU, Quadro di Sendai 2015-2030
```

**Potenziamenti di pagine esistenti (non in `/conoscere/`):**
- 🔲 `/normativa/` → sezione «quadro normativo annotato» (annotazioni per articolo del Codice).
- 🔲 `/glossario/` + `data/glossario.yaml` → lessico referenziato (nuove voci con fonte).

### B.2 — Perché sulle quattro fasi (motivazione della scelta già fatta)

L'ossatura su previsione / prevenzione / gestione / superamento **è corretta e va mantenuta**: è la struttura dell'**art. 2 del D.Lgs. 1/2018** (verificato verbatim), quindi l'architettura del sito ricalca l'architettura della legge. È ancorata alla fonte primaria per costruzione — il miglior antidoto all'arbitrarietà. Il catalogo dei rischi e i differenziatori si appendono a questa spina dorsale come «cosa» (i rischi) e «come» (le reti), mentre le quattro fasi restano il «quando/perché».

### B.3 — Intreccio dottrinale ↔ operativo (mappa di cross-linking)

Il livello-materia **non deve galleggiare separato**. Regola di linking bidirezionale (estende il pattern già in uso in Onda 1):

| Pagina dottrinale `/conoscere/` | Rimanda a (operativo) | Riceve link da |
|---|---|---|
| `le-quattro-fasi/previsione/` | `/allerte-meteo/`, `/strumenti/`, `/cartografia/`, `/cosa-succede-quando-scatta-allerta/` | — |
| `le-quattro-fasi/prevenzione/` | `/piano-emergenza/`, `/piano-familiare/`, `/esercitazioni/`, `/rischi-prevenzione/` | — |
| `le-quattro-fasi/soccorso/` (+ modello-di-intervento) | `/cosa-fare-adesso/`, `/emergenza/`, `/aree-attesa/` | art. COC, catena-comunicazioni |
| `catalogo-dei-rischi/rischio-X/` (materia) | `/rischi-prevenzione/rischio-X/` (cosa fare) | pagina operativa rischio-X (link «approfondisci la materia») |
| `rischio-vulcanico-colli-albani/` | `/rischi-prevenzione/rischio-vulcanico/` | ✅ già reciproco |
| `telecomunicazioni-emergenza/` | `/diventa-volontario/`, `/area-volontari/` | art. radio, Zamberletti |
| `scienza-del-rischio/` | `/strumenti/`, `/cruscotto/` | — |
| `storia-della-protezione-civile/` | `/storia/` (territorio), `/normativa/` | art. nascita-DPC |
| `dimensione-internazionale/` | `/normativa/`, `/standard-iso/` | — |

**Aggancio operativo nelle pagine `/rischi-prevenzione/`:** ognuna delle 7+ pagine operative riceve un bullet «**Approfondisci la materia**» verso la scheda `/conoscere/catalogo-dei-rischi/rischio-X/` corrispondente. È un'aggiunta di 1 riga per pagina, nessuna modifica strutturale (e nessun tocco al campo `image:`).

### B.4 — I due differenziatori (entrambi già piazzati)

- **#1 Telecomunicazioni in emergenza** — già pubblicato, ben collocato come ramo di primo livello dentro `/conoscere/`. Competenza radioamatoriale del webmaster (IU0QVW). *Proposta:* eventuale approfondimento tecnico opzionale (`reti-e-protocolli/`) in coda alle Onde, bassa priorità (il nucleo c'è).
- **#2 Vulcano dei Colli Albani** — già pubblicato e verificato (INGV+DPC), correttamente separato dalla pagina operativa. *Proposta:* è già una pagina-bandiera; in futuro si può aggiungere una scheda di monitoraggio live agganciata al `/cruscotto/`, ma è extra, non backlog.

Entrambi i differenziatori sono **fatti**: la leva competitiva del sito è già a terra. Le Onde 2+ servono a costruire la *completezza* attorno ad essi.

---

## C. Decisioni che spettano a te (con la mia raccomandazione)

> **DECISIONI APPROVATE — 29 maggio 2026** (l'utente ha scelto in terminale; alcune divergono dalla mia raccomandazione, e va bene così: consiglio io, decide lui).
>
> | # | Decisione | Esito approvato |
> |---|---|---|
> | C.1 | Etichetta menu | **Etichetta lunga «Conoscere la Protezione Civile»** mantenuta (resta in un dropdown, non nella barra: nessun overflow). |
> | C.2 | Primo livello vs annidata | **Resta sotto «Risorse»** (`parent = "risorse"`). *Non* promossa a primo livello. |
> | C.3 | Slug radice | **`/conoscere/`** confermato. |
> | C.4 | Collisione `/storia/` | **`/conoscere/storia-della-protezione-civile/`** (mia raccomandazione, non revisionata). |
> | C.5 | Ordine di costruzione | **Breadth-first**: prima l'ossatura completa (hub + stub), poi il riempimento. |
> | C.6 | Priorità differenziatori | Già fatti; completezza prioritaria. |
> | C.7 | Standard citazione | Modello a 3 livelli, dichiarato in `/metodo-editoriale/`. |
> | C.8 | Profondità | **Pagine ampie 2.000-3.000+ parole.** ⚠️ *Nota di sostenibilità (registrata una volta, poi rispettata):* è il massimo di autorevolezza ma il più impegnativo da mantenere/aggiornare per un webmaster solo; mitigazione = datare ogni pagina, sequenziare con calma, usare i gate `pc-normative-verifier`/`pc-content-freshness` per non far invecchiare i fatti. |
> | F.3 | Scope rischi tecnologici | **Inclusi in pieno** (chimico-industriale/Seveso, nucleare-radiologico, sanitario-pandemico) con ricerca su fonti primarie. |
>
> Restano da confermare a inizio sessione di costruzione: **F.2** (forma del cross-link `/storia/`↔storia-PC), **F.5** (spostare i file di lavoro Onda 1 in `.claude/planning/`?), **F.6** (approfondimenti differenziatori in coda sì/no).
>
> *Le motivazioni originali per ciascuna opzione restano qui sotto come traccia del ragionamento.*

### C.1 — Etichetta del menu
- **Raccomando: accorciare a «Conoscere la PC» oppure «La Protezione Civile»** nella navbar (mantenendo `<title>`/H1 della pagina = «Conoscere la Protezione Civile»). **Perché:** l'etichetta lunga ha già causato overflow orizzontale della navbar (regressione documentata 29/05/2026, per cui la voce è stata retrocessa sotto «Risorse»). Un'etichetta corta è la condizione tecnica per poterla eventualmente promuovere a primo livello (§C.2).
- Alternative: tenere «Conoscere la Protezione Civile» (resta sotto Risorse per forza); oppure «Conoscere».

### C.2 — Voce di primo livello vs sotto una sezione
- **Raccomando: promuovere a voce di primo livello come dropdown** «Conoscere la PC» (etichetta corta), con figli = le pagine principali del livello. **Perché:** un'opera di riferimento nazionale merita visibilità di primo livello; oggi è sepolta sotto «Risorse» solo per un incidente di larghezza, non per scelta editoriale. Vincolo: fattibile **solo** con etichetta corta (§C.1) — da verificare con screenshot Playwright prima del merge, come da rule sulla verifica visiva.
- Alternative: lasciarla sotto «Risorse» (zero rischio navbar, ma poca dignità per il livello faro); collocarla sotto «Per il Cittadino» (no: il target è più ampio del cittadino).

### C.3 — Slug radice del livello
- **Raccomando: confermare `/conoscere/`.** **Perché:** già live, già indicizzato, già cross-linkato da 6 articoli e dalla mappa-sito; cambiarlo significherebbe redirect e link rotti senza guadagno. È chiaro e breve.
- Alternative (sconsigliate ora): `/protezione-civile/`, `/la-materia/`, `/sistema/` — tutti comporterebbero migrazione.

### C.4 — Collisione con `/storia/` (slug per la storia della PC)
- **Raccomando: `/conoscere/storia-della-protezione-civile/`.** **Perché:** la storia *della materia* (nazionale: Vajont, legge 996/1970, Zamberletti, legge 225/1992, Codice 2018) è concettualmente parte del livello dottrinale; `/storia/` resta la storia *del rischio territoriale* dei Castelli. Slug diverso, zero collisione, e cross-link reciproco esplicito tra le due pagine per non confondere il lettore.
- Alternative: `/storia-protezione-civile/` (primo livello, ma duplica «storia» nella radice del sito e confonde); inglobarla in `servizio-nazionale/` (no: merita pagina propria).

### C.5 — Ordine di costruzione: depth-first vs breadth-first
- **Raccomando: depth-first mirato.** Costruire **1 pagina esemplare nuova, finita e rigorosa**, come **modello di qualità approvato** prima di aprire il fronte largo. Candidata: una scheda del **catalogo rischi** (es. `rischio-sismico/`), perché definisce il *template riusabile* per ~9 schede — il blocco di backlog più grande. **Perché:** il livello editoriale (citazioni, profondità, cross-link) si giudica meglio su una pagina vera che su uno scheletro; e fissare il template prima evita di riscrivere 9 pagine se cambi idea sulla struttura. L'ossatura «breadth» del catalogo (l'hub + gli stub) può seguire subito dopo l'approvazione del modello.
- Alternative: breadth-first puro (prima tutta l'ossatura, poi riempimento) — più veloce a dare l'impressione di completezza, ma rischia molte pagine mediocri da rifare; ibrido (hub + 1 scheda piena), che di fatto è la mia raccomandazione.

### C.6 — Priorità dei differenziatori
- **Raccomando: nessuna priorità di costruzione — sono già fatti.** Telecom e vulcano sono live e verificati. La priorità si sposta sulla **completezza** (catalogo rischi, storia, internazionale). Eventuali approfondimenti dei differenziatori (`reti-e-protocolli/`, monitoraggio vulcano live) vanno **in coda**, opzionali.
- Alternative: anticipare l'approfondimento telecom (ha senso solo se vuoi capitalizzare subito la competenza IU0QVW con una pagina tecnica).

### C.7 — Standard di citazione delle fonti (formato + dove dichiararlo)
- **Raccomando: formalizzare il modello a tre livelli già in uso** (link inline alla norma → etichetta `Fonte:` → sezione finale «Per approfondire — fonti istituzionali»), e **dichiararlo nella pagina `/metodo-editoriale/`** (ha già un'ancora `#fonti` e la gerarchia delle fonti). **Perché:** è già lo standard di fatto dell'Onda 1, è coerente AGID (link inline, niente note a piè di pagina), ed è verificabile dal lettore. La pagina Metodo è la casa naturale dell'impegno di trasparenza, ed è già linkata dal footer. Aggiungo: ogni pagina dottrinale chiude sempre con la sezione fonti, e ogni fatto puntuale (numero d'articolo, data, soglia, frequenza) ha un link a fonte primaria o un marker `<!-- FONTE-DA-VERIFICARE -->` finché non è chiuso.
- Alternative: note a piè di pagina numerate (più «accademico» ma fuori standard AGID e non usato altrove nel sito); bibliografia per-pagina separata (ridondante con la sezione fonti).

### C.8 — Profondità target per pagina
- **Raccomando: due fasce.** **Pagine-panorama e schede-rischio: 900–1.400 parole** (un filo sopra l'Onda 1, perché sono pagine di riferimento); **pagine-approfondimento dedicate** (modello di intervento, dopo-l'emergenza, scienza del rischio, internazionale): **1.400–2.200 parole**. Sempre con TOC, sezioni H2 brevi, frasi <20 parole (AGID). **Perché:** «punta in alto» del brief = profondità reale, ma la sostenibilità per un webmaster solo impone di non scrivere monografie da 5.000 parole che poi non si aggiornano. La profondità si ottiene con *rigore e cross-link*, non con la lunghezza pura.
- Alternative: pagine brevi uniformi 600-800 (più sostenibili ma non «opera di riferimento»); pagine lunghe 3.000+ (autorevoli ma fragili in manutenzione per una persona sola).

---

## D. Pagina-tipo, a livello di sola scaletta

Scelta: **`/conoscere/catalogo-dei-rischi/rischio-sismico/`** — è il *template riusabile* per ~9 schede del catalogo, quindi il campione più utile per giudicare lo standard. È una pagina **«materia»** (la scienza del fenomeno), distinta dalla pagina operativa `/rischi-prevenzione/rischio-sismico/` («cosa fare»).

> Scaletta a titoli; sotto ogni voce, *cosa conterrà* e *quali fonti primarie servono*. Niente prosa: è il modello dello standard editoriale.

**Front-matter:** `title: "Il rischio sismico in Italia: capire i terremoti"` · `description` (≤180 char) · `layout: single` · `toc: true` · `image: ""` · `date` · `dataUltimaRevisione`.

**Apertura (2-3 frasi):** che cos'è il rischio sismico, e che questa è la pagina-materia (rimando alla pagina operativa per l'autoprotezione).

**Disclaimer `alert-info`** (pattern fisso §A.2), variante: «sulla base delle fonti di INGV, DPC e ISPRA».

1. **## Che cos'è un terremoto** — origine tettonica, faglie, energia rilasciata; differenza **magnitudo vs intensità** (scala Richter/Mw vs MCS/EMS-98). *Fonti:* INGV (educational «terremoti»), Glossario INGV.
2. **## Come si misura: magnitudo, intensità, accelerazione** — Mw, scala macrosismica, PGA; perché due terremoti di pari magnitudo fanno danni diversi (R = P × V × E richiamato dalla panoramica). *Fonti:* INGV; rimando interno a `/conoscere/le-quattro-fasi/` per la formula del rischio.
3. **## La pericolosità sismica in Italia** — mappa di pericolosità **MPS04** (base della classificazione), zone sismiche; l'Italia come paese a sismicità medio-alta. *Fonti:* INGV (MPS), DPC (classificazione sismica nazionale), Normattiva (OPCM 3519/2006 — **da verificare verbatim**).
4. **## La classificazione sismica e le 4 zone** — zone 1-2-3-4, cosa implicano; **Genzano/Castelli in zona 2B** (consolidando i due articoli interni). *Fonti:* DPC, Regione Lazio (DGR classificazione — **da verificare**); articoli interni `sismicita-castelli-zona-2b`, `microzonazione-sismica-castelli`.
5. **## Microzonazione sismica: perché due strade vicine reagiscono diverse** — effetti di sito, amplificazione locale; il lavoro di microzonazione. *Fonti:* DPC/Centro microzonazione, ISPRA; articolo interno microzonazione.
6. **## Prevedere i terremoti si può? No, prepararsi sì** — smontare il mito della «previsione»; cosa significa davvero previsione probabilistica vs deterministica; il ruolo della prevenzione strutturale (norme antisismiche). *Fonti:* INGV (FAQ previsione), DPC «Io non rischio» terremoto.
7. **## Cosa fa la protezione civile per il rischio sismico** — sorveglianza INGV h24, allerta non possibile → enfasi su prevenzione; ruolo del volontariato (rilievo danni, assistenza, NON valutazioni di agibilità — quelle sono dei tecnici AeDES). *Fonti:* DPC, rimando a `/conoscere/le-quattro-fasi/superamento/` (AeDES).
8. **## Approfondimenti sul nostro sito** — `/rischi-prevenzione/rischio-sismico/` (cosa fare), `/conoscere/le-quattro-fasi/`, `/conoscere/rischio-vulcanico-colli-albani/` (sismicità vulcanica locale), `/storia/` (terremoto 1806, crisi 1989-90), `/glossario/`.
9. **## Per approfondire — fonti istituzionali** — elenco puntato con attribuzione: INGV, DPC «rischio sismico», ISPRA, Normattiva (norme tecniche costruzioni — da verificare).

*Note di rigore per questa pagina:* ogni dato puntuale (numero OPCM, soglie di zona, anno della mappa MPS04, magnitudo di eventi citati) richiede verifica su fonte primaria via `pc-normative-verifier`/WebFetch prima della pubblicazione; finché aperto, marker `<!-- FONTE-DA-VERIFICARE -->`. Nessuna magnitudo o data inventata.

---

## E. Piano di sequenziamento (Onde 2-N) — solo piano, non eseguito

**Aggiornato alle decisioni approvate (§C): breadth-first, rischi tecnologici inclusi, pagine ampie 2.000-3.000+.**

Logica breadth-first scelta dall'utente: **prima l'ossatura completa**, poi il riempimento per profondità. Pensato comunque per **un webmaster solo**: l'ossatura si costruisce in un colpo, ma ogni pagina-foglia poi si riempie e si data singolarmente, così il carico delle pagine ampie è spalmato nel tempo e nessuna pagina invecchia senza controllo.

| Onda | Contenuto | Tipo | Carico |
|---|---|---|---|
| **2 — Ossatura (breadth)** | `catalogo-dei-rischi/_index.md` (hub completo) + **tutti gli stub** delle schede rischio (sismico, idrogeologico, incendio, maremoto, neve-gelo, siccità, chimico-industriale, nucleare-radiologico, sanitario) + stub di `storia-della-protezione-civile/`, `dimensione-internazionale/`, `servizio-nazionale/scienza-del-rischio/`, `soccorso/modello-di-intervento/`, `superamento/dopo-l-emergenza/`. Ogni stub = front-matter + apertura + disclaimer + scaletta H2 con marker `<!-- DA SCRIVERE -->` e fonti previste, **escluso dalle liste** se non ancora sostanziale. | scheletro | 1-2 sessioni |
| **3 — Riempimento: rischi consolidabili** | `rischio-sismico/` (modello §D, ampio), `rischio-idrogeologico/`, `rischio-incendio/`, `rischio-neve-gelo/` — riusano articoli interni come fonte. | pagine piene 2-3k | 2-3 sessioni |
| **4 — Riempimento: gap nazionali naturali** | `rischio-maremoto/`, `rischio-siccita/` (fonti INGV/ISPRA/Copernicus/Min. Ambiente). | pagine piene 2-3k | 1-2 sessioni |
| **5 — Riempimento: rischi tecnologici** (incluso per decisione F.3) | `rischio-chimico-industriale/` (Seveso, fonti ISPRA/MASE), `rischio-nucleare-radiologico/` (Piano naz. emergenze radiologiche, ISIN), `rischio-sanitario/` (Min. Salute/ISS, Piano Pandemico). **Richiede ricerca su fonti primarie**, no materiale interno. | pagine piene 2-3k | 2-3 sessioni |
| **6 — Riempimento: storia + fasi** | `storia-della-protezione-civile/` (consolida nascita-DPC; cross-link `/storia/`) + `soccorso/modello-di-intervento/` (COC→COM→CCS→DiComaC, triage/PMA) + `superamento/dopo-l-emergenza/`. | pagine piene 2-3k | 2-3 sessioni |
| **7 — Riempimento: scienza + internazionale** | `servizio-nazionale/scienza-del-rischio/` (Centri di competenza) + `dimensione-internazionale/` (UCPM, rescEU, Sendai). | pagine piene 2-3k | 2 sessioni |
| **8 — Potenziamenti trasversali** | `/normativa/` annotato per articolo + nuove voci `/glossario/` (`data/glossario.yaml`) + eventuali approfondimenti differenziatori (F.6). | trasversale | continuativo |

**Nota breadth-first / gate render:** gli stub dell'Onda 2 che non sono ancora pagine vere vanno tenuti **fuori dalle liste e dalla ricerca** finché non sostanziali (front-matter `build: { list: never, render: always, publishResources: true }`), oppure linkati dall'hub come «in costruzione» — così l'ossatura è navigabile senza dare al cittadino pagine vuote spacciate per finite. Da concordare la modalità a inizio Onda 2.

Ogni onda chiude con: gate `pc-article-reviewer` (AGID) + `pc-normative-verifier` (vigenza norme — centrale) + `pc-accessibility-auditor` + `pc-internal-linker` + build `hugo --minify` pulito. Quando si tocca il menu, replica in `site-chrome.js` + verifica visiva. Niente onda tocca `image:`, il CSS della navbar, o introduce PWA/Service Worker/build step/librerie PDF.

---

## F. Domande aperte (mi serve una tua decisione/input prima di procedere)

1. **Le 8 decisioni del §C** — in particolare **C.1+C.2** (etichetta corta + promozione a primo livello, oppure status quo sotto Risorse) e **C.5** (depth-first sulla scheda sismica come modello). Sono il blocco che sblocca tutto.
2. **`/storia/` (§C.4):** confermi `/conoscere/storia-della-protezione-civile/`? E vuoi che la `/storia/` territoriale resti intatta (sì, per default) con solo un cross-link aggiunto?
3. **Rischi tecnologici (Onda 5):** chimico-industriale, nucleare-radiologico e sanitario-pandemico **non hanno materiale interno** e richiedono ricerca su fonti primarie (Min. Salute/ISS, ISPRA/MASE, piani nazionali). Vuoi includerli (completezza piena) o tenerli fuori dallo scope iniziale e marcarli «in costruzione» nell'hub?
4. **Profondità (§C.8):** ti sta bene la doppia fascia 900-1.400 / 1.400-2.200 parole, o preferisci pagine più snelle per sostenibilità?
5. **File di lavoro Onda 1** (`_FONTI-DA-VERIFICARE.md`, `_PR-DESCRIPTION.md`): sono esclusi dal sito (`build: render: never`) ma stanno dentro `content/conoscere/`. Li lasciamo come traccia di verifica (utile per audit) o li spostiamo in `.claude/planning/` per pulizia? *Mia preferenza:* spostarli qui, così `content/` resta solo contenuto.
6. **Telecom approfondito / vulcano live:** li vuoi nel piano (coda, Onda 10) o li consideri chiusi così come sono?

---

## Vincoli rispettati da questa proposta (checklist)

- ✅ Nessuna pagina creata in `content/`; nessun file pubblicato modificato; nessun tocco a menu/config/front-matter.
- ✅ Unico file scritto: questo, in `.claude/planning/` (fuori da `content/`, mai costruito da Hugo).
- ✅ Nessun merge su `main`, nessun deploy.
- ✅ `dangerous-clean-slate: false` resta intoccato; **PWA/Service Worker/offline-first esclusi** (categoria permanentemente fuori scope, non compaiono nemmeno nel backlog); Vanilla JS only; nessun build step; nessuna libreria PDF; nessun CSS nuovo; riuso componenti Bootstrap Italia (`alert`); navbar CSS non toccato.
- ✅ Disciplina delle fonti incorporata (§C.7, §D, §F): ogni fatto su fonte primaria o marcato da verificare; mai numeri/articoli/date/frequenze inventati.
- ✅ Disclaimer + `dataUltimaRevisione` previsti su ogni pagina futura (§A.2).
- ✅ In caso di conflitto col brief, vincono le regole `.claude/` (allineato a CLAUDE.md, rule 02/04b/05/06).
