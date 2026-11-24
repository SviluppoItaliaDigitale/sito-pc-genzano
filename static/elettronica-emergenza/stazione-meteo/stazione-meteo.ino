/*
  Stazione meteo con ESP32, BME280 e anemometro a coppe.
  Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
  https://www.protezionecivilegenzano.it/elettronica-emergenza/stazione-meteo/
  Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).

  Dispositivo NON certificato: le misure servono a osservare il tempo sul
  posto. Non sostituiscono le stazioni della rete regionale, i bollettini del
  Centro Funzionale ne' il 112.

  Funzionamento:
  - BME280 su I2C: temperatura, umidita' e pressione. Una misura al minuto
    in "forced mode", come consiglia la scheda tecnica Bosch per il
    monitoraggio meteo (capitolo 3.5.1). Le formule di compensazione sono
    quelle del capitolo 4.2.3 della scheda tecnica (numeri interi, pressione
    a 64 bit), riscritte qui.
  - Anemometro a coppe: ogni giro chiude un contatto reed. La scheda conta
    gli impulsi (con antirimbalzo) a blocchi di 3 secondi, calcola la media
    dell'ultimo minuto e il valore piu' alto su 3 secondi nell'ultima ora.
    Con KMH_PER_HZ in config.h trasforma gli impulsi al secondo in km/h.
  I dati escono sulla seriale ogni minuto e, se USA_WIFI e' true, su una
  pagina web nella rete locale (/ e /dati.json).

  Scheda: "ESP32 Dev Module" (core Arduino-ESP32 di Espressif, versione 3 o 4).
*/

#include <Arduino.h>
#include <Wire.h>
#include "esp_timer.h"
#include "config.h"

#if USA_WIFI
  #if __has_include("segreti.h")
    #include "segreti.h"
  #else
    #error "Manca segreti.h: copia segreti.h.esempio in segreti.h e scrivi i dati del Wi-Fi (oppure metti USA_WIFI false in config.h)."
  #endif
  #include <WiFi.h>
  #include <WebServer.h>
  WebServer server(80);
#endif

// ===================== INIZIO CALCOLI BME280 =====================
// Parametri di taratura scritti in fabbrica nel sensore (registri
// 0x88...0xA1 e 0xE1...0xE7, tabella 16 della scheda tecnica).
struct TaraturaBme280 {
  uint16_t T1; int16_t T2, T3;
  uint16_t P1; int16_t P2, P3, P4, P5, P6, P7, P8, P9;
  uint8_t H1; int16_t H2; uint8_t H3; int16_t H4, H5; int8_t H6;
};

// Ricava i parametri dai 26 byte letti da 0x88 e dai 7 byte letti da 0xE1.
static void decodificaTaratura(const uint8_t a[26], const uint8_t b[7], TaraturaBme280 &c) {
  c.T1 = (uint16_t)(a[1] << 8 | a[0]);
  c.T2 = (int16_t)(a[3] << 8 | a[2]);
  c.T3 = (int16_t)(a[5] << 8 | a[4]);
  c.P1 = (uint16_t)(a[7] << 8 | a[6]);
  c.P2 = (int16_t)(a[9] << 8 | a[8]);
  c.P3 = (int16_t)(a[11] << 8 | a[10]);
  c.P4 = (int16_t)(a[13] << 8 | a[12]);
  c.P5 = (int16_t)(a[15] << 8 | a[14]);
  c.P6 = (int16_t)(a[17] << 8 | a[16]);
  c.P7 = (int16_t)(a[19] << 8 | a[18]);
  c.P8 = (int16_t)(a[21] << 8 | a[20]);
  c.P9 = (int16_t)(a[23] << 8 | a[22]);
  c.H1 = a[25];                                   // registro 0xA1
  c.H2 = (int16_t)(b[1] << 8 | b[0]);             // 0xE1, 0xE2
  c.H3 = b[2];                                    // 0xE3
  c.H4 = (int16_t)(((int16_t)(int8_t)b[3] << 4) | (b[4] & 0x0F));  // 0xE4, 0xE5[3:0]
  c.H5 = (int16_t)(((int16_t)(int8_t)b[5] << 4) | (b[4] >> 4));    // 0xE6, 0xE5[7:4]
  c.H6 = (int8_t)b[6];                            // 0xE7
}

