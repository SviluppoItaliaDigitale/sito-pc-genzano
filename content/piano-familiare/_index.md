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
<div id="piano-stampabile" class="card shadow p-4 mb-4">
<div class="piano-print-header text-center">
<h2 class="mb-1">Piano di Emergenza Familiare</h2>
<p class="text-muted mb-0">Protezione Civile Genzano di Roma &mdash; Gruppo Comunale Volontari</p>
<p class="text-muted small mb-0">Documento generato il <span id="data-piano"></span></p>
</div>
<hr>
<div id="piano-contenuto"></div>
<div class="piano-numeri text-center mt-4 p-3">
<strong>Numeri di Emergenza</strong><br>
<strong>112</strong> Numero Unico Emergenze (NUE) &mdash; valido nel Lazio per qualsiasi emergenza<br>
<strong>803 555</strong> Sala Operativa Protezione Civile Lazio &mdash; segnalazioni non urgenti<br>
<small class="text-muted">Conservare in un luogo accessibile a tutti i familiari. Aggiornare almeno una volta all'anno.</small>
</div>
<div id="piano-print-appendice"></div>
</div>
<div class="d-flex flex-wrap gap-2 mb-4 piano-buttons">
<button type="button" class="btn btn-success btn-lg" onclick="stampaPiano()"><i class="bi bi-printer me-2" aria-hidden="true"></i>Stampa / Salva PDF</button>
<button type="button" class="btn btn-outline-primary btn-lg" onclick="document.getElementById('piano-output').classList.add('d-none');window.scrollTo({top:0,behavior:'smooth'})"><i class="bi bi-pencil me-2" aria-hidden="true"></i>Modifica</button>
</div>
</div>

<div class="piano-screen-only">

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

</div>

<script>
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML}

function generaPiano(){
  var cognome=esc(document.getElementById('cognome').value||'Non indicato');
  var indirizzo=esc(document.getElementById('indirizzo').value||'Non indicato');
  var adulti=parseInt(document.getElementById('adulti').value)||0;
  var bambini=parseInt(document.getElementById('bambini').value)||0;
  var anziani=parseInt(document.getElementById('anziani').value)||0;
  var animali=esc(document.getElementById('animali').value||'Nessuno');
  var vicino=esc(document.getElementById('ritrovo-vicino').value||'Non indicato');
  var lontano=esc(document.getElementById('ritrovo-lontano').value||'Non indicato');
  var contatto=esc(document.getElementById('contatto-fuori').value||'Non indicato');
  var medico=esc(document.getElementById('medico').value||'Non indicato');
  var kit=esc(document.getElementById('kit-emergenza').value||'Non indicato');
  var chiusure=esc(document.getElementById('chiusure').value||'Non indicato');
  var farmaci=esc(document.getElementById('farmaci').value||'Nessuno');
  var ausili=esc(document.getElementById('ausili').value||'Nessuno');
  var note=esc(document.getElementById('note').value||'');

  var h='';

  /* ── Sezione 1: Famiglia ── */
  h+='<h3 class="piano-section-title">La mia Famiglia</h3>';
  h+='<table class="piano-table" role="presentation"><tbody>';
  h+='<tr><td>Cognome</td><td><strong>'+cognome+'</strong></td></tr>';
  h+='<tr><td>Indirizzo</td><td><strong>'+indirizzo+'</strong></td></tr>';
  h+='<tr><td>Composizione</td><td>Adulti: <strong>'+adulti+'</strong> &mdash; Bambini/Ragazzi: <strong>'+bambini+'</strong> &mdash; Anziani/Fragili: <strong>'+anziani+'</strong></td></tr>';
  h+='<tr><td>Animali domestici</td><td><strong>'+animali+'</strong></td></tr>';
  h+='</tbody></table>';

  /* ── Sezione 2: Punti di Ritrovo ── */
  h+='<h3 class="piano-section-title">Punti di Ritrovo</h3>';
  h+='<table class="piano-table" role="presentation"><tbody>';
  h+='<tr><td>Vicino casa</td><td><strong>'+vicino+'</strong></td></tr>';
  h+='<tr><td>Lontano da casa</td><td><strong>'+lontano+'</strong></td></tr>';
  h+='</tbody></table>';

  /* ── Sezione 3: Contatti e Risorse ── */
  h+='<h3 class="piano-section-title">Contatti e Risorse</h3>';
  h+='<table class="piano-table" role="presentation"><tbody>';
  h+='<tr><td>Riferimento fuori citt\u00e0</td><td><strong>'+contatto+'</strong></td></tr>';
  h+='<tr><td>Medico di famiglia</td><td><strong>'+medico+'</strong></td></tr>';
  h+='<tr><td>Kit di emergenza</td><td><strong>'+kit+'</strong></td></tr>';
  h+='<tr><td>Rubinetti e quadro elettrico</td><td><strong>'+chiusure+'</strong></td></tr>';
  h+='</tbody></table>';

  /* ── Sezione 4: Esigenze specifiche (solo se compilate) ── */
  if(farmaci!=='Nessuno'||ausili!=='Nessuno'||note){
    h+='<h3 class="piano-section-title">Esigenze Specifiche</h3>';
    h+='<table class="piano-table" role="presentation"><tbody>';
    if(farmaci!=='Nessuno') h+='<tr><td>Farmaci</td><td><strong>'+farmaci+'</strong></td></tr>';
    if(ausili!=='Nessuno') h+='<tr><td>Ausili</td><td><strong>'+ausili+'</strong></td></tr>';
    if(note) h+='<tr><td>Note</td><td><strong>'+note+'</strong></td></tr>';
    h+='</tbody></table>';
  }

  document.getElementById('piano-contenuto').innerHTML=h;
  document.getElementById('data-piano').textContent=new Date().toLocaleDateString('it-IT');
  document.getElementById('piano-output').classList.remove('d-none');
  document.getElementById('piano-output').scrollIntoView({behavior:'smooth'});
}

function stampaPiano(){
  /* Clona consigli e checklist dentro l'area stampabile */
  var source=document.querySelector('.piano-screen-only');
  var target=document.getElementById('piano-print-appendice');
  if(source&&target){
    target.innerHTML='';
    var clone=source.cloneNode(true);
    clone.classList.remove('piano-screen-only');
    clone.className='piano-appendice-content';
    target.appendChild(clone);
  }

  document.body.classList.add('piano-printing');
  var cleanup=function(){
    document.body.classList.remove('piano-printing');
    if(target) target.innerHTML='';
  };
  window.addEventListener('afterprint',function handler(){
    cleanup();
    window.removeEventListener('afterprint',handler);
  });
  window.print();
  /* Fallback per browser senza afterprint */
  setTimeout(function(){
    if(document.body.classList.contains('piano-printing')) cleanup();
  },2000);
}
</script>
