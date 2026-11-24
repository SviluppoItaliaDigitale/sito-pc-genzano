/*
  Controllo della batteria a 12 V di un mezzo o di un gruppo elettrogeno, con ESP32.
  Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
  https://www.protezionecivilegenzano.it/elettronica-emergenza/batteria-12v/
  Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).

  Dispositivo NON certificato: la tensione misurata serve a notare per tempo
  una batteria che si sta scaricando. Non sostituisce un tester per batterie,
  la manutenzione del mezzo ne' il 112.

  Funzionamento: un partitore resistivo porta la tensione della batteria
  entro la scala dell'ADC1. Ogni 5 secondi la scheda fa 21 letture con
  analogReadMilliVolts() (valori corretti con la taratura di fabbrica
  dell'ESP32), prende la mediana e calcola la tensione della batteria.
  Se la tensione resta bassa per un minuto accende il LED: "tensione bassa
  da verificare". La stima della carica usa la tabella del produttore e
  vale solo con la batteria a riposo.
  I dati escono sulla seriale ogni minuto e, se USA_WIFI e' true, su una
  pagina web nella rete locale (/ e /dati.json).

  Scheda: "ESP32 Dev Module" (pacchetto esp32 di Espressif, versione 3 o 4).
*/

#include <Arduino.h>
#include "esp_sleep.h"
#include "config.h"
#include "calcoli.h"

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

static float voltUltima = 0.0f;
static int32_t mvUltima = 0;
static bool misuraValida = false;
static StatoSoglia statoBassa = {false, 0};
static int sottoSonno = 0;

// Oltre circa 2450 mV sul pin la misura dell'ESP32 e' meno precisa
// (datasheet ESP32, tabella 4-4, attenuazione 3).
static const int32_t MV_LIMITE_PRECISO = 2450;

static void misura() {
  int32_t letture[CAMPIONI];
  for (int i = 0; i < CAMPIONI; i++) {
    letture[i] = analogReadMilliVolts(PIN_TENSIONE);
    delay(2);
  }
  mvUltima = mediana(letture, CAMPIONI);
  voltUltima = tensioneBatteria((float)mvUltima, R_ALTA_OHM, R_BASSA_OHM, CORREZIONE);
  misuraValida = true;
}

static bool fuoriScala() { return mvUltima > MV_LIMITE_PRECISO; }

static String datiJson() {
  String s = "{";
  s += "\"secondi_dall_accensione\":" + String((uint32_t)(millis() / 1000UL));
  if (misuraValida) {
    s += ",\"tensione_v\":" + String(voltUltima, 2);
    s += ",\"millivolt_sul_pin\":" + String(mvUltima);
    float c = stimaCarica(voltUltima);
    if (c < 0.0f || c > 100.0f) s += ",\"carica_stimata_a_riposo_percento\":null";
    else s += ",\"carica_stimata_a_riposo_percento\":" + String((int)(c + 0.5f));
    s += ",\"fuori_scala\":" + String(fuoriScala() ? "true" : "false");
  } else {
    s += ",\"tensione_v\":null,\"millivolt_sul_pin\":null,\"carica_stimata_a_riposo_percento\":null,\"fuori_scala\":false";
  }
  s += ",\"soglia_bassa_v\":" + String(SOGLIA_BASSA_V, 2);
  s += ",\"tensione_bassa_da_verificare\":" + String(statoBassa.bassa ? "true" : "false");
  s += "}";
  return s;
}

#if USA_WIFI
static String testoCarica() {
  float c = stimaCarica(voltUltima);
  if (c < 0.0f) return "meno del 10%";
  if (c > 100.0f) return "oltre la tabella: batteria piena oppure in carica";
  return "circa " + String((int)(c + 0.5f)) + "%";
}

