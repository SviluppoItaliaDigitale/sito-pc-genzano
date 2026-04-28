/* Attestato inclusivo — versione senza soglia di punteggio.
   Pensato per i giochi /abili-a-proteggere/* (persone con disabilità
   cognitive, anziani, parlanti L2): chi partecipa, ottiene l'attestato.

   Comportamento:
   - Osserva quando una "schermata di fine" diventa visibile e vi
     inietta dentro un riquadro verde con: titolo, input nome,
     bottone Scarica e bottone Stampa.
   - Selettori cercati (in ordine): #end-screen, #card-screen,
     #results-screen, #esito, #end, .schermata-fine, .gioco-fine,
     [data-fine].
   - Nessun bottone "Ho finito" fluttuante durante il gioco: il riquadro
     compare solo quando si entra nella schermata fine, condizione
     semantica corretta. Tutti i 53 giochi del sito hanno una schermata
     fine fra i selettori monitorati (verificato).
   - Riusa AttestatoPC.genera/stampa (script: attestato.js) per produrre
     il file SVG istituzionale identico agli altri giochi.

   Inclusione minima nell'HTML del gioco:
     <script src="/giochi/assets/js/attestato.js"></script>
     <script src="/giochi/assets/js/attestato-inclusivo.js"></script>
*/

