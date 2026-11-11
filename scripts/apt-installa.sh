#!/usr/bin/env bash
# Installa pacchetti Ubuntu sui runner di GitHub anche quando i server di Ubuntu non rispondono.
# Prova nell'ordine: server predefiniti → mirror alternativi fuori da ubuntu.com → pacchetti .deb già conservati in $APT_DEB_CACHE.
#
# Uso:  bash scripts/apt-installa.sh [opzioni di apt-get install] pacchetto...
#       bash scripts/apt-installa.sh --solo-mirror
# Le opzioni di apt-get vanno in un solo argomento (per esempio --no-install-recommends): un'opzione col valore
# separato (-o X) finirebbe fra i pacchetti.
# --solo-mirror non installa niente: se i server predefiniti non rispondono passa ai mirror alternativi,
# così i passi successivi che usano apt da soli (per esempio `playwright install --with-deps`) trovano un server.
# Tempo massimo complessivo: $APT_TEMPO_MASSIMO secondi (predefiniti 900, e 300 con --solo-mirror), da tenere
# sotto il tempo massimo del job o del passo che chiama lo script.
# Esce con 0 se i pacchetti sono installati, con 1 se tutte le strade falliscono, con 2 se l'uso è sbagliato;
# con --solo-mirror esce sempre con 0.
# Se c'è $GITHUB_OUTPUT scrive fonte=server-predefiniti|mirror-alternativo|cache|nessuna|solo-mirror e
# deb=<numero di .deb conservati>, per decidere se salvare la cache.
#
# Nato l'11/11/2026: dalle 15 i runner non risolvevano archive.ubuntu.com, azure.archive.ubuntu.com e
# security.ubuntu.com; per ore ogni deploy si è fermato su apt-get (codice 100), e con il deploy anche
# i controlli delle PR e la lettura dei PDF dell'allerta regionale (pdftotext non installabile).
set -uo pipefail

CACHE="${APT_DEB_CACHE:-$HOME/.cache/apt-deb}"
MIRROR_ALTERNATIVI=(
  "https://mirrors.edge.kernel.org/ubuntu/"
  "https://mirror.init7.net/ubuntu/"
  "https://ftp.halifax.rwth-aachen.de/ubuntu/"
)

SOLO_MIRROR=0
OPZIONI_INSTALL=()
PACCHETTI=()
for a in "$@"; do
  case "$a" in
    --solo-mirror) SOLO_MIRROR=1 ;;
    -*) OPZIONI_INSTALL+=("$a") ;;
    *) PACCHETTI+=("$a") ;;
  esac
done
if [ "$SOLO_MIRROR" -eq 0 ] && [ "${#PACCHETTI[@]}" -eq 0 ]; then
  echo "Uso: $0 [opzioni di apt-get install] pacchetto...  |  $0 --solo-mirror" >&2
  exit 2
fi
if [ "$SOLO_MIRROR" -eq 1 ]; then
  TEMPO_MASSIMO="${APT_TEMPO_MASSIMO:-300}"
else
  TEMPO_MASSIMO="${APT_TEMPO_MASSIMO:-900}"
fi

mkdir -p "$CACHE/partial"
APT_OPZ=(-o Acquire::Retries=3 -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30
         -o "Dir::Cache::archives=$CACHE" -o APT::Keep-Downloaded-Packages=true)
LOG="$(mktemp)"
trap 'rm -f "$LOG"' EXIT

# Quote del tempo: un server che resta appeso non può consumare il tempo dei ripieghi (revisione
# dell'11/11/2026: con 240 secondi un primo update bloccato li usava tutti e a mirror e cache restava 1
# secondo). Server predefiniti fino al 40%, mirror alternativi fino all'80%, cache fino alla fine.
FINE_PREDEFINITI=$(( TEMPO_MASSIMO * 2 / 5 ))
FINE_MIRROR=$(( TEMPO_MASSIMO * 4 / 5 ))
FINE_FASE=$TEMPO_MASSIMO

resto() {
  # Secondi concessi a un passo: il suo massimo, mai oltre la fine della fase in corso (almeno 1: il passo fallisce subito).
  local r=$(( FINE_FASE - SECONDS ))
  [ "$r" -gt "$1" ] && r="$1"
  [ "$r" -lt 1 ] && r=1
  echo "$r"
}

fine() {
  # La cache resta leggibile dall'utente del runner, che la salva con actions/cache.
  sudo rm -rf "$CACHE/partial" "$CACHE/lock" 2>/dev/null || true
  sudo chown -R "$(id -u):$(id -g)" "$CACHE" 2>/dev/null || true
  if [ -n "${GITHUB_OUTPUT:-}" ]; then
    echo "fonte=$1" >> "$GITHUB_OUTPUT"
    echo "deb=$(find "$CACHE" -maxdepth 1 -name '*.deb' | wc -l)" >> "$GITHUB_OUTPUT"
  fi
}

aggiorna() {
  # L'esito vero lo dà l'installazione: un update che fallisce solo per un repository di terzi non deve fermare nulla.
  sudo dpkg --configure -a >/dev/null 2>&1 || true
  timeout "$(resto 300)" sudo apt-get "${APT_OPZ[@]}" update -q >"$LOG" 2>&1
  local rc=$?
  grep -E '^(Err:|W:|E:)' "$LOG" | head -n 8
  tail -n 2 "$LOG"
  return "$rc"
}

