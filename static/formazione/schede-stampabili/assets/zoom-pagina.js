/* Zoom della pagina per storie e libri pop-up (01/11/2026): nella barra in alto i pulsanti «−», «+» e
   «↺ Ripristina» ingrandiscono la pagina; ci si sposta scorrendo con un dito, col mouse o con le frecce.
   Servono dove il pizzico non c'è (lavagne a un solo tocco, mouse) e non toccano la stampa.
   JavaScript entro ECMAScript 5: deve partire anche sui browser delle LIM più vecchie (regola lim-scuole.md). */
(function () {
  'use strict';
  var barra = document.querySelector('.storia-toolbar, .scheda-toolbar');
  var pagine = document.querySelectorAll('.storia-page, .scheda-page');
  if (!barra || !pagine.length || barra.querySelector('.zp')) return;

  var PASSI = [1, 1.25, 1.5, 1.75, 2, 2.5, 3];
  var passo = 0;
  var html = document.documentElement;
  // Firefox ha la proprietà zoom solo dalla versione 126: prima si scala con transform.
  var conZoom = 'zoom' in html.style;

  var stile = document.createElement('style');
  // Lo zoom vale solo a schermo (@media screen): la stampa resta quella di sempre, con la sua scala
  // per pagina (le storie e le schede hanno uno zoom di stampa tarato sui fogli).
  var SEL = '.storia-page,.scheda-page';
  stile.textContent =
    '.zp{display:inline-flex;align-items:center;gap:4px;flex-wrap:nowrap}' +
    '.zp button{min-width:44px;min-height:44px;font-size:1.05rem;line-height:1;padding:0 .7rem;cursor:pointer}' +
    '.zp button[disabled]{opacity:.45;cursor:not-allowed}' +
    '.zp-valore{min-width:3.4em;text-align:center;font-weight:700;font-size:.9rem}' +
    '@media print{.zp{display:none!important}}' +
    '@media screen{' +
    'html.zp-on:not(.zp-tr) ' + SEL.replace(',', ',html.zp-on:not(.zp-tr) ') + '{zoom:var(--zp)}' +
    'html.zp-on.zp-tr ' + SEL.replace(',', ',html.zp-on.zp-tr ') +
    '{transform:scale(var(--zp));transform-origin:0 0;margin-right:var(--zp-mr);margin-bottom:var(--zp-mb)}}';
  document.head.appendChild(stile);

  var gruppo = document.createElement('span');
  gruppo.className = 'zp no-print';
  gruppo.setAttribute('role', 'group');
  gruppo.setAttribute('aria-label', 'Grandezza della pagina');
  gruppo.innerHTML =
    '<button type="button" data-zp="-1" aria-label="Riduci la pagina">−</button>' +
    '<span class="zp-valore" aria-live="polite">100%</span>' +
    '<button type="button" data-zp="1" aria-label="Ingrandisci la pagina">+</button>' +
    '<button type="button" data-zp="0"><span aria-hidden="true">↺</span> Ripristina</button>';
  // Prima del pulsante di stampa, che resta l'ultimo della barra.
  var stampa = barra.querySelector('button[onclick*="print"]');
  if (stampa) barra.insertBefore(gruppo, stampa); else barra.appendChild(gruppo);

  var valore = gruppo.querySelector('.zp-valore');
  var meno = gruppo.querySelector('[data-zp="-1"]');
  var piu = gruppo.querySelector('[data-zp="1"]');
  var reset = gruppo.querySelector('[data-zp="0"]');

  function applica(nuovo) {
    var vecchio = PASSI[passo];
    passo = Math.max(0, Math.min(PASSI.length - 1, nuovo));
    var z = PASSI[passo];
    // Il punto letto resta più o meno lo stesso: lo scorrimento cresce in proporzione.
    var x = window.pageXOffset * z / vecchio, y = window.pageYOffset * z / vecchio;
    html.style.setProperty('--zp', String(z));
    html.classList.toggle('zp-on', z !== 1);
    html.classList.toggle('zp-tr', !conZoom);
    if (!conZoom) {
      // Senza zoom CSS (Firefox prima della 126) si scala con transform: i margini lasciano lo spazio
      // che la pagina ingrandita occupa, altrimenti lo scorrimento non ci arriverebbe.
      for (var i = 0; i < pagine.length; i++) {
        var p = pagine[i];
        p.style.setProperty('--zp-mr', (p.offsetWidth * (z - 1)) + 'px');
        p.style.setProperty('--zp-mb', (p.offsetHeight * (z - 1)) + 'px');
      }
    }
    valore.textContent = Math.round(z * 100) + '%';
    meno.disabled = passo === 0;
    piu.disabled = passo === PASSI.length - 1;
    reset.disabled = passo === 0;
    window.scrollTo(x, y);
  }

  gruppo.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('button') : null;
    if (!b || b.disabled) return;
    var d = +b.getAttribute('data-zp');
    applica(d === 0 ? 0 : passo + d);
  });
  applica(0);
})();
