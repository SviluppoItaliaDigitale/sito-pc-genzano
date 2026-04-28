#!/usr/bin/env python3
"""Hash robusto del testo visibile di una pagina HTML.

Usato dal workflow `aggiorna-manuale.yml` per monitorare le fonti AGID /
Designers Italia / Bootstrap Italia. Calcola un SHA-256 del solo testo
visibile (e del solo `<main>` se presente), ignorando JS, CSS, header,
nav, footer, cookie banner, attributi `nonce`, ecc.

Risultato: gli hash sono stabili nel tempo e cambiano solo quando i
contenuti reali cambiano. Le modifiche cosmetiche (CSS rotativo, banner
cookie, timestamp di build, token CSRF) non scattano più.

Uso:
    python3 scripts/hash-fonte-agid.py <url>
    cat pagina.html | python3 scripts/hash-fonte-agid.py -

Stampa l'hash su stdout (40 caratteri esadecimali, prima parte di SHA-256).
Exit code:
    0 = hash calcolato
    2 = errore di rete o parsing
"""
import hashlib
import re
import sys
import urllib.request

from bs4 import BeautifulSoup

# Tag da rimuovere prima di estrarre il testo: contengono materiale che
# cambia spesso ma non riguarda i contenuti veri della pagina.
TAG_DA_RIMUOVERE = [
    "script",       # JS, sempre con bundler hash che cambia
    "style",        # CSS inline
    "noscript",     # contenuto fallback, raramente significativo
    "svg",          # icone con possibili id auto-generati
    "iframe",       # contenuti embed esterni
    "link",         # preload con hash, fingerprint asset
    "meta",         # CSRF, generator, OG tags volatili
]

# Selettori CSS dei "blocchi cornice" da escludere se presenti: header,
# nav, footer, cookie banner, side menu del sito che fa da ambiente
# uguale a tutte le pagine (cambia centralmente, non riguarda il
# contenuto specifico della pagina).
SELETTORI_CORNICE = [
    "header",
    "nav",
    "footer",
    "[role=banner]",
    "[role=contentinfo]",
    "[role=navigation]",
    ".cookie-bar",
    ".cookiebar",
    "#cookieConsent",
    "#consenso-cookie",
    ".announcement-bar",
    ".skip-link",
]

# Pattern di "rumore" testuale che capita ancora dopo il parsing:
# - timestamp ISO completi
# - hash esadecimali lunghi (token CSRF, fingerprint asset)
# - numeri >= 8 cifre (epoch, build ID)
PATTERN_RUMORE = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[Z+\-:0-9.]*\b"),
    re.compile(r"\b[a-f0-9]{16,}\b"),
    re.compile(r"\b\d{8,}\b"),
]


def estrai_testo_normalizzato(html: str) -> str:
    """Estrae il testo significativo della pagina, normalizzato.

    Strategia: usa <main> se esiste, altrimenti <body>. Rimuove i tag
    rumorosi e i blocchi cornice. Estrae il testo, normalizza spazi e
    pulisce i pattern volatili residui.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Rimuovi tag rumorosi
    for tag in TAG_DA_RIMUOVERE:
        for t in soup.find_all(tag):
            t.decompose()

    # Rimuovi blocchi cornice
    for selector in SELETTORI_CORNICE:
        for t in soup.select(selector):
            t.decompose()

    # Punto di partenza: <main>, fallback <body>, fallback radice
    radice = soup.find("main") or soup.find("body") or soup

    testo = radice.get_text(separator=" ", strip=True)

    # Normalizza: collassa spazi multipli, rimuovi pattern volatili
    testo = re.sub(r"\s+", " ", testo)
    for p in PATTERN_RUMORE:
        testo = p.sub("", testo)
    testo = re.sub(r"\s+", " ", testo).strip()

    return testo


def scarica(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; PCGenzanoBot/1.0; "
                "+https://www.protezionecivilegenzano.it/)"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
    # AGID usa utf-8; tolleranti su errori di encoding
    return body.decode("utf-8", errors="replace")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <url|->", file=sys.stderr)
        return 2

    arg = sys.argv[1]
    if arg == "-":
        html = sys.stdin.read()
    else:
        try:
            html = scarica(arg)
        except Exception as e:
            print(f"errore-download: {e}", file=sys.stderr)
            return 2

    try:
        testo = estrai_testo_normalizzato(html)
    except Exception as e:
        print(f"errore-parsing: {e}", file=sys.stderr)
        return 2

    if not testo:
        print("errore-vuoto", file=sys.stderr)
        return 2

    h = hashlib.sha256(testo.encode("utf-8")).hexdigest()
    print(h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
