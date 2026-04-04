---
title: "Crea il tuo Piano di Emergenza Familiare"
description: "Crea e stampa il tuo piano di emergenza familiare personalizzato. Tutti i dati restano solo sul tuo computer."
layout: "single"
aliases:
  - /pianofamiliare.html
  - /pianofamiliare/
---

La sicurezza parte da te e dalla tua famiglia. Dedica pochi minuti a compilare questo modulo: lo strumento genererà un piano personalizzato che potrai stampare e conservare in un luogo sicuro. **Tutti i dati inseriti restano solo sul tuo computer** — non vengono inviati né salvati da nessuna parte.

## Perché serve un Piano Familiare

Durante un'emergenza non c'è tempo per organizzarsi. Se la tua famiglia ha già discusso e concordato cosa fare, dove trovarsi e chi contattare, ognuno saprà come comportarsi anche se non siete insieme in quel momento.

Un piano familiare efficace risponde a tre domande:

1. **Dove ci troviamo?** — I punti di ritrovo concordati
2. **Chi chiamiamo?** — Il contatto di riferimento fuori città
3. **Cosa portiamo?** — Dove si trova il kit di emergenza

## Compila il tuo Piano

<div class="card shadow-sm p-4 mb-4">

### 1. La mia Famiglia

<div class="row g-3 mb-3">
<div class="col-md-6">
<label for="cognome" class="form-label">Cognome della famiglia</label>
<input type="text" class="form-control" id="cognome" placeholder="Es. Rossi">
</div>
<div class="col-md-6">
<label for="indirizzo" class="form-label">Indirizzo di casa</label>
<input type="text" class="form-control" id="indirizzo" placeholder="Es. Via Roma, 10">
</div>
<div class="col-md-3">
<label for="adulti" class="form-label">Adulti</label>
<input type="number" class="form-control" id="adulti" min="0" value="2">
</div>
<div class="col-md-3">
<label for="bambini" class="form-label">Bambini / Ragazzi</label>
<input type="number" class="form-control" id="bambini" min="0" value="0">
</div>
<div class="col-md-3">
<label for="anziani" class="form-label">Anziani o persone fragili</label>
<input type="number" class="form-control" id="anziani" min="0" value="0">
</div>
<div class="col-md-3">
<label for="animali" class="form-label">Animali domestici</label>
<input type="text" class="form-control" id="animali" placeholder="Es. 1 cane, 2 gatti">
</div>
</div>

### 2. I nostri Punti di Ritrovo

<div class="row g-3 mb-3">
<div class="col-md-6">
<label for="ritrovo-vicino" class="form-label">Punto di ritrovo VICINO casa</label>
<input type="text" class="form-control" id="ritrovo-vicino" placeholder="Es. Piazza Frasconi (AA1)">
<small class="text-muted">Consulta le <a href="/cartografia/">aree di attesa</a> più vicine</small>
</div>
<div class="col-md-6">
<label for="ritrovo-lontano" class="form-label">Punto di ritrovo LONTANO da casa</label>
<input type="text" class="form-control" id="ritrovo-lontano" placeholder="Es. Casa dei nonni a...">
</div>
</div>

### 3. Contatti e Risorse

<div class="row g-3 mb-3">
<div class="col-md-6">
<label for="contatto-fuori" class="form-label">Contatto di riferimento fuori città</label>
<input type="text" class="form-control" id="contatto-fuori" placeholder="Es. Zio Mario — 333 1234567">
</div>
<div class="col-md-6">
<label for="medico" class="form-label">Medico di famiglia (nome e telefono)</label>
<input type="text" class="form-control" id="medico" placeholder="Es. Dott. Bianchi — 06 123456">
</div>
<div class="col-md-6">
<label for="kit-emergenza" class="form-label">Dove si trova il Kit di emergenza?</label>
<input type="text" class="form-control" id="kit-emergenza" placeholder="Es. Armadio ingresso">
</div>
<div class="col-md-6">
<label for="chiusure" class="form-label">Dove sono i rubinetti gas/acqua e quadro elettrico?</label>
<input type="text" class="form-control" id="chiusure" placeholder="Es. Gas: cucina; Quadro: ingresso">
</div>
</div>

