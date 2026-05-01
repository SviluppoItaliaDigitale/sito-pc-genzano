_[Indice manuale](README.md)_

# Parte 17 — Coach didattico nei giochi e TTS esteso (maggio 2026)

### 17.1 Perché esiste il "Coach"

Ad aprile 2026 abbiamo notato che molti bambini, soprattutto della fascia 3-8 anni,
abbandonavano i giochi della sezione "Giochi della Sicurezza" dopo i primi errori:
non avendo studiato i temi, rispondevano a caso e perdevano la motivazione. Il
sistema di feedback esistente (testo "risposta sbagliata") era sufficiente a
registrare l'errore ma non a far imparare.

La soluzione è un sistema **a tre layer** ispirato alla campagna DPC "Io non rischio"
e alle linee guida AGID per accessibilità cognitiva:

1. **Onboarding pre-gioco**: bottone "💡 Consigli per giocare" sotto il titolo di
   ogni gioco. Click → dialog con regola in 1 frase + bullet "Come si gioca" +
   link alle pagine teoria del sito.
2. **TTS audio**: dentro il dialog, bottone "🔊 Ascolta i consigli" che legge
   regola + bullet via Web Speech API browser-native. Stessa cosa nei suggerimenti
   contestuali.
3. **Suggerimento contestuale su errore**: quando il bambino sbaglia, accanto al
   bottone Consigli appare un riquadro giallo con suggerimento mirato + link
   "Scopri perché →" alla teoria pertinente. Trasforma il fallimento in
   apprendimento senza richiedere proattività al bambino.

### 17.2 Architettura del Coach

Tutto in 2 file condivisi sotto `static/giochi/assets/`:

- **`css/coach.css`** — bottone trigger, dialog modale, hint contestuale, bottone
  TTS. Tre varianti per fascia (rosso infanzia, verde primaria, blu ragazzi).
  Rispetta `prefers-reduced-motion`. Nascosto in stampa.
- **`js/coach.js`** — modulo IIFE con: manifest dei 33 giochi, dialog accessibile
  (`role=dialog`, focus trap, ESC), hint contestuale, TTS Web Speech API.
  Auto-init via `data-coach-game="<id>"` sul `<body>` di ogni gioco.

Per **aggiungere un nuovo gioco** servono 3 righe HTML + 1 voce nel manifest:

```html
<head>
  ...
  <link rel="stylesheet" href="/giochi/assets/css/coach.css">
</head>
<body class="..." data-coach-game="nuovo-gioco-id">
  ...
  <script src="/giochi/assets/js/coach.js" defer></script>
</body>
```

E nel manifest dentro `coach.js`:

```js
'nuovo-gioco-id': {
  fascia: 'primaria',
  titolo: 'Consigli per il Nuovo Gioco',
  regola: 'Una frase chiara di cosa si fa.',
  come: ['Punto 1.', 'Punto 2.', 'Punto 3.'],
  teoria: [
    { titolo: 'Pagina teoria', url: '/percorso-pagina/' }
  ]
}
```

### 17.3 Layer 3: agganciare hint contestuale a un gioco

Per un gioco con feedback wrong/correct discreto, basta aggiungere 2 righe nel
callback wrong-answer e 1 nel callback correct-answer:

```js
// Su risposta sbagliata:
if (window.GameCoach && window.GameCoach.hint) {
  window.GameCoach.hint('Suggerimento mirato di 1-2 frasi.', '/percorso/teoria/');
}

// Su risposta corretta o passaggio a nuova domanda:
if (window.GameCoach && window.GameCoach.clearHint) {
  window.GameCoach.clearHint();
}
```

Il `if (window.GameCoach && ...)` garantisce **fallback graceful**: il gioco
continua a funzionare anche se `coach.js` non è caricato.

### 17.4 TTS esteso al sito

Lo stesso paradigma Web Speech API alimenta tre contesti distinti:

| Contesto | Componente | Quanti |
|---|---|---|
| Pagine Hugo | `partials/leggi-ad-alta-voce.html` (opt-in `tts: true` nel frontmatter) | 21 pagine |
| Coach giochi | `js/coach.js` (auto su tutti i giochi con `data-coach-game`) | 33 giochi |
| Storie e fiabe | `formazione/storie-e-racconti/assets/tts-storia.js` | 18 storie |

Le 21 pagine Hugo con `tts: true`:
- 12 storiche: cosa-fare-adesso, numeri-utili, facile-da-leggere, allerte-meteo,
  piano-familiare, 7 sotto-pagine rischi-prevenzione.
- 9 aggiunte (maggio 2026): assistente, faq, piano-emergenza, contatti, chi-siamo,
  diventa-volontario, glossario, rischi-prevenzione/{kit-emergenza,
  persone-necessita-specifiche}.

Per **attivare TTS su una nuova pagina Hugo**: aggiungere `tts: true` al frontmatter.

Per **attivare TTS su una nuova storia/racconto**: includere
`<script src="/formazione/storie-e-racconti/assets/tts-storia.js" defer></script>`
prima di `</body>`. Il bottone si aggiunge automaticamente nella `.storia-toolbar`.

### 17.5 Conformità AGID + WCAG 2.2

La scelta della **Web Speech API browser-native** è raccomandata da W3C-WAI per la
PA italiana al posto degli **overlay commerciali** (AccessiBe, UserWay, Equally AI),
sconsigliati perché mascherano problemi di accessibilità invece di risolverli.

Vantaggi:
- **Zero costi**: nessuna API key, nessun servizio cloud, nessun fee per parola.
- **Zero file da mantenere**: niente MP3 da rigenerare quando cambi il testo. La
  sintesi è al volo, sempre coerente col testo.
- **WCAG 2.2 compliant**: `aria-pressed` dinamico, focus visibile, gestione tastiera,
  fallback graceful se browser senza Speech API.
- **GDPR safe**: nessun dato esce dal browser, nessun tracker.

Specifiche tecniche complete in `.claude/rules/03-accessibility.md` § "TTS Leggi ad
alta voce" e § "Coach dei giochi".

---

*Fine del manuale. Per domande non coperte qui, apri un'Issue sul repository o contatta
il Chief Digital Officer del Gruppo.*

_[Indice manuale](README.md)_

[← Parte 16 — Bozze social: gestione quota Gemini API](parte-16-bozze-social-gestione-quota-gemini-api.md) · [↑ Indice](README.md)
