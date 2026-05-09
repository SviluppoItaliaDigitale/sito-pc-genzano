#!/usr/bin/env bash
# Wrapper avvio Claude Code sul progetto Sito PC Genzano.
# Usato da:
#   - icona desktop ~/Scrivania/Claude-PC-Genzano.desktop
#   - voce 20 del menu di ~/gestione-sito.sh
# Da terminale c'è anche l'alias `claude-protezionecivile` in ~/.bashrc.

# Carica nvm: necessario perché GNOME lancia i file .desktop con environment
# pulito (no .bashrc), quindi il PATH di nvm va caricato esplicitamente
# altrimenti il binario `claude` (installato via nvm) non viene trovato.
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

cd "$HOME/sito-pc-genzano" || exit 1
exec claude
