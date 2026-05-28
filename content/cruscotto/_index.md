---
title: "Cruscotto del territorio"
description: "Cruscotto multidisciplinare in tempo reale: terremoti e vulcani (INGV), radar pioggia, satellite, meteo, allerta, incendi, aria e mare, in un'unica pagina."
layout: "single"
tts: false
toc: false
aliases:
  - /dashboard/
---

Un'unica pagina per consultare i dati di rischio del territorio, da **fonti ufficiali e aperte**. Scegli il tema con i pulsanti qui sotto. Sono dati **indicativi**: per le allerte valgono i bollettini del [Centro Funzionale Regionale del Lazio](https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti), in emergenza chiama il **112**.

<div class="cruscotto-switch" role="tablist" aria-label="Temi del cruscotto">
  <button type="button" class="cruscotto-tab" id="tab-terremoti" data-panel="terremoti" role="tab" aria-selected="true" aria-controls="panel-terremoti" tabindex="0"><i class="bi bi-activity" aria-hidden="true"></i> Terremoti</button>
  <button type="button" class="cruscotto-tab" id="tab-vulcani" data-panel="vulcani" role="tab" aria-selected="false" aria-controls="panel-vulcani" tabindex="-1"><i class="bi bi-triangle" aria-hidden="true"></i> Vulcani</button>
  <button type="button" class="cruscotto-tab" id="tab-radar" data-panel="radar" role="tab" aria-selected="false" aria-controls="panel-radar" tabindex="-1"><i class="bi bi-cloud-rain-heavy" aria-hidden="true"></i> Radar pioggia</button>
  <button type="button" class="cruscotto-tab" id="tab-radar-im" data-panel="radar-im" role="tab" aria-selected="false" aria-controls="panel-radar-im" tabindex="-1"><i class="bi bi-cloud-rain-heavy-fill" aria-hidden="true"></i> Radar ItaliaMeteo</button>
  <button type="button" class="cruscotto-tab" id="tab-satellite" data-panel="satellite" role="tab" aria-selected="false" aria-controls="panel-satellite" tabindex="-1"><i class="bi bi-globe-europe-africa" aria-hidden="true"></i> Satellite (EUMETSAT)</button>
  <button type="button" class="cruscotto-tab" id="tab-satellite-im" data-panel="satellite-im" role="tab" aria-selected="false" aria-controls="panel-satellite-im" tabindex="-1"><i class="bi bi-globe2" aria-hidden="true"></i> Satellite ItaliaMeteo</button>
  <button type="button" class="cruscotto-tab" id="tab-meteo" data-panel="meteo" role="tab" aria-selected="false" aria-controls="panel-meteo" tabindex="-1"><i class="bi bi-cloud-sun" aria-hidden="true"></i> Meteo</button>
  <button type="button" class="cruscotto-tab" id="tab-previsioni-im" data-panel="previsioni-im" role="tab" aria-selected="false" aria-controls="panel-previsioni-im" tabindex="-1"><i class="bi bi-cloud-sun-fill" aria-hidden="true"></i> Previsioni ItaliaMeteo</button>
  <button type="button" class="cruscotto-tab" id="tab-obs-im" data-panel="obs-im" role="tab" aria-selected="false" aria-controls="panel-obs-im" tabindex="-1"><i class="bi bi-thermometer-half" aria-hidden="true"></i> Osservazioni ItaliaMeteo</button>
  <button type="button" class="cruscotto-tab" id="tab-allerta" data-panel="allerta" role="tab" aria-selected="false" aria-controls="panel-allerta" tabindex="-1"><i class="bi bi-exclamation-triangle" aria-hidden="true"></i> Allerta</button>
  <button type="button" class="cruscotto-tab" id="tab-incendi" data-panel="incendi" role="tab" aria-selected="false" aria-controls="panel-incendi" tabindex="-1"><i class="bi bi-fire" aria-hidden="true"></i> Incendi</button>
  <button type="button" class="cruscotto-tab" id="tab-aria" data-panel="aria" role="tab" aria-selected="false" aria-controls="panel-aria" tabindex="-1"><i class="bi bi-wind" aria-hidden="true"></i> Aria e pollini</button>
  <button type="button" class="cruscotto-tab" id="tab-aria-cams" data-panel="aria-cams" role="tab" aria-selected="false" aria-controls="panel-aria-cams" tabindex="-1"><i class="bi bi-cloud-haze2" aria-hidden="true"></i> Aria Europa (CAMS)</button>
  <button type="button" class="cruscotto-tab" id="tab-ems" data-panel="ems" role="tab" aria-selected="false" aria-controls="panel-ems" tabindex="-1"><i class="bi bi-map" aria-hidden="true"></i> Emergenze EU (EMS)</button>
  <button type="button" class="cruscotto-tab" id="tab-mare" data-panel="mare" role="tab" aria-selected="false" aria-controls="panel-mare" tabindex="-1"><i class="bi bi-water" aria-hidden="true"></i> Mare</button>
  <button type="button" class="cruscotto-tab" id="tab-mare-im" data-panel="mare-im" role="tab" aria-selected="false" aria-controls="panel-mare-im" tabindex="-1"><i class="bi bi-tsunami" aria-hidden="true"></i> Mare ItaliaMeteo</button>
