#!/bin/bash
# ============================================================
# SCRIPT DI AGGIORNAMENTO COMPLETO v3.0 — DEFINITIVO
# Protezione Civile Genzano di Roma — Sito Hugo
# Esegui con: bash aggiornamento-completo-v3.sh
#
# QUESTO FILE SOSTITUISCE I PRECEDENTI v1 e v2
# ============================================================

set -e
cd ~/sito-pc-genzano

echo "============================================"
echo "  AGGIORNAMENTO COMPLETO v3.0 DEL SITO"
echo "  Protezione Civile Genzano di Roma"
echo "============================================"
echo ""

# ── 0. PULL ──
echo "📥 Aggiornamento repository locale..."
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

# ── 1. IMMAGINE DI DEFAULT PER LE NOTIZIE (SVG) ──
echo "🖼️ Creazione immagine di default per le notizie..."
mkdir -p static/images
cat > static/images/notizia-default.svg << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#003366"/>
      <stop offset="100%" style="stop-color:#004080"/>
    </linearGradient>
  </defs>
  <rect width="800" height="400" fill="url(#bg)"/>
  <circle cx="650" cy="80" r="120" fill="rgba(255,255,255,0.03)"/>
  <circle cx="150" cy="350" r="80" fill="rgba(255,102,0,0.05)"/>
  <text x="400" y="170" font-family="Arial,sans-serif" font-size="48" fill="rgba(255,255,255,0.9)" text-anchor="middle" font-weight="700">PROTEZIONE CIVILE</text>
  <text x="400" y="220" font-family="Arial,sans-serif" font-size="24" fill="rgba(255,255,255,0.6)" text-anchor="middle">Genzano di Roma</text>
  <text x="400" y="280" font-family="Arial,sans-serif" font-size="16" fill="rgba(255,255,255,0.4)" text-anchor="middle">Gruppo Comunale Volontari</text>
  <line x1="350" y1="240" x2="450" y2="240" stroke="#FF6600" stroke-width="3"/>
</svg>
SVGEOF

# ── 2. CSS COMPLETO v3 ──
echo "🎨 Aggiornamento CSS completo v3..."
cat > themes/flavour-pcgenzano/static/css/custom.css << 'CSSEOF'
/* ============================================================
   CSS v3.0 — Protezione Civile Genzano di Roma
   Best-in-class per siti di protezione civile italiani
   ============================================================ */

:root {
  --pc-primary: #003366;
  --pc-primary-dark: #001a33;
  --pc-primary-light: #004080;
  --pc-secondary: #FF6600;
  --pc-accent: #009246;
  --pc-danger: #dc3545;
  --pc-light-bg: #f0f2f5;
  --pc-card-shadow: 0 2px 8px rgba(0,0,0,0.08);
  --pc-card-shadow-hover: 0 8px 24px rgba(0,0,0,0.12);
  --pc-radius: 8px;
}

