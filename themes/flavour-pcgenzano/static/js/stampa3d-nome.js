/*
  Nome e cognome sugli oggetti della stampa 3D (/stampa-3d/<oggetto>/, solo per gli oggetti con
  anteprima.nome in data/stampa_3d.yaml). Il file STL del nominativo si scarica, gli si aggiunge la riga
  con nome e cognome e si offre da scaricare il file nuovo: tutto su questo dispositivo, nulla viene
  inviato o salvato (niente localStorage, niente indirizzo). Le librerie (manifold-3d, opentype.js e il
  carattere Liberation Sans Bold, in vendor/stampa3d) si caricano solo al primo «Aggiungi».
  Collabora con stampa3d.js (evento «s3d:file» con il file del nominativo) e con stampa3d-vista.js
  (evento «s3d:geometria» con la forma nuova da mostrare). Eccezione dichiarata in check-sintassi-js:
  usa import() dinamico; senza, resta il file del solo nominativo.
*/
import { conNome, pulisci, MAX_CARATTERI } from './stampa3d-nome-core.js';

const DATI = JSON.parse(document.getElementById('s3d-dati').textContent);
const O = DATI.oggetto;
const box = document.querySelector('[data-s3d="nome-box"]');
const campo = document.getElementById('s3d-nome');
const bottone = document.querySelector('[data-s3d="nome-aggiungi"]');
const errore = document.getElementById('s3d-nome-errore');
const stato = document.querySelector('[data-s3d="nome-stato"]');
const scarica = document.querySelector('[data-s3d="scarica"]');
const conNomeTesto = document.querySelector('[data-s3d="con-nome"]');
const COSA = (box && box.dataset.s3dCosa) || 'nome e cognome';
const Cosa = COSA.charAt(0).toUpperCase() + COSA.slice(1);
const VENDOR = new URL('../vendor/stampa3d/', import.meta.url);

let librerie = null;          // promessa: { M, font }
let fileBase = '';            // file STL del solo nominativo (da stampa3d.js)
let nomeApplicato = '';       // nome e cognome nel file offerto ora
let blobUrl = '';
let giro = 0;
let ultimaForma = null;       // { pos, lato } del file con il nome, per rimostrarlo

function carica() {
  if (!librerie) {
    librerie = (async () => {
      const [{ default: Module }, opentype, ttf] = await Promise.all([
        import(new URL('manifold.js', VENDOR).href),
        import(new URL('opentype.min.mjs', VENDOR).href),
        fetch(new URL('LiberationSans-Bold.ttf', VENDOR)).then(r => { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); }),
      ]);
      const M = await Module({ locateFile: f => new URL(f, VENDOR).href });
      M.setup();
      return { M, font: opentype.parse(ttf) };
    })();
    librerie.catch(() => { librerie = null; });   // al prossimo tentativo si riprova
  }
  return librerie;
}

function scriviErrore(msg) {
  errore.textContent = msg;
  campo.classList.toggle('is-invalid', !!msg);
  if (msg) campo.setAttribute('aria-invalid', 'true'); else campo.removeAttribute('aria-invalid');
}

function nomeFile() {
  const m = fileBase.match(/([a-z]+)-(\d+)\.stl$/i);
  const n = m ? Number(m[2]) : '';
  return `${DATI.prefisso}-${n}-${O.id}-con-nome.stl`;
}

/* Torna al file del solo nominativo (stampa3d.js ha già scritto href e nome del file). */
function togliNome() {
  if (blobUrl) { URL.revokeObjectURL(blobUrl); blobUrl = ''; }
  nomeApplicato = '';
  ultimaForma = null;
  if (conNomeTesto) { conNomeTesto.hidden = true; conNomeTesto.textContent = ''; }
}

