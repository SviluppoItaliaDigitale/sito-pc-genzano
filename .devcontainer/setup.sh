#!/usr/bin/env bash
# =============================================================================
# Setup ambiente di sviluppo — Sito Protezione Civile Genzano di Roma
# CONFIGURAZIONE TOTALE IN UN UNICO FILE — pensata per GitHub Codespaces
# (e riusabile su qualsiasi Ubuntu/Debian quando il PC locale fa i capricci).
# =============================================================================
# Cosa configura, da zero, in modo idempotente:
#   1. Pacchetti di sistema (pdftotext, font, liblouis Braille, hunspell)
#   2. Hugo extended 0.154.5 — IDENTICO alla produzione
#   3. Dipendenze Python degli script (pillow, segno, pyyaml, ecc.)
#   4. Claude Code CLI
#   5. ~120 skill globali (Everything Claude Code + Marketing + Document skills
#      ufficiali Anthropic + last30days) con le liste EXCLUDE/KEEP curate —
#      stessa identica dotazione del PC
#   6. 5 agent globali ECC (gli agent pc-* sono già nel repo, project-scoped)
#   7. MCP: firecrawl + playwright
#
# Lo richiama .devcontainer/devcontainer.json (postCreateCommand). A mano:
#     bash .devcontainer/setup.sh
#
# COME AVVIARE UN CODESPACE: su GitHub → pulsante "<> Code" → scheda
# "Codespaces" → "Create codespace on main". Parte da solo questo script.
#
# SEGRETI: qui dentro non ce ne sono. Per i servizi che li usano imposta i
# Codespaces secrets del repo (Settings → Secrets and variables → Codespaces):
#   FIRECRAWL_API_KEY  GEMINI_API_KEY  FTP_SERVER  FTP_USERNAME  FTP_PASSWORD
# =============================================================================
set -euo pipefail

# Versione di Hugo IDENTICA a .github/workflows/deploy.yml. NON cambiarla senza
# aggiornare anche il workflow: alcune feature del tema dipendono dalla versione
# esatta (.Fragments.Identifiers su 0.154, sintassi frontmatter "build:").
HUGO_VERSION="0.154.5"

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCES="$HOME/.claude/skill-sources"
SKILLS_DEST="$HOME/.claude/skills"
AGENTS_DEST="$HOME/.claude/agents"