/* ── HERO ── */
.hero-section {
  background: linear-gradient(135deg, var(--pc-primary-dark) 0%, var(--pc-primary) 40%, var(--pc-primary-light) 100%);
  color: #fff;
  padding: 4rem 0 5rem;
  position: relative;
  overflow: hidden;
}
.hero-section::before {
  content: '';
  position: absolute;
  top: -30%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-section::after {
  content: '';
  position: absolute;
  bottom: -20%;
  left: -5%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(255,102,0,0.06) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-section h1 {
  font-size: 2.5rem;
  font-weight: 700;
  position: relative;
  z-index: 1;
  margin-bottom: 1rem;
}
.hero-section .lead {
  font-size: 1.15rem;
  opacity: 0.9;
  position: relative;
  z-index: 1;
  max-width: 600px;
}
.hero-section .btn { position: relative; z-index: 1; }
@media (max-width: 768px) {
  .hero-section h1 { font-size: 1.75rem; }
  .hero-section { padding: 3rem 0; }
}

/* ── EMERGENCY BANNER ── */
.emergency-banner {
  background: var(--pc-danger);
  color: #fff;
  padding: 0.6rem 0;
  font-size: 0.9rem;
}
.emergency-banner a { color: #fff; font-weight: 700; }

/* ── STATS ── */
.stats-section {
  background: var(--pc-primary);
  color: #fff;
  padding: 2.5rem 0;
}
.stat-item { text-align: center; padding: 1rem; }
.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  display: block;
  line-height: 1;
  margin-bottom: 0.25rem;
}
.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.75;
}

/* ── ALLERTA STATUS CARD ── */
.allerta-status-card {
  border-radius: var(--pc-radius);
  overflow: hidden;
  border: 2px solid #e9ecef;
}
.allerta-status-header {
  padding: 0.75rem 1rem;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.allerta-verde { background: #28a745; color: #fff; }
.allerta-gialla { background: #ffc107; color: #000; }
.allerta-arancione { background: #fd7e14; color: #fff; }
.allerta-rossa { background: #dc3545; color: #fff; }

/* ── SECTIONS ── */
.servizi-section { background-color: var(--pc-light-bg); padding: 3.5rem 0; }
.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--pc-primary);
  margin-bottom: 2rem;
  position: relative;
  padding-bottom: 0.75rem;
}
.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: var(--pc-secondary);
  border-radius: 2px;
}
.section-title.text-center::after {
  left: 50%;
  transform: translateX(-50%);
}

/* ── CARD SERVIZI ── */
.card-servizio {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: var(--pc-radius);
  background: #fff;
}
.card-servizio:hover {
  transform: translateY(-4px);
  box-shadow: var(--pc-card-shadow-hover);
}

/* ── NOTIZIE STILE COMUNI ── */
.notizie-section { padding: 3.5rem 0; background: #fff; }

.card-notizia {
  border: none;
  border-radius: 0;
  border-left: 4px solid var(--pc-primary);
  transition: all 0.2s ease;
  overflow: hidden;
}
.card-notizia:hover {
  border-left-color: var(--pc-secondary);
  box-shadow: var(--pc-card-shadow-hover);
}

.notizia-img-wrapper {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: var(--pc-primary);
}
.notizia-img-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.notizia-categoria {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.6rem;
  border-radius: 3px;
}
.notizia-categoria.allerta { background: #dc3545; color: #fff; }
.notizia-categoria.avviso { background: #ffc107; color: #000; }
.notizia-categoria.evento { background: var(--pc-accent); color: #fff; }
.notizia-categoria.comunicazione { background: var(--pc-primary); color: #fff; }

.notizia-data { font-size: 0.8rem; color: #6c757d; }
.notizia-data i { margin-right: 0.25rem; }

.notizia-titolo { font-size: 1.05rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.4rem; }
.notizia-titolo a { color: inherit; text-decoration: none; }
.notizia-titolo a:hover { color: var(--pc-primary); }

.notizia-excerpt { font-size: 0.88rem; color: #555; line-height: 1.5; }

.notizia-link {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--pc-primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}
.notizia-link:hover { color: var(--pc-secondary); }

/* ── NOTIZIA CON IMMAGINE (lista home) ── */
.card-notizia-featured {
  border: none;
  border-radius: var(--pc-radius);
  overflow: hidden;
  transition: all 0.2s ease;
  box-shadow: var(--pc-card-shadow);
}
.card-notizia-featured:hover {
  box-shadow: var(--pc-card-shadow-hover);
  transform: translateY(-2px);
}

/* ── BADGES ALLERTE ── */
.badge-allerta-verde { background: #28a745; color: #fff; padding: 0.5em 1em; font-size: 0.85rem; border-radius: 4px; }
.badge-allerta-gialla { background: #ffc107; color: #000; padding: 0.5em 1em; font-size: 0.85rem; border-radius: 4px; }
.badge-allerta-arancione { background: #fd7e14; color: #fff; padding: 0.5em 1em; font-size: 0.85rem; border-radius: 4px; }
.badge-allerta-rossa { background: #dc3545; color: #fff; padding: 0.5em 1em; font-size: 0.85rem; border-radius: 4px; }

/* ── TIMELINE ── */
.timeline-wrapper { position: relative; padding-left: 1rem; }
.timeline-item {
  position: relative;
  padding-left: 2rem;
  margin-bottom: 1.5rem;
  border-left: 3px solid var(--pc-primary);
  padding-bottom: 0.5rem;
}
.timeline-item::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 4px;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: var(--pc-primary);
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px var(--pc-primary);
}

/* ── TABLES ── */
table { width: 100%; margin-bottom: 1rem; border-collapse: collapse; }
table th { background: var(--pc-primary); color: #fff; padding: 0.75rem 1rem; font-weight: 600; font-size: 0.9rem; }
table td { padding: 0.75rem 1rem; border-bottom: 1px solid #e9ecef; font-size: 0.9rem; }
table tr:nth-child(even) { background: #f8f9fa; }
table tr:hover { background: #e8f4fd; }

/* ── BACK TO TOP ── */
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 48px;
  height: 48px;
  background: var(--pc-primary);
  color: #fff;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 999;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.back-to-top.visible { opacity: 1; visibility: visible; }
.back-to-top:hover { background: var(--pc-secondary); transform: translateY(-3px); }

/* ── ANIMATIONS ── */
.fade-in-up {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.fade-in-up.visible { opacity: 1; transform: translateY(0); }

/* ── SOCIAL SIDEBAR ── */
.card-social-link {
  border: 1px solid #e9ecef;
  border-radius: var(--pc-radius);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #333;
  padding: 0.75rem 1rem;
}
.card-social-link:hover { border-color: var(--pc-primary); box-shadow: var(--pc-card-shadow); color: #333; }

/* ── QUICK ACTIONS (Cosa fare in caso di...) ── */
.quick-action-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: var(--pc-radius);
  padding: 1.25rem;
  text-align: center;
  transition: all 0.2s ease;
  text-decoration: none;
  color: #333;
  display: block;
}
.quick-action-card:hover {
  border-color: var(--pc-primary);
  box-shadow: var(--pc-card-shadow-hover);
  color: var(--pc-primary);
  transform: translateY(-2px);
}
.quick-action-card i { font-size: 2rem; margin-bottom: 0.5rem; display: block; }

/* ── 404 ── */
.page-404 { text-align: center; padding: 5rem 0; }
.page-404 h1 { font-size: 6rem; font-weight: 700; color: var(--pc-primary); margin-bottom: 0; }
.page-404 h2 { font-size: 1.5rem; color: #555; margin-bottom: 2rem; }

/* ── FOOTER ── */
.footer-list { list-style: none; padding: 0; margin: 0; }
.footer-list li { margin-bottom: 0.5rem; }
.footer-list .list-item { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 0.9rem; }
.footer-list .list-item:hover { color: #fff; }

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
}
.skip-to-content:focus { top: 0; }

/* ── SEARCH ── */
#search-results .search-result-item { padding: 1rem 0; border-bottom: 1px solid #eee; }
#search-results .search-result-item h3 a { color: var(--pc-primary); }

/* ── PRINT ── */
@media print {
  .navbar, footer, .cookiebar, .skip-to-content, .it-header-slim-wrapper,
  .it-header-navbar-wrapper, .back-to-top, .emergency-banner, .stats-section {
    display: none !important;
  }
  .hero-section { background: #fff !important; color: #000 !important; padding: 1rem 0; }
}
CSSEOF

# ── 3. HOME PAGE v3 ──
echo "🏠 Home Page v3 con tutte le migliorie..."
cat > themes/flavour-pcgenzano/layouts/index.html << 'HTMLEOF'
{{ define "main" }}

<!-- BANNER EMERGENZA — Solo 112 e 803 555 -->
<div class="emergency-banner" role="complementary" aria-label="Numeri di emergenza">
  <div class="container text-center">
    <i class="bi bi-telephone-fill me-1" aria-hidden="true"></i>
    <strong>Emergenze: 112</strong>
    <span class="mx-2 d-none d-md-inline">|</span>
    <span class="d-block d-md-inline">Sala Operativa PC Lazio: <strong>803 555</strong></span>
  </div>
</div>

<!-- HERO -->
<section class="hero-section" aria-label="Benvenuto">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-8">
        <h1>Protezione Civile Genzano di Roma</h1>
        <p class="lead">Il sito ufficiale del Gruppo Comunale Volontari. Qui trovi informazioni, allerte meteo, buone pratiche e i contatti per la sicurezza del nostro territorio.</p>
        <div class="mt-4">
          <a href="{{ "allerte-meteo/" | relURL }}" class="btn btn-warning btn-lg me-2 mb-2">
            <i class="bi bi-exclamation-triangle-fill me-1" aria-hidden="true"></i> Allerte Meteo
          </a>
          <a href="{{ "piano-emergenza/" | relURL }}" class="btn btn-outline-light btn-lg me-2 mb-2">Piano di Emergenza</a>
          <a href="{{ "diventa-volontario/" | relURL }}" class="btn btn-outline-light btn-lg mb-2">Diventa Volontario</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- STATISTICHE -->
<section class="stats-section" aria-label="Il gruppo in numeri">
  <div class="container">
    <div class="row">
      <div class="col-6 col-md-3">
        <div class="stat-item"><span class="stat-number" data-count="44">0</span><span class="stat-label">Anni di attivita</span></div>
      </div>
      <div class="col-6 col-md-3">
        <div class="stat-item"><span class="stat-number" data-count="8">0</span><span class="stat-label">Automezzi operativi</span></div>
      </div>
      <div class="col-6 col-md-3">
        <div class="stat-item"><span class="stat-number" data-count="20">0</span><span class="stat-label">Emergenze nazionali</span></div>
      </div>
      <div class="col-6 col-md-3">
        <div class="stat-item"><span class="stat-number" data-count="365">0</span><span class="stat-label">Giorni di disponibilita</span></div>
      </div>
    </div>
  </div>
</section>

<!-- COSA FARE IN CASO DI... (Quick Actions) -->
<section class="py-4 bg-white fade-in-up" aria-labelledby="quickactions-heading">
  <div class="container">
    <h2 id="quickactions-heading" class="section-title text-center">Cosa fare in caso di...</h2>
    <div class="row mt-3">
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "rischi-prevenzione/rischio-sismico/" | relURL }}" class="quick-action-card">
          <i class="bi bi-tsunami text-warning" aria-hidden="true"></i>
          <strong>Terremoto</strong>
        </a>
      </div>
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "rischi-prevenzione/rischio-idrogeologico/" | relURL }}" class="quick-action-card">
          <i class="bi bi-cloud-rain-heavy text-primary" aria-hidden="true"></i>
          <strong>Alluvione</strong>
        </a>
      </div>
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "rischi-prevenzione/rischio-incendio/" | relURL }}" class="quick-action-card">
          <i class="bi bi-fire text-danger" aria-hidden="true"></i>
          <strong>Incendio</strong>
        </a>
      </div>
      <div class="col-6 col-md-3 mb-3">
        <a href="{{ "piano-familiare/" | relURL }}" class="quick-action-card">
          <i class="bi bi-house-heart text-success" aria-hidden="true"></i>
          <strong>Piano Familiare</strong>
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
            <i class="bi bi-house-heart fs-1 text-primary mb-3 d-block" aria-hidden="true"></i>
            <h3 class="h6">Piano Familiare</h3>
            <p class="text-muted small">Crea il piano di emergenza per la tua famiglia.</p>
            <a href="{{ "piano-familiare/" | relURL }}" class="btn btn-outline-primary btn-sm">Crea il piano</a>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-4">
        <div class="card card-servizio shadow-sm h-100">
          <div class="card-body text-center p-4">
            <i class="bi bi-exclamation-triangle fs-1 text-warning mb-3 d-block" aria-hidden="true"></i>
            <h3 class="h6">Rischi e Prevenzione</h3>
            <p class="text-muted small">Conosci i rischi del territorio.</p>
            <a href="{{ "rischi-prevenzione/" | relURL }}" class="btn btn-outline-primary btn-sm">Scopri</a>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-4">
        <div class="card card-servizio shadow-sm h-100">
          <div class="card-body text-center p-4">
            <i class="bi bi-map fs-1 text-info mb-3 d-block" aria-hidden="true"></i>
            <h3 class="h6">Cartografia Operativa</h3>
            <p class="text-muted small">Aree di emergenza del Piano Comunale.</p>
            <a href="{{ "cartografia/" | relURL }}" class="btn btn-outline-primary btn-sm">Consulta</a>
          </div>
        </div>
      </div>
      <div class="col-lg-3 col-md-6 mb-4">
        <div class="card card-servizio shadow-sm h-100">
          <div class="card-body text-center p-4">
            <i class="bi bi-download fs-1 text-success mb-3 d-block" aria-hidden="true"></i>
            <h3 class="h6">Area Download</h3>
            <p class="text-muted small">Documenti e modulistica ufficiale.</p>
            <a href="{{ "area-download/" | relURL }}" class="btn btn-outline-primary btn-sm">Scarica</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- NOTIZIE + SIDEBAR -->
<section class="notizie-section fade-in-up" aria-labelledby="notizie-heading">
  <div class="container">
    <div class="row">
      <div class="col-lg-8">
        <h2 id="notizie-heading" class="section-title">Ultime Notizie</h2>
        {{ range first 5 (where .Site.RegularPages "Section" "comunicazioni") }}
        <article class="card card-notizia mb-3">
          <div class="row g-0">
            <div class="col-md-4 d-none d-md-block">
              <div class="notizia-img-wrapper">
                {{ with .Params.image }}
                <img src="{{ . }}" alt="" loading="lazy">
                {{ else }}
                <img src="{{ "images/notizia-default.svg" | relURL }}" alt="" loading="lazy">
                {{ end }}
              </div>
            </div>
            <div class="col-md-8">
              <div class="card-body">
                <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
                  {{ with .Params.badge }}
                  <span class="notizia-categoria {{ . | lower }}">{{ . }}</span>
                  {{ end }}
                  <span class="notizia-data">
                    <i class="bi bi-calendar3" aria-hidden="true"></i>
                    <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date | time.Format ":date_long" }}</time>
                  </span>
                </div>
                <h3 class="notizia-titolo"><a href="{{ .Permalink }}">{{ .Title }}</a></h3>
                <p class="notizia-excerpt">{{ .Summary | truncate 120 }}</p>
                <a href="{{ .Permalink }}" class="notizia-link">Leggi di piu <i class="bi bi-arrow-right" aria-hidden="true"></i></a>
              </div>
            </div>
          </div>
        </article>
        {{ end }}
        <div class="mt-4">
          <a href="{{ "comunicazioni/" | relURL }}" class="btn btn-outline-primary">Tutte le comunicazioni <i class="bi bi-arrow-right ms-1" aria-hidden="true"></i></a>
        </div>
      </div>
      <!-- SIDEBAR -->
      <div class="col-lg-4 mt-4 mt-lg-0">
        <!-- Stato allerta -->
        <div class="allerta-status-card mb-4">
          <div class="allerta-status-header allerta-verde">
            <i class="bi bi-shield-check me-1" aria-hidden="true"></i> Stato Allerta: NESSUNA ALLERTA
          </div>
          <div class="p-3">
            <p class="small mb-2">Controlla sempre il bollettino ufficiale della Regione Lazio per aggiornamenti.</p>
            <a href="https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary w-100">Vai al Bollettino Ufficiale</a>
          </div>
        </div>

        <!-- Social -->
        <h3 class="h6 fw-bold mb-3">Seguici</h3>
        <a href="https://www.facebook.com/protezionecivilegenzanodiroma" target="_blank" rel="noopener noreferrer" class="card-social-link mb-2">
          <i class="bi bi-facebook fs-4 text-primary me-3" aria-hidden="true"></i>
          <div><strong>Facebook</strong><div class="small text-muted">Notizie e aggiornamenti</div></div>
        </a>
        <a href="https://www.instagram.com/protezionecivilegenzano/" target="_blank" rel="noopener noreferrer" class="card-social-link mb-2">
          <i class="bi bi-instagram fs-4 text-danger me-3" aria-hidden="true"></i>
          <div><strong>Instagram</strong><div class="small text-muted">Foto e storie dal campo</div></div>
        </a>
        <a href="https://t.me/pcalfagenzano" target="_blank" rel="noopener noreferrer" class="card-social-link mb-2">
          <i class="bi bi-telegram fs-4 text-info me-3" aria-hidden="true"></i>
          <div><strong>Telegram</strong><div class="small text-muted">Allerte in tempo reale</div></div>
        </a>
        <a href="https://x.com/alfagenzano" target="_blank" rel="noopener noreferrer" class="card-social-link mb-3">
          <i class="bi bi-twitter-x fs-4 me-3" aria-hidden="true"></i>
          <div><strong>X (Twitter)</strong><div class="small text-muted">Aggiornamenti rapidi</div></div>
        </a>

        <!-- IT-alert -->
        <div class="card bg-warning bg-opacity-10 border-warning mt-3">
          <div class="card-body p-3">
            <h3 class="h6 fw-bold"><i class="bi bi-phone-vibrate text-warning me-1" aria-hidden="true"></i> IT-alert</h3>
            <p class="small mb-2">Il sistema nazionale di allarme pubblico che invia messaggi sul tuo telefono in caso di gravi emergenze.</p>
            <a href="https://www.it-alert.it/it/" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-warning w-100">Scopri IT-alert</a>
          </div>
        </div>

        <!-- Numeri utili -->
        <div class="card bg-light border-0 mt-3">
          <div class="card-body p-3">
            <h3 class="h6 fw-bold"><i class="bi bi-telephone-fill text-danger me-1" aria-hidden="true"></i> Numeri Utili</h3>
            <ul class="list-unstyled small mb-0">
              <li class="mb-1"><strong>112</strong> — Numero Unico Emergenza</li>
              <li><strong>803 555</strong> — Sala Operativa PC Lazio</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- METEO -->
<section class="servizi-section py-5 fade-in-up" aria-labelledby="meteo-heading">
  <div class="container">
    <h2 id="meteo-heading" class="section-title">Meteo e Rischi in Tempo Reale</h2>
    <p><strong>Suggerimento:</strong> Clicca sull'icona delle opzioni per accedere a mappe e scenari diversi.</p>
    <div class="ratio ratio-16x9">
      <iframe src="https://embed.windy.com/embed.html?type=map&location=coordinates&metricRain=mm&metricTemp=%C2%B0C&metricWind=km/h&zoom=10&overlay=rain&product=ecmwf&level=surface&lat=41.71&lon=12.69" title="Mappa meteo interattiva per Genzano di Roma" loading="lazy" allowfullscreen></iframe>
    </div>
  </div>
</section>

{{ end }}

{{ define "scripts" }}
<script>
// Animazione contatori
(function(){
  var counters=document.querySelectorAll('[data-count]');
  if(!counters.length)return;
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting)return;
      var el=e.target;
      var target=parseInt(el.getAttribute('data-count'));
      var duration=1500;
      var start=0;
      var step=Math.ceil(target/60);
      var timer=setInterval(function(){
        start+=step;
        if(start>=target){start=target;clearInterval(timer)}
        el.textContent=start+(target===20?'+':'');
      },duration/60);
      obs.unobserve(el);
    });
  },{threshold:0.5});
  counters.forEach(function(c){obs.observe(c)});
})();
</script>
{{ end }}
HTMLEOF

# ── 4. BASEOF v3 CON BACK TO TOP + SCROLL + OG IMAGE ──
echo "🔝 Base template con Back to Top, animazioni, favicon..."
cat > themes/flavour-pcgenzano/layouts/_default/baseof.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ if not .IsHome }}{{ .Title }} — {{ end }}{{ .Site.Title }}</title>
  <meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
  <meta name="author" content="{{ .Site.Params.author }}">
  <meta property="og:title" content="{{ .Title }}">
  <meta property="og:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
  <meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
  <meta property="og:url" content="{{ .Permalink }}">
  <meta property="og:locale" content="it_IT">
  <meta property="og:site_name" content="{{ .Site.Title }}">
  <meta property="og:image" content="{{ "images/notizia-default.svg" | absURL }}">
  <link rel="icon" type="image/png" href="{{ "images/logo-pc-genzano.png" | relURL }}">
  <link rel="apple-touch-icon" href="{{ "images/logo-pc-genzano.png" | relURL }}">
  <link rel="stylesheet" href="{{ "vendor/bootstrap-italia/css/bootstrap-italia.min.css" | relURL }}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <link rel="stylesheet" href="{{ "css/custom.css" | relURL }}">
  <link rel="canonical" href="{{ .Permalink }}">
</head>
<body>
  <a class="skip-to-content" href="#main-content">Vai al contenuto principale</a>
  {{ partial "slim-header.html" . }}
  {{ partial "navbar.html" . }}
  <main id="main-content" tabindex="-1">
    {{ block "main" . }}{{ end }}
  </main>
  {{ partial "footer.html" . }}
  {{ partial "cookie-banner.html" . }}
  <button class="back-to-top" id="backToTop" aria-label="Torna in cima alla pagina" title="Torna su">
    <i class="bi bi-arrow-up" aria-hidden="true"></i>
  </button>
  <script src="{{ "vendor/bootstrap-italia/js/bootstrap-italia.bundle.min.js" | relURL }}"></script>
  <script>
    // Back to top
    (function(){var b=document.getElementById('backToTop');window.addEventListener('scroll',function(){b.classList.toggle('visible',window.scrollY>300)});b.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})})})();
    // Scroll animations
    (function(){var e=document.querySelectorAll('.fade-in-up');if(!e.length)return;var o=new IntersectionObserver(function(entries){entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('visible');o.unobserve(en.target)}})},{threshold:0.1});e.forEach(function(el){o.observe(el)})})();
  </script>
  {{ block "scripts" . }}{{ end }}
