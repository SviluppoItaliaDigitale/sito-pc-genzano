#!/usr/bin/env python3
"""Costruisce il cruciverba di protezione civile per la secondaria di primo grado.

Perché un generatore e non una griglia disegnata a mano: fino al 25/09/2026 la
scheda pubblicava uno schema 13×13 «indicativo», cioè una griglia che non
corrispondeva alle definizioni — un docente la stampava e gli alunni non
potevano risolverla (audit esterno del 25/09/2026, rilievo F15). Qui la griglia
è calcolata dalle parole: ogni definizione ha la sua casella numerata, ogni
incrocio condivide la lettera giusta, e lo script rifiuta di scrivere il file
se anche una sola sequenza di lettere della griglia non è una delle parole.

Come lavora:

1. L'elenco PAROLE è la sola fonte: risposta, definizione, tipo (sigla o
   parola). Ogni definizione riprende una voce del glossario del sito
   (`content/glossario/_index.md`) o una pagina di `/conoscere/`, così è
   verificabile dal docente e dall'alunno.
2. La ricerca dell'incastro è un piazzamento greedy con semi fissi (SEMI):
   lo stesso elenco produce sempre la stessa griglia, quindi rigenerare non
   cambia nulla se le parole non cambiano (idempotenza). Fra le griglie
   trovate vince quella con più incroci.
3. Regole del cruciverba classico: parole solo in caselle bianche contigue,
   caselle nere altrove, nessuna coppia di lettere affiancate che non
   appartenga a una parola dell'elenco, ogni parola incrociata con almeno
   un'altra. La numerazione è quella standard: numero progressivo da sinistra
   a destra e dall'alto in basso su ogni casella che inizia una parola.
4. Prima di scrivere, `verifica()` rilegge la griglia da zero e controlla con
   assert che le sequenze orizzontali e verticali di due o più lettere siano
   esattamente le parole dell'elenco.

Uso:
  python3 scripts/schede-didattiche/genera-cruciverba-secondaria.py          # scrive la scheda
  python3 scripts/schede-didattiche/genera-cruciverba-secondaria.py --check  # exit 1 se il file non è aggiornato

Dopo la rigenerazione: `python3 scripts/genera-pacchetti-schede.py`,
`python3 scripts/genera-pacchetti-kit.py`, `python3 scripts/check-parita-schede.py`.
"""

from __future__ import annotations

import html
import pathlib
import random
import sys

REV = "Rev. 2 · 25/09/2026"
LATO = 13
USCITA = pathlib.Path(__file__).resolve().parents[2] / (
    "static/formazione/schede-stampabili/cruciverba-secondaria/index.html")

# Semi provati in ordine: il primo che dà una griglia valida per tutte le
# parole entra nella rosa; fra i candidati vince quello con più incroci.
SEMI = range(0, 4000)
MAX_CANDIDATI = 40

# (risposta, definizione, tipo). La definizione non contiene mai la risposta.
# Fonte di ogni definizione: content/glossario/_index.md, salvo dove indicato.
PAROLE: list[tuple[str, str, str]] = [
    ("NUE", "Numero Unico Europeo di emergenza, il 112 (sigla)", "sigla"),
    ("DPC", "Dipartimento della Protezione Civile (sigla)", "sigla"),
    ("PAI", "Piano di Assetto Idrogeologico (sigla)", "sigla"),
    ("COC", "Centro Operativo Comunale, lo attiva il Sindaco (sigla)", "sigla"),
    ("AIB", "Antincendio Boschivo (sigla)", "sigla"),
    ("CFR", "Centro Funzionale Regionale, pubblica i bollettini di criticità (sigla)", "sigla"),
    ("INGV", "Istituto che monitora terremoti, vulcani e maremoti (sigla)", "sigla"),
    ("ITALERT", "Sistema nazionale di allarme pubblico sui cellulari (scrivilo senza trattino)", "parola"),
    ("RISCHIO", "«Io non …»: la campagna nazionale con i volontari in piazza", "parola"),
    ("IPOCENTRO", "Punto in profondità dove si genera il terremoto", "parola"),
    ("EPICENTRO", "Punto della superficie che sta proprio sopra l'origine del terremoto", "parola"),
    ("MAGNITUDO", "Misura l'energia rilasciata da un terremoto", "parola"),
    ("MITIGAZIONE", "Interventi che riducono gli effetti di un evento: argini, edifici antisismici", "parola"),
    ("RESILIENZA", "Capacità di una comunità di assorbire un evento avverso e ripartire", "parola"),
    ("ALLERTA", "Avviso preventivo delle autorità: può essere gialla, arancione o rossa", "parola"),
    ("SCIAME", "… sismico: molte scosse simili, in tempi ravvicinati, nella stessa area", "parola"),
]

