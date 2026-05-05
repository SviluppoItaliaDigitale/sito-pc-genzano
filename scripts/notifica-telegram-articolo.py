#!/usr/bin/env python3
"""
Notifica Telegram al canale per nuovi articoli urgenti.

Si triggera dal workflow notifica-telegram-articolo.yml su push che
aggiunge file in content/comunicazioni/.

Filtra per badge:
  - Allerta, Emergenza  → notifica + pin (messaggio critico fissato in cima)
  - Avviso, Aggiornamento → notifica senza pin
  - Tutti gli altri badge → no notifica (Comunicazione, Formazione, Volontariato,
    Evento, Attività, Prevenzione, Esercitazione, Informazione, Radiocomunicazioni)

Filtro su data: articoli con `date` futura (calendarizzati) NON vengono
notificati al momento del commit. La notifica è progettata per articoli
"immediato" (data passata o oggi). Per i calendarizzati la notifica al
momento del go-live richiederebbe un trigger giornaliero — non implementato
nella versione corrente.

Filtro su draft: articoli `draft: true` skippati (anche se la regola del
progetto è "niente articoli in revisione", filtro per sicurezza).

Cover: se l'articolo ha il campo `image` nel frontmatter e il file è
accessibile pubblicamente, usa sendPhoto (foto + caption) invece di
sendMessage testuale. Aspetta 3 minuti prima di provare per dare tempo
al deploy di completare. Se sendPhoto fallisce (404 o altro), fallback
graceful a sendMessage testuale.
"""

import re
import subprocess
import sys
import time
from datetime import datetime, date, timezone
from pathlib import Path

import yaml  # PyYAML — installato dal workflow

sys.path.insert(0, str(Path(__file__).resolve().parent))
from telegram_lib import (  # noqa: E402
    get_credentials, send_message, send_photo,
    pin_message, unpin_all, trunc_caption,
)

ROOT = Path(__file__).resolve().parent.parent
SITO_URL = "https://www.protezionecivilegenzano.it"

BADGE_CRITICI = {"Allerta", "Emergenza"}                # notifica + pin
BADGE_INFO = {"Avviso", "Aggiornamento"}                # notifica senza pin
BADGE_NOTIFICA = BADGE_CRITICI | BADGE_INFO

EMOJI_BADGE = {
    "Allerta": "🟡",
    "Avviso": "🟠",
    "Emergenza": "🚨",
    "Aggiornamento": "📢",
}

DEPLOY_WAIT_SECS = 180  # tempo di attesa per immagini di copertina disponibili


def trova_articoli_aggiunti() -> list[Path]:
    """Articoli .md effettivamente aggiunti (Added) nel commit corrente.

    Esclude modifiche/rinomine: notifichiamo solo i NUOVI articoli, non
    le revisioni di articoli esistenti (per evitare spam su correzione
    di refusi)."""
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=A", "HEAD~1", "HEAD",
             "--", "content/comunicazioni/"],
            capture_output=True, text=True, check=True, cwd=ROOT, timeout=15,
        )
    except subprocess.SubprocessError:
        return []
    risultato = []
    for line in out.stdout.splitlines():
        line = line.strip()
        if not line or not line.endswith(".md"):
            continue
        p = ROOT / line
        if p.exists() and p.name != "_index.md":
            risultato.append(p)
    return risultato