</body>
</html>
HTMLEOF

# ── 5. TEMPLATE SINGLE v3 ──
echo "📄 Template pagina singola v3..."
cat > themes/flavour-pcgenzano/layouts/_default/single.html << 'HTMLEOF'
{{ define "main" }}
<div class="container py-5">
  <div class="row">
    <div class="col-lg-8 mx-auto">
      <nav aria-label="Percorso di navigazione">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="{{ "/" | relURL }}">Home</a></li>
          {{ if and .Parent (not .Parent.IsHome) (ne .Parent.Permalink .Permalink) }}
          <li class="breadcrumb-item"><a href="{{ .Parent.Permalink }}">{{ .Parent.Title }}</a></li>
          {{ end }}
          <li class="breadcrumb-item active" aria-current="page">{{ .Title }}</li>
        </ol>
      </nav>

      {{ if and .Date (not (eq (.Date.Format "2006") "0001")) }}
      {{ with .Params.image }}
      <div class="notizia-img-wrapper mb-4" style="height:250px;border-radius:8px;">
        <img src="{{ . }}" alt="" loading="lazy">
      </div>
      {{ else }}
      {{ if eq $.Section "comunicazioni" }}
      <div class="notizia-img-wrapper mb-4" style="height:250px;border-radius:8px;">
        <img src="{{ "images/notizia-default.svg" | relURL }}" alt="" loading="lazy">
      </div>
      {{ end }}
      {{ end }}
      {{ end }}

      <h1>{{ .Title }}</h1>
      {{ with .Params.subtitle }}<p class="lead">{{ . }}</p>{{ end }}
      {{ if and .Date (not (eq (.Date.Format "2006") "0001")) }}
      <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
        {{ with .Params.badge }}
        <span class="notizia-categoria {{ . | lower }}">{{ . }}</span>
        {{ end }}
        <span class="notizia-data">
          <i class="bi bi-calendar3" aria-hidden="true"></i>
          <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date | time.Format ":date_long" }}</time>
        </span>
      </div>
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

