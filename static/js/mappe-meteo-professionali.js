(function () {
  'use strict';

  var pagina = document.getElementById('mmp-pagina');
  if (!pagina) return;

  var statoEl = document.getElementById('mmp-stato');
  var formEl = document.getElementById('mmp-comandi');
  var selModello = document.getElementById('mmp-modello');
  var selDominio = document.getElementById('mmp-dominio');
  var infoModello = document.getElementById('mmp-modello-info');
  var sezMini = document.getElementById('mmp-miniature-sezione');
  var griglia = document.getElementById('mmp-griglia');
  var sezVista = document.getElementById('mmp-visualizzatore');
  var titoloVista = document.getElementById('mmp-vista-titolo');
  var sottoVista = document.getElementById('mmp-vista-sotto');
  var btnPlay = document.getElementById('mmp-play');
  var playEtichetta = document.getElementById('mmp-play-etichetta');
  var btnPrec = document.getElementById('mmp-precedente');
  var btnSucc = document.getElementById('mmp-successiva');
  var selVelocita = document.getElementById('mmp-velocita');
  var cursore = document.getElementById('mmp-ora');
  var oraEtichetta = document.getElementById('mmp-ora-etichetta');
  var img = document.getElementById('mmp-immagine');
  var didascalia = document.getElementById('mmp-didascalia');
  var aGif = document.getElementById('mmp-scarica-gif');
  var aPng = document.getElementById('mmp-scarica-png');
  var aMp4 = document.getElementById('mmp-scarica-mp4');
  var btnCondividi = document.getElementById('mmp-condividi');
  var esitoEl = document.getElementById('mmp-esito');

  var manifesto = null;
  var prodottoAttivo = null;
  var indice = 0;
  var timer = null;
  var cacheImg = {};

  function urlBase() {
    return manifesto && manifesto.base_url ? manifesto.base_url.replace(/\/$/, '') : '';
  }

  function assoluto(rel) {
    if (!rel) return '';
    if (/^https?:\/\//i.test(rel)) return rel;
    return urlBase() + '/' + rel.replace(/^\//, '');
  }

  function scriviStato(testo) {
    statoEl.textContent = testo;
  }

  function nomiDomini() {
    return { italia: 'Italia e Mediterraneo centrale', europa: 'Europa' };
  }

  function modelliOrdinati() {
    var ids = Object.keys(manifesto.modelli || {});
    var ordine = ['gfs', 'ecmwf', 'ecmwf-aifs', 'icon-eu'];
    ids.sort(function (a, b) {
      var ia = ordine.indexOf(a);
      var ib = ordine.indexOf(b);
      return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
    });
    return ids;
  }

  function modelloCorrente() {
    return manifesto.modelli[selModello.value];
  }

  function prodottiDelDominio() {
    var m = modelloCorrente();
    if (!m || !m.domini || !m.domini[selDominio.value]) return {};
    return m.domini[selDominio.value].prodotti || {};
  }

  function popolaSelect() {
    selModello.innerHTML = '';
    modelliOrdinati().forEach(function (id) {
      var m = manifesto.modelli[id];
      var o = document.createElement('option');
      o.value = id;
      o.textContent = m.nome;
      selModello.appendChild(o);
    });
    aggiornaDomini();
  }

  function aggiornaDomini() {
    var m = modelloCorrente();
    var etichette = nomiDomini();
    var precedente = selDominio.value;
    selDominio.innerHTML = '';
    if (!m) return;
    Object.keys(m.domini || {}).forEach(function (id) {
      var o = document.createElement('option');
      o.value = id;
      o.textContent = etichette[id] || id;
      selDominio.appendChild(o);
    });
    if (precedente) {
      var esiste = Array.prototype.some.call(selDominio.options, function (o) { return o.value === precedente; });
      if (esiste) selDominio.value = precedente;
    }
    var attrib = m.attribuzione || m.ente;
    var corsa = m.init_testo || m.corsa;
    infoModello.textContent = m.risoluzione + ' · ' + attrib + ' · corsa ' + corsa;
  }

  function disegnaGriglia() {
    var prodotti = prodottiDelDominio();
    var chiavi = Object.keys(prodotti);
    chiavi.sort(function (a, b) {
      return (prodotti[a].ordine || 99) - (prodotti[b].ordine || 99);
    });
    griglia.innerHTML = '';
    chiavi.forEach(function (id) {
      var p = prodotti[id];
      var li = document.createElement('li');
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mmp-scheda' + (prodottoAttivo === id ? ' is-attiva' : '');
      btn.setAttribute('aria-pressed', prodottoAttivo === id ? 'true' : 'false');
      if (p.miniatura) {
        var im = document.createElement('img');
        im.src = assoluto(p.miniatura);
        im.alt = '';
        im.loading = 'lazy';
        btn.appendChild(im);
      }
      var corpo = document.createElement('div');
      corpo.className = 'mmp-scheda-corpo';
      var t = document.createElement('strong');
      t.textContent = p.titolo;
      var s = document.createElement('span');
      var n = p.fotogrammi ? p.fotogrammi.length : 0;
      s.textContent = n + (n === 1 ? ' fotogramma' : ' fotogrammi');
      corpo.appendChild(t);
      corpo.appendChild(s);
      btn.appendChild(corpo);
      btn.addEventListener('click', function () { apriProdotto(id); });
      li.appendChild(btn);
      griglia.appendChild(li);
    });
    sezMini.hidden = chiavi.length === 0;
    if (chiavi.length && (!prodottoAttivo || !prodotti[prodottoAttivo])) {
      apriProdotto(chiavi[0]);
    } else if (prodottoAttivo && prodotti[prodottoAttivo]) {
      apriProdotto(prodottoAttivo);
    }
  }

  function apriProdotto(id) {
    ferma();
    prodottoAttivo = id;
    var p = prodottiDelDominio()[id];
    if (!p || !p.fotogrammi || !p.fotogrammi.length) {
      sezVista.hidden = true;
      return;
    }
    titoloVista.textContent = p.titolo;
    sottoVista.textContent = p.sottotitolo || '';
    cursore.min = '0';
    cursore.max = String(p.fotogrammi.length - 1);
    cursore.disabled = false;
    indice = Math.min(indice, p.fotogrammi.length - 1);
    cursore.value = String(indice);
    sezVista.hidden = false;
    if (p.gif) {
      aGif.href = assoluto(p.gif);
      aGif.removeAttribute('hidden');
      aGif.setAttribute('download', nomeFile(id, 'gif'));
      btnCondividi.hidden = !condivisionePossibile();
    } else {
      aGif.href = '#';
      aGif.setAttribute('hidden', 'hidden');
      btnCondividi.hidden = true;
    }
    if (p.mp4) {
      aMp4.href = assoluto(p.mp4);
      aMp4.hidden = false;
      aMp4.setAttribute('download', nomeFile(id, 'mp4'));
    } else {
      aMp4.hidden = true;
    }
    Array.prototype.forEach.call(griglia.querySelectorAll('.mmp-scheda'), function (b) {
      var attiva = b.querySelector('strong') && b.querySelector('strong').textContent === p.titolo;
      b.classList.toggle('is-attiva', !!attiva);
      b.setAttribute('aria-pressed', attiva ? 'true' : 'false');
    });
    mostraFotogramma(indice);
    precacheVicini();
  }

  function nomeFile(id, ext) {
    var m = modelloCorrente();
    var corsa = m && m.corsa ? m.corsa : 'corsa';
    return 'mappa-' + selModello.value + '-' + selDominio.value + '-' + id + '-' + corsa + '.' + ext;
  }

  function mostraFotogramma(i) {
    var p = prodottiDelDominio()[prodottoAttivo];
    if (!p || !p.fotogrammi[i]) return;
    indice = i;
    cursore.value = String(i);
    var f = p.fotogrammi[i];
    var src = assoluto(f.png);
    img.src = src;
    var ore = typeof f.ora === 'number' ? f.ora : i;
    var etichetta = 'F' + (ore < 10 ? '00' : ore < 100 ? '0' : '') + String(ore) + '  ·  +' + ore + ' ore';
    oraEtichetta.textContent = etichetta;
    var alt = p.titolo + ', ' + etichetta;
    var m = modelloCorrente();
    if (m) alt += ', modello ' + m.nome + ', corsa ' + (m.init_testo || m.corsa);
    img.alt = alt;
    didascalia.textContent = alt;
    aPng.href = src;
    aPng.setAttribute('download', nomeFile(prodottoAttivo, 'png').replace(/\.png$/, '-f' + (ore < 10 ? '00' : ore < 100 ? '0' : '') + ore + '.png'));
  }

  function precacheVicini() {
    var p = prodottiDelDominio()[prodottoAttivo];
    if (!p) return;
    [indice - 1, indice + 1, indice + 2].forEach(function (k) {
      if (k < 0 || k >= p.fotogrammi.length) return;
      var src = assoluto(p.fotogrammi[k].png);
      if (cacheImg[src]) return;
      var im = new Image();
      im.src = src;
      cacheImg[src] = im;
    });
  }

  function vai(delta) {
    var p = prodottiDelDominio()[prodottoAttivo];
    if (!p) return;
    var n = p.fotogrammi.length;
    mostraFotogramma((indice + delta + n) % n);
    precacheVicini();
  }

  function avvia() {
    if (timer) return;
    btnPlay.setAttribute('aria-pressed', 'true');
    playEtichetta.textContent = 'Ferma animazione';
    var icona = btnPlay.querySelector('i');
    if (icona) icona.className = 'bi bi-pause-fill';
    timer = setInterval(function () { vai(1); }, parseInt(selVelocita.value, 10) || 450);
  }

  function ferma() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
    btnPlay.setAttribute('aria-pressed', 'false');
    playEtichetta.textContent = 'Avvia animazione';
    var icona = btnPlay.querySelector('i');
    if (icona) icona.className = 'bi bi-play-fill';
  }

  function onTasto(ev) {
    if (sezVista.hidden) return;
    var t = ev.target;
    var tag = t && t.tagName ? t.tagName.toLowerCase() : '';
    if (tag === 'input' || tag === 'select' || tag === 'textarea' || tag === 'button' || tag === 'a') {
      if (ev.key !== ' ' && ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight' && ev.key !== 'Home' && ev.key !== 'End') return;
      if (tag === 'input' || tag === 'select' || tag === 'textarea') return;
    }
    if (ev.key === 'ArrowLeft') { ev.preventDefault(); vai(-1); }
    else if (ev.key === 'ArrowRight') { ev.preventDefault(); vai(1); }
    else if (ev.key === 'Home') { ev.preventDefault(); mostraFotogramma(0); }
    else if (ev.key === 'End') {
      ev.preventDefault();
      var p = prodottiDelDominio()[prodottoAttivo];
      if (p) mostraFotogramma(p.fotogrammi.length - 1);
    } else if (ev.key === ' ') {
      ev.preventDefault();
      if (timer) ferma(); else avvia();
    }
  }

  function decodificaApi(json) {
    if (!json || !json.content) return null;
    var b64 = String(json.content).replace(/\s/g, '');
    var bin = atob(b64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    var testo = new TextDecoder('utf-8').decode(bytes);
    return JSON.parse(testo);
  }

  // I file stanno su un altro dominio: l'attributo download da solo non basta,
  // quindi si scarica il file e lo si salva con il nome giusto.
  function scaricaFile(ev) {
    var a = ev.currentTarget;
    var url = a.getAttribute('href');
    if (!url || url === '#') { ev.preventDefault(); return; }
    if (!window.fetch || !window.URL || !URL.createObjectURL) return;
    ev.preventDefault();
    var nome = a.getAttribute('download') || 'mappa-meteo';
    esitoEl.textContent = 'Preparazione del file…';
    fetch(url).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.blob();
    }).then(function (blob) {
      var link = document.createElement('a');
      var obj = URL.createObjectURL(blob);
      link.href = obj;
      link.download = nome;
      document.body.appendChild(link);
      link.click();
      setTimeout(function () { URL.revokeObjectURL(obj); link.remove(); }, 1500);
      esitoEl.textContent = 'File scaricato: ' + nome;
    }).catch(function () {
      esitoEl.textContent = 'Download diretto non riuscito: il file si apre in una nuova scheda.';
      window.open(url, '_blank', 'noopener');
    });
  }

  function condividiGif() {
    var url = aGif.getAttribute('href');
    if (!url || url === '#') return;
    var nome = aGif.getAttribute('download') || 'mappa-meteo.gif';
    esitoEl.textContent = 'Preparazione della GIF…';
    fetch(url).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.blob();
    }).then(function (blob) {
      var file = new File([blob], nome, { type: 'image/gif' });
      var dati = { files: [file], title: titoloVista.textContent, text: titoloVista.textContent + ' — Protezione Civile di Genzano di Roma' };
      if (navigator.canShare && navigator.canShare(dati)) {
        return navigator.share(dati).then(function () { esitoEl.textContent = 'GIF condivisa.'; });
      }
      throw new Error('condivisione non disponibile');
    }).catch(function (e) {
      if (e && e.name === 'AbortError') { esitoEl.textContent = ''; return; }
      esitoEl.textContent = 'Condivisione non disponibile su questo dispositivo: usa «Scarica GIF».';
    });
  }

  function condivisionePossibile() {
    try {
      var prova = new File([new Blob(['x'], { type: 'image/gif' })], 'prova.gif', { type: 'image/gif' });
      return !!(navigator.canShare && navigator.canShare({ files: [prova] }));
    } catch (e) {
      return false;
    }
  }

  function caricaManifesto() {
    var urlRaw = pagina.getAttribute('data-manifesto') + (pagina.getAttribute('data-manifesto').indexOf('?') >= 0 ? '&' : '?') + 't=' + Date.now();
    var urlApi = pagina.getAttribute('data-api');
    return fetch(urlRaw, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error('raw ' + r.status);
      return r.json();
    }).catch(function () {
      return fetch(urlApi, { headers: { 'Accept': 'application/vnd.github+json' } }).then(function (r) {
        if (!r.ok) throw new Error('api ' + r.status);
        return r.json();
      }).then(decodificaApi);
    });
  }

  selModello.addEventListener('change', function () {
    prodottoAttivo = null;
    indice = 0;
    aggiornaDomini();
    disegnaGriglia();
  });
  selDominio.addEventListener('change', function () {
    prodottoAttivo = null;
    indice = 0;
    disegnaGriglia();
  });
  btnPlay.addEventListener('click', function () { if (timer) ferma(); else avvia(); });
  btnPrec.addEventListener('click', function () { ferma(); vai(-1); });
  btnSucc.addEventListener('click', function () { ferma(); vai(1); });
  cursore.addEventListener('input', function () {
    ferma();
    mostraFotogramma(parseInt(cursore.value, 10) || 0);
  });
  selVelocita.addEventListener('change', function () {
    if (timer) { ferma(); avvia(); }
  });
  document.addEventListener('keydown', onTasto);
  aGif.addEventListener('click', scaricaFile);
  aPng.addEventListener('click', scaricaFile);
  aMp4.addEventListener('click', scaricaFile);
  btnCondividi.addEventListener('click', condividiGif);

  caricaManifesto().then(function (dati) {
    if (!dati || !dati.modelli || !Object.keys(dati.modelli).length) {
      scriviStato('Le carte della corsa più recente non sono ancora disponibili. Riprova fra poco, oppure consulta le allerte ufficiali.');
      return;
    }
    manifesto = dati;
    formEl.hidden = false;
    popolaSelect();
    disegnaGriglia();
    var nMod = Object.keys(dati.modelli).length;
    scriviStato('Carte aggiornate il ' + (dati.generato_testo || dati.generato) + '. Modelli disponibili: ' + nMod + '.');
  }).catch(function () {
    scriviStato('Non è stato possibile caricare le carte in questo momento. Le allerte ufficiali restano nella pagina Allerte meteo.');
  });
})();
