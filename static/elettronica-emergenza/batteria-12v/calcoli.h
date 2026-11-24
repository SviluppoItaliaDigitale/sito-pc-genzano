// Calcoli del controllo batteria 12 V: partitore, mediana, stima della carica.
// Funzioni pure, senza hardware: si provano anche sul computer.
// Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
// https://www.protezionecivilegenzano.it/elettronica-emergenza/batteria-12v/
// Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).
#pragma once
#include <stdint.h>

// Tensione della batteria in volt dalla tensione sul pin in millivolt.
// Partitore: r_alta fra il positivo e il pin, r_bassa fra il pin e GND.
static inline float tensioneBatteria(float mv_pin, float r_alta, float r_bassa, float correzione) {
  return (mv_pin / 1000.0f) * ((r_alta + r_bassa) / r_bassa) * correzione;
}

// Mediana di n valori (n <= 64). Ordina una copia, non tocca l'originale.
static inline int32_t mediana(const int32_t *v, int n) {
  int32_t c[64];
  if (n <= 0) return 0;
  if (n > 64) n = 64;
  for (int i = 0; i < n; i++) c[i] = v[i];
  for (int i = 1; i < n; i++) {
    int32_t x = c[i];
    int j = i - 1;
    while (j >= 0 && c[j] > x) { c[j + 1] = c[j]; j--; }
    c[j + 1] = x;
  }
  return c[n / 2];
}

// Tabella tensione a vuoto (a riposo) -> carica di una batteria al piombo da 12 V.
// Fonte: Trojan Battery Company, pagina «Battery maintenance», tabella dello
// stato di carica, colonna 12 V (verificata il 24/11/2026). Vale solo a riposo:
// batteria senza carica ne' scarica da almeno 6 ore, meglio 24, carichi staccati.
static const float TAB_VOLT[10]  = {11.51f, 11.66f, 11.81f, 11.89f, 12.10f, 12.27f, 12.37f, 12.50f, 12.62f, 12.73f};
static const float TAB_CARICA[10] = {10.0f, 20.0f, 30.0f, 40.0f, 50.0f, 60.0f, 70.0f, 80.0f, 90.0f, 100.0f};

// Stima della carica in percentuale, interpolando la tabella.
// Restituisce -1 sotto il primo valore (meno del 10%) e 101 sopra l'ultimo
// (oltre la tabella: batteria piena oppure in carica).
static inline float stimaCarica(float volt) {
  if (volt < TAB_VOLT[0]) return -1.0f;
  if (volt > TAB_VOLT[9]) return 101.0f;
  for (int i = 0; i < 9; i++) {
    if (volt <= TAB_VOLT[i + 1]) {
      float f = (volt - TAB_VOLT[i]) / (TAB_VOLT[i + 1] - TAB_VOLT[i]);
      return TAB_CARICA[i] + f * (TAB_CARICA[i + 1] - TAB_CARICA[i]);
    }
  }
  return 101.0f;
}

// Soglia con conferma e isteresi.
// Lo stato passa a «bassa» dopo `conferme` misure di fila sotto la soglia,
// e torna normale solo sopra soglia + isteresi.
struct StatoSoglia {
  bool bassa;
  int sotto;
};

// Restituisce true se lo stato e' cambiato con questa misura.
static inline bool aggiornaSoglia(StatoSoglia *s, float volt, float soglia, float isteresi, int conferme) {
  if (soglia <= 0.0f) return false;
  if (!s->bassa) {
    if (volt < soglia) {
      s->sotto++;
      if (s->sotto >= conferme) { s->bassa = true; s->sotto = 0; return true; }
    } else {
      s->sotto = 0;
    }
  } else if (volt >= soglia + isteresi) {
    s->bassa = false;
    s->sotto = 0;
    return true;
  }
  return false;
}
