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


STATI_IN_CORSO = ("queued", "in_progress", "waiting", "requested", "pending")


def ultimo_giro_social() -> dict | None:
    """Ultimo giro del workflow di pubblicazione nel repository privato:
    {"creato": datetime, "in_corso": bool}, o None se non leggibile."""
    token = _token_social()
    if not token:
        return None
    dati = _api(f"https://api.github.com/repos/{REPO_SOCIAL}/actions/workflows/"
                f"{WORKFLOW_SOCIAL}/runs?per_page=1", token)
    try:
        run = dati["workflow_runs"][0]  # type: ignore[index]
        return {"creato": _parse_iso(run["created_at"]),
                "in_corso": run.get("status") in STATI_IN_CORSO}
    except (KeyError, IndexError, TypeError):
        return None


def chiama_social() -> bool:
    """Lancia il workflow di pubblicazione del repository privato."""
    token = _token_social()
    if not token:
        log("SOCIAL_PAT assente: non posso chiamare il repository social.")
        return False
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO_SOCIAL}/actions/workflows/{WORKFLOW_SOCIAL}/dispatches",
        data=json.dumps({"ref": "main"}).encode("utf-8"), method="POST",
        headers={"Accept": "application/vnd.github+json", "User-Agent": UA,
                 "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return 200 <= r.status < 300
    except Exception as e:
        log(f"Chiamata al repository social non riuscita: {e}")
        return False


def articoli_aggiunti_di_recente(ore: float) -> set[str]:
    """Slug degli articoli comparsi su main nelle ultime `ore`, qualunque sia
    la loro data. Servono per gli articoli retrodatati (un resoconto scritto
    giorni dopo l'intervento), che la sola data farebbe cadere fuori da ogni
    finestra. Vuoto se l'API non risponde."""
    token = _token_sito()
    if not token:
        return set()
    da = (S.adesso() - dt.timedelta(hours=ore)).astimezone(dt.timezone.utc)
    url = (f"https://api.github.com/repos/{REPO_SITO}/commits?"
           + urllib.parse.urlencode({"path": "content/comunicazioni", "sha": "main",
                                     "since": da.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     "per_page": 100}))
    commits = _api(url, token)
    if not isinstance(commits, list):
        return set()
    slug = set()
    for c in commits:
        dettaglio = _api(f"https://api.github.com/repos/{REPO_SITO}/commits/{c.get('sha')}", token)
        for f in (dettaglio or {}).get("files", []) if isinstance(dettaglio, dict) else []:
            nome = f.get("filename", "")
            if (f.get("status") == "added" and nome.startswith("content/comunicazioni/")
                    and nome.endswith(".md") and not nome.endswith("-facile.md")
                    and not nome.endswith("_index.md")):
                slug.add(Path(nome).stem)
    return slug


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
    # File passati esplicitamente (articoli toccati da un push) e articoli
    # comparsi su main di recente (i retrodatati): valgono a qualunque età,
    # purché online e non versioni facili.
    recenti = [f"content/comunicazioni/{s}.md" for s in articoli_aggiunti_di_recente(args.ore)]
    for f in list(args.file) + recenti:
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


RIPROVA_MIN = 60  # una voce che il repository social ha già visto si richiama al massimo ogni ora
# Specchio di social_coda_lib.INTERVALLO_MINIMO_MINUTI: minuti fra un post e
# l'altro. Se cambia là, va cambiato qui.
INTERVALLO_SOCIAL_MIN = 30


def slot_previsti(coda: dict[str, dict], online: list[dt.datetime],
                  ora: dt.datetime) -> list[dt.datetime]:
    """Istanti che il repository social assegnerà agli articoli assenti dalla
    coda quando lo si sveglia: specchio di social_coda_lib.prossimo_slot, che
    parte da adesso (o dall'uscita sul sito) e scorre in avanti di mezz'ora
    finché non è lontano dagli altri post, pubblicati o in coda.

    Serve a sapere PRIMA di svegliarlo quali post non usciranno subito: la
    coda li conterrà solo dopo il suo giro, e nessun evento cadrà quando
    maturano (notte del 23/09/2026: due articoli online insieme, il secondo
    programmato mezz'ora dopo il primo è uscito solo col giro orario
    successivo, perché al momento della decisione la coda non lo conteneva).
    """
    passo = dt.timedelta(minutes=INTERVALLO_SOCIAL_MIN).total_seconds()
    occupati = [v["pubblica_il"] for v in coda.values()
                if v["stato"] in ("in_coda", "pubblicato") and v["pubblica_il"]]
    out = []
    for d in sorted(online):
        cand = max(d, ora)
        cambiato = True
        while cambiato:
            cambiato = False
            for o in occupati:
                if abs((cand - o).total_seconds()) < passo:
                    cand = o + dt.timedelta(seconds=passo)
                    cambiato = True
        occupati.append(cand)
        out.append(cand)
    return out


def decidi(args) -> tuple[bool, int]:
    """(chiamare adesso il repository social?, minuti alla prossima voce in
    coda che matura entro --attesa-max-min, 0 se nessuna).

    Con la coda leggibile la decisione è esatta:
      - voce in coda e matura, pagina online → sì, salvo che un giro sia già
        in corso, o che il repository social sia già partito dopo che la voce
        è maturata (allora al massimo una volta l'ora: un guasto che si
        ripete non deve consumare i suoi minuti a ogni deploy);
      - voce in coda ma programmata più avanti (i 30 minuti fra un post e
        l'altro) → no adesso, ma si segnala fra quanto matura;
      - articolo pronto e online ma assente dalla coda → sì, con la stessa
        regola dell'ora;
      - voce pubblicata, saltata o in errore → no.
    Con la coda illeggibile si procede per date: materiale pronto da meno di
    --recenti-min minuti e nessun giro partito negli ultimi --pausa-min.

    L'attesa conta anche i post che il repository social metterà in coda
    più avanti al giro che si sta per chiamare (slot_previsti): senza, con
    due articoli usciti insieme il secondo aspetterebbe il giro programmato.
    """
    ora = S.adesso()
    coda = voci_coda()
    giro = ultimo_giro_social()
    log("Coda del repository social: " + ("letta" if coda is not None
        else "non leggibile con questo token, si decide dalle sole date"))
    if giro:
        log(f"Ultimo giro del repository social: {S.fmt(giro['creato'])}"
            + (" (in corso)" if giro["in_corso"] else ""))

    def gia_visto(dal: dt.datetime) -> bool:
        """Il repository social è partito dopo `dal` e da meno di un'ora."""
        return bool(giro and giro["creato"] and giro["creato"] >= dal
                    and (ora - giro["creato"]).total_seconds() < RIPROVA_MIN * 60)

    pronti, attese, assenti = [], [], []
    for p, fm, d in S.articoli(args.ore, ora):
        slug = p.stem
        if not S.candidato_auto(p, fm) or not S.materiale_pubblicabile(slug):
            continue
        if coda is not None:
            voce = coda.get(slug)
            if voce is not None:
                if voce["stato"] != "in_coda":
                    continue
                quando = voce.get("pubblica_il")
                if quando is not None and quando > ora:
                    attese.append(quando)
                    continue
                if gia_visto(quando or d):
                    continue
            else:
                if gia_visto(pronto_dal(p, d, bozze=True)):
                    continue
        else:
            pronto = pronto_dal(p, d, bozze=True)
            if (ora - pronto).total_seconds() > args.recenti_min * 60:
                continue
        if not raggiungibile(slug):
            log(f"  pronto ma la pagina non risponde ancora: {slug} (aspetto il deploy)")
            continue
        log(f"  pronto e online: {slug}")
        pronti.append(slug)
        if coda is not None and slug not in coda:
            assenti.append(d)

    sveglia = False
    if pronti:
        if giro and giro["in_corso"]:
            log("Il repository social ha un giro in corso: pubblicherà lui.")
        elif (coda is None and giro and giro["creato"]
              and (ora - giro["creato"]).total_seconds() < args.pausa_min * 60):
            log(f"Il repository social è partito alle {S.fmt(giro['creato'])}: "
                f"non lo richiamo prima di {args.pausa_min} minuti.")
        else:
            sveglia = True

    if pronti:
        # Chi non esce a questo giro, il repository social lo mette in coda
        # più avanti: si calcola adesso quando, per affidarne l'attesa.
        if coda is not None:
            dopo = [q for q in slot_previsti(coda, assenti, ora)
                    if (q - ora).total_seconds() > 60]
            for q in dopo:
                log(f"  il repository social lo metterà in coda per le {S.fmt(q)}")
            attese.extend(dopo)
        elif len(pronti) > 1:
            attese.append(ora + dt.timedelta(minutes=INTERVALLO_SOCIAL_MIN))

    attesa = 0
    vicine = [q for q in attese if (q - ora).total_seconds() <= args.attesa_max_min * 60]
    if vicine:
        prossima = min(vicine)
        attesa = max(1, int((prossima - ora).total_seconds() // 60) + 1)
        log(f"Prossima voce in coda alle {S.fmt(prossima)} (fra {attesa} min).")
    return sveglia, attesa


def _scrivi_output(**valori) -> None:
    uscita = os.environ.get("GITHUB_OUTPUT")
    if uscita:
        with open(uscita, "a", encoding="utf-8") as fh:
            for k, v in valori.items():
                fh.write(f"{k}={v}\n")


def cmd_sveglia(args) -> int:
    sveglia, attesa = decidi(args)
    decisione = "si" if sveglia else "no"
    print(f"sveglia={decisione}")
    print(f"attesa_min={attesa}")
    _scrivi_output(sveglia=decisione, attesa_min=attesa)
    return 0


def cmd_attendi(args) -> int:
    """Resta sveglio fino a --max-min minuti e chiama il repository social
    ogni volta che una voce in coda matura. Serve ai post distanziati di
    mezz'ora: nessun altro evento cade in quell'istante, e i giri programmati
    di GitHub in questi repository partono a blocchi di ore. Gira nel
    repository del sito, i cui minuti sono gratuiti."""
    import time
    fine = time.monotonic() + args.max_min * 60
    while time.monotonic() < fine:
        sveglia, attesa = decidi(args)
        if sveglia:
            if chiama_social():
                log(f"{S.fmt(S.adesso())}: pubblicazione richiesta al repository social.")
            time.sleep(180)  # il tempo di partire e di aggiornare la coda
            continue
        if not attesa:
            log("Nessuna voce in attesa: finito.")
            return 0
        resto = fine - time.monotonic()
        pausa = min(attesa * 60 + 30, resto)
        if pausa <= 0:
            break
        log(f"Attendo {int(pausa // 60)} min.")
        time.sleep(pausa)
    log("Tempo massimo raggiunto: ci penseranno i giri programmati.")
    return 0


def cmd_controlla(args) -> int:
    ora = S.adesso()
    tolleranza = dt.timedelta(minutes=args.tolleranza_min)
    senza_materiale, non_pubblicati, non_verificabili = [], [], []
    coda = voci_coda()
    visti = set()
    for p, fm, d in S.articoli(args.ore, ora):
        visti.add(p.stem)
        slug = p.stem
        if not S.materiale_completo(slug):
            if ora - pronto_dal(p, d, bozze=False) >= tolleranza:
                senza_materiale.append((slug, d))
            continue
        if not S.candidato_auto(p, fm):
            continue
        if ora - pronto_dal(p, d, bozze=True) < tolleranza:
            continue
        if coda is None:
            non_verificabili.append((slug, d))
            continue
        voce = coda.get(slug)
        if voce is not None and voce["stato"] in STATI_CHIUSI:
            continue
        if voce is not None and voce["stato"] == "in_coda" \
                and voce.get("pubblica_il") and voce["pubblica_il"] > ora:
            continue  # programmata più avanti di proposito
        non_pubblicati.append((slug, d, voce["stato"] if voce else "assente dalla coda"))

    # Retrodatati: comparsi sul sito di recente con una data più vecchia della
    # finestra del repository social, che li scarta. Vanno pubblicati a mano.
    retrodatati = []
    for slug in sorted(articoli_aggiunti_di_recente(args.ore) - visti):
        p = S.CONTENT_COMUNICAZIONI / f"{slug}.md"
        fm = S.leggi_frontmatter(p)
        if not fm or not S.candidato_auto(p, fm) or not S.is_online(fm, ora):
            continue
        dal = S.online_dal(fm)
        if dal is None or dal >= ora - dt.timedelta(hours=S.FINESTRA_RECUPERO_ORE - 6):
            continue  # ancora dentro la finestra del repository social: non è retrodatato
        voce = (coda or {}).get(slug)
        if voce is not None and voce["stato"] in STATI_CHIUSI:
            continue
        retrodatati.append((slug, dal))

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
    if retrodatati:
        righe.append("### Articoli retrodatati: fuori dalla pubblicazione automatica\n")
        righe.append("Comparsi sul sito di recente ma con una data più vecchia di tre giorni: "
                     "il repository social li scarta. Vanno pubblicati a mano "
                     "(`coda-social.py accoda <slug>` nel repository social).\n")
        righe += [f"- `{s}` — datato {S.fmt(d)}" for s, d in retrodatati]
        righe.append("")
    if non_verificabili:
        righe.append("### Pubblicazione social non verificabile\n")
        righe.append(f"`SOCIAL_REPO_PAT` non riesce a leggere `coda-social.yaml` di `{REPO_SOCIAL}` "
                     "(permesso Contents: Read mancante, o API non raggiungibile): non si sa se "
                     f"questi articoli, pronti da oltre {args.tolleranza_min // 60} ore, siano usciti.\n")
        righe += [f"- `{s}` — online dal {S.fmt(d)}" for s, d in non_verificabili]
        righe.append("")
    if righe:
        print("\n".join(righe))
    return min(len(senza_materiale) + len(non_pubblicati) + len(retrodatati)
               + len(non_verificabili), 100)


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

    for nome, aiuto in (("sveglia", "decide se chiamare subito la pubblicazione"),
                        ("attendi", "resta sveglio e chiama la pubblicazione quando le voci in coda maturano")):
        s = sub.add_parser(nome, help=aiuto)
        s.add_argument("--ore", type=float, default=S.FINESTRA_RECUPERO_ORE - 6,
                       help="finestra degli articoli, un po' più stretta di quella del "
                            "repository social per non svegliarlo su voci che rifiuterebbe")
        s.add_argument("--recenti-min", type=int, default=120,
                       help="a coda illeggibile, sveglia solo per il materiale pronto da meno di N minuti")
        s.add_argument("--pausa-min", type=int, default=20,
                       help="a coda illeggibile, non richiamare se il repository social è partito da meno di N minuti")
        s.add_argument("--attesa-max-min", type=int, default=90,
                       help="segnala le voci in coda che maturano entro N minuti")
        if nome == "attendi":
            s.add_argument("--max-min", type=int, default=100, help="durata massima dell'attesa")

    c = sub.add_parser("controlla", help="controllo di salute: articoli rimasti indietro")
    c.add_argument("--ore", type=float, default=48)
    c.add_argument("--tolleranza-min", type=int, default=180)

    args = p.parse_args()
    return {"mancanti": cmd_mancanti, "sveglia": cmd_sveglia, "attendi": cmd_attendi,
            "controlla": cmd_controlla}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
