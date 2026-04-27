#!/usr/bin/env bash
# Scarica foto di CORPO per gli articoli "anniversari" (eventi storici di PC).
#
# Eseguire UNA VOLTA su macchina con rete libera (laptop, desktop).
# NON gira nella sandbox di Claude Code cloud.
#
# Output: file .webp in static/images/ con fascia blu istituzionale,
# nominati AAAA-MM-GG-slug-evento.webp (diversi dallo slug articolo
# per non sovrascrivere la copertina — vedi regola foto evento).
#
# Dipendenze: curl, jq, python3, magick (ImageMagick 7).
# Se manca magick: sudo apt install imagemagick
#
# Dopo l'esecuzione:
#   git add static/images/
#   git commit -m "Foto corpo articoli anniversari"
#   git push

set -uo pipefail   # -e rimosso: se un download fallisce continua con i successivi

cd "$(dirname "$0")/.."

# Funzione che chiama foto-da-wikipedia.sh e segnala fallimento senza fermarsi
fetch() {
  local titolo="$1"
  local nome="$2"
  local lang="${3:-it}"
  echo ""
  echo "==> $nome ($lang)"
  bash scripts/foto-da-wikipedia.sh "$titolo" "$nome" "$lang" \
    || echo "  ⚠️  FALLITO: $nome — aggiungere manualmente"
}

echo "== Foto di corpo per articoli anniversari =="
echo ""

# --- TERREMOTI ITALIANI ---
fetch "Terremoto del Belice"                          "2026-evento-belice-1968-frazione"           it
fetch "Terremoto del Friuli del 1976"                 "2026-evento-friuli-1976-gemona-macerie"     it
fetch "Terremoto dell'Irpinia del 1980"               "2026-evento-irpinia-1980-conza-distruzione" it
fetch "Terremoto di San Giuliano di Puglia del 2002"  "2026-evento-san-giuliano-2002-scuola"       it
fetch "Terremoto dell'Aquila del 2009"                "2026-evento-aquila-2009-centro-storico"     it
fetch "Terremoto dell'Emilia del 2012"                "2026-evento-emilia-2012-mirandola"          it
fetch "Terremoto del Centro Italia del 2016"          "2026-evento-amatrice-2016-prima-scossa"     it
fetch "Terremoto di Norcia del 30 ottobre 2016"       "2026-evento-norcia-2016-basilica-crollata"  it

# --- FRANE E ALLUVIONI ---
fetch "Alluvione di Firenze del 4 novembre 1966"      "2026-evento-firenze-1966-piazza-santa-croce" it
fetch "Disastro del Vajont"                           "2026-evento-vajont-1963-diga-erto"          it
fetch "Alluvione di Sarno e Quindici del 1998"        "2026-evento-sarno-1998-frana-paese"         it
fetch "Disastro della Val di Stava"                   "2026-evento-stava-1985-bacini-decantazione" it
fetch "Frana della Val Pola"                          "2026-evento-val-pola-1987-monte-zandila"    it
fetch "Alluvione delle Marche del 2022"               "2026-evento-marche-2022-senigallia-acqua"   it
fetch "Alluvione dell'Emilia-Romagna del 2023"        "2026-evento-emilia-romagna-2023-faenza"     it

# --- INFRASTRUTTURE E DISASTRI INDUSTRIALI ---
fetch "Crollo del ponte Morandi"                      "2026-evento-morandi-2018-genova-crollo"     it
fetch "Disastro di Seveso"                            "2026-evento-seveso-1976-icmesa-fabbrica"    it
fetch "Disastro di Černobyl'"                         "2026-evento-chernobyl-1986-reattore-4"      it

# --- EVENTI METEO ESTREMI ---
fetch "Tempesta Vaia"                                 "2026-evento-vaia-2018-foreste-devastate"    it
fetch "Frana di Pizzo Cengalo"                        "2026-evento-pizzo-cengalo-2017-bondo"       it

# --- EVENTI INTERNAZIONALI ---
fetch "Maremoto dell'Oceano Indiano del 2004"         "2026-evento-tsunami-2004-onda"              it
fetch "Terremoto e maremoto del Tōhoku del 2011"      "2026-evento-tohoku-2011-fukushima"          it
fetch "Terremoto di Messina del 1908"                 "2026-evento-messina-1908-rovine"            it

# --- EVENTI UMANI ---
fetch "Vermicino"                                     "2026-evento-vermicino-1981-pozzo"           it

echo ""
echo "== Fatto =="
echo ""
echo "File generati in static/images/:"
ls -lh static/images/2026-evento-*.webp 2>/dev/null | wc -l
echo ""
echo "Per pubblicare:"
echo "  git add static/images/2026-evento-*.webp"
echo "  git commit -m 'Foto corpo articoli anniversari (storia PC)'"
echo "  git push"
