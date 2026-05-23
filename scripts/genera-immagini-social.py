#!/usr/bin/env python3
"""Genera immagini Instagram (post 1080x1080 e story 1080x1920) a partire
dalla cover di un articolo del sito.

Template istituzionale:
  - Header blu #003366 con logo + brand "Protezione Civile - Genzano di Roma"
  - Cover articolo ridimensionata (preserva proporzioni)
  - Footer con titolo articolo + URL del sito

Design (formato 4:5 = 1080x1350, mai ritagliato neppure nella griglia profilo IG):
  - Slide 1 / post singolo: card-titolo verticale nativa (brand + badge + titolo)
  - Slide foto: immagine INTERA nitida (mai tagliata) su sfondo sfocato di se
    stessa, card con angoli arrotondati + ombra morbida + barra brand
  - Story 1080x1920: stessa estetica, sfondo sfocato + card intera + testo + CTA

Output (accanto ai testi delle bozze, comodo da scaricare insieme via mobile):
  social-bozze/<slug>/feed-post.jpg          (1080x1350, post singolo per il FEED)
  social-bozze/<slug>/feed-carosello-N.jpg   (1080x1350, carosello per il FEED)
  social-bozze/<slug>/storia.jpg             (1080x1920, per le STORIE 24h)

Nomi a prova di errore: "feed-" = post nel feed (Instagram + Facebook),
"storia" = storia verticale 24h. Il numero del carosello è l'ordine di caricamento.

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

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
CONTENT_COMUNICAZIONI = ROOT / "content" / "comunicazioni"
IMAGES_DIR = ROOT / "static" / "images"
BOZZE_DIR = ROOT / "social-bozze"  # Output: stessa cartella dei testi (instagram.txt ecc.)
LOGO_PATH = IMAGES_DIR / "logo-pc-genzano.png"
SITE_BASE = "https://www.protezionecivilegenzano.it"
# Font ufficiale del design system .italia (Titillium Web), già nel repo.
TITILLIUM_DIR = ROOT / "static" / "vendor" / "bootstrap-italia" / "fonts" / "Titillium_Web"


def slug_to_path(slug: str) -> Path:
    """Da slug 'AAAA-MM-GG-titolo' ricava la struttura nidificata
    AAAA/MM/AAAA-MM-GG-titolo per navigabilità in social-bozze/.

    Esempi:
      '2026-05-15-giro-italia' -> Path('2026/05/2026-05-15-giro-italia')
      'slug-senza-data'        -> Path('slug-senza-data')  (fallback piatto)

    Storia: il 16/05/2026 la cartella social-bozze/ aveva 103 cartelle
    piatte impossibili da navigare da mobile. Migrazione a struttura
    anno/mese per allineare alla logica della pagina /comunicazioni/.
    """
    parts = slug.split('-', 3)
    if (len(parts) >= 4
            and len(parts[0]) == 4 and parts[0].isdigit()
            and len(parts[1]) == 2 and parts[1].isdigit()
            and len(parts[2]) == 2 and parts[2].isdigit()):
        return Path(parts[0]) / parts[1] / slug
    return Path(slug)


def slug_dir(slug: str) -> Path:
    """Cartella di output per un dato slug. Crea se non esiste.
    Usa struttura nidificata social-bozze/AAAA/MM/AAAA-MM-GG-slug/."""
    d = BOZZE_DIR / slug_to_path(slug)
    d.mkdir(parents=True, exist_ok=True)
    return d

PRIMARY = (0, 51, 102)        # #003366 blu istituzionale
PRIMARY_DARK = (0, 26, 51)    # #001a33
WHITE = (255, 255, 255)
LIGHT_BG = (247, 249, 252)    # #f7f9fc
TEXT_DARK = (23, 50, 77)      # #17324D


def find_font(weight: str = "Bold") -> Path:
    """Restituisce il font ufficiale .italia (Titillium Web) dal repo; in mancanza,
    ripiega su Liberation Sans di sistema. Pillow legge solo .ttf/.otf (non .woff)."""
    titillium = {"Bold": "700", "Semibold": "600", "Regular": "regular"}.get(weight)
    if titillium:
        p = TITILLIUM_DIR / f"titillium-web-v10-latin-ext_latin-{titillium}.ttf"
        if p.is_file():
            return p
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
        "Font non trovato: né Titillium Web nel repo né Liberation Sans di sistema."
    )


def parse_frontmatter(testo: str) -> tuple[dict, str]:
    if not testo.startswith("---\n"):
        return {}, testo
    fine = testo.find("\n---", 4)
    if fine < 0:
        return {}, testo
    raw_fm = testo[4:fine].strip()
    body = testo[fine + 4:].lstrip("\n")

    def _strip_q(v: str) -> str:
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ("\"", "'"):
            v = v[1:-1]
        return v

    fm = {}
    chiave_lista = None  # ultima chiave a valore vuoto (possibile lista YAML)
    for riga in raw_fm.split("\n"):
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        # Voce di lista semplice "  - valore" sotto una chiave a valore vuoto.
        m_item = re.match(r"^\s+-\s+(.+)$", riga)
        if chiave_lista is not None and m_item:
            fm[chiave_lista].append(_strip_q(m_item.group(1)))
            continue
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", riga)
        if m:
            chiave, valore = m.group(1), m.group(2).strip()
            if valore == "":
                fm[chiave] = []          # possibile inizio di lista
                chiave_lista = chiave
            else:
                fm[chiave] = _strip_q(valore)
                chiave_lista = None
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


# ---------------------------------------------------------------------------
# Helper grafici — fit-contain (MAI ritaglio del contenuto), sfondo sfocato,
# card arrotondate con ombra, velo gradiente, barra brand, palette badge.
# ---------------------------------------------------------------------------

# Palette badge coerente con il sito (CLAUDE.md / custom.css).
BADGE_COLORI = {
    "allerta": (217, 54, 79), "emergenza": (127, 29, 29), "avviso": (180, 83, 9),
    "evento": (192, 38, 211), "comunicazione": (0, 51, 102),
    "radiocomunicazioni": (3, 105, 161), "informazione": (7, 89, 133),
    "prevenzione": (21, 128, 61), "esercitazione": (194, 65, 12),
    "aggiornamento": (67, 56, 202), "formazione": (124, 58, 237),
    "volontariato": (180, 83, 9), "attività": (14, 116, 144),
    "attivita": (14, 116, 144),
}
ACCENT = (255, 190, 46)       # giallo istituzionale #ffbe2e


def _badge_colore(badge: str) -> tuple:
    return BADGE_COLORI.get((badge or "").strip().lower(), PRIMARY)


def fit_size(src_w: int, src_h: int, box_w: int, box_h: int) -> tuple[int, int]:
    """Dimensioni per contenere l'immagine dentro box mantenendo le proporzioni.
    Nessun ritaglio: l'immagine intera resta visibile (contain)."""
    r = min(box_w / src_w, box_h / src_h)
    return max(1, round(src_w * r)), max(1, round(src_h * r))


