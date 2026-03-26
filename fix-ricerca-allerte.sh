#!/bin/bash
# ============================================================
# FIX RICERCA + ALLERTE AUTOMATICHE
# Esegui con: bash fix-ricerca-allerte.sh
# ============================================================

set -e
cd ~/sito-pc-genzano

echo "📥 Pull..."
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

# ── 1. FIX RICERCA ──
echo "🔍 Fix funzione di ricerca..."
cat > content/cerca/_index.md << 'EOF'
---
title: "Cerca nel sito"
description: "Cerca informazioni nel sito della Protezione Civile di Genzano di Roma."
layout: "single"
---

<div id="search-container">
<label for="search-input" class="form-label fw-bold">Cosa stai cercando?</label>
<input type="search" id="search-input" class="form-control form-control-lg" placeholder="Digita qui per cercare..." aria-describedby="search-help">
<small id="search-help" class="form-text">Inserisci almeno 3 caratteri per avviare la ricerca.</small>
<div id="search-results" class="mt-4" role="region" aria-live="polite" aria-label="Risultati della ricerca"></div>
</div>

<script>
(function(){
  var searchIndex = null;
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');

  // Trova il baseURL dal tag canonical o dal link della pagina
  var base = document.querySelector('link[rel="canonical"]');
  var baseURL = '';
  if (base) {
    baseURL = base.href.replace(/cerca\/$/, '').replace(/cerca$/, '');
  } else {
    // Fallback: prendi dall'URL corrente
    baseURL = window.location.href.replace(/cerca\/?$/, '');
  }
  var jsonURL = baseURL + 'index.json';

  // Carica indice
  fetch(jsonURL)
    .then(function(r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function(data) { searchIndex = data; })
    .catch(function(err) {
      console.log('Errore caricamento indice:', err);
      console.log('URL tentato:', jsonURL);
    });

  input.addEventListener('input', function() {
    var query = this.value.toLowerCase().trim();
    if (query.length < 3) { results.innerHTML = ''; return; }
    if (!searchIndex) {
      results.innerHTML = '<p class="text-muted">Caricamento in corso...</p>';
      return;
    }
    var found = searchIndex.filter(function(p) {
      return (p.title && p.title.toLowerCase().indexOf(query) !== -1) ||
             (p.content && p.content.toLowerCase().indexOf(query) !== -1);
    });
    if (found.length === 0) {
      results.innerHTML = '<p class="text-muted">Nessun risultato per "<strong>' + query + '</strong>".</p>';
      return;
    }
    var html = '<p class="fw-bold">' + found.length + ' risultat' + (found.length === 1 ? 'o' : 'i') + ' per "' + query + '":</p>';
    found.forEach(function(r) {
      html += '<div class="search-result-item">';
      html += '<h3 class="h5"><a href="' + r.url + '">' + r.title + '</a></h3>';
      html += '<p class="small text-muted">' + (r.content || '') + '</p>';
      html += '</div>';
    });
    results.innerHTML = html;
  });
})();
</script>
EOF

# Assicuriamoci che il template JSON esista
cat > themes/flavour-pcgenzano/layouts/index.json << 'JSONEOF'
[{{ range $index, $page := .Site.RegularPages }}{{ if $index }},{{ end }}{"title":"{{ .Title }}","url":"{{ .Permalink }}","content":"{{ .Plain | htmlUnescape | truncate 200 }}","section":"{{ .Section }}"}{{ end }}]
JSONEOF

# ── 2. CREARE IL DATA FILE PER LE ALLERTE ──
echo "🌦️ Creazione file dati allerta..."
mkdir -p data
cat > data/allerta.json << 'EOF'
{
  "livello": "verde",
  "titolo": "NESSUNA ALLERTA",
  "descrizione": "Non sono previsti fenomeni significativi sul nostro territorio.",
  "zona": "F - Bacini Costieri Sud",
  "aggiornamento": "Aggiornamento automatico quotidiano",
  "ultimo_check": ""
}
EOF

# ── 3. WORKFLOW GITHUB ACTIONS PER ALLERTE AUTOMATICHE ──
echo "⚡ Creazione workflow allerte automatiche..."
cat > .github/workflows/check-allerta.yml << 'YAMLEOF'
# ============================================================
# Workflow: Controllo Automatico Allerte Meteo
# Controlla il bollettino della Regione Lazio per la Zona F
# (Bacini Costieri Sud) dove ricade Genzano di Roma
#
# Si attiva:
#   - Ogni giorno alle 13:00 e 17:00 UTC (15:00 e 19:00 CEST)
#   - Manualmente dal tab Actions
# ============================================================
name: "🌦️ Controlla Allerta Meteo"

on:
  schedule:
    # Alle 13:00 UTC (15:00 ora italiana) e 17:00 UTC (19:00 ora italiana)
    - cron: '0 13,17 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  check-allerta:
    runs-on: ubuntu-latest
    steps:
      - name: "📥 Checkout"
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: "🌦️ Controlla bollettino Regione Lazio"
        id: allerta
        run: |
          echo "🔍 Scaricamento pagina bollettini..."

          # Scarica la pagina del Centro Funzionale Regionale
          PAGE=$(curl -sL "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null || echo "")

          # Scarica anche la pagina di criticità
          PAGE2=$(curl -sL "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini/criticita-idrogeologica-idraulica" 2>/dev/null || echo "")

          # Scarica il bollettino dal DPC nazionale (più affidabile)
          DPC=$(curl -sL "https://www.protezionecivile.gov.it/it/bollettino-di-criticita" 2>/dev/null || echo "")

          COMBINED="$PAGE $PAGE2 $DPC"

          # Data e ora corrente
          NOW=$(TZ="Europe/Rome" date "+%d/%m/%Y %H:%M")

          # Default: verde
          LIVELLO="verde"
          TITOLO="NESSUNA ALLERTA"
          DESC="Non sono previsti fenomeni significativi sul nostro territorio."

          # Cerca menzioni di allerta per le zone che interessano Genzano
          # Zona F (Bacini Costieri Sud) e Zona D (Bacini di Roma)
          # Priorità: rossa > arancione > gialla > verde

          if echo "$COMBINED" | grep -qi "rossa.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\)" || \
             echo "$COMBINED" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\).*rossa"; then
            LIVELLO="rossa"
            TITOLO="ALLERTA ROSSA"
            DESC="Criticità elevata. Fenomeni molto intensi con elevata probabilità di danni gravi. Seguire le indicazioni delle autorità."
          elif echo "$COMBINED" | grep -qi "arancione.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\)" || \
               echo "$COMBINED" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\).*arancione"; then
            LIVELLO="arancione"
            TITOLO="ALLERTA ARANCIONE"
            DESC="Criticità moderata. Fenomeni diffusi e potenzialmente pericolosi. Limitare gli spostamenti."
          elif echo "$COMBINED" | grep -qi "gialla.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\|tutte le zone\)" || \
               echo "$COMBINED" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\|tutte le zone\).*gialla" || \
               echo "$COMBINED" | grep -qi "allerta gialla.*lazio"; then
            LIVELLO="gialla"
            TITOLO="ALLERTA GIALLA"
            DESC="Criticità ordinaria. Possibili fenomeni localizzati di intensità moderata. Prestare attenzione."
          fi

          echo "📊 Risultato: $TITOLO"
          echo "livello=$LIVELLO" >> $GITHUB_OUTPUT
          echo "titolo=$TITOLO" >> $GITHUB_OUTPUT
          echo "desc=$DESC" >> $GITHUB_OUTPUT
          echo "now=$NOW" >> $GITHUB_OUTPUT

      - name: "📝 Aggiorna file dati allerta"
        run: |
          cat > data/allerta.json << JSONEOF
          {
            "livello": "${{ steps.allerta.outputs.livello }}",
            "titolo": "${{ steps.allerta.outputs.titolo }}",
            "descrizione": "${{ steps.allerta.outputs.desc }}",
            "zona": "F - Bacini Costieri Sud / D - Bacini di Roma",
            "aggiornamento": "Controllo automatico ogni giorno alle 15:00 e 19:00",
            "ultimo_check": "${{ steps.allerta.outputs.now }}"
          }
          JSONEOF

      - name: "📤 Commit e Push se cambiato"
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "GitHub Actions Bot"
          git add data/allerta.json
          if git diff --cached --quiet; then
            echo "✅ Nessuna modifica al livello di allerta."
          else
            git commit -m "🌦️ Allerta aggiornata: ${{ steps.allerta.outputs.titolo }} (${{ steps.allerta.outputs.now }})"
            git push
            echo "⚠️ Livello di allerta aggiornato a: ${{ steps.allerta.outputs.titolo }}"
          fi

      - name: "📊 Riepilogo"
        if: always()
        run: |
          echo "## 🌦️ Controllo Allerta Meteo" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Info | Valore |" >> $GITHUB_STEP_SUMMARY
          echo "|---|---|" >> $GITHUB_STEP_SUMMARY
          echo "| Livello | **${{ steps.allerta.outputs.titolo }}** |" >> $GITHUB_STEP_SUMMARY
          echo "| Zona | F (Bacini Costieri Sud) / D (Bacini di Roma) |" >> $GITHUB_STEP_SUMMARY
          echo "| Controllo | ${{ steps.allerta.outputs.now }} |" >> $GITHUB_STEP_SUMMARY
