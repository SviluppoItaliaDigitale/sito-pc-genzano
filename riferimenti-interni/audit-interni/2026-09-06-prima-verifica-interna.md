# Prima verifica interna — 6 settembre 2026 — snapshot c7e21f0 (PR #988)

Perimetro **mirato**: le tre aree che l'audit esterno del 6 settembre 2026 non ha coperto
(catena dell'allerta end-to-end, coerenza fra pagine, traduzioni). Eseguita in sola lettura
dagli agenti `pc-esercitazione-emergenza`, `pc-coerenza-trasversale`, `pc-revisore-traduzioni`
il giorno stesso della loro creazione, per metterli alla prova. Le correzioni seguono dopo
revisione e conferma dell'utente.

## Parte A — Coerenza trasversale (rapporto dell'agente)

| Famiglia | Fonte canonica | Contraddizione | Gravità |
|---|---|---|---|
| Anno/atto di fondazione del Gruppo | `content/chi-siamo/_index.md`, dossier «Il nostro Gruppo» (delibera 1991, sindaco Cesaroni) | l'articolo del 05/04/2026 «Quarant'anni di volontariato» data la delibera al **1993** (riga 34) e titola «quarant'anni» con fondazione 1981 (= 45 anni nel 2026) | Molto alta |
| Litri d'acqua del kit casa 72 ore | `kit-emergenza/_index.md` (4 L/persona/giorno, Ready.gov/FEMA), `piano-familiare` (4), `ondate-di-calore` (12 L per 3 giorni) | ~15 file con **3 L** (articoli 07/06, 26/05, 02/09 + facile, 21/04 + facile, 26/04 + facile; schede blackout-servizi-essenziali-secondaria, piano-familiare-secondaria, piano-familiare-primaria e pacchetti) e **2 L** (kit-scuola-secondaria-primo-grado:326, `rischi-prevenzione/blackout.md` righe 10 e 31) | Alta |
| Rigopiano: persone presenti | articolo 18/01/2027 e dossier «Neve e gelo»: 40 (29+11) | `caso-rigopiano-secondaria/index.html:86` «47 persone», poi 29+11 alla riga 91 (e pacchetto secondaria) | Alta |
| Visso/Ussita 26/10/2016: vittime | articolo 26/10/2026: «un solo morto in modo diretto» | `caso-amatrice-secondaria/index.html:96` «Nessuna vittima diretta» (e pacchetto) | Alta |
| Codici colore | `data/codici_colore.yaml`: giallo ordinaria, arancione moderata, rosso elevata | `decodifica-bollettino-secondaria2/index.html:91,100` «criticità elevata — ARANCIONE», «criticità massima — ROSSO» (e pacchetto secondaria2) | Media |
| Vajont: vittime | articolo 09/10/2026: «1.917 morti accertati (alcune fonti arrivano a 2.000)» | dossier Vajont riga 6 e 71, articolo dighe 07/10 riga 84, gioco linea-tempo-eventi riga 158: «1.910» come dato certo; schede e kit: 1.917 | Media |
| L'Aquila 2009: assistiti | dossier «Quando la terra trema»: ~67.000 | `caso-aquila-secondaria2` e pacchetti: ~65.000 | Bassa |
| Base normativa della fondazione | chi-siamo: nessuna legge del 2017 legata al 1981 | `layouts/assistente/list.html:935`: «costituita nel 1981 ai sensi della L.R. Lazio 9/2017» (anacronismo) | Bassa-media |

Famiglie verificate **senza** contraddizioni: candele/torce (74 occorrenze), ascensore (40+), numeri 112/803 555/1530, C.F., codice E10435833, sede/telefono/e-mail (anche nelle 7 traduzioni), 14° COI, nomi e capacità dei mezzi, Zona AIB 9, vittime L'Aquila (309) e Centro Italia (299), definizioni allerta/emergenza.

Proposta di fonte unica: portare i litri d'acqua del kit in `data/` (es. `kit_emergenza.yaml: acqua_litri_persona_giorno`) e citarli per riferimento; centralizzare le tre date istituzionali del Gruppo (1981, 1991, 2023/2024).

Grep di verifica residui (da rilanciare dopo le correzioni):

```bash
grep -rn "1993.*Cesaroni\|Cesaroni.*1993" content/
grep -rln "3 litri.*persona.*giorno\|3L/persona/giorno\|2 litri a persona" content/ static/formazione/schede-stampabili/
grep -rn "47 persone" static/formazione/schede-stampabili/caso-rigopiano-secondaria/
grep -rn "Nessuna vittima diretta" static/formazione/schede-stampabili/
grep -rn "criticità elevata — Codice ARANCIONE\|criticità massima — Codice ROSSO" static/formazione/schede-stampabili/
grep -rn "1.910 vittime\|1910 vittime" content/ static/
grep -rn "67.000 persone assistite\|65.000 sfollati" content/ static/
grep -rn "L.R. Lazio 9/2017" themes/
```

## Parte B — Traduzioni (rapporto dell'agente)

Perimetro reale: 7 hub `content/<lingua>/_index.md` + 21 pagine `cosa-fare-adesso`/`numeri-utili`/`piano-familiare` + `facile-da-leggere/{en,eo,ro,ar}` = 32 pagine. Nota: la mappa «4 pagine × 7 lingue» di CLAUDE.md/rule 09 §19 non corrisponde più al repo (esistono hub + 3 pagine, non `allerte-meteo` né `contatti`): da aggiornare.

### Bloccanti (dato istituzionale o comportamento diverso dall'italiano)

| Pagina | Lingue | Divergenza | Correzione |
|---|---|---|---|
| `piano-familiare` | tutte e 7 | riga 55: «acqua (3 L per persona)» senza «al giorno per 3 giorni»; canonico: ~4 L/persona/giorno per 3 giorni | 4 L/persona/giorno, per 3 giorni |
| hub, riquadro kit (riga 108) | fr, de, es, pt, ro, eo (en corretta) | «3 litri per persona» | allineare all'inglese: 4 L/persona/giorno per 3 giorni |
| `numeri-utili` (riga 42) | tutte e 7 | «In caso di emergenza contatta 112 **o 803 555**»: l'803 555 presentato come alternativa al 112 | «In un'emergenza chiama sempre il 112; l'803 555 serve per segnalazioni non urgenti» |

### Da sistemare

- **hreflang**: la famiglia `/facile-da-leggere/*` (it + en/eo/ro/ar) non emette `<link rel="alternate" hreflang>` (whitelist `$sezioniTradotte` non la copre; path non standard) → blocco `hreflang:` nel frontmatter come in `english/about-this-practice`.
- **og:locale**: `meta-social.html:66` non ha la chiave `ar` → la pagina araba emette `it_IT`. Aggiungere `"ar" "ar_AR"`.
- **tts: false** mancante sui 28 file hub+sottopagine (le 4 facile ce l'hanno): il TTS leggerebbe con voce italiana.
- **lang="it"** mancante su «Area di Attesa»/«aree di attesa» (26 occorrenze).
- **Copertura**: manca il box «Cosa NON fare» in tutte le `cosa-fare-adesso` tradotte; manca il 116117 (multilingue!) in tutte le `numeri-utili`; YouPol e «chiamata silenziosa» assenti; nelle 4 facile mancano «Vuoi saperne di più», «Schede con i simboli» (CAA), «ascoltare invece di leggere», link kit animali.
- **Esperanto**: «Operacia Salono» → probabilmente «Operacia Centro»; «Karabenistoj» → «Karabinieroj» (da verificare su PIV/Vikipedio).
- Le 7 traduzioni aggiungono «(anziani, bambini, persone con disabilità)» assente nel canonico: riportarlo nell'italiano o toglierlo.

## Parte C — Esercitazione della catena di emergenza (verbale dell'agente)

Scenario simulato in locale: arancione idrogeologica oggi, rossa domani → emergenza attiva → rientro a verde. Nessun commit, nessun workflow, nessun Telegram; dati ripristinati (`git status -- data/` vuoto).

| Anello | Esito |
|---|---|
| Parsing bollettino → `allerta.json` (`check-allerta.py` con fetch simulato) | ✅ livelli, `domani`, timestamp, anti-spam, stale-check, fallback PDF |
| `check-avvisi-meteo.py` / `check-rischi-incendi.py` | ⚠️ non provabili senza rete (nessun dry-run): da aggiungere un flag `--fixture` |
| Home: barra + blocco «domani» | ✅ server-rendered, `<noscript>` |
| `/allerte-meteo/` e `/cruscotto/` (shortcode `allerta-stato-attuale`) | ❌ **P1**: confronta `"giallo"`/`"rosso"` ma i dati dicono `"gialla"`/`"rossa"` → **allerta rossa mostrata con stile verde**; nessun blocco «domani» → **corretto lo stesso giorno** (livelli normalizzati, palette scoped `.allerta-stato-*` in `custom.css` al posto delle utility Bootstrap 5.3 assenti da Bootstrap Italia, blocco «domani»; verifica visiva desktop/mobile/contrasto giallo-su-nero) |
| `/emergenza/` lite | ❌ **P1**: CSS `.lite-allerta-giallo/-rosso` ma classe generata `-gialla/-rossa` → box senza colore per giallo e rosso; nessun blocco «domani» → **corretto lo stesso giorno** (selettori per entrambe le forme, livello scritto in chiaro, blocco «domani») |
| Banner emergenza site-wide, dual-mode home | ✅ nessun doppione, `role=alert` |
| CAP, `/allerta-stato/index.json` | ✅ coerenti in ogni fase |
| Telegram (testo generato, non inviato) | ❌ **P1/P2**: mancano «cosa fare» e «prossimo aggiornamento» (ISO 22329 punti 4 e 6), 3-4 emoji (tetto 2), nessun hashtag stabile → **corretto lo stesso giorno** (`scripts/notifica-telegram.py`: sei punti ISO 22329, azioni per livello/tipo dalle pagine canoniche, 2 emoji, hashtag stabili; dry-run dei cinque messaggi < 1.000 caratteri) |
| Degradazioni (DPC giù, CSV vuoto, no JS, immagini nascoste, screen reader) | ✅ |
| Fingerprint live | ⚠️ campione di 4 pagine tutte `a9b633a`; script completo non eseguibile per rete instabile |
| Tempi | ⚠️ stima teorica (≤5 min cron + build + FTP); run reali non consultabili dall'agente |
| Rientro e registro della prevenzione | ✅ (nessuna voce per scenario simulato, correttamente) |
| Produzione (sola lettura) | ✅; osservazione P3: `/allerta-stato/` senza slash-index risponde 403 Apache |

Correzione collaterale: in home, shortcode e pagina lite l'etichetta della pre-allerta era «Previsto domani (data): Previsto arancione» (titolo del data file ripetuto); ora «Previsto domani (data): allerta arancione», derivata dal livello. Backlog: flag `--fixture` per i tre script di parsing; risposta pulita per `/allerta-stato/` senza slash.

Prossima esercitazione: entro il 6 dicembre 2026 (trimestrale); una ripetizione breve dello scenario è stata fatta il 06/09/2026 dopo le correzioni (build con dati simulati gialla/rossa e rossa/arancione, dati ripristinati).