errori_di_rete() {
  # Errori di rete nell'ultimo update; con un argomento, solo quelli che lo contengono (per esempio ubuntu.com).
  grep -E "^Err:|Temporary failure resolving|Could not resolve|Could not connect|Cannot initiate the connection|Unable to connect|Failed to fetch|[Cc]onnection timed out" "$LOG" \
    | grep -qF -- "${1:-}"
}

errori_sui_mirror() {
  local m h
  for m in "${MIRROR_ALTERNATIVI[@]}"; do
    h="${m#*://}"
    errori_di_rete "${h%%/*}" && return 0
  done
  return 1
}

installa() {
  timeout "$(resto 600)" sudo env DEBIAN_FRONTEND=noninteractive \
    apt-get "${APT_OPZ[@]}" install -y -q "${OPZIONI_INSTALL[@]}" "${PACCHETTI[@]}"
}

usa_mirror_alternativi() {
  # I runner leggono i server da /etc/apt/apt-mirrors.txt (metodo mirror+file) per tutte le sezioni,
  # sicurezza compresa: basta sostituire l'elenco. I mirror servono gli stessi file firmati da Ubuntu.
  if [ -f /etc/apt/apt-mirrors.txt ] \
     && grep -rqsF 'mirror+file:/etc/apt/apt-mirrors.txt' /etc/apt/sources.list /etc/apt/sources.list.d/; then
    [ -f /etc/apt/apt-mirrors.txt.originale ] || sudo cp /etc/apt/apt-mirrors.txt /etc/apt/apt-mirrors.txt.originale
    local i=1 m
    for m in "${MIRROR_ALTERNATIVI[@]}"; do
      printf '%s\tpriority:%d\n' "$m" "$i"
      i=$((i + 1))
    done | sudo tee /etc/apt/apt-mirrors.txt >/dev/null
  else
    # Altrove: sorgenti deb822 sul primo mirror al posto di quelle di Ubuntu (copia in ubuntu.sources.originale).
    local codename
    codename="$(. /etc/os-release && echo "${VERSION_CODENAME:-}")"
    [ -n "$codename" ] || return 1
    if [ -f /etc/apt/sources.list.d/ubuntu.sources ]; then
      sudo mv /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.originale
    fi
    printf 'Types: deb\nURIs: %s\nSuites: %s %s-updates %s-security\nComponents: main restricted universe multiverse\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n' \
      "${MIRROR_ALTERNATIVI[0]}" "$codename" "$codename" "$codename" \
      | sudo tee /etc/apt/sources.list.d/mirror-alternativo.sources >/dev/null
  fi
  echo "Server dei pacchetti: ${MIRROR_ALTERNATIVI[*]}"
}

installati() {
  local p
  for p in "${PACCHETTI[@]}"; do
    [ "$(dpkg-query -W -f='${Status}' "$p" 2>/dev/null)" = "install ok installed" ] || return 1
  done
}

installa_da_cache() {
  compgen -G "$CACHE/*.deb" >/dev/null || return 1
  timeout "$(resto 300)" sudo env DEBIAN_FRONTEND=noninteractive \
    apt-get "${APT_OPZ[@]}" install -y -q --no-download "${OPZIONI_INSTALL[@]}" "${PACCHETTI[@]}" && return 0
  # Senza gli elenchi dei pacchetti apt non sa usare la cache: dpkg installa i .deb conservati, senza mai
  # sostituire una versione più nuova già presente sull'immagine. L'esito lo dice il controllo che segue.
  timeout "$(resto 300)" sudo env DEBIAN_FRONTEND=noninteractive \
    dpkg -i --skip-same-version --refuse-downgrade "$CACHE"/*.deb || true
  installati
}

if [ "$SOLO_MIRROR" -eq 1 ]; then
  FINE_FASE=$(( TEMPO_MASSIMO / 2 ))
  aggiorna || true
  FINE_FASE=$TEMPO_MASSIMO
  if errori_di_rete ubuntu.com || [ "$SECONDS" -ge $(( TEMPO_MASSIMO / 2 )) ]; then
    echo "::warning::Server Ubuntu predefiniti non raggiungibili: passo ai mirror alternativi."
    if usa_mirror_alternativi; then
      aggiorna || true
      if errori_sui_mirror; then
        echo "::warning::Anche i mirror alternativi danno errori: i passi che usano apt potrebbero fallire."
      fi
    fi
  fi
  fine "solo-mirror"
  exit 0
fi

FINE_FASE=$FINE_PREDEFINITI
aggiorna || true
if installa; then
  sudo apt-get "${APT_OPZ[@]}" autoclean -q >/dev/null 2>&1 || true
  fine "server-predefiniti"
  exit 0
fi

echo "::warning::Pacchetti non installati dai server Ubuntu predefiniti: provo i mirror alternativi."
FINE_FASE=$FINE_MIRROR
if usa_mirror_alternativi && { aggiorna || true; installa; }; then
  echo "::notice::Pacchetti installati da un mirror alternativo: ${PACCHETTI[*]}"
  sudo apt-get "${APT_OPZ[@]}" autoclean -q >/dev/null 2>&1 || true
  fine "mirror-alternativo"
  exit 0
fi

echo "::warning::Mirror alternativi non raggiungibili: provo i pacchetti conservati in cache."
FINE_FASE=$TEMPO_MASSIMO
if installa_da_cache; then
  echo "::notice::Pacchetti installati dalla cache: ${PACCHETTI[*]}"
  fine "cache"
  exit 0
fi

echo "::error::Pacchetti non installati (${PACCHETTI[*]}): server Ubuntu, mirror alternativi e cache non disponibili."
fine "nessuna"
exit 1
