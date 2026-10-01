#!/usr/bin/env python3
"""Copia d'archivio degli articoli appena usciti sulla Wayback Machine.

Perché esiste (01/10/2026): quando un nostro testo compare altrove, senza
fonte o con una data anteriore, serve poter dimostrare chi l'ha pubblicato
per primo. Il commit git lo dimostra a noi, non a un terzo. Una copia
d'archivio di Internet Archive invece è datata da un ente indipendente, è
consultabile da chiunque e non la possiamo modificare: è la prova di prima
pubblicazione più semplice che esista, ed è gratuita.

Che cosa fa, a ogni giro:

  1. individua gli articoli di content/comunicazioni/ ONLINE (data già
     arrivata, in ora italiana, come Hugo) usciti o cambiati di recente:
     data negli ultimi N giorni oppure ultimo commit del file negli ultimi
     N giorni (predefinito 3). Le versioni in italiano semplice (-facile)
     sono escluse: ripetono un articolo già archiviato;
  2. per ciascuno chiede a https://archive.org/wayback/available la copia
     più recente (timestamp = adesso: la copia «più vicina ad adesso» è
     l'ultima) e la confronta con l'ultima modifica dell'articolo, cioè il
     più recente fra la data dell'ultimo commit del file e la data di uscita,
     più MARGINE_DEPLOY minuti per il caricamento su Aruba. Se la copia è
     successiva, l'articolo è già coperto e si salta;
  3. altrimenti chiede il salvataggio, al massimo MAX_PER_GIRO articoli per
     giro, a distanza di qualche secondo l'uno dall'altro.

Due modi di chiedere il salvataggio:

  - senza credenziali: GET https://web.archive.org/save/<url> con un user
    agent che dice chi siamo. Limite di Internet Archive per gli anonimi:
    3 salvataggi al minuto, quindi la pausa è di 21 secondi;
  - con le chiavi gratuite di un account archive.org (variabili d'ambiente
    IA_S3_ACCESS e IA_S3_SECRET, da https://archive.org/account/s3.php):
    API Save Page Now 2, POST https://web.archive.org/save con
    `Authorization: LOW <access>:<secret>` e `Accept: application/json`,
    poi lettura dello stato su /save/status/<job_id>. Limite per gli utenti
    autenticati: 7 al minuto, pausa di 10 secondi. Parametri usati, tutti
    presi dalla documentazione pubblica SPN2 (aggiornata al 22/07/2026):
    `skip_first_archive=1` (non ci serve sapere se è la prima copia) e
    `js_behavior_timeout=0` (le nostre pagine sono statiche, niente da
    scorrere o cliccare).

Un 429 (troppe richieste) chiude il giro: si riprova al successivo. Qualunque
errore di rete finisce nel log e lo script esce comunque con 0: una copia
d'archivio mancata non deve mai fermare un deploy.

    python3 scripts/archivia-wayback.py [--giorni 3] [--max 10] [--dry-run] [--verifica]

Con --dry-run non contatta la rete: elenca gli articoli che verificherebbe e
salverebbe. Con --dry-run --verifica interroga anche l'API di disponibilità
(sola lettura), senza chiedere salvataggi.

Solo libreria standard.
"""

from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import social_comune as S  # noqa: E402

UA = "PCGenzanoArchivio/1.0 (+https://www.protezionecivilegenzano.it/)"
API_DISPONIBILE = "https://archive.org/wayback/available"
SALVA = "https://web.archive.org/save"
STATO = "https://web.archive.org/save/status/"

MAX_PER_GIRO = 10
# Limiti dichiarati da Internet Archive: 3 salvataggi al minuto per gli
# anonimi, 7 per gli autenticati. Le pause stanno un po' sotto.
PAUSA_ANONIMO_S = 21
PAUSA_AUTENTICATO_S = 10
TIMEOUT_DISPONIBILE_S = 30
# Una cattura può durare fino a 2 minuti dal lato di Internet Archive.
TIMEOUT_SALVA_S = 150
ATTESA_STATO_S = 120
# Tetto di tempo del giro: il job ha 20 minuti di timeout, e dieci salvataggi
# anonimi lenti (pausa + cattura fino a 150 s) li supererebbero. Passato il
# tetto non si apre un'altra richiesta: gli altri al giro successivo.
BUDGET_GIRO_S = 15 * 60
# Fra il commit su main e la pagina servita da Aruba passa il caricamento
# FTP (in genere un quarto d'ora): una copia fatta in quella finestra
# mostrerebbe ancora la versione precedente.
MARGINE_DEPLOY = dt.timedelta(minutes=20)