# ── 6. TEMPLATE LISTA v3 ──
echo "📰 Template lista v3..."
cat > themes/flavour-pcgenzano/layouts/_default/list.html << 'HTMLEOF'
{{ define "main" }}
<div class="container py-5">
  <div class="row">
    <div class="col-lg-8 mx-auto">
      <nav aria-label="Percorso di navigazione">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="{{ "/" | relURL }}">Home</a></li>
          <li class="breadcrumb-item active" aria-current="page">{{ .Title }}</li>
        </ol>
      </nav>
      <h1 class="section-title">{{ .Title }}</h1>
      {{ .Content }}
      {{ range .Paginator.Pages }}
      <article class="card card-notizia mb-3">
        <div class="row g-0">
          <div class="col-md-3 d-none d-md-block">
            <div class="notizia-img-wrapper" style="height:100%;min-height:140px;">
              {{ with .Params.image }}
              <img src="{{ . }}" alt="" loading="lazy">
              {{ else }}
              <img src="{{ "images/notizia-default.svg" | relURL }}" alt="" loading="lazy">
              {{ end }}
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
              <p class="notizia-excerpt">{{ .Summary | truncate 150 }}</p>
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

# ── 7. TEMPLATE RISCHI v3 ──
echo "⚠️ Template rischi v3..."
mkdir -p themes/flavour-pcgenzano/layouts/rischi-prevenzione
cat > themes/flavour-pcgenzano/layouts/rischi-prevenzione/list.html << 'HTMLEOF'
{{ define "main" }}
<div class="container py-5">
  <div class="row">
    <div class="col-lg-10 mx-auto">
      <nav aria-label="Percorso di navigazione">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="{{ "/" | relURL }}">Home</a></li>
          <li class="breadcrumb-item active" aria-current="page">{{ .Title }}</li>
        </ol>
      </nav>
      <h1 class="section-title">{{ .Title }}</h1>
      {{ .Content }}
      <div class="row mt-4 fade-in-up">
        {{ range .Pages }}
        <div class="col-lg-4 col-md-6 mb-4">
          <div class="card card-servizio shadow-sm h-100">
            <div class="card-body p-4">
              {{ if in .Title "Incendi" }}<i class="bi bi-fire fs-1 text-danger mb-3 d-block" aria-hidden="true"></i>
              {{ else if in .Title "Idrogeologico" }}<i class="bi bi-cloud-rain-heavy fs-1 text-primary mb-3 d-block" aria-hidden="true"></i>
              {{ else }}<i class="bi bi-tsunami fs-1 text-warning mb-3 d-block" aria-hidden="true"></i>{{ end }}
              <h2 class="h5">{{ .Title }}</h2>
              <p class="text-muted">{{ .Description }}</p>
              <a href="{{ .Permalink }}" class="notizia-link">Approfondisci <i class="bi bi-arrow-right" aria-hidden="true"></i></a>
            </div>
          </div>
        </div>
        {{ end }}
      </div>
      <div class="card shadow-sm mt-4 p-4 bg-light">
        <h2 class="h5 mb-3"><i class="bi bi-tools me-2" aria-hidden="true"></i>Strumenti di Prevenzione</h2>
        <div class="row">
          <div class="col-md-4 mb-2"><a href="{{ "piano-emergenza/" | relURL }}"><i class="bi bi-file-earmark-text me-1"></i> Piano di Emergenza</a></div>
          <div class="col-md-4 mb-2"><a href="{{ "piano-familiare/" | relURL }}"><i class="bi bi-house-heart me-1"></i> Piano Familiare</a></div>
          <div class="col-md-4 mb-2"><a href="{{ "allerte-meteo/" | relURL }}"><i class="bi bi-cloud-lightning me-1"></i> Allertamento Meteo</a></div>
          <div class="col-md-4 mb-2"><a href="{{ "cartografia/" | relURL }}"><i class="bi bi-map me-1"></i> Cartografia Operativa</a></div>
          <div class="col-md-4 mb-2"><a href="{{ "area-download/" | relURL }}"><i class="bi bi-download me-1"></i> Area Download</a></div>
        </div>
      </div>
    </div>
  </div>
