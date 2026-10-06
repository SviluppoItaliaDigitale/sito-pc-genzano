/* ============================================================
   CREA LA MIA LEZIONE v1.0 (06/10/2026)
   Compone una lezione con i materiali già pubblicati sul sito
   (catalogo in #crea-lezione-dati, generato da
   scripts/genera-materiali-lezione.py). Non scrive contenuti:
   sceglie, ordina e dà a ogni fase il suo tempo.
   - fasi diverse per 30, 45, 60 e 90 minuti;
   - per ogni fase il materiale della classe e dell'argomento
     scelti; se non c'è, la fase cambia o si toglie e il tempo
     passa all'attività principale;
   - «Proponi altri materiali» rimescola le scelte;
   - la scelta resta nell'indirizzo della pagina (?classe=…), così
     la lezione si può riaprire o mandare a un collega;
   - «Stampa la lezione» stampa solo il piano.
   ============================================================ */
(function () {
  'use strict';

  var datiEl = document.getElementById('crea-lezione-dati');
  var form = document.getElementById('crea-lezione-form');
  var esito = document.getElementById('crea-lezione-esito');
  if (!datiEl || !form || !esito) return;
  var DATI = JSON.parse(datiEl.textContent);
  var BASE = (window.PCGZ_BASE || '/').replace(/\/$/, '');
  var CLASSI = {
    'infanzia': "Scuola dell'infanzia",
    'primaria-bassa': 'Primaria, classi 1ª-2ª',
    'primaria-alta': 'Primaria, classi 3ª-5ª',
    'secondaria1': 'Secondaria di primo grado',
    'secondaria2': 'Secondaria di secondo grado'
  };
  var TIPI = {
    scheda: 'Scheda da stampare', storia: 'Storia', gioco: 'Gioco online',
    esperimento: 'Esperimento', colorare: 'Scheda da colorare', valutazione: 'Strumento di valutazione'
  };
  // [fase, minuti, tipi di materiale in ordine di preferenza]
  var SCALETTE = {
    30: [['intro', 5], ['principale', 20, ['scheda', 'colorare', 'storia']], ['gioco', 5, ['gioco']]],
    45: [['intro', 5], ['racconto', 10, ['storia']], ['principale', 20, ['scheda', 'colorare']], ['gioco', 5, ['gioco', 'esperimento']], ['chiusura', 5]],
    60: [['intro', 5], ['racconto', 10, ['storia']], ['principale', 20, ['scheda', 'colorare']], ['esperimento', 15, ['esperimento']], ['gioco', 5, ['gioco']], ['chiusura', 5]],
    90: [['intro', 10], ['racconto', 15, ['storia']], ['principale', 25, ['scheda', 'colorare']], ['esperimento', 20, ['esperimento']], ['gioco', 10, ['gioco']], ['chiusura', 10]]
  };
  var NOMI_FASI = {
    intro: 'Introduzione', racconto: 'Racconto', principale: 'Attività principale',
    esperimento: 'Esperimento', gioco: 'Gioco', chiusura: 'Chiusura e verifica'
  };

  function rimescola(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function candidati(tipi, classe, tema, usati) {
    var adatti = DATI.materiali.filter(function (m) {
      return tipi.indexOf(m.tipo) !== -1 && m.fasce.indexOf(classe) !== -1 &&
        m.temi.indexOf(tema) !== -1 && !usati[m.url + '|' + m.titolo];
    });
    // a parità di tipo, prima il tipo preferito
    return rimescola(adatti).sort(function (a, b) { return tipi.indexOf(a.tipo) - tipi.indexOf(b.tipo); });
  }
  function link(m) {
    var a = document.createElement('a');
    a.href = BASE + m.url;
    a.textContent = m.titolo;
    return a;
  }
  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt) e.textContent = txt;
    return e;
  }

  function componi(classe, minuti, tema, bes) {
    var t = DATI.temi[tema];
    var usati = {};
    var fasi = [];
    var avanzo = 0;
    SCALETTE[minuti].forEach(function (f) {
      var nome = f[0], min = f[1], tipi = f[2];
      if (nome === 'intro') {
        fasi.push({ nome: nome, min: min, intro: t.intro });
        return;
      }
      if (nome === 'chiusura') {
        fasi.push({ nome: nome, min: min });
        return;
      }
      var scelta = candidati(tipi, classe, tema, usati);
      if (nome === 'principale' && scelta.length) {
        // se la scheda dichiara la sua durata, si preferisce una che stia nella fase
        var nelTempo = scelta.filter(function (m) { return !m.minuti || m.minuti <= min + avanzo + 5; });
        if (nelTempo.length) scelta = nelTempo;
      }
      if (!scelta.length) { avanzo += min; return; }
      usati[scelta[0].url + '|' + scelta[0].titolo] = 1;
      fasi.push({ nome: nome, min: min, materiale: scelta[0] });
    });
    // il tempo delle fasi senza materiale va all'attività principale (o alla chiusura)
    if (avanzo) {
      var dest = fasi.filter(function (f) { return f.nome === 'principale'; })[0] ||
                 fasi.filter(function (f) { return f.nome === 'chiusura'; })[0] || fasi[fasi.length - 1];
      dest.min += avanzo;
    }
    var facilitate = bes ? DATI.materiali.filter(function (m) {
      return m.facilitata && m.temi.indexOf(tema) !== -1;
    }) : [];
    var valutazione = DATI.materiali.filter(function (m) {
      return m.tipo === 'valutazione' && m.fasce.indexOf(classe) !== -1;
    });
    return { classe: classe, minuti: minuti, tema: tema, t: t, fasi: fasi, bes: bes, facilitate: facilitate, valutazione: valutazione };
  }

  function disegna(l) {
    esito.textContent = '';
    var h = el('h2', null, 'Lezione pronta: ' + l.t.etichetta);
    h.id = 'lezione-titolo';
    esito.appendChild(h);
    esito.appendChild(el('p', 'crea-lezione-sintesi',
      CLASSI[l.classe] + ' · ' + l.minuti + ' minuti · ' + l.fasi.length + ' fasi'));
    var ol = el('ol', 'crea-lezione-fasi');
    var inizio = 0;
    l.fasi.forEach(function (f) {
      var li = el('li', 'crea-lezione-fase');
      var tempo = el('span', 'crea-lezione-tempo', inizio + '–' + (inizio + f.min) + ' min');
      inizio += f.min;
      var corpo = el('div', 'crea-lezione-corpo');
      corpo.appendChild(el('h3', null, NOMI_FASI[f.nome] + ' · ' + f.min + ' minuti'));
      if (f.nome === 'intro') {
        var p = el('p');
        if (f.intro) {
          p.appendChild(document.createTextNode('Presenta l’argomento con la pagina '));
          p.appendChild(link({ url: f.intro, titolo: l.t.etichetta }));
          p.appendChild(document.createTextNode(': puoi proiettarla con il pulsante «Modalità Aula» e chiedere alla classe che cosa sa già.'));
        } else {
          p.textContent = 'Chiedi alla classe che cosa sa già dell’argomento e annota le risposte alla lavagna: le riprenderete alla fine.';
        }
        corpo.appendChild(p);
      } else if (f.nome === 'chiusura') {
        var c = el('p', null, 'Riprendete le risposte dell’introduzione: che cosa è cambiato? Ogni alunno dice o scrive una cosa da fare e una persona a cui raccontarla a casa.');
        corpo.appendChild(c);
        if (l.valutazione.length) {
          var v = el('p', 'small');
          v.appendChild(document.createTextNode('Per osservare e valutare: '));
          l.valutazione.forEach(function (m, i) { if (i) v.appendChild(document.createTextNode(', ')); v.appendChild(link(m)); });
          v.appendChild(document.createTextNode('.'));
          corpo.appendChild(v);
        }
      } else {
        var m = f.materiale;
        var r = el('p');
        r.appendChild(el('span', 'crea-lezione-tipo', TIPI[m.tipo] || m.tipo));
        r.appendChild(document.createTextNode(' '));
        r.appendChild(link(m));
        if (m.minuti) r.appendChild(document.createTextNode(' (durata indicata: ' + m.minuti + ' minuti)'));
        corpo.appendChild(r);
        if (m.desc && m.tipo !== 'esperimento') corpo.appendChild(el('p', 'small', m.desc));
        if (m.tipo === 'esperimento') corpo.appendChild(el('p', 'small', 'Lo trovi nella pagina degli esperimenti, nella sezione «' + m.desc + '», con materiali e indicazioni di sicurezza: sempre con un adulto.'));
      }
      li.appendChild(tempo);
      li.appendChild(corpo);
      ol.appendChild(li);
    });
    esito.appendChild(ol);

    if (l.bes) {
      var box = el('div', 'crea-lezione-bes');
      box.appendChild(el('h3', null, 'Per gli alunni con bisogni educativi speciali'));
      var ul = el('ul');
      l.facilitate.forEach(function (m) {
        var li = el('li'); li.appendChild(document.createTextNode('Versione facilitata: ')); li.appendChild(link(m)); ul.appendChild(li);
      });
      [['/tabelle-comunicazione/', 'Tabelle di comunicazione (CAA)', ' con i pittogrammi, per chi non riesce a parlare o comprende meglio per immagini'],
       ['/facile-da-leggere/', 'Facile da leggere', ': le regole di autoprotezione in linguaggio semplice'],
       ['/lis/', 'Contenuti in LIS', ' per gli alunni sordi'],
       ['/pittogrammi/', 'Pittogrammi', ' da stampare per sostenere le consegne']].forEach(function (x) {
        var li = el('li'); li.appendChild(link({ url: x[0], titolo: x[1] })); li.appendChild(document.createTextNode(x[2] + '.')); ul.appendChild(li);
      });
      box.appendChild(ul);
      box.appendChild(el('p', 'small', 'In Modalità Aula i pulsanti A+ e A− ingrandiscono il testo proiettato. Adatta tempi e consegne al piano didattico personalizzato.'));
      esito.appendChild(box);
    }

    var nota = el('p', 'small crea-lezione-avviso', 'Prima della lezione apri e leggi ogni materiale: la composizione è automatica e non conosce la tua classe.');
    esito.appendChild(nota);
    var azioni = el('div', 'crea-lezione-azioni');
    var altro = el('button', 'btn btn-outline-primary', 'Proponi altri materiali');
    altro.type = 'button';
    altro.addEventListener('click', function () { genera(true); });
    var stampa = el('button', 'btn btn-outline-primary', 'Stampa la lezione');
    stampa.type = 'button';
    stampa.addEventListener('click', function () { window.print(); });
    azioni.appendChild(altro); azioni.appendChild(stampa);
    esito.appendChild(azioni);
    esito.hidden = false;
  }

  function genera(focus) {
    var classe = form.classe.value, minuti = form.minuti.value, tema = form.tema.value, bes = form.bes.checked;
    var l = componi(classe, minuti, tema, bes);
    disegna(l);
    try {
      var q = new URLSearchParams({ classe: classe, minuti: minuti, tema: tema });
      if (bes) q.set('bes', '1');
      history.replaceState(null, '', '?' + q.toString());
    } catch (e) { /* indirizzo non aggiornabile: la lezione resta comunque */ }
    if (focus) {
      var titolo = document.getElementById('lezione-titolo');
      titolo.setAttribute('tabindex', '-1');
      titolo.focus();
    }
  }

  form.addEventListener('submit', function (e) { e.preventDefault(); genera(true); });

  // lezione già scelta nell'indirizzo (?classe=…&minuti=…&tema=…)
  try {
    var q = new URLSearchParams(location.search);
    if (q.get('classe') && CLASSI[q.get('classe')] && SCALETTE[q.get('minuti')] && DATI.temi[q.get('tema')]) {
      form.classe.value = q.get('classe'); form.minuti.value = q.get('minuti'); form.tema.value = q.get('tema');
      form.bes.checked = q.get('bes') === '1';
      genera(false);
    }
  } catch (e) { /* niente */ }
})();
