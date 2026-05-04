/**
 * Site Chrome — Layout condiviso per le app standalone
 * Inietta header e footer del sito principale nelle app
 * (quizpc, giochi, formazionepc)
 */
(function () {
  'use strict';

  var SITE_URL = 'https://www.protezionecivilegenzano.it';

  var HEADER_HTML =
    '<a class="skip-to-content" href="#main-content">Vai al contenuto principale</a>' +
    '<div class="it-header-slim-wrapper" role="banner">' +
      '<div class="container">' +
        '<div class="row"><div class="col-12">' +
          '<div class="it-header-slim-wrapper-content">' +
            '<div class="nav-mobile">' +
              '<nav aria-label="Navigazione enti istituzionali">' +
                '<a class="it-opener d-lg-none" data-bs-toggle="collapse" href="#menu-enti" role="button" aria-expanded="false" aria-controls="menu-enti"><span>Enti istituzionali</span><svg class="icon icon-sm"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand"></use></svg></a>' +
                '<div class="link-list-wrapper collapse" id="menu-enti"><ul class="link-list" role="list">' +
                  '<li role="listitem"><a class="dropdown-item list-item" href="https://www.comune.genzanodiroma.roma.it/" target="_blank" rel="noopener noreferrer" aria-label="Sito del Comune di Genzano di Roma (si apre in una nuova finestra)"><strong>Comune di Genzano di Roma</strong></a></li>' +
                  '<li role="listitem"><a class="dropdown-item list-item" href="https://www.protezionecivile.gov.it/it/" target="_blank" rel="noopener noreferrer">Dipartimento Nazionale Protezione Civile</a></li>' +
                  '<li role="listitem"><a class="dropdown-item list-item" href="https://protezionecivile.regione.lazio.it/" target="_blank" rel="noopener noreferrer">Agenzia Regionale Protezione Civile Lazio</a></li>' +
                '</ul></div>' +
              '</nav>' +
            '</div>' +
            '<div class="it-header-slim-right-zone" role="navigation" aria-label="Link rapidi e social">' +
              '<a href="' + SITE_URL + '/facile-da-leggere/" class="btn btn-slim-header btn-easy-read me-2" aria-label="Vai alla versione facile da leggere del sito"><i class="bi bi-book-half me-1" aria-hidden="true"></i><span class="d-none d-md-inline">Facile da leggere</span><span class="d-md-none">Aa</span></a>' +
              '<a href="https://activepager.com/auth/login" target="_blank" rel="noopener noreferrer" class="btn btn-slim-header me-3" aria-label="Accedi al gestionale volontari (si apre in una nuova finestra)"><i class="bi bi-box-arrow-in-right me-1" aria-hidden="true"></i><span class="d-none d-md-inline">Area Volontari</span><span class="d-md-none">Accedi</span></a>' +
              '<span class="slim-header-divider d-none d-lg-inline" aria-hidden="true"></span>' +
              '<a href="https://www.facebook.com/protezionecivilegenzanodiroma" target="_blank" rel="noopener noreferrer" aria-label="Facebook" class="text-white me-2"><i class="bi bi-facebook" aria-hidden="true"></i></a>' +
              '<a href="https://www.instagram.com/protezionecivilegenzano/" target="_blank" rel="noopener noreferrer" aria-label="Instagram" class="text-white me-2"><i class="bi bi-instagram" aria-hidden="true"></i></a>' +
              '<a href="https://x.com/alfagenzano" target="_blank" rel="noopener noreferrer" aria-label="X Twitter" class="text-white me-2"><i class="bi bi-twitter-x" aria-hidden="true"></i></a>' +
              '<a href="https://t.me/pcalfagenzano" target="_blank" rel="noopener noreferrer" aria-label="Telegram" class="text-white"><i class="bi bi-telegram" aria-hidden="true"></i></a>' +
            '</div>' +
          '</div>' +
        '</div></div>' +
      '</div>' +
    '</div>' +
    '<div class="it-header-center-wrapper">' +
      '<div class="container">' +
        '<div class="row"><div class="col-12">' +
          '<div class="it-header-center-content-wrapper">' +
            '<div class="it-brand-wrapper">' +
              '<a href="' + SITE_URL + '/" aria-label="Torna alla pagina iniziale">' +
                '<img src="' + SITE_URL + '/images/logo-pc-genzano.png" alt="" width="82" height="82" aria-hidden="true">' +
                '<div class="it-brand-text">' +
                  '<div class="it-brand-title">Protezione Civile</div>' +
                  '<div class="it-brand-tagline d-none d-md-block">Gruppo Comunale Volontari di Genzano di Roma</div>' +
                '</div>' +
              '</a>' +
            '</div>' +
            '<div class="it-right-zone">' +
              '<div class="it-search-wrapper">' +
                '<a class="search-link rounded-icon" href="' + SITE_URL + '/cerca/" aria-label="Cerca nel sito"><svg class="icon"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-search"></use></svg></a>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div></div>' +
      '</div>' +
    '</div>' +
    '<div class="it-header-navbar-wrapper">' +
      '<div class="container">' +
        '<div class="row"><div class="col-12">' +
          '<nav class="navbar navbar-expand-lg has-megamenu" aria-label="Navigazione principale">' +
            '<button class="custom-navbar-toggler" type="button" aria-controls="nav-main" aria-expanded="false" aria-label="Apri il menu di navigazione" data-bs-toggle="navbarcollapsible" data-bs-target="#nav-main"><svg class="icon"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-burger"></use></svg></button>' +
            '<div class="navbar-collapsable" id="nav-main">' +
              '<div class="overlay" style="display:none;"></div>' +
              '<div class="close-div"><button class="btn close-menu" type="button" aria-label="Chiudi il menu di navigazione"><span class="visually-hidden">Chiudi</span><svg class="icon"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-close-big"></use></svg></button></div>' +
              '<div class="menu-wrapper"><ul class="navbar-nav" role="menubar">' +
                /*
                 * IMPORTANTE: questo menu deve restare SEMPRE allineato a hugo.toml
                 * sezione [[menus.main]] e a themes/flavour-pcgenzano/layouts/partials/navbar.html.
                 * Il workflow audit-sito.yml § "Coerenza menu Hugo ↔ site-chrome.js"
                 * apre un'issue settimanale se trova drift.
                 */
                '<li class="nav-item" role="none"><a class="nav-link" href="' + SITE_URL + '/" role="menuitem"><span>Home</span></a></li>' +
                /* Dropdown: Per il Cittadino (7 voci, +Kit pronti maggio 2026) */
                '<li class="nav-item dropdown" role="none">' +
                  '<a class="nav-link dropdown-toggle" href="#" id="navDropdown-per-il-cittadino" role="menuitem" data-bs-toggle="dropdown" aria-expanded="false">' +
                    '<span>Per il Cittadino</span>' +
                    '<svg class="icon icon-xs"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand"></use></svg>' +
                  '</a>' +
                  '<div class="dropdown-menu" aria-labelledby="navDropdown-per-il-cittadino"><div class="link-list-wrapper"><ul class="link-list" role="menu">' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/cosa-fare-adesso/" role="menuitem"><span>Cosa Fare Adesso</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/allerte-meteo/" role="menuitem"><span>Allerte Meteo</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/rischi-prevenzione/" role="menuitem"><span>Rischi e Prevenzione</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/cartografia/" role="menuitem"><span>Cartografia</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/numeri-utili/" role="menuitem"><span>Numeri Utili</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/piano-familiare/" role="menuitem"><span>Piano Familiare</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/formazione/kit-calamita/" role="menuitem"><span>Kit pronti per situazioni vulnerabili</span></a></li>' +
                  '</ul></div></div>' +
                '</li>' +
                /* Dropdown: Per le scuole (6 voci didattiche, splittato da "Educazione e Inclusione" maggio 2026) */
                '<li class="nav-item dropdown" role="none">' +
                  '<a class="nav-link dropdown-toggle" href="#" id="navDropdown-per-le-scuole" role="menuitem" data-bs-toggle="dropdown" aria-expanded="false">' +
                    '<span>Per le scuole</span>' +
                    '<svg class="icon icon-xs"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand"></use></svg>' +
                  '</a>' +
                  '<div class="dropdown-menu" aria-labelledby="navDropdown-per-le-scuole"><div class="link-list-wrapper"><ul class="link-list" role="menu">' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/formazione/" role="menuitem"><span>Kit per le scuole</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/formazione/percorsi-didattici/" role="menuitem"><span>Percorsi didattici pronti</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/formazione/schede-stampabili/" role="menuitem"><span>Schede didattiche stampabili</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/formazione/educazione-civica/" role="menuitem"><span>Per i docenti — Ed. Civica</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/formazione/storie-e-racconti/" role="menuitem"><span>Storie e Racconti</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/giochi/" role="menuitem"><span>Giochi della Sicurezza</span></a></li>' +
                  '</ul></div></div>' +
                '</li>' +
                /* Dropdown: Accessibilità e Supporti (2 voci trasversali, nuovo maggio 2026) */
                '<li class="nav-item dropdown" role="none">' +
                  '<a class="nav-link dropdown-toggle" href="#" id="navDropdown-accessibilita-supporti" role="menuitem" data-bs-toggle="dropdown" aria-expanded="false">' +
                    '<span>Accessibilità e Supporti</span>' +
                    '<svg class="icon icon-xs"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand"></use></svg>' +
                  '</a>' +
                  '<div class="dropdown-menu" aria-labelledby="navDropdown-accessibilita-supporti"><div class="link-list-wrapper"><ul class="link-list" role="menu">' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/abili-a-proteggere/" role="menuitem"><span>Abili a Proteggere</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/facile-da-leggere/" role="menuitem"><span>Facile da Leggere</span></a></li>' +
                  '</ul></div></div>' +
                '</li>' +
                /* Dropdown: Volontariato */
                '<li class="nav-item dropdown" role="none">' +
                  '<a class="nav-link dropdown-toggle" href="#" id="navDropdown-volontariato" role="menuitem" data-bs-toggle="dropdown" aria-expanded="false">' +
                    '<span>Volontariato</span>' +
                    '<svg class="icon icon-xs"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand"></use></svg>' +
                  '</a>' +
                  '<div class="dropdown-menu" aria-labelledby="navDropdown-volontariato"><div class="link-list-wrapper"><ul class="link-list" role="menu">' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/diventa-volontario/" role="menuitem"><span>Diventa Volontario</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/chi-siamo/" role="menuitem"><span>Chi Siamo</span></a></li>' +
                  '</ul></div></div>' +
                '</li>' +
                /* Dropdown: Risorse (6 voci, +Glossario maggio 2026) */
                '<li class="nav-item dropdown" role="none">' +
                  '<a class="nav-link dropdown-toggle" href="#" id="navDropdown-risorse" role="menuitem" data-bs-toggle="dropdown" aria-expanded="false">' +
                    '<span>Risorse</span>' +
                    '<svg class="icon icon-xs"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand"></use></svg>' +
                  '</a>' +
                  '<div class="dropdown-menu" aria-labelledby="navDropdown-risorse"><div class="link-list-wrapper"><ul class="link-list" role="menu">' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/faq/" role="menuitem"><span>FAQ</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/strumenti/" role="menuitem"><span>Strumenti in Tempo Reale</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/area-download/" role="menuitem"><span>Area Download</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/normativa/" role="menuitem"><span>Normativa</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/glossario/" role="menuitem"><span>Glossario</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/mappa-sito/" role="menuitem"><span>Mappa del Sito</span></a></li>' +
                  '</ul></div></div>' +
                '</li>' +
                '<li class="nav-item" role="none"><a class="nav-link" href="' + SITE_URL + '/comunicazioni/" role="menuitem"><span>Comunicazioni</span></a></li>' +
                '<li class="nav-item" role="none"><a class="nav-link" href="' + SITE_URL + '/contatti/" role="menuitem"><span>Contatti</span></a></li>' +
              '</ul></div>' +
            '</div>' +
          '</nav>' +
        '</div></div>' +
      '</div>' +
    '</div>';

  var FOOTER_HTML =
    '<div class="utility-bar" aria-label="Informazioni di aggiornamento">' +
      '<div class="container">' +
        '<div class="d-flex flex-wrap justify-content-between align-items-center">' +
          '<div class="utility-bar-item"><i class="bi bi-clock me-1" aria-hidden="true"></i><span id="live-datetime" aria-live="polite" aria-label="Data e ora corrente"></span></div>' +
          '<div class="utility-bar-item"><i class="bi bi-arrow-repeat me-1" aria-hidden="true"></i><span id="site-build-time">Sito aggiornato</span></div>' +
        '</div>' +
      '</div>' +
    '</div>' +
    '<footer class="it-footer" id="footer" role="contentinfo">' +
      '<div class="it-footer-main">' +
        '<div class="container">' +
          '<section class="py-4"><div class="row">' +
            '<div class="col-lg-4 col-md-4 pb-2">' +
              '<h2 class="h4 text-white">Protezione Civile</h2>' +
              '<p class="text-white">Gruppo Comunale Volontari di Genzano di Roma</p>' +
              '<p style="color:rgba(255,255,255,0.85);"><strong>Sede:</strong> Via Sicilia, 13-15 - 00045 Genzano Di Roma (RM)<br><strong>Telefono:</strong> <a href="tel:+39069362600" class="text-white fw-bold">+39 06 9362600</a><br><strong>Email:</strong> <a href="mailto:segreteria@protezionecivilegenzano.it" class="text-white fw-bold">segreteria@protezionecivilegenzano.it</a></p>' +
              '<p class="small" style="color:rgba(255,255,255,0.75);">15&deg; C.O.I. Prov. di Roma &mdash; Registro Regionale P.C. n.184<br>Iscritta al RUNTS sez. &laquo;Altri Enti del Terzo Settore&raquo; con determina n. G14230 del 28/10/2024<br>Aderente al Coordinamento FEPIVOL</p>' +
            '</div>' +
            '<div class="col-lg-4 col-md-4 pb-2">' +
              '<h2 class="h4 text-white">Servizi</h2>' +
              '<nav aria-label="Servizi nel footer"><ul class="footer-list" role="list">' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/piano-emergenza/" style="color:rgba(255,255,255,0.85);">Piano di Emergenza</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/piano-familiare/" style="color:rgba(255,255,255,0.85);">Piano Familiare</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/area-download/" style="color:rgba(255,255,255,0.85);">Area Download</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/cartografia/" style="color:rgba(255,255,255,0.85);">Cartografia Operativa</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/cosa-fare-adesso/" style="color:rgba(255,255,255,0.85);">Cosa Fare Adesso</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/numeri-utili/" style="color:rgba(255,255,255,0.85);">Numeri Utili</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/formazione/" style="color:rgba(255,255,255,0.85);">Formazione</a></li>' +
              '</ul></nav>' +
            '</div>' +
            '<div class="col-lg-4 col-md-4 pb-2">' +
              '<h2 class="h4 text-white">Link Utili</h2>' +
              '<nav aria-label="Link utili nel footer"><ul class="footer-list" role="list">' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/note-legali/" style="color:rgba(255,255,255,0.85);">Note Legali</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/privacy/" style="color:rgba(255,255,255,0.85);">Privacy</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/accessibilita/" style="color:rgba(255,255,255,0.85);">Accessibilit&agrave;</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/siti-utili/" style="color:rgba(255,255,255,0.85);">Siti Utili</a></li>' +
              '</ul></nav>' +
              '<div class="mt-3">' +
                '<h3 class="h6 text-white">Seguici su</h3>' +
                '<ul class="list-inline" role="list">' +
                  '<li class="list-inline-item" role="listitem"><a href="https://www.facebook.com/protezionecivilegenzanodiroma" target="_blank" rel="noopener noreferrer" class="text-white" aria-label="Facebook"><i class="bi bi-facebook fs-4" aria-hidden="true"></i></a></li>' +
                  '<li class="list-inline-item" role="listitem"><a href="https://www.instagram.com/protezionecivilegenzano/" target="_blank" rel="noopener noreferrer" class="text-white" aria-label="Instagram"><i class="bi bi-instagram fs-4" aria-hidden="true"></i></a></li>' +
                  '<li class="list-inline-item" role="listitem"><a href="https://x.com/alfagenzano" target="_blank" rel="noopener noreferrer" class="text-white" aria-label="X Twitter"><i class="bi bi-twitter-x fs-4" aria-hidden="true"></i></a></li>' +
                  '<li class="list-inline-item" role="listitem"><a href="https://t.me/pcalfagenzano" target="_blank" rel="noopener noreferrer" class="text-white" aria-label="Telegram"><i class="bi bi-telegram fs-4" aria-hidden="true"></i></a></li>' +
                '</ul>' +
              '</div>' +
            '</div>' +
          '</div></section>' +
        '</div>' +
      '</div>' +
      '<div class="it-footer-small-prints clearfix">' +
        '<div class="container">' +
          '<h3 class="visually-hidden">Informazioni legali</h3>' +
          '<ul class="it-footer-small-prints-list list-inline mb-0 d-flex flex-column flex-md-row" role="list">' +
            '<li class="list-inline-item" role="listitem"><a href="' + SITE_URL + '/note-legali/" style="color:rgba(255,255,255,0.85);">Note legali</a></li>' +
            '<li class="list-inline-item" role="listitem"><a href="' + SITE_URL + '/privacy/" style="color:rgba(255,255,255,0.85);">Privacy e cookie</a></li>' +
            '<li class="list-inline-item" role="listitem"><a href="' + SITE_URL + '/accessibilita/" style="color:rgba(255,255,255,0.85);">Accessibilit&agrave;</a></li>' +
          '</ul>' +
          '<p class="mt-2 mb-0 small" style="color:rgba(255,255,255,0.75);">&copy; ' + new Date().getFullYear() + ' Gruppo Comunale Volontari di Protezione Civile Genzano di Roma &mdash; C.F. 92011880588<br>I contenuti di questo sito, salvo diversa indicazione, sono distribuiti con licenza <a href="https://creativecommons.org/licenses/by/4.0/deed.it" target="_blank" rel="noopener noreferrer license" style="color:rgba(255,255,255,0.85);">CC BY 4.0</a>.<br>Sito Web ideato e realizzato da Alessandro Cuollo - Alfa 19 - IU0QVW.</p>' +
        '</div>' +
      '</div>' +
    '</footer>' +
    '<button class="back-to-top" id="backToTop" aria-label="Torna in cima alla pagina" title="Torna su"><i class="bi bi-arrow-up" aria-hidden="true"></i></button>';

  function injectChrome() {
    var main = document.querySelector('main') || document.getElementById('main-content');
    if (!main) return;

    // Header
    var headerDiv = document.createElement('div');
    headerDiv.id = 'site-header';
    headerDiv.innerHTML = HEADER_HTML;
    main.parentNode.insertBefore(headerDiv, main);

    // Footer
    var footerDiv = document.createElement('div');
    footerDiv.id = 'site-footer';
    footerDiv.innerHTML = FOOTER_HTML;
    main.parentNode.insertBefore(footerDiv, main.nextSibling);

    // Data/ora live
    var giorni = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];
    var mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
    var el = document.getElementById('live-datetime');
    if (el) {
      function aggiorna() {
        var now = new Date();
        el.textContent = giorni[now.getDay()] + ' ' + now.getDate() + ' ' + mesi[now.getMonth()] + ' ' + now.getFullYear() + ' — ' + String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
      }
      aggiorna();
      setInterval(aggiorna, 30000);
    }

    // Ultimo aggiornamento sito (timestamp build Hugo) — caricato da /build-info.js
    var buildEl = document.getElementById('site-build-time');
    if (buildEl) {
      function renderBuild() {
        var raw = window.SITE_BUILD_TIME;
        if (!raw) return;
        var d = new Date(raw);
        if (isNaN(d.getTime())) return;
        var label = 'Sito aggiornato il ' + d.getDate() + ' ' + mesi[d.getMonth()] + ' ' + d.getFullYear() +
                    ' alle ' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
        buildEl.innerHTML = '<time datetime="' + raw + '">' + label + '</time>';
      }
      if (window.SITE_BUILD_TIME) {
        renderBuild();
      } else {
        var bi = document.createElement('script');
        bi.src = SITE_URL + '/build-info.js';
        bi.onload = renderBuild;
        bi.onerror = function () { buildEl.textContent = ''; };
        document.head.appendChild(bi);
      }
    }

    // Back to top
    var btn = document.getElementById('backToTop');
    if (btn) {
      window.addEventListener('scroll', function () {
        btn.classList.toggle('visible', window.scrollY > 300);
      });
      btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // Bottone "Torna al menu" — abbandono rapido nei giochi/quiz/app interattive.
    // Si attiva SOLO se la pagina ha marker tipici di un'app interattiva
    // (schermate intro/game/end). Esclude pagine hub e statiche.
    aggiungiPulsanteEsciGioco();
  }

  function aggiungiPulsanteEsciGioco() {
    if (document.getElementById('gioco-esci-btn')) return;

    var marker = document.querySelector(
      '#intro, #intro-screen, #game, #game-screen, #end, #end-screen, ' +
      '#select-screen, #game-card, #scenario-box, .gioco-fine, ' +
      '.scena-corrente, [data-gioco], .game-container'
    );
    if (!marker) return;

    var crumbLinks = document.querySelectorAll(
      '.breadcrumb a, nav[aria-label="Percorso"] a'
    );
    var menuHref = '../index.html';
    if (crumbLinks.length > 0) {
      menuHref = crumbLinks[crumbLinks.length - 1].getAttribute('href') || menuHref;
    }

    var esci = document.createElement('a');
    esci.id = 'gioco-esci-btn';
    esci.href = menuHref;
    esci.setAttribute('aria-label', 'Esci dal gioco e torna al menu');
    esci.innerHTML = '<i class="bi bi-x-lg" aria-hidden="true"></i> <span class="gioco-esci-label">Torna al menu</span>';
    esci.style.cssText = [
      'position: fixed',
      'top: 1rem',
      'right: 1rem',
      'z-index: 9999',
      'background: #003366',
      'color: #ffffff',
      'text-decoration: none',
      'padding: 0.55rem 1rem',
      'border-radius: 24px',
      'font-weight: 600',
      'font-size: 0.95rem',
      'box-shadow: 0 3px 10px rgba(0,0,0,0.25)',
      'display: inline-flex',
      'align-items: center',
      'gap: 0.5rem',
      'border: 2px solid #ffffff'
    ].join(';');

    if (!document.getElementById('gioco-esci-btn-styles')) {
      var stile = document.createElement('style');
      stile.id = 'gioco-esci-btn-styles';
      stile.textContent = ''
        + '#gioco-esci-btn:hover, #gioco-esci-btn:focus {'
        + '  background: #002244 !important;'
        + '  outline: 3px solid #ffbe2e;'
        + '  outline-offset: 2px;'
        + '}'
        + '#gioco-esci-btn .gioco-esci-label { white-space: nowrap; }'
        + '@media (max-width: 480px) {'
        + '  #gioco-esci-btn .gioco-esci-label { display: none; }'
        + '  #gioco-esci-btn { padding: 0.55rem 0.7rem !important; }'
        + '}'
        + '@media print { #gioco-esci-btn { display: none !important; } }';
      document.head.appendChild(stile);
    }
    document.body.appendChild(esci);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectChrome);
  } else {
    injectChrome();
  }
})();
