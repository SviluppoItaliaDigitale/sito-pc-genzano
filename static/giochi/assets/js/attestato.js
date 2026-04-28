/* Generazione attestato stampabile — Protezione Civile Genzano
   Produce un SVG A4 landscape scaricabile o stampabile. */

(function (global) {
  'use strict';

  function sanitizzaNome(nome) {
    if (!nome) return '';
    var s = String(nome).trim();
    s = s.replace(/[<>"'`\\]/g, '');
    if (s.length > 40) s = s.substring(0, 40);
    return s;
  }

  function dataOggi() {
    var d = new Date();
    return d.toLocaleDateString('it-IT', { day: '2-digit', month: 'long', year: 'numeric' });
  }

  function nomeGioco(idGioco) {
    if (global.GiochiPC && global.GiochiPC.CATALOGO && global.GiochiPC.CATALOGO[idGioco]) {
      return global.GiochiPC.CATALOGO[idGioco].nome;
    }
    return 'Gioco della Sicurezza';
  }

  // A4 landscape a 72 dpi: 842 x 595 pt
  // tipo: "completato" (>=80%) | "partecipazione" (<80%) | "incluso" (giochi
  //        accessibili senza scoring: chi partecipa riceve l'attestato pieno)
  function costruisciSVG(nome, idGioco, percentuale, tipo) {
    var n = sanitizzaNome(nome) || 'Partecipante';
    var gioco = nomeGioco(idGioco);
    var data = dataOggi();
    var perc = Math.max(0, Math.min(100, Math.round(percentuale || 0)));
    tipo = tipo || 'completato';

    // Testo del corpo: cambia in funzione del tipo. Per partecipazione il
    // tono e' incentivante ("ha partecipato + continua ad esercitarti"),
    // mai svalutativo del bambino o del giocatore.
    var rigaAzione, rigaPercentuale, coloreAccento;
    if (tipo === 'partecipazione') {
      rigaAzione = 'ha partecipato al gioco educativo';
      rigaPercentuale = 'Continua a esercitarti: con un po’ di pratica raggiungerai il punteggio completo.';
      coloreAccento = '#b45309'; // ambra istituzionale per "in corso d'opera"
    } else if (tipo === 'incluso') {
      rigaAzione = 'ha partecipato al gioco educativo';
      rigaPercentuale = 'Grazie per aver giocato con noi!';
      coloreAccento = '#008758';
    } else {
      rigaAzione = 'ha completato con successo il gioco educativo';
      rigaPercentuale = 'con il ' + perc + '% di risposte corrette';
      coloreAccento = '#008758';
    }

    var svg = ''
      + '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 842 595" width="842" height="595">'
      + '<defs>'
      + '<linearGradient id="sfondo" x1="0" y1="0" x2="1" y2="1">'
      + '<stop offset="0" stop-color="#f7f9fc"/><stop offset="1" stop-color="#e8f0fe"/>'
      + '</linearGradient>'
      + '<linearGradient id="fascia" x1="0" y1="0" x2="1" y2="0">'
      + '<stop offset="0" stop-color="#003366"/><stop offset="1" stop-color="#0066CC"/>'
      + '</linearGradient>'
      + '</defs>'
      // Sfondo
      + '<rect width="842" height="595" fill="url(#sfondo)"/>'
      // Cornice decorativa
      + '<rect x="22" y="22" width="798" height="551" fill="none" stroke="#003366" stroke-width="3"/>'
      + '<rect x="32" y="32" width="778" height="531" fill="none" stroke="#0066CC" stroke-width="1"/>'
      // Decorazioni angoli (colore che cambia leggermente in modalita' partecipazione)
      + '<circle cx="60" cy="60" r="6" fill="' + coloreAccento + '"/>'
      + '<circle cx="782" cy="60" r="6" fill="' + coloreAccento + '"/>'
      + '<circle cx="60" cy="535" r="6" fill="' + coloreAccento + '"/>'
      + '<circle cx="782" cy="535" r="6" fill="' + coloreAccento + '"/>'
      // Fascia titolo
      + '<rect x="32" y="70" width="778" height="70" fill="url(#fascia)"/>'
      + '<text x="421" y="115" text-anchor="middle" font-family="Titillium Web, Arial, sans-serif" font-size="32" font-weight="700" fill="#fff">ATTESTATO DI PARTECIPAZIONE</text>'
      // Sottotitolo
      + '<text x="421" y="185" text-anchor="middle" font-family="Titillium Web, Arial, sans-serif" font-size="16" fill="#17324D">Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma</text>'
      // Si attesta che
      + '<text x="421" y="240" text-anchor="middle" font-family="Titillium Web, Arial, sans-serif" font-size="18" fill="#17324D">Si attesta che</text>'
      // Nome
      + '<text x="421" y="295" text-anchor="middle" font-family="Lora, Georgia, serif" font-size="38" font-weight="700" fill="#003366">'
      + escapeXml(n)
      + '</text>'
      + '<line x1="240" y1="310" x2="602" y2="310" stroke="#003366" stroke-width="1"/>'
      // Riga azione (cambia in funzione del tipo)
      + '<text x="421" y="355" text-anchor="middle" font-family="Titillium Web, Arial, sans-serif" font-size="16" fill="#17324D">'
      + escapeXml(rigaAzione)
      + '</text>'
      + '<text x="421" y="395" text-anchor="middle" font-family="Titillium Web, Arial, sans-serif" font-size="24" font-weight="700" fill="#003366">'
      + escapeXml(gioco)
      + '</text>'
      // Riga percentuale o messaggio incentivante
      + '<text x="421" y="440" text-anchor="middle" font-family="Titillium Web, Arial, sans-serif" font-size="' + (tipo === 'partecipazione' ? '15' : '18') + '" fill="' + coloreAccento + '" font-weight="' + (tipo === 'partecipazione' ? '600' : '700') + '">'
      + escapeXml(rigaPercentuale)
      + '</text>'
      // Data
      + '<text x="80" y="520" font-family="Titillium Web, Arial, sans-serif" font-size="13" fill="#17324D">Rilasciato il ' + escapeXml(data) + '</text>'
      + '<text x="762" y="520" text-anchor="end" font-family="Titillium Web, Arial, sans-serif" font-size="13" fill="#17324D" font-style="italic">Gruppo Comunale Volontari PC Genzano</text>'
      // Firma simbolica
      + '<line x1="550" y1="490" x2="762" y2="490" stroke="#003366" stroke-width="1"/>'
      // Footer licenza
      + '<text x="421" y="555" text-anchor="middle" font-family="Titillium Web, Arial, sans-serif" font-size="10" fill="#5b6b7c">protezionecivilegenzano.it — CC BY 4.0</text>'
      + '</svg>';
    return svg;
  }

  function escapeXml(s) {
    return String(s).replace(/[<>&'"]/g, function (c) {
      return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '\'': '&apos;', '"': '&quot;' }[c];
    });
  }

  function generaAttestato(nome, idGioco, percentuale, tipo) {
    var svg = costruisciSVG(nome, idGioco, percentuale, tipo);
    try {
      var blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      var dataFile = new Date().toISOString().substring(0, 10);
      a.href = url;
      a.download = 'attestato-' + (idGioco || 'gioco') + '-' + dataFile + '.svg';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
      return true;
    } catch (e) {
      console.log('[Attestato] download fallito:', e && e.message);
      return false;
    }
  }

  function anteprimaAttestato(nome, idGioco, percentuale, tipo) {
    return costruisciSVG(nome, idGioco, percentuale, tipo);
  }

  function stampaAttestato(nome, idGioco, percentuale, tipo) {
    var svg = costruisciSVG(nome, idGioco, percentuale, tipo);
    var w = window.open('', '_blank');
    if (!w) return false;
    w.document.write('<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Attestato</title>'
      + '<style>@page{size:A4 landscape;margin:0}body{margin:0}svg{width:100vw;height:100vh;display:block}</style>'
      + '</head><body>' + svg + '<script>window.onload=function(){setTimeout(function(){window.print()},200)}<\/script></body></html>');
    w.document.close();
    return true;
  }

  global.AttestatoPC = {
    genera: generaAttestato,
    stampa: stampaAttestato,
    anteprima: anteprimaAttestato,
    sanitizzaNome: sanitizzaNome
  };
})(typeof window !== 'undefined' ? window : this);