</div>
{{ end }}
HTMLEOF

# ── 8. PAGINA 404 ──
echo "🚫 Pagina 404..."
mkdir -p layouts
cat > layouts/404.html << 'HTMLEOF'
{{ define "main" }}
<div class="page-404">
  <div class="container">
    <h1>404</h1>
    <h2>Pagina non trovata</h2>
    <p class="text-muted mb-4">La pagina che stai cercando non esiste o e stata spostata.</p>
    <div class="d-flex flex-wrap justify-content-center gap-3">
      <a href="{{ "/" | relURL }}" class="btn btn-primary btn-lg"><i class="bi bi-house me-1" aria-hidden="true"></i> Torna alla Home</a>
      <a href="{{ "contatti/" | relURL }}" class="btn btn-outline-primary btn-lg"><i class="bi bi-envelope me-1" aria-hidden="true"></i> Contattaci</a>
    </div>
    <p class="text-muted mt-5">Emergenze: <strong>112</strong> — Sala Operativa PC Lazio: <strong>803 555</strong></p>
  </div>
</div>
{{ end }}
HTMLEOF

# ── 9. ROBOTS.TXT ──
echo "🤖 robots.txt..."
cat > static/robots.txt << 'EOF'
User-agent: *
Allow: /

Sitemap: https://sviluppoitaliadigitale.github.io/sito-pc-genzano/sitemap.xml
EOF

