const ANIM_SCOSSA = (u, a, b) => prog(u, a, .3) * (1 - prog(u, b, .5));
function trema(el, t, forza) {
  el.querySelectorAll(".trema").forEach(g => {
    const x = Math.sin(t * 34) * 6 * forza + Math.sin(t * 21 + 1) * 3 * forza, r = Math.sin(t * 27) * .8 * forza;
    g.setAttribute("transform", `translate(${x.toFixed(1)} 0) rotate(${r.toFixed(2)} 300 430)`);
  });
}
const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const ANIM = {
  scuola: (el, u, t) => {
    const f = ANIM_SCOSSA(u, 1.2, 3); trema(el, t, f * .6);
    el.querySelector(".onde").setAttribute("opacity", f.toFixed(2));
    anima(el, ".flavio", t, { x: 528, y: 488, s: .6, aD: 150, agitaD: true, aS: 14, bocca: f > .3 ? "o" : "sorriso" });
  },
  sismografo: (el, u, t) => {
    const fine = 80 + 440 * prog(u, 0, 4.5);
    let d = "M80 134", y = 134;
    for (let x = 80; x <= fine; x += 4) {
      const c = Math.exp(-Math.pow((x - 330) / 55, 2));
      y = 134 + Math.sin(x * 1.3) * (3 + 82 * c) * (hash(x) * .6 + .4); d += ` L${x} ${y.toFixed(1)}`;
    }
    el.querySelector(".traccia").setAttribute("d", d);
    el.querySelector(".penna").setAttribute("transform", `translate(${fine.toFixed(1)} ${y.toFixed(1)})`);
    const p = el.querySelector(".pensa"); p.setAttribute("transform", `translate(200 ${(380 + Math.sin(t * 3) * 6).toFixed(1)})`);
    svgPop(p.firstElementChild, prog(u, 1.4, .8));
    anima(el, ".flavio", t, { x: 120, y: 498, s: .42, aS: 150, aD: 20, bocca: "o" });
  },
  prima: (el, u, t, D) => {
    const at = CONFIG.scene[2].listaAt;
    pop(el, ".ok1", prog(u, at[0] + .8, .8));
    const m = el.querySelector(".mappa"); m.style.opacity = prog(u, at[1], .4); m.setAttribute("transform", `translate(0 ${((1 - outBack(prog(u, at[1], .6))) * -30).toFixed(1)})`);
    pop(el, ".zaino", prog(u, at[2], .8));
    const punta = u < at[1] ? 80 : u < at[2] ? 120 : 30;
    anima(el, ".flavio", t, { x: 240, y: 470, s: .55, aD: punta, aS: u > at[2] ? 40 : 14, flip: u >= at[2] });
  },
  tavolo: (el, u, t, D) => {
    const f = ANIM_SCOSSA(u, .3, D - 2.6); trema(el, t, f * .7);
    const p = inOutCubic(prog(u, .5, 1.4)), giu = prog(u, 1.9, .5);   // corre sotto il tavolo, poi si abbassa
    const st = el.querySelector(".flavio"); st.setAttribute("opacity", (1 - prog(u, 1.9, .15)).toFixed(2));
    anima(el, st, t, { x: lerp(40, 300, p), y: 424, s: .48, cammina: p > 0 && p < 1 ? 1 : 0, bocca: "o" });
    const g = el.querySelector(".giu"), sorride = u > D - 2.4;
    g.style.opacity = giu > 0 ? 1 : 0;
    const e = outElastic(giu), r = Math.sin(t * 3.2) * 2;
    g.setAttribute("transform", `translate(372 ${(424 + r * .3).toFixed(1)}) scale(${(.78 * lerp(.6, 1, e)).toFixed(3)} ${(.78 * lerp(1.3, 1, e)).toFixed(3)})`);
    const bl = (t % 3.4) < .13 ? .12 : 1;
    g.querySelector(".occhi").setAttribute("transform", `translate(0 6) scale(1 ${bl}) translate(0 -6)`);
    g.querySelector(".bocca.sorriso").setAttribute("opacity", sorride ? 1 : 0);
    g.querySelector(".bocca.o").setAttribute("opacity", sorride ? 0 : 1);
    el.querySelectorAll(".cade > *").forEach(r => {
      const i = +r.dataset.i, p = prog(u, 1.4 + i * .9, .8), y = lerp(-40, [233, 237, 229][i], p * p);
      r.setAttribute("transform", `translate(${170 + i * 120} ${y.toFixed(1)}) rotate(${(p * 180 * (i % 2 ? 1 : -1)).toFixed(1)})`);
      r.setAttribute("opacity", p > 0 ? 1 : 0);
    });
    ["brav1", "brav2", "brav3"].forEach((c, i) => { const g = el.querySelector("." + c); svgPop(g, prog(u, D - 2.2 + i * .2, .7));
      if (u > D - 1.4) g.style.transform += ` rotate(${(Math.sin(t * 4 + i) * 12).toFixed(1)}deg)`; });
  },
  aperto: (el, u, t, D) => {
    const f = ANIM_SCOSSA(u, .2, D - 2.4); trema(el, t, f * .55);
    const p = inOutCubic(prog(u, 1, 3.4)), arriva = prog(u, 4.4, .8);
    anima(el, ".flavio", t, { x: lerp(180, 455, p), y: 470, s: .5, cammina: p > 0 && p < 1 ? 1 : 0, aS: p >= 1 ? 140 : 18, aD: p >= 1 ? 140 : 18, agitaS: p >= 1, agitaD: p >= 1, bocca: p < 1 ? "o" : "sorriso" });
    const z = el.querySelector(".zona"); z.style.opacity = arriva; svgPop(z.firstElementChild, arriva);
    ["st1", "st2", "st3"].forEach((c, i) => svgPop(el.querySelector("." + c), prog(u, 4.6 + i * .2, .7)));
  },
  fila: (el, u, t) => {
    const p = inOutCubic(prog(u, .6, 6)), mov = p > 0 && p < 1 ? 1 : 0, x0 = lerp(260, 470, p);
    anima(el, ".ins", t, { x: x0, y: 470, s: .6, cammina: mov, aD: 130, aS: 14, fase: 0 });
    [".k1", ".k2", ".k3"].forEach((c, i) => anima(el, c, t, { x: x0 - 92 - i * 78, y: 470, s: .44, cammina: mov, fase: 1 + i * .9, aD: 40, aS: 14 }));
  },
  dopo: (el, u, t, D) => {
    const at = CONFIG.scene[7].listaAt, p = inOutCubic(prog(u, .3, 3)), mov = p > 0 && p < 1 ? 1 : 0, x = lerp(60, 330, p);
    anima(el, ".mamma", t, { x: x - 2, y: 470, s: .55, cammina: mov, aD: 30 });
    anima(el, ".flavio", t, { x: x + 110, y: 470, s: .45, cammina: mov, fase: 1.3, aS: u > at[0] && u < at[1] ? 120 : 20, aD: u > at[2] ? 150 : 20, agitaD: u > at[2] });
    const cg = el.querySelector(".cuore"), c = cg.firstElementChild; cg.setAttribute("transform", `translate(${(x + 50).toFixed(1)} ${(250 + Math.sin(t * 3) * 6).toFixed(1)})`);
    c.style.opacity = prog(u, at[0] + .2, .3); c.style.transformBox = "fill-box"; c.style.transformOrigin = "50% 50%";
    c.style.transform = `scale(${(outElastic(prog(u, at[0] + .2, .8)) * (1 + Math.sin(t * 6) * .06)).toFixed(3)})`;
  },
  sereno: (el, u, t) => {
    const s = el.querySelector(".sole"); s.setAttribute("transform", `translate(470 ${lerp(220, 110, outBack(prog(u, .1, 1.2))).toFixed(1)})`);
    el.querySelector(".raggi").setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`);
    anima(el, ".flavio", t, { x: 230, y: 492, s: .55, aD: 150, agitaD: true });
    anima(el, ".silvia", t, { x: 370, y: 492, s: .55, aS: 150, agitaS: true, fase: 2 });
  }
};
