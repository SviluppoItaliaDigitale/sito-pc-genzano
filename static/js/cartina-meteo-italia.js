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

    { id: 'italia_meteo_arpae_icon_2i', gruppo: 'alta', nome: 'ItaliaMeteo ARPAE ICON-2I', risoluzione: '2 km', aggiornamento: 'ogni 12 ore', giorni: 3, dominio: 'Italia intera e Mediterraneo centrale', ente: 'ItaliaMeteo / ARPAE' },
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
    { id: 'tempo_previsto', nome: 'Tempo previsto', unita: '', campi: ['weather_code', 'precipitation', 'snowfall', 'cape', 'showers'], scala: 'tempo', tempo: true, info: 'Tipo di tempo previsto dal codice WMO di Open-Meteo. I temporali con grandine (codici 96 e 99) arrivano solo da alcuni modelli. Un triangolo su un temporale indica CAPE elevato: è un indizio convettivo, non un\'allerta ufficiale.' },
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
    for (var lat = LAT_MIN; lat <= LAT_MAX + 1e-9; lat += PASSO) {
      for (var lon = LON_MIN; lon <= LON_MAX + 1e-9; lon += PASSO) {
        punti.push({ lat: arrotonda(lat, 2), lon: arrotonda(lon, 2) });
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
    sel.textContent = '';
    var gruppi = ['globali', 'europa', 'alta'];
    for (var g = 0; g < gruppi.length; g++) {
      var og = document.createElement('optgroup');
      og.label = GRUPPI[gruppi[g]];
      for (var i = 0; i < MODELLI.length; i++) {
        if (MODELLI[i].gruppo !== gruppi[g]) continue;
        var o = document.createElement('option');
        o.value = MODELLI[i].id;
        o.textContent = MODELLI[i].nome + ' — ' + MODELLI[i].risoluzione;
        og.appendChild(o);
      }
      sel.appendChild(og);
    }
    sel.value = valore;
  }
  function popolaSelect() {
    var selM = $('cmi-modello');
    var selV = $('cmi-variabile');
    var selB = $('cmi-modello-b');
    if (!selM || !selV) return;
    popolaSelectModello(selM, 'ecmwf_ifs');
    if (selB) popolaSelectModello(selB, 'ncep_gfs_global');
    for (var v = 0; v < VARIABILI.length; v++) {
      var ov = document.createElement('option');
      ov.value = VARIABILI[v].id;
      ov.textContent = VARIABILI[v].nome;
      selV.appendChild(ov);
    }
    selV.value = 'tempo_previsto';
    aggiornaInfoModello();
    aggiornaInfoVariabile();
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
  }
  function aggiornaInfoVariabile() {
    var v = variabileById($('cmi-variabile').value);
    var el = $('cmi-variabile-info');
    if (el) el.textContent = v.info || '';
  }
  function aggiornaOpzioniVariabile() {
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
    var bounds = boundsItalia();
    var map = L.map(id, {
      scrollWheelZoom: false,
      maxBounds: bounds.pad(0.35),
      minZoom: 5,
      zoomSnap: 0.25,
      zoomDelta: 0.25,
      zoomControl: true,
      attributionControl: true
    });
    map.attributionControl.setPrefix('');
    map.attributionControl.addAttribution('Confini: <a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a> · Dati: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> CC BY 4.0');
    map.fitBounds(L.latLngBounds([[LAT_MIN, LON_MIN], [LAT_MAX, LON_MAX]]), { padding: [4, 4], maxZoom: 7 });
    if (conClick) map.on('click', onClickMappa);
    var st = creaStratoCanvas(map);
    map.on('move zoom resize', function () { if (st) st.ridisegna(); });
    return { map: map, strato: st };
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
      var campo = L.latLngBounds([[LAT_MIN, LON_MIN], [LAT_MAX, LON_MAX]]);
      if (mappa) { mappa.invalidateSize(); mappa.fitBounds(campo, { padding: [4, 4], maxZoom: 7 }); }
      if (mappaB) { mappaB.invalidateSize(); mappaB.fitBounds(campo, { padding: [4, 4], maxZoom: 7 }); }
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
      disegnaVista(ctx, {
        w: lay.size.x,
        h: lay.size.y,
        xy: function (lat, lon) { return proietta(lat, lon, lay.topLeft); },
        inv: function (x, y) { return inversa(x, y, lay.topLeft); }
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
    for (i = 0; i < ny * nx; i++) { val[i] = null; u[i] = null; v[i] = null; cat[i] = null; cape[i] = null; }
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
      }
    }
    return { lats: lats, lons: lons, nx: nx, ny: ny, val: val, u: u, v: v, cat: cat, cape: cape, tempo: !!(variabile && variabile.tempo) };
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
    var arr = campo === 'u' ? mat.u : (campo === 'v' ? mat.v : mat.val);
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
    var m = 0.4;
    var fx = 1, fy = 1;
    if (lon < LON_MIN + m) fx = (lon - LON_MIN) / m;
    if (lon > LON_MAX - m) fx = (LON_MAX - lon) / m;
    if (lat < LAT_MIN + m) fy = (lat - LAT_MIN) / m;
    if (lat > LAT_MAX - m) fy = (LAT_MAX - lat) / m;
    if (fx < 0 || fy < 0) return 0;
    var f = Math.min(fx, fy, 1);
    return f * f * (3 - 2 * f);
  }
  function disegnaCampo(ctx, vista, mat, scalaId, alphaBase) {
    if (!mat) return;
    var step = 2;
    var imgW = Math.max(1, Math.ceil(vista.w / step));
    var imgH = Math.max(1, Math.ceil(vista.h / step));
    var tmp = document.createElement('canvas');
    tmp.width = imgW;
    tmp.height = imgH;
    var tctx = tmp.getContext('2d');
    var img = tctx.createImageData(imgW, imgH);
    var data = img.data;
    var px, py, i, ll, val, col, a;
    for (py = 0; py < imgH; py++) {
      for (px = 0; px < imgW; px++) {
        ll = vista.inv(px * step + step / 2, py * step + step / 2);
        if (mat.tempo) {
          var ccat = campionaVicino(mat, ll.lat, ll.lon, 'cat');
          col = ccat ? (COLORI_TEMPO[ccat] || null) : null;
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
    ctx.imageSmoothingQuality = 'high';
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
  function disegnaConfini(ctx, vista) {
    if (!geojson || !geojson.features) return;
    var f, i;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
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
  function disegnaIconeTempo(ctx, vista, mat) {
    if (!mat || !mat.tempo) return;
    var p0 = vista.xy(mat.lats[0], mat.lons[0]);
    var p1 = vista.xy(mat.lats[0], mat.lons[Math.min(1, mat.nx - 1)]);
    var dx = Math.abs(p1[0] - p0[0]) || 40;
    var ogni = Math.max(1, Math.round(48 / dx));
    var size = Math.max(22, Math.min(36, dx * ogni * 0.72));
    var iy, ix, j, cat, xy, img, cape;
    for (iy = 0; iy < mat.ny; iy += ogni) {
      for (ix = 0; ix < mat.nx; ix += ogni) {
        j = iy * mat.nx + ix;
        cat = mat.cat[j];
        if (!cat) continue;
        xy = vista.xy(mat.lats[iy], mat.lons[ix]);
        var limY = vista.h - 8;
        if (mat.tempo) {
          var ml = misureLegendaTempo(vista);
          limY = ml.y - 4;
        }
        if (xy[0] < 8 || xy[1] < 8 || xy[0] > vista.w - 8 || xy[1] > limY) continue;
        ctx.beginPath();
        ctx.arc(xy[0], xy[1], size / 2 + 2, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,255,255,0.86)';
        ctx.fill();
        img = iconeTempo[cat];
        if (img) ctx.drawImage(img, xy[0] - size / 2, xy[1] - size / 2, size, size);
        cape = mat.cape[j];
        if (cat === 'temporale' && cape !== null && cape >= 1000) {
          ctx.beginPath();
          ctx.moveTo(xy[0] + size / 2 - 2, xy[1] - size / 2 - 1);
          ctx.lineTo(xy[0] + size / 2 + 7, xy[1] - size / 2 - 1);
          ctx.lineTo(xy[0] + size / 2 + 2.5, xy[1] - size / 2 - 10);
          ctx.closePath();
          ctx.fillStyle = '#b45309';
          ctx.fill();
        }
      }
    }
  }
  function disegnaVista(ctx, vista, stato, opts) {

    opts = opts || {};
    ctx.fillStyle = '#c5d8e8';
    ctx.fillRect(0, 0, vista.w, vista.h);
    if (!stato || !stato.variabile || !stato.matrice) {
      disegnaConfini(ctx, vista);
      return;
    }
    disegnaCampo(ctx, vista, stato.matrice, stato.variabile.scala, stato.variabile.tempo ? 0.62 : 0.84);
    disegnaConfini(ctx, vista);
    if (isolineeAttive() && !stato.variabile.tempo) disegnaIsolinee(ctx, vista, stato.matrice, stato.variabile.scala);
    if (stato.variabile.vento && (opts.frecce || !particelleAttive() || motoRidotto())) {
      disegnaFrecce(ctx, vista, stato.matrice);
    }
    if (stato.variabile.tempo) disegnaIconeTempo(ctx, vista, stato.matrice);
    if (opts.decorazioni) disegnaDecorazioni(ctx, vista, stato);
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
    return modelId + '|' + varId + '|' + giorni;
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
      var candidati = ['weather_code', 'precipitation', 'snowfall', 'cape', 'showers'];
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
          showers: h.showers || null
        });
      }
      if (!orari || !orari.length || tuttiNull || !punti.length) {
        if (!isB) marcaNonDisponibile(mid, vid);
        throw new Error('Questa grandezza non è disponibile per il modello scelto, oppure il modello non copre l\'Italia in questo punto.');
      }
      var pacchetto = { punti: punti, orari: orari, scaricatoIl: new Date(), fuoriDominio: punti.length < puntiBase.length * 0.7 };
      cache[key] = pacchetto;
      applicaDati(pacchetto, variabile, modello, target, opzioni.mantieniOra);
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
    var indici = [];
    for (var i = 0; i < pacchetto.orari.length; i++) {
      if (i % 3 === 0 || i === pacchetto.orari.length - 1) indici.push(i);
    }
    stato.passi = indici;
    var meglio = 0, dist = Infinity, p, t, d;
    var ancora = mantieniOra && statoMappa.orari[statoMappa.indice];
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
      var extra = pacchetto.fuoriDominio ? ' Il modello non copre tutta l\'Italia: le zone fuori dal dominio restano senza colore.' : '';
      impostaStato('Cartina pronta: ' + modello.nome + ', ' + variabile.nome + '.' + extra, false, false);
      aggiornaCorsa();
      assicuraMarcatoreGenzano();
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
      nota.textContent = "I temporali con grandine (codici WMO 96 e 99) arrivano solo da alcuni modelli. Un triangolo su un temporale indica CAPE elevato: è un indizio convettivo, non un'allerta ufficiale.";
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
      '<strong>Aggiornato alle:</strong> ' + quando + ' (ora locale Europe/Rome). Fonte: Open-Meteo, licenza CC BY 4.0. Confini: Natural Earth, pubblico dominio.';
  }
  function aggiornaEtichetteConfronto() {
    var a = $('cmi-etichetta-a');
    var b = $('cmi-etichetta-b');
    if (a) a.textContent = statoMappa.modello ? ('Modello A: ' + statoMappa.modello.nome) : 'Modello A';
    if (b) b.textContent = statoMappaB.modello ? ('Modello B: ' + statoMappaB.modello.nome) : 'Modello B';
  }
  function assicuraMarcatoreGenzano() {
    if (!window.L) return;
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
    ctx.fillText('Dati modellistici: Open-Meteo, licenza CC BY 4.0.', 48, 1332);
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
  function vistaFissa(w, h, pad) {
    pad = pad || 8;
    var W = LON_MAX - LON_MIN, Hgt = LAT_MAX - LAT_MIN;
    return {
      w: w,
      h: h,
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
    var testata = 92, piede = 78;
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, 0, w, testata);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 22px Titillium Web, Arial, sans-serif';
    ctx.fillText('Cartina meteo dell\'Italia', 16, 28);
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
    var vista = vistaFissa(mw, mh, 6);
    disegnaVista(octx, vista, stato, { frecce: true, decorazioni: true });
    ctx.drawImage(off, 0, testata);
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, h - piede, w, piede);
    ctx.fillStyle = '#ffffff';
    ctx.font = '14px Titillium Web, Arial, sans-serif';
    ctx.fillText('Dati: Open-Meteo, licenza CC BY 4.0. Confini: Natural Earth, pubblico dominio.', 16, h - 48);
    ctx.fillText('protezionecivilegenzano.it/cartina-meteo-italia/', 16, h - 28);
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
    $('cmi-modello').addEventListener('change', function () {
      aggiornaInfoModello();
      aggiornaOpzioniVariabile();
      caricaGriglia('a');
    });
    $('cmi-variabile').addEventListener('change', function () {
      aggiornaInfoVariabile();
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
  function avvia() {
    leggiVelocitaSalvata();
    aggiornaVelocitaUI();
    popolaSelect();
    bind();
    pianificaRefresh();
    var cfg = leggiConfig();
    loadScript(cfg.leafletJs || '/vendor/leaflet/leaflet.js').then(function () {
      return Promise.all([caricaConfini(), caricaIconeTempo()]);
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
    avviaPlay: avviaPlay,
    fermaPlay: function () { fermaPlay(true); },
    inPlay: function () { return !!timerPlay; }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