UTC = dt.timezone.utc


class TroppeRichieste(Exception):
    """Internet Archive ha risposto 429: il giro finisce qui."""


def log(msg: str) -> None:
    print(msg, flush=True)


def ts_wayback(d: dt.datetime) -> str:
    return d.astimezone(UTC).strftime("%Y%m%d%H%M%S")


def da_ts_wayback(s: str) -> dt.datetime | None:
    try:
        return dt.datetime.strptime(s, "%Y%m%d%H%M%S").replace(tzinfo=UTC)
    except (TypeError, ValueError):
        return None


# ──────────────────────────────────────────────────────────────
# Git: data dell'ultimo commit di ogni articolo
# ──────────────────────────────────────────────────────────────

def _commit_di_confine() -> set[str]:
    """In un clone parziale (fetch-depth 1) il commit più vecchio presente
    risulta aver aggiunto TUTTI i file: la sua data non dice nulla sulle
    modifiche. Si ignorano i commit elencati in .git/shallow."""
    try:
        out = subprocess.run(["git", "rev-parse", "--git-path", "shallow"],
                             cwd=S.ROOT, capture_output=True, text=True, timeout=15).stdout.strip()
        p = (S.ROOT / out) if out and not Path(out).is_absolute() else Path(out)
        return set(p.read_text().split()) if out and p.is_file() else set()
    except (OSError, subprocess.SubprocessError):
        return set()


def ultimi_commit(giorni: int) -> dict[str, dt.datetime]:
    """Nome file → istante dell'ultimo commit che lo ha toccato negli ultimi
    `giorni` giorni (solo content/comunicazioni/)."""
    confine = _commit_di_confine()
    if confine:
        log("Avviso: clone parziale, ignoro i commit di confine (in CI serve fetch-depth: 0).")
    try:
        out = subprocess.run(
            ["git", "log", f"--since={giorni} days ago", "--name-only",
             "--format=@@%H %cI", "--", "content/comunicazioni/"],
            cwd=S.ROOT, capture_output=True, text=True, timeout=60,
        ).stdout
    except (OSError, subprocess.SubprocessError) as e:
        log(f"Avviso: git log non disponibile ({e}); uso solo la data degli articoli.")
        return {}
    mappa: dict[str, dt.datetime] = {}
    quando: dt.datetime | None = None
    for riga in out.splitlines():
        riga = riga.strip()
        if riga.startswith("@@"):
            sha, _, iso = riga[2:].partition(" ")
            quando = None if sha in confine else S.data_online(iso)
            continue
        if not riga or quando is None:
            continue
        nome = Path(riga).name
        # git log va dal più recente: il primo incontro è l'ultimo commit.
        mappa.setdefault(nome, quando)
    return mappa


# ──────────────────────────────────────────────────────────────
# Articoli da archiviare
# ──────────────────────────────────────────────────────────────

def candidati(giorni: int, ora: dt.datetime) -> list[dict]:
    limite = ora - dt.timedelta(days=giorni)
    commit = ultimi_commit(giorni)
    out = []
    for path, fm, online in S.articoli(ora=ora):
        modificato = commit.get(path.name)
        if online < limite and (modificato is None or modificato < limite):
            continue
        ultima = max(d for d in (online, modificato) if d is not None)
        out.append({
            "slug": path.stem,
            "url": S.url_articolo(path.stem),
            "online": online,
            "ultima_modifica": ultima,
            "da_superare": ultima + MARGINE_DEPLOY,
        })
    out.sort(key=lambda c: c["ultima_modifica"], reverse=True)
    return out


