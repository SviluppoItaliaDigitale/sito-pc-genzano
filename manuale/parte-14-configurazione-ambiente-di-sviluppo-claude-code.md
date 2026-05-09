_[Indice manuale](README.md)_

# Parte 14 — Configurazione ambiente di sviluppo (Claude Code)

Questa parte è **per chi gestisce il sito con Claude Code** (l'assistente AI di Anthropic). Spiega come predisporre l'ambiente la prima volta perché Claude possa scaricare immagini da fonti libere (Wikipedia, Wikimedia, NASA, USGS) senza essere bloccato dalla sandbox di sicurezza.

### 14.1 — Cos'è la sandbox di Claude Code

Claude Code esegue in una **sandbox di sicurezza** che, di default, blocca:

- chiamate di rete verso domini non autorizzati (Wikipedia, NASA, ecc.);
- scrittura file fuori dalla working directory;
- comandi considerati rischiosi.

È una protezione importante: senza, un errore o un suggerimento sbagliato potrebbe causare danni. Ma per il nostro flusso di lavoro — in cui scarichiamo regolarmente foto da Wikipedia e altre fonti pubbliche per illustrare gli articoli — la sandbox va **configurata** la prima volta con un'allowlist mirata.

### 14.2 — Il file `.claude/settings.local.json`

Le impostazioni della sandbox per questo repo sono in `.claude/settings.local.json` (il file è in `.gitignore` perché è una preferenza locale, non una scelta del Gruppo).

**Schema base usato da noi:**

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "WebFetch(domain:*.wikipedia.org)",
      "WebFetch(domain:commons.wikimedia.org)",
      "WebFetch(domain:upload.wikimedia.org)",
      "WebFetch(domain:*.nasa.gov)",
      "WebFetch(domain:earthquake.usgs.gov)",
      "WebFetch(domain:*.usgs.gov)",
      "Bash(curl:*.wikipedia.org/*)",
      "Bash(curl:commons.wikimedia.org/*)",
      "Bash(curl:upload.wikimedia.org/*)",
      "Bash(curl:images-api.nasa.gov/*)",
      "Bash(curl:images-assets.nasa.gov/*)",
      "Bash(curl:earthquake.usgs.gov/*)"
    ]
  },
  "sandbox": {
    "network": {
      "allowedDomains": [
        "*.wikipedia.org",
        "commons.wikimedia.org",
        "upload.wikimedia.org",
        "*.wikimedia.org",
        "images-api.nasa.gov",
        "images-assets.nasa.gov",
        "*.nasa.gov",
        "earthquake.usgs.gov",
        "*.usgs.gov"
      ]
    }
  }
}
```

**Sezioni distinte, entrambe necessarie:**

- `permissions.allow` autorizza i tool (`WebFetch`, `Bash curl`) a essere chiamati senza chiederti il permesso ogni volta.
- `sandbox.network.allowedDomains` sblocca a livello di rete le connessioni verso quei domini.

Senza la prima, Claude ti chiede conferma a ogni chiamata. Senza la seconda, la rete è bloccata anche se il tool è autorizzato. **Servono entrambe.**

### 14.3 — Domini autorizzati e perché

Sono **gli stessi domini** già whitelisted nello script `scripts/foto-da-*.sh` e nei workflow `.github/workflows/scarica-foto-automatica.yml`:

| Dominio | Uso | Script collegato |
|---|---|---|
| `*.wikipedia.org` | Pagine Wikipedia per estrarre l'immagine principale | `foto-da-wikipedia.sh` |
| `commons.wikimedia.org` | API Commons per ricerche immagini | `foto-da-wikipedia.sh` |
| `upload.wikimedia.org` | Download dei file immagine veri e propri | `foto-da-wikipedia.sh` |
| `*.wikimedia.org` | Altri sottodomini Wikimedia (es. file specifici) | `foto-da-wikipedia.sh` |
| `images-api.nasa.gov` | API NASA Image Library | `foto-da-nasa.sh` |
| `images-assets.nasa.gov` | CDN NASA per i file scaricabili | `foto-da-nasa.sh` |
| `*.nasa.gov` | Altri sottodomini NASA | `foto-da-nasa.sh` |
| `earthquake.usgs.gov` | API USGS per ShakeMap e dati sismici | `foto-da-usgs.sh` |
| `*.usgs.gov` | Altri sottodomini USGS | `foto-da-usgs.sh` |

Tutti sono **fonti libere** (pubblico dominio o CC) usate dal Gruppo per illustrare gli articoli con la fascia blu istituzionale (vedi **Parte 3.8 Metodo 4**).

### 14.4 — Procedura iniziale (una volta sola)

Quando inizi a usare Claude Code su questo repo:

1. **Verifica** se `.claude/settings.local.json` esiste:
   ```bash
   cat .claude/settings.local.json 2>/dev/null || echo "non esiste"
   ```
2. **Se non esiste**: crealo con il contenuto della **14.2**.
3. **Se esiste già con altri contenuti**: aggiungi i due blocchi `permissions.allow` e `sandbox.network.allowedDomains` ai blocchi esistenti, non sovrascrivere.
4. **Riavvia Claude Code**: la sandbox legge il file **all'avvio della sessione**, non dinamicamente. Senza riavvio le modifiche non hanno effetto.

Una volta fatto, dura **per sempre** in questo repo. Non serve ripeterlo a ogni sessione.

### 14.5 — Aggiungere un nuovo dominio

Se in futuro aggiungiamo uno script `foto-da-NUOVA.sh` (es. Copernicus, NOAA, EUMETSAT — vedi regola `05-github-aruba-deploy.md` "Aggiungere una nuova fonte"):

1. Aggiungi i domini necessari sia in `permissions.allow` (per `WebFetch` + `Bash curl`) sia in `sandbox.network.allowedDomains`.
2. Aggiorna la tabella della **14.3** con il nuovo dominio.
3. Riavvia Claude Code.
4. Aggiorna anche la `ALLOWED_SCRIPTS` del workflow `scarica-foto-automatica.yml` se aggiungi un nuovo script di download.

### 14.6 — Cosa NON mettere in `settings.local.json`

- **Niente token, niente credenziali, niente API key**: il file è in `.gitignore` ma per disciplina non ci mettiamo segreti. Se servono, vanno in variabili d'ambiente OS o in GitHub secrets.
- **Niente domini privati** (intranet, sistemi gestionali del Comune, ecc.): la sandbox è uno strato di difesa, non si "apre tutto" perché conviene.
- **Niente `*` come allowlist**: meglio aggiungere domini specifici man mano che servono.

### 14.7 — Quando serve sbloccare la sandbox per le foto

Lo sblocco della sandbox (vedi `.claude/settings.local.json` configurato per i ~17 domini delle nostre fonti foto) serve quando:

- vuoi che l'agent `pc-image-fixer` scarichi una foto da Wikipedia/NASA/USGS via WebFetch + curl, applichi fascia blu (`scripts/applica-fascia-foto.sh`), e inserisca shortcode `{{< foto >}}` nel corpo articolo — tutto dentro la sessione Claude Code;
- vuoi vedere l'immagine **prima del push** per verificare la fascia blu;
- vuoi inserire **più immagini nel corpo** durante una passata di revisione articoli storici.

> ⚠️ **Marker `# TODO-foto-*` BANDITO dal 3 maggio 2026.** Il vecchio meccanismo (marker nel frontmatter → workflow CI scarica + popola `image:`) è stato eliminato perché: (a) il marker veniva renderizzato da Hugo come `<h1>` in produzione finché il workflow non lo rimuoveva, e se `deploy.yml` finiva prima il sito andava live col marker visibile (incidente reale); (b) il workflow popolava `image:` con la foto sovrascrivendo il banner col titolo, contro la regola "BANNER COL TITOLO INTOCCABILE" (CLAUDE.md punto 9). Lo step 2 del workflow (cover tipografica auto) resta attivo.

