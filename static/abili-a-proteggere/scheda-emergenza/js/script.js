/* La Mia Scheda di Emergenza — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  var formScreen = document.getElementById('form-screen');
  var cardScreen = document.getElementById('card-screen');
  var form = document.getElementById('emergency-form');

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }

  function val(id) {
    var v = document.getElementById(id).value.trim();
    return v || '—';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Fill the card
    document.getElementById('card-nome').textContent = val('nome');
    document.getElementById('card-indirizzo').textContent = val('indirizzo');
    document.getElementById('card-allergie').textContent = val('allergie');
    document.getElementById('card-c1-nome').textContent = val('contatto1-nome');
    document.getElementById('card-c1-tel').textContent = val('contatto1-tel');
    document.getElementById('card-c2-nome').textContent = val('contatto2-nome');
    document.getElementById('card-c2-tel').textContent = val('contatto2-tel');
    document.getElementById('card-punto').textContent = val('punto-incontro');

    hide(formScreen);
    show(cardScreen);
    window.scrollTo(0, 0);
  });

  // Print
  document.getElementById('print-btn').addEventListener('click', function () {
    window.print();
  });

  // Edit
  document.getElementById('edit-btn').addEventListener('click', function () {
    hide(cardScreen);
    show(formScreen);
    window.scrollTo(0, 0);
  });
})();
