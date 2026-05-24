---
title: "Cruscotto del territorio"
description: "Cruscotto multidisciplinare: terremoti in tempo reale (INGV), radar pioggia, meteo del Lazio e stato di allerta, in un'unica pagina."
layout: "single"
tts: false
toc: false
aliases:
  - /dashboard/
---

Un'unica pagina per consultare i dati di rischio del territorio, da **fonti ufficiali e aperte**. Scegli il tema con i pulsanti qui sotto. Sono dati **indicativi**: per le allerte valgono i bollettini del [Centro Funzionale Regionale del Lazio](https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti), in emergenza chiama il **112**.

<div class="cruscotto-switch" role="tablist" aria-label="Temi del cruscotto">
  <button type="button" class="cruscotto-tab" id="tab-terremoti" data-panel="terremoti" role="tab" aria-selected="true" aria-controls="panel-terremoti" tabindex="0"><i class="bi bi-activity" aria-hidden="true"></i> Terremoti</button>
  <button type="button" class="cruscotto-tab" id="tab-radar" data-panel="radar" role="tab" aria-selected="false" aria-controls="panel-radar" tabindex="-1"><i class="bi bi-cloud-rain-heavy" aria-hidden="true"></i> Radar pioggia</button>
  <button type="button" class="cruscotto-tab" id="tab-meteo" data-panel="meteo" role="tab" aria-selected="false" aria-controls="panel-meteo" tabindex="-1"><i class="bi bi-cloud-sun" aria-hidden="true"></i> Meteo</button>
  <button type="button" class="cruscotto-tab" id="tab-allerta" data-panel="allerta" role="tab" aria-selected="false" aria-controls="panel-allerta" tabindex="-1"><i class="bi bi-exclamation-triangle" aria-hidden="true"></i> Allerta</button>
  <button type="button" class="cruscotto-tab" id="tab-aria" data-panel="aria" role="tab" aria-selected="false" aria-controls="panel-aria" tabindex="-1"><i class="bi bi-wind" aria-hidden="true"></i> Aria e pollini</button>
  <button type="button" class="cruscotto-tab" id="tab-mare" data-panel="mare" role="tab" aria-selected="false" aria-controls="panel-mare" tabindex="-1"><i class="bi bi-water" aria-hidden="true"></i> Mare</button>
</div>

<div class="cruscotto-panel" id="panel-terremoti" data-panel="terremoti" role="tabpanel" aria-labelledby="tab-terremoti" tabindex="0">

{{< dashboard-terremoti >}}

</div>

<div class="cruscotto-panel" id="panel-radar" data-panel="radar" role="tabpanel" aria-labelledby="tab-radar" tabindex="0" hidden>

{{< radar-dpc >}}

</div>

<div class="cruscotto-panel" id="panel-meteo" data-panel="meteo" role="tabpanel" aria-labelledby="tab-meteo" tabindex="0" hidden>

{{< meteo-lazio >}}

</div>

<div class="cruscotto-panel" id="panel-allerta" data-panel="allerta" role="tabpanel" aria-labelledby="tab-allerta" tabindex="0" hidden>

{{< allerta-stato-attuale >}}

</div>

<div class="cruscotto-panel" id="panel-aria" data-panel="aria" role="tabpanel" aria-labelledby="tab-aria" tabindex="0" hidden>

{{< dashboard-aria >}}

</div>

<div class="cruscotto-panel" id="panel-mare" data-panel="mare" role="tabpanel" aria-labelledby="tab-mare" tabindex="0" hidden>

{{< dashboard-mare >}}

</div>

<script>
(function(){
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.cruscotto-switch .cruscotto-tab'));
  var panels = document.querySelectorAll('.cruscotto-panel');
  function show(name, focus){
    tabs.forEach(function(t){
      var on = t.dataset.panel === name;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    panels.forEach(function(p){ p.hidden = (p.dataset.panel !== name); });
    // le mappe Leaflet nascoste hanno dimensione 0: un resize le ridisegna
    window.dispatchEvent(new Event('resize'));
    if (name === 'terremoti') window.dispatchEvent(new Event('cruscotto:terremoti'));
  }
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){ show(t.dataset.panel); });
    t.addEventListener('keydown', function(e){
      var n = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = (i + 1) % tabs.length;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') n = 0;
      else if (e.key === 'End') n = tabs.length - 1;
      if (n !== null) { e.preventDefault(); show(tabs[n].dataset.panel, true); }
    });
  });
})();
</script>

## Le fonti del cruscotto

- **Terremoti** — [INGV](https://terremoti.ingv.it/) (Istituto Nazionale di Geofisica e Vulcanologia), servizio FDSN open data, ultimi 7 giorni in Italia.
- **Radar pioggia** — [Radar-DPC](https://mappe.protezionecivile.gov.it/it/mappe-e-dashboard-rischi/piattaforma-radar/) (Dipartimento della Protezione Civile), servizi WMTS open data.
- **Meteo** — [Open-Meteo](https://open-meteo.com/) (modelli ECMWF), nostra elaborazione per il Lazio e Genzano di Roma.
- **Allerta** — [Centro Funzionale Regionale del Lazio](https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti).
- **Aria e pollini** — [Open-Meteo Air Quality](https://open-meteo.com/) (dati europei [Copernicus CAMS](https://atmosphere.copernicus.eu/)): indice AQI europeo, PM10, PM2.5, ozono, pollini.
- **Mare** — [Open-Meteo Marine](https://open-meteo.com/): altezza e periodo onde sulla costa laziale.

> La scheda **Terremoti** ha lo switch **Italia / Castelli Romani**: la vista locale mostra la sismicità del distretto vulcanico dei Colli Albani, su cui sorge Genzano di Roma.