// Temperatura in centesimi di grado; calcola anche tFine per le altre due.
static int32_t compensaTemperatura(int32_t adcT, const TaraturaBme280 &c, int32_t &tFine) {
  int32_t v1 = ((((adcT >> 3) - ((int32_t)c.T1 << 1))) * ((int32_t)c.T2)) >> 11;
  int32_t d = (adcT >> 4) - ((int32_t)c.T1);
  int32_t v2 = (((d * d) >> 12) * ((int32_t)c.T3)) >> 14;
  tFine = v1 + v2;
  return (tFine * 5 + 128) >> 8;
}

// Pressione in Pa moltiplicati per 256 (formato Q24.8).
static uint32_t compensaPressione(int32_t adcP, const TaraturaBme280 &c, int32_t tFine) {
  int64_t v1 = ((int64_t)tFine) - 128000;
  int64_t v2 = v1 * v1 * (int64_t)c.P6;
  v2 = v2 + ((v1 * (int64_t)c.P5) * 131072);           // << 17
  v2 = v2 + (((int64_t)c.P4) * 34359738368LL);         // << 35
  v1 = ((v1 * v1 * (int64_t)c.P3) >> 8) + ((v1 * (int64_t)c.P2) * 4096);  // << 12
  v1 = ((((int64_t)1) << 47) + v1) * ((int64_t)c.P1) >> 33;
  if (v1 == 0) return 0;  // evita la divisione per zero
  int64_t p = 1048576 - adcP;
  p = (((p * 2147483648LL) - v2) * 3125) / v1;         // << 31
  v1 = (((int64_t)c.P9) * (p >> 13) * (p >> 13)) >> 25;
  v2 = (((int64_t)c.P8) * p) >> 19;
  p = ((p + v1 + v2) >> 8) + (((int64_t)c.P7) * 16);   // << 4
  return (uint32_t)p;
}

// Umidita' relativa in % moltiplicata per 1024 (formato Q22.10).
static uint32_t compensaUmidita(int32_t adcH, const TaraturaBme280 &c, int32_t tFine) {
  int32_t x = tFine - ((int32_t)76800);
  x = (((((adcH << 14) - (((int32_t)c.H4) << 20) - (((int32_t)c.H5) * x)) + ((int32_t)16384)) >> 15) *
       (((((((x * ((int32_t)c.H6)) >> 10) * (((x * ((int32_t)c.H3)) >> 11) + ((int32_t)32768))) >> 10) +
          ((int32_t)2097152)) * ((int32_t)c.H2) + 8192) >> 14));
  x = (x - (((((x >> 15) * (x >> 15)) >> 7) * ((int32_t)c.H1)) >> 4));
  if (x < 0) x = 0;
  if (x > 419430400) x = 419430400;
  return (uint32_t)(x >> 12);
}
// ====================== FINE CALCOLI BME280 ======================

// --- BME280: registri (capitolo 5 della scheda tecnica) ---
static const uint8_t REG_ID = 0xD0, REG_CTRL_HUM = 0xF2, REG_STATUS = 0xF3,
                     REG_CTRL_MEAS = 0xF4, REG_CONFIG = 0xF5, REG_DATI = 0xF7;
static uint8_t indirizzoBme = 0;
static TaraturaBme280 taratura;
static bool bmeValido = false;        // ultima misura riuscita
static float temperaturaC = NAN, umiditaPct = NAN, pressioneHpa = NAN;
static uint32_t misureFallite = 0;

static bool scriviRegistro(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(indirizzoBme);
  Wire.write(reg);
  Wire.write(val);
  return Wire.endTransmission() == 0;
}

