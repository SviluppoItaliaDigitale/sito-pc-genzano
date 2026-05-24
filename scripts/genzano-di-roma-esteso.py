#!/usr/bin/env python3
"""
Estende "Genzano" -> "Genzano di Roma" sui contenuti, in modo CONSERVATIVO:

  - frontmatter: nei campi `title:` e `description:` (i "titoli")
  - corpo: SOLO la prima occorrenza per file (disambiguazione una volta per pagina)

Sicurezze:
  - lookahead negativo: non tocca "Genzano di Roma" né "Genzano di Lucania"
  - match solo su "Genzano" con G maiuscola e confine di parola: domini
    (protezionecivilegenzano.it), email, slug e path usano "genzano" minuscolo
    e non vengono toccati
  - salta i blocchi di codice fenced (``` ... ```) nel corpo

Uso:
  python3 scripts/genzano-di-roma-esteso.py --dry-run   # mostra cosa cambierebbe
  python3 scripts/genzano-di-roma-esteso.py             # applica
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# titoli/description: qualsiasi "Genzano" isolato (campi curati, sicuri)
RE_GZ = re.compile(r'\bGenzano\b(?! di Roma)(?! di Lucania)')
# corpo: SOLO in contesto geografico (preposizione + Genzano), per non toccare
# nomi propri tipo "CB Genzano", "PC Genzano", "Croce ... Genzano".
RE_BODY = re.compile(
    r'\b([Aa]|[Dd]i|[Dd]a|[Ss]u|[Pp]er|[Tt]ra|[Ff]ra|[Ii]n|[Nn]el(?:lo|la)?|'
    r'[Dd]el(?:lo|la)?|[Aa]l(?:lo|la)?|[Dd]al(?:lo|la)?|[Ss]ul(?:la)?|[Pp]resso|[Vv]erso) '
    r'Genzano\b(?! di Roma)(?! di Lucania)')
DRY = "--dry-run" in sys.argv


def split_fm(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[:end + 5], text[end + 5:]
    return "", text


def process(text):
    fm, body = split_fm(text)
    changes = 0

    # frontmatter: title + description
    def fm_line(m):
        nonlocal changes
        key, val = m.group(1), m.group(2)
        new = RE_GZ.sub("Genzano di Roma", val)
        if new != val:
            changes_local = len(RE_GZ.findall(val))
            return key + new, changes_local
        return m.group(0), 0
    if fm:
        out_lines = []
        for line in fm.split("\n"):
            m = re.match(r'^(title:\s*|description:\s*)(.*)$', line)
            if m:
                new_val = RE_GZ.sub("Genzano di Roma", m.group(2))
                if new_val != m.group(2):
                    changes += len(RE_GZ.findall(m.group(2)))
                    line = m.group(1) + new_val
            out_lines.append(line)
        fm = "\n".join(out_lines)

    # corpo: solo la PRIMA occorrenza in contesto geografico, saltando i code block
    parts = re.split(r'(```.*?```)', body, flags=re.DOTALL)
    done = False
    for i, p in enumerate(parts):
        if done or p.startswith("```"):
            continue
        new_p, n = RE_BODY.subn(r'\1 Genzano di Roma', p, count=1)
        if n:
            parts[i] = new_p
            changes += 1
            done = True
    body = "".join(parts)

    return fm + body, changes


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "content", "**", "*.md"), recursive=True))
    tot_files = 0
    tot_changes = 0
    sample = []
    for f in files:
        text = open(f, encoding="utf-8").read()
        new, ch = process(text)
        if ch:
            tot_files += 1
            tot_changes += ch
            if not DRY:
                open(f, "w", encoding="utf-8").write(new)
            elif len(sample) < 8:
                # primo cambiamento del file, per anteprima
                rel = os.path.relpath(f, ROOT)
                sample.append(rel)
    print(f"{'[DRY-RUN] ' if DRY else ''}File modificati: {tot_files} · sostituzioni: {tot_changes}")
    if DRY and sample:
        print("Esempi di file:")
        for s in sample:
            print("  -", s)


if __name__ == "__main__":
    main()
