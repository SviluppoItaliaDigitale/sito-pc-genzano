const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const raggi = (el, t) => el.querySelectorAll(".raggi").forEach(r => r.setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`));
function piove(el, t, v = 1) {
  const g = el.querySelector(".pioggia"); if (!g) return; const y0 = +g.dataset.y0, y1 = +g.dataset.y1;
  g.querySelectorAll("path").forEach(p => { const i = +p.dataset.i, q = (t * (1.3 + hash(i) * .6) * v + hash(i + 5)) % 1;
    p.setAttribute("transform", `translate(${(+p.dataset.x - q * 40).toFixed(1)} ${(y0 + q * (y1 - y0)).toFixed(1)})`); });
}
function alTelefono(el, sel, x, y, s, t) { el.querySelector(sel).setAttribute("transform", `translate(${(x + 46 * s).toFixed(1)} ${(y - 222 * s + Math.sin(t * 3.2) * 3).toFixed(1)}) scale(${s.toFixed(2)}) rotate(18)`); }
const ANIM = {
  semaforo: (el, u, t) => {
    el.querySelectorAll(".lamp").forEach(l => { const i = +l.dataset.i, q = (t * .8) % 4; const on = Math.floor(q) === i;
      const g = l.firstElementChild; g.style.transformBox = "fill-box"; g.style.transformOrigin = "50% 50%"; g.style.transform = `scale(${on ? 1.12 : .95})`; g.style.opacity = 1; });
    anima(el, ".flavio", t, { x: 400, y: 488, s: .58, aS: 120, aD: 14, flip: false });
  },
  zone: (el, u, t) => {
    const pz = el.querySelector(".pz"); pz.setAttribute("opacity", (prog(u, 1, .6) * (.75 + Math.sin(t * 4) * .25)).toFixed(2));
    el.querySelector(".pin").setAttribute("transform", `translate(385 ${(lerp(150, 300, outBack(prog(u, 4.5, .8))) + Math.sin(t * 3) * 3).toFixed(1)})`);
    el.querySelector(".pin").style.opacity = prog(u, 4.5, .2); el.querySelector(".fz").style.opacity = prog(u, 5, .4);
    const f = el.querySelector(".fog"); f.setAttribute("transform", `translate(110 ${(110 + Math.sin(t * 2) * 4).toFixed(1)}) rotate(-8)`); svgPop(f.firstElementChild, prog(u, .6, 1));
  },
  verde: (el, u, t) => { raggi(el, t); anima(el, ".flavio", t, { x: 280, y: 488, s: .62, aD: u > 2.4 ? 165 : 20, aS: 14 }); alTelefono(el, ".cell", 280, 488, .62, t); el.querySelector(".cell").style.opacity = prog(u, 2.4, .3); },
  gialla: (el, u, t) => { piove(el, t, .7); pop(el, ".no", prog(u, 4.6, .8));
    const p = inOutCubic(prog(u, 4.6, 2)); anima(el, ".flavio", t, { x: lerp(320, 170, p), y: 488, s: .55, cammina: p > 0 && p < 1 ? 1 : 0, flip: p > 0 && p < 1 }); },
  arancione: (el, u, t) => { piove(el, t, 1.2);
    anima(el, ".flavio", t, { x: 470, y: 488, s: .55, aS: u > 4.5 ? 110 : 14 });
    el.querySelector(".zai").setAttribute("transform", `translate(${lerp(640, 545, outBack(prog(u, 4.5, .8))).toFixed(1)} 410)`); },
  rossa: (el, u, t) => { piove(el, t, 1.6);
    const f = el.querySelector(".fl").firstElementChild, q = (t * .9) % 2.5; svgPop(f, q < .5 ? prog(q, 0, .3) : 1 - prog(q, .5, .3));
    el.querySelector(".vis").setAttribute("transform", `translate(0 ${(Math.sin(t * 2) * 2).toFixed(1)})`); },
  sito: (el, u, t) => {
    anima(el, ".mamma", t, { x: 120, y: 470, s: .6, aD: 60, aS: 14 });
    anima(el, ".flavio", t, { x: 470, y: 470, s: .46, aS: 70, fase: 1 });
    anima(el, ".silvia", t, { x: 540, y: 470, s: .42, aS: 14, aD: 14, fase: 2, bocca: "o" });
    el.querySelector(".barra").setAttribute("opacity", (.75 + Math.sin(t * 4) * .25).toFixed(2));
  },
  fine: (el, u, t) => { raggi(el, t);
    el.querySelectorAll(".pal").forEach(p => { const i = +p.dataset.i; svgPop(p.firstElementChild, prog(u, .3 + i * .3, .8));
      p.setAttribute("transform", `translate(${120 + i * 70} ${(160 + Math.sin(t * 3 + i) * 8).toFixed(1)})`); });
    anima(el, ".flavio", t, { x: 260, y: 492, s: .5, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 370, y: 492, s: .5, aS: 150, agitaS: true, fase: 2 }); }
};