### 14.8 — Pubblicare un articolo da cellulare: due modi

Il flusso editoriale è progettato per funzionare **anche senza un PC**: dal cellulare puoi pubblicare un articolo completo (testo + cover tipografica banner + deploy automatico).

**Modo 1 — App Claude mobile (la più comoda)**

Apri l'app Claude sul cellulare e chiedi all'AI: *"Crea un articolo su [argomento]"*. L'AI:

1. Crea il file `.md` in `content/comunicazioni/AAAA-MM-GG-slug.md` con frontmatter completo + `image: ""` (vuoto, la cover viene generata al deploy)
2. Fa `git add` + `git commit` + `git push`
3. Il workflow `scarica-foto-automatica.yml` step 2 (`auto-cover-mancanti.py`) genera la cover tipografica banner, popola `image:`, ri-triggera il deploy
4. Tra 5-10 minuti l'articolo è online col banner istituzionale

Per inserire una **foto inline nel corpo articolo**: dopo il push, chiedi a Claude *"trovami una foto gratuita per l'articolo X"*. L'agent `pc-image-fixer` (Parte 19) cerca via WebFetch su Wikipedia/NASA/etc, scarica, applica fascia blu, inserisce shortcode `{{< foto >}}` inline. Da app Claude mobile la procedura funziona perché l'app ha accesso a WebFetch + Bash; manca solo `applica-fascia-foto.sh` (richiede python3-pil): in quel caso l'agent lascia un commento HTML temporaneo e l'esecuzione viene fatta dal prossimo accesso PC.

