#!/usr/bin/env bash
# Spegne o riaccende l'invio della posizione del nodo di un mezzo.
# Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
# https://www.protezionecivilegenzano.it/elettronica-emergenza/posizione-mezzi-meshtastic/
# Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).
#
# Uso:   bash posizione.sh spegni  [porta]   fuori servizio: GPS spento, nessuna posizione
#        bash posizione.sh accendi [porta]   in servizio: GPS acceso, posizione sul canale SQUADRA
set -euo pipefail

AZIONE="${1:-}"
PORTA="${2:-}"
PRECISIONE_SQUADRA=18   # la stessa di configura-mezzo.sh
INDICE_SQUADRA=1

if ! command -v meshtastic >/dev/null 2>&1; then
  echo "Manca il programma meshtastic: pip3 install --upgrade \"meshtastic[cli]\"" >&2
  exit 1
fi
M=(meshtastic)
if [[ -n "$PORTA" ]]; then M+=(--port "$PORTA"); fi

case "$AZIONE" in
  spegni)
    "${M[@]}" --ch-set module_settings.position_precision 0 --ch-index "$INDICE_SQUADRA"
    sleep 8
    "${M[@]}" --set position.gps_mode DISABLED
    echo "Posizione spenta: il nodo non invia piu' dove si trova il mezzo."
    ;;
  accendi)
    "${M[@]}" --set position.gps_mode ENABLED
    sleep 8
    "${M[@]}" --ch-set module_settings.position_precision "$PRECISIONE_SQUADRA" --ch-index "$INDICE_SQUADRA"
    echo "Posizione accesa sul canale SQUADRA, solo per la durata del servizio."
    ;;
  *)
    echo "Uso: bash posizione.sh spegni|accendi [porta]" >&2
    exit 2
    ;;
esac
