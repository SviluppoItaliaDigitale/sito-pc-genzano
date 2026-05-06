---
title: "Strumenti di consultazione in tempo reale"
description: "Strumenti utili per consultare meteo, terremoti, rischio idrogeologico, incendi, qualità dell'aria, viabilità ed emergenze da fonti ufficiali o qualificate."
layout: "single"
aliases:
  - /monitoraggio.html
  - /monitoraggio/
sitemap:
  priority: 0.8
  changefreq: monthly
toc: true
tts: true
dataUltimaRevisione: "2026-05-06"
---

Questa pagina raccoglie strumenti online utili per consultare informazioni sul territorio: meteo, terremoti, incendi, qualità dell'aria, viabilità ed emergenze. Alcuni strumenti si aprono nel sito. Altri rimandano al sito ufficiale del fornitore.

<div class="alert alert-warning" role="note">
<p class="mb-0"><i class="bi bi-info-circle me-2" aria-hidden="true"></i><strong>Importante:</strong> questi strumenti aiutano a informarsi, ma non sostituiscono i bollettini ufficiali. Per Genzano di Roma la fonte di riferimento per le allerte meteo è il <a href="https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" target="_blank" rel="noopener noreferrer">Centro Funzionale della Regione Lazio</a>. In caso di emergenza chiama il <strong>112</strong>.</p>
</div>

## Come usare questa pagina

- Usa la barra di ricerca per trovare uno strumento per nome o tema.
- Usa i filtri per visualizzare solo una categoria.
- Controlla sempre la fonte indicata nella scheda.
- Durante un'emergenza segui le indicazioni delle autorità.

## Legenda

- <span class="badge badge-fonte-istituzionale"><i class="bi bi-patch-check-fill me-1" aria-hidden="true"></i>Fonte istituzionale</span> — dato fornito da enti pubblici o organismi ufficiali.
- <span class="badge badge-fonte-consultazione"><i class="bi bi-info-circle-fill me-1" aria-hidden="true"></i>Strumento di consultazione</span> — servizio privato o rete volontaria utile alla consultazione, ma non sostitutivo delle fonti ufficiali.
- **Apri widget sul sito** — lo strumento si apre dentro questo sito.
- **Apri sito ufficiale** — lo strumento si apre in una nuova scheda.

