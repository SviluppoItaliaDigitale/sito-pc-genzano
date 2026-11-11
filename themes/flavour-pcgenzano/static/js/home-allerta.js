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
  /* Stato neutro «da confermare»: quando l'ultimo controllo riuscito ha
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
    if (t) t.textContent = 'STATO DELL\u2019ALLERTA DA CONFERMARE';
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
    ck.textContent = t.getDate() + ' ' + mesi[t.getMonth()] + ' ' + t.getFullYear() + ', ' + pad(t.getHours()) + ':' + pad(t.getMinutes()) + ' — ultimo controllo di oltre 6 ore fa';
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
        // check-allerta.py ha già filtrato per validità, leggendo anche il PDF
        // del Centro Funzionale — con l'ora del suo ultimo controllo riuscito;
        // se quel controllo ha più di 6 ore lo dice segnalaDatoNonRecente.
        // Fino all'11/11/2026, con i CSV letti ma fuori validità, la riga
        // diventava «bollettino non verificabile in questo momento»: il CSV di
        // opendatasicilia era fermo al 9/11, il server leggeva il PDF, e la
        // frase era falsa e si leggeva come un guasto del sito.
        if (bollettini.length === 0) {
          bar.classList.remove('allerta-bar-loading');
          segnalaDatoNonRecente(bar);
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
        // Il browser legge solo il CSV del Dipartimento, mentre il livello
        // del build combina quel CSV con il bollettino del Centro Funzionale
        // della Regione Lazio (check-allerta.py, dall'08/10/2026). Quel giorno
        // la Regione ha portato la Zona F ad arancione a mezzogiorno con il
        // CSV DPC ancora fermo alla gialla: se il browser potesse abbassare il
        // livello, la homepage avrebbe mostrato gialla a chi la apriva. Qui si
        // può solo ALZARE il livello del build, mai abbassarlo: i declassamenti
        // arrivano con il deploy urgente che check-allerta lancia a ogni
        // cambio di livello, entro pochi minuti.
        var ordine = { verde: 0, gialla: 1, arancione: 2, rossa: 3 };
        var piuBasso = levelServer && ordine[levelServer] !== undefined && maxLevel < ordine[levelServer];
        if (piuBasso) {
          bar.classList.remove('allerta-bar-loading');
          // Resta il livello del build, ma se il suo controllo ha più di 6 ore lo si dice.
          segnalaDatoNonRecente(bar);
          return;
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
        // Come per oggi: il browser non abbassa né nasconde la pre-allerta del build.
        var domaniServer = 0;
        if (barDomani && barDomani.style.display !== 'none') {
          var mD = barDomani.className.match(/allerta-bar-domani-(gialla|arancione|rossa)/);
          if (mD) domaniServer = { gialla: 1, arancione: 2, rossa: 3 }[mD[1]];
        }
        if (barDomani && domaniLevel >= domaniServer) {
          if (domaniLevel >= 1 && domaniDate) {
            var liv = names[domaniLevel];
            var titoloDom = { gialla: 'allerta gialla', arancione: 'allerta arancione', rossa: 'allerta rossa' }[liv];
            var gDom = giornoRoma(domaniDate);
            barDomani.className = 'allerta-bar-domani allerta-bar-domani-' + liv;
            barDomani.style.display = '';
            var html = '<div class="container"><i class="bi bi-calendar-event me-2" aria-hidden="true"></i><strong><span data-giorno="' + gDom + '">' + etichetta(gDom, 'giorno', giornoRoma(new Date())) + '</span>:</strong> prevista <span id="allerta-domani-titolo">' + titoloDom + '</span>';
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

  /* ── 3. Giorni e avviso meteo: «Oggi», «Domani», «in vigore» ──
     Le etichette dei giorni le scrive la build, in ora italiana
     (partials/etichetta-giorno.html), ma la pagina può restare aperta oltre
     la mezzanotte o venire da una build della sera prima: qui si ricalcolano
     con l'orologio del dispositivo, sempre in ora italiana, al caricamento,
     ogni minuto e quando la scheda torna in primo piano. A mezzanotte
     «Domani, giovedì 12 novembre» diventa «Oggi, giovedì 12 novembre».
     Stesse parole del partial: chi cambia l'uno cambia anche l'altro.
     L'avviso meteo passa da «Da domani…» (toni tenui, role="status") a
     «in vigore» (toni pieni, role="alert", subito sotto la striscia di oggi)
     all'ora d'inizio, e sparisce alla scadenza. Nato l'11/11/2026: la
     striscia del vento previsto per il giorno dopo non diceva il giorno e,
     sotto «Nessuna allerta», sembrava già in vigore. */
  var GIORNI = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
  var MESI_NOMI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
  var TITOLO_PRECISATO = 'NESSUNA ALLERTA PER RISCHIO IDROGEOLOGICO E IDRAULICO';
  var RE_GIORNO = /^\d{4}-\d{2}-\d{2}$/;

  function due(x) { return (x < 10 ? '0' : '') + x; }

  // Giorno 'AAAA-MM-GG' di un istante, in ora italiana.
  function giornoRoma(d) {
    try {
      var parti = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(d);
      var o = {};
      for (var i = 0; i < parti.length; i++) o[parti[i].type] = parti[i].value;
      if (o.year && o.month && o.day) return o.year + '-' + o.month + '-' + o.day;
    } catch (e) { /* browser senza fusi orari: si usa l'ora del dispositivo */ }
    return d.getFullYear() + '-' + due(d.getMonth() + 1) + '-' + due(d.getDate());
  }

  function utcDaGiorno(g, piu) {
    var a = g.split('-');
    return new Date(Date.UTC(+a[0], +a[1] - 1, +a[2] + (piu || 0)));
  }

  function nomeGiorno(g) {
    var d = utcDaGiorno(g);
    return GIORNI[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MESI_NOMI[d.getUTCMonth()];
  }

  function etichetta(g, forma, oggi) {
    var nome = nomeGiorno(g);
    var dd = utcDaGiorno(oggi, 1);
    var domani = dd.getUTCFullYear() + '-' + due(dd.getUTCMonth() + 1) + '-' + due(dd.getUTCDate());
    if (forma === 'da') return g === oggi ? 'Da oggi, ' + nome : (g === domani ? 'Da domani, ' + nome : 'Da ' + nome);
    if (forma === 'fino') return g === oggi ? 'fino a fine giornata' : (g === domani ? 'fino a domani, ' + nome : 'fino a ' + nome);
    return g === oggi ? 'Oggi, ' + nome : (g === domani ? 'Domani, ' + nome : nome.charAt(0).toUpperCase() + nome.slice(1));
  }

  // Oggi verde con un avviso in vigore: «Nessuna allerta» da sola
  // contraddirebbe la striscia dell'avviso, quindi si dice di quale rischio
  // parla. Solo se la striscia di oggi è davvero di oggi (dopo mezzanotte,
  // finché la pagina non si ricostruisce, è quella di ieri e resta com'è).
  // Si torna al testo della build quando l'avviso finisce. Non tocca gli altri
  // stati (livello alzato dal CSV, «da confermare»).
  function precisaOggi(tipo, inVigore, oggi) {
    var oggiBar = document.getElementById('allerta-bar');
    var t = document.getElementById('allerta-titolo');
    var d = document.getElementById('allerta-desc');
    var g = document.getElementById('allerta-giorno');
    if (!oggiBar || !t) return;
    var originale = oggiBar.getAttribute('data-titolo') || 'NESSUNA ALLERTA';
    var diOggi = !g || g.getAttribute('data-giorno') === oggi;
    if (inVigore && diOggi && oggiBar.classList.contains('allerta-bar-verde')) {
      if (t.textContent === originale) {
        t.textContent = TITOLO_PRECISATO;
        if (d) d.textContent = '— È in vigore l\'avviso meteo per ' + tipo + ' qui sotto.';
      }
    } else if ((!inVigore || !diOggi) && t.textContent === TITOLO_PRECISATO) {
      t.textContent = originale;
      if (d) d.textContent = '— ' + (oggiBar.getAttribute('data-desc') || '');
    }
  }

  function aggiornaAvviso(adesso, oggi) {
    var bar = document.getElementById('avviso-meteo-bar');
    if (!bar) return;
    var ini = new Date(bar.getAttribute('data-inizio') || '');
    var fin = new Date(bar.getAttribute('data-fine') || '');
    if (isNaN(ini.getTime()) || isNaN(fin.getTime())) return;
    var tipoEl = document.getElementById('avviso-meteo-tipo');
    var tipo = tipoEl ? tipoEl.textContent : '';
    if (adesso > fin) {
      bar.style.display = 'none';
      precisaOggi(tipo, false, oggi);
      return;
    }
    var inVigore = adesso >= ini;
    var q = document.getElementById('avviso-meteo-quando');
    var st = document.getElementById('avviso-meteo-stato');
    var va = document.getElementById('avviso-meteo-validita');
    if (inVigore) {
      if (q) q.textContent = etichetta(oggi, 'giorno', oggi);
      if (st) st.textContent = ' in vigore';
      if (va) va.textContent = etichetta(giornoRoma(new Date(fin.getTime() - 60000)), 'fino', oggi);
      bar.classList.remove('avviso-meteo-bar-previsto');
      bar.setAttribute('role', 'alert');
      var oggiBar = document.getElementById('allerta-bar');
      if (oggiBar && oggiBar.parentNode && oggiBar.nextElementSibling !== bar) {
        oggiBar.parentNode.insertBefore(bar, oggiBar.nextSibling);
      }
    } else {
      if (q) q.textContent = etichetta(giornoRoma(ini), 'da', oggi);
      if (st) st.textContent = '';
      if (va) {
        var parti = [];
        if (bar.getAttribute('data-dal')) parti.push(bar.getAttribute('data-dal'));
        if (bar.getAttribute('data-durata')) parti.push('per ' + bar.getAttribute('data-durata'));
        va.textContent = parti.join(', ');
      }
      bar.classList.add('avviso-meteo-bar-previsto');
      bar.setAttribute('role', 'status');
    }
    precisaOggi(tipo, inVigore, oggi);
  }

  function aggiornaGiorni() {
    var adesso = new Date();
    var oggi = giornoRoma(adesso);
    var el = document.querySelectorAll('#allerta-bar [data-giorno], #allerta-bar-domani [data-giorno]');
    for (var i = 0; i < el.length; i++) {
      var g = el[i].getAttribute('data-giorno');
      if (!RE_GIORNO.test(g)) continue;
      var testo = etichetta(g, el[i].getAttribute('data-forma') || 'giorno', oggi);
      if (el[i].textContent !== testo) el[i].textContent = testo;
    }
    aggiornaAvviso(adesso, oggi);
  }

  aggiornaGiorni();
  setInterval(aggiornaGiorni, 60 * 1000);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) aggiornaGiorni(); });

  checkAllertaDPC();
  setInterval(checkAllertaDPC, 30 * 60 * 1000);
})();
