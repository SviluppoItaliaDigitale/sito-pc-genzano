---
title: "Strumenti di consultazione in tempo reale"
description: "Raccolta di strumenti ufficiali e di consultazione per monitorare meteo, terremoti, rischio idrogeologico, incendi, qualità dell'aria, viabilità ed emergenze."
layout: "single"
aliases:
  - /monitoraggio.html
  - /monitoraggio/
sitemap:
  priority: 0.8
  changefreq: monthly
---

Questa pagina raccoglie in un unico posto gli **strumenti online** che ti permettono di consultare in tempo reale le informazioni utili alla sicurezza del territorio: previsioni meteo, terremoti, incendi, qualità dell'aria, viabilità. Alcuni sono **incorporati direttamente** nel nostro sito (li puoi aprire con un click), altri rimandano al **sito ufficiale** del fornitore perché non consentono l'incorporamento.

<div class="alert alert-warning" role="note">
<p class="mb-0"><i class="bi bi-info-circle me-2" aria-hidden="true"></i><strong>Importante:</strong> questi strumenti sono un <strong>ausilio alla consultazione</strong>. In caso di allerta o emergenza, la fonte ufficiale per il territorio di Genzano di Roma resta sempre il <a href="https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" target="_blank" rel="noopener noreferrer">bollettino del Centro Funzionale della Regione Lazio</a> e, per emergenze in corso, il numero unico <strong>112</strong>.</p>
</div>

## Legenda

- <span class="badge badge-fonte-istituzionale"><i class="bi bi-patch-check-fill me-1" aria-hidden="true"></i>Fonte istituzionale</span> — dato fornito da enti pubblici (DPC, INGV, ISPRA, ARPA, Commissione UE, ecc.)
- <span class="badge badge-fonte-consultazione"><i class="bi bi-info-circle-fill me-1" aria-hidden="true"></i>Strumento di consultazione</span> — fornitore privato o rete volontaria, scientificamente affidabile ma non istituzionale
- **Apri widget sul sito** — lo strumento si apre direttamente sul nostro sito
- **Apri sito ufficiale** — lo strumento si apre sul sito del fornitore in una nuova scheda

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
  <p class="mb-0"><strong>Nessuno strumento trovato.</strong> Prova a cambiare il filtro o il termine cercato.</p>
</div>

<h2 data-categoria="meteo">Meteo, radar e fulmini</h2>

<div class="row g-4 mb-5" data-categoria="meteo">

{{< tool-card
    nome="Mappa meteo interattiva"
    fonte="Windy.com"
    icona="bi-cloud-rain-heavy"
    tipoFonte="consultazione"
    descrizione="Radar, precipitazioni, vento, temperatura e pressione su Genzano di Roma. Modelli previsionali ECMWF, GFS, ICON. Utile per vedere a colpo d'occhio cosa si avvicina."
    tipoAccesso="widget"
    url="/allerte-meteo/#meteo-windy" >}}

{{< tool-card
    nome="Radar nazionale precipitazioni"
    fonte="Dipartimento Protezione Civile"
    icona="bi-broadcast-pin"
    tipoFonte="istituzionale"
    descrizione="Mosaico radar nazionale aggiornato ogni 10 minuti. Mostra l'intensità reale della pioggia misurata dai radar meteo del Dipartimento di Protezione Civile."
    tipoAccesso="widget"
    url="/allerte-meteo/#radar-dpc" >}}

{{< tool-card
    nome="Previsione meteo Genzano — Aeronautica Militare"
    fonte="Aeronautica Militare — Servizio Meteorologico"
    icona="bi-cloud-sun-fill"
    tipoFonte="istituzionale"
    descrizione="Previsione meteorologica ufficiale italiana per Genzano di Roma. Fonte istituzionale del Servizio Meteorologico Nazionale."
    tipoAccesso="widget"
    url="/allerte-meteo/#meteo-aeronautica" >}}

{{< tool-card
    nome="Mappa fulmini in tempo reale"
    fonte="Blitzortung / Lightning Maps"
    icona="bi-lightning-charge-fill"
    tipoFonte="consultazione"
    descrizione="Fulmini rilevati in Europa dalla rete volontaria Blitzortung. Utile durante temporali per capire dove si sta muovendo la cella."
    tipoAccesso="widget"
    url="/rischi-prevenzione/temporali-intensi/#fulmini-blitzortung" >}}

