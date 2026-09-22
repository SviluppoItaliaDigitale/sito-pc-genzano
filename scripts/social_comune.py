#!/usr/bin/env python3
"""Regole comuni della catena social del sito.

Tre domande a cui rispondono tutti gli script dei social, e che devono
ricevere la stessa risposta ovunque:

  1. da quando un articolo è ONLINE sul sito;
  2. se il suo materiale social (testi + immagini) è COMPLETO;
  3. se è un CANDIDATO alla pubblicazione automatica su Instagram e Facebook.

Usata da genera-social.py, genera-immagini-social.py e social-pronti.py.

Perché esiste (22/09/2026): fino a quel giorno ogni generatore aveva il suo
controllo della data, basato su `datetime.date.today()` del runner (UTC) e
applicato solo al momento del commit. Un articolo calendarizzato, scritto con
data futura, veniva saltato al commit e poi nessuno lo riprendeva quando la
data arrivava: niente materiale, quindi niente post. Erano 108 gli articoli
già in calendario destinati a non uscire mai sui social.

Le regole del punto 3 sono lo specchio di quelle che il repository privato
social-pc-genzano applica dal suo lato (scripts/social_coda_lib.py:
BADGE_ESCLUSI_AUTO, candidato_auto, verifica_materiale): se cambiano là,
vanno cambiate qui.

Solo libreria standard.
"""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
CONTENT_COMUNICAZIONI = ROOT / "content" / "comunicazioni"
SOCIAL_BOZZE = ROOT / "social-bozze"
SITO_BASE = "https://www.protezionecivilegenzano.it"

# Lo stesso fuso di hugo.toml (timeZone = "Europe/Rome"): una data senza ora
# nel frontmatter vale dalla mezzanotte italiana, non da quella di Greenwich.
TZ = ZoneInfo("Europe/Rome")

# Specchio di social_coda_lib.BADGE_ESCLUSI_AUTO: comunicazioni di rischio che
# valgono nel momento in cui escono, e si pubblicano a mano.
BADGE_ESCLUSI_AUTO = frozenset({"Allerta", "Emergenza"})

# Specchio di `accoda-nuovi --max-eta-giorni 3`: oltre questa età il
# repository privato non accoda più un articolo (non ripesca l'archivio).
FINESTRA_RECUPERO_ORE = 72

TESTI = ("x", "facebook", "instagram", "telegram")


# ──────────────────────────────────────────────────────────────
# Tempo
# ──────────────────────────────────────────────────────────────

def adesso() -> dt.datetime:
    return dt.datetime.now(TZ)


def data_online(valore) -> dt.datetime | None:
    """Istante da cui Hugo pubblica l'articolo.

    - ``2026-09-22``                  → mezzanotte italiana di quel giorno
    - ``2026-09-22T00:02:00+02:00``   → esattamente quell'istante
    - ``2026-09-22T18:00:00`` (senza fuso) → ora italiana
    """
    s = str(valore or "").strip().strip('"').strip("'")
    if not s:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        try:
            return dt.datetime.combine(dt.date.fromisoformat(s), dt.time(0, 0), TZ)
        except ValueError:
            return None
    try:
        d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
        if not m:
            return None
        try:
            return dt.datetime.combine(dt.date.fromisoformat(m.group(1)), dt.time(0, 0), TZ)
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=TZ)
    return d.astimezone(TZ)


def fmt(d: dt.datetime | None) -> str:
    return d.astimezone(TZ).strftime("%d/%m/%Y %H:%M") if d else "?"


# ──────────────────────────────────────────────────────────────
# Articoli
# ──────────────────────────────────────────────────────────────

def parse_frontmatter(testo: str) -> tuple[dict, str]:
    """Frontmatter YAML minimale, senza dipendenze: coppie `chiave: valore`
    (virgolette tolte) e liste semplici `- voce` sotto una chiave vuota."""
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

    fm: dict = {}
    chiave_lista = None
    for riga in raw_fm.split("\n"):
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        m_item = re.match(r"^\s+-\s+(.+)$", riga)
        if chiave_lista is not None and m_item:
            fm[chiave_lista].append(_strip_q(m_item.group(1)))
            continue
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", riga)
        if m:
            chiave, valore = m.group(1), m.group(2).strip()
            if valore == "":
                fm[chiave] = []
                chiave_lista = chiave
            else:
                fm[chiave] = _strip_q(valore)
                chiave_lista = None
    return fm, body


