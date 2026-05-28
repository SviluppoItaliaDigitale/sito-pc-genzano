_[Indice manuale](README.md)_

# Parte 34 — Catalogo dei giochi (`/catalogo-giochi/`)

Da maggio 2026 il sito ha la sezione `/catalogo-giochi/`, **catalogo informativo** dei 33 giochi educativi della sicurezza. Affianca — non sostituisce — l'**Arena PC Genzano** (`/giochi/`), la webapp interattiva con badge e progressi.

Questa parte del manuale spiega cosa contiene il catalogo, perché esiste in parallelo all'Arena, come è generato dal manifest del Coach come fonte unica di verità, e come aggiungere o modificare una scheda.

---

## 34.1 Cosa è il catalogo e perché esiste

Il **catalogo dei giochi** è la pagina istituzionale informativa di ogni gioco. Per ogni gioco contiene una **scheda Markdown** con frontmatter AGID, breadcrumb, descrizione didattica, indicazioni di accessibilità, riferimenti normativi per l'Educazione Civica e un bottone CTA che apre il gioco interattivo.

L'**Arena PC Genzano** (`/giochi/`) è invece il **launcher interattivo**: griglia colorata, sistema di badge, progressi salvati nel browser, skin selezionabili. È pensata per chi vuole giocare subito.

| Pagina | Pubblico tipico | Vincoli tecnici |
|---|---|---|
| `/giochi/` (Arena) | Bambini, ragazzi, famiglie che vogliono **giocare subito** | Webapp HTML+JS statica, richiede browser moderno |
| `/catalogo-giochi/` (catalogo) | **Docenti, genitori, motori di ricerca, screen reader user** che vogliono capire prima di giocare | Pagina Hugo istituzionale, WCAG 2.2 AA, AGID, indicizzabile |

Le due pagine si linkano a vicenda: l'Arena ha un bottone "Vai al catalogo informativo dei giochi" sotto la lead; il catalogo ha un richiamo all'Arena nel paragrafo di apertura.

**Perché esiste questa duplicazione:** l'audit ChatGPT del 28 maggio 2026 ha rilevato che i giochi erano accessibili solo come webapp JS in `static/giochi/`, senza una pagina informativa per docenti, genitori e motori di ricerca. La webapp è ottima per chi gioca, ma non basta per chi cerca di **capire** cosa offre il sito e con quale valore didattico. La scheda del catalogo riempie quel buco.

---

## 34.2 Struttura della pagina hub `/catalogo-giochi/`

Hub `content/catalogo-giochi/_index.md` con `layout: "list"`. Contiene:

1. **Intro** che spiega cosa è il catalogo e rimanda all'Arena
2. **Indice per fascia** con ancore di sezione:
   - `#infanzia` (10 giochi, 3-6 anni)
   - `#primaria` (13 giochi, 6-11 anni)
   - `#ragazzi` (10 giochi, 11-19 anni e oltre)
3. Per ogni fascia: durata media, lingua, lista di tutti i giochi con:
   - nome del gioco (link alla scheda)
   - prima riga della regola
   - doppio link "Apri la scheda" + "Gioca subito"
4. **Per i docenti** — riferimento al D.M. 183/2024 (Educazione Civica) + link interni a percorsi didattici e schede stampabili
5. **Accessibilità complessiva** — riassunto degli standard rispettati

---

## 34.3 Struttura uniforme di ogni scheda gioco

Ogni scheda `content/catalogo-giochi/<slug>.md` segue **dieci sezioni AGID** in ordine fisso:

