#!/usr/bin/env bash
# Scarica la libreria di pittogrammi del sito da fonti ufficiali:
#  - ISO 7010 (sicurezza standard)  -> Wikimedia Commons (PD-shape / CC0)
#  - ARASAAC (CC BY-NC-SA)          -> api.arasaac.org (Gobierno de Aragón, Sergio Palao)
#
# Uso:
#   bash scripts/scarica-pittogrammi.sh           # scarica solo i mancanti
#   bash scripts/scarica-pittogrammi.sh --force   # ri-scarica tutto
#
# Output:
#   static/pittogrammi/iso7010/<nome>.svg
#   static/pittogrammi/arasaac/<nome>.png
#   static/pittogrammi/iso7010/LICENZA.txt
#   static/pittogrammi/arasaac/LICENZA.txt
#
# Le attribuzioni complete sono su /attribuzioni-pittogrammi/ (linkata dal footer).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST_ISO="$REPO_ROOT/static/pittogrammi/iso7010"
DEST_ARA="$REPO_ROOT/static/pittogrammi/arasaac"
FORCE=0
[ "${1:-}" = "--force" ] && FORCE=1

mkdir -p "$DEST_ISO" "$DEST_ARA"

UA="PC-Genzano-Bot/1.0 (sito istituzionale, https://www.protezionecivilegenzano.it)"

OK_ISO=0; FAIL_ISO=0; SKIP_ISO=0
OK_ARA=0; FAIL_ARA=0; SKIP_ARA=0
declare -a FAILED_ITEMS=()

# ---------------------------------------------------------------------------
# ISO 7010 — formato: CODICE|nome-file|descrizione
# ---------------------------------------------------------------------------
ISO7010=(
  # Evacuazione e primo soccorso (E)
  "E001|uscita-emergenza-sinistra|Uscita di emergenza a sinistra"
  "E002|uscita-emergenza-destra|Uscita di emergenza a destra"
  "E003|cassetta-primo-soccorso|Cassetta di primo soccorso"
  "E004|telefono-emergenza|Telefono di emergenza"
  "E007|punto-raccolta|Punto di raccolta"
  "E009|lavaggio-occhi|Stazione lavaggio occhi"
  "E010|defibrillatore-dae|Defibrillatore (DAE)"
  "E011|acqua-potabile|Acqua potabile"
  "E013|barella|Barella"
  "E018|porta-tirare|Porta da aprire tirando"
  "E019|porta-spingere|Porta da aprire spingendo"
  "E024|punto-evacuazione|Punto di evacuazione"

  # Antincendio (F)
  "F001|estintore|Estintore"
  "F002|idrante-muro|Idrante a muro"
  "F003|scala-antincendio|Scala antincendio"
  "F004|telefono-antincendio|Telefono per emergenze antincendio"
  "F005|pulsante-allarme-antincendio|Pulsante di allarme antincendio"

  # Pericolo / Avvertimento (W)
  "W001|pericolo-generico|Pericolo generico"
  "W002|pericolo-esplosivo|Pericolo materiale esplosivo"
  "W008|pericolo-corrosivo|Pericolo sostanze corrosive (W008 vecchia ed., conferma visiva)"
  "W009|pericolo-biologico|Pericolo biologico"
  "W010|pericolo-bassa-temperatura|Pericolo bassa temperatura"
  "W011|pavimento-scivoloso|Pavimento scivoloso"
  "W012|pericolo-elettrico|Pericolo elettrico"
  "W016|pericolo-tossico|Pericolo sostanze tossiche"
  "W017|superficie-calda|Superficie calda"
  "W018|allarme-antincendio-automatico|Allarme antincendio automatico"
  "W021|materiale-infiammabile|Materiale infiammabile"
  # NOTA: la voce "W023|caduta-massi" e' stata rimossa il 2 maggio 2026:
  # ISO 7010 W023 = Sostanza corrosiva (NON caduta massi). Lo script
  # scaricava il file corrosivo e lo salvava col nome sbagliato
  # "caduta-massi.svg", inducendo il Memory primaria ad abbinare un
  # pittogramma corrosivo alla voce "Attento alle frane" (bug segnalato
  # dall'utente). Per il concetto "frana" usare arasaac/frana.png
  # (gia' nella libreria, semantica chiara).
  "W024|pericolo-schiacciamento|Pericolo schiacciamento"

  # Obbligo (M)
  "M001|obbligo-generico|Obbligo generico"
  "M002|consultare-istruzioni|Consultare istruzioni"
  "M003|protezione-udito|Indossare protezione udito"
  "M004|protezione-occhi|Indossare protezione occhi"
  "M008|scarpe-protettive|Indossare scarpe protettive"
  "M009|guanti-protettivi|Indossare guanti protettivi"
  "M010|abito-protettivo|Indossare abito protettivo"
  "M013|maschera-protettiva|Indossare maschera protettiva"
  "M014|casco-protettivo|Indossare casco protettivo"
  "M015|alta-visibilita|Indossare giubbotto ad alta visibilità"

  # Divieto (P)
  "P001|divieto-generico|Divieto generico"
  "P002|vietato-fumare|Vietato fumare"
  "P003|vietato-fuochi|Vietato accendere fuochi"
  "P004|vietato-pedoni|Vietato l'accesso ai pedoni"
  "P010|vietato-toccare|Vietato toccare"
  "P022|vietato-bere|Acqua non potabile"
)

