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
var searchIndex = null;
var searchInput = document.getElementById('search-input');
var searchResults = document.getElementById('search-results');

fetch(document.baseURI.replace(/cerca\/$/, '') + 'index.json')
  .then(function(r) { return r.json(); })
  .then(function(data) { searchIndex = data; });

searchInput.addEventListener('input', function() {
  var query = this.value.toLowerCase().trim();
  if (query.length < 3) {
    searchResults.innerHTML = '';
    return;
  }
  if (!searchIndex) {
    searchResults.innerHTML = '<p>Caricamento indice di ricerca...</p>';
    return;
  }
  var results = searchIndex.filter(function(page) {
    return page.title.toLowerCase().indexOf(query) !== -1 || page.content.toLowerCase().indexOf(query) !== -1;
  });
  if (results.length === 0) {
    searchResults.innerHTML = '<p class="text-muted">Nessun risultato trovato per "<strong>' + query + '</strong>".</p>';
    return;
  }
  var html = '<p class="fw-bold">' + results.length + ' risultat' + (results.length === 1 ? 'o' : 'i') + ' per "' + query + '":</p>';
  results.forEach(function(r) {
    html += '<div class="search-result-item"><h3 class="h5"><a href="' + r.url + '">' + r.title + '</a></h3><p class="small text-muted">' + r.content + '</p></div>';
  });
  searchResults.innerHTML = html;
});
</script>
