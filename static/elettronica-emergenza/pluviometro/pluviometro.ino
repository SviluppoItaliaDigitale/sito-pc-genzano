/*
  Pluviometro a bascula con ESP32.
  Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
  https://www.protezionecivilegenzano.it/elettronica-emergenza/pluviometro/
  Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).

  Dispositivo NON certificato: le misure servono a osservare la pioggia sul
  posto. Non sostituiscono le stazioni della rete regionale, i bollettini del
  Centro Funzionale ne' il 112.

  Funzionamento: ogni ribaltamento della bascula chiude il contatto reed e
  genera un impulso. La scheda conta gli impulsi (con antirimbalzo), li somma
  minuto per minuto e calcola i mm dell'ultima ora con la taratura scritta in
  config.h. Senza taratura conta solo gli impulsi.
  I dati escono sulla seriale ogni minuto e, se USA_WIFI e' true, su una
  pagina web nella rete locale (/ e /dati.json).

  Scheda: "ESP32 Dev Module" (core Arduino-ESP32 di Espressif, versione 3 o 4).
*/

#include <Arduino.h>
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

// --- Conteggio degli impulsi (nell'interruzione) ---
static volatile uint32_t impulsiTotali = 0;
static volatile uint32_t ultimoImpulsoUs = 0;

void IRAM_ATTR suImpulso() {
  uint32_t ora = micros();
  if ((uint32_t)(ora - ultimoImpulsoUs) >= (uint32_t)ANTIRIMBALZO_MS * 1000UL) {
    impulsiTotali = impulsiTotali + 1;
    ultimoImpulsoUs = ora;
  }
}

// --- Somme per minuto: gli ultimi 60 minuti ---
static uint16_t perMinuto[60] = {0};
static uint32_t minutoCorrente = 0;   // minuti dall'accensione
static uint32_t impulsiContati = 0;   // impulsi gia' assegnati a un minuto
static bool pioggiaIntensa = false;

static bool tarato() { return MM_PER_SCATTO > 0.0f; }

static uint32_t leggiImpulsi() {
  noInterrupts();
  uint32_t n = impulsiTotali;
  interrupts();
  return n;
}

static uint32_t impulsiUltimaOra() {
  uint32_t s = 0;
  for (int i = 0; i < 60; i++) s += perMinuto[i];
  return s;
}

// Assegna al minuto giusto gli impulsi arrivati e azzera i minuti passati.
static void aggiornaMinuti() {
  // esp_timer conta in microsecondi a 64 bit: non torna a zero come millis().
  uint32_t minuto = (uint32_t)(esp_timer_get_time() / 60000000LL);
  uint32_t n = leggiImpulsi();
  while (minutoCorrente < minuto) {
    minutoCorrente++;
    perMinuto[minutoCorrente % 60] = 0;
  }
  uint32_t nuovi = n - impulsiContati;
  if (nuovi > 0) {
    uint32_t somma = perMinuto[minutoCorrente % 60] + nuovi;
    perMinuto[minutoCorrente % 60] = somma > 65535UL ? 65535 : (uint16_t)somma;
    impulsiContati = n;
  }
}

static void valutaSoglia(float mmOra) {
  if (!tarato() || SOGLIA_MM_ORA <= 0.0f) return;
  if (!pioggiaIntensa && mmOra >= SOGLIA_MM_ORA) {
    pioggiaIntensa = true;
    Serial.printf("PIOGGIA INTENSA DA VERIFICARE: %.1f mm nell'ultima ora, soglia %.1f.\n", mmOra, SOGLIA_MM_ORA);
  } else if (pioggiaIntensa && mmOra <= SOGLIA_MM_ORA - ISTERESI_MM_ORA) {
    pioggiaIntensa = false;
    Serial.printf("Valore rientrato: %.1f mm nell'ultima ora.\n", mmOra);
  }
  digitalWrite(PIN_LED, pioggiaIntensa ? HIGH : LOW);
}

