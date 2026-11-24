/*
  Monitor del caldo con ESP32 e sensore Sensirion SHT4x.
  Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
  https://www.protezionecivilegenzano.it/elettronica-emergenza/monitor-caldo/
  Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).

  Dispositivo NON certificato: segnala un'anomalia da verificare. Non
  sostituisce i bollettini sulle ondate di calore del Ministero della Salute,
  il parere di un medico ne' il 112.

  Funzionamento:
  - Ogni INTERVALLO_S secondi legge temperatura e umidita' dal sensore SHT4x
    (comando 0xFD, misura ad alta ripetibilita', controllo CRC-8: scheda
    tecnica Sensirion SHT4x, capitoli 4.4, 4.5 e 4.6).
  - Sulla mediana delle ultime misure calcola l'indice di calore (heat index)
    con il metodo del National Weather Service statunitense, pagina
    "The Heat Index Equation" del Weather Prediction Center: formula
    semplice, poi regressione di Rothfusz con le due correzioni.
  - Confronta l'indice con le quattro fasce del NWS (Caution, Extreme
    Caution, Danger, Extreme Danger) e accende i LED: 1, 2, 3 LED fissi,
    3 LED lampeggianti nella quarta fascia. Dalla prima fascia in su e'
    un'anomalia da verificare.
  I dati escono sulla seriale e, se USA_WIFI e' true, su una pagina web
  nella rete locale (/ e /dati.json).

  Scheda: "ESP32 Dev Module" (core Arduino-ESP32 di Espressif, versione 3 o 4).
*/

#include <Arduino.h>
#include <Wire.h>
#include <math.h>
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

// ===================== INIZIO CALCOLI =====================
// CRC-8 del sensore: polinomio 0x31, valore iniziale 0xFF
// (scheda tecnica SHT4x, capitolo 4.4; esempio: CRC(0xBEEF) = 0x92).
static uint8_t crc8Sht4x(const uint8_t *d, int n) {
  uint8_t crc = 0xFF;
  for (int i = 0; i < n; i++) {
    crc ^= d[i];
    for (int b = 0; b < 8; b++) crc = (crc & 0x80) ? (uint8_t)((crc << 1) ^ 0x31) : (uint8_t)(crc << 1);
  }
  return crc;
}

// Conversione dei valori grezzi (capitolo 4.6).
static float temperaturaDaGrezzo(uint16_t s) { return -45.0f + 175.0f * s / 65535.0f; }
static float umiditaDaGrezzo(uint16_t s) {
  float rh = -6.0f + 125.0f * s / 65535.0f;
  if (rh < 0.0f) rh = 0.0f;      // il capitolo 4.6 consiglia di tagliare a 0...100 %
  if (rh > 100.0f) rh = 100.0f;
  return rh;
}

static float celsiusInFahrenheit(float c) { return c * 1.8f + 32.0f; }
static float fahrenheitInCelsius(float f) { return (f - 32.0f) / 1.8f; }

// Indice di calore in gradi Fahrenheit, da temperatura in F e umidita' in %.
// Metodo della pagina WPC "The Heat Index Equation":
// 1) formula semplice; se la sua media con la temperatura e' sotto 80 F,
//    il risultato e' la formula semplice;
// 2) altrimenti regressione di Rothfusz (NWS Technical Attachment SR 90-23),
//    con la correzione per umidita' sotto il 13 % (fra 80 e 112 F) e quella
//    per umidita' sopra l'85 % (fra 80 e 87 F).
static float indiceCaloreF(float T, float RH) {
  float semplice = 0.5f * (T + 61.0f + ((T - 68.0f) * 1.2f) + (RH * 0.094f));
  if ((semplice + T) / 2.0f < 80.0f) return semplice;
  float hi = -42.379f + 2.04901523f * T + 10.14333127f * RH - 0.22475541f * T * RH
             - 0.00683783f * T * T - 0.05481717f * RH * RH + 0.00122874f * T * T * RH
             + 0.00085282f * T * RH * RH - 0.00000199f * T * T * RH * RH;
  if (RH < 13.0f && T >= 80.0f && T <= 112.0f) {
    hi -= ((13.0f - RH) / 4.0f) * sqrtf((17.0f - fabsf(T - 95.0f)) / 17.0f);
  } else if (RH > 85.0f && T >= 80.0f && T <= 87.0f) {
    hi += ((RH - 85.0f) / 10.0f) * ((87.0f - T) / 5.0f);
  }
  return hi;
}

// Fasce del NWS in gradi Fahrenheit: 80, 90, 103, 125.
// 0 = sotto la prima fascia; 1 Caution; 2 Extreme Caution; 3 Danger; 4 Extreme Danger.
static const float LIMITI_F[4] = {80.0f, 90.0f, 103.0f, 125.0f};