**Modo 2 — Browser su github.com (anche da cellulare)**

Se non vuoi usare l'AI, puoi creare l'articolo direttamente da `https://github.com/SviluppoItaliaDigitale/sito-pc-genzano`:

1. Tab **Code**, cartella `content/comunicazioni/`
2. **"Add file" → "Create new file"**
3. Nome file: `AAAA-MM-GG-slug.md` (rispetta il formato data — vedi Parte 1.3)
4. Contenuto: frontmatter + corpo articolo (con `image: ""` vuoto)
5. Tasto verde **"Commit changes"**
6. Aspetta 5-10 minuti → cover tipografica banner generata → articolo online

**Riassunto: cosa fa cosa**

| Componente | Dove gira | Funzione |
|---|---|---|
| App Claude Code mobile / web | cloud Anthropic | Scrive l'articolo, fa git push |
| Editor github.com | cloud GitHub | Scrive l'articolo, fa commit |
| Workflow `scarica-foto-automatica.yml` | runner GitHub Actions | Scarica foto, applica fascia, popola frontmatter |
| Workflow `deploy.yml` | runner GitHub Actions | Build Hugo + deploy FTP Aruba + GitHub Pages |
| Sandbox locale di Claude Code (PC) | il tuo PC | Solo per editing/testing locale, **non serve dal cellulare** |

**Punto chiave:** il `.claude/settings.local.json` e la sandbox locale **non hanno effetto** sull'app cloud / mobile / browser — quelle non leggono il filesystem del tuo PC. Tutto il lavoro lato cloud è gestito dai workflow GitHub Actions, che hanno rete libera.

### 14.9 — Foto Wikipedia nel corpo articolo: convenzione di posizionamento

**Regola del progetto** (rispettata dallo script `sposta-foto-wikipedia-nel-corpo.py` e dal workflow di download):

1. La **cover** dell'articolo (mostrata nelle anteprime e nelle card) è **sempre tipografica**: gradiente blu istituzionale + titolo articolo + fascia con logo. Generata da `scripts/genera-cover.py`. File: `static/images/<slug>.webp`.

2. Le **foto reali** (Wikipedia/NASA/USGS/NOAA), se presenti, vanno **nel corpo dell'articolo**, non nella cover. File: `static/images/<slug>-<descrittore>.webp` (nome diverso dallo slug, così `genera-cover.py` non la sovrascrive). Esempi di descrittore: `-fonte-wikipedia`, `-conza-campania-ricostruita`, `-zamberletti-padre-pc`.

