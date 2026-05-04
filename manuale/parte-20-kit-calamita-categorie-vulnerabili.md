# Parte 20 — Kit Calamità per categorie vulnerabili (maggio 2026)

A maggio 2026 il Gruppo ha realizzato un'iniziativa autonoma di **schede operative stampabili A4** per assistere persone particolarmente vulnerabili durante e dopo una calamità (terremoto, alluvione, incendio, evacuazione). Il progetto si è chiamato **"Kit Calamità"** e nasce dall'osservazione che in emergenza alcune categorie sono **doppiamente esposte**: bambini in stress da imprevisto, anziani disorientati, ospiti di RSA da evacuare, persone con disabilità, neonati, donne in gravidanza, animali, caregiver familiari, pazienti con terapie salvavita, persone senza dimora, parlanti italiano L2, e gli stessi volontari di PC esposti a stress operativo.

Il progetto **non sostituisce** i protocolli istituzionali del Sistema Nazionale di Protezione Civile: è un **complemento operativo** che traduce in pratica gli standard internazionali di settore per chi opera sul campo.

---

## 20.1 — Hub e architettura

L'**hub centrale** è in `/formazione/kit-calamita/` (`content/formazione/kit-calamita/_index.md`). È strutturato come **cruscotto** simile a `/formazione/scuole-da-dove-cominciare/`: il visitatore sceglie la propria situazione ("Sono...") e arriva in 1 click al kit specifico.

**12 kit attualmente pubblicati:**

| Kit | Standard di riferimento | Cartella content | Cartella static |
|---|---|---|---|
| 👧 Bambini 3-14 anni | NCTSN PFA Children + IFRC + WHO/UNHCR + Sphere 2018 | `content/formazione/kit-calamita-bambini/` | `static/formazione/kit-calamita-bambini/` |
| 👶 Neonati 0-3 anni | IFE Core Group v3.0 (2017) + WHO Code latte materno + Sphere | `content/formazione/kit-calamita-neonati/` | `static/formazione/kit-calamita-neonati/` |
| 👴 Anziani in casa | HelpAge International + WHO mhGAP + SIGG/AIP | `content/formazione/kit-calamita-anziani/` | `static/formazione/kit-calamita-anziani/` |
| 🤝 Caregiver familiari | L. 205/2017 + Carta Eurocarers 2014 + WHO Self-care 2022 + Zarit | `content/formazione/kit-calamita-caregiver-familiari/` | `static/formazione/kit-calamita-caregiver-familiari/` |
| 🏥 Strutture sanitarie / RSA | Min. Salute + AGENAS + WHO Hospital Safety Index + CSNAP | `content/formazione/kit-calamita-strutture-sanitarie/` | `static/formazione/kit-calamita-strutture-sanitarie/` |
| ♿ Disabilità adulti | CRPD ONU art. 11 + L. 18/2009 + WHO Disability Inclusive (2013) | `content/formazione/kit-calamita-disabilita-adulti/` | `static/formazione/kit-calamita-disabilita-adulti/` |
| 🩺 Terapie salvavita | WHO Health Cluster 2018 + Sphere § Essential health + ARERA 295/2018 | `content/formazione/kit-calamita-terapie-salvavita/` | `static/formazione/kit-calamita-terapie-salvavita/` |
| 🤰 Gravidanza e neomamme | MISP IAWG (2018) + WHO Pregnancy + UNFPA + Sphere | `content/formazione/kit-calamita-gravidanza/` | `static/formazione/kit-calamita-gravidanza/` |
| 🏚️ Senza fissa dimora | FEANTSA ETHOS + FIO.PSD + Min. Lavoro 2015 + Housing First | `content/formazione/kit-calamita-senza-fissa-dimora/` | `static/formazione/kit-calamita-senza-fissa-dimora/` |
| 🌐 Italiano L2 / stranieri | UNHCR CwC 2020 + IOM CCCM + Sphere § Communication | `content/formazione/kit-calamita-italiano-l2/` | `static/formazione/kit-calamita-italiano-l2/` |
| 🐕 Animali domestici | D.Lgs. 1/2018 art. 12 + L. 281/1991 + WSAVA Disaster Response | `content/formazione/kit-calamita-animali/` | `static/formazione/kit-calamita-animali/` |
| 🟢 Volontari PC (auto-cura) | IFRC Caring 2015 + NCTSN STS 2018 + WHO mhGAP + ProQOL-5 | `content/formazione/kit-calamita-volontari-pc/` | `static/formazione/kit-calamita-volontari-pc/` |