azzurro() { printf '\n\033[1;34m▸ %s\033[0m\n' "$*"; }
ok()      { printf '  \033[0;32m✓\033[0m %s\n' "$*"; }
nota()    { printf '  \033[0;33m·\033[0m %s\n' "$*"; }
in_list() { case " $2 " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# -----------------------------------------------------------------------------
# 1. Pacchetti di sistema (apt)
# -----------------------------------------------------------------------------
azzurro "Pacchetti di sistema (apt)"
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y -qq \
  poppler-utils fonts-liberation python3-louis liblouis-data hunspell hunspell-it \
  >/dev/null
ok "poppler-utils, fonts-liberation, liblouis, hunspell-it"

# -----------------------------------------------------------------------------
# 2. Hugo extended (versione di produzione)
# -----------------------------------------------------------------------------
azzurro "Hugo extended ${HUGO_VERSION}"
if hugo version 2>/dev/null | grep -q "v${HUGO_VERSION}"; then
  ok "già presente"
else
  DEB="/tmp/hugo_extended_${HUGO_VERSION}_linux-amd64.deb"
  curl -sSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb" -o "$DEB"
  sudo dpkg -i "$DEB" >/dev/null 2>&1 || sudo apt-get install -f -y -qq >/dev/null
  rm -f "$DEB"
  ok "$(hugo version | head -1)"
fi

# -----------------------------------------------------------------------------
# 3. Dipendenze Python (pip)
# -----------------------------------------------------------------------------
azzurro "Dipendenze Python — core"
pip install --quiet --break-system-packages \
  pyyaml pillow segno beautifulsoup4 requests spylls python-pptx fonttools brotli
ok "pyyaml, pillow, segno, beautifulsoup4, requests, spylls, python-pptx"

# Dipendenze delle document skills ufficiali Anthropic (docx/xlsx/pptx/pdf).
# python-pptx/pillow sono già sopra; qui le restanti. markitdown[pptx] = estrazione testo.
azzurro "Dipendenze Python — document skills (docx/xlsx/pptx/pdf)"
pip install --quiet --break-system-packages \
  python-docx openpyxl pypdf pdfplumber pandas reportlab "markitdown[pptx]" defusedxml lxml \
  && ok "python-docx, openpyxl, pypdf, pdfplumber, pandas, reportlab, markitdown, defusedxml, lxml" \
  || nota "alcune dipendenze document-skills non installate (non bloccante)"

azzurro "Dipendenze Python — meteo (opzionali, best-effort)"
pip install --quiet --break-system-packages matplotlib numpy >/dev/null 2>&1 \
  && ok "matplotlib, numpy" || nota "matplotlib/numpy saltati (non bloccante)"
pip install --quiet --break-system-packages cartopy >/dev/null 2>&1 \
  && ok "cartopy" || nota "cartopy saltato (vuole libgeos/proj; le cartine girano in CI)"

# -----------------------------------------------------------------------------
# 4. Claude Code CLI
# -----------------------------------------------------------------------------
azzurro "Claude Code CLI"
export PATH="$HOME/.local/bin:$PATH"
if command -v claude >/dev/null 2>&1; then
  ok "già installato ($(claude --version 2>/dev/null | head -1))"
  # Porta all'ultima versione: senza questo il Codespace resta su una versione
  # vecchia (postCreateCommand non rigira agli avvii, vedi postStartCommand).
  claude update >/dev/null 2>&1 \
    && ok "aggiornato ($(claude --version 2>/dev/null | head -1))" \
    || nota "claude update non riuscito (non bloccante)"
else
  curl -fsSL https://claude.ai/install.sh | bash >/dev/null 2>&1 || true
  command -v claude >/dev/null 2>&1 \
    && ok "installato ($(claude --version 2>/dev/null | head -1))" \
    || nota "installer non riuscito — riprova: curl -fsSL https://claude.ai/install.sh | bash"
fi
grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"

# -----------------------------------------------------------------------------
# 5. Skill globali — Everything Claude Code (ECC) + Marketing
# -----------------------------------------------------------------------------
# Stessa dotazione del PC: di ECC si installano SOLO le skill (no hooks/rules
# globali), con la lista EXCLUDE delle skill fuori dominio (mobile native, DB,
# web framework non usati, ecc.); del marketing solo 6 skill (KEEP) a valore
# istituzionale. Le collisioni con le skill built-in del harness diventano
# "ecc-<nome>". Vedi memory feedback_skill_cleanup_conservativo / reference_ecc.
azzurro "Skill globali (ECC + Marketing)"
mkdir -p "$SOURCES" "$SKILLS_DEST" "$AGENTS_DEST"

clona() {  # clona <url> <dir>
  if [ -d "$SOURCES/$2/.git" ]; then
    git -C "$SOURCES/$2" pull --ff-only --quiet 2>/dev/null || true; ok "$2 aggiornato"
  else
    git clone --depth 1 "$1" "$SOURCES/$2" >/dev/null 2>&1 \
      && ok "$2 clonato" || nota "clone $2 fallito (rete?) — riprova: git clone $1 $SOURCES/$2"
  fi
}
clona "https://github.com/affaan-m/everything-claude-code.git" "everything-claude-code"
clona "https://github.com/coreyhaines31/marketingskills.git"   "marketingskills"

ECC="$SOURCES/everything-claude-code"
MKT="$SOURCES/marketingskills"

# Skill built-in del harness: se ECC ne ha una omonima, installala come ecc-<nome>.
BUILTIN="update-config keybindings-help simplify fewer-permission-prompts loop schedule claude-api init review security-review statusline-setup"

# Skill ECC fuori dominio per un sito PA Hugo/AGID — NON installate.
EXCLUDE="\
android-clean-architecture compose-multiplatform-patterns dart-flutter-patterns flutter-dart-code-review foundation-models-on-device ios-icon-gen \
kotlin-coroutines-flows kotlin-exposed-patterns kotlin-ktor-patterns kotlin-patterns kotlin-testing swift-actor-persistence swift-concurrency-6-2 \
swift-protocol-di-testing swiftui-patterns windows-desktop-e2e cpp-coding-standards cpp-testing csharp-testing dotnet-patterns fsharp-testing \
golang-patterns golang-testing jpa-patterns java-coding-standards perl-patterns perl-security perl-testing rust-patterns rust-testing tinystruct-patterns \
angular-developer bun-runtime django-celery django-patterns django-security django-tdd django-verification fastapi-patterns laravel-patterns \
laravel-plugin-discovery laravel-security laravel-tdd laravel-verification nestjs-patterns nextjs-turbopack nuxt4-patterns pytorch-patterns \
quarkus-patterns quarkus-security quarkus-tdd quarkus-verification springboot-patterns springboot-security springboot-tdd springboot-verification \
ui-to-vue vite-patterns clickhouse-io mysql-patterns postgres-patterns redis-patterns database-migrations cisco-ios-patterns homelab-network-readiness \
homelab-network-setup homelab-pihole-dns homelab-vlan-segmentation homelab-wireguard-vpn netmiko-ssh-automation network-bgp-diagnostics \
network-config-validation network-interface-health healthcare-cdss-patterns healthcare-emr-patterns healthcare-eval-harness healthcare-phi-compliance \
hipaa-compliance agent-payment-x402 defi-amm-security evm-token-decimals llm-trading-agent-security nodejs-keccak256 customs-trade-compliance \
carrier-relationship-management inventory-demand-planning logistics-exception-management production-scheduling returns-reverse-logistics \
quality-nonconformance energy-procurement customer-billing-ops finance-billing-ops scientific-db-pubmed-database scientific-db-uspto-database \
scientific-pkg-gget scientific-thinking-literature-review scientific-thinking-scholar-evaluation manim-video remotion-video-creation video-editing \
videodb liquid-glass-design motion-advanced motion-foundations motion-patterns motion-ui flox-environments jira-integration mle-workflow \
nutrient-document-processing fal-ai-media dmux-workflows ck gan-style-harness hermes-imports nanoclaw-repl openclaw-persona-forge ralphinho-rfc-pipeline \
investor-materials investor-outreach security-bounty-hunter visa-doc-translate connections-optimizer social-graph-ranker messages-ops email-ops \
aso-audit ui-demo ecc-tools-cost-audit configure-ecc gateguard canary-watch prisma-patterns recsys-pipeline-architect uncloud"

ecc_n=0
if [ -d "$ECC/skills" ]; then
  for d in "$ECC"/skills/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    in_list "$name" "$EXCLUDE" && continue
    target="$name"; in_list "$name" "$BUILTIN" && target="ecc-$name"
    ln -sfn "$d" "$SKILLS_DEST/$target"; ecc_n=$((ecc_n+1))
  done
fi
ok "Skill ECC collegate: $ecc_n"

# Marketing: solo le 6 a valore istituzionale (SEO/IA/contenuti/social).
KEEP="ai-seo schema seo-audit site-architecture content-strategy social"
mkt_n=0
if [ -d "$MKT/skills" ]; then
  for name in $KEEP; do
    [ -d "$MKT/skills/$name" ] && ln -sfn "$MKT/skills/$name" "$SKILLS_DEST/$name" && mkt_n=$((mkt_n+1))
  done
fi
ok "Skill marketing collegate: $mkt_n"

# Document skills UFFICIALI ANTHROPIC (https://github.com/anthropics/skills):
# file Office/PDF veri (verbali .docx, bilanci .xlsx con formule, deck .pptx,
# moduli PDF) + skill-creator + le altre creative/tecniche. last30days
# (https://github.com/mvanhorn/last30days-skill, MIT) = trend social ultimi 30gg.
# Vedi memory reference_anthropic_skills_install.
clona "https://github.com/anthropics/skills.git"         "anthropic-skills"
clona "https://github.com/mvanhorn/last30days-skill.git" "last30days-skill"
ANT="$SOURCES/anthropic-skills"
L30="$SOURCES/last30days-skill"

# Tutte le skill Anthropic TRANNE claude-api (esiste la built-in del harness,
# con blocco TRIGGER, superiore: linkare l'Anthropic creerebbe un doppione).
ANT_KEEP="docx xlsx pptx pdf skill-creator algorithmic-art brand-guidelines canvas-design doc-coauthoring frontend-design internal-comms mcp-builder slack-gif-creator theme-factory web-artifacts-builder webapp-testing"
ant_n=0
if [ -d "$ANT/skills" ]; then
  for name in $ANT_KEEP; do
    [ -d "$ANT/skills/$name" ] && ln -sfn "$ANT/skills/$name" "$SKILLS_DEST/$name" && ant_n=$((ant_n+1))
  done
fi
ok "Skill Anthropic collegate: $ant_n"

l30_n=0
[ -d "$L30/skills/last30days" ] && ln -sfn "$L30/skills/last30days" "$SKILLS_DEST/last30days" && l30_n=1
ok "Skill last30days collegata: $l30_n"

# 5 agent globali ECC (gli agent pc-* del repo sono già project-scoped).
ECC_AGENTS="a11y-architect python-reviewer seo-specialist security-reviewer silent-failure-hunter"
ag_n=0
for a in $ECC_AGENTS; do
  [ -f "$ECC/agents/$a.md" ] && ln -sfn "$ECC/agents/$a.md" "$AGENTS_DEST/$a.md" && ag_n=$((ag_n+1))
done
ok "Agent globali ECC collegati: $ag_n / 5"

# -----------------------------------------------------------------------------
# 6. MCP servers — firecrawl + playwright (scope user)
# -----------------------------------------------------------------------------
azzurro "MCP servers (firecrawl + playwright)"
if command -v claude >/dev/null 2>&1; then
  if claude mcp list 2>/dev/null | grep -q '^firecrawl'; then
    ok "firecrawl già configurato"
  elif [ -n "${FIRECRAWL_API_KEY:-}" ]; then
    claude mcp add firecrawl -s user -e "FIRECRAWL_API_KEY=$FIRECRAWL_API_KEY" -- npx -y firecrawl-mcp >/dev/null 2>&1 \
      && ok "firecrawl aggiunto (con chiave)" || nota "firecrawl: aggiunta fallita"
  else
    claude mcp add firecrawl -s user -e 'FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}' -- npx -y firecrawl-mcp >/dev/null 2>&1 \
      && nota "firecrawl aggiunto SENZA chiave — imposta il Codespaces secret FIRECRAWL_API_KEY" \
      || nota "firecrawl: aggiunta fallita"
  fi
  # Su Codespace (Ubuntu 24.04) il bundle chromium si installa: --browser chromium
  # (sul PC serviva il Chrome di sistema per via di Ubuntu 26.04).
  if claude mcp list 2>/dev/null | grep -q '^playwright'; then
    ok "playwright già configurato"
  else
    claude mcp add playwright -s user -- npx -y @playwright/mcp@latest --browser chromium --no-sandbox >/dev/null 2>&1 \
      && ok "playwright aggiunto" || nota "playwright: aggiunta fallita"
  fi
  npx -y playwright install --with-deps chromium >/dev/null 2>&1 \
    && ok "chromium per Playwright installato" \
    || nota "chromium non scaricato — lancia: npx playwright install --with-deps chromium"
else
  nota "claude non disponibile: salto la configurazione MCP"
fi

# -----------------------------------------------------------------------------
# 7. Verifica finale
# -----------------------------------------------------------------------------
azzurro "Verifica build Hugo"
if hugo --quiet --minify --destination /tmp/hugo-setup-check >/dev/null 2>&1; then
  ok "Build Hugo pulita"; rm -rf /tmp/hugo-setup-check
else
  nota "Build Hugo con warning/errori — controlla con 'hugo --minify'"
fi

SKILL_TOT="$(find "$SKILLS_DEST" -maxdepth 1 -type l 2>/dev/null | wc -l | tr -d ' ')"
PC_AGENTS="$(ls "$REPO_DIR/.claude/agents"/*.md 2>/dev/null | wc -l | tr -d ' ')"
cat <<EOF

=============================================================================
 Ambiente pronto.
   Skill globali: ${SKILL_TOT}   ·   Agent globali ECC: ${ag_n}   ·   Agent pc-* (repo): ${PC_AGENTS}
   Hugo: $(hugo version 2>/dev/null | grep -o "v${HUGO_VERSION}[^ ]*" | head -1)

 Comandi utili:
   hugo server                 anteprima (porta 1313)
   hugo server --port 1314     anteprima per verifica grafica (Playwright)
   hugo --minify               build di produzione
   claude                      avvia Claude Code (carica skill/agent/MCP)
   gh auth login               autentica GitHub CLI se serve

 Segreti come Codespaces secrets: FIRECRAWL_API_KEY, GEMINI_API_KEY, FTP_*.
 Aggiornare le skill in futuro: rilancia  bash .devcontainer/setup.sh
=============================================================================
EOF
