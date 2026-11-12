/* I tempi seguono la voce: `quando(k, parola)` dà il secondo della scena k in cui la voce arriva a quella parola,
   in proporzione ai caratteri della frase (con durate.json usa la durata vera, altrimenti quella stimata). */
const voceDi = k => (DUR.length && DUR[k] != null) ? DUR[k] : CONFIG.scene[k].dur - 1.2;
const quando = (k, parola) => { const s = CONFIG.scene[k].sottotitolo, i = s.indexOf(parola); return .45 + voceDi(k) * (i < 0 ? 0 : i / s.length); };
CONFIG.scene[2].listaAt = ["crepe", "alberi", "piccoli", "Se li noti"].map(p => +quando(2, p).toFixed(2));
const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const metti = (g, x, y, r = 0) => g.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${r.toFixed(1)})`);
function piove(el, t, v = 1) {
  const g = el.querySelector(".pioggia"); if (!g) return; const y0 = +g.dataset.y0, y1 = +g.dataset.y1;
  g.querySelectorAll("path").forEach(p => { const i = +p.dataset.i, q = (t * (1.3 + hash(i) * .6) * v + hash(i + 5)) % 1;
    p.setAttribute("transform", `translate(${(+p.dataset.x - q * 40).toFixed(1)} ${(y0 + q * (y1 - y0)).toFixed(1)})`); });
}
const disegna = (el, sel, p) => { const c = el.querySelector(sel); c.setAttribute("stroke-dasharray", "1 1"); c.setAttribute("stroke-dashoffset", (1 - clamp(p)).toFixed(3)); c.setAttribute("opacity", p > 0 ? 1 : 0); };
const ANIM = {
  titolo: (el, u, t, D) => {
    const P = D / 2, ph = ((u + P * .42) % P) / P, q = inOutCubic(prog(ph, .1, .55)), vis = Math.min(prog(ph, 0, .06), 1 - prog(ph, .92, .08));
    const s = lerp(.76, .3, q), [x, y, a] = sulPendio(P_TIT, s, 2), lm = el.querySelector(".lembo");
    metti(lm, x, y, a + Math.sin(t * 30) * (q > 0 && q < 1 ? 1.2 : 0)); lm.setAttribute("opacity", vis.toFixed(2));
    el.querySelectorAll(".sassi > g").forEach(g => { const i = +g.dataset.i, qq = outCubic(prog(ph, .14 + i * .05, .6));
      const ss = lerp(.62 - i * .04, .16 - i * .035, qq), salto = Math.abs(Math.sin(qq * Math.PI * (3 + i))) * 16 * (1 - qq);
      const [sx, sy] = sulPendio(P_TIT, ss, 12 + salto); metti(g, sx, sy, -qq * 500); g.setAttribute("opacity", vis.toFixed(2)); });
    anima(el, ".flavio", t, { x: 66, y: 486, s: .5, aD: 128, aS: 14, bocca: q > .05 && q < 1 ? "o" : "sorriso" });
  },
  pioggia: (el, u, t, D) => {
    piove(el, t);
    const z = prog(u, D * .12, D * .55);
    el.querySelector(".zuppo").setAttribute("opacity", (.62 * z).toFixed(2));
    const r = el.querySelector(".rivoli"); r.setAttribute("stroke-dashoffset", (-t * 70).toFixed(1)); r.setAttribute("opacity", prog(u, D * .25, D * .3).toFixed(2));
    el.querySelectorAll(".onde path").forEach(o => { const i = +o.dataset.i, q = (t * .4 + i * .33) % 1;
      o.setAttribute("transform", `translate(${(330 + i * 60 + q * 40).toFixed(1)} ${(430 + i * 14).toFixed(1)})`); o.setAttribute("opacity", Math.sin(q * Math.PI).toFixed(2)); });
    pop(el, ".tgG", prog(u, quando(1, "Anche a Genzano"), .8)); pop(el, ".tgL", prog(u, quando(1, "lago di Nemi") - .3, .8));
  },
  segnali: (el, u, t, D) => {
    const at = CONFIG.scene[2].listaAt;
    disegna(el, ".crM", prog(u, at[0], .9)); disegna(el, ".crT", prog(u, at[0] + .5, .9));
    const p1 = outBack(prog(u, at[1], 1.1)), p1b = outBack(prog(u, at[1] + .45, 1.1));
    el.querySelector(".alb").setAttribute("transform", `rotate(${(15 * p1 + Math.sin(t * 2.4) * 1.2).toFixed(1)})`);
    el.querySelector(".palo").setAttribute("transform", `rotate(${(11 * p1b).toFixed(1)})`);
    const p2 = prog(u, at[2], 1.3), e2 = outCubic(p2), [x, y, a] = sulPendio(P_SEG, lerp(.52, .4, e2), 4);
    metti(el.querySelector(".smot"), x, y, a); el.querySelector(".nicchia").setAttribute("opacity", clamp(p2 * 3).toFixed(2));
    el.querySelectorAll(".sassi > g").forEach(g => { const i = +g.dataset.i, qq = outCubic(prog(u, at[2] + .15 + i * .15, 1.2));
      const [sx, sy] = sulPendio(P_SEG, lerp(.4, .2 - i * .06, qq), 8 + Math.abs(Math.sin(qq * Math.PI * 3)) * 10 * (1 - qq)); metti(g, sx, sy, -qq * 400); g.setAttribute("opacity", qq > 0 ? 1 : 0); });
    const p3 = prog(u, at[3], .8); pop(el, ".fum", p3);
    anima(el, ".flavio", t, { x: 556, y: 384, s: .36, aD: 14, aS: p3 > 0 ? 150 : u > at[0] ? 70 : 14, bocca: u > at[0] && p3 <= 0 ? "o" : "sorriso" });
  },
  casa: (el, u, t, D) => {
    const m = inOutCubic(prog(u, D * .1, D * .55)), d = 50 * m, trem = m > 0 && m < 1 ? Math.sin(t * 34) * 1.2 : 0;
    el.querySelector(".massa").setAttribute("transform", `translate(${(-.56 * d + trem).toFixed(1)} ${(.78 * d).toFixed(1)})`);
    el.querySelector(".muro").setAttribute("transform", `rotate(${(-15 * inOutCubic(prog(u, D * .34, D * .3))).toFixed(1)})`);
    el.querySelectorAll(".sassi > g").forEach(g => { const i = +g.dataset.i, qq = outCubic(prog(u, D * (.08 + i * .1), D * .3));
      const [sx, sy] = sulPendio(P_CASA, lerp(.6, .07 + i * .035, qq), 10 + Math.abs(Math.sin(qq * Math.PI * 3)) * 14 * (1 - qq)); metti(g, sx, sy, -qq * 500); g.setAttribute("opacity", qq > 0 ? 1 : 0); });
    const tv = quando(3, "Se la terra"), p = inOutCubic(prog(u, tv, Math.max(1.6, D * .3))), mov = p > 0 && p < 1 ? 1 : 0;
    anima(el, ".mamma", t, { x: lerp(278, 118, p), y: 488, s: .5, cammina: mov, aS: p >= 1 ? 30 : 14, aD: 30 });
    anima(el, ".flavio", t, { x: lerp(204, 44, p), y: 490, s: .45, cammina: mov, fase: 1.3, aS: 14, aD: p <= 0 && m > .1 ? 120 : 14, bocca: p <= 0 && m > .1 ? "o" : "sorriso" });
    el.querySelector(".via").setAttribute("opacity", (prog(u, tv - .2, .4) * (.75 + Math.sin(t * 5) * .25)).toFixed(2));
  },
  lato: (el, u, t, D) => {
    const Lf = lerp(.16, 1, inOutCubic(prog(u, D * .06, D * .62))), yb = 176 + 236 * Lf, wb = 22 + 66 * Lf;
    el.querySelector(".lingua").setAttribute("d", `M276 178 Q300 158 324 178 L${(300 + wb).toFixed(1)} ${yb.toFixed(1)} Q${(300 + wb * .6).toFixed(1)} ${(yb + 34).toFixed(1)} 300 ${(yb + 26).toFixed(1)} Q${(300 - wb * .6).toFixed(1)} ${(yb + 34).toFixed(1)} ${(300 - wb).toFixed(1)} ${yb.toFixed(1)}Z`);
    el.querySelectorAll(".sassi > g").forEach(g => { const i = +g.dataset.i; metti(g, 300 + (i - 2) * wb * .42, yb + 20 - Math.abs(i - 2) * 9 + Math.abs(Math.sin(t * 7 + i * 1.7)) * -8 * (Lf < 1 ? 1 : 0), t * 160 * (Lf < 1 ? 1 : 0) + i * 40); });
    const ff = el.querySelector(".fFrana"); ff.setAttribute("opacity", (prog(u, D * .05, .4) * (1 - prog(u, D * .56, D * .08)) * (.75 + Math.sin(t * 5) * .25)).toFixed(2));
    ff.setAttribute("transform", `translate(0 ${(Math.min(yb - 300, 40) + Math.sin(t * 5) * 5).toFixed(1)})`);
    const tv = quando(4, "spostati di lato"), p = inOutCubic(prog(u, tv, Math.max(1.8, D * .24))), mov = p > 0 && p < 1 ? 1 : 0;
    anima(el, ".flavio", t, { x: lerp(300, 512, p), y: lerp(488, 334, p * p), s: .45, cammina: mov, bocca: p < 1 ? "o" : "sorriso", aS: p >= 1 ? 150 : 14, aD: p >= 1 ? 150 : 14, agitaS: p >= 1, agitaD: p >= 1 });
    el.querySelector(".fVia").setAttribute("opacity", (prog(u, tv - .2, .4) * (1 - prog(u, quando(4, "Non fermarti") - .4, .5)) * (.75 + Math.sin(t * 5) * .25)).toFixed(2));
    pop(el, ".ok", prog(u, quando(4, "punto più alto"), .8));
    pop(el, ".np", prog(u, quando(4, "Non fermarti"), .8));
    el.querySelector(".al1").setAttribute("transform", `rotate(${(Math.sin(t * 2.2) * 2).toFixed(1)})`);
  },
  rannicchia: (el, u, t, D) => {
    const tB = quando(5, "Non avvicinarti"), b = prog(u, tB - .2, .5);
    el.querySelector(".gB").style.opacity = b;
    const giu = prog(u, quando(5, "rannicchiati") - .5, .7), e = outElastic(giu), g = el.querySelector(".giu");
    g.setAttribute("transform", `translate(300 ${(446 + Math.sin(t * 3.2) * .8).toFixed(1)}) scale(${(1.15 * lerp(.75, 1, e)).toFixed(3)} ${(1.15 * lerp(1.25, 1, e)).toFixed(3)})`);
    const bl = (t % 3.4) < .13 ? .12 : 1; g.querySelector(".occhi").setAttribute("transform", `translate(0 6) scale(1 ${bl}) translate(0 -6)`);
    const sc = el.querySelector(".scudo"); sc.setAttribute("opacity", prog(u, quando(5, "proteggi"), .4).toFixed(2)); sc.setAttribute("stroke-dashoffset", (-t * 30).toFixed(1));
    el.querySelectorAll(".gA .sassi > g").forEach(s => { const i = +s.dataset.i, q = ((u / D) * 1.5 + i * .3) % 1;
      metti(s, 620 - q * 660, 452 + i * 12 - Math.abs(Math.sin(q * Math.PI * 5)) * 10, -q * 900); });
    ["brav1", "brav2", "brav3"].forEach((c, i) => { const s = el.querySelector("." + c); svgPop(s, prog(u, quando(5, "proteggi") + .6 + i * .2, .7)); s.style.transform += ` rotate(${(Math.sin(t * 4 + i) * 12).toFixed(1)}deg)`; });
    pop(el, ".np", prog(u, tB + .3, .8));
    disegna(el, ".crepaB", prog(u, quando(5, "bordo"), .7));
    const c = prog(u, quando(5, "può cedere"), 1.1), cc = c * c;
    el.querySelector(".zolla").setAttribute("transform", `translate(${(-26 * c).toFixed(1)} ${(150 * cc).toFixed(1)}) rotate(${(-50 * c).toFixed(1)} 340 290)`);
    anima(el, ".silvia", t, { x: 520, y: 284, s: .45, aS: 14, aD: 14, bocca: c > 0 && c < 1 ? "o" : "sorriso" });
  },
  strada: (el, u, t, D) => {
    el.querySelector(".raggi").setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`);
    const pa = outCubic(prog(u, .1, Math.max(1.4, D * .2)));
    el.querySelector(".autoA").setAttribute("transform", `translate(${lerp(120, 318, pa).toFixed(1)} 308) scale(.8)`);
    el.querySelectorAll(".luce").forEach(l => l.setAttribute("opacity", pa >= 1 && (t % .9) < .45 ? 1 : 0));
    const tv = quando(6, "avvisa"), pb = outCubic(prog(u, tv - .2, Math.max(1.8, D * .28)));
    el.querySelector(".autoB").setAttribute("transform", `translate(${lerp(-70, 62, pb).toFixed(1)} 312) scale(.72)`);
    const su = prog(u, tv - .6, .4);
    anima(el, ".mamma", t, { x: 196, y: 404, s: .4, aS: su > 0 ? 150 : 14, aD: su > 0 ? 150 : 14, agitaS: su > 0, agitaD: su > 0 });
    anima(el, ".flavio", t, { x: 146, y: 408, s: .32, fase: 1.4, aS: 14, aD: 14 });
    el.querySelector(".mamma").style.opacity = el.querySelector(".flavio").style.opacity = prog(u, Math.max(1.2, D * .18), .4);
    pop(el, ".fum", prog(u, tv - .3, .8));
  }
};