Ogni kit ha **almeno**:

1. `00-guida-operatori.html` — leggere prima, principi, riferimenti standard, cosa NON fare
2. `01-...html` — di solito una **carta d'identità di emergenza** (anagrafica + salute + ausili + contatti)
3. `02-...html` — di solito una **checklist evacuazione** o un piano operativo
4. `index.html` — hub navigabile del kit (statico, fuori da Hugo) con sezione "Riutilizzo e attribuzione"
5. `_index.md` — landing Hugo che entra nei menu, breadcrumb, search

---

## 20.2 — Standard adottati (gerarchia)

I kit sono ispirati a un quadro **gerarchico** di standard. In caso di conflitto teorico, prevalgono i livelli superiori.

**Livello 1 — italiano vincolante**
- AGID (linee guida design PA)
- DPC (D.Lgs. 1/2018 Codice PC, Direttiva PCM 30 aprile 2021, Direttiva PCM 13 giugno 2006 psicosociale, Direttiva PCM 24 giugno 2016 sanitario, campagne "Io non rischio")
- Codici colore allerta meteo Centro Funzionale Regionale

**Livello 2 — standard internazionali umanitari**
- Sphere Standards 2018, WHO (Health Cluster, mhGAP-HIG, Self-care 2022, Hospital Safety Index, KMC, Code latte materno 1981, Disability 2013), IFRC (Caring for Volunteers 2015, PFA), UNHCR (CwC 2020, RFL), IOM (CCCM Toolkit), IFE Core Group (Operational Guidance v3.0 2017), IAWG MISP (2018), NCTSN (PFA, STS), WSAVA, HelpAge International, FEANTSA (ETHOS), Eurocarers (Carta 2014), CWA CEN/CENELEC

**Livello 3 — normativa italiana di settore**
- L. 18/2009 ratifica CRPD, L. 67/2006 antidiscriminazione, L. 205/2017 art. 1 c. 255 caregiver, L. 33/2023 anziani non autosufficienti, L. 104/1992, D.Lgs. 105/2022, L. 281/1991 animali, L. 189/2004, D.Lgs. 286/1998 art. 35 stranieri, D.Lgs. 25/2008, L. 47/2017 MSNA, D.P.R. 223/1989 art. 2 residenza fittizia, ARERA delibera 295/2018 elettromedicali

**Livello 4 — società scientifiche e federazioni italiane**
- Salute: SIGG, SICP, AIP, SIN, SIGO, AIOM, AIPO-ITS, SIMER, SIMM, CNT/CIST, UNIAMO+Telethon, AIMA, SIPEM SoS, FNOPO
- Inclusione: FISH, FAND, UICI, ENS, ANGSA, FIO.PSD, Housing First Italia, Eurocarers
- Animali: ENPA, OIPA, LAV, LNDC
- Strumenti CAA: ARASAAC (CC BY-NC-SA 4.0), ISO 7010

L'elenco completo delle citazioni è anche nell'hub `/formazione/kit-calamita/` § "Standard adottati".

---

## 20.3 — Eco-print: font URW Gothic L

Le schede sono progettate per essere stampabili **in calamità** quando le cartucce/toner sono risorse finite. Il font scelto è **URW Gothic L** (open-source GPL, ≈ Century Gothic / Avant Garde) che con le tracce sottili consuma circa **30% di inchiostro in meno di Arial/Helvetica** mantenendo leggibilità ottima per bambini piccoli e ipovisione.

CSS condiviso: `static/formazione/kit-calamita-shared/print.css`. Strategia completa documentata nel commento del file. Modalità "Eco-print" opzionale (`.eco-print`) attivabile sul `<body>` per ulteriori risparmi.

