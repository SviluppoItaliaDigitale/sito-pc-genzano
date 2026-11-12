/* I momenti dei disegni seguono la voce: quando(k, "parola") dà i secondi dall'inizio della scena. */
const pop = (el, sel, p) => { const g = el.querySelector(sel); if (g) svgPop(g.querySelector(":scope > g") || g, p); };
const forza = t => .6 + .4 * Math.sin(t * 2.3) * Math.sin(t * .7 + 1);   // raffiche: da 0,2 a 1
function piega(el, sel, x, y, s, t, f = 0, k = 1) {
  const a = (7 + 13 * forza(t + f) + Math.sin(t * 6 + f) * 2) * k;
  el.querySelector(sel).setAttribute("transform", `translate(${x} ${y}) scale(${s}) skewX(${(-a).toFixed(2)})`);
}
function soffia(el, t, x0, span, ys, k = 1, dy = 0) {
  el.querySelectorAll(".soffi path").forEach(p => { const i = +p.dataset.i, q = (t * (.5 + hash(i + 2) * .25) + hash(i + 8)) % 1;
    const xx = Array.isArray(x0) ? x0[i % x0.length] : x0;
    p.setAttribute("transform", `translate(${(xx + q * span).toFixed(1)} ${(ys[i % ys.length] + q * dy).toFixed(1)})`);
    p.setAttribute("opacity", (Math.sin(q * Math.PI) * k).toFixed(2)); });
}
function volano(el, t, x0, x1, y0, y1, k = 1) {
  el.querySelectorAll(".foglie path").forEach(p => { const i = +p.dataset.i, q = (t * (.26 + hash(i + 4) * .2) + hash(i + 13)) % 1;
    const x = lerp(x0, x1, q), y = lerp(y0, y1, hash(i + 21)) + Math.sin(q * 9 + i) * 20;
    p.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(q * 900 + i * 40).toFixed(0)})`);
    p.setAttribute("opacity", (clamp(Math.sin(q * Math.PI) * 3) * k).toFixed(2)); });
}
const metti = (el, sel, x, y, s = 1, r = 0, o = 1) => { const g = el.querySelector(sel);
  g.setAttribute("transform", `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${r.toFixed(1)}) scale(${s.toFixed(3)})`); g.setAttribute("opacity", o.toFixed(2)); };
const botto = (el, sel, u, t0) => { pop(el, sel, prog(u, t0, .35)); el.querySelector(sel).setAttribute("opacity", (u < t0 ? 0 : 1 - prog(u, t0 + .5, .5)).toFixed(2)); };
function alTelefono(el, x, y, s, t) {
  el.querySelector(".cell").setAttribute("transform", `translate(${(x + 46 * s).toFixed(1)} ${(y - 222 * s + Math.sin(t * 3.2) * 3).toFixed(1)}) scale(${s.toFixed(2)}) rotate(18)`);
}
const ANIM = {
  titolo: (el, u, t) => {
    piega(el, ".a1", 92, 452, 1.12, t); piega(el, ".a2", 300, 450, .82, t, 1.3);
    soffia(el, t, -60, 470, [78, 138, 196, 300, 384]); volano(el, t, -30, 640, 110, 400);
    const tT = quando(0, "tegole") - .75, pT = prog(u, tT, .65), gT = pT * pT;          // la tegola scivola dal tetto e cade
    metti(el, ".teg", lerp(408, 398, pT), lerp(214, 436, gT), 1, pT > 0 ? lerp(-37, 170, pT) : -37 + Math.sin(t * 22) * 4 * forza(t));
    botto(el, ".b1", u, tT + .65);
    const tV = quando(0, "vasi") - .85, pV = prog(u, tV, .6), gV = pV * pV;             // il vaso cade dal davanzale
    metti(el, ".vaso", lerp(470, 476, pV), lerp(356, 440, gV) - (pV >= 1 ? 16 : 0), 1.05, pV > 0 ? lerp(0, 96, pV) : Math.sin(t * 9) * 5 * forza(t));
    botto(el, ".b2", u, tV + .6);
    anima(el, ".flavio", t, { x: 196, y: 494, s: .5, aS: 20, aD: 112, bocca: "o" });
  },
  balcone: (el, u, t) => {
    const t1 = quando(1, "metti"), t2 = quando(1, "fissa"), t3 = quando(1, "balconi");
    const d1 = Math.max(.9, t2 - t1), p1 = inOutCubic(prog(u, t1, d1));                 // porta il vaso dentro casa
    const p2 = inOutCubic(prog(u, t2 + .1, 1.1));                                       // torna verso la sedia
    const x = p2 > 0 ? lerp(150, 372, p2) : lerp(262, 150, p1), mov = (p1 > 0 && p1 < 1) || (p2 > 0 && p2 < 1) ? 1 : 0;
    const dentro = prog(p1, .78, .22), fine = prog(u, t3 + 1.3, .3);
    anima(el, ".flavio", t, { x, y: 400, s: .52, cammina: mov, flip: p2 > 0 && p2 < 1, aS: p1 > 0 && p1 < 1 ? 70 : fine ? 150 : 14, agitaS: fine > 0, aD: p2 >= 1 && !fine ? 60 : 14 });
    metti(el, ".vA", p1 > 0 ? x - 38 : 312, 400 - (p1 > 0 ? 10 : 0), 1.15 * (1 - .4 * dentro), 0, 1 - dentro);
    pop(el, ".ok1", prog(u, t1 + d1, .7));
    el.querySelector(".cinghia").setAttribute("stroke-dashoffset", (330 * (1 - outCubic(prog(u, t2 + .9, .8)))).toFixed(1));
    pop(el, ".ok2", prog(u, t2 + 1.6, .7));
    const p3 = inOutCubic(prog(u, t3, .7));                                             // il vaso del davanzale va dentro, la finestra si chiude
    metti(el, ".vD", 440, 240 - p3 * 30, 1.25 * (1 - .4 * p3), 0, 1 - prog(p3, .6, .4));
    el.querySelector(".ante").setAttribute("opacity", prog(u, t3 + .6, .4).toFixed(2));
    pop(el, ".ok3", prog(u, t3 + .9, .7));
  },
  parcheggio: (el, u, t) => {
    piega(el, ".a1", 96, 410, 1.2, t, 0, .45); volano(el, t, 20, 420, 150, 330, .8);
    metti(el, ".autoA", 118, 446, 1.15);
    pop(el, ".avv", prog(u, quando(2, "allerta") - .5, .8));
    el.querySelector(".barra").setAttribute("fill", Math.sin(t * 6) > 0 ? "#ffd43b" : "#ffe9a3");
    const tP = quando(2, "parcheggia") - .2, p = outCubic(prog(u, tP, 1.5));            // l'auto entra nel posto libero
    metti(el, ".autoB", lerp(720, 492, p), 462 + (p > 0 && p < 1 ? Math.sin(t * 24) * 1.2 : 0), 1.2);
    el.querySelector(".autoB").setAttribute("transform", el.querySelector(".autoB").getAttribute("transform") + " scale(-1 1)");
    const tN = quando(2, "lontano");
    pop(el, ".no", prog(u, tN, .7)); pop(el, ".si", prog(u, tN + .9, .7));
    anima(el, ".flavio", t, { x: 352, y: 436, s: .46, aD: u < tP ? 150 : 14, aS: u > tN ? 110 : 14 });
  },
  casa: (el, u, t) => {
    const tP = quando(3, "Chiudi"), tF = quando(3, "finestre") - .2, tL = quando(3, "stai lontano");
    const cp = outCubic(prog(u, tP, .7)), cf = outCubic(prog(u, tF, .7));
    piega(el, ".a1", 150, 300, .72, t); volano(el, t, 30, 270, 110, 250);
    el.querySelector(".porta").setAttribute("transform", `translate(566 0) scale(${(-lerp(.22, 1, cp)).toFixed(3)} 1)`);
    el.querySelector(".antaS").setAttribute("transform", `translate(52 0) scale(${lerp(.2, 1, cf).toFixed(3)} 1)`);
    el.querySelector(".antaD").setAttribute("transform", `translate(238 0) scale(${(-lerp(.2, 1, cf)).toFixed(3)} 1)`);
    soffia(el, t, 150, 190, [150, 205, 262], 1 - cf);
    const p = inOutCubic(prog(u, tL, 1.2)), x = lerp(292, 408, p), mov = p > 0 && p < 1 ? 1 : 0;
    anima(el, ".flavio", t, { x, y: 476, s: .52, cammina: mov, aS: p >= 1 ? 14 : u > tF - .5 && u < tL ? 110 : 14, aD: p >= 1 ? 150 : 14, agitaD: p >= 1, bocca: u < tF ? "o" : "sorriso" });
    const d = el.querySelector(".dist"); d.setAttribute("opacity", prog(u, tL + .5, .4).toFixed(2)); d.setAttribute("transform", `translate(${(Math.sin(t * 5) * 5).toFixed(1)} 0)`);
    pop(el, ".ok", prog(u, tL + 1.2, .7));
  },
  fuori: (el, u, t) => {
    piega(el, ".a1", 84, 374, 1.02, t, 2); piega(el, ".a2", 268, 374, 1.18, t);
    soffia(el, t, -60, 500, [150, 200, 250, 320]); volano(el, t, -30, 640, 140, 350);
    pop(el, ".no", prog(u, quando(4, "evita") - .2, .7));
    const tR = quando(4, "i rami") - .15, p = prog(u, tR, .7), g = p * p;               // il ramo si spezza e cade
    metti(el, ".ramo", lerp(322, 350, p), lerp(250, 364, g), 1, p > 0 ? lerp(-10, 8, p) + Math.sin(p * Math.PI) * 50 : -10 + Math.sin(t * 7) * 9 * forza(t));
    botto(el, ".crac", u, tR);
    const tS = quando(4, "Stai lontano"), q = inOutCubic(prog(u, tS, 1));
    anima(el, ".flavio", t, { x: lerp(504, 548, q), y: 386, s: .46, cammina: q > 0 && q < 1 ? 1 : 0, aS: u > tS ? 14 : 105, aD: 14, bocca: u > tR && u < tR + 2 ? "o" : "sorriso" });
  },
  strada: (el, u, t, D) => {
    const urto = x => Math.max(0, 1 - ((x - 250) / 60) ** 2) + Math.max(0, 1 - ((x - 478) / 62) ** 2);   // zone delle raffiche: uscita e viadotto
    const va = (sel, x, s) => { const w = urto(x);
      el.querySelector(sel).setAttribute("transform", `translate(${(x + Math.sin(t * 8) * 3 * w).toFixed(1)} 300) rotate(${(Math.sin(t * 8 + .6) * 6 * w).toFixed(2)}) scale(${s})`); };
    const t0 = quando(5, "rallenta") - .9, tF = quando(5, "viadotti") + .9;
    va(".mac", lerp(96, 548, outCubic(prog(u, t0, tF - t0))), .9);
    va(".moto", lerp(110, 392, outCubic(prog(u, t0 + (tF - t0) * .42, (tF - t0) * .6))), .86);
    soffia(el, t, [196, 420], 110, [196, 204, 226, 234, 256, 264], .55 + .45 * forza(t), 22);
    el.querySelector(".manica > g").setAttribute("transform", `rotate(${(8 + Math.sin(t * 11) * 7 - forza(t) * 6).toFixed(1)})`);
  },
  dopo: (el, u, t) => {
    el.querySelectorAll(".scint path").forEach(p => { const i = +p.dataset.i; p.setAttribute("opacity", hash(Math.floor(t * 9) + i * 7) > .45 ? 1 : 0); });
    pop(el, ".nt", prog(u, quando(6, "non toccare") - .2, .7));
    const a = el.querySelector(".att"); a.setAttribute("transform", `translate(520 ${(214 + Math.sin(t * 4) * 4).toFixed(1)})`); pop(el, ".att", prog(u, quando(6, "un albero"), .7));
    const tC = quando(6, "chiama") - .3, c = u >= tC, x = 338, y = 400, s = .5;
    anima(el, ".flavio", t, { x, y, s, aS: c ? 14 : 100, aD: c ? 165 : 14, bocca: c ? "sorriso" : "o" });
    alTelefono(el, x, y, s, t); el.querySelector(".cell").style.opacity = prog(u, tC, .25);
    el.querySelector(".fum").setAttribute("transform", `translate(${x + 72} 214)`); svgPop(el.querySelector(".fum > g"), prog(u, tC + .25, .8));
  }
};
