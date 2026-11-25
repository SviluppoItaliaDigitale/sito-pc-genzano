/* Catalogo dei disciplinari DOP, IGP e STG (/cucina-emergenza/disciplinari/): ricerca per parole, regione
   e tipo di prodotto. Senza JavaScript il catalogo resta intero, diviso per tipo di prodotto.

   Come cerca la casella (dal 25/11/2026). Ogni parola scritta deve trovarsi nel prodotto, in uno di due modi:
   - all'inizio di una parola di data-p: nome del prodotto, parole chiave del suo tipo («formaggi», «olio»,
     «legumi»: data/disciplinari.json, campo «parole») e prima parola della regione;
   - come parola intera di data-e: sigla (DOP, IGP, STG) e nome della regione.
   Mai un pezzo in mezzo alla parola: prima «roma» trovava tutta l'Emilia-Romagna, «pane» le Valli Trapanesi
   e «olio» sette oli su cinquantuno. Le parole di almeno sei lettere si cercano senza la vocale finale, così
   «lenticchie» trova Lenticchia e «Amatrice» l'Amatriciana. Articoli, preposizioni e parole generiche
   («prodotti», «tipici») non contano: l'elenco VUOTE qui sotto lo legge anche il controllo dei dati
   (scripts/check-cucina-emergenza.py), perché una parola chiave uguale a una parola vuota non si troverebbe mai.

   Dal telefono il risultato sta sotto il riquadro: dopo una scelta dai menu la pagina scende quel tanto
   che basta a mostrare quanti prodotti restano e il pulsante che porta all'elenco; il tasto di invio della
   tastiera porta all'elenco. Il fuoco si sposta solo con il pulsante o con l'invio, mai da solo.

   Con una regione scelta dal menu, o scritta per intero nella casella, in ogni gruppo vengono prima i
   prodotti di quella sola regione, poi quelli che ne hanno anche altre, e la riga di ogni prodotto dice
   «Lazio e altre 7 regioni» al posto dell'elenco di tutte.

   La scelta resta nell'indirizzo (?q=…&regione=…&tipo=…), così un elenco filtrato si può condividere.
   Sintassi entro ECMAScript 2018 (scripts/check-sintassi-js.cjs). Prova nel browser, bloccante sulle pull
   request: scripts/prova-filtro-disciplinari.py. */
