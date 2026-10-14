#!/usr/bin/env python3
"""
Controllo delle «mappe raccontate»: ogni scheda del cruscotto ha la sua
spiegazione a parole, sotto la scheda e nella pagina che le raccoglie tutte.

Confronta tre posti che devono dire la stessa cosa:
  - content/cruscotto/_index.md: le schede (pulsanti role="tab" e pannelli
    id="panel-<id>"), ognuna con {{< mappa-raccontata id="<id>" >}} dentro il
    proprio pannello;
  - data/mappe_raccontate.yaml: una voce per scheda, con titolo uguale
    all'etichetta del pulsante e tutti i campi compilati (titolo, in_breve,
    mostra, colori, aggiornamento, limiti, fonte);
  - content/cruscotto/mappe-raccontate.md: per ogni scheda, nell'ordine dei
    pulsanti, il titolo «## <titolo> {#scheda-<id>}» seguito dallo shortcode
    con pagina="true".

Controlla la forma, non il contenuto: che le spiegazioni dicano il vero lo
verifica chi modifica una scheda, aggiornando la sua voce nella stessa
modifica (regola scritta in testa al file dati). Nasce il 14/10/2026 con la
proposta 64 della roadmap; gira su ogni pull request in validate-pr.yml.

Uso: python3 scripts/check-mappe-raccontate.py
Exit code 0 se tutto torna, 1 altrimenti. Python standard più PyYAML.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CRUSCOTTO = ROOT / "content" / "cruscotto" / "_index.md"
DATI = ROOT / "data" / "mappe_raccontate.yaml"
PAGINA = ROOT / "content" / "cruscotto" / "mappe-raccontate.md"

CAMPI_TESTO = ("titolo", "in_breve", "mostra", "aggiornamento", "fonte")
CAMPI_ELENCO = ("colori", "limiti")

RE_TAB = re.compile(r'<button[^>]*\bdata-panel="([a-z0-9-]+)"[^>]*\brole="tab"[^>]*>(.*?)</button>', re.S)
RE_PANNELLO = re.compile(r'<div class="cruscotto-panel" id="panel-([a-z0-9-]+)"[^>]*>(.*?)\n</div>', re.S)
RE_SHORTCODE = re.compile(r'\{\{<\s*mappa-raccontata\s+id="([a-z0-9-]+)"(\s+pagina="true")?\s*>\}\}')
RE_TITOLO = re.compile(r'^## (.+?) \{#scheda-([a-z0-9-]+)\}\s*$', re.M)


def etichetta(testo: str) -> str:
    """Testo visibile del pulsante, senza icona e senza spazi in più."""
    testo = re.sub(r"<[^>]+>", "", testo)
    return re.sub(r"\s+", " ", html.unescape(testo)).strip()


def main() -> int:
    errori: list[str] = []

    cruscotto = CRUSCOTTO.read_text(encoding="utf-8")
    schede = [(pid, etichetta(lab)) for pid, lab in RE_TAB.findall(cruscotto)]
    if not schede:
        print(f"::error::nessun pulsante di scheda trovato in {CRUSCOTTO.relative_to(ROOT)}")
        return 1
    ordine = [pid for pid, _ in schede]
    titoli_tab = dict(schede)

    # 1. ogni pannello contiene il proprio riquadro, una volta sola
    pannelli = dict(RE_PANNELLO.findall(cruscotto))
    for pid in ordine:
        corpo = pannelli.get(pid)
        if corpo is None:
            errori.append(f"cruscotto: il pulsante «{titoli_tab[pid]}» non ha il pannello id=\"panel-{pid}\"")
            continue
        trovati = [sid for sid, pag in RE_SHORTCODE.findall(corpo) if not pag]
        if trovati != [pid]:
            errori.append(
                f"cruscotto: nel pannello «{pid}» serve {{{{< mappa-raccontata id=\"{pid}\" >}}}} una volta sola "
                f"(trovato: {trovati or 'nessuno'})"
            )
    for pid in pannelli:
        if pid not in titoli_tab:
            errori.append(f"cruscotto: il pannello «{pid}» non ha un pulsante")

    # 2. il file dati ha una voce completa per ogni scheda, e nessuna in più
    try:
        dati = yaml.safe_load(DATI.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        print(f"::error::{DATI.relative_to(ROOT)} non è YAML valido: {e}")
        return 1
    voci = dati.get("schede") or {}
    for pid in ordine:
        voce = voci.get(pid)
        if not isinstance(voce, dict):
            errori.append(f"dati: manca la voce «{pid}» ({titoli_tab[pid]})")
            continue
        for campo in CAMPI_TESTO:
            if not isinstance(voce.get(campo), str) or not voce[campo].strip():
                errori.append(f"dati: «{pid}» senza il campo {campo}")
        for campo in CAMPI_ELENCO:
            v = voce.get(campo)
            if not isinstance(v, list) or not v or not all(isinstance(x, str) and x.strip() for x in v):
                errori.append(f"dati: «{pid}» senza l'elenco {campo} (almeno una voce di testo)")
        if isinstance(voce.get("titolo"), str) and voce["titolo"].strip() != titoli_tab[pid]:
            errori.append(
                f"dati: il titolo di «{pid}» è «{voce['titolo']}», il pulsante dice «{titoli_tab[pid]}»"
            )
    for pid in voci:
        if pid not in titoli_tab:
            errori.append(f"dati: la voce «{pid}» non corrisponde a nessuna scheda del cruscotto")

    # 3. la pagina che le raccoglie: stesso ordine, titolo giusto, shortcode subito sotto
    pagina = PAGINA.read_text(encoding="utf-8")
    titoli = RE_TITOLO.findall(pagina)
    if [sid for _, sid in titoli] != ordine:
        errori.append(
            "pagina: i titoli «## … {#scheda-<id>}» devono seguire l'ordine dei pulsanti: "
            f"atteso {ordine}, trovato {[sid for _, sid in titoli]}"
        )
    for testo, sid in titoli:
        if sid in titoli_tab and testo.strip() != titoli_tab[sid]:
            errori.append(f"pagina: il titolo di «{sid}» è «{testo}», il pulsante dice «{titoli_tab[sid]}»")
    blocchi = re.split(r"^## ", pagina, flags=re.M)
    for blocco in blocchi[1:]:
        m = re.match(r"(.+?) \{#scheda-([a-z0-9-]+)\}", blocco)
        if not m:
            continue
        sid = m.group(2)
        codici = RE_SHORTCODE.findall(blocco)
        if codici != [(sid, ' pagina="true"')]:
            errori.append(
                f"pagina: sotto il titolo di «{sid}» serve solo "
                f"{{{{< mappa-raccontata id=\"{sid}\" pagina=\"true\" >}}}}"
            )

    if errori:
        for e in errori:
            print(f"::error::{e}")
        print(f"\n{len(errori)} {'problema' if len(errori) == 1 else 'problemi'}. Vedi la regola in testa a {DATI.relative_to(ROOT)}.")
        return 1
    print(f"Mappe raccontate: {len(ordine)} schede, ognuna con voce, riquadro e titolo nella pagina.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