{{< tool-card
    nome="Confronto multi-modello"
    fonte="meteoblue"
    icona="bi-bar-chart-line-fill"
    tipoFonte="consultazione"
    descrizione="Confronto grafico tra più modelli previsionali (ECMWF, GFS, ICON, ecc.) per Genzano di Roma. Utile per valutare l'<strong>affidabilità</strong> di una previsione: se i modelli concordano la previsione è robusta, se divergono c'è incertezza. Prodotto commerciale, non sostituisce le fonti istituzionali."
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
    descrizione="Mappa e lista degli eventi sismici rilevati sul territorio italiano. Usa lo zoom per focalizzare l'area dei Castelli Romani e dei Colli Albani. Fonte scientifica ufficiale per la sismologia in Italia."
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
    descrizione="Piattaforma nazionale con mappe di pericolosità frane (inventario IFFI) e alluvioni (PAI). Cerca Genzano di Roma per vedere le aree censite sul nostro territorio."
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
    descrizione="Mappa europea degli incendi boschivi attivi, focolai rilevati da satellite e indice di pericolosità AIB. Particolarmente utile nel periodo giugno-settembre."
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
    descrizione="Dati delle centraline di monitoraggio di ARPA Lazio: PM10, PM2.5, ozono, biossido di azoto. Utile durante ondate di calore, incendi o episodi di inversione termica."
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
    descrizione="Stato della rete stradale nazionale: chiusure, incidenti, lavori in corso, traffico intenso. Utile per pianificare spostamenti durante eventi meteo avversi o emergenze."
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
    descrizione="Piattaforma cartografica regionale per il monitoraggio di emergenze in corso nel Lazio, incendi, allerte meteo, fenomeni estremi. Vista operativa della Regione."
    tipoAccesso="sito"
    url="https://temporeale.regione.lazio.it/aegis/" >}}

{{< tool-card
    nome="Copernicus EMS — Emergenze UE"
    fonte="Commissione Europea — Servizio Gestione Emergenze"
    icona="bi-shield-exclamation"
    tipoFonte="istituzionale"
    descrizione="Servizio europeo di mappatura rapida post-evento (alluvioni, incendi estesi, terremoti maggiori). Le attivazioni forniscono cartografia immediata alle autorità di protezione civile."
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
    descrizione="Raccolta di webcam pubbliche nei Castelli Romani e nell'area di Roma Sud. Utile per vedere in tempo reale le condizioni del cielo e del territorio."
    tipoAccesso="sito"
    url="https://www.windy.com/-Webcams/webcams/cams/41.691,12.692" >}}

</div>

<h2 data-categoria="educazione">Educazione e simulazione</h2>

<div class="row g-4 mb-5" data-categoria="educazione">

{{< tool-card
    nome="Stop Disasters! — Simulatore ONU"
    fonte="UNDRR (UN Office for Disaster Risk Reduction)"
    icona="bi-shield-fill-exclamation"
    tipoFonte="istituzionale"
    descrizione="Gioco-simulazione gratuito dell'Agenzia ONU per la Riduzione del Rischio di Disastri. Cinque scenari (terremoto, alluvione, tsunami, uragano, incendio boschivo) per imparare a costruire villaggi e città più sicuri. Disponibile in italiano, adatto a 9-17 anni e a contesti educativi."
    tipoAccesso="sito"
    url="https://www.stopdisastersgame.org/game/" >}}

</div>

## Fonti ufficiali primarie

Per completezza, ricordiamo le **fonti di riferimento istituzionali** per Genzano di Roma, che restano sempre prevalenti rispetto a qualunque strumento di consultazione:

- [Centro Funzionale Regionale Lazio — Bollettini di allerta](https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti) — fonte ufficiale allerte meteo per il Lazio
- [Dipartimento della Protezione Civile](https://www.protezionecivile.gov.it/) — coordinamento nazionale
- [Comune di Genzano di Roma](https://www.comune.genzanodiroma.roma.it/) — autorità territoriale
- [IT-alert](https://www.it-alert.it/) — sistema nazionale di allarme pubblico

Per emergenze in corso comporre sempre il **[112](tel:112)** — Numero Unico Europeo.

<script>
(function(){
  var input = document.getElementById('strumenti-cerca');
  var pills = document.querySelectorAll('.strumenti-pill');
  var counter = document.getElementById('strumenti-counter');
  var noRes = document.getElementById('strumenti-no-results');
  var rows = document.querySelectorAll('.row.g-4[data-categoria]');
  var h2s = document.querySelectorAll('h2[data-categoria]');
  var stato = {cat:'', q:''};

  // Conta totale strumenti
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

    // Nascondi h2 se la sua row è nascosta
    h2s.forEach(function(h){
      var hCat = h.getAttribute('data-categoria');
      // Trova la prossima row.row con stessa categoria
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

  // Hash deep-link: #cat=meteo
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

