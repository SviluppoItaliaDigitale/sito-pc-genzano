"""Funzioni condivise per le notifiche Telegram.

Importato da notifica-telegram.py (allerta/emergenza) e
notifica-telegram-articolo.py (nuovi articoli urgenti).

Usa solo libreria standard (urllib + json) — nessuna dipendenza esterna.
Eccezione: PyYAML per parsing frontmatter, lo importa solo lo script
articolo se necessario.
"""

import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


API_BASE = "https://api.telegram.org/bot{token}/{method}"


def get_credentials() -> tuple[str | None, str | None]:
    """Legge token e chat_id dalle env var. Ritorna (None, None) se mancano."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return (None, None)
    return (token, chat_id)


def _api_call(token: str, method: str, params: dict) -> tuple[bool, dict | None, str]:
    """Chiamata generica API Telegram.

    Ritorna (ok, result_dict, errore). result_dict è None se non ok.
    """
    url = API_BASE.format(token=token, method=method)
    data = urlencode(params).encode("utf-8")
    req = Request(url, data=data, method="POST")
    try:
        with urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            j = json.loads(body)
            if j.get("ok"):
                return (True, j.get("result"), "")
            return (False, None, str(j.get("description", body))[:200])
    except HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8")).get("description", "")
        except Exception:
            err = f"HTTP {e.code}"
        return (False, None, err[:200])
    except URLError as e:
        return (False, None, f"URL error: {e}")
    except Exception as e:
        return (False, None, f"errore: {e}")


def send_message(token: str, chat_id: str, text: str) -> tuple[bool, dict | None, str]:
    """Invia messaggio HTML semplice. Limite 4096 caratteri."""
    return _api_call(token, "sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "false",
    })


def send_photo(token: str, chat_id: str, photo_url: str, caption: str) -> tuple[bool, dict | None, str]:
    """Invia foto con caption HTML. Caption limite 1024 caratteri.

    Telegram scarica la foto dall'URL pubblico (deve essere accessibile
    via internet, non solo da rete privata)."""
    return _api_call(token, "sendPhoto", {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML",
    })


def pin_message(token: str, chat_id: str, message_id: int) -> tuple[bool, dict | None, str]:
    """Fissa un messaggio in cima al canale. disable_notification=true
    per non fare doppia notifica (la prima è già arrivata col send)."""
    return _api_call(token, "pinChatMessage", {
        "chat_id": chat_id,
        "message_id": str(message_id),
        "disable_notification": "true",
    })


def unpin_all(token: str, chat_id: str) -> tuple[bool, dict | None, str]:
    """Rimuove tutti i messaggi pinnati. Usato prima di pinnare il nuovo
    o quando un'allerta/emergenza cessa."""
    return _api_call(token, "unpinAllChatMessages", {
        "chat_id": chat_id,
    })


def trunc_caption(text: str, max_len: int = 1024) -> str:
    """Tronca testo per caption Telegram preservando la chiusura.

    Se il testo è troncato, finisce con '…' e mantiene il link al sito
    se è entro i primi N-50 caratteri (l'utente può sempre cliccare
    l'anteprima del link che Telegram costruisce).
    """
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"
