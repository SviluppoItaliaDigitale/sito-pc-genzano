/* ============================================================
   CALCOLATORE DELLA SCORTA 72 ORE v1.0 (13/10/2026)
   Dal numero di persone, bambini piccoli, animali e persone con
   terapie calcola acqua, pasti, farmaci e materiali per 3 giorni
   e compone una lista della spesa con caselle da spuntare.
   - riferimenti: circa 4 litri d'acqua a persona al giorno
     (Ready.gov/FEMA, ~3,8 L), 3 giorni; 3 pasti al giorno senza
     cottura; farmaci abituali per almeno 7 giorni; voci per
     persona e voci fisse dalla checklist del kit;
   - nessuna richiesta di rete; lo stato (scelte e caselle) resta
     nel browser con localStorage, sempre dentro try/catch;
   - «Stampa la lista» stampa la sola lista (classe stampa-scorta
     su <html>, regole in custom.css § CALCOLATORE SCORTA).
   ============================================================ */
(function () {
  'use strict';

  var form = document.getElementById('cs-form');
  var esito = document.getElementById('cs-esito');
  var messaggio = document.getElementById('cs-messaggio');
  var azzera = document.getElementById('cs-azzera');
  if (!form || !esito || !azzera || form.getAttribute('data-cs-init')) return;
  form.setAttribute('data-cs-init', '1');   // il calcolatore si avvia una sola volta

  var CHIAVE = 'pcgenzano-calcolatore-scorta';
  var GIORNI = 3;
  var LITRI_GIORNO = 4;       // circa 4 L a persona al giorno (Ready.gov/FEMA, ~3,8 L)
  var PASTI_GIORNO = 3;
  var GIORNI_FARMACI = 7;     // scorta minima dei farmaci abituali
  var BOTTIGLIA = 1.5;        // litri per bottiglia, per tradurre i litri in bottiglie
  var BOTTIGLIA_TESTO = String(BOTTIGLIA).replace('.', ',');

  // campi del modulo: intervallo ammesso e frase per chi scrive un numero fuori misura
  var LIMITI = {
    persone: { id: 'cs-persone', min: 1, max: 30, frase: 'persone in casa da 1 a 30' },
    piccoli: { id: 'cs-piccoli', min: 0, max: 30, frase: 'neonati o bambini piccoli non più delle persone in casa' },
    animali: { id: 'cs-animali', min: 0, max: 30, frase: 'animali domestici da 0 a 30' },
    farmaci: { id: 'cs-farmaci', min: 0, max: 30, frase: 'persone con farmaci abituali non più delle persone in casa' }
  };

  var corrente = null;        // numeri della lista mostrata adesso
  var salvabile = true;       // diventa false se il browser rifiuta di salvare

  // Numeri del modulo (o di un salvataggio) riportati dentro i limiti.
  // «corretti» elenca i campi che erano fuori misura: chi li ha scritti deve saperlo.
  function normalizza(grezzo) {
    var valori = {}, corretti = [];
    Object.keys(LIMITI).forEach(function (k) {
      var l = LIMITI[k];
      var testo = String(grezzo[k] === undefined || grezzo[k] === null ? '' : grezzo[k]).trim();
      var x = Number(testo);
      var c = (testo === '' || !isFinite(x)) ? l.min : Math.min(l.max, Math.max(l.min, Math.round(x)));
      valori[k] = c;
      // un campo vuoto vale zero dove lo zero è ammesso; altrove, e per ogni
      // numero cambiato, il campo è fuori misura
      if (testo === '' ? l.min > 0 : c !== x) corretti.push(k);
    });
    ['piccoli', 'farmaci'].forEach(function (k) {
      if (valori[k] > valori.persone) {
        valori[k] = valori.persone;
        if (corretti.indexOf(k) < 0) corretti.push(k);
      }
    });
    return { valori: valori, corretti: corretti };
  }
  function fraseCorrezioni(corretti) {
    var f = Object.keys(LIMITI).filter(function (k) { return corretti.indexOf(k) >= 0; })
      .map(function (k) { return LIMITI[k].frase; });
    return f.length ? 'Alcuni numeri erano fuori misura e sono stati corretti: ' + f.join('; ') + '.' : '';
  }

  // Un salvataggio illeggibile o con numeri che non tornano non si riprende: meglio
  // ripartire dal modulo vuoto che mostrare una lista per persone che nessuno ha scritto.
  function leggi() {
    try {
      var s = window.localStorage.getItem(CHIAVE);
      var o = s ? JSON.parse(s) : null;
      if (!o || typeof o !== 'object' || !o.valori || typeof o.valori !== 'object') return null;
      var grezzo = {};
      var completo = Object.keys(LIMITI).every(function (k) {
        grezzo[k] = o.valori[k];
        return typeof o.valori[k] === 'number';
      });
      if (!completo) return null;
      var spunte = {};
      if (o.spunte && typeof o.spunte === 'object') {
        Object.keys(o.spunte).forEach(function (c) { if (o.spunte[c] === true) spunte[c] = true; });
      }
      return { valori: normalizza(grezzo).valori, spunte: spunte };
    } catch (e) { return null; }
  }
  function salva(stato) {
    try {
      window.localStorage.setItem(CHIAVE, JSON.stringify(stato));
      salvabile = true;
    } catch (e) { salvabile = false; /* storage non disponibile: la lista resta in pagina */ }
  }
  function cancella() {
    try { window.localStorage.removeItem(CHIAVE); } catch (e) { /* niente da fare */ }
  }
  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt !== undefined) e.textContent = txt;
    return e;
  }
  function plurale(n, uno, tanti) { return n === 1 ? uno : tanti; }

  function dalModulo() {
    var grezzo = {};
    Object.keys(LIMITI).forEach(function (k) { grezzo[k] = document.getElementById(LIMITI[k].id).value; });
    return normalizza(grezzo);
  }
  function nelModulo(valori) {
    Object.keys(LIMITI).forEach(function (k) { document.getElementById(LIMITI[k].id).value = valori[k]; });
  }

  function lista(v) {
    var litri = v.persone * LITRI_GIORNO * GIORNI;
    var bottiglie = Math.ceil(litri / BOTTIGLIA);
    var pasti = v.persone * PASTI_GIORNO * GIORNI;
    var gruppi = [];

    gruppi.push({
      titolo: 'Acqua',
      nota: 'Circa ' + LITRI_GIORNO + ' litri a persona al giorno per ' + GIORNI + ' giorni, per bere e per l’igiene minima. Con caldo intenso, malattia, gravidanza o allattamento serve di più: chiedi al medico.',
      voci: [
        litri + ' litri di acqua in bottiglie sigillate (' + bottiglie + ' ' + plurale(bottiglie, 'bottiglia', 'bottiglie') + ' da ' + BOTTIGLIA_TESTO + ' L)',
        v.piccoli ? 'Acqua in più per ' + v.piccoli + ' ' + plurale(v.piccoli, 'bambino piccolo', 'bambini piccoli') + ' (latte ricostituito e igiene): quantità secondo l’età, non compresa nei litri sopra' : null,
        v.animali ? 'Acqua in più per ' + v.animali + ' ' + plurale(v.animali, 'animale', 'animali') + ': scorta dedicata, secondo specie e peso' : null
      ]
    });

    gruppi.push({
      titolo: 'Cibo senza cottura',
      nota: pasti + ' pasti in tutto (' + PASTI_GIORNO + ' al giorno per ' + v.persone + ' ' + plurale(v.persone, 'persona', 'persone') + ' per ' + GIORNI + ' giorni). Scegli alimenti a lunga conservazione che la famiglia mangia davvero: si ruotano prima della scadenza.',
      voci: [
        'Pane a lunga conservazione, fette biscottate o cracker',
        'Legumi, tonno o carne in scatola, pronti da mangiare',
        'Frutta secca, barrette, biscotti, marmellata',
        'Frutta e verdura in scatola o succhi in confezione',
        'Apriscatole manuale, posate e piatti usa e getta',
        v.piccoli ? 'Latte, pappe e alimenti per ' + v.piccoli + ' ' + plurale(v.piccoli, 'bambino piccolo', 'bambini piccoli') + ' per ' + GIORNI + ' giorni' : null,
        v.animali ? 'Cibo per ' + v.animali + ' ' + plurale(v.animali, 'animale', 'animali') + ' per ' + GIORNI + ' giorni, ciotola, trasportino e libretto sanitario' : null
      ]
    });

    gruppi.push({
      titolo: 'Farmaci e salute',
      nota: v.farmaci
        ? 'Scorta di almeno ' + GIORNI_FARMACI + ' giorni dei farmaci abituali per ' + v.farmaci + ' ' + plurale(v.farmaci, 'persona', 'persone') + ', con le ricette e l’elenco di terapie e allergie. Per terapie salvavita, catena del freddo e apparecchi elettromedicali segui la scheda dei kit per le terapie salvavita.'
        : 'Nessuna terapia abituale indicata: resta la cassetta di primo soccorso. Se cambia, rifai il calcolo.',
      voci: [
        v.farmaci ? 'Farmaci abituali per ' + GIORNI_FARMACI + ' giorni, con ricette e piano terapeutico' : null,
        'Cassetta di primo soccorso: cerotti, garze, disinfettante, guanti, termometro',
        'Occhiali di riserva, apparecchi acustici e batterie, ausili personali',
        v.piccoli ? 'Pannolini, salviette e creme per ' + GIORNI + ' giorni' : null
      ]
    });

    gruppi.push({
      titolo: 'Per ogni persona',
      nota: v.persone === 1 ? 'Una voce per la persona che vive in casa.' : 'Una voce per ciascuna delle ' + v.persone + ' persone in casa.',
      voci: [
        v.persone + ' ' + plurale(v.persone, 'torcia frontale', 'torce frontali') + ' con pile di scorta',
        v.persone + ' ' + plurale(v.persone, 'coperta o indumento caldo adatto alla stagione', 'coperte o indumenti caldi adatti alla stagione'),
        v.persone + ' ' + plurale(v.persone, 'fischietto', 'fischietti'),
        v.persone + ' ' + plurale(v.persone, 'copia dei documenti', 'copie dei documenti') + ' in busta impermeabile'
      ]
    });

    gruppi.push({
      titolo: 'Per la casa',
      nota: 'Voci fisse della checklist del kit, indipendenti dal numero di persone.',
      voci: [
        'Radio a pile o a manovella, con pile di scorta',
        'Power bank carico e cavi del telefono',
        'Lampada a pile per la stanza principale (niente candele)',
        'Salviette, gel igienizzante, sapone, carta igienica',
        'Almeno 10 sacchi grandi per i rifiuti',
        'Contanti in piccolo taglio',
        'Elenco cartaceo dei numeri utili e dei contatti di famiglia',
        'Chiavi di riserva di casa e auto'
      ]
    });

    gruppi.forEach(function (g) { g.voci = g.voci.filter(Boolean); });
    return { litri: litri, bottiglie: bottiglie, pasti: pasti, gruppi: gruppi };
  }

  // «nota»: frase sui numeri corretti, se ce n'è (sta nel riquadro, subito dopo il titolo)
  function mostra(v, spunte, nota) {
    var l = lista(v);
    corrente = v;
    esito.textContent = '';
    esito.hidden = false;

    var intro = el('div', 'alert alert-info', '');
    var h = el('h2', 'h5 mb-2', 'La scorta per ' + GIORNI + ' giorni della tua casa');
    h.id = 'cs-esito-titolo';
    h.setAttribute('tabindex', '-1');   // riceve il fuoco dopo «Calcola la scorta»
    intro.appendChild(h);
    var p = el('p', 'mb-0');
    p.appendChild(document.createTextNode('Per ' + v.persone + ' ' + plurale(v.persone, 'persona', 'persone') + ': '));
    var b1 = el('strong', null, l.litri + ' litri d’acqua');
    p.appendChild(b1);
    p.appendChild(document.createTextNode(' (' + l.bottiglie + ' ' + plurale(l.bottiglie, 'bottiglia', 'bottiglie') + ' da ' + BOTTIGLIA_TESTO + ' L), '));
    var b2 = el('strong', null, l.pasti + ' pasti senza cottura');
    p.appendChild(b2);
    p.appendChild(document.createTextNode(v.farmaci ? ', farmaci abituali per ' + GIORNI_FARMACI + ' giorni.' : '.'));
    intro.appendChild(p);
    if (nota) intro.appendChild(el('p', 'small mb-0 mt-2', nota));
    esito.appendChild(intro);

    var h2 = el('h2', 'h4 mt-3', 'Lista della spesa da spuntare');
    esito.appendChild(h2);
    var totale = 0, fatte = 0;
    l.gruppi.forEach(function (g, gi) {
      var sez = el('section', 'cs-gruppo');
      sez.appendChild(el('h3', 'h5', g.titolo));
      sez.appendChild(el('p', 'small text-muted', g.nota));
      var ul = el('ul', 'list-unstyled');
      g.voci.forEach(function (voce, vi) {
        var id = 'cs-v-' + gi + '-' + vi;
        var chiave = g.titolo + '|' + voce;   // le spunte si ritrovano dal testo della voce, non dalla posizione
        var li = el('li', 'form-check');
        var cb = el('input', 'form-check-input');
        cb.type = 'checkbox'; cb.id = id;
        cb.setAttribute('data-voce', chiave);
        cb.checked = !!(spunte && spunte[chiave]);
        if (cb.checked) fatte++;
        totale++;
        cb.addEventListener('change', function () { aggiornaSpunta(); });
        var lab = el('label', 'form-check-label', voce);
        lab.htmlFor = id;
        li.appendChild(cb); li.appendChild(lab); ul.appendChild(li);
      });
      sez.appendChild(ul);
      esito.appendChild(sez);
    });

    var stato = el('p', 'cs-stato small', '');
    stato.id = 'cs-stato';
    stato.setAttribute('role', 'status');   // a ogni spunta il conteggio viene annunciato, senza rileggere la lista
    esito.appendChild(stato);
    aggiornaStato(fatte, totale);

    var azioni = el('div', 'd-flex flex-wrap gap-2 mt-3 d-print-none');
    var stampa = el('button', 'btn btn-outline-primary', 'Stampa la lista');
    stampa.type = 'button';
    stampa.addEventListener('click', function () {
      var radice = document.documentElement;
      var togli = function () { radice.classList.remove('stampa-scorta'); };
      radice.classList.add('stampa-scorta');
      window.addEventListener('afterprint', togli, { once: true });
      window.print();
    });
    azioni.appendChild(stampa);
    esito.appendChild(azioni);

    var fonte = el('p', 'small text-muted mt-3 mb-0', 'Riferimenti: circa ' + LITRI_GIORNO + ' litri d’acqua a persona al giorno (Ready.gov/FEMA, ~3,8 litri arrotondati) per ' + GIORNI + ' giorni; ' + PASTI_GIORNO + ' pasti al giorno senza cottura; farmaci abituali per almeno ' + GIORNI_FARMACI + ' giorni. Quantità orientative, non valori clinici: per lattanti, dialisi e terapie salvavita chiedi al medico. Le voci seguono la pagina Kit di emergenza e la checklist del kit.');
    esito.appendChild(fonte);
  }

  function aggiornaStato(fatte, totale) {
    var s = document.getElementById('cs-stato');
    if (!s) return;
    var t = fatte + ' su ' + totale + ' voci spuntate' + (fatte === totale && totale ? ': scorta completa, segna la data del prossimo controllo fra sei mesi.' : '.');
    // le spunte promettono di restare nel browser: se non è vero, la pagina lo dice
    if (!salvabile) t += ' Questo browser non permette di salvare le spunte: restano finché la pagina è aperta.';
    s.textContent = t;
  }

  function aggiornaSpunta() {
    var spunte = {};
    var caselle = esito.querySelectorAll('input[type="checkbox"]');
    var fatte = 0;
    Array.prototype.forEach.call(caselle, function (cb) {
      if (cb.checked) { spunte[cb.getAttribute('data-voce')] = true; fatte++; }
    });
    salva({ valori: corrente, spunte: spunte });
    aggiornaStato(fatte, caselle.length);
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var r = dalModulo();
    var v = r.valori;
    var prima = leggi();
    // le spunte restano solo se i numeri sono gli stessi: con altri numeri la lista è un'altra
    var stesse = !!prima && Object.keys(LIMITI).every(function (k) { return prima.valori[k] === v[k]; });
    var spunte = stesse ? prima.spunte : {};
    salva({ valori: v, spunte: spunte });
    nelModulo(v);                       // il modulo mostra i numeri davvero usati
    if (messaggio) messaggio.textContent = '';
    mostra(v, spunte, fraseCorrezioni(r.corretti));
    var titolo = document.getElementById('cs-esito-titolo');
    if (titolo) titolo.focus();
  });

  azzera.addEventListener('click', function () {
    cancella();
    corrente = null;
    esito.textContent = '';
    esito.hidden = true;
    form.reset();
    if (messaggio) messaggio.textContent = 'Dati cancellati: la lista e le spunte salvate in questo browser sono state eliminate.';
  });

  // ripristino di una scelta precedente (senza spostare il fuoco)
  var salvato = leggi();
  if (salvato) {
    nelModulo(salvato.valori);
    mostra(salvato.valori, salvato.spunte, '');
  }
})();
