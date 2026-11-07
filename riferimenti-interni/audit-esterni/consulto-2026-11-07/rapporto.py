#!/usr/bin/env python3
"""Rapporti dei revisori del consulto per l'audit del sito del 07/11/2026: ripulisce e controlla ogni risposta, poi prepara
il testo della PR (senza nomi di strumenti) e l'esito per la bacheca. Lo usa esegui.sh, solo per questo audit.

Uso: rapporto.py scrivi LETTERA RISPOSTA.json USCITA.md   scrive il rapporto e stampa una riga JSON con l'esito
     rapporto.py riepilogo CARTELLA e:zai h:openrouter …   legge gli esiti in CARTELLA, scrive corpo-pr.md ed esito-bacheca.md
     rapporto.py bacheca COORDINAMENTO.md ESITO.md          mette l'esito al posto del segno nella richiesta in bacheca
Uscite: 0 fatto; 1 nessun rapporto (o risposta illeggibile); 2 errore d'uso.
"""

import json
import pathlib
import re
import sys
import time

CAMPI = ["Dove", "Che cosa non va", "Prova", "Priorità", "Esito"]
# Nomi di strumenti, servizi e modelli che nel rapporto non devono comparire: si segnalano, li toglie chi verifica.
NOMI = re.compile(r"\b(claude|anthropic|chatgpt|openai|gpt-?\w*|gemini|deepseek|qwen|kimi|moonshot|glm[-\w.]*|zhipu|"
                  r"z\.ai|cohere|command[ -]a\w*|openrouter|cloudflare|workers ai|nemotron|nvidia|gemma|llama|mistral|"
                  r"modello linguistico|language model|llm|intelligenza artificiale)\b", re.I)
SEGNO = "<!-- esito-consulto-revisori -->"
NOMI_SERVIZI = {"gemini": "Gemini API", "zai": "Z.ai", "openrouter": "OpenRouter", "cloudflare": "Cloudflare Workers AI",
                "cohere": "Cohere"}


def pulisci(testo):
    testo = re.sub(r"<think>.*?</think>", "", testo, flags=re.S)       # ragionamento che alcuni modelli scrivono in chiaro
    if "</think>" in testo:
        testo = testo.split("</think>", 1)[1]
    testo = testo.strip()
    recinto = re.match(r"^```[\w-]*\n(.*)\n```$", testo, flags=re.S)  # rapporto chiuso in un blocco di codice
    return recinto[1].strip() if recinto else testo


def scrivi(lettera, risposta, uscita):
    lettera = lettera.upper()
    esito = {"lettera": lettera, "ok": False}
    try:
        dati = json.loads(pathlib.Path(risposta).read_text(encoding="utf-8"))
        testo = pulisci(dati.get("testo") or "")
    except (OSError, ValueError, AttributeError) as e:
        esito["motivo"] = f"risposta illeggibile ({e.__class__.__name__})"
        print(json.dumps(esito, ensure_ascii=False))
        return 1
    esito.update(modello=dati.get("modello", ""), servizio=dati.get("servizio", ""))
    if len(testo.split()) < 50:
        esito["motivo"] = "risposta vuota o troppo corta"
        print(json.dumps(esito, ensure_ascii=False))
        return 1

    titolo = f"# Audit completo del sito — revisore {lettera}"
    avvisi = []
    m = re.search(r"^#\s*Audit completo del sito.*$", testo, flags=re.M | re.I)
    if m:
        if testo[:m.start()].strip():
            avvisi.append("testo prima del titolo, tolto")
        testo = titolo + testo[m.end():]
    else:
        avvisi.append("titolo mancante, aggiunto")
        testo = titolo + "\n\n" + testo
    if testo.count("```") % 2 and re.search(r"\n```\s*$", testo):   # chiusura del blocco aperto prima del titolo
        testo = re.sub(r"\n```\s*$", "", testo)

    mancanti = [str(n) for n in range(1, 7) if not re.search(rf"^##\s*{n}\.", testo, flags=re.M)]
    blocchi = re.split(r"^(?=###\s*R\d+)", testo, flags=re.M)[1:]
    if blocchi:   # l'ultimo rilievo finisce dove comincia la sezione successiva
        blocchi[-1] = re.split(r"^##\s", blocchi[-1], maxsplit=1, flags=re.M)[0]
    incompleti = [re.match(r"###\s*(R\d+)", b)[1] for b in blocchi
                  if any(not re.search(rf"\*\*{re.escape(c)}:?\*\*", b) for c in CAMPI)]
    nomi = sorted({x.lower() for x in NOMI.findall(testo)})
    interrotto = "6" in mancanti or not re.search(r"[.!?)»\]*_`]\s*$", testo)

    pathlib.Path(uscita).write_text(testo.rstrip() + "\n", encoding="utf-8")
    esito.update(ok=True, file=str(uscita), parole=len(testo.split()), rilievi=len(blocchi), sezioni_mancanti=mancanti,
                 rilievi_incompleti=incompleti, nomi=nomi, interrotto=interrotto, avvisi=avvisi)
    print(json.dumps(esito, ensure_ascii=False))
    return 0


