/* ============================================================
   PC-NOTIFICHE v1.0 — toast di conferma (componente Notifiche
   di Bootstrap Italia, classi .notification del bundle).
   Espone window.pcNotifica(titolo, testo, tipo) per conferme
   in-page delle azioni: es. "Piano salvato sul dispositivo",
   "Notifiche di allerta attivate".
   - role="alert": annunciata dagli screen reader;
   - chiusura con bottone, tasto ESC o auto-dismiss dopo 8s;
   - una sola notifica alla volta (la nuova sostituisce la vecchia);
   - nessuna animazione (niente impatti prefers-reduced-motion).
   ============================================================ */
(function () {
  'use strict';

  var TIPI = {
    success: { classe: 'success', icona: 'bi-check-circle' },
    warning: { classe: 'warning', icona: 'bi-exclamation-triangle' },
    error:   { classe: 'error',   icona: 'bi-x-circle' },
    info:    { classe: 'info',    icona: 'bi-info-circle' }
  };
  var timer = null;

  function chiudi() {
    var n = document.getElementById('pc-toast');
    if (n) n.remove();
    if (timer) { clearTimeout(timer); timer = null; }
    document.removeEventListener('keydown', suEsc);
  }

  function suEsc(e) { if (e.key === 'Escape') chiudi(); }

  function pcNotifica(titolo, testo, tipo) {
    chiudi();
    var t = TIPI[tipo] || TIPI.success;
    var n = document.createElement('div');
    n.id = 'pc-toast';
    n.className = 'notification with-icon dismissable pc-toast-visibile ' + t.classe;
    n.setAttribute('role', 'alert');

    var h = document.createElement('p');
    h.className = 'h5';
    var ic = document.createElement('i');
    ic.className = 'bi ' + t.icona + ' me-2';
    ic.setAttribute('aria-hidden', 'true');
    h.appendChild(ic);
    h.appendChild(document.createTextNode(titolo));
    n.appendChild(h);

    if (testo) {
      var p = document.createElement('p');
      p.textContent = testo;
      n.appendChild(p);
    }

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pc-toast-chiudi';
    btn.setAttribute('aria-label', 'Chiudi la notifica');
    btn.innerHTML = '<i class="bi bi-x-lg" aria-hidden="true"></i>';
    btn.addEventListener('click', chiudi);
    n.appendChild(btn);

    document.body.appendChild(n);
    document.addEventListener('keydown', suEsc);
    timer = setTimeout(chiudi, 8000);
  }

  window.pcNotifica = pcNotifica;
})();
