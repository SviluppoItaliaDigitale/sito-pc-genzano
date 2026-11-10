/* Cartina e previsioni meteo per l'Italia.
   Dati: Open-Meteo (CC BY 4.0). Sintassi ECMAScript 2018 (LIM / Chrome 64). */
(function () {
  'use strict';

  var API = 'https://api.open-meteo.com/v1/forecast';
  var TZ = 'Europe/Rome';
  var PASSO = 0.6;
  var LAT_MIN = 36.0, LAT_MAX = 47.2, LON_MIN = 6.4, LON_MAX = 18.8;
  var BATCH = 50;
  var GENZANO = { nome: 'Genzano di Roma', lat: 41.7085, lon: 12.6916 };

  var COMUNI_CASTELLI = [
    { nome: 'Frascati', lat: 41.8081, lon: 12.6812, allinea: 's', off: [0, 0], priorita: 1 },
    { nome: 'Marino', lat: 41.7706, lon: 12.6611, allinea: 'nw', off: [0, 0], priorita: 2 },
    { nome: 'Rocca di Papa', lat: 41.7619, lon: 12.7097, allinea: 'e', off: [0, 0], priorita: 3 },
    { nome: 'Castel Gandolfo', lat: 41.7464, lon: 12.6519, allinea: 'w', off: [0, 0], priorita: 4 },
    { nome: 'Albano Laziale', etichetta: 'Albano', lat: 41.7264, lon: 12.6590, allinea: 'w', off: [-10, -10], priorita: 5 },
    { nome: 'Ariccia', lat: 41.7208, lon: 12.6716, allinea: 's', off: [8, 12], priorita: 6 },
    { nome: 'Nemi', lat: 41.7217, lon: 12.7150, allinea: 'e', off: [0, 0], priorita: 7 },
    { nome: 'Genzano di Roma', etichetta: 'Genzano', lat: 41.7085, lon: 12.6916, allinea: 's', off: [6, 6], evidenziato: true, priorita: 8 },
    { nome: 'Lanuvio', lat: 41.6747, lon: 12.6978, allinea: 's', off: [0, 0], priorita: 9 },
    { nome: 'Velletri', lat: 41.6861, lon: 12.7775, allinea: 's', off: [0, 0], priorita: 10 }
  ];
  var COMUNI_LAZIO = [
    { nome: 'Viterbo', lat: 42.4178, lon: 12.1087, allinea: 's', off: [0, 0], priorita: 1 },
    { nome: 'Rieti', lat: 42.4048, lon: 12.8617, allinea: 's', off: [0, 0], priorita: 2 },
    { nome: 'Civitavecchia', lat: 42.0919, lon: 11.7968, allinea: 'n', off: [0, 0], priorita: 3 },
    { nome: 'Bracciano', lat: 42.1036, lon: 12.1756, allinea: 'e', off: [0, 0], priorita: 4 },
    { nome: 'Roma', lat: 41.9028, lon: 12.4964, allinea: 's', off: [0, 0], priorita: 5 },
    { nome: 'Tivoli', lat: 41.9636, lon: 12.8010, allinea: 'e', off: [15, 15], priorita: 6 },
    { nome: 'Guidonia', lat: 41.9936, lon: 12.7223, allinea: 'n', off: [-15, -15], priorita: 7 },
    { nome: 'Fiumicino', lat: 41.7676, lon: 12.2299, allinea: 'n', off: [0, 0], priorita: 8 },
    { nome: 'Genzano di Roma', etichetta: 'Genzano', lat: 41.7085, lon: 12.6916, allinea: 's', off: [-15, -5], evidenziato: true, priorita: 9 },
    { nome: 'Velletri', lat: 41.6861, lon: 12.7775, allinea: 'e', off: [15, 10], priorita: 10 },
    { nome: 'Latina', lat: 41.4676, lon: 12.9037, allinea: 'e', off: [0, 0], priorita: 11 },
    { nome: 'Anzio', lat: 41.4474, lon: 12.6287, allinea: 's', off: [0, 0], priorita: 12 },
    { nome: 'Frosinone', lat: 41.6398, lon: 13.3515, allinea: 's', off: [0, 0], priorita: 13 },
    { nome: 'Cassino', lat: 41.4901, lon: 13.8306, allinea: 's', off: [0, 0], priorita: 14 },
    { nome: 'Gaeta', lat: 41.2096, lon: 13.5707, allinea: 's', off: [0, 0], priorita: 15 },
    { nome: 'Terracina', lat: 41.2917, lon: 13.2486, allinea: 's', off: [0, 0], priorita: 16 }
  ];
  var COMUNI_ITALIA = [
    { nome: 'Aosta', lat: 45.7370, lon: 7.3201, allinea: 'n', livello: 1, off: [0, -4], off2: [0, 0], priorita: 1 },
    { nome: 'Torino', lat: 45.0703, lon: 7.6869, allinea: 's', livello: 1, off: [0, 0], off2: [0, 0], priorita: 2 },
    { nome: 'Milano', lat: 45.4642, lon: 9.1900, allinea: 'n', livello: 1, off: [0, 0], off2: [0, 0], priorita: 3 },
    { nome: 'Genova', lat: 44.4056, lon: 8.9463, allinea: 'e', livello: 1, off: [0, 0], off2: [0, 0], priorita: 4 },
    { nome: 'Bolzano', lat: 46.4983, lon: 11.3548, allinea: 'n', livello: 1, off: [0, -15], off2: [0, 0], priorita: 5 },
    { nome: 'Trento', lat: 46.0748, lon: 11.1217, allinea: 'w', livello: 1, off: [0, 15], off2: [0, 0], priorita: 6 },
    { nome: 'Venezia', lat: 45.4408, lon: 12.3155, allinea: 's', livello: 1, off: [0, 0], off2: [0, 0], priorita: 7 },
    { nome: 'Trieste', lat: 45.6495, lon: 13.7768, allinea: 's', livello: 1, off: [0, 0], off2: [0, 0], priorita: 8 },
    { nome: 'Bologna', lat: 44.4949, lon: 11.3426, allinea: 'e', livello: 1, off: [0, 0], off2: [0, 0], priorita: 9 },
    { nome: 'Firenze', lat: 43.7696, lon: 11.2558, allinea: 's', livello: 1, off: [0, 0], off2: [0, 0], priorita: 10 },
    { nome: 'Perugia', lat: 43.1107, lon: 12.3908, allinea: 'e', livello: 1, off: [0, 0], off2: [0, 0], priorita: 11 },
    { nome: 'Ancona', lat: 43.6158, lon: 13.5189, allinea: 'w', livello: 1, off: [0, 0], off2: [0, 0], priorita: 12 },
    { nome: 'Roma', lat: 41.9028, lon: 12.4964, allinea: 's', livello: 1, off: [-5, 0], off2: [0, 0], priorita: 13 },
    { nome: 'L\'Aquila', lat: 42.3498, lon: 13.3995, allinea: 's', livello: 1, off: [5, 0], off2: [0, 0], priorita: 14 },
    { nome: 'Campobasso', lat: 41.5603, lon: 14.6627, allinea: 'n', livello: 1, off: [0, -4], off2: [0, 0], priorita: 15 },
    { nome: 'Napoli', lat: 40.8518, lon: 14.2681, allinea: 'w', livello: 1, off: [0, 0], off2: [0, 0], priorita: 16 },
    { nome: 'Bari', lat: 41.1171, lon: 16.8719, allinea: 'w', livello: 1, off: [0, 0], off2: [0, 0], priorita: 17 },
    { nome: 'Potenza', lat: 40.6395, lon: 15.8056, allinea: 's', livello: 1, off: [0, 0], off2: [0, 0], priorita: 18 },
    { nome: 'Catanzaro', lat: 38.9098, lon: 16.5877, allinea: 'e', livello: 1, off: [0, 0], off2: [0, 0], priorita: 19 },
    { nome: 'Palermo', lat: 38.1157, lon: 13.3615, allinea: 's', livello: 1, off: [0, 0], off2: [0, 0], priorita: 20 },
    { nome: 'Cagliari', lat: 39.2238, lon: 9.1217, allinea: 'n', livello: 1, off: [0, 0], off2: [0, 0], priorita: 21 },
    { nome: 'Sassari', lat: 40.7259, lon: 8.5557, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 22 },
    { nome: 'Catania', lat: 37.5079, lon: 15.0830, allinea: 's', livello: 1, off: [0, 0], off2: [0, 0], priorita: 23 },
    { nome: 'Lecce', lat: 40.3515, lon: 18.1750, allinea: 'w', livello: 1, off: [0, 0], off2: [0, 0], priorita: 24 },
    { nome: 'Grosseto', lat: 42.7635, lon: 11.1124, allinea: 'w', livello: 2, off: [0, 0], off2: [0, 0], priorita: 25 },
    { nome: 'Foggia', lat: 41.4622, lon: 15.5446, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 26 },
    { nome: 'Cosenza', lat: 39.2983, lon: 16.2537, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 27 },
    { nome: 'Trapani', lat: 38.0176, lon: 12.5372, allinea: 'n', livello: 2, off: [0, 0], off2: [0, 0], priorita: 28 },
    { nome: 'Verona', lat: 45.4384, lon: 10.9916, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 29 },
    { nome: 'Udine', lat: 46.0711, lon: 13.2346, allinea: 'n', livello: 2, off: [0, 0], off2: [0, 0], priorita: 30 },
    { nome: 'Cuneo', lat: 44.3845, lon: 7.5427, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 31 },
    { nome: 'Pisa', lat: 43.7228, lon: 10.4017, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 32 },
    { nome: 'Rimini', lat: 44.0678, lon: 12.5695, allinea: 'w', livello: 2, off: [0, 0], off2: [0, 0], priorita: 33 },
    { nome: 'Taranto', lat: 40.4644, lon: 17.2470, allinea: 'n', livello: 2, off: [0, 0], off2: [0, 0], priorita: 34 },
    { nome: 'Salerno', lat: 40.6824, lon: 14.7681, allinea: 'e', livello: 2, off: [0, 0], off2: [0, 0], priorita: 35 },
    { nome: 'Latina', lat: 41.4676, lon: 12.9037, allinea: 'n', livello: 2, off: [0, 0], off2: [0, 0], priorita: 36 },
    { nome: 'Viterbo', lat: 42.4178, lon: 12.1087, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 37 },
    { nome: 'Nuoro', lat: 40.3209, lon: 9.3297, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 38 },
    { nome: 'Messina', lat: 38.1938, lon: 15.5540, allinea: 'w', livello: 2, off: [0, 0], off2: [0, 0], priorita: 39 },
    { nome: 'Agrigento', lat: 37.3111, lon: 13.5765, allinea: 's', livello: 2, off: [0, 0], off2: [0, 0], priorita: 40 },
    { nome: 'Belluno', lat: 46.1425, lon: 12.2167, allinea: 'n', livello: 2, off: [0, 0], off2: [0, 0], priorita: 41 },
    { nome: 'Pescara', lat: 42.4618, lon: 14.2160, allinea: 'w', livello: 2, off: [0, 0], off2: [0, 0], priorita: 42 }
  ];
  var NOTA_DOMINIO_LOCALE = 'Anche i modelli a 1,5–2 km risolvono quest\'area in modo approssimativo: un punto della griglia rappresenta qualche chilometro, non il singolo abitato. ICON-2I copre Lazio e Castelli Romani. ICON-D2, AROME, AROME HD e ICON-CH coprono soprattutto il Nord e l\'arco alpino e in genere restano fuori da questa inquadratura.';

  var DOMINI = [
    {
      id: 'italia', nome: 'Italia', titolo: 'Cartina meteo dell\'Italia',
      latMin: 36.0, latMax: 47.2, lonMin: 6.4, lonMax: 18.8,
      passo: 0.6, fade: 0.4, minZoom: 5, maxZoom: 9, maxZoomFit: 7,
      modello: 'ecmwf_ifs', locali: false, laghi: false, hillshade: false, comuni: COMUNI_ITALIA, refLon: 73.2
    },
    {
      id: 'lazio', nome: 'Lazio', titolo: 'Cartina meteo del Lazio',
      latMin: 40.78, latMax: 42.90, lonMin: 11.45, lonMax: 14.15,
      passo: 0.1, fade: 0.08, minZoom: 7, maxZoom: 11, maxZoomFit: 9, refLon: 380,
      modello: 'italia_meteo_arpae_icon_2i', locali: true, laghi: true, hillshade: false, comuni: COMUNI_LAZIO,
      nota: NOTA_DOMINIO_LOCALE
    },
    {
      id: 'castelli', nome: 'Castelli Romani', titolo: 'Cartina meteo dei Castelli Romani',
      latMin: 41.60, latMax: 41.85, lonMin: 12.50, lonMax: 12.85,
      passo: 0.015, fade: 0.015, minZoom: 10, maxZoom: 14, maxZoomFit: 13, refLon: 4000, fit: [[41.645, 12.61], [41.835, 12.82]],
      hillLatMin: 41.55, hillLatMax: 41.95, hillLonMin: 12.40, hillLonMax: 13.00,
      modello: 'italia_meteo_arpae_icon_2i', locali: true, laghi: true, hillshade: true, comuni: COMUNI_CASTELLI,
      nota: NOTA_DOMINIO_LOCALE
    }
  ];
  var dominioId = 'italia';
  var hillshadeImg = null;
  var laghiGeo = null;
  var regioniGeo = null;
  var oraIniziale = null;

  var MODELLI = [
    { id: 'ecmwf_ifs', gruppo: 'globali', nome: 'ECMWF IFS HRES', risoluzione: '9 km', aggiornamento: 'ogni 6 ore', giorni: 15, dominio: 'Italia intera', ente: 'ECMWF' },
    { id: 'ecmwf_ifs025', gruppo: 'globali', nome: 'ECMWF IFS 0,25°', risoluzione: '25 km', aggiornamento: 'ogni 6 ore', giorni: 15, dominio: 'Italia intera', ente: 'ECMWF' },
    { id: 'ecmwf_aifs025_single', gruppo: 'globali', nome: 'ECMWF AIFS', risoluzione: '25 km', aggiornamento: 'ogni 6 ore', giorni: 15, dominio: 'Italia intera', ente: 'ECMWF' },
    { id: 'ncep_gfs_global', gruppo: 'globali', nome: 'NCEP GFS', risoluzione: '13-25 km', aggiornamento: 'ogni 6 ore', giorni: 16, dominio: 'Italia intera', ente: 'NOAA / NCEP' },
    { id: 'ncep_aigfs025', gruppo: 'globali', nome: 'NCEP AIGFS', risoluzione: '25 km', aggiornamento: 'ogni 6 ore', giorni: 16, dominio: 'Italia intera', ente: 'NOAA / NCEP' },
    { id: 'ncep_hgefs025_ensemble_mean', gruppo: 'globali', nome: 'NCEP HGEFS (media ensemble)', risoluzione: '25 km', aggiornamento: 'ogni 6 ore', giorni: 16, dominio: 'Italia intera', ente: 'NOAA / NCEP' },
    { id: 'dwd_icon_global', gruppo: 'globali', nome: 'DWD ICON globale', risoluzione: '11 km', aggiornamento: 'ogni 3 ore', giorni: 7, dominio: 'Italia intera', ente: 'DWD', nota: 'Questo canale classico è annunciato in dismissione il 30 novembre 2026; è disponibile anche la versione nativa.' },
    { id: 'dwd_icon_global_native', gruppo: 'globali', nome: 'DWD ICON globale (nativo)', risoluzione: '11 km', aggiornamento: 'ogni 3 ore', giorni: 7, dominio: 'Italia intera', ente: 'DWD' },
    { id: 'dwd_aicon_global_native', gruppo: 'globali', nome: 'DWD AICON globale (nativo)', risoluzione: '11 km circa', aggiornamento: 'ogni 3-6 ore', giorni: 7, dominio: 'Italia intera', ente: 'DWD' },
    { id: 'meteofrance_arpege_world', gruppo: 'globali', nome: 'Météo-France ARPEGE mondo', risoluzione: '25 km', aggiornamento: 'ogni 6 ore', giorni: 4, dominio: 'Italia intera', ente: 'Météo-France' },
    { id: 'ukmo_global_deterministic_10km', gruppo: 'globali', nome: 'UKMO globale', risoluzione: '10 km', aggiornamento: 'ogni ora (corsa ogni 6 ore)', giorni: 7, dominio: 'Italia intera', ente: 'UK Met Office' },
    { id: 'gem_global', gruppo: 'globali', nome: 'GEM globale', risoluzione: '15 km', aggiornamento: 'ogni 6-12 ore', giorni: 10, dominio: 'Italia intera', ente: 'Servizio meteorologico canadese' },
    { id: 'jma_gsm', gruppo: 'globali', nome: 'JMA GSM', risoluzione: '55 km', aggiornamento: 'ogni 6 ore', giorni: 11, dominio: 'Italia intera', ente: 'JMA' },
    { id: 'cma_grapes_global', gruppo: 'globali', nome: 'CMA GRAPES', risoluzione: '15 km', aggiornamento: 'ogni 6 ore', giorni: 10, dominio: 'Italia intera', ente: 'CMA' },

    { id: 'dwd_icon_eu', gruppo: 'europa', nome: 'DWD ICON-EU', risoluzione: '7 km', aggiornamento: 'ogni 3 ore', giorni: 7, dominio: 'Italia intera (dominio europeo)', ente: 'DWD', nota: 'Canale classico annunciato in dismissione il 30 novembre 2026; è disponibile anche la versione nativa.' },
    { id: 'dwd_icon_eu_native', gruppo: 'europa', nome: 'DWD ICON-EU (nativo)', risoluzione: '7 km', aggiornamento: 'ogni 3 ore', giorni: 7, dominio: 'Italia intera (dominio europeo)', ente: 'DWD' },
    { id: 'meteofrance_arpege_europe', gruppo: 'europa', nome: 'Météo-France ARPEGE Europa', risoluzione: '11 km', aggiornamento: 'ogni 6 ore', giorni: 4, dominio: 'Italia intera (dominio europeo)', ente: 'Météo-France' },
    { id: 'knmi_harmonie_arome_europe', gruppo: 'europa', nome: 'KNMI HARMONIE-AROME Europa', risoluzione: '5,5 km', aggiornamento: 'ogni ora', giorni: 2, dominio: 'Copre il Centro-Nord; la Sicilia e parte del Sud possono restare fuori', ente: 'KNMI' },
    { id: 'dmi_harmonie_arome_europe', gruppo: 'europa', nome: 'DMI HARMONIE-AROME Europa', risoluzione: '2 km', aggiornamento: 'ogni 3 ore', giorni: 2, dominio: 'Copre il Centro-Nord; la Sicilia e parte del Sud possono restare fuori', ente: 'DMI' },
    { id: 'meteoswiss_icon_ch1', gruppo: 'europa', nome: 'MeteoSwiss ICON-CH1', risoluzione: '1 km', aggiornamento: 'ogni 3 ore', giorni: 5, dominio: 'Prevalentemente Nord Italia e arco alpino', ente: 'MeteoSwiss' },
    { id: 'meteoswiss_icon_ch2', gruppo: 'europa', nome: 'MeteoSwiss ICON-CH2', risoluzione: '2 km', aggiornamento: 'ogni 6 ore', giorni: 5, dominio: 'Prevalentemente Nord Italia e arco alpino', ente: 'MeteoSwiss' },
    { id: 'chmi_aladin_central_europe_2km', gruppo: 'europa', nome: 'CHMI ALADIN Europa centrale', risoluzione: '2 km', aggiornamento: 'ogni 6 ore', giorni: 3, dominio: 'Centro-Nord; la Sicilia può restare fuori', ente: 'CHMI' },
    { id: 'geosphere_claef_austria', gruppo: 'europa', nome: 'GeoSphere C-LAEF', risoluzione: '1 km', aggiornamento: 'ogni 3 ore', giorni: 2, dominio: 'Prevalentemente Nord-Est e arco alpino', ente: 'GeoSphere Austria' },

    { id: 'italia_meteo_arpae_icon_2i', gruppo: 'alta', nome: 'ItaliaMeteo ARPAE ICON-2I', risoluzione: '2 km', aggiornamento: 'ogni 12 ore', giorni: 3, dominio: 'Italia intera e Mediterraneo centrale', ente: 'ItaliaMeteo / ARPAE', consigliatoLocali: true, attribuzione: 'ItaliaMeteo-ARPAE ICON-2I, CC BY 4.0', nonDisponibili: ['lifted_index'], nota: 'Licenza CC BY 4.0. Orizzonte circa 72 ore. Il Lifted Index non è fornito da questa fonte.' },
    { id: 'dwd_icon_d2', gruppo: 'alta', nome: 'DWD ICON-D2', risoluzione: '2 km', aggiornamento: 'ogni 3 ore', giorni: 2, dominio: 'Prevalentemente Nord Italia', ente: 'DWD', nota: 'Canale classico annunciato in dismissione il 30 novembre 2026; è disponibile anche la versione nativa.' },
    { id: 'dwd_icon_d2_native', gruppo: 'alta', nome: 'DWD ICON-D2 (nativo)', risoluzione: '2 km', aggiornamento: 'ogni 3 ore', giorni: 2, dominio: 'Prevalentemente Nord Italia', ente: 'DWD' },
    { id: 'meteofrance_arome_france', gruppo: 'alta', nome: 'Météo-France AROME', risoluzione: '2,5 km', aggiornamento: 'ogni 3 ore', giorni: 2, dominio: 'Nord e parte del Centro; Sud e Isole spesso fuori', ente: 'Météo-France' },
    { id: 'meteofrance_arome_france_hd', gruppo: 'alta', nome: 'Météo-France AROME HD', risoluzione: '1,5 km', aggiornamento: 'ogni 3 ore', giorni: 2, dominio: 'Nord e parte del Centro; Sud e Isole spesso fuori', ente: 'Météo-France' }
  ];

  var GRUPPI = {
    globali: 'Modelli globali',
    europa: 'Modelli europei',
    alta: 'Alta risoluzione'
  };

  var VARIABILI = [
    { id: 'tempo_previsto', nome: 'Tempo previsto', unita: '', campi: ['weather_code', 'cloud_cover', 'precipitation', 'snowfall', 'cape', 'showers'], scala: 'tempo', tempo: true, info: 'Pittogramma del tempo all\'ora scelta sulle principali città, con temperatura minima (blu) e massima (rosso) del giorno mostrato, su una cartina pulita. I temporali con grandine (codici 96 e 99) arrivano solo da alcuni modelli.' },
    { id: 'pressure_msl', nome: 'Pressione al livello del mare', unita: 'hPa', campi: ['pressure_msl'], scala: 'mslp' },
    { id: 'precipitation', nome: 'Precipitazioni orarie', unita: 'mm', campi: ['precipitation'], scala: 'prec' },
    { id: 'precipitation_6h', nome: 'Precipitazioni in 6 ore', unita: 'mm', campi: ['precipitation'], scala: 'prec6', derivata: 'somma6' },
    { id: 'temperature_2m', nome: 'Temperatura a 2 metri', unita: '°C', campi: ['temperature_2m'], scala: 'temp' },
    { id: 'dew_point_2m', nome: 'Punto di rugiada a 2 metri', unita: '°C', campi: ['dew_point_2m'], scala: 'temp' },
    { id: 'temperature_850hPa', nome: 'Temperatura a 850 hPa', unita: '°C', campi: ['temperature_850hPa'], scala: 'temp', pressione: true },
    { id: 'temperature_500hPa', nome: 'Temperatura a 500 hPa', unita: '°C', campi: ['temperature_500hPa'], scala: 'temp500', pressione: true },
    { id: 'wind_10m', nome: 'Vento a 10 metri', unita: 'km/h', campi: ['wind_speed_10m', 'wind_direction_10m'], scala: 'vento', vento: { vel: 'wind_speed_10m', dir: 'wind_direction_10m' } },
    { id: 'wind_gusts_10m', nome: 'Raffiche a 10 metri', unita: 'km/h', campi: ['wind_gusts_10m'], scala: 'vento' },
    { id: 'wind_850hPa', nome: 'Vento a 850 hPa', unita: 'km/h', campi: ['wind_speed_850hPa', 'wind_direction_850hPa'], scala: 'vento', pressione: true, vento: { vel: 'wind_speed_850hPa', dir: 'wind_direction_850hPa' } },
    { id: 'wind_700hPa', nome: 'Vento a 700 hPa', unita: 'km/h', campi: ['wind_speed_700hPa', 'wind_direction_700hPa'], scala: 'vento', pressione: true, vento: { vel: 'wind_speed_700hPa', dir: 'wind_direction_700hPa' } },
    { id: 'wind_500hPa', nome: 'Vento a 500 hPa', unita: 'km/h', campi: ['wind_speed_500hPa', 'wind_direction_500hPa'], scala: 'vento', pressione: true, vento: { vel: 'wind_speed_500hPa', dir: 'wind_direction_500hPa' } },
    { id: 'wind_250hPa', nome: 'Corrente a getto a 250 hPa', unita: 'km/h', campi: ['wind_speed_250hPa', 'wind_direction_250hPa'], scala: 'getto', pressione: true, vento: { vel: 'wind_speed_250hPa', dir: 'wind_direction_250hPa' } },
    { id: 'geopotential_height_700hPa', nome: 'Geopotenziale a 700 hPa', unita: 'm', campi: ['geopotential_height_700hPa'], scala: 'geo700', pressione: true },
    { id: 'geopotential_height_500hPa', nome: 'Geopotenziale a 500 hPa', unita: 'm', campi: ['geopotential_height_500hPa'], scala: 'geo500', pressione: true },
    { id: 'relative_humidity_850hPa', nome: 'Umidità relativa a 850 hPa', unita: '%', campi: ['relative_humidity_850hPa'], scala: 'umidita', pressione: true },
    { id: 'relative_humidity_700hPa', nome: 'Umidità relativa a 700 hPa', unita: '%', campi: ['relative_humidity_700hPa'], scala: 'umidita', pressione: true },
    { id: 'cloud_cover', nome: 'Nuvolosità totale', unita: '%', campi: ['cloud_cover'], scala: 'nubi' },
    { id: 'cloud_cover_low', nome: 'Nuvolosità bassa', unita: '%', campi: ['cloud_cover_low'], scala: 'nubi' },
    { id: 'cape', nome: 'CAPE', unita: 'J/kg', campi: ['cape'], scala: 'cape' },
    { id: 'convective_inhibition', nome: 'Inibizione convettiva (CIN)', unita: 'J/kg', campi: ['convective_inhibition'], scala: 'cin' },
    { id: 'lifted_index', nome: 'Lifted Index', unita: 'K', campi: ['lifted_index'], scala: 'li' },
    { id: 'total_column_integrated_water_vapour', nome: 'Vapore acqueo in colonna', unita: 'kg/m²', campi: ['total_column_integrated_water_vapour'], scala: 'tcwv', info: 'È il vapore integrato in colonna, non il trasporto (IVT), che questa fonte non fornisce.' },
    { id: 'snowfall', nome: 'Neve oraria', unita: 'cm', campi: ['snowfall'], scala: 'neve' },
    { id: 'freezing_level_height', nome: 'Quota dello zero termico', unita: 'm', campi: ['freezing_level_height'], scala: 'zero' }
  ];

  var SPIEGAZIONI = {
    tempo_previsto: 'Questa cartina ti mostra che tempo farà: sole, nuvole, pioggia, temporali o neve. Sulle città vedi anche la temperatura più bassa (in blu) e quella più alta (in rosso) di quel giorno.',
    pressure_msl: 'Qui vedi quanto è «pesante» l\'aria. Dove i valori sono più bassi spesso arrivano nuvole e pioggia. Dove sono più alti il cielo è più spesso sereno.',
    precipitation: 'Questa cartina dice dove cadrà la pioggia o la neve in un\'ora. I colori più intensi vogliono dire più acqua.',
    precipitation_6h: 'Qui vedi quanta pioggia o neve è prevista in sei ore. Serve per capire se l\'acqua si accumula e il terreno può allagarsi.',
    temperature_2m: 'Questa è la temperatura dell\'aria all\'altezza di una persona, quella che sentiamo quando usciamo di casa. I colori caldi indicano caldo, quelli freddi indicano freddo.',
    dew_point_2m: 'Il punto di rugiada dice quanto l\'aria è umida. Se è vicino alla temperatura, l\'aria è molto umida e può formarsi nebbia o afa. Se è molto più basso, l\'aria è secca.',
    temperature_850hPa: 'Qui vedi se l\'aria a circa 1.500 metri di altezza è calda o fredda. Questa aria un po\' più in alto aiuta a capire se arriverà un rialzo o un calo di temperatura anche al suolo.',
    temperature_500hPa: 'Questa è la temperatura molto in alto, a circa 5.500 metri. L\'aria fredda in quota può favorire temporali; l\'aria meno fredda è in genere più tranquilla.',
    wind_10m: 'Qui vedi quanto è forte il vento vicino al suolo, all\'altezza di un palazzo basso, e da che parte tira. I colori più intensi indicano vento più forte.',
    wind_gusts_10m: 'Le raffiche sono i colpi di vento più forti, più intensi del vento medio. Questa cartina ti avvisa se potranno essere molto violente.',
    wind_850hPa: 'Questa è la direzione e la forza del vento a circa 1.500 metri. Mostra come si muove l\'aria un po\' più in alto, che spesso guida le nuvole e le piogge.',
    wind_700hPa: 'Qui vedi il vento a circa 3.000 metri. Serve a capire da dove arriva l\'aria e se porta umidità verso le montagne o verso il mare.',
    wind_500hPa: 'Questa è la corrente dell\'aria a circa 5.500 metri. Indica la «strada» che seguono le aree di maltempo.',
    wind_250hPa: 'La corrente a getto è un vento fortissimo molto in alto, a circa 10.000 metri, dove volano gli aerei. Quando è vicina e ondulata, il tempo a terra può cambiare in fretta.',
    geopotential_height_700hPa: 'Questa cartina mostra le «colline» e le «valli» dell\'aria a circa 3.000 metri. Nelle valli l\'aria gira spesso in modo da favorire nuvole e pioggia; sulle colline il tempo è in genere più stabile.',
    geopotential_height_500hPa: 'Qui vedi la forma delle correnti a circa 5.500 metri. Le grandi «fosse» (valori più bassi) portano spesso aria fredda e maltempo; le «cupole» (valori più alti) portano aria più mite e tempo più stabile.',
    relative_humidity_850hPa: 'Questa cartina dice quanto è piena d\'acqua l\'aria a circa 1.500 metri. Se l\'umidità è alta possono formarsi nubi basse, pioggia o nebbia.',
    relative_humidity_700hPa: 'Qui vedi l\'umidità a circa 3.000 metri. Se è alta, in quota ci sono spesso nubi e può piovere; se è bassa il cielo in alta quota è più pulito.',
    cloud_cover: 'Questa cartina mostra quanto cielo è coperto dalle nuvole, da quelle basse a quelle alte. I colori chiari indicano poco coperto, i grigi più scuri indicano cielo molto nuvoloso.',
    cloud_cover_low: 'Qui vedi solo le nuvole più vicine al suolo, come quelle che coprono le colline o portano pioggerella. Non considera le nuvole molto alte.',
    cape: 'Il CAPE misura quanta «spinta» ha l\'aria calda per salire in alto. Dove i valori sono alti possono nascere nubi a sviluppo verticale e temporali. Non dice da solo se pioverà, ma indica il rischio di temporali forti.',
    convective_inhibition: 'Questa cartina mostra se c\'è un «coperchio» di aria che impedisce ai temporali di partire. Valori più forti significano che l\'aria fa più fatica a salire. Se il coperchio si rompe, i temporali possono essere improvvisi.',
    lifted_index: 'Questo indice dice se l\'aria, salendo, diventa più instabile. I numeri sotto zero indicano che i temporali sono più probabili; i numeri sopra zero indicano un\'atmosfera più tranquilla.',
    total_column_integrated_water_vapour: 'Qui vedi quanta acqua, sotto forma di vapore, c\'è in tutta la colonna d\'aria, dal suolo fino in alto. Più vapore c\'è, più può piovere se arrivano i movimenti giusti.',
    snowfall: 'Questa cartina mostra dove e quanta neve è prevista in un\'ora. I colori più intensi indicano nevicata più abbondante.',
    freezing_level_height: 'Lo zero termico è l\'altezza a cui la temperatura arriva a zero gradi. Se è basso, la neve può arrivare anche in pianura; se è alto, in basso pioverà e la neve resterà solo in montagna.'
  };

  var SCALE = {
    temp: [[-15, 15, 40, 120], [0, 40, 90, 180], [10, 80, 170, 80], [20, 230, 200, 40], [30, 200, 40, 20], [40, 120, 0, 40]],
    temp500: [[-40, 15, 40, 120], [-25, 40, 90, 180], [-15, 80, 170, 80], [0, 230, 200, 40], [10, 200, 40, 20]],
    mslp: [[980, 80, 0, 80], [1000, 40, 80, 180], [1013, 240, 240, 240], [1025, 230, 180, 40], [1040, 160, 40, 20]],
    prec: [[0, 255, 255, 255], [0.2, 200, 230, 255], [1, 80, 160, 230], [3, 20, 80, 180], [8, 80, 0, 140], [20, 40, 0, 60]],
    prec6: [[0, 255, 255, 255], [1, 200, 230, 255], [5, 80, 160, 230], [15, 20, 80, 180], [30, 80, 0, 140], [50, 40, 0, 60]],
    vento: [[0, 235, 235, 245], [15, 150, 200, 150], [30, 230, 210, 40], [50, 220, 120, 20], [80, 160, 20, 30], [120, 90, 0, 40]],
    getto: [[40, 235, 235, 245], [80, 150, 200, 150], [120, 230, 210, 40], [160, 220, 120, 20], [200, 160, 20, 30], [250, 90, 0, 40]],
    geo500: [[5200, 15, 40, 120], [5400, 40, 90, 180], [5600, 240, 240, 240], [5700, 230, 200, 40], [5900, 160, 40, 20]],
    geo700: [[2700, 15, 40, 120], [2900, 40, 90, 180], [3000, 240, 240, 240], [3100, 230, 200, 40], [3300, 160, 40, 20]],
    umidita: [[0, 230, 200, 120], [40, 240, 240, 200], [70, 80, 170, 80], [90, 20, 80, 160], [100, 10, 40, 100]],
    nubi: [[0, 250, 250, 252], [30, 200, 210, 220], [60, 150, 160, 175], [80, 110, 120, 135], [100, 70, 75, 85]],
    cape: [[0, 255, 255, 255], [200, 255, 240, 140], [500, 240, 180, 40], [1000, 220, 80, 20], [2000, 140, 0, 40]],
    cin: [[-400, 90, 0, 40], [-200, 200, 80, 20], [-50, 240, 200, 80], [0, 255, 255, 255]],
    li: [[-8, 140, 0, 40], [-4, 220, 80, 20], [0, 240, 220, 80], [4, 200, 230, 255], [8, 255, 255, 255]],
    tcwv: [[5, 255, 255, 230], [15, 180, 220, 160], [25, 80, 160, 200], [35, 40, 60, 160], [50, 40, 0, 80]],
    neve: [[0, 255, 255, 255], [0.1, 200, 220, 255], [0.5, 140, 180, 255], [1, 80, 120, 230], [3, 40, 60, 180]],
    zero: [[0, 40, 80, 180], [500, 80, 160, 200], [1500, 240, 240, 200], [2500, 230, 160, 40], [3500, 160, 40, 20]]
  };

  var CITTA = [
    { id: 'genzano', nome: 'Genzano di Roma', lat: 41.7085, lon: 12.6916, locale: true },
    { id: 'roma', nome: 'Roma', lat: 41.9028, lon: 12.4964 },
    { id: 'milano', nome: 'Milano', lat: 45.4642, lon: 9.1900 },
    { id: 'torino', nome: 'Torino', lat: 45.0703, lon: 7.6869 },
    { id: 'venezia', nome: 'Venezia', lat: 45.4408, lon: 12.3155 },
    { id: 'bologna', nome: 'Bologna', lat: 44.4949, lon: 11.3426 },
    { id: 'firenze', nome: 'Firenze', lat: 43.7696, lon: 11.2558 },
    { id: 'genova', nome: 'Genova', lat: 44.4056, lon: 8.9463 },
    { id: 'napoli', nome: 'Napoli', lat: 40.8518, lon: 14.2681 },
    { id: 'bari', nome: 'Bari', lat: 41.1171, lon: 16.8719 },
    { id: 'palermo', nome: 'Palermo', lat: 38.1157, lon: 13.3615 },
    { id: 'cagliari', nome: 'Cagliari', lat: 39.2238, lon: 9.1217 },
    { id: 'bolzano', nome: 'Bolzano', lat: 46.4983, lon: 11.3548, soloScheda: true },
    { id: 'trieste', nome: 'Trieste', lat: 45.6495, lon: 13.7768 },
    { id: 'ancona', nome: 'Ancona', lat: 43.6158, lon: 13.5189, soloScheda: true },
    { id: 'perugia', nome: 'Perugia', lat: 43.1107, lon: 12.3908, soloScheda: true },
    { id: 'catania', nome: 'Catania', lat: 37.5079, lon: 15.0830 },
    { id: 'reggio', nome: 'Reggio Calabria', lat: 38.1113, lon: 15.6471, soloScheda: true }
  ];

  var CODICI = {
    0: 'Sereno', 1: 'Prevalentemente sereno', 2: 'Parzialmente nuvoloso', 3: 'Coperto',
    45: 'Nebbia', 48: 'Nebbia con brina',
    51: 'Pioviggine debole', 53: 'Pioviggine moderata', 55: 'Pioviggine intensa',
    56: 'Pioviggine gelata debole', 57: 'Pioviggine gelata intensa',
    61: 'Pioggia debole', 63: 'Pioggia moderata', 65: 'Pioggia intensa',
    66: 'Pioggia gelata debole', 67: 'Pioggia gelata intensa',
    71: 'Neve debole', 73: 'Neve moderata', 75: 'Neve intensa', 77: 'Granuli di neve',
    80: 'Rovesci deboli', 81: 'Rovesci moderati', 82: 'Rovesci intensi',
    85: 'Rovesci di neve deboli', 86: 'Rovesci di neve intensi',
    95: 'Temporale', 96: 'Temporale con grandine debole', 97: 'Temporale intenso', 99: 'Temporale con grandine intensa'
  };

  var INTERVALLO_AGGIORNAMENTO = 45 * 60 * 1000;
  var VELOCITA_BASE = 900;
  var FATTORI_VELOCITA = [0.25, 0.5, 1, 1.5, 2];
  var fattoreVelocita = 1;
  var iconeTempo = {};
  var campiTempoPerModello = {};

  var LEGENDA_TEMPO = [
    { id: 'sole', nome: 'Sole' },
    { id: 'poco-nuvoloso', nome: 'Poco nuvoloso' },
    { id: 'nuvoloso', nome: 'Nuvoloso' },
    { id: 'coperto', nome: 'Coperto' },
    { id: 'nebbia', nome: 'Nebbia' },
    { id: 'pioggerella', nome: 'Pioggerella' },
    { id: 'pioggia-debole', nome: 'Pioggia debole' },
    { id: 'pioggia-moderata', nome: 'Pioggia moderata' },
    { id: 'pioggia-forte', nome: 'Pioggia forte' },
    { id: 'rovesci', nome: 'Rovesci' },
    { id: 'temporale', nome: 'Temporale' },
    { id: 'temporale-grandine', nome: 'Temporale con grandine' },
    { id: 'neve', nome: 'Neve' },
    { id: 'pioggia-gelata', nome: 'Nevischio o pioggia gelata' }
  ];
  var COLORI_TEMPO = {
    'sole': [255, 228, 120],
    'poco-nuvoloso': [255, 240, 185],
    'nuvoloso': [210, 220, 232],
    'coperto': [160, 172, 186],
    'nebbia': [196, 202, 208],
    'pioggerella': [176, 210, 232],
    'pioggia-debole': [140, 184, 222],
    'pioggia-moderata': [90, 140, 200],
    'pioggia-forte': [48, 88, 158],
    'rovesci': [70, 118, 198],
    'temporale': [124, 100, 172],
    'temporale-grandine': [176, 78, 128],
    'neve': [226, 238, 255],
    'pioggia-gelata': [166, 210, 220]
  };

  var cache = {};
  var nonDisponibili = {};
  var statoMappa = { punti: [], orari: [], indice: 0, variabile: null, modello: null, scaricatoIl: null, matrice: null };
  var statoMappaB = { punti: [], orari: [], indice: 0, variabile: null, modello: null, scaricatoIl: null, matrice: null };
  var mappa, mappaB, mappaCitta, strato, stratoB, timerPlay = null, datiCitta = null, markerGenzano = null, markerGenzanoB = null;
  var geojson = null, timerRefresh = null, ultimoAggiornamento = null, syncing = false, ventoRaf = null;
  var particelle = [];
  var prontoRisovi = null;
  var prontoPromessa = new Promise(function (r) { prontoRisovi = r; });
  var esportazioneInCorso = false;

  function $(id) { return document.getElementById(id); }
  function modelloById(id) {
    for (var i = 0; i < MODELLI.length; i++) if (MODELLI[i].id === id) return MODELLI[i];
    return MODELLI[0];
  }
  function variabileById(id) {
    for (var i = 0; i < VARIABILI.length; i++) if (VARIABILI[i].id === id) return VARIABILI[i];
    return VARIABILI[0];
  }
  function dominioById(id) {
    for (var i = 0; i < DOMINI.length; i++) if (DOMINI[i].id === id) return DOMINI[i];
    return DOMINI[0];
  }
  function dominioCorrente() { return dominioById(dominioId); }
  function applicaDominio(d) {
    if (!d) d = dominioCorrente();
    dominioId = d.id;
    LAT_MIN = d.latMin;
    LAT_MAX = d.latMax;
    LON_MIN = d.lonMin;
    LON_MAX = d.lonMax;
    PASSO = d.passo;
  }
  function boundsCampo() {
    return L.latLngBounds([[LAT_MIN, LON_MIN], [LAT_MAX, LON_MAX]]);
  }
  function boundsHillshade(d) {
    if (d && d.hillLatMin != null) {
      return L.latLngBounds([[d.hillLatMin, d.hillLonMin], [d.hillLatMax, d.hillLonMax]]);
    }
    return null;
  }
  function boundsVisibili(d, campo) {
    var hill = boundsHillshade(d);
    return hill || campo.pad(0.45);
  }
  function leggiQuery() {
    var out = {};
    try {
      var p = new URLSearchParams(window.location.search);
      if (p.get('dominio')) out.dominio = p.get('dominio');
      if (p.get('modello')) out.modello = p.get('modello');
      if (p.get('var')) out.var = p.get('var');
      if (p.get('ora')) out.ora = p.get('ora');
    } catch (e) {}
    return out;
  }
  function aggiornaUrl() {
    try {
      var p = new URLSearchParams();
      p.set('dominio', dominioId);
      if ($('cmi-modello') && $('cmi-modello').value) p.set('modello', $('cmi-modello').value);
      if ($('cmi-variabile') && $('cmi-variabile').value) p.set('var', $('cmi-variabile').value);
      var iso = statoMappa.orari && statoMappa.orari[statoMappa.indice];
      if (iso) p.set('ora', iso);
      var url = window.location.pathname + '?' + p.toString();
      if (window.history && window.history.replaceState) window.history.replaceState(null, '', url);
    } catch (e) {}
  }
  function aggiornaNotaDominio() {
    var el = $('cmi-dominio-note');
    if (!el) return;
    var d = dominioCorrente();
    if (d.nota) {
      el.hidden = false;
      el.textContent = d.nota;
    } else {
      el.hidden = true;
      el.textContent = '';
    }
  }
  function arrotonda(x, n) {
    var f = Math.pow(10, n || 0);
    return Math.round(x * f) / f;
  }
  function confrontoAttivo() {
    var el = $('cmi-confronto');
    return el && el.checked;
  }
  function isolineeAttive() {
    var el = $('cmi-isolinee');
    return el && el.checked;
  }
  function particelleAttive() {
    var el = $('cmi-particelle');
    return el && el.checked;
  }
  function motoRidotto() {
    return document.documentElement.classList.contains('a11y-pause-animations') ||
      document.documentElement.classList.contains('a11y-pause-anim') ||
      (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function baseIconeUrl() {
    var base = (leggiConfig().iconeUrl) || '/images/meteo-icone/';
    if (base.charAt(base.length - 1) !== '/') base += '/';
    return base;
  }
  function urlIcona(cat) { return baseIconeUrl() + cat + '.svg'; }
  function categoriaDaCodice(code) {
    if (code === null || typeof code === 'undefined' || isNaN(code)) return null;
    var c = Math.round(code);
    if (c === 0) return 'sole';
    if (c === 1) return 'poco-nuvoloso';
    if (c === 2) return 'nuvoloso';
    if (c === 3) return 'coperto';
    if (c === 45 || c === 48) return 'nebbia';
    if (c === 51 || c === 53 || c === 55) return 'pioggerella';
    if (c === 61) return 'pioggia-debole';
    if (c === 63) return 'pioggia-moderata';
    if (c === 65) return 'pioggia-forte';
    if (c === 80 || c === 81 || c === 82) return 'rovesci';
    if (c === 95 || c === 97) return 'temporale';
    if (c === 96 || c === 99) return 'temporale-grandine';
    if (c === 71 || c === 73 || c === 75 || c === 77 || c === 85 || c === 86) return 'neve';
    if (c === 56 || c === 57 || c === 66 || c === 67) return 'pioggia-gelata';
    return null;
  }
  function raffinaCategoria(cat, snow, showers) {
    if (!cat) return cat;
    if (cat !== 'temporale-grandine' && cat !== 'neve' && cat !== 'temporale' && snow >= 0.2) return 'neve';
    if ((cat === 'pioggia-debole' || cat === 'pioggia-moderata' || cat === 'pioggia-forte') && showers >= 0.2) return 'rovesci';
    return cat;
  }
  function etichettaTempo(code) {
    if (code === null || typeof code === 'undefined') return 'dato non disponibile';
    var c = Math.round(code);
    return (typeof CODICI[c] !== 'undefined') ? CODICI[c] : ('Codice WMO ' + c);
  }
  function htmlIconaTempo(code, cls) {
    var cat = categoriaDaCodice(code);
    if (!cat) return '';
    return '<img class="' + (cls || 'cmi-icona-meteo') + '" src="' + urlIcona(cat) + '" alt="' + etichettaTempo(code) + '" width="32" height="32">';
  }
  function caricaIconeTempo() {
    var base = baseIconeUrl();
    var jobs = LEGENDA_TEMPO.map(function (item) {
      return new Promise(function (resolve) {
        if (iconeTempo[item.id]) { resolve(); return; }
        var img = new Image();
        img.onload = function () { iconeTempo[item.id] = img; resolve(); };
        img.onerror = function () { resolve(); };
        img.src = base + item.id + '.svg';
      });
    });
    return Promise.all(jobs);
  }
  function leggiVelocitaSalvata() {
    try {
      var s = window.localStorage.getItem('cmi-fattore-velocita');
      var n = parseFloat(s);
      if (FATTORI_VELOCITA.indexOf(n) !== -1) fattoreVelocita = n;
    } catch (e) {}
  }
  function salvaVelocita() {
    try { window.localStorage.setItem('cmi-fattore-velocita', String(fattoreVelocita)); }
    catch (e) {}
  }
  function durataFrame() {
    var ms = Math.round(VELOCITA_BASE / (fattoreVelocita || 1));
    if (motoRidotto()) ms = Math.max(ms, 1400);
    return ms;
  }
  function delayGifCs() {
    var cs = Math.round(durataFrame() / 10);
    if (cs < 8) cs = 8;
    if (cs > 200) cs = 200;
    return cs;
  }
  function aggiornaVelocitaUI() {
    var sel = $('cmi-velocita');
    if (sel) sel.value = String(fattoreVelocita);
    var info = $('cmi-velocita-info');
    if (info) info.textContent = durataFrame() + ' ms per fotogramma';
  }
  function impostaFattoreVelocita(n, riavvia) {
    var i, vicino = FATTORI_VELOCITA[0], dist = Infinity, d;
    for (i = 0; i < FATTORI_VELOCITA.length; i++) {
      d = Math.abs(FATTORI_VELOCITA[i] - n);
      if (d < dist) { dist = d; vicino = FATTORI_VELOCITA[i]; }
    }
    fattoreVelocita = vicino;
    salvaVelocita();
    aggiornaVelocitaUI();
    if (riavvia !== false && timerPlay) avviaPlay();
  }
  function cambiaFattore(delta) {
    var i = FATTORI_VELOCITA.indexOf(fattoreVelocita);
    if (i < 0) i = FATTORI_VELOCITA.indexOf(1);
    i += delta;
    if (i < 0) i = 0;
    if (i > FATTORI_VELOCITA.length - 1) i = FATTORI_VELOCITA.length - 1;
    impostaFattoreVelocita(FATTORI_VELOCITA[i]);
  }
  function costruisciGriglia() {
    var punti = [];
    var dec = 2;
    if (PASSO < 0.05) dec = 3;
    if (PASSO < 0.005) dec = 4;
    for (var lat = LAT_MIN; lat <= LAT_MAX + 1e-9; lat += PASSO) {
      for (var lon = LON_MIN; lon <= LON_MAX + 1e-9; lon += PASSO) {
        punti.push({ lat: arrotonda(lat, dec), lon: arrotonda(lon, dec) });
      }
    }
    return punti;
  }
  function coloreDi(val, scalaId) {
    if (val === null || typeof val === 'undefined' || isNaN(val)) return null;
    var stops = SCALE[scalaId] || SCALE.temp;
    if (val <= stops[0][0]) return [stops[0][1], stops[0][2], stops[0][3]];
    var last = stops[stops.length - 1];
    if (val >= last[0]) return [last[1], last[2], last[3]];
    for (var i = 0; i < stops.length - 1; i++) {
      var a = stops[i], b = stops[i + 1];
      if (val >= a[0] && val <= b[0]) {
        var t = (val - a[0]) / (b[0] - a[0] || 1);
        return [
          Math.round(a[1] + (b[1] - a[1]) * t),
          Math.round(a[2] + (b[2] - a[2]) * t),
          Math.round(a[3] + (b[3] - a[3]) * t)
        ];
      }
    }
    return [last[1], last[2], last[3]];
  }
  function gradiente(scalaId) {
    var stops = SCALE[scalaId] || SCALE.temp;
    var parts = [];
    for (var i = 0; i < stops.length; i++) {
      var p = Math.round(i * 100 / (stops.length - 1));
      parts.push('rgb(' + stops[i][1] + ',' + stops[i][2] + ',' + stops[i][3] + ') ' + p + '%');
    }
    return 'linear-gradient(90deg, ' + parts.join(', ') + ')';
  }
  function etichettaScala(scalaId) {
    var stops = SCALE[scalaId] || SCALE.temp;
    return { min: stops[0][0], max: stops[stops.length - 1][0] };
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function formatOra(iso) {
    if (!iso) return '—';
    var p = iso.split('T');
    var d = p[0] ? p[0].split('-') : [];
    var h = p[1] ? p[1].slice(0, 5) : '';
    if (d.length !== 3) return iso;
    return parseInt(d[2], 10) + '/' + d[1] + '/' + d[0] + ', ore ' + h;
  }
  function formatDataBreve(iso) {
    var mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
    var giorni = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
    var p = String(iso).split('T')[0].split('-');
    if (p.length !== 3) return iso;
    var dt = new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
    return giorni[dt.getDay()] + ' ' + parseInt(p[2], 10) + ' ' + mesi[dt.getMonth()];
  }
  function formatEmesso(iso) {
    if (!iso) return '';
    var m = String(iso).match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/);
    if (!m) return iso;
    return parseInt(m[3], 10) + '/' + m[2] + '/' + m[1] + ', ore ' + m[4] + ':' + m[5];
  }
  function formatDataIt(iso) {
    if (!iso) return '';
    var p = String(iso).split('-');
    if (p.length !== 3) return iso;
    return parseInt(p[2], 10) + '/' + p[1] + '/' + p[0];
  }
  function formatDataOraLocale(d) {
    if (!d) return '—';
    return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear() + ', ore ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
  }
  function formatOraCorta(iso) {
    if (!iso) return '';
    var p = iso.split('T');
    var d = p[0] ? p[0].split('-') : [];
    var h = p[1] ? p[1].slice(0, 5) : '';
    return (d[2] || '') + '/' + (d[1] || '') + ' ' + h;
  }

  function impostaStato(msg, errore, loading) {
    var el = $('cmi-stato');
    if (!el) return;
    el.className = 'cmi-stato' + (errore ? ' cmi-stato-errore' : '');
    el.textContent = '';
    if (loading) {
      var sp = document.createElement('span');
      sp.className = 'pc-spinner';
      sp.setAttribute('aria-hidden', 'true');
      el.appendChild(sp);
    }
    el.appendChild(document.createTextNode(msg || ''));
  }

  function popolaSelectModello(sel, valore) {
    var precedente = valore || sel.value;
    sel.textContent = '';
    var locali = dominioCorrente().locali;
    var gruppi = locali ? ['consigliati', 'globali', 'europa', 'alta'] : ['globali', 'europa', 'alta'];
    var etichette = { consigliati: 'Consigliati per quest\'area', globali: GRUPPI.globali, europa: GRUPPI.europa, alta: GRUPPI.alta };
    for (var g = 0; g < gruppi.length; g++) {
      var og = document.createElement('optgroup');
      og.label = etichette[gruppi[g]];
      for (var i = 0; i < MODELLI.length; i++) {
        if (gruppi[g] === 'consigliati') {
          if (!MODELLI[i].consigliatoLocali) continue;
        } else {
          if (MODELLI[i].gruppo !== gruppi[g]) continue;
          if (locali && MODELLI[i].consigliatoLocali) continue;
        }
        var o = document.createElement('option');
        o.value = MODELLI[i].id;
        o.textContent = MODELLI[i].nome + ' — ' + MODELLI[i].risoluzione;
        og.appendChild(o);
      }
      if (og.childNodes.length) sel.appendChild(og);
    }
    if (precedente) sel.value = precedente;
    if (!sel.value) sel.value = dominioCorrente().modello || 'ecmwf_ifs';
  }
  function popolaSelect() {
    var selM = $('cmi-modello');
    var selV = $('cmi-variabile');
    var selB = $('cmi-modello-b');
    var selD = $('cmi-dominio');
    if (!selM || !selV) return;
    if (selD) selD.value = dominioId;
    popolaSelectModello(selM, dominioCorrente().modello || 'ecmwf_ifs');
    if (selB) popolaSelectModello(selB, 'ncep_gfs_global');
    if (!selV.options.length) {
      for (var v = 0; v < VARIABILI.length; v++) {
        var ov = document.createElement('option');
        ov.value = VARIABILI[v].id;
        ov.textContent = VARIABILI[v].nome;
        selV.appendChild(ov);
      }
    }
    selV.value = 'tempo_previsto';
    aggiornaInfoModello();
    aggiornaInfoVariabile();
    aggiornaNotaDominio();
  }
  function applicaParametriUrl() {
    var q = leggiQuery();
    var d = dominioById(q.dominio || 'italia');
    applicaDominio(d);
    var selD = $('cmi-dominio');
    if (selD) selD.value = d.id;
    var predefM = d.modello || 'ecmwf_ifs';
    popolaSelectModello($('cmi-modello'), q.modello || predefM);
    if ($('cmi-modello-b')) popolaSelectModello($('cmi-modello-b'), $('cmi-modello-b').value || 'ncep_gfs_global');
    if (q.var && $('cmi-variabile')) $('cmi-variabile').value = q.var;
    if (q.ora) oraIniziale = q.ora;
    aggiornaInfoModello();
    aggiornaInfoVariabile();
    aggiornaNotaDominio();
  }
  function cambiaDominio(id) {
    var d = dominioById(id);
    var stesso = d.id === dominioId;
    fermaPlay(true);
    applicaDominio(d);
    var modelloAttuale = $('cmi-modello') ? $('cmi-modello').value : '';
    popolaSelectModello($('cmi-modello'), modelloAttuale || d.modello);
    if ($('cmi-modello-b')) popolaSelectModello($('cmi-modello-b'), $('cmi-modello-b').value);
    aggiornaInfoModello();
    aggiornaNotaDominio();
    adattaMappe();
    aggiornaUrl();
    if (stesso) return Promise.resolve();
    var jobs = [caricaGriglia('a')];
    if (confrontoAttivo()) jobs.push(caricaGriglia('b', { mantieniOra: true }));
    return Promise.all(jobs);
  }
  function testoInfoModello(m) {
    var parti = [m.ente, 'risoluzione ' + m.risoluzione, 'orizzonte ' + m.giorni + (m.giorni === 1 ? ' giorno' : ' giorni'), 'aggiornamento ' + m.aggiornamento, m.dominio];
    var txt = parti.join(' · ');
    if (m.nota) txt += ' ' + m.nota;
    return txt;
  }
  function aggiornaInfoModello() {
    var el = $('cmi-modello-info');
    if (el) el.textContent = testoInfoModello(modelloById($('cmi-modello').value));
    var elb = $('cmi-modello-b-info');
    if (elb && $('cmi-modello-b')) elb.textContent = testoInfoModello(modelloById($('cmi-modello-b').value));
    aggiornaAttribuzioneModello();
  }
  function aggiornaInfoVariabile() {
    var v = variabileById($('cmi-variabile').value);
    var el = $('cmi-variabile-info');
    if (el) el.textContent = v.info || '';
    aggiornaSpiegazione(v);
  }
  function aggiornaSpiegazione(v) {
    var titoloEl = $('cmi-spiegazione-titolo');
    var testoEl = $('cmi-spiegazione-testo');
    if (!titoloEl || !testoEl || !v) return;
    titoloEl.textContent = v.nome;
    testoEl.textContent = SPIEGAZIONI[v.id] || 'Questa cartina mostra la grandezza scelta, con i colori della legenda.';
  }
  function applicaNonDisponibiliDichiarati() {
    for (var i = 0; i < MODELLI.length; i++) {
      var elenco = MODELLI[i].nonDisponibili;
      if (!elenco) continue;
      if (!nonDisponibili[MODELLI[i].id]) nonDisponibili[MODELLI[i].id] = {};
      for (var j = 0; j < elenco.length; j++) nonDisponibili[MODELLI[i].id][elenco[j]] = true;
    }
  }
  var attribuzioneExtra = '';
  function aggiornaAttribuzioneModello() {
    var m = modelloById($('cmi-modello').value);
    var txt = (m && m.attribuzione) ? ('Modello: ' + m.attribuzione) : '';
    var maps = [mappa, mappaB];
    for (var i = 0; i < maps.length; i++) {
      if (!maps[i] || !maps[i].attributionControl) continue;
      if (attribuzioneExtra) maps[i].attributionControl.removeAttribution(attribuzioneExtra);
      if (txt) maps[i].attributionControl.addAttribution(txt);
    }
    attribuzioneExtra = txt;
  }
  function testoCreditoModello() {
    var m = (statoMappa && statoMappa.modello) ? statoMappa.modello : modelloById($('cmi-modello').value);
    return (m && m.attribuzione) ? (' ' + m.attribuzione + '.') : '';
  }
  function aggiornaOpzioniVariabile() {
    applicaNonDisponibiliDichiarati();
    var mid = $('cmi-modello').value;
    var blocco = nonDisponibili[mid] || {};
    var sel = $('cmi-variabile');
    var options = sel.options;
    for (var i = 0; i < options.length; i++) {
      var dis = !!blocco[options[i].value];
      options[i].disabled = dis;
      var base = variabileById(options[i].value).nome;
      options[i].textContent = dis ? base + ' (non disponibile in questo modello)' : base;
    }
    if (sel.options[sel.selectedIndex] && sel.options[sel.selectedIndex].disabled) {
      for (var j = 0; j < options.length; j++) {
        if (!options[j].disabled) { sel.value = options[j].value; break; }
      }
      aggiornaInfoVariabile();
    }
  }
  function marcaNonDisponibile(modelId, varId) {
    if (!nonDisponibili[modelId]) nonDisponibili[modelId] = {};
    nonDisponibili[modelId][varId] = true;
    aggiornaOpzioniVariabile();
  }
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      if (window.L) { resolve(); return; }
      var s = document.createElement('script');
      s.src = src;
      s.onload = function () { resolve(); };
      s.onerror = function () { reject(new Error('Impossibile caricare la libreria della mappa.')); };
      document.head.appendChild(s);
    });
  }
  function boundsItalia() {
    return L.latLngBounds([[36.2, 6.6], [47.2, 18.7]]);
  }
  function creaMappaBase(id, conClick) {
    var d = dominioCorrente();
    var campo = boundsCampo();
    var map = L.map(id, {
      scrollWheelZoom: false,
      maxBounds: campo.pad(0.45),
      minZoom: d.minZoom,
      maxZoom: d.maxZoom,
      zoomSnap: 0.25,
      zoomDelta: 0.25,
      zoomControl: true,
      attributionControl: true
    });
    map.attributionControl.setPrefix('');
    map.attributionControl.addAttribution('Confini: <a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a> · Dati: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> CC BY 4.0');
    vistaIniziale(map, d, campo);
    if (conClick) map.on('click', onClickMappa);
    var st = creaStratoCanvas(map);
    map.on('move zoom resize', function () { if (st) st.ridisegna(); });
    return { map: map, strato: st };
  }
  function zoomVistaIniziale(map, d, campo) {
    var b = d.fit ? L.latLngBounds(d.fit) : campo;
    var z = map.getBoundsZoom(b, false, L.point(16, 16));
    if (z > d.maxZoomFit) z = d.maxZoomFit;
    if (z < d.minZoom) z = d.minZoom;
    if (typeof map.options.minZoom === 'number' && z < map.options.minZoom) z = map.options.minZoom;
    return z;
  }
  function vistaIniziale(map, d, campo) {
    var b = d.fit ? L.latLngBounds(d.fit) : campo;
    map.setView(b.getCenter(), zoomVistaIniziale(map, d, campo), { animate: false });
  }
  function adattaMappe() {
    var d = dominioCorrente();
    var campo = boundsCampo();
    function sistema(map) {
      if (!map) return;
      if (map.stop) map.stop();
      map.setMaxBounds(null);
      map.options.minZoom = 0;
      map.options.maxZoom = 20;
      map.invalidateSize();
      var limiti = boundsVisibili(d, campo);
      var zMin = d.minZoom, zMax = d.maxZoom;
      if (boundsHillshade(d)) {
        var zCopre = map.getBoundsZoom(limiti, true, L.point(0, 0));
        if (isFinite(zCopre) && zCopre > zMin) zMin = zCopre;
        if (zMin > zMax) zMin = zMax;
      }
      map.options.minZoom = zMin;
      map.options.maxZoom = zMax;
      vistaIniziale(map, d, campo);
      map.fire('zoomlevelschange');
      map.setMaxBounds(limiti);
    }
    sistema(mappa);
    sistema(mappaB);
    setTimeout(function () { sistema(mappa); sistema(mappaB); }, 120);
  }
  function creaMappe() {
    var a = creaMappaBase('cmi-mappa', true);
    mappa = a.map;
    strato = a.strato;
    var bounds = boundsItalia();
    mappaCitta = L.map('cmi-mappa-citta', { scrollWheelZoom: false, minZoom: 6, maxBounds: bounds.pad(0.5) });
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
    }).addTo(mappaCitta);
    mappaCitta.fitBounds(bounds, { padding: [16, 16], maxZoom: 7 });
    function adatta() {
      adattaMappe();
      if (mappaCitta) { mappaCitta.invalidateSize(); mappaCitta.fitBounds(bounds, { padding: [16, 16], maxZoom: 7 }); }
    }
    setTimeout(adatta, 300);
    setTimeout(adatta, 1200);
  }
  function assicuraMappaB() {
    if (mappaB) {
      setTimeout(function () {
        mappaB.invalidateSize();
        if (mappa) sincronizza(mappa, mappaB);
      }, 80);
      return;
    }
    var b = creaMappaBase('cmi-mappa-b', false);
    mappaB = b.map;
    stratoB = b.strato;
    mappa.on('move', function () { if (confrontoAttivo()) sincronizza(mappa, mappaB); });
    mappaB.on('move', function () { if (confrontoAttivo()) sincronizza(mappaB, mappa); });
    setTimeout(function () {
      mappa.invalidateSize();
      mappaB.invalidateSize();
      sincronizza(mappa, mappaB);
    }, 80);
  }
  function sincronizza(src, dest) {
    if (syncing || !dest) return;
    syncing = true;
    dest.setView(src.getCenter(), src.getZoom(), { animate: false });
    syncing = false;
  }
  function creaStratoCanvas(map) {
    var campo = L.DomUtil.create('canvas', 'cmi-campo-canvas');
    var vento = L.DomUtil.create('canvas', 'cmi-vento-canvas');
    map.getPanes().overlayPane.appendChild(campo);
    map.getPanes().overlayPane.appendChild(vento);
    campo.style.position = 'absolute';
    campo.style.pointerEvents = 'none';
    vento.style.position = 'absolute';
    vento.style.pointerEvents = 'none';
    function layout(cv) {
      var size = map.getSize();
      var b = map.getBounds();
      var topLeft = map.latLngToLayerPoint(b.getNorthWest());
      L.DomUtil.setPosition(cv, topLeft);
      if (cv.width !== size.x) cv.width = size.x;
      if (cv.height !== size.y) cv.height = size.y;
      return { size: size, topLeft: topLeft };
    }
    function proietta(lat, lon, topLeft) {
      var pt = map.latLngToLayerPoint(L.latLng(lat, lon));
      return [pt.x - topLeft.x, pt.y - topLeft.y];
    }
    function inversa(x, y, topLeft) {
      var ll = map.layerPointToLatLng(L.point(x + topLeft.x, y + topLeft.y));
      return { lat: ll.lat, lon: ll.lng };
    }
    function ridisegna() {
      if (!map) return;
      var lay = layout(campo);
      layout(vento);
      var ctx = campo.getContext('2d');
      ctx.clearRect(0, 0, lay.size.x, lay.size.y);
      var stato = (map === mappaB) ? statoMappaB : statoMappa;
      var dVista = dominioCorrente();
      disegnaVista(ctx, {
        w: lay.size.x,
        h: lay.size.y,
        xy: function (lat, lon) { return proietta(lat, lon, lay.topLeft); },
        inv: function (x, y) { return inversa(x, y, lay.topLeft); },
        zoom: map.getZoom(),
        zoomFit: zoomVistaIniziale(map, dVista, boundsCampo())
      }, stato, { frecce: !dovrebbeAnimareVento(stato) });
      if (map !== mappaB) avviaOFermaVento();
    }
    function ridisegnaVento() {
      var lay = layout(vento);
      var ctx = vento.getContext('2d');
      ctx.clearRect(0, 0, lay.size.x, lay.size.y);
      if (!particelleAttive() || motoRidotto()) return;
      disegnaParticelle(ctx, function (lat, lon) { return proietta(lat, lon, lay.topLeft); });
    }
    return { ridisegna: ridisegna, ridisegnaVento: ridisegnaVento, canvasCampo: campo, canvasVento: vento, map: map };
  }

  function valorePunto(p, v, idx) {
    if (v.derivata === 'somma6') {
      var s = 0, found = false;
      for (var k = 0; k < 6; k++) {
        var j = idx - k;
        if (j < 0 || !p.val || p.val[j] === null || typeof p.val[j] === 'undefined') continue;
        s += p.val[j];
        found = true;
      }
      return found ? s : null;
    }
    if (!p.val) return null;
    var n = p.val[idx];
    return (n === null || typeof n === 'undefined') ? null : n;
  }
  function componentiVento(vel, dir) {
    if (vel === null || typeof vel === 'undefined' || dir === null || typeof dir === 'undefined') return null;
    var rad = dir * Math.PI / 180;
    return { u: -vel * Math.sin(rad), v: -vel * Math.cos(rad) };
  }
  function costruisciMatrice(punti, variabile, idx) {
    var lats = [], lons = [], seenLat = {}, seenLon = {};
    var i, k, p;
    for (i = 0; i < punti.length; i++) {
      p = punti[i];
      k = String(p.lat);
      if (!seenLat[k]) { seenLat[k] = true; lats.push(p.lat); }
      k = String(p.lon);
      if (!seenLon[k]) { seenLon[k] = true; lons.push(p.lon); }
    }
    lats.sort(function (a, b) { return a - b; });
    lons.sort(function (a, b) { return a - b; });
    var ny = lats.length, nx = lons.length;
    var latIx = {}, lonIx = {};
    for (i = 0; i < ny; i++) latIx[String(lats[i])] = i;
    for (i = 0; i < nx; i++) lonIx[String(lons[i])] = i;
    var val = new Array(ny * nx);
    var u = new Array(ny * nx);
    var v = new Array(ny * nx);
    var cat = new Array(ny * nx);
    var cape = new Array(ny * nx);
    var nubi = new Array(ny * nx);
    var pioggia = new Array(ny * nx);
    for (i = 0; i < ny * nx; i++) { val[i] = null; u[i] = null; v[i] = null; cat[i] = null; cape[i] = null; nubi[i] = null; pioggia[i] = null; }
    for (i = 0; i < punti.length; i++) {
      p = punti[i];
      var iy = latIx[String(p.lat)], ix = lonIx[String(p.lon)];
      if (iy === undefined || ix === undefined) continue;
      var j = iy * nx + ix;
      val[j] = valorePunto(p, variabile, idx);
      if (variabile.vento && p.dir) {
        var c = componentiVento(val[j], p.dir[idx]);
        if (c) { u[j] = c.u; v[j] = c.v; }
      }
      if (variabile.tempo) {
        var snow = (p.snow && p.snow[idx] !== null && typeof p.snow[idx] !== 'undefined') ? p.snow[idx] : 0;
        var showers = (p.showers && p.showers[idx] !== null && typeof p.showers[idx] !== 'undefined') ? p.showers[idx] : 0;
        cat[j] = raffinaCategoria(categoriaDaCodice(val[j]), snow, showers);
        cape[j] = (p.cape && p.cape[idx] !== null && typeof p.cape[idx] !== 'undefined') ? p.cape[idx] : null;
        if (p.nubi && p.nubi[idx] !== null && typeof p.nubi[idx] !== 'undefined') nubi[j] = p.nubi[idx];
        else nubi[j] = nuvolositaDaCodice(val[j]);
        if (p.prec && p.prec[idx] !== null && typeof p.prec[idx] !== 'undefined') pioggia[j] = p.prec[idx];
        else pioggia[j] = 0;
      }
    }
    return { lats: lats, lons: lons, nx: nx, ny: ny, val: val, u: u, v: v, cat: cat, cape: cape, nubi: nubi, pioggia: pioggia, tempo: !!(variabile && variabile.tempo) };
  }
  function indiceSotto(arr, x) {
    var lo = 0, hi = arr.length - 1;
    if (x <= arr[0]) return -1;
    if (x >= arr[hi]) return hi;
    while (hi - lo > 1) {
      var mid = (lo + hi) >> 1;
      if (arr[mid] <= x) lo = mid; else hi = mid;
    }
    return lo;
  }
  function mescolaAngoli(v00, v10, v01, v11, tx, ty) {
    var pezzi = [];
    if (v00 !== null && typeof v00 !== 'undefined') pezzi.push({ v: v00, w: (1 - tx) * (1 - ty) });
    if (v10 !== null && typeof v10 !== 'undefined') pezzi.push({ v: v10, w: tx * (1 - ty) });
    if (v01 !== null && typeof v01 !== 'undefined') pezzi.push({ v: v01, w: (1 - tx) * ty });
    if (v11 !== null && typeof v11 !== 'undefined') pezzi.push({ v: v11, w: tx * ty });
    if (!pezzi.length) return null;
    var s = 0, w = 0, i;
    for (i = 0; i < pezzi.length; i++) {
      if (pezzi[i].w <= 0) continue;
      s += pezzi[i].v * pezzi[i].w;
      w += pezzi[i].w;
    }
    if (w <= 0) return null;
    return s / w;
  }
  function campionaCampo(mat, lat, lon, campo) {
    if (!mat || !mat.nx) return null;
    var arr = (campo && mat[campo]) ? mat[campo] : mat.val;
    if (lon < mat.lons[0] - PASSO || lon > mat.lons[mat.nx - 1] + PASSO) return null;
    if (lat < mat.lats[0] - PASSO || lat > mat.lats[mat.ny - 1] + PASSO) return null;
    var ix = indiceSotto(mat.lons, lon);
    var iy = indiceSotto(mat.lats, lat);
    if (ix < 0) ix = 0;
    if (iy < 0) iy = 0;
    if (ix > mat.nx - 2) ix = mat.nx - 2;
    if (iy > mat.ny - 2) iy = mat.ny - 2;
    var x0 = mat.lons[ix], x1 = mat.lons[ix + 1];
    var y0 = mat.lats[iy], y1 = mat.lats[iy + 1];
    var tx = (lon - x0) / ((x1 - x0) || 1);
    var ty = (lat - y0) / ((y1 - y0) || 1);
    return mescolaAngoli(arr[iy * mat.nx + ix], arr[iy * mat.nx + ix + 1], arr[(iy + 1) * mat.nx + ix], arr[(iy + 1) * mat.nx + ix + 1], tx, ty);
  }
  function campionaVicino(mat, lat, lon, campo) {
    if (!mat || !mat.nx) return null;
    var arr = (campo && mat[campo]) ? mat[campo] : mat.val;
    if (lon < mat.lons[0] - PASSO || lon > mat.lons[mat.nx - 1] + PASSO) return null;
    if (lat < mat.lats[0] - PASSO || lat > mat.lats[mat.ny - 1] + PASSO) return null;
    var ix = indiceSotto(mat.lons, lon);
    var iy = indiceSotto(mat.lats, lat);
    if (ix < 0) ix = 0;
    if (iy < 0) iy = 0;
    if (ix < mat.nx - 1 && Math.abs(mat.lons[ix + 1] - lon) < Math.abs(mat.lons[ix] - lon)) ix += 1;
    if (iy < mat.ny - 1 && Math.abs(mat.lats[iy + 1] - lat) < Math.abs(mat.lats[iy] - lat)) iy += 1;
    return arr[iy * mat.nx + ix];
  }
  function fadeBordo(lat, lon) {
    var m = dominioCorrente().fade || 0.4;
    var fx = 1, fy = 1;
    if (lon < LON_MIN + m) fx = (lon - LON_MIN) / m;
    if (lon > LON_MAX - m) fx = (LON_MAX - lon) / m;
    if (lat < LAT_MIN + m) fy = (lat - LAT_MIN) / m;
    if (lat > LAT_MAX - m) fy = (LAT_MAX - lat) / m;
    if (fx < 0 || fy < 0) return 0;
    var f = Math.min(fx, fy, 1);
    return f * f * (3 - 2 * f);
  }
  function nuvolositaDaCodice(code) {
    if (code === null || typeof code === 'undefined' || isNaN(code)) return null;
    var c = Math.round(code);
    if (c === 0) return 8;
    if (c === 1) return 25;
    if (c === 2) return 55;
    if (c === 3) return 88;
    if (c === 45 || c === 48) return 92;
    if (c === 51 || c === 53 || c === 55 || c === 56 || c === 57) return 80;
    if (c === 61 || c === 63 || c === 65 || c === 66 || c === 67) return 85;
    if (c === 71 || c === 73 || c === 75 || c === 77 || c === 85 || c === 86) return 78;
    if (c === 80 || c === 81 || c === 82) return 90;
    if (c === 95 || c === 96 || c === 97 || c === 99) return 95;
    return 60;
  }
  function coloreFondoTempo(nubi, pioggia) {
    var stops = [
      [0, 255, 236, 196],
      [25, 240, 228, 200],
      [50, 210, 218, 228],
      [75, 168, 180, 200],
      [100, 128, 140, 162]
    ];
    var n = (nubi === null || typeof nubi === 'undefined' || isNaN(nubi)) ? 50 : nubi;
    if (n < 0) n = 0;
    if (n > 100) n = 100;
    var i, t, col;
    for (i = 0; i < stops.length - 1; i++) {
      if (n <= stops[i + 1][0] || i === stops.length - 2) {
        t = (n - stops[i][0]) / ((stops[i + 1][0] - stops[i][0]) || 1);
        if (t < 0) t = 0;
        if (t > 1) t = 1;
        col = [
          Math.round(stops[i][1] + (stops[i + 1][1] - stops[i][1]) * t),
          Math.round(stops[i][2] + (stops[i + 1][2] - stops[i][2]) * t),
          Math.round(stops[i][3] + (stops[i + 1][3] - stops[i][3]) * t)
        ];
        break;
      }
    }
    if (!col) col = [210, 218, 228];
    var p = (pioggia === null || typeof pioggia === 'undefined' || isNaN(pioggia)) ? 0 : pioggia;
    if (p > 0) {
      var f = p / 6;
      if (f > 1) f = 1;
      f = f * f * (3 - 2 * f);
      col = [
        Math.round(col[0] * (1 - f) + 64 * f),
        Math.round(col[1] * (1 - f) + 112 * f),
        Math.round(col[2] * (1 - f) + 186 * f)
      ];
    }
    return col;
  }
  function raggioSfocatura() {
    var px = Math.round((PASSO || 0.6) * 18);
    if (px < 2) px = 2;
    if (px > 12) px = 12;
    return px;
  }
  function applicaSfocatura(ctx, w, h, raggio) {
    if (!raggio || raggio < 1 || w < 4 || h < 4) return;
    var tmp = document.createElement('canvas');
    tmp.width = w;
    tmp.height = h;
    var tctx = tmp.getContext('2d');
    if (!tctx) return;
    try {
      if (typeof tctx.filter === 'string') {
        tctx.filter = 'blur(' + raggio + 'px)';
        tctx.drawImage(ctx.canvas, 0, 0, w, h, 0, 0, w, h);
        ctx.save();
        ctx.globalCompositeOperation = 'copy';
        ctx.drawImage(tmp, 0, 0);
        ctx.restore();
        return;
      }
    } catch (e) {}
    tctx.drawImage(ctx.canvas, 0, 0, w, h, 0, 0, w, h);
    ctx.drawImage(tmp, 0, 0);
  }
  function disegnaCampo(ctx, vista, mat, scalaId, alphaBase) {
    if (!mat) return;
    var step = PASSO >= 0.4 ? 3 : 2;
    var imgW = Math.max(1, Math.ceil(vista.w / step));
    var imgH = Math.max(1, Math.ceil(vista.h / step));
    var tmp = document.createElement('canvas');
    tmp.width = imgW;
    tmp.height = imgH;
    var tctx = tmp.getContext('2d');
    var img = tctx.createImageData(imgW, imgH);
    var data = img.data;
    var px, py, i, ll, val, col, a, nubi, pioggia;
    for (py = 0; py < imgH; py++) {
      for (px = 0; px < imgW; px++) {
        ll = vista.inv(px * step + step / 2, py * step + step / 2);
        if (mat.tempo) {
          nubi = campionaCampo(mat, ll.lat, ll.lon, 'nubi');
          pioggia = campionaCampo(mat, ll.lat, ll.lon, 'pioggia');
          col = (nubi === null && (pioggia === null || pioggia === 0)) ? null : coloreFondoTempo(nubi, pioggia);
        } else {
          val = campionaCampo(mat, ll.lat, ll.lon, 'val');
          col = coloreDi(val, scalaId);
        }
        if (!col) continue;
        a = (alphaBase || 0.82) * fadeBordo(ll.lat, ll.lon);
        i = (py * imgW + px) * 4;
        data[i] = col[0];
        data[i + 1] = col[1];
        data[i + 2] = col[2];
        data[i + 3] = Math.round(a * 255);
      }
    }
    tctx.putImageData(img, 0, 0);
    ctx.imageSmoothingEnabled = true;
    if (typeof ctx.imageSmoothingQuality === 'string') ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(tmp, 0, 0, vista.w, vista.h);
  }
  function perAnello(geom, fn) {
    var t = geom.type, i, j;
    if (t === 'Polygon') {
      for (i = 0; i < geom.coordinates.length; i++) fn(geom.coordinates[i]);
    } else if (t === 'MultiPolygon') {
      for (i = 0; i < geom.coordinates.length; i++) {
        for (j = 0; j < geom.coordinates[i].length; j++) fn(geom.coordinates[i][j]);
      }
    }
  }
  function tracciaAnello(ctx, ring, vista) {
    var i, xy;
    ctx.beginPath();
    for (i = 0; i < ring.length; i++) {
      xy = vista.xy(ring[i][1], ring[i][0]);
      if (i === 0) ctx.moveTo(xy[0], xy[1]);
      else ctx.lineTo(xy[0], xy[1]);
    }
    ctx.closePath();
  }
  function isolaItalia(stato) {
    return !!(stato && stato.variabile && stato.variabile.tempo);
  }
  function nomeEnclaveItaliana(nome) {
    return nome === 'San Marino' || nome === 'Vatican' || nome === 'Holy See' || nome === 'Città del Vaticano';
  }
  function disegnaConfini(ctx, vista, stato) {
    if (!geojson || !geojson.features) return;
    var f, i, solo = isolaItalia(stato);
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    if (!solo) {
      for (i = 0; i < geojson.features.length; i++) {
        f = geojson.features[i];
        if (!f.properties || f.properties.tipo !== 'vicino') continue;
        perAnello(f.geometry, function (ring) {
          tracciaAnello(ctx, ring, vista);
          ctx.fillStyle = 'rgba(255,255,255,0.14)';
          ctx.fill();
          ctx.strokeStyle = 'rgba(40,70,95,0.55)';
          ctx.lineWidth = 1;
          ctx.stroke();
        });
      }
    }
    if (solo && regioniGeo && regioniGeo.features) {
      ctx.save();
      ctx.strokeStyle = 'rgba(80, 70, 50, 0.28)';
      ctx.lineWidth = 0.8;
      for (i = 0; i < regioniGeo.features.length; i++) {
        f = regioniGeo.features[i];
        if (!f.geometry) continue;
        perAnello(f.geometry, function (ring) {
          tracciaAnello(ctx, ring, vista);
          ctx.stroke();
        });
      }
      ctx.restore();
    }
    for (i = 0; i < geojson.features.length; i++) {
      f = geojson.features[i];
      if (!f.properties || f.properties.tipo !== 'italia') continue;
      perAnello(f.geometry, function (ring) {
        tracciaAnello(ctx, ring, vista);
        ctx.strokeStyle = '#003366';
        ctx.lineWidth = 1.6;
        ctx.stroke();
      });
    }
  }

  function livelliIsolinee(scalaId) {
    var step, min, max;
    if (scalaId === 'mslp') { min = 980; max = 1044; step = 2; }
    else if (scalaId === 'temp') { min = -16; max = 42; step = 2; }
    else if (scalaId === 'temp500') { min = -40; max = 10; step = 2; }
    else if (scalaId === 'geo500') { min = 5000; max = 6000; step = 40; }
    else if (scalaId === 'geo700') { min = 2700; max = 3300; step = 20; }
    else if (scalaId === 'umidita' || scalaId === 'nubi') { min = 10; max = 100; step = 10; }
    else return [];
    var out = [];
    for (var v = min; v <= max + 1e-9; v += step) out.push(Math.round(v * 100) / 100);
    return out;
  }
  function lerpPunto(a, b, va, vb, livello) {
    var t = (livello - va) / ((vb - va) || 1e-9);
    if (t < 0) t = 0;
    if (t > 1) t = 1;
    return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
  }
  function isolineeDi(mat, livello) {
    var segs = [];
    var ny = mat.ny, nx = mat.nx, iy, ix;
    for (iy = 0; iy < ny - 1; iy++) {
      for (ix = 0; ix < nx - 1; ix++) {
        var v00 = mat.val[iy * nx + ix];
        var v10 = mat.val[iy * nx + ix + 1];
        var v01 = mat.val[(iy + 1) * nx + ix];
        var v11 = mat.val[(iy + 1) * nx + ix + 1];
        if (v00 === null || v10 === null || v01 === null || v11 === null) continue;
        if (typeof v00 === 'undefined' || typeof v10 === 'undefined' || typeof v01 === 'undefined' || typeof v11 === 'undefined') continue;
        var c = 0;
        if (v00 >= livello) c |= 1;
        if (v10 >= livello) c |= 2;
        if (v11 >= livello) c |= 4;
        if (v01 >= livello) c |= 8;
        if (c === 0 || c === 15) continue;
        var sw = [mat.lats[iy], mat.lons[ix]];
        var se = [mat.lats[iy], mat.lons[ix + 1]];
        var ne = [mat.lats[iy + 1], mat.lons[ix + 1]];
        var nw = [mat.lats[iy + 1], mat.lons[ix]];
        var bottom = lerpPunto(sw, se, v00, v10, livello);
        var right = lerpPunto(se, ne, v10, v11, livello);
        var top = lerpPunto(nw, ne, v01, v11, livello);
        var left = lerpPunto(sw, nw, v00, v01, livello);
        var coppie;
        if (c === 1 || c === 14) coppie = [left, bottom];
        else if (c === 2 || c === 13) coppie = [bottom, right];
        else if (c === 4 || c === 11) coppie = [right, top];
        else if (c === 8 || c === 7) coppie = [top, left];
        else if (c === 3 || c === 12) coppie = [left, right];
        else if (c === 6 || c === 9) coppie = [bottom, top];
        else if (c === 5) coppie = [left, top, bottom, right];
        else if (c === 10) coppie = [left, bottom, top, right];
        else continue;
        for (var s = 0; s < coppie.length; s += 2) segs.push([coppie[s], coppie[s + 1]]);
      }
    }
    return segs;
  }
  function disegnaIsolinee(ctx, vista, mat, scalaId) {
    var livelli = livelliIsolinee(scalaId);
    if (!livelli.length) return;
    ctx.save();
    ctx.lineWidth = 1;
    ctx.lineJoin = 'round';
    ctx.font = '11px Titillium Web, Arial, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    var L, s, segs, a, b, xy1, xy2;
    for (L = 0; L < livelli.length; L++) {
      segs = isolineeDi(mat, livelli[L]);
      ctx.strokeStyle = 'rgba(20,30,45,0.55)';
      ctx.beginPath();
      for (s = 0; s < segs.length; s++) {
        a = segs[s][0]; b = segs[s][1];
        xy1 = vista.xy(a[0], a[1]);
        xy2 = vista.xy(b[0], b[1]);
        ctx.moveTo(xy1[0], xy1[1]);
        ctx.lineTo(xy2[0], xy2[1]);
      }
      ctx.stroke();
      var passoEtichetta = (scalaId === 'mslp' || scalaId === 'temp' || scalaId === 'temp500') ? 2 : 1;
      if (Math.round(livelli[L] / ((livelli[1] - livelli[0]) || 1)) % passoEtichetta !== 0) continue;
      for (s = 8; s < segs.length; s += 28) {
        a = segs[s][0]; b = segs[s][1];
        xy1 = vista.xy((a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
        if (xy1[0] < 24 || xy1[1] < 16 || xy1[0] > vista.w - 24 || xy1[1] > vista.h - 20) continue;
        var et = String(livelli[L]);
        ctx.fillStyle = 'rgba(255,255,255,0.85)';
        var tw = ctx.measureText(et).width + 4;
        ctx.fillRect(xy1[0] - tw / 2, xy1[1] - 7, tw, 14);
        ctx.fillStyle = 'rgba(20,30,45,0.9)';
        ctx.fillText(et, xy1[0], xy1[1]);
      }
    }
    ctx.restore();
  }
  function disegnaFreccia(ctx, x, y, rad, len) {
    if (!len || len < 4) return;
    var x2 = x + Math.sin(rad) * len;
    var y2 = y - Math.cos(rad) * len;
    ctx.strokeStyle = 'rgba(20,20,20,0.8)';
    ctx.fillStyle = 'rgba(20,20,20,0.8)';
    ctx.lineWidth = 1.1;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    var a = rad + Math.PI + 0.45, b = rad + Math.PI - 0.45;
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 + Math.sin(a) * 5, y2 - Math.cos(a) * 5);
    ctx.lineTo(x2 + Math.sin(b) * 5, y2 - Math.cos(b) * 5);
    ctx.closePath();
    ctx.fill();
  }
  function disegnaFrecce(ctx, vista, mat) {
    var iy, ix, j, vel, dir, xy, len;
    ctx.save();
    for (iy = 0; iy < mat.ny; iy += 1) {
      for (ix = 0; ix < mat.nx; ix += 1) {
        if ((iy + ix) % 2 !== 0) continue;
        j = iy * mat.nx + ix;
        if (mat.u[j] === null || mat.v[j] === null) continue;
        vel = Math.sqrt(mat.u[j] * mat.u[j] + mat.v[j] * mat.v[j]);
        if (!vel) continue;
        dir = Math.atan2(mat.u[j], mat.v[j]);
        xy = vista.xy(mat.lats[iy], mat.lons[ix]);
        len = 7 + Math.min(18, vel / 6);
        disegnaFreccia(ctx, xy[0], xy[1], dir, len);
      }
    }
    ctx.restore();
  }
  function dovrebbeAnimareVento(stato) {
    return !!(stato && stato.variabile && stato.variabile.vento && particelleAttive() && !motoRidotto() && stato.matrice);
  }
  function misureLegendaTempo(vista) {
    var cols = 5, rows = 3, pad = 8, cellH = 26;
    var w = Math.max(280, vista.w - 20);
    var h = rows * cellH + pad * 2;
    return { cols: cols, rows: rows, pad: pad, cellH: cellH, w: w, h: h, x: 10, y: vista.h - h - 8, cellW: (w - pad * 2) / cols };
  }
  function disegnaLegendaTempo(ctx, vista) {
    var m = misureLegendaTempo(vista);
    ctx.fillStyle = 'rgba(255,255,255,0.94)';
    ctx.fillRect(m.x, m.y, m.w, m.h);
    ctx.strokeStyle = 'rgba(0,51,102,0.35)';
    ctx.strokeRect(m.x, m.y, m.w, m.h);
    ctx.font = '11px Titillium Web, Arial, sans-serif';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#003366';
    var i, cx, cy, item, img, iw = 18, nome, maxW;
    for (i = 0; i < LEGENDA_TEMPO.length; i++) {
      item = LEGENDA_TEMPO[i];
      cx = m.x + m.pad + (i % m.cols) * m.cellW;
      cy = m.y + m.pad + Math.floor(i / m.cols) * m.cellH + m.cellH / 2;
      img = iconeTempo[item.id];
      if (img) ctx.drawImage(img, cx, cy - iw / 2, iw, iw);
      nome = item.nome;
      maxW = m.cellW - iw - 8;
      if (ctx.measureText(nome).width > maxW) ctx.font = '10px Titillium Web, Arial, sans-serif';
      ctx.fillText(nome, cx + iw + 4, cy, maxW);
      ctx.font = '11px Titillium Web, Arial, sans-serif';
    }
  }
  function disegnaDecorazioni(ctx, vista, stato) {

    if (stato.variabile && stato.variabile.tempo) {
      disegnaLegendaTempo(ctx, vista);
      return;
    }
    var ext = etichettaScala(stato.variabile.scala);
    var x = 16, y = vista.h - 52, w = Math.min(260, vista.w - 32);
    ctx.fillStyle = 'rgba(255,255,255,0.88)';
    ctx.fillRect(x, y, w, 38);
    ctx.strokeStyle = 'rgba(0,51,102,0.35)';
    ctx.strokeRect(x, y, w, 38);
    var grd = ctx.createLinearGradient(x + 8, 0, x + w - 8, 0);
    var stops = SCALE[stato.variabile.scala] || SCALE.temp;
    for (var i = 0; i < stops.length; i++) {
      grd.addColorStop(i / (stops.length - 1), 'rgb(' + stops[i][1] + ',' + stops[i][2] + ',' + stops[i][3] + ')');
    }
    ctx.fillStyle = grd;
    ctx.fillRect(x + 8, y + 8, w - 16, 10);
    ctx.fillStyle = '#003366';
    ctx.font = '11px Titillium Web, Arial, sans-serif';
    ctx.fillText(String(ext.min), x + 8, y + 32);
    ctx.textAlign = 'right';
    ctx.fillText(String(ext.max) + ' ' + stato.variabile.unita, x + w - 8, y + 32);
    ctx.textAlign = 'left';
  }
  function rettangoloArrotondato(ctx, x, y, w, h, r) {
    if (r > w / 2) r = w / 2;
    if (r > h / 2) r = h / 2;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
  function rettangoliSovrapposti(a, b, pad) {
    pad = pad || 0;
    return !(a.x + a.w + pad < b.x || b.x + b.w + pad < a.x || a.y + a.h + pad < b.y || b.y + b.h + pad < a.y);
  }
  function eVistaStretta(vista) {
    return vista.w < 640 || (window.innerWidth && window.innerWidth < 720);
  }
  function massimoSchede(vista) {
    var stretta = eVistaStretta(vista);
    if (dominioId === 'italia') return stretta ? 10 : 15;
    if (dominioId === 'lazio') return stretta ? 8 : 16;
    return stretta ? 8 : 10;
  }
  function indiceOraLocale(loc, iso) {
    if (!loc || !loc.orari || !loc.orari.length) return -1;
    var i, meglio = 0, dist = Infinity, d;
    for (i = 0; i < loc.orari.length; i++) {
      if (loc.orari[i] === iso) return i;
      if (iso) {
        d = Math.abs(Date.parse(loc.orari[i]) - Date.parse(iso));
        if (d < dist) { dist = d; meglio = i; }
      }
    }
    return iso ? meglio : 0;
  }
  function ancoreScheda(xy, w, h, preferita) {
    var g = 8;
    var tutte = {
      s: { x: xy[0] - w / 2, y: xy[1] + g },
      n: { x: xy[0] - w / 2, y: xy[1] - h - g },
      e: { x: xy[0] + g, y: xy[1] - h / 2 },
      w: { x: xy[0] - w - g, y: xy[1] - h / 2 },
      ne: { x: xy[0] + g, y: xy[1] - h - g },
      nw: { x: xy[0] - w - g, y: xy[1] - h - g },
      se: { x: xy[0] + g, y: xy[1] + g },
      sw: { x: xy[0] - w - g, y: xy[1] + g }
    };
    var ordine = [preferita || 's', 's', 'n', 'e', 'w', 'ne', 'nw', 'se', 'sw'];
    var out = [], visti = {}, i, k;
    for (i = 0; i < ordine.length; i++) {
      k = ordine[i];
      if (!tutte[k] || visti[k]) continue;
      visti[k] = true;
      out.push(tutte[k]);
    }
    return out;
  }
  function distanzaMinimaComuni(vista, locali) {
    var min = Infinity, i, j, a, b, dx, dy, d;
    for (i = 0; i < locali.length; i++) {
      a = vista.xy(locali[i].lat, locali[i].lon);
      for (j = i + 1; j < locali.length; j++) {
        b = vista.xy(locali[j].lat, locali[j].lon);
        dx = a[0] - b[0]; dy = a[1] - b[1];
        d = Math.sqrt(dx * dx + dy * dy);
        if (d < min) min = d;
      }
    }
    return min;
  }

  function luminositaRgb(rgb) {
    if (!rgb) return 0;
    return (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255;
  }
  function testoConAureola(ctx, testo, x, y, maxW, fill) {
    ctx.save();
    ctx.lineJoin = 'round';
    ctx.miterLimit = 2;
    ctx.lineWidth = 4.5;
    ctx.strokeStyle = 'rgba(255,255,255,0.96)';
    ctx.strokeText(testo, x, y, maxW);
    ctx.fillStyle = fill || '#1a1a1a';
    ctx.fillText(testo, x, y, maxW);
    ctx.restore();
  }
  function disegnaIconaConAureola(ctx, img, x, y, s) {
    ctx.save();
    if (typeof ctx.filter !== 'undefined') {
      ctx.filter = 'drop-shadow(0 1px 1.6px rgba(18,48,74,0.38))';
    }
    ctx.drawImage(img, x, y, s, s);
    ctx.restore();
  }
  function disegnaCerchioTemperatura(ctx, x, y, r, temp, evidenziato) {
    var rgb = coloreDi(temp, 'temp');
    if (!rgb) rgb = [230, 200, 40];
    ctx.save();
    ctx.beginPath();
    ctx.arc(x + 0.6, y + 1, r + 0.6, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(18,48,74,0.22)';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
    ctx.fill();
    ctx.lineWidth = evidenziato ? 2.2 : 1.8;
    ctx.strokeStyle = evidenziato ? '#ffbe2e' : '#ffffff';
    ctx.stroke();
    var etichetta = String(Math.round(temp)) + '°';
    ctx.font = 'bold ' + Math.max(10, Math.round(r * 0.95)) + 'px Titillium Web, Arial, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = luminositaRgb(rgb) > 0.55 ? '#1a1a1a' : '#ffffff';
    ctx.fillText(etichetta, x, y + 0.5);
    ctx.restore();
  }

  function minMaxGiorno(loc, iso) {
    if (!loc || !loc.orari || !loc.temp || !iso) return null;
    var giorno = String(iso).slice(0, 10), i, v, mn = Infinity, mx = -Infinity;
    for (i = 0; i < loc.orari.length; i++) {
      if (String(loc.orari[i]).slice(0, 10) !== giorno) continue;
      v = loc.temp[i];
      if (v === null || typeof v === 'undefined' || isNaN(v)) continue;
      if (v < mn) mn = v;
      if (v > mx) mx = v;
    }
    return mn === Infinity ? null : { min: mn, max: mx };
  }
  function limitaNudge(off) {
    var x = (off && off[0]) ? off[0] : 0;
    var y = (off && off[1]) ? off[1] : 0;
    var L = Math.sqrt(x * x + y * y);
    if (L > 15) { x *= 15 / L; y *= 15 / L; }
    return [x, y];
  }
  function misuraUnitaTempo(k) {
    var S = Math.round(40 * k);
    var fT = (k >= 1) ? 12 : 11;
    var fN = 10;
    return { S: S, fT: fT, fN: fN, gap: 1 };
  }
  function disegnaSchedeTempo(ctx, vista, stato, opts) {
    var locali = (stato && stato.locali) || [];
    if (!locali.length) return;
    var d = dominioCorrente();
    var iso = (stato.orari && stato.orari[stato.indice]) || null;
    var latRif = (d.latMin + d.latMax) / 2;
    var p0 = vista.xy(latRif, 12), p1 = vista.xy(latRif, 13);
    var k = Math.abs(p1[0] - p0[0]) / (d.refLon || 73.2);
    if (!isFinite(k) || k <= 0) k = 1;
    var kGrezzo = k;
    if (k > 1.15) k = 1.15;
    if (k < 0.5) k = 0.5;
    var dettaglio = (vista && typeof vista.zoom === 'number' && typeof vista.zoomFit === 'number')
      ? (vista.zoom >= vista.zoomFit + 1)
      : (kGrezzo / k >= 1.4);
    var u = misuraUnitaTempo(k);
    var S = u.S, fT = u.fT, fN = u.fN, gap = u.gap;
    var i, loc, idx, code, cat, mm, xy, off, ix, iy, cx, yT, yN, img, cape, schede = [], s;
    for (i = 0; i < locali.length; i++) {
      loc = locali[i];
      idx = indiceOraLocale(loc, iso);
      if (idx < 0) continue;
      if ((loc.livello || 1) > 1 && !dettaglio) continue;
      code = (loc.code && loc.code[idx] !== null && typeof loc.code[idx] !== 'undefined') ? loc.code[idx] : null;
      cat = raffinaCategoria(categoriaDaCodice(code), (loc.snow && loc.snow[idx]) || 0, 0);
      mm = minMaxGiorno(loc, iso);
      if (!cat && !mm) continue;
      xy = vista.xy(loc.lat, loc.lon);
      if (xy[0] < -40 || xy[1] < -40 || xy[0] > vista.w + 40 || xy[1] > vista.h + 40) continue;
      off = limitaNudge((dettaglio && loc.off2) ? loc.off2 : (loc.off || [0, 0]));
      cape = (loc.cape && loc.cape[idx] !== null && typeof loc.cape[idx] !== 'undefined') ? loc.cape[idx] : null;
      schede.push({ loc: loc, xy: xy, cat: cat, mm: mm, cape: cape, cx: xy[0] + off[0], cy: xy[1] + off[1] });
    }
    ctx.save();
    for (i = 0; i < schede.length; i++) {
      s = schede[i];
      cx = s.cx; iy = s.cy - S / 2; ix = cx - S / 2;
      img = s.cat ? iconeTempo[s.cat] : null;
      if (img) disegnaIconaConAureola(ctx, img, ix, iy, S);
      if ((s.cat === 'temporale' || s.cat === 'temporale-grandine') && s.cape !== null && s.cape >= 1000) {
        var r = Math.max(3, 5 * k), tx = ix + S - r, ty = iy + r + 1;
        ctx.beginPath();
        ctx.moveTo(tx, ty - r);
        ctx.lineTo(tx + r, ty + r * 0.8);
        ctx.lineTo(tx - r, ty + r * 0.8);
        ctx.closePath();
        ctx.fillStyle = '#d97706';
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.2;
        ctx.stroke();
        ctx.fill();
      }
      yT = s.cy + S / 2 + gap;
      yN = yT + fT + gap;
      ctx.textBaseline = 'top';
      if (s.mm) {
        ctx.font = '700 ' + fT + 'px Titillium Web, Arial, sans-serif';
        ctx.textAlign = 'right';
        testoConAureola(ctx, Math.round(s.mm.min) + '°', cx - 3, yT, 60, '#1d4f8c');
        ctx.textAlign = 'left';
        testoConAureola(ctx, Math.round(s.mm.max) + '°', cx + 3, yT, 60, '#b42318');
        ctx.fillStyle = 'rgba(0,51,102,0.35)';
        ctx.fillRect(cx - 0.5, yT + 2, 1, fT - 3);
      }
      ctx.font = '600 ' + fN + 'px Titillium Web, Arial, sans-serif';
      ctx.textAlign = 'center';
      testoConAureola(ctx, s.loc.etichetta || s.loc.nome, cx, yN, 200, s.loc.evidenziato ? '#003366' : '#1a1a1a');
    }
    ctx.restore();
  }

  function disegnaTerraPulita(ctx, vista, stato) {
    if (!geojson || !geojson.features) return;
    var i, f, solo = isolaItalia(stato), nome;
    for (i = 0; i < geojson.features.length; i++) {
      f = geojson.features[i];
      if (!f.properties) continue;
      nome = f.properties.nome;
      if (solo) {
        if (f.properties.tipo !== 'italia' && !nomeEnclaveItaliana(nome)) continue;
        ctx.fillStyle = '#f3edd9';
      } else {
        ctx.fillStyle = f.properties.tipo === 'italia' ? '#f3edd9' : '#e4ddd0';
      }
      perAnello(f.geometry, function (ring) {
        tracciaAnello(ctx, ring, vista);
        ctx.fill();
      });
    }
  }
  function disegnaVista(ctx, vista, stato, opts) {

    opts = opts || {};
    ctx.fillStyle = '#c5d8e8';
    ctx.fillRect(0, 0, vista.w, vista.h);
    if (!stato || !stato.variabile || !stato.matrice) {
      disegnaHillshade(ctx, vista);
      disegnaConfini(ctx, vista, stato);
      disegnaLaghi(ctx, vista);
      disegnaEtichetteLaghi(ctx, vista);
      disegnaComuni(ctx, vista);
      return;
    }
    if (stato.variabile.tempo) {
      ctx.fillStyle = '#b7d4ea';
      ctx.fillRect(0, 0, vista.w, vista.h);
      disegnaTerraPulita(ctx, vista, stato);
    } else {
      disegnaCampo(ctx, vista, stato.matrice, stato.variabile.scala, 0.84);
      applicaSfocatura(ctx, vista.w, vista.h, raggioSfocatura());
    }
    disegnaHillshade(ctx, vista);
    disegnaConfini(ctx, vista, stato);
    disegnaLaghi(ctx, vista);
    if (isolineeAttive() && !stato.variabile.tempo) disegnaIsolinee(ctx, vista, stato.matrice, stato.variabile.scala);
    if (stato.variabile.vento && (opts.frecce || !particelleAttive() || motoRidotto())) {
      disegnaFrecce(ctx, vista, stato.matrice);
    }
    if (stato.variabile.tempo) {
      disegnaSchedeTempo(ctx, vista, stato, opts);
    } else {
      disegnaEtichetteLaghi(ctx, vista);
      disegnaComuni(ctx, vista);
    }
    if (opts.decorazioni) disegnaDecorazioni(ctx, vista, stato);
  }
  function disegnaHillshade(ctx, vista) {
    var d = dominioCorrente();
    if (!d.hillshade || !hillshadeImg) return;
    var latN = (d.hillLatMax != null) ? d.hillLatMax : d.latMax;
    var latS = (d.hillLatMin != null) ? d.hillLatMin : d.latMin;
    var lonW = (d.hillLonMin != null) ? d.hillLonMin : d.lonMin;
    var lonE = (d.hillLonMax != null) ? d.hillLonMax : d.lonMax;
    var p0 = vista.xy(latN, lonW);
    var p1 = vista.xy(latS, lonE);
    var x = Math.min(p0[0], p1[0]);
    var y = Math.min(p0[1], p1[1]);
    var w = Math.abs(p1[0] - p0[0]);
    var h = Math.abs(p1[1] - p0[1]);
    if (w < 8 || h < 8) return;
    ctx.save();
    ctx.globalAlpha = 0.40;
    ctx.globalCompositeOperation = 'multiply';
    try { ctx.drawImage(hillshadeImg, x, y, w, h); } catch (e) {}
    ctx.restore();
  }
  function disegnaLaghi(ctx, vista) {
    if (!dominioCorrente().laghi) return;
    if (!laghiGeo || !laghiGeo.features) return;
    var i, f, nome, xy, c;
    ctx.save();
    for (i = 0; i < laghiGeo.features.length; i++) {
      f = laghiGeo.features[i];
      if (!f.geometry) continue;
      perAnello(f.geometry, function (ring) {
        tracciaAnello(ctx, ring, vista);
        ctx.fillStyle = 'rgba(70, 130, 180, 0.55)';
        ctx.fill();
        ctx.strokeStyle = 'rgba(20, 55, 90, 0.85)';
        ctx.lineWidth = 1.4;
        ctx.stroke();
      });
    }
    ctx.restore();
  }
  function disegnaEtichetteLaghi(ctx, vista) {
    if (!dominioCorrente().laghi) return;
    if (!laghiGeo || !laghiGeo.features) return;
    var i, f, nome, xy, c, tw;
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    for (i = 0; i < laghiGeo.features.length; i++) {
      f = laghiGeo.features[i];
      nome = f.properties && f.properties.nome;
      c = centroideAnello(f.geometry);
      if (!nome || !c) continue;
      xy = vista.xy(c.lat, c.lon);
      if (xy[0] < 8 || xy[1] < 8 || xy[0] > vista.w - 8 || xy[1] > vista.h - 8) continue;
      ctx.font = 'bold 10px Titillium Web, Arial, sans-serif';
      tw = ctx.measureText(nome).width;
      ctx.lineWidth = 3;
      ctx.strokeStyle = 'rgba(255,255,255,0.9)';
      ctx.strokeText(nome, xy[0], xy[1]);
      ctx.fillStyle = '#003366';
      ctx.fillText(nome, xy[0], xy[1]);
    }
    ctx.restore();
  }
  function centroideAnello(geom) {
    var sommaLat = 0, sommaLon = 0, n = 0;
    perAnello(geom, function (ring) {
      var i, max = ring.length - 1;
      if (max < 1) return;
      if (ring[0][0] === ring[max][0] && ring[0][1] === ring[max][1]) max -= 1;
      for (i = 0; i <= max; i++) {
        sommaLon += ring[i][0];
        sommaLat += ring[i][1];
        n += 1;
      }
    });
    if (!n) return null;
    return { lat: sommaLat / n, lon: sommaLon / n };
  }
  function disegnaComuni(ctx, vista) {
    var comuni = (dominioCorrente().comuni || []).slice();
    if (!comuni.length) return;
    comuni.sort(function (a, b) { return (a.priorita || 99) - (b.priorita || 99); });
    var i, c, xy, allinea, evid, r, testo, tw, tx, ty, ax, ay, box;
    var occupati = [];
    ctx.save();
    ctx.font = 'bold 12px Titillium Web, Arial, sans-serif';
    ctx.textBaseline = 'middle';
    for (i = 0; i < comuni.length; i++) {
      c = comuni[i];
      xy = vista.xy(c.lat, c.lon);
      if (xy[0] < 4 || xy[1] < 4 || xy[0] > vista.w - 4 || xy[1] > vista.h - 4) continue;
      evid = !!c.evidenziato;
      r = evid ? 5 : 3.5;
      ctx.beginPath();
      ctx.arc(xy[0], xy[1], r, 0, Math.PI * 2);
      ctx.fillStyle = evid ? '#003366' : '#1a1a1a';
      ctx.fill();
      ctx.strokeStyle = evid ? '#ffbe2e' : '#ffffff';
      ctx.lineWidth = evid ? 2 : 1.2;
      ctx.stroke();
      testo = c.etichetta || c.nome;
      tw = ctx.measureText(testo).width;
      allinea = c.allinea || 'e';
      ax = 0; ay = 0;
      ctx.textAlign = 'left';
      if (allinea === 'w') { ctx.textAlign = 'right'; ax = -r - 5; }
      else if (allinea === 'e') { ax = r + 5; }
      else if (allinea === 'n') { ctx.textAlign = 'center'; ay = -r - 9; }
      else if (allinea === 's') { ctx.textAlign = 'center'; ay = r + 9; }
      else if (allinea === 'ne') { ax = r + 4; ay = -r - 6; }
      else if (allinea === 'nw') { ctx.textAlign = 'right'; ax = -r - 4; ay = -r - 6; }
      else if (allinea === 'se') { ax = r + 4; ay = r + 6; }
      else if (allinea === 'sw') { ctx.textAlign = 'right'; ax = -r - 4; ay = r + 6; }
      tx = xy[0] + ax;
      ty = xy[1] + ay;
      if (ctx.textAlign === 'center') box = { x: tx - tw / 2 - 2, y: ty - 7, w: tw + 4, h: 14 };
      else if (ctx.textAlign === 'right') box = { x: tx - tw - 2, y: ty - 7, w: tw + 4, h: 14 };
      else box = { x: tx - 2, y: ty - 7, w: tw + 4, h: 14 };
      var collision = false, o;
      for (o = 0; o < occupati.length; o++) {
        if (rettangoliSovrapposti(box, occupati[o], 2)) { collision = true; break; }
      }
      if (collision) continue;
      occupati.push(box);
      ctx.fillStyle = 'rgba(255,255,255,0.86)';
      ctx.fillRect(box.x, box.y, box.w, box.h);
      ctx.fillStyle = evid ? '#003366' : '#1a1a1a';
      ctx.fillText(testo, tx, ty);
    }
    ctx.restore();
  }
  function nuovaParticella() {
    return {
      lat: LAT_MIN + Math.random() * (LAT_MAX - LAT_MIN),
      lon: LON_MIN + Math.random() * (LON_MAX - LON_MIN),
      vita: 30 + Math.random() * 70,
      coda: []
    };
  }
  function assicuraParticelle(n) {
    while (particelle.length < n) particelle.push(nuovaParticella());
    if (particelle.length > n) particelle.length = n;
  }
  function passoParticelle(dt) {
    var mat = statoMappa.matrice;
    if (!mat) return;
    var i, p, u, v, dlat, dlon, factor = 55;
    for (i = 0; i < particelle.length; i++) {
      p = particelle[i];
      u = campionaCampo(mat, p.lat, p.lon, 'u');
      v = campionaCampo(mat, p.lat, p.lon, 'v');
      if (u === null || v === null) { particelle[i] = nuovaParticella(); continue; }
      dlat = (v / 111) * (dt / 1000) * factor;
      dlon = (u / (111 * Math.max(0.2, Math.cos(p.lat * Math.PI / 180)))) * (dt / 1000) * factor;
      p.coda.push([p.lat, p.lon]);
      if (p.coda.length > 9) p.coda.shift();
      p.lat += dlat;
      p.lon += dlon;
      p.vita -= 1;
      if (p.vita <= 0 || p.lat < LAT_MIN || p.lat > LAT_MAX || p.lon < LON_MIN || p.lon > LON_MAX) {
        particelle[i] = nuovaParticella();
      }
    }
  }
  function disegnaParticelle(ctx, xyFn) {
    var i, p, k, a, b, xy1, xy2, t;
    ctx.lineCap = 'round';
    for (i = 0; i < particelle.length; i++) {
      p = particelle[i];
      if (!p.coda.length) continue;
      for (k = 1; k < p.coda.length; k++) {
        a = p.coda[k - 1];
        b = p.coda[k];
        xy1 = xyFn(a[0], a[1]);
        xy2 = xyFn(b[0], b[1]);
        t = k / p.coda.length;
        ctx.strokeStyle = 'rgba(15,25,40,' + (0.15 + t * 0.65) + ')';
        ctx.lineWidth = 0.8 + t * 1.6;
        ctx.beginPath();
        ctx.moveTo(xy1[0], xy1[1]);
        ctx.lineTo(xy2[0], xy2[1]);
        ctx.stroke();
      }
    }
  }
  var ultimoVentoTs = 0;
  function cicloVento(ts) {
    if (!dovrebbeAnimareVento(statoMappa) || !strato) {
      ventoRaf = null;
      if (strato) strato.ridisegnaVento();
      return;
    }
    if (!ultimoVentoTs) ultimoVentoTs = ts;
    var dt = Math.min(50, ts - ultimoVentoTs);
    ultimoVentoTs = ts;
    assicuraParticelle(320);
    passoParticelle(dt || 16);
    strato.ridisegnaVento();
    ventoRaf = window.requestAnimationFrame(cicloVento);
  }
  function avviaOFermaVento() {
    if (dovrebbeAnimareVento(statoMappa)) {
      if (!ventoRaf) {
        ultimoVentoTs = 0;
        ventoRaf = window.requestAnimationFrame(cicloVento);
      }
    } else if (ventoRaf) {
      window.cancelAnimationFrame(ventoRaf);
      ventoRaf = null;
      if (strato) strato.ridisegnaVento();
    }
  }

  function onClickMappa(ev) {
    if (!statoMappa.punti.length) return;
    apriMeteogramma(ev.latlng.lat, ev.latlng.lng, ev.latlng);
  }
  function apriMeteogramma(lat, lon, latlng) {
    var vicino = null, dist = Infinity, i, p, d;
    for (i = 0; i < statoMappa.punti.length; i++) {
      p = statoMappa.punti[i];
      d = Math.abs(p.lat - lat) + Math.abs(p.lon - lon);
      if (d < dist) { dist = d; vicino = p; }
    }
    var v = statoMappa.variabile;
    var val = vicino ? valorePunto(vicino, v, statoMappa.indice) : null;
    var testoVal = (v.tempo)
      ? etichettaTempo(val)
      : (val === null ? 'dato non disponibile' : (Math.round(val * 10) / 10) + ' ' + v.unita);
    var iconaHtml = (v.tempo && val !== null) ? htmlIconaTempo(val, 'cmi-icona-meteo') : '';
    var contenuto = '<p style="margin:0 0 .3rem"><strong>' + arrotonda(lat, 2) + '°N, ' + arrotonda(lon, 2) + '°E</strong></p>' +
      '<p style="margin:0;display:flex;align-items:center;gap:.4rem">' + iconaHtml + ' ' + v.nome + ': ' + testoVal + '</p>' +
      '<p style="margin:.3rem 0 0;font-size:.9em">Meteogramma nelle prossime 72 ore sotto la cartina.</p>';
    if (mappa && window.L) {
      L.popup().setLatLng(latlng || L.latLng(lat, lon)).setContent(contenuto).openOn(mappa);
    }
    var box = $('cmi-meteogramma');
    var dove = $('cmi-meteo-dove');
    var valori = $('cmi-meteo-valori');
    var grafico = $('cmi-meteo-grafico');
    if (!box) return;
    box.hidden = false;
    dove.textContent = 'Punto ' + arrotonda(lat, 2) + '°N, ' + arrotonda(lon, 2) + '°E · ' +
      (statoMappa.modello ? statoMappa.modello.nome : '') + ' · validità ' + formatOra(statoMappa.orari[statoMappa.indice]);
    valori.textContent = '';
    function voce(dt, dd) {
      var a = document.createElement('dt'); a.textContent = dt;
      var b = document.createElement('dd'); b.textContent = dd;
      valori.appendChild(a); valori.appendChild(b);
    }
    if (v.tempo) {
      var riga = document.createElement('div');
      riga.className = 'cmi-meteo-icona-ora';
      riga.innerHTML = iconaHtml + '<span>' + testoVal + '</span>';
      valori.appendChild(riga);
    } else {
      voce('Valore sulla cartina', testoVal);
    }
    grafico.textContent = 'Carico il meteogramma…';
    var mid = statoMappa.modello ? statoMappa.modello.id : $('cmi-modello').value;
    var campiMeteo = [
      'temperature_2m,precipitation,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code,cloud_cover,relative_humidity_2m,snowfall,cape',
      'temperature_2m,precipitation,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code,cloud_cover,relative_humidity_2m,snowfall',
      'temperature_2m,precipitation,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code,cloud_cover,relative_humidity_2m'
    ];
    function urlMeteogramma(campi) {
      return API + '?latitude=' + arrotonda(lat, 4) + '&longitude=' + arrotonda(lon, 4) +
        '&hourly=' + encodeURIComponent(campi) +
        '&forecast_hours=72&timezone=' + encodeURIComponent(TZ) +
        '&wind_speed_unit=kmh&cell_selection=nearest&models=' + encodeURIComponent(mid);
    }
    function scaricaMeteogramma(i) {
      return fetchJson(urlMeteogramma(campiMeteo[i])).catch(function (err) {
        if (i < campiMeteo.length - 1) return scaricaMeteogramma(i + 1);
        throw err;
      });
    }
    scaricaMeteogramma(0).then(function (body) {
      var lista = Array.isArray(body) ? body : [body];
      var h = (lista[0] && lista[0].hourly) || {};
      var idx = 0;
      var oraIso = statoMappa.orari[statoMappa.indice];
      if (h.time && oraIso) {
        for (i = 0; i < h.time.length; i++) if (h.time[i] === oraIso) { idx = i; break; }
      }
      function n(arr) { return arr && arr[idx] !== null && typeof arr[idx] !== 'undefined' ? arr[idx] : null; }
      valori.textContent = '';
      var codeOra = n(h.weather_code);
      if (codeOra !== null || v.tempo) {
        var riga2 = document.createElement('div');
        riga2.className = 'cmi-meteo-icona-ora';
        riga2.innerHTML = htmlIconaTempo(codeOra !== null ? codeOra : val, 'cmi-icona-meteo') +
          '<span>' + etichettaTempo(codeOra !== null ? codeOra : val) + '</span>';
        valori.appendChild(riga2);
      } else {
        voce('Valore sulla cartina', testoVal);
      }
      var t = n(h.temperature_2m); if (t !== null) voce('Temperatura nel punto', Math.round(t * 10) / 10 + ' °C');
      var pr = n(h.pressure_msl); if (pr !== null) voce('Pressione', Math.round(pr) + ' hPa');
      var ws = n(h.wind_speed_10m); var wd = n(h.wind_direction_10m);
      if (ws !== null) voce('Vento', Math.round(ws) + ' km/h' + (wd !== null ? ' da ' + Math.round(wd) + '°' : ''));
      var pc = n(h.precipitation); if (pc !== null) voce('Precipitazioni', Math.round(pc * 10) / 10 + ' mm');
      var rh = n(h.relative_humidity_2m); if (rh !== null) voce('Umidità', Math.round(rh) + ' %');
      var cc = n(h.cloud_cover); if (cc !== null) voce('Nuvolosità', Math.round(cc) + ' %');
      var sn = n(h.snowfall); if (sn !== null && sn > 0) voce('Neve', Math.round(sn * 10) / 10 + ' cm');
      var cp = n(h.cape); if (cp !== null) voce('CAPE', Math.round(cp) + ' J/kg');
      var wmo = n(h.weather_code);
      if (wmo === 96 || wmo === 99) voce('Grandine', 'Prevista dal modello (codice WMO ' + wmo + ')');
      else if (cp !== null && cp >= 1000 && wmo !== null && (wmo === 95 || wmo === 97 || wmo >= 80)) {
        voce('Indizio convettivo', "CAPE elevato. Non è un'allerta ufficiale e il modello non indica grandine (96/99).");
      }
      renderMeteogramma(grafico, h);
    }).catch(function () {
      grafico.textContent = 'Non è stato possibile caricare il meteogramma per questo punto.';
    });
  }
  function renderMeteogramma(dest, h) {
    dest.textContent = '';
    var times = h.time || [];
    var n = Math.min(times.length, 72);
    if (!n) { dest.textContent = 'Nessun dato orario per il meteogramma.'; return; }
    var W = 720, H = 310, padL = 42, padR = 16, padT = 40, padB = 36;
    var i, tmin = Infinity, tmax = -Infinity, pmax = 0.4;
    for (i = 0; i < n; i++) {
      var tv = h.temperature_2m ? h.temperature_2m[i] : null;
      var pv = h.precipitation ? h.precipitation[i] : null;
      if (tv !== null && typeof tv !== 'undefined') {
        if (tv < tmin) tmin = tv;
        if (tv > tmax) tmax = tv;
      }
      if (pv !== null && pv > pmax) pmax = pv;
    }
    if (!isFinite(tmin)) { tmin = 0; tmax = 10; }
    if (tmax - tmin < 6) { var midt = (tmax + tmin) / 2; tmin = midt - 3; tmax = midt + 3; }
    tmin = Math.floor(tmin) - 1;
    tmax = Math.ceil(tmax) + 1;
    function xdi(i) { return padL + i * (W - padL - padR) / Math.max(1, n - 1); }
    function yT(v) { return padT + (tmax - v) / (tmax - tmin) * (H - padT - padB); }
    function yP(v) { return (H - padB) - (v / pmax) * (H - padT - padB) * 0.38; }
    var ns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Meteogramma: tempo previsto, temperatura e precipitazioni nelle prossime 72 ore.');
    function el(name, attrs, text) {
      var e = document.createElementNS(ns, name);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (text) e.textContent = text;
      svg.appendChild(e);
      return e;
    }
    el('rect', { x: 0, y: 0, width: W, height: H, fill: '#f8fafc' });
    var g, y;
    for (g = 0; g <= 4; g++) {
      y = padT + g * (H - padT - padB) / 4;
      el('line', { x1: padL, y1: y, x2: W - padR, y2: y, stroke: '#d5dee8', 'stroke-width': 1 });
      var tvl = tmax - g * (tmax - tmin) / 4;
      el('text', { x: padL - 6, y: y + 4, 'text-anchor': 'end', fill: '#003366', 'font-size': 11, 'font-family': 'Titillium Web, Arial, sans-serif' }, Math.round(tvl) + '°');
    }
    var barW = Math.max(2, (W - padL - padR) / n * 0.7);
    for (i = 0; i < n; i++) {
      var prc = h.precipitation ? h.precipitation[i] : 0;
      if (!prc) continue;
      var bh = (H - padB) - yP(prc);
      el('rect', { x: xdi(i) - barW / 2, y: yP(prc), width: barW, height: bh, fill: 'rgba(30,90,180,0.55)' });
    }
    var dpath = '';
    for (i = 0; i < n; i++) {
      var te = h.temperature_2m ? h.temperature_2m[i] : null;
      if (te === null || typeof te === 'undefined') continue;
      dpath += (dpath ? ' L ' : 'M ') + xdi(i) + ' ' + yT(te);
    }
    if (dpath) el('path', { d: dpath, fill: 'none', stroke: '#b42318', 'stroke-width': 2.2, 'stroke-linejoin': 'round' });
    for (i = 0; i < n; i += 6) {
      el('text', { x: xdi(i), y: H - 12, 'text-anchor': 'middle', fill: '#3a3a3a', 'font-size': 10, 'font-family': 'Titillium Web, Arial, sans-serif' }, formatOraCorta(times[i]));
    }
    el('text', { x: padL, y: 14, fill: '#b42318', 'font-size': 11, 'font-family': 'Titillium Web, Arial, sans-serif', 'font-weight': 700 }, 'Temperatura (°C)');
    el('text', { x: W - padR, y: 14, 'text-anchor': 'end', fill: '#1e5ab4', 'font-size': 11, 'font-family': 'Titillium Web, Arial, sans-serif', 'font-weight': 700 }, 'Precipitazioni (mm)');
    if (h.weather_code) {
      for (i = 0; i < n; i += 3) {
        var wc = h.weather_code[i];
        var catI = categoriaDaCodice(wc);
        if (!catI) continue;
        var im = el('image', {
          href: urlIcona(catI),
          x: xdi(i) - 9,
          y: 16,
          width: 18,
          height: 18
        });
        im.setAttributeNS('http://www.w3.org/1999/xlink', 'href', urlIcona(catI));
      }
    }
    dest.appendChild(svg);
  }
  function spezza(arr, n) {
    var out = [];
    for (var i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
    return out;
  }
  function attesa(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }
  function fetchJson(url, tentativo) {
    tentativo = tentativo || 0;
    return fetch(url).then(function (res) {
      if (res.status === 429 && tentativo < 3) {
        return attesa(2000 * (tentativo + 1) * (tentativo + 1)).then(function () {
          return fetchJson(url, tentativo + 1);
        });
      }
      return res.json().then(function (body) {
        if (!res.ok || (body && body.error)) {
          var err = new Error((body && body.reason) || ('Errore ' + res.status));
          err.status = res.status;
          err.reason = body && body.reason;
          throw err;
        }
        return body;
      });
    });
  }
  function chiaveCache(modelId, varId, giorni) {
    return dominioId + '|' + modelId + '|' + varId + '|' + giorni;
  }

  function scaricaLocali(mid, giorni) {
    var comuni = (dominioCorrente().comuni || []).slice();
    if (!comuni.length) return Promise.resolve([]);
    var lats = [], lons = [], i;
    for (i = 0; i < comuni.length; i++) {
      lats.push(comuni[i].lat);
      lons.push(comuni[i].lon);
    }
    var candidati = [
      'weather_code,temperature_2m,precipitation,cloud_cover,snowfall,cape',
      'weather_code,temperature_2m,precipitation,cloud_cover',
      'weather_code,temperature_2m'
    ];
    function urlCampi(campi) {
      return API + '?latitude=' + lats.join(',') +
        '&longitude=' + lons.join(',') +
        '&hourly=' + encodeURIComponent(campi) +
        '&forecast_days=' + giorni +
        '&timezone=' + encodeURIComponent(TZ) +
        '&cell_selection=nearest' +
        '&models=' + encodeURIComponent(mid);
    }
    function prova(idx) {
      return fetchJson(urlCampi(candidati[idx])).catch(function (err) {
        if (idx < candidati.length - 1) return prova(idx + 1);
        throw err;
      });
    }
    return prova(0).then(function (body) {
      var lista = Array.isArray(body) ? body : [body];
      var out = [], d, h, c;
      for (i = 0; i < comuni.length; i++) {
        c = comuni[i];
        d = lista[i] || {};
        h = d.hourly || {};
        out.push({
          nome: c.nome,
          etichetta: c.etichetta || c.nome,
          lat: c.lat,
          lon: c.lon,
          allinea: c.allinea || 's',
          allinea2: c.allinea2 || c.allinea || 's',
          off: c.off || null,
          off2: c.off2 || null,
          livello: c.livello || 1,
          evidenziato: !!c.evidenziato,
          priorita: c.priorita || (i + 20),
          orari: h.time || [],
          code: h.weather_code || [],
          temp: h.temperature_2m || [],
          cape: h.cape || [],
          snow: h.snowfall || []
        });
      }
      return out;
    }).catch(function () { return []; });
  }
  function caricaGriglia(target, opzioni) {
    opzioni = opzioni || {};
    var isB = target === 'b';
    var mid = isB ? $('cmi-modello-b').value : $('cmi-modello').value;
    var vid = $('cmi-variabile').value;
    var modello = modelloById(mid);
    var variabile = variabileById(vid);
    var giorni = Math.min(modello.giorni, 7);
    var key = chiaveCache(mid, vid, giorni);
    if (!isB) {
      fermaPlay(false);
      aggiornaInfoModello();
      aggiornaInfoVariabile();
    }
    if (cache[key]) {
      applicaDati(cache[key], variabile, modello, target, opzioni.mantieniOra);
      return Promise.resolve();
    }
    if (!isB) {
      impostaStato('Scarico i dati del modello ' + modello.nome + '…', false, true);
      $('cmi-ora').disabled = true;
    }
    var puntiBase = costruisciGriglia();
    var campi = variabile.campi.join(',');
    function procediConCampi(elencoCampi) {
      campi = elencoCampi.join(',');
      return eseguiScarico();
    }
    function scopriCampiTempo(modelId) {
      if (campiTempoPerModello[modelId]) return Promise.resolve(campiTempoPerModello[modelId]);
      var candidati = ['weather_code', 'cloud_cover', 'precipitation', 'snowfall', 'cape', 'showers'];
      function prova(lista) {
        var url = API + '?latitude=' + GENZANO.lat + '&longitude=' + GENZANO.lon +
          '&hourly=' + encodeURIComponent(lista.join(',')) +
          '&forecast_days=1&timezone=' + encodeURIComponent(TZ) +
          '&models=' + encodeURIComponent(modelId);
        return fetchJson(url).then(function () {
          campiTempoPerModello[modelId] = lista;
          return lista;
        }).catch(function (err) {
          if (lista.length <= 1) throw err;
          return prova(lista.slice(0, lista.length - 1));
        });
      }
      return prova(candidati);
    }
    function eseguiScarico() {
    function urlGruppo(gruppo) {
      var lats = [], lons = [];
      for (var i = 0; i < gruppo.length; i++) {
        lats.push(gruppo[i].lat);
        lons.push(gruppo[i].lon);
      }
      return API + '?latitude=' + lats.join(',') +
        '&longitude=' + lons.join(',') +
        '&hourly=' + encodeURIComponent(campi) +
        '&forecast_days=' + giorni +
        '&timezone=' + encodeURIComponent(TZ) +
        '&wind_speed_unit=kmh' +
        '&cell_selection=nearest' +
        '&models=' + encodeURIComponent(mid);
    }
    function chiediGruppo(gruppo) {
      if (!gruppo.length) return Promise.resolve([]);
      return fetchJson(urlGruppo(gruppo)).then(function (body) {
        var lista = Array.isArray(body) ? body : [body];
        var out = [];
        for (var i = 0; i < lista.length; i++) out.push({ punto: gruppo[i] || null, dati: lista[i] });
        return out;
      }).catch(function () {
        if (gruppo.length === 1) return [];
        var meta = Math.ceil(gruppo.length / 2);
        return chiediGruppo(gruppo.slice(0, meta)).then(function (a) {
          return chiediGruppo(gruppo.slice(meta)).then(function (b) { return a.concat(b); });
        });
      });
    }
    var gruppi = spezza(puntiBase, BATCH);
    var catena = Promise.resolve([]);
    gruppi.forEach(function (gruppo) {
      catena = catena.then(function (acc) {
        return chiediGruppo(gruppo).then(function (pezzi) { return acc.concat(pezzi); });
      });
    });
    return catena.then(function (lista) {
      var orari = null;
      var punti = [];
      var campoVal = variabile.tempo ? 'weather_code' : (variabile.vento ? variabile.vento.vel : variabile.campi[0]);
      var campoDir = variabile.vento ? variabile.vento.dir : null;
      var tuttiNull = true;
      for (var i = 0; i < lista.length; i++) {
        var item = lista[i] || {};
        var d = item.dati || {};
        var h = d.hourly || {};
        if (!orari) orari = h.time || [];
        var serie = h[campoVal] || [];
        var dirs = campoDir ? (h[campoDir] || []) : null;
        var haDato = false;
        for (var k = 0; k < serie.length; k++) {
          if (serie[k] !== null && typeof serie[k] !== 'undefined') { haDato = true; tuttiNull = false; break; }
        }
        if (!haDato) continue;
        punti.push({
          lat: item.punto ? item.punto.lat : d.latitude,
          lon: item.punto ? item.punto.lon : d.longitude,
          val: serie,
          dir: dirs,
          prec: h.precipitation || null,
          snow: h.snowfall || null,
          cape: h.cape || null,
          showers: h.showers || null,
          nubi: h.cloud_cover || null
        });
      }
      if (!orari || !orari.length || tuttiNull || !punti.length) {
        if (!isB) marcaNonDisponibile(mid, vid);
        throw new Error('Questa grandezza non è disponibile per il modello scelto, oppure il modello non copre l\'Italia in questo punto.');
      }
      var pacchetto = { punti: punti, orari: orari, scaricatoIl: new Date(), fuoriDominio: punti.length < puntiBase.length * 0.7, locali: [] };
      var dopo = variabile.tempo ? scaricaLocali(mid, giorni) : Promise.resolve([]);
      return dopo.then(function (locali) {
        pacchetto.locali = locali || [];
        cache[key] = pacchetto;
        applicaDati(pacchetto, variabile, modello, target, opzioni.mantieniOra);
      });
    }).catch(function (err) {
      var msg = (err && err.message) ? err.message : 'Non è stato possibile scaricare i dati.';
      if (err && err.reason && /hourly|invalid string|weather variable/i.test(err.reason)) {
        if (!isB) marcaNonDisponibile(mid, vid);
        msg = 'Questa grandezza non è disponibile per il modello ' + modello.nome + '. Scegline un\'altra.';
      }
      if (!isB) impostaStato(msg, true, false);
      else impostaStato('Confronto: ' + msg, true, false);
    });
    }
    if (variabile.tempo) {
      return scopriCampiTempo(mid).then(function (elenco) { return procediConCampi(elenco); });
    }
    return procediConCampi(variabile.campi);
  }
  function applicaDati(pacchetto, variabile, modello, target, mantieniOra) {
    var isB = target === 'b';
    var stato = isB ? statoMappaB : statoMappa;
    stato.punti = pacchetto.punti;
    stato.orari = pacchetto.orari;
    stato.variabile = variabile;
    stato.modello = modello;
    stato.scaricatoIl = pacchetto.scaricatoIl;
    stato.locali = pacchetto.locali || [];
    var indici = [];
    for (var i = 0; i < pacchetto.orari.length; i++) {
      if (i % 3 === 0 || i === pacchetto.orari.length - 1) indici.push(i);
    }
    stato.passi = indici;
    var meglio = 0, dist = Infinity, p, t, d;
    var ancora = (mantieniOra && statoMappa.orari[statoMappa.indice]) || (!isB && oraIniziale) || null;
    if (ancora) {
      for (p = 0; p < indici.length; p++) {
        if (pacchetto.orari[indici[p]] === ancora) { meglio = p; dist = 0; break; }
      }
    }
    if (dist !== 0) {
      var oraRif = ancora ? Date.parse(ancora) : Date.now();
      for (p = 0; p < indici.length; p++) {
        t = Date.parse(pacchetto.orari[indici[p]]);
        d = Math.abs(t - oraRif);
        if (d < dist) { dist = d; meglio = p; }
      }
    }
    stato.indicePasso = meglio;
    stato.indice = indici[meglio];
    stato.matrice = costruisciMatrice(stato.punti, stato.variabile, stato.indice);
    if (!isB) {
      ultimoAggiornamento = pacchetto.scaricatoIl;
      var sl = $('cmi-ora');
      sl.disabled = false;
      sl.min = 0;
      sl.max = String(indici.length - 1);
      sl.value = String(meglio);
      aggiornaOraUI();
      aggiornaLegenda();
      if (strato) strato.ridisegna();
      if (confrontoAttivo() && statoMappaB.orari.length) allineaB();
      var extra = pacchetto.fuoriDominio ? ' Il modello non copre tutta l\'area scelta: le zone fuori dal dominio restano senza colore.' : '';
      impostaStato('Cartina pronta: ' + dominioCorrente().nome + ', ' + modello.nome + ', ' + variabile.nome + '.' + extra, false, false);
      aggiornaCorsa();
      assicuraMarcatoreGenzano();
      aggiornaUrl();
      if (!isB) oraIniziale = null;
      if (prontoRisovi) { prontoRisovi(); prontoRisovi = null; }
    } else {
      allineaB();
      if (stratoB) stratoB.ridisegna();
      assicuraMarcatoreGenzano();
      aggiornaEtichetteConfronto();
    }
  }
  function allineaB() {
    if (!statoMappaB.orari.length || !statoMappa.orari.length) return;
    var iso = statoMappa.orari[statoMappa.indice];
    var i, meglio = 0, dist = Infinity, d;
    for (i = 0; i < statoMappaB.orari.length; i++) {
      if (statoMappaB.orari[i] === iso) { meglio = i; dist = 0; break; }
      d = Math.abs(Date.parse(statoMappaB.orari[i]) - Date.parse(iso));
      if (d < dist) { dist = d; meglio = i; }
    }
    statoMappaB.indice = meglio;
    if (statoMappaB.passi) {
      var p, bestP = 0, bestD = Infinity;
      for (p = 0; p < statoMappaB.passi.length; p++) {
        d = Math.abs(statoMappaB.passi[p] - meglio);
        if (d < bestD) { bestD = d; bestP = p; }
      }
      statoMappaB.indicePasso = bestP;
      statoMappaB.indice = statoMappaB.passi[bestP];
    }
    statoMappaB.matrice = costruisciMatrice(statoMappaB.punti, statoMappaB.variabile, statoMappaB.indice);
    if (stratoB) stratoB.ridisegna();
  }
  function aggiornaOraUI() {
    var iso = statoMappa.orari[statoMappa.indice];
    var el = $('cmi-ora-etichetta');
    if (el) el.textContent = formatOra(iso);
  }
  function aggiornaLegenda() {
    var v = statoMappa.variabile;
    if (!v) return;
    var scala = $('cmi-legenda-scala');
    scala.innerHTML = '';
    if (v.tempo) {
      $('cmi-legenda-titolo').textContent = 'Legenda: Tempo previsto';
      var griglia = document.createElement('div');
      griglia.className = 'cmi-legenda-icone';
      LEGENDA_TEMPO.forEach(function (item) {
        var voce = document.createElement('div');
        voce.className = 'cmi-legenda-voce';
        var img = document.createElement('img');
        img.src = urlIcona(item.id);
        img.alt = '';
        img.width = 32;
        img.height = 32;
        var sp = document.createElement('span');
        sp.textContent = item.nome;
        voce.appendChild(img);
        voce.appendChild(sp);
        griglia.appendChild(voce);
      });
      scala.appendChild(griglia);
      var nota = document.createElement('p');
      nota.className = 'cmi-legenda-note';
      nota.textContent = "Le icone mostrano il tempo previsto all'ora scelta nel comune. Sotto: temperatura minima (in blu) e massima (in rosso) del giorno di calendario mostrato, secondo il modello scelto. Un piccolo triangolo arancione su un temporale indica CAPE elevato (almeno 1000 J/kg): è un indizio convettivo, non un'allerta ufficiale. I temporali con grandine (codici WMO 96 e 99) arrivano solo da alcuni modelli.";
      scala.appendChild(nota);
      return;
    }
    var ext = etichettaScala(v.scala);
    $('cmi-legenda-titolo').textContent = 'Legenda: ' + v.nome + (v.unita ? ' (' + v.unita + ')' : '');
    var barra = document.createElement('div');
    barra.className = 'cmi-legenda-barra';
    barra.style.background = gradiente(v.scala);
    var vals = document.createElement('div');
    vals.className = 'cmi-legenda-valori';
    var a = document.createElement('span'); a.textContent = String(ext.min);
    var b = document.createElement('span'); b.textContent = String(ext.max) + ' ' + v.unita;
    vals.appendChild(a); vals.appendChild(b);
    scala.appendChild(barra); scala.appendChild(vals);
  }
  function aggiornaCorsa() {
    var el = $('cmi-corsa');
    if (!el || !statoMappa.modello) return;
    var m = statoMappa.modello;
    var quando = formatDataOraLocale(ultimoAggiornamento || statoMappa.scaricatoIl);
    el.innerHTML = '<strong>Ultima corsa:</strong> Open-Meteo non comunica l\'ora di inizializzazione della corsa; il modello ' +
      m.nome + ' si aggiorna ' + m.aggiornamento + '.<br>' +
      '<strong>Aggiornato alle:</strong> ' + quando + ' (ora locale Europe/Rome). Fonte: Open-Meteo, licenza CC BY 4.0.' + (m.attribuzione ? (' Modello: ' + m.attribuzione + '.') : '') + ' Confini: Natural Earth, pubblico dominio.';
  }
  function aggiornaEtichetteConfronto() {
    var a = $('cmi-etichetta-a');
    var b = $('cmi-etichetta-b');
    if (a) a.textContent = statoMappa.modello ? ('Modello A: ' + statoMappa.modello.nome) : 'Modello A';
    if (b) b.textContent = statoMappaB.modello ? ('Modello B: ' + statoMappaB.modello.nome) : 'Modello B';
  }
  function assicuraMarcatoreGenzano() {
    if (!window.L) return;
    if (statoMappa.variabile && statoMappa.variabile.tempo) {
      if (markerGenzano && mappa) { mappa.removeLayer(markerGenzano); markerGenzano = null; }
      if (markerGenzanoB && mappaB) { mappaB.removeLayer(markerGenzanoB); markerGenzanoB = null; }
      return;
    }
    var opt = { radius: 6, color: '#ffbe2e', weight: 2, fillColor: '#003366', fillOpacity: 1 };
    if (mappa) {
      if (markerGenzano) mappa.removeLayer(markerGenzano);
      markerGenzano = L.circleMarker([GENZANO.lat, GENZANO.lon], opt).addTo(mappa);
      markerGenzano.bindTooltip('Genzano di Roma');
    }
    if (mappaB) {
      if (markerGenzanoB) mappaB.removeLayer(markerGenzanoB);
      markerGenzanoB = L.circleMarker([GENZANO.lat, GENZANO.lon], opt).addTo(mappaB);
      markerGenzanoB.bindTooltip('Genzano di Roma');
    }
  }
  function vaiAPasso(n) {
    if (!statoMappa.passi || !statoMappa.passi.length) return;
    var max = statoMappa.passi.length - 1;
    if (n < 0) n = max;
    if (n > max) n = 0;
    statoMappa.indicePasso = n;
    statoMappa.indice = statoMappa.passi[n];
    statoMappa.matrice = costruisciMatrice(statoMappa.punti, statoMappa.variabile, statoMappa.indice);
    $('cmi-ora').value = String(n);
    aggiornaOraUI();
    if (strato) strato.ridisegna();
    if (confrontoAttivo()) allineaB();
    aggiornaUrl();
  }
  function fermaPlay(aggiornaBottone) {
    if (timerPlay) { clearInterval(timerPlay); timerPlay = null; }
    if (aggiornaBottone !== false) {
      var btn = $('cmi-play');
      btn.setAttribute('aria-pressed', 'false');
      $('cmi-play-etichetta').textContent = 'Avvia animazione';
      btn.classList.remove('cmi-play-on');
      var icon = btn.querySelector('i');
      if (icon) icon.className = 'bi bi-play-fill';
    }
  }
  function avviaPlay() {
    var attesa = durataFrame();
    fermaPlay(false);
    var btn = $('cmi-play');
    btn.setAttribute('aria-pressed', 'true');
    btn.classList.add('cmi-play-on');
    $('cmi-play-etichetta').textContent = 'Pausa';
    var icon = btn.querySelector('i');
    if (icon) icon.className = 'bi bi-pause-fill';
    timerPlay = setInterval(function () {
      vaiAPasso((statoMappa.indicePasso || 0) + 1);
    }, attesa);
  }

  function caricaCitta() {
    var lats = [], lons = [];
    for (var i = 0; i < CITTA.length; i++) { lats.push(CITTA[i].lat); lons.push(CITTA[i].lon); }
    var url = API + '?latitude=' + lats.join(',') +
      '&longitude=' + lons.join(',') +
      '&daily=' + encodeURIComponent('weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max') +
      '&forecast_days=5&timezone=' + encodeURIComponent(TZ) +
      '&wind_speed_unit=kmh&models=ecmwf_ifs';
    $('cmi-citta-stato').textContent = 'Aggiorno le temperature delle città…';
    return fetchJson(url).then(function (body) {
      var lista = Array.isArray(body) ? body : [body];
      datiCitta = lista;
      renderCitta(lista);
      $('cmi-citta-stato').textContent = 'Temperature di oggi e prossimi giorni: modello ECMWF IFS a 9 km, via Open-Meteo.';
    }).catch(function () {
      $('cmi-citta-stato').textContent = 'Non è stato possibile aggiornare le temperature delle città. Il bollettino scritto resta disponibile.';
      var vuoto = $('cmi-citta-vuoto');
      if (vuoto) vuoto.textContent = 'Temperature in diretta non disponibili in questo momento.';
    });
  }
  function renderCitta(lista) {
    var wrap = $('cmi-citta-lista');
    wrap.textContent = '';
    var markers = [];
    for (var i = 0; i < CITTA.length; i++) {
      var c = CITTA[i];
      var d = lista[i] || {};
      var day = d.daily || {};
      var tmin = day.temperature_2m_min ? day.temperature_2m_min[0] : null;
      var tmax = day.temperature_2m_max ? day.temperature_2m_max[0] : null;
      var code = day.weather_code ? day.weather_code[0] : null;
      var desc = (code !== null && typeof CODICI[code] !== 'undefined') ? CODICI[code] : 'Tempo non indicato';
      var scheda = document.createElement('article');
      scheda.className = 'cmi-citta-scheda' + (c.locale ? ' cmi-citta-genzano' : '');
      var h = document.createElement('h4');
      h.className = 'cmi-citta-nome';
      h.textContent = c.nome;
      var p = document.createElement('p');
      p.className = 'cmi-citta-temp';
      p.textContent = (tmin === null ? '—' : Math.round(tmin) + '°') + ' / ' + (tmax === null ? '—' : Math.round(tmax) + '°');
      var q = document.createElement('p');
      q.className = 'cmi-citta-desc';
      q.textContent = desc;
      scheda.appendChild(h); scheda.appendChild(p); scheda.appendChild(q);
      wrap.appendChild(scheda);
      if (mappaCitta && window.L && !c.soloScheda) {
        var html = '<div class="cmi-marker' + (c.locale ? ' cmi-marker-genzano' : '') + '">' +
          '<span class="cmi-marker-nome">' + c.nome + '</span>' +
          '<span class="cmi-marker-temp">' + (tmin === null ? '—' : Math.round(tmin)) + '° / ' + (tmax === null ? '—' : Math.round(tmax)) + '°</span></div>';
        var icon = L.divIcon({ className: '', html: html, iconSize: [108, 34], iconAnchor: [54, 17] });
        markers.push(L.marker([c.lat, c.lon], { icon: icon, keyboard: true, title: c.nome + ', ' + desc, zIndexOffset: c.locale ? 1000 : 0 }));
      }
    }
    if (mappaCitta && markers.length) {
      if (mappaCitta._cmiLayer) mappaCitta.removeLayer(mappaCitta._cmiLayer);
      mappaCitta._cmiLayer = L.layerGroup(markers).addTo(mappaCitta);
      mappaCitta.fitBounds(L.latLngBounds([[36.4, 6.6], [47.2, 18.7]]), { padding: [16, 16], maxZoom: 7 });
    }
    renderSchedeGenzano(lista);
  }
  function renderSchedeGenzano(lista) {
    var dest = $('cmi-schede-giorni');
    dest.textContent = '';
    var d = lista[0] || {};
    var day = d.daily || {};
    var times = day.time || [];
    for (var i = 0; i < times.length; i++) {
      var art = document.createElement('article');
      art.className = 'cmi-scheda-giorno';
      var g = document.createElement('div'); g.className = 'giorno'; g.textContent = formatDataBreve(times[i]);
      var code = day.weather_code ? day.weather_code[i] : null;
      var ic = document.createElement('div'); ic.className = 'icona';
      ic.setAttribute('aria-hidden', 'true');
      ic.innerHTML = iconaMeteo(code);
      var t = document.createElement('div'); t.className = 'temp';
      var tmin = day.temperature_2m_min ? day.temperature_2m_min[i] : null;
      var tmax = day.temperature_2m_max ? day.temperature_2m_max[i] : null;
      t.textContent = (tmin === null ? '—' : Math.round(tmin) + '°') + ' / ' + (tmax === null ? '—' : Math.round(tmax) + '°');
      var det = document.createElement('p'); det.className = 'dettaglio';
      var rain = day.precipitation_sum ? day.precipitation_sum[i] : null;
      var gust = day.wind_gusts_10m_max ? day.wind_gusts_10m_max[i] : null;
      var parti = [];
      if (code !== null && typeof CODICI[code] !== 'undefined') parti.push(CODICI[code]);
      if (rain !== null) parti.push(Math.round(rain * 10) / 10 + ' mm');
      if (gust !== null) parti.push('raffiche ' + Math.round(gust) + ' km/h');
      det.textContent = parti.join(' · ');
      art.appendChild(g); art.appendChild(ic); art.appendChild(t); art.appendChild(det);
      dest.appendChild(art);
    }
  }
  function iconaMeteo(code) {
    var svgHtml = htmlIconaTempo(code, 'cmi-icona-meteo');
    if (svgHtml) return svgHtml;
    var cls = 'bi-cloud';
    if (code === 0 || code === 1) cls = 'bi-sun';
    else if (code === 2) cls = 'bi-cloud-sun';
    else if (code === 3) cls = 'bi-cloud';
    else if (code === 45 || code === 48) cls = 'bi-cloud-fog2';
    else if (code === 71 || code === 73 || code === 75 || code === 77 || code === 85 || code === 86) cls = 'bi-snow';
    else if (code === 95 || code === 96 || code === 97 || code === 99) cls = 'bi-cloud-lightning-rain';
    else if (code !== null) cls = 'bi-cloud-rain';
    return '<i class="bi ' + cls + '"></i>';
  }
  function messaggioCondividi(txt) {
    var el = $('cmi-condividi-esito');
    if (el) el.textContent = txt || '';
  }
  function urlPagina() { return window.location.href.split('#')[0]; }
  function testoCondivisione() {
    var b = (leggiConfig().bollettino) || {};
    var titolo = 'Previsioni meteo per l\'Italia';
    var testo = (b.situazione_generale || titolo) + ' ' + urlPagina();
    return { title: titolo, text: testo, url: urlPagina() };
  }
  function copiaLink() {
    var url = urlPagina();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(url).then(function () {
        messaggioCondividi('Collegamento copiato.');
      }).catch(function () { fallbackCopia(url); });
    }
    fallbackCopia(url);
    return Promise.resolve();
  }
  function fallbackCopia(testo) {
    var ta = document.createElement('textarea');
    ta.value = testo;
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      messaggioCondividi('Collegamento copiato.');
    } catch (e) {
      messaggioCondividi('Copia questo collegamento: ' + testo);
    }
    document.body.removeChild(ta);
  }
  function condividi() {
    var p = testoCondivisione();
    if (navigator.share) {
      navigator.share(p).then(function () {
        messaggioCondividi('Condivisione avviata.');
      }).catch(function (err) {
        if (err && err.name === 'AbortError') return;
        copiaLink();
      });
    } else {
      copiaLink();
    }
  }
  function wrapText(ctx, text, x, y, maxWidth, lineHeight, maxLines) {
    var words = String(text || '').split(/\s+/);
    var line = '';
    var lines = 0;
    for (var n = 0; n < words.length; n++) {
      var test = line ? (line + ' ' + words[n]) : words[n];
      if (ctx.measureText(test).width > maxWidth && line) {
        ctx.fillText(line, x, y);
        line = words[n];
        y += lineHeight;
        lines += 1;
        if (maxLines && lines >= maxLines) {
          ctx.fillText('…', x, y);
          return y + lineHeight;
        }
      } else {
        line = test;
      }
    }
    if (line) { ctx.fillText(line, x, y); y += lineHeight; }
    return y;
  }

  function costruisciCanvasBollettino() {
    var canvas = document.createElement('canvas');
    canvas.width = 1080;
    canvas.height = 1350;
    var ctx = canvas.getContext('2d');
    var b = (leggiConfig().bollettino) || {};
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, 0, 1080, 220);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 28px Titillium Web, Arial, sans-serif';
    ctx.fillText('Protezione Civile Genzano di Roma', 48, 70);
    ctx.font = 'bold 46px Titillium Web, Arial, sans-serif';
    ctx.fillText('Previsioni meteo per l\'Italia', 48, 130);
    ctx.font = '24px Titillium Web, Arial, sans-serif';
    ctx.fillText('Emesso il ' + formatEmesso(b.emesso_il) + '  ·  Valido dal ' + formatDataIt(b.validita_da) + ' al ' + formatDataIt(b.validita_a), 48, 180);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 220, 1080, 1130);
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, 220, 1080, 8);
    ctx.fillStyle = '#1a1a1a';
    ctx.font = '28px Titillium Web, Arial, sans-serif';
    var y = wrapText(ctx, b.situazione_generale || '', 48, 280, 984, 38, 8);
    y += 20;
    ctx.fillStyle = '#003366';
    ctx.font = 'bold 32px Titillium Web, Arial, sans-serif';
    ctx.fillText('Oggi nelle città', 48, y);
    y += 20;
    if (datiCitta) {
      var colW = 486, rowH = 48, startY = y + 10, col = 0;
      for (var i = 0; i < CITTA.length; i++) {
        var c = CITTA[i];
        var day = (datiCitta[i] && datiCitta[i].daily) || {};
        var tmin = day.temperature_2m_min ? day.temperature_2m_min[0] : null;
        var tmax = day.temperature_2m_max ? day.temperature_2m_max[0] : null;
        var x = 48 + col * (colW + 12);
        var yy = startY + Math.floor(i / 2) * rowH;
        ctx.fillStyle = c.locale ? '#eef4fa' : '#f4f7fa';
        ctx.fillRect(x, yy, colW, rowH - 8);
        ctx.fillStyle = '#003366';
        ctx.font = 'bold 24px Titillium Web, Arial, sans-serif';
        ctx.fillText(c.nome, x + 12, yy + 32);
        ctx.font = '24px Titillium Web, Arial, sans-serif';
        var temp = (tmin === null ? '—' : Math.round(tmin) + '°') + ' / ' + (tmax === null ? '—' : Math.round(tmax) + '°');
        ctx.fillText(temp, x + colW - 12 - ctx.measureText(temp).width, yy + 32);
        col = 1 - col;
      }
      y = startY + Math.ceil(CITTA.length / 2) * rowH + 20;
    }
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 1188, 1080, 72);
    ctx.fillStyle = '#3a2e0e';
    ctx.font = '20px Titillium Web, Arial, sans-serif';
    wrapText(ctx, 'Non è un\'allerta ufficiale. Per i colori di allerta consulta la pagina Allerte meteo del sito. In emergenza chiama il 112.', 48, 1214, 984, 26, 2);
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, 1260, 1080, 90);
    ctx.fillStyle = '#ffffff';
    ctx.font = '22px Titillium Web, Arial, sans-serif';
    ctx.fillText('protezionecivilegenzano.it/cartina-meteo-italia/', 48, 1300);
    ctx.font = '20px Titillium Web, Arial, sans-serif';
    ctx.fillText('Dati modellistici: Open-Meteo, licenza CC BY 4.0.' + testoCreditoModello(), 48, 1332);
    return caricaLogo().then(function (logo) {
      if (logo) {
        try { ctx.drawImage(logo, 920, 40, 110, 110); } catch (e) {}
      }
      return canvas;
    });
  }
  function caricaLogo() {
    return new Promise(function (resolve) {
      var logo = new Image();
      logo.onload = function () { resolve(logo); };
      logo.onerror = function () { resolve(null); };
      var cfg = leggiConfig();
      logo.src = cfg.logoUrl || '/images/logo-pc-genzano.png';
    });
  }
  function canvasToBlob(canvas, tipo) {
    return new Promise(function (resolve) {
      canvas.toBlob(function (blob) { resolve(blob || null); }, tipo || 'image/png');
    });
  }
  function scaricaBlob(blob, nome) {
    if (!blob) return;
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = nome;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
  function scaricaImmagine() {
    return costruisciCanvasBollettino().then(function (canvas) {
      return canvasToBlob(canvas, 'image/png').then(function (blob) {
        var b = (leggiConfig().bollettino) || {};
        scaricaBlob(blob, 'previsioni-meteo-italia-' + (b.validita_da || 'bollettino') + '.png');
        messaggioCondividi('Immagine scaricata.');
        return blob;
      });
    });
  }
  function esportaBollettinoBlob() {
    return costruisciCanvasBollettino().then(function (canvas) {
      return canvasToBlob(canvas, 'image/png');
    });
  }
  function vistaMercatore(w, h, riservaBasso) {
    var d = dominioCorrente();
    var b = d.fit || [[d.latMin, d.lonMin], [d.latMax, d.lonMax]];
    function my(lat) { var r = lat * Math.PI / 180; return Math.log(Math.tan(Math.PI / 4 + r / 2)) * 180 / Math.PI; }
    var la0 = b[0][0], lo0 = b[0][1], la1 = b[1][0], lo1 = b[1][1];
    var pad = 10, hu = h - riservaBasso - 2 * pad, wu = w - 2 * pad;
    var sc = Math.min(wu / (lo1 - lo0), hu / (my(la1) - my(la0)));
    var ox = (w - (lo1 - lo0) * sc) / 2, oy = pad + (hu - (my(la1) - my(la0)) * sc) / 2;
    return {
      w: w,
      h: h,
      zoom: 0,
      zoomFit: 0,
      xy: function (lat, lon) { return [ox + (lon - lo0) * sc, oy + (my(la1) - my(lat)) * sc]; },
      inv: function (x, y) {
        var m = my(la1) - (y - oy) / sc;
        return { lon: lo0 + (x - ox) / sc, lat: (2 * Math.atan(Math.exp(m * Math.PI / 180)) - Math.PI / 2) * 180 / Math.PI };
      }
    };
  }
  function vistaFissa(w, h, pad) {
    pad = pad || 8;
    var W = LON_MAX - LON_MIN, Hgt = LAT_MAX - LAT_MIN;
    return {
      w: w,
      h: h,
      zoom: 0,
      zoomFit: 0,
      xy: function (lat, lon) {
        return [
          pad + (lon - LON_MIN) / W * (w - 2 * pad),
          pad + (LAT_MAX - lat) / Hgt * (h - 2 * pad)
        ];
      },
      inv: function (x, y) {
        return {
          lon: LON_MIN + ((x - pad) / (w - 2 * pad)) * W,
          lat: LAT_MAX - ((y - pad) / (h - 2 * pad)) * Hgt
        };
      }
    };
  }
  function costruisciFotogramma(stato, logo, w, h) {
    var canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    var ctx = canvas.getContext('2d');
    var haRilievo = !!(dominioCorrente().hillshade && hillshadeImg);
    var testata = 92, piede = haRilievo ? 96 : 78;
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, 0, w, testata);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 22px Titillium Web, Arial, sans-serif';
    ctx.fillText((dominioCorrente().titolo || 'Cartina meteo dell\'Italia'), 16, 28);
    ctx.font = '16px Titillium Web, Arial, sans-serif';
    ctx.fillText((stato.modello ? stato.modello.nome : '') + ' · ' + (stato.variabile ? stato.variabile.nome : ''), 16, 52);
    ctx.font = '15px Titillium Web, Arial, sans-serif';
    ctx.fillText('Validità: ' + formatOra(stato.orari[stato.indice]), 16, 74);
    if (logo) {
      try { ctx.drawImage(logo, w - 78, 10, 64, 64); } catch (e) {}
    }
    var mw = w, mh = h - testata - piede;
    var off = document.createElement('canvas');
    off.width = mw;
    off.height = mh;
    var octx = off.getContext('2d');
    var vista = (stato.variabile && stato.variabile.tempo) ? vistaMercatore(mw, mh, misureLegendaTempo({ w: mw, h: mh }).h + 18) : vistaFissa(mw, mh, 6);
    disegnaVista(octx, vista, stato, { frecce: true, decorazioni: true });
    ctx.drawImage(off, 0, testata);
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, h - piede, w, piede);
    ctx.fillStyle = '#ffffff';
    ctx.font = '14px Titillium Web, Arial, sans-serif';
    ctx.fillText('Dati: Open-Meteo, licenza CC BY 4.0.' + testoCreditoModello() + ' Confini: Natural Earth, pubblico dominio.', 16, h - (haRilievo ? 66 : 48));
    ctx.fillText('protezionecivilegenzano.it/cartina-meteo-italia/', 16, h - (haRilievo ? 46 : 28));
    if (haRilievo) ctx.fillText('Rilievo: Copernicus DEM GLO-30, Unione europea. Laghi: OpenStreetMap.', 16, h - 28);
    ctx.fillText('Aggiornato alle ' + formatDataOraLocale(ultimoAggiornamento || stato.scaricatoIl) + ' (Europe/Rome).', 16, h - 10);
    return canvas;
  }
  function mostraProgresso(visibile, testo, perc) {
    var wrap = $('cmi-export-progress');
    var lab = $('cmi-export-progress-testo');
    var bar = $('cmi-export-progress-barra');
    if (!wrap) return;
    wrap.hidden = !visibile;
    if (lab) lab.textContent = testo || '';
    if (bar) bar.style.width = Math.max(0, Math.min(100, perc || 0)) + '%';
  }
  function tick() {
    return new Promise(function (resolve) { setTimeout(resolve, 0); });
  }
  function indiciExport() {
    var passi = statoMappa.passi || [];
    if (passi.length <= 28) return passi.slice();
    var out = [], n = 28;
    for (var i = 0; i < n; i++) out.push(passi[Math.round(i * (passi.length - 1) / (n - 1))]);
    return out;
  }
  function esportaPngBlob() {
    if (!statoMappa.matrice) return Promise.reject(new Error('Cartina non pronta.'));
    return caricaLogo().then(function (logo) {
      var canvas = costruisciFotogramma(statoMappa, logo, 720, 900);
      return canvasToBlob(canvas, 'image/png');
    });
  }
  function scaricaPngCartina() {
    return esportaPngBlob().then(function (blob) {
      var iso = (statoMappa.orari[statoMappa.indice] || '').replace(/[:T]/g, '-').slice(0, 16);
      scaricaBlob(blob, 'cartina-meteo-italia-' + iso + '.png');
      impostaStato('Fotogramma PNG scaricato.', false, false);
      return blob;
    });
  }
  function esportaGifBlob() {
    if (!statoMappa.punti.length) return Promise.reject(new Error('Cartina non pronta.'));
    if (!window.CMI_GIF || !window.CMI_GIF.encode) {
      return Promise.reject(new Error('Encoder GIF non disponibile.'));
    }
    if (esportazioneInCorso) return Promise.reject(new Error('Esportazione già in corso.'));
    esportazioneInCorso = true;
    var W = 720, H = 900;
    var indici = indiciExport();
    var frames = [];
    var idxOrig = statoMappa.indice;
    mostraProgresso(true, 'Preparazione dell\'animazione…', 2);
    return caricaLogo().then(function (logo) {
      var catena = Promise.resolve();
      indici.forEach(function (idx, i) {
        catena = catena.then(function () {
          statoMappa.indice = idx;
          statoMappa.matrice = costruisciMatrice(statoMappa.punti, statoMappa.variabile, idx);
          var canvas = costruisciFotogramma(statoMappa, logo, W, H);
          var ctx = canvas.getContext('2d');
          var data = ctx.getImageData(0, 0, W, H).data;
          var cs = delayGifCs();
          var delay = (i === indici.length - 1) ? Math.min(200, cs * 2) : cs;
          frames.push({ data: data, delay: delay });
          mostraProgresso(true, 'Fotogramma ' + (i + 1) + ' di ' + indici.length + '…', Math.round(((i + 1) / (indici.length + 1)) * 90));
          return tick();
        });
      });
      return catena.then(function () {
        mostraProgresso(true, 'Codifica della GIF…', 92);
        return tick();
      }).then(function () {
        var bytes = window.CMI_GIF.encode(W, H, frames, delayGifCs(), 0);
        var blob = new Blob([bytes], { type: 'image/gif' });
        mostraProgresso(true, 'GIF pronta.', 100);
        return blob;
      });
    }).then(function (blob) {
      statoMappa.indice = idxOrig;
      statoMappa.matrice = costruisciMatrice(statoMappa.punti, statoMappa.variabile, idxOrig);
      if (strato) strato.ridisegna();
      esportazioneInCorso = false;
      setTimeout(function () { mostraProgresso(false, '', 0); }, 1200);
      return blob;
    }).catch(function (err) {
      statoMappa.indice = idxOrig;
      statoMappa.matrice = costruisciMatrice(statoMappa.punti, statoMappa.variabile, idxOrig);
      if (strato) strato.ridisegna();
      esportazioneInCorso = false;
      mostraProgresso(false, '', 0);
      throw err;
    });
  }
  function scaricaGifCartina() {
    mostraProgresso(true, 'Preparazione dell\'animazione…', 1);
    return esportaGifBlob().then(function (blob) {
      var mid = statoMappa.modello ? statoMappa.modello.id : 'modello';
      var vid = statoMappa.variabile ? statoMappa.variabile.id : 'variabile';
      scaricaBlob(blob, 'cartina-meteo-italia-' + mid + '-' + vid + '.gif');
      impostaStato('Animazione GIF scaricata.', false, false);
      return blob;
    }).catch(function (err) {
      impostaStato((err && err.message) || 'Non è stato possibile creare la GIF.', true, false);
    });
  }

  function nomePngCartina() {
    var iso = (statoMappa.orari[statoMappa.indice] || '').replace(/[:T]/g, '-').slice(0, 16);
    return 'cartina-meteo-italia-' + iso + '.png';
  }
  function nomeGifCartina() {
    var mid = statoMappa.modello ? statoMappa.modello.id : 'modello';
    var vid = statoMappa.variabile ? statoMappa.variabile.id : 'variabile';
    return 'cartina-meteo-italia-' + mid + '-' + vid + '.gif';
  }
  function condividiBlob(blob, nome, titolo) {
    if (!blob) return Promise.resolve();
    var file = null;
    try { file = new File([blob], nome, { type: blob.type || 'application/octet-stream' }); }
    catch (e) { file = null; }
    var dati = file ? { files: [file], title: titolo, text: titolo } : null;
    if (dati && navigator.canShare) {
      var ok = false;
      try { ok = navigator.canShare(dati); } catch (e2) { ok = false; }
      if (ok) {
        return navigator.share(dati).then(function () {
          impostaStato('Condivisione avviata.', false, false);
        }).catch(function (err) {
          if (err && err.name === 'AbortError') return;
          scaricaBlob(blob, nome);
          impostaStato('Condivisione non disponibile: file scaricato.', false, false);
        });
      }
    }
    scaricaBlob(blob, nome);
    impostaStato('Condivisione file non supportata su questo browser: file scaricato.', false, false);
    return Promise.resolve();
  }
  function condividiPngCartina() {
    return esportaPngBlob().then(function (blob) {
      return condividiBlob(blob, nomePngCartina(), 'Cartina meteo dell\'Italia');
    }).catch(function (err) {
      impostaStato((err && err.message) || 'Non è stato possibile preparare l\'immagine.', true, false);
    });
  }
  function condividiGifCartina() {
    mostraProgresso(true, 'Preparazione dell\'animazione…', 1);
    return esportaGifBlob().then(function (blob) {
      return condividiBlob(blob, nomeGifCartina(), 'Animazione della cartina meteo dell\'Italia');
    }).catch(function (err) {
      impostaStato((err && err.message) || 'Non è stato possibile creare la GIF.', true, false);
    });
  }
  function aggiornaConfrontoUI() {
    var on = confrontoAttivo();
    var campo = $('cmi-campo-confronto');
    var col = $('cmi-col-b');
    var etA = $('cmi-etichetta-a');
    var mappe = $('cmi-mappe');
    if (campo) campo.hidden = !on;
    if (col) col.hidden = !on;
    if (etA) etA.hidden = !on;
    if (mappe) {
      if (on) mappe.classList.add('cmi-mappe-doppie');
      else mappe.classList.remove('cmi-mappe-doppie');
    }
    if (on) {
      assicuraMappaB();
      aggiornaEtichetteConfronto();
      caricaGriglia('b', { mantieniOra: true });
    }
    setTimeout(function () {
      if (mappa) mappa.invalidateSize();
      if (mappaB) mappaB.invalidateSize();
    }, 80);
  }
  function pianificaRefresh() {
    if (timerRefresh) clearInterval(timerRefresh);
    timerRefresh = setInterval(function () {
      if (document.hidden) return;
      eseguiRefresh();
    }, INTERVALLO_AGGIORNAMENTO);
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden && ultimoAggiornamento && (Date.now() - ultimoAggiornamento.getTime() > INTERVALLO_AGGIORNAMENTO)) {
        eseguiRefresh();
      }
    });
  }
  function eseguiRefresh() {
    cache = {};
    impostaStato('Aggiorno i dati del modello…', false, true);
    var jobs = [caricaGriglia('a', { mantieniOra: true }), caricaCitta()];
    if (confrontoAttivo()) jobs.push(caricaGriglia('b', { mantieniOra: true }));
    Promise.all(jobs).then(function () { aggiornaCorsa(); });
  }
  function bind() {
    if ($('cmi-dominio')) {
      $('cmi-dominio').addEventListener('change', function () {
        cambiaDominio($('cmi-dominio').value);
      });
    }
    $('cmi-modello').addEventListener('change', function () {
      aggiornaInfoModello();
      aggiornaOpzioniVariabile();
      aggiornaUrl();
      caricaGriglia('a');
    });
    $('cmi-variabile').addEventListener('change', function () {
      aggiornaInfoVariabile();
      aggiornaUrl();
      caricaGriglia('a');
      if (confrontoAttivo()) caricaGriglia('b', { mantieniOra: true });
    });
    if ($('cmi-modello-b')) {
      $('cmi-modello-b').addEventListener('change', function () {
        aggiornaInfoModello();
        caricaGriglia('b', { mantieniOra: true });
      });
    }
    $('cmi-ora').addEventListener('input', function () {
      vaiAPasso(parseInt($('cmi-ora').value, 10) || 0);
    });
    $('cmi-play').addEventListener('click', function () {
      if (timerPlay) fermaPlay(true);
      else avviaPlay();
    });
    $('cmi-precedente').addEventListener('click', function () { fermaPlay(true); vaiAPasso((statoMappa.indicePasso || 0) - 1); });
    $('cmi-successiva').addEventListener('click', function () { fermaPlay(true); vaiAPasso((statoMappa.indicePasso || 0) + 1); });
    $('cmi-stampa').addEventListener('click', function () { window.print(); });
    $('cmi-condividi').addEventListener('click', condividi);
    $('cmi-copia-link').addEventListener('click', copiaLink);
    $('cmi-scarica').addEventListener('click', scaricaImmagine);
    if ($('cmi-scarica-png')) $('cmi-scarica-png').addEventListener('click', scaricaPngCartina);
    if ($('cmi-condividi-png')) $('cmi-condividi-png').addEventListener('click', condividiPngCartina);
    if ($('cmi-scarica-gif')) $('cmi-scarica-gif').addEventListener('click', scaricaGifCartina);
    if ($('cmi-condividi-gif')) $('cmi-condividi-gif').addEventListener('click', condividiGifCartina);
    if ($('cmi-velocita')) {
      $('cmi-velocita').addEventListener('change', function () {
        impostaFattoreVelocita(parseFloat($('cmi-velocita').value) || 1);
      });
    }
    if ($('cmi-velocita-meno')) $('cmi-velocita-meno').addEventListener('click', function () { cambiaFattore(-1); });
    if ($('cmi-velocita-piu')) $('cmi-velocita-piu').addEventListener('click', function () { cambiaFattore(1); });
    if ($('cmi-isolinee')) $('cmi-isolinee').addEventListener('change', function () { if (strato) strato.ridisegna(); if (stratoB) stratoB.ridisegna(); });
    if ($('cmi-particelle')) $('cmi-particelle').addEventListener('change', function () { if (strato) strato.ridisegna(); avviaOFermaVento(); });
    if ($('cmi-confronto')) $('cmi-confronto').addEventListener('change', aggiornaConfrontoUI);
    if ($('cmi-meteo-chiudi')) {
      $('cmi-meteo-chiudi').addEventListener('click', function () {
        $('cmi-meteogramma').hidden = true;
        if (mappa) mappa.closePopup();
      });
    }
    var emesso = $('cmi-emesso-il');
    if (emesso) emesso.textContent = formatEmesso(emesso.getAttribute('datetime') || emesso.textContent);
    document.addEventListener('keydown', function (ev) {
      var t = ev.target;
      var tag = (t && t.tagName) ? t.tagName.toLowerCase() : '';
      if (tag === 'input' || tag === 'select' || tag === 'textarea' || (t && t.isContentEditable)) return;
      if (ev.key === ' ' || ev.key === 'Spacebar') {
        ev.preventDefault();
        if (timerPlay) fermaPlay(true);
        else avviaPlay();
      } else if (ev.key === 'ArrowLeft') {
        ev.preventDefault();
        fermaPlay(true);
        vaiAPasso((statoMappa.indicePasso || 0) - 1);
      } else if (ev.key === 'ArrowRight') {
        ev.preventDefault();
        fermaPlay(true);
        vaiAPasso((statoMappa.indicePasso || 0) + 1);
      } else if (ev.key === '+' || ev.key === '=' || ev.key === 'Add') {
        ev.preventDefault();
        cambiaFattore(1);
      } else if (ev.key === '-' || ev.key === '_' || ev.key === 'Subtract') {
        ev.preventDefault();
        cambiaFattore(-1);
      }
    });
  }
  function caricaConfini() {
    var url = (leggiConfig().geoJsonUrl) || '/data/italia-confini.geojson';
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error('confini');
      return r.json();
    }).then(function (g) { geojson = g; }).catch(function () { geojson = null; });
  }
  function caricaLaghi() {
    var url = (leggiConfig().laghiUrl) || '/data/laghi-castelli-romani.geojson';
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error('laghi');
      return r.json();
    }).then(function (g) { laghiGeo = g; }).catch(function () { laghiGeo = null; });
  }
  function caricaRegioni() {
    var url = (leggiConfig().regioniUrl) || '/data/italia-regioni.geojson';
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error('regioni');
      return r.json();
    }).then(function (g) { regioniGeo = g; }).catch(function () { regioniGeo = null; });
  }
  function caricaHillshade() {
    var url = (leggiConfig().hillshadeCastelliUrl) || '/images/cartina-meteo-hillshade-castelli.png';
    return new Promise(function (resolve) {
      var img = new Image();
      img.onload = function () { hillshadeImg = img; resolve(); };
      img.onerror = function () { hillshadeImg = null; resolve(); };
      img.src = url;
    });
  }
  function avvia() {
    leggiVelocitaSalvata();
    aggiornaVelocitaUI();
    popolaSelect();
    applicaParametriUrl();
    bind();
    pianificaRefresh();
    var cfg = leggiConfig();
    loadScript(cfg.leafletJs || '/vendor/leaflet/leaflet.js').then(function () {
      return Promise.all([caricaConfini(), caricaLaghi(), caricaRegioni(), caricaHillshade(), caricaIconeTempo()]);
    }).then(function () {
      creaMappe();
      return Promise.all([caricaGriglia('a'), caricaCitta()]);
    }).catch(function (err) {
      impostaStato((err && err.message) || 'Impossibile avviare la cartina.', true, false);
      if (prontoRisovi) { prontoRisovi(); prontoRisovi = null; }
    });
  }
  function leggiConfig() {
    var el = document.getElementById('cmi-config');
    if (!el) return {};
    try { return JSON.parse(el.value || el.textContent || '{}'); }
    catch (e) { return {}; }
  }
  function attivaConfronto(modelId) {
    var chk = $('cmi-confronto');
    if (chk) chk.checked = true;
    if (modelId && $('cmi-modello-b')) $('cmi-modello-b').value = modelId;
    aggiornaConfrontoUI();
  }
  window.CMI_API = {
    pronto: function () { return prontoPromessa; },
    esportaGifBlob: esportaGifBlob,
    esportaPngBlob: esportaPngBlob,
    esportaBollettinoBlob: esportaBollettinoBlob,
    apriMeteogramma: apriMeteogramma,
    attivaConfronto: attivaConfronto,
    impostaVariabile: function (id) {
      var sel = $('cmi-variabile');
      if (sel) sel.value = id;
      aggiornaInfoVariabile();
      return caricaGriglia('a');
    },
    impostaVelocita: function (n) { impostaFattoreVelocita(n, false); },
    impostaDominio: function (id) {
      if ($('cmi-dominio')) $('cmi-dominio').value = id;
      return cambiaDominio(id);
    },
    avviaPlay: avviaPlay,
    fermaPlay: function () { fermaPlay(true); },
    inPlay: function () { return !!timerPlay; },
    dominio: function () { return dominioId; },
    misuraSchede: function () {
      if (!mappa || !statoMappa) return null;
      var d = dominioCorrente();
      var locali = (statoMappa.locali) || [];
      var iso = (statoMappa.orari && statoMappa.orari[statoMappa.indice]) || null;
      var mid = L.latLng((d.latMin + d.latMax) / 2, 12);
      var p0 = mappa.latLngToContainerPoint(mid);
      var p1 = mappa.latLngToContainerPoint(L.latLng(mid.lat, 13));
      var k = Math.abs(p1.x - p0.x) / (d.refLon || 73.2);
      if (!isFinite(k) || k <= 0) k = 1;
      var kGrezzo = k;
      if (k > 1.15) k = 1.15;
      if (k < 0.5) k = 0.5;
      var dettaglio = mappa.getZoom() >= (zoomVistaIniziale(mappa, d, boundsCampo()) + 1);
      var S = Math.round(62 * k);
      var out = [], i, loc, xy, off, c, dist, vis;
      for (i = 0; i < locali.length; i++) {
        loc = locali[i];
        if ((loc.livello || 1) > 1 && !dettaglio) continue;
        if (indiceOraLocale(loc, iso) < 0) continue;
        xy = mappa.latLngToContainerPoint(L.latLng(loc.lat, loc.lon));
        off = limitaNudge((dettaglio && loc.off2) ? loc.off2 : (loc.off || [0, 0]));
        c = { x: xy.x + off[0], y: xy.y + off[1] };
        dist = Math.sqrt((c.x - xy.x) * (c.x - xy.x) + (c.y - xy.y) * (c.y - xy.y));
        vis = xy.x >= -40 && xy.y >= -40 && xy.x <= mappa.getSize().x + 40 && xy.y <= mappa.getSize().y + 40;
        out.push({
          nome: loc.nome, livello: loc.livello || 1,
          lat: loc.lat, lon: loc.lon,
          allinea: (dettaglio && loc.allinea2) ? loc.allinea2 : (loc.allinea || 's'),
          off: off, punto: { x: +xy.x.toFixed(1), y: +xy.y.toFixed(1) },
          icona: { x: +c.x.toFixed(1), y: +c.y.toFixed(1) },
          distPx: +dist.toFixed(1), visibile: vis
        });
      }
      return {
        dominio: d.id, zoom: mappa.getZoom(),
        zoomFit: zoomVistaIniziale(mappa, d, boundsCampo()),
        k: +k.toFixed(3), kGrezzo: +kGrezzo.toFixed(3), S: S,
        size: { w: mappa.getSize().x, h: mappa.getSize().y },
        schede: out
      };
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