def gradiente_verticale(W: int, H: int, top: tuple, bottom: tuple) -> Image.Image:
    """Sfondo a gradiente verticale (1 colonna ridimensionata = veloce)."""
    col = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / max(1, H - 1)
        col.putpixel((0, y), tuple(round(top[i] + (bottom[i] - top[i]) * t)
                                   for i in range(3)))
    return col.resize((W, H), Image.BILINEAR)


def sfondo_sfocato(src: Image.Image, W: int, H: int,
                   blur: int = 48, scurisci: float = 0.5) -> Image.Image:
    """Sfondo W×H ricavato dall'immagine stessa: scalata a COPRIRE, sfocata e
    scurita, per riempire le bande senza vuoti. NB: solo lo sfondo decorativo
    viene coperto; l'immagine nitida sovrapposta resta SEMPRE intera."""
    r = max(W / src.width, H / src.height)
    nw, nh = max(1, round(src.width * r)), max(1, round(src.height * r))
    big = src.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - W) // 2, (nh - H) // 2
    bg = big.crop((left, top, left + W, top + H)).filter(ImageFilter.GaussianBlur(blur))
    return Image.blend(bg, Image.new("RGB", (W, H), PRIMARY_DARK), scurisci)


def _mask_arrotondata(size: tuple, raggio: int) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([(0, 0), (size[0] - 1, size[1] - 1)],
                                        radius=raggio, fill=255)
    return m