# ---------------------------------------------------------------------------
# ARASAAC — formato: keyword-ricerca|nome-file|tema
# ---------------------------------------------------------------------------
ARASAAC=(
  # Eventi e rischi naturali
  "terremoto|terremoto|rischio"
  "incendio|incendio|rischio"
  "fuoco|fuoco|rischio"
  "inondazione|alluvione|rischio"
  "valanga di fango|frana|rischio"
  "pioggia|pioggia|meteo"
  "temporale|temporale|meteo"
  "fulmine|fulmine|meteo"
  "grandine|grandine|meteo"
  "vento|vento|meteo"
  "tempesta|tempesta|meteo"
  "tornado|tornado|meteo"
  "neve|neve|meteo"
  "ghiaccio|ghiaccio|meteo"
  "caldo|caldo|meteo"
  "nebbia|nebbia|meteo"
  "fuga di gas|fuga-gas|rischio"
  "gas|gas|rischio"
  "vulcano|vulcano|rischio"
  "eruzione vulcanica|eruzione-vulcanica|rischio"
  "valanga|valanga|rischio"

  # Azioni di autoprotezione
  "telefonare|telefonare|azione"
  "telefono|telefono|azione"
  "ascoltare la radio|ascoltare-radio|azione"
  "radio|radio|azione"
  "guardare la televisione|guardare-tv|azione"
  "proteggere la testa|proteggere-testa|azione"
  "nascondersi|nascondersi|azione"
  "nascondersi sotto al tavolo|nascondersi-tavolo|azione"
  "uscire|uscire|azione"
  "scappare|scappare|azione"
  "entrare in casa|entrare-casa|azione"
  "chiudere|chiudere|azione"
  "chiudere il gas|chiudere-gas|azione"
  "chiudere la finestra|chiudere-finestra|azione"
  "chiudere la porta|chiudere-porta|azione"
  "aprire la finestra|aprire-finestra|azione"
  "aprire la porta|aprire-porta|azione"
  "spegnere|spegnere|azione"
  "scendere le scale|scendere-scale|azione"
  "salire le scale|salire-scale|azione"
  "correre|correre|azione"
  "camminare|camminare|azione"
  "aiutare|aiutare|azione"
  "calma|calma|azione"
  "tranquillo|tranquillo|azione"
  "aspettare|aspettare|azione"
  "evacuare|evacuare|azione"
  "lavarsi le mani|lavarsi-mani|azione"
  "bere acqua|bere-acqua|azione"

  # Oggetti del kit emergenza
  "zaino|zaino|kit"
  "borsa|borsa|kit"
  "torcia|torcia|kit"
  "lampada|lampada|kit"
  "acqua|acqua|kit"
  "bottiglia di acqua|bottiglia-acqua|kit"
  "cibo|cibo|kit"
  "coperta|coperta|kit"
  "medicina|medicina|kit"
  "farmaci|farmaci|kit"
  "documenti|documenti|kit"
  "carta di identità|carta-identita|kit"
  "mascherina|mascherina|kit"
  "casco|casco|kit"
  "pile|pile|kit"
  "candela|candela|kit"
  "vestiti|vestiti|kit"
  "scarpe|scarpe|kit"
  "guanti|guanti|kit"
  "fischietto|fischietto|kit"
  "chiavi|chiavi|kit"
  "soldi|soldi|kit"

  # Persone
  "bambino|bambino|persona"
  "bambina|bambina|persona"
  "famiglia|famiglia|persona"
  "mamma|mamma|persona"
  "papà|papa|persona"
  "nonno|nonno|persona"
  "nonna|nonna|persona"
  "anziano|anziano|persona"
  "volontario|volontario|persona"
  "pompiere|pompiere|persona"
  "vigile del fuoco|vigile-fuoco|persona"
  "medico|medico|persona"
  "infermiere|infermiere|persona"
  "poliziotto|poliziotto|persona"
  "carabiniere|carabiniere|persona"

  # Luoghi
  "casa|casa|luogo"
  "scuola|scuola|luogo"
  "ospedale|ospedale|luogo"
  "strada|strada|luogo"
  "bosco|bosco|luogo"
  "foresta|foresta|luogo"
  "fiume|fiume|luogo"
  "lago|lago|luogo"
  "mare|mare|luogo"
  "spiaggia|spiaggia|luogo"
  "montagna|montagna|luogo"
  "ufficio|ufficio|luogo"
  "chiesa|chiesa|luogo"
  "piazza|piazza|luogo"
  "ascensore|ascensore|luogo"
  "garage|garage|luogo"

  # Segnali e comunicazione
  "attenzione|attenzione|segnale"
  "pericolo|pericolo|segnale"
  "stop|stop|segnale"
  "allarme|allarme|segnale"
  "allarme incendio|sirena|segnale"
  "sì|si|segnale"
  "no|no|segnale"
  "aiuto|aiuto|segnale"
  "emergenza|emergenza|segnale"
  "urgente|urgente|segnale"
  "informazione|informazione|segnale"
  "ascoltare|ascoltare|segnale"
  "vedere|vedere|segnale"
  "mappa|mappa|segnale"
  "cartello|cartello|segnale"

  # Veicoli
  "ambulanza|ambulanza|veicolo"
  "camion dei pompieri|camion-pompieri|veicolo"
  "elicottero|elicottero|veicolo"
  "auto della polizia|auto-polizia|veicolo"

  # Tempo e numeri utili
  "112|112|numero"
  "orologio|orologio|tempo"
  "calendario|calendario|tempo"
)