H, V = "H", "V"


class Griglia:
    """Stato della ricerca: lettere, direzioni occupate, parole piazzate."""

    def __init__(self) -> None:
        self.lettere: list[list[str | None]] = [[None] * LATO for _ in range(LATO)]
        self.dirs: list[list[set[str]]] = [[set() for _ in range(LATO)] for _ in range(LATO)]
        self.piazzate: dict[str, tuple[int, int, str]] = {}
        self.incroci = 0

    def _lettera(self, r: int, c: int) -> str | None:
        if 0 <= r < LATO and 0 <= c < LATO:
            return self.lettere[r][c]
        return None

    def posizioni(self, parola: str) -> list[tuple[int, int, str, int]]:
        """Tutte le posizioni valide (r, c, dir, n_incroci) per la parola."""
        n = len(parola)
        out = []
        prima = not self.piazzate
        for d in (H, V):
            dr, dc = (0, 1) if d == H else (1, 0)
            for r in range(LATO):
                for c in range(LATO):
                    if r + dr * (n - 1) >= LATO or c + dc * (n - 1) >= LATO:
                        continue
                    # casella prima e dopo la parola: mai una lettera
                    if self._lettera(r - dr, c - dc) is not None:
                        continue
                    if self._lettera(r + dr * n, c + dc * n) is not None:
                        continue
                    inc = 0
                    ok = True
                    for i in range(n):
                        rr, cc = r + dr * i, c + dc * i
                        lett = self.lettere[rr][cc]
                        if lett is not None:
                            if lett != parola[i] or d in self.dirs[rr][cc]:
                                ok = False
                                break
                            inc += 1
                        else:
                            # casella vuota: i vicini perpendicolari devono essere
                            # vuoti, altrimenti nasce una sequenza che non è una parola
                            if d == H:
                                if self._lettera(rr - 1, cc) is not None or self._lettera(rr + 1, cc) is not None:
                                    ok = False
                                    break
                            else:
                                if self._lettera(rr, cc - 1) is not None or self._lettera(rr, cc + 1) is not None:
                                    ok = False
                                    break
                    if not ok or (not prima and inc == 0):
                        continue
                    out.append((r, c, d, inc))
        return out

    def metti(self, parola: str, r: int, c: int, d: str) -> list[tuple[int, int]]:
        dr, dc = (0, 1) if d == H else (1, 0)
        nuove = []
        for i, lett in enumerate(parola):
            rr, cc = r + dr * i, c + dc * i
            if self.lettere[rr][cc] is None:
                self.lettere[rr][cc] = lett
                nuove.append((rr, cc))
            else:
                self.incroci += 1
            self.dirs[rr][cc].add(d)
        self.piazzate[parola] = (r, c, d)
        return nuove

    def togli(self, parola: str, nuove: list[tuple[int, int]]) -> None:
        r, c, d = self.piazzate.pop(parola)
        dr, dc = (0, 1) if d == H else (1, 0)
        for i in range(len(parola)):
            rr, cc = r + dr * i, c + dc * i
            self.dirs[rr][cc].discard(d)
        for rr, cc in nuove:
            self.lettere[rr][cc] = None
        self.incroci -= len(parola) - len(nuove)


