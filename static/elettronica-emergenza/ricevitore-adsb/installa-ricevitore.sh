#!/usr/bin/env bash
# Installa il ricevitore ADS-B (solo ricezione) su un Raspberry Pi: scarica
# dalla fonte ufficiale lo script di installazione di readsb e tar1090, lo mostra e lo esegue.
# Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
# https://www.protezionecivilegenzano.it/elettronica-emergenza/ricevitore-adsb/
# Licenza di questo script: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).
#
# Uso:   bash installa-ricevitore.sh                 scarica, mostra e installa
#        bash installa-ricevitore.sh --solo-scarica  scarica e mostra, non installa
#
# I programmi installati sono di terzi e restano con le loro licenze:
#   readsb e tar1090 di wiedehopf (Matthias Wirth), GPL;
#   script di installazione adsb-scripts di wiedehopf, licenza MIT.
# Questo script non ne contiene il codice: lo scarica ogni volta dalla fonte.
# Non installa programmi che inviano i dati a servizi esterni e non imposta
# aggiornamenti automatici.
set -euo pipefail

FONTE="https://raw.githubusercontent.com/wiedehopf/adsb-scripts/master/readsb-install.sh"
PAGINA="https://github.com/wiedehopf/adsb-scripts/wiki/Automatic-installation-for-readsb"

SOLO_SCARICA=no
case "${1:-}" in
  "") ;;
  --solo-scarica) SOLO_SCARICA=si ;;
  *) echo "Uso: bash installa-ricevitore.sh [--solo-scarica]" >&2; exit 2 ;;
esac

if ! command -v apt-get >/dev/null 2>&1; then
  echo "Serve un sistema con apt, per esempio Raspberry Pi OS." >&2
  exit 1
fi
if command -v curl >/dev/null 2>&1; then
  scarica() { curl -fsSL -o "$2" "$1"; }
elif command -v wget >/dev/null 2>&1; then
  scarica() { wget -q -O "$2" "$1"; }
else
  echo "Manca curl o wget: sudo apt-get install -y curl" >&2
  exit 1
fi

CARTELLA="$(mktemp -d)"
trap 'rm -rf "$CARTELLA"' EXIT
FILE="$CARTELLA/readsb-install.sh"

echo "Scarico lo script ufficiale da:"
echo "  $FONTE"
if ! scarica "$FONTE" "$FILE"; then
  echo "Download non riuscito: controlla la rete e riprova." >&2
  exit 1
fi
if ! head -n 1 "$FILE" | grep -q '^#!/bin/bash'; then
  echo "Il file scaricato non sembra uno script: mi fermo." >&2
  exit 1
fi

echo
echo "Righe: $(wc -l < "$FILE")"
echo "Impronta SHA-256: $(sha256sum "$FILE" | cut -d' ' -f1)"
echo "Indirizzi internet scritti nello script:"
grep -oE 'https?://[A-Za-z0-9./_-]+' "$FILE" | sort -u | sed 's/^/  /'
echo
echo "Istruzioni dell'autore: $PAGINA"

if [[ "$SOLO_SCARICA" == si ]]; then
  cp "$FILE" ./readsb-install.sh
  echo
  echo "Copia salvata in ./readsb-install.sh: leggila prima di installare."
  exit 0
fi

echo
echo "Lo script installa readsb (decodifica) e tar1090 (mappa nel browser)"
echo "e toglie altri decodificatori gia' presenti: usa un Raspberry Pi dedicato."
read -r -p "Hai collegato la chiavetta RTL-SDR e vuoi installare? Scrivi si: " risposta
if [[ "$risposta" != "si" ]]; then
  echo "Installazione annullata."
  exit 0
fi

sudo bash "$FILE"

echo
echo "Posizione della sede (facoltativa): serve alla mappa per calcolare le distanze."
echo "Scrivi latitudine e longitudine in gradi decimali con il punto,"
echo "nel formato 41.12345 12.12345, oppure premi Invio per saltare."
read -r -p "Posizione: " lat lon || true
if [[ -n "${lat:-}" && -n "${lon:-}" ]]; then
  if [[ "$lat" =~ ^-?[0-9]{1,2}(\.[0-9]+)?$ && "$lon" =~ ^-?[0-9]{1,3}(\.[0-9]+)?$ ]]; then
    sudo readsb-set-location "$lat" "$lon"
  else
    echo "Formato non valido: la posizione non e' stata impostata."
    echo "Puoi farlo dopo con: sudo readsb-set-location LATITUDINE LONGITUDINE"
  fi
fi

IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
echo
echo "Fatto. Se e' il primo programma per SDR su questo Raspberry Pi, riavvia:"
echo "  sudo reboot"
echo "Poi apri da un computer della stessa rete:"
echo "  http://${IP:-INDIRIZZO-DEL-RASPBERRY}/tar1090"
echo
echo "I dati restano nella rete della sede. Non aprire la pagina su internet dal"
echo "router e non installare programmi di condivisione se non lo avete deciso."
