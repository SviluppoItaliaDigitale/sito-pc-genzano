#!/usr/bin/env python3
"""Tiene agganciati gli articoli del sito alla pubblicazione sui social.

Regola dell'utente (21/09/2026): ogni articolo che esce sul sito esce anche
su Instagram e Facebook, in concomitanza. Questo script è la parte del sito
di quella promessa, in tre comandi:

  mancanti   quali articoli ONLINE non hanno ancora il materiale social
             completo (testi + immagini): sono quelli da generare adesso.
  sveglia    se chiamare subito la pubblicazione nel repository privato
             social-pc-genzano: sì quando un articolo pronto è appena
             diventato raggiungibile sul sito e non risulta ancora pubblicato.
  controlla  per il controllo di salute giornaliero: articoli online da ore
             senza materiale, o con il materiale pronto ma mai pubblicati.

    python3 scripts/social-pronti.py mancanti [--ore 72] [--riserva-dopo-min 60] [FILE.md ...]
    python3 scripts/social-pronti.py sveglia  [--ore 72] [--recenti-min 120] [--pausa-min 20]
    python3 scripts/social-pronti.py controlla [--ore 48] [--tolleranza-min 180]

Perché esiste (22/09/2026): le bozze nascevano solo al commit di un
articolo, e un articolo calendarizzato al commit ha una data futura: veniva
saltato e nessuno lo riprendeva quando la data arrivava. Il repository
privato pubblica solo ciò che ha il materiale pronto, quindi quegli articoli
non uscivano mai sui social. Ora il workflow genera-social-bozze.yml gira
anche al termine di ogni deploy, cioè nel momento esatto in cui un articolo
diventa online, e chiede a questo script che cosa manca.

Variabili d'ambiente (tutte facoltative, lo script degrada con prudenza):
  GH_TOKEN / GITHUB_TOKEN   date dei commit dall'API di GitHub (repo del sito)
  GITHUB_REPOSITORY         owner/repo del sito (predefinito il nostro)
  SOCIAL_PAT                token verso il repository privato: ultimo giro
                            della pubblicazione e, se il token lo consente,
                            lettura della coda (chi è già pubblicato)

Solo libreria standard.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import social_comune as S  # noqa: E402

REPO_SITO = os.environ.get("GITHUB_REPOSITORY", "").strip() or "SviluppoItaliaDigitale/sito-pc-genzano"
REPO_SOCIAL = "SviluppoItaliaDigitale/social-pc-genzano"
WORKFLOW_SOCIAL = "pubblica-social-auto.yml"
UA = "PCGenzanoSocial/1.0 (+https://www.protezionecivilegenzano.it/)"

# Stati di coda chiusi per scelta o per esito (social_coda_lib.STATI):
# `errore` non è fra questi, perché è un post che doveva uscire e non è uscito.
STATI_CHIUSI = ("pubblicato", "saltato")


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


# ──────────────────────────────────────────────────────────────
# GitHub
# ──────────────────────────────────────────────────────────────

def _api(url: str, token: str | None) -> object | None:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": UA,
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def _token_sito() -> str | None:
    return (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip() or None


def _token_social() -> str | None:
    return os.environ.get("SOCIAL_PAT", "").strip() or None


def _parse_iso(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(S.TZ)
    except ValueError:
        return None


def _shallow_boundary() -> set[str]:
    p = S.ROOT / ".git" / "shallow"
    try:
        return set(p.read_text().split())
    except OSError:
        return set()


def ultimo_commit(rel: str) -> dt.datetime | None:
    """Quando `rel` (file o cartella del repo) è cambiato l'ultima volta su main.

    Prima l'API di GitHub, che vede tutta la storia; poi git locale, scartando
    il commit di confine di un clone superficiale, che finge di aver creato
    ogni file e darebbe una data falsa e recentissima.
    """
    token = _token_sito()
    if token:
        url = (f"https://api.github.com/repos/{REPO_SITO}/commits?"
               + urllib.parse.urlencode({"path": rel, "per_page": 1, "sha": "main"}))
        dati = _api(url, token)
        if isinstance(dati, list):
            if not dati:
                return None
            try:
                return _parse_iso(dati[0]["commit"]["committer"]["date"])
            except (KeyError, IndexError, TypeError):
                pass
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", rel],
                             cwd=S.ROOT, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    parti = out.stdout.strip().split()
    if len(parti) != 2 or parti[0] in _shallow_boundary():
        return None
    return _parse_iso(parti[1])


def pronto_dal(path: Path, online: dt.datetime, *, bozze: bool) -> dt.datetime:
    """Da quando l'articolo è pronto: online per data E nella sua versione
    attuale (articolo) o col materiale committato (bozze)."""
    if bozze:
        rel = ("social-bozze" / S.slug_to_path(path.stem)).as_posix()
    else:
        rel = f"content/comunicazioni/{path.name}"
    c = ultimo_commit(rel)
    return max(online, c) if c else online


def ultimo_giro_social() -> dt.datetime | None:
    token = _token_social()
    if not token:
        return None
    dati = _api(f"https://api.github.com/repos/{REPO_SOCIAL}/actions/workflows/"
                f"{WORKFLOW_SOCIAL}/runs?per_page=1", token)
    try:
        return _parse_iso(dati["workflow_runs"][0]["created_at"])  # type: ignore[index]
    except (KeyError, IndexError, TypeError):
        return None


def voci_coda() -> dict[str, dict] | None:
    """Stato e orario di ogni voce della coda del repository privato, se il
    token consente di leggerla; None altrimenti (e si decide con prudenza).

    La coda è scritta da yaml.safe_dump (social_coda_lib.salva_coda): voci
    `- slug:` a colonna 0 e campi a due spazi. Lo `stato` a due spazi è
    quello della voce; quelli più rientrati sono dei singoli social.
    """
    token = _token_social()
    if not token:
        return None
    dati = _api(f"https://api.github.com/repos/{REPO_SOCIAL}/contents/coda-social.yaml", token)
    if not isinstance(dati, dict) or "content" not in dati:
        return None
    try:
        testo = base64.b64decode(dati["content"]).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None
    voci: dict[str, dict] = {}
    corrente = None
    for riga in testo.splitlines():
        m = re.match(r"^- slug:\s*['\"]?([^'\"\s]+)", riga)
        if m:
            corrente = m.group(1)
            voci[corrente] = {"stato": "in_coda", "pubblica_il": None}
            continue
        if corrente is None:
            continue
        m = re.match(r"^  stato:\s*['\"]?(\w+)", riga)
        if m:
            voci[corrente]["stato"] = m.group(1)
            continue
        m = re.match(r"^  pubblica_il:\s*['\"]?([^'\"\s]+)", riga)
        if m:
            voci[corrente]["pubblica_il"] = _parse_iso(m.group(1))
    return voci


def raggiungibile(slug: str, timeout: float = 15.0) -> bool:
    """Stesso controllo del repository privato (articolo_raggiungibile):
    la pagina deve rispondere davvero, non basta la data."""
    req = urllib.request.Request(S.url_articolo(slug), method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200 <= r.status < 300
    except Exception:
        return False


# ──────────────────────────────────────────────────────────────
# Comandi
# ──────────────────────────────────────────────────────────────

def cmd_mancanti(args) -> int:
    ora = S.adesso()
    scelti: dict[Path, dt.datetime] = {}
    for p, _fm, d in S.articoli(args.ore, ora):
        scelti[p] = d
    # File passati esplicitamente (articoli toccati da un push): valgono a
    # qualunque età, purché online e non versioni facili.
    for f in args.file:
        p = (S.ROOT / f).resolve() if not Path(f).is_absolute() else Path(f)
        if not p.is_file() or p in scelti:
            continue
        fm = S.leggi_frontmatter(p)
        if not fm or S.is_facile(p, fm) or not S.is_online(fm, ora):
            continue
        scelti[p] = S.online_dal(fm)  # type: ignore[assignment]

    n = 0
    for p, d in sorted(scelti.items(), key=lambda t: t[1], reverse=True):
        slug = p.stem
        if S.materiale_completo(slug):
            continue
        pronto = pronto_dal(p, d, bozze=False)
        eta_min = (ora - pronto).total_seconds() / 60
        riserva = 1 if eta_min >= args.riserva_dopo_min else 0
        mancano = [x for x, ok in (("testi", S.testi_completi(slug)),
                                    ("immagini", S.immagini_complete(slug))) if not ok]
        log(f"  manca {' e '.join(mancano)}: {slug} (online dal {S.fmt(d)}, "
            f"pronto da {int(eta_min)} min{', testi di riserva ammessi' if riserva else ''})")
        print(f"{p.relative_to(S.ROOT).as_posix()}\t{riserva}")
        n += 1
    log(f"Articoli online senza materiale social completo: {n}")
    return 0


def cmd_sveglia(args) -> int:
    ora = S.adesso()
    coda = voci_coda()
    log("Coda del repository social: " + ("letta" if coda is not None
        else "non leggibile con questo token, si decide dalle sole date"))
    pronti = []
    for p, fm, d in S.articoli(args.ore, ora):
        slug = p.stem
        if not S.candidato_auto(p, fm) or not S.materiale_pubblicabile(slug):
            continue
        voce = coda.get(slug) if coda is not None else None
        if voce is not None:
            # La coda sa già tutto: si sveglia solo per una voce matura.
            # `errore` resta fermo: il repository privato ha aperto la sua
            # issue e senza una correzione riproverebbe a vuoto.
            if voce["stato"] != "in_coda":
                continue
            quando = voce.get("pubblica_il")
            if quando is not None and quando > ora:
                continue
        else:
            # Articolo non ancora in coda (o coda illeggibile): si sveglia solo
            # se il materiale è pronto da poco. Se è pronto da ore e non è
            # ancora uscito, lo prendono i giri programmati del repository
            # privato: richiamarlo a ogni deploy consumerebbe i suoi minuti
            # senza cambiare nulla.
            pronto = pronto_dal(p, d, bozze=True)
            if (ora - pronto).total_seconds() > args.recenti_min * 60:
                continue
        if not raggiungibile(slug):
            log(f"  pronto ma la pagina non risponde ancora: {slug} (aspetto il deploy)")
            continue
        log(f"  pronto e online: {slug}")
        pronti.append(slug)

    decisione = "no"
    if pronti:
        giro = ultimo_giro_social()
        if giro and (ora - giro).total_seconds() < args.pausa_min * 60:
            log(f"Il repository social ha un giro partito alle {S.fmt(giro)}: "
                f"non lo richiamo prima di {args.pausa_min} minuti.")
        else:
            decisione = "si"
    print(f"sveglia={decisione}")
    uscita = os.environ.get("GITHUB_OUTPUT")
    if uscita:
        with open(uscita, "a", encoding="utf-8") as fh:
            fh.write(f"sveglia={decisione}\n")
    return 0


def cmd_controlla(args) -> int:
    ora = S.adesso()
    tolleranza = dt.timedelta(minutes=args.tolleranza_min)
    senza_materiale, non_pubblicati = [], []
    coda = voci_coda()
    for p, fm, d in S.articoli(args.ore, ora):
        slug = p.stem
        if not S.materiale_completo(slug):
            if ora - pronto_dal(p, d, bozze=False) >= tolleranza:
                senza_materiale.append((slug, d))
            continue
        if coda is None or not S.candidato_auto(p, fm):
            continue
        voce = coda.get(slug)
        if voce is not None and voce["stato"] in STATI_CHIUSI:
            continue
        if voce is not None and voce["stato"] == "in_coda" \
                and voce.get("pubblica_il") and voce["pubblica_il"] > ora:
            continue  # programmata più avanti di proposito
        if ora - pronto_dal(p, d, bozze=True) >= tolleranza:
            non_pubblicati.append((slug, d, voce["stato"] if voce else "assente dalla coda"))

    righe = []
    if senza_materiale:
        righe.append("### Articoli online senza materiale social\n")
        righe.append(f"Online da oltre {args.tolleranza_min // 60} ore e ancora senza testi o "
                     "immagini in `social-bozze/`: il repository social non può pubblicarli.\n")
        righe += [f"- `{s}` — online dal {S.fmt(d)}" for s, d in senza_materiale]
        righe.append("\nDa controllare: il log di «📱 Genera bozze social automatiche» "
                     "(quota Gemini, cover mancante, errore di frontmatter).\n")
    if non_pubblicati:
        righe.append("### Articoli pronti ma non pubblicati sui social\n")
        righe += [f"- `{s}` — online dal {S.fmt(d)}, stato in coda: {st}" for s, d, st in non_pubblicati]
        righe.append(f"\nDa controllare: le issue e l'ultimo giro di `{REPO_SOCIAL}`.\n")
    if coda is None:
        log("Coda social non leggibile: controllata solo la presenza del materiale.")
    if righe:
        print("\n".join(righe))
    return min(len(senza_materiale) + len(non_pubblicati), 100)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("mancanti", help="articoli online senza materiale social completo")
    m.add_argument("file", nargs="*", help="articoli toccati da un push (qualunque età)")
    m.add_argument("--ore", type=float, default=S.FINESTRA_RECUPERO_ORE,
                   help="quanto indietro guardare (predefinito: la finestra del repository social)")
    m.add_argument("--riserva-dopo-min", type=int, default=60,
                   help="da quanti minuti l'articolo deve essere pronto perché, se Gemini "
                        "non risponde, si ammettano i testi di riserva")

    s = sub.add_parser("sveglia", help="decide se chiamare subito la pubblicazione")
    s.add_argument("--ore", type=float, default=S.FINESTRA_RECUPERO_ORE - 6,
                   help="finestra degli articoli, un po' più stretta di quella del "
                        "repository social per non svegliarlo su voci che rifiuterebbe")
    s.add_argument("--recenti-min", type=int, default=120,
                   help="sveglia solo per il materiale pronto da meno di N minuti")
    s.add_argument("--pausa-min", type=int, default=20,
                   help="non richiamare se il repository social è partito da meno di N minuti")

    c = sub.add_parser("controlla", help="controllo di salute: articoli rimasti indietro")
    c.add_argument("--ore", type=float, default=48)
    c.add_argument("--tolleranza-min", type=int, default=180)

    args = p.parse_args()
    return {"mancanti": cmd_mancanti, "sveglia": cmd_sveglia, "controlla": cmd_controlla}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
