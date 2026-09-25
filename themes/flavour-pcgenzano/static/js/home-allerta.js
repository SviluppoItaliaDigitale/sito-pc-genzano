/* ============================================================
   HOME-ALLERTA v1.0 — logica client delle barre di stato homepage.
   Estratto da layouts/index.html il 15/07/2026 (audit esterno:
   troppa logica inline nel template + parser CSV naïf).

   Contiene:
   1. Guard scadenza barra rischio incendi (nasconde la barra se la
      data di validità è passata anche quando l'HTML statico non è
      stato rigenerato — difesa complementare al guard di build Hugo).
   2. Allerta meteo DPC: legge i CSV per comune (opendatasicilia,
      bollettino-oggi + bollettino-domani), filtra per validità
      temporale, combina il MAX dei livelli e aggiorna le barre.
      Allineato alla logica server di check-allerta.yml.
      Aggiornamento: a ogni visita + ogni 30 minuti.

   Il parser CSV gestisce i campi tra virgolette (virgole e doppi
   apici interni, RFC 4180) e i fine-riga CRLF: lo split naïf su ','
   sbagliava colonna se un campo quotato conteneva una virgola.
   ============================================================ */
(function () {
  'use strict';

  /* ── 1. Guard scadenza barra incendi ── */
  (function () {
    var b = document.getElementById('incendi-bar'); if (!b) return;
    var d = b.getAttribute('data-valido'); if (!d) return;
    var t = new Date();
    var oggi = t.getFullYear() + '-' + ('0' + (t.getMonth() + 1)).slice(-2) + '-' + ('0' + t.getDate()).slice(-2);
    if (d < oggi) { b.style.display = 'none'; }
  })();

  /* ── 2. Allerta meteo DPC ── */

  // Split di una riga CSV secondo RFC 4180: campi quotati possono
  // contenere virgole e doppi apici raddoppiati ("").
  function splitCsvRiga(line) {
    var out = [], cur = '', inQ = false;
    for (var i = 0; i < line.length; i++) {
      var ch = line[i];
      if (inQ) {
        if (ch === '"') {
          if (line[i + 1] === '"') { cur += '"'; i++; }
          else inQ = false;
        } else cur += ch;
      } else {
        if (ch === '"') inQ = true;
        else if (ch === ',') { out.push(cur); cur = ''; }
        else cur += ch;
      }
    }
    out.push(cur);
    return out;
  }

  function parseBollettino(csv) {
    var lines = csv.replace(/\r/g, '').split('\n');
    if (lines.length < 2) return null;
    var header = splitCsvRiga(lines[0]);
    var col = {};
    for (var h = 0; h < header.length; h++) {
      var n = header[h].trim().toLowerCase();
      if (n.indexOf('data_validita_inizio') > -1) col.inizio = h;
      else if (n.indexOf('data_validita_fine') > -1) col.fine = h;
      else if (n.indexOf('avviso_criticita') > -1) col.criticita = h;
      else if (n.indexOf('avviso_idrogeologico') > -1) col.idrogeo = h;
      else if (n.indexOf('avviso_temporali') > -1) col.temporali = h;
      else if (n.indexOf('avviso_idraulico') > -1) col.idraulico = h;
    }
    for (var i = 1; i < lines.length; i++) {
      if (lines[i].toLowerCase().indexOf('genzano di roma') > -1) {
        var f = splitCsvRiga(lines[i]);
        var get = function (k) { return col[k] >= 0 && col[k] < f.length ? f[col[k]].trim() : ''; };
        return {
          inizio: get('inizio'),
          fine: get('fine'),
          criticita: get('criticita'),
          idrogeologico: get('idrogeo'),
          temporali: get('temporali'),
          idraulico: get('idraulico')
        };
      }
    }
    return null;
  }

  function levelFromValue(val) {
    var v = (val || '').toLowerCase();
    if (v.indexOf('allerta rossa') > -1) return 3;
    if (v.indexOf('allerta arancione') > -1) return 2;
    if (v.indexOf('allerta gialla') > -1) return 1;
    return 0;
  }

  /* Fail-safe di freschezza (audit 30/08/2026): quando la verifica live
     sul bollettino DPC fallisce, la barra resta com'era al build. Se
     l'ultimo controllo noto (data-controllo) ha più di 6 ore, lo stato
     NON deve continuare a sembrare attuale: la riga "Verificato" diventa
     un avviso esplicito che rimanda alla fonte ufficiale (rule 06 — mai
     spacciare per attuale un dato che non lo è). Con dato più fresco di
     6 ore non fa nulla: il timestamp già mostrato è onesto. */
  /* Stato neutro "non verificato": quando l'ultimo controllo riuscito ha
     più di 6 ore e il visitatore non riesce a leggere i bollettini, il
     colore e il titolo della barra non possono continuare a rassicurare
     (il verde resta il messaggio più forte della pagina). La barra passa
     al grigio e rimanda al bollettino ufficiale; la riga "Verificato"
     conserva l'ora dell'ultimo controllo riuscito (audit 25/09/2026). */
  function impostaStatoNonVerificato(bar) {
    var classi = bar.className.split(/\s+/);
    for (var i = 0; i < classi.length; i++) {
      if (classi[i].indexOf('allerta-bar-') === 0 && classi[i] !== 'allerta-bar-loading') {
        bar.classList.remove(classi[i]);
      }
    }
    bar.classList.add('allerta-bar-nonverificato');
    var t = document.getElementById('allerta-titolo');
    var d = document.getElementById('allerta-desc');
    var ic = document.getElementById('allerta-icon');
    if (t) t.textContent = 'STATO ALLERTA NON VERIFICATO';
    if (d) d.textContent = '\u2014 consulta il bollettino ufficiale del Centro Funzionale regionale.';
    if (ic) ic.className = 'bi bi-question-circle-fill me-2';
  }

  function segnalaDatoNonRecente(bar) {
    var iso = bar.getAttribute('data-controllo');
    if (!iso) return;
    var t = new Date(iso);
    if (isNaN(t.getTime())) return;
    if (Date.now() - t.getTime() < 6 * 60 * 60 * 1000) return;
    impostaStatoNonVerificato(bar);
    var ck = document.getElementById('allerta-controllo');
    if (!ck) return;
    var mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
    var pad = function (x) { return x < 10 ? '0' + x : '' + x; };
    ck.textContent = t.getDate() + ' ' + mesi[t.getMonth()] + ' ' + t.getFullYear() + ', ' + pad(t.getHours()) + ':' + pad(t.getMinutes()) + ' — dato non recente, consulta il bollettino del Centro Funzionale';
  }

  /* Nessun bollettino valido adesso (non ancora emesso, o l'ultimo è
     scaduto): lo stato mostrato resta quello del build e la riga "Verificato"
     dice, senza girarci intorno, che il bollettino non è verificabile in
     questo momento — mantenendo l'ora dell'ultimo controllo riuscito, mai
     quella corrente. */
  function segnalaBollettinoNonVerificabile(bar) {
    var ck = document.getElementById('allerta-controllo');
    if (!ck) return;
    var iso = bar.getAttribute('data-controllo');
    var quando = '';
    if (iso) {
      var t = new Date(iso);
      if (!isNaN(t.getTime())) {
        var mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
        var pad = function (x) { return x < 10 ? '0' + x : '' + x; };
        quando = t.getDate() + ' ' + mesi[t.getMonth()] + ' ' + t.getFullYear() + ', ' + pad(t.getHours()) + ':' + pad(t.getMinutes()) + ' — ';
      }
    }
    ck.textContent = quando + 'bollettino non verificabile in questo momento: consulta il Centro Funzionale regionale';
  }

  function checkAllertaDPC() {
    var bar = document.getElementById('allerta-bar');
    if (!bar) return;

    var BASE = 'https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/refs/heads/main/data/bollettini/';
    var URL_OGGI = BASE + 'bollettino-oggi-comuni-latest.csv';
    var URL_DOMANI = BASE + 'bollettino-domani-comuni-latest.csv';

    function fetchCsv(url) {
      return fetch(url).then(function (r) { return r.ok ? r.text() : null; }).catch(function () { return null; });
    }

    Promise.all([fetchCsv(URL_OGGI), fetchCsv(URL_DOMANI)])
      .then(function (results) {
        var now = new Date();
        var bollettini = [];
        for (var k = 0; k < results.length; k++) {
          if (!results[k]) continue;
          var b = parseBollettino(results[k]);
          if (!b) continue;
          var inizio = b.inizio ? new Date(b.inizio) : null;
          var fine = b.fine ? new Date(b.fine) : null;
          if (inizio && fine && now >= inizio && now <= fine) {
            bollettini.push(b);
          }
        }

        // Nessun bollettino nella sua finestra di validità: NON si ripiega su
        // uno scaduto. Fino al 14/09/2026 qui c'era un fallback che prendeva
        // comunque il "domani" o l'"oggi" disponibile ("meglio mostrare
        // qualcosa che niente") e più sotto la riga "Verificato" veniva
        // riscritta con l'ora corrente: il risultato era un bollettino
        // scaduto presentato come attuale, con un orario fresco. In protezione
        // civile è il contrario di ciò che serve (rule 06: mai spacciare per
        // attuale un dato che non lo è). Si tiene lo stato del build — che
        // check-allerta.py ha già filtrato per validità — e si dichiara che
        // in questo momento il bollettino non è verificabile.
        if (bollettini.length === 0) {
          bar.classList.remove('allerta-bar-loading');
          // Due casi diversi, due messaggi diversi: se i bollettini li abbiamo
          // letti ma sono tutti fuori validità, il dato non è verificabile
          // adesso; se invece non siamo riusciti a scaricarli (rete del
          // visitatore, fonte giù), il controllo fatto dal server resta valido
          // e va svalutato solo se è vecchio.
          var letti = false;
          for (var kr = 0; kr < results.length; kr++) { if (results[kr]) letti = true; }
          if (letti) segnalaBollettinoNonVerificabile(bar);
          else segnalaDatoNonRecente(bar);
          return;
        }

        var names = { 0: 'verde', 1: 'gialla', 2: 'arancione', 3: 'rossa' };
        var maxLevel = 0;
        var risksOrder = [];
        var risksSeen = {};
        var colonne = [
          { key: 'criticita', nome: 'Criticità' },
          { key: 'idrogeologico', nome: 'Idrogeologico' },
          { key: 'temporali', nome: 'Temporali' },
          { key: 'idraulico', nome: 'Idraulico' }
        ];

        for (var bi = 0; bi < bollettini.length; bi++) {
          var b2 = bollettini[bi];
          for (var c2 = 0; c2 < colonne.length; c2++) {
            var lev = levelFromValue(b2[colonne[c2].key]);
            if (lev > maxLevel) maxLevel = lev;
            if (lev > 0 && !risksSeen[colonne[c2].nome]) {
              risksSeen[colonne[c2].nome] = names[lev];
              risksOrder.push(colonne[c2].nome + ': ' + names[lev]);
            }
          }
        }

        var maxLiv = names[maxLevel];
        var titles = { verde: 'NESSUNA ALLERTA', gialla: 'ALLERTA GIALLA', arancione: 'ALLERTA ARANCIONE', rossa: 'ALLERTA ROSSA' };
        var descs = { verde: 'Non sono previsti fenomeni significativi sul nostro territorio.', gialla: 'Criticità ordinaria. Prestare attenzione.', arancione: 'Criticità moderata. Limitare gli spostamenti.', rossa: 'Criticità elevata. Seguire le indicazioni delle autorità.' };

        // Anti-flicker: se il livello calcolato dal CSV combacia con quello
        // già renderizzato dal server (classe CSS allerta-bar-<liv>), NON
        // sovrascrivere titolo/descrizione/icona: il testo del server è più
        // ricco e specifico. Sovrascrive solo se il LIVELLO è cambiato.
        var levelServer = null;
        var clsList = bar.className.split(/\s+/);
        for (var ci = 0; ci < clsList.length; ci++) {
          var c = clsList[ci];
          if (c.indexOf('allerta-bar-') === 0) {
            var suf = c.substring('allerta-bar-'.length);
            if (suf !== 'loading') levelServer = suf;
          }
        }
        if (levelServer !== maxLiv) {
          bar.className = 'allerta-bar allerta-bar-' + maxLiv;
          var t = document.getElementById('allerta-titolo');
          var d = document.getElementById('allerta-desc');
          var ic = document.getElementById('allerta-icon');
          if (t) t.textContent = titles[maxLiv];
          if (d) {
            var testo = '— ' + descs[maxLiv];
            if (risksOrder.length > 0) testo += ' (' + risksOrder.join(', ') + ')';
            d.textContent = testo;
          }
          if (ic) ic.className = maxLiv === 'verde' ? 'bi bi-shield-check me-2' : 'bi bi-exclamation-triangle-fill me-2';
        }

        // Aggiorna "Verificato: <ora>" con l'ora locale del client. Si arriva
        // qui solo con almeno un bollettino nella sua finestra di validità:
        // l'orario fresco certifica una verifica che è davvero avvenuta.
        var ck = document.getElementById('allerta-controllo');
        var mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
        if (ck) {
          var n = new Date();
          var pad = function (x) { return x < 10 ? '0' + x : '' + x; };
          ck.textContent = n.getDate() + ' ' + mesi[n.getMonth()] + ' ' + n.getFullYear() + ', ' + pad(n.getHours()) + ':' + pad(n.getMinutes());
        }

        // Pre-allerta DOMANI: se il bollettino-domani punta a un giorno
        // strettamente futuro con livello ≥ gialla, mostra la fascia.
        var barDomani = document.getElementById('allerta-bar-domani');
        var domaniRow = results[1] ? parseBollettino(results[1]) : null;
        var domaniLevel = 0;
        var domaniRisks = [];
        var domaniDate = null;
        if (domaniRow) {
          var inizioD = domaniRow.inizio ? new Date(domaniRow.inizio) : null;
          var p2 = function (x) { return x < 10 ? '0' + x : '' + x; };
          var oggiYMD = now.getFullYear() + '-' + p2(now.getMonth() + 1) + '-' + p2(now.getDate());
          var inizioYMD = inizioD ? inizioD.getFullYear() + '-' + p2(inizioD.getMonth() + 1) + '-' + p2(inizioD.getDate()) : null;
          if (inizioYMD && inizioYMD > oggiYMD) {
            for (var cd = 0; cd < colonne.length; cd++) {
              var levD = levelFromValue(domaniRow[colonne[cd].key]);
              if (levD > domaniLevel) domaniLevel = levD;
              if (levD > 0 && ['temporali', 'idrogeologico', 'idraulico'].indexOf(colonne[cd].key) >= 0) {
                var nomeR = colonne[cd].nome.toLowerCase();
                if (domaniRisks.indexOf(nomeR) < 0) domaniRisks.push(nomeR);
              }
            }
            domaniDate = inizioD;
          }
        }
        if (barDomani) {
          if (domaniLevel >= 1 && domaniDate) {
            var liv = names[domaniLevel];
            var titoloDom = { gialla: 'allerta gialla', arancione: 'allerta arancione', rossa: 'allerta rossa' }[liv];
            var dataLeg = domaniDate.getDate() + ' ' + mesi[domaniDate.getMonth()] + ' ' + domaniDate.getFullYear();
            barDomani.className = 'allerta-bar-domani allerta-bar-domani-' + liv;
            barDomani.style.display = '';
            var html = '<div class="container"><i class="bi bi-calendar-event me-2" aria-hidden="true"></i><strong>Previsto domani (' + dataLeg + '):</strong> <span id="allerta-domani-titolo">' + titoloDom + '</span>';
            if (domaniRisks.length > 0) html += ' <span class="text-nowrap">— ' + domaniRisks.join(', ') + '</span>';
            html += '</div>';
            barDomani.innerHTML = html;
          } else {
            barDomani.style.display = 'none';
          }
        }

        bar.classList.remove('allerta-bar-loading');
      })
      .catch(function () {
        bar.classList.remove('allerta-bar-loading');
        segnalaDatoNonRecente(bar);
      });
  }

  checkAllertaDPC();
  setInterval(checkAllertaDPC, 30 * 60 * 1000);
})();
