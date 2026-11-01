const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
function zz(el, t, x, y) {
  el.querySelectorAll(".zz text").forEach((z, i) => { const q = (t * .5 + i * .33) % 1;
    z.setAttribute("x", (x + i * 26 + Math.sin(q * 6) * 8).toFixed(1)); z.setAttribute("y", (y - q * 90).toFixed(1)); z.setAttribute("opacity", (Math.sin(q * Math.PI)).toFixed(2)); });
}
function alTelefono(el, sel, x, y, s, t) {
  el.querySelector(sel).setAttribute("transform", `translate(${(x + 46 * s).toFixed(1)} ${(y - 222 * s + Math.sin(t * 3.2) * 3).toFixed(1)}) scale(${s.toFixed(2)}) rotate(18)`);
}
const ANIM = {
  vulcano: (el, u, t) => { zz(el, t, 290, 130); anima(el, ".flavio", t, { x: 520, y: 492, s: .5, aS: 120, aD: 14 }); },
  dorme: (el, u, t) => { zz(el, t, 290, 130); const g = el.querySelector(".tempo"); g.setAttribute("transform", `translate(300 ${(420 + Math.sin(t * 2) * 5).toFixed(1)})`); svgPop(g.firstElementChild, prog(u, 1.4, 1)); },
  sorveglia: (el, u, t) => {
    el.querySelector(".sat").setAttribute("transform", `translate(${(300 + Math.sin(t * .8) * 30).toFixed(1)} ${(64 + Math.sin(t * 1.6) * 6).toFixed(1)}) rotate(${(Math.sin(t) * 6).toFixed(1)})`);
    el.querySelector(".seg").setAttribute("stroke-dashoffset", (-t * 50).toFixed(1));
    el.querySelector(".ago").setAttribute("transform", `rotate(${(Math.sin(t * 2.3) * 40).toFixed(1)} 455 245)`);
    anima(el, ".ricerc", t, { x: 330, y: 470, s: .55, aD: 100, aS: 14 });
  },
  gas: (el, u, t) => {
    const liv = prog(u, .6, 3.4); el.querySelector(".co2").setAttribute("opacity", (.15 + .5 * liv).toFixed(2));
    el.querySelectorAll(".bolle circle").forEach(c => { const i = +c.dataset.i, q = (t * .35 + hash(i) ) % 1;
      c.setAttribute("cx", (150 + hash(i + 3) * 300 + Math.sin(q * 8 + i) * 10).toFixed(1)); c.setAttribute("cy", (500 - q * 70).toFixed(1)); c.setAttribute("opacity", (liv * Math.sin(q * Math.PI)).toFixed(2)); });
    anima(el, ".flavio", t, { x: 520, y: 205, s: .4, aS: 14, aD: 100, bocca: "o" });
  },
  aria: (el, u, t) => {
    const ap = outBack(prog(u, .8, .8)); const p = el.querySelector(".porta"); p.setAttribute("transform", `translate(${(120 * (1 - Math.cos(ap * .9))).toFixed(1)} 0) scale(${(1 - .7 * ap).toFixed(3)} 1)`); p.setAttribute("transform-origin", "120 0");
    el.querySelectorAll(".vento path").forEach(v => { const i = +v.dataset.i, q = (t * .7 + i * .33) % 1;
      v.setAttribute("transform", `translate(${(150 + q * 160).toFixed(1)} ${(330 + i * 34).toFixed(1)})`); v.setAttribute("opacity", (prog(u, 1.2, .5) * Math.sin(q * Math.PI)).toFixed(2)); });
    pop(el, ".np", prog(u, 3.6, .8));
    anima(el, ".flavio", t, { x: 340, y: 470, s: .5, aS: 14, aD: 60 });
  },
  soccorso: (el, u, t, D) => {
    pop(el, ".np", prog(u, .8, .8));
    const p = inOutCubic(prog(u, 1.4, 1.6)), mov = p > 0 && p < 1 ? 1 : 0, x = lerp(250, 360, p);
    anima(el, ".flavio", t, { x, y: 470, s: .55, cammina: mov, aD: p >= 1 ? 165 : 20, aS: 14 });
    alTelefono(el, ".cell", x, 470, .55, t); el.querySelector(".cell").style.opacity = prog(u, 3, .3);
    const f = el.querySelector(".fum"); f.setAttribute("transform", `translate(${(x + 70).toFixed(1)} 180)`); svgPop(f.firstElementChild, prog(u, 3.2, .8));
    const v = el.querySelector(".vvf"); v.setAttribute("transform", `translate(${lerp(140, 0, outCubic(prog(u, 4.4, 1.2))).toFixed(1)} 0)`); v.style.opacity = prog(u, 4.4, .3);
  },
  sereno: (el, u, t) => {
    const s = el.querySelector(".sole"); s.setAttribute("transform", `translate(500 ${lerp(200, 90, outBack(prog(u, .1, 1.2))).toFixed(1)})`);
    el.querySelector(".raggi").setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`);
    anima(el, ".flavio", t, { x: 250, y: 492, s: .5, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 360, y: 492, s: .5, aS: 150, agitaS: true, fase: 2 });
  }
};
