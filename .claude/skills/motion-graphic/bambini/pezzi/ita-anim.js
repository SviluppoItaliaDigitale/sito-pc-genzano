const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
/* telefono che vibra a raffiche: posizione, scala e piccoli scatti di rotazione */
function telefono(el, u, x, y, s, forza = 1) {
  const raffica = (u % 2.4) < 1 ? 1 : 0, r = Math.sin(u * 40) * 3.2 * raffica * forza;
  el.querySelector(".tel").setAttribute("transform", `translate(${(x + Math.sin(u * 47) * 2 * raffica * forza).toFixed(1)} ${y}) rotate(${r.toFixed(2)}) scale(${s})`);
  const v = el.querySelector(".vib");
  if (v) { v.setAttribute("transform", `translate(${x} ${y}) scale(${s})`);
    v.querySelectorAll("path").forEach(p => { const i = +p.dataset.i, q = ((u % 2.4) - i * .16) / .9;
      p.setAttribute("opacity", (forza * (q > 0 && q < 1 ? Math.sin(q * Math.PI) : 0)).toFixed(2)); }); }
  return raffica;
}
const righeLette = (el, p) => el.querySelectorAll(".avv .riga").forEach(r => { const i = +r.dataset.i, q = clamp(p * 5 - i);
  r.setAttribute("opacity", (.4 + .6 * q).toFixed(2)); r.setAttribute("fill", q > 0 ? "#e8590c" : INK); });
