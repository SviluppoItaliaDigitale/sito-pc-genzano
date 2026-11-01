/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const COLLI = (zz = "") => `<path d="M-10 330 Q120 150 300 120 Q480 150 610 330 V520 H-10Z" fill="#8ce99a" ${O}/>
  <ellipse cx="210" cy="250" rx="62" ry="22" fill="#4dabf7" ${O}/><ellipse cx="380" cy="268" rx="48" ry="17" fill="#4dabf7" ${O}/>
  <g fill="#c9d4e2" ${O}>${[[120, 360], [175, 390], [450, 372], [500, 398]].map(([x, y]) => `<rect x="${x}" y="${y}" width="40" height="34"/><path d="M${x - 4} ${y} L${x + 20} ${y - 18} L${x + 44} ${y}Z" fill="#fa5252"/>`).join("")}</g>${zz}`;
const ZZ = `<g class="zz" font-family="Titillium Web" font-weight="900" fill="#4263eb" stroke="${INK}" stroke-width="2"><text class="z0" font-size="40">Z</text><text class="z1" font-size="30">Z</text><text class="z2" font-size="22">Z</text></g>`;
const ILL = {
  vulcano: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(30, 30, .55)}${NUVOLA(420, 20, .5)}${COLLI(ZZ)}
    <text x="210" y="300" text-anchor="middle" font-family="Titillium Web" font-weight="800" font-size="20" fill="${INK}">Albano</text>
    <text x="380" y="312" text-anchor="middle" font-family="Titillium Web" font-weight="800" font-size="20" fill="${INK}">Nemi</text>${PG("flavio")}</svg>`,
  dorme: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${COLLI(ZZ)}
    <g class="tempo"><g><rect x="-150" y="-50" width="300" height="100" rx="26" fill="#fff" ${O}/>
      <text x="0" y="-6" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="44" fill="#e8590c" stroke="${INK}" stroke-width="2">36.000</text>
      <text x="0" y="30" text-anchor="middle" font-family="Titillium Web" font-weight="800" font-size="24" fill="${INK}">anni fa, circa</text></g></g></svg>`,
  sorveglia: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${COLLI()}
    <g class="sat" ${O}><rect x="-24" y="-18" width="48" height="36" rx="6" fill="#ced4da"/><rect x="-80" y="-12" width="50" height="24" fill="#4dabf7"/><rect x="30" y="-12" width="50" height="24" fill="#4dabf7"/></g>
    ${ICOSVG("gps", 140, 190, .9)}<g class="seg" fill="none" stroke="#e8590c" stroke-width="5" stroke-dasharray="10 12" stroke-linecap="round"><path d="M150 140 L300 70"/><path d="M455 200 L330 80"/></g>
    <g ${O}><rect x="420" y="190" width="70" height="70" rx="12" fill="#fff"/><path class="ago" d="M455 245 L455 210" stroke="#e03131" stroke-width="6"/></g>
    <text x="455" y="282" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="22" fill="${INK}">GAS</text>
    ${PG("ricerc", { tipo: "adulto", maglia: "#fff", pantaloni: "#495057", capelli: "#5c3d1e" })}</svg>`,
  gas: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${PRATO(210, "#8ce99a")}
    <rect x="60" y="230" width="480" height="280" fill="#c9a27a" ${O}/>
    <rect x="120" y="270" width="360" height="220" rx="10" fill="#e9d5bf" ${O}/>
    <path d="M140 270 L210 270 L160 340 M230 270 H300" fill="none" ${O}/>
    <rect class="co2" x="124" y="420" width="352" height="66" fill="#74c0fc" opacity=".55"/>
    <g class="bolle">${Array.from({ length: 9 }, (_, i) => `<circle data-i="${i}" r="${6 + (i % 3) * 3}" fill="#a5d8ff" stroke="${INK}" stroke-width="3"/>`).join("")}</g>
    <text x="300" y="462" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="34" fill="${INK}">CO₂</text>
    ${PG("flavio")}</svg>`,
  aria: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(380, 30, .5)}${PRATO(440)}
    <g ${O}><rect x="40" y="170" width="260" height="270" fill="#e9d5bf"/><path d="M30 176 L170 90 L310 176Z" fill="#fa5252"/>
      <rect class="porta" x="120" y="300" width="90" height="140" fill="#5c3d1e"/></g>
    <g class="vento" fill="none" stroke="#4dabf7" stroke-width="7" stroke-linecap="round">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 0 q20 -14 40 0 t40 0"/>`).join("")}</g>
    ${ICOSVG("pozzo", 470, 360, 1.2)}${DIVIETO("np", 470, 360, 62)}${PG("flavio")}</svg>`,
  soccorso: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(380, 30, .5)}${PRATO(440)}
    <g ${O}><rect x="30" y="200" width="210" height="240" fill="#c9a27a"/><rect x="80" y="300" width="110" height="140" fill="#343a40"/></g>
    ${DIVIETO("np", 135, 360, 62)}
    <g class="vvf">${ICOSVG("casco", 470, 140, .9)}</g>
    ${PG("flavio")}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g>
    <g class="fum"><g><rect x="-58" y="-28" width="116" height="56" rx="24" fill="#fff" ${O}/><text x="0" y="14" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="36" fill="#e03131">112</text></g></g></svg>`,
  sereno: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 40, .6)}${SOLE(500, 90, 44)}${COLLI()}
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
