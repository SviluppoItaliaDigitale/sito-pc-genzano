#!/bin/bash
# consegna.sh: dopo il render (motion/out/it-alert-3d/dist/it-alert-muto.mp4) monta il mix sul video, prepara la versione
# per il sito (720×1280, H.264 Main 3.1, AAC, senza metadati), il poster e i sottotitoli .vtt.
# Uso: bash consegna.sh CARTELLA_SKILL PYTHON_CON_NUMPY_E_SCIPY
set -e
qui="$(cd "$(dirname "$0")" && pwd)"; out="$qui/../../out/it-alert-3d"; n=it-alert-3d-9x16
"$2" "$1/colonna-sonora/scripts/mixa.py" "$qui/colonna.json" --uscita "$out/mix.wav" --rapporto "$out/mix.rapporto.json" \
  --video "$out/dist/it-alert-muto.mp4" --video-uscita "$out/$n.mp4"
ffmpeg -hide_banner -loglevel error -y -i "$out/dist/it-alert-muto.mp4" -i "$out/mix.wav" -map 0:v -map 1:a \
  -vf "scale=720:1280:flags=lanczos,format=yuv420p" -c:v libx264 -preset slow -crf 23 -profile:v main -level 3.1 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -bsf:v filter_units=remove_types=6 \
  -c:a aac -b:a 128k -ar 48000 -shortest -movflags +faststart -map_metadata -1 -map_chapters -1 -fflags +bitexact \
  -flags:v +bitexact -flags:a +bitexact "$out/.web-tmp.mp4"
# seconda passata senza ricodifica: toglie anche l'etichetta del programma di codifica dalla traccia video
ffmpeg -hide_banner -loglevel error -y -i "$out/.web-tmp.mp4" -map 0:v -map 0:a -c copy -movflags +faststart -map_metadata -1 \
  -map_chapters -1 -fflags +bitexact -metadata:s:v:0 handler_name=Video -metadata:s:a:0 handler_name=Audio "$out/$n-web.mp4"
rm -f "$out/.web-tmp.mp4"
# poster: il telefono con l'avviso e il titolo (6,6 s)
ffmpeg -hide_banner -loglevel error -y -ss 6.6 -i "$out/dist/it-alert-muto.mp4" -frames:v 1 -vf "scale=720:1280:flags=lanczos" \
  -c:v libwebp -quality 82 -map_metadata -1 -fflags +bitexact "$out/$n-poster.webp"
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
echo "fatto: $out/$n.mp4, $n-web.mp4, $n-poster.webp, it-alert-3d.vtt"
