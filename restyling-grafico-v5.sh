#!/bin/bash
# ============================================================
# RESTYLING GRAFICO COMPLETO v5
# Protezione Civile Genzano di Roma
# Esegui con: bash restyling-grafico-v5.sh
# ============================================================

set -e
cd ~/sito-pc-genzano

echo "📥 Pull..."
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

# ── 1. CSS COMPLETO v5 — RESTYLING PROFESSIONALE ──
echo "🎨 CSS v5 completo..."
cat > themes/flavour-pcgenzano/static/css/custom.css << 'CSSEOF'
/* ============================================================
   CSS v5.0 — Protezione Civile Genzano di Roma
   Restyling grafico professionale
   Bootstrap Italia 2.17 + Linee guida AGID
   ============================================================ */

/* ── VARIABILI DESIGN SYSTEM ── */
:root {
  --pc-primary: #003366;
  --pc-primary-dark: #00244d;
  --pc-primary-light: #004080;
  --pc-secondary: #FF6600;
  --pc-accent: #009246;
  --pc-danger: #d9364f;
  --pc-light-bg: #f2f5f8;
  --pc-warm-bg: #fafbfc;
  --pc-border-subtle: rgba(0,51,102,0.08);
  --pc-shadow-sm: 0 1px 4px rgba(0,0,0,0.06);
  --pc-shadow-md: 0 4px 16px rgba(0,0,0,0.08);
  --pc-shadow-lg: 0 8px 32px rgba(0,0,0,0.1);
  --pc-shadow-hover: 0 12px 40px rgba(0,0,0,0.12);
  --pc-radius-sm: 4px;
  --pc-radius: 8px;
  --pc-radius-lg: 12px;
  --pc-transition: 0.25s cubic-bezier(0.4,0,0.2,1);
}

/* ── GLOBAL REFINEMENTS ── */
body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

