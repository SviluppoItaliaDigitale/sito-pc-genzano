#!/bin/bash
# ============================================================
# INSTALLA STRUMENTI DI GESTIONE SITO
# Esegui con: bash installa-strumenti.sh
# ============================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "📦 Installazione strumenti di gestione..."

# Copia gli script nella home
cp "$SCRIPT_DIR/modifica-pagina.sh" ~/modifica-pagina.sh 2>/dev/null || true
cp "$SCRIPT_DIR/gestione-sito.sh" ~/gestione-sito.sh 2>/dev/null || true

chmod +x ~/modifica-pagina.sh 2>/dev/null || true
chmod +x ~/gestione-sito.sh 2>/dev/null || true
chmod +x ~/pubblica-notizia.sh 2>/dev/null || true
chmod +x ~/pubblica-da-word.sh 2>/dev/null || true

echo ""
echo "============================================"
echo "  ✅ STRUMENTI INSTALLATI!"
echo "============================================"
echo ""
echo "  COMANDO PRINCIPALE (menu completo):"
echo "  bash ~/gestione-sito.sh"
echo ""
echo "  COMANDI SINGOLI:"
echo "  bash ~/pubblica-notizia.sh    → Nuova notizia"
echo "  bash ~/pubblica-da-word.sh    → Notizia da Word"
echo "  bash ~/modifica-pagina.sh     → Modifica pagina"
echo ""
echo "  💡 CONSIGLIO: Per avere il comando sempre"
echo "  a portata di mano, aggiungi al desktop:"
echo "  Tasto destro Desktop → Crea collegamento"
echo "============================================"
