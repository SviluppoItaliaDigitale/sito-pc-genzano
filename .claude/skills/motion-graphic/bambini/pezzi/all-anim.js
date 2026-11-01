const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const raggi = (el, t) => el.querySelectorAll(".raggi").forEach(r => r.setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`));
function piove(el, t, v = 1) {
  const g = el.querySelector(".pioggia"); if (!g) return; const y0 = +g.dataset.y0, y1 = +g.dataset.y1;
  g.querySelectorAll("path").forEach(p => { const i = +p.dataset.i, q = (t * (1.3 + hash(i) * .6) * v + hash(i + 5)) % 1;
    p.setAttribute("transform", `translate(${(+p.dataset.x - q * 40).toFixed(1)} ${(y0 + q * (y1 - y0)).toFixed(1)})`); });
}
const onda = (el, y, t) => { const a = el.querySelector(".acq"); if (a) a.setAttribute("transform", `translate(${(Math.sin(t * 1.6) * 30 - 40).toFixed(1)} ${y.toFixed(1)})`); };
const ANIM = {
  pioggia: (el, u, t) => {
    piove(el, t); anima(el, ".flavio", t, { x: 300, y: 488, s: .55, aD: 150, aS: 14 });
    el.querySelector(".om").setAttribute("transform", `translate(320 ${(280 + Math.sin(t * 3.2) * 3).toFixed(1)}) rotate(${(Math.sin(t * 2) * 4).toFixed(1)}) scale(.8)`);
  },
  sale: (el, u, t, D) => { piove(el, t); onda(el, lerp(500, 330, inOutCubic(prog(u, .6, D - 1.6))), t);
    el.querySelector(".orol").setAttribute("transform", `rotate(${(u * 40).toFixed(1)} 520 110)`); },
  prima: (el, u, t) => {
    anima(el, ".mamma", t, { x: 360, y: 470, s: .6, aS: 40, aD: 14 });
    anima(el, ".flavio", t, { x: 470, y: 470, s: .48, aS: 14, aD: u > 3.9 ? 120 : 20, fase: 1 });
    const z = el.querySelector(".zai"); z.setAttribute("transform", `translate(${(lerp(640, 530, outBack(prog(u, 3.9, .8)))).toFixed(1)} 330)`);
    el.querySelector(".barra").setAttribute("opacity", (.7 + Math.sin(t * 5) * .3).toFixed(2));
  },
  sali: (el, u, t) => {
    onda(el, lerp(470, 400, inOutCubic(prog(u, .4, 3))), t); pop(el, ".no", prog(u, 1.4, .8));
    const p = inOutCubic(prog(u, 2.6, 3)); const fx = lerp(300, 300, p), fy = lerp(330, 196, p);
    anima(el, ".flavio", t, { x: lerp(260, 300, p), y: fy, s: .42, cammina: p > 0 && p < 1 ? 1 : 0, aS: p >= 1 ? 150 : 14, agitaS: p >= 1 });
    el.querySelector(".frec").setAttribute("opacity", (.5 + Math.sin(t * 4) * .5).toFixed(2));
  },
  fuori: (el, u, t) => {
    onda(el, 430, t);
    el.querySelectorAll(".corr path").forEach(pp => { const i = +pp.dataset.i, q = (t * .7 + i * .33) % 1; pp.setAttribute("transform", `translate(${(-40 + q * 360).toFixed(1)} ${(470 + i * 12).toFixed(1)})`); pp.setAttribute("opacity", Math.sin(q * Math.PI).toFixed(2)); });
    const p = inOutCubic(prog(u, .6, 4)); anima(el, ".flavio", t, { x: lerp(330, 500, p), y: lerp(330, 200, p) + 60, s: .45, cammina: p > 0 && p < 1 ? 1 : 0, aS: p >= 1 ? 150 : 14, agitaS: p >= 1 });
    const s = el.querySelector(".st"); s.style.transformBox = "fill-box"; s.style.transformOrigin = "50% 50%"; s.style.transform = `scale(${outElastic(prog(u, 4.6, 1)).toFixed(3)}) rotate(${(t * 40).toFixed(1)}deg)`;
  },
  auto: (el, u, t) => { piove(el, t);
    const p = outCubic(prog(u, .2, 1.6)); el.querySelector(".mac").setAttribute("transform", `translate(${lerp(-80, 110, p).toFixed(1)} ${(232 + (p >= 1 ? Math.sin(t * 20) * 1.5 : 0)).toFixed(1)})`);
    pop(el, ".no", prog(u, 1.8, .8)); },
  dopo: (el, u, t) => {
    const p = inOutCubic(prog(u, .3, 1.6)); anima(el, ".flavio", t, { x: lerp(90, 150, p), y: 440, s: .5, cammina: p > 0 && p < 1 ? 1 : 0, aD: p >= 1 ? 100 : 14, bocca: p >= 1 ? "o" : "sorriso" });
    el.querySelector(".tomb").setAttribute("opacity", (prog(u, 1.8, .6) * (.6 + Math.sin(t * 5) * .4)).toFixed(2)); pop(el, ".no", prog(u, 2.6, .8));
  },
  arcobaleno: (el, u, t) => { raggi(el, t);
    el.querySelectorAll(".arco path").forEach((pp, i) => { const L = 760; pp.setAttribute("stroke-dasharray", L); pp.setAttribute("stroke-dashoffset", (L * (1 - outCubic(prog(u, .2 + i * .15, 1.2)))).toFixed(1)); });
    anima(el, ".flavio", t, { x: 250, y: 492, s: .5, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 360, y: 492, s: .5, aS: 150, agitaS: true, fase: 2 }); }
};
