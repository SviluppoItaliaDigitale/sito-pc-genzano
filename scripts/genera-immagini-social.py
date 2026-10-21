#!/usr/bin/env python3
"""Genera immagini Instagram (post 1080x1350 e story 1080x1920) a partire
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
  social-bozze/<slug>/testi-alternativi.json (testo alternativo di ogni immagine)

Nomi a prova di errore: "feed-" = post nel feed (Instagram + Facebook),
"storia" = storia verticale 24h. Il numero del carosello è l'ordine di caricamento.

testi-alternativi.json (dal 21/10/2026) descrive a parole ogni immagine, per chi
usa un lettore di schermo: la pubblicazione automatica lo invia a Instagram e a
Facebook. Nasce solo da ciò che la grafica disegna (sezione «Testi
alternativi»). È facoltativo: senza, i post escono come prima.

Formato: JPEG quality 90. Universalmente accettato da Instagram, Facebook,
X, Telegram, LinkedIn. WebP non funziona per upload su Instagram (web e
app mobile lo rifiutano). PNG sarebbe accettato ma 3-5x più pesante senza
benefici visibili sul nostro template (sfondi piatti + testo).

Uso:
  python3 scripts/genera-immagini-social.py content/comunicazioni/2026-04-20-articolo.md
  python3 scripts/genera-immagini-social.py --all
  python3 scripts/genera-immagini-social.py --force <articolo>
  python3 scripts/genera-immagini-social.py --out-dir /tmp/prove <articolo>   # prova
  python3 scripts/genera-immagini-social.py --solo-testi-alternativi --all
      # aggiunge testi-alternativi.json al materiale già fatto degli articoli
      # ancora nella finestra di pubblicazione (72 ore), senza toccare le
      # immagini: le ridisegna in una cartella provvisoria e scrive il file
      # solo se coincidono con quelle che ci sono.

Ogni immagine porta lungo i bordi una cornice di microtesto con la provenienza
(scripts/microtesto_cornice.py): invisibile da lontano, leggibile ingrandendo.

Il testo non viene MAI tagliato (dal 13/10/2026): ogni blocco sceglie il corpo
a cui entra intero, la sintesi si divide su più slide, e se il testo non entra
lo stesso la generazione si ferma (TestoIncompleto, uscita 1): nessuna immagine
nuova, e quelle di prima dell'articolo si tolgono, perché il repository social
non le pubblichi al posto delle nuove. Vedi la sezione «Testo sempre intero» e
scripts/check-grafiche-social.py.

Dipendenze: Pillow (pip install Pillow), font-liberation (apt: fonts-liberation).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from itertools import combinations
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import social_comune  # noqa: E402
from microtesto_cornice import cornice_microtesto  # noqa: E402

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


# Testi alternativi delle immagini, scritti accanto a loro (sezione «Testi
# alternativi» più sotto).
TESTI_ALTERNATIVI = "testi-alternativi.json"

# Le immagini che questo script scrive in una cartella: i nomi attuali e quelli
# vecchi (instagram-post*/instagram-story*, .webp di prima del 2 maggio 2026),
# più i loro testi alternativi, che descrivono quelle immagini e non hanno
# senso senza di loro.
IMMAGINI_GENERATE = ("feed-*.jpg", "storia.jpg",
                     "instagram-post*.jpg", "instagram-post*.webp",
                     "instagram-story*.jpg", "instagram-story*.webp",
                     TESTI_ALTERNATIVI)


def nome_feed(numero: int, totale: int) -> str:
    """Nome del file di una slide del feed: `feed-post.jpg` se il post ha una
    sola immagine, `feed-carosello-N.jpg` se è un carosello."""
    return "feed-post.jpg" if totale == 1 else f"feed-carosello-{numero}.jpg"


def togli_immagini(out_dir: Path) -> int:
    """Toglie le immagini generate per un articolo (e i loro testi
    alternativi); restituisce quanti file erano."""
    tolte = 0
    for pat in IMMAGINI_GENERATE:
        for vecchia in out_dir.glob(pat):
            vecchia.unlink()
            tolte += 1
    return tolte


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
    """Spezza un testo in righe che entrano nella larghezza_max, misurata dal
    punto in cui la riga viene disegnata al bordo destro dell'ultimo segno.
    Non scarta mai parole: una parola più larga dello spazio resta da sola su
    una riga, e la scarta poi il controllo di adatta_blocco (corpo più piccolo)."""
    parole = testo.split()
    if not parole:
        return []
    righe = []
    riga = parole[0]
    for parola in parole[1:]:
        candidato = riga + " " + parola
        if draw.textbbox((0, 0), candidato, font=font)[2] <= larghezza_max:
            riga = candidato
        else:
            righe.append(riga)
            riga = parola
    righe.append(riga)
    return righe


# ---------------------------------------------------------------------------
# Testo sempre intero (13/10/2026)
# ---------------------------------------------------------------------------
# Fino al 13/10/2026 ogni blocco di testo era troncato a un numero fisso di
# righe: tre per ogni punto della sintesi, cinque, sei o otto per titoli e
# citazione, 240 caratteri con i puntini per la descrizione della storia. Il
# post sul soccorso alpino del 13/10/2026 è uscito su Instagram e Facebook con
# tre punti su quattro tagliati a metà frase. Da quel giorno:
#   - ogni blocco sceglie il corpo più grande a cui il testo entra INTERO nel
#     suo riquadro, fino a un corpo minimo ancora leggibile da telefono;
#   - la sintesi, se non entra in una slide, si divide su più slide, sempre a
#     punti interi e nell'ordine dell'articolo;
#   - prima di disegnare, ogni riga viene confrontata con il suo riquadro e il
#     testo impaginato con quello originale, parola per parola;
#   - se il testo non entra nemmeno così, o contiene un carattere che il font
#     non sa disegnare, la generazione si ferma con TestoIncompleto e non
#     scrive nessuna immagine: meglio nessun post che un post con una frase a
#     metà. Lo stesso calcolo lo usa scripts/check-grafiche-social.py,
#     bloccante sulle pull request, perché il problema si veda prima del merge.
# Non rimettere limiti di righe con lo slicing ([:3], [:6]...) né tagli di
# caratteri con i puntini: è esattamente il difetto che questa sezione elimina.

# Corpo massimo (quello di sempre) e minimo leggibile di ogni blocco, in pixel.
TITOLO_CORPO = (74, 52)
CITAZIONE_CORPO = (60, 44)
PUNTI_CORPO = (46, 38)
STORIA_TITOLO_CORPO = (58, 46)
STORIA_DESCR_CORPO = (30, 26)
# Geometria fissa delle slide 1080×1350 e della storia 1080×1920.
AREA_TESTO_FONDO = 1350 - 200      # sotto inizia la sfumatura con l'indirizzo
PUNTI_X, PUNTI_Y, PUNTI_LARGHEZZA = 120, 340, 850
STORIA_FONDO = 1920 - 250          # sotto c'è il richiamo «Leggi sul sito»
MAX_SLIDE_CAROSELLO = 10           # limite di Instagram


class TestoIncompleto(RuntimeError):
    """Il testo non uscirebbe intero nella grafica: troppo lungo anche al corpo
    minimo, oppure con caratteri che il font non sa disegnare."""


# Caratteri senza disegno per natura (selettori di variante, spazi a larghezza
# zero, segni combinanti): non vanno contati fra quelli mancanti.
_SENZA_DISEGNO = {"Cf", "Mn", "Me"}
_FONT_CACHE: dict = {}
_MISURA = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def carattere(peso: str, corpo: int) -> ImageFont.FreeTypeFont:
    chiave = (peso, corpo)
    if chiave not in _FONT_CACHE:
        _FONT_CACHE[chiave] = ImageFont.truetype(str(find_font(peso)), corpo)
    return _FONT_CACHE[chiave]


def caratteri_mancanti(testo: str, ft: ImageFont.FreeTypeFont) -> list[str]:
    """Caratteri che il font non sa disegnare: uscirebbero come uno spazio vuoto.
    Titillium Web non ha, per esempio, → ≥ ≤ ≈ ‰ № e nessuna emoji."""
    mancanti = []
    for ch in dict.fromkeys(testo):
        if ch.isspace() or unicodedata.category(ch) in _SENZA_DISEGNO:
            continue
        if ft.getmask(ch).getbbox() is None:
            mancanti.append(ch)
    return mancanti


_PEDICI = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def per_grafica(testo: str) -> str:
    """Il testo come va disegnato: spazi normalizzati e pedici numerici resi con
    cifre normali (CO₂ → CO2, PM₂.₅ → PM2.5), che Titillium Web non ha. Nessuna
    parola si perde: cambia solo la grafia di quei segni."""
    return " ".join(str(testo or "").translate(_PEDICI).split())


def _controlla_caratteri(testo: str, peso: str, nome: str) -> None:
    mancanti = caratteri_mancanti(per_grafica(testo), carattere(peso, 40))
    if mancanti:
        elenco = " ".join(f"«{c}» (U+{ord(c):04X})" for c in mancanti)
        raise TestoIncompleto(
            f"{nome}: caratteri che il font non sa disegnare, uscirebbero come "
            f"spazi vuoti: {elenco}. Riscriverli a parole (per esempio «almeno», "
            f"«oltre», «circa», «verso»).")


def altezza_righe(n: int, ft: ImageFont.FreeTypeFont, passo: int) -> int:
    """Ingombro verticale di n righe disegnate a passo costante: dalla linea
    degli ascendenti della prima riga a quella dei discendenti dell'ultima."""
    if n <= 0:
        return 0
    ascendente, discendente = ft.getmetrics()
    return (n - 1) * passo + ascendente + discendente