def cerca(parole: list[str], seme: int) -> Griglia | None:
    """Piazzamento greedy a seme fisso: prima la parola più lunga al centro,
    poi ogni parola nella posizione con più incroci (a parità, a caso). Una
    parola che adesso non trova posto si rimanda al giro successivo; se dopo
    tutti i giri ne resta una fuori, il seme fallisce e si prova il successivo.
    Il backtracking esaustivo, provato prima, impiegava minuti per ogni seme."""
    rng = random.Random(seme)
    g = Griglia()
    ordine = sorted(parole, key=lambda p: (-len(p), rng.random()))
    prima = ordine.pop(0)
    centro = (LATO - len(prima)) // 2
    if rng.random() < 0.5:
        g.metti(prima, LATO // 2, centro, H)
    else:
        g.metti(prima, centro, LATO // 2, V)
    for _ in range(4):
        rimaste = []
        for parola in ordine:
            pos = g.posizioni(parola)
            if not pos:
                rimaste.append(parola)
                continue
            migliore = max(inc for *_, inc in pos)
            scelte = [x for x in pos if x[3] == migliore]
            r, c, d, _ = rng.choice(scelte)
            g.metti(parola, r, c, d)
        if not rimaste:
            return g
        ordine = rimaste
    return None


def sequenze(lettere: list[list[str | None]], d: str) -> dict[tuple[int, int], str]:
    """Le sequenze di 2+ lettere contigue nella direzione d, per casella iniziale."""
    out = {}
    for a in range(LATO):
        seq, inizio = "", None
        for b in range(LATO + 1):
            r, c = (a, b) if d == H else (b, a)
            lett = lettere[r][c] if b < LATO else None
            if lett:
                if inizio is None:
                    inizio = (r, c)
                seq += lett
            else:
                if len(seq) >= 2:
                    out[inizio] = seq
                seq, inizio = "", None
    return out


def verifica(g: Griglia, parole: list[str]) -> None:
    """Rilegge la griglia da zero: ogni sequenza è una parola, ogni parola c'è."""
    trovate = {}
    for d in (H, V):
        for (r, c), seq in sequenze(g.lettere, d).items():
            assert seq in parole, f"sequenza {seq!r} in {r},{c} non è una parola dell'elenco"
            assert seq not in trovate, f"parola {seq!r} presente due volte"
            trovate[seq] = (r, c, d)
    assert set(trovate) == set(parole), f"mancano {set(parole) - set(trovate)}"
    for p, pos in trovate.items():
        assert g.piazzate[p] == pos, f"{p}: posizione {pos} ≠ piazzata {g.piazzate[p]}"
    # ogni parola incrocia almeno un'altra (griglia connessa)
    for p, (r, c, d) in trovate.items():
        dr, dc = (0, 1) if d == H else (1, 0)
        assert any(len(g.dirs[r + dr * i][c + dc * i]) == 2 for i in range(len(p))), f"{p} isolata"


def numerazione(g: Griglia) -> tuple[dict[tuple[int, int], int], dict[str, int]]:
    """Numero progressivo (sinistra→destra, alto→basso) a ogni casella iniziale."""
    inizi = {}
    for d in (H, V):
        for (r, c), seq in sequenze(g.lettere, d).items():
            inizi.setdefault((r, c), []).append(seq)
    numeri, per_parola, n = {}, {}, 0
    for r in range(LATO):
        for c in range(LATO):
            if (r, c) in inizi:
                n += 1
                numeri[(r, c)] = n
                for seq in inizi[(r, c)]:
                    per_parola[seq] = n
    return numeri, per_parola


def scegli() -> Griglia:
    parole = [p for p, _, _ in PAROLE]
    assert len(set(parole)) == len(parole), "parole duplicate"
    assert all(p.isalpha() and p.isupper() for p in parole), "solo lettere maiuscole"
    candidati = []
    for seme in SEMI:
        g = cerca(parole, seme)
        if g is not None:
            verifica(g, parole)
            candidati.append((g.incroci, -seme, g))
            if len(candidati) >= MAX_CANDIDATI:
                break
    if not candidati:
        sys.exit("Nessuna griglia trovata: riduci o cambia le parole in PAROLE.")
    candidati.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return candidati[0][2]


def testo_griglia(g: Griglia, numeri: dict[tuple[int, int], int]) -> str:
    righe = []
    for r in range(LATO):
        celle = []
        for c in range(LATO):
            if g.lettere[r][c] is None:
                celle.append('<div class="cella nera"></div>')
            elif (r, c) in numeri:
                celle.append(f'<div class="cella"><span class="num">{numeri[(r, c)]}</span></div>')
            else:
                celle.append('<div class="cella"></div>')
        righe.append(f"      <!-- Riga {r + 1} -->\n      " + "".join(celle))
    return "\n".join(righe)


def testo_elenco(voci: list[tuple[int, str]]) -> str:
    return "\n".join(
        f'          <li value="{n}">{html.escape(defi, quote=False)}</li>' for n, defi in voci)


def costruisci() -> str:
    g = scegli()
    numeri, per_parola = numerazione(g)
    definizioni = {p: d for p, d, _ in PAROLE}
    orizz = sorted((per_parola[p], p) for p, (_, _, d) in g.piazzate.items() if d == H)
    vert = sorted((per_parola[p], p) for p, (_, _, d) in g.piazzate.items() if d == V)
    sigle = [p for p, _, t in PAROLE if t == "sigla"]
    n_tot = len(PAROLE)

    sol_o = ", ".join(f"{n}={p}" for n, p in orizz)
    sol_v = ", ".join(f"{n}={p}" for n, p in vert)
    aria = (f"Schema del cruciverba: {LATO} colonne per {LATO} righe, {n_tot} parole, "
            f"{len(orizz)} orizzontali e {len(vert)} verticali")

    return f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scheda stampabile: Cruciverba Protezione Civile — Secondaria I</title>
  <link rel="canonical" href="https://www.protezionecivilegenzano.it/formazione/schede-stampabili/cruciverba-secondaria/">
  <meta name="description" content="Scheda fotocopiabile per la Secondaria I. Cruciverba {LATO}×{LATO} con {n_tot} definizioni di Protezione Civile (sigle, fenomeni, ruoli), risolvibile con il glossario del sito.">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
    .crucibox {{
      display: grid; grid-template-columns: repeat({LATO}, 1.45rem);
      gap: 0; margin: 0.4rem auto; justify-content: center;
    }}
    .crucibox .cella {{
      width: 1.45rem; height: 1.45rem; border: 1.5px solid #333;
      display: flex; align-items: flex-start; justify-content: flex-start;
      font-size: 0.62rem; padding: 1px; position: relative; background: #fff;
    }}
    .crucibox .cella.nera {{ background: #333; border-color: #333; }}
    .crucibox .cella .num {{ position: absolute; top: 0; left: 2px; font-weight: 700; color: #003366; font-size: 0.52rem; line-height: 1.1; }}
    .definizioni {{
      display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem;
      margin: 0.5rem 0 0; font-size: 0.8rem; line-height: 1.4;
    }}
    .definizioni h3 {{ font-size: 0.92rem; color: var(--scheda-blu); margin: 0 0 0.25rem; }}
    .definizioni ol {{ padding-left: 1.5rem; margin: 0; }}
    .definizioni li {{ margin-bottom: 0.15rem; padding-left: 0.1rem; }}
    .definizioni li::marker {{ font-weight: 700; color: var(--scheda-blu); }}
    .istruzioni-prof {{
      margin-top: 0.6rem; padding: 0.45rem 0.8rem;
      background: #fff8e6; border-left: 4px solid var(--scheda-oro);
      border-radius: 0 6px 6px 0; font-size: 0.8rem; color: #664d03; line-height: 1.4;
    }}
    .risorse {{
      background: #eaf2fb; border-left: 4px solid var(--scheda-blu); padding: 0.4rem 0.8rem;
      border-radius: 0 8px 8px 0; margin: 0.3rem 0; font-size: 0.82rem; line-height: 1.45;
    }}
    .soluzione-capovolta.cruci-soluzione {{ margin-top: 4mm; }}
    /* Stampa: tutto su un solo foglio A4. L'area utile è 28,7 cm (margini
       @page di 5 mm, rule 09 § 15-ter): la scheda a corpo pieno ne occupava
       ~35. Si stringono margini interni, caselle e corpo delle definizioni,
       lasciando spazio per i font di sistema più larghi. */
    @media print {{
      .scheda-page {{ padding: 6mm 9mm 4mm; }}
      .scheda-page .scheda-header {{ padding-bottom: 0.25rem; margin-bottom: 0.3rem; }}
      .scheda-page .scheda-meta {{ padding: 0.25rem 0.6rem; font-size: 0.7rem; margin: 0.25rem 0; }}
      .scheda-page .scheda-intro {{ font-size: 0.76rem; line-height: 1.3; margin: 0.25rem 0; }}
      .scheda-page .risorse {{ font-size: 0.72rem; line-height: 1.3; padding: 0.25rem 0.6rem; }}
      .scheda-page .crucibox {{ grid-template-columns: repeat({LATO}, 1.22rem); margin: 0.25rem auto; }}
      .scheda-page .crucibox .cella {{ width: 1.22rem; height: 1.22rem; }}
      .scheda-page .definizioni {{ font-size: 0.7rem; line-height: 1.24; margin-top: 0.25rem; }}
      .scheda-page .definizioni li {{ margin-bottom: 0; }}
      .scheda-page .istruzioni-prof {{ font-size: 0.68rem; line-height: 1.28; margin-top: 0.3rem; padding: 0.25rem 0.6rem; }}
      .scheda-page .soluzione-capovolta.cruci-soluzione {{ margin-top: 1.5mm; padding: 1.5mm 3mm; font-size: 0.68rem; line-height: 1.3; }}
    }}
    @media (max-width: 580px) {{ .definizioni {{ grid-template-columns: 1fr; }} .crucibox {{ grid-template-columns: repeat({LATO}, 1.3rem); }} .crucibox .cella {{ width: 1.3rem; height: 1.3rem; font-size: 0.55rem; }} }}
  </style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/">← Torna alle schede</a>
    <span class="scheda-titolo">Cruciverba PC — Secondaria I</span>
    <button type="button" onclick="window.print()">🖨️ Stampa o salva come PDF</button>
  </div>

  <article class="scheda-page">
    <header class="scheda-header">
      <div class="scheda-logo" aria-hidden="true">PC</div>
      <div class="scheda-intestazione">
        <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
        <h1 class="scheda-titolo-principale">Cruciverba di Protezione Civile</h1>
        <div class="scheda-sottotitolo">Scheda fotocopiabile — Secondaria di primo grado (11-13 anni)</div>
      </div>
    </header>

    <div class="scheda-meta">
      <span><strong>Destinatari:</strong> 11-13 anni</span>
      <span><strong>Obiettivo:</strong> consolidare il lessico tecnico (sigle, fenomeni, ruoli)</span>
      <span><strong>Discipline:</strong> italiano, scienze, educazione civica</span>
    </div>

    <p class="scheda-intro">
      Cruciverba con <strong>{n_tot} definizioni tecniche</strong> di Protezione Civile: sigle istituzionali, fenomeni geofisici, concetti del sistema. Scrivi una lettera per casella, in stampatello maiuscolo; le caselle nere separano le parole. Se una risposta non ti viene, cercala nel <a href="/glossario/">glossario del sito</a>.
    </p>

    <div class="risorse">
      <strong style="color: var(--scheda-blu);">🧩 Risorse per risolverlo:</strong> oltre al glossario, le pagine <a href="/rischi-prevenzione/">/rischi-prevenzione/</a> e <a href="/conoscere/">/conoscere/</a>. Le sigle in gioco: <strong>{", ".join(sigle)}</strong>. Le altre risposte sono fenomeni e concetti che trovi nelle stesse pagine.
    </div>

    <div class="crucibox" role="img" aria-label="{aria}">
{testo_griglia(g, numeri)}
    </div>

    <div class="definizioni">
      <div>
        <h3>→ ORIZZONTALI</h3>
        <ol>
{testo_elenco([(n, definizioni[p]) for n, p in orizz])}
        </ol>
      </div>
      <div>
        <h3>↓ VERTICALI</h3>
        <ol>
{testo_elenco([(n, definizioni[p]) for n, p in vert])}
        </ol>
      </div>
    </div>

    <div class="istruzioni-prof">
      <strong>Per il/la prof · Note didattiche:</strong>
      <ul style="margin:0.25rem 0 0 1rem; padding:0;">
        <li>Ogni definizione riprende una voce del <a href="/glossario/">glossario del sito</a>: si può risolvere in classe con il glossario aperto (lettura e ricerca) oppure a libro chiuso, come verifica del lessico. Le <strong>soluzioni sono in fondo alla scheda, capovolte</strong>: gira il foglio.</li>
        <li><strong>Estensione</strong>: <a href="/formazione/schede-stampabili/cruciverba-primaria/">Cruciverba (Primaria)</a> per il livello base e <a href="/formazione/schede-stampabili/cruciverba-secondaria2/">Glossario commentato (Secondaria II)</a> per la versione approfondita.</li>
      </ul>
    </div>

    <div class="soluzione-capovolta cruci-soluzione">
      <span class="titolo">Soluzioni (capovolte — per il docente: gira il foglio)</span>
      <p style="margin: 0;"><strong>Orizzontali</strong>: {sol_o}.<br>
      <strong>Verticali</strong>: {sol_v}.</p>
    </div>

    <footer class="scheda-footer">
      <span class="scheda-site">protezionecivilegenzano.it</span>
      <span>Scheda "Cruciverba PC tecnico" · Secondaria I · italiano/scienze · {REV}</span>
    </footer>
  </article>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    doc = costruisci()
    if "--check" in argv:
        attuale = USCITA.read_text(encoding="utf-8") if USCITA.exists() else ""
        if attuale != doc:
            print(f"NON aggiornato: {USCITA.relative_to(USCITA.parents[4])} — rigenera con questo script")
            return 1
        print("Scheda aggiornata.")
        return 0
    USCITA.parent.mkdir(parents=True, exist_ok=True)
    USCITA.write_text(doc, encoding="utf-8")
    print(f"Scritto {USCITA}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
