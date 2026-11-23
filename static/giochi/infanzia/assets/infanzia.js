/* Giochi dell'infanzia: porta in vista la risposta di Tina dopo una scelta.
   Sul telefono il messaggio cade spesso sotto le scelte, dietro la barra in basso
   e il pulsante SOS 112 del sito (circa 200 px): si scorre quel tanto che basta.
   La misura si prende un attimo dopo, quando il riquadro dei consigli (coach.js)
   che compare con la risposta sbagliata ha gia' spostato la pagina.
   ECMAScript 5, come chiede la regola delle LIM. */
(function () {
  'use strict';
  window.InfInVista = function (el) {
    if (!el || !el.getBoundingClientRect) return;
    window.setTimeout(function () {
      var libero = window.innerWidth < 992 ? 200 : 20;
      var sotto = el.getBoundingClientRect().bottom - (window.innerHeight - libero);
      if (sotto > 0) window.scrollBy(0, sotto);
    }, 80);
  };
})();
