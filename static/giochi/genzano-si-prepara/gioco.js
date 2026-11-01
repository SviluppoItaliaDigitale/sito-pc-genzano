/* Genzano si prepara — motore del gioco.
 * Simulazione a scenari sulla mappa vera di Genzano di Roma (dati OpenStreetMap,
 * luoghi.json generato da scripts/genera-mappa-gioco-genzano.py): prima si
 * sceglie la preparazione, poi si affrontano gli eventi, infine il resoconto
 * mostra che cosa la preparazione ha evitato. Nessun dato lascia il browser.
 */
(function () {
  'use strict';

  var ID_GIOCO = 'genzano-si-prepara';
  var root = document.getElementById('gsp');
  if (!root || !window.GenzanoScenari) return;

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var pannello = $('#gsp-pannello');
  var camera = $('#gsp-camera');
  var mappa = $('#gsp-mappa');
  var segni = $('#gsp-segni');
  var pioggiaTela = $('#gsp-pioggia');
  var cielo = $('#gsp-cielo');
  var dove = $('#gsp-dove');
  var barraAllerta = $('#gsp-allerta');
  var interruttoreAree = $('#gsp-mostra-aree');
  var LUOGHI = null;
  var VISTA = [1000, 1116];

  var stato = null;

  /* ------------------------------------------------------------ utilità */
  function esc(t) {
    return String(t).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function movimentoRidotto() {
    var h = document.documentElement.classList;
    return h.contains('a11y-pause-anim') || h.contains('a11y-pause-animations') ||
      (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  function valore(v, p) { return typeof v === 'function' ? v(p) : v; }
  function ls(k, v) {
    try {
      if (v === undefined) return localStorage.getItem(k);
      localStorage.setItem(k, v);
    } catch (e) { return null; }
  }
  function link(url, testo) {
    return '<a href="' + esc(url) + '" target="_blank" rel="noopener">' + esc(testo) +
      '<span class="visually-hidden"> (si apre in una nuova scheda)</span></a>';
  }

  /* ------------------------------------------------------------- mappa */
  function caricaLuoghi() {
    return fetch('luoghi.json').then(function (r) { return r.json(); }).then(function (d) {
      LUOGHI = d;
      VISTA = d.vista;
      disegnaSegni();
    }).catch(function () { LUOGHI = { luoghi: {}, aree: [] }; });
  }

  function svgEl(tag, attr, testo) {
    var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.keys(attr || {}).forEach(function (k) { e.setAttribute(k, attr[k]); });
    if (testo) e.textContent = testo;
    return e;
  }

  function disegnaSegni() {
    segni.setAttribute('viewBox', '0 0 ' + VISTA[0] + ' ' + VISTA[1]);
    var aree = svgEl('g', { id: 'gsp-aree', 'class': 'gsp-aree' });
    LUOGHI.aree.filter(function (a) { return a.tipo === 'AA'; }).forEach(function (a) {
      var g = svgEl('g', { transform: 'translate(' + a.x + ' ' + a.y + ')' });
      g.appendChild(svgEl('title', {}, 'Area di attesa ' + a.id + ': ' + a.nome + ', ' + a.indirizzo));
      g.appendChild(svgEl('rect', { x: -15, y: -11, width: 30, height: 22, rx: 4, 'class': 'gsp-aa' }));
      g.appendChild(svgEl('text', { x: 0, y: 5, 'class': 'gsp-aa-t' }, a.id.replace('AA', '')));
      aree.appendChild(g);
    });
    segni.appendChild(aree);
    var lago = LUOGHI.luoghi.lago;
    if (lago) segni.appendChild(svgEl('text', { x: lago.x, y: lago.y, 'class': 'gsp-etichetta' }, 'Lago di Nemi'));
    var pin = svgEl('g', { id: 'gsp-pin', 'class': 'gsp-pin', visibility: 'hidden' });
    pin.appendChild(svgEl('circle', { r: 26, 'class': 'gsp-pin-alone' }));
    pin.appendChild(svgEl('circle', { r: 11, 'class': 'gsp-pin-punto' }));
    segni.appendChild(pin);
    mostraAree(interruttoreAree.checked);
    var elenco = $('#gsp-elenco-aree');
    if (elenco) {
      elenco.innerHTML = LUOGHI.aree.filter(function (a) { return a.tipo === 'AA'; }).map(function (a) {
        return '<li>' + esc(a.id) + ' — ' + esc(a.nome) + ', ' + esc(a.indirizzo) + '</li>';
      }).join('');
    }
  }

  function mostraAree(si) {
    var g = $('#gsp-aree');
    if (g) g.style.display = si ? '' : 'none';
    ls('pcgenzano.gsp.aree', si ? '1' : '0');
  }

  function inquadra(chiave, zoom) {
    var l = LUOGHI && LUOGHI.luoghi[chiave];
    var pin = $('#gsp-pin');
    var cw = mappa.clientWidth, ch = mappa.clientHeight;
    var scala = cw / VISTA[0];
    var Z = zoom || 1;
    var px, py;
    if (l) {
      px = l.x * scala; py = l.y * scala;
      pin.setAttribute('transform', 'translate(' + l.x + ' ' + l.y + ')');
      pin.setAttribute('visibility', 'visible');
      dove.textContent = 'Dove sei: ' + l.nome;
    } else {
      px = cw / 2; py = 420 * scala;
      pin.setAttribute('visibility', 'hidden');
      dove.textContent = 'Genzano di Roma';
    }
    var alto = VISTA[1] * scala;
    var dx = cw / 2 - px, dy = ch / 2 - py;
    // niente bordi vuoti: la mappa copre sempre il riquadro
    dx = Math.min(dx, (Z - 1) * px);
    dx = Math.max(dx, cw - px - (cw - px) * Z);
    dy = Math.min(dy, (Z - 1) * py);
    dy = Math.max(dy, ch - py - (alto - py) * Z);
    camera.style.transformOrigin = px + 'px ' + py + 'px';
    camera.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(' + Z + ')';
  }

  /* ------------------------------------------------------------ meteo */
  var gocce = [], animazione = null, meteoAttuale = 'sereno';
  function meteo(tipo) {
    meteoAttuale = tipo;
    root.setAttribute('data-meteo', tipo);
    if ((tipo === 'pioggia' || tipo === 'buio') && !movimentoRidotto()) avviaPioggia();
    else fermaPioggia();
  }
  function avviaPioggia() {
    if (animazione) return;
    var c = pioggiaTela, ctx = c.getContext('2d');
    function misura() {
      c.width = c.clientWidth; c.height = c.clientHeight;
      var n = Math.round(c.width * c.height / 2600);
      gocce = [];
      for (var i = 0; i < n; i++) gocce.push({ x: Math.random() * c.width, y: Math.random() * c.height, v: 7 + Math.random() * 7 });
    }
    misura();
    function passo() {
      ctx.clearRect(0, 0, c.width, c.height);
      ctx.strokeStyle = meteoAttuale === 'buio' ? 'rgba(200,215,235,.45)' : 'rgba(40,70,110,.35)';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      gocce.forEach(function (d) {
        ctx.moveTo(d.x, d.y); ctx.lineTo(d.x - 2, d.y + 10);
        d.y += d.v; d.x -= .6;
        if (d.y > c.height) { d.y = -10; d.x = Math.random() * c.width; }
      });
      ctx.stroke();
      animazione = requestAnimationFrame(passo);
    }
    animazione = requestAnimationFrame(passo);
    window.addEventListener('resize', misura);
  }
  function fermaPioggia() {
    if (animazione) cancelAnimationFrame(animazione);
    animazione = null;
    var ctx = pioggiaTela.getContext('2d');
    ctx.clearRect(0, 0, pioggiaTela.width, pioggiaTela.height);
  }
  // se la persona chiede di fermare le animazioni a pagina aperta
  new MutationObserver(function () { meteo(meteoAttuale); })
    .observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mq.addEventListener) mq.addEventListener('change', function () { meteo(meteoAttuale); });
  }

  /* --------------------------------------------------- lettura ad alta voce */
  var parla = ('speechSynthesis' in window) ? window.speechSynthesis : null;
  function leggi() {
    if (!parla) return;
    if (parla.speaking) { parla.cancel(); return; }
    var testo = Array.prototype.map.call(pannello.querySelectorAll('[data-leggi]'), function (e) {
      return e.textContent.trim();
    }).join('. ');
    var u = new SpeechSynthesisUtterance(testo);
    u.lang = 'it-IT';
    var r = parseFloat(ls('pcgenzano-tts-rate'));
    u.rate = r > 0 ? r : 0.95;
    var voce = parla.getVoices().filter(function (v) { return /^it/i.test(v.lang); })[0];
    if (voce) u.voice = voce;
    parla.speak(u);
  }
  function smettiDiLeggere() { if (parla) parla.cancel(); }

  /* ------------------------------------------------------------- schermate */
  function mostra(html, chiaveLuogo, zoom) {
    smettiDiLeggere();
    pannello.innerHTML = html +
      (parla ? '<p class="gsp-ascolta"><button type="button" class="btn btn-outline-primary btn-sm" data-azione="ascolta">' +
        '<i class="bi bi-volume-up-fill me-1" aria-hidden="true"></i>Ascolta</button></p>' : '');
    inquadra(chiaveLuogo, zoom);
    var h = pannello.querySelector('h2');
    if (h) {
      h.setAttribute('tabindex', '-1');
      h.focus({ preventScroll: true });
      // su telefono la mappa sta sopra: si porta in vista l'inizio del testo
      var r = h.getBoundingClientRect();
      if (r.top < 0 || r.top > window.innerHeight * 0.6) {
        h.scrollIntoView({ behavior: movimentoRidotto() ? 'auto' : 'smooth', block: 'start' });
      }
    }
  }

  function schermataIniziale() {
    var s = window.GenzanoScenari.temporale;
    barraAllerta.hidden = true;
    meteo('sereno');
    mostra(
      '<h2 data-leggi>Scegli lo scenario</h2>' +
      '<p data-leggi>Una famiglia di Genzano, una città vera e un evento simulato. Prima ti prepari, poi affronti quello che succede, alla fine scopri che cosa la preparazione ha evitato.</p>' +
      '<div class="gsp-scenari">' +
      '<button type="button" class="gsp-scenario" data-azione="inizia" data-scenario="temporale">' +
      '<span class="gsp-scenario-t"><i class="bi bi-cloud-lightning-rain-fill me-2" aria-hidden="true"></i>' + esc(s.titolo) + '</span>' +
      '<span class="gsp-scenario-d">' + esc(s.rischio) + ' · ' + esc(s.durata) + '</span></button>' +
      '<div class="gsp-scenario gsp-presto" aria-disabled="true"><span class="gsp-scenario-t"><i class="bi bi-house-exclamation me-2" aria-hidden="true"></i>La scossa della notte</span><span class="gsp-scenario-d">Rischio sismico · in preparazione</span></div>' +
      '<div class="gsp-scenario gsp-presto" aria-disabled="true"><span class="gsp-scenario-t"><i class="bi bi-fire me-2" aria-hidden="true"></i>Fumo sulla collina</span><span class="gsp-scenario-d">Incendio boschivo · in preparazione</span></div>' +
      '<div class="gsp-scenario gsp-presto" aria-disabled="true"><span class="gsp-scenario-t"><i class="bi bi-thermometer-sun me-2" aria-hidden="true"></i>Luglio rovente</span><span class="gsp-scenario-d">Ondata di calore · in preparazione</span></div>' +
      '</div>' +
      '<h3 class="h6 mt-3">Come si gioca</h3>' +
      '<ul class="gsp-come"><li>Prima dell\'evento scegli come usare il tempo che hai: non puoi fare tutto.</li>' +
      '<li>Durante l\'evento scegli che cosa fare. Dopo ogni scelta leggi perché è giusta o sbagliata.</li>' +
      '<li>Non c\'è un tempo limite: leggi con calma.</li></ul>',
      null, 1);
  }

  function inizia(id) {
    var s = window.GenzanoScenari[id];
    stato = { s: s, scelte: {}, prep: [], indice: -1, punti: 0, massimo: 0, diario: [] };
    meteo('sereno');
    mostra(
      '<p class="gsp-ora" data-leggi>' + esc(s.prima.ora) + '</p>' +
      '<h2 data-leggi>' + esc(s.titolo) + '</h2>' +
      s.intro.map(function (t) { return '<p data-leggi>' + esc(t) + '</p>'; }).join('') +
      '<button type="button" class="btn btn-primary" data-azione="prima">Prepararsi</button>',
      'casa', 1.6);
    barraAllerta.hidden = false;
    barraAllerta.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i><strong>' +
      esc(s.allerta.testo) + '</strong><span class="gsp-allerta-fonte"> · Fonte: ' + esc(s.allerta.fonte) + ' (simulazione)</span>';
  }

  function schermataPrima() {
    var p = stato.s.prima;
    var html = '<p class="gsp-ora" data-leggi>' + esc(p.ora) + '</p>' +
      '<h2 data-leggi>Prepararsi</h2>' +
      '<p data-leggi>' + esc(p.testo) + '</p>' +
      '<p class="gsp-contatore" id="gsp-contatore" aria-live="polite"></p>' +
      '<ul class="gsp-azioni">';
    p.azioni.forEach(function (a) {
      html += '<li><button type="button" class="gsp-azione" aria-pressed="false" data-azione="prep" data-id="' + a.id + '">' +
        '<span class="gsp-spunta" aria-hidden="true"></span><span>' + esc(a.testo) + '</span></button></li>';
    });
    html += '</ul><button type="button" class="btn btn-primary" data-azione="via" disabled>È venerdì: andiamo avanti</button>';
    mostra(html, 'casa', 1.6);
    aggiornaContatore();
  }

  function aggiornaContatore() {
    var n = stato.prep.length, max = stato.s.prima.posti;
    $('#gsp-contatore').textContent = 'Hai scelto ' + n + ' cose su ' + max + '.' +
      (n === max ? ' Puoi andare avanti, o cambiare una scelta.' : '');
    pannello.querySelectorAll('.gsp-azione').forEach(function (b) {
      var su = stato.prep.indexOf(b.getAttribute('data-id')) >= 0;
      b.setAttribute('aria-pressed', su ? 'true' : 'false');
      b.disabled = !su && n >= max;
    });
    $('[data-azione="via"]', pannello).disabled = n !== max;
  }

  function preparazione() {
    var p = {};
    stato.prep.forEach(function (id) { p[id] = true; });
    return p;
  }

  function prossimoEvento() {
    var p = preparazione();
    var ev = stato.s.eventi;
    var prima = stato.indice >= 0 ? ev[stato.indice] : null;
    do { stato.indice++; } while (stato.indice < ev.length && ev[stato.indice].solo && !ev[stato.indice].solo(p));
    if (stato.indice >= ev.length) return resoconto();
    var e = ev[stato.indice];
    if (prima && prima.fase === 'durante' && e.fase === 'dopo') return passaggioAlDopo();
    mostraEvento(e, p);
  }

  function passaggioAlDopo() {
    barraAllerta.innerHTML = '<i class="bi bi-check-circle-fill me-2" aria-hidden="true"></i><strong>Allerta terminata</strong><span class="gsp-allerta-fonte"> · Fonte: Centro Funzionale della Regione Lazio (simulazione)</span>';
    barraAllerta.classList.add('gsp-allerta-fine');
    meteo('sereno');
    mostra('<h2 data-leggi>La notte è passata</h2>' +
      '<p data-leggi>La pioggia è finita. Adesso comincia il dopo: anche qui le scelte contano.</p>' +
      '<button type="button" class="btn btn-primary" data-azione="dopo">Vai alla mattina</button>', 'casa', 1.4);
  }

  function mostraEvento(e, p) {
    meteo(e.meteo);
    var scelte = valore(e.scelte, p);
    stato.scelteCorrenti = scelte;
    var html = '<p class="gsp-ora" data-leggi>' + esc(e.ora) + ' · ' + (e.fase === 'dopo' ? 'Dopo' : 'Durante') + '</p>' +
      '<h2 data-leggi>' + esc(e.titolo) + '</h2>' +
      '<p data-leggi>' + esc(valore(e.testo, p)) + '</p>' +
      '<p class="gsp-domanda" data-leggi>Che cosa fai?</p><ul class="gsp-scelte">';
    scelte.forEach(function (c, i) {
      html += '<li><button type="button" class="gsp-scelta" data-azione="scegli" data-i="' + i + '" data-leggi>' + esc(c.testo) + '</button></li>';
    });
    html += '</ul>';
    mostra(html, e.luogo, 2.1);
  }

  function scegli(i) {
    var e = stato.s.eventi[stato.indice];
    var scelte = stato.scelteCorrenti;
    var c = scelte[i];
    var max = Math.max.apply(null, scelte.map(function (x) { return x.punti; }));
    var ottimo = 3;
    stato.punti += c.punti;
    stato.massimo += ottimo;
    stato.diario.push({ titolo: e.titolo, scelta: c.testo, punti: c.punti, perche: c.perche, link: e.link });
    var tipo = c.punti === 3 ? 'giusta' : (c.punti > 0 ? 'meglio' : 'sbagliata');
    var etichetta = { giusta: 'Scelta giusta', meglio: 'Si poteva fare meglio', sbagliata: 'Scelta sbagliata' }[tipo];
    var icona = { giusta: 'bi-check-circle-fill', meglio: 'bi-dash-circle-fill', sbagliata: 'bi-x-circle-fill' }[tipo];
    pannello.querySelectorAll('.gsp-scelta').forEach(function (b, j) {
      b.disabled = true;
      if (j === i) b.classList.add('gsp-scelta-tua');
    });
    var nota = (max < 3 && c.punti === max)
      ? '<p class="gsp-nota">In questa situazione non c\'era una scelta perfetta: la preparazione di ieri l\'avrebbe resa possibile.</p>' : '';
    var box = document.createElement('div');
    box.className = 'gsp-esito gsp-esito-' + tipo;
    box.innerHTML = '<p class="gsp-esito-t" data-leggi><i class="bi ' + icona + ' me-2" aria-hidden="true"></i>' + etichetta + '</p>' +
      '<p data-leggi>' + esc(c.perche) + '</p>' + nota +
      '<p class="gsp-esito-link">Approfondisci: ' + link(e.link, 'la pagina del sito') + '</p>' +
      '<button type="button" class="btn btn-primary" data-azione="avanti">Avanti</button>';
    pannello.insertBefore(box, pannello.querySelector('.gsp-ascolta'));
    var t = box.querySelector('.gsp-esito-t');
    t.setAttribute('tabindex', '-1');
    t.focus();
  }

  function resoconto() {
    var s = stato.s, p = preparazione();
    var pesi = s.prima.azioni.map(function (a) { return a.peso; }).sort(function (a, b) { return b - a; });
    var maxPrep = pesi.slice(0, s.prima.posti).reduce(function (a, b) { return a + b; }, 0);
    var prep = s.prima.azioni.filter(function (a) { return p[a.id]; }).reduce(function (t, a) { return t + a.peso; }, 0);
    var totale = prep + stato.punti, massimo = maxPrep + stato.massimo;
    var perc = Math.round(totale / massimo * 100);
    var evitati = s.resoconto.filter(function (r) { return p[r.se]; });
    var successi = s.resoconto.filter(function (r) { return !p[r.se]; });
    var inutili = s.prima.azioni.filter(function (a) { return p[a.id] && a.peso === 0; });
    meteo('sereno');
    barraAllerta.hidden = true;

    var html = '<h2 data-leggi>Com\'è andata</h2>' +
      '<p class="gsp-punteggio" data-leggi>Preparazione: ' + prep + ' su ' + maxPrep + ' · Decisioni: ' + stato.punti + ' su ' + stato.massimo + '</p>' +
      '<div class="gsp-barra" role="img" aria-label="Risultato complessivo: ' + perc + ' per cento"><div style="width:' + perc + '%"></div></div>';
    if (evitati.length) {
      html += '<h3 class="h5 mt-3" data-leggi>I disastri che non sono successi</h3><ul class="gsp-lista gsp-lista-si">' +
        evitati.map(function (r) { return '<li data-leggi>' + esc(r.si) + '</li>'; }).join('') + '</ul>';
    }
    if (successi.length) {
      html += '<h3 class="h5 mt-3" data-leggi>Che cosa poteva andare meglio</h3><ul class="gsp-lista gsp-lista-no">' +
        successi.map(function (r) { return '<li data-leggi>' + esc(r.no) + '</li>'; }).join('') + '</ul>';
    }
    if (inutili.length) {
      html += '<p class="gsp-nota" data-leggi>' + inutili.map(function (a) { return esc(a.perche); }).join(' ') + '</p>';
    }
    html += '<details class="gsp-diario"><summary>Rivedi le tue scelte</summary><ol>' +
      stato.diario.map(function (d) {
        return '<li><strong>' + esc(d.titolo) + '</strong>: ' + esc(d.scelta) + ' <em>(' + d.punti + ' su 3)</em><br>' + esc(d.perche) + '</li>';
      }).join('') + '</ol></details>';

    var aa = areaPiuVicina();
    html += '<div class="gsp-ricorda"><h3 class="h6" data-leggi>Per la vita vera</h3><ul>' +
      '<li data-leggi>Controlla l\'allerta di oggi su ' + link('/allerte-meteo/', 'Allerte meteo') + '.</li>' +
      '<li data-leggi>Prepara il ' + link('/piano-familiare/', 'piano familiare') + ' e il ' + link('/rischi-prevenzione/kit-emergenza/', 'kit di emergenza') + '.</li>' +
      (aa ? '<li data-leggi>Per il terremoto il punto di ritrovo è l\'area di attesa: per la casa del gioco la più vicina è la ' + esc(aa.id) + ', ' + esc(aa.nome) + '. Trova la tua su ' + link('/aree-attesa/', 'Aree di attesa') + '.</li>' : '') +
      '<li data-leggi>In emergenza chiama il 112 e segui solo le fonti ufficiali.</li></ul></div>' +
      '<div id="gsp-attestato"></div>' +
      '<p class="mt-3"><button type="button" class="btn btn-primary me-2" data-azione="rigioca">Gioca di nuovo</button>' +
      '<button type="button" class="btn btn-outline-primary" data-azione="scenari">Torna agli scenari</button></p>';
    mostra(html, 'casa', 1);
    if (window.GiochiUtil && window.GiochiUtil.salvaEMostraAttestato) {
      window.GiochiUtil.salvaEMostraAttestato(ID_GIOCO, totale, massimo, '#gsp-attestato');
    }
  }

  function areaPiuVicina() {
    if (!LUOGHI || !LUOGHI.luoghi.casa) return null;
    var c = LUOGHI.luoghi.casa, meglio = null, dist = Infinity;
    LUOGHI.aree.forEach(function (a) {
      if (a.tipo !== 'AA') return;
      var d = Math.hypot(a.x - c.x, a.y - c.y);
      if (d < dist) { dist = d; meglio = a; }
    });
    return meglio;
  }

  /* -------------------------------------------------------------- eventi */
  pannello.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-azione]');
    if (!b || b.disabled) return;
    var a = b.getAttribute('data-azione');
    if (a === 'inizia') inizia(b.getAttribute('data-scenario'));
    else if (a === 'prima') schermataPrima();
    else if (a === 'prep') {
      var id = b.getAttribute('data-id'), k = stato.prep.indexOf(id);
      if (k >= 0) stato.prep.splice(k, 1); else stato.prep.push(id);
      aggiornaContatore();
      var az = stato.s.prima.azioni.filter(function (x) { return x.id === id; })[0];
      inquadra(az.luogo, 1.6);
    }
    else if (a === 'via') prossimoEvento();
    else if (a === 'scegli') scegli(parseInt(b.getAttribute('data-i'), 10));
    else if (a === 'avanti' || a === 'dopo') prossimoEvento();
    else if (a === 'rigioca') inizia(stato.s.id);
    else if (a === 'scenari') schermataIniziale();
    else if (a === 'ascolta') leggi();
  });
  interruttoreAree.addEventListener('change', function () { mostraAree(interruttoreAree.checked); });
  window.addEventListener('resize', function () {
    if (!LUOGHI) return;
    var t = camera.style.transform.match(/scale\(([\d.]+)\)/);
    var e = stato && stato.indice >= 0 && stato.s.eventi[stato.indice];
    inquadra(e ? e.luogo : 'casa', t ? parseFloat(t[1]) : 1);
  });
  window.addEventListener('pagehide', smettiDiLeggere);

  interruttoreAree.checked = ls('pcgenzano.gsp.aree') !== '0';
  caricaLuoghi().then(schermataIniziale);
})();
