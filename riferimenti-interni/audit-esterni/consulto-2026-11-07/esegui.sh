#!/usr/bin/env bash
# Audit del sito del 07/11/2026, revisori del consulto: si esegue sul PC, dove stanno le chiavi gratuite dei servizi.
# Ogni revisore riceve richiesta.md e fascicolo.md; i rapporti vanno in riferimenti-interni/audit-esterni/ con una PR in bozza.
#
# Uso, dalla cartella del repository sito-pc-genzano (qualunque ramo sia aperto, la copia di lavoro non si tocca):
#   git fetch -q origin && bash <(git show origin/main:riferimenti-interni/audit-esterni/consulto-2026-11-07/esegui.sh)
# Per rifare solo alcuni revisori, le loro lettere in fondo: … esegui.sh) b j
# Dura fino a mezz'ora (i revisori lavorano insieme): in una sessione di Claude va lanciato in background.
set -euo pipefail

CARTELLA="riferimenti-interni/audit-esterni/consulto-2026-11-07"
RAMO="claude/audit-consulto-revisori-20261107"
declare -A SERVIZIO=([b]=gemini [e]=zai [h]=openrouter [i]=cloudflare [j]=cohere)
if [ $# -gt 0 ]; then LETTERE=("$@"); else LETTERE=(b e h i j); fi
for l in "${LETTERE[@]}"; do
  [ -n "${SERVIZIO[$l]:-}" ] || { echo "Revisore sconosciuto: $l (si può: ${!SERVIZIO[*]})."; exit 2; }
done

radice=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "Lancialo dalla cartella del repository sito-pc-genzano."; exit 2; }
case "$(git -C "$radice" remote get-url origin)" in
  *sito-pc-genzano*) ;;
  *) echo "Questa non è la copia del repository sito-pc-genzano."; exit 2 ;;
esac
command -v gh >/dev/null || { echo "Serve gh, con l'accesso a GitHub."; exit 2; }

git -C "$radice" fetch -q origin
git -C "$radice" worktree prune
tmp=$(mktemp -d "${TMPDIR:-/tmp}/audit-consulto-XXXXXX")
lavoro="$tmp/sito"
if git -C "$radice" rev-parse -q --verify "refs/remotes/origin/$RAMO" >/dev/null; then base="origin/$RAMO"; else base="origin/main"; fi
git -C "$radice" worktree add -q -B "$RAMO" "$lavoro" "$base"
pulizia() { git -C "$radice" worktree remove --force "$lavoro" 2>/dev/null || true; }
trap pulizia EXIT
for f in richiesta.md fascicolo.md rapporto.py; do
  [ -f "$lavoro/$CARTELLA/$f" ] || { echo "Manca $CARTELLA/$f su $base: la PR che lo porta non è ancora unita."; exit 1; }
done
( cd "$lavoro" && bash scripts/imposta-identita-git.sh >/dev/null )

chiedi() {   # un revisore: due tentativi, il secondo con una risposta più corta, dopo un minuto
  local l=$1 L codice=0 domanda
  L=$(printf '%s' "$l" | tr '[:lower:]' '[:upper:]')
  domanda=$(sed "s/<LETTERA>/$L/g" "$lavoro/$CARTELLA/richiesta.md")
  ( cd "$lavoro/$CARTELLA" && CONSULTO_ATTESA=900 CONSULTO_MAX_TOKENS=16000 \
      python3 -I "$lavoro/scripts/consulto-ai.py" "${SERVIZIO[$l]}" "$domanda" --file fascicolo.md --json ) \
      >"$tmp/$l.json" 2>"$tmp/$l.err" || codice=$?
  if [ "$codice" -ne 0 ]; then
    sleep 60
    codice=0
    ( cd "$lavoro/$CARTELLA" && CONSULTO_ATTESA=900 CONSULTO_MAX_TOKENS=8000 \
        python3 -I "$lavoro/scripts/consulto-ai.py" "${SERVIZIO[$l]}" "$domanda" --file fascicolo.md --json ) \
        >"$tmp/$l.json" 2>>"$tmp/$l.err" || codice=$?
  fi
  if [ "$codice" -ne 0 ]; then { cat "$tmp/$l.json"; tail -n 3 "$tmp/$l.err"; } >"$tmp/$l.motivo"; fi
  echo "$codice" >"$tmp/$l.codice"
}

echo "Revisori al lavoro: ${LETTERE[*]^^} (fino a mezz'ora)…"
for l in "${LETTERE[@]}"; do chiedi "$l" & done
wait

coppie=()
for l in "${LETTERE[@]}"; do
  coppie+=("$l:${SERVIZIO[$l]}")
  if [ "$(cat "$tmp/$l.codice")" = 0 ]; then
    python3 -I "$lavoro/$CARTELLA/rapporto.py" scrivi "$l" "$tmp/$l.json" \
      "$lavoro/riferimenti-interni/audit-esterni/2026-11-07-audit-completo-revisore-$l.md" >"$tmp/$l.esito" || true
  fi
done
if ! python3 -I "$lavoro/$CARTELLA/rapporto.py" riepilogo "$tmp" "${coppie[@]}"; then
  echo "Nessun rapporto da pubblicare. Risposte e messaggi in $tmp (file .json, .err, .motivo)."
  exit 1
fi
python3 -I "$lavoro/$CARTELLA/rapporto.py" bacheca "$lavoro/COORDINAMENTO.md" "$tmp/esito-bacheca.md" || true

cd "$lavoro"
mapfile -t fatti <"$tmp/file-fatti.txt"
git add -- "${fatti[@]}" COORDINAMENTO.md
lettere_fatte=$(for f in "${fatti[@]}"; do f=${f##*-revisore-}; printf '%s\n' "${f%.md}"; done \
  | tr '[:lower:]' '[:upper:]' | paste -sd, - | sed 's/,\([^,]*\)$/ e \1/; s/,/, /g')
case "$lettere_fatte" in *,* | *" e "*) cosa="rapporti dei revisori" ;; *) cosa="rapporto del revisore" ;; esac
git commit -q -m "Audit del sito: $cosa $lettere_fatte (consulto del 07/11/2026)" \
  -m "Rapporti scritti dai revisori sul fascicolo pubblico del sito, da verificare rilievo per rilievo prima di unire."
git push -q -u origin "$RAMO"
# API REST e non «gh pr»: funziona anche dove GraphQL non è disponibile (sessioni cloud)
url=$(gh api "repos/{owner}/{repo}/pulls?head=SviluppoItaliaDigitale:$RAMO&state=open" --jq '.[0].html_url // empty')
if [ -n "$url" ]; then
  echo "PR già aperta, aggiornata: $url"
else
  url=$(gh api "repos/{owner}/{repo}/pulls" -f base=main -f head="$RAMO" \
        -f title="Audit del sito: rapporti dei revisori del consulto" -F body=@"$tmp/corpo-pr.md" -F draft=true --jq .html_url)
  echo "PR in bozza: $url"
fi
cd "$radice"
pulizia
git -C "$radice" branch -q -D "$RAMO" 2>/dev/null || true
echo "Fatto. Il resto (verifica dei rilievi, esiti, unione) lo fa Claude."