static int fasciaDa(float hiF) {
  int f = 0;
  for (int i = 0; i < 4; i++) if (hiF >= LIMITI_F[i]) f = i + 1;
  return f;
}

// Con isteresi: sale subito, scende solo sotto il limite meno l'isteresi.
static int fasciaConIsteresi(float hiF, int attuale, float isteresiF) {
  int nuova = fasciaDa(hiF);
  if (nuova >= attuale) return nuova;
  while (attuale > nuova && hiF < LIMITI_F[attuale - 1] - isteresiF) attuale--;
  return attuale;
}
// ====================== FINE CALCOLI ======================

static const char *NOMI_FASCE[5] = {
  "sotto la prima fascia", "Caution", "Extreme Caution", "Danger", "Extreme Danger"};

// --- Misure ---
static float campioniT[CAMPIONI], campioniRH[CAMPIONI];
static int numeroCampioni = 0, prossimoCampione = 0;
static bool sensoreOk = false;
static uint32_t lettureFallite = 0;
static float temperaturaC = NAN, umiditaPct = NAN, indiceC = NAN;
static int fascia = 0;

static bool leggiSht4x(float &tC, float &rh) {
  Wire.beginTransmission(INDIRIZZO_SHT4X);
  Wire.write(0xFD);                       // misura T e RH ad alta ripetibilita'
  if (Wire.endTransmission() != 0) return false;
  delay(10);                              // durata massima 8,3 ms (capitolo 3.1)
  if (Wire.requestFrom((int)INDIRIZZO_SHT4X, 6) != 6) return false;
  uint8_t d[6];
  for (int i = 0; i < 6; i++) d[i] = Wire.read();
  if (crc8Sht4x(d, 2) != d[2] || crc8Sht4x(d + 3, 2) != d[5]) return false;
  tC = temperaturaDaGrezzo((uint16_t)(d[0] << 8 | d[1]));
  rh = umiditaDaGrezzo((uint16_t)(d[3] << 8 | d[4]));
  return true;
}

static float mediana(const float *v, int n) {
  float c[CAMPIONI];
  for (int i = 0; i < n; i++) c[i] = v[i];
  for (int i = 1; i < n; i++) {           // ordinamento per inserzione
    float x = c[i]; int j = i - 1;
    while (j >= 0 && c[j] > x) { c[j + 1] = c[j]; j--; }
    c[j + 1] = x;
  }
  return (n % 2) ? c[n / 2] : (c[n / 2 - 1] + c[n / 2]) / 2.0f;
}

static void misura() {
  float t, rh;
  if (leggiSht4x(t, rh)) {
    lettureFallite = 0;
    campioniT[prossimoCampione] = t;
    campioniRH[prossimoCampione] = rh;
    prossimoCampione = (prossimoCampione + 1) % CAMPIONI;
    if (numeroCampioni < CAMPIONI) numeroCampioni++;
  } else {
    lettureFallite++;
  }
  // Tre letture fallite di fila: sensore da controllare. Lo stato dei LED
  // non mostra piu' una fascia, perche' i dati non sono aggiornati.
  if (lettureFallite >= 3 || numeroCampioni == 0) {
    sensoreOk = false;
    return;
  }
  sensoreOk = true;
  temperaturaC = mediana(campioniT, numeroCampioni);
  umiditaPct = mediana(campioniRH, numeroCampioni);
  float hiF = indiceCaloreF(celsiusInFahrenheit(temperaturaC), umiditaPct);
  indiceC = fahrenheitInCelsius(hiF);
  int prima = fascia;
  fascia = fasciaConIsteresi(hiF, fascia, ISTERESI_C * 1.8f);
  if (fascia != prima) {
    if (fascia > 0) Serial.printf("ANOMALIA DA VERIFICARE: indice di calore %.1f C, fascia NWS \"%s\".\n", indiceC, NOMI_FASCE[fascia]);
    else Serial.printf("Valore rientrato: indice di calore %.1f C.\n", indiceC);
  }
}

static void aggiornaLed() {
  bool acceso[3] = {false, false, false};
  if (!sensoreOk) {
    // Sensore da controllare: lampeggia solo il LED centrale, un lampo ogni 2 secondi.
    acceso[1] = (millis() % 2000) < 200;
  } else if (fascia >= 1 && fascia <= 3) {
    for (int i = 0; i < fascia; i++) acceso[i] = true;
  } else if (fascia == 4) {
    // Quarta fascia: tre LED che lampeggiano una volta al secondo.
    bool on = (millis() % 1000) < 500;
    acceso[0] = acceso[1] = acceso[2] = on;
  }
  digitalWrite(PIN_LED_1, acceso[0] ? HIGH : LOW);
  digitalWrite(PIN_LED_2, acceso[1] ? HIGH : LOW);
  digitalWrite(PIN_LED_3, acceso[2] ? HIGH : LOW);
}

