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

/* ---------- Catalogo: cerca e gruppi ----------
   Senza JavaScript il catalogo resta intero, diviso per gruppi. Con JavaScript compaiono il campo di
   ricerca e i pulsanti dei gruppi (aria-pressed); il numero degli oggetti mostrati si annuncia. */
const filtri = document.querySelector('[data-s3d="filtri"]');
if (filtri) {
  const cerca = document.getElementById('s3d-cerca');
  const chip = Array.from(filtri.querySelectorAll('[data-s3d-filtro]'));
  const conteggio = filtri.querySelector('[data-s3d="conteggio"]');
  const nessuno = document.querySelector('[data-s3d="nessuno"]');
  const voci = Array.from(document.querySelectorAll('.s3d-voce'));
  const gruppi = Array.from(document.querySelectorAll('[data-s3d-gruppo]'));
  let gruppo = '';
  const norm = t => String(t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim();
  function filtra() {
    const parole = norm(cerca.value).split(/\s+/).filter(Boolean);
    let n = 0;
    voci.forEach(li => {
      const testo = norm(li.dataset.s3dTesto);
      const si = (!gruppo || li.dataset.s3dCat === gruppo) && parole.every(p => testo.indexOf(p) >= 0);
      li.hidden = !si;
      if (si) n++;
    });
    gruppi.forEach(ul => {
      const vuoto = !ul.querySelector('.s3d-voce:not([hidden])');
      ul.hidden = vuoto;
      const titolo = ul.previousElementSibling;
      if (titolo && /^H[2-3]$/.test(titolo.tagName)) titolo.hidden = vuoto;
    });
    if (nessuno) nessuno.hidden = n > 0;
    conteggio.textContent = n === voci.length ? `${n} oggetti.` : `${n} ${n === 1 ? 'oggetto' : 'oggetti'} su ${voci.length}.`;
  }
  chip.forEach(b => b.addEventListener('click', () => {
    gruppo = b.dataset.s3dFiltro;
    chip.forEach(c => c.setAttribute('aria-pressed', c === b ? 'true' : 'false'));
    filtra();
  }));
  cerca.addEventListener('input', filtra);
  filtri.hidden = false;
  filtra();
}

/* ---------- Pagina di un oggetto: schede ----------
   Le sezioni (data-s3d-titolo) diventano schede con il modello ARIA «tablist»: frecce, Inizio e Fine
   per spostarsi. Un collegamento a #come-stamparlo o con data-s3d-vai apre la scheda giusta.
   In stampa le sezioni tornano tutte visibili (CSS). */
const schede = document.querySelector('[data-s3d="schede"]');
if (schede) {
  const sezioni = Array.from(schede.querySelectorAll('[data-s3d-titolo]'));
  const lista = document.createElement('div');
  lista.className = 's3d-tab d-print-none';
  lista.setAttribute('role', 'tablist');
  lista.setAttribute('aria-label', 'Informazioni sull\'oggetto');
  const tab = sezioni.map((s, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.id = `s3d-tab-${s.id}`;
    b.className = 's3d-tab-voce';
    b.setAttribute('role', 'tab');
    b.setAttribute('aria-controls', s.id);
    b.textContent = s.dataset.s3dTitolo;
    s.setAttribute('role', 'tabpanel');
    s.setAttribute('aria-labelledby', b.id);
    s.setAttribute('tabindex', '0');
    const h = s.querySelector('h2');
    if (h) h.classList.add('visually-hidden');
    b.addEventListener('click', () => apri(i, false));
    lista.appendChild(b);
    return b;
  });
  function apri(i, fuoco) {
    tab.forEach((b, k) => {
      const si = k === i;
      b.setAttribute('aria-selected', si ? 'true' : 'false');
      b.tabIndex = si ? 0 : -1;
      sezioni[k].hidden = !si;
    });
    if (fuoco) tab[i].focus();
  }
  lista.addEventListener('keydown', ev => {
    const i = tab.indexOf(document.activeElement);
    if (i < 0) return;
    let j = null;
    if (ev.key === 'ArrowRight') j = (i + 1) % tab.length;
    else if (ev.key === 'ArrowLeft') j = (i - 1 + tab.length) % tab.length;
    else if (ev.key === 'Home') j = 0;
    else if (ev.key === 'End') j = tab.length - 1;
    if (j === null) return;
    ev.preventDefault();
    apri(j, true);
  });
  schede.insertBefore(lista, schede.firstChild);
  schede.classList.add('s3d-schede-attive');
  const daHash = () => sezioni.findIndex(s => `#${s.id}` === location.hash);
  apri(Math.max(0, daHash()), false);
  window.addEventListener('hashchange', () => { const i = daHash(); if (i >= 0) apri(i, false); });
  document.addEventListener('click', ev => {
    const a = ev.target.closest('a[href^="#"]');
    if (!a) return;
    const i = sezioni.findIndex(s => `#${s.id}` === a.getAttribute('href'));
    if (i < 0) return;
    ev.preventDefault();
    apri(i, false);
    const fermo = matchMedia('(prefers-reduced-motion: reduce)').matches || document.documentElement.classList.contains('a11y-pause-anim');
    lista.scrollIntoView({ block: 'start', behavior: fermo ? 'auto' : 'smooth' });
    tab[i].focus({ preventScroll: true });
  });
  window.addEventListener('beforeprint', () => sezioni.forEach(s => { s.hidden = false; }));
  window.addEventListener('afterprint', () => apri(Math.max(0, tab.findIndex(b => b.getAttribute('aria-selected') === 'true')), false));
}
