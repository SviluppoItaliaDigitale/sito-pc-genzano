#!/usr/bin/env python3
"""
Manda notifica al canale Telegram quando cambia lo stato di allerta o emergenza.

Triggerato dal workflow .github/workflows/notifica-telegram.yml a ogni push
che modifica data/allerta.json o data/emergenza.json.

Logica:

- ALLERTA: notifica solo se cambia il `livello` (verde/gialla/arancione/rossa).
  Mai per cambi solo del campo `ultimo_controllo` (sennò il workflow
  check-allerta che gira ogni 6h spammerebbe il canale).
  Pin del messaggio per livelli arancione/rossa. Unpin per cessazione (verde).

- EMERGENZA: notifica per attivazione (false→true), cessazione (true→false)
  o aggiornamento sostanziale (titolo/descrizione/tipo/link cambiati mentre
  attiva). Pin del messaggio per attivazione e aggiornamento, unpin per
  cessazione.

Configurazione: legge BOT_TOKEN e CHAT_ID dalle env var TELEGRAM_BOT_TOKEN
e TELEGRAM_CHAT_ID. Se mancano, exit pulito senza inviare (non blocca CI).
"""

import json
import subprocess
import sys
from pathlib import Path

# Lib condivisa
sys.path.insert(0, str(Path(__file__).resolve().parent))
from telegram_lib import (  # noqa: E402
    get_credentials, send_message, pin_message, unpin_all,
)

ROOT = Path(__file__).resolve().parent.parent
ALLERTA_PATH = ROOT / "data" / "allerta.json"
EMERGENZA_PATH = ROOT / "data" / "emergenza.json"

SITO_URL = "https://www.protezionecivilegenzano.it"

EMOJI_LIVELLO = {
    "verde": "🟢",
    "gialla": "🟡",
    "giallo": "🟡",
    "arancione": "🟠",
    "rossa": "🔴",
    "rosso": "🔴",
}

# Categoria della notifica determina pin/unpin
CRITICAL = "critical"        # unpin all + send + pin
INFORMATIONAL = "info"        # send (no pin/unpin)
CESSATION = "cessation"       # unpin all + send (no pin)


def leggi_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def leggi_json_precedente(rel_path: str) -> dict | None:
    """Legge la versione precedente di un file via git show HEAD~1:<path>."""
    try:
        out = subprocess.run(
            ["git", "show", f"HEAD~1:{rel_path}"],
            capture_output=True, text=True, cwd=ROOT, timeout=10,
        )
        if out.returncode != 0:
            return None
        return json.loads(out.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError):
        return None


def msg_allerta_cambiata(prev: dict | None, curr: dict) -> str:
    livello = (curr.get("livello") or "").lower()
    emoji = EMOJI_LIVELLO.get(livello, "ℹ️")
    titolo = curr.get("titolo", "Allerta meteo aggiornata")
    descrizione = curr.get("descrizione", "")
    livello_prev = (prev.get("livello") or "").lower() if prev else None

    if livello == "verde":
        if livello_prev and livello_prev != "verde":
            header = f"{emoji} <b>CESSATA ALLERTA</b>"
            sotto = f"Si torna in stato verde dopo livello <b>{livello_prev}</b>."
        else:
            header = f"{emoji} <b>STATO VERDE</b>"
            sotto = "Nessuna allerta in corso."
    else:
        liv_label = livello.upper()
        header = f"{emoji} <b>ALLERTA {liv_label}</b>"
        if livello_prev and livello_prev != livello:
            sotto = f"Cambio di livello: <b>{livello_prev or 'verde'}</b> → <b>{livello}</b>."
        else:
            sotto = "Aggiornamento dello stato di allerta."

    parti = [header, "", f"<b>{titolo}</b>", sotto]
    if descrizione:
        parti.extend(["", descrizione])
    parti.extend([
        "",
        f"🔗 Dettagli: {SITO_URL}/allerte-meteo/",
        f"📞 In emergenza chiama <b>112</b>",
        "",
        "<i>Fonte: Centro Funzionale Regione Lazio · Gruppo Comunale Volontari PC Genzano</i>",
    ])
    return "\n".join(parti)


def msg_emergenza_attivata(curr: dict) -> str:
    titolo = curr.get("titolo") or "Emergenza in corso"
    descrizione = curr.get("descrizione") or ""
    link = curr.get("link") or ""
    parti = ["🚨 <b>EMERGENZA IN CORSO</b>", "", f"<b>{titolo}</b>"]
    if descrizione:
        parti.extend(["", descrizione])
    if link:
        parti.extend(["", f"🔗 Maggiori informazioni: {link}"])
    parti.extend([
        "",
        f"🌐 Pagina sito: {SITO_URL}/emergenza/",
        f"📞 In emergenza immediata chiama <b>112</b>",
        "",
        "<i>Gruppo Comunale Volontari PC Genzano di Roma</i>",
    ])
    return "\n".join(parti)


