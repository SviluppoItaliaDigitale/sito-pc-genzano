/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const VOL = c => PG(c, { tipo: "adulta", maglia: "#ffd43b", pantaloni: "#1c4fa0", capelli: "#5c3d1e" });
const VOL2 = c => PG(c, { tipo: "adulto", maglia: "#ffd43b", pantaloni: "#1c4fa0", capelli: "#3b2412", pelle: "#c68642" });
const ILL = {
  gruppo: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(30, 30, .55)}${NUVOLA(420, 20, .5)}${PRATO(440)}
    ${VOL("v1")}${PG("p1", { tipo: "adulto", maglia: "#e03131", pantaloni: "#495057", capelli: "#3b2412" })}${PG("p2", { tipo: "adulta", maglia: "#4dabf7", pantaloni: "#495057", capelli: "#e8a33d" })}
    ${VOL2("v2")}${PG("flavio")}<g class="cuori">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 18 C-30 -6 -26 -30 -8 -30 C0 -30 0 -22 0 -22 C0 -22 0 -30 8 -30 C26 -30 30 -6 0 18Z" fill="#e03131" stroke="${INK}" stroke-width="4"/>`).join("")}</g></svg>`,
  chi: () => `<div class="tiles">${tile("comune", "Il Comune", "")}${tile("casco", "I Vigili del Fuoco", "")}${tile("ambulanza", "La sanità", "")}${tile("gilet", "I volontari", "")}</div>`,
  volontari: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 30, .5)}${PRATO(440)}
    <g ${O}><rect x="370" y="200" width="200" height="240" fill="#e9ecef"/><rect x="420" y="320" width="90" height="120" fill="#4dabf7"/><rect x="360" y="170" width="220" height="40" rx="8" fill="#1c4fa0"/></g>
    <text x="470" y="198" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="22" fill="#fff">PROTEZIONE CIVILE</text>
    ${VOL("v1")}<g class="scat"><rect x="-34" y="-26" width="68" height="52" rx="6" fill="#c08a4f" ${O}/><path d="M-34 -6 H34" ${O}/></g>${VOL2("v2")}
    <g class="radio"><rect x="-12" y="-24" width="24" height="48" rx="5" fill="#495057" ${O}/><path d="M6 -24 V-46" ${O}/></g></svg>`,
  catena: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(450, "#8ce99a")}
    ${[["persone", 90, "Tu"], ["telefono", 230, "112"], ["comune", 370, "Autorità"], ["gilet", 510, "Volontari"]].map(([n, x, l], j) =>
      `<g class="c${j}" transform="translate(${x} 240)"><g><circle r="62" fill="#fff" ${O}/>${ICOSVG(n, 0, -6, .8)}<text y="98" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="26" fill="${INK}">${l}</text></g></g>`).join("")}
    ${[0, 1, 2].map(j => `<g class="f${j}" transform="translate(${160 + j * 140} 240)"><path d="M-12 0 H12 M2 -12 L14 0 L2 12" stroke="#e8590c" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>`).join("")}</svg>`,
  entra: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${PRATO(440)}
    <g class="torta"><g><rect x="-70" y="-30" width="140" height="70" rx="12" fill="#ffc9c9" ${O}/><rect x="-60" y="-60" width="120" height="34" rx="10" fill="#fff" ${O}/>
      <text y="-34" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="28" fill="#e03131">16</text></g></g>
    ${PG("ragazzo", { tipo: "adulto", maglia: "#ff922b", pantaloni: "#4dabf7", capelli: "#8b5a2b" })}${VOL("v1")}
    <g class="lib">${ICOSVG("fumetto", 0, 0, .9)}</g></svg>`,
  parte: () => `<svg ${S0}><rect width="600" height="510" fill="#fff4d6"/><rect y="420" width="600" height="90" fill="#e9b872" stroke="${INK}" stroke-width="5"/>
    <g ${O}><rect x="170" y="80" width="260" height="190" rx="10" fill="#fff"/><path d="M200 120 H400 M200 160 H360 M200 200 H380" stroke="#ced4da" stroke-width="8"/></g>
    <text x="300" y="250" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="26" fill="${INK}">IL NOSTRO PIANO</text>
    ${PG("mamma", { tipo: "adulta", maglia: "#9775fa", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#40c057", pantaloni: "#f783ac", capelli: "#3b2412" })}
    ${STELLA("s1", 470, 110, 24)}${STELLA("s2", 120, 120, 18, "#ff922b")}</svg>`,
  sereno: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 50, .6)}${SOLE(500, 100, 46)}${PRATO(430)}
    ${VOL("v1")}${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