(function (global) {
  'use strict';

  if (!global.document) return;

  var SELETTORI_FINE = [
    '#end-screen',
    '#card-screen',
    '#results-screen',
    '#esito',
    '#end',
    '.schermata-fine',
    '.gioco-fine',
    '[data-fine]'
  ];

  var iniettato = false;

  function idGiocoDaUrl() {
    // /abili-a-proteggere/chiama-112/ -> chiama-112
    // /giochi/infanzia/tartaruga-saggia/ -> tartaruga-saggia
    var path = (location.pathname || '').replace(/\/index\.html?$/i, '').replace(/\/+$/, '');
    var parts = path.split('/').filter(Boolean);
    return parts[parts.length - 1] || 'gioco';
  }

  function nomeGiocoDaPagina() {
    var h1 = document.querySelector('h1');
    if (h1 && h1.textContent) return h1.textContent.trim();
    if (document.title) return document.title.split('—')[0].trim();
    return 'Gioco della Sicurezza';
  }

  function elementoVisibile(el) {
    if (!el) return false;
    if (el.classList && el.classList.contains('hide')) return false;
    if (el.hidden) return false;
    var st = global.getComputedStyle ? global.getComputedStyle(el) : null;
    if (st && (st.display === 'none' || st.visibility === 'hidden')) return false;
    return el.offsetParent !== null || el.getClientRects().length > 0;
  }

  function trovaSchermataFine() {
    for (var i = 0; i < SELETTORI_FINE.length; i++) {
      var el = document.querySelector(SELETTORI_FINE[i]);
      if (el && elementoVisibile(el)) return el;
    }
    return null;
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[<>&'"]/g, function (c) {
      return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '\'': '&#39;', '"': '&quot;' }[c];
    });
  }

  function costruisciBox(idGioco, nomeGioco) {
    var box = document.createElement('div');
    box.className = 'attestato-inclusivo-box';
    box.setAttribute('role', 'region');
    box.setAttribute('aria-label', 'Attestato di partecipazione');
    box.style.cssText = ''
      + 'background:#e7f5ec;'
      + 'border:2px solid #198754;'
      + 'border-radius:14px;'
      + 'padding:1.1rem 1.2rem;'
      + 'margin:1.2rem auto 0 auto;'
      + 'max-width:560px;'
      + 'text-align:center;'
      + 'font-size:1.05rem;'
      + 'line-height:1.5;';

    box.innerHTML = ''
      + '<p style="margin:0 0 0.6rem 0;font-size:1.15rem;font-weight:700;color:#0f5132;">'
      + '<span aria-hidden="true" style="font-size:1.6rem;">🏅</span>'
      + ' Hai partecipato! Vuoi il tuo attestato?'
      + '</p>'
      + '<p style="margin:0 0 0.8rem 0;color:#1f5235;">'
      + 'Scrivi il tuo nome e premi <strong>Scarica</strong> o <strong>Stampa</strong>.'
      + '</p>'
      + '<label for="attestato-incl-nome" class="form-label" style="font-weight:600;">Il tuo nome</label>'
      + '<input id="attestato-incl-nome" type="text" maxlength="40" autocomplete="name" '
      + '       placeholder="Scrivi qui il tuo nome" '
      + '       style="width:100%;max-width:360px;padding:0.6rem 0.8rem;font-size:1.1rem;'
      + '              border:2px solid #198754;border-radius:8px;margin-bottom:0.8rem;">'
      + '<div style="display:flex;flex-wrap:wrap;gap:0.6rem;justify-content:center;">'
      + '  <button type="button" data-azione="scarica" '
      + '          style="background:#198754;color:#fff;border:0;border-radius:8px;'
      + '                 padding:0.7rem 1.4rem;font-size:1.05rem;font-weight:600;cursor:pointer;'
      + '                 min-height:48px;min-width:140px;">'
      + '    <span aria-hidden="true">⬇</span> Scarica'
      + '  </button>'
      + '  <button type="button" data-azione="stampa" '
      + '          style="background:#fff;color:#198754;border:2px solid #198754;border-radius:8px;'
      + '                 padding:0.7rem 1.4rem;font-size:1.05rem;font-weight:600;cursor:pointer;'
      + '                 min-height:48px;min-width:140px;">'
      + '    <span aria-hidden="true">🖨</span> Stampa'
      + '  </button>'
      + '</div>'
      + '<p id="attestato-incl-msg" style="margin:0.6rem 0 0 0;font-size:0.9rem;color:#0f5132;" '
      + '   role="status" aria-live="polite"></p>';

    function leggiNome() {
      var inp = box.querySelector('#attestato-incl-nome');
      return (inp && inp.value || '').trim();
    }

    function feedback(testo) {
      var p = box.querySelector('#attestato-incl-msg');
      if (p) p.textContent = testo;
    }

    box.querySelector('[data-azione="scarica"]').addEventListener('click', function () {
      var nome = leggiNome();
      if (!nome) { feedback('Per favore scrivi prima il tuo nome.'); return; }
      if (global.AttestatoPC) {
        // tipo "incluso": giochi senza scoring, l'SVG mostra "ha partecipato"
        // + "Grazie per aver giocato con noi", senza percentuale.
        global.AttestatoPC.genera(nome, idGioco, 100, 'incluso');
        feedback('Attestato scaricato! Trovi il file nella cartella Download.');
      } else {
        feedback('Non posso creare l’attestato in questo momento.');
      }
    });

    box.querySelector('[data-azione="stampa"]').addEventListener('click', function () {
      var nome = leggiNome();
      if (!nome) { feedback('Per favore scrivi prima il tuo nome.'); return; }
      if (global.AttestatoPC) {
        global.AttestatoPC.stampa(nome, idGioco, 100, 'incluso');
        feedback('Si apre la finestra di stampa.');
      } else {
        feedback('Non posso aprire la stampa in questo momento.');
      }
    });

    return box;
  }

  function inietta(target) {
    if (iniettato) return;
    if (!target) return;
    if (target.querySelector && target.querySelector('.attestato-inclusivo-box')) {
      iniettato = true;
      return;
    }
    var idGioco = idGiocoDaUrl();
    var nome = nomeGiocoDaPagina();
    var box = costruisciBox(idGioco, nome);
    // Se la schermata fine ha già bottoni "Rifai/Torna", inserisco prima di
    // quelli — l'attestato ha la priorità visiva
    var bottoni = target.querySelector('.d-flex.flex-wrap.justify-content-center')
                  || target.querySelector('.azioni-fine');
    if (bottoni && bottoni.parentNode === target) {
      target.insertBefore(box, bottoni);
    } else {
      target.appendChild(box);
    }
    iniettato = true;
  }

  function avvia() {
    // Se la schermata fine è già visibile al momento del load (es. se l'utente
    // ricarica la pagina dopo aver finito), inietta subito.
    var subito = trovaSchermataFine();
    if (subito) inietta(subito);

    // Osservatore: monitora il body e le sue mutazioni (cambio di classi
    // hide / display:none) e prova a iniettare quando la schermata fine
    // diventa visibile.
    if (global.MutationObserver) {
      var mo = new MutationObserver(function () {
        if (iniettato) { mo.disconnect(); return; }
        var t = trovaSchermataFine();
        if (t) inietta(t);
      });
      mo.observe(document.body, {
        attributes: true,
        attributeFilter: ['class', 'style', 'hidden'],
        subtree: true,
        childList: true
      });
    }

    // Niente piu' fallback FAB: la presenza di un bottone "Ho finito"
    // fluttuante durante il gioco era percepita come invadente, perche'
    // appariva dopo 20s anche se il gioco era ancora in corso.
    // L'attestato compare ora SOLO quando il MutationObserver rileva
    // che e' diventata visibile una schermata di fine: e' la condizione
    // semantica giusta. Tutti i 53 giochi del sito (verificati) hanno
    // una schermata fine fra i selettori monitorati.
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', avvia);
  } else {
    avvia();
  }
})(typeof window !== 'undefined' ? window : this);
