#!/usr/bin/env python3
"""rassegna-da-fare.py — punto 0 della routine «Rassegna normativa e albo pretorio»: in questo giro c'è lavoro?
Solo lettura (API REST di GitHub con `gh api` o GITHUB_TOKEN, più il JSON di normativa-watcher.py): uscita 0 = niente da fare, 10 = lavoro da fare con l'elenco, 2 = non ha potuto controllare (si fa il giro intero).

Che cosa conta come lavoro (dall'11/11/2026, per non far leggere a ogni giro decine di file quando non c'è niente):
  1. voci nuove nel JSON di normativa-watcher.py che non compaiono in nessuna issue `normativa-watcher`
     (corpo o commenti, ultimi 21 giorni): il dedup si rifà qui con l'API REST, perché quello dello script
     usa `gh issue list`, che nelle sessioni cloud non funziona;
  2. fonti primarie in errore (campo `errori`): un albo che non risponde può nascondere un atto;
     fonti della rassegna stampa in errore (`errori_news`) solo se non c'è già aperta la issue
     «⚠️ Normativa watcher: … rassegna stampa …», che è lavoro della routine dei guasti;
  3. issue `normativa-watcher` aperte (escluse quelle «⚠️», dei guasti), salvo quelle «in sospeso»: l'ultimo
     commento è dell'account e porta il segno `<!-- rassegna: in sospeso -->` (PR del punto 3-ter in attesa
     dell'utente, atto «In attesa» già cercato). Anche una issue in sospeso torna lavoro se una PR citata nel
     commento è stata unita o chiusa, o, per le issue «In attesa», se l'ultimo controllo ha più di 20 ore;
  4. comunicati (punto 6-bis): articoli fra i candidati di check-comunicati.py andati online o modificati dopo
     l'ultimo segno della rassegna, o rinviati dall'ultimo giro (`<!-- comunicato-rinviato: <slug> -->`);
     senza un segno negli ultimi tre giorni, tutti i candidati.

Uso (dalla cartella del repository):
  python3 scripts/normativa-watcher.py --days 2 --fonti tutte --out /tmp/novita.json --issue-body /tmp/issue.md
  python3 scripts/rassegna-da-fare.py --novita /tmp/novita.json            # decide
  python3 scripts/rassegna-da-fare.py --novita /tmp/novita.json --segna    # se esce 0, scrive anche il commento-segno
  python3 scripts/rassegna-da-fare.py --prova                              # prove senza rete
Con `--segna` il commento va sulla issue «Rassegna normativa e albo pretorio — …» più recente, aperta o chiusa:
è il segno che la riserva automatica di assistente-personale cerca dopo ogni giro.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
REPO = os.environ.get("GITHUB_REPOSITORY") or "SviluppoItaliaDigitale/sito-pc-genzano"
ACCOUNT = "SviluppoItaliaDigitale"
ROMA = dt.timezone(dt.timedelta(hours=1))  # solo per stampare; i confronti sono in UTC

SEGNO_SOSPESO = "<!-- rassegna: in sospeso -->"
SEGNO_VUOTO = "<!-- rassegna: giro senza lavoro -->"
RE_RINVIATO = re.compile(r"<!--\s*comunicato-rinviato:\s*([a-z0-9-]+)\s*-->")
RE_URL = re.compile(r"https?://[^\s)\]>\"'<]+")
RE_PR = re.compile(r"(?:/pull/|#)(\d{3,6})\b")
RE_CHIUSURA = re.compile(r"^\W*(chius[aoe]\s+(come|perch[eé])\s+)?(duplicat|superat)", re.I)
ESITO_VUOTO, ESITO_LAVORO, ESITO_ERRORE = 0, 10, 2
ORE_ATTESA = 20


# ---------------------------------------------------------------- API REST di GitHub

class ErroreAPI(RuntimeError):
    pass


def api(percorso: str, metodo: str = "GET", dati: dict | None = None):
    """Una chiamata REST: `gh api` se c'è (nelle sessioni GraphQL è vietato, REST no), altrimenti GITHUB_TOKEN."""
    if shutil.which("gh"):
        cmd = ["gh", "api", "-X", metodo, percorso]
        entrata = None
        if dati is not None:
            cmd += ["--input", "-"]
            entrata = json.dumps(dati)
        r = subprocess.run(cmd, input=entrata, capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            raise ErroreAPI(f"gh api {percorso}: {(r.stderr or r.stdout).strip()[:300]}")
        return json.loads(r.stdout or "null")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise ErroreAPI("né gh né GITHUB_TOKEN: non si può leggere GitHub")
    req = urllib.request.Request(
        f"https://api.github.com/{percorso.lstrip('/')}", method=metodo,
        data=json.dumps(dati).encode() if dati is not None else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "User-Agent": "rassegna-da-fare"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read() or b"null")
    except Exception as e:  # noqa: BLE001
        raise ErroreAPI(f"{percorso}: {e}") from e


def pagine(percorso: str, massimo: int = 5) -> list:
    sep = "&" if "?" in percorso else "?"
    tutto = []
    for n in range(1, massimo + 1):
        blocco = api(f"{percorso}{sep}per_page=100&page={n}")
        tutto += blocco
        if len(blocco) < 100:
            break
    return tutto


def ora_utc(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def titolo_rassegna(t: str) -> bool:
    t = (t or "").strip()
    return t.lower().startswith("rassegna") or t.startswith("Novità normative PC")


# ---------------------------------------------------------------- lettura dello stato

def leggi_stato(adesso: dt.datetime) -> dict:
    """Issue della rassegna (21 giorni), commenti, ultimo segno, PR citate. Tutto in sola lettura."""
    da = (adesso - dt.timedelta(days=21)).strftime("%Y-%m-%dT%H:%M:%SZ")
    issues = [i for i in pagine(f"repos/{REPO}/issues?labels=normativa-watcher&state=all&since={da}")
              if "pull_request" not in i]
    commenti = pagine(f"repos/{REPO}/issues/comments?sort=created&direction=asc&since={da}", massimo=10)
    per_numero = {i["number"]: i for i in issues}
    commenti_per_issue: dict[int, list] = {}
    for c in commenti:
        n = int(c["issue_url"].rsplit("/", 1)[1])
        if n in per_numero:
            commenti_per_issue.setdefault(n, []).append(c)
    return {"issues": issues, "commenti": commenti_per_issue}


def ultimo_segno(stato: dict, adesso: dt.datetime) -> tuple[dt.datetime | None, str]:
    """Ultimo segno dell'account sulle issue della rassegna (stesse regole della riserva automatica)."""
    migliore, corpo = None, ""
    limite = adesso - dt.timedelta(days=3)
    for i in stato["issues"]:
        if not titolo_rassegna(i["title"]):
            continue
        if i["user"]["login"] == ACCOUNT and "<!-- riserva" not in (i.get("body") or ""):
            t = ora_utc(i["created_at"])
            if t >= limite and (migliore is None or t > migliore):
                migliore, corpo = t, i.get("body") or ""
        for c in stato["commenti"].get(i["number"], []):
            testo = c.get("body") or ""
            if c["user"]["login"] != ACCOUNT or "<!-- riserva" in testo or RE_CHIUSURA.match(testo):
                continue
            t = ora_utc(c["created_at"])
            if t >= limite and (migliore is None or t > migliore):
                migliore, corpo = t, testo
    return migliore, corpo


def url_gia_visti(stato: dict) -> set[str]:
    visti = set()
    for i in stato["issues"]:
        visti.update(RE_URL.findall(i.get("body") or ""))
        for c in stato["commenti"].get(i["number"], []):
            visti.update(RE_URL.findall(c.get("body") or ""))
    return {u.rstrip(".,;:") for u in visti}


def stato_pr(numero: int) -> str:
    pr = api(f"repos/{REPO}/pulls/{numero}")
    if pr.get("merged_at"):
        return "unita"
    return pr.get("state") or "?"


# ---------------------------------------------------------------- comunicati (punto 6-bis)

def candidati_comunicato() -> list[tuple[str, dt.datetime, str]]:
    """Stesso elenco di `check-comunicati.py --candidati`: (slug, online dal, titolo)."""
    sys.path.insert(0, str(RADICE / "scripts"))
    import social_comune as sc
    spec = importlib.util.spec_from_file_location("check_comunicati", RADICE / "scripts" / "check-comunicati.py")
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)
    gia = set()
    for p in cc.CARTELLA.glob("*.md"):
        if p.name == "_index.md":
            continue
        try:
            fm, _ = cc.leggi(p)
        except Exception:  # noqa: BLE001
            continue
        slug = str(fm.get("articolo") or "").strip("/").split("/")[-1]
        if slug:
            gia.add(slug)
    out = []
    for p, fm, d in sc.articoli(finestra_ore=48):
        badge = sc.testo_campo(fm, "badge")
        if (sc.testo_campo(fm, "archiviato").lower() == "true" or badge in ("Allerta", "Emergenza")
                or p.stem in gia):
            continue
        out.append((p.stem, d, sc.testo_campo(fm, "title")))
    return out


def modificato_dopo(slug: str, quando: dt.datetime) -> bool:
    r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", f"content/comunicazioni/{slug}.md"],
                       cwd=RADICE, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return True  # non si sa: meglio valutarlo
    return dt.datetime.fromisoformat(r.stdout.strip()) > quando


# ---------------------------------------------------------------- decisione

def decidi(novita: dict, stato: dict, adesso: dt.datetime, candidati: list, segno: tuple,
           pr_di=stato_pr, modificato=modificato_dopo) -> list[str]:
    """Elenco delle cose da fare in questo giro; vuoto = niente da fare."""
    lavoro: list[str] = []
    visti = url_gia_visti(stato)
    nuove = [v for v in novita.get("novita", []) if v.get("link", "").rstrip(".,;:") not in visti]
    for v in nuove:
        luogo = " (territorio)" if v.get("locale") else ""
        lavoro.append(f"voce nuova{luogo}: {v.get('fonte')} — {str(v.get('titolo'))[:90]} {v.get('link')}")
    for e in novita.get("errori", []):
        lavoro.append(f"fonte primaria in errore (leggerla a mano): {e}")
    aperte = [i for i in stato["issues"] if i["state"] == "open"]
    guasto_stampa = any(i["title"].startswith("⚠️") and "rassegna stampa" in i["title"] for i in aperte)
    if novita.get("errori_news") and not guasto_stampa:
        for e in novita["errori_news"]:
            lavoro.append(f"fonte della rassegna stampa in errore, senza issue dei guasti aperta: {e[:160]}")
    for i in aperte:
        if i["title"].startswith("⚠️"):
            continue  # guasti: li ripara la routine delle 14:07
        commenti = stato["commenti"].get(i["number"], [])
        ultimo = commenti[-1] if commenti else None
        sospesa = bool(ultimo and ultimo["user"]["login"] == ACCOUNT and SEGNO_SOSPESO in (ultimo.get("body") or ""))
        if not sospesa:
            lavoro.append(f"issue aperta da lavorare: #{i['number']} {i['title']}")
            continue
        corpo = ultimo.get("body") or ""
        for n in sorted({int(x) for x in RE_PR.findall(corpo)}):
            try:
                st = pr_di(n)
            except ErroreAPI:
                continue  # un numero che non è una PR (o un'issue citata) non è lavoro
            if st in ("unita", "closed"):
                lavoro.append(f"issue in sospeso #{i['number']}: la PR #{n} risulta {st}, va chiusa o ripresa")
        if i["title"].startswith("In attesa") and adesso - ora_utc(ultimo["created_at"]) > dt.timedelta(hours=ORE_ATTESA):
            lavoro.append(f"issue «In attesa» #{i['number']}: ultimo controllo dell'albo oltre {ORE_ATTESA} ore fa")
    quando, corpo_segno = segno
    rinviati = set(RE_RINVIATO.findall(corpo_segno or ""))
    for slug, online, titolo in candidati:
        if quando is None:
            motivo = "nessun segno della rassegna negli ultimi tre giorni"
        elif slug in rinviati:
            motivo = "rinviato dal giro precedente"
        elif online > quando:
            motivo = "online dopo l'ultimo giro"
        elif modificato(slug, quando):
            motivo = "modificato dopo l'ultimo giro"
        else:
            continue
        lavoro.append(f"comunicato da decidere ({motivo}): {slug} — {titolo}")
    return lavoro


def issue_del_segno(stato: dict) -> dict | None:
    """La issue «Rassegna normativa e albo pretorio — …» più recente, aperta o chiusa (titolo che la riserva conta)."""
    cand = [i for i in stato["issues"] if i["title"].startswith("Rassegna normativa e albo pretorio")]
    if not cand:
        cand = [i for i in stato["issues"] if titolo_rassegna(i["title"])]
    return max(cand, key=lambda i: i["created_at"]) if cand else None


def testo_segno(novita: dict, adesso: dt.datetime) -> str:
    ora_it = adesso.astimezone(ROMA_ZONA()).strftime("%d/%m/%Y alle %H:%M")
    fonti = ", ".join(novita.get("fonti_lette", [])) or "nessuna"
    return (f"Giro della rassegna del {ora_it}: nessun lavoro. Nessuna voce nuova rispetto alle issue della "
            f"rassegna, nessuna fonte primaria in errore, nessuna issue aperta da lavorare, nessun articolo nuovo "
            f"da valutare per un comunicato. Fonti lette: {fonti}. Voci trovate dallo script, tutte già "
            f"nelle issue: {novita.get('totale', 0)}.\n\n{SEGNO_VUOTO}")


def ROMA_ZONA():
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo("Europe/Rome")
    except Exception:  # noqa: BLE001
        return ROMA


# ---------------------------------------------------------------- prove senza rete

def prova() -> int:
    t = lambda s: ora_utc(s)  # noqa: E731
    adesso = t("2026-11-11T11:55:00Z")
    issue = lambda n, tit, stato="closed", autore="github-actions[bot]", corpo="": {  # noqa: E731
        "number": n, "title": tit, "state": stato, "user": {"login": autore}, "created_at": "2026-11-11T06:55:00Z",
        "body": corpo}
    comm = lambda testo, quando="2026-11-11T07:10:00Z", autore=ACCOUNT: {  # noqa: E731
        "user": {"login": autore}, "body": testo, "created_at": quando}
    base = {"issues": [issue(1, "Rassegna normativa e albo pretorio — 11/11/2026 (1 atti, 0 diretti)",
                             corpo="[a](https://ex.it/atto1)")],
            "commenti": {1: [comm("Giro: atto1 scartato, https://ex.it/atto1")]}}
    vuoto = {"novita": [{"link": "https://ex.it/atto1", "fonte": "Albo", "titolo": "x"}], "errori": [], "errori_news": []}
    segno = ultimo_segno(base, adesso)
    casi = []
    casi.append(("niente di nuovo", decidi(vuoto, base, adesso, [], segno) == []))
    nuovo = dict(vuoto, novita=vuoto["novita"] + [{"link": "https://ex.it/atto2", "fonte": "Albo", "titolo": "y"}])
    casi.append(("voce nuova", len(decidi(nuovo, base, adesso, [], segno)) == 1))
    casi.append(("fonte primaria in errore", len(decidi(dict(vuoto, errori=["Albo: 500"]), base, adesso, [], segno)) == 1))
    stampa = dict(vuoto, errori_news=["Il Mamilio: 404"])
    casi.append(("stampa in errore senza issue", len(decidi(stampa, base, adesso, [], segno)) == 1))
    con_guasto = {"issues": base["issues"] + [issue(2, "⚠️ Normativa watcher: una o più fonti della rassegna stampa non rispondono", "open")],
                  "commenti": base["commenti"]}
    casi.append(("stampa in errore con issue dei guasti", decidi(stampa, con_guasto, adesso, [], segno) == []))
    aperta = {"issues": base["issues"] + [issue(3, "Novità normative PC — settimana", "open")], "commenti": base["commenti"]}
    casi.append(("issue aperta", len(decidi(vuoto, aperta, adesso, [], segno)) == 1))
    sospesa = {"issues": base["issues"] + [issue(4, "Rassegna normativa e albo pretorio — 10/11", "open")],
               "commenti": {**base["commenti"], 4: [comm(f"PR #1234 in attesa dell'OK. {SEGNO_SOSPESO}")]}}
    casi.append(("sospesa con PR aperta", decidi(vuoto, sospesa, adesso, [], segno, pr_di=lambda n: "open") == []))
    casi.append(("sospesa con PR unita", len(decidi(vuoto, sospesa, adesso, [], segno, pr_di=lambda n: "unita")) == 1))
    attesa = {"issues": base["issues"] + [issue(5, "In attesa: delibera n. 189", "open", ACCOUNT)],
              "commenti": {**base["commenti"], 5: [comm(f"Albo controllato. {SEGNO_SOSPESO}", "2026-11-10T06:00:00Z")]}}
    casi.append(("in attesa controllata oltre 20 ore", len(decidi(vuoto, attesa, adesso, [], segno)) == 1))
    vecchio = t("2026-11-10T20:00:00Z")
    recente = t("2026-11-11T09:00:00Z")
    casi.append(("comunicato già deciso", decidi(vuoto, base, adesso, [("a", vecchio, "A")], segno,
                                                 modificato=lambda s, q: False) == []))
    casi.append(("comunicato nuovo", len(decidi(vuoto, base, adesso, [("b", recente, "B")], segno,
                                                modificato=lambda s, q: False)) == 1))
    rinvio = {"issues": base["issues"],
              "commenti": {1: [comm("Giro: comunicato su a. <!-- comunicato-rinviato: c -->")]}}
    casi.append(("comunicato rinviato", len(decidi(vuoto, rinvio, adesso, [("c", vecchio, "C")],
                                                   ultimo_segno(rinvio, adesso), modificato=lambda s, q: False)) == 1))
    casi.append(("senza segno, ogni candidato", len(decidi(dict(vuoto, novita=[]), {"issues": [], "commenti": {}}, adesso,
                                                           [("a", vecchio, "A")], (None, ""))) == 1))
    casi.append(("chiusura come duplicato non è un segno",
                 ultimo_segno({"issues": base["issues"], "commenti": {1: [comm("Chiusa come duplicato di #2")]}},
                              adesso)[0] is None))
    casi.append(("segno sulla issue della rassegna", (issue_del_segno(base) or {}).get("number") == 1))
    sbagliati = [nome for nome, ok in casi if not ok]
    for nome, ok in casi:
        print(f"{'ok ' if ok else 'NO '} {nome}")
    if sbagliati:
        print(f"Prove fallite: {', '.join(sbagliati)}")
        return 1
    print(f"OK: {len(casi)} prove, nessuna richiesta esterna.")
    return 0


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--novita", help="JSON di normativa-watcher.py (--out)")
    ap.add_argument("--segna", action="store_true", help="se non c'è lavoro, scrive il commento-segno sulla issue")
    ap.add_argument("--prova", action="store_true", help="prove senza rete")
    a = ap.parse_args()
    if a.prova:
        return prova()
    if not a.novita:
        print("Serve --novita (il JSON di normativa-watcher.py): senza, non si sa se ci sono voci nuove.")
        return ESITO_ERRORE
    adesso = dt.datetime.now(dt.timezone.utc)
    try:
        novita = json.loads(Path(a.novita).read_text(encoding="utf-8"))
        stato = leggi_stato(adesso)
        segno = ultimo_segno(stato, adesso)
        candidati = candidati_comunicato()
        lavoro = decidi(novita, stato, adesso, candidati, segno)
    except (OSError, ValueError, ErroreAPI) as e:
        print(f"Controllo non riuscito ({e}): fai il giro intero.")
        return ESITO_ERRORE
    quando = segno[0].astimezone(ROMA_ZONA()).strftime("%d/%m %H:%M") if segno[0] else "nessuno negli ultimi 3 giorni"
    print(f"Ultimo segno della rassegna: {quando}. Candidati comunicato nelle 48 ore: {len(candidati)}.")
    if lavoro:
        print(f"\nLAVORO DA FARE ({len(lavoro)}): continua dal punto 1.")
        for riga in lavoro:
            print(f"- {riga}")
        return ESITO_LAVORO
    issue = issue_del_segno(stato)
    testo = testo_segno(novita, adesso)
    if not issue:
        print("Niente da fare, ma nessuna issue «Rassegna …» su cui lasciare il segno: crea la issue del giro "
              "con il corpo di /tmp/issue.md e commentala con il testo qui sotto.")
        print("\n" + testo)
        return ESITO_LAVORO
    print(f"\nNIENTE DA FARE. Segno da lasciare su #{issue['number']} «{issue['title']}»:\n\n{testo}")
    if a.segna:
        try:
            c = api(f"repos/{REPO}/issues/{issue['number']}/comments", "POST", {"body": testo})
        except ErroreAPI as e:
            print(f"\nCommento non scritto ({e}): scrivilo tu con i tool GitHub.")
            return ESITO_ERRORE
        print(f"\nSegno scritto: {c.get('html_url')}")
    return ESITO_VUOTO


if __name__ == "__main__":
    sys.exit(main())
