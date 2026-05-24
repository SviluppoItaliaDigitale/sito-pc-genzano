/* Condivisione delle cartine meteo (immagine SVG / clip WebP).
   Pulsanti con [data-condividi-cartina] + data-img + data-title.
   Prova a condividere il FILE (Web Share API con files), poi il link di pagina,
   infine fallback: scarica l'immagine + copia il link. Privacy-first, nessun SDK. */
(function () {
  if (window.__condividiCartina) return;
  window.__condividiCartina = true;

  function scarica(url, nome) {
    var a = document.createElement("a");
    a.href = url; a.download = nome || ""; a.rel = "noopener";
    document.body.appendChild(a); a.click(); a.remove();
  }

  function slug(s) { return (s || "cartina").replace(/[^a-z0-9]+/gi, "-").toLowerCase().replace(/^-|-$/g, ""); }

  function feedback(btn, msg) {
    var t = btn.querySelector(".cartina-azione-label");
    if (!t) return;
    var old = t.getAttribute("data-old") || t.textContent;
    t.setAttribute("data-old", old);
    t.textContent = msg;
    setTimeout(function () { t.textContent = old; }, 2200);
  }

  async function copiaLink(btn, pagina) {
    try { await navigator.clipboard.writeText(pagina); feedback(btn, "Link copiato"); return; }
    catch (e) { /* prova il fallback execCommand */ }
    try {
      var ta = document.createElement("textarea");
      ta.value = pagina; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove();
      feedback(btn, "Link copiato");
    } catch (e) { feedback(btn, "Copia il link dalla barra"); }
  }

  async function condividi(btn) {
    var url = btn.getAttribute("data-img");
    var titolo = btn.getAttribute("data-title") || "Cartina meteo";
    // URL ASSOLUTO della cartina (non della pagina): è questo che si condivide/copia.
    var imgAbs = url ? new URL(url, location.href).href : location.href;
    // 1) condividi il FILE (ideale su mobile: condivide la cartina / la clip)
    if (navigator.canShare && url) {
      try {
        var resp = await fetch(url);
        var blob = await resp.blob();
        var ext = (blob.type.split("/")[1] || "png").replace("svg+xml", "svg");
        var file = new File([blob], slug(titolo) + "." + ext, { type: blob.type });
        if (navigator.canShare({ files: [file] })) {
          await navigator.share({ files: [file], title: titolo, text: titolo });
          return;
        }
      } catch (e) { if (e && e.name === "AbortError") return; }
    }
    // 2) condividi il LINK della cartina (Web Share senza file)
    if (navigator.share) {
      try { await navigator.share({ title: titolo, text: titolo, url: imgAbs }); return; }
      catch (e) { if (e && e.name === "AbortError") return; }
    }
    // 3) fallback desktop: copia il link della CARTINA negli appunti (non la pagina)
    copiaLink(btn, imgAbs);
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-condividi-cartina]");
    if (b) { e.preventDefault(); condividi(b); }
  });
})();
