/* ============================================================
   PC-FETCH-CACHE v1.0 — "ultimo dato valido" per il cruscotto.
   Le schede dati (INGV, Open-Meteo, ItaliaMeteo, Copernicus EMS)
   salvano in localStorage l'ultimo payload ricevuto con successo;
   se la fonte esterna non risponde (tipico proprio durante una
   crisi su vasta scala), la scheda mostra i dati dell'ultimo
   aggiornamento riuscito CON ETICHETTA ONESTA di data/ora — mai
   spacciati per attuali (comunicazione del rischio, rule 06).

   API (tutte fail-safe: localStorage assente/pieno = no-op):
     pcCache.salva(chiave, dati)        → memorizza {t, d}
     pcCache.leggi(chiave, maxOre)      → {t, d} | null (scaduto = null)
     pcCache.frase(t)                   → testo per la riga di stato
   ============================================================ */
(function () {
  'use strict';

  var PREFISSO = 'pcgz-cache:';

  function salva(chiave, dati) {
    try {
      localStorage.setItem(PREFISSO + chiave, JSON.stringify({ t: Date.now(), d: dati }));
    } catch (e) { /* quota piena o storage negato: pazienza */ }
  }

  function leggi(chiave, maxOre) {
    try {
      var raw = localStorage.getItem(PREFISSO + chiave);
      if (!raw) return null;
      var o = JSON.parse(raw);
      if (!o || o.d == null || typeof o.t !== 'number') return null;
      if (maxOre && (Date.now() - o.t) > maxOre * 3600000) return null;
      return o;
    } catch (e) { return null; }
  }

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function frase(t) {
    var d = new Date(t);
    return 'Fonte al momento non raggiungibile — dati dell’ultimo aggiornamento riuscito: ' +
      pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + ' alle ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
  }

  window.pcCache = { salva: salva, leggi: leggi, frase: frase };
})();
