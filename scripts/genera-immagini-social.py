#!/usr/bin/env python3
"""Genera immagini Instagram (post 1080x1080 e story 1080x1920) a partire
dalla cover di un articolo del sito.

Template istituzionale:
  - Header blu #003366 con logo + brand "Protezione Civile - Genzano di Roma"
  - Cover articolo ridimensionata (preserva proporzioni)
  - Footer con titolo articolo + URL del sito

Output (accanto ai testi delle bozze, comodo da scaricare insieme via mobile):
  social-bozze/<slug>/instagram-post.jpg         (1080x1080, 1 sola foto)
  social-bozze/<slug>/instagram-post-N.jpg       (carosello, 2-10 foto)
  social-bozze/<slug>/instagram-story.jpg        (1080x1920, sempre 1)

Formato: JPEG quality 90. Universalmente accettato da Instagram, Facebook,
X, Telegram, LinkedIn. WebP non funziona per upload su Instagram (web e
app mobile lo rifiutano). PNG sarebbe accettato ma 3-5x più pesante senza
benefici visibili sul nostro template (sfondi piatti + testo).

Uso:
  python3 scripts/genera-immagini-social.py content/comunicazioni/2026-04-20-articolo.md
  python3 scripts/genera-immagini-social.py --all
  python3 scripts/genera-immagini-social.py --force <articolo>

Dipendenze: Pillow (pip install Pillow), font-liberation (apt: fonts-liberation).
"""

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CONTENT_COMUNICAZIONI = ROOT / "content" / "comunicazioni"
IMAGES_DIR = ROOT / "static" / "images"
BOZZE_DIR = ROOT / "social-bozze"  # Output: stessa cartella dei testi (instagram.txt ecc.)
LOGO_PATH = IMAGES_DIR / "logo-pc-genzano.png"


def slug_dir(slug: str) -> Path:
    """Cartella di output per un dato slug. Crea se non esiste."""
    d = BOZZE_DIR / slug
    d.mkdir(parents=True, exist_ok=True)
    return d

PRIMARY = (0, 51, 102)        # #003366 blu istituzionale
PRIMARY_DARK = (0, 26, 51)    # #001a33
WHITE = (255, 255, 255)
LIGHT_BG = (247, 249, 252)    # #f7f9fc
TEXT_DARK = (23, 50, 77)      # #17324D


