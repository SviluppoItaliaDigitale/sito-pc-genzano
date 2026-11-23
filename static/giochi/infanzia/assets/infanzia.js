/* Giochi dell'infanzia: porta in vista la risposta di Tina dopo una scelta.
   Sul telefono il messaggio cade spesso sotto le scelte, dietro la barra in basso
   e il pulsante SOS 112 del sito (circa 170 px): si scorre quel tanto che basta.
   ECMAScript 5, come chiede la regola delle LIM. */
(function () {
  'use strict';
  window.InfInVista = function (el) {
    if (!el || !el.getBoundingClientRect) return;
    var libero = window.innerWidth < 992 ? 170 : 20;
    var sotto = el.getBoundingClientRect().bottom - (window.innerHeight - libero);
    if (sotto > 0) window.scrollBy(0, sotto);
  };
})();
