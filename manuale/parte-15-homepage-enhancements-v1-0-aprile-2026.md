_[Indice manuale](README.md)_

# Parte 15 — Homepage enhancements v1.0 (aprile 2026)

Quattro micro-miglioramenti grafici applicati alla **sola homepage** (scoped via
`body.home-page`), tutti AGID-compliant, tutti rispettano `prefers-reduced-motion`,
`@media print` e il toolbar di accessibilità "pausa animazioni". Funzionano in modo
identico su desktop e su mobile (nessuna `@media (hover: hover)` o esclusione touch).

### 15.1 Live dot pulse blu accanto a "Notizie in Evidenza"

Piccolo cerchio blu istituzionale (`#003366`) accanto al titolo della sezione notizie,
con animazione `livePulse` 2.5s che produce un'onda di box-shadow espansiva — pattern
che richiama l'animazione `sosPulse` del bottone SOS-112 ma in chiave **informativa**
(blu) invece di **emergenza** (rosso). Significato: "qui ci sono notizie aggiornate".

Selettore: `.live-dot` (definito in `custom.css` sezione **HOMEPAGE ENHANCEMENTS v1.0**).
Markup: `<span class="live-dot" aria-hidden="true"></span>` davanti al testo del titolo.
File coinvolto: `themes/flavour-pcgenzano/layouts/partials/latest-news.html`.

Per estendere a un'altra sezione (es. "Allerte attive"): basta aggiungere lo stesso span
davanti al titolo e il dot apparirà animato.

### 15.2 Reveal-on-scroll delle card

Le card della homepage (`quick-action-card`, `card-servizio`, `card-notizia-hero`,
`card.border-danger`, `stat-hero-item`, `card-numero-utile`) appaiono con
`opacity 0 → 1 + translateY(15px → 0)` quando entrano nel viewport.

Implementazione: `themes/flavour-pcgenzano/static/js/homepage-reveal.js` —
IntersectionObserver puro stdlib, threshold 0.15, `rootMargin -50px` in basso.
Lo script si auto-disabilita se `prefers-reduced-motion: reduce` è attivo o se
il browser non supporta IntersectionObserver (graceful degradation: card visibili
direttamente). Caricato `defer` in `baseof.html` solo per `.IsHome`:

```go-html-template
{{ if .IsHome }}<script src="{{ "js/homepage-reveal.js" | relURL }}" defer></script>{{ end }}
```

### 15.3 Hero con pattern di linee oblique + gradiente animato

Il banner blu della homepage ha:
- Pattern di linee oblique 45° molto sottili (opacity 0.045) sovrapposto al gradiente,
  via `repeating-linear-gradient` puro CSS (zero data:URL, zero asset esterni).
- Shifting cromatico lentissimo del gradiente (`background-size: 180%`, animazione
  `heroGradientShift` 35s ease-in-out infinite). Il movimento è quasi impercettibile
  ma rompe la planarità del banner.

In stampa il pattern sparisce e il banner diventa piatto. Con `reduced-motion` il
gradiente non si muove (resta fisso al frame iniziale).

### 15.4 Hover lift card + freccia CTA che scivola

Tutte le card della homepage hanno:
- `translateY(-3px)` + ombra blu istituzionale `0 10px 22px rgba(0, 51, 102, 0.14)` al `:hover` o `:focus-within`.
- L'icona `bi-arrow-right` delle CTA scivola di 4px a destra al hover/focus.

Su mobile l'effetto si attiva al `:focus-within` (cioè quando l'utente tocca/seleziona
la card), che è il comportamento standard touch — non è una limitazione, è il pattern
nativo del Web.

#### Estensione globale del pattern (sessione 2026-05-06)

Il pattern era inizialmente scoped a `body.home-page`. Dopo audit di consistency
(commit `71c460a`) è stato esteso al **default globale** per coerenza tra tutte
le pagine del sito. 8 selettori card uniformati al pattern v1.0 (era una mistura
di `-2px`, `-4px`, `-5px` con ombre diverse):

- `.quick-action-card`, `.card-servizio`, `.card-notizia-hero` (homepage)
- `.lang-card` (selettore lingue)
- `.articolo-nav-card` (prev/next articolo)
- `.articolo-correlato-card` (leggi anche)
- `.ms-card` (mappa sito, CSS in content/mappa-sito/_index.md)
- `.back-to-top` (FAB scroll-to-top)

Card a "lift laterale" (`.card-notizia-small`, `.card-social-link`) lasciate
invariate per intenzione: hanno layout orizzontale, il `translateX(2-4px)` è
coerente col loro contesto.

Header documentale centralizzato in `custom.css` prima della prima card che usa
il pattern (cerca `PATTERN HOVER-LIFT v1.0`) — elenco selettori + valori esatti
per evitare drift futuro.

### 15.5 Estendere o disattivare le enhancement

**Disattivare un singolo elemento**: rimuovi il selettore corrispondente dalla sezione
**HOMEPAGE ENHANCEMENTS v1.0** in `custom.css`.

**Disattivare tutto** (per chi vuole homepage piatta): aggiungi `class=""` a `<body>`
in `baseof.html` (rimuovendo la condizione `.IsHome`). Tutto torna allo stato pre-v1.0.

**Estendere a un'altra pagina (es. /comunicazioni/)**: cambia la condizione in
`baseof.html` da `{{ if .IsHome }}` a una condizione più ampia. Aggiorna gli
selettori CSS da `body.home-page` al nuovo class.

---

_[Indice manuale](README.md)_

[← Parte 14 — Configurazione ambiente di sviluppo (Claude Code)](parte-14-configurazione-ambiente-di-sviluppo-claude-code.md) · [↑ Indice](README.md) · [Parte 16 — Bozze social: gestione quota Gemini API →](parte-16-bozze-social-gestione-quota-gemini-api.md)
