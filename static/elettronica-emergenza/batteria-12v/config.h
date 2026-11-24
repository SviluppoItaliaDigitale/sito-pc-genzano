// Impostazioni del controllo della batteria a 12 V.
// Modifica solo questo file. Pagina del progetto:
// https://www.protezionecivilegenzano.it/elettronica-emergenza/batteria-12v/
#pragma once

// --- Collegamenti (ESP32 classico, per esempio ESP32-DevKitC) ---
// GPIO 34 e' un canale dell'ADC1 (ADC1_CH6): funziona anche con il Wi-Fi acceso.
// Non usare i pin dell'ADC2 (0, 2, 4, 12-15, 25-27): li usa il Wi-Fi.
#define PIN_TENSIONE  34   // centro del partitore
#define PIN_LED       26   // LED con resistenza da 330 ohm verso GND

// --- Partitore resistivo (resistenze all'1%) ---
// R_ALTA fra il positivo della batteria (dopo il fusibile) e il pin,
// R_BASSA fra il pin e GND. Con 100 kohm e 15 kohm il pin riceve circa
// 1/7,67 della tensione: 18,7 V diventano 2,45 V, il limite della
// misura precisa dell'ADC con l'attenuazione massima.
#define R_ALTA_OHM   100000.0f
#define R_BASSA_OHM   15000.0f

// --- Taratura: DA FARE con un multimetro ---
// CORREZIONE = tensione letta dal multimetro / tensione mostrata dalla scheda.
// Lascia 1.0 finche' non hai fatto la prova.
#define CORREZIONE  1.000f

// --- Misura ---
#define CAMPIONI               21     // letture per ogni misura (si usa la mediana)
#define INTERVALLO_MISURA_MS   5000   // una misura ogni 5 secondi

// --- Tensione bassa: anomalia da verificare ---
// Sotto SOGLIA_BASSA_V per CONFERME misure di fila (12 x 5 s = 1 minuto)
// il LED si accende. Torna normale sopra SOGLIA_BASSA_V + ISTERESI_V.
// 12,10 V corrisponde al 50% di carica nella tabella del produttore,
// ma solo con la batteria a riposo: vedi la pagina del progetto.
// 0 = nessuna soglia.
#define SOGLIA_BASSA_V   12.10f
#define ISTERESI_V        0.20f
#define CONFERME          12

// --- Riposo della scheda per non scaricare la batteria (0 = mai) ---
// Sotto questa tensione, per CONFERME misure di fila, la scheda va in
// sonno profondo per SONNO_MINUTI e poi rimisura.
#define TENSIONE_SONNO_V  11.80f
#define SONNO_MINUTI      60

// --- Pagina web nella rete locale ---
// true: si collega al Wi-Fi indicato in segreti.h e mostra i dati
// all'indirizzo che stampa sulla seriale. false: solo seriale.
#define USA_WIFI  true