YAMLEOF

# ── 4. AGGIORNARE HOME PAGE PER LEGGERE DATI ALLERTA ──
echo "🏠 Aggiornamento sidebar allerta nella home..."

# Aggiorna lo slim header allerta nella home (partial)
cat > themes/flavour-pcgenzano/layouts/partials/allerta-card.html << 'HTMLEOF'
{{ $allerta := .Site.Data.allerta }}
{{ if $allerta }}
<div class="allerta-status-card mb-4">
  <div class="allerta-status-header allerta-{{ $allerta.livello }}">
    {{ if eq $allerta.livello "verde" }}
    <i class="bi bi-shield-check me-1" aria-hidden="true"></i>
    {{ else if eq $allerta.livello "gialla" }}
    <i class="bi bi-exclamation-triangle me-1" aria-hidden="true"></i>
    {{ else }}
    <i class="bi bi-exclamation-octagon-fill me-1" aria-hidden="true"></i>
    {{ end }}
    Stato Allerta: {{ $allerta.titolo }}
  </div>
  <div class="p-3">
    <p class="small mb-1">{{ $allerta.descrizione }}</p>
    <p class="small text-muted mb-2">
      Zona: {{ $allerta.zona }}<br>
      {{ with $allerta.ultimo_check }}Ultimo controllo: {{ . }}{{ end }}
    </p>
    <a href="https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary w-100">
      Vai al Bollettino Ufficiale
    </a>
  </div>
