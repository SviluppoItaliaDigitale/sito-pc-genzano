const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const ANIM = {
  gruppo: (el, u, t) => {
    [["v1", 110, .5], ["p1", 210, .52], ["p2", 310, .5], ["v2", 410, .52]].forEach(([c, x, s], i) => anima(el, "." + c, t, { x, y: 480, s, fase: i * 1.3, aS: 14, aD: 14 }));
    anima(el, ".flavio", t, { x: 510, y: 480, s: .42, aD: 150, agitaD: true });
    el.querySelectorAll(".cuori path").forEach(h => { const i = +h.dataset.i, q = (t * .4 + i * .33) % 1;
      h.setAttribute("transform", `translate(${(180 + i * 120 + Math.sin(q * 6) * 14).toFixed(1)} ${(220 - q * 140).toFixed(1)}) scale(.8)`); h.setAttribute("opacity", (Math.sin(q * Math.PI) * prog(u, .8, .5)).toFixed(2)); });
  },
  volontari: (el, u, t) => {
    const p = inOutCubic(prog(u, .5, 2.2)), mov = p > 0 && p < 1 ? 1 : 0, x = lerp(60, 250, p);
    anima(el, ".v1", t, { x, y: 470, s: .6, cammina: mov, aS: 40, aD: 40 });
    el.querySelector(".scat").setAttribute("transform", `translate(${x.toFixed(1)} ${(470 - 82 + Math.sin(t * 3.2) * 3 - (mov ? Math.abs(Math.sin(t * 9)) * 7 : 0)).toFixed(1)})`);
    anima(el, ".v2", t, { x: 330, y: 470, s: .6, aD: 150, aS: 14, fase: 1.4 });
    el.querySelector(".radio").setAttribute("transform", `translate(${(330 + 40).toFixed(1)} ${(470 - 270 * .6 + Math.sin(t * 3.2 + 1.4) * 3).toFixed(1)}) scale(.8)`);
  },
  catena: (el, u, t) => {
    [0, 1, 2, 3].forEach(j => pop(el, ".c" + j, prog(u, .6 + j * 1.3, .8)));
    [0, 1, 2].forEach(j => { const g = el.querySelector(".f" + j); g.style.opacity = prog(u, 1.2 + j * 1.3, .4); g.firstElementChild.setAttribute("transform", `translate(${(Math.sin(t * 5 + j) * 4).toFixed(1)} 0)`); });
  },
  entra: (el, u, t) => {
    const g = el.querySelector(".torta"); g.setAttribute("transform", `translate(140 ${(220 + Math.sin(t * 2) * 5).toFixed(1)})`); svgPop(g.firstElementChild, prog(u, .6, .9));
    anima(el, ".ragazzo", t, { x: 260, y: 470, s: .56, aD: 150, agitaD: u < 3, aS: 14 });
    anima(el, ".v1", t, { x: 430, y: 470, s: .6, aS: 120, aD: 14, fase: 1.2 });
    const l = el.querySelector(".lib"); l.setAttribute("transform", `translate(430 ${(150 + Math.sin(t * 2.4) * 6).toFixed(1)})`); l.style.opacity = prog(u, 2.4, .4);
  },
  parte: (el, u, t) => {
    anima(el, ".mamma", t, { x: 150, y: 470, s: .6, aD: 100, aS: 14 });
    anima(el, ".flavio", t, { x: 300, y: 470, s: .48, aS: 120, aD: 14, fase: 1 });
    anima(el, ".silvia", t, { x: 440, y: 470, s: .48, aS: 14, aD: 150, agitaD: true, fase: 2 });
    ["s1", "s2"].forEach((c, i) => svgPop(el.querySelector("." + c), prog(u, 5.2 + i * .2, .7)));
  },
  sereno: (el, u, t) => {
    const s = el.querySelector(".sole"); s.setAttribute("transform", `translate(500 ${lerp(210, 100, outBack(prog(u, .1, 1.2))).toFixed(1)})`);
    el.querySelector(".raggi").setAttribute("transform", `rotate(${(t * 25).toFixed(1)})`);
    anima(el, ".v1", t, { x: 170, y: 492, s: .58, aD: 150, agitaD: true });
    anima(el, ".flavio", t, { x: 300, y: 492, s: .48, aD: 150, agitaD: true, fase: 1 });
    anima(el, ".silvia", t, { x: 410, y: 492, s: .48, aS: 150, agitaS: true, fase: 2 });
  }
};