def parse_frontmatter(text: str) -> dict | None:
    """Estrae il frontmatter YAML in cima al file Markdown."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None


def data_articolo_passata(date_field) -> bool:
    """Verifica che la `date` del frontmatter sia passata (= articolo già live)."""
    if date_field is None:
        return False
    if isinstance(date_field, datetime):
        return date_field.date() <= date.today()
    if isinstance(date_field, date):
        return date_field <= date.today()
    if isinstance(date_field, str):
        s = date_field.strip()
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
            return d.date() <= date.today()
        except ValueError:
            try:
                return datetime.strptime(s[:10], "%Y-%m-%d").date() <= date.today()
            except ValueError:
                return False
    return False


def slug_da_path(p: Path) -> str:
    return p.stem


def url_immagine(art: dict) -> str | None:
    img = art.get("image", "")
    if not img or not isinstance(img, str):
        return None
    if img.startswith("http"):
        return img
    if not img.startswith("/"):
        img = "/" + img
    return f"{SITO_URL}{img}"


def costruisci_messaggio(art: dict, slug: str) -> str:
    badge = art.get("badge", "Comunicazione")
    titolo = art.get("title", "Comunicazione")
    descrizione = art.get("description", "") or ""
    emoji = EMOJI_BADGE.get(badge, "ℹ️")

    parti = [
        f"{emoji} <b>{badge.upper()}</b>",
        "",
        f"<b>{titolo}</b>",
    ]
    if descrizione:
        parti.extend(["", descrizione])
    parti.extend([
        "",
        f"🔗 Leggi sul sito: {SITO_URL}/comunicazioni/{slug}/",
        f"📞 In emergenza chiama <b>112</b>",
        "",
        "<i>Gruppo Comunale Volontari PC Genzano</i>",
    ])
    return "\n".join(parti)


def filtra_da_notificare(paths: list[Path]) -> list[tuple[Path, dict]]:
    """Ritorna lista di (path, frontmatter_dict) per articoli che soddisfano:
    - frontmatter parsabile
    - draft != true
    - badge in BADGE_NOTIFICA
    - data passata o oggi (non futura)
    """
    risultato = []
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            print(f"  Skip {p.name}: errore lettura")
            continue
        fm = parse_frontmatter(text)
        if fm is None:
            print(f"  Skip {p.name}: frontmatter non parsabile")
            continue
        if fm.get("draft", False):
            print(f"  Skip {p.name}: draft=true")
            continue
        badge = fm.get("badge", "")
        if badge not in BADGE_NOTIFICA:
            print(f"  Skip {p.name}: badge='{badge}' non in lista notifiche")
            continue
        if not data_articolo_passata(fm.get("date")):
            print(f"  Skip {p.name}: data futura {fm.get('date')!r} (calendarizzato, niente notifica ora)")
            continue
        risultato.append((p, fm))
    return risultato


def notifica_articolo(token: str, chat_id: str, path: Path, fm: dict) -> bool:
    """Notifica singolo articolo. Ritorna True se inviato (testo o foto)."""
    slug = slug_da_path(path)
    badge = fm.get("badge", "")
    msg = costruisci_messaggio(fm, slug)
    img = url_immagine(fm)
    e_critico = badge in BADGE_CRITICI

    print(f"\n→ Notifico {slug} (badge={badge}, image={'sì' if img else 'no'}, pin={'sì' if e_critico else 'no'})")

    sent_id = None

    # Tentativo 1: con foto, se disponibile
    if img:
        ok, result, err = send_photo(token, chat_id, img, trunc_caption(msg))
        if ok:
            sent_id = result.get("message_id") if result else None
            print(f"  ✓ Foto + caption inviata (msg_id={sent_id})")
        else:
            print(f"  ⚠ sendPhoto fallito: {err}. Fallback a testo.")

    # Tentativo 2 (o fallback): solo testo
    if sent_id is None:
        ok, result, err = send_message(token, chat_id, msg)
        if not ok:
            print(f"  ✗ sendMessage fallito: {err}", file=sys.stderr)
            return False
        sent_id = result.get("message_id") if result else None
        print(f"  ✓ Messaggio testo inviato (msg_id={sent_id})")

    # Pin per badge critici
    if e_critico and sent_id:
        ok, _, err = unpin_all(token, chat_id)
        if not ok:
            print(f"  (unpin: {err}) — proseguo col pin")
        ok, _, err = pin_message(token, chat_id, sent_id)
        if ok:
            print("  ✓ Messaggio fissato in cima al canale.")
        else:
            print(f"  ⚠ Pin fallito: {err}")

    return True


def main() -> int:
    token, chat_id = get_credentials()
    if not token or not chat_id:
        print("⚠ TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID non configurati. Skip notifica.")
        return 0

    aggiunti = trova_articoli_aggiunti()
    if not aggiunti:
        print("Nessun articolo aggiunto nel commit corrente.")
        return 0

    print(f"Articoli aggiunti nel commit: {len(aggiunti)}")
    for p in aggiunti:
        print(f"  - {p.relative_to(ROOT)}")

    da_notificare = filtra_da_notificare(aggiunti)
    if not da_notificare:
        print("\nNessun articolo da notificare dopo il filtro (badge/data/draft).")
        return 0

    # Attesa per il deploy: serve solo se almeno un articolo ha image
    serve_attesa = any(url_immagine(fm) for _, fm in da_notificare)
    if serve_attesa:
        print(f"\nAspetto {DEPLOY_WAIT_SECS}s per dare tempo al deploy del sito (immagini di copertina)...")
        time.sleep(DEPLOY_WAIT_SECS)
    else:
        print("\nNessuna immagine di copertina presente: niente attesa, vado subito.")

    fail = 0
    for p, fm in da_notificare:
        try:
            ok = notifica_articolo(token, chat_id, p, fm)
            if not ok:
                fail += 1
        except Exception as e:
            print(f"  ✗ Errore su {p.name}: {e}", file=sys.stderr)
            fail += 1

    print(f"\nCompletato. Notificati: {len(da_notificare) - fail}/{len(da_notificare)}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