echo "==> ISO 7010 (Wikimedia Commons)"
for entry in "${ISO7010[@]}"; do
  IFS='|' read -r CODE NAME DESC <<< "$entry"
  OUT="$DEST_ISO/$NAME.svg"
  if [ -f "$OUT" ] && [ "$FORCE" -eq 0 ]; then
    SKIP_ISO=$((SKIP_ISO+1))
    continue
  fi
  URL="https://commons.wikimedia.org/wiki/Special:FilePath/ISO_7010_${CODE}.svg"
  if curl -sLf -A "$UA" -o "$OUT" "$URL"; then
    # Verifica che sia davvero SVG, non HTML di errore
    if head -c 200 "$OUT" | grep -q -i "<svg\|<?xml"; then
      OK_ISO=$((OK_ISO+1))
      echo "  [ok]   $CODE -> $NAME.svg"
    else
      rm -f "$OUT"
      FAIL_ISO=$((FAIL_ISO+1))
      FAILED_ITEMS+=("ISO 7010 $CODE ($DESC) — file scaricato non è SVG")
      echo "  [FAIL] $CODE non è SVG"
    fi
  else
    FAIL_ISO=$((FAIL_ISO+1))
    FAILED_ITEMS+=("ISO 7010 $CODE ($DESC) — non trovato su Wikimedia")
    echo "  [FAIL] $CODE non trovato"
  fi
  sleep 1.0
done

