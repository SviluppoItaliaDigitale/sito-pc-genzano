#!/usr/bin/env python3
"""Genera i poster A2 "In emergenza chiama il 112" multilingua (8 lingue del sito).

Legge le traduzioni da scripts/poster_emergenza_i18n.json (lista di dict con:
code, endonimo, title, subtitle, actionsHeading, actions[6], footerTagline).
Produce, per ogni lingua, un PNG A2 (420x594mm @150dpi) + un PDF stampabile in
static/poster-emergenza-multilingua/.

Composizione loghi (vincolo cogente, vedi rule 02): ESATTAMENTE 4 loghi.
- Header: firma PC Genzano.
- Footer (blocco affiliazioni): Quality Label ESC + codice E10435833, FE.PI.VOL., SNPC Volontariato.

Font: Titillium Web (design system .italia), copre latin-ext (esperanto + rumeno).
Privacy-first: il QR punta alla pagina /emergenza/ del sito (nessun terzo).
"""
import json, os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTDIR = os.path.join(ROOT, "static/vendor/bootstrap-italia/fonts/Titillium_Web")
OUTDIR = os.path.join(ROOT, "static/poster-emergenza-multilingua")
I18N = os.path.join(ROOT, "scripts/poster_emergenza_i18n.json")

# A2 @ 150 dpi
W, H = 2480, 3508
M = 170                      # margine
BLUE = (0, 51, 102)
RED = (193, 18, 31)
DARK = (26, 26, 26)
GREY = (90, 100, 112)
WHITE = (255, 255, 255)
CODE_ESC = "E10435833"
SITE_URL = "www.protezionecivilegenzano.it/emergenza"

def font(weight, size):
    fn = {"r": "titillium-web-v10-latin-ext_latin-regular.ttf",
          "6": "titillium-web-v10-latin-ext_latin-600.ttf",
          "7": "titillium-web-v10-latin-ext_latin-700.ttf"}[weight]
    return ImageFont.truetype(os.path.join(FONTDIR, fn), size)

def load_logo(path, target_h):
    im = Image.open(os.path.join(ROOT, path)).convert("RGBA")
    r = target_h / im.height
    return im.resize((round(im.width * r), target_h), Image.LANCZOS)

def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def wrap(d, s, f, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def make_poster(L):
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Header: firma PC Genzano + endonimo lingua ----
    logo = load_logo("static/images/logo-pc-genzano.png", 200)
    img.paste(logo, (M, M), logo)
    fe = font("7", 84)
    endo = L["endonimo"]
    d.text((W - M - text_w(d, endo, fe), M + 60), endo, font=fe, fill=BLUE)
    d.line((M, M + 250, W - M, M + 250), fill=(214, 224, 236), width=4)

    y = M + 330

    # ---- Blocco 112 (riquadro rosso) ----
    box_h = 920
    d.rounded_rectangle((M, y, W - M, y + box_h), radius=48, fill=RED)
    f_small = font("6", 86)
    d.text((W // 2 - text_w(d, L["title"].replace("112", "").strip(), f_small) // 2, y + 70),
           L["title"].replace("112", "").strip(), font=f_small, fill=WHITE)
    f_112 = font("7", 560)
    d.text((W // 2 - text_w(d, "112", f_112) // 2, y + 150), "112", font=f_112, fill=WHITE)
    f_sub = font("r", 64)
    for i, ln in enumerate(wrap(d, L["subtitle"], f_sub, W - 2 * M - 120)):
        d.text((W // 2 - text_w(d, ln, f_sub) // 2, y + 760 + i * 78), ln, font=f_sub, fill=WHITE)
    y += box_h + 110

    # ---- Cosa fare ----
    f_h = font("7", 110)
    d.text((M, y), L["actionsHeading"], font=f_h, fill=BLUE)
    y += 170
    f_a = font("r", 66)
    f_n = font("7", 60)
    for i, act in enumerate(L["actions"][:6], start=1):
        cx = M + 46
        d.ellipse((M, y, M + 92, y + 92), fill=BLUE)
        d.text((cx - text_w(d, str(i), f_n) // 2, y + 12), str(i), font=f_n, fill=WHITE)
        lines = wrap(d, act, f_a, W - 2 * M - 150)
        for j, ln in enumerate(lines):
            d.text((M + 140, y + 6 + j * 80), ln, font=f_a, fill=DARK)
        y += max(110, len(lines) * 80 + 30)

    # ---- QR + URL ----
    qr_y = H - 720
    try:
        qr = Image.open(os.path.join(ROOT, "static/qr/emergenza.png")).convert("RGBA").resize((360, 360), Image.NEAREST)
        img.paste(qr, (M, qr_y), qr)
    except Exception:
        pass
    f_url = font("6", 56)
    d.text((M + 410, qr_y + 70), L.get("footerTagline", ""), font=f_url, fill=BLUE)
    d.text((M + 410, qr_y + 150), SITE_URL, font=f_url, fill=DARK)

    # ---- Footer: blocco affiliazioni (3 loghi + codice ESC) ----
    fy = H - 250
    d.line((M, fy - 30, W - M, fy - 30), fill=(214, 224, 236), width=4)
    esc = load_logo("static/images/quality-label-esc.png", 150)
    fep = load_logo("static/images/logo-fepivol.png", 150)
    snpc = load_logo("static/images/logo-snpc-volontariato.png", 150)
    x = M
    img.paste(esc, (x, fy), esc); x += esc.width + 20
    f_code = font("7", 44)
    d.text((x, fy + 55), CODE_ESC, font=f_code, fill=BLUE); x += text_w(d, CODE_ESC, f_code) + 90
    img.paste(fep, (x, fy), fep); x += fep.width + 90
    img.paste(snpc, (x, fy), snpc)

    os.makedirs(OUTDIR, exist_ok=True)
    png = os.path.join(OUTDIR, f"poster-emergenza-{L['code']}.png")
    img.save(png, "PNG")
    img.save(os.path.join(OUTDIR, f"poster-emergenza-{L['code']}.pdf"), "PDF", resolution=150.0)
    return png

def main():
    if not os.path.exists(I18N):
        print(f"ERRORE: manca {I18N}", file=sys.stderr); sys.exit(1)
    data = json.load(open(I18N, encoding="utf-8"))
    for L in data:
        p = make_poster(L)
        print(f"[ok] {L['code']} -> {os.path.relpath(p, ROOT)}")
    print(f"Generati {len(data)} poster in static/poster-emergenza-multilingua/")

if __name__ == "__main__":
    main()