Cascata font: `'URW Gothic L', 'Century Gothic', 'Avant Garde Gothic', 'Avant Garde', 'ITC Avant Garde Gothic', 'Liberation Sans', sans-serif`.

---

## 20.4 — Template uniforme `.carta-id-*` per le schede compilabili

Tutte le carte d'identità di emergenza usano lo stesso template **scoped** `.carta-id-*` definito in `static/formazione/kit-calamita-shared/print.css`. Layout block (label sopra, riga sotto), robusto in stampa A4. Spazio scrittura adeguato a mano: riga singola **11mm** (no 6mm), box libero 30/45/60mm.

Componenti disponibili:
- `.carta-id-corpo` — wrapper della `.scheda-attivita` per allineamento corretto
- `.carta-id-sez` — sezione con bordo + h2 azzurro istituzionale + page-break-inside avoid
- `.carta-id-campo` — campo singolo (label + riga 11mm)
- `.carta-id-coppia` / `.carta-id-tris` — 2 / 3 campi affiancati via grid
- `.carta-id-opzioni` — checkbox inline (label + opzioni)
- `.carta-id-box` — area scrittura libera (small/medio/grande, opzionalmente con righe orizzontali)
- `.carta-id-nota` — alert rosso con bordo `#c1121f`

Quando si crea una nuova scheda compilabile **usare sempre questo template**. Vietato riprendere il vecchio pattern `.form-row` (flex sparso, layout rotto in stampa) o `.campo` con `min-height: 6mm` (campi troppo piccoli per scrittura a mano).

---

## 20.5 — Soluzioni capovolte sui giochi (paradigma enigmistico)

I giochi (cruciverba, sudoku, word search) hanno la **soluzione stampata in fondo alla stessa scheda**, **ruotata 180°** via CSS `transform: rotate(180deg)`. L'utente che vuole verificare la risposta deve **girare fisicamente il foglio sottosopra**: i bambini non la vedono per caso, l'operatore la verifica al volo.

Classe CSS: `.soluzione-capovolta` in `static/formazione/kit-calamita-shared/print.css`.

Quando si aggiunge un nuovo gioco verificabile, usare il pattern:
```html
</section>
<div class="soluzione-capovolta">
  <span class="titolo">🔑 Soluzione — gira il foglio sottosopra per leggere</span>
  <p>...</p>
</div>
```

Niente più `<details>` con `<summary>` (vecchio paradigma). Niente foglio operatore separato (eliminato `99-soluzioni-giochi.html` da kit bambini).

---

## 20.6 — Riutilizzo e attribuzione

I materiali sono **rilasciati gratuitamente** e sono **liberi e riutilizzabili** da altri Comuni, Gruppi di Protezione Civile, scuole, RSA e operatori sanitari. Le schede che includono pittogrammi **ARASAAC** ereditano la licenza **CC BY-NC-SA 4.0**.

La citazione del Gruppo è **molto gradita**: la formula consigliata è
> *Adattato dai Kit Calamità del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma — www.protezionecivilegenzano.it*

Il box "Riutilizzo e attribuzione" appare in tutti i 9 hub statici (`index.html`) dei kit + nella landing centrale `/formazione/kit-calamita/` (sezione "Riutilizzo e attribuzione").

---

## 20.7 — Integrazione con il resto del sito

**Menu di navigazione** (`hugo.toml` + `static/app-shared/site-chrome.js`):
- voce **"Kit pronti per situazioni vulnerabili"** sotto **"Per il Cittadino"** → punta a `/formazione/kit-calamita/` (riorganizzazione v3 maggio 2026: spostato da "Educazione e Inclusione" perché il pubblico target è il cittadino in difficoltà, non la scuola)

**Mappa del sito** (`content/mappa-sito/_index.md`):
- nuova sezione "Kit Calamità — Schede stampabili per categorie vulnerabili" con 13 card colorate (hub + 12 kit specifici)

**Assistente virtuale** (`themes/flavour-pcgenzano/layouts/assistente/list.html`):
- nuovo path "Kit Calamità per categorie vulnerabili" in `mode_informa.options`
- sotto-albero `kc_*` di 13 nodi (12 categorie + hub) per arrivare in 2 click al kit giusto

