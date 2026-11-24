// Impostazioni del sensore del livello dell'acqua.
// Modifica solo questo file. Tutte le misure sono in centimetri.
// Pagina del progetto: https://www.protezionecivilegenzano.it/elettronica-emergenza/livello-acqua/
#pragma once

// --- Collegamenti (ESP32 classico, per esempio ESP32-DevKitC) ---
#define PIN_TRIG      25   // al pin Trig del modulo JSN-SR04T
#define PIN_ECHO      34   // al pin Echo del modulo (GPIO 34 e' solo ingresso: va bene)
#define PIN_LED       27   // LED con resistenza da 330 ohm verso GND
#define PIN_CICALINO  26   // ingresso del modulo cicalino attivo (con transistor)

// --- Taratura: DA MISURARE SUL POSTO, non lasciare 0 ---
// Distanza fra la faccia del sensore e il fondo del fosso o del sottopasso,
// misurata con un metro quando non c'e' acqua.
#define ALTEZZA_SENSORE_CM   0.0f
// Livello dell'acqua (dal fondo) oltre il quale il dispositivo segnala
// un'anomalia da verificare. Deciderlo con chi gestisce il luogo.
#define SOGLIA_LIVELLO_CM    0.0f
// Quanto deve scendere il livello sotto la soglia per considerarlo rientrato.
#define ISTERESI_CM          5.0f

// --- Limiti del sensore (scheda tecnica del JSN-SR04T versione 3.0) ---
// Sotto circa 20 cm il sensore non misura: montalo piu' in alto della soglia
// di almeno questa distanza.
#define DISTANZA_MIN_CM      21.0f
#define DISTANZA_MAX_CM      600.0f

// --- Misura ---
#define N_LETTURE            7      // letture per ogni misura (si usa la mediana)
#define LETTURE_VALIDE_MIN   4      // sotto questo numero la misura non vale
#define PAUSA_LETTURE_MS     70     // pausa fra due letture (almeno 60 ms)
// Velocita' del suono in cm al microsecondo a circa 20 gradi.
// Cambia con la temperatura: circa 0,6 m/s per grado.
#define VELOCITA_SUONO_CM_US 0.0343f

// --- Tempi ---
#define INTERVALLO_S          300   // fra due misure, in condizioni normali
#define INTERVALLO_ANOMALIA_S 60    // fra due misure, durante un'anomalia
#define NON_VALIDE_PER_GUASTO 3     // misure non valide di fila prima di "sensore da controllare"

// --- Segnali locali ---
#define CICALINO_ATTIVO      true   // false: solo LED, nessun suono