def msg_emergenza_aggiornata(curr: dict) -> str:
    titolo = curr.get("titolo") or "Emergenza in corso"
    descrizione = curr.get("descrizione") or ""
    link = curr.get("link") or ""
    parti = ["📢 <b>AGGIORNAMENTO EMERGENZA</b>", "", f"<b>{titolo}</b>"]
    if descrizione:
        parti.extend(["", descrizione])
    if link:
        parti.extend(["", f"🔗 Aggiornamento: {link}"])
    parti.extend([
        "",
        f"🌐 Pagina sito: {SITO_URL}/emergenza/",
        f"📞 In emergenza immediata chiama <b>112</b>",
        "",
        "<i>Gruppo Comunale Volontari PC Genzano di Roma</i>",
    ])
    return "\n".join(parti)


def msg_emergenza_cessata(prev: dict) -> str:
    titolo_prev = prev.get("titolo") or "Emergenza"
    parti = [
        "✅ <b>CESSATA EMERGENZA</b>",
        "",
        f"L'emergenza «<b>{titolo_prev}</b>» è cessata.",
        "Si torna alla normale operatività ordinaria.",
        "",
        f"🌐 Sito: {SITO_URL}/",
        f"📞 In emergenza chiama sempre <b>112</b>",
        "",
        "<i>Gruppo Comunale Volontari PC Genzano di Roma</i>",
    ]
    return "\n".join(parti)


def determina_notifica() -> tuple[str, str] | None:
    """Decide cosa inviare e con quale categoria.

    Ritorna (testo, categoria) dove categoria è uno di CRITICAL/INFORMATIONAL/CESSATION.
    Ritorna None se non c'è nulla da notificare.
    """
    allerta_curr = leggi_json(ALLERTA_PATH)
    allerta_prev = leggi_json_precedente("data/allerta.json")
    emergenza_curr = leggi_json(EMERGENZA_PATH)
    emergenza_prev = leggi_json_precedente("data/emergenza.json")

    # Priorità 1: emergenza
    if emergenza_curr or emergenza_prev:
        attiva_curr = bool(emergenza_curr.get("attiva"))
        attiva_prev = bool((emergenza_prev or {}).get("attiva"))

        if attiva_curr and not attiva_prev:
            return (msg_emergenza_attivata(emergenza_curr), CRITICAL)
        if not attiva_curr and attiva_prev:
            return (msg_emergenza_cessata(emergenza_prev or {}), CESSATION)
        if attiva_curr and attiva_prev:
            cambi = ["titolo", "descrizione", "tipo", "link"]
            if any((emergenza_curr.get(k) or "") != ((emergenza_prev or {}).get(k) or "") for k in cambi):
                return (msg_emergenza_aggiornata(emergenza_curr), CRITICAL)

    # Priorità 2: allerta
    if allerta_curr:
        livello_curr = (allerta_curr.get("livello") or "").lower()
        livello_prev = (allerta_prev or {}).get("livello", "").lower() if allerta_prev else None

        if allerta_prev is None:
            # Primo commit sul branch — notifica solo se non-verde
            if livello_curr and livello_curr != "verde":
                cat = CRITICAL if livello_curr in ("arancione", "rossa", "rosso") else INFORMATIONAL
                return (msg_allerta_cambiata(None, allerta_curr), cat)
            return None

        if livello_curr != livello_prev:
            if livello_curr == "verde":
                return (msg_allerta_cambiata(allerta_prev, allerta_curr), CESSATION)
            if livello_curr in ("arancione", "rossa", "rosso"):
                return (msg_allerta_cambiata(allerta_prev, allerta_curr), CRITICAL)
            # gialla
            return (msg_allerta_cambiata(allerta_prev, allerta_curr), INFORMATIONAL)

    return None


def main() -> int:
    token, chat_id = get_credentials()
    if not token or not chat_id:
        print("⚠ TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID non configurati. Skip notifica.")
        print("  Per attivare le notifiche: vedi scripts/README-telegram.md")
        return 0

    risultato = determina_notifica()
    if risultato is None:
        print("Nessun cambiamento significativo da notificare.")
        return 0

    testo, categoria = risultato
    print(f"Categoria: {categoria}")
    print("Messaggio da inviare:")
    print("-" * 60)
    print(testo)
    print("-" * 60)

    # Step 1: per categoria CESSATION o CRITICAL, unpin di pulizia prima
    if categoria in (CRITICAL, CESSATION):
        ok, _, err = unpin_all(token, chat_id)
        if ok:
            print("✓ Messaggi pinnati precedenti rimossi.")
        else:
            # Niente di pinnato è ok, non bloccare
            print(f"  (unpin: {err}) — proseguo")

    # Step 2: invia il messaggio
    ok, result, err = send_message(token, chat_id, testo)
    if not ok:
        print(f"✗ Invio fallito: {err}", file=sys.stderr)
        return 1
    msg_id = result.get("message_id") if result else None
    print(f"✓ Messaggio inviato al canale Telegram (msg_id={msg_id}).")

    # Step 3: pin per categoria CRITICAL
    if categoria == CRITICAL and msg_id:
        ok, _, err = pin_message(token, chat_id, msg_id)
        if ok:
            print("✓ Messaggio fissato in cima al canale.")
        else:
            print(f"⚠ Pin fallito: {err}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
