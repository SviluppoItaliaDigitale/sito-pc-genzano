/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const TEL = (cls, x, y, s, schermo) => `<g class="${cls}" transform="translate(${x} ${y}) scale(${s})" ${O}><rect x="-80" y="-160" width="160" height="320" rx="26" fill="#495057"/>
  <rect x="-68" y="-128" width="136" height="246" rx="8" fill="#e7f5ff"/>${schermo}<circle cx="0" cy="138" r="9" fill="#868e96" stroke="none"/></g>`;
const ONDE = cls => `<g class="${cls}" fill="none" stroke="#4dabf7" stroke-width="7" stroke-linecap="round"><path d="M0 -26 a26 26 0 0 1 0 52"/><path d="M14 -46 a46 46 0 0 1 0 92"/></g>`;
const CUFFIA = `<path d="M-62 -10 a62 62 0 0 1 124 0" fill="none" stroke="${INK}" stroke-width="9"/><rect x="-74" y="-20" width="22" height="34" rx="8" fill="#495057" stroke="${INK}" stroke-width="4"/><path d="M-62 12 Q-60 46 -20 44" fill="none" stroke="${INK}" stroke-width="5"/><circle cx="-18" cy="44" r="6" fill="#495057"/>`;
const ILL = {
  numero: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(30, 40, .6)}${NUVOLA(420, 26, .5)}${PRATO(450)}
    ${TEL("tel", 250, 250, 1, `<text x="0" y="10" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="78" fill="#e03131" stroke="${INK}" stroke-width="3">112</text>
      <rect x="-44" y="54" width="88" height="40" rx="20" fill="#40c057"/><path d="M-12 74 q12 -14 24 0" stroke="#fff" stroke-width="5" fill="none"/>`)}
    <g class="onde1" transform="translate(340 170)">${ONDE("o1")}</g>${PG("flavio")}</svg>`,
  quando: () => `<div class="tiles">${tile("malore", "Qualcuno sta male", "")}${tile("fuoco", "Fuoco o fumo", "")}${tile("incidente", "Un incidente", "")}${tile("pericolo", "Un pericolo serio", "")}</div>`,
  dire: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(380, 30, .5)}${PRATO(450)}
    <g class="fum"><g><rect x="-150" y="-80" width="300" height="150" rx="34" fill="#fff" ${O}/><path d="M-40 66 L-70 110 L0 68" fill="#fff" ${O}/>
      ${["persone", "pin", "fumetto", "cerotto"].map((n, j) => `<g class="d${j}" transform="translate(${-105 + j * 70} -5)"><g>${ICOSVG(n, 0, 0, .58)}</g></g>`).join("")}</g></g>
    ${PG("flavio")}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g></svg>`,
  calma: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(450, "#8ce99a")}
    <path class="filo" d="M170 220 Q300 120 430 220" fill="none" stroke="#4dabf7" stroke-width="8" stroke-dasharray="4 18" stroke-linecap="round"/>
    ${PG("flavio")}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g>
    ${PG("op", { tipo: "adulto", maglia: "#4263eb", pantaloni: "#495057", capelli: "#3b2412" })}<g class="cuffia">${CUFFIA}</g>
    <g class="ok"><g><rect x="-58" y="-26" width="116" height="52" rx="26" fill="#fff" ${O}/><text x="0" y="12" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="30" fill="${INK}">OK!</text></g></g></svg>`,
  insieme: () => `<svg ${S0}><rect width="600" height="510" fill="#fff4d6"/><rect y="420" width="600" height="90" fill="#e9b872" stroke="${INK}" stroke-width="5"/>
    <rect x="40" y="70" width="130" height="110" rx="8" fill="#a5d8ff" ${O}/><path d="M105 70 V180 M40 125 H170" ${O}/>
    ${PG("mamma", { tipo: "adulta", maglia: "#9775fa", pantaloni: "#495057", capelli: "#3b2412" })}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g>
    ${PG("flavio")}${STELLA("s1", 470, 120, 22)}${STELLA("s2", 520, 170, 16, "#ff922b")}</svg>`,
  scherzo: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 40, .55)}${PRATO(450)}
    ${TEL("tel", 200, 260, .9, `<text x="0" y="0" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="64" fill="#e03131">112</text>
      <text x="0" y="60" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="40" fill="${INK}">AH AH!</text>`)}
    ${DIVIETO("no", 200, 250, 110)}
    <g class="fila">${["#ffd8b1", "#f1c27d", "#c68642"].map((p, i) => PG("att" + i, { pelle: p, maglia: ["#40c057", "#ff922b", "#9775fa"][i], tipo: i === 1 ? "adulta" : "adulto", capelli: "#3b2412" })).join("")}</g>
    <g class="orologio">${ICOSVG("orologio", 470, 120, .9)}</g></svg>`,
  sereno: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 50, .6)}${SOLE(470, 110, 50)}
    <g class="cartello"><g ${O}><rect x="-8" y="0" width="16" height="190" fill="#868e96"/><rect x="-120" y="-80" width="240" height="110" rx="20" fill="#fff"/>
      <text x="0" y="0" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="84" fill="#e03131" stroke="${INK}" stroke-width="3">112</text></g></g>
    ${PRATO(430)}${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
