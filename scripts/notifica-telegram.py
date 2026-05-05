#!/usr/bin/env python3
"""
Manda notifica al canale Telegram quando cambia lo stato di allerta o emergenza.

Triggerato dal workflow .github/workflows/notifica-telegram.yml a ogni push
che modifica data/allerta.json o data/emergenza.json.

Logica:

- ALLERTA: notifica solo se cambia il `livello` (verde/gialla/arancione/rossa).
  Mai per cambi solo del campo `ultimo_controllo` (sennò il workflow check-allerta
  che controlla ogni 6h spammerebbe il canale).

- EMERGENZA: notifica se cambia `attiva` (false→true = ATTIVAZIONE,
  true→false = CESSATA) oppure se mentre è attiva cambia `descrizione`
  o `tipo` (= AGGIORNAMENTO).

Configurazione: legge BOT_TOKEN e CHAT_ID dalle env var TELEGRAM_BOT_TOKEN
e TELEGRAM_CHAT_ID. Se mancano, exit pulito senza inviare (non blocca CI).

Per il diff usa `git show HEAD~1:<path>`. Se HEAD~1 non esiste (primo commit
sul branch), tratta lo stato come "sempre cambiato" e notifica solo se
livello != verde / emergenza attiva (per evitare notifica iniziale "tutto OK").
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

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


def leggi_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def leggi_json_precedente(rel_path: str) -> dict | None:
    """Legge la versione precedente di un file via git show HEAD~1:<path>.
    Ritorna None se HEAD~1 non esiste o il file non era presente."""
    try:
        out = subprocess.run(
            ["git", "show", f"HEAD~1:{rel_path}"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=10,
        )
        if out.returncode != 0:
            return None
        return json.loads(out.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError):
        return None


def manda_telegram(token: str, chat_id: str, testo: str) -> tuple[bool, str]:
    """Invia messaggio HTML al canale. Ritorna (ok, descrizione_errore)."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": testo,
        "parse_mode": "HTML",
        "disable_web_page_preview": "false",
    }
    data = urlencode(payload).encode("utf-8")
    req = Request(url, data=data, method="POST")
    try:
        with urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            if resp.status == 200:
                return (True, body)
            return (False, f"HTTP {resp.status}: {body[:200]}")
    except HTTPError as e:
        return (False, f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}")
    except URLError as e:
        return (False, f"URL error: {e}")


def msg_allerta_cambiata(prev: dict, curr: dict) -> str:
    livello = (curr.get("livello") or "").lower()
    emoji = EMOJI_LIVELLO.get(livello, "ℹ️")
    titolo = curr.get("titolo", "Allerta meteo aggiornata")
    descrizione = curr.get("descrizione", "")

    livello_prev = (prev.get("livello") or "").lower() if prev else None

    # Costruisci header in base alla transizione
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
    parti = [
        "🚨 <b>EMERGENZA IN CORSO</b>",
        "",
        f"<b>{titolo}</b>",
    ]
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
    parti = [
        "📢 <b>AGGIORNAMENTO EMERGENZA</b>",
        "",
        f"<b>{titolo}</b>",
    ]
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


def determina_messaggio() -> str | None:
    """Decide se inviare e cosa. Ritorna testo da inviare, None per skip."""
    allerta_curr = leggi_json(ALLERTA_PATH)
    allerta_prev = leggi_json_precedente("data/allerta.json")
    emergenza_curr = leggi_json(EMERGENZA_PATH)
    emergenza_prev = leggi_json_precedente("data/emergenza.json")

    # Priorità 1: cambiamento di emergenza (più grave)
    if emergenza_curr or emergenza_prev:
        attiva_curr = bool(emergenza_curr.get("attiva"))
        attiva_prev = bool((emergenza_prev or {}).get("attiva"))

        if attiva_curr and not attiva_prev:
            return msg_emergenza_attivata(emergenza_curr)
        if not attiva_curr and attiva_prev:
            return msg_emergenza_cessata(emergenza_prev or {})
        if attiva_curr and attiva_prev:
            cambi = ["titolo", "descrizione", "tipo", "link"]
            if any((emergenza_curr.get(k) or "") != ((emergenza_prev or {}).get(k) or "") for k in cambi):
                return msg_emergenza_aggiornata(emergenza_curr)

    # Priorità 2: cambiamento di livello allerta
    if allerta_curr:
        livello_curr = (allerta_curr.get("livello") or "").lower()
        livello_prev = (allerta_prev or {}).get("livello", "").lower() if allerta_prev else None

        if allerta_prev is None:
            # Primo commit sul branch — notifica solo se siamo in stato non-verde
            # (per evitare notifica spamming all'inizializzazione del sistema)
            if livello_curr and livello_curr != "verde":
                return msg_allerta_cambiata(None, allerta_curr)
            return None

        if livello_curr != livello_prev:
            return msg_allerta_cambiata(allerta_prev, allerta_curr)

    return None


def main() -> int:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        print("⚠ TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID non configurati. Skip notifica.")
        print("  Per attivare le notifiche: vedi scripts/README-telegram.md")
        return 0

    testo = determina_messaggio()
    if testo is None:
        print("Nessun cambiamento significativo da notificare.")
        return 0

    print("Messaggio da inviare:")
    print("-" * 60)
    print(testo)
    print("-" * 60)

    ok, descr = manda_telegram(token, chat_id, testo)
    if ok:
        print("✓ Messaggio inviato al canale Telegram.")
        return 0
    else:
        print(f"✗ Invio fallito: {descr}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