### 4. Esigenze specifiche (opzionale)

<div class="row g-3 mb-3">
<div class="col-md-6">
<label for="farmaci" class="form-label">Farmaci indispensabili</label>
<input type="text" class="form-control" id="farmaci" placeholder="Es. Insulina, antipertensivo...">
</div>
<div class="col-md-6">
<label for="ausili" class="form-label">Ausili o necessità particolari</label>
<input type="text" class="form-control" id="ausili" placeholder="Es. Sedia a rotelle, bombola O2...">
</div>
<div class="col-12">
<label for="note" class="form-label">Note aggiuntive</label>
<textarea class="form-control" id="note" rows="2" placeholder="Es. Bambino allergico alle arachidi; gatto che si spaventa..."></textarea>
</div>
</div>

<button type="button" class="btn btn-primary btn-lg" onclick="generaPiano()">
  <i class="bi bi-file-earmark-check me-2" aria-hidden="true"></i>Crea il mio Piano
</button>
</div>

<div id="piano-output" class="d-none">
<div class="card shadow p-4 mb-4" id="piano-stampabile">
<h2 class="text-center mb-1">Piano di Emergenza Familiare</h2>
<p class="text-center text-muted mb-0">Protezione Civile Genzano di Roma — Gruppo Comunale Volontari</p>
<p class="text-center text-muted small">Documento generato il <span id="data-piano"></span></p>
<hr>
<div id="piano-contenuto"></div>
<hr>
<p class="small text-muted text-center mb-0">
Numeri di Emergenza: <strong>112</strong> (NUE) — <strong>115</strong> (VVF) — <strong>118</strong> (Sanitaria) — <strong>803 555</strong> (PC Lazio) — <strong>1515</strong> (Incendi boschivi)<br>
Conservare in un luogo accessibile a tutti i familiari. Aggiornare almeno una volta all'anno.</p>
</div>
<div class="d-flex flex-wrap gap-2 mb-4">
<button type="button" class="btn btn-success btn-lg" onclick="window.print()"><i class="bi bi-printer me-2" aria-hidden="true"></i>Stampa il Piano</button>
<button type="button" class="btn btn-outline-primary btn-lg" onclick="document.getElementById('piano-output').classList.add('d-none');window.scrollTo({top:0,behavior:'smooth'})"><i class="bi bi-pencil me-2" aria-hidden="true"></i>Modifica</button>
</div>
</div>

## Consigli per famiglie con bambini

- Spiega ai bambini cosa potrebbe succedere, con parole semplici e senza spaventarli
- Assicurati che sappiano il loro **nome completo**, **indirizzo** e almeno **un numero di telefono** da chiamare
- Insegna loro a riconoscere il suono di un allarme
- Fai delle "prove" giocando a raggiungere il punto di ritrovo
- Metti un documento identificativo nel loro zainetto

## Consigli per famiglie con anziani

- Verifica che le vie di fuga dalla casa siano accessibili e senza ostacoli
- Tieni una lista scritta dei farmaci e dei dosaggi sempre aggiornata
- Lascia una copia delle chiavi di casa a un vicino di fiducia
- Programma il telefono con i numeri di emergenza in memoria rapida
- Se la persona è sola, organizza un sistema di "chiamata giornaliera" con un familiare o un vicino

## Consigli per persone con disabilità

- Includi nel piano tutti gli ausili necessari (sedia a rotelle, apparecchi acustici, protesi)
- Se dipendi da apparecchiature elettriche, [contatta la ASL](/rischi-prevenzione/persone-necessita-specifiche/) per la lista utenze non disalimentabili
- Individua almeno due persone (vicini, amici) che possano aiutarti in caso di evacuazione
- Memorizza i percorsi di uscita accessibili dalla tua abitazione

