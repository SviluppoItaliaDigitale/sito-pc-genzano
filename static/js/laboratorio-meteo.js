/* Laboratorio meteo — costruttore di grafici client-side.
   Dati live: archivio ERA5 via Open-Meteo (CC BY 4.0). Esempi pre-cotti: /open-data/clima-*.json.
   Niente librerie esterne: rendering SVG vanilla + tabella dati equivalente (WCAG 1.1.1 / 1.4.1). */
(function () {
  'use strict';

  var ARCHIVE = 'https://archive-api.open-meteo.com/v1/archive';   // ERA5: storico, latenza ~5 gg
  var FORECAST = 'https://api.open-meteo.com/v1/forecast';         // copre il recente passato fino a ieri
  var OPENDATA = (window.LAB_OPENDATA || '/open-data/');

  // Luoghi dei Castelli Romani (coordinate indicative del centro abitato).
  var LUOGHI = [
    { id: 'genzano',         nome: 'Genzano di Roma', lat: 41.7085, lon: 12.6916 },
    { id: 'albano',          nome: 'Albano Laziale',  lat: 41.7286, lon: 12.6607 },
    { id: 'ariccia',         nome: 'Ariccia',         lat: 41.7211, lon: 12.6722 },
    { id: 'castel-gandolfo', nome: 'Castel Gandolfo', lat: 41.7475, lon: 12.6510 },
    { id: 'frascati',        nome: 'Frascati',        lat: 41.8076, lon: 12.6803 },
    { id: 'grottaferrata',   nome: 'Grottaferrata',   lat: 41.7884, lon: 12.6680 },
    { id: 'lanuvio',         nome: 'Lanuvio',         lat: 41.6750, lon: 12.6980 },
    { id: 'marino',          nome: 'Marino',          lat: 41.7686, lon: 12.6580 },
    { id: 'nemi',            nome: 'Nemi',            lat: 41.7197, lon: 12.7156 },
    { id: 'rocca-di-papa',   nome: 'Rocca di Papa',   lat: 41.7600, lon: 12.7080 },
    { id: 'velletri',        nome: 'Velletri',        lat: 41.6870, lon: 12.7780 }
  ];

  // Variabili selezionabili → parametri Open-Meteo + come renderizzarle.
  var VARIABILI = {
    temperatura: {
      etichetta: 'Temperatura', unita: '°C', tipo: 'line',
      daily: ['temperature_2m_max', 'temperature_2m_min'],
      serie: [
        { campo: 'temperature_2m_max', nome: 'Massima', colore: '#c1121f', tratto: 'solid' },
        { campo: 'temperature_2m_min', nome: 'Minima',  colore: '#0369a1', tratto: 'dash' }
      ]
    },
    pioggia: {
      etichetta: 'Pioggia', unita: 'mm', tipo: 'bar',
      daily: ['precipitation_sum'],
      serie: [{ campo: 'precipitation_sum', nome: 'Pioggia', colore: '#003366', tratto: 'solid' }]
    },
    vento: {
      etichetta: 'Vento', unita: 'km/h', tipo: 'line',
      daily: ['wind_speed_10m_max'],
      serie: [{ campo: 'wind_speed_10m_max', nome: 'Velocità max', colore: '#15803d', tratto: 'solid' }]
    }
  };

  var $ = function (id) { return document.getElementById(id); };
  var SVGNS = 'http://www.w3.org/2000/svg';

  // ---- Utilità date --------------------------------------------------------
  function iso(d) { return d.toISOString().slice(0, 10); }
  function oggi() { return new Date(); }
  function ggFa(n) { var d = oggi(); d.setDate(d.getDate() - n); return d; }
  function fmtData(s) {
    var p = s.split('-'); if (p.length !== 3) return s;
    var mesi = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
    return parseInt(p[2], 10) + ' ' + mesi[parseInt(p[1], 10) - 1] + ' ' + p[0];
  }

  // ---- Stato UI ------------------------------------------------------------
  function stato(msg, errore, loading) {
    var el = $('lab-stato');
    if (loading) {
      el.textContent = '';
      el.appendChild(el.ownerDocument.createElement('span')).className = 'pc-spinner';
      el.appendChild(el.ownerDocument.createTextNode(msg || ''));
    } else {
      el.textContent = msg || '';
    }
    el.className = 'lab-stato' + (errore ? ' lab-stato-errore' : '');
  }

  var ultimoDati = null; // per il download CSV

  // ---- Fetch live ----------------------------------------------------------
  function caricaLive(luogo, varKey, da, a) {
    var v = VARIABILI[varKey];
    // Per periodi recenti (inizio entro ~90 gg) uso l'endpoint forecast, che ha i dati
    // fino a ieri; per le serie storiche lunghe uso l'archivio ERA5 (latenza ~5 gg).
    var limite = ggFa(90);
    var endpoint = (new Date(da) >= limite) ? FORECAST : ARCHIVE;
    var url = endpoint + '?latitude=' + luogo.lat + '&longitude=' + luogo.lon +
      '&start_date=' + da + '&end_date=' + a +
      '&daily=' + v.daily.join(',') + '&timezone=Europe%2FRome';

    $('lab-output').hidden = false;
    stato('Sto scaricando i dati di ' + luogo.nome + '…', false, true);
    $('lab-grafico-wrap').hidden = true;
    $('lab-tabella-blocco').hidden = true;

    fetch(url).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (j) {
      if (!j.daily || !j.daily.time || !j.daily.time.length) {
        throw new Error('Nessun dato per questo periodo.');
      }
      var d = j.daily;
      var dati = {
        titolo: v.etichetta + ' a ' + luogo.nome,
        sottotitolo: 'Dal ' + fmtData(da) + ' al ' + fmtData(a),
        tipo: v.tipo, unita: v.unita,
        x: d.time,
        serie: v.serie.map(function (s) {
          return { nome: s.nome, colore: s.colore, tratto: s.tratto, valori: d[s.campo] || [] };
        })
      };
      disegna(dati);
      stato('');
      aggiornaUrl({ l: luogo.id, v: varKey, da: da, a: a });
    }).catch(function (e) {
      stato('Non sono riuscito a caricare i dati (' + e.message + '). Riprova tra qualche istante o cambia periodo.', true);
      $('lab-grafico-wrap').hidden = true;
      $('lab-tabella-blocco').hidden = true;
    });
  }

  // ---- Render: dispatch ----------------------------------------------------
  function disegna(dati) {
    ultimoDati = dati;
    $('lab-output').hidden = false;
    $('lab-grafico-titolo').textContent = dati.titolo + (dati.sottotitolo ? ' — ' + dati.sottotitolo : '');
    var box = $('lab-grafico');
    box.textContent = '';
    var r = (dati.tipo === 'bar') ? svgBarre(dati) : svgLinee(dati);
    box.appendChild(r.svg);
    montaInterazione(box, r, dati);
    $('lab-grafico-wrap').hidden = false;
    costruisciTabella(dati);
    $('lab-tabella-blocco').hidden = false;
  }

  // ---- Scale ----------------------------------------------------------------
  var W = 860, H = 440, M = { t: 30, r: 26, b: 76, l: 60 };
  function plotW() { return W - M.l - M.r; }
  function plotH() { return H - M.t - M.b; }
  function valido(v) { return !(v === null || v === undefined || isNaN(v)); }
  function fmtVal(v) { return String(Math.round(v * 10) / 10).replace('.', ','); }

  function estremi(serie) {
    var min = Infinity, max = -Infinity;
    serie.forEach(function (s) {
      s.valori.forEach(function (v) {
        if (v === null || v === undefined || isNaN(v)) return;
        if (v < min) min = v; if (v > max) max = v;
      });
    });
    if (min === Infinity) { min = 0; max = 1; }
    if (min === max) { min -= 1; max += 1; }
    return { min: min, max: max };
  }

  function el(name, attrs, text) {
    var n = document.createElementNS(SVGNS, name);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]);
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function baseSvg(titoloAcc) {
    var svg = el('svg', {
      viewBox: '0 0 ' + W + ' ' + H, role: 'img', class: 'lab-svg',
      'aria-labelledby': 'lab-svg-title lab-svg-desc', preserveAspectRatio: 'xMidYMid meet'
    });
    svg.appendChild(el('title', { id: 'lab-svg-title' }, titoloAcc));
    svg.appendChild(el('desc', { id: 'lab-svg-desc' },
      'Grafico dei dati; passa il puntatore o usa le frecce per leggere i valori. Gli stessi dati sono nella tabella qui sotto.'));
    // rettangolo trasparente che cattura i movimenti del puntatore su tutta l'area
    svg.appendChild(el('rect', { x: 0, y: 0, width: W, height: H, fill: '#fff', 'fill-opacity': '0', 'pointer-events': 'all' }));
    return svg;
  }

  function assiY(svg, ex, unita) {
    var n = 5;
    for (var i = 0; i <= n; i++) {
      var val = ex.min + (ex.max - ex.min) * i / n;
      var y = M.t + plotH() - plotH() * i / n;
      svg.appendChild(el('line', { x1: M.l, y1: y, x2: M.l + plotW(), y2: y, stroke: '#e0e6ee', 'stroke-width': 1 }));
      svg.appendChild(el('text', { x: M.l - 8, y: y + 4, 'text-anchor': 'end', class: 'lab-svg-tick' },
        (Math.round(val * 10) / 10) + ''));
    }
    svg.appendChild(el('text', {
      x: 14, y: M.t + plotH() / 2, 'text-anchor': 'middle', class: 'lab-svg-axis',
      transform: 'rotate(-90 14 ' + (M.t + plotH() / 2) + ')'
    }, unita));
  }

  // pxFn = stessa funzione di posizione X del grafico (allinea le etichette ai dati).
  // ogni = true → un'etichetta per ogni valore (es. ogni anno sotto la sua barra).
  function assiX(svg, x, pxFn, ogni) {
    var n = x.length, idxs = [];
    if (ogni) {
      for (var k = 0; k < n; k++) idxs.push(k);
    } else {
      var passo = Math.max(1, Math.ceil((n - 1) / 7));
      for (var i = 0; i < n; i += passo) idxs.push(i);
      if (idxs[idxs.length - 1] !== n - 1) idxs.push(n - 1);
    }
    var ruota = ogni && n > 12;  // diagonale per non sovrapporre quando sono molte
    idxs.forEach(function (i) {
      var px = pxFn(i), y = H - M.b + (ruota ? 16 : 22);
      var attrs = { x: px, y: y, class: 'lab-svg-tick' };
      if (ruota) {
        attrs['text-anchor'] = 'end';
        attrs.transform = 'rotate(-45 ' + px + ' ' + y + ')';
      } else {
        attrs['text-anchor'] = i === 0 ? 'start' : (i === n - 1 ? 'end' : 'middle');
      }
      svg.appendChild(el('text', attrs, fmtData(x[i])));
    });
  }

  function svgLinee(dati) {
    var svg = baseSvg(dati.titolo);
    var ex = estremi(dati.serie), n = dati.x.length;
    assiY(svg, ex, dati.unita);
    assiX(svg, dati.x, px, false);
    function px(i) { return M.l + (n === 1 ? plotW() / 2 : plotW() * i / (n - 1)); }
    function py(v) { return M.t + plotH() - plotH() * (v - ex.min) / (ex.max - ex.min); }
    dati.serie.forEach(function (s) {
      var d = '', started = false;
      s.valori.forEach(function (v, i) {
        if (!valido(v)) { started = false; return; }
        d += (started ? ' L' : ' M') + px(i) + ' ' + py(v); started = true;
      });
      svg.appendChild(el('path', {
        d: d.trim(), fill: 'none', stroke: s.colore, 'stroke-width': 2.5,
        'stroke-dasharray': s.tratto === 'dash' ? '7 4' : '0', 'pointer-events': 'none'
      }));
      // punti marcati su ogni valore
      s.valori.forEach(function (v, i) {
        if (valido(v)) svg.appendChild(el('circle', { cx: px(i), cy: py(v), r: 2.8, fill: s.colore, 'pointer-events': 'none' }));
      });
    });
    // etichette di valore quando i punti sono pochi (niente sovrapposizioni)
    if (dati.serie.length * n <= 28) {
      dati.serie.forEach(function (s) {
        s.valori.forEach(function (v, i) {
          if (valido(v)) svg.appendChild(el('text', { x: px(i), y: py(v) - 9, 'text-anchor': 'middle', class: 'lab-svg-val', 'pointer-events': 'none' }, fmtVal(v)));
        });
      });
    }
    legenda(svg, dati.serie);
    var hover = el('g', { 'pointer-events': 'none' }); svg.appendChild(hover);
    return { svg: svg, kind: 'line', n: n, px: px, py: py, ex: ex, hover: hover };
  }

  function svgBarre(dati) {
    var svg = baseSvg(dati.titolo);
    var s = dati.serie[0], n = dati.x.length;
    var ex = estremi(dati.serie); if (ex.min > 0) ex.min = 0;
    assiY(svg, ex, dati.unita);
    assiX(svg, dati.x, px, n <= 24);
    var bw = plotW() / n * 0.7;
    function px(i) { return M.l + plotW() * (i + 0.5) / n; }
    function py(v) { return M.t + plotH() - plotH() * (v - ex.min) / (ex.max - ex.min); }
    var y0 = py(ex.min < 0 ? 0 : ex.min);
    s.valori.forEach(function (v, i) {
      if (!valido(v)) return;
      var cx = px(i), y = py(v);
      svg.appendChild(el('rect', { x: cx - bw / 2, y: Math.min(y, y0), width: bw, height: Math.abs(y0 - y), fill: s.colore, 'pointer-events': 'none' }));
      // etichetta di valore sopra la barra quando le barre sono poche
      if (n <= 24) svg.appendChild(el('text', { x: cx, y: Math.min(y, y0) - 5, 'text-anchor': 'middle', class: 'lab-svg-val', 'pointer-events': 'none' }, fmtVal(v)));
    });
    legenda(svg, dati.serie);
    var hover = el('g', { 'pointer-events': 'none' }); svg.appendChild(hover);
    return { svg: svg, kind: 'bar', n: n, px: px, py: py, ex: ex, bw: bw, y0: y0, hover: hover };
  }

  // ---- Interazione: tooltip (puntatore/tocco) + tastiera ------------------
  function montaInterazione(box, r, dati) {
    box.style.position = 'relative';
    var tip = document.createElement('div');
    tip.className = 'lab-tip'; tip.hidden = true;
    tip.setAttribute('role', 'status'); tip.setAttribute('aria-live', 'polite');
    box.appendChild(tip);
    var svg = r.svg, n = r.n;

    function idxDaX(clientX) {
      var rect = svg.getBoundingClientRect();
      var vx = ((clientX - rect.left) / rect.width) * W;
      var i = (r.kind === 'bar')
        ? Math.floor((vx - M.l) / (plotW() / n))
        : Math.round((vx - M.l) / (n > 1 ? plotW() / (n - 1) : 1));
      return Math.max(0, Math.min(n - 1, i));
    }

    function mostra(i, clientX, clientY) {
      r.hover.textContent = '';
      var gx = r.px(i);
      r.hover.appendChild(el('line', { x1: gx, y1: M.t, x2: gx, y2: M.t + plotH(), stroke: '#003366', 'stroke-width': 1, 'stroke-dasharray': '3 3', opacity: '0.55' }));
      var html = '<strong>' + escapeHtml(fmtData(dati.x[i])) + '</strong>';
      dati.serie.forEach(function (s) {
        var v = s.valori[i];
        var testo = valido(v) ? (fmtVal(v) + ' ' + dati.unita) : 'dato non disponibile';
        if (valido(v)) {
          if (r.kind === 'bar') {
            r.hover.appendChild(el('rect', { x: gx - r.bw / 2, y: Math.min(r.py(v), r.y0), width: r.bw, height: Math.abs(r.y0 - r.py(v)), fill: 'none', stroke: '#ffbe2e', 'stroke-width': 2.5 }));
          } else {
            r.hover.appendChild(el('circle', { cx: gx, cy: r.py(v), r: 5, fill: s.colore, stroke: '#fff', 'stroke-width': 2 }));
          }
        }
        html += '<br><span class="lab-tip-pall" style="background:' + s.colore + '"></span>' + escapeHtml(s.nome) + ': <strong>' + escapeHtml(testo) + '</strong>';
      });
      tip.innerHTML = html;
      tip.hidden = false;
      var brect = box.getBoundingClientRect();
      var left, top;
      if (clientX != null) { left = clientX - brect.left + 14; top = clientY - brect.top + 14; }
      else { var sr = svg.getBoundingClientRect(); left = (gx / W) * sr.width + (sr.left - brect.left) + 14; top = 14; }
      if (left + tip.offsetWidth > box.clientWidth) left = box.clientWidth - tip.offsetWidth - 6;
      if (left < 0) left = 6;
      if (top + tip.offsetHeight > box.clientHeight) top = box.clientHeight - tip.offsetHeight - 6;
      tip.style.left = left + 'px'; tip.style.top = top + 'px';
    }
    function nascondi() { tip.hidden = true; r.hover.textContent = ''; }

    svg.addEventListener('pointermove', function (e) { mostra(idxDaX(e.clientX), e.clientX, e.clientY); });
    svg.addEventListener('pointerdown', function (e) { mostra(idxDaX(e.clientX), e.clientX, e.clientY); });
    svg.addEventListener('pointerleave', nascondi);

    // tastiera: frecce per scorrere giorno per giorno
    var cur = 0;
    box.tabIndex = 0;
    box.setAttribute('aria-label', 'Grafico interattivo: usa le frecce sinistra e destra per leggere i valori uno per uno. La tabella sotto contiene tutti i dati.');
    box.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { cur = Math.min(n - 1, cur + 1); }
      else if (e.key === 'ArrowLeft') { cur = Math.max(0, cur - 1); }
      else if (e.key === 'Home') { cur = 0; }
      else if (e.key === 'End') { cur = n - 1; }
      else if (e.key === 'Escape') { nascondi(); return; }
      else { return; }
      e.preventDefault(); mostra(cur, null, null);
    });
    box.addEventListener('blur', nascondi);
  }

  function legenda(svg, serie) {
    var x = M.l, y = H - 14;
    serie.forEach(function (s) {
      svg.appendChild(el('line', { x1: x, y1: y, x2: x + 24, y2: y, stroke: s.colore, 'stroke-width': 3, 'stroke-dasharray': s.tratto === 'dash' ? '7 4' : '0' }));
      var t = el('text', { x: x + 30, y: y + 4, class: 'lab-svg-legend' }, s.nome);
      svg.appendChild(t);
      x += 30 + s.nome.length * 8 + 24;
    });
  }

  // ---- Tabella dati equivalente -------------------------------------------
  function costruisciTabella(dati) {
    var t = $('lab-tabella');
    t.textContent = '';
    var thead = document.createElement('thead'), trh = document.createElement('tr');
    trh.appendChild(creaTh('Data'));
    dati.serie.forEach(function (s) { trh.appendChild(creaTh(s.nome + ' (' + dati.unita + ')')); });
    thead.appendChild(trh); t.appendChild(thead);
    var tb = document.createElement('tbody');
    dati.x.forEach(function (d, i) {
      var tr = document.createElement('tr');
      var tdd = document.createElement('td'); tdd.textContent = fmtData(d); tr.appendChild(tdd);
      dati.serie.forEach(function (s) {
        var td = document.createElement('td');
        var v = s.valori[i];
        td.textContent = (v === null || v === undefined || isNaN(v)) ? '—' : (Math.round(v * 10) / 10) + '';
        tr.appendChild(td);
      });
      tb.appendChild(tr);
    });
    t.appendChild(tb);
  }
  function creaTh(txt) {
    var th = document.createElement('th'); th.setAttribute('scope', 'col'); th.textContent = txt; return th;
  }

  // ---- CSV -----------------------------------------------------------------
  function scaricaCsv() {
    if (!ultimoDati) return;
    var d = ultimoDati, righe = [];
    righe.push(['Data'].concat(d.serie.map(function (s) { return s.nome + ' (' + d.unita + ')'; })).join(','));
    d.x.forEach(function (x, i) {
      var r = [x];
      d.serie.forEach(function (s) { var v = s.valori[i]; r.push((v === null || v === undefined || isNaN(v)) ? '' : v); });
      righe.push(r.join(','));
    });
    var blob = new Blob(['﻿' + righe.join('\n')], { type: 'text/csv;charset=utf-8;' });
    var url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = 'laboratorio-meteo-' + (d.x[0] || 'dati') + '.csv';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // ---- Esempi pre-cotti ----------------------------------------------------
  function caricaEsempi() {
    fetch(OPENDATA + 'clima-manifest.json').then(function (r) {
      if (!r.ok) throw new Error('no manifest');
      return r.json();
    }).then(function (lista) {
      var grid = $('lab-esempi-grid');
      grid.textContent = '';
      if (!lista || !lista.length) { grid.innerHTML = '<p class="text-muted">Nessun esempio disponibile al momento.</p>'; return; }
      lista.forEach(function (item) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'lab-esempio-card';
        b.innerHTML = '<span class="lab-esempio-titolo"><i class="bi bi-graph-up" aria-hidden="true"></i> ' +
          escapeHtml(item.titolo) + '</span><span class="lab-esempio-descr">' + escapeHtml(item.descr || '') + '</span>';
        b.addEventListener('click', function () { apriEsempio(item.file); });
        grid.appendChild(b);
      });
    }).catch(function () {
      $('lab-esempi').hidden = true; // niente esempi: nascondi la sezione, resta il builder live
    });
  }

  function apriEsempio(file) {
    var path = file.charAt(0) === '/' ? file : (OPENDATA + file);
    $('lab-output').hidden = false;
    stato("Apro l'esempio…", false, true);
    fetch(path).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (dati) { disegna(dati); stato(''); aggiornaUrl({ ex: file }); $('lab-output').scrollIntoView({ behavior: 'smooth', block: 'start' }); })
      .catch(function (e) { stato('Esempio non disponibile (' + e.message + ').', true); });
  }

  // ---- URL condivisibile + scarica PNG + stampa + condividi ----------------
  function aggiornaUrl(cfg) {
    try {
      var qs = Object.keys(cfg).map(function (k) { return k + '=' + encodeURIComponent(cfg[k]); }).join('&');
      history.replaceState(null, '', location.pathname + '?' + qs);
    } catch (e) { /* no-op */ }
  }

  function scaricaPng() {
    var svg = document.querySelector('#lab-grafico svg');
    if (!svg) return;
    var clone = svg.cloneNode(true);
    var style = document.createElementNS(SVGNS, 'style');
    style.textContent = 'text{font-family:Trebuchet MS,Verdana,Arial,sans-serif}' +
      '.lab-svg-tick{font-size:11px;fill:#5a6678}.lab-svg-axis{font-size:12px;fill:#003366;font-weight:600}' +
      '.lab-svg-legend{font-size:13px;fill:#1a1a1a}' +
      '.lab-svg-val{font-size:10.5px;fill:#1a2a3a;font-weight:600;stroke:#fff;stroke-width:3px;paint-order:stroke fill}';
    clone.insertBefore(style, clone.firstChild);
    clone.setAttribute('width', W); clone.setAttribute('height', H);
    var xml = new XMLSerializer().serializeToString(clone);
    var src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(xml);
    var titolo = ($('lab-grafico-titolo').textContent || 'Laboratorio meteo');
    var img = new Image();
    img.onload = function () {
      var scale = 2, th = 30;
      var canvas = document.createElement('canvas');
      canvas.width = W * scale; canvas.height = (H + th) * scale;
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#003366'; ctx.font = 'bold ' + (13 * scale) + 'px Trebuchet MS,Verdana,Arial,sans-serif';
      ctx.fillText(titolo, 8 * scale, 19 * scale, canvas.width - 16 * scale);
      ctx.drawImage(img, 0, th * scale, W * scale, H * scale);
      canvas.toBlob(function (blob) {
        var url = URL.createObjectURL(blob), a = document.createElement('a');
        a.href = url; a.download = 'laboratorio-meteo-' + (ultimoDati && ultimoDati.x[0] ? ultimoDati.x[0] : 'grafico') + '.png';
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 'image/png');
    };
    img.onerror = function () { stato('Non riesco a generare il PNG su questo browser. Usa Stampa → Salva come PDF.', true); };
    img.src = src;
  }

  function copiaLink() {
    var url = location.href;
    var done = function () {
      var b = $('lab-copia-link'); if (!b) return;
      var t = b.innerHTML; b.innerHTML = '<i class="bi bi-check2 me-1" aria-hidden="true"></i>Link copiato';
      setTimeout(function () { b.innerHTML = t; }, 2000);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(done, function () { window.prompt('Copia il link:', url); });
    } else { window.prompt('Copia il link:', url); }
  }

  function condividi() {
    if (navigator.share) {
      navigator.share({ title: $('lab-grafico-titolo').textContent || 'Laboratorio meteo', url: location.href }).catch(function () {});
    }
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ---- Init ----------------------------------------------------------------
  function init() {
    var sel = $('lab-luogo');
    if (!sel) return;
    LUOGHI.forEach(function (l) {
      var o = document.createElement('option'); o.value = l.id; o.textContent = l.nome; sel.appendChild(o);
    });
    // periodo default: ultimi 30 giorni fino a ieri (l'endpoint forecast copre fino a ieri)
    var fine = ggFa(1), inizio = ggFa(31);
    $('lab-a').value = iso(fine);
    $('lab-da').value = iso(inizio);
    $('lab-a').max = iso(ggFa(1));
    $('lab-da').max = iso(ggFa(1));

    $('lab-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var luogo = LUOGHI.filter(function (l) { return l.id === sel.value; })[0] || LUOGHI[0];
      var da = $('lab-da').value, a = $('lab-a').value;
      if (!da || !a) { stato('Scegli un giorno di inizio e uno di fine.', true); return; }
      if (da > a) { stato('Il giorno di inizio deve venire prima di quello di fine.', true); return; }
      caricaLive(luogo, $('lab-variabile').value, da, a);
    });

    Array.prototype.forEach.call(document.querySelectorAll('.lab-chip'), function (chip) {
      chip.addEventListener('click', function () {
        var fineD = ggFa(1);
        if (chip.dataset.giorni) {
          $('lab-a').value = iso(fineD);
          $('lab-da').value = iso(ggFa(1 + parseInt(chip.dataset.giorni, 10)));
        } else if (chip.dataset.annoScorso) {
          var f = ggFa(1); f.setFullYear(f.getFullYear() - 1);
          var i = new Date(f); i.setMonth(i.getMonth() - 1);
          $('lab-a').value = iso(f); $('lab-da').value = iso(i);
        }
        $('lab-form').requestSubmit ? $('lab-form').requestSubmit() : $('lab-genera').click();
      });
    });

    $('lab-scarica-csv').addEventListener('click', scaricaCsv);
    $('lab-scarica-png').addEventListener('click', scaricaPng);
    $('lab-stampa').addEventListener('click', function () { window.print(); });
    $('lab-copia-link').addEventListener('click', copiaLink);
    if (navigator.share) { var cd = $('lab-condividi'); cd.hidden = false; cd.addEventListener('click', condividi); }

    caricaEsempi();

    // grafico condivisibile: ricostruisci dallo stato nell'URL
    var p = new URLSearchParams(location.search);
    if (p.get('ex')) {
      apriEsempio(p.get('ex'));
    } else if (p.get('l') && p.get('v') && p.get('da') && p.get('a')) {
      var luogo = LUOGHI.filter(function (l) { return l.id === p.get('l'); })[0];
      if (luogo) {
        sel.value = luogo.id;
        if (VARIABILI[p.get('v')]) $('lab-variabile').value = p.get('v');
        $('lab-da').value = p.get('da'); $('lab-a').value = p.get('a');
        caricaLive(luogo, $('lab-variabile').value, p.get('da'), p.get('a'));
      }
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
