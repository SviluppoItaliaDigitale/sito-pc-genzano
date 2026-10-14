---
title: "Cruscotto del territorio"
description: "Cruscotto multidisciplinare in tempo reale: terremoti e vulcani (INGV), radar pioggia, satellite, meteo, allerta, incendi, aria e mare, in un'unica pagina."
layout: "single"
tts: false
toc: false
aliases:
  - /dashboard/
---

Un'unica pagina per consultare i dati di rischio del territorio, da **fonti ufficiali e aperte**. Scegli il tema con i pulsanti qui sotto. Sono dati **indicativi**: per le allerte valgono i bollettini del [Centro Funzionale Regionale del Lazio](https://www.regione.lazio.it/protezione-civile/bollettini-allertamenti), in emergenza chiama il **112**.

Sotto ogni scheda c'è la sua **spiegazione a parole**: che cosa mostra, come si leggono i colori e i simboli, ogni quanto si aggiorna e che cosa non dice. Le spiegazioni di tutte le schede, insieme a quelle dei grafici del Laboratorio meteo, sono raccolte anche in una pagina sola, da leggere o ascoltare: [Le mappe e i grafici spiegati a parole](/cruscotto/mappe-raccontate/).

<div class="cruscotto-callout" role="note"><i class="bi bi-graph-up-arrow" aria-hidden="true"></i> <span>Vuoi <strong>esplorare i dati nel tempo</strong>? Nel <a href="/laboratorio-meteo/">Laboratorio meteo</a> costruisci grafici di temperatura, pioggia e vento dei Castelli Romani, con tabella dei dati e download.</span></div>

<div class="cruscotto-switch" role="tablist" aria-label="Temi del cruscotto">
  <button type="button" class="cruscotto-tab" id="tab-terremoti" data-panel="terremoti" role="tab" aria-selected="true" aria-controls="panel-terremoti" tabindex="0"><i class="bi bi-activity" aria-hidden="true"></i> Terremoti</button>
  <button type="button" class="cruscotto-tab" id="tab-vulcani" data-panel="vulcani" role="tab" aria-selected="false" aria-controls="panel-vulcani" tabindex="-1"><i class="bi bi-triangle" aria-hidden="true"></i> Vulcani</button>
  <button type="button" class="cruscotto-tab" id="tab-radar" data-panel="radar" role="tab" aria-selected="false" aria-controls="panel-radar" tabindex="-1"><i class="bi bi-cloud-rain-heavy" aria-hidden="true"></i> Radar pioggia</button>
  <button type="button" class="cruscotto-tab" id="tab-radar-im" data-panel="radar-im" role="tab" aria-selected="false" aria-controls="panel-radar-im" tabindex="-1"><i class="bi bi-cloud-rain-heavy-fill" aria-hidden="true"></i> Radar ItaliaMeteo</button>
  <button type="button" class="cruscotto-tab" id="tab-satellite" data-panel="satellite" role="tab" aria-selected="false" aria-controls="panel-satellite" tabindex="-1"><i class="bi bi-globe-europe-africa" aria-hidden="true"></i> Satellite (EUMETSAT)</button>
  <button type="button" class="cruscotto-tab" id="tab-satellite-im" data-panel="satellite-im" role="tab" aria-selected="false" aria-controls="panel-satellite-im" tabindex="-1"><i class="bi bi-globe2" aria-hidden="true"></i> Satellite ItaliaMeteo</button>
  <button type="button" class="cruscotto-tab" id="tab-meteo" data-panel="meteo" role="tab" aria-selected="false" aria-controls="panel-meteo" tabindex="-1"><i class="bi bi-cloud-sun" aria-hidden="true"></i> Meteo</button>
  <button type="button" class="cruscotto-tab" id="tab-previsioni-im" data-panel="previsioni-im" role="tab" aria-selected="false" aria-controls="panel-previsioni-im" tabindex="-1"><i class="bi bi-cloud-sun-fill" aria-hidden="true"></i> Previsioni ItaliaMeteo</button>
  <button type="button" class="cruscotto-tab" id="tab-ecmwf" data-panel="ecmwf" role="tab" aria-selected="false" aria-controls="panel-ecmwf" tabindex="-1"><i class="bi bi-globe-europe-africa" aria-hidden="true"></i> Meteo Europa (ECMWF)</button>
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

{{< mappa-raccontata id="terremoti" >}}

</div>

<div class="cruscotto-panel" id="panel-vulcani" data-panel="vulcani" role="tabpanel" aria-labelledby="tab-vulcani" tabindex="0" hidden>

{{< dashboard-vulcani >}}

{{< mappa-raccontata id="vulcani" >}}

</div>