# ── 10. NOTIZIE CON IMMAGINE DEFAULT ──
echo "📝 Aggiornamento notizie..."
cat > content/comunicazioni/2025-10-14-io-non-rischio.md << 'EOF'
---
title: "Io Non Rischio 2025 - Genzano in piazza"
date: 2025-10-14
badge: "Evento"
description: "I volontari del Gruppo in Piazza Tommaso Frasconi per la campagna nazionale Io Non Rischio."
---

Sabato 14 e Domenica 15 Ottobre 2025 il nostro Gruppo partecipa alle giornate nazionali della campagna **"Io non rischio — Buone pratiche di protezione civile"**.

L'appuntamento con i nostri volontari e in **Piazza Tommaso Frasconi — Genzano di Roma**.

Vieni a scoprire come ciascuno di noi puo contribuire a ridurre i rischi del territorio!
EOF

cat > content/comunicazioni/2025-06-15-campagna-aib.md << 'EOF'
---
title: "Avvio Campagna Antincendio Boschivo 2025"
date: 2025-06-15
badge: "Allerta"
description: "Dal 15 giugno al 30 settembre il territorio e in stato di massima allerta per il rischio incendi."
---

Con l'arrivo della stagione estiva si intensifica il rischio di incendi boschivi. Dal 15 giugno al 30 settembre e in vigore lo **stato di massima allerta** su tutto il territorio comunale.

