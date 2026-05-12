# Parte 26 — Pagina Podcast + Scarica trascrizione PDF

Aggiunta a maggio 2026 nell'ambito del **Punto 15 della roadmap accessibilità**: *Versione audio podcast auto-generata*.

Il sito offre **due funzionalità complementari** per chi vuole ascoltare gli articoli invece di leggerli, o portarli con sé come testo stampato:

1. Una **pagina podcast** `/podcast/` con elenco di tutti gli articoli ascoltabili e la **durata stimata** della lettura ad alta voce.
2. Su ogni articolo, un bottone **"Scarica trascrizione PDF"** che apre la finestra di stampa del browser per salvare l'articolo come PDF.

Entrambe le funzioni sono **a costo zero**: usano la Web Speech API del browser (che è gratuita e già presente sul dispositivo dell'utente) e il rendering CSS `@media print` nativo del sito.

## 26.1 Perché esiste

Il bottone **"Leggi ad alta voce"** è presente su ogni articolo dal Sera 1 di maggio 2026 (vedi Parte 18). Funziona bene ma è poco **scopribile**: chi non lo cerca attivamente non sa che esiste.

La pagina `/podcast/` lo rende **scopribile**: il cittadino vede un elenco strutturato di tutti gli articoli "audibili", con la durata stimata, e può scegliere cosa ascoltare. È un'esperienza più simile a un'app podcast classica, ma senza richiedere registrazione, app, o costi.

Il bottone "Scarica trascrizione PDF" risponde a un'esigenza diversa: chi vuole **conservare** o **stampare** l'articolo (es. per consultarlo offline durante un'emergenza, per portarlo a una riunione, per stamparlo per chi non ha smartphone) ha un modo immediato per farlo. La logica è minimale: chiama `window.print()` e il browser apre la propria finestra di stampa, dove l'utente sceglie "Salva come PDF" come destinazione.

Niente generazione MP3 server-side. Niente feed RSS podcast. Niente costi TTS a pagamento. Niente WeasyPrint o wkhtmltopdf installati sul runner CI. **Tutto sul dispositivo dell'utente, gratuito, privacy-first.**

## 26.2 Pagina `/podcast/`

**Path:** `content/podcast/_index.md` (frontmatter + intro user-facing) + `themes/flavour-pcgenzano/layouts/podcast/list.html` (template).

**Voce menu:** "Podcast" sotto "Risorse" (weight 9, fra "Open Data" e "Mappa del Sito").

**Sincronia obbligatoria** `hugo.toml` + `static/app-shared/site-chrome.js` (vincolo storico — vedi `rule 04b § Sincronizzazione obbligatoria`).

**Cosa mostra il template:**
- Intro user-facing dal `_index.md` (spiega come funziona la lettura vocale + privacy + tasti rapidi).
- Lista card-style di tutti gli articoli `/comunicazioni/` con:
  - Icona altoparlante blu istituzionale.
  - Titolo (link cliccabile, `stretched-link` per zona tap mobile).
  - Badge categoria + data lunga.
  - Description del frontmatter.
  - **Durata stimata audio** in colonna destra (background grigio chiaro, font bold).
- Conteggio totale articoli ascoltabili a fine pagina.

**Filtri applicati nel template** (deve restare allineato a `_default/single.html` e `_default/list.html` per coerenza):
- `where .Site.RegularPages "Section" "comunicazioni"` → solo articoli (non pagine generiche).
- `where ... "Draft" "ne" true` → niente bozze.
- `where ... "Params.tts" "ne" false` → opt-out manuale via frontmatter `tts: false` lo esclude.
- `where ... "WordCount" "gt" 30` → soglia minima, esclude articoli "ponte" senza testo significativo.

Hugo include automaticamente solo articoli con `date <= now`, quindi gli articoli **calendarizzati futuri** entrano nella lista podcast quando arriva la loro data di pubblicazione (via workflow `pubblica-programmata.yml` 06:00 UTC giornaliero).

## 26.3 Calcolo della durata stimata audio

La voce italiana del TTS browser parla a **~150 parole al minuto** (più lenta della lettura visiva media di **~200 wpm**). Quindi:

```
durata_audio_min = ReadingTime × (200 / 150) = ReadingTime × 1.33
```

Implementato nel template:

```go-template
{{ $audioMin := math.Max 1 (int (math.Round (mul .ReadingTime 1.33))) }}
```

Esempi:
- Articolo da 4 minuti di lettura visiva → ~5 minuti audio.
- Articolo da 8 minuti → ~11 minuti audio.
- Articolo molto breve (< 1 min di lettura) → minimo 1 minuto (math.Max).

La stima è **indicativa**: la velocità reale dipende dalla voce italiana installata sul dispositivo dell'utente e dalla scelta "Lenta / Normale / Veloce" nel pannello accessibilità (0.75x / 0.95x / 1.15x).

## 26.4 Bottone "Scarica trascrizione PDF"

**Path:** `themes/flavour-pcgenzano/layouts/partials/scarica-trascrizione-pdf.html`.

**Markup**: un singolo `<button>` con `onclick="window.print()"` + frase di contesto:

> *"Apre la finestra di stampa del browser. Scegli 'Salva come PDF' come destinazione: avrai l'articolo formattato A4 senza il chrome del sito."*

**Posizione**: in `_default/single.html` subito dopo il partial `scarica-braille.html`, sopra il `<article class="article-body">`. Cluster accessibilità coerente:

```
1. Tempo di lettura (~N minuti)
2. Bottone "Leggi ad alta voce" + selettore velocità
3. Bottone "Scarica versione braille" (se .brf esiste)
4. Bottone "Scarica trascrizione PDF"
5. <article>...corpo articolo...</article>
```

**Perché funziona senza altro setup**: il sito ha già una regola CSS `@media print` globale (`themes/.../custom.css`) che, alla stampa, nasconde navbar, footer, banner, cookie, utility bar, page tools, e mostra solo il corpo dell'articolo formattato per A4. Quando l'utente clicca il bottone PDF, il browser apre la propria finestra di stampa che usa quegli stili: il PDF che ne esce è pulito, leggibile, AGID-conforme.

**Niente generazione PDF server-side**: zero dipendenze CI aggiuntive (WeasyPrint richiederebbe `apt-get install python3-weasyprint` + 200 MB di librerie GTK). Approccio scelto perché bilancia ergonomia (1 click) con manutenibilità (zero setup).

## 26.5 CSS

Sezioni dedicate in `themes/flavour-pcgenzano/static/css/custom.css`:

- **`SCARICA TRASCRIZIONE PDF v1.0`** (~15 righe): stile coordinato col bottone TTS e braille — `btn-outline-primary btn-sm` + frase contesto small text-muted. Nascosto in stampa (`@media print { display: none }`).
- **`PODCAST LIST v1.0`** (~50 righe): card style, border-left blu, hover lift, responsive stack su mobile (`<576px`: la durata passa sotto invece che a destra), override stampa con bullet list semplice.

## 26.6 Cosa NON entra nell'MVP

1. **Generazione MP3 server-side**: richiederebbe TTS a pagamento (Google Cloud TTS, AWS Polly, Azure Cognitive Speech) — minimo $4/M caratteri. Su 388 articoli × ~4000 caratteri ≈ 1.5 M caratteri = $6/mese ricorrente. Scartato per coerenza con la politica "niente costi runtime ricorrenti".
2. **Feed RSS podcast** (RSS 2.0 con `<enclosure>` audio): richiederebbe MP3 reali. Senza MP3, l'enclosure non ha URL → non è un podcast valido per app come Apple Podcasts, Spotify, ecc. Saltato.
3. **Generazione PDF server-side** con WeasyPrint / wkhtmltopdf: 200+ MB di dipendenze sul runner CI + 5-10 sec extra per articolo. `window.print()` raggiunge lo stesso risultato senza costi.
4. **Player audio embedded nella pagina** (tipo HTML5 `<audio controls>`): richiederebbe MP3 o lo stream TTS in tempo reale. Il bottone "Leggi ad alta voce" esistente già copre questo caso.
5. **Statistiche di ascolto** (chi ha ascoltato cosa, quanto a lungo): impossibili senza tracking server-side. Coerente con la scelta privacy-first del sito.

## 26.7 Cosa NON funziona

- **Browser senza Web Speech API** (Tor Browser, alcune build di LibreWolf): il bottone "Leggi ad alta voce" sull'articolo si nasconde via JS (`speechSynthesis` non c'è). Il bottone "Scarica trascrizione PDF" resta funzionante (è una semplice `window.print()`). La pagina `/podcast/` resta utile come elenco strutturato dei contenuti.
- **Browser con cache aggressiva sui CSS** (raro post Sera 2 del Punto 14, dato il cache-buster): se un utente vede ancora versioni vecchie del template, può servire hard refresh.

## 26.8 Test di accettazione

Dopo il deploy, verifica:

1. `/podcast/` carica e mostra una lista di N articoli con durata stimata.
2. Clic su un articolo → atterri sulla pagina articolo, in cima trovi il cluster "Leggi ad alta voce" + "Scarica versione braille" (se disponibile) + "Scarica trascrizione PDF".
3. Clic su "Scarica trascrizione PDF" → si apre la finestra di stampa del browser, scegli "Salva come PDF" → ottieni un PDF pulito con solo il corpo articolo + immagini, senza navbar/footer/banner.
4. Clic su "Leggi ad alta voce" → la voce italiana inizia a leggere; cambia velocità con il selettore; ferma con il bottone "Ferma lettura".
5. La voce menu "Podcast" è presente in "Risorse" sia nelle pagine Hugo sia nelle pagine HTML statiche (es. giochi, schede stampabili) — vincolo sync `site-chrome.js`.

## 26.9 Riferimenti

- **Web Speech API** (MDN): <https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API>
- **W3C Web Speech API spec**: <https://wicg.github.io/speech-api/>
- **Manuale Parte 18 — Lettura accessibile**: documenta il bottone TTS originale (Sera 1) + selettore velocità + segui-parole rimosso.
- **CLAUDE.md regola 10 STAMPA**: il blocco `@media print` globale che rende il PDF pulito.