<div class="cruscotto-panel" id="panel-radar" data-panel="radar" role="tabpanel" aria-labelledby="tab-radar" tabindex="0" hidden>

{{< radar-dpc >}}

{{< mappa-raccontata id="radar" >}}

</div>

<div class="cruscotto-panel" id="panel-radar-im" data-panel="radar-im" role="tabpanel" aria-labelledby="tab-radar-im" tabindex="0" hidden>

{{< dashboard-italiameteo-radar >}}

{{< mappa-raccontata id="radar-im" >}}

</div>

<div class="cruscotto-panel" id="panel-satellite" data-panel="satellite" role="tabpanel" aria-labelledby="tab-satellite" tabindex="0" hidden>

{{< dashboard-satellite >}}

{{< mappa-raccontata id="satellite" >}}

</div>

<div class="cruscotto-panel" id="panel-satellite-im" data-panel="satellite-im" role="tabpanel" aria-labelledby="tab-satellite-im" tabindex="0" hidden>

{{< dashboard-italiameteo-satellite >}}

{{< mappa-raccontata id="satellite-im" >}}

</div>

<div class="cruscotto-panel" id="panel-meteo" data-panel="meteo" role="tabpanel" aria-labelledby="tab-meteo" tabindex="0" hidden>

{{< meteo-lazio >}}

{{< mappa-raccontata id="meteo" >}}

</div>

<div class="cruscotto-panel" id="panel-previsioni-im" data-panel="previsioni-im" role="tabpanel" aria-labelledby="tab-previsioni-im" tabindex="0" hidden>

{{< dashboard-italiameteo >}}

{{< mappa-raccontata id="previsioni-im" >}}

</div>

<div class="cruscotto-panel" id="panel-ecmwf" data-panel="ecmwf" role="tabpanel" aria-labelledby="tab-ecmwf" tabindex="0" hidden>

{{< dashboard-ecmwf >}}

{{< mappa-raccontata id="ecmwf" >}}

</div>

<div class="cruscotto-panel" id="panel-obs-im" data-panel="obs-im" role="tabpanel" aria-labelledby="tab-obs-im" tabindex="0" hidden>

{{< dashboard-italiameteo-osservazioni >}}

{{< mappa-raccontata id="obs-im" >}}

</div>

<div class="cruscotto-panel" id="panel-allerta" data-panel="allerta" role="tabpanel" aria-labelledby="tab-allerta" tabindex="0" hidden>

{{< allerta-stato-attuale >}}

{{< mappa-raccontata id="allerta" >}}

</div>

<div class="cruscotto-panel" id="panel-incendi" data-panel="incendi" role="tabpanel" aria-labelledby="tab-incendi" tabindex="0" hidden>

{{< dashboard-incendi >}}

{{< mappa-raccontata id="incendi" >}}

</div>

<div class="cruscotto-panel" id="panel-aria" data-panel="aria" role="tabpanel" aria-labelledby="tab-aria" tabindex="0" hidden>

{{< dashboard-aria >}}

{{< mappa-raccontata id="aria" >}}

</div>

<div class="cruscotto-panel" id="panel-aria-cams" data-panel="aria-cams" role="tabpanel" aria-labelledby="tab-aria-cams" tabindex="0" hidden>

{{< dashboard-cams >}}

{{< mappa-raccontata id="aria-cams" >}}

</div>

<div class="cruscotto-panel" id="panel-ems" data-panel="ems" role="tabpanel" aria-labelledby="tab-ems" tabindex="0" hidden>

{{< dashboard-ems >}}

{{< mappa-raccontata id="ems" >}}

</div>

<div class="cruscotto-panel" id="panel-mare" data-panel="mare" role="tabpanel" aria-labelledby="tab-mare" tabindex="0" hidden>

{{< dashboard-mare >}}

{{< mappa-raccontata id="mare" >}}

</div>

<div class="cruscotto-panel" id="panel-mare-im" data-panel="mare-im" role="tabpanel" aria-labelledby="tab-mare-im" tabindex="0" hidden>

{{< dashboard-italiameteo-mare >}}

{{< mappa-raccontata id="mare-im" >}}

</div>

