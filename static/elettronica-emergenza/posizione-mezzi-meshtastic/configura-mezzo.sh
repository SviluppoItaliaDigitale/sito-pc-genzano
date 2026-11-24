#!/usr/bin/env bash
# Configura il nodo Meshtastic con GPS di un mezzo: invia la posizione sul
# canale privato SQUADRA creato con configura-primo-nodo.sh.
# Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
# https://www.protezionecivilegenzano.it/elettronica-emergenza/posizione-mezzi-meshtastic/
# Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).
#
# Uso:   bash configura-mezzo.sh "PC Genzano Mezzo 01" M01 [porta]
# Esempio con la porta: bash configura-mezzo.sh "PC Genzano Mezzo 01" M01 /dev/ttyUSB0
#
# Prima: antenna LoRa avvitata, radio collegata con il cavo USB, programma
# "meshtastic" installato (pip3 install --upgrade "meshtastic[cli]").
# L'indirizzo dei canali (dal QR del primo nodo) si scrive quando lo chiede
# lo script: non resta in nessun file ne' nella cronologia.
set -euo pipefail

NOME_LUNGO="${1:-}"
NOME_BREVE="${2:-}"
PORTA="${3:-}"

# --- Impostazioni della posizione (modificabili) ---
# Precisione sul canale SQUADRA, in bit: 32 = piena; 18 = circa 91 m;
# 17 = circa 182 m; 16 = circa 364 m (tabella della documentazione Meshtastic).
# Usa la precisione minima che serve al servizio.
PRECISIONE_SQUADRA=18
INDICE_SQUADRA=1             # SQUADRA e' il secondo canale (indice 1)
INTERVALLO_FISSO_S=900       # posizione almeno ogni 15 minuti
DISTANZA_MINIMA_M=200        # invio "intelligente": dopo 200 m di strada...
INTERVALLO_MINIMO_S=120      # ...ma non piu' spesso di ogni 2 minuti
AGGIORNAMENTO_GPS_S=60       # lettura del GPS ogni minuto

if [[ -z "$NOME_LUNGO" || -z "$NOME_BREVE" ]]; then
  echo "Uso: bash configura-mezzo.sh \"PC Genzano Mezzo 01\" M01 [porta]" >&2
  exit 2
fi
if (( ${#NOME_BREVE} > 4 )); then
  echo "Il nome breve ha al massimo 4 caratteri." >&2
  exit 2
fi
if ! [[ "$PRECISIONE_SQUADRA" =~ ^[0-9]+$ ]] || (( PRECISIONE_SQUADRA < 1 || PRECISIONE_SQUADRA > 32 )); then
  echo "PRECISIONE_SQUADRA va da 1 a 32." >&2
  exit 2
fi
if ! command -v meshtastic >/dev/null 2>&1; then
  echo "Manca il programma meshtastic: pip3 install --upgrade \"meshtastic[cli]\"" >&2
  exit 1
fi

M=(meshtastic)
if [[ -n "$PORTA" ]]; then M+=(--port "$PORTA"); fi

echo "Il nome e' quello del mezzo, mai dell'autista: lo vede tutta la rete."
read -r -p "Antenna LoRa collegata? Scrivi si per continuare: " risposta
if [[ "$risposta" != "si" ]]; then
  echo "Collega l'antenna prima di accendere la radio in trasmissione." >&2
  exit 1
fi
read -r -s -p "Incolla l'indirizzo dei canali (non viene mostrato): " INDIRIZZO
echo
if [[ "$INDIRIZZO" != https://meshtastic.org/e/* && "$INDIRIZZO" != https://www.meshtastic.org/e/* ]]; then
  echo "L'indirizzo non sembra quello di un canale Meshtastic." >&2
  exit 1
fi

# 1. Canali e impostazioni radio del primo nodo.
"${M[@]}" --seturl "$INDIRIZZO"
unset INDIRIZZO
sleep 8
# 2. Regione europea, limite del tempo in aria, ruolo TRACKER, niente risparmio
#    energetico (il nodo e' alimentato dal mezzo), MQTT e mappa pubblica spenti.
"${M[@]}" --set lora.region EU_868 --set lora.override_duty_cycle false \
          --set device.role TRACKER --set power.is_power_saving false \
          --set mqtt.enabled false --set mqtt.map_reporting_enabled false \
          --set-owner "$NOME_LUNGO" --set-owner-short "$NOME_BREVE"
sleep 8
# 3. GPS acceso e intervalli di invio della posizione.
"${M[@]}" --set position.gps_mode ENABLED --set position.fixed_position false \
          --set position.gps_update_interval "$AGGIORNAMENTO_GPS_S" \
          --set position.position_broadcast_secs "$INTERVALLO_FISSO_S" \
          --set position.position_broadcast_smart_enabled true \
          --set position.broadcast_smart_minimum_distance "$DISTANZA_MINIMA_M" \
          --set position.broadcast_smart_minimum_interval_secs "$INTERVALLO_MINIMO_S"
sleep 8
# 4. Canale pubblico: nessuna posizione, nessun passaggio verso internet.
"${M[@]}" --ch-set module_settings.position_precision 0 \
          --ch-set uplink_enabled false --ch-set downlink_enabled false --ch-index 0
sleep 8
# 5. Canale SQUADRA: posizione con la precisione scelta, nessun passaggio verso internet.
"${M[@]}" --ch-set module_settings.position_precision "$PRECISIONE_SQUADRA" \
          --ch-set uplink_enabled false --ch-set downlink_enabled false --ch-index "$INDICE_SQUADRA"
sleep 8

echo
echo "Controlla qui sotto: regione EU_868, ruolo TRACKER, MQTT spento,"
echo "e che il canale con indice $INDICE_SQUADRA sia SQUADRA."
"${M[@]}" --info | grep -iE "region|role|overrideDutyCycle|\"enabled\"|mapReporting|Index|name" || true
echo
echo "Fatto. Usa la posizione solo durante il servizio; a fine servizio"
echo "spegni il nodo oppure esegui: bash posizione.sh spegni"
