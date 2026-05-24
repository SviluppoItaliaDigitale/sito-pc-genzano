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

  async function condividi(btn) {
    var url = btn.getAttribute("data-img");
    var titolo = btn.getAttribute("data-title") || "Cartina meteo";
    var pagina = location.href;
    try {
      if (navigator.canShare && url) {
        var resp = await fetch(url);
        var blob = await resp.blob();
        var ext = (blob.type.split("/")[1] || "png").replace("svg+xml", "svg");
        var file = new File([blob], slug(titolo) + "." + ext, { type: blob.type });
        if (navigator.canShare({ files: [file] })) {
          await navigator.share({ files: [file], title: titolo, text: titolo });
          return;
        }
      }
      if (navigator.share) { await navigator.share({ title: titolo, text: titolo, url: pagina }); return; }
    } catch (e) {
      if (e && e.name === "AbortError") return; // l'utente ha annullato
    }
    // fallback: scarica l'immagine + copia il link di pagina
    if (url) scarica(url, slug(titolo));
    try {
      await navigator.clipboard.writeText(pagina);
      btn.setAttribute("data-copiato", "1");
      var t = btn.querySelector(".cartina-azione-label");
      if (t) { var old = t.textContent; t.textContent = "Link copiato"; setTimeout(function () { t.textContent = old; }, 2000); }
    } catch (e) { /* niente clipboard: il download è già partito */ }
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-condividi-cartina]");
    if (b) { e.preventDefault(); condividi(b); }
  });
})();
