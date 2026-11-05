#!/usr/bin/env python3
"""Genera le versioni animate delle illustrazioni degli esperimenti.

Parte dagli SVG statici di static/formazione/illustrazioni-udl/ (che non
tocca mai) e scrive accanto, in static/formazione/illustrazioni-udl/animate/,
una copia con le animazioni CSS: stesso disegno, stesse scritte, stesso
viewBox 1200x620, più il movimento che fa capire il fenomeno (le bolle che
salgono, la biglia che affonda, il livello che cresce...).

Regole delle animazioni (rule 03 e .claude/rules/lim-scuole.md):
- solo CSS dentro l'SVG, niente JavaScript, niente risorse esterne;
- nessun lampeggio: al massimo un cambio di luce ogni pochi secondi (WCAG 2.3.1);
- l'animazione non parte da sola sul sito: la avvia il pulsante dello
  shortcode illustrazione-udl, che la ferma tornando al disegno statico
  (WCAG 2.2.2); dentro l'SVG c'è comunque prefers-reduced-motion;
- il disegno a riposo (prima che parta l'animazione) dice le stesse cose
  della versione statica.

Uso:
    python3 scripts/genera-animazioni-esperimenti.py           # rigenera
    python3 scripts/genera-animazioni-esperimenti.py --check   # verifica, esce 1 se diverso
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "static/formazione/illustrazioni-udl"
OUT = SRC / "animate"

BASE_CSS = (
    ".fermo{display:none}"
    ".fb{transform-box:fill-box}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def sostituisci(testo: str, vecchio: str, nuovo: str, nome: str) -> str:
    n = testo.count(vecchio)
    if n != 1:
        raise SystemExit(f"{nome}: il frammento da sostituire compare {n} volte (atteso 1):\n  {vecchio[:90]}")
    return testo.replace(vecchio, nuovo)


def sostituisci_re(testo: str, schema: str, nuovo, attese: int, nome: str) -> str:
    risultato, n = re.subn(schema, nuovo, testo)
    if n != attese:
        raise SystemExit(f"{nome}: lo schema {schema!r} trova {n} frammenti (attesi {attese})")
    return risultato


# ---------------------------------------------------------------------------
# Ricette: per ogni illustrazione, le modifiche al disegno (patch), il CSS e
# gli elementi in più (overlay), più titolo e descrizione dell'animazione.
# ---------------------------------------------------------------------------

def r_viscosita(s, n):
    s = sostituisci(s, '<g fill="#f8ffff" stroke="#367eac" stroke-width="3">',
                    '<g class="fermo" fill="#f8ffff" stroke="#367eac" stroke-width="3">', n)
    s = sostituisci(s, '<g fill="#ffe9cb" stroke="#86481e" stroke-width="4">',
                    '<g class="fermo" fill="#ffe9cb" stroke="#86481e" stroke-width="4">', n)
    css = (
        "@keyframes sale{0%{transform:translateY(0);opacity:0}8%{opacity:1}"
        "88%{transform:translate(-30px,-128px);opacity:1}100%{transform:translate(-32px,-136px);opacity:0}}"
        ".bl{animation:sale 2.4s linear infinite}"
        "@keyframes fatica{0%{transform:translateY(0) scale(.6);opacity:0}8%{opacity:1}"
        "70%{transform:translate(-40px,-112px) scale(1.2);opacity:1}82%{transform:translate(-44px,-122px) scale(1.35);opacity:1}"
        "86%{transform:translate(-44px,-126px) scale(1.6);opacity:0}100%{transform:translate(-44px,-126px) scale(1.6);opacity:0}}"
        ".bd{animation:fatica 7.5s ease-in infinite;transform-origin:50% 50%}"
        "@keyframes schizzo{0%,81%{opacity:0;transform:translateY(0)}84%{opacity:1}94%{opacity:0;transform:translateY(-14px)}100%{opacity:0}}"
        ".sz{animation:schizzo 7.5s linear infinite}"
    )
    o = ['<g fill="#f8ffff" stroke="#367eac" stroke-width="3">']
    for i, (x, r) in enumerate([(350, 9), (338, 12), (362, 7), (344, 11), (356, 8), (348, 6)]):
        o.append(f'<circle class="bl" style="animation-delay:-{i * 0.4:.1f}s" cx="{x}" cy="442" r="{r}"/>')
    o.append('</g><g fill="#ffe9cb" stroke="#86481e" stroke-width="4">')
    for i, x in enumerate([930, 930, 930]):
        o.append(f'<circle class="bd fb" style="animation-delay:-{i * 2.5:.1f}s" cx="{x}" cy="440" r="16"/>')
    o.append('</g><g fill="none" stroke="#a8622c" stroke-width="5" stroke-linecap="round">')
    for i, x in enumerate([930, 930, 930]):
        o.append(f'<path class="sz" style="animation-delay:-{i * 2.5:.1f}s" d="M{x - 62} 282 l-10 -16 M{x - 44} 276 V254 M{x - 26} 282 l10 -16"/>')
    o.append('</g>')
    return s, css, "".join(o)


def r_gelatina(s, n):
    s = sostituisci(s, '<g transform="translate(298 472) rotate(0 0 0)">',
                    '<g transform="translate(298 472)"><g class="oscR">', n)
    s = sostituisci(s, '</g></g><g transform="translate(891 472) rotate(-9 0 0)">',
                    '</g></g></g><g transform="translate(891 472)"><g class="oscG">', n)
    s = sostituisci(s, '</g></g>\n<path d="M250 230', '</g></g></g>\n<path d="M250 230', n)
    s = sostituisci(s, '<path d="M695 472 Q734 462', '<path class="gel fb" d="M695 472 Q734 462', n)
    css = (
        "@keyframes oR{from{transform:rotate(-1.5deg)}to{transform:rotate(1.5deg)}}"
        ".oscR{transform-origin:0 0;animation:oR .45s ease-in-out infinite alternate}"
        "@keyframes oG{from{transform:rotate(-9deg)}to{transform:rotate(9deg)}}"
        ".oscG{transform-origin:0 0;animation:oG .9s ease-in-out infinite alternate}"
        "@keyframes gl{from{transform:scaleY(1)}to{transform:scaleY(.86)}}"
        ".gel{transform-origin:50% 100%;animation:gl .45s ease-in-out infinite alternate}"
    )
    return s, css, ""


def r_sabbia(s, n):
    s = sostituisci(s, '<g transform="translate(120 242)">', '<g class="scuoti"><g transform="translate(120 242)">', n)
    s = sostituisci(s, '</g><g transform="translate(711 242)">', '</g></g><g class="scuoti"><g transform="translate(711 242)">', n)
    s = sostituisci(s, '</g>\n<path d="M117 530', '</g></g>\n<path d="M117 530', n)
    s = sostituisci(s, '<circle cx="174" cy="120" r="28"', '<circle class="affonda" cx="174" cy="38" r="28"', n)
    s = sostituisci(s, '<path d="M170 505 l9 -8', '<path class="vibra" d="M170 505 l9 -8', n)
    css = (
        "@keyframes sc{0%,100%{transform:translateY(0)}15%{transform:translateY(-4px)}30%{transform:translateY(1px)}45%{transform:translateY(0)}}"
        ".scuoti{animation:sc .5s linear infinite}"
        "@keyframes vb{0%,100%{opacity:.25}15%{opacity:1}45%{opacity:.25}}.vibra{animation:vb .5s linear infinite}"
        "@keyframes af{0%,10%{transform:translateY(0);opacity:1}70%,88%{transform:translateY(82px);opacity:1}"
        "95%{transform:translateY(82px);opacity:0}96%{transform:translateY(0);opacity:0}100%{transform:translateY(0);opacity:1}}"
        ".affonda{animation:af 9s ease-in-out infinite}"
    )
    return s, css, ""


def r_sismografo(s, n):
    s = sostituisci(s, '<path d="M134 212 H715 V470 H134Z"', '<g class="scatola"><path d="M134 212 H715 V470 H134Z"', n)
    s = sostituisci(s, '<path d="M134 469 H715" stroke="#977b5c" stroke-width="18"/>',
                    '<path d="M134 469 H715" stroke="#977b5c" stroke-width="18"/></g>', n)
    s = sostituisci(s, '<path d="M196 461 Q224 440', '<path class="fermo" d="M196 461 Q224 440', n)
    durata, v = 9.0, 40.0

    def env(t):  # scossa fra 2 e 6 secondi, con attacco e coda morbidi
        if t < 2 or t > 6:
            return 0.0
        return math.sin(math.pi * (t - 2) / 4) ** 2

    def onda(t):
        return math.sin(2 * math.pi * 1.0 * t) * env(t)

    punti = []
    t = 0.0
    while t <= durata + 1e-9:
        punti.append(f"{430 - v * t:.1f} {461 - 19 * onda(t):.1f}")
        t += 0.03
    traccia = "M" + " L".join(punti)
    frames = []
    for i in range(0, 181):
        tt = durata * i / 180
        frames.append(f"{i / 1.8:.2f}%{{transform:translateX({9 * onda(tt):.1f}px)}}")
    css = (
        "@keyframes sb{" + "".join(frames) + "}"
        f".scatola{{animation:sb {durata}s linear infinite}}"
        f"@keyframes carta{{from{{transform:translateX(0)}}to{{transform:translateX({v * durata:.0f}px)}}}}"
        f".carta{{animation:carta {durata}s linear infinite}}"
        "@keyframes svan{0%,94%{opacity:1}99%,100%{opacity:0}}"
        f".svan{{animation:svan {durata}s linear infinite}}"
    )
    o = ('<clipPath id="nastro"><rect x="430" y="436" width="330" height="52"/></clipPath>'
         '<g clip-path="url(#nastro)"><g class="svan"><g class="carta">'
         f'<path d="{traccia}" fill="none" stroke="#c35e49" stroke-width="4" stroke-linejoin="round"/>'
         '</g></g></g>')
    return s, css, o


def r_spugna(s, n):
    for d in ("M359 105 Q354 115 360 125", "M367 130 Q361 140 368 150",
              "M375 155 Q368 165 376 175", "M383 180 Q375 190 384 200"):
        s = sostituisci(s, f'<path d="{d}"', f'<path class="fermo" d="{d}"', n)
    css = (
        "@keyframes gc{0%{transform:translate(0,0);opacity:0}10%{opacity:1}80%{transform:translate(6px,62px);opacity:1}100%{transform:translate(6px,70px);opacity:0}}"
        ".gc{animation:gc 1.6s ease-in infinite}"
        "@keyframes as{0%,40%{opacity:0}70%{opacity:.45}100%{opacity:0}}"
        ".as{animation:as 1.6s linear infinite}"
        "@keyframes fl{to{stroke-dashoffset:-56}}"
        ".fl{animation:fl .7s linear infinite}"
        "@keyframes fg{0%{transform:translate(0,0);opacity:0}12%{opacity:1}80%{transform:translate(70px,30px);opacity:1}100%{transform:translate(78px,40px);opacity:0}}"
        ".fg{animation:fg 2.2s ease-in infinite}"
    )
    o = ['<g transform="translate(45 138) scale(1.04)">',
         '<ellipse class="as" cx="352" cy="190" rx="34" ry="12" fill="#9a7444"/>']
    for i in range(3):
        o.append(f'<circle class="gc" style="animation-delay:-{i * 0.53:.2f}s" cx="358" cy="112" r="6" fill="#3AADE0"/>')
    o.append('</g><g transform="translate(631 138) scale(1.04)">'
             '<path class="fl" d="M359 109 Q374 175 389 234 Q406 278 446 298" fill="none" stroke="#d7f2ff" '
             'stroke-width="5" stroke-dasharray="14 14" stroke-linecap="round"/>')
    for i in range(4):
        o.append(f'<circle class="fg" style="animation-delay:-{i * 0.55:.2f}s" cx="382" cy="258" r="6" fill="#7b583e"/>')
    o.append('</g>')
    return s, css, "".join(o)


PIOGGIA_CSS = (
    "@keyframes pg{0%{transform:translateY(0);opacity:0}15%{opacity:1}75%{opacity:1}100%{transform:translateY(34px);opacity:0}}"
    ".pg{animation:pg 1.1s linear infinite}"
    ".p1{animation-delay:-.27s}.p2{animation-delay:-.55s}.p3{animation-delay:-.82s}"
)


def pioggia(s, lunghezza, attese, n):
    contatore = {"i": 0}

    def sub(m):
        contatore["i"] += 1
        return f'<path class="pg p{contatore["i"] % 4}" d="{m.group(1)}"'

    return sostituisci_re(s, r'<path d="(M\d+ \d+ l-9 ' + str(lunghezza) + r')"', sub, attese, n)


def r_radici(s, n):
    s = pioggia(s, 18, 14, n)
    s = sostituisci(s, '<g fill="#a77a58">', '<g class="fermo" fill="#a77a58">', n)
    css = PIOGGIA_CSS + (
        "@keyframes fl{to{stroke-dashoffset:-40}}.fl{animation:fl .9s linear infinite}"
        "@keyframes er{0%{transform:translate(0,0);opacity:0}10%{opacity:1}85%{transform:translate(122px,64px);opacity:1}100%{transform:translate(130px,68px);opacity:0}}"
        ".er{animation:er 3s ease-in infinite}"
    )
    o = ['<path class="fl" d="M443 401 Q495 426 546 439" fill="none" stroke="#dff4ff" stroke-width="3" stroke-dasharray="10 10" stroke-linecap="round"/>',
         '<g fill="#a77a58">']
    for i, r in enumerate([9, 7, 8, 6, 7]):
        o.append(f'<circle class="er" style="animation-delay:-{i * 0.6:.1f}s" cx="990" cy="396" r="{r}"/>')
    o.append('</g>')
    return s, css, "".join(o)


def r_prato(s, n):
    s = pioggia(s, 18, 14, n)
    css = PIOGGIA_CSS + (
        "@keyframes inf{0%{transform:translateY(0);opacity:0}15%{opacity:.95}85%{opacity:.95}100%{transform:translateY(120px);opacity:0}}"
        ".inf{animation:inf 2.4s linear infinite}"
        "@keyframes dfl{0%{transform:translate(0,0);opacity:0}8%{opacity:1}80%{transform:translate(380px,0);opacity:1}"
        "92%{transform:translate(400px,18px);opacity:.6}100%{transform:translate(400px,24px);opacity:0}}"
        ".dfl{animation:dfl 2.6s linear infinite}"
    )
    o = ['<g fill="#2b8fc0">']
    for i, x in enumerate([168, 313, 455, 240, 385]):
        o.append(f'<ellipse class="inf" style="animation-delay:-{i * 0.48:.2f}s" cx="{x}" cy="335" rx="5" ry="7"/>')
    o.append('</g><g fill="#2b8fc0">')
    for i in range(4):
        o.append(f'<ellipse class="dfl" style="animation-delay:-{i * 0.65:.2f}s" cx="700" cy="301" rx="12" ry="4"/>')
    o.append('</g>')
    return s, css, "".join(o)


def r_pluviometro(s, n):
    s = pioggia(s, 23, 9, n)
    s = sostituisci(s, '<path d="M299 419 Q327 414', '<path class="fermo" d="M299 419 Q327 414', n)
    s = sostituisci(s, '<path d="M299 420 H463"', '<path class="fermo" d="M299 420 H463"', n)
    s = sostituisci(s, '<rect x="932" y="375" width="73" height="92"', '<rect class="fermo" x="932" y="375" width="73" height="92"', n)
    s = sostituisci(s, '<path d="M996 378 H1102"', '<path class="fermo" d="M996 378 H1102"', n)
    s = sostituisci(s, '<path d="M1009 366 l-13 12 13 12"', '<path class="fermo" d="M1009 366 l-13 12 13 12"', n)
    s = sostituisci(s, '<text x="1102" y="356"', '<text class="fermo" x="1102" y="356"', n)
    css = PIOGGIA_CSS.replace("1.1s", "1.4s") + (
        "@keyframes lv{0%,4%{transform:translateY(-35px)}78%,100%{transform:translateY(-85px)}}"
        ".lv{animation:lv 11s ease-out infinite}"
        "@keyframes lr{0%,4%{transform:translateY(-40px)}78%,100%{transform:translateY(-92px)}}"
        ".lr{animation:lr 11s ease-out infinite}"
        "@keyframes rs{0%,90%{opacity:1}97%{opacity:0}100%{opacity:1}}"
        ".rs{animation:rs 11s linear infinite}"
    )
    o = ('<clipPath id="bott"><path d="M291 296 L306 507 H454 L469 296Z"/></clipPath>'
         '<clipPath id="prov"><rect x="932" y="240" width="73" height="227"/></clipPath>'
         '<g class="rs"><g clip-path="url(#bott)"><g class="lv">'
         '<rect x="285" y="504" width="190" height="220" fill="url(#water)" opacity=".95"/>'
         '<path d="M290 504 H470" stroke="#176f9e" stroke-width="5" stroke-dasharray="9 7"/></g></g>'
         '<path d="M560 469 H580" stroke="#176f9e" stroke-width="4"/><text x="590" y="475" font-family="Arial,sans-serif" '
         'font-size="17" font-weight="700" fill="#176f9e">0</text>'
         '<g clip-path="url(#prov)"><g class="lr"><rect x="932" y="467" width="73" height="240" fill="#7bc3e4" opacity=".8"/></g></g>'
         '<g transform="translate(0 89)"><g class="lr"><path d="M996 378 H1102" stroke="#287eaa" stroke-width="5"/>'
         '<path d="M1009 366 l-13 12 13 12" fill="none" stroke="#287eaa" stroke-width="5"/>'
         '<text x="1102" y="356" font-family="Arial,sans-serif" font-size="17" font-weight="700" fill="#166f9e" text-anchor="middle">livello</text></g></g></g>')
    return s, css, o


def r_maremoto(s, n):
    s = sostituisci(s, '<path d="M115 214 L237 214', '<g class="barca"><path d="M115 214 L237 214', n)
    s = sostituisci(s, '<path d="M115 244 Q132 255 151 244 T190 244 T229 244"',
                    '</g><path d="M115 244 Q132 255 151 244 T190 244 T229 244"', n)
    s = sostituisci(s, '<circle cx="1086" cy="269" r="20"', '<g class="fuga"><circle cx="1086" cy="269" r="20"', n)
    s = sostituisci(s, '<path d="M1077 305 L1050 327 M1106 306 L1126 290" fill="none" stroke="#EDBA98" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>',
                    '<path d="M1077 305 L1050 327 M1106 306 L1126 290" fill="none" stroke="#EDBA98" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>', n)
    css = (
        "@keyframes onda{0%{transform:translateX(0) scale(1.4,.3);opacity:0}6%{opacity:1}"
        "50%{transform:translateX(500px) scale(1.3,.36)}80%{transform:translateX(690px) scale(.85,.9)}"
        "90%{transform:translateX(730px) scale(.7,1.3);opacity:1}96%{opacity:0}100%{transform:translateX(740px) scale(.7,1.3);opacity:0}}"
        ".onda{transform-origin:50% 100%;animation:onda 9s cubic-bezier(.3,0,.7,1) infinite}"
        "@keyframes bc{from{transform:translateY(-3px)}to{transform:translateY(3px)}}"
        ".barca{animation:bc 1.6s ease-in-out infinite alternate}"
        "@keyframes fg{0%{transform:translate(0,0);opacity:0}8%{opacity:1}85%{transform:translate(34px,-26px);opacity:1}96%,100%{transform:translate(38px,-29px);opacity:0}}"
        ".fuga{animation:fg 9s linear infinite}"
    )
    o = ('<path class="onda fb" d="M20 247 C60 247 70 205 110 205 C150 205 160 247 200 247 Z" fill="#3f9ccc" '
         'stroke="#e6fbff" stroke-width="5" stroke-linejoin="round"/>')
    return s, css, o


def r_tombino(s, n):
    s = sostituisci(s, '<path d="M118 157 V198 M152 157 V198 M188 157 V198 M224 157 V198"',
                    '<path class="sc1" stroke-dasharray="10 8" d="M118 157 V198 M152 157 V198 M188 157 V198 M224 157 V198"', n)
    s = sostituisci(s, '<path d="M186 156 V198 M220 155 V198"', '<path class="sc2" stroke-dasharray="10 14" d="M186 156 V198 M220 155 V198"', n)
    s = sostituisci(s, '<rect x="81" y="131" width="186" height="14"', '<rect class="pozza fb" x="81" y="131" width="186" height="14"', n)
    s = sostituisci(s, '<path d="M78 131 Q113 126', '<path class="sup" d="M78 131 Q113 126', n)
    s = sostituisci(s, '<rect x="81" y="115" width="186" height="30"', '<rect class="pozza fb" x="81" y="115" width="186" height="30"', n)
    s = sostituisci(s, '<path d="M78 115 Q113 110', '<path class="sup" d="M78 115 Q113 110', n)
    lancette = [("164.34712181799046 216.0658658130567", 45.8), ("169.9914720608301 230.58399044602578", 91.7),
                ("163.50926361102302 244.74787431082493", 137.4)]
    for k, (punta, gradi) in enumerate(lancette):
        s = sostituisci(s, f'<path d="M150 230 L{punta}"', f'<path class="lan{k}" d="M150 230 L{punta}"', n)
    livelli = {}
    for i, (sx, y) in enumerate([(129, "470.6"), (521, "511.4"), (913, "548.6")]):
        s = sostituisci(s, f'<path d="M{sx} {y} Q', f'<path class="fermo" d="M{sx} {y} Q', n)
        s = sostituisci(s, f'<path d="M{sx + 1} {y} Q', f'<path class="fermo" d="M{sx + 1} {y} Q', n)
        livelli[i] = (sx, float(y))
    # stessa velocità di lancetta per i tre orologi (137,4 gradi in 8 secondi):
    # ciascuna si ferma quando sotto la griglia non scende più acqua. Si versa
    # per lo stesso tempo nei tre casi (fino a fine[0]); dopo, nel caso 2
    # l'acqua della pozza scende ancora per un po', nel caso 3 resta sopra.
    fine = [0.4 + g / 137.4 * 8 for _, g in lancette]
    css = (
        "@keyframes cad{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(16px);opacity:0}}"
        ".cad{animation:cad .5s linear infinite}"
        "@keyframes sc{to{stroke-dashoffset:-36}}"
        ".sc1{animation:sc .45s linear infinite,on0 10s linear infinite}"
        ".sc2{animation:sc 1.2s linear infinite,on1 10s linear infinite}"
        f"@keyframes pz{{0%,4%{{transform:scaleY(0)}}{fine[0] * 10:.1f}%,100%{{transform:scaleY(1)}}}}"
        ".pozza{transform-origin:50% 100%;animation:pz 10s linear infinite}"
        f"@keyframes sp{{0%,{fine[0] * 10 - 6:.1f}%{{opacity:0}}{fine[0] * 10:.1f}%,100%{{opacity:1}}}}"
        ".sup{animation:sp 10s linear infinite}"
        "@keyframes gs{0%{transform:translateY(0);opacity:0}10%{opacity:1}85%{transform:translateY(80px);opacity:1}100%{transform:translateY(88px);opacity:0}}"
        ".g1{animation:gs .9s ease-in infinite}.g2{animation:gs 1.8s ease-in infinite}.g3{animation:gs 4s ease-in infinite}"
        "@keyframes rs{0%,90%{opacity:1}97%{opacity:0}100%{opacity:1}}.rs{animation:rs 10s linear infinite}"
    )
    for k, (_, gradi) in enumerate(lancette):
        css += (f"@keyframes la{k}{{0%,4%{{transform:rotate(-{gradi}deg)}}{fine[k] * 10:.1f}%,100%{{transform:rotate(0)}}}}"
                f".lan{k}{{transform-origin:150px 230px;animation:la{k} 10s linear infinite}}"
                f"@keyframes on{k}{{0%,{fine[k] * 10:.1f}%{{opacity:1}}{fine[k] * 10 + 1:.1f}%,100%{{opacity:0}}}}"
                f".on{k}{{animation:on{k} 10s linear infinite}}")
    o = ['<g class="on0">']
    for k, ox in enumerate([34, 426, 818]):
        o.append(f'<circle class="cad" style="animation-delay:-{k * 0.17:.2f}s" cx="{ox + 287}" cy="{153 + 125}" r="5" fill="#47B0DD"/>')
    o.append('</g>')
    goccie = {0: (4, "g1", 0.22), 1: (2, "g2", 0.9), 2: (1, "g3", 0)}
    for k, ox in enumerate([0, 392, 784]):
        quante, classe, passo = goccie[k]
        o.append(f'<g class="on{k}">')
        for j in range(quante):
            x = ox + 175 + j * 24
            o.append(f'<ellipse class="{classe}" style="animation-delay:-{j * passo:.2f}s" cx="{x}" cy="372" rx="4" ry="6" fill="#47B0DD"/>')
        o.append('</g>')
    for k, (sx, y) in livelli.items():
        salita = 556 - y
        css += f"@keyframes lv{k}{{0%,4%{{transform:translateY(0)}}{fine[k] * 10:.1f}%,100%{{transform:translateY(-{salita:.1f}px)}}}}"
        o.append(f'<clipPath id="bk{k}"><path d="M{sx} 443 H{sx + 169} V545 Q{sx + 169} 556 {sx + 158} 556 H{sx + 11} Q{sx} 556 {sx} 545Z"/></clipPath>'
                 f'<g class="rs"><g clip-path="url(#bk{k})"><g style="animation:lv{k} 10s linear infinite">'
                 f'<path d="M{sx} 556 Q{sx + 84.5} 548 {sx + 169} 556 V680 H{sx}Z" fill="#5CBCE3" opacity=".91"/>'
                 f'<path d="M{sx + 1} 556 Q{sx + 84.5} 548 {sx + 168} 556" fill="none" stroke="#EFFDFF" stroke-width="5"/>'
                 '</g></g></g>')
    return s, css, "".join(o)


def r_triangolo(s, n):
    s = sostituisci(s, '<path d="M554 442 C489', '<g class="fiamma fb"><g class="guizzo fb"><path d="M554 442 C489', n)
    s = sostituisci(s, 'C655 458 629 469 604 449Z" fill="#ffe0a0"/>', 'C655 458 629 469 604 449Z" fill="#ffe0a0"/></g></g>', n)
    s = sostituisci(s, '<rect x="421" y="97" width="361" height="74" rx="16" fill="#1b6b87"/>',
                    '<g class="ossigeno"><rect x="421" y="97" width="361" height="74" rx="16" fill="#1b6b87"/>', n)
    s = sostituisci(s, "ossigeno dell'aria</text>", "ossigeno dell'aria</text></g>", n)
    s = sostituisci(s, '<text x="600" y="539"', '<text class="frase1" x="600" y="539"', n)
    css = (
        "@keyframes gz{from{transform:scale(1,1)}to{transform:scale(.96,1.04)}}"
        ".guizzo{transform-origin:50% 100%;animation:gz .5s ease-in-out infinite alternate}"
        "@keyframes fm{0%,40%{transform:scale(1);opacity:1}62%{transform:scale(.15);opacity:.2}66%,100%{transform:scale(0);opacity:0}}"
        ".fiamma{transform-origin:50% 100%;animation:fm 10s ease-in-out infinite}"
        "@keyframes ox{0%,38%{opacity:1}48%,100%{opacity:.25}}"
        ".ossigeno{animation:ox 10s linear infinite}"
        "@keyframes f1{0%,38%{opacity:1}44%,100%{opacity:0}}.frase1{animation:f1 10s linear infinite}"
        "@keyframes f2{0%,40%{opacity:0}46%,100%{opacity:1}}.frase2{animation:f2 10s linear infinite;opacity:0}"
    )
    o = ('<text class="frase2" x="600" y="539" font-family="Arial,sans-serif" font-size="23" fill="#123a59" '
         'text-anchor="middle" font-weight="700">Se manca l\'ossigeno, la fiamma si spegne.</text>')
    return s, css, o


def r_calore(s, n):
    s = sostituisci(s, '<rect x="25" y="137" width="13" height="57" rx="6" fill="#3987b9"/>',
                    '<rect class="tf fb" x="25" y="137" width="13" height="57" rx="6" fill="#3987b9"/>', n)
    s = sostituisci(s, '<rect x="25" y="74" width="13" height="120" rx="6" fill="#cc6042"/>',
                    '<rect class="tc fb" x="25" y="74" width="13" height="120" rx="6" fill="#cc6042"/>', n)
    s = sostituisci(s, '<path d="M176 208 L246 282 M174 236 L218 304 M768 208 L838 282 M767 236 L811 304"',
                    '<path class="rg" stroke-dasharray="16 10" d="M176 208 L246 282 M174 236 L218 304 M768 208 L838 282 M767 236 L811 304"', n)
    css = (
        "@keyframes rg{to{stroke-dashoffset:-52}}.rg{animation:rg 1s linear infinite}"
        "@keyframes tf{0%,6%{transform:scaleY(.18)}75%,92%{transform:scaleY(1)}100%{transform:scaleY(.18)}}"
        ".tf{transform-origin:50% 100%;animation:tf 10s ease-out infinite}"
        "@keyframes tc{0%,6%{transform:scaleY(.085)}75%,92%{transform:scaleY(1)}100%{transform:scaleY(.085)}}"
        ".tc{transform-origin:50% 100%;animation:tc 10s ease-out infinite}"
        "@keyframes rf{0%{transform:translate(0,0);opacity:0}20%{opacity:.9}100%{transform:translate(34px,-46px);opacity:0}}"
        ".rf{animation:rf 1.6s linear infinite}"
        "@keyframes cs{0%{transform:translateY(0);opacity:0}25%{opacity:.8}100%{transform:translateY(-40px);opacity:0}}"
        ".cs{animation:cs 2.2s linear infinite}"
    )
    o = ['<g stroke="#e4b244" stroke-width="5" stroke-linecap="round" fill="none">']
    for i, (x, y) in enumerate([(250, 300), (300, 296), (210, 312)]):
        o.append(f'<path class="rf" style="animation-delay:-{i * 0.53:.2f}s" d="M{x} {y} l16 -22"/>')
    o.append('</g><g stroke="#b8664a" stroke-width="4" stroke-linecap="round" fill="none">')
    for i, x in enumerate([790, 850, 910]):
        o.append(f'<path class="cs" style="animation-delay:-{i * 0.73:.2f}s" d="M{x} 300 q8 -8 0 -16 t0 -16"/>')
    o.append('</g>')
    return s, css, "".join(o)


def r_manica(s, n):
    s = sostituisci(s, '<ellipse cx="53" cy="0" rx="14" ry="34" fill="#f2ede3" stroke="#9b805f" stroke-width="5"/><path d="M53 -34 C92',
                    '<g class="mD"><ellipse cx="53" cy="0" rx="14" ry="34" fill="#f2ede3" stroke="#9b805f" stroke-width="5"/><path d="M53 -34 C92', n)
    s = sostituisci(s, '</g><g transform="translate(774 258)">', '</g></g><g transform="translate(774 258)">', n)
    s = sostituisci(s, '<ellipse cx="53" cy="0" rx="14" ry="34" fill="#f2ede3" stroke="#9b805f" stroke-width="5"/><path d="M53 -34 L218',
                    '<g class="mF"><ellipse cx="53" cy="0" rx="14" ry="34" fill="#f2ede3" stroke="#9b805f" stroke-width="5"/><path d="M53 -34 L218', n)
    s = sostituisci(s, '</g>\n<path d="M77 314', '</g></g>\n<path d="M77 314', n)
    s = sostituisci(s, '<path d="M77 314 Q111 302', '<path class="vD" d="M77 314 Q111 302', n)
    for y in (294, 338, 382):
        s = sostituisci(s, f'<path d="M673 {y} H', f'<path class="vF" style="animation-delay:-{(y - 294) / 44 * 0.25:.2f}s" d="M673 {y} H', n)
    css = (
        "@keyframes mD{from{transform:rotate(-3deg)}to{transform:rotate(4deg)}}"
        ".mD{transform-origin:40px 0;animation:mD 2.4s ease-in-out infinite alternate}"
        "@keyframes mF{from{transform:rotate(-2.5deg) scaleY(.96)}to{transform:rotate(2.5deg) scaleY(1.03)}}"
        ".mF{transform-origin:40px 0;animation:mF .35s ease-in-out infinite alternate}"
        "@keyframes vD{0%{transform:translateX(-14px);opacity:0}40%{opacity:1}100%{transform:translateX(18px);opacity:0}}"
        ".vD{animation:vD 3s ease-in-out infinite}"
        "@keyframes vF{0%{transform:translateX(-24px);opacity:0}25%{opacity:1}100%{transform:translateX(26px);opacity:0}}"
        ".vF{animation:vF .75s linear infinite}"
    )
    return s, css, ""


def r_lampo(s, n):
    s = sostituisci(s, '<path d="M706 159 L659 256', '<path class="saetta" d="M706 159 L659 256', n)
    s = sostituisci(s, '<path d="M685 274 L376 274" fill="none" stroke="#254960"',
                    '<g class="luce"><path d="M685 274 L376 274" fill="none" stroke="#254960"', n)
    s = sostituisci(s, '<path d="M380 274 L408 258 L408 290Z" fill="#FFE171" stroke="#254960" stroke-width="2"/>',
                    '<path d="M380 274 L408 258 L408 290Z" fill="#FFE171" stroke="#254960" stroke-width="2"/></g>', n)
    s = sostituisci(s, '<path d="M1050 372 Q995 337 938 373 T826 373 T714 373 T602 373 T490 373 L379 373" fill="none" stroke="#16364D"',
                    '<g class="suono"><path d="M1050 372 Q995 337 938 373 T826 373 T714 373 T602 373 T490 373 L379 373" fill="none" stroke="#16364D"', n)
    s = sostituisci(s, '<path d="M379 373 L405 358 L405 388Z" fill="#D7F5FF" stroke="#16364D" stroke-width="2"/>',
                    '<path d="M379 373 L405 358 L405 388Z" fill="#D7F5FF" stroke="#16364D" stroke-width="2"/></g>', n)
    s = sostituisci(s, '<rect x="610" y="399" width="545" height="58"', '<g class="calcolo fb"><rect x="610" y="399" width="545" height="58"', n)
    s = sostituisci(s, '9 secondi : 3 = circa 3 km</text>', '9 secondi : 3 = circa 3 km</text></g>', n)
    T = 12
    pct = lambda sec: f"{sec / T * 100:.2f}%"  # noqa: E731
    css = (
        f"@keyframes sa{{0%{{opacity:.35}}{pct(.25)}{{opacity:1}}{pct(1)}{{opacity:1}}{pct(1.6)},100%{{opacity:.35}}}}"
        f".saetta{{animation:sa {T}s linear infinite}}"
        f"@keyframes lu{{0%,{pct(.2)}{{opacity:0}}{pct(.35)},{pct(11.4)}{{opacity:1}}100%{{opacity:0}}}}"
        f".luce{{animation:lu {T}s linear infinite}}"
        f"@keyframes so{{0%,{pct(.3)}{{opacity:.3}}{pct(9.3)}{{opacity:.3}}{pct(9.5)},{pct(11.4)}{{opacity:1}}100%{{opacity:.3}}}}"
        f".suono{{animation:so {T}s linear infinite}}"
        f"@keyframes fr{{0%,{pct(.3)}{{transform:translateX(0);opacity:0}}{pct(.6)}{{opacity:1}}"
        f"{pct(9.3)}{{transform:translateX(-650px);opacity:1}}{pct(9.6)},100%{{transform:translateX(-650px);opacity:0}}}}"
        f".fronte{{animation:fr {T}s linear infinite}}"
        f"@keyframes cf{{0%{{opacity:1}}{pct(1) }{{opacity:1}}{pct(1.01)},100%{{opacity:0}}}}"
        f".cifra{{opacity:0;animation:cf {T}s linear infinite}}"
        f"@keyframes eti{{0%,{pct(1.2)}{{opacity:0}}{pct(1.3)},{pct(10.3)}{{opacity:1}}{pct(10.4)},100%{{opacity:0}}}}"
        f".eti{{opacity:0;animation:eti {T}s linear infinite}}"
        f"@keyframes cc{{0%,{pct(9.4)}{{transform:scale(1)}}{pct(9.8)}{{transform:scale(1.05)}}{pct(10.4)},100%{{transform:scale(1)}}}}"
        f".calcolo{{transform-origin:50% 50%;animation:cc {T}s ease-in-out infinite}}"
    )
    o = ['<g class="fronte" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round">'
         '<path d="M1040 351 q-14 22 0 44"/><path d="M1058 343 q-20 30 0 60"/><path d="M1076 335 q-26 38 0 76"/></g>',
         '<g class="eti"><rect x="122" y="90" width="132" height="72" rx="12" fill="#FFFFFF" stroke="#9AB7C5" stroke-width="3"/>'
         '<text x="188" y="155" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="700" fill="#173C57" '
         'text-anchor="middle">secondi</text></g>']
    for i in range(1, 10):
        o.append(f'<text class="cifra" style="animation-delay:{0.3 + i:.1f}s" x="188" y="136" font-family="Arial,Helvetica,sans-serif" '
                 f'font-size="40" font-weight="700" fill="#173C57" text-anchor="middle">{i}</text>')
    return s, css, "".join(o)


RICETTE = {
    "esperimento-viscosita-gas": (r_viscosita,
        "Animazione: bolle nel liquido fluido e nella miscela densa",
        "Nel bicchiere con il liquido fluido le bolle salgono in fretta e arrivano in superficie. Nella miscela densa le bolle salgono piano, si gonfiano restando intrappolate e poi escono di colpo con uno schizzo. È un modello didattico, non un'eruzione."),
    "esperimento-terreno-rigido-gelatina": (r_gelatina,
        "Animazione: la stessa torretta su terreno rigido e su gelatina",
        "Le due basi vengono scosse allo stesso modo. La torretta sul supporto rigido oscilla poco; quella sulla gelatina, che si deforma, oscilla molto di più. È un modello da tavolo: non stabilisce la sicurezza di un edificio."),
    "esperimento-sabbia-liquefazione": (r_sabbia,
        "Animazione: vibrazioni su sabbia asciutta e su sabbia satura",
        "Le due vaschette vibrano nello stesso modo. Sulla sabbia asciutta la biglia resta in superficie; nella sabbia satura d'acqua la biglia scende lentamente, perché il terreno perde sostegno. Il risultato reale dipende da molti fattori."),
    "esperimento-sismografo": (r_sismografo,
        "Animazione: come il sismografo di cartone registra la scossa",
        "La striscia di carta scorre sotto la penna. Quando la scatola viene scossa, il peso appeso resta quasi fermo e la penna lascia sulla carta una linea ondulata; finita la scossa la linea torna diritta. Il modello registra le oscillazioni, non prevede i terremoti."),
    "esperimento-spugna-saturazione": (r_spugna,
        "Animazione: la spugna che assorbe e la spugna satura",
        "A sinistra poche gocce cadono sulla spugna e vengono assorbite. A destra il getto d'acqua continua su una spugna già piena: l'acqua scorre via e trascina granelli di terra nel piatto. È un modello semplificato, non una previsione di frana."),
    "radici-erosione-terreno": (r_radici,
        "Animazione: la pioggia sul pendio con le radici e su quello nudo",
        "La pioggia cade sui due pendii. Dove ci sono erba e radici scorre soprattutto acqua; sul terreno nudo l'acqua porta via granelli di terra lungo il pendio. Le radici limitano l'erosione superficiale, ma non impediscono ogni frana."),
    "pioggia-prato-asfalto": (r_prato,
        "Animazione: la pioggia sul prato e sull'asfalto",
        "La pioggia cade su prato e asfalto. Nel prato le gocce entrano nel terreno; sull'asfalto l'acqua scorre in superficie fino alla caditoia. Schema semplificato: l'infiltrazione dipende anche dal tipo e dallo stato del terreno."),
    "esperimento-pluviometro": (r_pluviometro,
        "Animazione: il pluviometro che si riempie",
        "La pioggia entra nell'imbuto e il livello dell'acqua nella bottiglia sale piano; a destra lo stesso livello si legge sulla scala. Per avere i millimetri di pioggia la scala va tarata sull'area dell'imbuto."),
    "esperimento-maremoto-fondale": (r_maremoto,
        "Animazione: l'onda di maremoto che cresce vicino alla costa",
        "In mare profondo l'onda corre veloce ed è bassa; quando il fondale sale verso la costa rallenta e diventa più alta. Intanto la persona si allontana dalla riva verso un punto alto."),
    "esperimento-tombino-ostruito": (r_tombino,
        "Animazione: la stessa acqua su griglia libera, mezza coperta e quasi chiusa",
        "Dalla stessa caraffa si versa la stessa acqua sulle tre griglie. Con la griglia libera l'acqua passa subito e il contenitore sotto si riempie; con la griglia mezza coperta passa meno acqua e sopra si forma una pozza; con la griglia quasi chiusa sotto arriva pochissima acqua e la pozza sopra è più alta. L'esperimento si fa sul tavolo, mai in strada."),
    "triangolo-del-fuoco": (r_triangolo,
        "Animazione: senza ossigeno la fiamma si spegne",
        "Il triangolo mostra i tre elementi del fuoco: combustibile, comburente e calore. Quando l'ossigeno dell'aria viene a mancare, come sotto il barattolo, la fiamma si riduce e si spegne. Poi l'animazione ricomincia da capo. Schema semplificato, non una procedura di spegnimento."),
    "esperimento-superfici-calore": (r_calore,
        "Animazione: superficie chiara e superficie scura sotto lo stesso sole",
        "Lo stesso sole illumina le due superfici. Quella chiara rimanda indietro più luce e il suo termometro sale poco; quella scura assorbe più luce, si scalda di più e il suo termometro sale di più. Non sono temperature reali."),
    "esperimento-manica-vento": (r_manica,
        "Animazione: la manica a vento con vento debole e con vento più forte",
        "Con vento debole la manica si muove piano e resta poco gonfia; con vento più forte si distende nella direzione in cui scorre l'aria e vibra. Osserva da un posto sicuro, mai durante un temporale."),
    "esperimento-lampo-tuono": (r_lampo,
        "Animazione: dal lampo al tuono contando i secondi",
        "Il lampo si vede subito e il bambino comincia a contare i secondi, da 1 a 9. Il suono del tuono viaggia più lento e arriva quando il conteggio è a 9: 9 secondi diviso 3 fa circa 3 chilometri. Al primo tuono entra al chiuso ed esci 30 minuti dopo l'ultimo tuono."),
}


def genera(nome: str) -> str:
    ricetta, titolo, descrizione = RICETTE[nome]
    s = (SRC / f"{nome}.svg").read_text(encoding="utf-8")
    s = s.replace("\r\n", "\n")
    s, css, overlay = ricetta(s, nome)
    # titolo e descrizione: quelli dell'animazione
    s = sostituisci_re(s, r"<title id=\"([^\"]+)\">[^<]*</title>", lambda m: f'<title id="{m.group(1)}">{titolo}</title>', 1, nome)
    s = sostituisci_re(s, r"<desc id=\"([^\"]+)\">[^<]*</desc>", lambda m: f'<desc id="{m.group(1)}">{descrizione}</desc>', 1, nome)
    stile = f"<style>{BASE_CSS}{css}</style>"
    s = sostituisci_re(s, r"(<svg [^>]*>)", lambda m: m.group(1) + stile, 1, nome)
    if not s.rstrip().endswith("</svg>"):
        raise SystemExit(f"{nome}: il file non finisce con </svg>")
    s = s.rstrip()[: -len("</svg>")] + overlay + "</svg>\n"
    return s


def main() -> int:
    controlla = "--check" in sys.argv[1:]
    OUT.mkdir(exist_ok=True)
    diversi = []
    for nome in RICETTE:
        atteso = genera(nome)
        dest = OUT / f"{nome}-animata.svg"
        if controlla:
            if not dest.exists() or dest.read_text(encoding="utf-8") != atteso:
                diversi.append(dest.relative_to(ROOT))
        else:
            if not dest.exists() or dest.read_text(encoding="utf-8") != atteso:
                dest.write_text(atteso, encoding="utf-8")
                print(f"scritto {dest.relative_to(ROOT)}")
    # la descrizione dell'animazione nella pagina (alt_animazione) deve
    # coincidere con quella dentro l'SVG: è lo stesso testo, in due posti
    pagina = (ROOT / "content/formazione/esperimenti.md").read_text(encoding="utf-8")
    for nome, (_, _, descrizione) in RICETTE.items():
        m = re.search(r'animazione="/formazione/illustrazioni-udl/animate/' + re.escape(nome)
                      + r'-animata\.svg" alt_animazione="([^"]*)"', pagina)
        if not m:
            diversi.append(f"content/formazione/esperimenti.md: manca l'animazione di {nome}")
        elif m.group(1) != descrizione:
            diversi.append(f"content/formazione/esperimenti.md: alt_animazione di {nome} diverso dalla descrizione nel generatore")
    previsti = {f"{n}-animata.svg" for n in RICETTE}
    estranei = sorted(p.name for p in OUT.glob("*.svg") if p.name not in previsti)
    if controlla:
        if diversi or estranei:
            for d in diversi:
                print(f"❌ {d}: allinea pagina e generatore, poi rilancia python3 scripts/genera-animazioni-esperimenti.py")
            for e in estranei:
                print(f"❌ {e} in animate/ non ha una ricetta nel generatore")
            return 1
        print(f"✅ {len(RICETTE)} animazioni allineate ai disegni statici")
    return 0


if __name__ == "__main__":
    sys.exit(main())