static void paginaPrincipale() {
  String h = "<!DOCTYPE html><html lang=\"it\"><head><meta charset=\"utf-8\">"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
             "<meta http-equiv=\"refresh\" content=\"60\">"
             "<title>Batteria 12 V</title>"
             "<style>body{font-family:sans-serif;margin:1.5rem;line-height:1.5;color:#1a1a1a}"
             "h1{color:#003366}dt{font-weight:bold}dd{margin:0 0 .8rem 0;font-size:1.4rem}</style>"
             "</head><body><h1>Batteria 12 V</h1><dl>";
  if (misuraValida) {
    h += "<dt>Tensione</dt><dd>" + String(voltUltima, 2) + " V</dd>";
    h += "<dt>Carica stimata, solo a riposo</dt><dd>" + testoCarica() + "</dd>";
    if (fuoriScala()) h += "<dt>Misura</dt><dd>fuori dalla scala precisa: controlla il partitore</dd>";
  } else {
    h += "<dt>Tensione</dt><dd>misura in corso</dd>";
  }
  h += "<dt>Stato</dt><dd>";
  h += statoBassa.bassa ? "tensione bassa da verificare" : "nessuna anomalia";
  h += "</dd></dl><p>La stima della carica vale solo con la batteria a riposo da almeno "
       "6 ore, senza carica ne' carichi collegati. Con il motore acceso o il caricabatterie "
       "collegato la tensione sale e la stima non vale.</p>"
       "<p>Dispositivo non certificato. In pericolo chiama il 112.</p>"
       "<p>La pagina si aggiorna ogni minuto.</p></body></html>";
  server.send(200, "text/html; charset=utf-8", h);
}
#endif

static void vaiASonno() {
  Serial.printf("Tensione %.2f V sotto %.2f V: la scheda dorme per %d minuti per non scaricare la batteria.\n",
                voltUltima, TENSIONE_SONNO_V, SONNO_MINUTI);
  digitalWrite(PIN_LED, LOW);
  Serial.flush();
#if USA_WIFI
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
#endif
  esp_sleep_enable_timer_wakeup((uint64_t)SONNO_MINUTI * 60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

static void valuta() {
  if (aggiornaSoglia(&statoBassa, voltUltima, SOGLIA_BASSA_V, ISTERESI_V, CONFERME)) {
    if (statoBassa.bassa) {
      Serial.printf("TENSIONE BASSA DA VERIFICARE: %.2f V, soglia %.2f V.\n", voltUltima, SOGLIA_BASSA_V);
    } else {
      Serial.printf("Valore rientrato: %.2f V.\n", voltUltima);
    }
  }
  digitalWrite(PIN_LED, statoBassa.bassa ? HIGH : LOW);

  if (TENSIONE_SONNO_V > 0.0f && !fuoriScala() && voltUltima < TENSIONE_SONNO_V) {
    sottoSonno++;
    if (sottoSonno >= CONFERME) vaiASonno();
  } else {
    sottoSonno = 0;
  }
}

void setup() {
  Serial.begin(115200);
  delay(50);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);
  analogReadResolution(12);
  analogSetPinAttenuation(PIN_TENSIONE, ADC_11db);

  if (CORREZIONE == 1.0f) {
    Serial.println("Taratura non ancora fatta: confronta la tensione con un multimetro e scrivi CORREZIONE in config.h.");
  }

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
    Serial.println("Wi-Fi non raggiunto: la misura continua, riprovo da solo.");
  }
  WiFi.setAutoReconnect(true);
  server.on("/", paginaPrincipale);
  server.on("/dati.json", []() { server.send(200, "application/json", datiJson()); });
  server.onNotFound([]() { server.send(404, "text/plain; charset=utf-8", "Pagina non trovata"); });
  server.begin();
#endif

  misura();
}

void loop() {
  static uint32_t ultimaMisura = 0;
  static uint32_t ultimaStampa = 0;
  if (millis() - ultimaMisura >= (uint32_t)INTERVALLO_MISURA_MS) {
    ultimaMisura = millis();
    misura();
    valuta();
  }
  if (millis() - ultimaStampa >= 60000UL) {
    ultimaStampa = millis();
    Serial.println(datiJson());
  }
#if USA_WIFI
  server.handleClient();
#endif
  delay(5);
}