In caso di avvistamento incendio, chiamare immediatamente il **112**.
EOF

cat > content/comunicazioni/2025-03-10-formazione-base.md << 'EOF'
---
title: "Corso di Formazione Base per nuovi volontari"
date: 2025-03-10
badge: "Comunicazione"
description: "A marzo parte il nuovo ciclo di formazione per i volontari appena iscritti al Gruppo."
---

Il Gruppo organizza un nuovo **Corso di Formazione Base** destinato ai volontari di recente iscrizione presso la sede di Via Sicilia.

Per informazioni e iscrizioni: [segreteria@protezionecivilegenzano.it](mailto:segreteria@protezionecivilegenzano.it)
EOF

cat > content/comunicazioni/2024-12-20-auguri-2025.md << 'EOF'
---
title: "Auguri di Buone Feste dal Gruppo"
date: 2024-12-20
badge: "Comunicazione"
description: "Il Coordinatore e il Consiglio Direttivo augurano buone feste a tutti."
---

Il Coordinatore Dario Iacoangeli e tutto il Consiglio Direttivo augurano a tutti i volontari, alle famiglie e ai cittadini un sereno Natale e un felice Anno Nuovo.
EOF

# ── 11. DIVENTA VOLONTARIO MIGLIORATA ──
echo "🤝 Pagina Diventa Volontario..."
cat > content/diventa-volontario/_index.md << 'EOF'
---
title: "Diventa Volontario"
description: "Unisciti al Gruppo Comunale di Protezione Civile di Genzano di Roma."
layout: "single"
---

<div class="card border-primary mb-4">
<div class="card-body bg-primary bg-opacity-10 p-4 text-center">
<i class="bi bi-heart-fill fs-1 text-primary d-block mb-3" aria-hidden="true"></i>
<h2 class="h4 text-primary">Metti il tuo tempo al servizio della comunita</h2>
<p class="mb-0">Entrare a far parte della Protezione Civile significa fare una scelta di cuore e di responsabilita. Significa mettere il proprio tempo e le proprie energie al servizio della comunita, per costruire un futuro piu sicuro per tutti.</p>
</div>
</div>

## Requisiti

