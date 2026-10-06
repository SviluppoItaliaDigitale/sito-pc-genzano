#!/usr/bin/env python3
"""
Open Kit PC Genzano: pacchetti ZIP dei componenti riusabili del sito.

Ogni componente (lettura ad alta voce, pannello di accessibilità, glossario,
tabelle CAA, pagina rischio, feed CAP, «I miei contenuti», Modalità Aula,
«Crea la mia lezione», controllo dei fogli di stampa) diventa uno ZIP in
static/open-kit/ con i file VERI del sito, le sole sezioni di CSS che servono,
un LEGGIMI con istruzioni, licenza e attribuzioni, e il testo della EUPL 1.2.

Perché si genera al deploy (deploy.yml, prima della build) e non si committa:
un kit copiato a mano invecchia dal giorno dopo. Così ogni pacchetto è sempre
la versione in linea del componente. Gli ZIP sono riproducibili (data fissa
delle voci), quindi non cambiano finché non cambiano i file.

Licenze: codice dei componenti EUPL 1.2 (scelta dell'autore, 06/10/2026);
testi ed esempi di contenuto CC BY 4.0 come il resto del sito. I pittogrammi
ARASAAC (CC BY-NC-SA 4.0) e le librerie di terzi NON sono nei pacchetti: il
LEGGIMI dice dove prenderli.

Uso:
  python3 scripts/genera-open-kit.py            # scrive static/open-kit/*.zip e data/open_kit.json
L'indice data/open_kit.json (componenti e descrizioni, senza dimensioni) è
committato e la pagina /open-kit/ lo legge; la dimensione di ogni ZIP la legge
la pagina dal file, che esiste solo nella build del deploy.
  python3 scripts/genera-open-kit.py --elenco   # mostra i componenti e i file
Solo libreria standard.
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = "themes/flavour-pcgenzano"
CSS = ROOT / T / "static/css/custom.css"
OUT = ROOT / "static/open-kit"
LICENZA = ROOT / "scripts/open-kit/EUPL-1.2.txt"
DATA_FISSA = (2026, 10, 6, 0, 0, 0)
AUTORE = "Alessandro Cuollo — Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"
SITO = "https://www.protezionecivilegenzano.it"

COMPONENTI = [
    {
        "id": "lettura-ad-alta-voce",
        "titolo": "Leggi ad alta voce",
        "desc": "Pulsante che legge la pagina con la voce del browser (Web Speech API), con tre velocità. Niente file audio, niente servizi esterni.",
        "file": [f"{T}/layouts/partials/leggi-ad-alta-voce.html"],
        "css": ["TTS — Pulsante \"Leggi ad alta voce\"", "TTS FALLBACK"],
        "uso": "Includi il partial dove vuoi il pulsante, passando il selettore del testo da leggere: "
               "{{ partial \"leggi-ad-alta-voce.html\" (dict \"selector\" \".article-body\") }}. "
               "Su un sito non Hugo copia il markup e lo script del partial in una pagina HTML.",
    },
    {
        "id": "pannello-accessibilita",
        "titolo": "Pannello «Strumenti di accessibilità»",
        "desc": "Pulsante fisso che apre le preferenze di lettura: dimensione del testo, carattere per dislessia, cinque contrasti, spaziatura, pausa animazioni. Le scelte restano nel browser.",
        "file": [f"{T}/layouts/partials/accessibility-toolbar.html", f"{T}/static/css/a11y-toolbar.css",
                 f"{T}/static/js/a11y-toolbar.js"],
        "css": [],
        "uso": "Includi il partial in fondo al <body>, il CSS nel <head> e lo script con defer. Per evitare il lampo "
               "di pagina non adattata, copia anche lo script breve nel <head> descritto nei commenti di "
               "a11y-toolbar.js. Il carattere per dislessia (OpenDyslexic, SIL OFL 1.1) va scaricato a parte.",
    },
    {
        "id": "glossario-inline",
        "titolo": "Glossario nel testo",
        "desc": "La prima volta che in una pagina compare una sigla (COC, NUE, IT-alert…) diventa un pulsante che apre la definizione, accessibile da tastiera.",
        "file": [f"{T}/layouts/partials/glossario-inline.html", "static/js/glossario-inline.js", "data/glossario.yaml"],
        "css": ["GLOSSARIO INLINE"],
        "uso": "Il partial legge data/glossario.yaml e passa le voci allo script. Le definizioni del file sono "
               "nostre (CC BY 4.0): puoi usarle citando la fonte o sostituirle con le tue.",
    },
    {
        "id": "tabelle-caa",
        "titolo": "Tabelle di comunicazione (CAA)",
        "desc": "Griglie di pittogrammi e parole da indicare per chi in emergenza non riesce a parlare, stampabili su A4.",
        "file": [f"{T}/layouts/shortcodes/caa-tabella.html", f"{T}/layouts/shortcodes/caa-voce.html"],
        "css": ["TABELLE DI COMUNICAZIONE CAA"],
        "uso": "{{< caa-tabella titolo=\"Ho bisogno di\" >}}{{< caa-voce src=\"/pittogrammi/arasaac/acqua.png\" "
               "parola=\"Acqua\" >}}{{< /caa-tabella >}}. I pittogrammi ARASAAC non sono inclusi: si scaricano "
               "da arasaac.org e hanno licenza CC BY-NC-SA 4.0 (uso non commerciale, attribuzione a Sergio Palao "
               "e al Governo di Aragona, stessa licenza per le opere derivate).",
    },
    {
        "id": "pagina-rischio",
        "titolo": "Modello di pagina rischio",
        "desc": "Struttura fissa delle pagine dei rischi (prima, durante, dopo, cosa non fare, chi chiamare) con i due riquadri finali.",
        "file": [f"{T}/layouts/shortcodes/cosa-non-fare.html", f"{T}/layouts/shortcodes/chi-chiamare.html"],
        "css": ["COSA NON FARE", "CHI CHIAMARE BOX"],
        "extra": {"modello-pagina-rischio.md": (
            "---\ntitle: \"Rischio …: cosa fare\"\ndescription: \"…\"\n---\n\n"
            "## Perché è rilevante sul nostro territorio\n\n…\n\n"
            "## Cosa fare PRIMA\n\n- …\n\n## Cosa fare DURANTE\n\n- …\n\n## Cosa fare DOPO\n\n- …\n\n"
            "{{< cosa-non-fare titolo=\"Cosa NON fare\" >}}\n- …\n{{< /cosa-non-fare >}}\n\n{{< chi-chiamare >}}\n")},
        "uso": "Copia il modello in content/ e scrivi i comportamenti prendendoli dalle indicazioni del "
               "Dipartimento della Protezione Civile. Il riquadro «Chi chiamare» contiene i numeri del Lazio "
               "(112 e 803 555): sostituisci la sala operativa con quella della tua regione.",
    },
    {
        "id": "feed-cap",
        "titolo": "Feed CAP 1.2 dell'allerta",
        "desc": "Il livello di allerta pubblicato come feed Common Alerting Protocol (standard OASIS), leggibile da app e aggregatori.",
        "file": [f"{T}/layouts/index.cap.xml", "data/allerta.json"],
        "css": [],
        "extra": {"hugo-config.toml": (
            "[outputFormats.CAP]\n  mediaType = \"application/xml\"\n  baseName = \"allerta-cap\"\n"
            "  isPlainText = true\n  notAlternative = true\n  rel = \"alternate\"\n\n"
            "[outputs]\n  home = [\"HTML\", \"RSS\", \"CAP\"]\n")},
        "uso": "Aggiungi le righe di hugo-config.toml alla tua configurazione e il template nel tema. "
               "data/allerta.json è un esempio della struttura: il livello deve venire dal bollettino ufficiale "
               "del Centro Funzionale della tua regione, mai inserito a stima.",
    },
    {
        "id": "i-miei-contenuti",
        "titolo": "I miei contenuti",
        "desc": "Il cittadino salva le pagine che gli servono e le ritrova in un elenco. Tutto resta nel suo browser: nessun account, nessun dato inviato.",
        "file": [f"{T}/static/js/miei-contenuti.js", "content/i-miei-contenuti/_index.md"],
        "css": ["I MIEI CONTENUTI"],
        "uso": "Lo script cerca un pulsante .btn-salva-pagina (con data-titolo) e l'elenco #miei-contenuti-elenco "
               "della pagina dedicata: il markup del pulsante è in partials/page-tools.html del nostro tema. "
               "Ricorda di citare il salvataggio nel browser nella tua informativa privacy.",
    },
    {
        "id": "modalita-aula",
        "titolo": "Modalità Aula",
        "desc": "La pagina diventa una sequenza di schermate a tutto schermo, testo grande e niente menu, da proiettare in classe.",
        "file": [f"{T}/layouts/partials/modalita-aula.html", f"{T}/static/js/modalita-aula.js"],
        "css": ["MODALITÀ AULA"],
        "uso": "{{ partial \"modalita-aula.html\" (dict \"page\" . \"selector\" \".article-body\") }}. Le schermate "
               "nascono dagli h2 del contenuto; i riquadri interattivi restano nella pagina.",
    },
    {
        "id": "crea-la-mia-lezione",
        "titolo": "Crea la mia lezione",
        "desc": "Il docente sceglie classe, minuti e argomento e il sito compone una lezione in fasi con i materiali già pubblicati.",
        "file": ["scripts/genera-materiali-lezione.py", f"{T}/layouts/shortcodes/crea-lezione.html",
                 f"{T}/static/js/crea-lezione.js"],
        "css": ["CREA LA MIA LEZIONE"],
        "uso": "Il generatore legge l'indice delle schede, delle storie, dei giochi e degli esperimenti del nostro "
               "sito: va adattato alla struttura dei tuoi materiali (funzioni schede(), storie(), giochi(), "
               "esperimenti()). Il resto funziona così com'è.",
    },
    {
        "id": "controllo-fogli-stampa",
        "titolo": "Controllo dei fogli di stampa e delle pagine",
        "desc": "Stampa davvero le pagine con Chromium e blocca fogli bianchi, ultimi fogli quasi vuoti ed errori JavaScript; controlla titolo, h1 e testo alternativo di tutte le pagine.",
        "file": ["scripts/check-fogli-stampa.py", "scripts/check-qualita-pagine.py",
                 ".github/workflows/controllo-fogli-stampa.yml"],
        "css": [],
        "uso": "Dopo la build: python3 check-qualita-pagine.py public e python3 check-fogli-stampa.py --public public "
               "(servono playwright con Chromium e pymupdf). Le cartelle delle pagine stampabili sono nella "
               "funzione stampabili(): adattale alle tue.",
    },
]


def sezione_css(titolo: str) -> str:
    """Una sezione di custom.css: dal commento-banner che contiene il titolo al successivo."""
    righe = CSS.read_text(encoding="utf-8").splitlines()
    banner = re.compile(r"^/\* ?(=|─|═|\*)")
    for i, r in enumerate(righe):
        if titolo in r:
            inizio = i
            while inizio > 0 and not banner.match(righe[inizio]):
                inizio -= 1
            fine = i + 1
            while fine < len(righe) and not banner.match(righe[fine]):
                fine += 1
            return "\n".join(righe[inizio:fine]).rstrip() + "\n"
    raise SystemExit(f"Sezione CSS non trovata in custom.css: {titolo!r}")


def leggimi(c: dict, nomi: list[str]) -> str:
    return (
        f"{c['titolo']} — Open Kit PC Genzano\n{'=' * (len(c['titolo']) + 26)}\n\n"
        f"{c['desc']}\n\n"
        f"Come si usa\n-----------\n{c['uso']}\n\n"
        f"File del pacchetto\n------------------\n" + "".join(f"- {n}\n" for n in nomi) +
        f"\nI percorsi riproducono quelli del nostro sito (Hugo, tema Bootstrap Italia).\n"
        f"Il componente in funzione: {SITO}/ — pagina dell'Open Kit: {SITO}/open-kit/\n\n"
        f"Licenza\n-------\n"
        f"Codice: EUPL 1.2 (European Union Public Licence), testo in LICENZA-EUPL-1.2.txt.\n"
        f"Il testo ufficiale in italiano è nella Decisione di esecuzione (UE) 2017/863:\n"
        f"https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32017D0863\n"
        f"Testi ed esempi di contenuto: CC BY 4.0.\n"
        f"Autore: {AUTORE}.\n"
        f"Riusando il componente, cita: «Open Kit PC Genzano — {SITO}/open-kit/».\n\n"
        f"Non inclusi\n-----------\n"
        f"Bootstrap Italia (BSD-3-Clause), Bootstrap Icons (MIT), i pittogrammi ARASAAC (CC BY-NC-SA 4.0)\n"
        f"e le altre librerie di terzi si scaricano dalle loro fonti, con le loro licenze.\n"
    )


def main() -> int:
    if "--elenco" in sys.argv:
        for c in COMPONENTI:
            print(c["id"], "→", ", ".join(c["file"]), "| css:", ", ".join(c["css"]) or "—")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    indice = []
    licenza = LICENZA.read_text(encoding="utf-8")
    for c in COMPONENTI:
        voci: dict[str, str | bytes] = {}
        for f in c["file"]:
            p = ROOT / f
            if not p.exists():
                print(f"File mancante per {c['id']}: {f}", file=sys.stderr)
                return 1
            voci[f] = p.read_bytes()
        if c["css"]:
            voci[f"{c['id']}.css"] = "".join(sezione_css(t) + "\n" for t in c["css"])
        for nome, testo in c.get("extra", {}).items():
            voci[nome] = testo
        voci["LICENZA-EUPL-1.2.txt"] = licenza
        voci["LEGGIMI.txt"] = leggimi(c, sorted(voci))
        zip_path = OUT / f"{c['id']}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for nome in sorted(voci):
                info = zipfile.ZipInfo(f"{c['id']}/{nome}", DATA_FISSA)
                info.compress_type = zipfile.ZIP_DEFLATED
                dato = voci[nome]
                z.writestr(info, dato if isinstance(dato, bytes) else dato.encode("utf-8"))
        indice.append({"id": c["id"], "titolo": c["titolo"], "desc": c["desc"],
                       "zip": f"/open-kit/{c['id']}.zip", "file": len(voci)})
    (ROOT / "data/open_kit.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Open Kit: {len(indice)} pacchetti in static/open-kit/ "
          f"({sum((OUT / (i['id'] + '.zip')).stat().st_size for i in indice) // 1024} KB in tutto)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
