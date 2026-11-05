/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const LIV = { verde: ["#40c057", "VERDE"], gialla: ["#ffd43b", "GIALLA"], arancione: ["#ff922b", "ARANCIONE"], rossa: ["#e03131", "ROSSA"] };
const PIOGGIA = (n = 26, x0 = 0, x1 = 600, y0 = 0, y1 = 440) => `<g class="pioggia" stroke="#4dabf7" stroke-width="5" stroke-linecap="round" data-y0="${y0}" data-y1="${y1}">${Array.from({ length: n }, (_, i) =>
  `<path data-i="${i}" data-x="${(x0 + hash(i + 31) * (x1 - x0)).toFixed(0)}" d="M0 0 l-8 22"/>`).join("")}</g>`;
const NERA = (x, y, s = 1, c = "#adb5bd") => `<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 40 Q-4 10 26 12 Q34 -14 64 -4 Q84 -22 106 0 Q132 2 128 30 Q140 44 120 52 H8 Q-10 52 0 40Z" fill="${c}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/></g>`;
const FASCIA = k => `<rect x="0" y="0" width="600" height="64" fill="${LIV[k][0]}" stroke="${INK}" stroke-width="5"/><text x="300" y="45" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="38" fill="${INK}">${LIV[k][1]}</text>`;
const CASETTA = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})" ${O}><path d="M0 0 V-130 L90 -200 L180 -130 V0Z" fill="#ffe066"/><rect x="20" y="-115" width="54" height="46" fill="#a5d8ff"/><rect x="106" y="-115" width="54" height="46" fill="#a5d8ff"/><rect x="66" y="-60" width="48" height="60" rx="4" fill="#c08a4f"/></g>`;
const FULMINE = `<path class="fulm" d="M0 0 L-24 54 H-4 L-18 104 L26 38 H6 L20 0Z" fill="#ffd43b" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`;
const ILL = {
  semaforo: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(440)}
    <g ${O}><rect x="80" y="40" width="150" height="400" rx="40" fill="#495057"/><path d="M155 440 V470" /></g>
    ${["verde", "gialla", "arancione", "rossa"].map((k, i) => `<g class="lamp" data-i="${i}" transform="translate(155 ${375 - i * 92})"><g><circle r="38" fill="${LIV[k][0]}" stroke="${INK}" stroke-width="5"/></g></g>`).join("")}
    ${PG("flavio")}</svg>`,
  zone: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>
    <g ${O}><path d="M120 120 Q220 40 330 90 Q440 60 500 170 Q560 280 470 360 Q380 460 260 420 Q130 400 100 300 Q60 200 120 120Z" fill="#fff"/>
      <path d="M330 90 Q300 220 260 420 M100 300 Q260 260 470 360 M120 120 Q260 180 500 170" fill="none"/></g>
    <g class="pz"><path d="M265 395 Q300 290 330 260 Q420 300 455 350 Q380 430 265 395Z" fill="#ffd43b" opacity=".85" stroke="${INK}" stroke-width="4"/></g>
    <g class="pin">${ICOSVG("pin", 0, 0, .9)}</g><text class="fz" x="330" y="378" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="34" fill="${INK}">F</text>
    <g class="fog"><g><rect x="-60" y="-74" width="120" height="148" rx="10" fill="#fff" ${O}/><path d="M-40 -40 H40 M-40 -14 H40 M-40 12 H24" ${O}/><circle cx="-24" cy="44" r="12" fill="#40c057" ${O}/><circle cx="4" cy="44" r="12" fill="#ffd43b" ${O}/><circle cx="32" cy="44" r="12" fill="#e03131" ${O}/></g></g></svg>`,
  verde: () => `<svg ${S0}><rect width="600" height="510" fill="#ebfbee"/>${SOLE(470, 150, 44)}${PRATO(440)}${FASCIA("verde")}
    ${PG("flavio", { maglia: "#ff922b" })}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g></svg>`,
  gialla: () => `<svg ${S0}><rect width="600" height="510" fill="#fff9db"/>${NERA(60, 90, .8, "#ced4da")}${NERA(330, 100, .9, "#ced4da")}${PIOGGIA(14, 40, 560, 140, 430)}${PRATO(440, "#8ce99a")}
    ${ICOSVG("fosso", 440, 400, 1.6)}${DIVIETO("no", 440, 290, 38)}${FASCIA("gialla")}${PG("flavio")}</svg>`,
  arancione: () => `<svg ${S0}><rect width="600" height="510" fill="#fff4e6"/>${NERA(30, 80, 1, "#868e96")}${NERA(320, 90, 1.1, "#868e96")}${PIOGGIA(26, 0, 600, 140, 440)}${PRATO(440, "#8ce99a")}
    ${CASETTA(70, 450, 1.3)}${FASCIA("arancione")}${PG("flavio")}<g class="zai">${ICOSVG("zaino", 0, 0, 1.2)}</g></svg>`,
  rossa: () => `<svg ${S0}><rect width="600" height="510" fill="#ffe3e3"/>${NERA(10, 70, 1.1, "#495057")}${NERA(330, 80, 1.2, "#495057")}${PIOGGIA(38, 0, 600, 140, 450)}
    <g class="fl" transform="translate(300 150)"><g>${FULMINE}</g></g>${PRATO(440, "#8ce99a")}${CASETTA(200, 450, 1.1)}
    <g ${O}><rect x="230" y="302" width="58" height="50" fill="#fff4d6"/></g>${FASCIA("rossa")}<g class="vis"><circle cx="259" cy="330" r="16" fill="#ffd8b1" stroke="${INK}" stroke-width="4"/><path d="M251 330 h4 M263 330 h4" stroke="${INK}" stroke-width="4"/></g></svg>`,
  sito: () => `<svg ${S0}><rect width="600" height="510" fill="#fff4d6"/>${STANZA}
    <g ${O}><rect x="200" y="200" width="200" height="130" rx="10" fill="#495057"/><rect x="212" y="212" width="176" height="106" rx="4" fill="#fff"/><path d="M170 340 H430 L410 360 H190Z" fill="#adb5bd"/></g>
    <rect x="212" y="212" width="176" height="24" fill="#1c4fa0" stroke="none"/><rect class="barra" x="212" y="236" width="176" height="26" fill="#40c057" stroke="${INK}" stroke-width="3"/>
    <path d="M226 282 H330 M226 300 H300" stroke="#adb5bd" stroke-width="7" stroke-linecap="round"/>
    ${PG("mamma", { tipo: "adulta", maglia: "#40c057", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`,
  fine: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${SOLE(470, 100, 46)}${PRATO(430)}
    ${["verde", "gialla", "arancione", "rossa"].map((k, i) => `<g class="pal" data-i="${i}" transform="translate(${120 + i * 70} 160)"><g><circle r="26" fill="${LIV[k][0]}" stroke="${INK}" stroke-width="5"/></g></g>`).join("")}
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