Quando si aggiunge un nuovo kit, **aggiornare tutti e 4 i punti di accesso**:
1. `content/formazione/kit-calamita-NEW/_index.md` (Hugo content)
2. Hub centrale `/formazione/kit-calamita/` (sezione tematica)
3. `content/mappa-sito/_index.md` (card)
4. `themes/flavour-pcgenzano/layouts/assistente/list.html` (nodo `kc_*` + opzione in `info_kit_calamita`)

---

## 20.8 — Procedura operativa per un nuovo kit

1. Identifica la categoria vulnerabile + standard internazionali di riferimento (almeno 1 livello 2 + 1 livello 3 italiano)
2. Crea le cartelle:
   ```bash
   mkdir -p content/formazione/kit-calamita-NEW \
            static/formazione/kit-calamita-NEW
   ```
3. Scrivi `00-guida-operatori.html` con sezioni: principi, segnali rossi, cosa NON fare, riferimenti istituzionali (lista citata)
4. Scrivi 1-2 schede operative (carta d'identità + checklist) usando il template `.carta-id-*`
5. Scrivi `index.html` (hub statico) con: introduzione + standard di riferimento + indice schede + box "Riutilizzo e attribuzione" + footer
6. Scrivi `_index.md` (Hugo content): frontmatter `layout: "single"` + tabella scheda
7. Aggiungi voce a `/formazione/kit-calamita/_index.md` (sezione tematica + standard)
8. Aggiungi card a `content/mappa-sito/_index.md`
9. Aggiungi sotto-albero `kc_*` + opzione in `info_kit_calamita` di `themes/flavour-pcgenzano/layouts/assistente/list.html`
10. Build pulito: `hugo --quiet --minify`
11. Commit + push

---

## 20.9 — Cronologia evolutiva

**Iter 1-7 (maggio 2026)** — Realizzazione iniziale dei 3 kit principali (bambini, anziani, RSA), template eco-print, schede compilabili, illustrazioni reali integrate (cane, camion, tende, elicottero, lavarsi mani WHO, mandala, Canadair).

**Iter 8 (3 maggio 2026)** — Completamento Kit Strutture Sanitarie (20 schede operative). Menu rinominato "Kit Emergenza Schede" per generalità futura (poi spostato in "Per il Cittadino" e rinominato "Kit pronti per situazioni vulnerabili" nell'Iter 11).

**Iter 9 (3-4 maggio 2026)** — 5 nuovi kit MVP: disabilità adulti, neonati, animali, volontari PC, gravidanza. Aggiornamento landing principale con 8 kit.

**Iter 10 (4 maggio 2026)** — 4 nuovi kit MVP: senza fissa dimora, italiano L2, caregiver familiari, terapie salvavita. **Hub cruscotto** ridisegnato con 12 categorie + sezione "Standard adottati" gerarchica + sezione "Riutilizzo e attribuzione". Template uniforme `.carta-id-*` aggiunto al CSS condiviso e applicato a tutte le 9 carte d'identità (anche retroattivamente). Soluzioni dei giochi convertite al paradigma enigmistico (rotazione 180° in fondo alla stessa pagina). Mappa sito + assistente virtuale aggiornati con tutti i 12 kit.

---

## 20.10 — Riferimenti incrociati nel manuale

- **Parte 3** (Immagini per gli articoli) — il template fascia blu è applicato anche alle illustrazioni reali integrate nei kit (cane da soccorso, camion PC, tende campo, elicottero, ecc.)
- **Parte 19** (Agenti specializzati) — `pc-print-card-qa` è l'agent QA per le schede stampabili
- **Parte 13** (Social Media Policy + gerarchia fonti) — la stessa gerarchia di standard è applicata sia alla comunicazione sui social sia ai kit
- **Parte 18** (Lettura accessibile) — i kit sono complementari alle altre azioni di accessibilità del sito (TTS, glossario inline, sillabazione)

Ogni kit cita esplicitamente gli standard di riferimento sia nella propria guida operatori sia nel `_index.md` Hugo, per dare massima trasparenza istituzionale e facilitare il riutilizzo da parte di altri Comuni e Gruppi.