def _righe_entrano(righe: list[str], ft, larghezza: int) -> bool:
    return all(_MISURA.textbbox((0, 0), r, font=ft)[2] <= larghezza for r in righe)


def adatta_blocco(testo: str, peso: str, corpi: tuple, larghezza: int,
                  altezza: int, interlinea: float, nome: str):
    """Il corpo più grande, fra corpi[0] e corpi[1], a cui `testo` entra intero
    nel riquadro larghezza × altezza. Ritorna (font, righe, passo); se non
    entra nemmeno al corpo minimo, TestoIncompleto."""
    testo = per_grafica(testo)
    if not testo:
        raise TestoIncompleto(f"{nome}: testo vuoto")
    _controlla_caratteri(testo, peso, nome)
    corpo_max, corpo_min = corpi
    for corpo in range(corpo_max, corpo_min - 1, -2):
        ft = carattere(peso, corpo)
        righe = wrap_testo(_MISURA, testo, ft, larghezza)
        passo = round(corpo * interlinea)
        if (altezza_righe(len(righe), ft, passo) <= altezza
                and _righe_entrano(righe, ft, larghezza)):
            return ft, righe, passo
    raise TestoIncompleto(
        f"{nome}: troppo lungo per la grafica anche al corpo minimo "
        f"({corpo_min} px): {len(testo)} caratteri. Accorciarlo nel frontmatter.")


def controlla_integro(righe: list[str], testo: str, nome: str) -> None:
    """Il testo impaginato deve essere quello originale, parola per parola."""
    if " ".join(righe).split() != per_grafica(testo).split():
        raise TestoIncompleto(f"{nome}: il testo impaginato non coincide con l'originale")


def scrivi_righe(draw: ImageDraw.ImageDraw, x: int, y: int, righe: list[str],
                 ft: ImageFont.FreeTypeFont, passo: int, riquadro: tuple,
                 colore: tuple, nome: str) -> tuple:
    """Disegna le righe solo dopo aver verificato che ognuna stia per intero
    nel riquadro (x0, y0, x1, y1). Ritorna l'ingombro reale del blocco."""
    x0, y0, x1, y1 = riquadro
    scatole = []
    for i, riga in enumerate(righe):
        s = draw.textbbox((x, y + i * passo), riga, font=ft)
        if s[0] < x0 or s[1] < y0 or s[2] > x1 or s[3] > y1:
            raise TestoIncompleto(
                f"{nome}: la riga «{riga}» uscirebbe dal suo spazio "
                f"({s} fuori da {riquadro})")
        scatole.append(s)
    for i, riga in enumerate(righe):
        draw.text((x, y + i * passo), riga, font=ft, fill=colore)
    return (min(s[0] for s in scatole), min(s[1] for s in scatole),
            max(s[2] for s in scatole), max(s[3] for s in scatole))


def impagina_punti(punti: list) -> dict | None:
    """Divide i punti della sintesi in slide e sceglie il corpo. Ogni slide
    contiene punti interi, nell'ordine dell'articolo; si usa il minor numero di
    slide possibile e, a parità, il corpo più grande e la divisione più
    equilibrata. Ritorna {"corpo": int, "pagine": [[(testo, righe), ...], ...]}
    oppure None se non ci sono punti."""
    punti = [per_grafica(p) for p in punti if str(p).strip()]
    if not punti:
        return None
    for i, p in enumerate(punti, 1):
        _controlla_caratteri(p, "Semibold", f"social_punti, punto {i}")
    altezza = AREA_TESTO_FONDO - PUNTI_Y
    corpi = list(range(PUNTI_CORPO[0], PUNTI_CORPO[1] - 1, -2))
    misure = {}
    for corpo in corpi:
        ft = carattere("Semibold", corpo)
        passo, spazio = _passi_punti(corpo)
        righe = [wrap_testo(_MISURA, p, ft, PUNTI_LARGHEZZA) for p in punti]
        if not all(_righe_entrano(rr, ft, PUNTI_LARGHEZZA) for rr in righe):
            continue  # una parola più larga dello spazio: corpo troppo grande
        alt = [altezza_righe(len(rr), ft, passo) for rr in righe]
        misure[corpo] = (righe, alt, spazio)

    n = len(punti)
    for k in range(1, n + 1):
        migliore = None
        for tagli in combinations(range(1, n), k - 1):
            confini = (0, *tagli, n)
            for corpo, (righe, alt, spazio) in misure.items():
                altezze = [sum(alt[a:b]) + spazio * (b - a - 1)
                           for a, b in zip(confini, confini[1:])]
                if max(altezze) <= altezza:
                    chiave = (corpo, -max(altezze))
                    if migliore is None or chiave > migliore[0]:
                        migliore = (chiave, corpo, confini)
                    break  # i corpi sono in ordine decrescente
        if migliore:
            _, corpo, confini = migliore
            righe = misure[corpo][0]
            pagine = [[(punti[i], righe[i]) for i in range(a, b)]
                      for a, b in zip(confini, confini[1:])]
            return {"corpo": corpo, "pagine": pagine}
    raise TestoIncompleto(
        f"social_punti: un punto non entra in una slide nemmeno al corpo minimo "
        f"({PUNTI_CORPO[1]} px), oppure contiene una parola più larga della slide. "
        f"Accorciarlo nel frontmatter.")


def _passi_punti(corpo: int) -> tuple[int, int]:
    """Passo fra le righe e spazio fra i punti, in proporzione al corpo 46."""
    return round(corpo * 60 / 46), round(corpo * 30 / 46)


def piano_storia(titolo: str, descrizione: str, inizio: int,
                 fondo: int = STORIA_FONDO, W: int = 1080) -> dict | None:
    """Titolo e descrizione della storia, interi, fra `inizio` e `fondo`: prima
    ai corpi pieni, poi riducendoli insieme. None se non entrano."""
    larghezza = W - 140
    titolo = per_grafica(titolo)
    descrizione = per_grafica(descrizione)
    t_max, t_min = STORIA_TITOLO_CORPO
    d_max, d_min = STORIA_DESCR_CORPO
    passi = max(t_max - t_min, d_max - d_min) // 2 + 1
    for i in range(passi):
        ct = max(t_min, t_max - 2 * i)
        cd = max(d_min, d_max - round(2 * i * (d_max - d_min) / (t_max - t_min)))
        ft_t = carattere("Bold", ct)
        passo_t = round(ct * 74 / 58)
        righe_t = wrap_testo(_MISURA, titolo, ft_t, larghezza)
        if not _righe_entrano(righe_t, ft_t, larghezza):
            continue
        alt = altezza_righe(len(righe_t), ft_t, passo_t)
        righe_d, ft_d, passo_d = [], None, 0
        if descrizione:
            ft_d = carattere("Regular", cd)
            passo_d = round(cd * 44 / 30)
            righe_d = wrap_testo(_MISURA, descrizione, ft_d, larghezza)
            if not _righe_entrano(righe_d, ft_d, larghezza):
                continue
            alt += 26 + altezza_righe(len(righe_d), ft_d, passo_d)
        if inizio + alt <= fondo:
            return {"ft_t": ft_t, "righe_t": righe_t, "passo_t": passo_t,
                    "ft_d": ft_d, "righe_d": righe_d, "passo_d": passo_d}
    return None


