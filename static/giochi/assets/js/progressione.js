/* Sistema di progressione giochi — Protezione Civile Genzano
   Salva/legge risultati da localStorage. Namespace: pcgenzano.giochi.v1.<id>
   Badge sbloccato se percentuale >= 80%. */

(function (global) {
  'use strict';

  var NS = 'pcgenzano.giochi.v1.';
  var SOGLIA_BADGE = 80;

  // Catalogo ID giochi (per validazione/visualizzazione)
  // Gli ID devono corrispondere a quelli passati a GiochiUtil.salvaEMostraAttestato
  // o GiochiPC.salvaRisultato nei singoli giochi.
  var CATALOGO = {
    // Infanzia 3-6 (8 giochi)
    'tartaruga-saggia':       { nome: 'La Tartaruga Saggia',        fascia: 'infanzia', icona: 'bi-shield-shaded' },
    'numero-emergenza':       { nome: 'Il Numero 112',              fascia: 'infanzia', icona: 'bi-telephone-fill' },
    'suoni-emergenza':        { nome: 'I Suoni dell’Emergenza',fascia: 'infanzia', icona: 'bi-volume-up-fill' },
    'memory-facile':          { nome: 'Memory Facile',              fascia: 'infanzia', icona: 'bi-grid-3x3-gap-fill' },
    'vesti-tina':             { nome: 'Lo Zaino di Tina',           fascia: 'infanzia', icona: 'bi-backpack-fill' },
    'rifugio-tina':           { nome: 'Il Rifugio di Tina',         fascia: 'infanzia', icona: 'bi-house-fill' },
    'cielo-oggi':             { nome: 'Il Cielo di Oggi',           fascia: 'infanzia', icona: 'bi-cloud-sun-fill' },
    'trova-cartello':         { nome: 'Trova il Cartello',          fascia: 'infanzia', icona: 'bi-sign-turn-right-fill' },
    // Primaria 6-11 (13 giochi)
    'quiz-primaria':          { nome: 'Quiz della Sicurezza',       fascia: 'primaria', icona: 'bi-question-circle-fill' },
    'memory-primaria':        { nome: 'Memory dei Rischi',          fascia: 'primaria', icona: 'bi-grid-3x3-gap-fill' },
    'caccia-al-rischio':      { nome: 'Caccia al Rischio',          fascia: 'primaria', icona: 'bi-search' },
    'zaino-emergenza':        { nome: 'Lo Zaino di Emergenza',      fascia: 'primaria', icona: 'bi-backpack2-fill' },
    'semaforo-rischio':       { nome: 'Il Semaforo del Rischio',    fascia: 'primaria', icona: 'bi-stoplights-fill' },
    'cosa-faccio-se':         { nome: 'Cosa Faccio Se…',       fascia: 'primaria', icona: 'bi-signpost-split-fill' },
    'abbina-impara':          { nome: 'Abbina e Impara',            fascia: 'primaria', icona: 'bi-link-45deg' },
    'anagrammi':              { nome: 'Anagrammi della Sicurezza',  fascia: 'primaria', icona: 'bi-shuffle' },
    'cruciverba':             { nome: 'Cruciverba della Sicurezza', fascia: 'primaria', icona: 'bi-grid-3x3' },
    'puzzle-scenari':         { nome: 'Puzzle degli Scenari',       fascia: 'primaria', icona: 'bi-list-check' },
    'labirinto-evacuazione':  { nome: 'Labirinto di Evacuazione',   fascia: 'primaria', icona: 'bi-signpost-2-fill' },
    'chiamata-112':           { nome: 'Chiamata al 112',            fascia: 'primaria', icona: 'bi-telephone-fill' },
    'posiziona-cartelli':     { nome: 'Posiziona i Cartelli',       fascia: 'primaria', icona: 'bi-sign-turn-right-fill' },
    // Ragazzi 11-19 (9 giochi)
    'simulatore-coc':         { nome: 'Simulatore COC',             fascia: 'ragazzi',  icona: 'bi-diagram-3-fill' },
    'emergency-responder':    { nome: 'Emergency Responder',        fascia: 'ragazzi',  icona: 'bi-person-walking' },
    'mappa-rischio':          { nome: 'La Mappa del Rischio',       fascia: 'ragazzi',  icona: 'bi-geo-alt-fill' },
    'radio-emergency':        { nome: 'Radio Emergency',            fascia: 'ragazzi',  icona: 'bi-broadcast' },
    'codice-arancione':       { nome: 'Codice Arancione',           fascia: 'ragazzi',  icona: 'bi-bounding-box' },
    'vero-o-bufala':          { nome: 'Vero o bufala?',             fascia: 'ragazzi',  icona: 'bi-patch-check-fill' },
    'triage-start':           { nome: 'Triage S.T.A.R.T.',          fascia: 'ragazzi',  icona: 'bi-heart-pulse-fill' },
    'linea-tempo-eventi':     { nome: 'Linea del tempo',            fascia: 'ragazzi',  icona: 'bi-calendar-event-fill' },
    'cartelli-pericolo':      { nome: 'Cartelli di Pericolo',       fascia: 'ragazzi',  icona: 'bi-exclamation-diamond-fill' }
  };

  var IDS = Object.keys(CATALOGO);

  function log() {
    try {
      var args = Array.prototype.slice.call(arguments);
      args.unshift('[GiochiPC]');
      console.log.apply(console, args);
    } catch (e) { /* noop */ }
  }

  function chiave(id) { return NS + id; }

  function safeParse(s) {
    try { return JSON.parse(s); } catch (e) { return null; }
  }

  function leggiGrezzo(id) {
    try {
      if (typeof localStorage === 'undefined') return null;
      var s = localStorage.getItem(chiave(id));
      return s ? safeParse(s) : null;
    } catch (e) {
      log('localStorage non disponibile (read):', e && e.message);
      return null;
    }
  }

  function scriviGrezzo(id, valore) {
    try {
      if (typeof localStorage === 'undefined') return false;
      localStorage.setItem(chiave(id), JSON.stringify(valore));
      return true;
    } catch (e) {
      log('localStorage non disponibile (write):', e && e.message);
      return false;
    }
  }

  function salvaRisultato(id, punteggio, max) {
    if (!id || typeof punteggio !== 'number' || typeof max !== 'number' || max <= 0) return null;
    var perc = Math.round((punteggio / max) * 100);
    var precedente = leggiGrezzo(id);
    var tentativi = (precedente && precedente.tentativi) ? precedente.tentativi + 1 : 1;
    // Mantieni il miglior punteggio
    var migliore = precedente && precedente.percentuale >= perc ? precedente : null;
    var record = migliore ? {
      punteggio: migliore.punteggio,
      max: migliore.max,
      percentuale: migliore.percentuale,
      data: migliore.data,
      tentativi: tentativi,
      ultimoPunteggio: punteggio,
      ultimoMax: max,
      ultimaPercentuale: perc,
      ultimaData: new Date().toISOString()
    } : {
      punteggio: punteggio,
      max: max,
      percentuale: perc,
      data: new Date().toISOString(),
      tentativi: tentativi,
      ultimoPunteggio: punteggio,
      ultimoMax: max,
      ultimaPercentuale: perc,
      ultimaData: new Date().toISOString()
    };
    scriviGrezzo(id, record);
    log('salvaRisultato', id, perc + '%', 'badge=' + (perc >= SOGLIA_BADGE));
    return record;
  }

  function leggiRisultato(id) {
    var r = leggiGrezzo(id);
    if (!r) return { completato: false, punteggio: 0, max: 0, percentuale: 0, data: null, tentativi: 0 };
    return {
      completato: true,
      punteggio: r.punteggio || 0,
      max: r.max || 0,
      percentuale: r.percentuale || 0,
      data: r.data || null,
      tentativi: r.tentativi || 1
    };
  }

  function elencoBadge() {
    var out = [];
    for (var i = 0; i < IDS.length; i++) {
      var id = IDS[i];
      var r = leggiRisultato(id);
      out.push({
        id: id,
        nome: CATALOGO[id].nome,
        fascia: CATALOGO[id].fascia,
        icona: CATALOGO[id].icona,
        completato: r.completato,
        percentuale: r.percentuale,
        ottenuto: r.percentuale >= SOGLIA_BADGE,
        data: r.data
      });
    }
    return out;
  }

  function reset() {
    try {
      if (typeof localStorage === 'undefined') return false;
      for (var i = 0; i < IDS.length; i++) {
        localStorage.removeItem(chiave(IDS[i]));
      }
      log('reset completato');
      return true;
    } catch (e) { return false; }
  }

  function formattaData(iso) {
    if (!iso) return '';
    try {
      var d = new Date(iso);
      return d.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric' });
    } catch (e) { return ''; }
  }

  global.GiochiPC = {
    salvaRisultato: salvaRisultato,
    leggiRisultato: leggiRisultato,
    elencoBadge: elencoBadge,
    reset: reset,
    formattaData: formattaData,
    CATALOGO: CATALOGO,
    IDS: IDS,
    SOGLIA_BADGE: SOGLIA_BADGE
  };
})(typeof window !== 'undefined' ? window : this);
