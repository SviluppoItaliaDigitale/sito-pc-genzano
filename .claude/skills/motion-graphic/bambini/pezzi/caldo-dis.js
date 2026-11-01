/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const TERMO = `<g ${O}><rect x="-16" y="-110" width="32" height="140" rx="16" fill="#fff"/><circle cy="40" r="28" fill="#e03131"/><rect class="liv" x="-8" y="-60" width="16" height="100" rx="8" fill="#e03131" stroke="none"/></g>`;
const ILL = {
  sole: () => `<svg ${S0}><rect width="600" height="510" fill="#fff3bf"/>${SOLE(300, 150, 70)}${PRATO(440, "#c0eb75")}
    <g class="termo" transform="translate(500 330)">${TERMO}</g>${PG("flavio")}<g class="goccia"><path d="M0 -14 C8 -2 10 4 10 8 a10 10 0 0 1 -20 0 C-10 4 -8 -2 0 -14Z" fill="#74c0fc" stroke="${INK}" stroke-width="3"/></g></svg>`,
  acqua: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${NUVOLA(400, 30, .5)}${PRATO(440)}
    <g class="borr">${ICOSVG("borraccia", 0, 0, 1.3)}</g><g class="gocce">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 -14 C8 -2 10 4 10 8 a10 10 0 0 1 -20 0 C-10 4 -8 -2 0 -14Z" fill="#74c0fc" stroke="${INK}" stroke-width="3"/>`).join("")}</g>
    ${PG("flavio")}</svg>`,
  ore: () => `<svg ${S0}><rect width="600" height="510" fill="#fff3bf"/>${SOLE(470, 90, 44)}${PRATO(440, "#c0eb75")}
    <g transform="translate(150 200)"><circle r="96" fill="#fff" ${O}/>${Array.from({ length: 12 }, (_, i) => `<path d="M0 -84 V-72" ${O} transform="rotate(${i * 30})"/>`).join("")}
      <path d="M0 0 L${(Math.sin(11 / 12 * 2 * Math.PI) * 84).toFixed(1)} ${(-Math.cos(11 / 12 * 2 * Math.PI) * 84).toFixed(1)} A84 84 0 0 1 ${(Math.sin(6 / 12 * 2 * Math.PI) * 84).toFixed(1)} ${(-Math.cos(6 / 12 * 2 * Math.PI) * 84).toFixed(1)}Z" fill="#ff922b" opacity=".45"/>
      <g class="lancetta"><path d="M0 0 V-62" stroke="${INK}" stroke-width="8" stroke-linecap="round"/></g><circle r="8" fill="${INK}"/></g>
    ${ICOSVG("ombra", 420, 330, 2.4)}${PG("flavio")}</svg>`,
  vestiti: () => `<svg ${S0}><rect width="600" height="510" fill="#fff3bf"/>${SOLE(500, 80, 40)}${PRATO(440, "#c0eb75")}
    ${PG("flavio", { maglia: "#fff", pantaloni: "#a5d8ff" })}<g class="capp">${ICOSVG("cappello", 0, 0, .9)}</g>
    <g class="occh"><path d="M-40 0 H40" stroke="${INK}" stroke-width="5"/><circle cx="-20" r="14" fill="#343a40" stroke="${INK}" stroke-width="4"/><circle cx="20" r="14" fill="#343a40" stroke="${INK}" stroke-width="4"/></g>
    <g class="frut"><g>${ICOSVG("frutta", 470, 370, 1.1)}</g></g></svg>`,
  auto: () => `<svg ${S0}><rect width="600" height="510" fill="#fff3bf"/>${SOLE(470, 90, 44)}<rect y="400" width="600" height="110" fill="#adb5bd" ${O}/>
    ${ICOSVG("auto", 250, 300, 3.6)}${DIVIETO("no", 250, 260, 90)}<g class="onde" fill="none" stroke="#ff922b" stroke-width="6" stroke-linecap="round">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 0 q10 -12 0 -24 t0 -24"/>`).join("")}</g></svg>`,
  vicini: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(440)}
    <g ${O}><rect x="330" y="150" width="240" height="290" fill="#ffe066"/><rect x="400" y="300" width="90" height="140" rx="8" fill="#4dabf7"/><circle cx="472" cy="372" r="5" fill="${INK}"/></g>
    ${PG("nonna", { tipo: "adulta", maglia: "#b197fc", pantaloni: "#868e96", capelli: "#dee2e6" })}${PG("mamma", { tipo: "adulta", maglia: "#40c057", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}
    <g class="cuore"><path d="M0 18 C-30 -6 -26 -30 -8 -30 C0 -30 0 -22 0 -22 C0 -22 0 -30 8 -30 C26 -30 30 -6 0 18Z" fill="#e03131" stroke="${INK}" stroke-width="4" transform="scale(1.4)"/></g></svg>`,
  malore: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(440)}${ICOSVG("ombra", 170, 300, 3.2)}
    ${PG("mamma", { tipo: "adulta", maglia: "#40c057", pantaloni: "#495057", capelli: "#3b2412" })}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g>${PG("flavio")}
    <g class="fum"><g><rect x="-58" y="-28" width="116" height="56" rx="24" fill="#fff" ${O}/><text x="0" y="14" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="36" fill="#e03131">112</text></g></g></svg>`,
  sereno: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 50, .6)}${SOLE(470, 110, 50)}${PRATO(430)}${ICOSVG("ombra", 150, 330, 2.6)}
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