def incolla_card(base: Image.Image, foto: Image.Image, x: int, y: int,
                 raggio: int = 28, ombra: int = 22) -> None:
    """Incolla 'foto' su 'base' (RGBA) come card: angoli arrotondati, cornice
    bianca sottile, ombra morbida. base modificata in place. Nessun ritaglio."""
    foto = foto.convert("RGB")
    mask = _mask_arrotondata(foto.size, raggio)
    # Ombra morbida
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    blocco = Image.new("RGBA", foto.size, (0, 20, 40, 135))
    blocco.putalpha(mask)
    sh.paste(blocco, (x, y + 12), blocco)
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(ombra)))
    # Cornice bianca
    b = 6
    cornice = Image.new("RGBA", (foto.width + b * 2, foto.height + b * 2), (0, 0, 0, 0))
    bianco = Image.new("RGBA", cornice.size, (255, 255, 255, 235))
    bianco.putalpha(_mask_arrotondata(cornice.size, raggio + b))
    base.alpha_composite(bianco, (x - b, y - b))
    # Foto
    fr = foto.convert("RGBA")
    fr.putalpha(mask)
    base.alpha_composite(fr, (x, y))


def scrim(W: int, h: int, dall_alto: bool = True, alpha_max: int = 215,
          colore: tuple = (0, 18, 38)) -> Image.Image:
    """Velo gradiente verticale (per la leggibilità del testo sulle foto)."""
    col = Image.new("RGBA", (1, h), (0, 0, 0, 0))
    for y in range(h):
        t = (1 - y / max(1, h - 1)) if dall_alto else (y / max(1, h - 1))
        col.putpixel((0, y), (*colore, int(alpha_max * t)))
    return col.resize((W, h))


def _barra_brand(base: Image.Image, W: int) -> None:
    """Logo + denominazione in alto su un velo scuro. base RGBA in place."""
    base.alpha_composite(scrim(W, 210, dall_alto=True, alpha_max=205), (0, 0))
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        lh = 96
        logo = logo.resize((round(logo.width * (lh / logo.height)), lh), Image.LANCZOS)
        base.alpha_composite(logo, (60, 42))
    d = ImageDraw.Draw(base)
    d.text((176, 50), "PROTEZIONE CIVILE",
           font=ImageFont.truetype(str(find_font("Bold")), 38), fill=WHITE)
    d.text((176, 100), "Gruppo Comunale Volontari — Genzano di Roma",
           font=ImageFont.truetype(str(find_font("Regular")), 24), fill=(220, 232, 245))