# ──────────────────────────────────────────────────────────────
# Internet Archive
# ──────────────────────────────────────────────────────────────

def _richiesta(url: str, *, dati: dict | None = None, intestazioni: dict | None = None,
               timeout: int = 30) -> tuple[int, str, dict, str]:
    """(codice HTTP, URL finale, intestazioni, corpo). Solleva TroppeRichieste
    sul 429; gli altri errori HTTP tornano come codice."""
    corpo = urllib.parse.urlencode(dati).encode() if dati is not None else None
    req = urllib.request.Request(url, data=corpo, headers={"User-Agent": UA, **(intestazioni or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            testo = r.read(2_000_000).decode("utf-8", "replace")
            return r.getcode(), r.geturl(), dict(r.headers), testo
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise TroppeRichieste() from e
        try:
            testo = e.read(200_000).decode("utf-8", "replace")
        except OSError:
            testo = ""
        return e.code, url, dict(e.headers or {}), testo
    except http.client.HTTPException as e:
        # IncompleteRead e simili non sono OSError: si convertono, così il
        # chiamante salta solo questo articolo invece di chiudere il giro.
        raise OSError(type(e).__name__) from e


def copia_piu_recente(url: str, ora: dt.datetime) -> tuple[dt.datetime | None, str]:
    """Ultima copia con esito 200 nota all'API di disponibilità."""
    q = urllib.parse.urlencode({"url": url, "timestamp": ts_wayback(ora)})
    codice, _, _, testo = _richiesta(f"{API_DISPONIBILE}?{q}", timeout=TIMEOUT_DISPONIBILE_S)
    if codice != 200:
        raise OSError(f"API di disponibilità: HTTP {codice}")
    vicina = (json.loads(testo).get("archived_snapshots") or {}).get("closest") or {}
    if not vicina.get("available") or str(vicina.get("status")) != "200":
        return None, ""
    return da_ts_wayback(vicina.get("timestamp", "")), vicina.get("url", "")


def _indirizzo_copia(ts: str, url: str) -> str:
    return f"archiviato: https://web.archive.org/web/{ts}/{url}"


def salva_anonimo(url: str) -> str:
    """La risposta può essere la copia (redirect su /web/<timestamp>/) oppure
    una pagina che dice che la cattura è in corso: nel secondo caso la copia
    si conferma al giro successivo, con l'API di disponibilità."""
    codice, finale, intest, _ = _richiesta(f"{SALVA}/{url}", timeout=TIMEOUT_SALVA_S)
    for candidato in (finale, intest.get("Content-Location", ""), intest.get("Location", "")):
        m = re.search(r"/web/(\d{14})", candidato or "")
        if m:
            return _indirizzo_copia(m.group(1), url)
    if 200 <= codice < 300:
        return "richiesta accettata, copia in preparazione (la conferma al prossimo giro)"
    raise OSError(f"salvataggio rifiutato (HTTP {codice})")


def salva_spn2(url: str, access: str, secret: str) -> str:
    intest = {"Accept": "application/json", "Authorization": f"LOW {access}:{secret}"}
    codice, _, _, testo = _richiesta(
        SALVA, dati={"url": url, "skip_first_archive": "1", "js_behavior_timeout": "0"},
        intestazioni=intest, timeout=TIMEOUT_DISPONIBILE_S,
    )
    try:
        risposta = json.loads(testo)
    except ValueError:
        raise OSError(f"risposta non JSON (HTTP {codice})")
    job = risposta.get("job_id")
    if not job:
        raise OSError(f"richiesta rifiutata (HTTP {codice}): {risposta.get('message') or risposta.get('status_ext') or testo[:200]}")
    scadenza = time.monotonic() + ATTESA_STATO_S
    while time.monotonic() < scadenza:
        time.sleep(6)
        _, _, _, testo = _richiesta(STATO + job, intestazioni=intest, timeout=TIMEOUT_DISPONIBILE_S)
        try:
            stato = json.loads(testo)
        except ValueError:
            continue
        if stato.get("status") == "success" and stato.get("timestamp"):
            return _indirizzo_copia(stato["timestamp"], stato.get("original_url") or url)
        if stato.get("status") == "error":
            raise OSError(f"{stato.get('status_ext', 'errore')}: {stato.get('message', '')}")
    raise OSError(f"cattura ancora in corso dopo {ATTESA_STATO_S} s (job {job})")


# ──────────────────────────────────────────────────────────────
# Giro
# ──────────────────────────────────────────────────────────────

def giro(args: argparse.Namespace) -> None:
    ora = S.adesso()
    lista = candidati(args.giorni, ora)
    access = os.environ.get("IA_S3_ACCESS", "").strip()
    secret = os.environ.get("IA_S3_SECRET", "").strip()
    autenticato = bool(access and secret)
    pausa = PAUSA_AUTENTICATO_S if autenticato else PAUSA_ANONIMO_S
    modo = "Save Page Now 2 con chiavi" if autenticato else "salvataggio anonimo"

    log(f"Articoli online usciti o cambiati negli ultimi {args.giorni} giorni: {len(lista)}"
        f" — modo: {modo}, massimo {args.max} salvataggi per giro.")
    if not lista:
        return

    if args.dry_run and not args.verifica:
        for c in lista[:args.max]:
            log(f"- {c['url']}\n    ultima modifica {S.fmt(c['ultima_modifica'])}:"
                f" verificherei la copia più recente; se precede {S.fmt(c['da_superare'])}"
                f" chiederei il salvataggio")
        if len(lista) > args.max:
            log(f"(altri {len(lista) - args.max} rimandati al giro successivo)")
        return

    salvati = 0
    inizio = time.monotonic()
    for c in lista:
        if time.monotonic() - inizio > BUDGET_GIRO_S:
            log("Tempo del giro esaurito: gli altri al prossimo.")
            break
        if salvati >= args.max:
            log("Raggiunto il massimo del giro: gli altri al prossimo.")
            break
        url = c["url"]
        try:
            ts, copia = copia_piu_recente(url, ora)
        except TroppeRichieste:
            log("Internet Archive risponde 429 (troppe richieste): riprovo al prossimo giro.")
            return
        except (OSError, ValueError) as e:
            log(f"- {url}\n    verifica non riuscita ({e}): salto")
            continue
        if ts and ts >= c["da_superare"]:
            log(f"- {url}\n    già archiviato il {S.fmt(ts)}: {copia}")
            continue
        motivo = f"ultima copia del {S.fmt(ts)}" if ts else "nessuna copia"
        if args.dry_run:
            log(f"- {url}\n    {motivo}, modificato il {S.fmt(c['ultima_modifica'])}: chiederei il salvataggio")
            salvati += 1
            continue
        if salvati:
            time.sleep(pausa)
        try:
            indirizzo = salva_spn2(url, access, secret) if autenticato else salva_anonimo(url)
            log(f"- {url}\n    {motivo} → {indirizzo}")
        except TroppeRichieste:
            log("Internet Archive risponde 429 (troppe richieste): riprovo al prossimo giro.")
            return
        except (OSError, ValueError) as e:
            log(f"- {url}\n    {motivo} → salvataggio non riuscito: {e}")
        salvati += 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Copia d'archivio degli articoli recenti sulla Wayback Machine.")
    ap.add_argument("--giorni", type=int, default=3, help="finestra degli articoli usciti o cambiati (predefinito 3)")
    ap.add_argument("--max", type=int, default=MAX_PER_GIRO, help=f"salvataggi massimi per giro (predefinito {MAX_PER_GIRO})")
    ap.add_argument("--dry-run", action="store_true", help="non chiede salvataggi; senza --verifica non usa la rete")
    ap.add_argument("--verifica", action="store_true", help="con --dry-run interroga anche l'API di disponibilità")
    args = ap.parse_args()
    args.max = max(0, min(args.max, MAX_PER_GIRO))
    try:
        giro(args)
    except Exception as e:  # noqa: BLE001 — una copia mancata non ferma mai la pipeline
        log(f"Errore non bloccante: {type(e).__name__}: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
