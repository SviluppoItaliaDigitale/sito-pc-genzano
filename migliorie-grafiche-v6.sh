#!/bin/bash
# ============================================================
# MIGLIORIE GRAFICHE COMPLETE v6
# Tutte le migliorie: hero, card, footer, pulse, icone, mobile
# Esegui con: bash migliorie-grafiche-v6.sh
# ============================================================

set -e
cd ~/sito-pc-genzano

echo "📥 Pull..."
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

# ── 1. CSS v6 COMPLETO ──
echo "🎨 CSS v6 con tutte le migliorie..."
cat > themes/flavour-pcgenzano/static/css/custom.css << 'CSSEOF'
/* ============================================================
   CSS v6.0 — Protezione Civile Genzano di Roma
   Migliorie grafiche complete
   ============================================================ */

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

body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
::selection { background: var(--pc-primary); color: #fff; }

/* ── EMERGENCY BANNER ── */
.emergency-banner {
  background: var(--pc-danger);
  color: #fff;
  padding: 0.5rem 0;
  font-size: 0.85rem;
  letter-spacing: 0.02em;
}
.emergency-banner a { color: #fff; font-weight: 700; }

/* ── ALLERTA BAR + PULSE ── */
.allerta-bar { padding: 0.6rem 0; font-size: 0.85rem; font-weight: 500; transition: background var(--pc-transition); }
.allerta-bar-verde { background: #28a745 !important; color: #fff !important; }
.allerta-bar-gialla { background: #ffc107 !important; color: #000 !important; }
.allerta-bar-arancione { background: #fd7e14 !important; color: #fff !important; }
.allerta-bar-rossa { background: #dc3545 !important; color: #fff !important; }

.allerta-bar-gialla,
.allerta-bar-arancione,
.allerta-bar-rossa { animation: pulse-allerta 2.5s ease-in-out infinite; }

@keyframes pulse-allerta {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}

.allerta-bar-btn { border-radius: 20px; font-size: 0.78rem; padding: 0.25rem 1rem; font-weight: 600; transition: all var(--pc-transition); }
.allerta-bar-verde .allerta-bar-btn { color: #fff; border-color: rgba(255,255,255,0.5); }
.allerta-bar-gialla .allerta-bar-btn { color: #000; border-color: rgba(0,0,0,0.3); }
.allerta-bar-arancione .allerta-bar-btn,
.allerta-bar-rossa .allerta-bar-btn { color: #fff; border-color: rgba(255,255,255,0.5); }
.allerta-bar-verde .allerta-bar-btn:hover,
.allerta-bar-arancione .allerta-bar-btn:hover,
.allerta-bar-rossa .allerta-bar-btn:hover { background: rgba(255,255,255,0.2); }
.allerta-bar-gialla .allerta-bar-btn:hover { background: rgba(0,0,0,0.1); }

/* ── HERO CON PATTERN ── */
.hero-section {
  background: linear-gradient(145deg, var(--pc-primary-dark) 0%, var(--pc-primary) 35%, var(--pc-primary-light) 100%);
  color: #fff;
  padding: 4rem 0 4.5rem;
  position: relative;
  overflow: hidden;
}
.hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 80% 20%, rgba(255,255,255,0.06) 0%, transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(255,102,0,0.05) 0%, transparent 50%),
    url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 30 L30 0 L60 30 L30 60Z' fill='none' stroke='rgba(255,255,255,0.03)' stroke-width='1'/%3E%3C/svg%3E");
  pointer-events: none;
}
.hero-section h1 {
  font-size: 2.8rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
  position: relative;
  z-index: 1;
}
.hero-section h1 span.hero-highlight {
  display: block;
  color: var(--pc-secondary);
  font-size: 0.85em;
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
.hero-section .btn-warning { background: var(--pc-secondary); border-color: var(--pc-secondary); color: #fff; }
.hero-section .btn-warning:hover { background: #e65c00; border-color: #e65c00; color: #fff; transform: translateY(-1px); }
@media (max-width: 768px) {
  .hero-section h1 { font-size: 2rem; }
  .hero-section { padding: 3rem 0; }
}

/* ── STATS HERO ── */
.stats-hero {
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--pc-radius-lg);
  padding: 1.5rem;
}
.stat-hero-item { text-align: center; padding: 0.75rem 0; position: relative; }
.stat-hero-num { font-size: 2.4rem; font-weight: 800; display: block; line-height: 1; letter-spacing: -0.02em; }
.stat-hero-label { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.6; margin-top: 0.3rem; display: block; }
/* Separatori verticali */
.stats-hero .col-6:nth-child(odd) .stat-hero-item::after {
  content: '';
  position: absolute;
  right: 0;
  top: 15%;
  height: 70%;
  width: 1px;
  background: rgba(255,255,255,0.15);
}

/* ── MINI HERO PER PAGINE INTERNE ── */
.page-hero {
  background: linear-gradient(135deg, var(--pc-primary-dark), var(--pc-primary));
  color: #fff;
  padding: 2rem 0;
  position: relative;
  overflow: hidden;
}
.page-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 30 L30 0 L60 30 L30 60Z' fill='none' stroke='rgba(255,255,255,0.03)' stroke-width='1'/%3E%3C/svg%3E");
  pointer-events: none;
}
.page-hero h1 { font-size: 1.8rem; font-weight: 700; margin: 0; position: relative; z-index: 1; }
.page-hero .breadcrumb { margin-bottom: 0.5rem; font-size: 0.85rem; position: relative; z-index: 1; }
.page-hero .breadcrumb-item a { color: rgba(255,255,255,0.7); text-decoration: none; }
.page-hero .breadcrumb-item a:hover { color: #fff; }
.page-hero .breadcrumb-item.active { color: rgba(255,255,255,0.9); }
.page-hero .breadcrumb-item+.breadcrumb-item::before { color: rgba(255,255,255,0.4); }

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

/* ── QUICK ACTIONS (piu grandi) ── */
.quick-action-card {
  background: #fff;
  border: 1px solid var(--pc-border-subtle);
  border-radius: var(--pc-radius-lg);
  padding: 1.5rem 1rem;
  text-align: center;
  transition: all var(--pc-transition);
  text-decoration: none;
  color: #333;
  display: block;
}
.quick-action-card:hover {
  border-color: var(--pc-primary);
  box-shadow: var(--pc-shadow-lg);
  color: var(--pc-primary);
  transform: translateY(-5px);
}
.quick-action-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  font-size: 1.6rem;
  transition: transform var(--pc-transition);
}
.quick-action-card:hover .quick-action-icon { transform: scale(1.1) rotate(-5deg); }
.quick-action-icon.icon-warning { background: rgba(255,193,7,0.12); color: #e6a700; }
.quick-action-icon.icon-primary { background: rgba(0,51,102,0.08); color: var(--pc-primary); }
.quick-action-icon.icon-danger { background: rgba(220,53,69,0.1); color: #dc3545; }
.quick-action-icon.icon-success { background: rgba(0,146,70,0.1); color: var(--pc-accent); }
.quick-action-card strong { font-size: 0.9rem; display: block; margin-top: 0.25rem; }
.quick-action-card .qa-desc { font-size: 0.75rem; color: #888; margin-top: 0.25rem; }

/* ── CARD SERVIZI CON ICONE CIRCOLARI ── */
.card-servizio {
  transition: all var(--pc-transition);
  border: 1px solid var(--pc-border-subtle);
  border-radius: var(--pc-radius-lg);
  background: #fff;
  overflow: hidden;
}
.card-servizio:hover {
  transform: translateY(-5px);
  box-shadow: var(--pc-shadow-hover);
  border-color: transparent;
}
.card-servizio .btn { border-radius: 20px; font-size: 0.8rem; padding: 0.35rem 1.2rem; }
.servizio-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-bottom: 1rem;
  transition: all var(--pc-transition);
}
.card-servizio:hover .servizio-icon { transform: scale(1.08); }
.servizio-icon.si-blue { background: rgba(0,51,102,0.08); color: var(--pc-primary); }
.servizio-icon.si-orange { background: rgba(255,102,0,0.08); color: var(--pc-secondary); }
.servizio-icon.si-teal { background: rgba(0,123,138,0.08); color: #007b8a; }
.servizio-icon.si-green { background: rgba(0,146,70,0.08); color: var(--pc-accent); }

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
.card-notizia-hero-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.card-notizia-hero:hover .card-notizia-hero-img img { transform: scale(1.05); }
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
.notizia-titolo { font-size: 1.05rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.4rem; line-height: 1.35; }
.notizia-titolo a { color: inherit; text-decoration: none; }
.notizia-titolo a:hover { color: var(--pc-primary); }
.notizia-excerpt { font-size: 0.88rem; color: #555; line-height: 1.55; }
.notizia-link {
  font-size: 0.82rem; font-weight: 600; color: var(--pc-primary); text-decoration: none;
  display: inline-flex; align-items: center; gap: 0.3rem; transition: all var(--pc-transition);
}
.notizia-link:hover { color: var(--pc-secondary); gap: 0.5rem; }

.notizia-img-wrapper { width: 100%; overflow: hidden; background: var(--pc-primary); }
.notizia-img-wrapper img { width: 100%; height: 100%; object-fit: cover; }

.card-notizia {
  border: none; border-radius: 0; border-left: 4px solid var(--pc-primary);
  transition: all var(--pc-transition); background: #fff;
}
.card-notizia:hover { border-left-color: var(--pc-secondary); box-shadow: var(--pc-shadow-md); }

/* ── SOCIAL ── */
.card-social-link {
  border: 1px solid var(--pc-border-subtle); border-radius: var(--pc-radius);
  transition: all var(--pc-transition); display: flex; align-items: center;
  text-decoration: none; color: #333; padding: 0.7rem 1rem;
}
.card-social-link:hover { border-color: var(--pc-primary); box-shadow: var(--pc-shadow-sm); color: #333; transform: translateX(2px); }

/* ── BADGES ALLERTE ── */
.badge-allerta-verde { background: #28a745; color: #fff; padding: 0.5em 1em; border-radius: var(--pc-radius-sm); }
.badge-allerta-gialla { background: #ffc107; color: #000; padding: 0.5em 1em; border-radius: var(--pc-radius-sm); }
.badge-allerta-arancione { background: #fd7e14; color: #fff; padding: 0.5em 1em; border-radius: var(--pc-radius-sm); }
.badge-allerta-rossa { background: #dc3545; color: #fff; padding: 0.5em 1em; border-radius: var(--pc-radius-sm); }

/* ── TIMELINE ── */
.timeline-wrapper { position: relative; padding-left: 1rem; }
.timeline-item {
  position: relative; padding-left: 2rem; margin-bottom: 1.25rem;
  border-left: 2px solid rgba(0,51,102,0.15); padding-bottom: 0.5rem;
  transition: all var(--pc-transition);
}
.timeline-item:hover { border-left-color: var(--pc-secondary); }
.timeline-item::before {
  content: ''; position: absolute; left: -7px; top: 6px;
  width: 12px; height: 12px; border-radius: 50%;
  background: var(--pc-primary); border: 2px solid #fff;
  box-shadow: 0 0 0 2px var(--pc-primary); transition: all var(--pc-transition);
}
.timeline-item:hover::before { background: var(--pc-secondary); box-shadow: 0 0 0 2px var(--pc-secondary); }

/* ── TABLES ── */
table { width: 100%; margin-bottom: 1rem; border-collapse: collapse; border-radius: var(--pc-radius); overflow: hidden; box-shadow: var(--pc-shadow-sm); }
table th { background: var(--pc-primary); color: #fff; padding: 0.75rem 1rem; font-weight: 600; font-size: 0.85rem; }
table td { padding: 0.75rem 1rem; border-bottom: 1px solid #e9ecef; font-size: 0.88rem; }
table tr:nth-child(even) { background: #f8f9fa; }
table tr { transition: background var(--pc-transition); }
table tr:hover { background: #e8f4fd; }

/* ── FOOTER RIDISEGNATO ── */
.it-footer .it-footer-main { background: var(--pc-primary) !important; }
.it-footer .it-footer-small-prints { background: var(--pc-primary-dark) !important; }

/* ── BACK TO TOP ── */
.back-to-top {
  position: fixed; bottom: 2rem; right: 2rem; width: 44px; height: 44px;
  background: var(--pc-primary); color: #fff; border: none; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-size: 1.15rem;
  cursor: pointer; opacity: 0; visibility: hidden; transition: all 0.3s ease;
  z-index: 999; box-shadow: var(--pc-shadow-md);
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

/* ── FOOTER LINK ── */
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
select:focus-visible, textarea:focus-visible { outline: 3px solid #ff9900; outline-offset: 2px; }
.skip-to-content {
  position: absolute; top: -100%; left: 0; background: var(--pc-primary); color: #fff;
  padding: 0.75rem 1.5rem; z-index: 9999; font-weight: 700; text-decoration: none;
  border-radius: 0 0 var(--pc-radius-sm) var(--pc-radius-sm);
}
.skip-to-content:focus { top: 0; }

/* ── BUTTONS ── */
.btn-outline-primary { border-color: var(--pc-primary); color: var(--pc-primary); border-radius: 20px; font-weight: 600; font-size: 0.88rem; padding: 0.45rem 1.5rem; transition: all var(--pc-transition); }
.btn-outline-primary:hover { background: var(--pc-primary); color: #fff; box-shadow: var(--pc-shadow-sm); }
.btn-primary { background: var(--pc-primary); border-color: var(--pc-primary); border-radius: 20px; font-weight: 600; }
.btn-primary:hover { background: var(--pc-primary-dark); border-color: var(--pc-primary-dark); }

/* ── PRINT ── */
@media print {
  .navbar, footer, .cookiebar, .skip-to-content, .it-header-slim-wrapper,
  .it-header-navbar-wrapper, .back-to-top, .emergency-banner, .allerta-bar, .stats-hero, .page-hero {
    display: none !important;
  }
  .hero-section { background: #fff !important; color: #000 !important; padding: 1rem 0; }
}

/* ── MOBILE ── */
@media (max-width: 768px) {
  .card-notizia-hero-img { height: 200px; }
  .section-title { font-size: 1.35rem; }
  .stat-hero-num { font-size: 1.8rem; }
  .quick-action-card { padding: 1rem; }
  .quick-action-icon { width: 52px; height: 52px; font-size: 1.3rem; }
  .page-hero h1 { font-size: 1.4rem; }
  .servizio-icon { width: 56px; height: 56px; font-size: 1.4rem; }
}
CSSEOF

# ── 2. HOME PAGE v6 CON QUICK ACTIONS E SERVIZI MIGLIORATI ──
echo "🏠 Home page v6..."
cat > themes/flavour-pcgenzano/layouts/index.html << 'HTMLEOF'
{{ define "main" }}

<!-- BANNER EMERGENZA -->
<div class="emergency-banner" role="complementary" aria-label="Numeri di emergenza">
  <div class="container text-center">
    <i class="bi bi-telephone-fill me-1" aria-hidden="true"></i>
    <strong>Emergenze: 112</strong>
    <span class="mx-2 d-none d-md-inline">|</span>
    <span class="d-block d-md-inline">Sala Operativa PC Lazio: <strong>803 555</strong></span>
  </div>
</div>

<!-- BARRA ALLERTA -->
{{ $allerta := .Site.Data.allerta }}
{{ if $allerta }}
<div class="allerta-bar allerta-bar-{{ $allerta.livello }}" role="alert" aria-label="Stato allerta meteo">
  <div class="container d-flex flex-wrap justify-content-between align-items-center">
    <div>
      {{ if eq $allerta.livello "verde" }}<i class="bi bi-shield-check me-2" aria-hidden="true"></i>
      {{ else }}<i class="bi bi-exclamation-triangle-fill me-2" aria-hidden="true"></i>{{ end }}
      <strong>{{ $allerta.titolo }}</strong>
      <span class="d-none d-md-inline ms-2">— {{ $allerta.descrizione }}</span>
    </div>
    <a href="https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" target="_blank" rel="noopener noreferrer" class="btn btn-sm allerta-bar-btn ms-2 mt-1 mt-md-0">
      Bollettino Ufficiale <i class="bi bi-box-arrow-up-right ms-1" aria-hidden="true"></i>
    </a>
  </div>
</div>
{{ end }}

<!-- HERO -->
<section class="hero-section" aria-label="Benvenuto">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-7">
        <h1>Protezione Civile<br><span class="hero-highlight">Genzano di Roma</span></h1>
        <p class="lead mt-3">Gruppo Comunale Volontari — al servizio della comunita dal 1981.</p>
        <div class="mt-4 d-flex flex-wrap gap-2">
          <a href="{{ "allerte-meteo/" | relURL }}" class="btn btn-warning btn-lg">
            <i class="bi bi-exclamation-triangle-fill me-1" aria-hidden="true"></i> Allerte Meteo
          </a>
          <a href="{{ "piano-emergenza/" | relURL }}" class="btn btn-outline-light btn-lg">Piano di Emergenza</a>
          <a href="{{ "diventa-volontario/" | relURL }}" class="btn btn-outline-light btn-lg">Diventa Volontario</a>
        </div>
      </div>
      <div class="col-lg-5 d-none d-lg-block text-end" style="position:relative;z-index:1;">
        <div class="stats-hero">
          <div class="row g-3">
            <div class="col-6"><div class="stat-hero-item"><span class="stat-hero-num" data-count="44">0</span><span class="stat-hero-label">Anni di Attivita</span></div></div>
            <div class="col-6"><div class="stat-hero-item"><span class="stat-hero-num" data-count="8">0</span><span class="stat-hero-label">Automezzi Operativi</span></div></div>
            <div class="col-6"><div class="stat-hero-item"><span class="stat-hero-num" data-count="20">0</span><span class="stat-hero-label">Emergenze Nazionali</span></div></div>
            <div class="col-6"><div class="stat-hero-item"><span class="stat-hero-num" data-count="365">0</span><span class="stat-hero-label">Giorni di Operativita</span></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- COSA FARE IN CASO DI... -->
<section class="py-5 bg-white" aria-labelledby="quickactions-heading">
  <div class="container">
    <h2 id="quickactions-heading" class="section-title text-center">Cosa fare in caso di...</h2>
    <div class="row mt-4">
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "rischi-prevenzione/rischio-sismico/" | relURL }}" class="quick-action-card">
          <div class="quick-action-icon icon-warning"><i class="bi bi-tsunami" aria-hidden="true"></i></div>
          <strong>Terremoto</strong>
          <span class="qa-desc">Scopri come proteggerti</span>
        </a>
      </div>
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "rischi-prevenzione/rischio-idrogeologico/" | relURL }}" class="quick-action-card">
          <div class="quick-action-icon icon-primary"><i class="bi bi-cloud-rain-heavy" aria-hidden="true"></i></div>
          <strong>Alluvione</strong>
          <span class="qa-desc">Norme di comportamento</span>
        </a>
      </div>
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "rischi-prevenzione/rischio-incendio/" | relURL }}" class="quick-action-card">
          <div class="quick-action-icon icon-danger"><i class="bi bi-fire" aria-hidden="true"></i></div>
          <strong>Incendio</strong>
          <span class="qa-desc">Previeni e segnala</span>
        </a>
      </div>
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "piano-familiare/" | relURL }}" class="quick-action-card">
          <div class="quick-action-icon icon-success"><i class="bi bi-house-heart" aria-hidden="true"></i></div>
          <strong>Piano Familiare</strong>
          <span class="qa-desc">Crea il tuo piano</span>
        </a>
      </div>
    </div>
  </div>
</section>

<!-- SERVIZI -->
<section class="servizi-section fade-in-up" aria-labelledby="servizi-heading">
  <div class="container">
    <h2 id="servizi-heading" class="section-title text-center">Servizi per il cittadino</h2>
    <div class="row mt-4">
      <div class="col-lg-3 col-md-6 mb-4">
        <div class="card card-servizio shadow-sm h-100">
          <div class="card-body text-center p-4">
            <div class="servizio-icon si-blue"><i class="bi bi-house-heart" aria-hidden="true"></i></div>
            <h3 class="h6">Piano Familiare</h3>
            <p class="text-muted small">Crea il piano di emergenza per la tua famiglia.</p>
            <a href="{{ "piano-familiare/" | relURL }}" class="btn btn-outline-primary btn-sm">Crea il piano</a>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-4">
        <div class="card card-servizio shadow-sm h-100">
          <div class="card-body text-center p-4">
            <div class="servizio-icon si-orange"><i class="bi bi-exclamation-triangle" aria-hidden="true"></i></div>
            <h3 class="h6">Rischi e Prevenzione</h3>
            <p class="text-muted small">Conosci i rischi del territorio.</p>
            <a href="{{ "rischi-prevenzione/" | relURL }}" class="btn btn-outline-primary btn-sm">Scopri</a>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-4">
        <div class="card card-servizio shadow-sm h-100">
          <div class="card-body text-center p-4">
            <div class="servizio-icon si-teal"><i class="bi bi-map" aria-hidden="true"></i></div>
            <h3 class="h6">Cartografia Operativa</h3>
            <p class="text-muted small">Aree di emergenza del Piano Comunale.</p>
            <a href="{{ "cartografia/" | relURL }}" class="btn btn-outline-primary btn-sm">Consulta</a>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-4">
        <div class="card card-servizio shadow-sm h-100">
          <div class="card-body text-center p-4">
            <div class="servizio-icon si-green"><i class="bi bi-download" aria-hidden="true"></i></div>
            <h3 class="h6">Area Download</h3>
            <p class="text-muted small">Documenti e modulistica ufficiale.</p>
            <a href="{{ "area-download/" | relURL }}" class="btn btn-outline-primary btn-sm">Scarica</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- NOTIZIE -->
{{ $maxAge := now.AddDate 0 -2 0 }}
{{ $recentNews := where (where .Site.RegularPages "Section" "comunicazioni") ".Date" ">=" $maxAge }}
{{ if $recentNews }}
<section class="notizie-section fade-in-up" aria-labelledby="notizie-heading">
  <div class="container">
    <h2 id="notizie-heading" class="section-title">Notizie in Evidenza</h2>
    <div class="row">
      {{ with index $recentNews 0 }}
      <div class="col-lg-6 mb-4">
        <a href="{{ .Permalink }}" class="card card-notizia-hero text-decoration-none h-100">
          <div class="card-notizia-hero-img">
            {{ with .Params.image }}<img src="{{ . }}" alt="" loading="lazy">
            {{ else }}<img src="{{ "images/notizia-default.svg" | relURL }}" alt="" loading="lazy">{{ end }}
          </div>
          <div class="card-body">
            {{ with .Params.badge }}<span class="notizia-categoria {{ . | lower }}">{{ . }}</span>{{ end }}
            <span class="notizia-data ms-2">{{ .Date | time.Format ":date_long" }}</span>
            <h3 class="h4 mt-2 text-dark">{{ .Title }}</h3>
            <p class="text-muted">{{ with .Description }}{{ . }}{{ else }}{{ .Summary | truncate 200 }}{{ end }}</p>
          </div>
        </a>
      </div>
      {{ end }}
      <div class="col-lg-6">
        {{ range after 1 (first 5 $recentNews) }}
        <a href="{{ .Permalink }}" class="card card-notizia-small mb-3 text-decoration-none">
          <div class="row g-0">
            <div class="col-4">
              <div class="card-notizia-small-img">
                {{ with .Params.image }}<img src="{{ . }}" alt="" loading="lazy">
                {{ else }}<img src="{{ "images/notizia-default.svg" | relURL }}" alt="" loading="lazy">{{ end }}
              </div>
            </div>
            <div class="col-8">
              <div class="card-body py-2 px-3">
                {{ with .Params.badge }}<span class="notizia-categoria {{ . | lower }}" style="font-size:0.6rem;">{{ . }}</span>{{ end }}
                <h3 class="h6 mt-1 mb-1 text-dark" style="line-height:1.3;">{{ .Title }}</h3>
                <span class="notizia-data" style="font-size:0.75rem;">{{ .Date | time.Format ":date_long" }}</span>
              </div>
            </div>
          </div>
        </a>
        {{ end }}
      </div>
    </div>
    <div class="text-center mt-3">
      <a href="{{ "comunicazioni/" | relURL }}" class="btn btn-outline-primary">Tutte le comunicazioni <i class="bi bi-arrow-right ms-1" aria-hidden="true"></i></a>
    </div>
  </div>
</section>
{{ end }}

<!-- SOCIAL + IT-ALERT -->
<section class="py-4 bg-white fade-in-up">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-8">
        <h2 class="h5 fw-bold mb-3"><i class="bi bi-share me-2" aria-hidden="true"></i>Seguici sui nostri canali</h2>
        <div class="d-flex flex-wrap gap-2">
          <a href="https://www.facebook.com/protezionecivilegenzanodiroma" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm"><i class="bi bi-facebook me-1"></i> Facebook</a>
          <a href="https://www.instagram.com/protezionecivilegenzano/" target="_blank" rel="noopener noreferrer" class="btn btn-danger btn-sm"><i class="bi bi-instagram me-1"></i> Instagram</a>
          <a href="https://t.me/pcalfagenzano" target="_blank" rel="noopener noreferrer" class="btn btn-info btn-sm text-white"><i class="bi bi-telegram me-1"></i> Telegram</a>
          <a href="https://x.com/alfagenzano" target="_blank" rel="noopener noreferrer" class="btn btn-dark btn-sm"><i class="bi bi-twitter-x me-1"></i> X</a>
        </div>
      </div>
      <div class="col-lg-4 mt-3 mt-lg-0">
        <div class="card bg-warning bg-opacity-10 border-warning">
          <div class="card-body p-3 d-flex align-items-center">
            <i class="bi bi-phone-vibrate fs-3 text-warning me-3" aria-hidden="true"></i>
            <div><strong class="small">IT-alert</strong><p class="small text-muted mb-0">Sistema di allarme pubblico.</p></div>
            <a href="https://www.it-alert.it/it/" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-warning ms-auto">Info</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- METEO -->
<section class="servizi-section py-4 fade-in-up" aria-labelledby="meteo-heading">
  <div class="container">
    <h2 id="meteo-heading" class="h5 fw-bold mb-3"><i class="bi bi-cloud-sun me-2" aria-hidden="true"></i>Meteo in Tempo Reale</h2>
    <div class="ratio ratio-21x9">
      <iframe src="https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=%C2%B0C&metricWind=km/h&zoom=10&overlay=rain&product=ecmwf&level=surface&lat=41.71&lon=12.69" title="Mappa meteo interattiva per Genzano di Roma" loading="lazy" allowfullscreen></iframe>
    </div>
  </div>
</section>

{{ end }}

{{ define "scripts" }}
<script>
(function(){
  var counters=document.querySelectorAll('[data-count]');
  if(!counters.length)return;
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting)return;
      var el=e.target;
      var target=parseInt(el.getAttribute('data-count'));
      var start=0,step=Math.ceil(target/50);
      var timer=setInterval(function(){
        start+=step;
        if(start>=target){start=target;clearInterval(timer)}
        el.textContent=start+(target===20?'+':'');
      },30);
      obs.unobserve(el);
    });
  },{threshold:0.5});
  counters.forEach(function(c){obs.observe(c)});
})();
</script>
{{ end }}
HTMLEOF

# ── 3. TEMPLATE SINGLE CON PAGE-HERO ──
echo "📄 Template single con mini hero..."
cat > themes/flavour-pcgenzano/layouts/_default/single.html << 'HTMLEOF'
{{ define "main" }}
<div class="page-hero">
  <div class="container">
    <nav aria-label="Percorso di navigazione">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="{{ "/" | relURL }}">Home</a></li>
        {{ if and .Parent (not .Parent.IsHome) (ne .Parent.Permalink .Permalink) }}
        <li class="breadcrumb-item"><a href="{{ .Parent.Permalink }}">{{ .Parent.Title }}</a></li>
        {{ end }}
        <li class="breadcrumb-item active" aria-current="page">{{ .Title }}</li>
      </ol>
    </nav>
    <h1>{{ .Title }}</h1>
  </div>
</div>
<div class="container py-4">
  <div class="row">
    <div class="col-lg-8 mx-auto">
      {{ with .Params.subtitle }}<p class="lead">{{ . }}</p>{{ end }}
      {{ if and .Date (not (eq (.Date.Format "2006") "0001")) }}
      <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
        {{ with .Params.badge }}<span class="notizia-categoria {{ . | lower }}">{{ . }}</span>{{ end }}
        <span class="notizia-data"><i class="bi bi-calendar3" aria-hidden="true"></i> <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date | time.Format ":date_long" }}</time></span>
      </div>
      {{ end }}
      {{ if and (eq .Section "comunicazioni") }}
      {{ with .Params.image }}
      <div class="notizia-img-wrapper mb-4" style="height:250px;border-radius:8px;"><img src="{{ . }}" alt="" loading="lazy"></div>
      {{ else }}
      <div class="notizia-img-wrapper mb-4" style="height:250px;border-radius:8px;"><img src="{{ "images/notizia-default.svg" | relURL }}" alt="" loading="lazy"></div>
      {{ end }}
      {{ end }}
      <article>{{ .Content }}</article>
      {{ if eq .Section "comunicazioni" }}
      <hr class="mt-5">
      <a href="{{ "comunicazioni/" | relURL }}" class="notizia-link"><i class="bi bi-arrow-left me-1" aria-hidden="true"></i> Torna a tutte le comunicazioni</a>
      {{ end }}
    </div>
  </div>
</div>
{{ end }}
HTMLEOF

# ── 4. TEMPLATE LIST CON PAGE-HERO ──
echo "📰 Template list con mini hero..."
cat > themes/flavour-pcgenzano/layouts/_default/list.html << 'HTMLEOF'
{{ define "main" }}
<div class="page-hero">
  <div class="container">
    <nav aria-label="Percorso di navigazione">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="{{ "/" | relURL }}">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page">{{ .Title }}</li>
      </ol>
    </nav>
    <h1>{{ .Title }}</h1>
  </div>
</div>
<div class="container py-4">
  <div class="row">
    <div class="col-lg-8 mx-auto">
      {{ .Content }}
      {{ range .Paginator.Pages }}
      <article class="card card-notizia mb-3">
        <div class="row g-0">
          <div class="col-md-3 d-none d-md-block">
            <div class="notizia-img-wrapper" style="height:100%;min-height:140px;">
              {{ with .Params.image }}<img src="{{ . }}" alt="" loading="lazy">
              {{ else }}<img src="{{ "images/notizia-default.svg" | relURL }}" alt="" loading="lazy">{{ end }}
            </div>
          </div>
          <div class="col-md-9">
            <div class="card-body">
              <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
                {{ with .Params.badge }}<span class="notizia-categoria {{ . | lower }}">{{ . }}</span>{{ end }}
                {{ if and .Date (not (eq (.Date.Format "2006") "0001")) }}
                <span class="notizia-data"><i class="bi bi-calendar3" aria-hidden="true"></i> <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date | time.Format ":date_long" }}</time></span>
                {{ end }}
              </div>
              <h2 class="notizia-titolo"><a href="{{ .Permalink }}">{{ .Title }}</a></h2>
              <p class="notizia-excerpt">{{ with .Description }}{{ . }}{{ else }}{{ .Summary | truncate 150 }}{{ end }}</p>
              <a href="{{ .Permalink }}" class="notizia-link">Leggi di piu <i class="bi bi-arrow-right" aria-hidden="true"></i></a>
            </div>
          </div>
        </div>
      </article>
      {{ end }}
      {{ template "_internal/pagination.html" . }}
    </div>
  </div>
</div>
{{ end }}
HTMLEOF

# ── 5. TEMPLATE RISCHI CON PAGE-HERO ──
echo "⚠️ Template rischi con mini hero..."
mkdir -p themes/flavour-pcgenzano/layouts/rischi-prevenzione
cat > themes/flavour-pcgenzano/layouts/rischi-prevenzione/list.html << 'HTMLEOF'
{{ define "main" }}
<div class="page-hero">
  <div class="container">
    <nav aria-label="Percorso di navigazione">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="{{ "/" | relURL }}">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page">{{ .Title }}</li>
      </ol>
    </nav>
    <h1>{{ .Title }}</h1>
  </div>
</div>
<div class="container py-4">
  <div class="row">
    <div class="col-lg-10 mx-auto">
      {{ .Content }}
      <div class="row mt-4 fade-in-up">
        {{ range .Pages }}
        <div class="col-lg-4 col-md-6 mb-4">
          <div class="card card-servizio shadow-sm h-100">
            <div class="card-body p-4 text-center">
              {{ if in .Title "Incendi" }}<div class="servizio-icon si-orange mx-auto"><i class="bi bi-fire" aria-hidden="true"></i></div>
              {{ else if in .Title "Idrogeologico" }}<div class="servizio-icon si-blue mx-auto"><i class="bi bi-cloud-rain-heavy" aria-hidden="true"></i></div>
              {{ else }}<div class="servizio-icon si-orange mx-auto"><i class="bi bi-tsunami" aria-hidden="true"></i></div>{{ end }}
              <h2 class="h5 mt-2">{{ .Title }}</h2>
              <p class="text-muted small">{{ .Description }}</p>
              <a href="{{ .Permalink }}" class="notizia-link">Approfondisci <i class="bi bi-arrow-right" aria-hidden="true"></i></a>
            </div>
          </div>
        </div>
        {{ end }}
      </div>
    </div>
  </div>
</div>
{{ end }}
HTMLEOF

# ── 6. COMMIT E PUSH ──
echo "📤 Pubblicazione..."
git add -A
git commit -m "🎨 Migliorie grafiche v6: hero pattern, page-hero, quick actions grandi, icone circolari, pulse allerta, footer"
git push

echo ""
echo "============================================"
echo "  ✅ MIGLIORIE GRAFICHE v6 COMPLETATE!"
echo "============================================"
echo ""
echo "  ✓ Hero con pattern geometrico e titolo bicolore"
echo "  ✓ Mini hero blu su tutte le pagine interne"
echo "  ✓ Quick Actions con icone circolari colorate"
echo "  ✓ Card servizi con icone circolari su sfondo"
echo "  ✓ Effetto pulse sulla barra allerta (gialla/arancione/rossa)"
echo "  ✓ Separatori verticali tra le statistiche"
echo "  ✓ Footer con due fasce (blu + blu scuro)"
echo "  ✓ Micro-interazioni migliorate (rotazione icone, zoom)"
echo "  ✓ Sottotitoli nelle quick actions"
echo "  ✓ Mobile ottimizzato"
echo "============================================"
