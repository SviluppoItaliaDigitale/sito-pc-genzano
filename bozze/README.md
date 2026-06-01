# bozze/ — articoli in lavorazione (NON online)

Questa cartella contiene le **bozze** degli articoli: testi in lavorazione che
**non vanno mai pubblicati sul sito** finché non sei tu a deciderlo.

## Perché qui e non in `content/comunicazioni/`

Hugo costruisce il sito **solo** da `content/`, `static/`, `themes/`, `data/`,
`assets/`, `layouts/`. Una cartella di livello root come `bozze/` (esattamente
come `riferimenti-interni/`) **resta fuori dal sito**: né su Aruba né su GitHub
Pages. Una bozza qui dentro **non può finire online per sbaglio**.

Questo evita il problema che aveva fatto togliere `draft: true` a maggio 2026:
le bozze dentro `content/` si accumulavano dimenticate e rischiavano di andare
live. Qui invece sono separate in modo netto.

## Come si usano (script `gestione-sito.sh`)

- **Crea bozza** (voce 5) → scrive un file `bozze/<slug>.md`.
- **Modifica bozza** (voce 6) → apre la bozza con nano.
- **Pubblica bozza** (voce 7) → chiede la data, sposta il file in
  `content/comunicazioni/<data>-<slug>.md` con `draft: false`. Da quel momento
  è un articolo normale: per mandarlo online usa "Pubblica modifiche online".
- **Elimina bozza** (voce 8) → cancella la bozza.

Le bozze sono tracciate da git, quindi una bozza iniziata sul PC è modificabile
anche da mobile/cloud (sincronizzate via GitHub).

## Articoli sospesi in attesa di ufficialità

- **`2026-06-01-avvio-campagna-aib-lazio-2026.md`** (+ versione facile) —
  sospeso il 1 giugno 2026 perché l'avvio della campagna antincendio boschivo
  del Lazio **non era ancora ufficiale** (manca il decreto/atto regionale con la
  data). La cover resta in `static/images/`. Per **ripubblicarlo** quando esce
  l'atto ufficiale: aggiorna il campo `date:` alla data reale, sposta i due file
  in `content/comunicazioni/<data>-<slug>.md`, e ricontrolla regole e divieti
  citati con la fonte ufficiale. I QR verranno rigenerati al deploy.