<style>
.strumenti-filtri{position:sticky;top:0;z-index:50;background:#fff;border-radius:12px;padding:1rem 1.2rem;margin:1.5rem 0 2rem 0;box-shadow:0 2px 12px rgba(0,0,0,.08);border:1px solid #dee2e6}
.strumenti-filtri-row{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center}
.strumenti-cerca{flex:1 1 280px;min-width:200px;padding:.55rem .9rem;font-size:1rem;border:1.5px solid #ced4da;border-radius:8px}
.strumenti-cerca:focus{outline:2px solid #ffbe2e;outline-offset:1px;border-color:#003366}
.strumenti-pill{background:#fff;border:1.5px solid #003366;color:#003366;border-radius:22px;padding:.4rem .9rem;font-size:.9rem;font-weight:600;cursor:pointer;min-height:40px;transition:all .15s}
.strumenti-pill:hover,.strumenti-pill:focus{background:#e7f1ff;outline:2px solid #ffbe2e;outline-offset:1px}
.strumenti-pill.attivo{background:#003366;color:#fff}
.strumenti-counter{font-size:.85rem;color:#6c757d;margin-left:auto;padding-left:.6rem}
.strumenti-counter strong{color:#003366}
.strumenti-no-results{display:none;padding:1.5rem;text-align:center;background:#fff3cd;border:2px solid #d4a72c;border-radius:10px;color:#664d03;margin:1rem 0}
.strumenti-hidden{display:none!important}
@media print{.strumenti-filtri,.strumenti-no-results{display:none!important}.strumenti-hidden{display:block!important}}
</style>

<div class="strumenti-filtri" role="region" aria-label="Filtri ricerca strumenti">
  <div class="strumenti-filtri-row">
    <label class="visually-hidden" for="strumenti-cerca">Cerca tra gli strumenti</label>
    <input id="strumenti-cerca" type="search" class="strumenti-cerca" placeholder="Cerca: Windy, INGV, EFFIS, radar, terremoti..." autocomplete="off" aria-label="Cerca tra gli strumenti">
  </div>
  <div class="strumenti-filtri-row mt-2">
    <button type="button" class="strumenti-pill attivo" data-categoria="" aria-pressed="true">Tutti</button>
    <button type="button" class="strumenti-pill" data-categoria="meteo" aria-pressed="false">🌦️ Meteo</button>
    <button type="button" class="strumenti-pill" data-categoria="sismico" aria-pressed="false">🌐 Sismico</button>
    <button type="button" class="strumenti-pill" data-categoria="idrogeologico" aria-pressed="false">💧 Idrogeologico</button>
    <button type="button" class="strumenti-pill" data-categoria="incendi" aria-pressed="false">🔥 Incendi</button>
    <button type="button" class="strumenti-pill" data-categoria="aria" aria-pressed="false">🌬️ Aria</button>
    <button type="button" class="strumenti-pill" data-categoria="viabilita" aria-pressed="false">🚗 Viabilità</button>
    <button type="button" class="strumenti-pill" data-categoria="emergenze" aria-pressed="false">🚨 Emergenze</button>
    <button type="button" class="strumenti-pill" data-categoria="webcam" aria-pressed="false">📷 Webcam</button>
    <button type="button" class="strumenti-pill" data-categoria="educazione" aria-pressed="false">📚 Educazione</button>
    <span class="strumenti-counter" id="strumenti-counter" aria-live="polite"></span>
  </div>
</div>

<div id="strumenti-no-results" class="strumenti-no-results" role="status">
  <p class="mb-0"><strong>Nessuno strumento trovato.</strong> Prova a cambiare filtro o parola cercata.</p>
</div>

<h2 data-categoria="meteo">Meteo, radar e fulmini</h2>

<div class="row g-4 mb-5" data-categoria="meteo">

{{< tool-card
    nome="Mappa meteo interattiva"
    fonte="Windy.com"
    icona="bi-cloud-rain-heavy"
    tipoFonte="consultazione"
    descrizione="Radar, precipitazioni, vento, temperatura e pressione su Genzano di Roma. Utile per vedere a colpo d'occhio cosa si avvicina."
    tipoAccesso="widget"
    url="/allerte-meteo/#meteo-windy" >}}

{{< tool-card
    nome="Radar nazionale precipitazioni"
    fonte="Dipartimento Protezione Civile"
    icona="bi-broadcast-pin"
    tipoFonte="istituzionale"
    descrizione="Mosaico radar nazionale delle precipitazioni. Mostra la pioggia rilevata dai radar meteorologici del Dipartimento della Protezione Civile."
    tipoAccesso="widget"
    url="/allerte-meteo/#radar-dpc" >}}

{{< tool-card
    nome="Previsione meteo Genzano — Aeronautica Militare"
    fonte="Aeronautica Militare — Servizio Meteorologico"
    icona="bi-cloud-sun-fill"
    tipoFonte="istituzionale"
    descrizione="Previsione meteorologica ufficiale per Genzano di Roma, pubblicata dal Servizio Meteorologico dell'Aeronautica Militare."
    tipoAccesso="widget"
    url="/allerte-meteo/#meteo-aeronautica" >}}

{{< tool-card
    nome="Mappa fulmini in tempo reale"
    fonte="Blitzortung / Lightning Maps"
    icona="bi-lightning-charge-fill"
    tipoFonte="consultazione"
    descrizione="Fulmini rilevati in Europa dalla rete Blitzortung. Utile durante i temporali per capire dove si sta muovendo la cella temporalesca."
    tipoAccesso="widget"
    url="/rischi-prevenzione/temporali-intensi/#fulmini-blitzortung" >}}

{{< tool-card
    nome="Confronto multi-modello"
    fonte="meteoblue"
    icona="bi-bar-chart-line-fill"
    tipoFonte="consultazione"
    descrizione="Confronto tra più modelli previsionali per Genzano di Roma. Aiuta a capire se una previsione è stabile o incerta. Non sostituisce le fonti istituzionali."
    tipoAccesso="sito"
    url="https://www.meteoblue.com/it/tempo/previsioni/multimodel/genzano-di-roma_italia_3176203" >}}

</div>

<h2 data-categoria="sismico">Sismico</h2>

<div class="row g-4 mb-5" data-categoria="sismico">

{{< tool-card
    nome="Terremoti recenti in Italia"
    fonte="INGV — Istituto Nazionale di Geofisica e Vulcanologia"
    icona="bi-activity"
    tipoFonte="istituzionale"
    descrizione="Mappa e lista degli eventi sismici registrati in Italia. Usa lo zoom per consultare l'area dei Castelli Romani e dei Colli Albani."
    tipoAccesso="widget"
    url="/rischi-prevenzione/rischio-sismico/#sismico-ingv" >}}

</div>

<h2 data-categoria="idrogeologico">Rischio idrogeologico</h2>

<div class="row g-4 mb-5" data-categoria="idrogeologico">

{{< tool-card
    nome="IdroGEO — Rischio frane e alluvioni"
    fonte="ISPRA — Istituto Superiore per la Protezione e Ricerca Ambientale"
    icona="bi-water"
    tipoFonte="istituzionale"
    descrizione="Piattaforma nazionale con mappe di pericolosità per frane e alluvioni. Cerca Genzano di Roma per consultare le aree censite."
    tipoAccesso="sito"
    url="https://idrogeo.isprambiente.it/app/" >}}

</div>

<h2 data-categoria="incendi">Incendi boschivi</h2>

<div class="row g-4 mb-5" data-categoria="incendi">

{{< tool-card
    nome="EFFIS — Situazione incendi in Europa"
    fonte="Copernicus / JRC — Commissione Europea"
    icona="bi-fire"
    tipoFonte="istituzionale"
    descrizione="Mappa europea degli incendi boschivi attivi, dei focolai rilevati da satellite e dell'indice di pericolosità AIB."
    tipoAccesso="sito"
    url="https://effis.jrc.ec.europa.eu/apps/effis_current_situation/" >}}

</div>

<h2 data-categoria="aria">Qualità dell'aria e ambiente</h2>

<div class="row g-4 mb-5" data-categoria="aria">

{{< tool-card
    nome="Qualità dell'aria in provincia di Roma"
    fonte="ARPA Lazio"
    icona="bi-wind"
    tipoFonte="istituzionale"
    descrizione="Dati delle centraline di ARPA Lazio su PM10, PM2.5, ozono e biossido di azoto. Utile durante caldo intenso, incendi o inversione termica."
    tipoAccesso="sito"
    url="https://www.arpalazio.it/ambiente/aria" >}}

</div>

<h2 data-categoria="viabilita">Viabilità</h2>

<div class="row g-4 mb-5" data-categoria="viabilita">

{{< tool-card
    nome="Viabilità in tempo reale"
    fonte="ANAS — Rete stradale nazionale"
    icona="bi-signpost-split"
    tipoFonte="istituzionale"
    descrizione="Stato della rete stradale nazionale: chiusure, incidenti, lavori e traffico. Utile per pianificare gli spostamenti durante maltempo o emergenze."
    tipoAccesso="sito"
    url="https://www.stradeanas.it/it/vai-traffico-in-tempo-reale" >}}

</div>

<h2 data-categoria="emergenze">Emergenze e cartografia operativa</h2>

<div class="row g-4 mb-5" data-categoria="emergenze">

{{< tool-card
    nome="AEGIS — Tempo reale Regione Lazio"
    fonte="Regione Lazio"
    icona="bi-geo-alt-fill"
    tipoFonte="istituzionale"
    descrizione="Piattaforma cartografica regionale per consultare informazioni operative su emergenze, incendi, allerte e fenomeni estremi nel Lazio."
    tipoAccesso="sito"
    url="https://temporeale.regione.lazio.it/aegis/" >}}

{{< tool-card
    nome="Copernicus EMS — Emergenze UE"
    fonte="Commissione Europea — Servizio Gestione Emergenze"
    icona="bi-shield-exclamation"
    tipoFonte="istituzionale"
    descrizione="Servizio europeo di mappatura rapida dopo grandi emergenze, come alluvioni, incendi estesi e terremoti rilevanti."
    tipoAccesso="sito"
    url="https://emergency.copernicus.eu/" >}}

</div>

<h2 data-categoria="webcam">Webcam del territorio</h2>

<div class="row g-4 mb-5" data-categoria="webcam">

{{< tool-card
    nome="Webcam nei dintorni di Genzano"
    fonte="Windy.com (webcam pubbliche)"
    icona="bi-camera-video-fill"
    tipoFonte="consultazione"
    descrizione="Webcam pubbliche nei Castelli Romani e nell'area di Roma Sud. Sono utili per osservare le condizioni visive del tempo e del territorio."
    tipoAccesso="sito"
    url="https://www.windy.com/-Webcams/webcams/cams/41.691,12.692" >}}

</div>

<h2 data-categoria="educazione">Educazione e simulazione</h2>

<div class="row g-4 mb-5" data-categoria="educazione">

{{< tool-card
    nome="Stop Disasters! — Simulatore ONU"
    fonte="UNDRR — United Nations Office for Disaster Risk Reduction"
    icona="bi-shield-fill-exclamation"
    tipoFonte="istituzionale"
    descrizione="Gioco-simulazione gratuito sulla riduzione del rischio di disastri. Propone scenari su terremoti, alluvioni, tsunami, uragani e incendi boschivi."
    tipoAccesso="sito"
    url="https://www.stopdisastersgame.org/game/" >}}

</div>

## Fonti ufficiali primarie

Per Genzano di Roma, le fonti istituzionali da consultare sono:

- [Centro Funzionale Regionale Lazio — Bollettini di allerta](https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti)
- [Dipartimento della Protezione Civile](https://www.protezionecivile.gov.it/)
- [Comune di Genzano di Roma](https://www.comune.genzanodiroma.roma.it/)
- [IT-alert](https://www.it-alert.it/)

Per emergenze in corso chiama sempre il **[112](tel:112)**.

<script>
(function(){
  var input = document.getElementById('strumenti-cerca');
  var pills = document.querySelectorAll('.strumenti-pill');
  var counter = document.getElementById('strumenti-counter');
  var noRes = document.getElementById('strumenti-no-results');
  var rows = document.querySelectorAll('.row.g-4[data-categoria]');
  var h2s = document.querySelectorAll('h2[data-categoria]');
  var stato = {cat:'', q:''};
  var totale = 0;
  rows.forEach(function(r){ totale += r.querySelectorAll('.tool-card').length; });
  function filtra(){
    var q = stato.q.trim().toLowerCase();
    var cat = stato.cat;
    var visibili = 0;
    rows.forEach(function(row){
      var rowCat = row.getAttribute('data-categoria');
      var rowVisibili = 0;
      row.querySelectorAll('.tool-card').forEach(function(card){
        var col = card.closest('.col-md-6, .col-lg-4');
        if (!col) col = card.parentElement;
        var okCat = !cat || rowCat === cat;
        var okQ = !q || card.textContent.toLowerCase().indexOf(q) !== -1;
        var ok = okCat && okQ;
        col.classList.toggle('strumenti-hidden', !ok);
        if (ok) rowVisibili++;
      });
      row.classList.toggle('strumenti-hidden', rowVisibili === 0);
      visibili += rowVisibili;
    });
    h2s.forEach(function(h){
      var hCat = h.getAttribute('data-categoria');
      var sib = h.nextElementSibling;
      while (sib && !(sib.classList && sib.classList.contains('row') && sib.getAttribute('data-categoria') === hCat)) {
        sib = sib.nextElementSibling;
      }
      var hide = (cat && hCat !== cat) || (sib && sib.classList.contains('strumenti-hidden'));
      h.classList.toggle('strumenti-hidden', hide);
    });
    counter.innerHTML = '<strong>' + visibili + '</strong> di ' + totale + ' strumenti';
    noRes.style.display = visibili === 0 ? 'block' : 'none';
  }
  pills.forEach(function(p){
    p.addEventListener('click', function(){
      pills.forEach(function(x){x.classList.remove('attivo'); x.setAttribute('aria-pressed','false');});
      p.classList.add('attivo');
      p.setAttribute('aria-pressed','true');
      stato.cat = p.getAttribute('data-categoria');
      filtra();
    });
  });
  var t;
  if (input) input.addEventListener('input', function(){
    clearTimeout(t);
    t = setTimeout(function(){ stato.q = input.value; filtra(); }, 150);
  });
  var m = (location.hash||'').match(/cat=([a-z]+)/);
  if (m) {
    var pt = document.querySelector('.strumenti-pill[data-categoria="'+m[1]+'"]');
    if (pt) pt.click();
  } else {
    filtra();
  }
})();
</script>

## Vedi anche

- [Allerte meteo](/allerte-meteo/) — stato di allerta corrente
- [Cartografia](/cartografia/) — mappe del territorio
- [Siti utili](/siti-utili/) — fonti istituzionali esterne
- [Numeri utili](/numeri-utili/) — chi chiamare in caso di emergenza