## Consigli per gli animali domestici

- Includi nel kit cibo e acqua per almeno 3 giorni
- Tieni pronto guinzaglio, trasportino e museruola (se necessaria)
- Conserva il libretto sanitario con le vaccinazioni aggiornate
- Identifica in anticipo un luogo dove portare gli animali se la tua casa non è agibile

## Checklist finale

Verifica di aver fatto tutto:

- ☐ Compilato e stampato il Piano Familiare
- ☐ Individuato le aree di attesa più vicine a casa e al lavoro
- ☐ Preparato il [kit di emergenza](/rischi-prevenzione/kit-emergenza/)
- ☐ Concordato i punti di ritrovo con tutti i familiari
- ☐ Comunicato il piano al contatto di riferimento fuori città
- ☐ Verificato dove sono i rubinetti del gas/acqua e il quadro elettrico
- ☐ Scaricato l'app [Where ARE U](https://where.areu.lombardia.it/) per le chiamate al 112

<script>
function generaPiano() {
  var cognome = document.getElementById('cognome').value || 'Non indicato';
  var indirizzo = document.getElementById('indirizzo').value || 'Non indicato';
  var adulti = document.getElementById('adulti').value;
  var bambini = document.getElementById('bambini').value;
  var anziani = document.getElementById('anziani').value;
  var animali = document.getElementById('animali').value || 'Nessuno';
  var vicino = document.getElementById('ritrovo-vicino').value || 'Non indicato';
  var lontano = document.getElementById('ritrovo-lontano').value || 'Non indicato';
  var contatto = document.getElementById('contatto-fuori').value || 'Non indicato';
  var medico = document.getElementById('medico').value || 'Non indicato';
  var kit = document.getElementById('kit-emergenza').value || 'Non indicato';
  var chiusure = document.getElementById('chiusure').value || 'Non indicato';
  var farmaci = document.getElementById('farmaci').value || 'Nessuno';
  var ausili = document.getElementById('ausili').value || 'Nessuno';
  var note = document.getElementById('note').value || '';

  var html = '<h3>Famiglia ' + cognome + '</h3>';
  html += '<p><strong>Indirizzo:</strong> ' + indirizzo + '</p>';
  html += '<p>Adulti: <strong>' + adulti + '</strong> — Bambini/Ragazzi: <strong>' + bambini + '</strong> — Anziani/Fragili: <strong>' + anziani + '</strong></p>';
  html += '<p>Animali domestici: <strong>' + animali + '</strong></p>';

  html += '<h3>Punti di Ritrovo</h3>';
  html += '<p>Vicino casa: <strong>' + vicino + '</strong></p>';
  html += '<p>Lontano da casa: <strong>' + lontano + '</strong></p>';

  html += '<h3>Contatti e Risorse</h3>';
  html += '<p>Riferimento fuori città: <strong>' + contatto + '</strong></p>';
  html += '<p>Medico di famiglia: <strong>' + medico + '</strong></p>';
  html += '<p>Kit di emergenza: <strong>' + kit + '</strong></p>';
  html += '<p>Rubinetti e quadro elettrico: <strong>' + chiusure + '</strong></p>';

  if (farmaci !== 'Nessuno' || ausili !== 'Nessuno' || note) {
    html += '<h3>Esigenze Specifiche</h3>';
    if (farmaci !== 'Nessuno') html += '<p>Farmaci: <strong>' + farmaci + '</strong></p>';
    if (ausili !== 'Nessuno') html += '<p>Ausili: <strong>' + ausili + '</strong></p>';
    if (note) html += '<p>Note: <strong>' + note + '</strong></p>';
  }

  document.getElementById('piano-contenuto').innerHTML = html;
  document.getElementById('data-piano').textContent = new Date().toLocaleDateString('it-IT');
  document.getElementById('piano-output').classList.remove('d-none');
  document.getElementById('piano-output').scrollIntoView({behavior: 'smooth'});
}
</script>