async function aggiungi() {
  const testo = pulisci(campo.value);
  if (!fileBase || (scarica && scarica.closest('[hidden]'))) {
    scriviErrore('Prima scrivi il numero del tuo nominativo e premi «Mostra».');
    document.getElementById('s3d-numero') && document.getElementById('s3d-numero').focus();
    return;
  }
  if (!testo) {
    // campo vuoto: si torna al file senza nome
    scriviErrore('');
    if (nomeApplicato) {
      togliNome();
      document.dispatchEvent(new CustomEvent('s3d:file', { detail: fileBase }));
      ripristinaScarica();
      stato.textContent = `${Cosa}: tolto dal file, che ha solo il nominativo.`;
    } else {
      scriviErrore(`Scrivi ${COSA}, oppure lascia il campo vuoto e scarica il file con il solo nominativo.`);
      campo.focus();
    }
    return;
  }
  if (testo.length > MAX_CARATTERI) { scriviErrore(`Scrivi al massimo ${MAX_CARATTERI} caratteri.`); campo.focus(); return; }
  scriviErrore('');
  const mio = ++giro;
  bottone.disabled = true;
  stato.textContent = `Sto preparando il file con ${COSA}…`;
  try {
    const [{ M, font }, buf] = await Promise.all([
      carica(),
      fetch(fileBase).then(r => { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); }),
    ]);
    if (mio !== giro) return;
    let r;
    try { r = conNome(buf, O.anteprima, testo, font, M); }
    catch (e) {
      let msg = e.message || 'Il file non si è potuto preparare.';
      // riga troppo lunga: con un'etichetta diversa (es. nome del mezzo) il consiglio vale per entrambi i casi
      if (/non entrano/.test(msg) && box.dataset.s3dCosa !== 'nome e cognome') msg = 'Il testo non entra: accorcialo. Per una persona scrivi solo l\'iniziale del nome, per esempio «M. Rossi»; per un mezzo solo il modello, per esempio «Defender 130».';
      scriviErrore(msg); stato.textContent = ''; campo.focus(); return;
    }
    togliNome();
    blobUrl = URL.createObjectURL(new Blob([r.stl], { type: 'model/stl' }));
    nomeApplicato = testo;
    if (scarica) {
      scarica.href = blobUrl;
      scarica.setAttribute('download', nomeFile());
      document.querySelectorAll('[data-s3d="file"]').forEach(e => { e.textContent = nomeFile(); });
    }
    if (conNomeTesto) { conNomeTesto.textContent = ` e il nome «${testo}»`; conNomeTesto.hidden = false; }
    ultimaForma = { pos: r.pos, lato: r.lato };
    document.dispatchEvent(new CustomEvent('s3d:geometria', { detail: ultimaForma }));
    stato.textContent = r.lato === 'retro'
      ? `Fatto: «${testo}» è inciso sul retro. Premi «Retro» nella vista per vederlo, poi scarica il file.`
      : `Fatto: «${testo}» è sul davanti, in rilievo. Ora scarica il file.`;
  } catch (e) {
    if (mio !== giro) return;
    stato.textContent = '';
    scriviErrore(`Il file con ${COSA} non si è potuto preparare: controlla la connessione e riprova. Puoi comunque scaricare il file con il solo nominativo.`);
  } finally {
    if (mio === giro) bottone.disabled = false;
  }
}

function ripristinaScarica() {
  if (!scarica || !fileBase) return;
  const m = fileBase.match(/(\d+)\.stl$/);
  const file = `${DATI.prefisso}-${m ? Number(m[1]) : ''}-${O.id}.stl`;
  scarica.href = fileBase;
  scarica.setAttribute('download', file);
  document.querySelectorAll('[data-s3d="file"]').forEach(e => { e.textContent = file; });
}

if (box && campo && bottone && O && O.anteprima && O.anteprima.nome) {
  box.hidden = false;
  fileBase = window.pcgzS3dFile || '';
  bottone.addEventListener('click', aggiungi);
  campo.addEventListener('keydown', ev => { if (ev.key === 'Enter') { ev.preventDefault(); aggiungi(); } });
  // nuovo nominativo: se c'era un nome, si rifà il file con lo stesso nome
  document.addEventListener('s3d:file', ev => {
    if (ev.detail === fileBase) {
      // stesso nominativo confermato di nuovo: stampa3d.js ha rimesso il file senza nome, si rimette quello con il nome
      if (nomeApplicato && blobUrl && scarica) {
        scarica.href = blobUrl;
        scarica.setAttribute('download', nomeFile());
        document.querySelectorAll('[data-s3d="file"]').forEach(e => { e.textContent = nomeFile(); });
        if (ultimaForma) document.dispatchEvent(new CustomEvent('s3d:geometria', { detail: ultimaForma }));
      }
      return;
    }
    fileBase = ev.detail;
    const prima = nomeApplicato;
    togliNome();
    giro++;
    bottone.disabled = false;
    if (prima && pulisci(campo.value) === prima && !(scarica && scarica.closest('[hidden]'))) aggiungi();
    else stato.textContent = '';
  });
  // se la pagina resta nella cache del browser (tasto Indietro) il file con il nome resta valido
  window.addEventListener('pagehide', ev => { if (!ev.persisted) togliNome(); });
}
