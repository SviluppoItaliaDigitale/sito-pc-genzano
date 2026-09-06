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

# Struttura dei messaggi (rule 02 § "Comunicazione di crisi sui social",
# ISO 22329 + CWA CEN/CENELEC), in quest'ordine: (1) tipo di evento,
# (2) livello e colore, (3) area + finestra temporale, (4) cosa fare,
# (5) fonte ufficiale con link, (6) prossimo aggiornamento.
# Vincoli di accessibilità (rule 03): al massimo DUE emoji per messaggio
# (qui: colore del livello + telefono), niente maiuscole continue oltre il
# titolo, niente caratteri decorativi. Hashtag stabili del Gruppo.
# Esercitazione 06/09/2026: i messaggi precedenti mancavano dei punti 4 e 6
# e avevano 3-4 emoji.
HASHTAG_ALLERTA = "#PCGenzano #AllertaLazio #Genzano"
HASHTAG_EMERGENZA = "#PCGenzano #Genzano"
FONTE_CFR = ("Fonte: Centro Funzionale Regionale Lazio — "
             "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti")
PROSSIMO_AGG = ("Prossimo aggiornamento: su questo canale al cambio di livello; "
                f"stato verificato in continuo su {SITO_URL}/allerte-meteo/")

# Azioni di autoprotezione per livello: stesse frasi della pagina canonica
# /allerte-meteo/ (§ "Cosa fare" per colore) — se cambiano là, cambiano qui.
COSA_FARE = {
    "gialla": [
        "Segui i bollettini ufficiali.",
        "Evita zone soggette ad allagamento.",
        "Non sostare lungo corsi d'acqua, fossi o sottopassaggi.",
    ],
    "arancione": [
        "Limita gli spostamenti non necessari.",
        "Metti in sicurezza balconi, cantine e seminterrati, solo se puoi farlo senza pericolo.",
        "Tieni pronto il kit di emergenza e segui le indicazioni delle autorità.",
    ],
    "rossa": [
        "Non uscire se non è strettamente necessario.",
        "Allontanati da piani interrati e seminterrati; non attraversare strade allagate o sottopassaggi.",
        "Segui solo le indicazioni delle autorità e tieni il telefono carico.",
    ],
    "verde": [
        "Non sono richieste azioni specifiche.",
        "Resta informato attraverso i canali ufficiali.",
    ],
}

# Azioni per gli avvisi meteo avversi (blocco avviso_meteo), per tipo: stesse
# frasi delle pagine canoniche /rischi-prevenzione/{vento-forte,ondate-di-calore,
# temporali-intensi}/ § "Cosa fare DURANTE" e /allerte-meteo/. La chiave è
# cercata come sottostringa del campo `tipo` (es. "vento, neve").
COSA_FARE_AVVISO = {
    "vento": [
        "Rimani in casa se possibile, lontano da finestre e vetrate.",
        "Se sei all'aperto, allontanati da alberi, pali della luce, impalcature e cartelloni.",
        "In auto rallenta ed evita le strade alberate.",
    ],
    "neve": [
        "Limita gli spostamenti in auto; se devi guidare, usa pneumatici invernali o catene.",
        "Fai attenzione al ghiaccio su strade e marciapiedi.",
        "Tieni a portata di mano torcia, coperte e telefono carico.",
    ],
    "ghiaccio": [
        "Fai attenzione al ghiaccio su strade, marciapiedi e scale esterne.",
        "Limita gli spostamenti in auto nelle ore più fredde.",
    ],
    "calore": [
        "Bevi molta acqua anche se non senti sete; evita alcolici e bevande zuccherate.",
        "Non uscire nelle ore più calde (11:00-17:00).",
        "Controlla anziani, bambini e persone fragili; non lasciare mai persone o animali in auto al sole.",
    ],
    "temporali": [
        "Entra in un edificio solido o in auto con i finestrini chiusi.",
        "Allontanati da alberi isolati, pali metallici, tralicci e corsi d'acqua.",
        "Non attraversare sottopassaggi allagati.",
    ],
    "mareggiate": [
        "Non sostare su moli, scogliere, spiagge e lungomare.",
        "Non entrare in acqua e tieni lontane le imbarcazioni dalla riva.",
    ],
}

# Categoria della notifica determina pin/unpin
CRITICAL = "critical"        # unpin all + send + pin
INFORMATIONAL = "info"        # send (no pin/unpin)
CESSATION = "cessation"       # unpin all + send (no pin)


def _norm_livello(liv: str | None) -> str:
    liv = (liv or "").lower().strip()
    return {"giallo": "gialla", "rosso": "rossa"}.get(liv, liv)


