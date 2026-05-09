#!/usr/bin/env bash
# Wrapper avvio Claude Code sul progetto Sito PC Genzano.
# Usato da:
#   - icona desktop ~/Scrivania/Claude-PC-Genzano.desktop
#   - voce 25 del menu di ~/gestione-sito.sh
# Da terminale c'è anche l'alias `claude-protezionecivile` in ~/.bashrc.

cd "$HOME/sito-pc-genzano" || exit 1
exec claude
