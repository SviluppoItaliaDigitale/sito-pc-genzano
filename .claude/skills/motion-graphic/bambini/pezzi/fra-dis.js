/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const TERRA = "#b98a55", TERRA2 = "#8f6236";
const SASSO = (cls, r = 12, c = "#ced4da") => `<path class="${cls}" d="M${-r} ${r * .3} Q${-r * 1.1} ${-r * .7} ${-r * .2} ${-r} Q${r * .9} ${-r * 1.05} ${r} ${-r * .1} Q${r * 1.05} ${r * .8} ${r * .1} ${r} Q${-r * .8} ${r * 1.05} ${-r} ${r * .3}Z" fill="${c}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`;
const SASSI = (cls, n, r = 11) => `<g class="${cls}">${Array.from({ length: n }, (_, i) => `<g data-i="${i}">${SASSO("", r - (i % 3) * 2, i % 2 ? "#adb5bd" : "#ced4da")}</g>`).join("")}</g>`;
/* punto e inclinazione lungo una curva di pendio (Bézier quadratica); n = distanza dalla superficie verso l'esterno */
function sulPendio(c, s, n = 0) {
  const [x0, y0, x1, y1, x2, y2] = c, a = 1 - s;
  const x = a * a * x0 + 2 * a * s * x1 + s * s * x2, y = a * a * y0 + 2 * a * s * y1 + s * s * y2;
  const tx = 2 * a * (x1 - x0) + 2 * s * (x2 - x1), ty = 2 * a * (y1 - y0) + 2 * s * (y2 - y1), m = Math.hypot(tx, ty);
  return [x + ty / m * n, y - tx / m * n, Math.atan2(ty, tx) * 180 / Math.PI];
}
const P_TIT = [130, 410, 380, 320, 610, 80], P_SEG = [330, 345, 470, 300, 610, 200], P_CASA = [330, 432, 470, 330, 610, 70];
/* nicchia di distacco (lente scavata nel pendio) e colata (massa di terra appoggiata sul pendio) */
function LENTE(c, s0, s1, prof, fuori = 0) {
  const N = 12, su = [], giu = [];
  for (let i = 0; i <= N; i++) { const k = i / N, s = lerp(s0, s1, k), g = Math.sin(k * Math.PI);
    su.push(sulPendio(c, s, fuori * g * (1 + .22 * Math.sin(k * 17))).slice(0, 2).map(v => v.toFixed(1)).join(" "));
    giu.push(sulPendio(c, s, -prof * g).slice(0, 2).map(v => v.toFixed(1)).join(" ")); }
  return "M" + su.join(" L") + " L" + giu.reverse().join(" L") + "Z";
}
/* albero e palo: origine alla base; il gruppo interno (classe) si inclina */
const ALBERO = (cls, x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})"><g class="${cls}"><rect x="-9" y="-84" width="18" height="84" fill="#a0703c" ${O}/><circle cx="0" cy="-112" r="46" fill="#40c057" ${O}/><circle cx="-16" cy="-124" r="9" fill="#8ce99a" stroke="none"/></g></g>`;
const PALO = (cls, x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})"><g class="${cls}"><rect x="-6" y="-170" width="12" height="170" fill="#c08a4f" ${O}/><rect x="-34" y="-158" width="68" height="11" rx="4" fill="#c08a4f" ${O}/><circle cx="-26" cy="-164" r="6" fill="#fff" ${O}/><circle cx="26" cy="-164" r="6" fill="#fff" ${O}/></g></g>`;
const CASA = (x, base, w, h, col = "#ffe066") => `<g ${O}><rect x="${x}" y="${base - h}" width="${w}" height="${h}" fill="${col}"/><path d="M${x - 10} ${base - h} L${x + w / 2} ${base - h - w * .38} L${x + w + 10} ${base - h}Z" fill="#fa5252"/>
  <rect x="${x + w * .58}" y="${base - h * .58}" width="${w * .24}" height="${h * .58}" fill="#c08a4f"/><rect x="${x + w * .14}" y="${base - h * .7}" width="${w * .28}" height="${h * .3}" fill="#a5d8ff"/></g>`;