def find_font(weight: str = "Bold") -> Path:
    candidates = [
        f"/usr/share/fonts/truetype/liberation/LiberationSans-{weight}.ttf",
        f"/usr/share/fonts/liberation/LiberationSans-{weight}.ttf",
        f"/usr/share/fonts/truetype/liberation2/LiberationSans-{weight}.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if Path(c).is_file():
            return Path(c)
    raise RuntimeError(
        "Font Liberation Sans non trovato. Su Ubuntu: sudo apt install fonts-liberation"
    )


def parse_frontmatter(testo: str) -> tuple[dict, str]:
    if not testo.startswith("---\n"):
        return {}, testo
    fine = testo.find("\n---", 4)
    if fine < 0:
        return {}, testo
    raw_fm = testo[4:fine].strip()
    body = testo[fine + 4:].lstrip("\n")
    fm = {}
    for riga in raw_fm.split("\n"):
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", riga)
        if m:
            chiave = m.group(1)
            valore = m.group(2).strip()
            if valore.startswith('"') and valore.endswith('"'):
                valore = valore[1:-1]
            fm[chiave] = valore
    return fm, body


def wrap_testo(draw: ImageDraw.ImageDraw, testo: str, font: ImageFont.FreeTypeFont,
               larghezza_max: int) -> list[str]:
    """Spezza un testo in righe che entrano nella larghezza_max."""
    parole = testo.split()
    if not parole:
        return []
    righe = []
    riga = parole[0]
    for parola in parole[1:]:
        candidato = riga + " " + parola
        bbox = draw.textbbox((0, 0), candidato, font=font)
        if bbox[2] - bbox[0] <= larghezza_max:
            riga = candidato
        else:
            righe.append(riga)
            riga = parola
    righe.append(riga)
    return righe


def crea_post_quadrato(cover_path: Path, titolo: str, out_path: Path) -> Path:
    """Genera l'immagine 1080x1080 per Instagram feed nel path indicato."""
    W, H = 1080, 1080
    HEADER_H = 140
    FOOTER_H = 280

    img = Image.new("RGB", (W, H), LIGHT_BG)
    draw = ImageDraw.Draw(img)

    # Header blu con logo + brand
    draw.rectangle([(0, 0), (W, HEADER_H)], fill=PRIMARY)
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_h = 90
        logo_w = int(logo.width * (logo_h / logo.height))
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        img.paste(logo, (40, (HEADER_H - logo_h) // 2), logo)

    font_brand_lg = ImageFont.truetype(str(find_font("Bold")), 32)
    font_brand_sm = ImageFont.truetype(str(find_font("Regular")), 20)
    draw.text((150, 35), "Protezione Civile", font=font_brand_lg, fill=WHITE)
    draw.text((150, 80), "Gruppo Comunale Volontari — Genzano di Roma",
              font=font_brand_sm, fill=WHITE)

    # Cover articolo
    cover_area_h = H - HEADER_H - FOOTER_H  # 660
    if cover_path.exists():
        cover = Image.open(cover_path).convert("RGB")
        # Crop al rapporto necessario (W/cover_area_h ≈ 1080/660 = 1.636).
        # IMPORTANTE: le cover tipografiche del sito hanno il titolo
        # allineato a SINISTRA. Un crop centrato taglierebbe le prime
        # lettere. Usiamo offset=0 (preserve-left) per mantenere intatto
        # il bordo sinistro. Per le foto evento il soggetto è di solito
        # nei 2/3 sinistri, quindi anche per quelle preserve-left
        # funziona meglio del crop centrato.
        target_ratio = W / cover_area_h
        src_ratio = cover.width / cover.height
        if src_ratio > target_ratio:
            # cover troppo larga: tieni il bordo sinistro, taglia da destra
            new_w = int(cover.height * target_ratio)
            cover = cover.crop((0, 0, new_w, cover.height))
        else:
            # cover troppo alta: crop centrato verticalmente
            new_h = int(cover.width / target_ratio)
            offset = (cover.height - new_h) // 2
            cover = cover.crop((0, offset, cover.width, offset + new_h))
        cover = cover.resize((W, cover_area_h), Image.LANCZOS)
        img.paste(cover, (0, HEADER_H))

    # Footer con titolo + URL
    draw.rectangle([(0, H - FOOTER_H), (W, H)], fill=LIGHT_BG)
    font_titolo = ImageFont.truetype(str(find_font("Bold")), 38)
    font_url = ImageFont.truetype(str(find_font("Regular")), 22)

    # Titolo wrap fino a 4 righe
    righe = wrap_testo(draw, titolo, font_titolo, W - 120)
    righe = righe[:4]
    y = H - FOOTER_H + 40
    for r in righe:
        draw.text((60, y), r, font=font_titolo, fill=PRIMARY)
        y += 50

    # URL in basso
    draw.text((60, H - 60), "protezionecivilegenzano.it",
              font=font_url, fill=TEXT_DARK)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "JPEG", quality=90, optimize=True, progressive=True)
    return out_path


def crea_story_verticale(cover_path: Path, titolo: str, descrizione: str,
                         out_path: Path) -> Path:
    """Genera l'immagine 1080x1920 per Instagram story / reel nel path indicato."""
    W, H = 1080, 1920
    HEADER_H = 240
    FOOTER_H = 200

    img = Image.new("RGB", (W, H), LIGHT_BG)
    draw = ImageDraw.Draw(img)

    # Header blu
    draw.rectangle([(0, 0), (W, HEADER_H)], fill=PRIMARY)
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_h = 130
        logo_w = int(logo.width * (logo_h / logo.height))
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        img.paste(logo, (60, (HEADER_H - logo_h) // 2), logo)

    font_brand_lg = ImageFont.truetype(str(find_font("Bold")), 44)
    font_brand_sm = ImageFont.truetype(str(find_font("Regular")), 26)
    draw.text((220, 70), "Protezione Civile", font=font_brand_lg, fill=WHITE)
    draw.text((220, 130), "Gruppo Comunale Volontari", font=font_brand_sm, fill=WHITE)
    draw.text((220, 165), "Genzano di Roma", font=font_brand_sm, fill=WHITE)

    # Cover articolo (rapporto 16:9 originale, ridimensionata 1080 di larghezza).
    # Stesso preserve-left del template post per mantenere intatto il titolo
    # allineato a sinistra delle cover tipografiche.
    cover_y = HEADER_H + 40
    cover_h = 600
    if cover_path.exists():
        cover = Image.open(cover_path).convert("RGB")
        target_ratio = W / cover_h
        src_ratio = cover.width / cover.height
        if src_ratio > target_ratio:
            new_w = int(cover.height * target_ratio)
            cover = cover.crop((0, 0, new_w, cover.height))
        else:
            new_h = int(cover.width / target_ratio)
            offset = (cover.height - new_h) // 2
            cover = cover.crop((0, offset, cover.width, offset + new_h))
        cover = cover.resize((W, cover_h), Image.LANCZOS)
        img.paste(cover, (0, cover_y))

    # Area testo (titolo + descrizione)
    testo_y = cover_y + cover_h + 60
    font_titolo = ImageFont.truetype(str(find_font("Bold")), 56)
    font_desc = ImageFont.truetype(str(find_font("Regular")), 30)

    # Titolo
    righe_t = wrap_testo(draw, titolo, font_titolo, W - 140)
    righe_t = righe_t[:5]
    y = testo_y
    for r in righe_t:
        draw.text((70, y), r, font=font_titolo, fill=PRIMARY)
        y += 72

    # Spazio + descrizione
    y += 40
    if descrizione:
        # Limita la descrizione a ~250 char
        desc_breve = descrizione[:250]
        if len(descrizione) > 250:
            desc_breve = desc_breve.rsplit(" ", 1)[0] + "…"
        righe_d = wrap_testo(draw, desc_breve, font_desc, W - 140)
        # Limita a 6 righe massimo
        righe_d = righe_d[:6]
        for r in righe_d:
            draw.text((70, y), r, font=font_desc, fill=TEXT_DARK)
            y += 42

    # Footer "Leggi sul sito"
    draw.rectangle([(0, H - FOOTER_H), (W, H)], fill=PRIMARY)
    font_cta = ImageFont.truetype(str(find_font("Bold")), 36)
    font_url2 = ImageFont.truetype(str(find_font("Regular")), 28)
    draw.text((70, H - FOOTER_H + 50), "→ Leggi sul sito", font=font_cta, fill=WHITE)
    draw.text((70, H - FOOTER_H + 110), "protezionecivilegenzano.it",
              font=font_url2, fill=WHITE)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "JPEG", quality=90, optimize=True, progressive=True)
    return out_path


def estrai_foto_inline(body: str) -> list[Path]:
    """Estrae tutti i path delle foto inline dallo shortcode {{< foto src="..." >}}.
    Ritorna lista di Path assoluti (relativi a static/).
    Supporta sia {{< foto >}} che {{% foto %}}."""
    pattern = re.compile(
        r'\{\{[<%]\s*foto\s+(?:[^>%]*?\s+)?src=["\']([^"\']+)["\']',
        re.IGNORECASE,
    )
    risultati = []
    for src in pattern.findall(body):
        # Path relativi (/images/...) -> static/images/...
        risultati.append(ROOT / "static" / src.lstrip("/"))
    return risultati


def crea_cover_tipografica(art_path: Path) -> Path | None:
    """Se la cover dell'articolo non esiste, genera una cover tipografica
    auto chiamando scripts/genera-cover.py. Ritorna il path della cover
    creata o None se la generazione fallisce."""
    cover_script = ROOT / "scripts" / "genera-cover.py"
    if not cover_script.exists():
        return None
    try:
        subprocess.run(
            ["python3", str(cover_script), str(art_path)],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"  ERRORE genera-cover.py: {e.stderr[:300]}", file=sys.stderr)
        return None
    # genera-cover.py salva in static/images/<slug>.webp
    return IMAGES_DIR / f"{art_path.stem}.webp"


def estrai_articolo(path: Path) -> dict | None:
    try:
        testo = path.read_text(encoding="utf-8")
    except OSError:
        return None
    fm, body = parse_frontmatter(testo)
    if fm.get("draft", "").lower() in ("true", "yes", "1"):
        return None
    m = re.match(r"(\d{4}-\d{2}-\d{2})", fm.get("date", ""))
    if not m:
        return None
    if datetime.date.fromisoformat(m.group(1)) > datetime.date.today():
        return None

    # Cover principale dal frontmatter
    cover_rel = fm.get("image", "")
    cover_path = None
    if cover_rel:
        cover_path = ROOT / "static" / cover_rel.lstrip("/")
        if not cover_path.exists():
            cover_path = None  # path nel frontmatter ma file mancante

    # Se cover assente, prova a generare quella tipografica al volo
    if cover_path is None:
        cover_path = crea_cover_tipografica(path)
        if cover_path is None or not cover_path.exists():
            return None

    # Foto inline dal corpo (per il carosello Instagram)
    foto_inline = estrai_foto_inline(body)

    # Carosello = cover + inline (deduplicato, mantenendo ordine)
    carousel = [cover_path] + foto_inline
    seen = set()
    carousel_unique = []
    for p in carousel:
        if not p.exists():
            continue
        chiave = str(p.resolve())
        if chiave in seen:
            continue
        seen.add(chiave)
        carousel_unique.append(p)
    # Limite Instagram: 10 immagini per carosello
    carousel_unique = carousel_unique[:10]

    return {
        "slug": path.stem,
        "title": fm.get("title", ""),
        "description": fm.get("description", ""),
        "cover": cover_path,
        "carousel": carousel_unique,
    }


def trova_articoli_pubblicati() -> list[Path]:
    risultati = []
    oggi = datetime.date.today()
    for p in sorted(CONTENT_COMUNICAZIONI.glob("*.md")):
        if p.name == "_index.md":
            continue
        try:
            testo = p.read_text(encoding="utf-8")
        except OSError:
            continue
        fm, _ = parse_frontmatter(testo)
        if fm.get("draft", "").lower() in ("true", "yes", "1"):
            continue
        m = re.match(r"(\d{4}-\d{2}-\d{2})", fm.get("date", ""))
        if not m or datetime.date.fromisoformat(m.group(1)) > oggi:
            continue
        risultati.append(p)
    return risultati


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("articolo", nargs="?", help="Path .md singolo")
    parser.add_argument("--all", action="store_true", help="Tutti pubblicati")
    parser.add_argument("--force", action="store_true", help="Sovrascrivi esistenti")
    args = parser.parse_args()

    if args.articolo:
        articoli = [Path(args.articolo)]
    elif args.all:
        articoli = trova_articoli_pubblicati()
    else:
        print("Specifica un articolo o --all", file=sys.stderr)
        return 2

    ok = 0
    saltati = 0
    for path in articoli:
        art = estrai_articolo(path)
        if not art:
            print(f"  SKIP (non pubblicato o senza cover): {path.name}", file=sys.stderr)
            saltati += 1
            continue

        n_foto = len(art["carousel"])
        out_dir = slug_dir(art["slug"])
        story_path = out_dir / "instagram-story.jpg"

        # Naming:
        #   1 sola foto -> instagram-post.jpg
        #   2+ foto    -> instagram-post-1.jpg, instagram-post-2.jpg, ...
        if n_foto == 1:
            target = out_dir / "instagram-post.jpg"
            if not args.force and target.exists() and story_path.exists():
                print(f"  GIÀ PRESENTE (--force per ri-generare): {art['slug']}",
                      file=sys.stderr)
                saltati += 1
                continue
        else:
            target_1 = out_dir / "instagram-post-1.jpg"
            if not args.force and target_1.exists() and story_path.exists():
                print(f"  GIÀ PRESENTE carosello (--force per ri-generare): {art['slug']}",
                      file=sys.stderr)
                saltati += 1
                continue

        # --force: pulisci eventuali immagini precedenti (incluse vecchie .webp
        # da prima del 2 maggio 2026 quando IG non accettava il formato)
        if args.force:
            for old in out_dir.glob("instagram-post*.webp"):
                old.unlink()
            for old in out_dir.glob("instagram-post*.jpg"):
                old.unlink()

        try:
            if n_foto == 1:
                crea_post_quadrato(art["carousel"][0], art["title"],
                                   out_dir / "instagram-post.jpg")
            else:
                for idx, foto in enumerate(art["carousel"], 1):
                    crea_post_quadrato(foto, art["title"],
                                       out_dir / f"instagram-post-{idx}.jpg")

            # Story: sempre 1 sola, usa la cover principale
            crea_story_verticale(art["cover"], art["title"], art["description"],
                                 story_path)

            tipo = "singolo" if n_foto == 1 else f"carosello x{n_foto}"
            print(f"  ✓ {art['slug']} ({tipo})", file=sys.stderr)
            ok += 1
        except Exception as e:
            print(f"  ERRORE {art['slug']}: {e}", file=sys.stderr)

    print(f"\nFatto. OK={ok}, saltati={saltati}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
