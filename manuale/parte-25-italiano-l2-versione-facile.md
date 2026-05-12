# Parte 25 — Versione "italiano semplice" (A2 CEFR) per gli articoli

Aggiunta a maggio 2026 nell'ambito del **Punto 16 della roadmap accessibilità**.

Per ogni articolo "complesso" del sito (specialmente quelli normativi, scientifici, tecnici) è possibile creare in parallelo una **versione semplificata** in italiano L2 livello **A2** del Quadro Europeo CEFR. Le due versioni vivono come file Markdown affiancati nel repo, Hugo le renderizza come pagine separate, e un banner in cima a ciascuna permette di passare dall'una all'altra con un click.

## 25.1 Perché esiste

Il sito istituzionale parla a **tutta la cittadinanza di Genzano**, non solo agli italiani madrelingua. Sul territorio vivono:

- **Parlanti italiano L2** (immigrazione di prima generazione, lavoratori stagionali, studenti stranieri).
- **Persone con disabilità cognitive** o difficoltà di lettura (dislessia, deficit cognitivi lievi).
- **Anziani** con esperienza scolastica limitata o con declino cognitivo precoce.
- **Cittadini che leggono in fretta** o in stress (durante un'emergenza, prima di uscire).

Per loro un articolo scritto in italiano AGID standard (frasi 18-22 parole, lessico amministrativo, sigle, riferimenti normativi) può essere troppo denso. Una versione "italiano semplice" — frasi corte 8-12 parole, parole comuni, sigle spiegate, esempi concreti — diventa il **ponte** che permette di ricevere lo stesso messaggio essenziale.

## 25.2 Convenzione di naming

Coppia di file Markdown nella stessa cartella, con suffisso `-facile`:

```
content/comunicazioni/
  ├── 2026-05-12-iso-22324-codici-colore-allerta.md          ← versione completa
  └── 2026-05-12-iso-22324-codici-colore-allerta-facile.md   ← versione italiano semplice (A2)
```

Stessa data, stesso slug-base, suffisso `-facile`. Hugo genera due URL distinti:

```
/comunicazioni/2026-05-12-iso-22324-codici-colore-allerta/         ← completa
/comunicazioni/2026-05-12-iso-22324-codici-colore-allerta-facile/  ← facile
```

## 25.3 Frontmatter incrociato

**Sull'articolo completo** aggiungere:

```yaml
versione_facile: "2026-05-12-iso-22324-codici-colore-allerta-facile"
```

**Sull'articolo facile** aggiungere:

```yaml
versione_facile_di: "2026-05-12-iso-22324-codici-colore-allerta"
```

Il valore è lo **slug** (file basename senza `.md`), NON l'URL completo.

Frontmatter completo della versione facile (esempio):

```yaml
---
title: "Perché le allerte hanno colori? Versione facile da leggere"
date: 2026-05-12T00:03:00+02:00
description: "Versione semplificata (italiano A2) dell'articolo sui codici colore delle allerte. Frasi corte, parole comuni."
badge: "Informazione"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: ""
image_alt: ""
scadenza: ""
area: "Lazio"
allegati: []
versione_facile_di: "2026-05-12-iso-22324-codici-colore-allerta"
draft: false
_build:
  list: false
  render: true
---
```

**Note operative:**
- `image: ""` sulla versione facile → Hugo genererà automaticamente una cover tipografica (vedi regola progetto sul banner). Mai una foto utente.
- `date` della versione facile: usare lo **stesso giorno** della versione completa con orario leggermente posteriore (`T00:03` vs `T00:02`) per mantenere l'ordering cronologico Hugo.
- `description`: indicare chiaramente che è la **versione semplificata**.
- **`_build.list = false` OBBLIGATORIO** (vedi § 25.11 sotto).

## 25.4 Bottone toggle (automatico via partial)

Il partial `themes/flavour-pcgenzano/layouts/partials/versione-facile-toggle.html` viene chiamato in cima a ogni articolo da `_default/single.html` e mostra:

- **Sulla versione standard** (se ha `versione_facile` nel frontmatter):
  > 📖 **Leggi in italiano semplice** \[A2\]
  >
  > Esiste una versione di questo articolo in italiano semplificato (livello A2 — Quadro Europeo CEFR), pensata per parlanti italiano L2, persone con disabilità cognitive, anziani e chi legge in fretta.

- **Sulla versione facile** (se ha `versione_facile_di`):
  > 🟡 **Italiano semplice — Livello A2**
  >
  > Questa è la versione facile da leggere dell'articolo. Frasi corte, parole comuni. Per il testo completo, con tutti i dettagli e le fonti, leggi la **versione completa**.

Stile visivo distintivo (background giallo chiaro `#fff8e1`, bordo sinistro `#ffb300`) per essere riconoscibile senza disturbare gli altri lettori. Nascosto in stampa.

## 25.5 Eccezione gate AGID

L'articolo facile **NON** segue il linguaggio AGID standard (frasi 18-22 parole, lessico amministrativo, retorica istituzionale). Usa invece le regole **CEFR A2**:

- Frasi corte (8-12 parole massimo).
- Lessico delle 2000 parole più frequenti dell'italiano.
- Verbi al presente indicativo come default; passato prossimo solo per fatti recenti.
- Sigle **spiegate la prima volta** (es. "il 112, il numero unico europeo").
- Numeri scritti in cifre, mai in lettere.
- Liste numerate per passi sequenziali.
- Niente subordinate concatenate, niente incidentali.
- Niente metafore, niente retorica.

Questo è un **registro deliberatamente diverso** dall'AGID per il cittadino. La regola progetto (`CLAUDE.md` § "Auto-gate AGID prima del commit di un nuovo articolo") prevede esplicitamente l'**eccezione "registro non-AGID su richiesta esplicita dell'utente"**: la versione facile rientra in questa categoria.

**Implicazione operativa**: NON invocare l'agent `pc-article-reviewer` sui file `.md` che hanno `versione_facile_di` nel frontmatter — l'agent rigetterebbe le frasi "troppo corte" o "tono troppo elementare". Il review della versione facile va fatto secondo i criteri CEFR A2, non secondo l'AGID.

## 25.6 Come generare una versione facile (workflow)

La generazione è **on-demand**, una conversazione alla volta con un'IA o riscrittura manuale:

1. **Apri l'articolo standard** in `content/comunicazioni/<slug>.md`.
2. **Chiedi a Claude / ChatGPT / Gemini**: "Genera la versione facile da leggere di questo articolo in italiano L2 livello A2 CEFR: frasi corte 8-12 parole, parole comuni, sigle spiegate, niente subordinate, niente retorica. Mantieni il messaggio essenziale ma elimina i dettagli normativi e le sfumature."
3. **Verifica manualmente** la bozza prodotta: rileggi con la voce di un parlante L2.
4. **Salva** in `content/comunicazioni/<slug>-facile.md` con frontmatter `versione_facile_di: <slug>` + le altre proprietà come da § 25.3.
5. **Aggiungi** `versione_facile: <slug>-facile` al frontmatter dell'articolo originale.
6. **Build Hugo locale** + verifica visiva del bottone toggle su entrambe le pagine.
7. **Commit** e push.

**Costo**: zero costi runtime (il sito è statico, le pagine sono pre-renderizzate). Solo tempo redazionale on-demand.

## 25.7 Quali articoli meritano la versione facile?

Non tutti. Priorità:

**Alta priorità:**
- Bollettini di allerta meteo / criticità (devono raggiungere tutti).
- Procedure di autoprotezione (terremoti, alluvioni, incendi).
- Numeri di emergenza (112, 115, ecc.).
- Iscrizioni volontariato / corsi base.
- Articoli su standard internazionali (ISO 22324, ISO 22320 — sono normalmente densi).

**Media priorità:**
- Anniversari di eventi storici.
- Articoli normativi.
- Approfondimenti scientifici (sismologia, idrogeologia).

**Bassa priorità (probabilmente non serve):**
- Comunicati interni del Gruppo (eventi di servizio, anniversari interni).
- Aggiornamenti routine (presa servizio, esercitazioni passate).

**Mai**: articoli a contenuto giuridico stretto (delibere, ordinanze) — la semplificazione potrebbe alterare il valore giuridico, e questi documenti sono già accompagnati dai PDF originali in allegato.

## 25.8 Esempio campione disponibile

Come riferimento operativo, c'è una versione facile completa del primo articolo: [ISO 22324 — Codici colore delle allerte](/comunicazioni/2026-05-12-iso-22324-codici-colore-allerta-facile/). Mostra il pattern da seguire (frontmatter, struttura, stile, link alla versione completa).

## 25.9 Cosa NON entra nell'MVP

1. **Generazione automatica via API LLM** (Gemini/Claude API runtime): le versioni facili sono on-demand, redatte dall'autore, non automatiche. Costo zero, controllo qualità massimo.
2. **Audit automatico CEFR**: nessuno script che verifica che la versione facile rispetti effettivamente A2 (es. contando frasi >15 parole). Possibile aggiunta futura via `scripts/audit-italiano-facile.py`.
3. **Multilingua sulla versione facile**: per ora solo italiano A2. Versioni inglese / arabo / rumeno / cinese semplificate sono fuori scope (esisterebbe la traduzione automatica di Chrome/iOS).
4. **Toggle "Mostra entrambe affiancate"** (split-view): l'utente sceglie una versione e legge solo quella. Niente UI complessa.

## 25.11 Hide dalle liste — `_build.list = false` OBBLIGATORIO

Da 12 maggio 2026 (revisione richiesta dall'utente dopo prima pubblicazione P16) **ogni file `<slug>-facile.md` deve avere `_build.list: false` nel frontmatter**. Senza questa regola la versione facile compariva in homepage come "ultima notizia" doppia, nell'archivio `/comunicazioni/`, nella pagina `/podcast/`, nel feed RSS e nell'indice di ricerca — confondendo gli utenti.

Lo standard Hugo `_build`:

```yaml
_build:
  list: false       # esclusa da homepage, archivio, RSS, sitemap,
                    # podcast list, articoli correlati, index.json (ricerca)
  render: true      # ma resta renderizzata come pagina HTML accessibile
                    # via URL diretto
```

**Cosa esclude `_build.list: false`:**
- `where .Site.RegularPages "..."` → niente più in homepage `partials/latest-news.html`
- `.Site.AllPages` → niente più in `index.json` di ricerca, sitemap.xml, RSS feed di sezione
- `articoli-correlati.html` (legge da `.Site.RegularPages`) → niente più nei correlati
- `podcast/list.html` (filtra da `.Site.RegularPages`) → niente più in /podcast/

**Cosa resta funzionante:**
- URL diretto `/comunicazioni/<slug>-facile/` → HTML renderizzato (perché `render: true`)
- Bottone "Leggi in italiano semplice" sull'articolo madre (lo costruisce il partial `versione-facile-toggle.html` leggendo `Params.versione_facile`, non `Site.Pages`)
- Bottone "Torna alla versione completa" sulla versione facile (legge dal proprio frontmatter `versione_facile_di`)

**Risultato netto:** la versione facile è raggiungibile **solo** dall'articolo madre. Non appare in nessuna lista pubblica. Esattamente il comportamento richiesto.

## 25.12 Riferimenti

- **CEFR (Quadro Comune Europeo di Riferimento per le Lingue)** — Consiglio d'Europa: <https://www.coe.int/en/web/common-european-framework-reference-languages/>
- **Italiano L2 A2** — descrittori ufficiali: comprensione di frasi e parole frequenti su famiglia, lavoro, ambiente immediato. Lettura di testi brevi con vocabolario ad alta frequenza.
- **AGID — Linguaggio della PA**: <https://www.agid.gov.it/it/argomenti/comunicare-online> (l'eccezione A2 è documentata in CLAUDE.md § "Auto-gate AGID").
- **Pagina "Facile da leggere" del sito**: <https://www.protezionecivilegenzano.it/facile-da-leggere/> — sezione dedicata con linguaggio + pittogrammi ARASAAC.