| # | Sezione | Contenuto |
|---|---|---|
| 1 | Intro istituzionale | "**Nome** è un gioco educativo gratuito del **Gruppo Comunale Volontari** di PC Genzano…" — Gruppo come soggetto |
| 2 | A chi è rivolto | Fascia, età, durata, modalità, lingua |
| 3 | In una frase | Blockquote con la **regola** dal manifest del Coach |
| 4 | Come si gioca | Lista numerata dai bullet `come` del manifest |
| 5 | Apri il gioco interattivo | CTA shortcode `bottone-gioco` che linka a `/giochi/<fascia>/<slug>/` |
| 6 | Approfondisci sul sito | Linkografia interna dal campo `teoria` del manifest |
| 7 | Accessibilità | WCAG 2.2 AA, tastiera, TTS, pittogrammi ISO 7010 / ARASAAC, contrasto, focus, `prefers-reduced-motion` |
| 8 | Per i docenti | Riferimento D.M. 183/2024 (Educazione Civica, 33 ore annuali) + link interni |
| 9 | Licenza | CC BY-NC-SA 4.0, con clausola pittogrammi ARASAAC |
| 10 | Altri giochi della stessa fascia | Link al filtro `/catalogo-giochi/#<fascia>` |

**Tono:** descrittivo-funzionale, **non narrativo**. La scheda è un riferimento istituzionale, non un racconto. Il gate AGID standard `pc-article-reviewer` va invocato sulle modifiche **al testo libero** delle schede, non sulle parti generate dal manifest (regola, come, teoria — viene tutto direttamente dal Coach).

---

## 34.4 Frontmatter AGID

Esempio dalla scheda `acchiappa-pericolo.md`:

```yaml
---
title: "Gioco: Acchiappa il Pericolo"
description: "Scheda del gioco Acchiappa il Pericolo (3-6 anni): tocca SOLO le cose pericolose."
image: ""
image_alt: ""
date: 2026-05-28
draft: false
type: "catalogo-giochi"
layout: "single"
toc: false
tts: true
fascia: "infanzia"
fascia_eta: "3-6 anni"
fascia_label: "Infanzia"
durata: "circa 5 minuti"
gioco_url: "/giochi/infanzia/acchiappa-pericolo/"
gioco_slug: "acchiappa-pericolo"
tags: ["giochi", "infanzia", "educazione-civica", "scuola"]
sitemap:
  priority: 0.55
  changefreq: monthly
---
```

**Note critiche:**

- `image: ""` + `image_alt: ""` vuoti: la cover tipografica banner viene generata automaticamente da `scripts/auto-cover-mancanti.py` al prossimo deploy (rule 09 § 9, divieto banner col titolo intoccabile).
- `gioco_url` punta al gioco interattivo statico: il render-link hook gestisce correttamente il subpath GitHub Pages (rule 04a § render-link-hook).
- `type: "catalogo-giochi"` permette in futuro di personalizzare il template `_default/single.html` con uno specifico `catalogo-giochi/single.html` (oggi non serve, il default basta).
- `tags` array YAML inline: forma `["giochi", "<fascia>", "educazione-civica", "scuola"]`.

---

## 34.5 Fonte unica di verità: il manifest del Coach

🟢 **Le 33 schede non sono scritte a mano.** Sono generate da `static/giochi/assets/js/coach.js`, dove vive il manifest `CONTENUTI` con:

- `titolo` → nome umano del gioco (es. *"Consigli per Acchiappa il Pericolo"* → *"Acchiappa il Pericolo"*)
- `fascia` → `"infanzia"` | `"primaria"` | `"ragazzi"`
- `regola` → frase chiave (va in *"In una frase"* della scheda)
- `come` → lista bullet (va in *"Come si gioca"*)
- `teoria` → lista `{titolo, url}` (va in *"Approfondisci sul sito"*)

**Perché questa scelta:** il manifest era **già curato** dal Gruppo per il bottone "💡 Consigli per giocare" presente in ogni gioco. Riusarlo come fonte per le schede del catalogo significa: (a) niente informazioni inventate, (b) coerenza automatica fra Coach e scheda, (c) un solo posto da aggiornare se cambia la regola di un gioco.

**Procedura di rigenerazione completa:**

```bash
# 1. estrai il manifest da coach.js → JSON
node /tmp/dump-coach-manifest.js > /tmp/coach-manifest.json

# 2. genera le 33 schede + hub
python3 /tmp/genera-schede-giochi.py
```