static bool leggiRegistri(uint8_t reg, uint8_t *buf, size_t n) {
  Wire.beginTransmission(indirizzoBme);
  Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom((int)indirizzoBme, (int)n) != (int)n) return false;
  for (size_t i = 0; i < n; i++) buf[i] = Wire.read();
  return true;
}

static bool provaIndirizzo(uint8_t ind) {
  indirizzoBme = ind;
  uint8_t id = 0;
  return leggiRegistri(REG_ID, &id, 1) && id == 0x60;  // chip_id del BME280
}

static bool avviaBme280() {
  bool trovato = false;
  if (INDIRIZZO_BME280 != 0) trovato = provaIndirizzo(INDIRIZZO_BME280);
  else trovato = provaIndirizzo(0x76) || provaIndirizzo(0x77);
  if (!trovato) { indirizzoBme = 0; return false; }
  uint8_t a[26], b[7];
  if (!leggiRegistri(0x88, a, 26) || !leggiRegistri(0xE1, b, 7)) return false;
  decodificaTaratura(a, b, taratura);
  // Filtro spento (config = 0), come nelle impostazioni per il meteo.
  return scriviRegistro(REG_CONFIG, 0x00);
}

// Una misura in forced mode con sovracampionamento x1 su tutti e tre i valori.
static bool misuraBme280() {
  if (indirizzoBme == 0 && !avviaBme280()) return false;
  // ctrl_hum va scritto prima di ctrl_meas (capitolo 5.4.3).
  if (!scriviRegistro(REG_CTRL_HUM, 0x01)) return false;            // osrs_h = x1
  if (!scriviRegistro(REG_CTRL_MEAS, (1 << 5) | (1 << 2) | 0x01)) return false;  // osrs_t x1, osrs_p x1, forced
  // Tempo massimo di misura con x1 su tutto: circa 9,3 ms (appendice 9.1).
  delay(10);
  uint8_t stato = 0x08;
  for (int i = 0; i < 20 && (stato & 0x08); i++) {
    if (!leggiRegistri(REG_STATUS, &stato, 1)) return false;
    if (stato & 0x08) delay(2);
  }
  uint8_t d[8];
  if (!leggiRegistri(REG_DATI, d, 8)) return false;                  // lettura unica 0xF7...0xFE
  int32_t adcP = ((int32_t)d[0] << 12) | ((int32_t)d[1] << 4) | (d[2] >> 4);
  int32_t adcT = ((int32_t)d[3] << 12) | ((int32_t)d[4] << 4) | (d[5] >> 4);
  int32_t adcH = ((int32_t)d[6] << 8) | d[7];
  if (adcT == 0x80000 || adcP == 0x80000 || adcH == 0x8000) return false;  // valori di "misura saltata"
  int32_t tFine;
  int32_t t = compensaTemperatura(adcT, taratura, tFine);
  uint32_t p = compensaPressione(adcP, taratura, tFine);
  uint32_t h = compensaUmidita(adcH, taratura, tFine);
  if (p == 0) return false;
  temperaturaC = t / 100.0f;
  pressioneHpa = (p / 256.0f) / 100.0f;
  umiditaPct = h / 1024.0f;
  return true;
}

// --- Anemometro: impulsi contati nell'interruzione ---
static volatile uint32_t impulsiTotali = 0;
static volatile uint32_t ultimoImpulsoUs = 0;

void IRAM_ATTR suImpulso() {
  uint32_t ora = micros();
  if ((uint32_t)(ora - ultimoImpulsoUs) >= (uint32_t)ANTIRIMBALZO_MS * 1000UL) {
    impulsiTotali = impulsiTotali + 1;
    ultimoImpulsoUs = ora;
  }
}

static uint32_t leggiImpulsi() {
  noInterrupts();
  uint32_t n = impulsiTotali;
  interrupts();
  return n;
}

