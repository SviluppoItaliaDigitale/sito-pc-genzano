_[Indice manuale](README.md)_

# Parte 3 — Immagini per gli articoli

### 3.1 — Tipologie

| Tipo | Uso | Esempio |
|---|---|---|
| Foto originale | Resoconti attività, eventi, formazione | Foto dell'esercitazione, foto di gruppo |
| Foto di archivio | Articoli commemorativi, storici | Foto terremoto Aquila 2009 (da archivi pubblici) |
| Infografica | Articoli formativi, prevenzione | Triangolo del fuoco, kit di emergenza |
| Logo / Emblema | Articoli istituzionali | Logo DPC, logo Regione Lazio |
| Default | Articoli senza foto dedicata | `notizia-default.svg` (già in `static/images/`) |

### 3.2 — Diritti d'uso (obbligo)

Prima di pubblicare un'immagine, verifica che tu possa farlo:

- **Foto scattate da te o dal gruppo**: ✅ sempre OK.
- **Foto da banche immagini libere**: OK se sono **Creative Commons 0** (pubblico dominio)
  o CC BY (richiede attribuzione nel corpo dell'articolo).
- **Foto da siti istituzionali** (DPC, Regione, Comune): OK, con attribuzione.
- **Foto da Google Images, Facebook, stampa**: ❌ salvo che non sia chiaramente pubblicata
  con licenza libera. Rischio violazione copyright.

**Banche immagini consigliate (libere):**

- [Unsplash](https://unsplash.com) (CC0, attribuzione facoltativa)
- [Pexels](https://pexels.com) (CC0)
- [Pixabay](https://pixabay.com) (CC0)
- [Wikimedia Commons](https://commons.wikimedia.org) (varie licenze libere, sempre con attribuzione)

### 3.3 — Specifiche tecniche

| Parametro | Valore | Motivo |
|---|---|---|
| Formato | **WebP** (preferito), JPEG accettato, PNG per grafiche senza fotografia | WebP pesa il 30% meno di JPEG a pari qualità |
| Larghezza | **1200 px** (ideale), minimo 800 px | Standard Open Graph; non serve oltre 1200 su siti statici |
| Altezza | Automatica secondo proporzioni | |
| Proporzioni | **16:9** (1200×675) o **3:2** (1200×800), orizzontale | Compatibile con preview social |
| Dimensione file | **Max 200 KB** per WebP, max 300 KB per JPEG | Performance mobile |
| Risoluzione | 72 DPI (web) | Non serve più su monitor |
| Spazio colore | sRGB | Standard web |
| Nome file | `AAAA-MM-GG-descrizione-breve.webp`, minuscolo, trattini | Coerenza con articoli |
| Percorso | `static/images/` | Hugo serve tutto da qui |

**Da evitare:**

- File oltre 500 KB (anche in WebP): rallenta il caricamento su mobile.
- Nomi come `IMG_20260515_083042.webp` o `foto1.webp`: privi di contesto.
- PNG per fotografie: pesano 5-10 volte più di WebP.
- Immagini verticali (meno di 1:1): si troncano nelle preview.

### 3.4 — Come scattare una foto originale

Se fotografi tu o un collega:

- **Orizzontale** (landscape), smartphone ruotato.
- **Luce naturale** possibile. Evita controluce forte.
- **Soggetto centrale** o sulla regola dei terzi.
- **Inquadratura chiara**: non troppi elementi dispersivi.
- **Volti di persone**: chiedi il consenso per la pubblicazione online. Per minori, serve
  consenso scritto dei genitori.
- **Targhe automobili e volti non autorizzati**: offusca (strumento: GIMP, Photoshop, mobile app).

### 3.5 — Come cercare una foto libera

**Esempio: cerchi una foto di un pompiere in azione.**

1. Vai su [Unsplash](https://unsplash.com).
2. Cerca "firefighter action".
3. Apri un risultato, verifica la licenza (Unsplash License = utilizzo libero, anche commerciale).
4. Scarica la versione **Full resolution**.
5. Ridimensiona a 1200 px (vedi Passo 3.7).
6. Aggiungi la fascia blu (vedi 3.8).
7. Comprimi in WebP (vedi 3.9).

### 3.6 — Come editare: strumenti consigliati

Tre alternative, dalla più semplice alla più potente:

#### Canva (online, semplicissimo)

- Gratis con account: [canva.com](https://canva.com)
- Crea un design custom 1200×675 o 1200×800.
- Carica la tua foto, trascinala come sfondo.
- Usa il template "Fascia blu PC Genzano" se esistente, altrimenti creala (vedi 3.8).
- Scarica in PNG o JPG a qualità alta.

#### GIMP (desktop, gratis, potente)

- Gratis: [gimp.org](https://gimp.org)
- Apri la foto, `Immagine → Scala immagine` per portarla a 1200 px.
- Usa un template di fascia blu salvato in `.xcf` (modello GIMP), oppure crea un livello
  nuovo rettangolare in basso e riempilo di #003366.
- Esporta in WebP: `File → Esporta come → nome.webp`, qualità 80%.

#### Photoshop (desktop, a pagamento)

- Abbonamento Adobe Creative Cloud.
- Apri la foto, `Immagine → Dimensione immagine` per 1200 px.
- Usa un'azione registrata per applicare la fascia blu in un clic.
- Esporta con `File → Esporta → Salva per web → WebP`.

### 3.7 — Ridimensionare a 1200 px

#### GIMP

1. `Immagine → Scala immagine`.
2. Larghezza: **1200**, altezza si aggiorna automaticamente.
3. Interpolazione: **LoHalo** o **NoHalo** (ottima qualità).
4. `Scala`.

#### Riga di comando (ImageMagick)

```bash
# Installazione (Ubuntu/Debian)
sudo apt install imagemagick

# Ridimensionamento
convert originale.jpg -resize 1200x output.jpg
```

#### Online (caricare file, pochi clic)

- [Squoosh](https://squoosh.app) — Google, gratis, nessun account.

### 3.8 — Aggiungere la fascia blu istituzionale

Ogni immagine di copertina **deve** avere la fascia blu in basso. Identifica visivamente i
contenuti come ufficiali del Gruppo.

#### Specifiche della fascia

| Parametro | Valore |
|---|---|
| Posizione | In basso, a tutta larghezza |
| Altezza | **15-18% dell'altezza totale** (~105-125 px su immagine 1200×696) |
| Colore sfondo | `#003366` (variabile CSS `--pc-primary`) |
| Opacità sfondo | 85-90% |
| **Riga 1** | `PROTEZIONE CIVILE` |
| Font riga 1 | Sans-serif bold (Arial Black, Montserrat ExtraBold, DM Sans Bold) |
| Dimensione riga 1 | ~28-32 px (su immagine 1200 px larga) |
| Colore riga 1 | `#FFFFFF` |
| **Riga 2** | `Gruppo Comunale Volontari — Genzano di Roma` |
| Font riga 2 | Sans-serif regular (Arial, Montserrat, DM Sans) |
| Dimensione riga 2 | ~14-16 px |
| Colore riga 2 | `#FFFFFF`, opacità ~90% |
| **Logo** | `logo-pc-genzano.png` circolare |
| Dimensione logo | Altezza ~70-80 px, proporzionale |
| Posizione logo | Margine sinistro ~15 px, centrato verticalmente nella fascia |
| Posizione testo | A destra del logo, margine sinistro ~100 px dal bordo |

#### Schema visivo

```
+--------------------------------------------------+
|                                                  |
|              FOTO DELL'ARTICOLO                  |
|                                                  |
|                                                  |
+--------------------------------------------------+
| [LOGO]  PROTEZIONE CIVILE                       |
|         Gruppo Comunale Volontari — Genzano di R.|
+--------------------------------------------------+
  ^^^^    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  Logo    Testo bianco su sfondo #003366
```

#### Come applicarla: 3 metodi

##### Metodo 1 — Canva (più semplice)

1. Apri Canva, crea un design 1200×696.
2. Trascina la foto come sfondo, occupando l'intera area.
3. Aggiungi un **rettangolo** in basso: colore `#003366`, opacità 85%, altezza ~110 px.
4. Inserisci il logo (caricandolo come file personalizzato) a sinistra: altezza 75 px, margine
   sinistro 15 px.
5. Aggiungi testo "PROTEZIONE CIVILE" — bianco, bold, 30 pt.
6. Sotto: "Gruppo Comunale Volontari — Genzano di Roma" — bianco, regular, 15 pt.
7. Scarica in PNG alta qualità.
8. Converti in WebP (vedi 3.9).

##### Metodo 2 — GIMP

1. Apri la foto ridimensionata a 1200 px.
2. Crea un nuovo livello: `Livello → Nuovo livello`, tipo "Trasparenza".
3. Seleziona un rettangolo in basso con `Strumenti → Selezione rettangolare`, altezza ~110 px.
4. Riempi con colore `#003366` (strumento Riempimento).
5. Nel pannello livelli, imposta opacità 85%.
6. Inserisci il logo: `File → Apri come livelli → logo-pc-genzano.png`.
7. Ridimensiona il logo a altezza 75 px (`Livello → Scala livello`).
8. Spostalo a sinistra, centrato verticalmente nella fascia.
9. Aggiungi testo: `Strumenti → Testo`, scrivi "PROTEZIONE CIVILE", font Arial Bold 30 pt,
   bianco. Posizionalo a destra del logo.
10. Aggiungi secondo testo sotto: "Gruppo Comunale Volontari — Genzano di Roma", Arial Regular 15 pt.
11. `Immagine → Appiattisci immagine`.
12. `File → Esporta come → nome.webp` (qualità 80%).

##### Metodo 3 — AI generativa (prompt)

Se usi DALL-E, Midjourney, Canva AI, Photoshop Generative Fill:

> **Prompt:**
> "Aggiungi una fascia orizzontale in basso all'immagine, alta circa il 16% dell'altezza totale.
> Sfondo colore esadecimale #003366 con opacità 85%. A sinistra inserisci il logo circolare
> della Protezione Civile di Genzano di Roma (altezza ~75 px, margine sinistro ~15 px,
> centrato verticalmente). A destra del logo, testo bianco (#FFFFFF) su due righe:
> riga 1 'PROTEZIONE CIVILE' in grassetto maiuscolo grande (~30 px, font sans-serif bold),
> riga 2 'Gruppo Comunale Volontari — Genzano di Roma' in testo normale più piccolo
> (~15 px, font sans-serif regular). L'immagine finale deve essere 1200 px di larghezza
> proporzionata."

##### Metodo 4 — Script `applica-fascia-foto.sh` (raccomandato per le foto fornite dall'utente)

Per le **foto evento** (interventi, esercitazioni, formazione, ricorrenze) fornite in formato
grezzo (JPG/PNG/WebP), il repository include uno script riusabile che applica la fascia blu
in modo automatico e uniforme:

```bash
bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-estensione>
```

**Esempi reali:**

```bash
bash scripts/applica-fascia-foto.sh /home/utente/Scaricati/Zamberletti.jpg zamberletti-ritratto-istituzionale
bash scripts/applica-fascia-foto.sh /home/utente/Scaricati/Genzano-alto.jpg 2026-06-23-genzano-infiorata-aerea
```

**Cosa fa lo script:**

1. Ridimensiona la foto sorgente a **1200 px di larghezza** mantenendo il rapporto d'aspetto.
2. Aggiunge sotto la foto una **fascia blu `#003366` alta 100 px**.
3. Compone il **logo PC Genzano** (72×72) a sinistra e il testo istituzionale a due righe
   ("PROTEZIONE CIVILE" + "Gruppo Comunale Volontari — Genzano di Roma") a destra del logo.
4. Esporta come **WebP** qualità 85 (compressione `method=6`) in `static/images/<nome>.webp`.
5. Se il risultato supera i **200 KB** ricomprime automaticamente a qualità 75.

**Requisiti:**

- **Python 3 con Pillow** installato (`apt install python3-pil` su Ubuntu/Debian; `pip install Pillow` altrove). Lo script di composizione è scritto in Python+Pillow per essere cross-platform e indipendente da ImageMagick (motivazioni in `.claude/rules/05-github-aruba-deploy.md`).
- Il logo `static/images/logo-pc-genzano.png` deve essere presente (lo è già nel repository).
- I font Liberation (Liberation-Sans, Liberation-Sans-Bold) installati — di default sui sistemi
  Linux Ubuntu/Debian, normalmente disponibili via `apt install fonts-liberation`.

**Perché è raccomandato:**

- Uniformità grafica con tutte le foto precedenti (stessa fascia, stesso logo, stessa tipografia).
- Zero passaggi manuali in Canva/GIMP per il trattamento di routine.
- Nome file di output sotto controllo: passa un nome **diverso dallo slug dell'articolo**
  (vedi Parte 3.13) per evitare che `genera-cover.py` sovrascriva la foto con una copertina
  tipografica.

**Differenza con `scripts/genera-cover.py`:**

| Script | Quando usarlo | Input | Output |
|---|---|---|---|
| `genera-cover.py` | Copertine automatiche tipografiche (gradiente + titolo + badge) | Solo il file `.md` dell'articolo | `static/images/<slug>.webp` |
| `applica-fascia-foto.sh` | Foto evento reali fornite dall'utente | Foto sorgente + nome output | `static/images/<nome>.webp` |

### 3.9 — Convertire in WebP e comprimere

Target: **max 200 KB**.

#### Online (facile)

- [Squoosh](https://squoosh.app): trascina l'immagine, scegli WebP, qualità 75-80%,
  scarica.

#### Riga di comando

```bash
# Installazione
sudo apt install webp

# Conversione
cwebp -q 80 originale.png -o nome.webp

# Verifica dimensione
ls -lh nome.webp
```

Se la dimensione supera 200 KB:

```bash
cwebp -q 70 originale.png -o nome.webp
```

Scendi con la qualità fino a rientrare. Sotto q=60 la qualità inizia a calare visibilmente.

### 3.10 — Alt text (obbligatorio per ogni immagine)

L'alt text è il testo alternativo letto dagli screen reader e mostrato se l'immagine non
carica. È obbligatorio per **accessibilità**.

| Tipo immagine | Alt text |
|---|---|
| Foto informativa | Descrive il soggetto: "Volontari al lavoro nel campo di accoglienza di Fossa dopo il terremoto 2009" |
| Infografica | Descrive il dato principale: "Diagramma del triangolo del fuoco: combustibile, comburente, innesco" |
| Logo | Nome dell'ente: "Logo della Protezione Civile di Genzano di Roma" |
| Ritratto | Nome e ruolo: "Giuseppe Zamberletti, primo Ministro per la Protezione Civile" |
| Puramente decorativa | Alt vuoto: `alt=""` |

**Regole:**

- Mai "Immagine di...", "Foto di...", "Grafica che mostra...".
- Mai ridondante con la didascalia o il testo adiacente.
- Massimo ~120 caratteri.
- In italiano corretto (anche se l'immagine è di fonte estera).

**Nel frontmatter** (immagine di copertina): l'alt text viene generato automaticamente dal
titolo dell'articolo.

**Nel corpo** (immagini inline in Markdown):

```markdown
![Volontari al lavoro a Fossa dopo il terremoto 2009](/images/2009-04-fossa-volontari.webp)
```

Parentesi quadre = alt text, parentesi tonde = URL.

### 3.11 — Dove salvare nel repository

```
static/
└── images/
    ├── AAAA-MM-GG-descrizione-articolo.webp   ← immagini di copertina
    ├── logo-pc-genzano.png                     ← logo (non toccare)
    ├── notizia-default.svg                     ← fallback (non toccare)
    └── og-default.png                          ← OG di default (non toccare)
```

### 3.12 — Checklist immagine

- [ ] Formato WebP (preferito) o JPEG/PNG
- [ ] Larghezza 1200 px
- [ ] Proporzioni orizzontali (16:9 o 3:2)
- [ ] Dimensione file sotto 200 KB
- [ ] Fascia blu istituzionale presente
- [ ] Logo PC Genzano nella fascia
- [ ] Testo "PROTEZIONE CIVILE" + "Gruppo Comunale Volontari — Genzano di Roma"
- [ ] Nome file `AAAA-MM-GG-descrizione.webp`
- [ ] Salvata in `static/images/`
- [ ] Diritti di pubblicazione verificati
- [ ] Alt text definito (nel frontmatter o nel Markdown)

### 3.13 — Copertina automatica (tipografica) vs foto evento

Il sito distingue **due tipi** di immagine per articolo:

**1. Copertina automatica (tipografica)** — generata dallo script `scripts/genera-cover.py`
che produce una grafica istituzionale con gradiente blu, titolo dell'articolo, badge
colorato e fascia blu con logo. È associata automaticamente al frontmatter tramite
`scripts/aggiorna-image-frontmatter.py`. Nome file: identico allo slug dell'articolo,
es. `2026-04-15-frana-costone-nemi-chiusura-via-nemorense.webp`.

**2. Foto evento (contenuto redazionale)** — forniscono testimonianza fotografica reale
di un intervento, attività, formazione. Vanno sempre **inserite nel corpo dell'articolo**,
non sostituiscono la copertina.

Regole per le foto evento:
- Nome file: `AAAA-MM-GG-descrizione-specifica.webp`, con descrizione **diversa dallo slug**
  (così `genera-cover.py` non le sovrascrive).
- Devono comunque avere la **fascia blu istituzionale** (vedi Parte 3.8). Per trattarle in
  modo uniforme e rapido usa lo script `scripts/applica-fascia-foto.sh` (Parte 3.8, Metodo 4).
- Si inseriscono con lo shortcode `foto` — mai con markdown `![...]()` diretto.

### 3.14 — Shortcode `foto` (click per ingrandire)

Lo shortcode `foto` inserisce un'immagine nel corpo dell'articolo con click-per-ingrandire
accessibile da tastiera, `<figure>`/`<figcaption>` semantici, alt text obbligatorio e
didascalia opzionale.

**Sintassi:**

```go-html-template
{{< foto src="/images/AAAA-MM-GG-descrizione.webp"
         alt="Descrizione significativa dell'immagine per screen reader"
         caption="Didascalia visibile sotto la foto (opzionale)." >}}
```

**Parametri:**

| Parametro | Obbligatorio | Descrizione |
|---|---|---|
| `src` | sì | Percorso dell'immagine in `/images/...` |
| `alt` | sì | Testo alternativo per screen reader. Mai "immagine di..." |
| `caption` | no | Didascalia visibile. Supporta markdown inline. |

**Comportamento:**

- L'immagine è cliccabile: si apre a dimensione intera in una **nuova scheda**.
- Il link ha `aria-label` descrittivo per screen reader.
- `loading="lazy"` per performance.
- Responsive (`img-fluid` di Bootstrap Italia).
- Nessun JavaScript richiesto: funziona con tastiera, screen reader, e anche con JS
  disattivato.

**Esempio reale:**

```go-html-template
{{< foto src="/images/2026-04-20-incendio-cecchina-casolare-spegnimento.webp"
         alt="Casolare dopo le operazioni di spegnimento a Cecchina"
         caption="Il casolare dopo le operazioni di spegnimento e messa in sicurezza." >}}
```

**Quando usare lo shortcode vs markdown:**

- **Shortcode `foto`**: per tutte le foto evento (interventi, formazione, attività,
  ricorrenze con foto reali). Sempre.
- **Markdown `![alt](src)`**: solo per icone o immagini puramente decorative inline,
  quando non serve l'ingrandimento.

### 3.15 — Tipografia del corpo articolo (`.article-body` v7.2)

Le pagine `single` degli articoli avvolgono il contenuto in
`<article class="article-body">` (template `themes/flavour-pcgenzano/layouts/_default/single.html`).
Il blocco CSS **v7.2** in `themes/flavour-pcgenzano/static/css/custom.css` applica a questo
wrapper una tipografia istituzionale curata che non influisce su homepage, liste, card o widget.

**Cosa applica automaticamente:**

| Elemento | Trattamento |
|---|---|
| Base | `font-size: 1.05rem`, `line-height: 1.75`, colore `#1a1a1a` (contrasto massimo) |
| Primo paragrafo (`lede`) | `font-size: 1.15rem`, colore `#003366`, `font-weight: 500` |
| Capolettera | Prima lettera del primo paragrafo: `3rem`, blu `#003366`, float left |
| `<h2>` | Barra blu `3px` a sinistra, `margin-top: 2.5rem`, colore `#003366`, bold |
| `<h3>` / `<h4>` | Colore `#003366`, peso 600, spaziatura ridotta |
| `<ul>` / `<ol>` | `::marker` blu `#003366`, spaziatura voci `0.4rem` |
| `<blockquote>` | Bordo sinistro blu `4px`, sfondo `#f4f7fb`, corsivo, bordi arrotondati |
| `<figure>` | Max-width `640px`, ombra morbida `rgba(0,51,102,0.12)`, cornice sottile |
| `<figcaption>` | Corsivo blu `#003366`, centrato, `0.925rem` |
| `<a>` (non `.btn`) | Colore blu, `underline` 1 px, 2 px al hover/focus |
| `<table>` | Header blu `#003366` su bianco, zebra leggera `#f8f9fb`, border-collapse |
| `<hr>` | Sfumatura orizzontale blu (decorativa, utile prima di "Riferimenti") |
| `<code>` inline | Sfondo `#f4f7fb`, colore blu, padding 0.1×0.35rem |

**Regole di override integrate:**

- `@media (max-width: 768px)`: riduce il capolettera, comprime le spaziature degli H2, regola
  la dimensione della `lede`.
- `@media (prefers-reduced-motion: reduce)`: disattiva la transizione sull'underline dei link.
- `@media print`: azzera capolettera, ombre, gradienti e sfondi colorati. Mantiene la
  gerarchia visiva in bianco e nero con bordi grigi e colori neutri — il risultato stampato è
  leggibile e sobrio.

**Cosa devi fare tu come redattore:**

- **Niente**: la tipografia si applica automaticamente a qualsiasi articolo in `content/comunicazioni/`.
- **Non introdurre stili inline** nel Markdown (tipo `<span style="color:...">`): il tema li
  sovrascriverà o li renderà incoerenti con la linea visiva.
- **Non usare `<h1>` nel corpo**: il titolo pagina è già `<h1>`, il corpo parte da `<h2>`.
- **Il primo paragrafo conta**: per sfruttare il rendering della *lede* e del capolettera,
  fai in modo che il primo paragrafo sia un vero incipit di senso compiuto (almeno 2 frasi),
  non una singola parola o un'immagine.
- **I `<blockquote>`** sono per **citazioni testuali** (dichiarazioni ufficiali, estratti di
  norme, slogan istituzionali). Non per qualsiasi paragrafo da evidenziare.

**Compatibilità:**

- Conforme **WCAG 2.2 AA**: tutti i colori testo/sfondo superano il rapporto 4.5:1.
- Nessuna informazione veicolata solo dal colore.
- Rispetta `prefers-reduced-motion` e `prefers-contrast` (base Bootstrap Italia).
- Stampa pulita: header/navbar/footer sono già nascosti dal blocco `@media print` globale
  (vedi Parte 1.10).

### 3.16 — Pittogrammi (ISO 7010 + ARASAAC)

Il sito ha una **libreria di pittogrammi standardizzati** per supportare la comprensione del testo a **bambini, anziani, persone con disabilità cognitive e parlanti italiano L2** (regola di accessibilità cognitiva, WCAG 2.2 — sezione 1.4 Distinguishable + 3.1 Readable).

**Cosa contiene la libreria:**

| Tipo | Cartella | Numero | Formato | Fonte / licenza |
|---|---|---|---|---|
| ISO 7010 (sicurezza standard) | `static/pittogrammi/iso7010/` | 46 | SVG vettoriale | Wikimedia Commons (PD-shape / CC0) |
| ARASAAC (comprensione cognitiva) | `static/pittogrammi/arasaac/` | 125 | PNG 500 px | ARASAAC, autore Sergio Palao, CC BY-NC-SA 4.0 |

ISO 7010 copre evacuazione (E*), antincendio (F*), avvertimento (W*), obbligo (M*), divieto (P*).
ARASAAC copre eventi e rischi naturali, azioni di autoprotezione, oggetti del kit di emergenza, persone, luoghi, segnali, veicoli e numeri utili.

**Re-download della libreria** (idempotente, scarica solo i mancanti):

```bash
bash scripts/scarica-pittogrammi.sh           # solo i mancanti
bash scripts/scarica-pittogrammi.sh --force   # ri-scarica tutto
```

Lo script ha un rate-limit di 1 secondo tra le richieste a Wikimedia per evitare ban temporanei.
Per aggiungere nuovi pittogrammi alla libreria, modifica gli array `ISO7010` e `ARASAAC` in cima allo script (formato `codice|nome-file|descrizione`).

**Uso negli articoli e nelle pagine — shortcode `pittogramma`:**

Uso block (figure centrata, con didascalia opzionale):

```go-html-template
{{< pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto"
                size="large" >}}
```

Uso inline (dentro una frase, dimensione adattata al testo):

```go-html-template
Chiama subito il {{< pittogramma src="/pittogrammi/arasaac/112.png" alt="numero 112" inline="true" >}} 112.
```

Parametri:
- `src` (**obbligatorio**) — percorso del pittogramma in `/pittogrammi/iso7010/...` o `/pittogrammi/arasaac/...`
- `alt` (**obbligatorio**) — testo alternativo significativo per screen reader. **Mai stringa vuota**: il pittogramma è esplicativo, non decorativo
- `caption` (opzionale, solo modalità block) — didascalia visibile sotto
- `inline="true"` — inserimento inline dentro una frase (default: block)
- `size` — `small` (48 px), `medium` (96 px, default), `large` (160 px), `xlarge` (240 px)

**Regole editoriali per l'uso dei pittogrammi:**

1. **Mai sostituire il testo con il solo pittogramma**: il pittogramma è di **supporto** alla comprensione, mai sostituto. WCAG 1.4.5 (Images of Text) e principio di leggibilità per L2.
2. **Un pittogramma per concetto chiave**, non come decorazione visiva continua. La sovrabbondanza riduce l'efficacia comunicativa per gli utenti che ne hanno davvero bisogno.
3. **Per segnali di sicurezza** (obblighi, divieti, avvertimenti formali): preferire i simboli **ISO 7010** (riconoscibili a livello internazionale).
4. **Per situazioni narrative o didattiche** rivolte a bambini: preferire **ARASAAC** (colore e tratto più immediati).
5. **Alt text sempre descrittivo**: mai "Immagine di...", "Pittogramma di..." in modo generico. Esempio buono: `alt="Persona che si nasconde sotto al tavolo in caso di terremoto"`.

**Attribuzioni — obbligatorie:**

- Il footer di tutte le pagine linka alla pagina **`/attribuzioni-pittogrammi/`** che riporta autori, licenze e fonti.
- ARASAAC è **CC BY-NC-SA 4.0**: le opere derivate (in particolare le **schede stampabili PDF** dei kit didattici) che includono pittogrammi ARASAAC ereditano automaticamente la stessa licenza CC BY-NC-SA 4.0.
- Quando produci una scheda stampabile che usa pittogrammi ARASAAC, indica nel piè di pagina della scheda: *"Pittogrammi: ARASAAC — Sergio Palao (CC BY-NC-SA 4.0). Distribuita con la stessa licenza."*

**Tecnica e accessibilità:**

- Lo shortcode emette `<img>` con `role="img"` e `loading="lazy"`, oppure `<figure>` con `<figcaption>` opzionale.
- CSS scoped in `themes/flavour-pcgenzano/static/css/custom.css` (sezione **PITTOGRAMMI v1.0**): dimensioni fisse, override mobile (large/xlarge ridotti su <576 px), mantenimento dei colori in stampa (i colori dei segnali ISO 7010 sono parte dell'informazione di sicurezza e non devono essere convertiti in scala di grigi).

### 3.17 — Shortcode `chi-chiamare` (chiusura pagine rischio)

Sezione finale standardizzata delle 7 pagine `/rischi-prevenzione/*` con tabella accessibile dei numeri da chiamare per livello di gravità + nota istituzionale.

**Uso:**

```go-html-template
{{< chi-chiamare >}}
```

Nessun parametro. Va aggiunto **sempre alla fine** della pagina, dopo `{{< cosa-non-fare >}}`.

**Cosa produce:**

- `<h2>` "Chi chiamare"
- Tabella accessibile: 3 righe (vita in pericolo → 112, pericolo concreto → 112, segnalazione non urgente → 803 555 Sala Operativa PC Lazio) con `<caption>` + `<th scope="col">`.
- Numero 112 cliccabile via `<a href="tel:112">` (mobile).
- Alert role=note con il chiarimento: *"Il Gruppo Comunale non può essere attivato direttamente dai cittadini"*.

**Quando usarlo:** **sempre** sulle pagine rischio operative (le 7 attuali + eventuali nuove). **Non** sulle pagine di supporto (`kit-emergenza.md`, `persone-necessita-specifiche.md`).

**Struttura uniforme finale di ogni pagina rischio (ordine non negoziabile):**

1. Perché è rilevante sul nostro territorio
2. Segnali e situazioni tipiche (opzionale)
3. Cosa fare PRIMA
4. Cosa fare DURANTE
5. Cosa fare DOPO
6. `{{< cosa-non-fare >}}`
7. `{{< chi-chiamare >}}`  ← chiusura standard

CSS scoped in `custom.css` sezione **CHI CHIAMARE BOX v1.0**.

### 3.18 — Tabelle accessibili (render hook automatico)

Tutte le tabelle Markdown del sito sono rese dal **render hook universale** `themes/flavour-pcgenzano/layouts/_default/_markup/render-table.html`. Comportamento automatico:

- **`<th scope="col">`** su ogni cella di intestazione (riga `<thead>`) — WCAG 1.3.1 (Info and Relationships).
- **Wrapping in `.table-responsive`** Bootstrap Italia per scroll orizzontale su mobile.
- **Allineamento colonne** preservato dal Markdown (`:---`, `---:`, `:---:`).

**Quando scrivi una nuova tabella in Markdown** non devi fare nulla di particolare: la sintassi standard è sufficiente.

```markdown
| Numero | Servizio | Quando chiamare |
|---|---|---|
| 112 | NUE | Qualsiasi emergenza |
```

Il render hook genera automaticamente:

```html
<div class="table-responsive">
<table>
<thead>
<tr><th scope="col">Numero</th><th scope="col">Servizio</th>...</tr>
</thead>
...
```

#### Quando aggiungere `<caption>` esplicito

Per le **tabelle landing critiche** (`/contatti/`, `/numeri-utili/`, `/chi-siamo/` e in futuro `/cartografia/`) è raccomandato un `<caption>` che descriva lo scopo della tabella (WCAG 2.4.6).

**Limitazione tecnica:** la sintassi attribute block di Goldmark `{caption="..."}` **non funziona** sulle tabelle Markdown in Hugo. Soluzione: convertire la tabella in **HTML diretto** dentro Markdown:

```html
<div class="table-responsive">
<table>
<caption>Numeri di emergenza validi nel Lazio: quale chiamare e in quali casi</caption>
<thead>
<tr><th scope="col">Numero</th><th scope="col">Servizio</th></tr>
</thead>
<tbody>
<tr><td><strong>112</strong></td><td>Numero Unico Emergenze</td></tr>
</tbody>
</table>
</div>
```

Per tabelle in cui il `<caption>` sarebbe ridondante visivamente (c'è già un card-header sopra), usare `class="visually-hidden"` sul caption: nasconde visivamente ma resta accessibile.

CSS scoped in `custom.css` sezione **TABLE CAPTION v1.0**.

### 3.19 — FAQ accordion (`.faq-item`)

Per ridurre muri di testo in pagine con molte domande/risposte (es. `/allerte-meteo/`, `/faq/`), il sito ha una classe `.faq-item` che stilizza l'elemento HTML nativo `<details>`/`<summary>` come accordion accessibile.

```html
<details class="faq-item">
<summary><strong>Domanda concisa</strong></summary>

Risposta in **Markdown** standard. Bullet, link, enfasi.

</details>
```

Vantaggi:
- **Semantica nativa**: zero JS, zero ARIA hand-rolled.
- **Tastiera**: Enter/Space su `<summary>` apre/chiude.
- **Stampa**: tutti i `<details>` aperti automaticamente, niente chevron.
- **Mobile**: padding ridotto su <576 px.

CSS scoped in `custom.css` sezione **FAQ ACCORDION v1.0**.

### 3.20 — Striscia pittogrammi (`.kit-pittogrammi-row`)

Riga visiva di pittogrammi inline ARASAAC per dare un colpo d'occhio immediato a una pagina lista (es. `/rischi-prevenzione/kit-emergenza/`).

```html
<div class="kit-pittogrammi-row" role="img" aria-label="Componenti essenziali del kit di emergenza: zaino, acqua, cibo, torcia, radio, medicine">
{{< pittogramma src="/pittogrammi/arasaac/zaino.png" alt="Zaino" size="small" inline="true" >}}
{{< pittogramma src="/pittogrammi/arasaac/acqua.png" alt="Acqua" size="small" inline="true" >}}
...
</div>
```

**Regola accessibilità:** `role="img"` + `aria-label` complessivo sul wrapper (gli screen reader leggono la striscia come **una sola immagine descrittiva** invece di leggere ogni `alt` singolo). I pittogrammi all'interno sono `size="small"` (48 px) e `inline="true"` per evitare il layout `<figure>` block.

CSS scoped in `custom.css` sezione **STRISCIA PITTOGRAMMI v1.0**.

---

_[Indice manuale](README.md)_

[← Parte 02 — Le regole AGID in dettaglio](parte-02-le-regole-agid-in-dettaglio.md) · [↑ Indice](README.md) · [Parte 04 — Scrivere una pagina (diverso da articolo) →](parte-04-scrivere-una-pagina-diverso-da-articolo.md)
