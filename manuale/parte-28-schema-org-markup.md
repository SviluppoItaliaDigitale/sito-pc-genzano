# Parte 28 — Markup Schema.org (SEO + rich result Google)

Aggiunta a maggio 2026. Il sito dichiara markup strutturato **Schema.org** in formato JSON-LD su tutte le pagine, per migliorare visibilità SEO, rich snippets Google, pannello di conoscenza, FAQ direttamente nei risultati di ricerca e box "How To" per le procedure di emergenza.

## 28.1 Architettura

**Un solo partial centrale**: `themes/flavour-pcgenzano/layouts/partials/structured-data.html` (~350 righe). Chiamato da `_default/baseof.html` su **ogni** pagina. Genera markup JSON-LD context-aware: il tipo dipende dalla sezione e dal frontmatter della pagina.

Nessun partial separato per tipo. Pattern unico, mantenibile.

## 28.2 Tipi Schema.org attivi sul sito

| Tipo | Pagine | Quando si attiva |
|---|---|---|
| `Organization` + `NGO` | Homepage | `.IsHome` |
| `ContactPoint`, `PostalAddress`, `GeoCoordinates`, `City` | Annidati in `Organization` | Sempre (homepage) |
| `WebSite` + `SearchAction` | Homepage | `.IsHome` |
| `Article` | ~104 articoli `/comunicazioni/` | `.Section == "comunicazioni"` e `.IsPage` |
| `Event` | 4 articoli con `badge: "Evento"` | `eq .Params.badge "Evento"` (annidato in Article) |
| `FAQPage` + `Question`/`Answer` | `/faq/` | `$isFAQ` (10 Q&A serializzate dal frontmatter) |
| `HowTo` + `HowToStep` | 8 pagine `/rischi-prevenzione/*` | `if and .Params.howto_prima .Params.howto_durante .Params.howto_dopo` |
| `BreadcrumbList` + `ListItem` | 283 pagine | `not .IsHome` |
| `WebPage` | Tutto il resto | Default fallback |
| `ImageObject` | Annidato in `Article` | Quando l'articolo ha `image:` |

## 28.3 Vincolo di principio — Organization+NGO, non GovernmentOrganization

🔴 **VINCOLO STORICO INVIOLABILE.** La homepage usa `["Organization", "NGO"]` e **NON** `GovernmentOrganization` né `EmergencyService`. Documentato in `rule 04a-hugo-shortcode-partial.md § "Partial structured-data"`.

Motivo: il Gruppo è un'**associazione di volontariato OdV**, non ente governativo né servizio di emergenza chiamabile direttamente. Marcare la homepage con tipi che inducano Google/Alexa/Siri a presentare il Gruppo come "ente che risponde alle emergenze" creerebbe confusione pericolosa col 112 (Numero Unico Europeo), che è l'**unico** canale corretto per chiamare aiuto.

Il vincolo è stato riconfermato esplicitamente dall'utente nella sessione del 12 maggio 2026 prima di implementare HowTo.

## 28.4 Markup HowTo — cosa fa

Aiuta Google a generare un **box "How To"** nei risultati di ricerca per le pagine procedure di emergenza. Quando l'utente cerca "cosa fare durante un terremoto" o "alluvione casa", il box compare in cima ai risultati con i 3 step PRIMA / DURANTE / DOPO già visibili.

Schema generato per ciascuna delle 8 pagine `/rischi-prevenzione/*`:

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "<title della pagina>",
  "description": "<description del frontmatter>",
  "totalTime": "PT<N>M",
  "inLanguage": "it-IT",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Prima",
      "text": "<frontmatter howto_prima>",
      "url": "<URL pagina>#cosa-fare-prima"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Durante",
      "text": "<frontmatter howto_durante>",
      "url": "<URL pagina>#cosa-fare-durante"
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "Dopo",
      "text": "<frontmatter howto_dopo>",
      "url": "<URL pagina>#cosa-fare-dopo"
    }
  ]
}
```

**`totalTime`** calcolato come `max(5, ReadingTime × 1.5)` minuti — stima tempo lettura + applicazione pratica. **`url` di ciascun step** punta al frammento `#cosa-fare-prima` / `#cosa-fare-durante` / `#cosa-fare-dopo` della pagina, ancore presenti grazie alla struttura uniforme delle pagine rischio (`rule 06-protezione-civile-scientifica.md`).

## 28.5 Come aggiungere HowTo a una nuova pagina rischio

Quando aggiungi una nuova pagina `/rischi-prevenzione/*` (es. neve, alluvioni costiere, tsunami), basta:

1. Scrivere la pagina con la struttura uniforme PRIMA/DURANTE/DOPO (vedi `rule 06`).
2. Aggiungere nel frontmatter i 3 campi:

