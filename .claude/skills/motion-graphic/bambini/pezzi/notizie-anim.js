const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
function bolle(el, u, sel = ".bolla", passo = .45, da = .4) {
  el.querySelectorAll(sel).forEach(b => {
    const i = +b.dataset.i, p = prog(u, da + i * passo, .6);
    b.style.opacity = clamp(p * 4); b.style.transformBox = "fill-box"; b.style.transformOrigin = "0 50%";
    b.style.transform = `scale(${outElastic(p).toFixed(3)})`;
  });
}
const ANIM = {
  telefono: (el, u, t) => {
    bolle(el, u + 3);
    pop(el, ".si", prog(u + 4, 0, 1)); pop(el, ".no", prog(u + 4, 0, 1));
    ["si", "no"].forEach((c, i) => { const g = el.querySelector(`.${c} > g`); g.style.transform += ` rotate(${(Math.sin(t * 2.4 + i * 2) * 8).toFixed(1)}deg)`; });
    anima(el, ".flavio", t, { x: 530, y: 492, s: .5, aS: 150, agitaS: true, aD: 14 });
  },
  chat: (el, u, t) => {
    bolle(el, u, ".x", .4, .2);
    el.querySelectorAll(".vb").forEach(b => {
      const i = +b.dataset.i, ciclo = 2.6, p = ((u - .8 - i * .37) / ciclo), q = p - Math.floor(p);
      if (u < .8 + i * .37) { b.style.opacity = 0; return; }
      const x = lerp(170, 560, q) + Math.sin(q * 9 + i) * 18, y = lerp(240, -40, q) + Math.sin(q * 6 + i * 2) * 26;
      b.parentNode.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
      b.style.opacity = (clamp(q * 6) * clamp((1 - q) * 4)).toFixed(2);
      b.style.transformBox = "fill-box"; b.style.transformOrigin = "50% 50%"; b.style.transform = `rotate(${(Math.sin(q * 8 + i) * 10).toFixed(1)}deg) scale(${lerp(.7, 1.05, q).toFixed(2)})`;
    });
    anima(el, ".flavio", t, { x: 470, y: 496, s: .5, aS: 165, aD: 165, bocca: "o" });
  },
  lente: (el, u, t, D) => {
    const at = CONFIG.scene[2].listaAt;
    const x = 270 + Math.sin(u * 1.5) * 120, y = 140 + Math.sin(u * 2.3) * 30;
    el.querySelector(".lente").setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
    at.forEach((a, j) => pop(el, ".b" + j, prog(u, a, .8)));
    anima(el, ".flavio", t, { x: 530, y: 500, s: .42, aS: 140, aD: 14, bocca: u > at[2] + .5 ? "sorriso" : "o" });
  },
  inoltra: (el, u, t) => {
    bolle(el, u + 2);
    const f = el.querySelector(".freccia"); f.setAttribute("transform", `translate(${lerp(170, 236, outCubic(prog(u, .5, 1))).toFixed(1)} 250)`);
    f.style.opacity = clamp(prog(u, .5, .3));
    pop(el, ".stop", prog(u, 1.4, .9));
    const s = el.querySelector(".stop > g"); if (u > 2.3) s.style.transform += ` rotate(${(Math.sin(t * 3) * 6).toFixed(1)}deg)`;
    anima(el, ".flavio", t, { x: 500, y: 496, s: .5, aD: 165, aS: 14, bocca: "sorriso" });
  },
  adulto: (el, u, t, D) => {
    anima(el, ".ins", t, { x: 200, y: 470, s: .66, aD: 110, aS: 14 });
    el.querySelector(".tel").setAttribute("transform", `translate(${(200 + 34 * .66 + 72 * .66).toFixed(1)} ${(470 - 170 * .66 + Math.sin(t * 3.2) * 3).toFixed(1)}) rotate(-12)`);
    anima(el, ".flavio", t, { x: 400, y: 470, s: .5, aS: u > D * .55 ? 150 : 40, agitaS: u > D * .55, fase: 1.4, bocca: u > D * .55 ? "sorriso" : "o" });
    const fm = el.querySelector(".fumetto"); fm.setAttribute("transform", `translate(300 ${(110 + Math.sin(t * 2.5) * 5).toFixed(1)})`);
    svgPop(fm.firstElementChild, prog(u, .9, .8));
    const cambio = prog(u, D * .55, .4);
    el.querySelector(".dubbio").setAttribute("opacity", (1 - cambio).toFixed(2));
    const ce = el.querySelector(".certo"); ce.style.opacity = cambio; ce.style.transformBox = "fill-box"; ce.style.transformOrigin = "50% 50%"; ce.style.transform = `scale(${outElastic(cambio).toFixed(3)})`;
    const cg = el.querySelector(".cuore"), c = cg.firstElementChild; cg.setAttribute("transform", `translate(470 ${(250 + Math.sin(t * 3) * 6).toFixed(1)})`);
    const pc = prog(u, D * .62, .8); c.style.opacity = pc > 0 ? 1 : 0; c.style.transformBox = "fill-box"; c.style.transformOrigin = "50% 50%";
    c.style.transform = `scale(${(1.4 * outElastic(pc) * (1 + Math.sin(t * 6) * .06)).toFixed(3)})`;
  },
  sereno: (el, u, t) => {
    const s = el.querySelector(".sole"); s.setAttribute("transform", `translate(470 ${lerp(220, 110, outBack(prog(u, .1, 1.2))).toFixed(1)})`);
    el.querySelector(".raggi").setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`);
    anima(el, ".flavio", t, { x: 230, y: 492, s: .55, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 370, y: 492, s: .55, aS: 150, agitaS: true, fase: 2 });
  }
};
