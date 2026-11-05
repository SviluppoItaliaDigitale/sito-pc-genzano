/* Riquadro «Pagine di servizio» sopra i risultati di Pagefind.
   Quando la ricerca contiene una parola delle regole di data/ricerca.json
   (allerta, terremoto, 112, area di attesa…), mostra per prime le pagine
   operative: Pagefind da solo mette davanti gli articoli brevi con la parola
   nel titolo (audit esterno 31/10/2026, A12). Nessuna richiesta di rete. */
(function () {
  "use strict";
  function norma(t) {
    return (t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/\s+/g, " ").trim();
  }
  function corrisponde(query, parole) {
    var q = norma(query);
    if (q.length < 2) return false;
    var token = q.split(/[^a-z0-9']+/).filter(Boolean);
    return parole.some(function (p) {
      p = norma(p);
      if (p.indexOf(" ") >= 0) return q.indexOf(p) >= 0;
      return token.some(function (t) {
        // la parola cercata comincia con la regola («terremoti» → «terremot»),
        // oppure è l'inizio della regola mentre si scrive («terr» → «terremot»)
        return t.indexOf(p) === 0 || (t.length >= 4 && p.indexOf(t) === 0);
      });
    });
  }
  function avvia(box, voci) {
    var radice = document.getElementById(box.getAttribute("data-radice"));
    if (!radice) return;
    var lista = box.querySelector(".ricerca-servizio-lista");
    var ultimo = null;
    function aggiorna() {
      var campo = radice.querySelector(".pagefind-ui__search-input");
      var q = campo ? campo.value : "";
      var area0 = radice.querySelector(".pagefind-ui__results-area");
      var chiave = q + (area0 ? "|r" : "");
      if (chiave === ultimo) return;
      ultimo = chiave;
      var trovate = voci.filter(function (v) { return corrisponde(q, v.parole); }).slice(0, 3);
      lista.textContent = "";
      trovate.forEach(function (v) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = v.url;
        a.textContent = v.titolo;
        li.appendChild(a);
        if (v.descrizione) {
          var d = document.createElement("span");
          d.className = "ricerca-servizio-desc";
          d.textContent = v.descrizione;
          li.appendChild(d);
        }
        lista.appendChild(li);
      });
      // Fra il campo e i risultati, così il campo non si sposta mentre si scrive.
      var area = radice.querySelector(".pagefind-ui__results-area");
      if (area && box.nextSibling !== area) area.parentNode.insertBefore(box, area);
      box.hidden = trovate.length === 0 || !area;
    }
    setInterval(aggiorna, 300);
  }
  function init() {
    document.querySelectorAll(".ricerca-servizio").forEach(function (box) {
      var dati = box.nextElementSibling;
      if (!dati || !dati.classList.contains("ricerca-servizio-dati")) return;
      try { avvia(box, JSON.parse(dati.textContent)); } catch (e) { /* senza riquadro la ricerca funziona comunque */ }
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
