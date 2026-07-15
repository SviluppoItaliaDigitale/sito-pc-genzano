#!/usr/bin/env python3
"""
genera-chrome-menu.py — FONTE UNICA del menu di navigazione.

Genera il blocco del menu principale dentro static/app-shared/site-chrome.js
a partire da hugo.toml [[menus.main]] — la stessa fonte usata dal partial
Hugo navbar.html. Elimina la doppia manutenzione manuale (hugo.toml ↔
site-chrome.js) che dal 2026 richiedeva allineamento a mano e un check
settimanale anti-drift (audit-sito.yml § 41). Audit esterno 15/07/2026,
punto "una sola fonte per il menu".

Il blocco generato vive tra i marker:
    /* MENU-AUTOGEN:START ... */
    /* MENU-AUTOGEN:END */
Tutto ciò che sta tra i marker è SCRITTO DA QUESTO SCRIPT: non modificarlo
a mano — modifica hugo.toml e rilancia lo script.

Uso:
    python3 scripts/genera-chrome-menu.py            # rigenera site-chrome.js
    python3 scripts/genera-chrome-menu.py --check    # exit 1 se c'è drift
                                                     # (usato da validate-pr.yml)

Ordinamento: identico a Hugo (weight crescente, a parità di weight nome
alfabetico). I pesi in hugo.toml sono tenuti senza pareggi proprio per
rendere l'ordine deterministico e uguale nei due chrome.
"""
import html
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = ROOT / "static/app-shared/site-chrome.js"
START = "/* MENU-AUTOGEN:START"
END = "/* MENU-AUTOGEN:END */"

IND = "                "  # indentazione base del blocco dentro NAV


def esc(name: str) -> str:
    """Escape per stringa JS single-quoted + entità HTML per à/è/…"""
    s = name.replace("\\", "\\\\").replace("'", "\\'")
    # à → &agrave; ecc. per coerenza col resto del file (ASCII-safe)
    return s.encode("ascii", "xmlcharrefreplace").decode("ascii")


def genera_blocco(menus: list[dict]) -> str:
    top = sorted(
        (e for e in menus if "parent" not in e),
        key=lambda e: (e.get("weight", 0), e["name"]),
    )
    figli = {}
    for e in menus:
        if "parent" in e:
            figli.setdefault(e["parent"], []).append(e)
    for v in figli.values():
        v.sort(key=lambda e: (e.get("weight", 0), e["name"]))

    righe = []
    for voce in top:
        nome = esc(voce["name"])
        ident = voce.get("identifier")
        if ident and ident in figli:
            righe.append(f"{IND}'<li class=\"nav-item dropdown\" role=\"none\">' +")
            righe.append(
                f"{IND}  '<a class=\"nav-link dropdown-toggle\" href=\"#\" id=\"navDropdown-{ident}\" role=\"menuitem\" data-bs-toggle=\"dropdown\" aria-expanded=\"false\">' +"
            )
            righe.append(f"{IND}    '<span>{nome}</span>' +")
            righe.append(
                f"{IND}    '<svg class=\"icon icon-xs\"><use href=\"' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand\"></use></svg>' +"
            )
            righe.append(f"{IND}  '</a>' +")
            righe.append(
                f"{IND}  '<div class=\"dropdown-menu\" aria-labelledby=\"navDropdown-{ident}\"><div class=\"link-list-wrapper\"><ul class=\"link-list\" role=\"menu\">' +"
            )
            for f in figli[ident]:
                righe.append(
                    f"{IND}    '<li role=\"none\"><a class=\"list-item\" href=\"' + SITE_URL + '{f['url']}\" role=\"menuitem\"><span>{esc(f['name'])}</span></a></li>' +"
                )
            righe.append(f"{IND}  '</ul></div></div>' +")
            righe.append(f"{IND}'</li>' +")
        else:
            righe.append(
                f"{IND}'<li class=\"nav-item\" role=\"none\"><a class=\"nav-link\" href=\"' + SITE_URL + '{voce['url']}\" role=\"menuitem\"><span>{nome}</span></a></li>' +"
            )
    return "\n".join(righe)


def main() -> int:
    check = "--check" in sys.argv

    with open(ROOT / "hugo.toml", "rb") as fh:
        menus = tomllib.load(fh)["menus"]["main"]

    blocco = genera_blocco(menus)
    testo = CHROME.read_text(encoding="utf-8")

    i = testo.find(START)
    j = testo.find(END)
    if i < 0 or j < 0:
        print("ERRORE: marker MENU-AUTOGEN mancanti in site-chrome.js", file=sys.stderr)
        return 2
    fine_start = testo.index("*/", i) + 2

    nuovo = (
        testo[:fine_start]
        + "\n"
        + blocco
        + "\n"
        + IND
        + testo[j:]
    )

    if nuovo == testo:
        print("site-chrome.js già allineato a hugo.toml.")
        return 0
    if check:
        print(
            "DRIFT: il menu di site-chrome.js non corrisponde a hugo.toml.\n"
            "Rilancia: python3 scripts/genera-chrome-menu.py  (e committa)",
            file=sys.stderr,
        )
        return 1
    CHROME.write_text(nuovo, encoding="utf-8")
    print("site-chrome.js rigenerato da hugo.toml [[menus.main]].")
    return 0


if __name__ == "__main__":
    sys.exit(main())
