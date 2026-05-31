/* Laboratorio meteo — costruttore di grafici client-side.
   Dati live: archivio ERA5 via Open-Meteo (CC BY 4.0). Esempi pre-cotti: /open-data/clima-*.json.
   Niente librerie esterne: rendering SVG vanilla + tabella dati equivalente (WCAG 1.1.1 / 1.4.1). */
(function () {
  'use strict';

  var ARCHIVE = 'https://archive-api.open-meteo.com/v1/archive';
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
  function stato(msg, errore) {
    var el = $('lab-stato');
    el.textContent = msg || '';
    el.className = 'lab-stato' + (errore ? ' lab-stato-errore' : '');
  }

  var ultimoDati = null; // per il download CSV

  // ---- Fetch live ----------------------------------------------------------
  function caricaLive(luogo, varKey, da, a) {
    var v = VARIABILI[varKey];
    var url = ARCHIVE + '?latitude=' + luogo.lat + '&longitude=' + luogo.lon +
      '&start_date=' + da + '&end_date=' + a +
      '&daily=' + v.daily.join(',') + '&timezone=Europe%2FRome';

    $('lab-output').hidden = false;
    stato('Sto scaricando i dati di ' + luogo.nome + '…');
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
    var svg = (dati.tipo === 'bar') ? svgBarre(dati) : svgLinee(dati);
    box.appendChild(svg);
    $('lab-grafico-wrap').hidden = false;
    costruisciTabella(dati);
    $('lab-tabella-blocco').hidden = false;
  }

  // ---- Scale ----------------------------------------------------------------
  var W = 820, H = 420, M = { t: 20, r: 20, b: 70, l: 56 };
  function plotW() { return W - M.l - M.r; }
  function plotH() { return H - M.t - M.b; }

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
      'Grafico dei dati; gli stessi valori sono nella tabella qui sotto.'));
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

  function assiX(svg, x) {
    var n = x.length, passo = Math.max(1, Math.ceil(n / 7));
    for (var i = 0; i < n; i += passo) {
      var px = M.l + (n === 1 ? plotW() / 2 : plotW() * i / (n - 1));
      svg.appendChild(el('text', { x: px, y: H - M.b + 22, 'text-anchor': 'middle', class: 'lab-svg-tick' },
        fmtData(x[i])));
    }
  }

  function svgLinee(dati) {
    var svg = baseSvg(dati.titolo);
    var ex = estremi(dati.serie), n = dati.x.length;
    assiY(svg, ex, dati.unita);
    assiX(svg, dati.x);
    function px(i) { return M.l + (n === 1 ? plotW() / 2 : plotW() * i / (n - 1)); }
    function py(v) { return M.t + plotH() - plotH() * (v - ex.min) / (ex.max - ex.min); }
    dati.serie.forEach(function (s) {
      var d = '', started = false;
      s.valori.forEach(function (v, i) {
        if (v === null || v === undefined || isNaN(v)) { started = false; return; }
        d += (started ? ' L' : ' M') + px(i) + ' ' + py(v); started = true;
      });
      svg.appendChild(el('path', {
        d: d.trim(), fill: 'none', stroke: s.colore, 'stroke-width': 2.5,
        'stroke-dasharray': s.tratto === 'dash' ? '7 4' : '0'
      }));
    });
    legenda(svg, dati.serie);
    return svg;
  }

  function svgBarre(dati) {
    var svg = baseSvg(dati.titolo);
    var s = dati.serie[0], n = dati.x.length;
    var ex = estremi(dati.serie); if (ex.min > 0) ex.min = 0;
    assiY(svg, ex, dati.unita);
    assiX(svg, dati.x);
    var bw = plotW() / n * 0.7;
    function py(v) { return M.t + plotH() - plotH() * (v - ex.min) / (ex.max - ex.min); }
    s.valori.forEach(function (v, i) {
      if (v === null || v === undefined || isNaN(v)) return;
      var cx = M.l + plotW() * (i + 0.5) / n;
      var y = py(v), y0 = py(ex.min < 0 ? 0 : ex.min);
      svg.appendChild(el('rect', { x: cx - bw / 2, y: Math.min(y, y0), width: bw, height: Math.abs(y0 - y), fill: s.colore }));
    });
    legenda(svg, dati.serie);
    return svg;
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
    stato("Apro l'esempio…");
    fetch(path).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (dati) { disegna(dati); stato(''); $('lab-output').scrollIntoView({ behavior: 'smooth', block: 'start' }); })
      .catch(function (e) { stato('Esempio non disponibile (' + e.message + ').', true); });
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
    // periodo default: ultimi 30 giorni con margine di 6 gg (latenza archivio ERA5)
    var fine = ggFa(6), inizio = ggFa(36);
    $('lab-a').value = iso(fine);
    $('lab-da').value = iso(inizio);
    $('lab-a').max = iso(ggFa(5));
    $('lab-da').max = iso(ggFa(5));

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
        var fineD = ggFa(6);
        if (chip.dataset.giorni) {
          $('lab-a').value = iso(fineD);
          $('lab-da').value = iso(ggFa(6 + parseInt(chip.dataset.giorni, 10)));
        } else if (chip.dataset.annoScorso) {
          var f = ggFa(6); f.setFullYear(f.getFullYear() - 1);
          var i = new Date(f); i.setMonth(i.getMonth() - 1);
          $('lab-a').value = iso(f); $('lab-da').value = iso(i);
        }
        $('lab-form').requestSubmit ? $('lab-form').requestSubmit() : $('lab-genera').click();
      });
    });

    $('lab-scarica-csv').addEventListener('click', scaricaCsv);
    caricaEsempi();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
