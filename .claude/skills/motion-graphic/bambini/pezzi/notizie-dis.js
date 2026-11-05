/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const CROCE = (cls, x, y, r = 34) => `<g class="${cls}" transform="translate(${x} ${y})"><g><circle r="${r}" fill="#e03131" stroke="${INK}" stroke-width="5"/><path d="M${-r * .38} ${-r * .38} L${r * .38} ${r * .38} M${r * .38} ${-r * .38} L${-r * .38} ${r * .38}" stroke="#fff" stroke-width="${r * .24}" stroke-linecap="round"/></g></g>`;
const BOLLA = (x, y, w, c, i, cls = "bolla") => `<g transform="translate(${x} ${y})"><g class="${cls}" data-i="${i}"><rect width="${w}" height="54" rx="18" fill="${c}" ${O}/>
  <rect x="16" y="15" width="${w - 52}" height="8" rx="4" fill="${INK}" opacity=".45"/><rect x="16" y="31" width="${w - 84}" height="8" rx="4" fill="${INK}" opacity=".3"/></g></g>`;
const TELEFONO = (x, y, w, h, dentro = "") => `<g transform="translate(${x} ${y})" ${O}><rect width="${w}" height="${h}" rx="26" fill="#495057"/>
  <rect x="12" y="34" width="${w - 24}" height="${h - 70}" rx="8" fill="#e7f5ff"/><rect x="${w / 2 - 24}" y="14" width="48" height="8" rx="4" fill="#868e96" stroke="none"/>
  <circle cx="${w / 2}" cy="${h - 18}" r="9" fill="#868e96" stroke="none"/>${dentro}</g>`;
const ILL = {
  telefono: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(30, 40, .6)}${NUVOLA(420, 30, .5)}${PRATO(450)}
    ${TELEFONO(150, 70, 200, 390, BOLLA(24, 60, 130, "#b2f2bb", 0) + BOLLA(46, 140, 130, "#ffe066", 1) + BOLLA(24, 220, 130, "#ffc9c9", 2))}
    ${SPUNTA("si", 410, 170, 36)}${CROCE("no", 410, 300, 36)}${PG("flavio")}</svg>`,
  chat: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(380, 40, .5)}${PRATO(455)}
    ${TELEFONO(40, 150, 170, 320, BOLLA(20, 50, 110, "#ffe066", 0, "x") + BOLLA(34, 120, 110, "#ffc9c9", 1, "x"))}
    <g class="volo">${Array.from({ length: 7 }, (_, i) => BOLLA(0, 0, 90 + (i % 3) * 18, ["#ffe066", "#ffc9c9", "#d0bfff", "#a5d8ff"][i % 4], i, "vb")).join("")}</g>
    ${PG("flavio")}</svg>`,
  lente: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${PRATO(470)}
    <g transform="translate(80 60)"><rect width="380" height="150" rx="34" fill="#ffd8a8" ${O}/><path d="M60 148 L40 196 L110 148" fill="#ffd8a8" ${O}/>
      <rect x="34" y="34" width="250" height="16" rx="8" fill="${INK}" opacity=".45"/><rect x="34" y="66" width="200" height="16" rx="8" fill="${INK}" opacity=".35"/><rect x="34" y="98" width="230" height="16" rx="8" fill="${INK}" opacity=".3"/>
      <text x="330" y="104" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="80" fill="#e03131" stroke="${INK}" stroke-width="3">?</text></g>
    <g class="lente"><circle r="58" fill="rgba(255,255,255,.45)" stroke="${INK}" stroke-width="12"/><circle r="58" fill="none" stroke="#ffd43b" stroke-width="5"/>
      <path d="M44 44 L96 96" stroke="${INK}" stroke-width="26" stroke-linecap="round"/><path d="M44 44 L96 96" stroke="#c08a4f" stroke-width="15" stroke-linecap="round"/></g>
    ${[["persone", 120], ["calendario", 250], ["scudo", 380]].map(([n, x], j) => `<g class="b${j}" transform="translate(${x} 352)"><g><circle r="54" fill="#fff" ${O}/><g transform="translate(-36 -36) scale(.72)">${INTERNO(n)}</g>
      <g transform="translate(40 -40)"><circle r="18" fill="#40c057" ${O}/><path d="M-8 0 L-2 7 L9 -7" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/></g></g></g>`).join("")}
    ${PG("flavio")}</svg>`,
  fonti: () => `<div class="tiles">${tile("comune", "Il Comune", BOLLO_SI)}${tile("pc", "La Protezione Civile", BOLLO_SI)}${tile("allarme", "IT-alert sul cellulare", BOLLO_SI)}${tile("sito", "Il sito del Gruppo", BOLLO_SI)}</div>`,
  inoltra: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(380, 40, .5)}${PRATO(455)}
    ${TELEFONO(50, 110, 170, 330, BOLLA(20, 60, 110, "#ffc9c9", 0))}
    <g class="freccia"><path d="M0 0 H110 M76 -34 L110 0 L76 34" stroke="${INK}" stroke-width="26" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M0 0 H110 M76 -34 L110 0 L76 34" stroke="#74c0fc" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
    ${DIVIETO("stop", 330, 250, 70)}${PG("flavio")}</svg>`,
  adulto: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 40, .55)}${PRATO(440)}
    <g class="fumetto"><g><rect x="-100" y="-56" width="200" height="96" rx="30" fill="#fff" ${O}/><path d="M-20 38 L-40 74 L14 38" fill="#fff" ${O}/>
      <g class="dubbio"><text x="0" y="22" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="64" fill="#e03131">?</text></g>
      <g class="certo">${SPUNTA("", 0, -6, 30)}</g></g></g>
    <g class="cuore"><path d="M0 18 C-30 -6 -26 -30 -8 -30 C0 -30 0 -22 0 -22 C0 -22 0 -30 8 -30 C26 -30 30 -6 0 18Z" fill="#e03131" stroke="${INK}" stroke-width="4" transform="scale(1.4)"/></g>
    ${PG("ins", { tipo: "adulta", maglia: "#40c057", pantaloni: "#5c7cfa", capelli: "#5c3d1e" })}
    <g class="tel"><rect x="-22" y="-38" width="44" height="76" rx="9" fill="#495057" ${O}/><rect x="-14" y="-28" width="28" height="50" rx="3" fill="#a5d8ff"/></g>
    ${PG("flavio")}</svg>`,
  sereno: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 50, .6)}${SOLE(470, 110, 50)}
    <g ${O}>${[[30, "#ff8787", 110], [140, "#ffd43b", 140], [250, "#74c0fc", 120], [370, "#b197fc", 150], [480, "#8ce99a", 110]].map(([x, c, h]) =>
      `<rect x="${x}" y="${420 - h}" width="96" height="${h}" fill="${c}"/><path d="M${x - 8} ${428 - h} L${x + 48} ${380 - h} L${x + 104} ${428 - h}Z" fill="#fa5252"/><rect x="${x + 34}" y="${384 - h * .4}" width="26" height="26" fill="#fff"/>`).join("")}</g>
    ${PRATO(430)}${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