def motivo_breve(testo):
    """Il motivo di una mancata risposta, corto e senza nulla che somigli a una chiave."""
    testo = re.sub(r"[A-Za-z0-9_\-]{32,}", "[…]", " ".join(testo.split()))
    return (testo[:220] + "…") if len(testo) > 220 else (testo or "nessun messaggio")


def avvisi_di(e):
    pezzi = []
    if e.get("sezioni_mancanti"):
        pezzi.append("sezioni mancanti: " + ", ".join(e["sezioni_mancanti"]))
    if e.get("rilievi_incompleti"):
        pezzi.append("rilievi senza tutte le righe: " + ", ".join(e["rilievi_incompleti"]))
    if e.get("nomi"):
        n = len(e["nomi"])
        pezzi.append("1 nome di strumento da togliere" if n == 1 else f"{n} nomi di strumenti da togliere")
    if e.get("interrotto"):
        pezzi.append("forse interrotto")
    pezzi += e.get("avvisi") or []
    return pezzi


def quanti(n, uno, tanti):
    return f"{n} {uno if n == 1 else tanti}"


def riepilogo(cartella, coppie):
    cartella = pathlib.Path(cartella)
    righe_pr, righe_bacheca, file_fatti = [], [], []
    for coppia in coppie:
        lettera, _, sigla = coppia.partition(":")
        L = lettera.upper()
        esito = {}
        p = cartella / f"{lettera}.esito"
        if p.exists():
            try:
                esito = json.loads(p.read_text(encoding="utf-8").strip() or "{}")
            except ValueError:
                esito = {}
        if esito.get("ok"):
            file_fatti.append(esito["file"])
            extra = avvisi_di(esito)
            numeri = f"{quanti(esito['parole'], 'parola', 'parole')}, {quanti(esito['rilievi'], 'rilievo', 'rilievi')}"
            righe_pr.append(f"- Revisore {L}: rapporto di {numeri}"
                            + (f" ({'; '.join(extra)})." if extra else "."))
            righe_bacheca.append(f"{L} {NOMI_SERVIZI.get(sigla, sigla)} ({esito.get('modello') or 'modello non indicato'}):"
                                 f" {numeri}"
                                 + (f", {'; '.join(extra)}" if extra else ""))
        else:
            q = cartella / f"{lettera}.motivo"   # lo scrive esegui.sh quando il servizio non risponde
            grezzo = q.read_text(encoding="utf-8", errors="replace") if q.exists() else ""
            motivo = esito.get("motivo") or motivo_breve(grezzo)
            righe_pr.append(f"- Revisore {L}: nessun rapporto.")
            righe_bacheca.append(f"{L} {NOMI_SERVIZI.get(sigla, sigla)}: nessun rapporto ({motivo})")
    ora = time.strftime("%d/%m/%Y, %H:%M")
    corpo = (
        "Rapporti dell'audit completo del sito del 07/11/2026 scritti dai revisori del consulto. Ognuno ha lavorato da solo "
        "sul fascicolo pubblico del sito (`riferimenti-interni/audit-esterni/consulto-2026-11-07/fascicolo.md`), con la "
        "richiesta `richiesta.md` della stessa cartella, senza aprire il sito.\n\n" + "\n".join(righe_pr) + "\n\n"
        "Ogni rilievo porta «Esito: da verificare». Prima di unire si verifica ogni rilievo sul sito pubblicato e sul "
        "repository e si scrive l'esito accanto; i nomi di strumenti segnalati si tolgono. La PR resta in bozza finché la "
        "verifica non è fatta.\n")
    (cartella / "corpo-pr.md").write_text(corpo, encoding="utf-8")
    (cartella / "esito-bacheca.md").write_text(
        f"- **Esito ({ora}, sul PC).** " + "; ".join(righe_bacheca)
        + f". Rapporti sul ramo `claude/audit-consulto-revisori-20261107`, PR in bozza: Claude verifica ogni rilievo, "
          "scrive l'esito accanto e unisce.\n", encoding="utf-8")
    (cartella / "file-fatti.txt").write_text("".join(f + "\n" for f in file_fatti), encoding="utf-8")
    print("\n".join(righe_bacheca))
    return 0 if file_fatti else 1


def bacheca(coordinamento, esito_file):
    p = pathlib.Path(coordinamento)
    testo = p.read_text(encoding="utf-8")
    esito = pathlib.Path(esito_file).read_text(encoding="utf-8").strip()
    riga = next((r for r in testo.splitlines() if r.strip() == SEGNO), None)
    if riga is None:
        print("Segno dell'esito non trovato nella bacheca: l'esito va scritto a mano.")
        return 1
    rientro = riga[:len(riga) - len(riga.lstrip())]
    p.write_text(testo.replace(riga, f"{rientro}{esito}\n{riga}", 1), encoding="utf-8")
    return 0


def main(argv):
    if len(argv) >= 1 and argv[0] == "scrivi" and len(argv) == 4:
        return scrivi(*argv[1:])
    if len(argv) >= 3 and argv[0] == "riepilogo":
        return riepilogo(argv[1], argv[2:])
    if len(argv) == 3 and argv[0] == "bacheca":
        return bacheca(argv[1], argv[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
