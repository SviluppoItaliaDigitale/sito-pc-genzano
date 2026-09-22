# satellite.js — propagazione orbitale SGP4

Libreria vendorizzata, **non** caricata da CDN (stessa regola di Leaflet e del
bundle Bootstrap Italia: la CSP del sito non consente script di terze parti).

- **Versione**: 6.0.0, bundle UMD `satellite.min.js` (24 KB)
- **Licenza**: MIT (`LICENSE.md` in questa cartella)
- **Origine**: pacchetto npm `satellite.js@6.0.0`, file `dist/satellite.min.js`
- **Usata da**: `static/monitor/index.html`, vista SATELLITI

## Perché la 6 e non la 7

La 7.x è distribuita come moduli ES con una componente WebAssembly: servirebbe un
passaggio di compilazione che questo sito non ha. La 6.0.0 è l'ultima che
pubblica un bundle UMD caricabile con un normale `<script>`.

## Perché una libreria e non una formula

La propagazione SGP4 è il modello con cui sono definite le TLE stesse: calcolare
una posizione "per approssimazione" produrrebbe un dato inventato. Verificato il
22/09/2026 contro una fonte indipendente sulla posizione della ISS: **scarto di
0,4 km in orizzontale e 0,0 km in quota**.

## Aggiornare

Scaricare `dist/satellite.min.js` dalla versione 6.x più recente su npm e
rifare la verifica di cui sopra prima di committare.
