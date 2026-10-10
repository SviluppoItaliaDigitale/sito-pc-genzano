#!/usr/bin/env python3
"""Pulizia periodica delle immagini social già pubblicate.

Le immagini in social-bozze/AAAA/MM/<slug>/ servono al repository privato
social-pc-genzano solo nella finestra di pubblicazione (tre giorni dall'uscita
dell'articolo). Dopo restano lì senza uso: circa 50 MB al mese. Questo script
toglie le immagini (.jpg, .png, .webp) delle cartelle di articoli usciti da più
di N giorni (60 di default), lascia testi e README e scrive il marcatore
`.immagini-rimosse`, così una modifica successiva all'articolo non le rigenera
(scripts/social-pronti.py lo rispetta). Se servono di nuovo:
    python3 scripts/genera-immagini-social.py --force content/comunicazioni/<slug>.md

Uso:
    python3 scripts/pulisci-social-bozze.py [--giorni 60] [--dry-run]

La storia di git conserva le versioni vecchie: questo frena la crescita del
repository e alleggerisce i checkout, non accorcia la storia.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import social_comune as S  # noqa: E402

ESTENSIONI = {".jpg", ".jpeg", ".png", ".webp"}


def data_cartella(cartella: Path) -> dt.datetime | None:
    """Data di uscita dell'articolo; se l'articolo non c'è più, quella del nome."""
    md = S.ROOT / "content" / "comunicazioni" / f"{cartella.name}.md"
    if md.is_file():
        d = S.online_dal(S.leggi_frontmatter(md))
        if d:
            return d
    try:
        return dt.datetime.strptime(cartella.name[:10], "%Y-%m-%d").replace(
            tzinfo=S.adesso().tzinfo)
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--giorni", type=int, default=60)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.giorni < 7:
        print("Soglia troppo bassa: sotto i 7 giorni si rischia di togliere immagini ancora da pubblicare.")
        return 2

    limite = S.adesso() - dt.timedelta(days=args.giorni)
    oggi = S.adesso().strftime("%Y-%m-%d")
    cartelle = file_tolti = byte_tolti = 0
    for cartella in sorted(p for p in S.SOCIAL_BOZZE.glob("*/*/*") if p.is_dir()):
        immagini = [f for f in cartella.iterdir() if f.suffix.lower() in ESTENSIONI]
        if not immagini:
            continue
        d = data_cartella(cartella)
        if d is None or d > limite:
            continue
        cartelle += 1
        for f in immagini:
            byte_tolti += f.stat().st_size
            file_tolti += 1
            if not args.dry_run:
                f.unlink()
        if not args.dry_run:
            (cartella / S.MARCATORE_PULITO).write_text(
                f"Immagini rimosse il {oggi} dalla pulizia periodica "
                f"(scripts/pulisci-social-bozze.py, articolo uscito da oltre "
                f"{args.giorni} giorni).\n", encoding="utf-8")
    azione = "da togliere" if args.dry_run else "tolti"
    print(f"{cartelle} cartelle, {file_tolti} file {azione}, {byte_tolti / 1e6:.1f} MB.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