const FRECCIA = (cls, d, c) => `<g class="${cls}" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="${d}" stroke="${INK}" stroke-width="21"/><path d="${d}" stroke="${c}" stroke-width="11"/></g>`;
const TARGA = (cls, x, y, testo, w) => `<g class="${cls}" transform="translate(${x} ${y})"><g><rect x="${-w / 2}" y="-19" width="${w}" height="38" rx="14" fill="#fff" stroke="${INK}" stroke-width="4"/><text x="0" y="8" text-anchor="middle" font-family="Titillium Web" font-weight="800" font-size="22" fill="${INK}">${testo}</text></g></g>`;
const PIOGGIA = (n = 26, x0 = 0, x1 = 600, y0 = 0, y1 = 440) => `<g class="pioggia" stroke="#4dabf7" stroke-width="5" stroke-linecap="round" data-y0="${y0}" data-y1="${y1}">${Array.from({ length: n }, (_, i) =>
  `<path data-i="${i}" data-x="${(x0 + hash(i + 31) * (x1 - x0)).toFixed(0)}" d="M0 0 l-8 22"/>`).join("")}</g>`;
const NERA = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 40 Q-4 10 26 12 Q34 -14 64 -4 Q84 -22 106 0 Q132 2 128 30 Q140 44 120 52 H8 Q-10 52 0 40Z" fill="#adb5bd" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/></g>`;
/* accovacciato, con tutte e due le braccia sopra la testa */
function ACCUCCIATO(cls, o = {}) {
  const c = Object.assign({ maglia: "#ff922b", pantaloni: "#4dabf7", pelle: "#ffd8b1", capelli: "#8b5a2b" }, o);
  return `<g class="${cls}" stroke="${INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"><g class="corpo">
    <rect x="-78" y="-34" width="96" height="34" rx="16" fill="${c.pantaloni}"/><ellipse cx="-80" cy="-12" rx="14" ry="13" fill="#495057"/>
    <rect x="-58" y="-86" width="42" height="70" rx="18" fill="${c.pantaloni}"/>
    <rect x="-52" y="-150" width="72" height="98" rx="30" fill="${c.maglia}" transform="rotate(38 -16 -70)"/>
    <path d="M-16 -122 Q-40 -186 8 -196 Q30 -200 44 -190" fill="none" stroke-width="30"/><path d="M-16 -122 Q-40 -186 8 -196 Q30 -200 44 -190" fill="none" stroke="${c.maglia}" stroke-width="20"/>
    <g class="testa" transform="translate(40 -118)"><circle r="50" fill="${c.pelle}"/>
      <path d="M-46 -14 Q-44 -56 0 -52 Q40 -54 48 -14 Q30 -34 2 -30 Q-26 -36 -46 -14Z" fill="${c.capelli}"/>
      <g class="occhi"><ellipse cx="2" cy="6" rx="6" ry="9" fill="${INK}" stroke="none"/><ellipse cx="30" cy="6" rx="6" ry="9" fill="${INK}" stroke="none"/></g>
      <circle cx="40" cy="24" r="8" fill="#ff8787" opacity=".55" stroke="none"/>
      <path class="bocca sorriso" d="M8 26 Q20 36 32 26" fill="none"/><ellipse class="bocca o" cx="20" cy="30" rx="7" ry="8" fill="#c92a2a" opacity="0"/></g>
    <circle cx="48" cy="-188" r="12" fill="${c.pelle}"/>
    <path d="M-2 -132 Q14 -186 52 -176 Q82 -168 84 -150" fill="none" stroke-width="30"/><path d="M-2 -132 Q14 -186 52 -176 Q82 -168 84 -150" fill="none" stroke="${c.maglia}" stroke-width="20"/><circle cx="84" cy="-148" r="12" fill="${c.pelle}"/>
  </g></g>`;
}
Object.assign(ICONE, {
  crepa: `<svg viewBox="0 0 100 100"><rect x="10" y="14" width="80" height="72" rx="8" fill="#e9d5bf" ${O}/><path d="M10 38 H90 M10 62 H90" stroke="#c9a27a" stroke-width="4"/><path d="M54 14 L42 34 L60 50 L40 68 L52 86" fill="none" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/></svg>`,
  storto: `<svg viewBox="0 0 100 100"><path d="M6 84 Q50 74 94 88" fill="none" ${O}/><g transform="rotate(20 36 82)"><rect x="31" y="46" width="10" height="36" fill="#a0703c" ${O}/><circle cx="36" cy="34" r="20" fill="#40c057" ${O}/></g><g transform="rotate(16 74 86)"><path d="M74 86 V26 M60 34 H88" stroke="#c08a4f" stroke-width="8" stroke-linecap="round"/></g></svg>`,
  smotta: `<svg viewBox="0 0 100 100"><path d="M8 88 L88 16 V88Z" fill="#8ce99a" ${O}/><path d="M70 34 Q50 40 36 64 Q30 78 44 80 Q60 76 66 60 Q76 48 70 34Z" fill="${TERRA}" ${O}/><circle cx="26" cy="82" r="7" fill="#ced4da" ${O}/><circle cx="42" cy="88" r="5" fill="#adb5bd" ${O}/></svg>`
});
const ILL = {
  titolo: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 36, .55)}${NUVOLA(290, 22, .45)}
    <path d="M-10 430 L130 410 Q380 320 610 80 V520 H-10Z" fill="#8ce99a" ${O}/>
    <path d="${LENTE(P_TIT, .34, .86, 30)}" fill="${TERRA2}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
    <g class="lembo"><path d="M-66 4 Q-74 -30 -34 -36 Q0 -46 38 -36 Q76 -30 66 4 Q0 18 -66 4Z" fill="${TERRA}" ${O}/><path d="M-52 -30 Q-26 -44 2 -43 Q30 -43 54 -30" fill="none" stroke="#40c057" stroke-width="13" stroke-linecap="round"/><circle cx="-24" cy="-8" r="7" fill="${TERRA2}"/><circle cx="20" cy="-12" r="5" fill="${TERRA2}"/></g>
    ${SASSI("sassi", 4, 13)}${PG("flavio")}</svg>`,
  pioggia: () => `<svg ${S0}><rect width="600" height="510" fill="#c5dff8"/>${NERA(20, 18, .9)}${NERA(230, 34, 1)}${NERA(440, 14, .8)}
    <path d="M300 520 V350 Q460 280 610 210 V520Z" fill="#69db7c" ${O}/>
    <ellipse cx="410" cy="446" rx="200" ry="46" fill="#4dabf7" ${O}/>
    <g class="onde" fill="none" stroke="#d0ebff" stroke-width="5" stroke-linecap="round">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 0 q14 -8 28 0 t28 0"/>`).join("")}</g>
    <path d="M-10 192 H128 Q190 194 218 262 L330 520 H-10Z" fill="#8ce99a" ${O}/>
    <path class="zuppo" d="M150 197 Q192 204 214 264 L322 512 H214 L132 300Z" fill="${TERRA2}" opacity="0"/>
    <g class="rivoli" fill="none" stroke="#4dabf7" stroke-width="6" stroke-linecap="round" stroke-dasharray="14 20"><path d="M176 214 Q204 270 222 318 L296 500"/><path d="M158 240 Q180 300 204 350 L262 500"/></g>
    <path d="M-10 192 H128 Q190 194 218 262 L330 520" fill="none" ${O}/>
    ${CASA(14, 192, 44, 36)}${CASA(70, 192, 40, 44, "#ffd8a8")}
    ${PIOGGIA(30)}${TARGA("tgG", 78, 110, "Genzano", 120)}${TARGA("tgL", 436, 448, "lago di Nemi", 164)}</svg>`,
  segnali: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${NUVOLA(50, 26, .6)}${NUVOLA(300, 50, .45)}
    <path d="M330 345 Q470 300 610 200 V400 H330Z" fill="#69db7c" ${O}/>
    <path class="nicchia" d="${LENTE(P_SEG, .36, .62, 16)}" fill="${TERRA2}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
    <g class="smot"><path d="M-30 6 Q-34 -14 -10 -16 Q14 -22 30 -8 Q36 6 22 12 Q-8 18 -30 6Z" fill="${TERRA}" ${O}/><path d="M-22 -12 Q-4 -22 20 -14" fill="none" stroke="#40c057" stroke-width="9" stroke-linecap="round"/></g>
    ${SASSI("sassi", 3, 9)}
    <path d="M-10 336 Q300 330 610 372 V520 H-10Z" fill="#8ce99a" ${O}/>
    <g ${O}><rect x="36" y="230" width="124" height="110" fill="#e9d5bf"/><path d="M36 266 H160 M36 302 H160 M98 230 V266 M66 266 V302 M130 266 V302 M98 302 V340" stroke="#c9a27a" stroke-width="4"/><rect x="36" y="230" width="124" height="110" fill="none"/></g>
    <path class="crM" pathLength="1" d="M104 230 L90 258 L112 282 L92 310 L104 340" fill="none" stroke="${INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
    <path class="crT" pathLength="1" d="M172 356 L196 366 L212 354 L236 370 L254 360" fill="none" stroke="#5c3d1e" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>
    ${ALBERO("alb", 300, 342, .95)}${PALO("palo", 388, 349, .95)}
    <g class="fum" transform="translate(478 176)"><g><path d="M-58 -46 H58 Q70 -46 70 -34 V30 Q70 42 58 42 H44 L60 70 L14 42 H-58 Q-70 42 -70 30 V-34 Q-70 -46 -58 -46Z" fill="#fff" ${O}/><g transform="translate(-40 -42) scale(.8)">${INTERNO("comune")}</g></g></g>
    ${PG("flavio")}</svg>`,
  casa: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(30, 34, .5)}${NUVOLA(250, 60, .4)}
    <path d="M-10 432 H330 Q470 330 610 70 V520 H-10Z" fill="#8ce99a" ${O}/>
    <path d="${LENTE(P_CASA, .5, .93, 26)}" fill="${TERRA2}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
    ${CASA(120, 432, 150, 104)}
    <g class="massa"><path d="${LENTE(P_CASA, .24, .8, 0, 52)}" fill="${TERRA}" ${O}/>${[.34, .46, .58, .7].map((s, i) => { const [x, y] = sulPendio(P_CASA, s, 18 + (i % 2) * 14); return `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${7 + (i % 2) * 3}" fill="${TERRA2}" stroke="none"/>`; }).join("")}
      ${[.3, .52].map((s, i) => { const [x, y] = sulPendio(P_CASA, s, 30); return `<g transform="translate(${x.toFixed(0)} ${y.toFixed(0)})">${SASSO("", 11 - i * 2, i ? "#adb5bd" : "#ced4da")}</g>`; }).join("")}</g>
    ${SASSI("sassi", 3, 10)}
    <g transform="translate(336 434)"><g class="muro" ${O}><rect x="-13" y="-96" width="26" height="96" fill="#ced4da"/><path d="M-13 -64 H13 M-13 -32 H13" stroke-width="3"/></g></g>
    ${FRECCIA("via", "M252 196 H76 M120 160 L76 196 L120 232", "#40c057")}
    ${PG("mamma", { tipo: "adulta", maglia: "#9775fa", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}</svg>`,
  lato: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(20, 24, .5)}${NUVOLA(440, 30, .5)}
    <path d="M-10 520 V300 Q300 20 610 300 V520Z" fill="#8ce99a" ${O}/>
    <path class="lingua" d="" fill="${TERRA}" ${O}/>${SASSI("sassi", 5, 12)}
    ${FRECCIA("fFrana", "M300 176 V296 M266 258 L300 298 L334 258", "#e03131")}
    <path d="M356 520 V444 Q450 300 610 290 V520Z" fill="#69db7c" ${O}/>
    ${ALBERO("al1", 76, 440, .9)}${PALO("pa1", 168, 452, .8)}${DIVIETO("np", 122, 330, 46)}
    ${FRECCIA("fVia", "M338 470 Q420 452 468 392 M424 388 L470 386 L476 432", "#40c057")}
    ${PG("flavio")}${SPUNTA("ok", 566, 222, 30)}</svg>`,
  rannicchia: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>
    <g class="gA"><path d="M-10 330 Q300 210 610 300 V520 H-10Z" fill="#8ce99a" ${O}/>${PRATO(440)}
      ${SASSI("sassi", 3, 9)}
      <path class="scudo" d="M214 318 A132 132 0 0 1 478 318" fill="none" stroke="#f59f00" stroke-width="11" stroke-linecap="round" stroke-dasharray="2 24"/>
      ${ACCUCCIATO("giu")}${STELLA("brav1", 500, 150, 26)}${STELLA("brav2", 548, 214, 18, "#ff922b")}${STELLA("brav3", 446, 108, 16, "#4dabf7")}</g>
    <g class="gB"><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 40, .55)}
      <path d="M-10 520 V476 Q120 410 300 452 L290 520Z" fill="${TERRA}" ${O}/><g transform="translate(90 462)">${SASSO("", 14)}</g><g transform="translate(170 448)">${SASSO("", 10, "#adb5bd")}</g><g transform="translate(232 466)">${SASSO("", 12)}</g>
      <path d="M322 252 H610 V520 H276 L296 420 L316 344 L304 294Z" fill="${TERRA}" ${O}/><path d="M340 330 L352 380 M330 420 L348 470 M400 320 V360" stroke="${TERRA2}" stroke-width="6" stroke-linecap="round" fill="none"/>
      <path d="M322 252 H610 V288 H334 Q314 276 322 252Z" fill="#8ce99a" ${O}/>
      <g class="zolla"><path d="M322 252 H384 L374 312 L316 312 L304 292Z" fill="${TERRA}" ${O}/><path d="M322 252 H384 L380 284 H330 Q314 274 322 252Z" fill="#8ce99a" ${O}/></g>
      <path class="crepaB" pathLength="1" d="M386 250 L378 276 L388 296 L374 318" fill="none" stroke="${INK}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
      ${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}${DIVIETO("np", 372, 150, 50)}</g></svg>`,
  strada: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${SOLE(52, 162, 26)}${NUVOLA(330, 118, .45)}
    <path d="M-10 300 V268 Q110 236 270 300Z" fill="#69db7c" ${O}/><path d="M240 300 Q430 250 610 96 V300Z" fill="#8ce99a" ${O}/>
    <path d="M604 130 Q560 190 536 250 L560 262 Q580 200 610 170Z" fill="${TERRA2}" stroke="${INK}" stroke-width="4"/>
    <rect x="-10" y="290" width="620" height="62" fill="#868e96" ${O}/><path d="M0 321 H480" stroke="#fff" stroke-width="5" stroke-dasharray="34 26"/>
    <path d="M-10 352 H610 V520 H-10Z" fill="#69db7c" ${O}/>
    <g class="mucchio"><path d="M610 196 Q560 250 528 296 Q492 340 506 388 H610Z" fill="${TERRA}" ${O}/><circle cx="572" cy="300" r="9" fill="${TERRA2}"/><circle cx="548" cy="350" r="7" fill="${TERRA2}"/>
      <g transform="translate(520 372)">${SASSO("", 13)}</g><g transform="translate(556 330)">${SASSO("", 10, "#adb5bd")}</g><g transform="translate(486 380)">${SASSO("", 8)}</g></g>
    <g class="autoB"><g transform="translate(-50 -50)">${INTERNO("auto").replace("#ff8787", "#74c0fc")}</g></g>
    <g class="autoA"><g transform="translate(-50 -50)">${INTERNO("auto")}</g><circle class="luce" cx="40" cy="6" r="6" fill="#ff922b" stroke="${INK}" stroke-width="3"/><circle class="luce" cx="-42" cy="6" r="6" fill="#ff922b" stroke="${INK}" stroke-width="3"/></g>
    ${PG("mamma", { tipo: "adulta", maglia: "#9775fa", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}
    <g class="fum" transform="translate(196 196)"><g><path d="M-62 -30 H62 Q76 -30 76 -16 V14 Q76 28 62 28 H10 L-6 52 L-14 28 H-62 Q-76 28 -76 14 V-16 Q-76 -30 -62 -30Z" fill="#fff" ${O}/><text x="0" y="10" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="30" fill="#c2410c">Frana!</text></g></g></svg>`
};