::selection { background: var(--pc-primary); color: #fff; }

img { transition: opacity var(--pc-transition); }

/* ── EMERGENCY BANNER ── */
.emergency-banner {
  background: var(--pc-danger);
  color: #fff;
  padding: 0.5rem 0;
  font-size: 0.85rem;
  letter-spacing: 0.02em;
}
.emergency-banner a { color: #fff; font-weight: 700; text-decoration: underline; text-underline-offset: 2px; }

/* ── ALLERTA BAR ── */
.allerta-bar { padding: 0.6rem 0; font-size: 0.85rem; font-weight: 500; transition: background var(--pc-transition); }
.allerta-bar-verde { background: #28a745 !important; color: #fff !important; }
.allerta-bar-gialla { background: #ffc107 !important; color: #000 !important; }
.allerta-bar-arancione { background: #fd7e14 !important; color: #fff !important; }
.allerta-bar-rossa { background: #dc3545 !important; color: #fff !important; }
.allerta-bar-btn { border-radius: 20px; font-size: 0.78rem; padding: 0.25rem 1rem; font-weight: 600; transition: all var(--pc-transition); }
.allerta-bar-verde .allerta-bar-btn { color: #fff; border-color: rgba(255,255,255,0.5); }
.allerta-bar-verde .allerta-bar-btn:hover { background: rgba(255,255,255,0.2); }
.allerta-bar-gialla .allerta-bar-btn { color: #000; border-color: rgba(0,0,0,0.3); }
.allerta-bar-gialla .allerta-bar-btn:hover { background: rgba(0,0,0,0.1); }
.allerta-bar-arancione .allerta-bar-btn,
.allerta-bar-rossa .allerta-bar-btn { color: #fff; border-color: rgba(255,255,255,0.5); }
.allerta-bar-arancione .allerta-bar-btn:hover,
.allerta-bar-rossa .allerta-bar-btn:hover { background: rgba(255,255,255,0.2); }

/* ── HERO ── */
.hero-section {
  background: linear-gradient(145deg, var(--pc-primary-dark) 0%, var(--pc-primary) 35%, var(--pc-primary-light) 100%);
  color: #fff;
  padding: 3.5rem 0 4rem;
  position: relative;
  overflow: hidden;
}
.hero-section::before {
  content: '';
  position: absolute;
  top: -40%;
  right: -15%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
.hero-section::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(255,102,0,0.04) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
.hero-section h1 {
  font-size: 2.6rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  position: relative;
  z-index: 1;
}
.hero-section .lead {
  font-size: 1.1rem;
  opacity: 0.85;
  position: relative;
  z-index: 1;
  max-width: 560px;
  line-height: 1.6;
}
.hero-section .btn { position: relative; z-index: 1; font-weight: 600; letter-spacing: 0.01em; }
.hero-section .btn-warning { background: #FF6600; border-color: #FF6600; color: #fff; }
.hero-section .btn-warning:hover { background: #e65c00; border-color: #e65c00; color: #fff; }
@media (max-width: 768px) {
  .hero-section h1 { font-size: 1.8rem; }
  .hero-section { padding: 2.5rem 0 3rem; }
}

/* ── STATS HERO (glassmorphism) ── */
.stats-hero {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--pc-radius-lg);
  padding: 1.5rem;
}
.stat-hero-item { text-align: center; padding: 0.75rem 0; }
.stat-hero-num { font-size: 2.2rem; font-weight: 800; display: block; line-height: 1; letter-spacing: -0.02em; }
.stat-hero-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.65; margin-top: 0.25rem; display: block; }

/* ── SEZIONI ── */
.servizi-section { background: var(--pc-light-bg); padding: 3.5rem 0; }
.section-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--pc-primary);
  margin-bottom: 1.75rem;
  position: relative;
  padding-bottom: 0.75rem;
  letter-spacing: -0.01em;
}
.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 48px;
  height: 3px;
  background: var(--pc-secondary);
  border-radius: 2px;
}
.section-title.text-center::after { left: 50%; transform: translateX(-50%); }

/* ── QUICK ACTIONS ── */
.quick-action-card {
  background: #fff;
  border: 1px solid var(--pc-border-subtle);
  border-radius: var(--pc-radius);
  padding: 1.25rem;
  text-align: center;
  transition: all var(--pc-transition);
  text-decoration: none;
  color: #333;
  display: block;
}
.quick-action-card:hover {
  border-color: var(--pc-primary);
  box-shadow: var(--pc-shadow-md);
  color: var(--pc-primary);
  transform: translateY(-3px);
}
.quick-action-card i { font-size: 1.8rem; margin-bottom: 0.4rem; display: block; transition: transform var(--pc-transition); }
.quick-action-card:hover i { transform: scale(1.15); }
.quick-action-card strong { font-size: 0.85rem; }

/* ── CARD SERVIZI ── */
.card-servizio {
  transition: all var(--pc-transition);
  border: 1px solid var(--pc-border-subtle);
  border-radius: var(--pc-radius);
  background: #fff;
  overflow: hidden;
}
.card-servizio:hover {
  transform: translateY(-4px);
  box-shadow: var(--pc-shadow-hover);
  border-color: transparent;
}
.card-servizio .btn { border-radius: 20px; font-size: 0.8rem; padding: 0.35rem 1.2rem; }

/* ── NOTIZIE ── */
.notizie-section { padding: 3.5rem 0; background: var(--pc-warm-bg); }

.card-notizia-hero {
  border: none;
  border-radius: var(--pc-radius-lg);
  overflow: hidden;
  box-shadow: var(--pc-shadow-md);
  transition: all var(--pc-transition);
  background: #fff;
}
.card-notizia-hero:hover { box-shadow: var(--pc-shadow-hover); transform: translateY(-4px); }
.card-notizia-hero-img { height: 260px; overflow: hidden; }
.card-notizia-hero-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.card-notizia-hero:hover .card-notizia-hero-img img { transform: scale(1.04); }

.card-notizia-small {
  border: none;
  border-radius: var(--pc-radius);
  overflow: hidden;
  box-shadow: var(--pc-shadow-sm);
  transition: all var(--pc-transition);
  background: #fff;
}
.card-notizia-small:hover { box-shadow: var(--pc-shadow-md); transform: translateX(4px); }
.card-notizia-small-img { height: 100%; min-height: 90px; overflow: hidden; }
.card-notizia-small-img img { width: 100%; height: 100%; object-fit: cover; }

.notizia-categoria {
  display: inline-block;
  font-size: 0.6rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.2rem 0.6rem;
  border-radius: 3px;
}
.notizia-categoria.allerta { background: var(--pc-danger); color: #fff; }
.notizia-categoria.avviso { background: #ffc107; color: #000; }
.notizia-categoria.evento { background: var(--pc-accent); color: #fff; }
.notizia-categoria.comunicazione { background: var(--pc-primary); color: #fff; }

.notizia-data { font-size: 0.78rem; color: #6c757d; }
.notizia-data i { margin-right: 0.2rem; }
.notizia-titolo { font-size: 1.05rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.4rem; line-height: 1.35; }
.notizia-titolo a { color: inherit; text-decoration: none; }
.notizia-titolo a:hover { color: var(--pc-primary); }
.notizia-excerpt { font-size: 0.88rem; color: #555; line-height: 1.55; }
.notizia-link {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--pc-primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: all var(--pc-transition);
}
.notizia-link:hover { color: var(--pc-secondary); gap: 0.5rem; }

.notizia-img-wrapper { width: 100%; overflow: hidden; background: var(--pc-primary); }
.notizia-img-wrapper img { width: 100%; height: 100%; object-fit: cover; }

/* ── CARD NOTIZIA (lista) ── */
.card-notizia {
  border: none;
  border-radius: 0;
  border-left: 4px solid var(--pc-primary);
  transition: all var(--pc-transition);
  background: #fff;
}
.card-notizia:hover { border-left-color: var(--pc-secondary); box-shadow: var(--pc-shadow-md); }

/* ── SOCIAL BUTTONS ── */
.card-social-link {
  border: 1px solid var(--pc-border-subtle);
  border-radius: var(--pc-radius);
  transition: all var(--pc-transition);
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #333;
  padding: 0.7rem 1rem;
}
.card-social-link:hover { border-color: var(--pc-primary); box-shadow: var(--pc-shadow-sm); color: #333; transform: translateX(2px); }

/* ── BADGES ALLERTE ── */
.badge-allerta-verde { background: #28a745; color: #fff; padding: 0.5em 1em; font-size: 0.85rem; border-radius: var(--pc-radius-sm); }
.badge-allerta-gialla { background: #ffc107; color: #000; padding: 0.5em 1em; font-size: 0.85rem; border-radius: var(--pc-radius-sm); }
.badge-allerta-arancione { background: #fd7e14; color: #fff; padding: 0.5em 1em; font-size: 0.85rem; border-radius: var(--pc-radius-sm); }
.badge-allerta-rossa { background: #dc3545; color: #fff; padding: 0.5em 1em; font-size: 0.85rem; border-radius: var(--pc-radius-sm); }

/* ── TIMELINE ── */
.timeline-wrapper { position: relative; padding-left: 1rem; }
.timeline-item {
  position: relative;
  padding-left: 2rem;
  margin-bottom: 1.25rem;
  border-left: 2px solid rgba(0,51,102,0.15);
  padding-bottom: 0.5rem;
  transition: all var(--pc-transition);
}
.timeline-item:hover { border-left-color: var(--pc-secondary); }
.timeline-item::before {
  content: '';
  position: absolute;
  left: -7px;
  top: 6px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--pc-primary);
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px var(--pc-primary);
  transition: all var(--pc-transition);
}
.timeline-item:hover::before { background: var(--pc-secondary); box-shadow: 0 0 0 2px var(--pc-secondary); }

/* ── TABLES ── */
table { width: 100%; margin-bottom: 1rem; border-collapse: collapse; border-radius: var(--pc-radius); overflow: hidden; box-shadow: var(--pc-shadow-sm); }
table th { background: var(--pc-primary); color: #fff; padding: 0.75rem 1rem; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.02em; }
table td { padding: 0.75rem 1rem; border-bottom: 1px solid #e9ecef; font-size: 0.88rem; }
table tr:nth-child(even) { background: #f8f9fa; }
table tr { transition: background var(--pc-transition); }
table tr:hover { background: #e8f4fd; }

/* ── BACK TO TOP ── */
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 44px;
  height: 44px;
  background: var(--pc-primary);
  color: #fff;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15rem;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 999;
  box-shadow: var(--pc-shadow-md);
}
.back-to-top.visible { opacity: 1; visibility: visible; }
.back-to-top:hover { background: var(--pc-secondary); transform: translateY(-3px); box-shadow: var(--pc-shadow-lg); }

/* ── ANIMATIONS ── */
.fade-in-up { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-in-up.visible { opacity: 1; transform: translateY(0); }

/* ── 404 ── */
.page-404 { text-align: center; padding: 5rem 0; }
.page-404 h1 { font-size: 7rem; font-weight: 800; color: var(--pc-primary); margin-bottom: 0; letter-spacing: -0.04em; opacity: 0.85; }
.page-404 h2 { font-size: 1.4rem; color: #555; margin-bottom: 2rem; font-weight: 400; }

/* ── FOOTER ── */
.footer-list { list-style: none; padding: 0; margin: 0; }
.footer-list li { margin-bottom: 0.4rem; }
.footer-list .list-item { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 0.88rem; transition: color var(--pc-transition); }
.footer-list .list-item:hover { color: #fff; }

/* ── SEARCH ── */
#search-results .search-result-item { padding: 1rem 0; border-bottom: 1px solid #eee; }
#search-results .search-result-item h3 a { color: var(--pc-primary); text-decoration: none; }
#search-results .search-result-item h3 a:hover { text-decoration: underline; }

/* ── ACCESSIBILITY ── */
a:focus-visible, button:focus-visible, input:focus-visible,
select:focus-visible, textarea:focus-visible {
  outline: 3px solid #ff9900;
  outline-offset: 2px;
}
.skip-to-content {
  position: absolute; top: -100%; left: 0;
  background: var(--pc-primary); color: #fff;
  padding: 0.75rem 1.5rem; z-index: 9999;
  font-weight: 700; text-decoration: none;
  border-radius: 0 0 var(--pc-radius-sm) var(--pc-radius-sm);
}
.skip-to-content:focus { top: 0; }

/* ── BREADCRUMB ── */
.breadcrumb { font-size: 0.85rem; margin-bottom: 1.5rem; }
.breadcrumb-item a { color: var(--pc-primary); text-decoration: none; }
.breadcrumb-item a:hover { text-decoration: underline; }

/* ── BUTTONS REFINEMENT ── */
.btn-outline-primary { border-color: var(--pc-primary); color: var(--pc-primary); border-radius: 20px; font-weight: 600; font-size: 0.88rem; padding: 0.45rem 1.5rem; transition: all var(--pc-transition); }
.btn-outline-primary:hover { background: var(--pc-primary); color: #fff; box-shadow: var(--pc-shadow-sm); }
.btn-primary { background: var(--pc-primary); border-color: var(--pc-primary); border-radius: 20px; font-weight: 600; }
.btn-primary:hover { background: var(--pc-primary-dark); border-color: var(--pc-primary-dark); }

/* ── PRINT ── */
@media print {
  .navbar, footer, .cookiebar, .skip-to-content, .it-header-slim-wrapper,
  .it-header-navbar-wrapper, .back-to-top, .emergency-banner, .allerta-bar, .stats-hero {
    display: none !important;
  }
  .hero-section { background: #fff !important; color: #000 !important; padding: 1rem 0; }
}

/* ── MOBILE REFINEMENTS ── */
@media (max-width: 768px) {
  .card-notizia-hero-img { height: 200px; }
  .section-title { font-size: 1.35rem; }
  .stat-hero-num { font-size: 1.8rem; }
  .quick-action-card { padding: 1rem; }
  .quick-action-card i { font-size: 1.5rem; }
}
CSSEOF

# ── 2. COMMIT ──
echo "📤 Pubblicazione restyling..."
git add -A
git commit -m "🎨 Restyling grafico v5: CSS professionale, micro-interazioni, tipografia raffinata, ombre migliorate"
git push

echo ""
echo "============================================"
echo "  ✅ RESTYLING GRAFICO v5 COMPLETATO!"
echo "============================================"
echo ""
echo "  MIGLIORIE CSS:"
echo "  ✓ Sistema di variabili CSS completo"
echo "  ✓ Ombre progressive (sm/md/lg/hover)"
echo "  ✓ Transizioni fluide cubic-bezier"
echo "  ✓ Bordi arrotondati consistenti"
echo "  ✓ Micro-interazioni su hover (card, quick actions, timeline)"
echo "  ✓ Bottone Warning arancione (non giallo) nel hero"
echo "  ✓ Font smoothing antialiased"
echo "  ✓ Selezione testo con colore primario"
echo "  ✓ Breadcrumb raffinato"
echo "  ✓ Bottoni con border-radius pillola (20px)"
echo "  ✓ Tipografia: letter-spacing e line-height raffinati"
echo "  ✓ Mobile: spacing e font-size ottimizzati"
echo "  ✓ Quick actions con zoom icona su hover"
echo "  ✓ Timeline con colore che cambia su hover"
echo "  ✓ Tabelle con border-radius e ombre"
echo "  ✓ Footer link con transizione colore"
echo "============================================"
