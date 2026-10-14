/* ============================================================
   PC-WMS v1.0 — istanti e legende dei livelli WMS del cruscotto.
   ItaliaMeteo (maps.mistralportal.it) e Copernicus CAMS
   (eccharts.ecmwf.int) pubblicano le previsioni a istanti precisi:
   chiedere un'ora che non esiste dà un'immagine vuota senza nessun
   errore visibile. Fino al 14/10/2026 «Adesso» mandava time=null
   (livello vuoto dopo il primo clic) e «+72h» cadeva oltre la fine
   della corsa. Qui si leggono gli istanti disponibili dalle
   capabilities, una volta per pagina, e per ItaliaMeteo la scala
   dei colori dallo stile del livello (GetStyles), per disegnare una
   legenda con i valori: quelle della fonte sono solo colori.
   Usato da dashboard-italiameteo, dashboard-italiameteo-mare,
   dashboard-italiameteo-radar e dashboard-cams. Vanilla JS.

   API (Promise: se la fonte non risponde la Promise fallisce e la
   scheda usa il proprio ripiego, dichiarato nella riga di stato):
     pcWms.tempi(urlCapabilities, livello, fresco)
         → {lista: [ms…] in ordine, predefinito: ms|null}
     pcWms.istante(lista, ms)      → {ms, limite: ''|'prima'|'ultima'}
     pcWms.vicino(lista, ms)       → istante disponibile più vicino (ms)
     pcWms.iso(ms, senzaMillesimi) → «2026-10-14T05:00:00.000Z»
     pcWms.stile(urlWms, livello)  → [{q, c, o}] (ColorMap «intervals»)
     pcWms.legenda(el, voci, opz)  → disegna barra dei colori e valori
     pcWms.quando(ms)              → «martedì 14 ottobre, ore 07:00»
     pcWms.aperta(el, evento, fn)  → fn subito se el è visibile, se no
                                      alla prima apertura della scheda
     pcWms.tessere(livello, fn)    → fn(arrivate, mancate) a ogni carico
   ============================================================ */