static String numeroOppureNull(float v, int decimali) {
  if (!sensoreOk || isnan(v)) return "null";
  return String(v, decimali);
}

static String datiJson() {
  String s = "{";
  s += "\"secondi_dall_accensione\":" + String((uint32_t)(millis() / 1000UL));
  s += ",\"sensore_ok\":" + String(sensoreOk ? "true" : "false");
  s += ",\"temperatura_c\":" + numeroOppureNull(temperaturaC, 1);
  s += ",\"umidita_pct\":" + numeroOppureNull(umiditaPct, 1);
  s += ",\"indice_calore_c\":" + numeroOppureNull(indiceC, 1);
  s += ",\"fascia\":" + (sensoreOk ? String(fascia) : String("null"));
  s += ",\"fascia_nws\":" + (sensoreOk ? "\"" + String(NOMI_FASCE[fascia]) + "\"" : String("null"));
  s += ",\"anomalia_da_verificare\":" + String(sensoreOk && fascia > 0 ? "true" : "false");
  s += "}";
  return s;
}

#if USA_WIFI
static void paginaPrincipale() {
  String h = "<!DOCTYPE html><html lang=\"it\"><head><meta charset=\"utf-8\">"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
             "<meta http-equiv=\"refresh\" content=\"30\">"
             "<title>Monitor del caldo</title>"
             "<style>body{font-family:sans-serif;margin:1.5rem;line-height:1.5;color:#1a1a1a}"
             "h1{color:#003366}dt{font-weight:bold}dd{margin:0 0 .8rem 0;font-size:1.4rem}"
             ".nota{border-left:4px solid #003366;padding-left:.8rem}</style>"
             "</head><body><h1>Monitor del caldo</h1>";
  if (!sensoreOk) {
    h += "<p><strong>Sensore da controllare:</strong> nessuna misura valida.</p>";
  } else {
    h += "<dl><dt>Temperatura dell'aria</dt><dd>" + String(temperaturaC, 1) + " &deg;C</dd>";
    h += "<dt>Umidit&agrave; relativa</dt><dd>" + String(umiditaPct, 0) + " %</dd>";
    h += "<dt>Indice di calore (metodo del National Weather Service)</dt><dd>" + String(indiceC, 1) + " &deg;C</dd>";
    h += "<dt>Fascia</dt><dd>" + String(fascia) + " di 4: " + String(NOMI_FASCE[fascia]) + "</dd></dl>";
    if (fascia > 0) h += "<p><strong>Anomalia da verificare.</strong> Avvisa il responsabile della struttura.</p>";
  }
  h += "<p class=\"nota\">Dispositivo non certificato. Le fasce sono quelle del servizio meteorologico "
       "statunitense e valgono all'ombra. Per i consigli sul caldo segui le indicazioni del "
       "Ministero della Salute (salute.gov.it, sezione Ondate di calore). In pericolo chiama il 112.</p>"
       "<p>La pagina si aggiorna ogni 30 secondi.</p></body></html>";
  server.send(200, "text/html; charset=utf-8", h);
}
#endif

void setup() {
  Serial.begin(115200);
  delay(50);
  pinMode(PIN_LED_1, OUTPUT);
  pinMode(PIN_LED_2, OUTPUT);
  pinMode(PIN_LED_3, OUTPUT);
  // Prova dei LED all'accensione: si accendono uno per volta.
  const int pin[3] = {PIN_LED_1, PIN_LED_2, PIN_LED_3};
  for (int i = 0; i < 3; i++) { digitalWrite(pin[i], HIGH); delay(300); digitalWrite(pin[i], LOW); }
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(100000);

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
    Serial.println("Wi-Fi non raggiunto: misure e LED funzionano lo stesso, riprovo da solo.");
  }
  WiFi.setAutoReconnect(true);
  server.on("/", paginaPrincipale);
  server.on("/dati.json", []() { server.send(200, "application/json", datiJson()); });
  server.onNotFound([]() { server.send(404, "text/plain; charset=utf-8", "Pagina non trovata"); });
  server.begin();
#endif
  misura();
  Serial.println(datiJson());
}

void loop() {
  static uint32_t ultimaMisura = millis();
  if (millis() - ultimaMisura >= (uint32_t)INTERVALLO_S * 1000UL) {
    ultimaMisura = millis();
    misura();
    Serial.println(datiJson());
  }
  aggiornaLed();
#if USA_WIFI
  server.handleClient();
#endif
  delay(5);
}
