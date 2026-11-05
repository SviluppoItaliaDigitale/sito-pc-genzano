const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
/* telefono all'orecchio: segue la testa del personaggio */
function alTelefono(el, sel, x, y, s, t, lato = 1) {
  const c = el.querySelector(sel); c.setAttribute("transform", `translate(${(x + lato * 46 * s).toFixed(1)} ${(y - 222 * s + Math.sin(t * 3.2) * 3).toFixed(1)}) scale(${s.toFixed(2)}) rotate(${lato * 18})`);
}
const ANIM = {
  numero: (el, u, t) => {
    const tel = el.querySelector(".tel"); tel.setAttribute("transform", `translate(250 ${(250 + Math.sin(t * 2.2) * 6).toFixed(1)}) rotate(${(Math.sin(t * 9) * (Math.sin(t * 1.6) > .6 ? 4 : 0)).toFixed(1)}) scale(1)`);
    el.querySelector(".o1").setAttribute("opacity", (.4 + .6 * Math.abs(Math.sin(t * 4))).toFixed(2));
    anima(el, ".flavio", t, { x: 470, y: 492, s: .55, aS: 95, aD: 14 });
  },
  dire: (el, u, t) => {
    const at = CONFIG.scene[2].listaAt;
    const f = el.querySelector(".fum"); f.setAttribute("transform", `translate(330 ${(150 + Math.sin(t * 2.4) * 5).toFixed(1)})`); svgPop(f.firstElementChild, prog(u, .4, .8));
    at.forEach((a, j) => pop(el, ".d" + j, prog(u, a, .7)));
    anima(el, ".flavio", t, { x: 150, y: 492, s: .58, aD: 165, aS: 14, bocca: Math.sin(t * 9) > 0 ? "o" : "sorriso" });
    alTelefono(el, ".cell", 150, 492, .58, t);
  },
  calma: (el, u, t, D) => {
    anima(el, ".flavio", t, { x: 130, y: 470, s: .55, aD: 165, aS: 14 }); alTelefono(el, ".cell", 130, 470, .55, t);
    anima(el, ".op", t, { x: 470, y: 470, s: .6, aS: 40, aD: 30, fase: 1.5 });
    el.querySelector(".cuffia").setAttribute("transform", `translate(470 ${(470 - 268 * .6 + Math.sin(t * 3.2 + 1.5) * 3).toFixed(1)}) scale(.6)`);
    el.querySelector(".filo").setAttribute("stroke-dashoffset", (-t * 60).toFixed(1));
    const ok = el.querySelector(".ok"); ok.setAttribute("transform", `translate(470 120)`); svgPop(ok.firstElementChild, prog(u, D - 2.4, .8));
  },
  insieme: (el, u, t, D) => {
    const p = inOutCubic(prog(u, .5, 1.8)), mov = p > 0 && p < 1 ? 1 : 0;
    anima(el, ".mamma", t, { x: 380, y: 470, s: .64, aD: u > 2.6 ? 165 : 30, aS: 14 });
    alTelefono(el, ".cell", 380, 470, .64, t); el.querySelector(".cell").style.opacity = prog(u, 2.6, .3);
    anima(el, ".flavio", t, { x: lerp(110, 260, p), y: 470, s: .5, cammina: mov, aD: p >= 1 ? 120 : 20, fase: 1 });
    ["s1", "s2"].forEach((c, i) => svgPop(el.querySelector("." + c), prog(u, D - 2.6 + i * .2, .7)));
  },
  scherzo: (el, u, t) => {
    pop(el, ".no", prog(u, 1, .8));
    el.querySelectorAll(".fila .pg").forEach((g, i) => anima(el, g, t, { x: 380 + i * 70, y: 492, s: .4, fase: i * 1.7, aS: 14, aD: i === 0 ? 120 : 14, bocca: "o" }));
    const o = el.querySelector(".orologio > g"); o.setAttribute("transform", `translate(-50 -50) rotate(${(Math.sin(t * 6) * 8).toFixed(1)} 50 50)`);
  },
  sereno: (el, u, t) => {
    const s = el.querySelector(".sole"); s.setAttribute("transform", `translate(470 ${lerp(220, 110, outBack(prog(u, .1, 1.2))).toFixed(1)})`);
    el.querySelector(".raggi").setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`);
    const c = el.querySelector(".cartello"); c.setAttribute("transform", `translate(220 ${(220 + Math.sin(t * 2) * 4).toFixed(1)})`); svgPop(c.firstElementChild, prog(u, .6, 1), "50%", "100%");
    anima(el, ".flavio", t, { x: 370, y: 492, s: .5, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 470, y: 492, s: .5, aS: 150, agitaS: true, fase: 2 });
  }
};