</div>

<div class="cruscotto-panel" id="panel-terremoti" data-panel="terremoti" role="tabpanel" aria-labelledby="tab-terremoti" tabindex="0">

{{< dashboard-terremoti >}}

</div>

<div class="cruscotto-panel" id="panel-vulcani" data-panel="vulcani" role="tabpanel" aria-labelledby="tab-vulcani" tabindex="0" hidden>

{{< dashboard-vulcani >}}

</div>

<div class="cruscotto-panel" id="panel-radar" data-panel="radar" role="tabpanel" aria-labelledby="tab-radar" tabindex="0" hidden>

{{< radar-dpc >}}

</div>

<div class="cruscotto-panel" id="panel-radar-im" data-panel="radar-im" role="tabpanel" aria-labelledby="tab-radar-im" tabindex="0" hidden>

{{< dashboard-italiameteo-radar >}}

</div>

<div class="cruscotto-panel" id="panel-satellite" data-panel="satellite" role="tabpanel" aria-labelledby="tab-satellite" tabindex="0" hidden>

{{< dashboard-satellite >}}

</div>

<div class="cruscotto-panel" id="panel-satellite-im" data-panel="satellite-im" role="tabpanel" aria-labelledby="tab-satellite-im" tabindex="0" hidden>

{{< dashboard-italiameteo-satellite >}}

</div>

<div class="cruscotto-panel" id="panel-meteo" data-panel="meteo" role="tabpanel" aria-labelledby="tab-meteo" tabindex="0" hidden>

{{< meteo-lazio >}}

</div>

<div class="cruscotto-panel" id="panel-previsioni-im" data-panel="previsioni-im" role="tabpanel" aria-labelledby="tab-previsioni-im" tabindex="0" hidden>

{{< dashboard-italiameteo >}}

</div>

<div class="cruscotto-panel" id="panel-obs-im" data-panel="obs-im" role="tabpanel" aria-labelledby="tab-obs-im" tabindex="0" hidden>

{{< dashboard-italiameteo-osservazioni >}}

</div>

<div class="cruscotto-panel" id="panel-allerta" data-panel="allerta" role="tabpanel" aria-labelledby="tab-allerta" tabindex="0" hidden>

{{< allerta-stato-attuale >}}

</div>

<div class="cruscotto-panel" id="panel-incendi" data-panel="incendi" role="tabpanel" aria-labelledby="tab-incendi" tabindex="0" hidden>

{{< dashboard-incendi >}}

</div>

<div class="cruscotto-panel" id="panel-aria" data-panel="aria" role="tabpanel" aria-labelledby="tab-aria" tabindex="0" hidden>

{{< dashboard-aria >}}

</div>

<div class="cruscotto-panel" id="panel-aria-cams" data-panel="aria-cams" role="tabpanel" aria-labelledby="tab-aria-cams" tabindex="0" hidden>

{{< dashboard-cams >}}

</div>

<div class="cruscotto-panel" id="panel-ems" data-panel="ems" role="tabpanel" aria-labelledby="tab-ems" tabindex="0" hidden>