def _altezza_badge(badge: str) -> int:
    """Altezza della pastiglia del badge: corpo 30 e 16 px sopra e sotto."""
    tb = _MISURA.textbbox((0, 0), badge.upper(), font=carattere("Bold", 30))
    return (tb[3] - tb[1]) + 32


def _disegna_badge(d: ImageDraw.ImageDraw, badge: str, x: int, y: int) -> None:
    ft = carattere("Bold", 30)
    txt = badge.upper()
    tb = d.textbbox((0, 0), txt, font=ft)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = 30, 16
    d.rounded_rectangle([(x, y), (x + tw + px * 2, y + th + py * 2)],
                        radius=(th + py * 2) // 2, fill=_badge_colore(badge))
    d.text((x + px, y + py - tb[1]), txt, font=ft, fill=WHITE)


def piano_titolo(titolo: str, badge: str) -> dict:
    """Impaginazione del titolo nella prima slide (sotto il badge)."""
    area_top = 250 + (_altezza_badge(badge) + 56 if badge else 0)
    nome = "titolo (prima slide)"
    ft, righe, passo = adatta_blocco(titolo, "Bold", TITOLO_CORPO, 1080 - 200,
                                     AREA_TESTO_FONDO - area_top, 90 / 74, nome)
    controlla_integro(righe, titolo, nome)
    return {"area_top": area_top, "ft": ft, "righe": righe, "passo": passo}


def piano_citazione(testo: str) -> dict:
    """Impaginazione della slide con social_citazione (sotto le virgolette)."""
    area_top = 440
    nome = "social_citazione"
    ft, righe, passo = adatta_blocco(testo, "Semibold", CITAZIONE_CORPO, 1080 - 200,
                                     AREA_TESTO_FONDO - area_top, 80 / 60, nome)
    controlla_integro(righe, testo, nome)
    return {"area_top": area_top, "ft": ft, "righe": righe, "passo": passo}


STORIA_FOTO_H = 720   # altezza del riquadro della foto in evidenza nella storia


def piano_storia_completo(titolo: str, descrizione: str, badge: str,
                          con_foto: bool) -> dict:
    """Impaginazione della storia con titolo e descrizione INTERI. Se con la
    foto in evidenza non entrano nemmeno ai corpi minimi, la foto si toglie; se
    ancora non entrano, si toglie la descrizione (resta il titolo, che è
    l'informazione); altrimenti TestoIncompleto. Mai una frase a metà."""
    _controlla_caratteri(titolo, "Bold", "titolo (storia)")
    if descrizione:
        _controlla_caratteri(descrizione, "Regular", "description (storia)")
    inizio = 250 + (_altezza_badge(badge) + 44 if badge else 0)
    tentativi = []
    if con_foto:
        tentativi.append((True, descrizione, inizio + STORIA_FOTO_H + 56))
    tentativi.append((False, descrizione, inizio))
    if descrizione:
        tentativi.append((False, "", inizio))
    for foto, descr, testo_da in tentativi:
        piano = piano_storia(titolo, descr, testo_da)
        if piano is None:
            continue
        controlla_integro(piano["righe_t"], titolo, "titolo (storia)")
        if descr:
            controlla_integro(piano["righe_d"], descr, "description (storia)")
        piano.update(con_foto=foto, inizio=inizio,
                     descrizione_tolta=bool(descrizione) and not descr)
        return piano
    raise TestoIncompleto(
        f"titolo (storia): troppo lungo per la storia anche al corpo minimo "
        f"({STORIA_TITOLO_CORPO[1]} px). Accorciarlo nel frontmatter.")


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


# I JPEG sono salvati BASELINE, non progressive: la Content Publishing API di
# Instagram rifiuta i progressive con l'errore "Only photo or video can be
# accepted as media type" (code 9004). Verificato sul campo il 20/09/2026, alla
# prima pubblicazione automatica. Non rimettere progressive=True.


def _salva_jpeg(base: Image.Image, out_path: Path, quality: int = 92, **extra) -> None:
    """Applica la cornice di microtesto sui bordi dell'immagine composta (mai
    sopra le foto, che stanno sempre ad almeno 60 px dal bordo) e salva il
    JPEG baseline. Cornice decorativa: provenienza del Gruppo + dominio + anno."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img = cornice_microtesto(base.convert("RGB"), corpo=8)
    img.save(out_path, "JPEG", quality=quality, optimize=True,
             progressive=False, **extra)


def crea_slide_titolo(titolo: str, badge: str, out_path: Path,
                      W: int = 1080, H: int = 1350) -> Path:
    """Slide 1 del carosello / post singolo: card-titolo verticale nativa 4:5.
    Costruita a misura: riempie perfettamente, senza ritagli né bande."""
    base = _sfondo_titolo(W, H)
    _barra_brand(base, W)
    d = ImageDraw.Draw(base)
    d.line([(60, 190), (W - 60, 190)], fill=(255, 255, 255, 55), width=2)

    # Titolo INTERO: il corpo scende da 74 a 52 px finché entra (mai troncato).
    # Il piano si calcola prima di disegnare: se il titolo non entra, nessuna slide.
    piano = piano_titolo(titolo, badge)
    if badge:
        _disegna_badge(d, badge, 60, 250)
    area_top, area_bot = piano["area_top"], AREA_TESTO_FONDO
    ft_tit, righe, line_h = piano["ft"], piano["righe"], piano["passo"]
    blocco_h = altezza_righe(len(righe), ft_tit, line_h)
    ty = area_top + (area_bot - area_top - blocco_h) // 2
    ingombro = scrivi_righe(d, 100, ty, righe, ft_tit, line_h,
                            (100, area_top, W - 100, area_bot), WHITE,
                            "titolo (prima slide)")
    d.rectangle([(60, ingombro[1]), (72, ingombro[3])], fill=ACCENT)

    base.alpha_composite(scrim(W, 170, dall_alto=False, alpha_max=150), (0, H - 170))
    d.text((60, H - 92), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)

    _salva_jpeg(base, out_path)
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

    _salva_jpeg(base, out_path)
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
    # Citazione INTERA: il corpo scende da 60 a 44 px finché entra (mai troncata).
    piano = piano_citazione(testo)
    area_top, area_bot = piano["area_top"], AREA_TESTO_FONDO
    ft, righe, line_h = piano["ft"], piano["righe"], piano["passo"]
    blocco_h = altezza_righe(len(righe), ft, line_h)
    ty = area_top + (area_bot - area_top - blocco_h) // 2
    scrivi_righe(d, 100, ty, righe, ft, line_h,
                 (100, area_top, W - 100, area_bot), WHITE, "social_citazione")
    base.alpha_composite(scrim(W, 170, dall_alto=False, alpha_max=150), (0, H - 170))
    d.text((60, H - 92), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)
    _salva_jpeg(base, out_path)
    return out_path


def crea_slide_punti(pagina: list, out_path: Path, corpo: int = PUNTI_CORPO[0],
                     numero: int = 1, totale: int = 1,
                     W: int = 1080, H: int = 1350) -> Path:
    """Slide 'In sintesi': i punti chiave dell'articolo (frontmatter social_punti),
    mai inventati e mai tagliati. `pagina` viene da impagina_punti(): ogni punto
    è intero e il corpo è già quello a cui tutti i punti della slide entrano;
    se la sintesi occupa più slide, l'intestazione porta «1/2», «2/2»."""
    base = _sfondo_titolo(W, H)
    _barra_brand(base, W)
    d = ImageDraw.Draw(base)
    d.line([(60, 190), (W - 60, 190)], fill=(255, 255, 255, 55), width=2)
    intestazione = "IN SINTESI" if totale == 1 else f"IN SINTESI · {numero}/{totale}"
    d.text((60, 238), intestazione,
           font=ImageFont.truetype(str(find_font("Bold")), 36), fill=ACCENT)
    ft = carattere("Semibold", corpo)
    passo, spazio = _passi_punti(corpo)
    diametro, scarto = round(corpo * 26 / 46), round(corpo * 18 / 46)
    riquadro = (PUNTI_X, PUNTI_Y, PUNTI_X + PUNTI_LARGHEZZA, AREA_TESTO_FONDO)
    y = PUNTI_Y
    for testo, righe in pagina:
        controlla_integro(righe, testo, "social_punti")
        d.ellipse([(64, y + scarto), (64 + diametro, y + scarto + diametro)], fill=ACCENT)
        scrivi_righe(d, PUNTI_X, y, righe, ft, passo, riquadro, WHITE, "social_punti")
        y += altezza_righe(len(righe), ft, passo) + spazio
    base.alpha_composite(scrim(W, 170, dall_alto=False, alpha_max=150), (0, H - 170))
    d.text((60, H - 92), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)
    _salva_jpeg(base, out_path)
    return out_path


# Loghi della slide finale, con le righe scritte sotto ciascuno e l'eventuale
# codice: (file in static/images, righe, codice). Le stesse righe servono al
# testo alternativo della slide (alt_affiliazioni), così i due non divergono.
AFFILIAZIONI = (
    ("logo-esc-quality-label-it.png",
     ("Quality Label", "European Solidarity Corps"), "Codice: E10435833"),
    ("logo-fepivol.png",
     ("Coordinamento", "FE.PI.VOL.", "Volontariato Lazio"), None),
    ("logo-snpc-volontariato.png",
     ("Servizio Nazionale", "di Protezione Civile"), None),
)


def crea_slide_affiliazioni(out_path: Path,
                            W: int = 1080, H: int = 1350) -> Path:
    """Slide finale 'Affiliazioni e riconoscimenti': 3 loghi affiancati.
    - Quality Label ESC (codice E10435833 obbligatorio per Reg. UE 2021/888)
    - Coordinamento FEPIVOL (Federazione Pronto Intervento Volontariato ODV)
    - SNPC Volontariato (Servizio Nazionale Protezione Civile)
    Sempre come ultima slide del carosello: dichiara la legittimazione del
    Gruppo davanti al pubblico social. Il logo PC Genzano NON è qui: è la
    firma istituzionale (barra brand top di ogni slide), non un'affiliazione."""
    base = _sfondo_titolo(W, H)
    _barra_brand(base, W)
    d = ImageDraw.Draw(base)

    d.line([(60, 190), (W - 60, 190)], fill=(255, 255, 255, 55), width=2)
    d.text((60, 238), "AFFILIAZIONI E RICONOSCIMENTI",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=ACCENT)

    # 3 loghi affiancati in card bianche rotonde — ESC usa la versione HI-RES
    # 4016x4016 ufficiale UE per massima nitidezza (cerchio Quality Label).
    loghi = [(IMAGES_DIR / file, righe, codice) for file, righe, codice in AFFILIAZIONI]

    # Card più grandi per maggiore nitidezza visiva post-compressione JPEG
    card_size = 280
    gap = 30
    total_w = card_size * 3 + gap * 2
    base_x = (W - total_w) // 2
    base_y = 360

    for idx, (lp, _, _) in enumerate(loghi):
        x = base_x + idx * (card_size + gap)
        card = Image.new("RGBA", (card_size, card_size), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.ellipse([(0, 0), (card_size, card_size)], fill=WHITE)
        if lp.exists():
            li = Image.open(lp).convert("RGBA")
            # Scaling LANCZOS sulla risoluzione originale (massima nitidezza)
            li.thumbnail((card_size - 36, card_size - 36), Image.LANCZOS)
            lx = (card_size - li.width) // 2
            ly = (card_size - li.height) // 2
            card.paste(li, (lx, ly), li)
        base.alpha_composite(card, (x, base_y))

    # Etichette sotto ogni logo
    lab_ft = ImageFont.truetype(str(find_font("Semibold")), 22)
    code_ft = ImageFont.truetype(str(find_font("Bold")), 22)
    labels_y = base_y + card_size + 25

    for idx, (_, lines, code) in enumerate(loghi):
        cx = base_x + idx * (card_size + gap) + card_size // 2
        yy = labels_y
        for ln in lines:
            tb = d.textbbox((0, 0), ln, font=lab_ft)
            d.text((cx - (tb[2] - tb[0]) // 2, yy), ln, font=lab_ft, fill=WHITE)
            yy += 30
        if code:
            tb = d.textbbox((0, 0), code, font=code_ft)
            d.text((cx - (tb[2] - tb[0]) // 2, yy + 8), code, font=code_ft, fill=ACCENT)

    # Footer CTA URL
    base.alpha_composite(scrim(W, 170, dall_alto=False, alpha_max=150), (0, H - 170))
    d.text((60, H - 92), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Bold")), 30), fill=WHITE)

    # JPEG quality 95 (era 92) per ridurre artifact su dettagli fini dei loghi
    _salva_jpeg(base, out_path, quality=95, subsampling=0)
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

    # Titolo e descrizione INTERI (dal 13/10/2026 niente più tagli a 5 righe né
    # descrizione accorciata con i puntini): vedi piano_storia_completo().
    piano = piano_storia_completo(titolo, descrizione, badge, bool(featured))
    if featured and not piano["con_foto"]:
        print("  ! storia: testo lungo, tolgo la foto per farlo entrare intero",
              file=sys.stderr)
        featured = None
    if piano["descrizione_tolta"]:
        print("  ! storia: descrizione troppo lunga anche senza foto, la tolgo "
              "(nessuna frase tagliata)", file=sys.stderr)

    # Badge sotto la barra brand (una volta sola)
    if badge:
        _disegna_badge(d, badge, 70, 250)
    testo_y = piano["inizio"]
    box_h = STORIA_FOTO_H

    # Foto reale in evidenza (NON la cover tipografica, che ripeterebbe titolo).
    if featured:
        fsrc = Image.open(featured).convert("RGB")
        box_w = W - 140
        fw, fh = fit_size(fsrc.width, fsrc.height, box_w, box_h)
        cov = fsrc.resize((fw, fh), Image.LANCZOS)
        cy = testo_y
        incolla_card(base, cov, (W - fw) // 2, cy + (box_h - fh) // 2)
        testo_y = cy + box_h + 56

    riquadro = (70, testo_y, W - 70, STORIA_FONDO)
    scrivi_righe(d, 70, testo_y, piano["righe_t"], piano["ft_t"], piano["passo_t"],
                 riquadro, WHITE, "titolo (storia)")
    testo_y += altezza_righe(len(piano["righe_t"]), piano["ft_t"], piano["passo_t"]) + 26
    if piano["righe_d"]:
        scrivi_righe(d, 70, testo_y, piano["righe_d"], piano["ft_d"], piano["passo_d"],
                     riquadro, (223, 234, 245), "description (storia)")

    # CTA footer (dentro la safe-zone bassa). La freccia è disegnata: il
    # carattere «→» non esiste in Titillium Web e usciva come uno spazio vuoto.
    base.alpha_composite(scrim(W, 230, dall_alto=False, alpha_max=210), (0, H - 230))
    ft_cta = ImageFont.truetype(str(find_font("Bold")), 38)
    _, sup, _, inf = d.textbbox((0, H - 158), "L", font=ft_cta)
    cy = (sup + inf) // 2
    d.line([(70, cy), (98, cy)], fill=WHITE, width=5)
    d.polygon([(92, cy - 11), (108, cy), (92, cy + 11)], fill=WHITE)
    d.text((124, H - 158), "Leggi sul sito", font=ft_cta, fill=WHITE)
    d.text((70, H - 100), "protezionecivilegenzano.it",
           font=ImageFont.truetype(str(find_font("Regular")), 30), fill=(223, 234, 245))

    _salva_jpeg(base, out_path)
    return out_path


# Uno shortcode {{< foto ... >}} (o {{% foto ... %}}) e i suoi parametri,
# fra virgolette doppie (con \" all'interno), apici inversi o virgolette semplici.
_FOTO_SHORTCODE = re.compile(r"\{\{[<%]\s*foto\s(.*?)[>%]\}\}", re.IGNORECASE | re.DOTALL)
_FOTO_PARAMETRO = re.compile(
    r"""(\w+)\s*=\s*(?:"((?:[^"\\]|\\.)*)"|`([^`]*)`|'([^']*)')""", re.DOTALL)


def estrai_foto_inline_info(body: str) -> list[dict]:
    """Le foto inline del corpo, nell'ordine dell'articolo, con i parametri
    dello shortcode foto: {"path": Path in static/, "alt": str, "caption": str}.
    Supporta sia {{< foto >}} che {{% foto %}}."""
    risultati = []
    for m in _FOTO_SHORTCODE.finditer(body):
        parametri = {}
        for p in _FOTO_PARAMETRO.finditer(m.group(1)):
            valore = next(v for v in p.groups()[1:] if v is not None)
            parametri[p.group(1).lower()] = valore.replace('\\"', '"')
        src = parametri.get("src", "").strip()
        if not src:
            continue
        risultati.append({
            # Path relativi (/images/...) -> static/images/...
            "path": ROOT / "static" / src.lstrip("/"),
            "alt": parametri.get("alt", ""),
            "caption": parametri.get("caption", ""),
        })
    return risultati


def estrai_foto_inline(body: str) -> list[Path]:
    """Estrae tutti i path delle foto inline dallo shortcode {{< foto src="..." >}}.
    Ritorna lista di Path assoluti (relativi a static/)."""
    return [f["path"] for f in estrai_foto_inline_info(body)]


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
    riga_alt = ""
    if (out_dir / TESTI_ALTERNATIVI).is_file():
        riga_alt = (f"| `{TESTI_ALTERNATIVI}` | testo alternativo di ogni immagine, "
                    f"per chi usa un lettore di schermo: la pubblicazione automatica "
                    f"lo invia a Instagram e Facebook; chi pubblica a mano lo incolla "
                    f"come testo alternativo di ciascuna immagine |\n")
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
{riga_alt}| `instagram.txt` | testo per Instagram |
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


# ---------------------------------------------------------------------------
# Testi alternativi (21/10/2026)
# ---------------------------------------------------------------------------
# Accanto alle immagini il generatore scrive testi-alternativi.json, con un
# testo alternativo per ogni immagine del feed e uno per la storia:
#   {"versione": 1,
#    "feed": {"feed-carosello-1.jpg": "…", "feed-carosello-2.jpg": "…"},
#    "storia": "…"}
# (per un post con una sola immagine la chiave è "feed-post.jpg"). Il
# repository social-pc-genzano li invia a Instagram (alt_text) e a Facebook
# (alt_text_custom), così chi usa un lettore di schermo sa che cosa dice la
# grafica (rule 03 § «Accessibilità dei post sui social media», WCAG 1.1.1).
# Regole:
#   - i testi nascono SOLO da ciò che la grafica disegna: etichetta e titolo,
#     citazione, punti della sintesi, alt e attribuzione delle foto
#     dell'articolo, titolo e descrizione della storia. Niente di inventato;
#   - al massimo 1000 caratteri (limite di Instagram per alt_text): se servisse
#     accorciare, si tolgono frasi intere dalla fine, mai una parola a metà;
#   - mai «immagine di» o «foto di» in apertura (il lettore di schermo dice già
#     che è un'immagine), niente emoji, punto finale;
#   - il file è facoltativo: se non si riesce a comporlo, le immagini escono
#     lo stesso e i post partono senza testo alternativo. Non blocca nulla.

ALT_MAX = 1000          # limite di Instagram per alt_text, in caratteri
FIRMA_GRUPPO = "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"
_FINE_FRASE = ".!?…"
_CHIUSURE = "»”\"’')]"
_APERTURE = "«“\"‘'(["
# Emoji e simboli pittografici (con selettori di variante e giunzioni): i
# lettori di schermo li leggono uno per uno. Il segno di grado e simili restano.
_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍⃣"
    "\U000E0020-\U000E007F]")
# Link Markdown, anche con parentesi tonde dentro l'indirizzo
# («…/File:Po_a_San_Benedetto_(Mantova)_1.jpg»).
_LINK_MD = re.compile(r"\[([^\]]*)\]\((?:[^()\s]|\([^()\s]*\))*\)")
_APERTURA_RIDONDANTE = re.compile(r"^(?:immagine|immagini|foto|fotografia)\s+di\s+",
                                  re.IGNORECASE)
# Etichette con cui le didascalie delle foto attribuiscono l'immagine
# («Foto: Gruppo Comunale…», «Immagine: Comune di Genzano di Roma»…).
_ETICHETTE_ATTRIBUZIONE = ("Foto", "Immagine", "Immagini", "Grafica",
                           "Illustrazione", "Infografica", "Fonte", "Mappa",
                           "Cartina", "Elaborazione", "Credito", "Crediti", "Disegno")
_ATTRIBUZIONE = re.compile(r"\b(" + "|".join(_ETICHETTE_ATTRIBUZIONE) + r")\s*:")


def alt_lunghezza(testo: str) -> int:
    """Lunghezza come la conta Instagram, in unità UTF-16: per i caratteri
    fuori dal piano di base vale 2, così il limite non si supera mai."""
    return len(testo.encode("utf-16-le")) // 2


def alt_pulisci(testo) -> str:
    """Testo pronto per un testo alternativo: link Markdown ridotti al loro
    testo (quelli verso la «fonte originale» tolti), enfasi tolta, emoji
    tolte, spazi e pedici come nella grafica (per_grafica)."""
    s = str(testo or "")
    s = _LINK_MD.sub(lambda m: "" if m.group(1).strip().lower() in
                     ("fonte originale", "fonte") else m.group(1), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", s)
    s = _EMOJI.sub("", s)
    s = re.sub(r"\(\s*\)", "", s)                  # parentesi rimaste vuote
    s = per_grafica(s)
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)         # spazio prima della punteggiatura
    return re.sub(r"(?<!\.)\.\.(?!\.)", ".", s)    # «Commons..» dopo un link tolto


def _maiuscola(testo: str) -> str:
    return testo[:1].upper() + testo[1:] if testo[:1].islower() else testo


def alt_frase(testo: str) -> str:
    """La frase finisce con un segno di fine frase: si aggiunge il punto se
    manca (dopo le virgolette di chiusura, all'italiana), e una virgola o un
    punto e virgola finali diventano punto."""
    t = re.sub(r"[\s,;:—–-]+$", "", str(testo or "").strip())
    if not t:
        return ""
    nucleo = t.rstrip(_CHIUSURE)
    if nucleo and nucleo[-1] in _FINE_FRASE:
        return t
    return t + "."


def _dividi_frasi(testo: str) -> list[str]:
    """Divide un testo in frasi: dopo . ! ? … (con eventuali virgolette o
    parentesi di chiusura) seguiti da una parola maiuscola o da un numero. Non
    divide dopo un'iniziale («J. Smith») né dentro una sigla puntata
    («FE.PI.VOL.»)."""
    parole = testo.split(" ")
    frasi, corrente = [], []
    for i, parola in enumerate(parole):
        corrente.append(parola)
        nucleo = parola.rstrip(_CHIUSURE)
        if not nucleo or nucleo[-1] not in _FINE_FRASE or i + 1 >= len(parole):
            continue
        seguente = parole[i + 1].lstrip(_APERTURE)
        if not seguente or not (seguente[0].isupper() or seguente[0].isdigit()):
            continue
        if nucleo[-1] == ".":
            radice = nucleo[:-1].lstrip(_APERTURE)
            if "." in radice or len(radice) < 2:
                continue
        frasi.append(" ".join(corrente))
        corrente = []
    if corrente:
        frasi.append(" ".join(corrente))
    return [f for f in frasi if f.strip()]


def alt_limita(testo: str, limite: int = ALT_MAX) -> str:
    """Al massimo `limite` caratteri: si tolgono frasi intere dalla fine. Solo
    se la prima frase da sola supera il limite si taglia all'ultima parola
    intera, con i puntini. Mai una parola a metà."""
    testo = " ".join(testo.split())
    if alt_lunghezza(testo) <= limite:
        return testo
    tenuto = ""
    for frase in _dividi_frasi(testo):
        candidato = f"{tenuto} {frase}".strip()
        if alt_lunghezza(candidato) > limite:
            break
        tenuto = candidato
    if tenuto:
        return tenuto
    for parola in testo.split():
        candidato = f"{tenuto} {parola}".strip()
        if alt_lunghezza(candidato + "…") > limite:
            break
        tenuto = candidato
    return re.sub(r"[\s,;:—–-]+$", "", tenuto) + "…"


def alt_virgolette(testo: str) -> str:
    """Il testo fra caporali, come una citazione: tolte le virgolette che lo
    racchiudono già, quelle interne «» diventano “”. Un punto finale esce
    dalle virgolette (lo mette la frase che le contiene: «… l'area».), mentre
    ? ! e … restano dentro."""
    t = str(testo or "").strip()
    for apre, chiude in (("«", "»"), ("“", "”"), ('"', '"')):
        interno = t[1:-1]
        if (len(t) >= 2 and t.startswith(apre) and t.endswith(chiude)
                and apre not in interno and chiude not in interno):
            t = interno.strip()
            break
    t = re.sub(r"(?<!\.)\.$", "", t).rstrip()
    t = t.replace("«", "“").replace("»", "”")
    return f"«{t}»"


def attribuzione_foto(didascalia: str) -> str:
    """L'attribuzione scritta nella didascalia di una foto («Foto: …»,
    «Immagine: …», «Fonte: …»): la frase che comincia con l'etichetta, all'inizio
    della didascalia, dopo la fine di una frase o fra parentesi. Stringa vuota
    se la didascalia non ne ha."""
    testo = alt_pulisci(didascalia)
    for m in _ATTRIBUZIONE.finditer(testo):
        prima = testo[:m.start()].rstrip()
        if prima and prima[-1] not in _FINE_FRASE + _CHIUSURE + "(":
            continue  # l'etichetta sta in mezzo a una frase: non è un'attribuzione
        resto = testo[m.start():]
        if prima.endswith("("):
            resto = resto.split(")", 1)[0]
        frase = _dividi_frasi(resto)[0] if resto.strip() else ""
        frase = re.sub(r"[\s,;:—–-]+$", "", frase)
        if len(frase) > len(m.group(0)) + 1:
            return alt_frase(frase)
    return ""


def alt_titolo(titolo: str, badge: str) -> str:
    """Prima slide: la grafica del Gruppo con l'etichetta e il titolo intero."""
    t = alt_virgolette(alt_pulisci(titolo))
    if badge:
        return (f"Grafica del {FIRMA_GRUPPO} con l'etichetta "
                f"{alt_virgolette(alt_pulisci(badge))} e il titolo {t}.")
    return f"Grafica del {FIRMA_GRUPPO} con il titolo {t}."


def alt_citazione(testo: str) -> str:
    """Slide della citazione: la frase intera dell'articolo."""
    return f"Citazione dall'articolo: {alt_virgolette(alt_pulisci(testo))}."


def alt_punti(testi: list, numero: int = 1, totale: int = 1) -> str:
    """Slide «In sintesi»: i punti interi, nell'ordine; se la sintesi è divisa
    su più slide, quale delle slide è («1 di 2»)."""
    intestazione = "In sintesi." if totale == 1 else f"In sintesi, {numero} di {totale}."
    punti = [alt_frase(_maiuscola(alt_pulisci(t))) for t in testi]
    return " ".join([intestazione] + [p for p in punti if p])


def alt_affiliazioni() -> str:
    """Slide finale: i loghi delle affiliazioni con le righe scritte sotto,
    codice del Quality Label compreso (Reg. UE 2021/888)."""
    voci = []
    for _, righe, codice in AFFILIAZIONI:
        voce = " ".join(righe)
        if codice:
            voce += ", " + re.sub(r"^Codice:\s*", "codice ", codice)
        voci.append(voce)
    return "Affiliazioni e riconoscimenti del Gruppo, con i loghi: " + "; ".join(voci) + "."


def _descrizione_foto(info: dict | None) -> str:
    """L'alt della foto, come scritto nell'articolo, senza «Foto di» in apertura."""
    if not info:
        return ""
    alt = alt_pulisci(info.get("alt", ""))
    alt = _APERTURA_RIDONDANTE.sub("", alt)
    return alt_frase(_maiuscola(alt))


def alt_foto(info: dict | None, titolo: str = "") -> str:
    """Slide di una foto: l'alt dello shortcode foto e l'attribuzione della
    didascalia, se c'è."""
    descrizione = _descrizione_foto(info)
    if not descrizione:
        # Lo shortcode foto ha sempre l'alt (Hugo si ferma senza): qui si arriva
        # solo con dati incompleti. Si dice il vero, senza inventare.
        return f"Foto dell'articolo {alt_virgolette(alt_pulisci(titolo))}."
    attribuzione = attribuzione_foto(info.get("caption", "")) if info else ""
    return f"{descrizione} {attribuzione}".strip()


def info_foto(art: dict, path) -> dict | None:
    """Alt e didascalia della foto `path`, dagli shortcode dell'articolo."""
    if path is None:
        return None
    return art.get("foto_info", {}).get(str(Path(path).resolve()))


def alt_storia(art: dict) -> str:
    """Storia: etichetta, titolo e descrizione come compaiono (la descrizione
    solo se la storia la mostra), la foto in evidenza se c'è e l'invito finale.
    Usa la stessa impaginazione di crea_story_verticale()."""
    hero = art["carousel"][1] if len(art.get("carousel") or []) > 1 else None
    con_foto = bool(hero and Path(hero).exists())
    piano = piano_storia_completo(art["title"], art.get("description", ""),
                                  art.get("badge", ""), con_foto)
    t = alt_virgolette(alt_pulisci(art["title"]))
    badge = art.get("badge", "")
    if badge:
        parti = [f"Grafica per le storie del {FIRMA_GRUPPO} con l'etichetta "
                 f"{alt_virgolette(alt_pulisci(badge))} e il titolo {t}."]
    else:
        parti = [f"Grafica per le storie del {FIRMA_GRUPPO} con il titolo {t}."]
    if piano["righe_d"]:
        parti.append(f"Sotto il titolo, il testo "
                     f"{alt_virgolette(alt_pulisci(art.get('description', '')))}.")
    if piano["con_foto"]:
        descrizione = _descrizione_foto(info_foto(art, hero))
        if descrizione:
            parti.append(f"Sopra il titolo, la foto dell'articolo. {descrizione}")
    parti.append("In fondo, l'invito «Leggi sul sito» con l'indirizzo "
                 "protezionecivilegenzano.it.")
    return " ".join(parti)


def testi_alternativi(art: dict, slides: list[tuple]) -> dict:
    """Il contenuto di testi-alternativi.json per il piano `slides`
    (piano_carosello) e la storia dell'articolo."""
    feed = {}
    for numero, (kind, data) in enumerate(slides, 1):
        if kind == "titolo":
            testo = alt_titolo(art["title"], art.get("badge", ""))
        elif kind == "citazione":
            testo = alt_citazione(data)
        elif kind == "punti":
            pagina, _corpo, n, totale = data
            testo = alt_punti([t for t, _righe in pagina], n, totale)
        elif kind == "affiliazioni":
            testo = alt_affiliazioni()
        else:
            testo = alt_foto(info_foto(art, data), art["title"])
        feed[nome_feed(numero, len(slides))] = alt_limita(testo)
    return {"versione": 1, "feed": feed, "storia": alt_limita(alt_storia(art))}


def controlla_testi_alternativi(dati: dict, nomi_feed: list[str]) -> list[str]:
    """Problemi del contenuto di testi-alternativi.json (lista vuota se va
    bene): struttura, una voce per ogni immagine del feed, nessun testo vuoto,
    più lungo di ALT_MAX, senza punto finale, con «immagine di» in apertura o
    con emoji."""
    problemi = []
    if not isinstance(dati, dict) or dati.get("versione") != 1:
        return ["manca \"versione\": 1"]
    feed = dati.get("feed")
    if not isinstance(feed, dict) or list(feed) != list(nomi_feed):
        problemi.append(f"le voci del feed {list(feed or {})} non sono le immagini {nomi_feed}")
        feed = feed if isinstance(feed, dict) else {}
    voci = list(feed.items()) + [("storia", dati.get("storia"))]
    for nome, testo in voci:
        if not isinstance(testo, str) or not testo.strip():
            problemi.append(f"{nome}: testo vuoto")
            continue
        if alt_lunghezza(testo) > ALT_MAX:
            problemi.append(f"{nome}: {alt_lunghezza(testo)} caratteri, oltre {ALT_MAX}")
        if testo.rstrip(_CHIUSURE)[-1:] not in _FINE_FRASE:
            problemi.append(f"{nome}: senza punto finale")
        if _APERTURA_RIDONDANTE.match(testo):
            problemi.append(f"{nome}: comincia con «immagine di» o «foto di»")
        if _EMOJI.search(testo):
            problemi.append(f"{nome}: contiene emoji")
    return problemi


def scrivi_testi_alternativi(cartella: Path, art: dict, slides: list[tuple]) -> bool:
    """Scrive testi-alternativi.json in `cartella`. Se i testi non si possono
    comporre o non passano il controllo, non scrive nulla, lo dice e torna
    False: le immagini escono lo stesso, i post partono senza testo alternativo."""
    try:
        dati = testi_alternativi(art, slides)
        problemi = controlla_testi_alternativi(
            dati, [nome_feed(i, len(slides)) for i in range(1, len(slides) + 1)])
    except Exception as e:  # noqa: BLE001 — i testi alternativi non bloccano le immagini
        problemi = [f"errore: {e}"]
    if problemi:
        msg = (f"testi alternativi non scritti per {art.get('slug', '?')}: "
               + "; ".join(problemi))
        print(f"  ! {msg}", file=sys.stderr)
        if os.environ.get("GITHUB_ACTIONS"):
            print(f"::warning::{msg}")
        return False
    (cartella / TESTI_ALTERNATIVI).write_text(
        json.dumps(dati, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def estrai_articolo(path: Path, crea_cover: bool = True) -> dict | None:
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
    m = re.match(r"(\d{4}-\d{2}-\d{2})", social_comune.testo_campo(fm, "date"))
    if not m:
        return None
    # Online come lo decide Hugo, in ora italiana (scripts/social_comune.py).
    if not social_comune.is_online(fm):
        return None

    # Cover principale dal frontmatter
    cover_rel = fm.get("image", "")
    cover_path = None
    if cover_rel:
        cover_path = ROOT / "static" / cover_rel.lstrip("/")
        if not cover_path.exists():
            cover_path = None  # path nel frontmatter ma file mancante

    # Se cover assente, prova a generare quella tipografica al volo (non con
    # --solo-testi-alternativi, che non deve creare altro che il file dei testi)
    if cover_path is None:
        if not crea_cover:
            return None
        cover_path = crea_cover_tipografica(path)
        if cover_path is None or not cover_path.exists():
            return None

    # Foto inline dal corpo (per il carosello Instagram), con alt e didascalia
    # (per i testi alternativi). Se la stessa foto compare due volte, vale la
    # prima, come nel carosello.
    foto_info_lista = estrai_foto_inline_info(body)
    foto_inline = [f["path"] for f in foto_info_lista]
    foto_info = {}
    for f in foto_info_lista:
        foto_info.setdefault(str(f["path"].resolve()),
                             {"alt": f["alt"], "caption": f["caption"]})

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
        "foto_info": foto_info,
    }


def trova_articoli_pubblicati() -> list[Path]:
    risultati = []
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
        if not social_comune.is_online(fm):
            continue
        risultati.append(p)
    return risultati


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("articolo", nargs="?", help="Path .md singolo")
    parser.add_argument("--all", action="store_true", help="Tutti pubblicati")
    parser.add_argument("--force", action="store_true", help="Sovrascrivi esistenti")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Cartella base alternativa al posto di social-bozze/ (prove)")
    parser.add_argument("--solo-testi-alternativi", action="store_true",
                        help="Scrive solo testi-alternativi.json per immagini già fatte, "
                             "senza toccarle; con --all, solo per gli articoli ancora "
                             "nella finestra di pubblicazione (72 ore)")
    args = parser.parse_args()
    if args.out_dir:
        global BOZZE_DIR
        BOZZE_DIR = args.out_dir

    if args.solo_testi_alternativi:
        return main_solo_testi_alternativi(args)

    if args.articolo:
        articoli = [Path(args.articolo)]
    elif args.all:
        articoli = trova_articoli_pubblicati()
    else:
        print("Specifica un articolo o --all", file=sys.stderr)
        return 2

    ok = 0
    saltati = 0
    falliti = 0
    for path in articoli:
        art = estrai_articolo(path)
        if not art:
            print(f"  SKIP (non pubblicato o senza cover): {path.name}", file=sys.stderr)
            saltati += 1
            continue

        out_dir = slug_dir(art["slug"])
        story_path = out_dir / "storia.jpg"

        # Immagini tolte dalla pulizia periodica (scripts/pulisci-social-bozze.py):
        # senza --force non si rigenerano, neppure con --all, altrimenti un
        # lancio manuale annullerebbe la pulizia. Con --force si rigenerano e
        # il marcatore si toglie (solo a generazione riuscita).
        marcatore = out_dir / ".immagini-rimosse"
        if marcatore.exists() and not args.force:
            print(f"  IMMAGINI RIMOSSE dalla pulizia (--force per rigenerarle): {art['slug']}",
                  file=sys.stderr)
            saltati += 1
            continue

        primo = out_dir / "feed-carosello-1.jpg"
        if (not args.force and story_path.exists()
                and (primo.exists() or (out_dir / "feed-post.jpg").exists())):
            print(f"  GIÀ PRESENTE (--force per ri-generare): {art['slug']}",
                  file=sys.stderr)
            saltati += 1
            continue

        try:
            slides = piano_carosello(art)
            genera_immagini(art, slides, out_dir)
            if marcatore.exists():
                marcatore.unlink()
            scrivi_readme(out_dir, art, len(slides))
            n_sintesi = sum(1 for k, _ in slides if k == "punti")
            extra = []
            if art.get("citazione"):
                extra.append("citazione")
            if n_sintesi:
                extra.append("punti" if n_sintesi == 1 else f"punti su {n_sintesi} slide")
            tipo = f"carosello x{len(slides)}"
            if extra:
                tipo += " +" + "/".join(extra)
            print(f"  ✓ {art['slug']} ({tipo})", file=sys.stderr)
            ok += 1
        except TestoIncompleto as e:
            falliti += 1
            # Le immagini che c'erano non corrispondono al testo di adesso: sono
            # di una versione precedente o, se le ha fatte il generatore di prima
            # del 13/10/2026, tagliate. Lasciarle significherebbe farle uscire: il
            # repository social pubblica qualunque articolo abbia il feed e una
            # didascalia, anche col giro orario e senza essere svegliato. Si
            # tolgono, e l'articolo resta senza post finché il testo non entra.
            tolte = togli_immagini(out_dir)
            msg = "testo che non entrerebbe intero nella grafica: nessuna immagine nuova"
            if tolte:
                msg += f", tolte le {tolte} di prima perché non escano al posto delle nuove"
            msg += f": {e}"
            print(f"  ✗ {art['slug']}: {msg}", file=sys.stderr)
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::error file=content/comunicazioni/{art['slug']}.md::{msg}")
        except Exception as e:
            falliti += 1
            print(f"  ERRORE {art['slug']}: {e}", file=sys.stderr)

    print(f"\nFatto. OK={ok}, saltati={saltati}, falliti={falliti}", file=sys.stderr)
    return 1 if falliti else 0


def piano_carosello(art: dict) -> list[tuple]:
    """Piano del carosello, in ordine: titolo → citazione → sintesi (una o più
    slide) → foto → affiliazioni. Citazione e sintesi solo se presenti nel
    frontmatter (social_citazione / social_punti). Affiliazioni: slide finale
    fissa con Quality Label ESC (codice E10435833 obbligatorio, Reg. UE
    2021/888) + SNPC Volontariato. Limite Instagram di 10 slide: se serve si
    tolgono foto in coda (restano nell'articolo), MAI slide di testo; se le
    slide di testo da sole superano il limite, TestoIncompleto."""
    testo = [("titolo", None)]
    if art.get("citazione"):
        testo.append(("citazione", art["citazione"]))
    sintesi = impagina_punti(art.get("punti") or [])
    if sintesi:
        totale = len(sintesi["pagine"])
        for numero, pagina in enumerate(sintesi["pagine"], 1):
            testo.append(("punti", (pagina, sintesi["corpo"], numero, totale)))
    posti_foto = MAX_SLIDE_CAROSELLO - 1 - len(testo)
    if posti_foto < 0:
        raise TestoIncompleto(
            f"le slide di testo ({len(testo)}) più quella delle affiliazioni superano "
            f"il limite di {MAX_SLIDE_CAROSELLO} slide di Instagram: accorciare social_punti")
    foto = [("foto", f) for f in art["carousel"][1:]][:posti_foto]
    return testo + foto + [("affiliazioni", None)]


def genera_immagini(art: dict, slides: list[tuple], out_dir: Path) -> None:
    """Disegna carosello e storia in una cartella provvisoria e, SOLO se tutto
    è riuscito, sostituisce le immagini precedenti. Un errore a metà non lascia
    mai un carosello incompleto né mescola immagini nuove e vecchie; se l'errore
    è un testo che non entra (TestoIncompleto), main() toglie anche le vecchie."""
    provvisoria = Path(tempfile.mkdtemp(prefix="immagini-social-"))
    try:
        for idx, (kind, data) in enumerate(slides, 1):
            dest = provvisoria / nome_feed(idx, len(slides))
            if kind == "titolo":
                crea_slide_titolo(art["title"], art["badge"], dest)
            elif kind == "citazione":
                crea_slide_citazione(data, dest)
            elif kind == "punti":
                pagina, corpo, numero, totale = data
                crea_slide_punti(pagina, dest, corpo, numero, totale)
            elif kind == "affiliazioni":
                crea_slide_affiliazioni(dest)
            else:
                crea_slide_foto(data, dest)

        # Storia: foto reale (1ª inline) in evidenza se c'è, altrimenti titolo
        hero = art["carousel"][1] if len(art["carousel"]) > 1 else None
        crea_story_verticale(art["cover"], art["title"], art["description"],
                             provvisoria / "storia.jpg", art["badge"], hero)

        # Testi alternativi delle immagini appena disegnate, dallo stesso piano.
        # Se non si riescono a comporre, le immagini escono lo stesso.
        scrivi_testi_alternativi(provvisoria, art, slides)

        # Tutto riuscito: via le immagini precedenti, dentro le nuove.
        out_dir.mkdir(parents=True, exist_ok=True)
        togli_immagini(out_dir)
        for nuova in sorted(provvisoria.iterdir()):
            shutil.move(str(nuova), str(out_dir / nuova.name))
    finally:
        shutil.rmtree(provvisoria, ignore_errors=True)


# ---------------------------------------------------------------------------
# --solo-testi-alternativi: il file dei testi per materiale già fatto
# ---------------------------------------------------------------------------
# Il materiale generato prima del 21/10/2026 non ha testi-alternativi.json. Per
# gli articoli ancora nella finestra di pubblicazione lo si aggiunge senza
# toccare le immagini. Ma un testo alternativo deve descrivere l'immagine che
# c'è davvero, e il frontmatter può essere cambiato dopo (un titolo corretto,
# una sintesi aggiunta): per questo le immagini si ridisegnano in una cartella
# provvisoria e il file si scrive solo se coincidono con quelle presenti. Se
# non coincidono, non si scrive nulla e lo si dice: vanno rigenerate (--force).

# Due JPEG «coincidono» se sono uguali byte per byte oppure se differiscono solo
# per la codifica (un'altra versione di Pillow o di libjpeg): al più lo 0,05%
# dei pixel con uno scarto oltre 48 su 255 in un canale. Una parola cambiata in
# un titolo cambia migliaia di pixel ben oltre quella soglia.
SOGLIA_SCARTO = 48
QUOTA_PIXEL_DIVERSI = 0.0005


def stesse_immagini(a: Path, b: Path) -> bool:
    if a.read_bytes() == b.read_bytes():
        return True
    with Image.open(a) as ia, Image.open(b) as ib:
        if ia.size != ib.size:
            return False
        diff = ImageChops.difference(ia.convert("RGB"), ib.convert("RGB"))
    r, g, b_ = diff.split()
    massimo = ImageChops.lighter(ImageChops.lighter(r, g), b_)
    istogramma = massimo.histogram()
    diversi = sum(istogramma[SOGLIA_SCARTO + 1:])
    return diversi <= QUOTA_PIXEL_DIVERSI * massimo.width * massimo.height


def aggiungi_testi_alternativi(path: Path, forza: bool = False) -> tuple[bool, str]:
    """Scrive testi-alternativi.json (e aggiorna il README) per le immagini già
    presenti di un articolo, senza toccarle. Ritorna (scritto, motivo)."""
    art = estrai_articolo(path, crea_cover=False)
    if not art:
        return False, "non online, versione facile o senza cover"
    out_dir = BOZZE_DIR / slug_to_path(art["slug"])
    if not out_dir.is_dir():
        return False, "nessun materiale"
    if (out_dir / social_comune.MARCATORE_PULITO).exists():
        return False, "immagini tolte dalla pulizia periodica"
    if (out_dir / TESTI_ALTERNATIVI).exists() and not forza:
        return False, "già presente"
    try:
        slides = piano_carosello(art)
    except TestoIncompleto as e:
        return False, f"il testo di adesso non entra nella grafica: {e}"
    attese = [nome_feed(i, len(slides)) for i in range(1, len(slides) + 1)] + ["storia.jpg"]
    presenti = sorted({p.name for p in out_dir.glob("feed-*.jpg")}
                      | {p.name for p in out_dir.glob("storia.jpg")})
    if sorted(attese) != presenti:
        return False, (f"le immagini presenti ({', '.join(presenti) or 'nessuna'}) non sono "
                       f"quelle del testo di adesso ({len(slides)} nel feed più la storia): "
                       f"rigenerarle con --force")
    with tempfile.TemporaryDirectory(prefix="testi-alternativi-") as tmp:
        prova = Path(tmp)
        try:
            genera_immagini(art, slides, prova)
        except TestoIncompleto as e:
            return False, f"il testo di adesso non entra nella grafica: {e}"
        diverse = [n for n in attese if not stesse_immagini(prova / n, out_dir / n)]
        if diverse:
            return False, (f"{', '.join(diverse)} non corrisponde al testo di adesso "
                           f"(articolo cambiato dopo le immagini): rigenerarle con --force")
        nuovo = prova / TESTI_ALTERNATIVI
        if not nuovo.is_file():
            return False, "testi alternativi non composti (vedi sopra)"
        shutil.copyfile(nuovo, out_dir / TESTI_ALTERNATIVI)
    scrivi_readme(out_dir, art, len(slides))
    return True, "scritto"


def main_solo_testi_alternativi(args) -> int:
    """Con un articolo: solo quello. Con --all: gli articoli andati online
    nella finestra di pubblicazione (social_comune.FINESTRA_RECUPERO_ORE), gli
    unici che il repository social può ancora pubblicare."""
    if args.articolo:
        articoli = [Path(args.articolo)]
    elif args.all:
        articoli = [p for p, _fm, _d in
                    social_comune.articoli(social_comune.FINESTRA_RECUPERO_ORE)]
    else:
        print("Specifica un articolo o --all", file=sys.stderr)
        return 2
    scritti = saltati = 0
    for path in articoli:
        try:
            scritto, motivo = aggiungi_testi_alternativi(path, args.force)
        except Exception as e:  # noqa: BLE001 — un articolo non ferma gli altri
            scritto, motivo = False, f"errore: {e}"
        if scritto:
            scritti += 1
            print(f"  ✓ {path.stem}: testi alternativi scritti", file=sys.stderr)
        else:
            saltati += 1
            print(f"  - {path.stem}: {motivo}", file=sys.stderr)
            if os.environ.get("GITHUB_ACTIONS") and "rigenerarle" in motivo:
                print(f"::warning::{path.stem}: testi alternativi non aggiunti, {motivo}")
    print(f"\nFatto. Testi alternativi scritti={scritti}, saltati={saltati}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
