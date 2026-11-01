/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const PIOGGIA = (n = 26, x0 = 0, x1 = 600, y0 = 0, y1 = 440) => `<g class="pioggia" stroke="#4dabf7" stroke-width="5" stroke-linecap="round" data-y0="${y0}" data-y1="${y1}">${Array.from({ length: n }, (_, i) =>
  `<path data-i="${i}" data-x="${(x0 + hash(i + 31) * (x1 - x0)).toFixed(0)}" d="M0 0 l-8 22"/>`).join("")}</g>`;
const NERA = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})"><path d="M0 40 Q-4 10 26 12 Q34 -14 64 -4 Q84 -22 106 0 Q132 2 128 30 Q140 44 120 52 H8 Q-10 52 0 40Z" fill="#adb5bd" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/></g>`;
const OMBRELLO = `<g class="ombr" stroke="${INK}" stroke-width="5" stroke-linejoin="round"><path d="M0 0 V110 q0 16 -16 16" fill="none"/><path d="M-90 0 Q-90 -70 0 -74 Q90 -70 90 0 Q68 -16 45 0 Q22 -16 0 0 Q-22 -16 -45 0 Q-68 -16 -90 0Z" fill="#e03131"/></g>`;
const ONDA = (cls, y, c = "#74c0fc") => `<path class="${cls}" d="M-20 ${y} Q40 ${y - 14} 100 ${y} T220 ${y} T340 ${y} T460 ${y} T580 ${y} T700 ${y} V560 H-20Z" fill="${c}" opacity=".85" stroke="${INK}" stroke-width="4"/>`;
Object.assign(ICONE, {
  sottopasso: `<svg viewBox="0 0 100 100"><path d="M6 30 H94 V40 H6Z" fill="#adb5bd" ${O}/><path d="M6 40 Q50 96 94 40" fill="none" ${O}/><path d="M24 62 Q50 84 76 62Z" fill="#74c0fc" stroke="none"/><path d="M6 40 Q50 96 94 40" fill="none" ${O}/></svg>`
});
const ILL = {
  pioggia: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NERA(60, 20, .9)}${NERA(330, 40, 1)}${PIOGGIA()}${PRATO(440, "#8ce99a")}
    <ellipse cx="420" cy="470" rx="90" ry="14" fill="#74c0fc" stroke="${INK}" stroke-width="4"/>${PG("flavio", { maglia: "#ffd43b" })}<g class="om">${OMBRELLO}</g></svg>`,
  sale: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NERA(380, 20, .8)}${PIOGGIA(18, 300, 600, 0, 300)}
    <g ${O}><path d="M120 470 V220 L260 120 L400 220 V470Z" fill="#ffe066"/><rect x="230" y="370" width="60" height="100" rx="6" fill="#c08a4f"/><rect x="160" y="250" width="60" height="56" fill="#a5d8ff"/><rect x="300" y="250" width="60" height="56" fill="#a5d8ff"/></g>
    <g class="acq">${ONDA("ond", 0)}</g>
    <g class="metro" ${O}><rect x="470" y="200" width="40" height="270" rx="8" fill="#fff"/>${[0, 1, 2, 3, 4].map(i => `<path d="M470 ${440 - i * 54} H490"/>`).join("")}</g>
    <g class="orol">${ICOSVG("orologio", 520, 110, .9)}</g></svg>`,
  pericoli: () => `<div class="tiles">${tile("cantina", "Cantine e garage")}${tile("sottopasso", "Sottopassi")}${tile("fosso", "Fossi e torrenti")}${tile("pericolo", "Zone basse")}</div>`,
  prima: () => `<svg ${S0}><rect width="600" height="510" fill="#fff4d6"/>${STANZA}
    <g ${O}><rect x="110" y="120" width="160" height="110" rx="12" fill="#495057"/><rect x="122" y="132" width="136" height="74" rx="4" fill="#fff"/></g>
    <rect class="barra" x="122" y="132" width="136" height="26" fill="#ffd43b" stroke="${INK}" stroke-width="3"/><text x="190" y="190" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="22" fill="${INK}">ALLERTA</text>
    ${PG("mamma", { tipo: "adulta", maglia: "#40c057", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}<g class="zai">${ICOSVG("zaino", 0, 0, 1.2)}</g></svg>`,
  sali: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>
    <g ${O}><rect x="90" y="60" width="360" height="420" fill="#ffe066"/><path d="M90 200 H450 M90 340 H450" /><rect x="90" y="340" width="360" height="140" fill="#c08a4f"/></g>
    <text x="270" y="420" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="30" fill="#fff" stroke="${INK}" stroke-width="2">CANTINA</text>
    <g class="acq">${ONDA("ond", 0)}</g>${DIVIETO("no", 400, 410, 36)}
    <g ${O} fill="#fff"><path d="M330 330 h40 v-40 h40 v-40 h40" fill="none"/></g>
    <path class="frec" d="M500 330 V120 M470 160 L500 120 L530 160" fill="none" stroke="#40c057" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    ${PG("flavio")}</svg>`,
  fuori: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NERA(40, 10, .7)}
    <path d="M330 520 L330 260 Q470 140 620 150 V520Z" fill="#8ce99a" stroke="${INK}" stroke-width="5"/>
    <g class="acq">${ONDA("ond", 0)}</g><g class="corr" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 0 h50 l-14 -12 m14 12 l-14 12"/>`).join("")}</g>
    ${STELLA("st", 530, 120, 26)}${PG("flavio")}</svg>`,
  auto: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NERA(380, 10, .8)}${PIOGGIA(14, 300, 600, 0, 300)}
    <path d="M-10 240 H140 Q300 470 460 240 H610 V520 H-10Z" fill="#adb5bd" stroke="${INK}" stroke-width="5"/>
    <path d="M182 300 Q300 470 418 300Z" fill="#74c0fc" opacity=".9" stroke="${INK}" stroke-width="4"/>
    <g class="mac">${ICOSVG("auto", 0, 0, 1.6)}</g>${DIVIETO("no", 300, 150, 60)}</svg>`,
  dopo: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(330, "#8ce99a")}
    <ellipse cx="300" cy="430" rx="230" ry="50" fill="#a0703c" stroke="${INK}" stroke-width="5"/><ellipse cx="300" cy="430" rx="190" ry="36" fill="#74c0fc" opacity=".85"/>
    <g class="tomb"><ellipse cx="330" cy="436" rx="40" ry="12" fill="none" stroke="${INK}" stroke-width="5" stroke-dasharray="10 8"/><text x="330" y="400" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="40" fill="#e03131" stroke="${INK}" stroke-width="2">?</text></g>
    ${PG("flavio")}${DIVIETO("no", 470, 300, 38)}</svg>`,
  arcobaleno: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>
    <g class="arco" fill="none" stroke-width="20">${["#e03131", "#ff922b", "#ffd43b", "#40c057", "#4dabf7"].map((c, i) => `<path d="M60 430 A240 240 0 0 1 540 430" stroke="${c}" transform="translate(${i * 20} ${i * 20}) scale(${(1 - i * .083).toFixed(3)} ${(1 - i * .083).toFixed(3)})"/>`).join("")}</g>
    ${SOLE(480, 100, 46)}${PRATO(430)}${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
