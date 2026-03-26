---
title: "Crea il tuo Piano di Emergenza Familiare"
description: "Crea e stampa il tuo piano di emergenza familiare personalizzato. Tutti i dati restano solo sul tuo computer."
layout: "single"
---

La sicurezza parte da te e dalla tua famiglia. Dedica pochi minuti a compilare questo modulo. Lo strumento generera un piano personalizzato che potrai stampare e conservare in un luogo sicuro. **Tutti i dati inseriti restano solo sul tuo computer.**

<div class="card shadow-sm p-4 mb-4">

### 1. La mia Famiglia

<div class="row g-3 mb-3">
<div class="col-md-6">
<label for="adulti" class="form-label">Numero Adulti</label>
<input type="number" class="form-control" id="adulti" min="0" value="2">
</div>
<div class="col-md-6">
<label for="bambini" class="form-label">Numero Bambini / Ragazzi</label>
<input type="number" class="form-control" id="bambini" min="0" value="0">
</div>
<div class="col-md-6">
<label for="anziani" class="form-label">Numero Anziani o persone con necessita speciali</label>
<input type="number" class="form-control" id="anziani" min="0" value="0">
</div>
<div class="col-md-6">
<label for="animali" class="form-label">Animali domestici (tipo e numero)</label>
<input type="text" class="form-control" id="animali" placeholder="Es. 1 cane, 2 gatti">
</div>
</div>

### 2. I nostri Punti di Ritrovo

<div class="row g-3 mb-3">
<div class="col-md-6">
<label for="ritrovo-vicino" class="form-label">Punto di ritrovo sicuro VICINO casa</label>
<input type="text" class="form-control" id="ritrovo-vicino" placeholder="Es. Piazza del Comune">
</div>
<div class="col-md-6">
<label for="ritrovo-lontano" class="form-label">Punto di ritrovo sicuro LONTANO da casa</label>
<input type="text" class="form-control" id="ritrovo-lontano" placeholder="Es. Casa dei nonni a...">
</div>
</div>

### 3. Contatti e Risorse

<div class="row g-3 mb-3">
<div class="col-md-6">
<label for="contatto-fuori" class="form-label">Contatto di riferimento fuori citta (Nome e Telefono)</label>
<input type="text" class="form-control" id="contatto-fuori" placeholder="Es. Zio Mario - 333 1234567">
</div>
<div class="col-md-6">
<label for="kit-emergenza" class="form-label">Dove si trova il Kit di emergenza?</label>
<input type="text" class="form-control" id="kit-emergenza" placeholder="Es. Armadio ingresso">
</div>
</div>

<button type="button" class="btn btn-primary btn-lg" onclick="generaPiano()">Crea il mio Piano</button>
</div>

<div id="piano-output" class="d-none">
<div class="card shadow p-4 mb-4" id="piano-stampabile">
<h2 class="text-center mb-4">Piano di Emergenza Familiare</h2>
<p class="text-center text-muted">Protezione Civile Genzano di Roma — Gruppo Comunale Volontari</p>
<hr>
<div id="piano-contenuto"></div>
<hr>
<p class="small text-muted text-center">Documento generato il <span id="data-piano"></span> — Conservare in un luogo accessibile a tutti i familiari.<br>
Numeri di Emergenza: <strong>112</strong> (NUE) — <strong>115</strong> (VVF) — <strong>118</strong> (Sanitaria) — <strong>1515</strong> (Incendi boschivi)</p>
</div>
<button type="button" class="btn btn-success btn-lg me-2" onclick="window.print()">Stampa il Piano</button>
</div>

<script>
function generaPiano() {
  var adulti = document.getElementById('adulti').value;
  var bambini = document.getElementById('bambini').value;
  var anziani = document.getElementById('anziani').value;
  var animali = document.getElementById('animali').value || 'Nessuno';
  var vicino = document.getElementById('ritrovo-vicino').value || 'Non indicato';
  var lontano = document.getElementById('ritrovo-lontano').value || 'Non indicato';
  var contatto = document.getElementById('contatto-fuori').value || 'Non indicato';
  var kit = document.getElementById('kit-emergenza').value || 'Non indicato';
  var html = '<h3>La nostra Famiglia</h3>';
  html += '<p>Adulti: <strong>' + adulti + '</strong> — Bambini/Ragazzi: <strong>' + bambini + '</strong> — Anziani/Necessita speciali: <strong>' + anziani + '</strong></p>';
  html += '<p>Animali domestici: <strong>' + animali + '</strong></p>';
  html += '<h3>Punti di Ritrovo</h3>';
  html += '<p>Vicino casa: <strong>' + vicino + '</strong></p>';
  html += '<p>Lontano da casa: <strong>' + lontano + '</strong></p>';
  html += '<h3>Contatti e Risorse</h3>';
  html += '<p>Riferimento fuori citta: <strong>' + contatto + '</strong></p>';
  html += '<p>Kit di emergenza: <strong>' + kit + '</strong></p>';
  document.getElementById('piano-contenuto').innerHTML = html;
  document.getElementById('data-piano').textContent = new Date().toLocaleDateString('it-IT');
  document.getElementById('piano-output').classList.remove('d-none');
  document.getElementById('piano-output').scrollIntoView({behavior: 'smooth'});
}
</script>
