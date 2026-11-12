#!/bin/bash
# consegna.sh: dopo i due render (motion/out/it-alert-3d/dist/it-alert-9x16-muto.mp4 e it-alert-16x9-muto.mp4) monta il mix
# sui video, prepara le versioni per il sito (720×1280 e 1280×720, H.264 Main 3.1, AAC 192k, senza metadati), i poster
# e i sottotitoli .vtt. Uso: bash consegna.sh CARTELLA_SKILL PYTHON_CON_NUMPY_E_SCIPY
set -e
qui="$(cd "$(dirname "$0")" && pwd)"; out="$qui/../../out/it-alert-3d"
for fmt in 9x16 16x9; do
  n=it-alert-3d-$fmt; muto="$out/dist/it-alert-$fmt-muto.mp4"
  [ $fmt = 9x16 ] && misura=720:1280 || misura=1280:720
  "$2" "$1/colonna-sonora/scripts/mixa.py" "$qui/colonna.json" --uscita "$out/mix.wav" --rapporto "$out/mix-$fmt.rapporto.json" \
    --video "$muto" --video-uscita "$out/$n.mp4"
  ffmpeg -hide_banner -loglevel error -y -i "$muto" -i "$out/mix.wav" -map 0:v -map 1:a \
    -vf "scale=$misura:flags=lanczos,format=yuv420p" -c:v libx264 -preset slow -crf 23 -profile:v main -level 3.1 \
    -colorspace bt709 -color_primaries bt709 -color_trc bt709 -bsf:v filter_units=remove_types=6 \
    -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart -map_metadata -1 -map_chapters -1 -fflags +bitexact \
    -flags:v +bitexact -flags:a +bitexact "$out/.web-tmp.mp4"
  # seconda passata senza ricodifica: toglie anche l'etichetta del programma di codifica dalla traccia video
  ffmpeg -hide_banner -loglevel error -y -i "$out/.web-tmp.mp4" -map 0:v -map 0:a -c copy -movflags +faststart -map_metadata -1 \
    -map_chapters -1 -fflags +bitexact -metadata:s:v:0 handler_name=Video -metadata:s:a:0 handler_name=Audio "$out/$n-web.mp4"
  rm -f "$out/.web-tmp.mp4"
  # poster: il telefono con l'avviso e il titolo (7,5 s)
  ffmpeg -hide_banner -loglevel error -y -ss 7.5 -i "$muto" -frames:v 1 -vf "scale=$misura:flags=lanczos" \
    -c:v libwebp -quality 82 -map_metadata -1 -fflags +bitexact "$out/$n-poster.webp"
done
python3 - "$qui/sottotitoli.json" "$out/it-alert-3d.vtt" <<'PY'
import json, sys
def ts(s):
    h, r = divmod(s, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"
righe = ["WEBVTT", ""]
for i, f in enumerate(json.load(open(sys.argv[1], encoding="utf-8")), 1):
    righe += [str(i), f"{ts(f['inizio'])} --> {ts(f['fine'])}", f["testo"], ""]
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(righe))
PY
echo "fatto"
