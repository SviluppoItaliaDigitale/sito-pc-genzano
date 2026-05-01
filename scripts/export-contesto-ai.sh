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
- 11 regole di governance (\`.claude/rules/\` — 01-08 incluse 04a/b/c)
- Manuale operativo completo (\`MANUALE-SITO.md\` indice + 18 file \`manuale/parte-NN.md\`)
- Piano editoriale con fonti e calendario (\`PIANO-EDITORIALE.md\`)
- README del progetto
- Template articoli (\`archetypes/comunicazioni.md\`)
- Configurazione Hugo (\`hugo.toml\`)
- Shortcode custom (\`foto.html\`)
- Data files chiave (\`numeri_utili.yaml\`, \`emergenza.json\`, \`allerta.json\`)
- Workflow GitHub Actions principali (deploy, audit-sito 38 sezioni, smoke-test)
- Script di automazione (\`smoke-test-live.sh\`, \`applica-fascia-foto.sh\`)
- Memorie utente (feedback + project — durevoli)

---

## Indice

1. [README — Panoramica del progetto](#1-readme--panoramica-del-progetto)
2. [CLAUDE.md — Istruzioni principali](#2-claudemd--istruzioni-principali)
3. [Regole di governance (11 file in \`.claude/rules/\`)](#3-regole-di-governance)
4. [MANUALE-SITO — Manuale operativo completo (split in 18 file)](#4-manuale-sito--manuale-operativo-completo-split-in-18-file)
5. [PIANO-EDITORIALE — Fonti e calendario](#5-piano-editoriale--fonti-e-calendario)
6. [Archetype articoli (\`archetypes/comunicazioni.md\`)](#6-archetype-articoli)
7. [Configurazione Hugo (\`hugo.toml\`)](#7-configurazione-hugo)
8. [Shortcode \`foto\` (\`themes/.../shortcodes/foto.html\`)](#8-shortcode-foto)
9. [Data files chiave (\`numeri_utili.yaml\`, \`emergenza.json\`)](#9-data-files-chiave)
10. [Workflow GitHub Actions principali](#10-workflow-github-actions-principali)
11. [Script di automazione](#11-script-di-automazione)
12. [Memorie utente (feedback + project)](#12-memorie-utente-feedback--project)

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
echo -e "\n## 3. Regole di governance\n\nQuesti file sono importati automaticamente da CLAUDE.md e definiscono le regole operative per dominio.\n\n---\n" >> "$OUTPUT"

include_file ".claude/rules/01-governance-pa.md" "3.1 01-governance-pa.md"
include_file ".claude/rules/02-content-design-pa.md" "3.2 02-content-design-pa.md"
include_file ".claude/rules/03-accessibility.md" "3.3 03-accessibility.md"
include_file ".claude/rules/04-hugo-architecture.md" "3.4 04-hugo-architecture.md"
include_file ".claude/rules/04a-hugo-shortcode-partial.md" "3.5 04a-hugo-shortcode-partial.md"
include_file ".claude/rules/04b-hugo-template-css.md" "3.6 04b-hugo-template-css.md"
include_file ".claude/rules/04c-hugo-static-cartelle.md" "3.7 04c-hugo-static-cartelle.md"
include_file ".claude/rules/05-github-aruba-deploy.md" "3.8 05-github-aruba-deploy.md"
include_file ".claude/rules/06-protezione-civile-scientifica.md" "3.9 06-protezione-civile-scientifica.md"
include_file ".claude/rules/07-proattivita-coerenza.md" "3.10 07-proattivita-coerenza.md"
include_file ".claude/rules/08-claude-code-setup.md" "3.11 08-claude-code-setup.md"

# ── 4. MANUALE-SITO (indice + 18 parti) ──────────────────────────────────────
echo -e "\n## 4. MANUALE-SITO — Manuale operativo completo (split in 18 file)\n\nIl manuale operativo è stato spezzato a maggio 2026 in 18 file separati nella cartella \`manuale/\` (1 file per Parte) per facilitare manutenzione e revisioni puntuali. \`MANUALE-SITO.md\` nella root resta come indice/redirect.\n\n---\n" >> "$OUTPUT"
include_file "MANUALE-SITO.md" "4.0 MANUALE-SITO.md (indice)"
include_file "manuale/README.md" "4.1 manuale/README.md (indice navigabile)"
# Includi tutte le 18 parti nell'ordine
sub_idx=2
for parte_file in $(ls manuale/parte-*.md 2>/dev/null | sort); do
    parte_name="$(basename "$parte_file" .md)"
    include_file "$parte_file" "4.$sub_idx ${parte_name}"
    sub_idx=$((sub_idx + 1))
done

# ── 5. PIANO-EDITORIALE ──────────────────────────────────────────────────────
include_file "PIANO-EDITORIALE.md" "5. PIANO-EDITORIALE — Fonti e calendario"

# ── 6. Archetype articoli ────────────────────────────────────────────────────
include_file "archetypes/comunicazioni.md" "6. Archetype articoli" "markdown"

# ── 7. hugo.toml ─────────────────────────────────────────────────────────────
include_file "hugo.toml" "7. Configurazione Hugo" "toml"

# ── 8. Shortcode foto ────────────────────────────────────────────────────────
include_file "themes/flavour-pcgenzano/layouts/shortcodes/foto.html" "8. Shortcode foto" "go-html-template"

# ── 9. Data files chiave ─────────────────────────────────────────────────────
echo -e "\n## 9. Data files chiave\n\nFile sotto \`data/\` che alimentano il rendering. Le modifiche qui sono il modo principale per aggiornare contenuti dinamici senza toccare i template.\n\n---\n" >> "$OUTPUT"
include_file "data/numeri_utili.yaml" "9.1 numeri_utili.yaml" "yaml"
include_file "data/emergenza.json" "9.2 emergenza.json" "json"
include_file "data/allerta.json" "9.3 allerta.json (esempio struttura)" "json"

# ── 10. Workflow GitHub Actions ──────────────────────────────────────────────
echo -e "\n## 10. Workflow GitHub Actions principali\n\nIl sito ha 9 workflow attivi. Includiamo i 3 più importanti per dare contesto all'AI: deploy, audit completo (38 sezioni), smoke test post-deploy. Gli altri 6 sono descritti in CLAUDE.md sezione 'Automazioni periodiche'.\n\n---\n" >> "$OUTPUT"
include_file ".github/workflows/deploy.yml" "10.1 deploy.yml — build + Aruba + GitHub Pages" "yaml"
include_file ".github/workflows/audit-sito.yml" "10.2 audit-sito.yml — 38 sezioni di audit completo (lun 09:00)" "yaml"
include_file ".github/workflows/smoke-test-post-deploy.yml" "10.3 smoke-test-post-deploy.yml — verifica live post-deploy" "yaml"

# ── 11. Script di automazione ────────────────────────────────────────────────
echo -e "\n## 11. Script di automazione\n\nScript in \`scripts/\` che l'AI può consigliare all'utente di lanciare in caso di bisogno.\n\n---\n" >> "$OUTPUT"
include_file "scripts/smoke-test-live.sh" "11.1 smoke-test-live.sh — smoke test del sito live (50+ controlli)" "bash"
include_file "scripts/applica-fascia-foto.sh" "11.2 applica-fascia-foto.sh — fascia blu istituzionale per foto utente" "bash"

# ── 12. Memorie utente (feedback durevoli + project) ─────────────────────────
MEMORY_DIR="$HOME/.claude/projects/-home-iu0qvw-sito-pc-genzano/memory"
{
    echo ""
    echo "## 12. Memorie utente (feedback + project)"
    echo ""
    echo "Queste sono le regole che l'utente ha esplicitamente chiesto di ricordare tra sessioni. Ogni altra AI deve rispettarle come parte del contratto operativo. Sono divise in:"
    echo "- **feedback_*.md** — guidance comportamentale (cosa fare/non fare)"
    echo "- **project_*.md** — fatti specifici sul progetto (es. COI 15°, IRC solo link)"
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
            echo "### 12.0 Indice memorie (MEMORY.md)"
            echo ""
            cat "$MEMORY_DIR/MEMORY.md"
            echo ""
            echo "---"
            echo ""
        } >> "$OUTPUT"
    fi

    # Includi ogni feedback_*.md e project_*.md (ordinati alfabeticamente)
    idx=1
    for mem_file in $(ls "$MEMORY_DIR"/feedback_*.md "$MEMORY_DIR"/project_*.md 2>/dev/null | sort); do
        [ -f "$mem_file" ] || continue
        mem_name="$(basename "$mem_file")"
        {
            echo "### 12.$idx $mem_name"
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