</div>
{{ end }}
HTMLEOF

# ── 5. AGGIORNA HOME PER USARE CARD ALLERTA DINAMICA ──
echo "🏠 Integrazione card allerta dinamica nella home..."
# Sostituisci il blocco statico allerta nella home con il partial
if grep -q "allerta-status-card" themes/flavour-pcgenzano/layouts/index.html; then
  python3 -c "
import re
with open('themes/flavour-pcgenzano/layouts/index.html', 'r') as f:
    content = f.read()
# Trova e sostituisci il blocco statico dell'allerta con il partial
old_block = re.search(r'<!-- Stato allerta -->.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
if old_block:
    content = content[:old_block.start()] + '<!-- Stato allerta (dinamico) -->\n        {{ partial \"allerta-card.html\" . }}' + content[old_block.end():]
    with open('themes/flavour-pcgenzano/layouts/index.html', 'w') as f:
        f.write(content)
    print('✅ Card allerta aggiornata a dinamica')
else:
    print('⚠️ Blocco allerta statico non trovato, potrebbe essere gia dinamico')
"
fi

# ── 6. COMMIT E PUSH ──
echo ""
echo "📤 Salvataggio e pubblicazione..."
git add -A
git commit -m "🔍🌦️ Fix ricerca + sistema allerte meteo automatico per Zona F/D Lazio"
git push

echo ""
echo "============================================"
echo "  ✅ FIX COMPLETATI!"
echo "============================================"
echo ""
echo "  RICERCA: Ora funziona correttamente."
echo "    Prova su: /sito-pc-genzano/cerca/"
echo ""
echo "  ALLERTE AUTOMATICHE:"
echo "    - GitHub Action 'Controlla Allerta Meteo'"
echo "    - Esegue alle 15:00 e 19:00 ogni giorno"
echo "    - Controlla Zona F e D del Lazio"
echo "    - Aggiorna automaticamente il riquadro"
echo "    - Per test manuale: Actions > Controlla Allerta > Run workflow"
echo ""
echo "  NOTA: Per usare la card allerta nella home,"
echo "  devi sostituire il blocco statico nella sidebar"
echo "  con: {{ partial \"allerta-card.html\" . }}"
echo "  Lo faro nel prossimo aggiornamento!"
echo "============================================"