I due script (`dump-coach-manifest.js` e `genera-schede-giochi.py`) **non sono nel repo** perché eseguibili da Claude Code on-demand quando serve rigenerare. Sono documentati qui sotto in 34.7 e 34.8 per riferimento.

---

## 34.6 Aggiungere un nuovo gioco al sito (workflow completo)

Quando aggiungi un nuovo gioco interattivo al sito, segui questi sei passi:

1. **Crea la webapp del gioco** in `static/giochi/<fascia>/<slug>/index.html` (con assets correlati). Convenzione standard del repo: `<body data-coach-game="<slug>">` + `<link rel="stylesheet" href="/giochi/assets/css/coach.css">` + `<script src="/giochi/assets/js/coach.js" defer></script>`.
2. **Aggiungi una voce al manifest `CONTENUTI`** in `static/giochi/assets/js/coach.js`:
   ```js
   '<slug>': {
     fascia: 'infanzia' | 'primaria' | 'ragazzi',
     titolo: 'Consigli per <Nome umano>',
     regola: 'Frase chiave del gioco.',
     come: [
       'Bullet 1.',
       'Bullet 2.',
       'Bullet 3.'
     ],
     teoria: [
       { titolo: 'Pagina del sito pertinente', url: '/percorso/' }
     ]
   },
   ```
