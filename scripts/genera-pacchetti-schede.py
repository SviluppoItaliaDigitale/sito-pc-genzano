#!/usr/bin/env python3
"""
Genera pacchetti HTML A4 pronti per la stampa in un solo click.

Per ogni fascia scolastica (infanzia, primaria, secondaria I, secondaria II)
produce un singolo file HTML che contiene tutte le schede del kit
corrispondente, concatenate con page-break tra una e l'altra.

L'utente clicca "Stampa tutte le schede di Infanzia (44 fogli A4)" dalla hub
schede-stampabili → si apre il pacchetto con la finestra di stampa già aperta
(grazie a ?autoprint=1 in querystring).

Output: static/formazione/schede-stampabili/pacchetti/<fascia>.html

Fonte di verità della lista schede per fascia:
content/formazione/kit-scuola-<fascia>.md (stesso usato da
genera-pacchetti-kit.py per gli ZIP scaricabili offline).

Idempotente: ricrea sempre da zero in base ai .md e alle schede esistenti.
Aggiornamento automatico:
  - Eseguito in deploy.yml prima della build Hugo (rete di sicurezza)
  - Eseguito manualmente con: python3 scripts/genera-pacchetti-schede.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KITS = {
    "infanzia": {
        "md": "kit-scuola-infanzia.md",
        "label": "Scuola dell'Infanzia",
        "eta": "3-6 anni",
        "color": "#c026d3",
        "iconbg": "#fde8ea",
    },
    "primaria": {
        "md": "kit-scuola-primaria.md",
        "label": "Scuola Primaria",
        "eta": "6-11 anni",
        "color": "#0066cc",
        "iconbg": "#cfe2ff",
    },
    "secondaria": {
        "md": "kit-scuola-secondaria-primo-grado.md",
        "label": "Scuola Secondaria di I grado",
        "eta": "11-13 anni",
        "color": "#15803d",
        "iconbg": "#d1e7dd",
    },
    "secondaria2": {
        "md": "kit-scuola-secondaria-secondo-grado.md",
        "label": "Scuola Secondaria di II grado",
        "eta": "14-19 anni",
        "color": "#b45309",
        "iconbg": "#fff3cd",
    },
}

CONTENT_BASE = ROOT / "content" / "formazione"
SCHEDE_BASE = ROOT / "static" / "formazione" / "schede-stampabili"
OUTPUT_DIR = SCHEDE_BASE / "pacchetti"


def lista_schede_kit(md_path: Path) -> list[str]:
    """Lista ordinata di slug schede linkati dal kit (prima apparizione)."""
    text = md_path.read_text(encoding="utf-8")
    seen: list[str] = []
    for m in re.finditer(
        r'/formazione/schede-stampabili/([a-z0-9][a-z0-9-]*?)/?(?=[)"\s\]])', text
    ):
        slug = m.group(1)
        if slug in ("assets", "pacchetti"):
            continue
        if slug not in seen:
            seen.append(slug)
    return seen


def _testo_da_html(frammento):
    """Testo pulito da un frammento HTML, senza incollare le parole.

    Un `<br>` separa due parole tanto quanto uno spazio: toglierlo e basta
    produceva titoli come «Il libro pop-updella protezione civile», arrivati
    fino al pacchetto pubblicato e letti così anche dagli screen reader.
    Stessa cura per i tag di blocco, che a video vanno a capo.
    """
    testo = re.sub(r"<br\s*/?>", " ", frammento, flags=re.IGNORECASE)
    testo = re.sub(r"</(p|div|li|h[1-6]|tr|td|th)>", " ", testo, flags=re.IGNORECASE)
    testo = re.sub(r"<[^>]+>", "", testo)
    return re.sub(r"\s+", " ", testo).strip()


def estrai_styles_articoli_titolo(
    html: str, slug: str
) -> tuple[list[str], list[tuple[str, str]], str]:
    """
    Estrae da una scheda:
      - blocchi <style>...</style>
      - lista di (tag_html, contenuto_interno) per ogni "pagina A4" trovata
        (tre varianti: scheda-page, scheda-immagine-wrapper, foglio)
      - titolo per l'indice

    Riscrive i path relativi di src/href verso path assoluti relativi alla
    cartella della scheda originale (così le immagini funzionano anche
    quando inglobate dentro /pacchetti/<fascia>.html).
    """
    m_title = re.search(
        r'<h1\s+class="scheda-titolo-principale"[^>]*>(.+?)</h1>',
        html, re.IGNORECASE | re.DOTALL
    )
    if m_title:
        titolo = _testo_da_html(m_title.group(1))
    else:
        m_h1 = re.search(r"<h1[^>]*>(.+?)</h1>", html, re.IGNORECASE | re.DOTALL)
        if m_h1:
            titolo = _testo_da_html(m_h1.group(1))
        else:
            m_t = re.search(r"<title>([^<]+)</title>", html, re.IGNORECASE)
            titolo = (m_t.group(1) if m_t else "Scheda").strip()
            titolo = re.sub(r"^Scheda stampabile:\s*", "", titolo, flags=re.IGNORECASE)
            titolo = re.sub(r"\s+[—\-]\s+.*$", "", titolo)

    styles = re.findall(r"<style[^>]*>(.*?)</style>", html, re.IGNORECASE | re.DOTALL)

    # Tre varianti di wrapper-pagina, in ordine di frequenza
    pattern = (
        r'<(article|main)\s+class="(scheda-page|scheda-immagine-wrapper|foglio)"[^>]*>'
        r'(.*?)'
        r'</\1>'
    )
    pagine: list[tuple[str, str]] = []
    for m in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
        classe = m.group(2)
        inner = m.group(3)
        # Riscrive path relativi a path assoluti del sito
        inner = reindirizza_path_relativi(inner, slug)
        pagine.append((classe, inner))

    return styles, pagine, titolo


# ---------------------------------------------------------------------------
# Isolamento degli stili delle schede dentro il pacchetto (06/10/2026)
#
# Ogni scheda porta i suoi <style>. Concatenati nell'intestazione del
# pacchetto valevano per tutte le schede: vinceva l'ultima regola, e una
# scala di stampa su html (o un .scheda-footer senza margini) scritta per una
# scheda cambiava l'impaginazione di tutte le altre. Ora ogni regola vale solo
# dentro la <section> della sua scheda:
#   - i selettori ricevono il prefisso :where([id="scheda-<slug>"]), che non
#     aggiunge specificità: dentro la sezione la scheda si comporta come
#     stampata da sola rispetto a scheda-print.css;
#   - html { font-size: N% } (la scala di stampa della scheda) diventa
#     zoom: N/100 sulla sola sezione, perché le dimensioni in rem dipendono
#     dalla radice del documento e non si possono ridurre per una sezione;
#   - body tiene solo font-size (lo sfondo è del pacchetto);
#   - @page senza nome della scheda non passa al pacchetto, che stampa tutto
#     in A4 verticale con margine di 5 mm: il browser usa un solo formato per
#     documento. Le schede pensate in orizzontale (i libri pop-up) si riducono
#     in proporzione per entrare nel foglio, altrimenti sporgerebbero e il
#     browser rimpicciolirebbe l'intero pacchetto. Pagine con nome e
#     @font-face restano come sono.
# ---------------------------------------------------------------------------

_AT_CON_REGOLE = ("@media", "@supports", "@container", "@layer", "@document")


def _salta_fino(css: str, i: int, stop: str) -> int:
    """Indice del primo carattere in `stop` a partire da i, saltando commenti
    e stringhe (le schede usano content: "{" e simili). len(css) se assente."""
    n = len(css)
    while i < n:
        c = css[i]
        if c == "/" and css.startswith("/*", i):
            j = css.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c in "\"'":
            j = i + 1
            while j < n and css[j] != c:
                j += 2 if css[j] == "\\" else 1
            i = j + 1
            continue
        if c in stop:
            return i
        i += 1
    return n


def _blocco(css: str, i: int) -> int:
    """Dato l'indice dopo una '{', restituisce l'indice della '}' che la chiude."""
    livello = 1
    while True:
        i = _salta_fino(css, i, "{}")
        if i >= len(css):
            return len(css)
        livello += 1 if css[i] == "{" else -1
        if livello == 0:
            return i
        i += 1


def _dividi_selettori(prelude: str) -> list[str]:
    parti, prof, cur = [], 0, []
    for c in prelude:
        if c in "([":
            prof += 1
        elif c in ")]":
            prof -= 1
        if c == "," and prof == 0:
            parti.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    parti.append("".join(cur))
    return [s.strip() for s in parti if s.strip()]


_RE_RADICE = re.compile(r"^(?:html|:root)(?:\s+body)?(?![\w-])|^body(?![\w-])")


def _scope_regola(prelude: str, corpo: str, sezione: str) -> str:
    selettori = _dividi_selettori(re.sub(r"/\*.*?\*/", "", prelude, flags=re.S))
    sulla_sezione, dentro = [], []
    radice_html = False
    for sel in selettori:
        m = _RE_RADICE.match(sel)
        if m:
            resto = sel[m.end():]
            if not resto.strip():
                sulla_sezione.append(sel)
                radice_html = radice_html or not sel.startswith("body")
            else:
                dentro.append(f"{sezione}{resto}" if resto[0] in " >~+" else f"{sezione} {resto.strip()}")
        else:
            dentro.append(f"{sezione} {sel}")
    out = []
    if dentro:
        out.append(f"{', '.join(dentro)} {{{corpo}}}")
    if sulla_sezione:
        # Della radice si tiene solo la dimensione del testo: su html diventa
        # zoom della sezione (scala di stampa), su body resta font-size.
        decl = []
        for d in corpo.split(";"):
            if ":" not in d:
                continue
            k, v = d.split(":", 1)
            k, v = k.strip().lower(), v.strip()
            if k != "font-size":
                continue
            mp = re.fullmatch(r"(\d+(?:\.\d+)?)%\s*(!important)?", v)
            if radice_html and mp:
                decl.append(f"zoom: {float(mp.group(1)) / 100:g}")
            elif not radice_html:
                decl.append(f"font-size: {v}")
        if decl:
            out.append(f"{sezione} {{ {'; '.join(decl)}; }}")
    return "\n".join(out)


def scope_css(css: str, slug: str) -> str:
    """Riscrive un foglio di stile di scheda perché valga solo nella sua sezione."""
    sezione = f':where([id="scheda-{slug}"])'
    out: list[str] = []
    i, n = 0, len(css)
    while i < n:
        j = _salta_fino(css, i, "{};")
        prelude = css[i:j].strip()
        if j >= n:
            break
        if css[j] == ";":                      # @import, @charset: non servono
            i = j + 1
            continue
        if css[j] == "}":                      # graffa orfana: si ignora
            i = j + 1
            continue
        fine = _blocco(css, j + 1)
        corpo = css[j + 1:fine]
        testa = re.sub(r"/\*.*?\*/", "", prelude, flags=re.S).strip()
        if testa.lower().startswith(_AT_CON_REGOLE):
            out.append(f"{testa} {{\n{scope_css(corpo, slug)}\n}}")
        elif re.fullmatch(r"@page", testa, flags=re.I):
            # Pagina senza nome della scheda (di solito il margine): diventa una
            # pagina con nome riservata alla sua sezione, così il margine vale
            # solo per lei. Il formato resta quello del pacchetto (A4 verticale).
            decl = [d.strip() for d in corpo.split(";") if ":" in d]
            orizzontale = any(
                d.split(":", 1)[0].strip().lower() == "size" and "landscape" in d.lower()
                for d in decl)
            # Il margine della scheda non si porta nel pacchetto: tutte le
            # schede stampano con il margine del pacchetto (5 mm). Le pagine con
            # nome lo permetterebbero, ma Chromium le impagina male (provato il
            # 06/10/2026: un'immagine a tutta pagina scivolava sul foglio dopo).
            if orizzontale:
                # Il browser stampa un documento in un solo formato: una scheda
                # pensata in orizzontale (i libri pop-up) sporgerebbe dal foglio
                # verticale e lui rimpicciolirebbe TUTTO il pacchetto per farla
                # entrare. Si riduce invece la sola scheda, in proporzione.
                mm = 5.0
                for d in decl:
                    k, v = d.split(":", 1)
                    mv = re.fullmatch(r"\s*(\d+(?:\.\d+)?)mm\s*", v)
                    if k.strip().lower() == "margin" and mv:
                        mm = float(mv.group(1))
                out.append(f"@media print {{ {sezione} {{ zoom: {(210 - 2 * mm) / (297 - 2 * mm):.3f}; }} }}")
        elif testa.startswith("@"):            # @page con nome, @font-face, @keyframes
            out.append(f"{testa} {{{corpo}}}")
        elif testa:
            out.append(_scope_regola(testa, corpo, sezione))
        i = fine + 1
    return "\n".join(x for x in out if x.strip())


def reindirizza_path_relativi(html: str, slug: str) -> str:
    """
    Riscrive src/href relativi in path assoluti dipendenti dalla cartella
    originale della scheda. Esempio:
      src="scheda-completa.png"
      → src="/formazione/schede-stampabili/<slug>/scheda-completa.png"
    Non tocca: assoluti (/...), URL (http://, https://), mailto/tel/#, data URI.
    """
    base = f"/formazione/schede-stampabili/{slug}"

    def rewrite_attr(match: re.Match) -> str:
        attr = match.group(1)
        quote = match.group(2)
        value = match.group(3)
        if not value or value.startswith(("/", "http://", "https://",
                                          "mailto:", "tel:", "#", "data:",
                                          "javascript:")):
            return match.group(0)
        # Path relativo: aggiungo il base path della scheda
        return f'{attr}={quote}{base}/{value}{quote}'

    html = re.sub(
        r'\b(src|href|poster|data-src)=(["\'])([^"\']*)\2',
        rewrite_attr,
        html,
    )
    return html


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pacchetto stampa: __LABEL__ (__ETA__) — __N__ schede A4</title>
  <meta name="description" content="Stampa in un click tutte le __N__ schede stampabili della __LABEL__ (__ETA__). Pacchetto auto-aggiornato dal sito istituzionale.">
  <meta name="robots" content="noindex,follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
    /* === Stili del pacchetto stampa (schermo) === */
    body {
      background: #eef2f7;
      margin: 0;
      padding: 0;
      color: #212529;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Cantarell, "Helvetica Neue", Arial, sans-serif;
    }
    .pacchetto-toolbar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: __COLOR__;
      color: #fff;
      padding: 0.85rem 1.25rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }
    .pacchetto-toolbar a,
    .pacchetto-toolbar a:visited {
      color: #fff;
      text-decoration: none;
      font-size: 0.95rem;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    .pacchetto-toolbar a:hover,
    .pacchetto-toolbar a:focus {
      text-decoration: underline;
      outline: 2px solid #ffbe2e;
      outline-offset: 2px;
    }
    .pacchetto-titolo {
      font-weight: 600;
      font-size: 1.05rem;
      flex: 1 1 auto;
      text-align: center;
      min-width: 240px;
    }
    .pacchetto-toolbar button {
      background: #fff;
      color: __COLOR__;
      border: 0;
      border-radius: 6px;
      padding: 0.6rem 1.2rem;
      font-weight: 700;
      cursor: pointer;
      font-size: 0.95rem;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    .pacchetto-toolbar button:hover,
    .pacchetto-toolbar button:focus {
      background: #f0f4f8;
      outline: 2px solid #ffbe2e;
      outline-offset: 2px;
    }
    .pacchetto-intro {
      max-width: 21cm;
      margin: 1.5rem auto;
      background: #fff;
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    .pacchetto-intro h1 {
      color: __COLOR__;
      font-size: 1.4rem;
      margin: 0 0 0.5rem 0;
    }
    .pacchetto-intro p {
      font-size: 0.95rem;
      line-height: 1.55;
      margin: 0.4rem 0;
    }
    .pacchetto-stampa-conferma {
      background: __ICONBG__;
      border-left: 4px solid __COLOR__;
      padding: 0.8rem 1.1rem;
      border-radius: 0 8px 8px 0;
      font-size: 0.92rem;
      margin: 0.6rem 0 0 0;
    }
    .pacchetto-stampa-conferma strong { color: __COLOR__; }
    .pacchetto-toc {
      max-width: 21cm;
      margin: 1.5rem auto;
      background: #fff;
      border-radius: 8px;
      padding: 1.2rem 1.5rem;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    .pacchetto-toc h2 {
      color: __COLOR__;
      font-size: 1.1rem;
      margin: 0 0 0.6rem 0;
      padding-bottom: 0.4rem;
      border-bottom: 2px solid __COLOR__;
    }
    .pacchetto-toc ol {
      margin: 0;
      padding-left: 1.5rem;
      font-size: 0.92rem;
      line-height: 1.65;
      columns: 2;
      column-gap: 1.5rem;
    }
    @media (max-width: 700px) {
      .pacchetto-toc ol { columns: 1; }
    }
    .pacchetto-toc li {
      margin: 0.15rem 0;
      break-inside: avoid;
    }
    .pacchetto-toc a {
      color: __COLOR__;
      text-decoration: none;
    }
    .pacchetto-toc a:hover,
    .pacchetto-toc a:focus {
      text-decoration: underline;
      outline: 2px solid #ffbe2e;
      outline-offset: 1px;
    }
    .pacchetto-toc .toc-meta {
      color: #6c757d;
      font-size: 0.85rem;
    }

    /* === Stampa: nascondi toolbar/intro/toc, forza page-break tra schede === */
    @media print {
      .pacchetto-toolbar,
      .pacchetto-intro,
      .pacchetto-toc,
      .no-print {
        display: none !important;
      }
      body { background: #fff; }
      .pacchetto-scheda {
        page-break-after: always;
        break-after: page;
      }
      .pacchetto-scheda:last-of-type {
        page-break-after: auto;
        break-after: auto;
      }
    }
  </style>
  <style>
__STYLES_SCHEDE__
  </style>
  <style>
    /* Formato del pacchetto: A4 verticale, margine 5 mm, per tutte le schede. Le regole
       @page delle schede non passano al pacchetto; le schede orizzontali (il libro pop-up
       con la storia) sono ridotte in proporzione per entrare nel foglio. */
    @media print { @page { size: A4; margin: 5mm; } }
  </style>
</head>
<body>

  <header class="pacchetto-toolbar no-print" role="banner">
    <a href="/formazione/schede-stampabili/" aria-label="Torna alla hub delle schede stampabili">← Torna alle schede</a>
    <span class="pacchetto-titolo">Pacchetto stampa: __LABEL__ · __N__ schede A4</span>
    <button type="button" onclick="window.print()" aria-label="Apri la finestra di stampa per tutte le __N__ schede di __LABEL__">
      🖨️ Stampa tutto (__N_PAGINE__ fogli A4)
    </button>
  </header>

  <section class="pacchetto-intro no-print" aria-labelledby="pacchetto-intro-h1">
    <h1 id="pacchetto-intro-h1">Pacchetto stampa — __LABEL__</h1>
    <p>
      Questo pacchetto contiene <strong>__N__ schede stampabili</strong> della __LABEL__ (__ETA__),
      per un totale di <strong>__N_PAGINE__ fogli A4</strong>.
      Premi <strong>"Stampa tutto"</strong> in alto (oppure <kbd>Ctrl+P</kbd> su Windows/Linux, <kbd>Cmd+P</kbd> su Mac)
      per aprire la finestra di stampa. Per archiviare in digitale scegli <em>"Salva come PDF"</em> come stampante.
    </p>
    <p>
      Per stampare <strong>una singola scheda</strong>, torna alla
      <a href="/formazione/schede-stampabili/">hub delle schede</a> e clicca quella che ti interessa.
      Per il <strong>pacchetto offline ZIP</strong> con indice cliccabile, vedi i bottoni "Scarica pacchetto" nella stessa hub.
    </p>
    <p class="pacchetto-stampa-conferma">
      <strong>Suggerimento per risparmiare carta:</strong> nella finestra di stampa imposta
      <em>"Stampa fronte/retro"</em> per dimezzare l'uso di carta,
      oppure <em>"2 pagine per foglio"</em> per ridurre l'ingombro nel raccoglitore.
    </p>
  </section>

  <nav class="pacchetto-toc no-print" aria-label="Indice del pacchetto">
    <h2>Indice — __N__ schede in questo pacchetto</h2>
    <ol>
__TOC__
    </ol>
  </nav>

  <main>
__ARTICOLI__
  </main>

  <script>
    // Auto-stampa se chiamato con ?autoprint=1
    (function() {
      try {
        var params = new URLSearchParams(window.location.search);
        if (params.get('autoprint') === '1') {
          window.addEventListener('load', function() {
            // Aspetta un attimo per il caricamento di font/immagini
            setTimeout(function() { window.print(); }, 800);
          });
        }
      } catch (e) {
        /* Browser senza URLSearchParams: nessun problema, l'utente
           può comunque cliccare il bottone Stampa */
      }
    })();
  </script>

</body>
</html>
"""


def costruisci_pacchetto(
    fascia: str,
    info: dict,
    schede: list[tuple[str, str, list[str], list[tuple[str, str]]]],
) -> str:
    n = len(schede)
    n_pagine = sum(len(pagine) for _, _, _, pagine in schede)

    # Stili di ogni scheda isolati nella sua sezione (vedi scope_css).
    all_styles: list[str] = []
    for slug, _, styles, _ in schede:
        scoped = "\n".join(scope_css(s, slug) for s in styles).strip()
        if scoped:
            all_styles.append(scoped)

    toc_items: list[str] = []
    for slug, titolo, _, pagine in schede:
        anchor = f"scheda-{slug}"
        n_p = len(pagine)
        meta = "" if n_p == 1 else f' <span class="toc-meta">· {n_p} fogli</span>'
        toc_items.append(
            f'      <li><a href="#{anchor}">{escape_html(titolo)}</a>{meta}</li>'
        )
    toc_html = "\n".join(toc_items)

    schede_html: list[str] = []
    for slug, titolo, _, pagine in schede:
        anchor = f"scheda-{slug}"
        pagine_inner_parts: list[str] = []
        for classe, inner in pagine:
            tag = "main" if classe in ("scheda-immagine-wrapper", "foglio") else "article"
            # Forziamo class="scheda-page" su tutti i wrapper: così la regola
            # @media print di scheda-print.css (.scheda-page { page-break-after: always })
            # si applica uniformemente. La classe originale resta come secondo nome.
            classi_finali = f"scheda-page {classe}" if classe != "scheda-page" else "scheda-page"
            pagine_inner_parts.append(
                f'  <{tag} class="{classi_finali}">{inner}</{tag}>'
            )
        schede_html.append(
            f'<section id="{anchor}" class="pacchetto-scheda" '
            f'aria-label="Scheda: {escape_html(titolo)}">\n'
            f'{chr(10).join(pagine_inner_parts)}\n</section>'
        )
    articoli_aggregati = "\n\n".join(schede_html)

    styles_concat = "\n\n".join(all_styles)

    return (HTML_TEMPLATE
        .replace("__LABEL__", info["label"])
        .replace("__ETA__", info["eta"])
        .replace("__COLOR__", info["color"])
        .replace("__ICONBG__", info["iconbg"])
        .replace("__N_PAGINE__", str(n_pagine))
        .replace("__N__", str(n))
        .replace("__TOC__", toc_html)
        .replace("__ARTICOLI__", articoli_aggregati)
        .replace("__STYLES_SCHEDE__", styles_concat)
    )


def main() -> int:
    if not SCHEDE_BASE.exists():
        print(f"[errore] Cartella schede non trovata: {SCHEDE_BASE}", file=sys.stderr)
        return 2

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    totale_schede = 0
    totale_pagine = 0

    for fascia, info in KITS.items():
        md_path = CONTENT_BASE / info["md"]
        if not md_path.exists():
            print(f"[skip] Kit md mancante per {fascia}: {md_path}")
            continue

        slugs = lista_schede_kit(md_path)
        schede: list[tuple[str, str, list[str], list[tuple[str, str]]]] = []
        mancanti: list[str] = []
        for slug in slugs:
            scheda_html = SCHEDE_BASE / slug / "index.html"
            if not scheda_html.exists():
                mancanti.append(slug)
                continue
            html = scheda_html.read_text(encoding="utf-8")
            styles, pagine, titolo = estrai_styles_articoli_titolo(html, slug)
            if not pagine:
                mancanti.append(f"{slug} (nessun wrapper pagina riconosciuto)")
                continue
            schede.append((slug, titolo, styles, pagine))

        if not schede:
            print(f"[skip] Nessuna scheda valida per {fascia}")
            continue

        pacchetto_html = costruisci_pacchetto(fascia, info, schede)
        out_path = OUTPUT_DIR / f"{fascia}.html"
        out_path.write_text(pacchetto_html, encoding="utf-8")

        n_pagine = sum(len(p) for _, _, _, p in schede)
        totale_schede += len(schede)
        totale_pagine += n_pagine
        size_kb = out_path.stat().st_size / 1024
        skip_msg = f" (skip: {len(mancanti)})" if mancanti else ""
        print(
            f"[ok] {fascia}: {len(schede)} schede, {n_pagine} pagine A4, "
            f"{size_kb:.0f} KB → {out_path.relative_to(ROOT)}{skip_msg}"
        )

    print(
        f"\n[totale] {totale_schede} schede, {totale_pagine} pagine A4 "
        f"in {len(KITS)} pacchetti → {OUTPUT_DIR.relative_to(ROOT)}/"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
