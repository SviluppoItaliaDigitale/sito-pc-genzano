/* Suoni dei giochi — Protezione Civile Genzano
   Caricato da site-chrome.js in ogni gioco di /giochi/. Aggiunge:
   - il pulsante «Suoni» accanto a «Schermo intero» e «Torna al menu»
     (acceso o spento, scelta salvata nel browser);
   - nei giochi che non hanno suoni propri, un «ding» alla risposta giusta e un
     tono neutro a quella sbagliata, letti dalle classi che il gioco già mette
     sulle risposte (correct/wrong, giusto/sbagliato, corretto/errato; non ok/ko,
     che molti giochi usano per riquadri e cronologie);
   - in tutti i giochi, una breve musica a fine partita, quando il gioco salva il
     risultato (GiochiPC.salvaRisultato).
   Il suono accompagna e non sostituisce mai le scritte del gioco.
   Sintassi ES5 (regola LIM: browser delle lavagne fino a Chrome 64). */

(function (global) {
  'use strict';

  var GIUSTE = ['correct', 'giusto', 'corretto', 'is-correct'];
  var SBAGLIATE = ['wrong', 'sbagliato', 'errato', 'is-wrong'];
  var VOLUME_ACCESO = 0.6;

  function A() { return global.AudioSintetico; }

  function ha(el, nomi) {
    if (!el || !el.classList) return false;
    for (var i = 0; i < nomi.length; i++) { if (el.classList.contains(nomi[i])) return true; }
    return false;
  }
  function aveva(vecchie, nomi) {
    var parti = (' ' + (vecchie || '') + ' ');
    for (var i = 0; i < nomi.length; i++) { if (parti.indexOf(' ' + nomi[i] + ' ') !== -1) return true; }
    return false;
  }

  // ---- Pulsante «Suoni» -----------------------------------------------------
  function pulsante() {
    var comandi = document.getElementById('gioco-comandi');
    if (!comandi || document.getElementById('gioco-suoni-btn') || !A()) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.id = 'gioco-suoni-btn';
    // Nome fisso (sul telefono la scritta si nasconde); lo stato lo dice aria-pressed.
    b.setAttribute('aria-label', 'Suoni');
    function aggiorna() {
      var on = A().getVolume() > 0;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.innerHTML = '<i class="bi ' + (on ? 'bi-volume-up-fill' : 'bi-volume-mute-fill') + '" aria-hidden="true"></i>'
        + '<span class="gioco-esci-label">Suoni</span>';
      b.title = on ? 'Suoni accesi: tocca per spegnerli' : 'Suoni spenti: tocca per accenderli';
    }
    b.addEventListener('click', function () {
      var on = A().getVolume() > 0;
      A().setVolume(on ? 0 : VOLUME_ACCESO);
      if (on && A().ferma) A().ferma();
      aggiorna();
      if (!on) A().dingPositivo();
    });
    aggiorna();
    comandi.insertBefore(b, comandi.firstChild);
    // Lo stile viene dalla barra del gioco (site-chrome.js, #gioco-comandi).
  }

  // ---- Fine partita -----------------------------------------------------------
  function fine() {
    var pc = global.GiochiPC;
    if (!pc || !pc.salvaRisultato || pc.__suoni) return;
    var originale = pc.salvaRisultato;
    pc.salvaRisultato = function (id, punteggio, max) {
      var esito = originale.apply(this, arguments);
      try {
        var perc = max ? Math.round(100 * punteggio / max) : undefined;
        if (A() && A().fineGioco) setTimeout(function () { A().fineGioco(perc); }, 350);
      } catch (e) { /* noop */ }
      return esito;
    };
    pc.__suoni = true;
  }

  // ---- Risposte giuste e sbagliate (solo giochi senza suoni propri) ----------
  var ultimo = 0;
  function suona(giusta) {
    var ora = Date.now();
    if (ora - ultimo < 600) return;
    ultimo = ora;
    if (giusta) A().dingPositivo(); else A().tonoNeutro();
  }

  function osserva() {
    if (!global.MutationObserver) return;
    var area = document.querySelector('main') || document.body;
    var obs = new MutationObserver(function (lista) {
      var g = 0, s = 0;
      for (var i = 0; i < lista.length; i++) {
        var m = lista[i];
        if (m.type === 'attributes') {
          var el = m.target;
          if (el.id === 'gioco-comandi' || (el.closest && el.closest('#gioco-comandi, .coach-dialog, .gioco-coach'))) continue;
          if (ha(el, GIUSTE) && !aveva(m.oldValue, GIUSTE)) g++;
          else if (ha(el, SBAGLIATE) && !aveva(m.oldValue, SBAGLIATE)) s++;
        } else {
          for (var j = 0; j < m.addedNodes.length; j++) {
            var n = m.addedNodes[j];
            if (n.nodeType !== 1) continue;
            if (ha(n, GIUSTE)) g++; else if (ha(n, SBAGLIATE)) s++;
          }
        }
      }
      // Molte risposte colorate tutte insieme sono un riepilogo o la soluzione
      // mostrata: niente suono.
      if (g + s === 0 || g + s > 3) return;
      if (g && !s) suona(true);
      else if (s && !g) suona(false);
      else suona(false);
    });
    obs.observe(area, { subtree: true, childList: true, attributes: true, attributeFilter: ['class'], attributeOldValue: true });
  }

  function avvia(suoniPropri) {
    pulsante();
    fine();
    if (!suoniPropri) osserva();
  }

  // Chiamato da site-chrome.js; `suoniPropri` dice se il gioco suona già da sé.
  global.SuoniGioco = { avvia: avvia };
})(typeof window !== 'undefined' ? window : this);