<script>
(function(){
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.cruscotto-switch .cruscotto-tab'));
  var panels = document.querySelectorAll('.cruscotto-panel');
  var nomi = tabs.map(function(t){ return t.dataset.panel; });
  function show(name, focus, scrivi){
    tabs.forEach(function(t){
      var on = t.dataset.panel === name;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
    });
    panels.forEach(function(p){ p.hidden = (p.dataset.panel !== name); });
    // l'indirizzo dice quale scheda è aperta, così si può condividere o tornarci
    // dalla pagina delle mappe spiegate a parole (#panel-<scheda>)
    if (scrivi !== false && window.history && history.replaceState) {
      try { history.replaceState(null, '', '#panel-' + name); } catch (e) {}
    }
    // le mappe Leaflet nascoste hanno dimensione 0: un resize le ridisegna
    window.dispatchEvent(new Event('resize'));
    // init lazy della scheda mostrata (terremoti, satellite, ...)
    window.dispatchEvent(new Event('cruscotto:' + name));
  }
  // scheda chiesta dall'indirizzo: #panel-<scheda> oppure #<scheda>
  function dallIndirizzo(){
    var h = (location.hash || '').replace(/^#/, '').replace(/^panel-/, '');
    return nomi.indexOf(h) >= 0 ? h : null;
  }
  var iniziale = dallIndirizzo();
  if (iniziale && iniziale !== nomi[0]) {
    show(iniziale, false, false);
    var sw = document.querySelector('.cruscotto-switch');
    if (sw && sw.scrollIntoView) sw.scrollIntoView();
  }
  window.addEventListener('hashchange', function(){
    var n = dallIndirizzo();
    if (n) show(n, false, false);
  });
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

## La lettura ragionata dei dati

I dati live di questa pagina dicono *cosa sta succedendo adesso*. Per il quadro d'insieme — rischio per rischio, con la fase attuale del ciclo di protezione civile e la fonte di ogni valutazione — consulta [Lo stato del territorio](/stato-del-territorio/).

## Le fonti del cruscotto

- **Terremoti** — [INGV](https://terremoti.ingv.it/) (Istituto Nazionale di Geofisica e Vulcanologia), servizio FDSN open data, ultimi 7 giorni in Italia.
- **Vulcani** — [INGV](https://terremoti.ingv.it/): sismicità degli ultimi 30 giorni nel Distretto Vulcanico dei Colli Albani, il vulcano quiescente su cui sorge Genzano di Roma.
- **Radar pioggia** — [Radar-DPC](https://mappe.protezionecivile.gov.it/it/mappe-e-dashboard-rischi/piattaforma-radar/) (Dipartimento della Protezione Civile), servizi WMTS open data.
- **Radar ItaliaMeteo** — [Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/meteo/dati-osservati/radar/) (prodotto SRI, intensità di pioggia al suolo), cartine WMS da [MeteoHub](https://meteohub.agenziaitaliameteo.it/), elaborate dai radar della rete nazionale del Dipartimento della Protezione Civile, licenza CC BY-SA. Complementare al radar DPC.
- **Satellite (EUMETSAT)** — [EUMETSAT](https://www.eumetsat.int/) (Meteosat, nuvole a colori naturali aggiornate ogni 10 minuti), [Copernicus](https://www.copernicus.eu/) (mosaico a colori naturali del giorno dei satelliti Sentinel-3A e 3B, circa 300 metri, con l'elenco delle scene usate dal catalogo pubblico, il prossimo passaggio diurno calcolato dalle effemeridi [CelesTrak](https://celestrak.org/) le mappature d'emergenza Copernicus EMS attive in Italia e il confronto «prima e dopo» fra due giorni a scelta con una linea che si trascina sulla cartina, con Sentinel-3 dal 2020, NASA VIIRS dal 2012 o Sentinel-2 a 10 metri sulle ultime scene poco nuvolose di 16 km attorno a Genzano, dall'archivio pubblico Copernicus sul programma AWS Open Data) e [NASA GIBS](https://worldview.earthdata.nasa.gov/) (immagine true-color del giorno dal satellite NOAA-21, pioggia stimata GPM IMERG ogni 30 minuti, luci notturne NOAA-20, e i livelli tematici con legenda scritta: alluvioni viste dal satellite, neve, umidità del suolo, temperatura del suolo, vegetazione, polveri e fumo); dalle scene Sentinel-2 anche gli indici di vegetazione, acqua e aree bruciate e la mappa dei cambiamenti fra le due scene più recenti, con le superfici in ettari; con le chiavi dell'account Copernicus del Gruppo anche le misure Sentinel-3 (temperatura della superficie a Genzano, fuochi attivi nel Lazio, clorofilla e torbidità dei laghi Albano e di Nemi), l'ultima immagine radar Sentinel-1 di 30 km attorno a Genzano e la mappa dei cambiamenti radar rispetto al passaggio precedente sulla stessa orbita. Indici e cambiamenti sono indizi calcolati con soglie dichiarate, da verificare sul posto.
- **Satellite ItaliaMeteo** — immagini Meteosat lette direttamente da [EUMETSAT](https://www.eumetsat.int/) (GeoColour a circa 1 km e canale visibile a 500 m); l'[Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/meteo/dati-osservati/satelliti/) pubblica sul suo sito le immagini Meteosat dell'Italia e dell'Europa.
- **Osservazioni ItaliaMeteo** — [Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/meteo/dati-osservati/stazioni-al-suolo/), misure reali delle stazioni al suolo delle reti regionali (temperatura, umidità, vento, pioggia) dall'API aperta [MeteoHub](https://meteohub.agenziaitaliameteo.it/) (solo stazioni a licenza CC BY 4.0, aggiornamento orario).
- **Meteo** — [Open-Meteo](https://open-meteo.com/), che per ogni punto sceglie da sé i modelli meteorologici più adatti: nostra elaborazione per il Lazio e Genzano di Roma.
- **Previsioni ItaliaMeteo** — [Agenzia nazionale per la meteorologia e climatologia «ItaliaMeteo»](https://www.agenziaitaliameteo.it/), modello ICON-2I (con Arpae Emilia-Romagna e CINECA): temperatura, pioggia, neve, vento, nuvole, umidità, pressione, zero termico. Cartine WMS dalla piattaforma [MeteoHub](https://meteohub.agenziaitaliameteo.it/), licenza CC BY 4.0. Il modello riparte **due volte al giorno**, dai dati delle 00 e delle 12 UTC, e ogni corsa copre le 72 ore successive.
- **Meteo Europa (ECMWF)** — [ECMWF OpenCharts](https://charts.ecmwf.int/), carte di previsione sinottiche a medio termine del Centro europeo per le previsioni meteo (pressione e vento, temperatura, precipitazioni, temporali). Dato pienamente aperto con licenza CC BY 4.0; le carte sono **auto-ospitate** dal nostro sito e aggiornate automaticamente. Quadro generale europeo, complementare alle previsioni locali Open-Meteo/ItaliaMeteo.
- **Mare ItaliaMeteo** — [Agenzia ItaliaMeteo](https://www.agenziaitaliameteo.it/mare/), modello d'onda WW3 MEDITA: altezza e periodo delle onde sui mari italiani (CC BY 4.0).
- **Allerta** — [Centro Funzionale Regionale del Lazio](https://www.regione.lazio.it/protezione-civile/centro-funzionale-regionale/bollettini-criticita-idrogeologica-idraulica), bollettino di criticità idrogeologica e idraulica per la Zona F, quella di Genzano di Roma.
- **Incendi** — [EFFIS](https://forest-fire.emergency.copernicus.eu/) e [GWIS](https://gwis.jrc.ec.europa.eu/), i sistemi d'informazione sugli incendi del programma europeo Copernicus: anomalie di calore rilevate dai satelliti MODIS e VIIRS negli ultimi 7 giorni.
- **Aria e pollini** — [Open-Meteo Air Quality](https://open-meteo.com/) (dati europei [Copernicus CAMS](https://atmosphere.copernicus.eu/)): indice AQI europeo, PM10, PM2.5, ozono, pollini su Genzano; mappe di previsione di [ARPA Lazio](https://qa.arpalazio.net/) (modello FARM).
- **Aria Europa (CAMS)** — [Copernicus Atmosphere Monitoring Service](https://atmosphere.copernicus.eu/), mappe di previsione servite dal Centro europeo ECMWF: polveri sottili PM10 e PM2.5, ozono, biossido di azoto, biossido di zolfo, polveri del deserto.
- **Emergenze EU (EMS)** — [Copernicus Emergency Management Service](https://emergency.copernicus.eu/), servizio di mappatura rapida: le attivazioni recenti in Europa e nel mondo, con il tipo di evento e lo stato.
- **Mare** — [Open-Meteo Marine](https://open-meteo.com/): altezza, periodo e provenienza delle onde al largo di Anzio-Nettuno; lo stato del mare a parole è calcolato da noi con la scala Douglas.

> La scheda **Terremoti** ha lo switch **Italia / Castelli Romani**: la vista locale mostra la sismicità del distretto vulcanico dei Colli Albani, su cui sorge Genzano di Roma.

<!-- cache-bust: 2026-05-28-fix-terremoti-leaflet-pixelbounds — forza re-upload FTP -->
<!-- cache-bust: 2026-05-28T17:15 preferCanvas fix -->
<!-- cache-bust: 2026-05-28T17:24 render-defensive -->
<!-- cache-bust: 2026-05-28T18:00 filtro-italia + divIcon -->
<!-- cache-bust: 2026-05-28T18:30 tabella-terremoti -->
<!-- cache-bust: 2026-05-28T18:40 stack verticale -->
<!-- cache-bust: 2026-05-28T19:00 allineamento header tabella -->
