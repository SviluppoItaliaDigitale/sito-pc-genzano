/*
  Sensore del livello dell'acqua per un fosso o un sottopasso.
  Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
  https://www.protezionecivilegenzano.it/elettronica-emergenza/livello-acqua/
  Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).

  Dispositivo NON certificato: segnala sul posto un'anomalia da verificare.
  Non sostituisce le allerte ufficiali, gli idrometri della rete regionale
  ne' il 112. Se c'e' pericolo per le persone, chiama il 112.

  Funzionamento: ogni INTERVALLO_S secondi la scheda si sveglia, misura la
  distanza dall'acqua (mediana di N_LETTURE), calcola il livello, accende LED
  e cicalino se il livello supera la soglia, poi torna a dormire.
  Una misura non valida non cambia lo stato: si riprova al risveglio dopo.
  Le impostazioni stanno in config.h.

  Scheda: "ESP32 Dev Module" (core Arduino-ESP32 di Espressif, versione 3 o 4).
*/

#include <Arduino.h>
#include "esp_sleep.h"
#include "config.h"

// Lo stato resta nella memoria RTC durante il sonno profondo.
RTC_DATA_ATTR bool anomalia = false;
RTC_DATA_ATTR uint8_t nonValideDiFila = 0;
RTC_DATA_ATTR uint32_t risvegli = 0;

static bool tarato() {
  return ALTEZZA_SENSORE_CM > 0.0f && SOGLIA_LIVELLO_CM > 0.0f &&
         SOGLIA_LIVELLO_CM - ISTERESI_CM > 0.0f &&
         ALTEZZA_SENSORE_CM - SOGLIA_LIVELLO_CM >= DISTANZA_MIN_CM;
}

// Una lettura singola in cm, oppure -1 se il sensore non risponde
// o se la distanza e' fuori dai limiti della scheda tecnica.
static float letturaCm() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(4);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(20);  // la scheda tecnica chiede almeno 10 microsecondi
  digitalWrite(PIN_TRIG, LOW);
  // Senza eco il modulo riporta Echo basso dopo circa 40 ms: attesa massima 50 ms.
  unsigned long durata = pulseIn(PIN_ECHO, HIGH, 50000UL);
  if (durata == 0) return -1.0f;
  float cm = (float)durata * VELOCITA_SUONO_CM_US / 2.0f;
  if (cm < DISTANZA_MIN_CM || cm > DISTANZA_MAX_CM) return -1.0f;
  return cm;
}

// Mediana delle letture valide, oppure -1 se le valide sono troppo poche.
static float misuraCm() {
  float v[N_LETTURE];
  int n = 0;
  for (int i = 0; i < N_LETTURE; i++) {
    float cm = letturaCm();
    if (cm > 0.0f) v[n++] = cm;
    delay(PAUSA_LETTURE_MS);
  }
  if (n < LETTURE_VALIDE_MIN) return -1.0f;
  for (int i = 1; i < n; i++) {  // ordinamento per inserimento
    float x = v[i];
    int j = i - 1;
    while (j >= 0 && v[j] > x) { v[j + 1] = v[j]; j--; }
    v[j + 1] = x;
  }
  return (n % 2) ? v[n / 2] : (v[n / 2 - 1] + v[n / 2]) / 2.0f;
}

static void lampeggia(int volte, int accesoMs, int spentoMs, bool suono) {
  for (int i = 0; i < volte; i++) {
    digitalWrite(PIN_LED, HIGH);
    if (suono && CICALINO_ATTIVO) digitalWrite(PIN_CICALINO, HIGH);
    delay(accesoMs);
    digitalWrite(PIN_LED, LOW);
    digitalWrite(PIN_CICALINO, LOW);
    delay(spentoMs);
  }
}

static void dormi(uint32_t secondi) {
  Serial.flush();
  esp_sleep_enable_timer_wakeup((uint64_t)secondi * 1000000ULL);
  esp_deep_sleep_start();
}

void setup() {
  Serial.begin(115200);
  delay(50);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_CICALINO, OUTPUT);
  digitalWrite(PIN_LED, LOW);
  digitalWrite(PIN_CICALINO, LOW);
  risvegli++;

  if (!tarato()) {
    // Senza taratura il dispositivo non giudica nulla: due lampi lunghi.
    Serial.println("Taratura mancante o incoerente: imposta ALTEZZA_SENSORE_CM e SOGLIA_LIVELLO_CM in config.h.");
    lampeggia(2, 600, 300, false);
    dormi(INTERVALLO_S);
  }

  float distanza = misuraCm();
  if (distanza < 0.0f) {
    if (nonValideDiFila < 255) nonValideDiFila++;
    Serial.printf("%lu;misura non valida (%u di fila);stato invariato;%s\n",
                  (unsigned long)risvegli, nonValideDiFila,
                  anomalia ? "anomalia da verificare" : "normale");
    if (nonValideDiFila >= NON_VALIDE_PER_GUASTO) {
      Serial.println("Sensore da controllare: niente misure valide da diversi risvegli.");
      lampeggia(5, 80, 120, false);  // cinque lampi rapidi
    }
    dormi(anomalia ? INTERVALLO_ANOMALIA_S : INTERVALLO_S);
  }
  nonValideDiFila = 0;

  float livello = ALTEZZA_SENSORE_CM - distanza;
  if (livello < 0.0f) livello = 0.0f;

  if (!anomalia && livello >= SOGLIA_LIVELLO_CM) {
    anomalia = true;
    Serial.printf("ANOMALIA DA VERIFICARE: livello %.1f cm, soglia %.1f cm.\n", livello, SOGLIA_LIVELLO_CM);
  } else if (anomalia && livello <= SOGLIA_LIVELLO_CM - ISTERESI_CM) {
    anomalia = false;
    Serial.printf("Valore rientrato: livello %.1f cm, sotto %.1f cm.\n", livello, SOGLIA_LIVELLO_CM - ISTERESI_CM);
  }

  Serial.printf("%lu;distanza %.1f cm;livello %.1f cm;%s\n", (unsigned long)risvegli,
                distanza, livello, anomalia ? "anomalia da verificare" : "normale");

  if (anomalia) {
    lampeggia(3, 400, 200, true);  // LED e cicalino a ogni misura, finche' non rientra
    dormi(INTERVALLO_ANOMALIA_S);
  }
  lampeggia(1, 30, 0, false);  // breve lampo: il dispositivo e' acceso e misura
  dormi(INTERVALLO_S);
}

void loop() {
  // Non si arriva qui: ogni ciclo finisce con il sonno profondo.
}
