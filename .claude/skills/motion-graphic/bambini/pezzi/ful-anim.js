const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const op = (el, sel, v) => el.querySelector(sel).setAttribute("opacity", clamp(v).toFixed(2));
function piove(el, t, v = 1) {
  el.querySelectorAll(".pioggia").forEach(g => { const y0 = +g.dataset.y0, y1 = +g.dataset.y1;
    g.querySelectorAll("path").forEach(p => { const i = +p.dataset.i, q = (t * (1.3 + hash(i) * .6) * v + hash(i + 5)) % 1;
      p.setAttribute("transform", `translate(${(+p.dataset.x - q * 40).toFixed(1)} ${(y0 + q * (y1 - y0)).toFixed(1)})`); }); });
}
/* fulmine disegnato: compare di colpo, resta, sfuma. Il velo chiaro è debole (al massimo .2) e raro. */
const lampo = (u, tempi) => Math.max(...tempi.map(a => { const p = u - a; return p < 0 || p > .75 ? 0 : p < .06 ? p / .06 : 1 - prog(p, .4, .35); }));
function saetta(el, u, tempi, velo = .2) {
  const l = lampo(u, tempi); op(el, ".saetta", l);
  const v = el.querySelector(".velo"); if (v) v.setAttribute("opacity", (l * velo).toFixed(2));
  return l;
}
const raggi = (el, t) => el.querySelectorAll(".raggi").forEach(r => r.setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`));
const ANIM = {
  temporale: (el, u, t) => {
    piove(el, t); op(el, ".buio", lerp(.2, .5, prog(u, 0, 3.2)));
    const l = saetta(el, u, [-.1, 3.8, 6.9]);
    el.querySelector(".nuvolone").setAttribute("transform", `translate(${(Math.sin(t * .7) * 8).toFixed(1)} ${(Math.sin(t * 1.1) * 3).toFixed(1)})`);
    anima(el, ".flavio", t, { x: 150, y: 486, s: .58, aS: 14, aD: 150, bocca: l > .2 ? "o" : "sorriso" });
  },
  prima: (el, u, t) => {
    const scuro = inOutCubic(prog(u, 5.5, 1.6)), via = inOutCubic(prog(u, 7.0, 1.5)), gioca = 1 - prog(u, 6.3, .5);
    op(el, ".buio", scuro * .42); raggi(el, t);
    el.querySelector(".arriva").setAttribute("transform", `translate(${lerp(640, 352, scuro).toFixed(1)} 52)`);
    pop(el, ".prev", prog(u, 2.9, .8)); op(el, ".barra", .7 + Math.sin(t * 5) * .3);
    const q = (Math.sin(u * 2.6) + 1) / 2, salto = Math.abs(Math.sin(u * 2.6 * 2)) * 60 * gioca;
    const fx = lerp(225, 160, via), sx = lerp(365, 240, via), mov = via > 0 && via < 1 ? 1 : 0;
    el.querySelector(".palla").setAttribute("transform", `translate(${lerp(lerp(258, 332, q), 300, 1 - gioca).toFixed(1)} ${(452 - salto).toFixed(1)}) rotate(${(u * 160 * gioca).toFixed(1)})`);
    anima(el, ".flavio", t, { x: fx, y: 470, s: .45, cammina: mov, aD: scuro > .5 && !mov && via < 1 ? 150 : 24, aS: 14, bocca: scuro > .3 && via < 1 ? "o" : "sorriso" });
    anima(el, ".silvia", t, { x: sx, y: 470, s: .45, cammina: mov, fase: 1.7, aS: 24, aD: 14, bocca: scuro > .3 && via < 1 ? "o" : "sorriso" });
  },
  tuono: (el, u, t) => {
    piove(el, t);
    const forza = prog(u, .3, .3) * (1 - prog(u, 4.6, 1.2));
    el.querySelectorAll(".onde path").forEach(p => { const i = +p.dataset.i, q = (u * .55 + i / 3) % 1, r = 110 + q * 230, a0 = .12, a1 = 1.25;
      p.setAttribute("d", `M${(150 + Math.cos(a0) * r).toFixed(1)} ${(96 + Math.sin(a0) * r).toFixed(1)} A${r.toFixed(1)} ${r.toFixed(1)} 0 0 1 ${(150 + Math.cos(a1) * r).toFixed(1)} ${(96 + Math.sin(a1) * r).toFixed(1)}`);
      p.setAttribute("opacity", (forza * Math.sin(q * Math.PI) * .8).toFixed(2)); });
    pop(el, ".km", prog(u, 2.6, .8));
    const p = inOutCubic(prog(u, 5.4, 2.1)), mov = p > 0 && p < 1 ? 1 : 0;
    anima(el, ".flavio", t, { x: lerp(96, 466, p), y: 464, s: .5, cammina: mov, aS: p >= 1 ? 14 : 30, aD: p >= 1 ? 150 : 30, agitaD: p >= 1, bocca: p < 1 ? "o" : "sorriso" });
    pop(el, ".ok", prog(u, 7.5, .7));
  },
  riparo: (el, u, t) => {
    const at = CONFIG.scene[3].listaAt; piove(el, t);
    const p = inOutCubic(prog(u, .5, 1.3)), f = el.querySelector(".flavio");
    anima(el, f, t, { x: lerp(250, 86, p), y: 376, s: .36, cammina: p > 0 && p < 1 ? 1 : 0, bocca: "o" });
    f.setAttribute("opacity", (1 - prog(u, 1.75, .25)).toFixed(2));
    pop(el, ".ok1", prog(u, at[0] + .2, .7));
    pop(el, ".auto", prog(u, at[1] - .5, .8)); pop(el, ".ok2", prog(u, at[1] + .5, .7));
    pop(el, ".no3", prog(u, at[2] + .2, .7));
  },
  aperto: (el, u, t) => {
    const at = CONFIG.scene[4].listaAt; piove(el, t);
    const va = inOutCubic(prog(u, .3, 1.5)), torna = inOutCubic(prog(u, 5.2, 1.4)), x = lerp(lerp(40, 132, va), 52, torna);
    const mov = (va > 0 && va < 1) || (torna > 0 && torna < 1) ? 1 : 0;
    const l = saetta(el, u, [4.5], .18);
    anima(el, ".flavio", t, { x, y: 374, s: .38, cammina: mov, aS: 14, aD: u > at[0] && u < 5.2 ? 60 : 16, bocca: u > at[0] && torna < 1 ? "o" : "sorriso" });
    el.querySelector(".pino").setAttribute("transform", `rotate(${(l * Math.sin(t * 40) * 1.5).toFixed(2)} 215 362)`);
    [".n0", ".n1", ".n2", ".n3"].forEach((s, i) => pop(el, s, prog(u, at[i] + (i ? .15 : .1), .7)));
  },
  casa: (el, u, t) => {
    piove(el, t);
    const ch = inOutCubic(prog(u, 1.0, 1.0));   // le ante si chiudono
    const aS = el.querySelector(".antaS"), aD = el.querySelector(".antaD"), w = lerp(14, 66, ch);
    aS.setAttribute("width", w.toFixed(1)); aD.setAttribute("width", w.toFixed(1)); aD.setAttribute("x", (166 - w).toFixed(1));
    pop(el, ".okf", prog(u, 2.0, .7));
    const st = inOutCubic(prog(u, 3.0, .9)), sx = lerp(486, 462, st), sy = lerp(321, 388, st);
    el.querySelector(".spina").setAttribute("transform", `translate(${sx.toFixed(1)} ${sy.toFixed(1)}) rotate(${lerp(90, 20, st).toFixed(1)})`);
    el.querySelector(".filo").setAttribute("d", `M444 392 Q${lerp(470, 452, st).toFixed(1)} ${lerp(410, 404, st).toFixed(1)} ${(sx - 6).toFixed(1)} ${(sy + 4).toFixed(1)}`);
    const acceso = st < 1 ? "#74c0fc" : "#343a40"; el.querySelector(".tv").setAttribute("fill", acceso); el.querySelector(".pcs").setAttribute("fill", acceso);
    pop(el, ".nof", prog(u, 5.4, .7));
    const tel = prog(u, 6.9, .4);
    anima(el, ".flavio", t, { x: 540, y: 470, s: .5, aS: st > 0 && st < 1 ? 70 : 14, aD: tel > 0 ? 165 : 20 });
    const c = el.querySelector(".cell"); c.setAttribute("transform", `translate(563 ${(359 + Math.sin(t * 3.2) * 3).toFixed(1)}) scale(.5) rotate(18)`); c.setAttribute("opacity", tel.toFixed(2));
    pop(el, ".okc", prog(u, 7.3, .7)); pop(el, ".dopo", prog(u, 8.3, .8));
  },
  sereno: (el, u, t) => {
    const g = prog(u, .5, 3.6), a = g * 180, r = 68, rad = a * Math.PI / 180;
    el.querySelector(".lanc").setAttribute("transform", `rotate(${a.toFixed(1)})`);
    el.querySelector(".spicchio").setAttribute("d", a < .5 ? "" : `M0 0 L0 ${-r} A${r} ${r} 0 0 1 ${(Math.sin(rad) * r).toFixed(1)} ${(-Math.cos(rad) * r).toFixed(1)}Z`);
    pop(el, ".min", prog(u, .9, .8));
    const sch = inOutCubic(prog(u, 2.2, 2.2));
    op(el, ".buio", .3 * (1 - sch));
    el.querySelector(".via").setAttribute("transform", `translate(${lerp(330, 660, sch).toFixed(1)} 112)`);
    el.querySelector(".sole").setAttribute("transform", `translate(492 ${lerp(196, 176, sch).toFixed(1)}) scale(${lerp(.8, 1, outBack(sch)).toFixed(3)})`);
    raggi(el, t);
    const fuori = sch >= 1;
    anima(el, ".flavio", t, { x: 318, y: 404, s: .44, aD: fuori ? 150 : 20, agitaD: fuori, aS: 14 });
    anima(el, ".silvia", t, { x: 404, y: 404, s: .44, aS: fuori ? 150 : 20, agitaS: fuori, aD: 14, fase: 2 });
  }
};
