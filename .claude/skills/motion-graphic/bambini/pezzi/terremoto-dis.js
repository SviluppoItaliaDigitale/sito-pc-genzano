/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const ILL = {
  scuola: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(30, 50, .7)}${NUVOLA(400, 30, .55)}${PRATO(445)}
    <g class="trema" ${O}>
      <path d="M300 128 V78" /><rect x="300" y="78" width="16" height="24" fill="#40c057"/><rect x="316" y="78" width="16" height="24" fill="#fff"/><rect x="332" y="78" width="16" height="24" fill="#e03131"/>
      <rect x="150" y="230" width="300" height="215" fill="#ffe066"/>
      <path d="M126 238 L300 128 L474 238Z" fill="#ff6b6b"/>
      <rect x="236" y="188" width="128" height="38" rx="10" fill="#fff"/>
      <text x="300" y="216" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="26" fill="${INK}" stroke="none">SCUOLA</text>
      ${[[172, 262], [368, 262], [172, 350], [368, 350]].map(([x, y]) => `<rect x="${x}" y="${y}" width="60" height="52" rx="6" fill="#a5d8ff"/><path d="M${x + 30} ${y} V${y + 52}"/>`).join("")}
      <rect x="268" y="345" width="64" height="100" rx="8" fill="#4dabf7"/><circle cx="318" cy="398" r="4" fill="${INK}"/></g>
    <g class="onde" fill="none" stroke="#4dabf7" stroke-width="6" stroke-linecap="round"><path d="M120 470 Q140 455 160 470"/><path d="M440 470 Q460 455 480 470"/></g>
    ${PG("flavio")}</svg>`,
  sismografo: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(470, "#8ce99a")}
    <rect x="60" y="34" width="480" height="200" rx="14" fill="#fff" ${O}/>
    <g stroke="#d0ebff" stroke-width="3">${[74, 114, 154, 194].map(y => `<path d="M72 ${y} H528"/>`).join("")}</g>
    <path class="traccia" d="" stroke="#e03131" stroke-width="6" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
    <g class="penna"><path d="M0 0 L0 -50" stroke="${INK}" stroke-width="6"/><circle r="10" fill="#e03131" stroke="${INK}" stroke-width="4"/></g>
    <rect x="40" y="246" width="520" height="96" rx="20" fill="#74c0fc" ${O}/>
    <text x="300" y="306" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="30" fill="${INK}">QUANDO? NESSUNO PUÒ SAPERLO</text>
    <g class="pensa"><g><circle cx="0" cy="0" r="34" fill="#fff" ${O}/><circle cx="-30" cy="34" r="8" fill="#fff" ${O}/>
      <text x="0" y="16" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="46" fill="#e03131">?</text></g></g>
    ${PG("flavio")}</svg>`,
  prima: () => `<svg ${S0}>${STANZA}
    <rect x="40" y="70" width="140" height="120" rx="8" fill="#a5d8ff" ${O}/><path d="M110 70 V190 M40 130 H180" ${O}/>
    <g class="mappa"><rect x="400" y="60" width="150" height="120" rx="8" fill="#d3f9d8" ${O}/><path d="M412 150 Q450 100 480 130 T540 90" fill="none" stroke="#4dabf7" stroke-width="6"/>
      <g transform="translate(475 70) scale(.62)">${INTERNO("pin")}</g></g>
    <g ${O}><rect x="250" y="296" width="250" height="24" rx="6" fill="#c08a4f"/><path d="M270 320 V420 M480 320 V420" stroke-width="16"/><path d="M270 320 V420 M480 320 V420" stroke="#c08a4f" stroke-width="7"/></g>
    ${SPUNTA("ok1", 375, 260, 30)}
    <g class="zaino"><g><g transform="translate(110 340) scale(.8)">${INTERNO("zaino")}</g></g></g>
    ${PG("flavio")}</svg>`,
  tavolo: () => `<svg ${S0}><g class="trema">${STANZA}
    <rect x="40" y="60" width="130" height="110" rx="8" fill="#a5d8ff" ${O}/><path d="M105 60 V170 M40 115 H170" ${O}/>
    <g ${O}><rect x="120" y="248" width="380" height="28" rx="8" fill="#c08a4f"/><path d="M150 276 V424 M476 276 V424" stroke-width="20"/><path d="M150 276 V424 M476 276 V424" stroke="#c08a4f" stroke-width="10"/></g></g>
    <g class="cade" ${O}><rect data-i="0" x="-30" y="-10" width="60" height="20" rx="4" fill="#4dabf7"/><rect data-i="1" x="-28" y="-6" width="56" height="12" rx="6" fill="#ffd43b"/><circle data-i="2" cx="0" cy="0" r="14" fill="#ff922b"/></g>
    ${PG("flavio")}${RANNICCHIATO("giu")}${STELLA("brav1", 520, 110, 26)}${STELLA("brav2", 560, 170, 18, "#ff922b")}${STELLA("brav3", 470, 70, 16, "#4dabf7")}</svg>`,
  pericolo: () => `<div class="tiles">${tile("finestra", "Lontano dalle finestre")}${tile("mobile", "Lontano dai mobili alti")}${tile("ascensore", "Niente ascensore")}${tile("corsa", "Non correre fuori")}</div>`,
  aperto: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(380, 40, .6)}${PRATO(395)}
    <g class="trema" ${O}><rect x="10" y="140" width="130" height="260" fill="#ced4da"/>${[[30, 170], [80, 170], [30, 250], [80, 250]].map(([x, y]) => `<rect x="${x}" y="${y}" width="34" height="40" fill="#a5d8ff"/>`).join("")}
      <rect x="198" y="270" width="22" height="130" fill="#a0703c"/><circle cx="209" cy="236" r="56" fill="#40c057"/>
      <rect x="282" y="190" width="12" height="210" fill="#868e96"/><circle cx="288" cy="184" r="16" fill="#ffd43b"/></g>
    <path d="M140 172 Q215 210 288 196" stroke="${INK}" stroke-width="4" fill="none"/>
    <g class="zona"><ellipse cx="455" cy="468" rx="110" ry="30" fill="#b2f2bb" stroke="#2f9e44" stroke-width="5" stroke-dasharray="14 10"/></g>
    ${STELLA("st1", 360, 300, 18)}${STELLA("st2", 560, 280, 22, "#ff922b")}${STELLA("st3", 530, 360, 14, "#4dabf7")}
    ${PG("flavio")}</svg>`,
  fila: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(250, 30, .6)}
    <rect x="-10" y="430" width="620" height="90" fill="#dee2e6" ${O}/>
    <g ${O}><rect x="-10" y="130" width="160" height="300" fill="#ffe066"/><rect x="38" y="330" width="64" height="100" rx="8" fill="#4dabf7"/>
      <rect x="20" y="170" width="100" height="90" rx="6" fill="#a5d8ff"/></g>
    <g transform="translate(42 178) scale(.7)">${INTERNO("zaino")}</g>
    <g ${O}><rect x="540" y="230" width="12" height="200" fill="#868e96"/><rect x="470" y="170" width="140" height="70" rx="12" fill="#40c057"/></g>
    <text x="540" y="216" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="24" fill="#fff">RACCOLTA</text>
    ${PG("ins", { tipo: "adulta", maglia: "#40c057", pantaloni: "#5c7cfa", capelli: "#5c3d1e" })}
    ${PG("k1", { maglia: "#ff922b" })}${PG("k2", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}${PG("k3", { tipo: "elio", maglia: "#4dabf7", pantaloni: "#495057", capelli: "#e8a33d" })}</svg>`,
  dopo: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 40, .55)}${PRATO(400)}
    <g ${O}><rect x="180" y="200" width="12" height="190" fill="#868e96"/><rect x="408" y="200" width="12" height="190" fill="#868e96"/>
      <rect x="140" y="110" width="320" height="100" rx="18" fill="#40c057"/></g>
    <text x="300" y="174" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="36" fill="#fff">AREA DI ATTESA</text>
    <g class="cuore"><path d="M0 18 C-30 -6 -26 -30 -8 -30 C0 -30 0 -22 0 -22 C0 -22 0 -30 8 -30 C26 -30 30 -6 0 18Z" fill="#e03131" stroke="${INK}" stroke-width="4" transform="scale(1.6)"/></g>
    ${PG("mamma", { tipo: "adulta", maglia: "#9775fa", pantaloni: "#495057", capelli: "#3b2412" })}${PG("flavio")}</svg>`,
  sereno: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 50, .6)}${SOLE(470, 110, 50)}
    <g ${O}>${[[30, "#ff8787", 110], [140, "#ffd43b", 140], [250, "#74c0fc", 120], [370, "#b197fc", 150], [480, "#8ce99a", 110]].map(([x, c, h], i) =>
      `<rect x="${x}" y="${420 - h}" width="96" height="${h}" fill="${c}"/><path d="M${x - 8} ${428 - h} L${x + 48} ${380 - h} L${x + 104} ${428 - h}Z" fill="#fa5252"/><rect x="${x + 34}" y="${384 - h * .4}" width="26" height="26" fill="#fff"/>`).join("")}</g>
    ${PRATO(430)}${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
