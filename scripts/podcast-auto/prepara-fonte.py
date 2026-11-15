#!/usr/bin/env python3
"""prepara-fonte.py — Prepara la fonte unica e le istruzioni per una puntata.

Prende la prima puntata «da-fare» di coda.yaml (o quella indicata) e scrive in
~/podcast-lavoro/<id>/ il file fonte.md (testo delle pagine verificate del
sito, senza frontmatter né shortcode) e istruzioni.txt, da incollare nella
personalizzazione della panoramica audio. Uso: prepara-fonte.py [ID]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parents[2]
CODA = Path(__file__).with_name("coda.yaml")
LAVORO = Path.home() / "podcast-lavoro"

ISTRUZIONI = """Episodio breve per i cittadini di Genzano di Roma e dei Castelli Romani sul tema: {titolo}. Il cuore della puntata sono i comportamenti di autoprotezione che le fonti indicano, detti in modo semplice. Regole obbligatorie, da rispettare frase per frase: usa SOLO le informazioni delle fonti, quasi con le loro parole. Non spiegare perché succede una cosa, non dare cause, meccanismi fisici o tecnici, analogie o metafore che le fonti non contengono. Non trarre conclusioni o morali dagli esempi storici e non attribuire a un evento conseguenze che la fonte non dice: racconta un esempio solo come lo racconta la fonte, oppure non raccontarlo. Non aggiungere numeri, date, nomi, norme, numeri di telefono (l'unico numero da dire è il 112), consigli o motivazioni che le fonti non contengono; se una fonte mette una cautela (per esempio "se sai farlo in sicurezza"), ripetila. Non rendere più gravi i fatti: niente superlativi ("il più letale", "per nessun motivo"), niente "sempre", "mai", "certo", "garantito" se le fonti non usano quella parola. Non parlare di documenti, manuali, fonti, linee guida o materiali letti: parla direttamente ("la Protezione Civile consiglia di..."). Non usare nomi propri per presentarvi e non citare programmi, applicazioni, intelligenza artificiale o lo strumento con cui è fatto l'audio. Apri dicendo che è il podcast del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma; chiudi invitando a leggere le pagine sul sito protezionecivilegenzano.it. Il numero di emergenza si pronuncia "uno, uno, due". Il Gruppo comunale non si chiama direttamente: in emergenza si chiama il 112. Non parlare dell'allerta o della situazione di oggi. Tono calmo, concreto, rassicurante ma non minimizzante, senza battute sulle emergenze."""


def pulisci(testo: str) -> str:
    testo = re.sub(r"\A---\n.*?\n---\n", "", testo, flags=re.S)
    testo = re.sub(r"\{\{[<%].*?[>%]\}\}", "", testo, flags=re.S)
    testo = re.sub(r"<[^>]+>", "", testo)
    testo = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", testo)
    testo = re.sub(r"\n{3,}", "\n\n", testo)
    return testo.strip()


def main() -> int:
    coda = yaml.safe_load(CODA.read_text(encoding="utf-8"))["puntate"]
    if len(sys.argv) > 1:
        voci = [v for v in coda if v["id"] == sys.argv[1]]
    else:
        voci = [v for v in coda if v.get("stato") == "da-fare"][:1]
    if not voci:
        print("Nessuna puntata da fare in coda.")
        return 2
    voce = voci[0]
    dest = LAVORO / voce["id"]
    dest.mkdir(parents=True, exist_ok=True)
    parti = [f"# {voce['titolo']}\n\nFonte: pagine del sito del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma (protezionecivilegenzano.it).\n"]
    for rel in voce["fonti"]:
        p = RADICE / rel
        if not p.exists():
            print(f"ERRORE: fonte mancante {rel}", file=sys.stderr)
            return 1
        parti.append(pulisci(p.read_text(encoding="utf-8")))
    (dest / "fonte.md").write_text("\n\n".join(parti) + "\n", encoding="utf-8")
    (dest / "istruzioni.txt").write_text(ISTRUZIONI.format(titolo=voce["titolo"]), encoding="utf-8")
    print(f"ID={voce['id']}")
    print(f"CARTELLA={dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