def leggi_frontmatter(path: Path) -> dict:
    try:
        return parse_frontmatter(path.read_text(encoding="utf-8"))[0]
    except OSError:
        return {}


def testo_campo(fm: dict, chiave: str) -> str:
    """Valore testuale di un campo (una chiave vuota diventa lista vuota nel
    parser: qui torna stringa vuota)."""
    v = fm.get(chiave, "")
    return v.strip() if isinstance(v, str) else ""


def is_bozza(fm: dict) -> bool:
    return testo_campo(fm, "draft").lower() in ("true", "yes", "1")


def is_facile(path: Path, fm: dict) -> bool:
    """Versione in italiano semplice (A2): nascosta da liste e feed, non va
    sui social (rule 04b § "Bozze social automatiche")."""
    return path.stem.endswith("-facile") or bool(testo_campo(fm, "versione_facile_di"))


def online_dal(fm: dict) -> dt.datetime | None:
    """Istante da cui l'articolo è online, o None se è una bozza o senza data."""
    if is_bozza(fm):
        return None
    return data_online(testo_campo(fm, "date"))


def is_online(fm: dict, ora: dt.datetime | None = None) -> bool:
    d = online_dal(fm)
    return d is not None and d <= (ora or adesso())


def articoli(finestra_ore: float | None = None,
             ora: dt.datetime | None = None) -> list[tuple[Path, dict, dt.datetime]]:
    """Articoli online (non bozze, non versioni facili), dal più recente.

    Con `finestra_ore` restano solo quelli andati online nelle ultime N ore.
    """
    ora = ora or adesso()
    limite = ora - dt.timedelta(hours=finestra_ore) if finestra_ore else None
    out = []
    for p in CONTENT_COMUNICAZIONI.glob("*.md"):
        if p.name == "_index.md":
            continue
        fm = leggi_frontmatter(p)
        if not fm or is_facile(p, fm):
            continue
        d = online_dal(fm)
        if d is None or d > ora:
            continue
        if limite and d < limite:
            continue
        out.append((p, fm, d))
    out.sort(key=lambda t: t[2], reverse=True)
    return out


# ──────────────────────────────────────────────────────────────
# Materiale social
# ──────────────────────────────────────────────────────────────

def slug_to_path(slug: str) -> Path:
    """Da 'AAAA-MM-GG-titolo' ricava AAAA/MM/AAAA-MM-GG-titolo."""
    parts = slug.split("-", 3)
    if (len(parts) >= 4
            and len(parts[0]) == 4 and parts[0].isdigit()
            and len(parts[1]) == 2 and parts[1].isdigit()
            and len(parts[2]) == 2 and parts[2].isdigit()):
        return Path(parts[0]) / parts[1] / slug
    return Path(slug)


def cartella_bozze(slug: str) -> Path:
    return SOCIAL_BOZZE / slug_to_path(slug)


def _non_vuoto(p: Path) -> bool:
    try:
        return p.is_file() and p.read_text(encoding="utf-8").strip() != ""
    except OSError:
        return False


def testi_completi(slug: str) -> bool:
    c = cartella_bozze(slug)
    return all(_non_vuoto(c / f"{t}.txt") for t in TESTI)


def immagini_complete(slug: str) -> bool:
    c = cartella_bozze(slug)
    feed = (c / "feed-post.jpg").is_file() or (c / "feed-carosello-1.jpg").is_file()
    return feed and (c / "storia.jpg").is_file()


def materiale_completo(slug: str) -> bool:
    """Tutto ciò che i generatori producono: 4 testi, feed e storia."""
    return testi_completi(slug) and immagini_complete(slug)


def materiale_pubblicabile(slug: str) -> bool:
    """Il minimo che il repository privato esige per pubblicare
    (social_coda_lib.verifica_materiale): immagini del feed e almeno una
    didascalia fra Instagram e Facebook."""
    c = cartella_bozze(slug)
    feed = (c / "feed-post.jpg").is_file() or any(c.glob("feed-carosello-*.jpg"))
    testo = _non_vuoto(c / "instagram.txt") or _non_vuoto(c / "facebook.txt")
    return feed and testo


def candidato_auto(path: Path, fm: dict) -> bool:
    """L'articolo va sui social in automatico? (materiale a parte)"""
    return (not is_facile(path, fm) and not is_bozza(fm)
            and testo_campo(fm, "badge") not in BADGE_ESCLUSI_AUTO)


def url_articolo(slug: str) -> str:
    return f"{SITO_BASE}/comunicazioni/{slug}/"