// Blocchi da 3 secondi: 20 blocchi = 1 minuto.
static const uint32_t BLOCCO_S = 3;
static uint16_t perBlocco[20] = {0};
static uint32_t bloccoCorrente = 0;
static uint32_t impulsiContati = 0;
// Massimo di impulsi in un blocco, minuto per minuto: gli ultimi 60 minuti.
static uint16_t massimoPerMinuto[60] = {0};

static void aggiornaVento() {
  uint32_t blocco = (uint32_t)(esp_timer_get_time() / (BLOCCO_S * 1000000LL));
  uint32_t n = leggiImpulsi();
  while (bloccoCorrente < blocco) {
    bloccoCorrente++;
    perBlocco[bloccoCorrente % 20] = 0;
    if (bloccoCorrente % 20 == 0) massimoPerMinuto[(bloccoCorrente / 20) % 60] = 0;
  }
  uint32_t nuovi = n - impulsiContati;
  if (nuovi > 0) {
    uint32_t s = perBlocco[bloccoCorrente % 20] + nuovi;
    perBlocco[bloccoCorrente % 20] = s > 65535UL ? 65535 : (uint16_t)s;
    impulsiContati = n;
  }
  uint16_t &m = massimoPerMinuto[(bloccoCorrente / 20) % 60];
  if (perBlocco[bloccoCorrente % 20] > m) m = perBlocco[bloccoCorrente % 20];
}

static bool ventoTarato() { return KMH_PER_HZ > 0.0f; }

// Impulsi al secondo, media dell'ultimo minuto: i 19 blocchi completi, senza
// il blocco in corso (ancora a meta') che farebbe sottostimare fino al 5 %.
static float hzMediaMinuto() {
  uint32_t s = 0;
  const int corrente = (int)(bloccoCorrente % 20);
  for (int i = 0; i < 20; i++) if (i != corrente) s += perBlocco[i];
  return s / (19.0f * BLOCCO_S);
}

// Impulsi al secondo, valore piu' alto su 3 secondi nell'ultima ora.
static float hzMassimo3sOra() {
  uint16_t m = 0;
  for (int i = 0; i < 60; i++) if (massimoPerMinuto[i] > m) m = massimoPerMinuto[i];
  return m / (float)BLOCCO_S;
}

static String numeroOppureNull(float v, int decimali) {
  if (isnan(v)) return "null";
  return String(v, decimali);
}

static String datiJson() {
  float hzMedia = hzMediaMinuto(), hzMax = hzMassimo3sOra();
  String s = "{";
  s += "\"secondi_dall_accensione\":" + String((uint32_t)(esp_timer_get_time() / 1000000LL));
  s += ",\"sensore_bme280_ok\":" + String(bmeValido ? "true" : "false");
  s += ",\"temperatura_c\":" + numeroOppureNull(bmeValido ? temperaturaC : NAN, 2);
  s += ",\"umidita_pct\":" + numeroOppureNull(bmeValido ? umiditaPct : NAN, 1);
  s += ",\"pressione_hpa_alla_stazione\":" + numeroOppureNull(bmeValido ? pressioneHpa : NAN, 1);
  s += ",\"vento_hz_media_1min\":" + String(hzMedia, 2);
  s += ",\"vento_hz_max_3s_ultima_ora\":" + String(hzMax, 2);
  if (ventoTarato()) {
    s += ",\"kmh_per_hz\":" + String(KMH_PER_HZ, 3);
    s += ",\"vento_kmh_media_1min\":" + String(hzMedia * KMH_PER_HZ, 1);
    s += ",\"vento_kmh_max_3s_ultima_ora\":" + String(hzMax * KMH_PER_HZ, 1);
  } else {
    s += ",\"kmh_per_hz\":null,\"vento_kmh_media_1min\":null,\"vento_kmh_max_3s_ultima_ora\":null";
  }
  s += ",\"impulsi_vento_totali\":" + String(leggiImpulsi());
  s += "}";
  return s;
}