def crea_slide_titolo(titolo: str, badge: str, out_path: Path,
                      W: int = 1080, H: int = 1350) -> Path:
    """Slide 1 del carosello / post singolo: card-titolo verticale nativa 4:5.
    Costruita a misura: riempie perfettamente, senza ritagli né bande."""
    base = _sfondo_titolo(W, H)
    _barra_brand(base, W)
    d = ImageDraw.Draw(base)
    d.line([(60, 190), (W - 60, 190)], fill=(255, 255, 255, 55), width=2)

    y = 250
    if badge:
        ft = ImageFont.truetype(str(find_font("Bold")), 30)
        txt = badge.upper()
        tb = d.textbbox((0, 0), txt, font=ft)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        px, py = 30, 16
        d.rounded_rectangle([(60, y), (60 + tw + px * 2, y + th + py * 2)],
                            radius=(th + py * 2) // 2, fill=_badge_colore(badge))
        d.text((60 + px, y + py - tb[1]), txt, font=ft, fill=WHITE)
        y += th + py * 2 + 56

    ft_tit = ImageFont.truetype(str(find_font("Bold")), 74)
    righe = wrap_testo(d, titolo, ft_tit, W - 200)[:6]
    line_h = 90
    blocco_h = len(righe) * line_h
    area_top, area_bot = y, H - 200
    ty = area_top + max(0, (area_bot - area_top - blocco_h) // 2)
    d.rectangle([(60, ty + 8), (72, ty + blocco_h - 12)], fill=ACCENT)
    for r in righe:
        d.text((100, ty), r, font=ft_tit, fill=WHITE)
        ty += line_h

    base.alpha_composite(scrim(W, 170, dall_alto=False, alpha_max=150), (0, H - 170))
    d.text((60, H - 92), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True, progressive=True)
    return out_path


def crea_slide_foto(foto_path: Path, out_path: Path,
                    W: int = 1080, H: int = 1350) -> Path:
    """Slide foto del carosello: l'immagine INTERA (mai tagliata) nitida su uno
    sfondo sfocato ricavato da se stessa, in una card arrotondata con ombra,
    barra brand in alto e URL in basso."""
    foto = Image.open(foto_path).convert("RGB")
    base = sfondo_sfocato(foto, W, H).convert("RGBA")

    area_top, area_bot = 210, H - 150
    box_w, box_h = W - 120, area_bot - area_top - 40
    fw, fh = fit_size(foto.width, foto.height, box_w, box_h)
    foto_fit = foto.resize((fw, fh), Image.LANCZOS)
    x = (W - fw) // 2
    yy = area_top + (area_bot - area_top - fh) // 2
    incolla_card(base, foto_fit, x, yy)

    _barra_brand(base, W)
    base.alpha_composite(scrim(W, 150, dall_alto=False, alpha_max=175), (0, H - 150))
    ImageDraw.Draw(base).text(
        (60, H - 92), "protezionecivilegenzano.it",
        font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True, progressive=True)
    return out_path


def _sfondo_titolo(W: int, H: int) -> Image.Image:
    """Sfondo blu istituzionale a gradiente + trama diagonale leggera (RGBA)."""
    base = gradiente_verticale(W, H, PRIMARY_DARK, PRIMARY).convert("RGBA")
    trama = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dt = ImageDraw.Draw(trama)
    for x in range(-H, W, 48):
        dt.line([(x, 0), (x + H, H)], fill=(255, 255, 255, 6), width=2)
    base.alpha_composite(trama)
    return base


def crea_slide_citazione(testo: str, out_path: Path,
                         W: int = 1080, H: int = 1350) -> Path:
    """Slide 'citazione': una frase forte dell'articolo, grande, tra virgolette.
    Testo preso dal frontmatter (social_citazione), mai inventato."""
    base = _sfondo_titolo(W, H)
    _barra_brand(base, W)
    d = ImageDraw.Draw(base)
    # Virgoletta decorativa grande in accento
    d.text((66, 232), "“",
           font=ImageFont.truetype(str(find_font("Bold")), 180), fill=ACCENT)
    ft = ImageFont.truetype(str(find_font("Semibold")), 60)
    righe = wrap_testo(d, testo, ft, W - 200)[:8]
    line_h = 80
    blocco_h = len(righe) * line_h
    area_top, area_bot = 440, H - 200
    ty = area_top + max(0, (area_bot - area_top - blocco_h) // 2)
    for r in righe:
        d.text((100, ty), r, font=ft, fill=WHITE)
        ty += line_h
    base.alpha_composite(scrim(W, 170, dall_alto=False, alpha_max=150), (0, H - 170))
    d.text((60, H - 92), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True, progressive=True)
    return out_path


def crea_slide_punti(punti: list, out_path: Path,
                     W: int = 1080, H: int = 1350) -> Path:
    """Slide 'punti chiave': elenco di 2-5 punti brevi dall'articolo (frontmatter
    social_punti). Marcatore accento + testo, mai inventato."""
    base = _sfondo_titolo(W, H)
    _barra_brand(base, W)
    d = ImageDraw.Draw(base)
    d.line([(60, 190), (W - 60, 190)], fill=(255, 255, 255, 55), width=2)
    d.text((60, 238), "IN SINTESI",
           font=ImageFont.truetype(str(find_font("Bold")), 36), fill=ACCENT)
    ft = ImageFont.truetype(str(find_font("Semibold")), 46)
    y = 340
    for p in punti[:5]:
        righe = wrap_testo(d, p, ft, W - 230)[:3]
        d.ellipse([(64, y + 18), (90, y + 44)], fill=ACCENT)
        for r in righe:
            d.text((120, y), r, font=ft, fill=WHITE)
            y += 60
        y += 30
    base.alpha_composite(scrim(W, 170, dall_alto=False, alpha_max=150), (0, H - 170))
    d.text((60, H - 92), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True, progressive=True)
    return out_path


def crea_story_verticale(cover_path: Path, titolo: str, descrizione: str,
                         out_path: Path, badge: str = "",
                         hero_path: Path = None) -> Path:
    """Story / reel 1080×1920: sfondo sfocato + badge + titolo + descrizione + CTA.
    Se l'articolo ha una foto reale (es. locandina) la mette in evidenza come
    card intera (mai tagliata); altrimenti resta una card-titolo nativa pulita.
    Niente doppioni di badge/titolo. Testo fuori dalle safe-zone UI di IG/FB."""
    W, H = 1080, 1920
    featured = (hero_path if (hero_path and Path(hero_path).exists()) else None)
    bg_path = featured or cover_path
    bg_src = (Image.open(bg_path).convert("RGB")
              if bg_path and Path(bg_path).exists() else None)
    base = (sfondo_sfocato(bg_src, W, H) if bg_src
            else gradiente_verticale(W, H, PRIMARY_DARK, PRIMARY)).convert("RGBA")

    _barra_brand(base, W)
    d = ImageDraw.Draw(base)

    # Badge sotto la barra brand (una volta sola)
    testo_y = 250
    if badge:
        ft = ImageFont.truetype(str(find_font("Bold")), 30)
        txt = badge.upper()
        tb = d.textbbox((0, 0), txt, font=ft)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        px, py = 30, 16
        d.rounded_rectangle([(70, testo_y), (70 + tw + px * 2, testo_y + th + py * 2)],
                            radius=(th + py * 2) // 2, fill=_badge_colore(badge))
        d.text((70 + px, testo_y + py - tb[1]), txt, font=ft, fill=WHITE)
        testo_y += th + py * 2 + 44

    # Foto reale in evidenza (NON la cover tipografica, che ripeterebbe titolo).
    if featured:
        fsrc = Image.open(featured).convert("RGB")
        box_w, box_h = W - 140, 720
        fw, fh = fit_size(fsrc.width, fsrc.height, box_w, box_h)
        cov = fsrc.resize((fw, fh), Image.LANCZOS)
        cy = testo_y
        incolla_card(base, cov, (W - fw) // 2, cy + (box_h - fh) // 2)
        testo_y = cy + box_h + 56

    ft_tit = ImageFont.truetype(str(find_font("Bold")), 58)
    for r in wrap_testo(d, titolo, ft_tit, W - 140)[:5]:
        d.text((70, testo_y), r, font=ft_tit, fill=WHITE)
        testo_y += 74
    testo_y += 26
    if descrizione:
        desc = descrizione[:240]
        if len(descrizione) > 240:
            desc = desc.rsplit(" ", 1)[0] + "…"
        ft_d = ImageFont.truetype(str(find_font("Regular")), 30)
        for r in wrap_testo(d, desc, ft_d, W - 140)[:6]:
            d.text((70, testo_y), r, font=ft_d, fill=(223, 234, 245))
            testo_y += 44

    # CTA footer (dentro la safe-zone bassa)
    base.alpha_composite(scrim(W, 230, dall_alto=False, alpha_max=210), (0, H - 230))
    d.text((70, H - 158), "→ Leggi sul sito",
           font=ImageFont.truetype(str(find_font("Bold")), 38), fill=WHITE)
    d.text((70, H - 100), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Regular")), 30), fill=(223, 234, 245))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True, progressive=True)
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


def scrivi_readme(out_dir: Path, art: dict, n_immagini: int) -> None:
    """Scrive README.md con la mappa 'a prova di errore' delle immagini + testi.
    Unico proprietario del README della cartella (genera-social.py non lo scrive)."""
    if n_immagini <= 1:
        riga_feed = ("| `feed-post.jpg` | FEED Instagram + Facebook — post con "
                     "una sola immagine (1080×1350) |")
    else:
        nomi = ", ".join(f"`feed-carosello-{i}.jpg`" for i in range(1, n_immagini + 1))
        riga_feed = (f"| {nomi} | FEED Instagram + Facebook — carosello: "
                     f"caricale **tutte, in ordine** (1080×1350) |")
    url = f"{SITE_BASE}/comunicazioni/{art['slug']}/"
    testo = f"""# Immagini e testi social per «{art['title']}»

- **Articolo**: {url}
- **Data**: {art.get('date', '')}
- **Badge**: {art.get('badge', '')}

## Dove va ogni file (a prova di errore)

Regola: **`feed-` = post nel FEED** (Instagram + Facebook), **`storia` = STORIA 24h**.
Il numero del carosello è l'ordine di caricamento.

| File | Dove si pubblica |
|---|---|
{riga_feed}
| `storia.jpg` | STORIE Instagram + Facebook — verticale, sparisce dopo 24h (1080×1920) |
| `instagram.txt` | testo per Instagram |
| `facebook.txt` | testo per Facebook (anteprima OG dall'URL) |
| `x.txt` | testo per X — max 280 caratteri |
| `telegram.txt` | testo per Telegram (Markdown) |

I **testi** sono indipendenti per social: puoi pubblicare anche su un solo
canale usando solo il suo `.txt`. Le **immagini** sono per destinazione (feed o
storia) e sono condivise tra Instagram e Facebook (stesse misure).

> La stessa immagine (es. una locandina) può comparire sia nel feed sia nella
> storia: sono due posti diversi, quindi si usano **entrambe**, non sono alternative.

> Per **X** e **Telegram** vanno bene le immagini del feed (1080×1350): Telegram
> le mostra intere, X le espande al tap. Non servono misure dedicate.

> **Nota**: queste sono BOZZE. Rileggi sempre prima di pubblicare.
"""
    (out_dir / "README.md").write_text(testo, encoding="utf-8")


def estrai_articolo(path: Path) -> dict | None:
    try:
        testo = path.read_text(encoding="utf-8")
    except OSError:
        return None
    fm, body = parse_frontmatter(testo)
    if fm.get("draft", "").lower() in ("true", "yes", "1"):
        return None
    # Le versioni "facile" (A2) sono nascoste da liste/feed: niente social dedicato.
    if fm.get("versione_facile_di"):
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

    citazione = fm.get("social_citazione", "")
    if not isinstance(citazione, str):
        citazione = ""
    punti = fm.get("social_punti") or []
    if not isinstance(punti, list):
        punti = []

    return {
        "slug": path.stem,
        "title": fm.get("title", ""),
        "description": fm.get("description", ""),
        "badge": fm.get("badge", ""),
        "date": m.group(1),
        "citazione": citazione.strip(),
        "punti": [str(p).strip() for p in punti if str(p).strip()],
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
        if fm.get("versione_facile_di"):
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

        out_dir = slug_dir(art["slug"])
        story_path = out_dir / "storia.jpg"

        # Piano del carosello (ordine): titolo -> citazione -> punti -> foto.
        # Citazione e punti solo se presenti nel frontmatter (social_citazione /
        # social_punti). Max 10 slide (limite Instagram).
        slides = [("titolo", None)]
        if art.get("citazione"):
            slides.append(("citazione", art["citazione"]))
        if art.get("punti"):
            slides.append(("punti", art["punti"]))
        for foto in art["carousel"][1:]:
            slides.append(("foto", foto))
        slides = slides[:10]
        n_slide = len(slides)

        # Nomi a prova di errore: 1 sola slide -> feed-post.jpg; 2+ -> feed-carosello-N.jpg
        primo = out_dir / ("feed-post.jpg" if n_slide == 1 else "feed-carosello-1.jpg")
        if not args.force and primo.exists() and story_path.exists():
            print(f"  GIÀ PRESENTE (--force per ri-generare): {art['slug']}",
                  file=sys.stderr)
            saltati += 1
            continue

        # --force: pulisci immagini precedenti, sia i nomi nuovi sia quelli
        # vecchi (instagram-post*/instagram-story*, e .webp pre-2 maggio 2026).
        if args.force:
            for pat in ("feed-*.jpg", "storia.jpg",
                        "instagram-post*.jpg", "instagram-post*.webp",
                        "instagram-story*.jpg", "instagram-story*.webp"):
                for old in out_dir.glob(pat):
                    old.unlink()

        def _render(kind, data, dest):
            if kind == "titolo":
                crea_slide_titolo(art["title"], art["badge"], dest)
            elif kind == "citazione":
                crea_slide_citazione(data, dest)
            elif kind == "punti":
                crea_slide_punti(data, dest)
            else:
                crea_slide_foto(data, dest)

        try:
            if n_slide == 1:
                _render(*slides[0], out_dir / "feed-post.jpg")
            else:
                for idx, (kind, data) in enumerate(slides, 1):
                    _render(kind, data, out_dir / f"feed-carosello-{idx}.jpg")

            # Story: foto reale (1ª inline) in evidenza se c'è, altrimenti titolo
            hero = art["carousel"][1] if len(art["carousel"]) > 1 else None
            crea_story_verticale(art["cover"], art["title"], art["description"],
                                 story_path, art["badge"], hero)

            # README.md della cartella (mappa file -> destinazione)
            scrivi_readme(out_dir, art, n_slide)

            extra = []
            if art.get("citazione"):
                extra.append("citazione")
            if art.get("punti"):
                extra.append("punti")
            tipo = "singolo" if n_slide == 1 else f"carosello x{n_slide}"
            if extra:
                tipo += " +" + "/".join(extra)
            print(f"  ✓ {art['slug']} ({tipo})", file=sys.stderr)
            ok += 1
        except Exception as e:
            print(f"  ERRORE {art['slug']}: {e}", file=sys.stderr)

    print(f"\nFatto. OK={ok}, saltati={saltati}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