def _blocco_cosa_fare(livello: str) -> list[str]:
    azioni = COSA_FARE.get(livello) or COSA_FARE["gialla"]
    return ["<b>Cosa fare</b>"] + [f"• {a}" for a in azioni]


def _blocco_cosa_fare_avviso(tipo: str, livello: str) -> list[str]:
    """Azioni per un avviso meteo avverso: unione delle liste dei tipi
    riconosciuti in `tipo` (max 4 voci); se nessun tipo è noto, ripiega
    sulle azioni del livello di allerta."""
    t = (tipo or "").lower()
    azioni: list[str] = []
    for chiave, lista in COSA_FARE_AVVISO.items():
        if chiave in t:
            for a in lista:
                if a not in azioni:
                    azioni.append(a)
    if not azioni:
        return _blocco_cosa_fare(livello or "gialla")
    return ["<b>Cosa fare</b>"] + [f"• {a}" for a in azioni[:4]]


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
    livello = _norm_livello(curr.get("livello"))
    emoji = EMOJI_LIVELLO.get(livello, "🟡")
    titolo = curr.get("titolo", "Allerta meteo aggiornata")
    descrizione = curr.get("descrizione", "")
    livello_prev = _norm_livello(prev.get("livello")) if prev else None

    if livello == "verde":
        if livello_prev and livello_prev != "verde":
            header = f"{emoji} <b>Cessata allerta meteo</b>"
            sotto = f"Si torna al livello verde dopo l'allerta {livello_prev}. Comune di Genzano di Roma."
        else:
            header = f"{emoji} <b>Allerta meteo: livello verde</b>"
            sotto = "Nessuna allerta in corso per il Comune di Genzano di Roma."
    else:
        header = f"{emoji} <b>Allerta meteo {livello}</b>"
        if livello_prev and livello_prev != livello:
            sotto = f"Allerta {livello} (in precedenza {livello_prev or 'verde'}). Comune di Genzano di Roma."
        else:
            sotto = f"Allerta {livello}. Comune di Genzano di Roma."

    parti = [header, "", f"<b>{titolo}</b>", sotto]
    if descrizione:
        parti.extend(["", descrizione])
    parti.append("")
    parti.extend(_blocco_cosa_fare(livello))
    parti.extend([
        "📞 In caso di pericolo chiama il <b>112</b>. Segnalazioni non urgenti: 803 555.",
        "",
        f"<i>{FONTE_CFR}</i>",
        f"<i>{PROSSIMO_AGG}</i>",
        "",
        HASHTAG_ALLERTA,
    ])
    return "\n".join(parti)


def msg_avviso_meteo(curr: dict | None) -> str:
    """Messaggio per il blocco avviso_meteo (vento, neve, calore, gelate...).
    curr=None o senza `tipo` => avviso rientrato."""
    if not curr or not (curr.get("tipo") or "").strip():
        return "\n".join([
            "🟢 <b>Avviso meteo rientrato</b>",
            "",
            "L'avviso per fenomeni meteo avversi non è più in vigore per il Comune di Genzano di Roma.",
            "",
            "📞 In caso di pericolo chiama il <b>112</b>.",
            "",
            f"<i>{FONTE_CFR}</i>",
            f"<i>{PROSSIMO_AGG}</i>",
            "",
            HASHTAG_ALLERTA,
        ])
    tipo = (curr.get("tipo") or "").strip()
    livello = _norm_livello(curr.get("livello"))
    emoji = EMOJI_LIVELLO.get(livello, "🟠")
    descrizione = (curr.get("descrizione") or "").strip()
    url = (curr.get("url") or "").strip()
    header = f"{emoji} <b>Avviso meteo: {tipo}</b>"
    sotto = (f"Allerta {livello}. Comune di Genzano di Roma." if livello
             else "Avviso per fenomeni meteo avversi. Comune di Genzano di Roma.")
    parti = [header, "", sotto]
    if descrizione:
        parti.extend(["", descrizione])
    parti.append("")
    parti.extend(_blocco_cosa_fare_avviso(tipo, livello))
    parti.append("📞 In caso di pericolo chiama il <b>112</b>. Segnalazioni non urgenti: 803 555.")
    parti.append("")
    if url:
        parti.append(f"<i>Fonte: avviso del Centro Funzionale Regionale Lazio — {url}</i>")
    else:
        parti.append(f"<i>{FONTE_CFR}</i>")
    parti.extend([f"<i>{PROSSIMO_AGG}</i>", "", HASHTAG_ALLERTA])
    return "\n".join(parti)