static String datiJson() {
  uint32_t tot = leggiImpulsi();
  uint32_t ora = impulsiUltimaOra();
  String s = "{";
  s += "\"secondi_dall_accensione\":" + String((uint32_t)(esp_timer_get_time() / 1000000LL));
  s += ",\"impulsi_totali\":" + String(tot);
  s += ",\"impulsi_ultima_ora\":" + String(ora);
  if (tarato()) {
    s += ",\"mm_per_scatto\":" + String(MM_PER_SCATTO, 4);
    s += ",\"mm_totali\":" + String(tot * MM_PER_SCATTO, 1);
    s += ",\"mm_ultima_ora\":" + String(ora * MM_PER_SCATTO, 1);
  } else {
    s += ",\"mm_per_scatto\":null,\"mm_totali\":null,\"mm_ultima_ora\":null";
  }
  s += ",\"pioggia_intensa_da_verificare\":" + String(pioggiaIntensa ? "true" : "false");
  s += "}";
  return s;
}

#if USA_WIFI
static void paginaPrincipale() {
  uint32_t tot = leggiImpulsi();
  uint32_t ora = impulsiUltimaOra();
  String h = "<!DOCTYPE html><html lang=\"it\"><head><meta charset=\"utf-8\">"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
             "<meta http-equiv=\"refresh\" content=\"60\">"
             "<title>Pluviometro</title>"
             "<style>body{font-family:sans-serif;margin:1.5rem;line-height:1.5;color:#1a1a1a}"
             "h1{color:#003366}dt{font-weight:bold}dd{margin:0 0 .8rem 0;font-size:1.4rem}</style>"
             "</head><body><h1>Pluviometro</h1><dl>";
  if (tarato()) {
    h += "<dt>Pioggia nell'ultima ora</dt><dd>" + String(ora * MM_PER_SCATTO, 1) + " mm</dd>";
    h += "<dt>Pioggia dall'accensione</dt><dd>" + String(tot * MM_PER_SCATTO, 1) + " mm</dd>";
  } else {
    h += "<dt>Taratura</dt><dd>mancante: i millimetri non si calcolano</dd>";
  }
  h += "<dt>Ribaltamenti nell'ultima ora</dt><dd>" + String(ora) + "</dd>";
  h += "<dt>Ribaltamenti dall'accensione</dt><dd>" + String(tot) + "</dd>";
  if (pioggiaIntensa) h += "<dt>Stato</dt><dd>pioggia intensa da verificare</dd>";
  h += "</dl><p>Dispositivo non certificato. Non sostituisce i bollettini ufficiali. "
       "In pericolo chiama il 112.</p><p>La pagina si aggiorna ogni minuto.</p></body></html>";
  server.send(200, "text/html; charset=utf-8", h);
}
#endif

void setup() {
  Serial.begin(115200);
  delay(50);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);
  // Pull-up interna; con un cavo lungo aggiungi una resistenza da 10 kohm verso 3,3 V.
  pinMode(PIN_REED, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_REED), suImpulso, FALLING);

  if (!tarato()) {
    Serial.println("Taratura mancante: imposta MM_PER_SCATTO in config.h. Per ora conto solo gli impulsi.");
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
    Serial.println("Wi-Fi non raggiunto: il conteggio continua, riprovo da solo.");
  }
  WiFi.setAutoReconnect(true);
  server.on("/", paginaPrincipale);
  server.on("/dati.json", []() { server.send(200, "application/json", datiJson()); });
  server.onNotFound([]() { server.send(404, "text/plain; charset=utf-8", "Pagina non trovata"); });
  server.begin();
#endif
}

void loop() {
  static uint32_t ultimaStampa = 0;
  aggiornaMinuti();
  if (millis() - ultimaStampa >= 60000UL) {
    ultimaStampa = millis();
    float mmOra = impulsiUltimaOra() * MM_PER_SCATTO;
    valutaSoglia(mmOra);
    Serial.println(datiJson());
  }
#if USA_WIFI
  server.handleClient();
#endif
  delay(5);
}
