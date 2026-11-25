// Impostazioni del pluviometro a bascula.
// Modifica solo questo file. Pagina del progetto:
// https://www.protezionecivilegenzano.it/elettronica-emergenza/pluviometro/
#pragma once

// --- Collegamenti (ESP32 classico, per esempio ESP32-DevKitC) ---
#define PIN_REED  27   // un filo del contatto reed; l'altro filo va a GND
#define PIN_LED   26   // LED con resistenza da 330 ohm verso GND

// --- Taratura: DA MISURARE, non lasciare 0 ---
// Millimetri di pioggia che corrispondono a un ribaltamento della bascula.
// Si ricava con la prova descritta nel file LEGGIMI.txt
// (acqua versata nota, area dell'imbuto misurata, ribaltamenti contati).
#define MM_PER_SCATTO  0.0f

// --- Antirimbalzo ---
// Un contatto reed chiude piu' volte in pochi millisecondi a ogni
// ribaltamento: gli impulsi piu' vicini di questo tempo si contano una volta.
#define ANTIRIMBALZO_MS  150

// --- Soglia facoltativa (0 = nessuna) ---
// Pioggia dell'ultima ora, in mm, oltre la quale il LED resta acceso:
// "pioggia intensa da verificare". Non e' un'allerta.
#define SOGLIA_MM_ORA    0.0f
#define ISTERESI_MM_ORA  2.0f

// --- Pagina web nella rete locale ---
// true: si collega al Wi-Fi indicato in segreti.h e mostra i dati
// all'indirizzo che stampa sulla seriale. false: solo seriale.
#define USA_WIFI  true
