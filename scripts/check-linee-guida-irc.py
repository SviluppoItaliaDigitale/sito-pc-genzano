#!/usr/bin/env python3
"""Controllo settimanale Linee Guida RCP 2025 (IRC) — solo stdlib.

Confronta i capitoli con PDF pubblicati sulla pagina ufficiale IRC
(https://www.ircouncil.it/linee-guida-rcp-2025/) con la tabella dei
PDF in content/formazione/primo-soccorso/_index.md e segnala:

  1. capitoli NUOVI pubblicati da IRC ma assenti dalla nostra tabella
     (IRC rilascia le traduzioni progressivamente: senza questo check
     i capitoli nuovi si scoprono per caso — richiesta utente 10/07/2026,
     capitolo 5 ALS scoperto così);
  2. capitoli presenti in entrambi ma con URL del PDF CAMBIATO
     (IRC ricarica i file con data nel nome, es. _13.04.2026.pdf);
  3. capitoli nella nostra tabella ma spariti dalla pagina IRC.

La riparazione è editoriale (aggiornare la tabella e la nota sui
capitoli attesi), mai automatica: NO INVENZIONI. I link morti sono
già coperti site-wide da check-links-sito.yml (lychee).

Output: report markdown su stdout. Exit code = numero di segnalazioni
(0 = tutto allineato). Eseguibile in locale:
    python3 scripts/check-linee-guida-irc.py
"""

import html
import re
import sys
import urllib.request

URL_IRC = "https://www.ircouncil.it/linee-guida-rcp-2025/"
PAGINA_NOSTRA = "content/formazione/primo-soccorso/_index.md"
UA = "Mozilla/5.0 (compatible; pc-genzano-check/1.0; +https://www.protezionecivilegenzano.it/)"


def scarica_pagina_irc():
    req = urllib.request.Request(URL_IRC, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def capitoli_irc(html_irc):
    """num -> (url_pdf, titolo). Match dei link ai PDF dei capitoli."""
    caps = {}
    # <a href="...pdf" ...>5_Advanced Life Support ...  (il numero è
    # l'inizio del testo del link, convenzione stabile della pagina IRC)
    for m in re.finditer(
        r'<a[^>]+href="(https://www\.ircouncil\.it/[^"]+\.pdf)"[^>]*>\s*(\d{1,2})_([^<]{0,90})',
        html_irc,
    ):
        url, num, titolo = m.group(1), int(m.group(2)), m.group(3)
        caps[num] = (url, html.unescape(titolo).strip().rstrip("( ").strip())
    return caps


def capitoli_nostri(md):
    """num -> url dalla tabella '| N | Titolo | Revisori | [Scarica (PDF)](url) |'."""
    caps = {}
    for m in re.finditer(
        r"^\|\s*(\d{1,2})\s*\|[^|]*\|[^|]*\|\s*\[[^\]]*\]\((https://www\.ircouncil\.it/[^)]+\.pdf)\)",
        md,
        re.M,
    ):
        caps[int(m.group(1))] = m.group(2)
    return caps


def main():
    segnalazioni = []

    try:
        html_irc = scarica_pagina_irc()
    except Exception as e:  # rete giù o pagina spostata: va comunque segnalato
        print("## Linee Guida RCP 2025 — pagina IRC non raggiungibile\n")
        print(f"- ❌ `{URL_IRC}` non risponde: `{e}`")
        print("- Se l'errore persiste su più settimane, IRC ha spostato la pagina:")
        print("  aggiornare `URL_IRC` in questo script e i link su")
        print(f"  `{PAGINA_NOSTRA}`.")
        return 1

    try:
        md = open(PAGINA_NOSTRA, encoding="utf-8").read()
    except OSError as e:
        print(f"- ❌ impossibile leggere `{PAGINA_NOSTRA}`: `{e}`")
        return 1

    irc = capitoli_irc(html_irc)
    nostri = capitoli_nostri(md)

    if not irc:
        segnalazioni.append(
            "❌ Nessun PDF di capitolo riconosciuto sulla pagina IRC: "
            "il markup della pagina è cambiato, aggiornare il parser "
            "(`capitoli_irc()` in `scripts/check-linee-guida-irc.py`)."
        )
    if not nostri:
        segnalazioni.append(
            f"❌ Nessuna riga-capitolo riconosciuta nella tabella di `{PAGINA_NOSTRA}`: "
            "la struttura della tabella è cambiata, aggiornare il parser."
        )

    for num in sorted(irc):
        url, titolo = irc[num]
        if num not in nostri:
            segnalazioni.append(
                f"🆕 **Capitolo {num} — {titolo}**: pubblicato da IRC ma assente "
                f"dalla nostra tabella. Aggiungere la riga (con i revisori indicati "
                f"sulla pagina IRC) e togliere il capitolo dalla nota \"in corso di "
                f"rilascio\". PDF: {url}"
            )
        elif nostri[num] != url:
            segnalazioni.append(
                f"🔄 **Capitolo {num}**: IRC ha cambiato il file del PDF.\n"
                f"   - nostro link: {nostri[num]}\n"
                f"   - link attuale IRC: {url}"
            )

    for num in sorted(set(nostri) - set(irc)):
        segnalazioni.append(
            f"⚠️ **Capitolo {num}**: presente nella nostra tabella ma non più "
            f"linkato dalla pagina IRC (ritirato o markup cambiato). Verificare."
        )

    print("## Linee Guida RCP 2025 — allineamento con la pagina IRC\n")
    print(f"- Pagina controllata: {URL_IRC}")
    print(f"- Capitoli con PDF su IRC: {sorted(irc) or '—'}")
    print(f"- Capitoli nella nostra tabella (`{PAGINA_NOSTRA}`): {sorted(nostri) or '—'}\n")

    if not segnalazioni:
        print("✅ Tabella allineata: nessun capitolo nuovo, nessun URL cambiato.")
        return 0

    for s in segnalazioni:
        print(f"- {s}")
    print(
        "\nDopo l'aggiornamento della tabella, ricontrollare anche le schede di "
        "`/formazione/primo-soccorso/` che citano i capitoli pertinenti."
    )
    return len(segnalazioni)


if __name__ == "__main__":
    sys.exit(main())
