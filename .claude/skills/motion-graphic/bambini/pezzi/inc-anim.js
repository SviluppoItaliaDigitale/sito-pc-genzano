const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const raggi = (el, t) => el.querySelectorAll(".raggi").forEach(r => r.setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`));
function alTelefono(el, sel, x, y, s, t) { el.querySelector(sel).setAttribute("transform", `translate(${(x + 46 * s).toFixed(1)} ${(y - 222 * s + Math.sin(t * 3.2) * 3).toFixed(1)}) scale(${s.toFixed(2)}) rotate(18)`); }
function fumo(el, t) { el.querySelectorAll(".fumo circle").forEach(c => { const i = +c.dataset.i, q = (t * .35 + i * .25) % 1;
  c.setAttribute("cx", (Math.sin(q * 5 + i) * 14 + q * 40).toFixed(1)); c.setAttribute("cy", (-q * 150).toFixed(1)); c.setAttribute("r", (14 + q * 26).toFixed(1)); c.setAttribute("opacity", (Math.sin(q * Math.PI) * .9).toFixed(2)); }); }
function fiamma(el, sel, t, s = 1) { const g = el.querySelector(sel); if (!g) return; const f = g.firstElementChild; f.style.transformBox = "fill-box"; f.style.transformOrigin = "50% 100%";
  f.style.transform = `scale(${(s * (1 + Math.sin(t * 9) * .06)).toFixed(3)} ${(s * (1 + Math.sin(t * 7 + 1) * .1)).toFixed(3)})`; f.style.opacity = s > 0 ? 1 : 0; }
const ANIM = {
  bosco: (el, u, t) => { fumo(el, t); anima(el, ".flavio", t, { x: 380, y: 488, s: .56, aS: 14, aD: 14, bocca: "o" }); },
  cresce: (el, u, t) => { raggi(el, t);
    el.querySelectorAll(".vento path").forEach(p => { const i = +p.dataset.i, q = (t * .8 + i * .33) % 1; p.setAttribute("transform", `translate(${(q * 260).toFixed(1)} ${(i * 40).toFixed(1)})`); p.setAttribute("opacity", Math.sin(q * Math.PI).toFixed(2)); });
    fiamma(el, ".f1", t, outBack(prog(u, .8, .8)) * .7); fiamma(el, ".f2", t, outBack(prog(u, 1.8, .8)) * 1); fiamma(el, ".f3", t, outBack(prog(u, 2.8, .8)) * 1.3);
    const m = el.querySelector(".mesi"); m.setAttribute("transform", `translate(300 ${(150 + Math.sin(t * 2) * 4).toFixed(1)})`); svgPop(m.firstElementChild, prog(u, 4, 1)); },
  area: (el, u, t) => { fiamma(el, ".fb", t, 1);
    anima(el, ".papa", t, { x: 380, y: 470, s: .6, aS: 40, aD: 14 }); anima(el, ".flavio", t, { x: 470, y: 470, s: .46, aS: 14, aD: 14, fase: 1 });
    const n = el.querySelector(".nov"); n.setAttribute("transform", `translate(470 130) rotate(${(Math.sin(t * 2) * 6).toFixed(1)})`); svgPop(n.firstElementChild, prog(u, 5.6, .8)); },
  vedi: (el, u, t) => { fumo(el, t); fiamma(el, ".fv", t, 1);
    const p = inOutCubic(prog(u, .6, 1.6)); anima(el, ".flavio", t, { x: lerp(320, 430, p), y: 488, s: .46, cammina: p > 0 && p < 1 ? 1 : 0, aS: p >= 1 ? 60 : 14, fase: 1 });
    anima(el, ".mamma", t, { x: 520, y: 488, s: .58, aD: u > 3 ? 165 : 30, aS: 14 }); alTelefono(el, ".cell", 520, 488, .58, t); el.querySelector(".cell").style.opacity = prog(u, 3, .3);
    const f = el.querySelector(".fum"); f.setAttribute("transform", `translate(470 150)`); svgPop(f.firstElementChild, prog(u, 3.6, .8)); },
  solo: (el, u, t) => {
    anima(el, ".flavio", t, { x: 300, y: 488, s: .6, aD: u > .8 ? 165 : 20, aS: 14 }); alTelefono(el, ".cell", 300, 488, .6, t); el.querySelector(".cell").style.opacity = prog(u, .8, .3);
    const f = el.querySelector(".fum"); f.setAttribute("transform", `translate(430 180)`); svgPop(f.firstElementChild, prog(u, 1.4, .8));
    const d = el.querySelector(".dove"); d.setAttribute("transform", `translate(150 150)`); svgPop(d.firstElementChild, prog(u, 3.6, .8)); },
  fuga: (el, u, t) => { fiamma(el, ".ff", t, 1); fiamma(el, ".ff2", t, 1); pop(el, ".nos", prog(u, 4.8, .8));
    el.querySelector(".si").setAttribute("opacity", (prog(u, .8, .4) * (.6 + Math.sin(t * 4) * .4)).toFixed(2));
    const p = inOutCubic(prog(u, 1, 3.4)); anima(el, ".flavio", t, { x: lerp(270, 90, p), y: 440, s: .42, cammina: p > 0 && p < 1 ? 1 : 0, flip: true }); },
  spettacolo: (el, u, t) => { pop(el, ".noz", prog(u, 4.6, .8));
    const p = inOutCubic(prog(u, .6, 3)); anima(el, ".flavio", t, { x: lerp(320, 110, p), y: 488, s: .52, cammina: p > 0 && p < 1 ? 1 : 0, flip: true }); },
  verde: (el, u, t) => { raggi(el, t);
    anima(el, ".flavio", t, { x: 250, y: 492, s: .5, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 360, y: 492, s: .5, aS: 150, agitaS: true, fase: 2 }); }
};