- Aver compiuto il **16 anno di eta** (piena operativita al compimento del 18)
- Essere cittadino italiano, UE, o extracomunitario con regolare permesso di soggiorno
- Godere dei diritti civili e politici
- Non aver riportato condanne penali
- Avere una sana e robusta costituzione fisica (certificata dal medico)

## Percorso Formativo

Ogni nuovo volontario segue un **corso di formazione base obbligatorio** che fornisce le conoscenze essenziali sul Sistema di Protezione Civile, sui rischi del territorio e sulle procedure operative.

## Come Iscriversi

<div class="row mt-3">
<div class="col-md-4 mb-3">
<div class="card text-center p-3 h-100 shadow-sm">
<i class="bi bi-geo-alt fs-2 text-primary d-block mb-2" aria-hidden="true"></i>
<strong>Di persona</strong>
<p class="small text-muted mb-0">Via Sicilia, 13-15<br>Genzano di Roma</p>
</div>
</div>
<div class="col-md-4 mb-3">
<div class="card text-center p-3 h-100 shadow-sm">
<i class="bi bi-telephone fs-2 text-primary d-block mb-2" aria-hidden="true"></i>
<strong>Telefonicamente</strong>
<p class="small text-muted mb-0"><a href="tel:+39069362600">+39 069362600</a></p>
</div>
</div>
<div class="col-md-4 mb-3">
<div class="card text-center p-3 h-100 shadow-sm">
<i class="bi bi-envelope fs-2 text-primary d-block mb-2" aria-hidden="true"></i>
<strong>Via email</strong>
<p class="small text-muted mb-0"><a href="mailto:segreteria@protezionecivilegenzano.it">segreteria@protezionecivilegenzano.it</a></p>
</div>
</div>
</div>
EOF

# ── 12. FIX CONTATTI — solo 112 e 803 555 ──
echo "📞 Fix numeri emergenza nei Contatti..."
cat > content/contatti/_index.md << 'EOF'
---
title: "Contatti e Sede"
description: "Recapiti, mappa e modalita di attivazione in emergenza."
layout: "single"
---

Per informazioni, richieste non urgenti o per comunicazioni amministrative, questi sono i nostri recapiti.

## Recapiti Ordinari (NON per emergenze)

- **Sede:** Via Sicilia, 13-15 - 00045 Genzano Di Roma (RM)
- **Telefono Segreteria:** [+39 069362600](tel:+39069362600)
- **Email:** [segreteria@protezionecivilegenzano.it](mailto:segreteria@protezionecivilegenzano.it)
- **Links:** [Tutti i link web del Gruppo](https://linktr.ee/protezionecivilegenzano)

<div class="card border-danger mt-4 mb-4">
<div class="card-body bg-danger bg-opacity-10 p-4">
<h2 class="h4 text-danger fw-bold">ATTENZIONE: Come Attivarci in Caso di Emergenza</h2>
<p>Il Gruppo Comunale di Protezione Civile <strong>non puo essere attivato direttamente dai cittadini</strong>. Per garantire un coordinamento efficace dei soccorsi, il nostro intervento viene richiesto esclusivamente dalle autorita competenti.</p>
<p class="fw-bold mb-2">In caso di emergenza, contatta:</p>
<ul class="mb-2">
<li>Numero Unico di Emergenza: <strong>112</strong></li>
<li>Sala Operativa Protezione Civile Lazio: <strong>803 555</strong></li>
</ul>
<p class="mb-0">Saranno loro, una volta valutata la situazione, ad allertare e attivare le nostre squadre sul territorio.</p>
</div>
</div>

## Mappa della Sede

<div class="ratio ratio-16x9 mb-4">
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2978.5!2d12.6895!3d41.7075!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDHCsDQyJzI3LjAiTiAxMsKwNDEnMjIuMiJF!5e0!3m2!1sit!2sit!4v1" title="Mappa della sede" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe>
</div>
EOF

# ── 13. COMMIT E PUSH ──
echo ""
echo "📤 Salvataggio e pubblicazione..."
git add -A
git commit -m "✨ v3.0: Restyling definitivo — notizie con immagini, quick actions, IT-alert, stato allerta, contatori animati, solo 112/803555"
git push

echo ""
echo "============================================"
echo "  ✅ AGGIORNAMENTO v3.0 COMPLETATO!"
echo "============================================"
echo ""
echo "  Aspetta 2-3 minuti e verifica su:"
echo "  https://sviluppoitaliadigitale.github.io/sito-pc-genzano/"
echo ""
echo "  NOVITA v3.0:"
echo "  ✓ Solo 112 e 803 555 come numeri emergenza"
echo "  ✓ Immagine di default SVG per tutte le notizie"
echo "  ✓ Notizie con immagine affiancata (stile Comuni)"
echo "  ✓ Sezione 'Cosa fare in caso di...' con 4 quick actions"
echo "  ✓ Card 'Stato Allerta' nella sidebar (link al bollettino)"
echo "  ✓ Card IT-alert per promuovere il sistema di allarme"
echo "  ✓ Contatori animati che si incrementano allo scroll"
echo "  ✓ Open Graph image per condivisioni social"
echo "  ✓ Apple touch icon"
echo "  ✓ Pagina 404 personalizzata"
echo "  ✓ Pulsante Torna Su"
echo "  ✓ Animazioni scroll fade-in"
echo "  ✓ robots.txt per SEO"
echo "============================================"