3. **Aggiungi il gioco all'Arena** in `static/giochi/index.html` (griglia di card).
4. **Rigenera la scheda del catalogo** con i due script di 34.5: a quel punto compare una nuova `content/catalogo-giochi/<slug>.md` e l'hub viene aggiornato automaticamente con il nuovo gioco nella sezione di fascia corretta.
5. **Verifica con `pc-article-reviewer`** (sulla nuova scheda + sull'hub aggiornato).
6. **Commit + push + PR + merge.** Al deploy, il workflow `scarica-foto-automatica.yml` step 2 genererà la cover tipografica banner automaticamente.

⚠️ **Non bypassare il passo 2 (manifest)**: se aggiungi il gioco senza voce nel Coach, il bottone "💡 Consigli per giocare" non avrà contenuto e il sistema Layer 3 (hint contestuale sugli errori) non funzionerà.

---

## 34.7 Lo script `dump-coach-manifest.js`

Estrae l'oggetto `CONTENUTI` da `coach.js` eseguendolo in un sandbox `vm` di Node.js, e lo stampa come JSON su stdout. Niente modifiche al file originale. Richiede Node ≥ 14.

```javascript
const fs = require('fs');
const vm = require('vm');

const src = fs.readFileSync('/home/user/sito-pc-genzano/static/giochi/assets/js/coach.js', 'utf8');
const match = src.match(/var\s+CONTENUTI\s*=\s*(\{[\s\S]*?\n\s*\};)/);
if (!match) { console.error('Manifest non trovato'); process.exit(1); }

const sandbox = { CONTENUTI: null };
vm.createContext(sandbox);
vm.runInContext('CONTENUTI = ' + match[1].replace(/;$/, ''), sandbox);
console.log(JSON.stringify(sandbox.CONTENUTI, null, 2));
```

**Perché Node e non Python:** il manifest usa apostrofi italiani nelle stringhe (`"Tina la Tartaruga"` con `'`), template letterali, e sintassi JS pulita. Parsare con regex Python è fragile; eseguire come JS in un sandbox è sicuro e robusto.

---

## 34.8 Lo script `genera-schede-giochi.py`

Legge il JSON prodotto da 34.7 e genera le 33 schede + l'hub. La logica è:

1. **Pulisce il titolo:** rimuove i prefissi `Consigli per ` e `Consigli con `, capitalizza la prima lettera se serve.
2. **Compone la description AGID** (≤ 160 char) con il nome del gioco + fascia + prima frase della regola.
3. **Scrive il frontmatter** con tutti i campi di 34.4.
4. **Costruisce il corpo Markdown** in 10 sezioni fisse, usando i campi `regola`, `come` e `teoria` del manifest.
5. **Genera l'hub** raggruppando i giochi per fascia, con ancore `#infanzia`, `#primaria`, `#ragazzi`.

**Mappatura fascia → metadata:**

| Fascia | Età | Durata stimata | Scuola | Lingua |
|---|---|---|---|---|
| infanzia | 3-6 anni | circa 5 minuti | scuola dell'infanzia | italiano semplice |
| primaria | 6-11 anni | circa 10 minuti | scuola primaria | italiano standard |
| ragazzi | 11-19 anni e oltre | circa 15 minuti | scuola secondaria di primo e secondo grado | italiano standard |

La mappatura è dentro il dict `FASCIA_META` dello script: per cambiare durate o etichette basta editarlo e rilanciare.

---

## 34.9 Shortcode `bottone-gioco`

Il CTA "Apri il gioco" è uno shortcode dedicato in `themes/flavour-pcgenzano/layouts/shortcodes/bottone-gioco.html`:

```go-html-template
{{- $url := .Get "url" | strings.TrimPrefix "/" | relURL -}}
{{- $testo := .Get "testo" -}}
<p class="bottone-gioco-wrap">
  <a class="btn btn-primary btn-lg" href="{{ $url }}" role="button"
     aria-label="{{ $testo }} (si apre nella stessa scheda)">
    <i class="bi bi-play-circle-fill me-2" aria-hidden="true"></i>{{ $testo }}
  </a>
</p>
```

**Uso nelle schede:**

```markdown
{{< bottone-gioco url="/giochi/infanzia/acchiappa-pericolo/" testo="Apri «Acchiappa il Pericolo»" >}}
```

**Perché non Markdown puro con attribute syntax:** Goldmark in Hugo non supporta `{.btn .btn-primary}` sui link inline (rule 04a). HTML grezzo con `href="/giochi/..."` invece **rompe il subpath GitHub Pages** (`/sito-pc-genzano/giochi/...`). Lo shortcode applica `relURL` con `strings.TrimPrefix "/"` per ottenere il path corretto su entrambi gli ambienti deploy (Aruba root + GH Pages subpath).

---

## 34.10 Cross-link bidirezionali

La nuova sezione è linkata da 4 pagine principali del sito:

| Da | Tipo di link | Posizione |
|---|---|---|
| `static/giochi/index.html` (Arena) | Bottone "Vai al catalogo informativo dei giochi" | Sotto la `<p class="lead">` del page-hero |
| `content/formazione/_index.md` | Bottone "Catalogo informativo" affianco al bottone Arena | Card "Voglio imparare giocando" |
| `content/formazione/_index.md` | Voce lista | Sezione "Storie, giochi e attività" |
| `content/scuole/_index.md` | Voce lista | Card "Sono uno studente o studentessa" |
| `content/mappa-sito/_index.md` | Nuova card `ms-edu` con icona `bi-card-checklist` | Affianco alla card "Giochi della Sicurezza" |

A questi si aggiunge la voce di menu (vedi 34.11).

---

## 34.11 Voce di menu (sincronizzazione obbligata)

🔴 **Rule 04b § "Menu di navigazione — Sincronizzazione obbligatoria `hugo.toml` ↔ `site-chrome.js`":**

In `hugo.toml`:

```toml
[[menus.main]]
  name = "Catalogo dei giochi"
  url = "/catalogo-giochi/"
  parent = "per-le-scuole"
  weight = 7
```

In `static/app-shared/site-chrome.js`, riga aggiunta speculare nel dropdown `navDropdown-per-le-scuole` (dopo la voce "Giochi della Sicurezza"):

```javascript
'<li role="none"><a class="list-item" href="' + SITE_URL + '/catalogo-giochi/" role="menuitem">' +
  '<span>Catalogo dei giochi</span></a></li>' +
```

Il workflow `audit-sito.yml` § 41 ("Coerenza menu Hugo ↔ site-chrome.js") verifica ogni lunedì la simmetria fra i due punti.

---

## 34.12 Cosa NON contiene il catalogo (vincoli editoriali)

Per coerenza con la rule editoriale del sito:

- **No screenshot del gioco** nel banner della scheda: il banner resta la cover tipografica istituzionale col solo titolo (rule 09 § 9, divieto banner col titolo intoccabile). Aggiungere uno screenshot inline come `{{< foto >}}` è possibile in futuro, ma va trattato come "foto utente": va nel corpo, non nel banner.
- **No conteggi inventario** ("33 giochi totali", "10 per fascia infanzia"): le pagine hub e indici descrivono i contenuti **qualitativamente**, non con numeri di catalogo. Eccezioni puntuali nella prosa quando il conteggio è citazionale o serve davvero alla comprensione (es. *"divisi in tre fasce"*), ma niente *"10 giochi disponibili"* come metrica dichiarata.
- **No tono pubblicitario o promozionale** sui giochi: la scheda è descrittiva-funzionale, non un *"Vieni a giocare al gioco più bello!"*. Coerente con rule 02 § "Regole editoriali" + rule 01 § "Divieti".
- **No info inventata sul valore educativo**: il riferimento al D.M. 183/2024 (Ed. Civica, 33 ore annuali) è dichiarato in modo neutro come opportunità di uso, non come endorsement MIM.

---

## 34.13 Manutenzione e follow-up

**Quando rigenerare il deck di presentazione:** la nuova sezione `/catalogo-giochi/` è ora citata nel deck `static/manuali/presentazione-struttura-sito.pdf` come slide "Catalogo informativo dei giochi" (subito dopo la slide "Giochi della sicurezza"). Se in futuro modifichi le sezioni del sito o i dati mostrati nelle slide, rigenera il deck con `python3 scripts/genera-presentazione.py` (richiede venv `python-pptx pillow fonttools brotli` + LibreOffice per la conversione PDF).

**Quando aggiornare il catalogo:**

| Trigger | Cosa fare |
|---|---|
| Aggiungi un nuovo gioco | Workflow di 34.6 (manifest Coach + rigenera schede) |
| Cambia la regola di un gioco esistente | Modifica `regola` nel manifest Coach, rigenera la scheda di quel gioco |
| Cambia un link teoria | Modifica `teoria` nel manifest Coach, rigenera la scheda |
| Cambia la fascia d'età standard (durata, lingua) | Modifica `FASCIA_META` in `genera-schede-giochi.py` e rigenera tutto |
| D.M. ed. civica viene aggiornato | Cerca e sostituisci `D.M. 183/2024` su tutti i 33 file + hub |

**Verifiche automatiche:**

- `audit-sito.yml` § 41 verifica menu sincronizzato fra `hugo.toml` e `site-chrome.js`
- `audit-sito.yml` § 43 ("Stale FTP files detection") può essere esteso in futuro per coprire `/catalogo-giochi/` se la sezione diventa target di staleness ricorrenti — al momento (28/05/2026) le 22 URL del campione bastano

---

## 34.14 Sintesi operativa per Claude

Quando un futuro intervento tocca i giochi del sito, ricorda:

1. **Coach è la fonte unica di verità**, sia per il bottone consigli sia per il catalogo.
2. **Aggiungere un gioco** = 6 passi (34.6), non meno.
3. **Le 33 schede non si editano a mano**: editare il manifest e rigenerare.
4. **`/giochi/` = Arena interattiva**, `/catalogo-giochi/` = catalogo informativo. Sono complementari, non sostitutive.
5. **`image: ""` resta vuoto** nel frontmatter: la cover tipografica banner è generata automaticamente (mai foto utente nel banner).
6. **Bottone CTA = shortcode `bottone-gioco`**, non Markdown attribute syntax (incompatibile con Goldmark del sito).
7. **D.M. 183/2024** (non 91/2024) è il riferimento corretto per l'Educazione Civica.

---

_[Indice manuale](README.md)_
