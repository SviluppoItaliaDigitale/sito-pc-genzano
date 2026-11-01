/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const OG = {
  bottiglia: `<g ${O}><rect x="-8" y="-62" width="16" height="12" rx="3" fill="#495057"/><path d="M-22 -50 h44 v100 q0 10 -10 10 h-24 q-10 0 -10 -10Z" fill="#a5d8ff"/><path d="M-22 -10 H22" /></g>`,
  scatola: `<g ${O}><rect x="-34" y="-30" width="68" height="60" rx="8" fill="#ff8787"/><ellipse cx="0" cy="-30" rx="34" ry="9" fill="#dee2e6"/><rect x="-34" y="-6" width="68" height="20" fill="#fff"/></g>`,
  apri: `<g ${O}><rect x="-50" y="-8" width="70" height="16" rx="8" fill="#868e96"/><circle cx="34" cy="0" r="16" fill="#ced4da"/><path d="M26 -8 L44 8" /></g>`,
  torcia: `<g ${O}><rect x="-50" y="-16" width="70" height="32" rx="8" fill="#4263eb"/><path d="M20 -24 L44 -32 V32 L20 24Z" fill="#ced4da"/></g>`,
  radio: `<g ${O}><rect x="-50" y="-34" width="100" height="68" rx="12" fill="#ff922b"/><circle cx="-18" cy="0" r="20" fill="#495057"/><rect x="12" y="-14" width="28" height="10" rx="3" fill="#fff"/><path d="M30 -34 L50 -66"/></g>`,
  pile: `<g ${O}><rect x="-26" y="-12" width="22" height="40" rx="5" fill="#40c057"/><rect x="4" y="-12" width="22" height="40" rx="5" fill="#40c057"/><rect x="-20" y="-18" width="10" height="6" fill="#adb5bd"/><rect x="10" y="-18" width="10" height="6" fill="#adb5bd"/></g>`,
  soccorso: `<g ${O}><rect x="-46" y="-36" width="92" height="72" rx="12" fill="#4dabf7"/><path d="M-14 -40 V-48 H14 V-40" fill="none"/><path d="M0 -20 V20 M-20 0 H20" stroke="#fff" stroke-width="12" stroke-linecap="round"/></g>`,
  medicine: `<g ${O}><rect x="-22" y="-30" width="44" height="12" rx="3" fill="#fff"/><rect x="-20" y="-18" width="40" height="52" rx="8" fill="#ffd43b"/><rect x="-20" y="-2" width="40" height="18" fill="#fff"/></g>`,
  busta: `<g ${O}><rect x="-48" y="-36" width="96" height="72" rx="8" fill="#e7f5ff" opacity=".9"/><rect x="-36" y="-24" width="60" height="44" fill="#fff"/><path d="M-28 -12 H14 M-28 0 H6 M-28 12 H14"/></g>`,
  soldi: `<g ${O}><rect x="-44" y="-24" width="88" height="48" rx="6" fill="#b2f2bb"/><circle r="14" fill="#69db7c"/><text x="0" y="7" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="20" fill="${INK}" stroke="none">€</text></g>`,
  carica: `<g ${O}><rect x="-36" y="-22" width="40" height="44" rx="8" fill="#f8f9fa"/><path d="M-26 -22 V-36 M-14 -22 V-36"/><path d="M4 0 Q40 0 40 30 Q40 50 60 50" fill="none"/></g>`,
  fischietto: `<g ${O}><path d="M-46 -12 H10 A26 26 0 1 1 -10 22 H-46Z" fill="#e03131"/><circle cx="18" cy="12" r="8" fill="#fff"/></g>`,
  maglia: `<g ${O}><path d="M-40 -30 L-16 -40 Q0 -30 16 -40 L40 -30 L52 -6 L34 0 V40 H-34 V0 L-52 -6Z" fill="#9775fa"/></g>`,
  coperta: `<g ${O}><rect x="-50" y="-26" width="100" height="52" rx="26" fill="#ffa8a8"/><path d="M-30 -26 V26 M0 -26 V26 M30 -26 V26" stroke="#fff" stroke-width="5"/></g>`,
  ciotola: `<g ${O}><path d="M-40 -6 H40 L30 22 H-30Z" fill="#4dabf7"/><circle cx="-12" cy="-12" r="9" fill="#c08a4f"/><circle cx="6" cy="-14" r="9" fill="#c08a4f"/><circle cx="22" cy="-10" r="8" fill="#c08a4f"/></g>`
};
const POSTI = [[140, 160], [160, 335], [310, 210], [320, 360]];
const KIT = (nomi, extra = "") => `<svg ${S0}><rect width="600" height="510" fill="#fff4d6"/>${STANZA}${extra}
  ${nomi.map((n, i) => `<g class="og" data-i="${i}" data-x="${POSTI[i][0]}" data-y="${POSTI[i][1]}" transform="translate(${POSTI[i][0]} ${POSTI[i][1]})"><g>${OG[n]}</g></g>`).join("")}
  <g class="zb" transform="translate(470 330)"><g>${INTERNO("zaino").replace(/^/, `<g transform="scale(2.4) translate(-50 -50)">`)}</g></g></g></svg>`;
const ONDE = `<g class="suono" fill="none" stroke="#ff922b" stroke-width="6" stroke-linecap="round">${[0, 1, 2].map(i => `<path data-i="${i}" d="M0 -20 Q14 0 0 20"/>`).join("")}</g>`;
const ILL = {
  zaino: () => `<svg ${S0}><rect width="600" height="510" fill="#fff4d6"/>${STANZA}
    <g class="zb" transform="translate(220 310)"><g><g transform="scale(2.8) translate(-50 -50)">${INTERNO("zaino")}</g></g></g>
    <g class="tre"><g><circle r="58" fill="#fff" ${O}/><text x="0" y="-2" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="48" fill="#e8590c" stroke="${INK}" stroke-width="2">3</text><text x="0" y="28" text-anchor="middle" font-family="Titillium Web" font-weight="800" font-size="20" fill="${INK}">giorni</text></g></g>
    ${PG("flavio")}</svg>`,
  cibo: () => KIT(["bottiglia", "scatola", "apri"]),
  luce: () => KIT(["torcia", "radio", "pile"], `<path class="raggio" d="M215 150 L330 50 L370 125Z" fill="#ffe066" opacity=".6"/>`),
  cura: () => KIT(["soccorso", "medicine"]),
  documenti: () => KIT(["busta", "soldi"]),
  suoni: () => KIT(["carica", "fischietto"], `<g transform="translate(250 335)">${ONDE}</g>`),
  vestiti: () => KIT(["maglia", "coperta", "ciotola"]),
  porta: () => `<svg ${S0}><rect width="600" height="510" fill="#fff4d6"/>${STANZA}
    <g ${O}><rect x="60" y="120" width="150" height="300" rx="6" fill="#c08a4f"/><circle cx="185" cy="280" r="9" fill="#ffd43b"/></g>
    <g transform="translate(270 360)"><g transform="scale(1.6) translate(-50 -50)">${INTERNO("zaino")}</g></g>
    <g class="cal"><g>${ICOSVG("calendario", 0, 0, 1.2)}<text x="0" y="70" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="24" fill="${INK}">ogni 6 mesi</text></g></g>
    ${PG("mamma", { tipo: "adulta", maglia: "#40c057", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}</svg>`
};