function minitel(el, sel, p, t, i = 0) {
  const g = el.querySelector(sel); g.querySelector(".lcd").setAttribute("fill", p > 0 ? "#ffd43b" : "#a5d8ff");
  const s = g.querySelector(".seg > g"); svgPop(s, p, "50%", "100%"); if (p >= 1) s.style.transform = `scale(${(1 + Math.sin(t * 6 + i) * .08).toFixed(3)})`;
}
const ANIM = {
  avviso: (el, u, t) => {
    const r = telefono(el, u, 235, 244, 1.08);
    el.querySelector(".avv .evid").setAttribute("opacity", (.75 + .25 * Math.sin(t * 5)).toFixed(2));
    anima(el, ".flavio", t, { x: 492, y: 490, s: .56, aS: 100, aD: 14, bocca: r ? "o" : "sorriso" });
  },
  zona: (el, u, t, D) => {
    el.querySelectorAll(".anelli circle").forEach(c => { const q = (u * .42 + (+c.dataset.i) / 4) % 1;
      c.setAttribute("r", (20 + q * 500).toFixed(1)); c.setAttribute("opacity", ((1 - q) * .85).toFixed(2)); });
    const arr = [.9, 1.35, 1.8];
    anima(el, ".flavio", t, { x: 250, y: 462, s: .4, aD: 60, aS: 14, bocca: u > arr[0] && u < arr[0] + 1.2 ? "o" : "sorriso" });
    anima(el, ".silvia", t, { x: 356, y: 462, s: .4, aD: 60, aS: 14, fase: 2, bocca: u > arr[1] && u < arr[1] + 1.2 ? "o" : "sorriso" });
    anima(el, ".papa", t, { x: 466, y: 462, s: .4, aD: 60, aS: 14, fase: 3.4, bocca: u > arr[2] && u < arr[2] + 1.2 ? "o" : "sorriso" });
    arr.forEach((a, i) => minitel(el, ".t" + i, prog(u, a, .7), t, i));
    const a0 = quando(1, "Non serve scaricare"), a1 = quando(1, "e non serve iscriversi");
    [a0, a1].forEach((a, i) => { pop(el, ".b" + i, prog(u, a - .5, .7)); pop(el, ".n" + i, prog(u, a + .15, .7)); pop(el, ".e" + i, prog(u, a + .35, .6)); });
  },
  suono: (el, u, t, D) => {
    const a = quando(2, "e sullo schermo"), b = quando(2, "IT-alert");
    telefono(el, u, 215, 246, 1.05, 1 - .6 * prog(u, a, .6));
    el.querySelector(".alt").setAttribute("opacity", (1 - prog(u, a - .1, .3)).toFixed(2));
    el.querySelector(".alt").setAttribute("transform", `translate(0 ${-4}) scale(${(1 + Math.sin(u * 8) * .06).toFixed(3)})`);
    pop(el, ".avv", prog(u, a, .8));
    const e = el.querySelector(".avv .evid"), pb = prog(u, b - .2, .5);
    e.setAttribute("fill", pb > 0 ? "#ffd43b" : "#fff3bf"); e.setAttribute("opacity", pb > 0 ? (.8 + .2 * Math.sin(t * 7)).toFixed(2) : 1);
    anima(el, ".flavio", t, { x: 478, y: 490, s: .58, aS: u < a ? 150 : 100, aD: 14, bocca: u < a ? "o" : "sorriso" });
  },
  casi: (el, u, t) => {
    const at = CONFIG.scene[3].listaAt;
    at.forEach((a, j) => { pop(el, ".c" + j, prog(u, a, .8));
      if (u > a + .8) el.querySelector(`.c${j} > g`).style.transform = `scale(${(1 + Math.sin(t * 2.6 + j * 1.3) * .03).toFixed(3)})`; });
    anima(el, ".flavio", t, { x: 84, y: 386, s: .5, aD: 120, aS: 14, bocca: u > at[3] + 1 ? "sorriso" : "o" });
    const m = el.querySelector(".t0"); m.setAttribute("transform", `translate(134 ${(282 + Math.sin(t * 3.2) * 3).toFixed(1)}) rotate(14)`);
    minitel(el, ".t0", prog(u, .5, .7), t);
  },
  nonsi: (el, u, t) => {
    pop(el, ".k0", prog(u, .3, .8)); pop(el, ".k1", prog(u, .5, .8));
    const a0 = quando(4, "i terremoti"), a1 = quando(4, "le allerte meteo"), a2 = quando(4, "Per il maltempo"), a3 = quando(4, "il colore");
    el.querySelector(".casa").setAttribute("transform", `translate(${(Math.sin(u * 30) * 3 * (1 - prog(u, a0, .5))).toFixed(1)} -12)`);
    el.querySelectorAll(".gocce path").forEach(g => { const i = +g.dataset.i, q = (t * 1.1 + hash(i + 4)) % 1;
      g.setAttribute("transform", `translate(${-44 + i * 20 - q * 8} ${(6 + q * 44).toFixed(1)})`); g.setAttribute("opacity", Math.sin(q * Math.PI).toFixed(2)); });
    pop(el, ".n0", prog(u, a0, .7)); pop(el, ".n1", prog(u, a1, .7));
    pop(el, ".sito", prog(u, 1, .9));
    el.querySelectorAll(".sito .col").forEach(c => { const i = +c.dataset.i, p = prog(u, a3 + i * .28, .6), g = c.firstElementChild;
      g.firstElementChild.setAttribute("fill", p > 0 ? g.firstElementChild.dataset.c : "#dee2e6");
      g.style.transformBox = "fill-box"; g.style.transformOrigin = "50% 50%"; g.style.transform = `scale(${lerp(1, 1.25, Math.sin(clamp(p) * Math.PI)).toFixed(3)})`; if (p >= 1) g.style.transform = `scale(${(1 + Math.sin(t * 3 + i * 1.6) * .05).toFixed(3)})`; });
    anima(el, ".flavio", t, { x: 84, y: 488, s: .5, aD: u > a2 ? 100 : 14, aS: 14, bocca: u > a2 ? "sorriso" : "o" });
  },
  passi: (el, u, t, D) => {
    const a1 = quando(5, "fermati"), a2 = quando(5, "leggi tutto"), a3 = quando(5, "Poi segui");
    const p = prog(u, .2, Math.max(.3, a1 - .2)), mov = p > 0 && p < 1 ? 1 : 0;
    anima(el, ".flavio", t, { x: lerp(-30, 98, p), y: 480, s: .55, cammina: mov, aD: u > a2 ? 70 : 14, aS: 14, bocca: u > a1 && u < a3 ? "o" : "sorriso" });
    pop(el, ".alt", prog(u, a1, .7)); pop(el, ".n1", prog(u, a1 + .2, .6));
    const pt = outBack(prog(u, .5, .9));
    el.querySelector(".tel").setAttribute("transform", `translate(300 ${lerp(640, 268, pt).toFixed(1)}) rotate(${(Math.sin(t * 1.6) * 1.5).toFixed(2)}) scale(.86)`);
    righeLette(el, prog(u, a2, Math.max(.6, a3 - a2 - .2))); pop(el, ".n2", prog(u, a2, .6));
    const pv = outCubic(prog(u, a3 - .3, .9));
    anima(el, ".vol", t, { x: lerp(690, 500, pv), y: 480, s: .52, cammina: pv > 0 && pv < 1 ? 1 : 0, aS: 14, aD: pv >= 1 ? 110 : 14, fase: 1.2 });
    pop(el, ".fre", prog(u, a3 + .5, .7)); pop(el, ".n3", prog(u, a3 + .7, .6));
  },
  prova: (el, u, t) => {
    const a1 = quando(6, "è solo una prova"), a2 = quando(6, "non devi fare niente");
    el.querySelector(".tel").setAttribute("transform", `translate(150 ${(256 + Math.sin(t * 2) * 4).toFixed(1)}) rotate(${(Math.sin(t * 1.4) * 2).toFixed(2)}) scale(.7)`);
    el.querySelector(".avv .evid").setAttribute("opacity", (.75 + .25 * Math.sin(t * 5)).toFixed(2));
    pop(el, ".ok", prog(u, a1, .8)); pop(el, ".niente", prog(u, a2, .8));
    const fest = u > a2;
    anima(el, ".flavio", t, { x: 362, y: 398, s: .5, aD: fest ? 150 : 14, agitaD: fest, aS: 14 });
    anima(el, ".silvia", t, { x: 478, y: 398, s: .5, aS: fest ? 150 : 14, agitaS: fest, aD: 14, fase: 2 });
  }
};
