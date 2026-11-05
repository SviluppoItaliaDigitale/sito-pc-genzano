const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
function alTelefono(el, sel, x, y, s, t) { el.querySelector(sel).setAttribute("transform", `translate(${(x + 46 * s).toFixed(1)} ${(y - 222 * s + Math.sin(t * 3.2) * 3).toFixed(1)}) scale(${s.toFixed(2)}) rotate(18)`); }
const raggi = (el, t) => el.querySelectorAll(".raggi").forEach(r => r.setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`));
const ANIM = {
  sole: (el, u, t) => {
    raggi(el, t); const s = el.querySelector(".sole"); s.setAttribute("transform", `translate(300 150) scale(${(1 + Math.sin(t * 3) * .05).toFixed(3)})`);
    el.querySelector(".liv").setAttribute("transform", `translate(0 ${(lerp(60, 0, outCubic(prog(u, .4, 2.5)))).toFixed(1)})`);
    anima(el, ".flavio", t, { x: 340, y: 488, s: .55, aD: 160, aS: 14, bocca: "o" });
    el.querySelector(".goccia").setAttribute("transform", `translate(${380} ${(300 + ((t * 40) % 60)).toFixed(1)})`);
  },
  acqua: (el, u, t) => {
    const b = el.querySelector(".borr"); b.setAttribute("transform", `translate(370 ${(300 + Math.sin(t * 2) * 6).toFixed(1)}) rotate(${(lerp(0, -40, inOutCubic(prog(u, 1.4, .8))) * (u < 4.5 ? 1 : 1 - prog(u, 4.5, .6))).toFixed(1)})`);
    el.querySelectorAll(".gocce path").forEach(g => { const i = +g.dataset.i, q = (t * 1.2 + i * .33) % 1; g.setAttribute("transform", `translate(${(380 + i * 18).toFixed(1)} ${(240 - q * 100).toFixed(1)})`); g.setAttribute("opacity", (Math.sin(q * Math.PI) * prog(u, 2, .5)).toFixed(2)); });
    anima(el, ".flavio", t, { x: 470, y: 470, s: .6, aS: 100, aD: 14 });
  },
  ore: (el, u, t) => {
    raggi(el, t); const a = lerp(330, 540, (u / 6) % 1); el.querySelector(".lancetta").setAttribute("transform", `rotate(${a.toFixed(1)})`);
    const p = inOutCubic(prog(u, 1, 2)); anima(el, ".flavio", t, { x: lerp(290, 420, p), y: 470, s: .5, cammina: p > 0 && p < 1 ? 1 : 0, aS: p >= 1 ? 120 : 14 });
  },
  vestiti: (el, u, t) => {
    const at = CONFIG.scene[3].listaAt, x = 250, y = 470, s = .62;
    anima(el, ".flavio", t, { x, y, s, aS: 14, aD: 14 });
    const c = el.querySelector(".capp"), pc = prog(u, at[1], .7); c.setAttribute("transform", `translate(${x} ${(lerp(-60, y - 260 * s - 20, outBack(pc))).toFixed(1)}) scale(.9)`); c.style.opacity = pc > 0 ? 1 : 0;
    const o = el.querySelector(".occh"), po = prog(u, at[1] + .6, .5); o.setAttribute("transform", `translate(${x} ${(y - 224 * s + 2).toFixed(1)}) scale(${(s * lerp(2, 1, outBack(po))).toFixed(3)})`); o.style.opacity = po > 0 ? 1 : 0;
    pop(el, ".frut", prog(u, at[2], .8));
  },
  auto: (el, u, t) => {
    raggi(el, t); pop(el, ".no", prog(u, 1, .8));
    el.querySelectorAll(".onde path").forEach(p => { const i = +p.dataset.i, q = (t * .8 + i * .33) % 1; p.setAttribute("transform", `translate(${(180 + i * 70).toFixed(1)} ${(250 - q * 60).toFixed(1)})`); p.setAttribute("opacity", Math.sin(q * Math.PI).toFixed(2)); });
  },
  vicini: (el, u, t) => {
    const p = inOutCubic(prog(u, .4, 2)), mov = p > 0 && p < 1 ? 1 : 0;
    anima(el, ".nonna", t, { x: 445, y: 470, s: .55, aS: 14, aD: p >= 1 ? 90 : 14, fase: 2, bocca: "sorriso" });
    anima(el, ".mamma", t, { x: lerp(60, 250, p), y: 470, s: .58, cammina: mov, aD: 30 });
    anima(el, ".flavio", t, { x: lerp(-40, 330, p), y: 470, s: .45, cammina: mov, fase: 1, aD: p >= 1 ? 150 : 20, agitaD: p >= 1 });
    const cg = el.querySelector(".cuore"), c = cg.firstElementChild; cg.setAttribute("transform", `translate(390 ${(200 + Math.sin(t * 3) * 6).toFixed(1)})`);
    const pc = prog(u, 3, .8); c.style.opacity = pc > 0 ? 1 : 0; c.style.transformBox = "fill-box"; c.style.transformOrigin = "50% 50%"; c.style.transform = `scale(${(1.4 * outElastic(pc)).toFixed(3)})`;
  },
  malore: (el, u, t) => {
    anima(el, ".mamma", t, { x: 330, y: 470, s: .6, aD: u > 2.2 ? 165 : 30, aS: 14 }); alTelefono(el, ".cell", 330, 470, .6, t); el.querySelector(".cell").style.opacity = prog(u, 2.2, .3);
    const p = inOutCubic(prog(u, .4, 1.4)); anima(el, ".flavio", t, { x: lerp(560, 450, p), y: 470, s: .45, cammina: p > 0 && p < 1 ? 1 : 0, aS: 120, fase: 1 });
    const f = el.querySelector(".fum"); f.setAttribute("transform", `translate(420 160)`); svgPop(f.firstElementChild, prog(u, 2.6, .8));
  },
  sereno: (el, u, t) => {
    const s = el.querySelector(".sole"); s.setAttribute("transform", `translate(470 ${lerp(220, 110, outBack(prog(u, .1, 1.2))).toFixed(1)})`); raggi(el, t);
    anima(el, ".flavio", t, { x: 310, y: 492, s: .5, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 420, y: 492, s: .5, aS: 150, agitaS: true, fase: 2 });
  }
};
