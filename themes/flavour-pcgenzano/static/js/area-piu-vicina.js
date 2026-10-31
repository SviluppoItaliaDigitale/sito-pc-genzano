/* «Trova l'area di attesa più vicina»: posizione del browser (solo dopo il
   permesso), distanza in linea d'aria con la formula dell'emisenoverso dalle
   aree di attesa del Piano, le tre più vicine. Nessuna richiesta di rete.
   Markup e dati nello shortcode area-piu-vicina.html. */
(function () {
  "use strict";
  if (!("geolocation" in navigator)) return;

  function distanzaMetri(lat1, lon1, lat2, lon2) {
    var R = 6371000, rad = Math.PI / 180;
    var dLat = (lat2 - lat1) * rad, dLon = (lon2 - lon1) * rad;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * R * Math.asin(Math.sqrt(a));
  }
  function testoDistanza(m) {
    if (m < 1000) return "circa " + (Math.round(m / 10) * 10) + " metri";
    return "circa " + (m / 1000).toFixed(1).replace(".", ",") + " km";
  }
  function el(tag, testo, attr) {
    var n = document.createElement(tag);
    if (testo) n.textContent = testo;
    if (attr) Object.keys(attr).forEach(function (k) { n.setAttribute(k, attr[k]); });
    return n;
  }

  function avvia(box) {
    var aree;
    try { aree = JSON.parse(box.getAttribute("data-aree")); } catch (e) { return; }
    if (!aree || !aree.length) return;
    var cartelli = box.getAttribute("data-cartelli") || "/cartelli/";
    var elenco = box.getAttribute("data-elenco") || "/aree-attesa/";
    var btn = box.querySelector(".area-vicina-btn");
    var esito = box.querySelector(".area-vicina-esito");
    var etichetta = btn.innerHTML;
    box.hidden = false;

    function messaggio(t) { esito.textContent = ""; esito.appendChild(el("p", t)); }

    btn.addEventListener("click", function () {
      btn.disabled = true;
      btn.textContent = "Cerco la tua posizione…";
      messaggio("Cerco la tua posizione…");
      navigator.geolocation.getCurrentPosition(function (pos) {
        var lat = pos.coords.latitude, lon = pos.coords.longitude;
        var ordinate = aree.map(function (a) {
          return { a: a, m: distanzaMetri(lat, lon, a.lat, a.lon) };
        }).sort(function (x, y) { return x.m - y.m; });
        esito.textContent = "";
        if (ordinate[0].m > 15000) {
          // Lontano da Genzano: niente indicazioni a piedi per decine di km.
          var lontano = el("p", "Sembri lontano da Genzano di Roma: l'area di attesa più vicina è a " +
            testoDistanza(ordinate[0].m) + ". Per il posto in cui ti trovi consulta il piano di emergenza di quel Comune. Le aree di Genzano sono nell'");
          lontano.appendChild(el("a", "elenco delle aree di attesa", { href: elenco }));
          lontano.appendChild(document.createTextNode("."));
          esito.appendChild(lontano);
          btn.innerHTML = etichetta;
          btn.disabled = false;
          return;
        }
        esito.appendChild(el("p", "Le aree di attesa più vicine a te, in linea d'aria:"));
        var lista = el("ol");
        ordinate.slice(0, 3).forEach(function (o) {
          var li = el("li");
          li.appendChild(el("strong", o.a.id + " — " + o.a.nome));
          li.appendChild(document.createTextNode(", " + o.a.indirizzo + ": "));
          li.appendChild(el("span", testoDistanza(o.m), { "class": "area-vicina-dist" }));
          li.appendChild(el("br"));
          var dest = o.a.lat + "," + o.a.lon;
          li.appendChild(el("a", "Indicazioni a piedi (Google Maps)", {
            href: "https://www.google.com/maps/dir/?api=1&travelmode=walking&destination=" + dest,
            target: "_blank", rel: "noopener noreferrer"
          }));
          li.appendChild(document.createTextNode(" · "));
          li.appendChild(el("a", "Cartello dell'area", {
            href: cartelli + o.a.id + ".png", target: "_blank", rel: "noopener"
          }));
          lista.appendChild(li);
        });
        esito.appendChild(lista);
        // Stesse indicazioni della pagina sul rischio sismico (§ «Cosa fare DURANTE» e «DOPO»).
        var nota = "La distanza è in linea d'aria. Vai a piedi per un percorso sicuro: stai lontano da costruzioni danneggiate, alberi, lampioni e linee elettriche, e cerca il cartello con il codice dell'area.";
        if (pos.coords.accuracy > 300) {
          nota += " La posizione del telefono è approssimativa (circa " + testoDistanza(pos.coords.accuracy).replace("circa ", "") + "): controlla l'area sulla tabella.";
        }
        esito.appendChild(el("p", nota));
        btn.innerHTML = etichetta;
        btn.disabled = false;
      }, function (err) {
        var t = "Non riesco a leggere la tua posizione.";
        if (err.code === 1) t = "Non hai dato il permesso di usare la posizione.";
        if (err.code === 3) t = "La posizione non è arrivata in tempo.";
        esito.textContent = "";
        var p = el("p", t + " Trova la tua area cercando la via più vicina a te nell'");
        p.appendChild(el("a", "elenco delle aree di attesa", { href: elenco }));
        p.appendChild(document.createTextNode("."));
        esito.appendChild(p);
        btn.innerHTML = etichetta;
        btn.disabled = false;
      }, { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 });
    });
  }

  function init() { document.querySelectorAll(".area-vicina").forEach(avvia); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