{{< dashboard-ems >}}

</div>

<div class="cruscotto-panel" id="panel-mare" data-panel="mare" role="tabpanel" aria-labelledby="tab-mare" tabindex="0" hidden>

{{< dashboard-mare >}}

</div>

<div class="cruscotto-panel" id="panel-mare-im" data-panel="mare-im" role="tabpanel" aria-labelledby="tab-mare-im" tabindex="0" hidden>

{{< dashboard-italiameteo-mare >}}

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
    // init lazy della scheda mostrata (terremoti, satellite, ...)
    window.dispatchEvent(new Event('cruscotto:' + name));
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
- **Vulcani** — [INGV](https://terremoti.ingv.it/): sismicità degli ultimi 30 giorni nel Distretto Vulcanico dei Colli Albani, la caldera quiescente su cui sorge Genzano di Roma.
- **Radar pioggia** — [Radar-DPC](https://mappe.protezionecivile.gov.it/it/mappe-e-dashboard-rischi/piattaforma-radar/) (Dipartimento della Protezione Civile), servizi WMTS open data.
- **Radar ItaliaMeteo** — [Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/meteo/dati-osservati/radar/) (prodotto SRI, intensità di pioggia al suolo), cartine WMS da [MeteoHub](https://meteohub.agenziaitaliameteo.it/), licenza CC BY 4.0. Complementare al radar DPC.
- **Satellite (EUMETSAT)** — [EUMETSAT](https://www.eumetsat.int/) (Meteosat, nuvole a colori naturali aggiornate ogni 10 minuti) e [NASA GIBS](https://worldview.earthdata.nasa.gov/) (immagine true-color del giorno).
- **Satellite ItaliaMeteo** — immagini Meteosat di [EUMETSAT](https://www.eumetsat.int/) come distribuite dall'[Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/meteo/dati-osservati/satelliti/) (GeoColour 1 km + visibile alta risoluzione 500 m).
- **Osservazioni ItaliaMeteo** — [Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/meteo/dati-osservati/stazioni-al-suolo/), misure reali delle stazioni al suolo (temperatura, umidità, vento, pioggia) dall'API aperta [MeteoHub](https://meteohub.agenziaitaliameteo.it/) (solo stazioni a licenza CC BY 4.0, aggiornamento orario).
- **Meteo** — [Open-Meteo](https://open-meteo.com/) (modelli ECMWF), nostra elaborazione per il Lazio e Genzano di Roma.
- **Previsioni ItaliaMeteo** — [Agenzia nazionale per la meteorologia e climatologia «ItaliaMeteo»](https://www.agenziaitaliameteo.it/), modello ICON-2I (con Arpae Emilia-Romagna e CINECA): temperatura, pioggia, neve, vento, nuvole, umidità, pressione, zero termico. Cartine WMS dalla piattaforma [MeteoHub](https://meteohub.agenziaitaliameteo.it/), licenza CC BY 4.0. Aggiornate **due volte al giorno** (corse delle 00 e 12 UTC), orizzonte 72 ore.
- **Mare ItaliaMeteo** — [Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/mare/), modello d'onda WW3 MEDITA: altezza e periodo delle onde sui mari italiani (CC BY 4.0).
- **Allerta** — [Centro Funzionale Regionale del Lazio](https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti).
- **Incendi** — [EFFIS — Copernicus EMS](https://forest-fire.emergency.copernicus.eu/): focolai attivi rilevati dai satelliti VIIRS e MODIS, su base satellitare.
- **Aria e pollini** — [Open-Meteo Air Quality](https://open-meteo.com/) (dati europei [Copernicus CAMS](https://atmosphere.copernicus.eu/)): indice AQI europeo, PM10, PM2.5, ozono, pollini.
- **Mare** — [Open-Meteo Marine](https://open-meteo.com/): altezza e periodo onde sulla costa laziale.

> La scheda **Terremoti** ha lo switch **Italia / Castelli Romani**: la vista locale mostra la sismicità del distretto vulcanico dei Colli Albani, su cui sorge Genzano di Roma.

<!-- cache-bust: 2026-05-28-fix-terremoti-leaflet-pixelbounds — forza re-upload FTP -->
