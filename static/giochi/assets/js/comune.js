/* Utility comuni per i giochi — Protezione Civile Genzano */

(function (global) {
  'use strict';

  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function crea(tag, attrs, testo) {
    var el = document.createElement(tag);
    if (attrs) {
      for (var k in attrs) {
        if (!attrs.hasOwnProperty(k)) continue;
        if (k === 'class') el.className = attrs[k];
        else if (k === 'dataset') {
          for (var d in attrs[k]) el.dataset[d] = attrs[k][d];
        } else if (k.indexOf('aria-') === 0 || k === 'role' || k === 'tabindex') {
          el.setAttribute(k, attrs[k]);
        } else {
          el[k] = attrs[k];
        }
      }
    }
    if (testo !== undefined && testo !== null) el.textContent = testo;
    return el;
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function preferscRidotto() {
    try {
      return global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (e) { return false; }
  }

  function annuncia(testo) {
    var live = document.getElementById('giochi-aria-live');
    if (!live) {
      live = document.createElement('div');
      live.id = 'giochi-aria-live';
      live.setAttribute('aria-live', 'polite');
      live.setAttribute('aria-atomic', 'true');
      live.style.cssText = 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0';
      document.body.appendChild(live);
    }
    live.textContent = '';
    setTimeout(function () { live.textContent = testo; }, 50);
  }

  // Crea un pulsante volume riutilizzabile
  function creaPulsanteVolume() {
    var btn = crea('button', {
      type: 'button',
      class: 'btn btn-sm btn-outline-primary gioco-volume-btn',
      'aria-label': 'Regola volume audio'
    });
    var stati = [
      { soglia: 0, icona: 'bi-volume-mute-fill', label: 'Audio disattivato (clicca per riattivare)' },
      { soglia: 0.35, icona: 'bi-volume-down-fill', label: 'Audio basso (clicca per alzare)' },
      { soglia: 0.75, icona: 'bi-volume-up-fill', label: 'Audio alto (clicca per abbassare)' }
    ];
    function aggiorna() {
      var v = (global.AudioSintetico && global.AudioSintetico.getVolume()) || 0;
      var stato = stati[0];
      if (v > 0.5) stato = stati[2];
      else if (v > 0) stato = stati[1];
      btn.innerHTML = '<i class="bi ' + stato.icona + '" aria-hidden="true"></i>';
      btn.setAttribute('aria-label', stato.label);
    }
    btn.addEventListener('click', function () {
      if (!global.AudioSintetico) return;
      var v = global.AudioSintetico.getVolume();
      var nuovo;
      if (v === 0) nuovo = 0.3;
      else if (v < 0.6) nuovo = 0.8;
      else nuovo = 0;
      global.AudioSintetico.setVolume(nuovo);
      aggiorna();
    });
    aggiorna();
    return btn;
  }

  // Mostra pannello fine gioco con attestato se percentuale >= 80
  function pannelloFineGioco(opzioni) {
    opzioni = opzioni || {};
    var contenitore = opzioni.contenitore;
    var idGioco = opzioni.idGioco;
    var percentuale = opzioni.percentuale;
    var onRiprova = opzioni.onRiprova;
    var puoAttestato = percentuale >= (global.GiochiPC && global.GiochiPC.SOGLIA_BADGE || 80);

    var html = ''
      + '<div class="gioco-fine text-center">'
      + '  <div class="display-4 mb-2 ' + (puoAttestato ? 'text-success' : 'text-primary') + '">'
      + '    <i class="bi ' + (puoAttestato ? 'bi-award-fill' : 'bi-emoji-smile') + '" aria-hidden="true"></i>'
      + '  </div>'
      + '  <h2>' + (puoAttestato ? 'Complimenti!' : 'Bravo!') + '</h2>'
      + '  <p class="lead">Hai ottenuto il <strong>' + percentuale + '%</strong> di risposte corrette.</p>';
    if (puoAttestato) {
      html += ''
        + '  <div class="alert alert-success border-0" style="border-radius:12px;">'
        + '    <p class="mb-2"><strong>Hai sbloccato il badge!</strong> Vuoi l\u2019attestato di partecipazione?</p>'
        + '    <div class="mb-2">'
        + '      <label for="nome-attestato" class="form-label small">Scrivi il tuo nome (max 40 caratteri):</label>'
        + '      <input type="text" id="nome-attestato" class="form-control" maxlength="40" placeholder="Il tuo nome">'
        + '    </div>'
        + '    <div class="d-flex flex-wrap gap-2 justify-content-center">'
        + '      <button type="button" id="btn-scarica-attestato" class="btn btn-success"><i class="bi bi-download me-1" aria-hidden="true"></i> Scarica attestato</button>'
        + '      <button type="button" id="btn-stampa-attestato" class="btn btn-outline-success"><i class="bi bi-printer me-1" aria-hidden="true"></i> Stampa attestato</button>'
        + '    </div>'
        + '  </div>';
    } else {
      html += '<p class="text-muted">Per ottenere l\u2019attestato devi rispondere correttamente almeno all\u201880% delle domande.</p>';
    }
    html += ''
      + '  <div class="d-flex flex-wrap gap-2 justify-content-center mt-3">'
      + '    <button type="button" id="btn-riprova" class="btn btn-primary"><i class="bi bi-arrow-clockwise me-1" aria-hidden="true"></i> Gioca ancora</button>'
      + '    <a href="../index.html" class="btn btn-outline-secondary"><i class="bi bi-grid-fill me-1" aria-hidden="true"></i> Altri giochi</a>'
      + '  </div>'
      + '</div>';

    contenitore.innerHTML = html;

    if (puoAttestato) {
      var inpNome = qs('#nome-attestato', contenitore);
      qs('#btn-scarica-attestato', contenitore).addEventListener('click', function () {
        var n = inpNome.value;
        if (global.AttestatoPC) global.AttestatoPC.genera(n, idGioco, percentuale);
      });
      qs('#btn-stampa-attestato', contenitore).addEventListener('click', function () {
        var n = inpNome.value;
        if (global.AttestatoPC) global.AttestatoPC.stampa(n, idGioco, percentuale);
      });
    }

    if (typeof onRiprova === 'function') {
      qs('#btn-riprova', contenitore).addEventListener('click', onRiprova);
    }
  }

  // Badge miglior risultato (da mostrare all'avvio di un gioco)
  function badgeMigliorRisultato(idGioco) {
    if (!global.GiochiPC) return null;
    var r = global.GiochiPC.leggiRisultato(idGioco);
    if (!r.completato) return null;
    var el = crea('div', { class: 'gioco-miglior-risultato', role: 'note' });
    el.innerHTML = '<i class="bi bi-trophy-fill me-1" aria-hidden="true"></i> Miglior risultato: <strong>' + r.percentuale + '%</strong>';
    return el;
  }

  // Salva risultato + mostra box attestato nel container indicato.
  // Funzione comoda per integrare l'attestato nei giochi esistenti.
  function salvaEMostraAttestato(idGioco, score, max, containerSelOrEl) {
    if (!idGioco || typeof score !== 'number' || typeof max !== 'number' || max <= 0) return;
    if (global.GiochiPC) global.GiochiPC.salvaRisultato(idGioco, score, max);
    var perc = Math.round((score / max) * 100);
    var cont = typeof containerSelOrEl === 'string' ? document.querySelector(containerSelOrEl) : containerSelOrEl;
    if (!cont) return;
    var box = cont.querySelector('.attestato-inject');
    if (!box) {
      box = document.createElement('div');
      box.className = 'attestato-inject my-3';
      cont.appendChild(box);
    }
    if (perc < 80) {
      box.innerHTML = '<p class="text-muted small mb-0"><i class="bi bi-info-circle me-1" aria-hidden="true"></i> Per ottenere l\u2019attestato devi ottenere almeno l\u201980%.</p>';
      return;
    }
    box.innerHTML = ''
      + '<div class="alert alert-success border-0 text-start" style="border-radius:12px;max-width:520px;margin:0 auto;">'
      + '  <p class="mb-2"><strong><i class="bi bi-award-fill me-1" aria-hidden="true"></i> Hai sbloccato il badge!</strong> Vuoi l\u2019attestato?</p>'
      + '  <label for="nome-att-' + idGioco + '" class="form-label small">Scrivi il tuo nome (max 40 caratteri):</label>'
      + '  <input type="text" id="nome-att-' + idGioco + '" class="form-control mb-2" maxlength="40" placeholder="Il tuo nome">'
      + '  <div class="d-flex flex-wrap gap-2 justify-content-center">'
      + '    <button type="button" class="btn btn-success" data-azione="scarica"><i class="bi bi-download me-1" aria-hidden="true"></i> Scarica</button>'
      + '    <button type="button" class="btn btn-outline-success" data-azione="stampa"><i class="bi bi-printer me-1" aria-hidden="true"></i> Stampa</button>'
      + '  </div>'
      + '</div>';
    var inp = box.querySelector('input');
    box.querySelector('[data-azione="scarica"]').addEventListener('click', function () {
      if (global.AttestatoPC) global.AttestatoPC.genera(inp.value, idGioco, perc);
    });
    box.querySelector('[data-azione="stampa"]').addEventListener('click', function () {
      if (global.AttestatoPC) global.AttestatoPC.stampa(inp.value, idGioco, perc);
    });
  }

  // Inietta automaticamente un bottone "Torna al menu" in ogni pagina di gioco.
  // Permette al bambino (o all'adulto che lo accompagna) di abbandonare il gioco
  // in qualsiasi momento senza dover finire la sessione. Determina il link
  // di destinazione dal breadcrumb della pagina (penultimo link, di solito
  // "Scuola Primaria" / "Infanzia" / "Ragazzi" / "Giochi della Sicurezza").
  function aggiungiPulsanteEsciGioco() {
    // Esci se è una pagina hub (lista giochi della fascia) — per loro c'è già il breadcrumb.
    // Una pagina di gioco specifica ha sempre uno di questi marker:
    var marker = document.querySelector(
      '#intro, #game, #end, #select-screen, #game-screen, #end-screen, #game-card, .gioco-fine, .scena-corrente, [data-gioco], .giochi-section main .game-container'
    );
    if (!marker) return;

    // Trova il link al menu della fascia: ultimo <a> nel breadcrumb prima dell'item active
    var crumbLinks = document.querySelectorAll('.breadcrumb a, nav[aria-label="Percorso"] a');
    var menuHref = '../index.html';
    if (crumbLinks.length > 0) {
      menuHref = crumbLinks[crumbLinks.length - 1].getAttribute('href') || menuHref;
    }

    // Il bottone è già presente? Non duplicare.
    if (document.getElementById('gioco-esci-btn')) return;

    var btn = document.createElement('a');
    btn.id = 'gioco-esci-btn';
    btn.href = menuHref;
    btn.setAttribute('aria-label', 'Esci dal gioco e torna al menu');
    btn.innerHTML = '<i class="bi bi-x-lg" aria-hidden="true"></i> <span class="gioco-esci-label">Torna al menu</span>';
    btn.style.cssText = [
      'position: fixed',
      'top: 1rem',
      'right: 1rem',
      'z-index: 9999',
      'background: #003366',
      'color: #ffffff',
      'text-decoration: none',
      'padding: 0.55rem 1rem',
      'border-radius: 24px',
      'font-weight: 600',
      'font-size: 0.95rem',
      'box-shadow: 0 3px 10px rgba(0,0,0,0.25)',
      'display: inline-flex',
      'align-items: center',
      'gap: 0.5rem',
      'border: 2px solid #ffffff'
    ].join(';');

    // Su schermi molto stretti, mostra solo l'icona (la label resta come aria-label)
    var stile = document.createElement('style');
    stile.textContent = ''
      + '#gioco-esci-btn:hover, #gioco-esci-btn:focus {'
      + '  background: #002244 !important;'
      + '  outline: 3px solid #ffbe2e;'
      + '  outline-offset: 2px;'
      + '}'
      + '#gioco-esci-btn .gioco-esci-label {'
      + '  white-space: nowrap;'
      + '}'
      + '@media (max-width: 480px) {'
      + '  #gioco-esci-btn .gioco-esci-label { display: none; }'
      + '  #gioco-esci-btn { padding: 0.55rem 0.7rem !important; }'
      + '}'
      + '@media print {'
      + '  #gioco-esci-btn { display: none !important; }'
      + '}';
    document.head.appendChild(stile);
    document.body.appendChild(btn);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', aggiungiPulsanteEsciGioco);
  } else {
    aggiungiPulsanteEsciGioco();
  }

  global.GiochiUtil = {
    qs: qs,
    qsa: qsa,
    crea: crea,
    shuffle: shuffle,
    preferscRidotto: preferscRidotto,
    annuncia: annuncia,
    creaPulsanteVolume: creaPulsanteVolume,
    pannelloFineGioco: pannelloFineGioco,
    badgeMigliorRisultato: badgeMigliorRisultato,
    salvaEMostraAttestato: salvaEMostraAttestato,
    aggiungiPulsanteEsciGioco: aggiungiPulsanteEsciGioco
  };
})(typeof window !== 'undefined' ? window : this);