echo ""
echo "==> ARASAAC (api.arasaac.org)"
for entry in "${ARASAAC[@]}"; do
  IFS='|' read -r KEY NAME TEMA <<< "$entry"
  OUT="$DEST_ARA/$NAME.png"
  if [ -f "$OUT" ] && [ "$FORCE" -eq 0 ]; then
    SKIP_ARA=$((SKIP_ARA+1))
    continue
  fi
  KEY_ENC=$(printf '%s' "$KEY" | jq -sRr @uri)
  RESP=$(curl -sf -A "$UA" "https://api.arasaac.org/api/pictograms/it/search/${KEY_ENC}" || echo "[]")
  ID=$(printf '%s' "$RESP" | jq -r '.[0]._id // empty')
  if [ -z "$ID" ]; then
    FAIL_ARA=$((FAIL_ARA+1))
    FAILED_ITEMS+=("ARASAAC '$KEY' ($TEMA) — nessun risultato API")
    echo "  [FAIL] '$KEY' nessun risultato"
    continue
  fi
  IMG_URL="https://static.arasaac.org/pictograms/${ID}/${ID}_500.png"
  if curl -sLf -A "$UA" -o "$OUT" "$IMG_URL"; then
    OK_ARA=$((OK_ARA+1))
    echo "  [ok]   '$KEY' (id $ID) -> $NAME.png"
  else
    rm -f "$OUT"
    FAIL_ARA=$((FAIL_ARA+1))
    FAILED_ITEMS+=("ARASAAC '$KEY' (id $ID, $TEMA) — download immagine fallito")
    echo "  [FAIL] '$KEY' id $ID download fallito"
  fi
  sleep 0.15
done

# ---------------------------------------------------------------------------
# File LICENZA.txt — stub locali. Attribuzioni complete su /attribuzioni-pittogrammi/.
# ---------------------------------------------------------------------------
cat > "$DEST_ISO/LICENZA.txt" <<'EOF'
Pittogrammi ISO 7010 — Wikimedia Commons
=========================================

Fonte: https://commons.wikimedia.org/wiki/Category:ISO_7010_safety_signs

I segni grafici della norma ISO 7010 sono di pubblico dominio in quanto
forme geometriche standardizzate (PD-shape). Le specifiche rappresentazioni
SVG presenti su Wikimedia Commons sono pubblicate prevalentemente in pubblico
dominio o con licenza CC0.

La norma ISO 7010 stessa è proprietà ISO; questa libreria contiene solo le
rappresentazioni grafiche pubblicamente diffuse, non il documento normativo.

Attribuzione completa: https://www.protezionecivilegenzano.it/attribuzioni-pittogrammi/
EOF

cat > "$DEST_ARA/LICENZA.txt" <<'EOF'
Pittogrammi ARASAAC
====================

Autore: Sergio Palao
Origine: ARASAAC (https://arasaac.org)
Licenza: Creative Commons BY-NC-SA 4.0
         https://creativecommons.org/licenses/by-nc-sa/4.0/deed.it
Proprietà: Governo di Aragona (Spagna) — Departamento de Educación, Cultura y Deporte

I pittogrammi ARASAAC sono utilizzati a scopi non commerciali per facilitare
la comprensione dei contenuti del sito istituzionale del Gruppo Comunale
Volontari di Protezione Civile di Genzano di Roma, in particolare per
bambini, persone con disabilità cognitive e parlanti l'italiano come lingua
seconda (L2).

Le opere derivate (schede stampabili, materiali didattici) che includono
pittogrammi ARASAAC ereditano la stessa licenza CC BY-NC-SA 4.0.

Attribuzione completa: https://www.protezionecivilegenzano.it/attribuzioni-pittogrammi/
EOF

echo ""
echo "==================================================="
echo "Pittogrammi scaricati:"
echo "  ISO 7010   ok=$OK_ISO  skip=$SKIP_ISO  fail=$FAIL_ISO"
echo "  ARASAAC    ok=$OK_ARA  skip=$SKIP_ARA  fail=$FAIL_ARA"
echo "==================================================="

if [ "${#FAILED_ITEMS[@]}" -gt 0 ]; then
  echo ""
  echo "Elementi non scaricati (verifica manuale):"
  for it in "${FAILED_ITEMS[@]}"; do
    echo "  - $it"
  done
fi