def _coda_emergenza(link: str, etichetta_link: str) -> list[str]:
    parti = []
    if link:
        parti.append(f"{etichetta_link}: {link}")
    parti.extend([
        f"Pagina di emergenza del sito: {SITO_URL}/emergenza/",
        "",
        "<i>Fonte: Comune di Genzano di Roma — Gruppo Comunale Volontari di Protezione Civile</i>",
        f"<i>Prossimo aggiornamento: su questo canale e su {SITO_URL}/emergenza/ appena la situazione cambia</i>",
        "",
        HASHTAG_EMERGENZA,
    ])
    return parti


def msg_emergenza_attivata(curr: dict) -> str:
    titolo = curr.get("titolo") or "Emergenza in corso"
    descrizione = curr.get("descrizione") or ""
    link = curr.get("link") or ""
    parti = ["🚨 <b>Emergenza in corso</b>", "", f"<b>{titolo}</b>", "Comune di Genzano di Roma."]
    if descrizione:
        parti.extend(["", descrizione])
    parti.extend([
        "",
        "<b>Cosa fare</b>",
        "• Segui le indicazioni del Comune e delle autorità.",
        "• Non recarti sul luogo dell'emergenza e non intralciare i soccorsi.",
        "• Usa il telefono solo per comunicazioni necessarie.",
        "📞 In caso di pericolo immediato chiama il <b>112</b>.",
        "",
    ])
    parti.extend(_coda_emergenza(link, "Maggiori informazioni"))
    return "\n".join(parti)


def msg_emergenza_aggiornata(curr: dict) -> str:
    titolo = curr.get("titolo") or "Emergenza in corso"
    descrizione = curr.get("descrizione") or ""
    link = curr.get("link") or ""
    parti = ["🚨 <b>Aggiornamento emergenza</b>", "", f"<b>{titolo}</b>", "Comune di Genzano di Roma."]
    if descrizione:
        parti.extend(["", descrizione])
    parti.extend([
        "",
        "<b>Cosa fare</b>",
        "• Continua a seguire le indicazioni del Comune e delle autorità.",
        "• Non recarti sul luogo dell'emergenza e non intralciare i soccorsi.",
        "📞 In caso di pericolo immediato chiama il <b>112</b>.",
        "",
    ])
    parti.extend(_coda_emergenza(link, "Aggiornamento"))
    return "\n".join(parti)


def msg_emergenza_cessata(prev: dict) -> str:
    titolo_prev = prev.get("titolo") or "Emergenza"
    parti = [
        "🟢 <b>Cessata emergenza</b>",
        "",
        f"L'emergenza «<b>{titolo_prev}</b>» è cessata. Comune di Genzano di Roma.",
        "Si torna alla normale operatività.",
        "",
        "<b>Cosa fare</b>",
        "• Presta comunque attenzione a eventuali situazioni locali residue.",
        "• Segnalazioni non urgenti alla Sala operativa regionale: 803 555.",
        "📞 In caso di pericolo chiama sempre il <b>112</b>.",
        "",
    ]
    parti.extend(_coda_emergenza("", ""))
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
        livello_curr = _norm_livello(allerta_curr.get("livello"))
        livello_prev = _norm_livello((allerta_prev or {}).get("livello")) if allerta_prev else None

        if allerta_prev is None:
            # Primo commit sul branch — notifica solo se non-verde
            if livello_curr and livello_curr != "verde":
                cat = CRITICAL if livello_curr in ("arancione", "rossa", "rosso") else INFORMATIONAL
                return (msg_allerta_cambiata(None, allerta_curr), cat)
        elif livello_curr != livello_prev:
            if livello_curr == "verde":
                return (msg_allerta_cambiata(allerta_prev, allerta_curr), CESSATION)
            if livello_curr in ("arancione", "rossa", "rosso"):
                return (msg_allerta_cambiata(allerta_prev, allerta_curr), CRITICAL)
            # gialla
            return (msg_allerta_cambiata(allerta_prev, allerta_curr), INFORMATIONAL)

    # Priorità 3: avviso meteo avverso (blocco avviso_meteo), se l'allerta non ha già notificato.
    # Scatta su comparsa/variazione di tipo o livello, e su rientro.
    avviso_curr = (allerta_curr or {}).get("avviso_meteo") or {}
    avviso_prev = (allerta_prev or {}).get("avviso_meteo") or {}
    tipo_curr = (avviso_curr.get("tipo") or "").strip()
    tipo_prev = (avviso_prev.get("tipo") or "").strip()
    liv_curr = _norm_livello(avviso_curr.get("livello"))
    liv_prev = _norm_livello(avviso_prev.get("livello"))
    if (tipo_curr, liv_curr) != (tipo_prev, liv_prev):
        if not tipo_curr and tipo_prev:
            return (msg_avviso_meteo(None), CESSATION)
        if tipo_curr:
            cat = CRITICAL if liv_curr in ("arancione", "rossa", "rosso") else INFORMATIONAL
            return (msg_avviso_meteo(avviso_curr), cat)

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