(function () {
  'use strict';
  var filtri = document.querySelector('[data-disc="filtri"]');
  if (!filtri) return;
  var cerca = document.getElementById('disc-cerca');
  var regione = document.getElementById('disc-regione');
  var gruppo = document.getElementById('disc-gruppo');
  var conteggio = filtri.querySelector('[data-disc="conteggio"]');
  var azioni = filtri.querySelector('[data-disc="azioni"]');
  var vai = filtri.querySelector('[data-disc="vai"]');
  var azzera = filtri.querySelector('[data-disc="azzera"]');
  var trovati = document.querySelector('[data-disc="trovati"]');
  var nessuno = document.querySelector('[data-disc="nessuno"]');
  var perche = nessuno ? nessuno.querySelector('[data-disc="perche"]') : null;
  var blocchi = Array.prototype.slice.call(document.querySelectorAll('[data-disc-gruppo]'));
  if (!cerca || !regione || !gruppo || !conteggio || !blocchi.length) return;

  var VUOTE = {};
  ('a ad agli ai al all alla alle allo col con d da dai dal dalla dalle de degli dei del dell della delle dello di ' +
   'e ed gli i il in l la le lo nei nel nella o per su sul sulla un una uno ' +
   'prodotti prodotto tipici tipico tipica tipiche').split(' ').forEach(function (p) { VUOTE[p] = true; });

  function norm(t) {
    return String(t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function parole(t) {
    var n = norm(t);
    return n ? n.split(' ') : [];
  }
  /* «lenticchie» e «lenticchia», «amatrice» e «amatriciana»: sotto le sei lettere no, o «pesce» troverebbe le pesche. */
  function radice(p) {
    return p.length >= 6 ? p.replace(/[aeiou]$/, '') : p;
  }

  var voci = [];
  blocchi.forEach(function (blocco) {
    var id = blocco.getAttribute('data-disc-gruppo');
    Array.prototype.forEach.call(blocco.querySelectorAll('.disc-voce'), function (li) {
      var luogo = li.querySelector('.disc-luogo');
      voci.push({
        li: li,
        gruppo: id,
        inizi: parole(li.getAttribute('data-p')),
        intere: parole(li.getAttribute('data-e')),
        regioni: (li.getAttribute('data-r') || '').split('|'),
        luogo: luogo,                           /* la riga con le regioni del prodotto */
        dove: luogo ? luogo.textContent : '',   /* come la scrive la pagina: tutte le regioni */
        lista: li.parentNode,
        posto: voci.length                      /* l'ordine della pagina */
      });
    });
  });

  /* Le regioni del menu, con le parole del loro nome («emilia», «romagna»): servono a riconoscere una regione
     scritta per intero nella casella. */
  var REGIONI = Array.prototype.filter.call(regione.options, function (o) { return o.value; }).map(function (o) {
    var nome = o.text.replace(/\s*\(\d+\)\s*$/, '');
    return { valore: o.value, nome: nome, parole: parole(nome).filter(function (p) { return !VUOTE[p]; }) };
  });

  function contiene(voce, parola) {
    if (voce.intere.indexOf(parola) >= 0) return true;
    var r = radice(parola);
    return voce.inizi.some(function (p) { return p.indexOf(r) === 0; });
  }

  /* Le parole da cercare, senza quelle vuote: «prodotti tipici» da solo non restringe l'elenco. */
  function chieste() {
    return parole(cerca.value).filter(function (p) { return !VUOTE[p]; });
  }

  function haOpzione(select, valore) {
    return Array.prototype.some.call(select.options, function (o) { return o.value === valore; });
  }
  /* «Lazio (30)» → «Lazio». */
  function scelta(select) {
    var o = select.options[select.selectedIndex];
    return o ? o.text.replace(/\s*\(\d+\)\s*$/, '') : '';
  }

  /* Titolo del gruppo (h2 prima del blocco) e sua voce nell'indice «In questa pagina». */
  function mostraGruppo(blocco, visibile) {
    blocco.hidden = !visibile;
    var titolo = blocco.previousElementSibling;
    if (titolo && /^H[2-3]$/.test(titolo.tagName)) {
      titolo.hidden = !visibile;
      if (titolo.id) {
        Array.prototype.forEach.call(document.querySelectorAll('a[href="#' + titolo.id + '"]'), function (a) {
          var li = a.closest ? a.closest('li') : null;
          if (li) li.hidden = !visibile;
        });
      }
    }
  }

  /* Il conteggio è una regione con role="status": si aggiorna poco dopo l'ultima scelta, così chi usa uno
     screen reader sente un solo annuncio. Al caricamento («subito») si scrive prima di mostrare i filtri,
     perché la pagina non parli da sola. */
  var attesa = null;
  function annuncia(n, subito, generiche) {
    var tot = voci.length;
    var testo = !n ? 'Nessun prodotto per questa ricerca.'
      : n === tot ? tot + ' prodotti.'
        : n + (n === 1 ? ' prodotto' : ' prodotti') + ' su ' + tot + '.';
    if (generiche) testo += ' Le parole scritte non restringono l’elenco.';
    window.clearTimeout(attesa);
    if (subito) { conteggio.textContent = testo; return; }
    attesa = window.setTimeout(function () { conteggio.textContent = testo; }, 250);
  }

  function scriviIndirizzo() {
    if (!window.history || !window.history.replaceState || !window.URLSearchParams) return;
    var p = new URLSearchParams(window.location.search);
    [['q', cerca.value.trim()], ['regione', regione.value], ['tipo', gruppo.value]].forEach(function (c) {
      if (c[1]) p.set(c[0], c[1]); else p.delete(c[0]);
    });
    var s = p.toString();
    try {
      window.history.replaceState(null, '', window.location.pathname + (s ? '?' + s : '') + window.location.hash);
    } catch (e) { /* in un file locale o in una cornice l'indirizzo non si cambia: il filtro vale lo stesso */ }
  }

  /* La regione «in evidenza»: quella scelta dal menu o, se il menu è vuoto, quella scritta per intero nella
     casella («lazio», «emilia romagna»). */
  function regioneInEvidenza(r, cercate) {
    if (r) return { valore: r, nome: scelta(regione) };
    var trovata = null;
    REGIONI.forEach(function (reg) {
      if (reg.parole.length && reg.parole.every(function (p) { return cercate.indexOf(p) >= 0; }) &&
          (!trovata || reg.parole.length > trovata.parole.length)) trovata = reg;
    });
    return trovata;
  }

  /* Con una regione in evidenza la riga del prodotto dice quella, e quante altre ne ha: dopo aver scelto il
     Lazio, le otto regioni scritte sotto «Mortadella Bologna» facevano pensare che il filtro non scegliesse
     («mi mette tutte le regioni», 25/11/2026). Senza regione in evidenza la riga torna com'è nella pagina. */
  function scriviLuogo(v, evid) {
    if (!v.luogo) return;
    if (!evid || v.regioni.indexOf(evid.valore) < 0) {
      if (v.cambiato) { v.luogo.textContent = v.dove; v.cambiato = false; }
      return;
    }
    var altre = v.regioni.length - 1;
    var forte = document.createElement('strong');
    forte.textContent = evid.nome;
    v.luogo.textContent = '';
    v.luogo.appendChild(forte);
    if (altre) v.luogo.appendChild(document.createTextNode(altre === 1 ? ' e un’altra regione' : ' e altre ' + altre + ' regioni'));
    v.cambiato = true;
  }

  /* Con una regione in evidenza, in ogni gruppo vengono prima i prodotti di quella sola regione, poi quelli
     che ne hanno anche altre, dai meno ai più condivisi. Si spostano le righe, non solo il loro aspetto: chi
     ascolta la pagina o usa la tastiera le trova nello stesso ordine di chi guarda. */
  var ordinePerRegione = false;
  function riordina(perRegione) {
    if (perRegione === ordinePerRegione) return;
    ordinePerRegione = perRegione;
    var liste = [];
    voci.forEach(function (v) { if (liste.indexOf(v.lista) < 0) liste.push(v.lista); });
    liste.forEach(function (lista) {
      voci.filter(function (v) { return v.lista === lista; })
        .sort(function (a, b) { return (perRegione ? a.regioni.length - b.regioni.length : 0) || a.posto - b.posto; })
        .forEach(function (v) { lista.appendChild(v.li); });
    });
  }

  /* Senza risultati, il perché: una parola che non sta in nessun prodotto («vino»), parole che ci sono ma
     mai insieme («prosciutto crudo»), prodotti che ci sono ma non con la regione o il tipo scelti. Così chi
     cerca sa che cosa cambiare. */
  function motivo(cercate, r, g) {
    if (!cercate.length) return r && g ? 'Nella regione scelta non ci sono prodotti di questo tipo. ' : '';
    var ignote = cercate.filter(function (p) { return !voci.some(function (v) { return contiene(v, p); }); });
    if (ignote.length === 1) return 'Nel catalogo nessun prodotto ha la parola «' + ignote[0] + '»: prova a toglierla. ';
    if (ignote.length) return 'Nel catalogo nessun prodotto ha queste parole: «' + ignote.join('», «') + '». Prova a toglierle. ';
    var insieme = voci.some(function (v) { return cercate.every(function (p) { return contiene(v, p); }); });
    if (insieme) return 'Ci sono prodotti con queste parole, ma non con la regione o il tipo scelti nei menu. ';
    return 'Le parole scritte ci sono, ma mai nello stesso prodotto: prova con una sola. ';
  }

  function filtra(subito) {
    var scritto = cerca.value.trim().replace(/\s+/g, ' ');
    var cercate = chieste();
    var r = regione.value;
    var g = gruppo.value;
    var attivo = !!(cercate.length || r || g);
    /* Nella casella ci sono solo articoli, preposizioni o parole generiche («prodotti tipici»): l'elenco
       resta intero, e la pagina lo dice invece di tacere. */
    var generiche = !!scritto && !attivo;
    var evid = regioneInEvidenza(r, cercate);
    var n = 0;
    var soli = 0;        /* prodotti in elenco che hanno solo la regione in evidenza */
    var condivisi = 0;   /* prodotti in elenco che ne hanno anche altre */
    var vivi = {};
    voci.forEach(function (v) {
      var si = (!g || v.gruppo === g) && (!r || v.regioni.indexOf(r) >= 0) &&
        cercate.every(function (p) { return contiene(v, p); });
      v.li.hidden = !si;
      scriviLuogo(v, si ? evid : null);
      if (si) {
        n++; vivi[v.gruppo] = true;
        if (evid && v.regioni.indexOf(evid.valore) >= 0) { if (v.regioni.length === 1) soli++; else condivisi++; }
      }
    });
    riordina(!!evid);
    blocchi.forEach(function (blocco) { mostraGruppo(blocco, !!vivi[blocco.getAttribute('data-disc-gruppo')]); });
    if (nessuno) nessuno.hidden = n > 0;
    if (perche) perche.textContent = n ? '' : motivo(cercate, r, g);
    if (azzera) azzera.hidden = !(attivo || scritto);
    if (trovati) {
      var pezzi = [];
      if (generiche) {
        pezzi.push('Le parole scritte («' + scritto + '») non restringono l’elenco: qui sotto ci sono tutti i ' +
          'prodotti. Scrivi il nome di un prodotto o di un luogo, oppure un tipo di prodotto.');
      } else {
        pezzi.push(n === 1 ? '1 prodotto trovato.' : n + ' prodotti trovati.');
        if (cercate.length) pezzi.push('Parole cercate: ' + scritto + '.');
        if (r) pezzi.push('Regione: ' + scelta(regione) + '.');
        if (g) pezzi.push('Tipo di prodotto: ' + scelta(gruppo) + '.');
        if (soli && condivisi) {
          pezzi.push('Per primi i prodotti solo di questa regione (' + soli + '), poi quelli che ne hanno anche altre (' +
            condivisi + ').');
        }
      }
      trovati.textContent = pezzi.join(' ');
      trovati.hidden = !((attivo || generiche) && n > 0);
    }
    if (vai) {
      vai.textContent = n === 1 ? 'Vai al prodotto trovato' : 'Vai ai ' + n + ' prodotti trovati';
      vai.hidden = !(attivo && n > 0);
    }
    annuncia(n, subito === true, generiche);
    scriviIndirizzo();
  }

  /* Dove comincia ciò che copre il fondo dello schermo sopra la riga «riga»: la barra di navigazione del
     telefono, la striscia dei cookie alla prima visita e i pulsanti flottanti (SOS 112, accessibilità,
     assistente, lingua, torna su). Conta ciò che sta nella metà bassa dello schermo e nella stessa fascia
     orizzontale della riga: un pulsante flottante nel margine, a schermo largo, non copre niente. */
  function fondoVisibile(riga) {
    var alto = window.innerHeight;
    var fondo = alto;
    ['.bottom-nav', '#cookie-banner', '#sos-button', '#a11yToolbarOpen', '#assistente-fab', '#lang-toggle',
      '#backToTop'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (!el || !el.getClientRects().length || window.getComputedStyle(el).visibility === 'hidden') return;
      var b = el.getBoundingClientRect();
      if (b.height > 0 && b.top > alto / 2 && b.top < fondo && b.left < riga.right && b.right > riga.left) fondo = b.top;
    });
    return fondo;
  }
  /* La pagina scorre come vuole il sito (dolce, se chi legge non ha chiesto meno movimento); di colpo con
     «Pausa animazioni» del pannello accessibilità o con il movimento ridotto del sistema. */
  function fermo() {
    var c = document.documentElement.classList;
    return c.contains('a11y-pause-anim') || c.contains('a11y-pause-animations') ||
      !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  /* I browser che non conoscono le opzioni di scorrimento (Safari fino alla 15.3) non conoscono nemmeno lo
     scorrimento dolce: lì basta la forma di sempre. */
  function scorri(quanto, diColpo) {
    if (!('scrollBehavior' in document.documentElement.style)) { window.scrollBy(0, quanto); return; }
    try {
      window.scrollBy({ top: quanto, left: 0, behavior: (diColpo || fermo()) ? 'instant' : 'auto' });
    } catch (e) { window.scrollBy(0, quanto); }
  }
  /* Dopo una scelta dai menu: se il conteggio e i pulsanti sono finiti sotto il fondo dello schermo, la
     pagina scende quel tanto che basta a mostrarli, senza far uscire dall'alto il menu appena usato.
     Il fuoco resta sul menu. Di colpo, non in modo dolce: da tastiera il menu cambia a ogni freccia, e una
     misura presa a metà di uno scorrimento farebbe oscillare la pagina. */
  function scopriEsito(menu) {
    var r = (azioni || conteggio).getBoundingClientRect();
    var fondo = fondoVisibile(r);
    var spazio = menu.getBoundingClientRect().top - 8;
    if (r.bottom > fondo - 8 && spazio > 0) scorri(Math.min(r.bottom - fondo + 16, spazio), true);
  }
  /* Con il pulsante o con l'invio: l'elenco in cima allo schermo, sotto la testata, e il fuoco sulla riga
     che dice quanti prodotti ci sono. */
  function vaiA(el) {
    if (!el || el.hidden) return;
    scorri(el.getBoundingClientRect().top - 110);
    try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
  }

  if (window.URLSearchParams) {
    var iniziali = new URLSearchParams(window.location.search);
    if (iniziali.get('q')) cerca.value = iniziali.get('q').slice(0, 80);
    if (iniziali.get('regione') && haOpzione(regione, iniziali.get('regione'))) regione.value = iniziali.get('regione');
    if (iniziali.get('tipo') && haOpzione(gruppo, iniziali.get('tipo'))) gruppo.value = iniziali.get('tipo');
  }

  cerca.addEventListener('input', function () { filtra(); });
  cerca.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' || e.isComposing || e.keyCode === 229) return;
    e.preventDefault();
    filtra();
    if (trovati && !trovati.hidden) vaiA(trovati);
    else if (nessuno && !nessuno.hidden) vaiA(nessuno);
  });
  regione.addEventListener('change', function () { filtra(); scopriEsito(regione); });
  gruppo.addEventListener('change', function () { filtra(); scopriEsito(gruppo); });
  if (vai) {
    vai.addEventListener('click', function (e) {
      e.preventDefault();
      vaiA(trovati);
    });
  }
  if (azzera) {
    azzera.addEventListener('click', function () {
      cerca.value = '';
      regione.value = '';
      gruppo.value = '';
      filtra();
      cerca.focus();
    });
  }
  filtra(true);
  filtri.hidden = false;
})();
