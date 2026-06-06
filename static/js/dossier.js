/* ============================================================
   dossier.js — interattività dei dossier scrollytelling.
   Vanilla JS, nessuna dipendenza. Accessibile da tastiera,
   rispetta prefers-reduced-motion e html.a11y-pause-anim.
   ============================================================ */
(function () {
  "use strict";
  var root = document.querySelector(".dossier");
  if (!root) return;

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function animOff() {
    return reduce || document.documentElement.classList.contains("a11y-pause-anim");
  }

  /* 1. Comparsa al viewport (reveal) -------------------------- */
  var reveals = root.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.18, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* 2. Barra di avanzamento lettura --------------------------- */
  var bar = root.querySelector(".dossier-progress > span");
  var backLink = root.querySelector(".dossier-back");
  /* 3. Navigazione a pallini (sezione attiva) ----------------- */
  var dots = Array.prototype.slice.call(root.querySelectorAll(".dossier-dots a"));
  var sections = dots.map(function (d) { return document.getElementById(d.getAttribute("href").slice(1)); });

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var st = window.pageYOffset || document.documentElement.scrollTop;
      var docH = document.documentElement.scrollHeight - window.innerHeight;
      if (bar) bar.style.width = (docH > 0 ? (st / docH) * 100 : 0) + "%";
      if (backLink) backLink.classList.toggle("is-visible", st > window.innerHeight * 0.6);

      if (dots.length) {
        var mid = st + window.innerHeight * 0.4, active = 0;
        sections.forEach(function (s, i) { if (s && s.offsetTop <= mid) active = i; });
        dots.forEach(function (d, i) { d.classList.toggle("is-active", i === active); });
      }
      // parallax delle scene (lo sfondo scorre più lento del testo)
      if (!animOff()) {
        root.querySelectorAll(".dossier-scena__bg").forEach(function (bg) {
          var r = bg.parentElement.getBoundingClientRect();
          if (r.bottom > -60 && r.top < window.innerHeight + 60) {
            var prog = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
            bg.style.transform = "translateY(" + (prog * -34).toFixed(1) + "px) scale(1.08)";
          }
        });
      }
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* 4. Contatori animati -------------------------------------- */
  function animateNum(el) {
    var target = parseFloat(el.getAttribute("data-to"));
    var dec = (el.getAttribute("data-dec") || "0") | 0;
    if (isNaN(target)) return;
    if (animOff()) { el.firstChild ? (el.childNodes[0].nodeValue = fmt(target, dec)) : (el.textContent = fmt(target, dec)); return; }
    var start = null, dur = 1400;
    function fmt(v, d) { return v.toFixed(d).replace(".", ","); }
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.childNodes[0].nodeValue = fmt(target * eased, dec);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var nums = root.querySelectorAll(".dossier-dato__num[data-to]");
  if ("IntersectionObserver" in window && nums.length) {
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { animateNum(e.target); io2.unobserve(e.target); } });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { io2.observe(n); });
  } else {
    nums.forEach(animateNum);
  }

  /* 5. Slider di confronto ------------------------------------ */
  root.querySelectorAll(".dossier-confronto").forEach(function (c) {
    var range = c.querySelector('input[type="range"]');
    function set(v) { c.style.setProperty("--pos", v + "%"); }
    if (range) {
      set(range.value);
      range.addEventListener("input", function () { set(range.value); });
    }
  });

  /* 6. Hotspot (popover accessibile) -------------------------- */
  var openPunto = null;
  function closePunto() { if (openPunto) { openPunto.setAttribute("aria-expanded", "false"); openPunto = null; } }
  root.querySelectorAll(".dossier-punto").forEach(function (p) {
    p.setAttribute("aria-expanded", "false");
    p.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var wasOpen = p.getAttribute("aria-expanded") === "true";
      closePunto();
      if (!wasOpen) {
        p.setAttribute("aria-expanded", "true"); openPunto = p;
        p.classList.remove("is-below", "is-left-pop", "is-right-pop");
        if (p.getBoundingClientRect().top < 210) p.classList.add("is-below");
        var pop = p.querySelector(".dossier-punto__pop");
        if (pop) {
          var pr = pop.getBoundingClientRect();
          if (pr.right > window.innerWidth - 12) p.classList.add("is-left-pop");
          else if (pr.left < 12) p.classList.add("is-right-pop");
        }
      }
    });
  });
  document.addEventListener("click", closePunto);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { if (openPunto) { var t = openPunto; closePunto(); t.focus(); } } });

  /* 7. Copia link (condivisione) ------------------------------ */
  var copyBtn = root.querySelector("[data-dossier-copy]");
  if (copyBtn) copyBtn.addEventListener("click", function () {
    var url = copyBtn.getAttribute("data-dossier-copy");
    var done = function () { copyBtn.classList.add("is-copied"); setTimeout(function () { copyBtn.classList.remove("is-copied"); }, 1800); };
    if (navigator.clipboard) { navigator.clipboard.writeText(url).then(done, function () {}); } else { done(); }
  });

  /* 8. Condivisione nativa (mobile) ---------------------------- */
  var natBtn = root.querySelector("[data-dossier-share]");
  if (natBtn) {
    if (navigator.share) {
      natBtn.addEventListener("click", function () {
        navigator.share({ title: document.title, url: location.href }).catch(function () {});
      });
    } else { natBtn.hidden = true; }
  }

  /* 9. Hotspot: i punti compaiono "a cascata" quando l'immagine entra ---- */
  var hotspots = root.querySelectorAll(".dossier-hotspot");
  if ("IntersectionObserver" in window && hotspots.length) {
    var io3 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-revealed"); io3.unobserve(e.target); } });
    }, { threshold: 0.35 });
    hotspots.forEach(function (h) { io3.observe(h); });
  } else {
    hotspots.forEach(function (h) { h.classList.add("is-revealed"); });
  }

  /* 10. Elementi decorativi animati (stelle cadenti, anelli orbitanti) --- */
  if (!animOff()) {
    root.querySelectorAll(".dossier-dati, .dossier-chiusura").forEach(function (sec) {
      var s1 = document.createElement("span"); s1.className = "dossier-shootstar"; s1.setAttribute("aria-hidden", "true");
      var s2 = document.createElement("span"); s2.className = "dossier-shootstar s2"; s2.setAttribute("aria-hidden", "true");
      sec.appendChild(s1); sec.appendChild(s2);
    });
    root.querySelectorAll(".dossier-chiusura").forEach(function (sec) {
      var o1 = document.createElement("span"); o1.className = "dossier-orbit"; o1.setAttribute("aria-hidden", "true");
      var o2 = document.createElement("span"); o2.className = "dossier-orbit r2"; o2.setAttribute("aria-hidden", "true");
      sec.insertBefore(o2, sec.firstChild); sec.insertBefore(o1, sec.firstChild);
    });
  }

  /* 11. Slider di confronto: piccola "spinta" automatica alla prima vista - */
  root.querySelectorAll(".dossier-confronto").forEach(function (c) {
    var range = c.querySelector('input[type="range"]');
    if (!range) return;
    var touched = false;
    range.addEventListener("pointerdown", function () { touched = true; });
    range.addEventListener("keydown", function () { touched = true; });
    if (animOff() || !("IntersectionObserver" in window)) return;
    var ioN = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        ioN.unobserve(e.target);
        if (touched) return;
        var seq = [50, 64, 38, 50], i = 0;
        (function nudge() {
          if (touched || i >= seq.length) return;
          var from = parseFloat(c.style.getPropertyValue("--pos")) || 50, to = seq[i++], t0 = null;
          function anim(ts) {
            if (touched) return;
            if (t0 === null) t0 = ts;
            var p = Math.min((ts - t0) / 520, 1), eased = 1 - Math.pow(1 - p, 3);
            var v = from + (to - from) * eased;
            c.style.setProperty("--pos", v + "%");
            range.value = v;
            if (p < 1) requestAnimationFrame(anim); else setTimeout(nudge, 120);
          }
          requestAnimationFrame(anim);
        })();
      });
    }, { threshold: 0.55 });
    ioN.observe(c);
  });
})();
