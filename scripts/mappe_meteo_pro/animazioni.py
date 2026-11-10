"""GIF animate e, se ffmpeg è disponibile, anche un MP4."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image


def _riduci(im: Image.Image, max_lato: int = 1400) -> Image.Image:
    w, h = im.size
    if max(w, h) <= max_lato:
        return im.convert("RGB")
    scala = max_lato / max(w, h)
    return im.convert("RGB").resize((int(w * scala), int(h * scala)), Image.Resampling.LANCZOS)


def scrivi_gif(fotogrammi: list[Path], dest: Path, durata_ms: int = 450, max_lato: int = 1100) -> Path | None:
    """Compone una GIF in loop. Restituisce il percorso, o None se ci sono troppi pochi fotogrammi."""
    esistenti = [p for p in fotogrammi if p.is_file()]
    if len(esistenti) < 2:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    immagini = [_riduci(Image.open(p), max_lato) for p in esistenti]
    # Quantizzazione adattiva per tenere il file leggero (condivisione sui social).
    quant = [im.convert("P", palette=Image.Palette.ADAPTIVE, colors=128) for im in immagini]
    quant[0].save(
        dest,
        save_all=True,
        append_images=quant[1:],
        duration=durata_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )
    for im in immagini + quant:
        im.close()
    return dest


def scrivi_miniatura(fotogramma: Path, dest: Path, larghezza: int = 640) -> Path | None:
    if not fotogramma.is_file():
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(fotogramma) as im:
        im = im.convert("RGB")
        h = int(im.height * (larghezza / im.width))
        im.resize((larghezza, h), Image.Resampling.LANCZOS).save(dest, "JPEG", quality=85, optimize=True)
    return dest


def scrivi_video(fotogrammi: list[Path], dest_mp4: Path, fps: float = 2.5) -> dict[str, Path]:
    """Genera un MP4 se ffmpeg è nel PATH. Non è obbligatorio."""
    esistenti = [p for p in fotogrammi if p.is_file()]
    out: dict[str, Path] = {}
    if len(esistenti) < 2 or not shutil.which("ffmpeg"):
        return out
    dest_mp4.parent.mkdir(parents=True, exist_ok=True)
    elenco = dest_mp4.with_suffix(".txt")
    elenco.write_text("".join(f"file '{p.resolve()}'\nduration {1.0 / fps:.3f}\n" for p in esistenti), encoding="utf-8")
    # L'ultimo fotogramma va ripetuto, altrimenti ffmpeg lo mostra un attimo solo.
    with elenco.open("a", encoding="utf-8") as f:
        f.write(f"file '{esistenti[-1].resolve()}'\n")

    def run(args) -> bool:
        r = subprocess.run(args, capture_output=True, text=True)
        return r.returncode == 0

    if run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(elenco),
        "-vf", "fps=10,scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p", "-movflags", "+faststart",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(dest_mp4),
    ]):
        out["mp4"] = dest_mp4
    try:
        elenco.unlink()
    except OSError:
        pass
    return out
