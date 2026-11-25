// Impostazioni della stazione meteo con ESP32.
// Modifica solo questo file. Pagina del progetto:
// https://www.protezionecivilegenzano.it/elettronica-emergenza/stazione-meteo/
#pragma once

// --- Collegamenti (ESP32 classico, per esempio ESP32-DevKitC) ---
#define PIN_SDA          21   // I2C, dato: pin SDA del BME280
#define PIN_SCL          22   // I2C, orologio: pin SCL del BME280
#define PIN_ANEMOMETRO   27   // un filo del contatto reed; l'altro filo va a GND

// --- Indirizzo I2C del BME280 ---
// 0x76 con il pin SDO a GND, 0x77 con il pin SDO a 3,3 V
// (scheda tecnica Bosch, capitolo 6.2). 0 = lo sketch prova da solo
// prima 0x76 e poi 0x77.
#define INDIRIZZO_BME280  0

// --- Taratura dell'anemometro: DA SCRIVERE, non lasciare 0 ---
// Chilometri all'ora che corrispondono a un impulso al secondo.
// Si prende dalla scheda tecnica del TUO anemometro oppure si misura
// con la taratura descritta nella pagina del progetto.
// Con 0 lo sketch mostra solo gli impulsi al secondo (Hz).
#define KMH_PER_HZ  0.0f

// --- Antirimbalzo dell'anemometro ---
// Un contatto reed puo' chiudere piu' volte in pochi millisecondi:
// gli impulsi piu' vicini di questo tempo si contano una volta.
// Con 5 ms si contano fino a 200 impulsi al secondo.
#define ANTIRIMBALZO_MS  5

// --- Intervallo fra due misure del BME280, in secondi ---
// La scheda tecnica consiglia per il monitoraggio meteo una misura al
// minuto in "forced mode" (capitolo 3.5.1): il sensore si scalda meno.
#define INTERVALLO_BME_S  60

// --- Pagina web nella rete locale ---
// true: si collega al Wi-Fi indicato in segreti.h e mostra i dati
// all'indirizzo che stampa sulla seriale. false: solo seriale.
#define USA_WIFI  true