(function () {
  'use strict';
  if (window.pcWms) return;

  var documenti = {}, stili = {}, formato = null;
  var MEZZORA = 30 * 60000;

  function durataMs(p) {
    var m = /^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$/.exec(p || '');
    if (!m) return 0;
    return ((+(m[1] || 0) * 24 + +(m[2] || 0)) * 60 + +(m[3] || 0)) * 60000 + +(m[4] || 0) * 1000;
  }

  // «a,b,c» oppure «inizio/fine/PT1H», anche mescolati (eccharts).
  function istanti(testo) {
    var out = [];
    String(testo || '').split(',').forEach(function (pezzo) {
      pezzo = pezzo.trim();
      if (!pezzo) return;
      var p = pezzo.split('/');
      if (p.length === 3) {
        var a = Date.parse(p[0]), b = Date.parse(p[1]), passo = durataMs(p[2]);
        if (isNaN(a) || isNaN(b) || !passo) return;
        for (var t = a; t <= b && out.length < 20000; t += passo) out.push(t);
      } else {
        var t1 = Date.parse(pezzo);
        if (!isNaN(t1)) out.push(t1);
      }
    });
    out.sort(function (x, y) { return x - y; });
    return out;
  }

  function documento(url, fresco) {
    if (fresco || !documenti[url]) {
      var pr = fetch(url, { mode: 'cors' }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.text();
      }).then(function (t) {
        var d = new DOMParser().parseFromString(t, 'application/xml');
        if (d.getElementsByTagName('parsererror').length) throw new Error('XML non valido');
        return d;
      });
      documenti[url] = pr;
      pr.catch(function () { if (documenti[url] === pr) delete documenti[url]; });
    }
    return documenti[url];
  }

  // Nelle capabilities globali di GeoServer il nome può comparire senza
  // lo spazio di lavoro («t2m-t2m» invece di «meteohub:t2m-t2m»). In WMS
  // 1.3.0 gli istanti stanno in <Dimension>, in 1.1.1 in <Extent>.
  function tempi(url, livello, fresco) {
    var corto = String(livello).split(':').pop();
    return documento(url, fresco).then(function (doc) {
      var nomi = doc.getElementsByTagName('Name');
      for (var i = 0; i < nomi.length; i++) {
        var n = nomi[i].textContent.trim();
        if (n !== livello && n !== corto) continue;
        var lay = nomi[i].parentNode;
        if (!lay || lay.localName !== 'Layer') continue;
        for (var c = lay.firstElementChild; c; c = c.nextElementSibling) {
          if ((c.localName !== 'Dimension' && c.localName !== 'Extent') ||
              (c.getAttribute('name') || '').toLowerCase() !== 'time') continue;
          var lista = istanti(c.textContent);
          if (!lista.length) continue;
          var def = Date.parse(c.getAttribute('default') || '');
          return { lista: lista, predefinito: isNaN(def) ? null : def };
        }
      }
      throw new Error('istanti non trovati per ' + livello);
    });
  }

  function vicino(lista, ms) {
    var meglio = null, distanza = Infinity;
    for (var i = 0; i < lista.length; i++) {
      var d = Math.abs(lista[i] - ms);
      if (d < distanza) { distanza = d; meglio = lista[i]; }
    }
    return meglio;
  }

  // Oltre la fine della corsa (o prima dell'inizio) si mostra l'estremo
  // e la scheda lo dice: non si chiede mai un'ora che non esiste.
  function istante(lista, ms) {
    if (!lista || !lista.length) return null;
    var primo = lista[0], ultimo = lista[lista.length - 1];
    if (ms > ultimo + MEZZORA) return { ms: ultimo, limite: 'ultima' };
    if (ms < primo - MEZZORA) return { ms: primo, limite: 'prima' };
    return { ms: vicino(lista, ms), limite: '' };
  }

  function iso(ms, senzaMillesimi) {
    var s = new Date(ms).toISOString();
    return senzaMillesimi ? s.slice(0, 19) + 'Z' : s;
  }

  // Scala dei colori dallo stile GeoServer: in una ColorMap «intervals»
  // ogni colore vale fino al proprio valore. Si accettano solo colori
  // esadecimali: il testo arriva da un server esterno.
  function stile(url, livello) {
    var k = url + '|' + livello;
    if (!stili[k]) {
      var pr = fetch(url + '?service=WMS&request=GetStyles&version=1.1.1&layers=' + encodeURIComponent(livello), { mode: 'cors' })
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.text();
        }).then(function (t) {
          var d = new DOMParser().parseFromString(t, 'application/xml');
          var cm = d.getElementsByTagNameNS('*', 'ColorMap')[0];
          if (!cm || (cm.getAttribute('type') || 'ramp') !== 'intervals') throw new Error('scala non leggibile');
          var e = cm.getElementsByTagNameNS('*', 'ColorMapEntry'), voci = [];
          for (var i = 0; i < e.length; i++) {
            var q = parseFloat(e[i].getAttribute('quantity')), c = e[i].getAttribute('color') || '';
            var o = e[i].getAttribute('opacity');
            if (isNaN(q) || !/^#[0-9a-f]{6}$/i.test(c)) continue;
            voci.push({ q: q, c: c.toLowerCase(), o: o === null ? 1 : Math.max(0, Math.min(1, parseFloat(o) || 0)) });
          }
          voci.sort(function (a, b) { return a.q - b.q; });
          if (voci.length < 2) throw new Error('scala vuota');
          return voci;
        });
      stili[k] = pr;
      pr.catch(function () { if (stili[k] === pr) delete stili[k]; });
    }
    return stili[k];
  }

  function numero(v, dec) {
    return Number(v).toLocaleString('it-IT', { maximumFractionDigits: dec == null ? 2 : dec });
  }

  function testo(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // opz: titolo, unita, conv(q)→valore mostrato, dec, etichette (quante al
  // massimo), inizio (indice del primo confine da scrivere), nota (testo).
  function legenda(el, voci, opz) {
    opz = opz || {};
    var conv = opz.conv || function (q) { return q; };
    var vis = [], soglia = null;
    for (var i = 0; i < voci.length; i++) {
      if (voci[i].o === 0) { soglia = voci[i].q; continue; }
      // due intervalli consecutivi dello stesso colore sono uno solo
      var u = vis[vis.length - 1];
      if (u && u.c === voci[i].c && u.o === voci[i].o) vis[vis.length - 1] = voci[i];
      else vis.push(voci[i]);
    }
    if (!vis.length) { el.innerHTML = ''; return; }
    var n = vis.length, passo = Math.max(1, Math.ceil((n - 1) / (opz.etichette || 8)));
    var unita = opz.unita ? (opz.unita === '%' ? '%' : ' ' + testo(opz.unita)) : '';
    var barra = '', num = '';
    for (var j = 0; j < n; j++) {
      barra += '<span style="background:' + vis[j].c + (vis[j].o < 1 ? ';opacity:' + vis[j].o : '') + '"></span>';
    }
    // sotto la soglia trasparente la scala comincia da quel valore
    if (soglia !== null) num += '<span class="inizio" style="left:0">' + numero(conv(soglia), opz.dec) + '</span>';
    // il confine fra il colore k e il k+1 è il valore massimo del colore k
    for (var k = (opz.inizio == null ? passo - 1 : opz.inizio); k < n - 1; k += passo) {
      num += '<span style="left:' + ((k + 1) / n * 100).toFixed(2) + '%">' + numero(conv(vis[k].q), opz.dec) + '</span>';
    }
    el.innerHTML = '<p class="wms-legenda-tit">' + testo(opz.titolo) +
      '<span class="visually-hidden">. Scala dei colori: valori bassi a sinistra, alti a destra; i numeri sotto la barra sono i confini fra un colore e l\'altro.</span></p>' +
      '<div class="wms-legenda-barra" aria-hidden="true">' + barra + '</div>' +
      '<div class="wms-legenda-num">' + num + '</div>' +
      (soglia !== null ? '<p class="wms-legenda-nota">Sotto ' + numero(conv(soglia), opz.dec) + unita + ' la mappa resta trasparente.</p>' : '') +
      (opz.nota ? '<p class="wms-legenda-nota">' + testo(opz.nota) + '</p>' : '');
  }

  function quando(ms) {
    try {
      if (!formato) {
        formato = new Intl.DateTimeFormat('it-IT', { timeZone: 'Europe/Rome', weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
      }
      var p = {};
      formato.formatToParts(new Date(ms)).forEach(function (x) { p[x.type] = x.value; });
      return p.weekday + ' ' + p.day + ' ' + p.month + ', ore ' + p.hour + ':' + p.minute;
    } catch (e) {
      return new Date(ms).toLocaleString('it-IT');
    }
  }

  // Le schede del cruscotto sono nascoste finché non si aprono: la
  // richiesta alla fonte parte solo quando servono.
  function aperta(el, evento, fn) {
    if (el && el.offsetParent !== null) { fn(); return; }
    window.addEventListener(evento, fn, { once: true });
  }

  // Leaflet segnala «load» anche quando tutte le tessere sono in errore:
  // un'ora rifiutata dalla fonte risponde con un XML al posto del PNG.
  function tessere(livello, fn) {
    var ok = 0, ko = 0;
    livello.on('loading', function () { ok = 0; ko = 0; });
    livello.on('tileload', function () { ok++; });
    livello.on('tileerror', function () { ko++; });
    livello.on('load', function () { fn(ok, ko); });
  }

  window.pcWms = {
    tempi: tempi, istante: istante, vicino: vicino, iso: iso, stile: stile,
    legenda: legenda, quando: quando, aperta: aperta, tessere: tessere
  };
})();
