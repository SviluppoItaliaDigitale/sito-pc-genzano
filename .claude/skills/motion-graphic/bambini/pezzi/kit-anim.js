const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
/* gli oggetti compaiono uno alla volta, poi volano nello zaino */
function riempi(el, u, t, D) {
  const ogg = el.querySelectorAll(".og"), n = ogg.length, via = D - 1.15;
  ogg.forEach(g => { const i = +g.dataset.i, x0 = +g.dataset.x, y0 = +g.dataset.y;
    const a = prog(u, .6 + i * .7, .8), f = inOutCubic(prog(u, via + i * .18, .7));
    const x = lerp(x0, 470, f), y = lerp(y0, 300, f) - Math.sin(f * Math.PI) * 120, s = (a <= 0 ? 0 : outElastic(a)) * lerp(1.5, .4, f);
    g.setAttribute("transform", `translate(${x.toFixed(1)} ${(y + Math.sin(t * 2.4 + i) * 4 * (1 - f)).toFixed(1)}) scale(${s.toFixed(3)}) rotate(${(f * 200 + Math.sin(t * 2 + i) * 5).toFixed(1)})`);
    g.style.opacity = f >= 1 ? 0 : 1; });
  const zb = el.querySelector(".zb > g"), k = prog(u, via + .45, 1); const w = Math.sin(k * Math.PI * 4) * (1 - k) * .12;
  zb.setAttribute("transform", `scale(${(1 + w).toFixed(3)} ${(1 - w).toFixed(3)})`);
}
const ANIM = {
  zaino: (el, u, t) => {
    const zb = el.querySelector(".zb > g"); zb.setAttribute("transform", `translate(0 ${(Math.sin(t * 2.2) * 6).toFixed(1)})`);
    const tr = el.querySelector(".tre"); tr.setAttribute("transform", `translate(420 140) rotate(${(Math.sin(t * 1.6) * 6).toFixed(1)})`); svgPop(tr.firstElementChild, 1);
    anima(el, ".flavio", t, { x: 440, y: 470, s: .55, aS: 140, aD: 14, agitaS: true });
  },
  cibo: riempi, cura: riempi, documenti: riempi, vestiti: riempi,
  luce: (el, u, t, D) => { riempi(el, u, t, D); el.querySelector(".raggio").setAttribute("opacity", (prog(u, .7, .4) * (1 - prog(u, D - 1.15, .3)) * (.45 + Math.sin(t * 6) * .15)).toFixed(2)); },
  suoni: (el, u, t, D) => { riempi(el, u, t, D);
    el.querySelectorAll(".suono path").forEach(p => { const i = +p.dataset.i, q = (t * 1.4 + i * .33) % 1; p.setAttribute("transform", `translate(${(20 + q * 60).toFixed(1)} 0) scale(${(.6 + q).toFixed(2)})`);
      p.setAttribute("opacity", (Math.sin(q * Math.PI) * prog(u, 1.4, .4) * (1 - prog(u, D - 1.15, .3))).toFixed(2)); }); },
  porta: (el, u, t) => {
    const c = el.querySelector(".cal"); c.setAttribute("transform", `translate(450 150) rotate(${(Math.sin(t * 1.5) * 5).toFixed(1)})`); svgPop(c.firstElementChild, prog(u, 2, 1));
    anima(el, ".mamma", t, { x: 400, y: 470, s: .58, aS: 30, aD: 14 });
    anima(el, ".flavio", t, { x: 510, y: 470, s: .46, aS: 150, agitaS: true, fase: 1 });
  }
};