```yaml
howto_prima: "Riassunto in 1-3 frasi delle azioni preventive da fare prima dell'evento. Mantenere lo stesso tono e lo stesso lessico della pagina principale per coerenza SEO. Niente sigle non spiegate."
howto_durante: "Riassunto in 1-3 frasi delle azioni immediate. Mettere prima le azioni di sicurezza (es. 'allontanati', 'chiama il 112') poi le accortezze ('non avvicinarti', 'non fare X')."
howto_dopo: "Riassunto in 1-3 frasi delle azioni di recupero. Includere segnalazione al 112 per pericoli persistenti."
```

Hugo genera automaticamente il blocco HowTo. Verifica post-build:

```bash
hugo --minify
python3 -c "
import re, json
with open('public/rischi-prevenzione/<nuova-pagina>/index.html') as f: html = f.read()
scripts = re.findall(r'<script type=application/ld\+json>(.*?)</script>', html, re.DOTALL)
for s in scripts:
    d = json.loads(s)
    if d.get('@type') == 'HowTo':
        print('HowTo OK:', len(d['step']), 'step')
"
```

Poi test online con [Google Rich Results Test](https://search.google.com/test/rich-results) e [validator.schema.org](https://validator.schema.org/).

## 28.6 Sintassi critica `| jsonify | safeJS`

⚠️ **OBBLIGATORIA** per ogni campo testuale dentro `<script type="application/ld+json">`. Hugo applica un **secondo escape JS contestuale** alle stringhe dentro `<script>`, e il solo `| jsonify` produce **doppio escape** (es. `name: "\"Foo\""`). Aggiungere `| safeJS` dopo `| jsonify` impedisce il secondo escape:

```go-html-template
{{/* ❌ SBAGLIATO — produce \"Foo\" doppio escape */}}
"name": {{ .Title | jsonify }}

{{/* ✅ CORRETTO — produce "Foo" pulito */}}
"name": {{ .Title | jsonify | safeJS }}
```

Vale anche per campi con apostrofi italiani come "L'unica difesa" → con `| safeJS` resta `"L'unica difesa"`, senza diventerebbe `"L'unica difesa"` con escape Unicode aggressivo.

Bug catturato e fixato durante implementazione P-Schema HowTo del 12 maggio 2026.

## 28.7 Validazione

Tre livelli di test consigliati:

### Livello 1 — Validazione locale parser JSON (CLI)

```bash
python3 -c "
import re, json
import glob
errors = 0
for f in glob.glob('public/**/index.html', recursive=True):
    html = open(f).read()
    for s in re.findall(r'<script type=application/ld\+json>(.*?)</script>', html, re.DOTALL):
        try: json.loads(s)
        except json.JSONDecodeError as e:
            print(f'❌ {f}: {e}')
            errors += 1
print(f'JSON-LD errors: {errors}')
"
```

Atteso: `errors: 0` su tutte le pagine.

### Livello 2 — schema.org Validator (web)

Vai su <https://validator.schema.org/> e incolla l'URL della pagina. Mostra warning se proprietà obbligatorie mancano, errori se la struttura è invalida. Atteso: 0 errori, warning informativi accettabili.

### Livello 3 — Google Rich Results Test (web)

Vai su <https://search.google.com/test/rich-results> e incolla l'URL. Verifica che Google riconosca il tipo (Article, HowTo, FAQPage, Event) e che possa generare il rich result. Atteso: tutti i tipi attesi marcati ✅.

## 28.8 Tipi NON attivi (scelte deliberate)

| Tipo | Perché non lo usiamo |
|---|---|
| `GovernmentOrganization` | Vincolo storico § 28.3 — il Gruppo è OdV, non ente governativo |
| `EmergencyService` | Stessa ragione — Google indurrebbe gli utenti a chiamare il Gruppo al posto del 112 |
| `EducationalOccupationalCredential` | Non ci sono pagine dedicate ai corsi formali con attestato. Valutabile in futuro quando `/formazione/corso-base/` sarà una pagina autonoma con frontmatter strutturato (data, durata, attestato, ente certificante) |
| `Course` | Stessa ragione di Educational |
| `MedicalCondition`, `Drug` | Fuori scope — il sito non fornisce contenuti medico-clinici |
| `Product`, `Offer` | Fuori scope — non vendiamo nulla |

## 28.9 Riferimenti

- **Schema.org**: <https://schema.org/>
- **Schema.org HowTo**: <https://schema.org/HowTo>
- **Schema.org HowToStep**: <https://schema.org/HowToStep>
- **Google Rich Results Test**: <https://search.google.com/test/rich-results>
- **Schema.org Validator**: <https://validator.schema.org/>
- **W3C JSON-LD 1.1**: <https://www.w3.org/TR/json-ld11/>
- **Manuale Parte XX SEO** (futuro): linea guida AGID per la PA su SEO + rich result.
