---
title: "Cerca nel sito"
description: "Cerca informazioni nel sito della Protezione Civile di Genzano di Roma."
layout: "single"
---

<div id="search-container">
<label for="search-input" class="form-label fw-bold">Cosa stai cercando?</label>
<input type="search" id="search-input" class="form-control form-control-lg" placeholder="Digita qui per cercare..." aria-describedby="search-help">
<small id="search-help" class="form-text">Inserisci almeno 3 caratteri per avviare la ricerca.</small>
<div id="search-results" class="mt-4" role="region" aria-live="polite" aria-label="Risultati della ricerca"></div>
</div>

<script>
(function(){
  var searchIndex = null;
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');

  // Costruisci URL del JSON dal pathname corrente
  var path = window.location.pathname;
  var basePath = path.substring(0, path.indexOf('/cerca'));
  var jsonURL = window.location.origin + basePath + '/index.json';

  fetch(jsonURL)
    .then(function(r) { return r.json(); })
    .then(function(data) { searchIndex = data; })
    .catch(function(err) { console.log('Errore:', err, 'URL:', jsonURL); });

  input.addEventListener('input', function() {
    var query = this.value.toLowerCase().trim();
    if (query.length < 3) { results.innerHTML = ''; return; }
    if (!searchIndex) {
      results.innerHTML = '<p class="text-muted">Caricamento in corso...</p>';
      return;
    }
    var found = searchIndex.filter(function(p) {
      return (p.title && p.title.toLowerCase().indexOf(query) !== -1) ||
             (p.content && p.content.toLowerCase().indexOf(query) !== -1);
    });
    if (found.length === 0) {
      results.innerHTML = '<p class="text-muted">Nessun risultato per "<strong>' + query + '</strong>".</p>';
      return;
    }
    var html = '<p class="fw-bold">' + found.length + ' risultat' + (found.length === 1 ? 'o' : 'i') + ':</p>';
    found.forEach(function(r) {
      html += '<div class="search-result-item"><h3 class="h5"><a href="' + r.url + '">' + r.title + '</a></h3><p class="small text-muted">' + (r.content || '') + '</p></div>';
    });
    results.innerHTML = html;
  });
})();
</script>