#if USA_WIFI
static void paginaPrincipale() {
  float hzMedia = hzMediaMinuto(), hzMax = hzMassimo3sOra();
  String h = "<!DOCTYPE html><html lang=\"it\"><head><meta charset=\"utf-8\">"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
             "<meta http-equiv=\"refresh\" content=\"60\">"
             "<title>Stazione meteo</title>"
             "<style>body{font-family:sans-serif;margin:1.5rem;line-height:1.5;color:#1a1a1a}"
             "h1{color:#003366}dt{font-weight:bold}dd{margin:0 0 .8rem 0;font-size:1.4rem}</style>"
             "</head><body><h1>Stazione meteo</h1><dl>";
  if (bmeValido) {
    h += "<dt>Temperatura</dt><dd>" + String(temperaturaC, 1) + " &deg;C</dd>";
    h += "<dt>Umidit&agrave; relativa</dt><dd>" + String(umiditaPct, 0) + " %</dd>";
    h += "<dt>Pressione alla quota della stazione</dt><dd>" + String(pressioneHpa, 1) + " hPa</dd>";
  } else {
    h += "<dt>Sensore BME280</dt><dd>da controllare: nessuna misura valida</dd>";
  }
  if (ventoTarato()) {
    h += "<dt>Vento, media dell'ultimo minuto</dt><dd>" + String(hzMedia * KMH_PER_HZ, 1) + " km/h</dd>";
    h += "<dt>Vento, valore pi&ugrave; alto su 3 secondi nell'ultima ora</dt><dd>" + String(hzMax * KMH_PER_HZ, 1) + " km/h</dd>";
  } else {
    h += "<dt>Vento</dt><dd>taratura mancante: " + String(hzMedia, 2) + " impulsi al secondo</dd>";
  }
  h += "</dl><p>La pressione non &egrave; riportata al livello del mare: non si confronta "
       "direttamente con quella dei bollettini.</p>"
       "<p>Dispositivo non certificato. Non sostituisce i bollettini ufficiali. "
       "In pericolo chiama il 112.</p><p>La pagina si aggiorna ogni minuto.</p></body></html>";
  server.send(200, "text/html; charset=utf-8", h);
}
#endif

void setup() {
  Serial.begin(115200);
  delay(50);
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(100000);
  // Pull-up interna; con un cavo lungo aggiungi una resistenza da 10 kohm verso 3,3 V.
  pinMode(PIN_ANEMOMETRO, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_ANEMOMETRO), suImpulso, FALLING);

  if (!avviaBme280()) Serial.println("BME280 non trovato a 0x76 ne' a 0x77: controlla i collegamenti. Riprovo a ogni misura.");
  if (!ventoTarato()) Serial.println("Taratura del vento mancante: imposta KMH_PER_HZ in config.h. Per ora mostro gli impulsi al secondo.");

#if USA_WIFI
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Collegamento al Wi-Fi");
  for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("Pagina dei dati: http://");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Wi-Fi non raggiunto: le misure continuano, riprovo da solo.");
  }
  WiFi.setAutoReconnect(true);
  server.on("/", paginaPrincipale);
  server.on("/dati.json", []() { server.send(200, "application/json", datiJson()); });
  server.onNotFound([]() { server.send(404, "text/plain; charset=utf-8", "Pagina non trovata"); });
  server.begin();
#endif
}

void loop() {
  static uint32_t ultimaMisura = 0;
  static bool prima = true;
  aggiornaVento();
  if (prima || millis() - ultimaMisura >= (uint32_t)INTERVALLO_BME_S * 1000UL) {
    prima = false;
    ultimaMisura = millis();
    bmeValido = misuraBme280();
    if (!bmeValido) {
      misureFallite++;
      indirizzoBme = 0;  // al prossimo giro cerca di nuovo il sensore
      Serial.println("Misura del BME280 non riuscita: sensore da controllare.");
    }
    Serial.println(datiJson());
  }
#if USA_WIFI
  server.handleClient();
#endif
  delay(5);
}