3. **Posizione delle foto nel corpo** (convenzione adottata aprile 2026 dopo arricchimento di 35 foto su 30+ articoli storici):

   | Foto | Posizione | Razionale |
   |---|---|---|
   | **1ª foto** | Dopo il **1° H2**, dopo il primo paragrafo di contenuto | Lega la foto al primo blocco di approfondimento (introduzione contestuale) |
   | **2ª foto** | Dopo il **2° H2**, dopo il primo paragrafo | Apre una seconda dimensione narrativa (ricostruzione, contesto secondario, conseguenze) |
   | **3ª, 4ª foto…** | Dopo l'H2 dell'evento storico citato | Una foto per ogni evento storico specifico (es. articoli che raccontano sequenze di terremoti — Irpinia 1980, L'Aquila 2009, Centro Italia 2016) |

   **Mai a casaccio**: ogni foto deve avere un legame tematico con la sezione che la precede. Mai "una foto subito dopo l'intro": l'intro non ha ancora un H2 a cui ancorarla.

4. **Filtro automatico bandiere comunali**: lo script `foto-da-wikipedia.sh` scarta automaticamente i risultati che corrispondono a bandiere/stemmi (pattern: `*Bandiera.svg`, `Flag_of_*`, `*-Stemma.svg`, `*Coat_of_arms*`, `*Stemma_di_*`). Sono SVG decorativi che non aggiungono valore narrativo. Quando capita, lo script ritorna exit code `4` e suggerisce di provare un titolo più specifico (un monumento, una piazza, una veduta). Esempio operativo: per "Cardoso 1996" non usare *"Stazzema"* (restituirebbe la bandiera); usare *"Cardoso (Stazzema)"* o *"Alpi Apuane"*.

5. **Cornice e didascalia**: applicate via CSS scoped (`custom.css` sezione "Figure dallo shortcode foto"). Cornice istituzionale bianca con padding 8px, ombra `0 10px 28px rgba(0,51,102,0.18)`, didascalia centrata con border-top blu trasparente. Il caption deve sempre includere autore + licenza + link "Fonte originale".

6. **Markup**: solo via shortcode `{{< foto src="..." alt="..." caption="..." >}}` (mai markdown `![...]()` diretto).

**Esempio caption ben fatto**:
```
caption="Foto: USGS — Public domain — via Wikimedia Commons. [Fonte originale](https://commons.wikimedia.org/wiki/File:...)."
```

**Quando aggiungere una seconda/terza foto a un articolo esistente**: criterio operativo — un articolo merita foto multiple se (a) ha **almeno sezioni H2**, (b) racconta **eventi storici specifici** (anniversari, memoria, ricostruzioni, sequenze sismiche), (c) le foto trovate hanno **valore narrativo** (luoghi, persone, mappe, satellite — non bandiere o stemmi). Non aggiungere foto a articoli di servizio quotidiano (preparazione casa, salute mentale, ecc.) o a articoli dottrinali (colonne mobili, normativa). Vale la regola del progetto: "non elemosinare le immagini, ma senza esagerare".

### 14.10 — Avvio rapido di Claude Code e del menu di gestione

Per evitare di dover ricordare comandi come `cd ~/sito-pc-genzano && claude` oppure `bash ~/gestione-sito.sh`, da maggio 2026 il progetto ha **3 punti di accesso paralleli** per i due strumenti principali. Tutti fanno la stessa cosa: scegli quello che ti viene comodo.

**Strumento 1 — Claude Code (l'AI assistant)**:

| Modo | Come si attiva |
|---|---|
| Icona desktop | Doppio click su **Claude PC Genzano** (`~/Scrivania/Claude-PC-Genzano.desktop`, icona terminale) |
| Alias da terminale | Scrivi `claude-protezionecivile` (autocomplete: `cl` + TAB) |
| Voce menu gestione | Voce **25 — Avvia Claude Code** dentro `gestione-sito.sh` (quando esci con `/exit` torni al menu) |

**Strumento 2 — Menu interattivo gestione sito** (27 voci: contenuti, emergenze, allerte, deploy, ecc.):

| Modo | Come si attiva |
|---|---|
| Icona desktop | Doppio click su **Gestione PC Genzano** (`~/Scrivania/Gestione-PC-Genzano.desktop`, icona ingranaggio) |
| Alias da terminale | Scrivi `menu-protezionecivile` (autocomplete: `me` + TAB) |
| Comando tradizionale | `bash ~/gestione-sito.sh` (sempre valido) |

L'icona **Sito PC Genzano** esistente (apre VS Code col progetto) resta intatta.

**Architettura**:

- I 2 alias sono in `~/.bashrc` (il file di configurazione bash dell'utente — non versionato).
- I 2 file `.desktop` sono in `~/Scrivania/` (non versionati — sono personali del PC dell'utente).
- I 2 wrapper bash sono nel repo: `scripts/avvia-claude.sh` e `scripts/avvia-menu.sh`. **Versionati**: se in futuro cambia il path del progetto, modifichi solo lo script wrapper, non le icone né gli alias.

**Quando hai appena aggiunto un alias**: i terminali già aperti non lo vedono. Soluzioni: chiudi e riapri il terminale, oppure esegui `source ~/.bashrc` nel terminale corrente.

**File `.txt` di reminder personale**: `~/Scrivania/COME-AVVIARE-Claude-e-Menu.txt` riepiloga le istruzioni in formato testo semplice (non versionato — è del PC, non del repo).

**Su un nuovo PC** (o se reinstalli il sistema): per ricreare la setup serve aggiungere a `~/.bashrc` le 2 righe:

```bash
alias claude-protezionecivile='cd ~/sito-pc-genzano && claude'
alias menu-protezionecivile='bash ~/gestione-sito.sh'
```

E creare i 2 file `.desktop` in `~/Scrivania/` (template in questa stessa parte del manuale, sezione precedente non necessaria — gli script wrapper sono già nel repo).

---

## Appendici

### Appendice A — Colori del sito

| Variabile CSS | Valore | Uso |
|---|---|---|
| `--pc-primary` | `#003366` | Blu istituzionale principale, fascia immagini |
| `--pc-primary-dark` | `#00244d` | Variante scura |
| `--pc-primary-light` | `#004080` | Variante chiara |
| `--pc-secondary` | `#FF6600` | Arancione accento |
| `--pc-accent` | `#009246` | Verde |
| `--pc-danger` | `#d9364f` | Rosso emergenze |
| `--pc-warning` | `#FFC107` | Giallo allerta |

### Appendice B — Struttura delle cartelle

```
sito-pc-genzano/
├── archetypes/                     Template frontmatter per nuovi articoli/pagine
├── content/
│   ├── comunicazioni/              Articoli (Parte 1)
│   └── <altre-sezioni>/            Pagine statiche (Parte 4)
├── data/                           File dati: allerta.json, emergenza.json, numeri_utili.yaml, ecc.
├── static/
│   ├── images/                     Immagini (Parte 3)
│   ├── documenti/                  PDF e allegati
│   ├── giochi/                     Giochi interattivi (standalone)
│   ├── cartelli/                   Immagini cartelli area emergenza
│   └── app-shared/                 site-chrome.js (header/footer per pagine standalone)
├── themes/flavour-pcgenzano/       Tema custom, modificabile
│   ├── layouts/                    Template Hugo
│   └── static/css/                 CSS custom
├── layouts/                        Override locali (shadowing del tema)
├── .claude/rules/                  Regole per Claude Code
├── .github/workflows/              GitHub Actions (deploy, aggiornamento manuale)
├── hugo.toml                       Configurazione Hugo
├── CLAUDE.md                       Istruzioni per Claude Code
└── MANUALE-SITO.md                 Questo file
```

### Appendice C — Comandi rapidi

```bash
# Avviare il sito in locale (solo contenuti pubblicati)
hugo server

# Avviare il sito in locale (mostra anche le bozze)
hugo server -D

# Avviare Claude Code sul progetto (alias in ~/.bashrc)
claude-protezionecivile

# Avviare il menu interattivo di gestione (alias in ~/.bashrc)
menu-protezionecivile

# Nuovo articolo
hugo new comunicazioni/AAAA-MM-GG-titolo-breve.md

# Build di produzione (verifica pre-push)
hugo --minify

# Build con baseURL di produzione (Aruba)
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"

# Commit e push (pubblica)
git add .
git commit -m "descrizione breve"
git push origin main

# Rollback dell'ultimo commit (se qualcosa è andato storto)
git revert HEAD
git push origin main

# Lanciare il check manuale del manuale
gh workflow run aggiorna-manuale.yml
```

### Appendice D — Glossario

| Termine | Significato |
|---|---|
| **AGID** | Agenzia per l'Italia Digitale |
| **AIB** | Antincendio Boschivo |
| **ARPA** | Agenzia Regionale per la Protezione Ambientale |
| **Bootstrap Italia** | Framework CSS/JS ufficiale per siti PA italiani |
| **COC** | Centro Operativo Comunale |
| **CSS** | Cascading Style Sheets — linguaggio per lo stile delle pagine web |
| **DPC** | Dipartimento della Protezione Civile |
| **ETS** | Ente del Terzo Settore |
| **Fepivol** | Coordinamento regionale volontari PC Lazio |
| **Frontmatter** | Intestazione YAML in cima a ogni file `.md`, contiene metadati |
| **Hugo** | Generatore di siti statici usato per questo sito |
| **Markdown** | Linguaggio leggero di formattazione del testo (`**grassetto**`, `# Titolo`) |
| **NUE** | Numero Unico di Emergenza (il 112) |
| **OG (Open Graph)** | Metadata per le anteprime su social (Facebook, LinkedIn, ecc.) |
| **RUNTS** | Registro Unico Nazionale Terzo Settore |
| **SEO** | Search Engine Optimization |
| **Slug** | Versione URL-friendly di un titolo (`titolo-dell-articolo`) |
| **WCAG** | Web Content Accessibility Guidelines |
| **WebP** | Formato immagine moderno, più leggero di JPEG/PNG |

### Appendice E — Template pronti

Copia e incolla nel tuo nuovo file.

#### Template articolo breve (avviso o comunicazione)

```markdown
---
title: "Titolo breve e chiaro"
date: 2026-05-15
description: "Sommario in max 160 caratteri. Dice il fatto principale."
badge: "Avviso"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: ""
scadenza: ""
area: "Comune di Genzano di Roma"
allegati: []
draft: false
---

**Apertura in grassetto con il fatto principale.** Chi, cosa, dove, quando.

## Cosa succede

Descrizione breve.

## Cosa fare

- Prima azione.
- Seconda azione.
- Terza azione.

## Informazioni

Per chiedere informazioni: 06 9362 600 (segreteria).
```

#### Template articolo lungo (formazione o approfondimento)

```markdown
---
title: "Titolo descrittivo (max 80 caratteri)"
date: 2026-05-15
description: "Sommario SEO in max 160 caratteri."
badge: "Prevenzione"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-05-15-descrizione.webp"
scadenza: ""
area: "Comune di Genzano di Roma"
allegati:
  - titolo: "Checklist PDF (120 KB)"
    url: "/documenti/checklist.pdf"
draft: false
---

**Apertura forte in grassetto.** Il fatto principale in una frase chiara.

---

## Contesto

Breve inquadramento storico o normativo.

---

## Punto principale Paragrafo esplicativo. Frasi brevi, concetti chiari.

## Punto principale 2

Altro paragrafo.

---

## Cosa puoi fare tu

- Azione concreta 1.
- Azione concreta 2.
- Azione concreta 3.

---

## Numeri utili

- **112** — Numero unico di emergenza
- **06 9362 600** — Segreteria del Gruppo (informazioni non urgenti)

---

*Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma promuove la cultura
della prevenzione sul territorio.*
```

#### Template comunicato di emergenza

```markdown
---
title: "EMERGENZA: [descrizione breve]"
date: 2026-05-15
description: "Descrizione dell'emergenza in atto, con area e comportamenti da adottare."
badge: "Emergenza"
priorita: "urgente"
autore: "Gruppo Comunale Volontari PC Genzano"
image: ""
scadenza: ""
area: "Zona interessata"
allegati: []
draft: false
---

**In corso una situazione di emergenza in [zona].** [Una frase con il fatto principale.]

## Cosa sta succedendo

Descrizione fattuale, senza allarmismo. Solo informazioni verificate.

## Cosa fare subito

1. Azione immediata 1.
2. Azione immediata 2.
3. Chiama il **112** se vedi persone in pericolo.

## Aree interessate

- Zona 1
- Zona 2

## Aggiornamenti

Questo articolo viene aggiornato in tempo reale. Ultimo aggiornamento: ore HH:MM.

---

*Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma è attivo sul
territorio. Per emergenze chiama sempre il **112**.*
```

#### Template pagina

```markdown
---
title: "Titolo della pagina"
description: "Sommario SEO (max 160 caratteri)."
draft: false
---

Breve introduzione di una-due frasi.

## Sezione principale 1

Contenuto.

## Sezione principale 2

Contenuto.

## Contatti

Per informazioni su questa pagina: 06 9362 600 o [segreteria@protezionecivilegenzano.it](mailto:segreteria@protezionecivilegenzano.it).
```

### Appendice F — Errori comuni e come evitarli

| Errore | Conseguenza | Come evitarlo |
|---|---|---|
| `date: 2026-05-15T10:00:00Z` | Articolo escluso dalla build | Usa solo `date: 2026-05-15` |
| `draft: true` dimenticato | Articolo non pubblicato | Metti `draft: false` prima del push |
| Description > 160 caratteri | Troncata in Google/social | Verifica con `echo "..." | wc -m` |
| Badge inventato | Colore random (potrebbe cozzare) | Usa la tabella del Passo 1.2 |
| Immagine senza fascia blu | Incoerenza visiva | Segui Parte 3.8 |
| Immagine > 1 MB | Lentezza caricamento | Comprimi in WebP, max 200 KB |
| `+39069362600` nel testo | Illeggibile | Scrivi `06 9362 600` |
| "Cliccate qui" come link | Accessibilità violata | Testo descrittivo del link |
| H1 nel corpo | Gerarchia SEO rotta | H1 solo nel frontmatter, usa H2 nel corpo |
| Alt text "Foto di..." | Screen reader ridondante | Descrivi il contenuto, non il formato |
| `.docx` o `.pages` come allegato | Non tutti possono aprirli | Esporta sempre in PDF |
| Push con build rotto | Sito non aggiornato | Fai `hugo --minify` locale prima del push |

### Appendice G — Risorse esterne ufficiali

**Linee guida AGID e Designers Italia:**

- [designers.italia.it](https://designers.italia.it)
- [docs.italia.it/italia/designers-italia/](https://docs.italia.it/italia/designers-italia/)
- [Writing Toolkit](https://designers.italia.it/risorse-per-il-design/writing-toolkit/)
- [Manuale operativo design PA](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/)
- [Linee guida accessibilità AGID](https://www.agid.gov.it/it/design-servizi/accessibilita)

**Protezione civile:**

- [Dipartimento della Protezione Civile](https://www.protezionecivile.gov.it/)
- [Agenzia Regionale di Protezione Civile Lazio](https://www.regione.lazio.it/cittadini/protezione-civile)
- [Centro Funzionale Regionale Lazio](https://www.regione.lazio.it/rl/centrofunzionale/)
- [IT-alert](https://www.it-alert.it/)

**Framework e strumenti:**

- [Bootstrap Italia](https://italia.github.io/bootstrap-italia/)
- [Hugo](https://gohugo.io/)
- [GitHub Actions per Hugo](https://github.com/peaceiris/actions-hugo)

**Strumenti per immagini:**

- [Squoosh](https://squoosh.app) — conversione e compressione
- [Canva](https://canva.com) — editor online
- [GIMP](https://gimp.org) — editor desktop gratuito
- [Unsplash](https://unsplash.com) — foto libere CC0
- [Pexels](https://pexels.com) — foto libere CC0

**Verifica accessibilità:**

- [WAVE](https://wave.webaim.org/) — validatore accessibilità
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) — incluso in Chrome DevTools
- [axe DevTools](https://www.deque.com/axe/devtools/) — estensione browser

**Verifica SEO:**

- [Google Search Console](https://search.google.com/search-console)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)

---

_[Indice manuale](README.md)_

[← Parte 13 — Social Media Policy pubblica](parte-13-social-media-policy-pubblica.md) · [↑ Indice](README.md) · [Parte 15 — Homepage enhancements v1.0 (aprile 2026) →](parte-15-homepage-enhancements-v1-0-aprile-2026.md)
