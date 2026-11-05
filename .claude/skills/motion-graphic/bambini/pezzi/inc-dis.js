/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const ALBERO = (x, y, s = 1, c = "#40c057") => `<g transform="translate(${x} ${y}) scale(${s})" ${O}><rect x="-10" y="-60" width="20" height="60" fill="#a0703c"/><path d="M0 -190 L60 -60 H-60Z" fill="${c}"/><path d="M0 -150 L48 -90 H-48Z" fill="${c}"/></g>`;
const FIAMMA = (cls, x, y, s = 1) => `<g class="${cls}" transform="translate(${x} ${y}) scale(${s})"><g><g transform="translate(-50 -94)">${INTERNO("fuoco")}</g></g></g>`;
const FUMO = `<g class="fumo" fill="#adb5bd" stroke="${INK}" stroke-width="3">${[0, 1, 2, 3].map(i => `<circle data-i="${i}" r="22"/>`).join("")}</g>`;
const VENTO = `<g class="vento" fill="none" stroke="#74c0fc" stroke-width="6" stroke-linecap="round">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 0 h70 q20 0 20 -16 q0 -14 -14 -14"/>`).join("")}</g>`;
Object.assign(ICONE, {
  mozzicone: `<svg viewBox="0 0 100 100"><rect x="14" y="44" width="56" height="14" rx="4" fill="#fff" ${O}/><rect x="70" y="44" width="16" height="14" rx="3" fill="#ff922b" ${O}/><path d="M80 34 Q86 24 80 14 M90 34 Q96 24 90 14" fill="none" stroke="#adb5bd" stroke-width="5" stroke-linecap="round"/></svg>`,
  fiammifero: `<svg viewBox="0 0 100 100"><path d="M30 86 L64 30" stroke="#c08a4f" stroke-width="10" stroke-linecap="round"/><circle cx="66" cy="27" r="9" fill="#e03131" ${O}/><path d="M66 18 C76 8 70 -2 66 -2 C62 6 56 8 66 18Z" fill="#ff922b" ${O} transform="translate(0 4)"/></svg>`,
  falo: `<svg viewBox="0 0 100 100"><path d="M20 84 L80 70 M20 70 L80 84" stroke="#a0703c" stroke-width="10" stroke-linecap="round"/><path d="M50 18 C62 36 74 44 72 60 C70 74 60 80 50 80 C38 80 28 74 28 60 C28 48 38 42 40 30 C44 38 46 42 50 44 C52 34 50 26 50 18Z" fill="#ff922b" ${O}/></svg>`,
  ventoico: `<svg viewBox="0 0 100 100"><path d="M10 40 H64 Q80 40 80 26 Q80 14 68 14 M10 60 H76 Q90 60 90 74 Q90 86 78 86" fill="none" stroke="#4dabf7" stroke-width="9" stroke-linecap="round"/></svg>`
});
const ILL = {
  bosco: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${PRATO(430)}${ALBERO(90, 440, 1)}${ALBERO(200, 450, 1.25)}${ALBERO(520, 445, 1.1)}
    <g transform="translate(150 230)">${FUMO}</g>${PG("flavio")}</svg>`,
  cause: () => `<div class="tiles">${tile("mozzicone", "Un mozzicone")}${tile("fiammifero", "Un fiammifero")}${tile("falo", "Un fuoco lasciato acceso")}</div>`,
  cresce: () => `<svg ${S0}><rect width="600" height="510" fill="#fff3bf"/>${SOLE(480, 90, 44)}${PRATO(430, "#e9c46a")}
    ${Array.from({ length: 22 }, (_, i) => `<path d="M${20 + i * 27} 470 l-6 -26 M${26 + i * 27} 470 l6 -22" stroke="#c99a2e" stroke-width="5" stroke-linecap="round"/>`).join("")}
    <g transform="translate(60 230)">${VENTO}</g>${FIAMMA("f1", 220, 470, 1)}${FIAMMA("f2", 320, 470, 1)}${FIAMMA("f3", 420, 470, 1)}
    <g class="mesi"><g><rect x="-160" y="-30" width="320" height="60" rx="30" fill="#fff" ${O}/><text x="0" y="10" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="26" fill="#e8590c">da giugno a settembre</text></g></g></svg>`,
  area: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${PRATO(430)}${ALBERO(530, 440, 1)}
    <g ${O}><rect x="40" y="110" width="200" height="70" rx="10" fill="#40c057"/><path d="M90 180 V250 M190 180 V250" /></g>
    <text x="140" y="140" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="22" fill="#fff">AREA</text><text x="140" y="166" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="22" fill="#fff">ATTREZZATA</text>
    <g ${O}><rect x="200" y="380" width="110" height="60" rx="6" fill="#adb5bd"/><rect x="214" y="364" width="82" height="20" fill="#495057"/></g>${FIAMMA("fb", 255, 368, .45)}
    ${PG("papa", { tipo: "adulto", maglia: "#1c7ed6", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}
    <g class="nov"><g>${DIVIETO("", 0, 0, 52)}${ICOSVG("ventoico", 0, 0, .75)}<path d="M-34 34 L34 -34" stroke="#e03131" stroke-width="13" stroke-linecap="round"/></g></g></svg>`,
  vedi: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/><path d="M-10 300 Q150 200 330 260 V520 H-10Z" fill="#8ce99a" stroke="${INK}" stroke-width="5"/>
    ${ALBERO(80, 300, .6)}${ALBERO(150, 280, .7)}${ALBERO(230, 285, .6)}<g transform="translate(160 200)">${FUMO}</g>${FIAMMA("fv", 160, 280, .5)}${PRATO(450)}
    ${PG("mamma", { tipo: "adulta", maglia: "#40c057", pantaloni: "#495057", capelli: "#3b2412" })}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g>${PG("flavio")}
    <g class="fum"><g><rect x="-58" y="-28" width="116" height="56" rx="24" fill="#fff" ${O}/><text x="0" y="14" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="36" fill="#e03131">112</text></g></g></svg>`,
  solo: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(440)}${ALBERO(90, 440, .9)}
    ${PG("flavio")}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g>
    <g class="fum"><g><rect x="-58" y="-28" width="116" height="56" rx="24" fill="#fff" ${O}/><text x="0" y="14" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="36" fill="#e03131">112</text></g></g>
    <g class="dove"><g>${ICOSVG("pin", 0, 0, 1.1)}<rect x="-86" y="52" width="172" height="40" rx="20" fill="#fff" ${O}/><text x="0" y="80" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="22" fill="${INK}">dove sono</text></g></g></svg>`,
  fuga: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/><path d="M300 520 L300 300 Q440 160 620 170 V520Z" fill="#8ce99a" stroke="${INK}" stroke-width="5"/>
    ${FIAMMA("ff", 520, 250, .8)}${FIAMMA("ff2", 430, 290, .6)}
    <rect x="-10" y="400" width="320" height="60" fill="#adb5bd" stroke="${INK}" stroke-width="5"/><path d="M10 430 H290" stroke="#fff" stroke-width="6" stroke-dasharray="24 18"/>
    <path d="M-10 470 H330 V520 H-10Z" fill="#74c0fc" stroke="${INK}" stroke-width="4"/>
    <path class="si" d="M280 380 H80 M110 350 L80 380 L110 410" fill="none" stroke="#40c057" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    ${DIVIETO("nos", 380, 160, 40)}<path d="M350 250 L410 190" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
    ${PG("flavio")}</svg>`,
  spettacolo: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(440)}
    <path d="M300 440 Q420 400 610 410 V440Z" fill="#495057" stroke="${INK}" stroke-width="4"/>
    ${ALBERO(400, 430, .8, "#343a40")}${ALBERO(520, 430, .9, "#343a40")}<g ${O}><path d="M330 440 V380 M410 440 V380 M490 440 V380 M570 440 V380 M320 395 H600" fill="none" stroke="#c08a4f"/></g>
    ${DIVIETO("noz", 470, 250, 46)}${PG("flavio")}</svg>`,
  verde: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${SOLE(480, 100, 46)}${PRATO(430)}${ALBERO(80, 440, 1)}${ALBERO(530, 440, 1.1)}
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
