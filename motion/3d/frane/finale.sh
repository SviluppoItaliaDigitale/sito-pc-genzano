#!/bin/bash
# finale.sh: dai due video muti (9:16 e 16:9) ai video finiti. Mix con la voce in primo piano (mixa.py), master senza
# metadati dell'encoder, versione per il sito (720 px sul lato corto, H.264 Main 3.1, AAC 192k dal WAV del mix,
# faststart), poster e sottotitoli.
# Uso: bash finale.sh CARTELLA_SKILL PYTHON_CON_NUMPY_SCIPY   (dopo i render: out/frane-3d/dist/frane-3d-<fmt>-muto.mp4)
set -e
qui="$(cd "$(dirname "$0")" && pwd)"; out="$qui/../../out/frane-3d"; S="$1"; PY="${2:-python3}"
cd "$out"
for fmt in 9x16 16x9; do
  [ "$fmt" = 9x16 ] && lati=720:1280 || lati=1280:720
  "$PY" "$S/colonna-sonora/scripts/mixa.py" "$qui/colonna.json" --uscita mix.wav --rapporto "mix-$fmt.rapporto.json" \
    --video "dist/frane-3d-$fmt-muto.mp4" --video-uscita "frane-3d-$fmt.mp4"
  ffmpeg -v error -y -i "frane-3d-$fmt.mp4" -i mix.wav -map 0:v:0 -map 1:a:0 -vf "scale=$lati:flags=lanczos" \
    -c:v libx264 -profile:v main -level 3.1 -pix_fmt yuv420p -preset slow -crf 23 -g 60 \
    -color_primaries bt709 -color_trc bt709 -colorspace bt709 -af volume=-0.3dB -c:a aac -b:a 192k -ar 48000 \
    -fflags +bitexact -flags:v +bitexact -flags:a +bitexact -shortest web-tmp.mp4
  # seconda passata senza ricodifica: toglie ogni traccia del programma di codifica (etichette e dati SEI)
  ffmpeg -v error -y -i web-tmp.mp4 -map 0 -c copy -bsf:v filter_units=remove_types=6 -map_metadata -1 -map_chapters -1 \
    -fflags +bitexact -metadata:s:v:0 handler_name=Video -metadata:s:a:0 handler_name=Audio -movflags +faststart "frane-3d-$fmt-web.mp4"
  rm -f web-tmp.mp4
  ffmpeg -v error -y -ss "${POSTER_T:-38.6}" -i "frane-3d-$fmt.mp4" -frames:v 1 -vf "scale=$lati:flags=lanczos" poster.png
  python3 -c "from PIL import Image; Image.open('poster.png').convert('RGB').save('frane-3d-$fmt-poster.webp', quality=82)"; rm -f poster.png
done
python3 "$qui/vtt.py" "$out"
ls -la frane-3d-*.mp4 frane-3d-*-poster.webp frane-3d.vtt
