# Librerie per nome e cognome sugli oggetti della stampa 3D

Usate da `js/stampa3d-nome.js` e `js/stampa3d-nome-core.js` (pagine `/stampa-3d/<oggetto>/`), e dalla
prova `scripts/prova-stampa3d-nome.mjs`. Copia locale perché la CSP non ammette script di terzi.
Si caricano solo quando il volontario preme «Aggiungi»: nessuna richiesta fuori dal sito.

| File | Progetto | Versione | Licenza | Fonte |
|---|---|---|---|---|
| `manifold.js`, `manifold.wasm` | manifold-3d (Emmett Lalish e collaboratori) | 3.5.5 | Apache 2.0 (`LICENSE-manifold.txt`) | npm `manifold-3d` |
| `opentype.min.mjs` | opentype.js (Frederik De Bleser e collaboratori) | 2.0.0 | MIT (`LICENSE-opentype.txt`) | npm `opentype.js`, `dist/opentype.min.mjs` senza la riga `sourceMappingURL` |
| `LiberationSans-Bold.ttf` | Liberation Fonts | 2.1 | SIL Open Font License 1.1 (`LICENSE-liberation-OFL.txt`) | stesso carattere dei modelli OpenSCAD |

Aggiornare: scaricare la nuova versione da npm, sostituire i file, poi
`node scripts/prova-stampa3d-nome.mjs /tmp/prova-nome && python3 scripts/genera-stampa-3d.py --prova-nome /tmp/prova-nome`
(ogni oggetto deve restare un pezzo solo, chiuso e senza supporti).
