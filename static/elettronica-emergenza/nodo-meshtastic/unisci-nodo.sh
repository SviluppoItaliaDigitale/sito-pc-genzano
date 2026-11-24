#!/usr/bin/env bash
# Configura un ALTRO nodo della squadra con i canali del primo nodo.
# Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
# https://www.protezionecivilegenzano.it/elettronica-emergenza/nodo-meshtastic/
# Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).
#
# Uso:   bash unisci-nodo.sh "PC Genzano 02" PC02 [ruolo] [porta]
# Ruolo: CLIENT (predefinito), CLIENT_MUTE (tante radio nello stesso posto),
#        CLIENT_BASE (stazione fissa in sede).
#
# L'indirizzo del canale (letto dal QR del primo nodo) si scrive quando lo
# chiede lo script e non resta in nessun file ne' nella cronologia.
set -euo pipefail

NOME_LUNGO="${1:-}"
NOME_BREVE="${2:-}"
RUOLO="${3:-CLIENT}"
PORTA="${4:-}"

if [[ -z "$NOME_LUNGO" || -z "$NOME_BREVE" ]]; then
  echo "Uso: bash unisci-nodo.sh \"PC Genzano 02\" PC02 [CLIENT|CLIENT_MUTE|CLIENT_BASE] [porta]" >&2
  exit 2
fi
case "$RUOLO" in
  CLIENT|CLIENT_MUTE|CLIENT_BASE) ;;
  *) echo "Ruolo non previsto: $RUOLO (usa CLIENT, CLIENT_MUTE o CLIENT_BASE)." >&2; exit 2 ;;
esac
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

read -r -p "Antenna collegata? Scrivi si per continuare: " risposta
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

# I canali e le impostazioni radio arrivano dall'indirizzo: sostituiscono quelli del nodo.
"${M[@]}" --seturl "$INDIRIZZO"
unset INDIRIZZO
sleep 8
# Regione e limite del tempo in aria ribaditi, poi ruolo, nomi e MQTT spento.
"${M[@]}" --set lora.region EU_868 --set lora.override_duty_cycle false \
          --set device.role "$RUOLO" --set mqtt.enabled false \
          --set-owner "$NOME_LUNGO" --set-owner-short "$NOME_BREVE"
sleep 8
"${M[@]}" --info | grep -iE "region|modemPreset|role|overrideDutyCycle" || true
echo "Fatto. Prova un messaggio sul canale SQUADRA con un altro nodo."
