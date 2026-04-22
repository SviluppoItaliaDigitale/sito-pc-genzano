#!/bin/bash
# ══════════════════════════════════════════════════════════════════════════════
#   export-contesto-ai.sh
#   Genera un file unico CONTESTO-AI.md con tutta la documentazione del sito,
#   pronto da incollare in qualsiasi AI esterna (ChatGPT, Gemini, Claude web,
#   Mistral, ecc.) per continuare la gestione senza perdere contesto.
#
#   Uso: bash scripts/export-contesto-ai.sh
#   Output: CONTESTO-AI.md nella root del progetto
# ══════════════════════════════════════════════════════════════════════════════

set -e

# Trova la root del progetto (directory che contiene hugo.toml)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

OUTPUT="CONTESTO-AI.md"
DATA_NOW="$(date '+%Y-%m-%d %H:%M:%S %Z')"
GIT_COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo 'sconosciuto')"
GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'sconosciuto')"

# ── Intestazione ─────────────────────────────────────────────────────────────
cat > "$OUTPUT" <<EOF
# CONTESTO-AI — Sito Protezione Civile Genzano di Roma

> **File generato automaticamente da \`scripts/export-contesto-ai.sh\`.**
> Non modificare manualmente: rigenera con lo script.

**Generato il:** $DATA_NOW
**Commit corrente:** \`$GIT_COMMIT\` (branch \`$GIT_BRANCH\`)
**Repository:** https://github.com/SviluppoItaliaDigitale/sito-pc-genzano
**Sito pubblico:** https://www.protezionecivilegenzano.it/

---

## Come usare questo file

Questo file contiene **TUTTA** la documentazione necessaria per gestire il sito
della Protezione Civile di Genzano di Roma con una qualsiasi AI (ChatGPT,
Gemini, Claude web, Mistral, altre sessioni di Claude Code, ecc.).

**Procedura:**

1. Copia l'intero contenuto di questo file.
2. Incollalo come primo messaggio (o allegato) nella nuova sessione AI.
3. Aggiungi: *"Sei un assistente specializzato nella gestione di questo sito.
   Leggi la documentazione qui sopra e agisci secondo le regole descritte."*
4. L'AI avrà tutto il contesto per operare.

**Copertura di questo file:**
- Istruzioni generali (\`CLAUDE.md\`)
- 6 regole di governance (\`.claude/rules/\`)
- Manuale operativo completo (\`MANUALE-SITO.md\`)
- Piano editoriale con fonti e calendario (\`PIANO-EDITORIALE.md\`)
- README del progetto
- Template articoli (\`archetypes/comunicazioni.md\`)
- Configurazione Hugo (\`hugo.toml\`)
- Shortcode custom (\`foto.html\`)
- Memorie utente (feedback durevoli)

---

## Indice

1. [README — Panoramica del progetto](#1-readme--panoramica-del-progetto)
2. [CLAUDE.md — Istruzioni principali](#2-claudemd--istruzioni-principali)
3. [Regole di governance (6 file)](#3-regole-di-governance-6-file)
   - 3.1 [Governance PA](#31-01-governance-pamd)
   - 3.2 [Content Design PA](#32-02-content-design-pamd)
   - 3.3 [Accessibilità](#33-03-accessibilitymd)
   - 3.4 [Hugo Architecture](#34-04-hugo-architecturemd)
   - 3.5 [GitHub + Aruba Deploy](#35-05-github-aruba-deploymd)
   - 3.6 [Protezione Civile scientifica](#36-06-protezione-civile-scientificamd)
4. [MANUALE-SITO — Manuale operativo completo](#4-manuale-sito--manuale-operativo-completo)
5. [PIANO-EDITORIALE — Fonti e calendario](#5-piano-editoriale--fonti-e-calendario)
6. [Archetype articoli (\`archetypes/comunicazioni.md\`)](#6-archetype-articoli)
7. [Configurazione Hugo (\`hugo.toml\`)](#7-configurazione-hugo)
8. [Shortcode \`foto\` (\`themes/.../shortcodes/foto.html\`)](#8-shortcode-foto)
9. [Memorie utente (feedback durevoli)](#9-memorie-utente-feedback-durevoli)

---

EOF

# ── Helper: includi un file con intestazione e separatore ───────────────────
include_file() {
    local file_path="$1"
    local section_title="$2"
    local code_fence="${3:-}"

    if [ ! -f "$file_path" ]; then
        echo -e "\n## $section_title\n\n> FILE NON TROVATO: \`$file_path\`\n" >> "$OUTPUT"
        return
    fi

    {
        echo ""
        echo "## $section_title"
        echo ""
        echo "**Percorso:** \`$file_path\`"
        echo "**Dimensione:** $(wc -c < "$file_path" | tr -d ' ') byte · $(wc -l < "$file_path" | tr -d ' ') righe"
        echo ""

        if [ -n "$code_fence" ]; then
            echo "\`\`\`$code_fence"
            cat "$file_path"
            echo ""
            echo "\`\`\`"
        else
            cat "$file_path"
        fi

        echo ""
        echo "---"
        echo ""
    } >> "$OUTPUT"
}

# ── 1. README ───────────────────────────────────────────────────────────────
include_file "README.md" "1. README — Panoramica del progetto"

# ── 2. CLAUDE.md ────────────────────────────────────────────────────────────
include_file "CLAUDE.md" "2. CLAUDE.md — Istruzioni principali"

# ── 3. Regole di governance ─────────────────────────────────────────────────
echo -e "\n## 3. Regole di governance (6 file)\n\nQuesti 6 file sono importati automaticamente da CLAUDE.md e definiscono le regole operative per dominio.\n\n---\n" >> "$OUTPUT"

include_file ".claude/rules/01-governance-pa.md" "3.1 01-governance-pa.md"
include_file ".claude/rules/02-content-design-pa.md" "3.2 02-content-design-pa.md"
include_file ".claude/rules/03-accessibility.md" "3.3 03-accessibility.md"
include_file ".claude/rules/04-hugo-architecture.md" "3.4 04-hugo-architecture.md"
include_file ".claude/rules/05-github-aruba-deploy.md" "3.5 05-github-aruba-deploy.md"
include_file ".claude/rules/06-protezione-civile-scientifica.md" "3.6 06-protezione-civile-scientifica.md"

# ── 4. MANUALE-SITO ──────────────────────────────────────────────────────────
include_file "MANUALE-SITO.md" "4. MANUALE-SITO — Manuale operativo completo"

# ── 5. PIANO-EDITORIALE ──────────────────────────────────────────────────────
include_file "PIANO-EDITORIALE.md" "5. PIANO-EDITORIALE — Fonti e calendario"

# ── 6. Archetype articoli ────────────────────────────────────────────────────
include_file "archetypes/comunicazioni.md" "6. Archetype articoli" "markdown"

# ── 7. hugo.toml ─────────────────────────────────────────────────────────────
include_file "hugo.toml" "7. Configurazione Hugo" "toml"

# ── 8. Shortcode foto ────────────────────────────────────────────────────────
include_file "themes/flavour-pcgenzano/layouts/shortcodes/foto.html" "8. Shortcode foto" "go-html-template"

# ── 9. Memorie utente (feedback durevoli) ────────────────────────────────────
MEMORY_DIR="$HOME/.claude/projects/-home-iu0qvw-sito-pc-genzano/memory"
{
    echo ""
    echo "## 9. Memorie utente (feedback durevoli)"
    echo ""
    echo "Queste sono le regole che l'utente ha esplicitamente chiesto di ricordare tra sessioni. Ogni altra AI deve rispettarle come parte del contratto operativo."
    echo ""
    echo "**Percorso originale (solo su macchina dell'utente):** \`$MEMORY_DIR\`"
    echo ""
    echo "---"
    echo ""
} >> "$OUTPUT"

if [ -d "$MEMORY_DIR" ]; then
    # Includi MEMORY.md (indice)
    if [ -f "$MEMORY_DIR/MEMORY.md" ]; then
        {
            echo "### 9.0 Indice memorie (MEMORY.md)"
            echo ""
            cat "$MEMORY_DIR/MEMORY.md"
            echo ""
            echo "---"
            echo ""
        } >> "$OUTPUT"
    fi

    # Includi ogni feedback_*.md
    idx=1
    for mem_file in "$MEMORY_DIR"/feedback_*.md; do
        [ -f "$mem_file" ] || continue
        mem_name="$(basename "$mem_file")"
        {
            echo "### 9.$idx $mem_name"
            echo ""
            echo "\`\`\`markdown"
            cat "$mem_file"
            echo ""
            echo "\`\`\`"
            echo ""
            echo "---"
            echo ""
        } >> "$OUTPUT"
        idx=$((idx + 1))
    done
else
    echo -e "\n> Directory memorie non trovata in questo ambiente: \`$MEMORY_DIR\`\n" >> "$OUTPUT"
fi

# ── Riepilogo finale ─────────────────────────────────────────────────────────
SIZE_BYTES=$(wc -c < "$OUTPUT" | tr -d ' ')
SIZE_KB=$((SIZE_BYTES / 1024))
LINES=$(wc -l < "$OUTPUT" | tr -d ' ')

{
    echo ""
    echo "---"
    echo ""
    echo "## Fine del contesto"
    echo ""
    echo "**Totale questo file:** $LINES righe · ${SIZE_KB} KB"
    echo "**Generato il:** $DATA_NOW"
    echo "**Commit sorgente:** \`$GIT_COMMIT\` su branch \`$GIT_BRANCH\`"
    echo ""
    echo "Per rigenerare questo file con lo stato attuale del repository:"
    echo ""
    echo "\`\`\`bash"
    echo "bash scripts/export-contesto-ai.sh"
    echo "\`\`\`"
} >> "$OUTPUT"

# ── Output a terminale ───────────────────────────────────────────────────────
echo ""
echo "✓ File generato: $PROJECT_ROOT/$OUTPUT"
echo "  Dimensione:   ${SIZE_KB} KB ($SIZE_BYTES byte)"
echo "  Righe:        $LINES"
echo "  Commit:       $GIT_COMMIT ($GIT_BRANCH)"
echo ""
echo "Prossimi passi:"
echo "  1. Apri $OUTPUT"
echo "  2. Copia tutto il contenuto"
echo "  3. Incollalo come primo messaggio nell'altra AI"
echo ""
