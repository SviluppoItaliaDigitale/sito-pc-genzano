// Impostazioni del monitor del caldo con ESP32.
// Modifica solo questo file. Pagina del progetto:
// https://www.protezionecivilegenzano.it/elettronica-emergenza/monitor-caldo/
#pragma once

// --- Collegamenti (ESP32 classico, per esempio ESP32-DevKitC) ---
#define PIN_SDA     21   // I2C, dato: pin SDA del sensore SHT4x
#define PIN_SCL     22   // I2C, orologio: pin SCL del sensore SHT4x
#define PIN_LED_1   25   // primo LED (giallo), con resistenza da 330 ohm verso GND
#define PIN_LED_2   26   // secondo LED (arancione)
#define PIN_LED_3   27   // terzo LED (rosso)

// --- Indirizzo I2C del sensore ---
// SHT40, SHT41 e SHT45 nella versione "AD1B" rispondono a 0x44
// (scheda tecnica Sensirion SHT4x). Altre versioni: 0x45 o 0x46,
// scritto nella scheda del modulo.
#define INDIRIZZO_SHT4X  0x44

// --- Misure ---
// Una misura ogni INTERVALLO_S secondi; l'indice si calcola sulla mediana
// delle ultime CAMPIONI misure, cosi' una lettura storta non cambia lo stato.
#define INTERVALLO_S  10
#define CAMPIONI      5

// --- Isteresi, in gradi Celsius di indice di calore ---
// Per scendere di fascia l'indice deve stare sotto il limite della fascia
// di almeno questo valore: i LED non si accendono e spengono di continuo.
#define ISTERESI_C  0.5f

// --- Pagina web nella rete locale ---
// true: si collega al Wi-Fi indicato in segreti.h e mostra i dati
// all'indirizzo che stampa sulla seriale. false: solo seriale e LED.
#define USA_WIFI  true
