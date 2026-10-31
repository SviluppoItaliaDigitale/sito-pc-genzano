# three.js (copia locale)

Libreria 3D usata solo dalla pagina «Il libro che si esplora» (`/formazione/libro-che-si-esplora/`, script `static/js/libro-3d.js`). È copiata qui perché la Content-Security-Policy del sito non ammette script da CDN.

- Versione: three.js r160 (pacchetto npm `three@0.160.0`), licenza MIT (file `LICENSE`).
- File: `build/three.module.min.js` e `examples/jsm/controls/OrbitControls.js`. In `OrbitControls.js` l'import `from 'three'` è sostituito con `from './three.module.min.js'`, perché il sito non usa una import map.
- Aggiornamento: riscaricare gli stessi due file della nuova versione da `https://cdn.jsdelivr.net/npm/three@<versione>/`, ripetere la sostituzione dell'import, provare tutti i capitoli della pagina.
