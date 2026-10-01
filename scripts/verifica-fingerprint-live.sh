#!/usr/bin/env bash
# Guardia anti-stale del sito su Aruba — involucro di compatibilità.
#
# Dal 01/10/2026 il controllo è in scripts/verifica-deploy-aruba.py: confronta
# le pagine servite con /build-manifest.json (impronta sha256 di ogni file
# della build) invece di leggere la meta pc-build-sha, che non esiste più.
# Questo file resta perché agenti, routine e documentazione lo chiamano con
# le opzioni di prima (--base, --sha, --retries, --wait, --stale-hours,
# --diagnostica): le passa tali e quali, lo script Python le riconosce.
exec python3 "$(dirname "$0")/verifica-deploy-aruba.py" "$@"
