/*
  Stampa 3D con il nominativo (/stampa-3d/ e /stampa-3d/<oggetto>/).
  Il volontario scrive il numero del suo nominativo: il sito lo ricorda nel browser e lo usa in tutte
  le pagine. Nel catalogo cambia immagini e collegamenti; nella pagina di un oggetto mostra il file
  vero in 3D (si gira da ogni lato con dito, mouse, tastiera o pulsanti) e il pulsante per scaricarlo.
  Dati dallo shortcode stampa3d (blocco JSON #s3d-dati, da data/stampa_3d.yaml).
  La vista in 3D è in stampa3d-vista.js, caricato solo nelle pagine degli oggetti. Sintassi entro
  ECMAScript 2018 (browser delle LIM). Nessuna richiesta fuori dal sito; nel browser resta solo il
  numero del nominativo (chiave pcgenzano-stampa3d-nominativo, elencata nell'informativa privacy).
*/
const DATI = JSON.parse(document.getElementById('s3d-dati').textContent);
const CHIAVE = 'pcgenzano-stampa3d-nominativo';
const form = document.querySelector('[data-s3d="form"]');
const campo = document.getElementById('s3d-numero');
const errore = document.getElementById('s3d-errore');
const stato = document.querySelector('[data-s3d="stato"]');
const pref = DATI.prefisso.toLowerCase();

const nome3 = n => String(n).padStart(3, '0');
const percorso = (id, n, est) => `${DATI.base}${id}/${pref}-${nome3(n)}.${est}`;

function leggiNumero(testo) {
  const m = String(testo).match(/\d+/);
  if (!m) return null;
  const n = parseInt(m[0], 10);
  return n >= DATI.primo && n <= DATI.ultimo ? n : NaN;
}
function ricorda(n) { try { localStorage.setItem(CHIAVE, String(n)); } catch (e) { /* memoria del browser non disponibile */ } }
function ricordato() {
  try { const n = leggiNumero(localStorage.getItem(CHIAVE) || ''); return n && !Number.isNaN(n) ? n : null; } catch (e) { return null; }
}
function dimentica() { try { localStorage.removeItem(CHIAVE); } catch (e) { /* niente da togliere */ } }

function mostraErrore(msg) {
  errore.textContent = msg;
  campo.setAttribute('aria-invalid', msg ? 'true' : 'false');
}

/* Riga sotto il campo: quale nominativo si sta usando e come toglierlo. */
function scriviStato(n) {
  stato.textContent = '';
  if (!n) return;
  stato.append(`Stai usando il nominativo ${DATI.prefisso} ${n}, ricordato su questo dispositivo. `);
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'btn btn-link p-0 align-baseline s3d-dimentica';
  b.textContent = 'Non ricordarlo più';
  b.addEventListener('click', () => {
    dimentica();
    campo.value = '';
    applica(null);
    stato.textContent = 'Il nominativo non è più ricordato su questo dispositivo.';
    campo.focus();
  });
  stato.append(b);
}

/* ---------- Catalogo ---------- */

function applicaCatalogo(n) {
  const num = n || DATI.primo;
  document.querySelectorAll('[data-s3d-miniatura]').forEach(img => {
    img.src = percorso(img.dataset.s3dMiniatura, num, 'webp');
  });
  document.querySelectorAll('[data-s3d-voce]').forEach(a => {
    const base = a.getAttribute('href').split('#')[0];
    a.setAttribute('href', n ? `${base}#${pref}-${n}` : base);
  });
}

/* ---------- Pagina di un oggetto ---------- */

const O = DATI.oggetto;
const vista = O && { img: document.querySelector('[data-s3d="immagine"]') };

function applicaOggetto(n) {
  const num = n || DATI.primo;
  const nominativo = `${DATI.prefisso} ${num}`;
  document.querySelectorAll('[data-s3d="nominativo"]').forEach(e => { e.textContent = nominativo; });
  document.querySelectorAll('[data-s3d="esempio"]').forEach(e => { e.hidden = !!n; });
  vista.img.src = percorso(O.id, num, 'webp');
  vista.img.alt = `${O.nome} con il nominativo ${nominativo}${n ? '' : ', come esempio'}.`;
  const box = document.querySelector('[data-s3d="scarica-box"]');
  const vuoto = document.querySelector('[data-s3d="scarica-vuoto"]');
  if (box) {
    box.hidden = !n;
    if (vuoto) vuoto.hidden = !!n;
    if (n) {
      const file = `${DATI.prefisso}-${n}-${O.id}.stl`;
      const a = box.querySelector('[data-s3d="scarica"]');
      a.href = percorso(O.id, n, 'stl');
      a.setAttribute('download', file);
      box.querySelectorAll('[data-s3d="file"]').forEach(e => { e.textContent = file; });
    }
  }
  // la vista in 3D (stampa3d-vista.js) prende il file da qui
  window.pcgzS3dFile = percorso(O.id, num, 'stl');
  document.dispatchEvent(new CustomEvent('s3d:file', { detail: window.pcgzS3dFile }));
}

function applica(n) {
  scriviStato(n);
  if (DATI.pagina === 'catalogo') applicaCatalogo(n);
  else applicaOggetto(n);
  try {
    history.replaceState(null, '', n ? `#${pref}-${n}` : location.pathname + location.search);
  } catch (e) { /* indirizzo non modificabile */ }
}

form.addEventListener('submit', ev => {
  ev.preventDefault();
  const n = leggiNumero(campo.value);
  if (n === null) { mostraErrore('Scrivi il numero del tuo nominativo, per esempio 57.'); campo.focus(); return; }
  if (Number.isNaN(n)) { mostraErrore(`Non c'è questo numero. Scrivi un numero da ${DATI.primo} a ${DATI.ultimo}.`); campo.focus(); return; }
  mostraErrore('');
  ricorda(n);
  applica(n);
});

/* ---------- Avvio: nominativo dall'indirizzo (#alfa-57, condivisibile) o dalla memoria ---------- */
const daIndirizzo = location.hash.match(new RegExp(`^#${pref}-(\\d+)$`));
let iniziale = null;
if (daIndirizzo) {
  const n = leggiNumero(daIndirizzo[1]);
  if (n && !Number.isNaN(n)) { iniziale = n; ricorda(n); }
}
if (!iniziale) iniziale = ricordato();
if (iniziale) campo.value = String(iniziale);
applica(iniziale);
