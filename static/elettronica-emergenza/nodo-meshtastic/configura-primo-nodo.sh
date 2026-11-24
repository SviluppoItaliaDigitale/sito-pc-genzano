#!/usr/bin/env bash
# Configura il PRIMO nodo Meshtastic della squadra e crea il canale privato.
# Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
# https://www.protezionecivilegenzano.it/elettronica-emergenza/nodo-meshtastic/
# Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).
#
# Uso:   bash configura-primo-nodo.sh "PC Genzano 01" PC01 [porta]
# Esempio con la porta: bash configura-primo-nodo.sh "PC Genzano 01" PC01 /dev/ttyUSB0
#
# Prima: antenna avvitata, radio collegata con il cavo USB, programma
# "meshtastic" installato (pip3 install --upgrade "meshtastic[cli]").
# Lo script non scrive mai la chiave del canale su disco.
set -euo pipefail

NOME_LUNGO="${1:-}"
NOME_BREVE="${2:-}"
PORTA="${3:-}"
NOME_CANALE="SQUADRA"

if [[ -z "$NOME_LUNGO" || -z "$NOME_BREVE" ]]; then
  echo "Uso: bash configura-primo-nodo.sh \"PC Genzano 01\" PC01 [porta]" >&2
  exit 2
fi
if (( ${#NOME_BREVE} > 4 )); then
  echo "Il nome breve ha al massimo 4 caratteri." >&2
  exit 2
fi
if ! command -v meshtastic >/dev/null 2>&1; then
  echo "Manca il programma meshtastic: pip3 install --upgrade \"meshtastic[cli]\"" >&2
  exit 1
fi

M=(meshtastic)
if [[ -n "$PORTA" ]]; then M+=(--port "$PORTA"); fi

echo "Usa nomi di servizio, mai nome e cognome: li vede tutta la rete."
read -r -p "Antenna collegata? Scrivi si per continuare: " risposta
if [[ "$risposta" != "si" ]]; then
  echo "Collega l'antenna prima di accendere la radio in trasmissione." >&2
  exit 1
fi

# 1. Regione europea 868 MHz, preset della rete locale, limite del tempo in aria attivo.
"${M[@]}" --set lora.region EU_868 --set lora.modem_preset LONG_FAST \
          --set lora.hop_limit 3 --set lora.override_duty_cycle false
sleep 8
# 2. Ruolo e nomi del nodo, MQTT spento (i messaggi restano sulla radio).
"${M[@]}" --set device.role CLIENT --set mqtt.enabled false \
          --set-owner "$NOME_LUNGO" --set-owner-short "$NOME_BREVE"
sleep 8
# 3. Canale primario pubblico: nessuna posizione inviata.
"${M[@]}" --ch-set module_settings.position_precision 0 --ch-index 0
sleep 8
# 4. Canale della squadra con chiave casuale a 256 bit.
"${M[@]}" --ch-add "$NOME_CANALE"
sleep 8
"${M[@]}" --ch-set psk random --ch-index 1
sleep 8

echo
echo "Fatto. Ora mostra il codice QR dei canali e fallo inquadrare di persona"
echo "dagli altri volontari. Non fotografarlo, non mandarlo in chat o per email:"
echo "contiene la chiave del canale."
echo
"${M[@]}" --qr-all
