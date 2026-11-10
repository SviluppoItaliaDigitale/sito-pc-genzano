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

  var cache = {};
  var nonDisponibili = {};
  var statoMappa = { punti: [], orari: [], indice: 0, variabile: null, modello: null, scaricatoIl: null };
  var mappa, mappaCitta, strato, timerPlay = null, datiCitta = null, markerGenzano = null;

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
  function cssRgb(c) { return c ? 'rgb(' + c[0] + ',' + c[1] + ',' + c[2] + ')' : 'transparent'; }
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

  function popolaSelect() {
    var selM = $('cmi-modello');
    var selV = $('cmi-variabile');
    if (!selM || !selV) return;
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
      selM.appendChild(og);
    }
    selM.value = 'ecmwf_ifs';
    for (var v = 0; v < VARIABILI.length; v++) {
      var ov = document.createElement('option');
      ov.value = VARIABILI[v].id;
      ov.textContent = VARIABILI[v].nome;
      selV.appendChild(ov);
    }
    selV.value = 'temperature_2m';
    aggiornaInfoModello();
    aggiornaInfoVariabile();
  }

  function aggiornaInfoModello() {
    var m = modelloById($('cmi-modello').value);
    var parti = [
      m.ente,
      'risoluzione ' + m.risoluzione,
      'orizzonte ' + m.giorni + (m.giorni === 1 ? ' giorno' : ' giorni'),
      'aggiornamento ' + m.aggiornamento,
      m.dominio
    ];
    var txt = parti.join(' · ');
    if (m.nota) txt += ' ' + m.nota;
    $('cmi-modello-info').textContent = txt;
  }
  function aggiornaInfoVariabile() {
    var v = variabileById($('cmi-variabile').value);
    $('cmi-variabile-info').textContent = v.info || '';
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

  function creaMappe() {
    var osm = function () {
      return L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
      });
    };
    var bounds = L.latLngBounds([[36.2, 6.6], [47.2, 18.7]]);
    mappa = L.map('cmi-mappa', { scrollWheelZoom: false, maxBounds: bounds.pad(0.5), minZoom: 6 });
    osm().addTo(mappa);
    mappa.fitBounds(bounds, { padding: [8, 8], maxZoom: 7 });
    mappa.on('click', onClickMappa);
    strato = creaStratoCanvas(mappa);
    mappa.on('move zoom resize', function () { if (strato) strato.ridisegna(); });

    mappaCitta = L.map('cmi-mappa-citta', { scrollWheelZoom: false, minZoom: 6, maxBounds: bounds.pad(0.5) });
    osm().addTo(mappaCitta);
    mappaCitta.fitBounds(bounds, { padding: [16, 16], maxZoom: 7 });
    function adatta() {
      if (mappa) { mappa.invalidateSize(); mappa.fitBounds(bounds, { padding: [8, 8], maxZoom: 7 }); }
      if (mappaCitta) { mappaCitta.invalidateSize(); mappaCitta.fitBounds(bounds, { padding: [16, 16], maxZoom: 7 }); }
    }
    setTimeout(adatta, 300);
    setTimeout(adatta, 1200);
  }

  function creaStratoCanvas(map) {
    var canvas = L.DomUtil.create('canvas', 'cmi-grid-canvas');
    map.getPanes().overlayPane.appendChild(canvas);
    canvas.style.position = 'absolute';
    canvas.style.pointerEvents = 'none';
    function ridisegna() {
      if (!map) return;
      var size = map.getSize();
      var b = map.getBounds();
      var topLeft = map.latLngToLayerPoint(b.getNorthWest());
      L.DomUtil.setPosition(canvas, topLeft);
      canvas.width = size.x;
      canvas.height = size.y;
      var ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, size.x, size.y);
      var v = statoMappa.variabile;
      if (!v || !statoMappa.punti.length || !statoMappa.orari.length) return;
      var idx = statoMappa.indice;
      var half = PASSO / 2;
      for (var i = 0; i < statoMappa.punti.length; i++) {
        var p = statoMappa.punti[i];
        var val = valorePunto(p, v, idx);
        var col = coloreDi(val, v.scala);
        if (!col) continue;
        var sw = map.latLngToLayerPoint(L.latLng(p.lat - half, p.lon - half));
        var ne = map.latLngToLayerPoint(L.latLng(p.lat + half, p.lon + half));
        var x = sw.x - topLeft.x;
        var y = ne.y - topLeft.y;
        var w = ne.x - sw.x;
        var h = sw.y - ne.y;
        ctx.fillStyle = 'rgba(' + col[0] + ',' + col[1] + ',' + col[2] + ',0.62)';
        ctx.fillRect(x, y, w, h);
        if (v.vento && p.dir && p.dir[idx] !== null && typeof p.dir[idx] !== 'undefined' && val !== null) {
          disegnaFreccia(ctx, (sw.x + ne.x) / 2 - topLeft.x, (sw.y + ne.y) / 2 - topLeft.y, p.dir[idx], Math.min(w, h) * 0.35);
        }
      }
    }
    return { ridisegna: ridisegna, canvas: canvas };
  }

  function disegnaFreccia(ctx, x, y, dir, len) {
    if (!len || len < 4) return;
    var rad = (dir - 90) * Math.PI / 180;
    var x2 = x + Math.cos(rad) * len;
    var y2 = y + Math.sin(rad) * len;
    ctx.save();
    ctx.strokeStyle = 'rgba(20,20,20,0.85)';
    ctx.fillStyle = 'rgba(20,20,20,0.85)';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    var a = rad + 2.6, b = rad - 2.6;
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 + Math.cos(a) * 5, y2 + Math.sin(a) * 5);
    ctx.lineTo(x2 + Math.cos(b) * 5, y2 + Math.sin(b) * 5);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
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

  function onClickMappa(ev) {
    if (!statoMappa.punti.length) return;
    var vicino = null, dist = Infinity;
    for (var i = 0; i < statoMappa.punti.length; i++) {
      var p = statoMappa.punti[i];
      var d = Math.abs(p.lat - ev.latlng.lat) + Math.abs(p.lon - ev.latlng.lng);
      if (d < dist) { dist = d; vicino = p; }
    }
    if (!vicino || dist > PASSO * 1.5) return;
    var v = statoMappa.variabile;
    var val = valorePunto(vicino, v, statoMappa.indice);
    var testo = v.nome + ': ' + (val === null ? 'dato non disponibile' : (Math.round(val * 10) / 10) + ' ' + v.unita);
    L.popup().setLatLng(ev.latlng).setContent(testo).openOn(mappa);
  }

  function spezza(arr, n) {
    var out = [];
    for (var i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
    return out;
  }

  function fetchJson(url) {
    return fetch(url).then(function (res) {
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

  function caricaGriglia() {
    var mid = $('cmi-modello').value;
    var vid = $('cmi-variabile').value;
    var modello = modelloById(mid);
    var variabile = variabileById(vid);
    var giorni = Math.min(modello.giorni, 7);
    var key = chiaveCache(mid, vid, giorni);
    fermaPlay(false);
    aggiornaInfoModello();
    aggiornaInfoVariabile();
    if (cache[key]) {
      applicaDati(cache[key], variabile, modello);
      return Promise.resolve();
    }
    impostaStato('Scarico i dati del modello ' + modello.nome + '…', false, true);
    $('cmi-ora').disabled = true;
    var puntiBase = costruisciGriglia();
    var campi = variabile.campi.join(',');
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
        for (var i = 0; i < lista.length; i++) {
          out.push({ punto: gruppo[i] || null, dati: lista[i] });
        }
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
      var campoVal = variabile.vento ? variabile.vento.vel : variabile.campi[0];
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
          dir: dirs
        });
      }
      if (!orari || !orari.length || tuttiNull || !punti.length) {
        marcaNonDisponibile(mid, vid);
        throw new Error('Questa grandezza non è disponibile per il modello scelto, oppure il modello non copre l\'Italia in questo punto.');
      }
      var pacchetto = { punti: punti, orari: orari, scaricatoIl: new Date(), fuoriDominio: punti.length < puntiBase.length * 0.7 };
      cache[key] = pacchetto;
      applicaDati(pacchetto, variabile, modello);
    }).catch(function (err) {
      var msg = (err && err.message) ? err.message : 'Non è stato possibile scaricare i dati.';
      if (err && err.reason && /hourly|invalid string|weather variable/i.test(err.reason)) {
        marcaNonDisponibile(mid, vid);
        msg = 'Questa grandezza non è disponibile per il modello ' + modello.nome + '. Scegline un\'altra.';
      }
      impostaStato(msg, true, false);
    });
  }

  function applicaDati(pacchetto, variabile, modello) {
    statoMappa.punti = pacchetto.punti;
    statoMappa.orari = pacchetto.orari;
    statoMappa.variabile = variabile;
    statoMappa.modello = modello;
    statoMappa.scaricatoIl = pacchetto.scaricatoIl;
    var indici = [];
    for (var i = 0; i < pacchetto.orari.length; i++) {
      if (i % 3 === 0 || i === pacchetto.orari.length - 1) indici.push(i);
    }
    statoMappa.passi = indici;
    var ora = new Date();
    var meglio = 0, dist = Infinity;
    for (var p = 0; p < indici.length; p++) {
      var t = Date.parse(pacchetto.orari[indici[p]]);
      var d = Math.abs(t - ora.getTime());
      if (d < dist) { dist = d; meglio = p; }
    }
    statoMappa.indicePasso = meglio;
    statoMappa.indice = indici[meglio];
    var sl = $('cmi-ora');
    sl.disabled = false;
    sl.min = 0;
    sl.max = String(indici.length - 1);
    sl.value = String(meglio);
    aggiornaOraUI();
    aggiornaLegenda();
    if (strato) strato.ridisegna();
    var extra = pacchetto.fuoriDominio ? ' Il modello non copre tutta l\'Italia: le zone fuori dal dominio restano senza colore.' : '';
    impostaStato('Cartina pronta: ' + modello.nome + ', ' + variabile.nome + '.' + extra, false, false);
    aggiornaCorsa();
    assicuraMarcatoreGenzano();
  }

  function aggiornaOraUI() {
    var iso = statoMappa.orari[statoMappa.indice];
    $('cmi-ora-etichetta').textContent = formatOra(iso);
  }
  function aggiornaLegenda() {
    var v = statoMappa.variabile;
    if (!v) return;
    var ext = etichettaScala(v.scala);
    $('cmi-legenda-titolo').textContent = 'Legenda: ' + v.nome + ' (' + v.unita + ')';
    var scala = $('cmi-legenda-scala');
    scala.innerHTML = '';
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
    var quando = statoMappa.scaricatoIl ? formatOra(statoMappa.scaricatoIl.toISOString().replace('Z', '')) : '';
    // Use local format
    if (statoMappa.scaricatoIl) {
      var d = statoMappa.scaricatoIl;
      var pad = function (n) { return (n < 10 ? '0' : '') + n; };
      quando = pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear() + ', ore ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
    }
    el.textContent = 'Modello ' + statoMappa.modello.nome + ' (' + statoMappa.modello.risoluzione + ', ' + statoMappa.modello.ente + '). Dati scaricati il ' + quando + ' (ora locale). Fonte: Open-Meteo, licenza CC BY 4.0.';
  }
  function assicuraMarcatoreGenzano() {
    if (!mappa || !window.L) return;
    if (markerGenzano) { mappa.removeLayer(markerGenzano); }
    markerGenzano = L.circleMarker([GENZANO.lat, GENZANO.lon], {
      radius: 6, color: '#ffbe2e', weight: 2, fillColor: '#003366', fillOpacity: 1
    }).addTo(mappa);
    markerGenzano.bindTooltip('Genzano di Roma');
  }

  function vaiAPasso(n) {
    if (!statoMappa.passi || !statoMappa.passi.length) return;
    var max = statoMappa.passi.length - 1;
    if (n < 0) n = max;
    if (n > max) n = 0;
    statoMappa.indicePasso = n;
    statoMappa.indice = statoMappa.passi[n];
    $('cmi-ora').value = String(n);
    aggiornaOraUI();
    if (strato) strato.ridisegna();
  }
  function fermaPlay(aggiornaBottone) {
    if (timerPlay) { clearInterval(timerPlay); timerPlay = null; }
    if (aggiornaBottone !== false) {
      var btn = $('cmi-play');
      btn.setAttribute('aria-pressed', 'false');
      $('cmi-play-etichetta').textContent = 'Avvia animazione';
      var icon = btn.querySelector('i');
      if (icon) icon.className = 'bi bi-play-fill';
    }
  }
  function avviaPlay() {
    var ridotto = document.documentElement.classList.contains('a11y-pause-animations') ||
      document.documentElement.classList.contains('a11y-pause-anim') ||
      (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var attesa = ridotto ? 1400 : 500;
    fermaPlay(false);
    var btn = $('cmi-play');
    btn.setAttribute('aria-pressed', 'true');
    $('cmi-play-etichetta').textContent = 'Metti in pausa';
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
      scheda.innerHTML = '';
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

  function urlPagina() {
    return window.location.href.split('#')[0];
  }

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
          ctx.fillText(line.replace(/.{0}$/, '…'), x, y);
          return y + lineHeight;
        }
      } else {
        line = test;
      }
    }
    if (line) { ctx.fillText(line, x, y); y += lineHeight; }
    return y;
  }

  function scaricaImmagine() {
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
      var colW = 486, rowH = 58, startY = y + 16, col = 0;
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

    ctx.fillStyle = '#3a2e0e';
    ctx.font = '22px Titillium Web, Arial, sans-serif';
    y = wrapText(ctx, 'Non è un\'allerta ufficiale. Per i colori di allerta consulta la pagina Allerte meteo del sito. In emergenza chiama il 112.', 48, Math.min(y, 1180), 984, 32, 3);
    ctx.fillStyle = '#003366';
    ctx.fillRect(0, 1260, 1080, 90);
    ctx.fillStyle = '#ffffff';
    ctx.font = '22px Titillium Web, Arial, sans-serif';
    ctx.fillText('protezionecivilegenzano.it/cartina-meteo-italia/', 48, 1300);
    ctx.font = '20px Titillium Web, Arial, sans-serif';
    ctx.fillText('Dati modellistici: Open-Meteo, licenza CC BY 4.0.', 48, 1332);

    function scarica() {
      canvas.toBlob(function (blob) {
        if (!blob) return;
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'previsioni-meteo-italia-' + (b.validita_da || 'bollettino') + '.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        messaggioCondividi('Immagine scaricata.');
      }, 'image/png');
    }

    var logo = new Image();
    logo.onload = function () {
      try { ctx.drawImage(logo, 920, 40, 110, 110); } catch (e) {}
      scarica();
    };
    logo.onerror = function () { scarica(); };
    var cfg = leggiConfig();
    logo.src = cfg.logoUrl || '/images/logo-pc-genzano.png';
  }

  function formatDataIt(iso) {
    if (!iso) return '';
    var p = String(iso).split('-');
    if (p.length !== 3) return iso;
    return parseInt(p[2], 10) + '/' + p[1] + '/' + p[0];
  }

  function bind() {
    $('cmi-modello').addEventListener('change', function () {
      aggiornaInfoModello();
      aggiornaOpzioniVariabile();
      caricaGriglia();
    });
    $('cmi-variabile').addEventListener('change', function () {
      aggiornaInfoVariabile();
      caricaGriglia();
    });
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
    var emesso = $('cmi-emesso-il');
    if (emesso) emesso.textContent = formatEmesso(emesso.getAttribute('datetime') || emesso.textContent);
  }

  function avvia() {
    popolaSelect();
    bind();
    var cfg = leggiConfig();
    loadScript(cfg.leafletJs || '/vendor/leaflet/leaflet.js').then(function () {
      creaMappe();
      return Promise.all([caricaGriglia(), caricaCitta()]);
    }).catch(function (err) {
      impostaStato((err && err.message) || 'Impossibile avviare la cartina.', true, false);
    });
  }

  function leggiConfig() {
    var el = document.getElementById('cmi-config');
    if (!el) return {};
    try { return JSON.parse(el.value || el.textContent || '{}'); }
    catch (e) { return {}; }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
