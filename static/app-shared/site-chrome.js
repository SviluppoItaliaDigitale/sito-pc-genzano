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
              '<a href="' + SITE_URL + '/area-volontari/" class="btn btn-slim-header me-3" aria-label="Area Volontari: informazioni e accesso al gestionale"><i class="bi bi-box-arrow-in-right me-1" aria-hidden="true"></i><span class="d-none d-md-inline">Area Volontari</span><span class="d-md-none">Accedi</span></a>' +
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
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/cruscotto/" role="menuitem"><span>Cruscotto del territorio</span></a></li>' +
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
                    /* Quiz "Quanto sei preparato?" rimosso dal menu il 22 maggio 2026:
                       ancorato come strumento dentro /piano-familiare/ (autovalutazione del cittadino). */
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
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/lis/" role="menuitem"><span>Contenuti in LIS</span></a></li>' +
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
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/san-pio-da-pietrelcina/" role="menuitem"><span>Il nostro patrono</span></a></li>' +
                    /* Aggiunto 16/05/2026: hub addestramento del Gruppo (turni + esercitazioni) */
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/esercitazioni/" role="menuitem"><span>Addestramento e buone pratiche</span></a></li>' +
                  '</ul></div></div>' +
                '</li>' +
                /* Dropdown: Risorse (6 voci, riorganizzato maggio 2026):
                   - Podcast + Articoli da ascoltare → hub "Audio e podcast"
                   - Open Data + Stato del Sito → sezioni in /trasparenza/
                   - Trasparenza + Stato del Sito → footer (accountability)
                   - Mappa del Sito → solo footer (era duplicata)
                   - Storia del territorio → "Per il Cittadino"
                   - Standard ISO → sezione in /normativa/ (norme tecniche
                     internazionali, completa la tassonomia nazionale/
                     regionale/comunale; testo a pagamento iso.org/uni.com) */
                '<li class="nav-item dropdown" role="none">' +
                  '<a class="nav-link dropdown-toggle" href="#" id="navDropdown-risorse" role="menuitem" data-bs-toggle="dropdown" aria-expanded="false">' +
                    '<span>Risorse</span>' +
                    '<svg class="icon icon-xs"><use href="' + SITE_URL + '/vendor/bootstrap-italia/svg/sprites.svg#it-expand"></use></svg>' +
                  '</a>' +
                  '<div class="dropdown-menu" aria-labelledby="navDropdown-risorse"><div class="link-list-wrapper"><ul class="link-list" role="menu">' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/faq/" role="menuitem"><span>FAQ</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/glossario/" role="menuitem"><span>Glossario</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/area-download/" role="menuitem"><span>Area Download</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/normativa/" role="menuitem"><span>Normativa</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/strumenti/" role="menuitem"><span>Strumenti in Tempo Reale</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/audio-e-podcast/" role="menuitem"><span>Audio e podcast</span></a></li>' +
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/risorse-pronte/" role="menuitem"><span>Materiali pronti</span></a></li>' +
                    /* Spostato da "Per il Cittadino" maggio 2026: timeline storica = consultazione narrativa, fra le risorse */
                    '<li role="none"><a class="list-item" href="' + SITE_URL + '/storia/" role="menuitem"><span>Storia del territorio</span></a></li>' +
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
              '<p style="color:rgba(255,255,255,0.85);"><strong>Sede:</strong> Via Sicilia, 13-15 - 00045 Genzano di Roma (RM)<br><strong>Telefono:</strong> <a href="tel:+39069362600" class="text-white fw-bold">+39 06 9362600</a><br><strong>Email:</strong> <a href="mailto:segreteria@protezionecivilegenzano.it" class="text-white fw-bold">segreteria@protezionecivilegenzano.it</a></p>' +
              '<p class="small" style="color:rgba(255,255,255,0.75);">14&deg; COI Prov. di Roma &mdash; Registro Regionale P.C. n.184<br>Iscritta al RUNTS sez. &laquo;Altri Enti del Terzo Settore&raquo; con determina n. G14230 del 28/10/2024<br>Aderente al Coordinamento FEPIVOL</p>' +
              '<div class="loghi-istituzionali d-flex align-items-center gap-3 flex-wrap mt-3" aria-label="Loghi istituzionali di appartenenza">' +
                '<img src="' + SITE_URL + '/images/logo-snpc-volontariato.png" alt="Servizio Nazionale Protezione Civile — Volontariato" width="96" height="112" style="background:#fff; border-radius:6px; padding:3px;">' +
                '<img src="' + SITE_URL + '/images/logo-pc-lazio.png" alt="Protezione Civile Regione Lazio" width="104" height="104" style="background:#fff; border-radius:50%; padding:3px;">' +
                '<img src="' + SITE_URL + '/images/logo-fepivol.png" alt="Coordinamento FE.PI.VOL. — Federazione Pronto Intervento Volontariato ODV" width="104" height="104" style="background:#fff; border-radius:50%; padding:3px;">' +
              '</div>' +
              '<div class="esc-quality-label d-flex align-items-center gap-2 mt-3">' +
                '<img src="' + SITE_URL + '/images/quality-label-esc.png" alt="Quality Label European Solidarity Corps" width="112" height="112" style="background:#fff; border-radius:50%; padding:3px; flex-shrink:0;">' +
                '<span class="small" style="color:rgba(255,255,255,0.85); line-height:1.3;">Quality Label<br>European Solidarity Corps<br><span style="font-family: monospace; font-size: 0.85em;">Codice: E10435833</span></span>' +
              '</div>' +
            '</div>' +
            '<div class="col-lg-4 col-md-4 pb-2">' +
              '<h2 class="h4 text-white">Servizi</h2>' +
              '<nav aria-label="Servizi nel footer"><ul class="footer-list" role="list">' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/piano-emergenza/" style="color:rgba(255,255,255,0.85);">Piano di Emergenza</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/piano-familiare/" style="color:rgba(255,255,255,0.85);">Piano Familiare</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/allerte-meteo/" style="color:rgba(255,255,255,0.85);">Allerte Meteo</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/area-download/" style="color:rgba(255,255,255,0.85);">Area Download</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/cartografia/" style="color:rgba(255,255,255,0.85);">Cartografia Operativa</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/cosa-fare-adesso/" style="color:rgba(255,255,255,0.85);">Cosa Fare Adesso</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/numeri-utili/" style="color:rgba(255,255,255,0.85);">Numeri Utili</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/faq/" style="color:rgba(255,255,255,0.85);">FAQ</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/formazione/" style="color:rgba(255,255,255,0.85);">Formazione</a></li>' +
              '</ul></nav>' +
            '</div>' +
            '<div class="col-lg-4 col-md-4 pb-2">' +
              '<h2 class="h4 text-white">Link Utili</h2>' +
              '<nav aria-label="Link utili nel footer"><ul class="footer-list" role="list">' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/note-legali/" style="color:rgba(255,255,255,0.85);">Note Legali</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/privacy/" style="color:rgba(255,255,255,0.85);">Privacy</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/accessibilita/" style="color:rgba(255,255,255,0.85);">Accessibilit&agrave;</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/metodo-editoriale/" style="color:rgba(255,255,255,0.85);">Metodo editoriale</a></li>' +
                /* Trasparenza + Stato del Sito spostati da "Risorse" a maggio 2026:
                   accountability istituzionale, coerenti nel footer accanto a
                   Note Legali / Privacy / Accessibilità. */
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/trasparenza/" style="color:rgba(255,255,255,0.85);">Trasparenza</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/siti-utili/" style="color:rgba(255,255,255,0.85);">Siti Utili</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/mappa-sito/" style="color:rgba(255,255,255,0.85);">Mappa del Sito</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/stato-sistema/" style="color:rgba(255,255,255,0.85);">Stato del Sito</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/open-data/" style="color:rgba(255,255,255,0.85);">Open Data</a></li>' +
                '<li role="listitem"><a class="list-item" href="' + SITE_URL + '/feed-rss/" style="color:rgba(255,255,255,0.85);">Feed RSS</a></li>' +
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
            '<li class="list-inline-item" role="listitem"><a href="' + SITE_URL + '/social-media-policy/" style="color:rgba(255,255,255,0.85);">Social Media Policy</a></li>' +
            '<li class="list-inline-item" role="listitem"><a href="' + SITE_URL + '/attribuzioni-pittogrammi/" style="color:rgba(255,255,255,0.85);">Attribuzioni pittogrammi</a></li>' +
          '</ul>' +
          '<p class="mt-2 mb-0 small" style="color:rgba(255,255,255,0.75);">&copy; ' + new Date().getFullYear() + ' Gruppo Comunale Volontari di Protezione Civile Genzano di Roma &mdash; C.F. 92011880588<br>I contenuti di questo sito, salvo diversa indicazione, sono distribuiti con licenza <a href="https://creativecommons.org/licenses/by/4.0/deed.it" target="_blank" rel="noopener noreferrer license" style="color:rgba(255,255,255,0.85);">CC BY 4.0</a>.<br>Sito Web ideato e realizzato da Alessandro Cuollo - Alfa 19 - IU0QVW.</p>' +
        '</div>' +
      '</div>' +
    '</footer>' +
    '<button class="back-to-top" id="backToTop" aria-label="Torna in cima alla pagina" title="Torna su"><i class="bi bi-arrow-up" aria-hidden="true"></i></button>';

  /* ----------------------------------------------------------------
     SOS 112 + Strumenti di accessibilità per le pagine statiche.
     Sulle pagine Hugo questi componenti arrivano da baseof.html
     (partial sos-112.html + accessibility-toolbar.html + a11y-toolbar.js).
     Le pagine statiche (giochi, quizpc, formazionepc, schede stampabili,
     abili-a-proteggere, ...) non passano da Hugo: senza questo blocco
     restavano prive del pulsante SOS 112 e della toolbar a11y, a differenza
     del resto del sito. Aggiunto dopo l'audit del 2026-05-22.
     MARKUP DA TENERE ALLINEATO con i partial Hugo citati sopra.
     ---------------------------------------------------------------- */
  var SOS_HTML =
    '<button type="button" id="sos-button" class="sos-button" aria-label="Chiama il numero unico di emergenza 112 (con conferma)" aria-haspopup="dialog" aria-controls="sos-modal">' +
      '<span class="sos-icon" aria-hidden="true">SOS</span>' +
      '<span class="sos-label">112</span>' +
    '</button>' +
    '<div id="sos-modal" class="sos-modal" role="dialog" aria-modal="true" aria-labelledby="sos-modal-title" aria-describedby="sos-modal-desc" hidden>' +
      '<div class="sos-modal-backdrop" data-sos-close="true" aria-hidden="true"></div>' +
      '<div class="sos-modal-dialog" role="document">' +
        '<div class="sos-modal-header">' +
          '<h2 id="sos-modal-title" class="sos-modal-title"><i class="bi bi-telephone-fill" aria-hidden="true"></i> Stai per chiamare il <strong>112</strong></h2>' +
        '</div>' +
        '<div class="sos-modal-body">' +
          '<p id="sos-modal-desc" class="sos-modal-desc">Il <strong>112</strong> è il <strong>Numero Unico di Emergenza</strong>: chiamalo <strong>solo se c\'è una vera emergenza</strong> (incidente, incendio, ferito grave, evento naturale in corso).</p>' +
          '<p class="sos-modal-info">Se confermi, parte la chiamata. Una volta connesso, parla con calma: di\' <strong>cosa è successo</strong> e <strong>dove sei</strong>. Non riagganciare prima dell\'operatore.</p>' +
          '<div class="sos-modal-warning"><i class="bi bi-exclamation-triangle-fill" aria-hidden="true"></i> Le chiamate al 112 per scherzo o per motivi non urgenti sono <strong>punite per legge</strong> (art. 658 Codice penale).</div>' +
          '<p class="sos-modal-alt"><i class="bi bi-question-circle-fill" aria-hidden="true"></i> <strong>Non sei sicuro che sia un\'emergenza?</strong> Usa l\'<strong>assistente guidato</strong>: ti accompagna con domande semplici fino alla risposta giusta.</p>' +
        '</div>' +
        '<div class="sos-modal-footer">' +
          '<button type="button" id="sos-modal-cancel" class="btn btn-outline-secondary btn-lg sos-modal-btn-cancel" data-sos-close="true"><i class="bi bi-x-lg me-1" aria-hidden="true"></i> Annulla</button>' +
          '<a href="' + SITE_URL + '/assistente/" id="sos-modal-guide" class="btn btn-outline-primary btn-lg sos-modal-btn-guide"><i class="bi bi-question-circle-fill me-1" aria-hidden="true"></i> Cosa devo fare?</a>' +
          '<a href="tel:112" id="sos-modal-call" class="btn btn-danger btn-lg sos-modal-btn-call"><i class="bi bi-telephone-fill me-1" aria-hidden="true"></i> Sì, chiama il 112</a>' +
        '</div>' +
      '</div>' +
    '</div>';

  var A11Y_HTML =
    '<button type="button" id="a11yToolbarOpen" class="a11y-fab" aria-label="Apri strumenti di accessibilità" aria-haspopup="dialog" aria-controls="a11yDialog" title="Strumenti di accessibilità">' +
      '<i class="bi bi-universal-access" aria-hidden="true"></i><span class="visually-hidden">Strumenti di accessibilità</span>' +
    '</button>' +
    '<div class="a11y-backdrop" id="a11yBackdrop" hidden></div>' +
    '<div class="a11y-dialog" id="a11yDialog" role="dialog" aria-modal="true" aria-labelledby="a11yDialogTitle" hidden>' +
      '<header class="a11y-dialog-header">' +
        '<h2 id="a11yDialogTitle" class="a11y-dialog-title"><i class="bi bi-universal-access me-2" aria-hidden="true"></i> Strumenti di accessibilità</h2>' +
        '<button type="button" id="a11yDialogClose" class="a11y-close" aria-label="Chiudi strumenti di accessibilità"><i class="bi bi-x-lg" aria-hidden="true"></i></button>' +
      '</header>' +
      '<div class="a11y-dialog-body">' +
        '<p class="a11y-intro">Personalizza la lettura del sito. Le tue scelte vengono ricordate sul tuo dispositivo.</p>' +
        '<fieldset class="a11y-section">' +
          '<legend class="a11y-section-title"><i class="bi bi-fonts me-2" aria-hidden="true"></i>Testo</legend>' +
          '<div class="a11y-control"><span class="a11y-control-label" id="a11yLblTextSize">Dimensione del testo</span>' +
            '<div class="a11y-segments" role="radiogroup" aria-labelledby="a11yLblTextSize">' +
              '<button type="button" class="a11y-seg" data-pref="textSize" data-value="0" aria-pressed="true">100%</button>' +
              '<button type="button" class="a11y-seg" data-pref="textSize" data-value="1" aria-pressed="false">110%</button>' +
              '<button type="button" class="a11y-seg" data-pref="textSize" data-value="2" aria-pressed="false">125%</button>' +
              '<button type="button" class="a11y-seg" data-pref="textSize" data-value="3" aria-pressed="false">150%</button>' +
            '</div></div>' +
          '<div class="a11y-control"><span class="a11y-control-label" id="a11yLblTextAlign">Allineamento del testo</span>' +
            '<div class="a11y-segments" role="radiogroup" aria-labelledby="a11yLblTextAlign">' +
              '<button type="button" class="a11y-seg" data-pref="textAlign" data-value="default" aria-pressed="true">Predefinito</button>' +
              '<button type="button" class="a11y-seg" data-pref="textAlign" data-value="left" aria-pressed="false">A sinistra</button>' +
              '<button type="button" class="a11y-seg" data-pref="textAlign" data-value="justify" aria-pressed="false">Giustificato</button>' +
            '</div></div>' +
          '<div class="a11y-control"><span class="a11y-control-label" id="a11yLblFontFamily">Tipo carattere</span>' +
            '<div class="a11y-segments a11y-segments-stack" role="radiogroup" aria-labelledby="a11yLblFontFamily">' +
              '<button type="button" class="a11y-seg" data-pref="fontFamily" data-value="default" aria-pressed="true">Predefinito</button>' +
              '<button type="button" class="a11y-seg" data-pref="fontFamily" data-value="readable" aria-pressed="false">Alta leggibilità</button>' +
              '<button type="button" class="a11y-seg" data-pref="fontFamily" data-value="dyslexic" aria-pressed="false">Per dislessia (OpenDyslexic)</button>' +
            '</div></div>' +
          '<button type="button" class="a11y-toggle" data-pref="spacing" aria-pressed="false"><i class="bi bi-distribute-vertical me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Spaziatura ampia (righe e lettere)</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
          '<button type="button" class="a11y-toggle" data-pref="readingMode" aria-pressed="false"><i class="bi bi-book me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Modalità lettura (sfondo crema + spaziatura)</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
        '</fieldset>' +
        '<fieldset class="a11y-section">' +
          '<legend class="a11y-section-title"><i class="bi bi-volume-up-fill me-2" aria-hidden="true"></i>Lettura ad alta voce</legend>' +
          '<div class="a11y-control"><span class="a11y-control-label" id="a11yLblTtsRate">Velocità di lettura</span>' +
            '<div class="a11y-segments" role="radiogroup" aria-labelledby="a11yLblTtsRate">' +
              '<button type="button" class="a11y-seg" data-pref="ttsRate" data-value="0.75" aria-pressed="false">Lenta</button>' +
              '<button type="button" class="a11y-seg" data-pref="ttsRate" data-value="0.95" aria-pressed="true">Normale</button>' +
              '<button type="button" class="a11y-seg" data-pref="ttsRate" data-value="1.15" aria-pressed="false">Veloce</button>' +
            '</div></div>' +
        '</fieldset>' +
        '<fieldset class="a11y-section">' +
          '<legend class="a11y-section-title"><i class="bi bi-eye-fill me-2" aria-hidden="true"></i>Visivo</legend>' +
          '<div class="a11y-control"><span class="a11y-control-label" id="a11yLblContrast">Contrasto</span>' +
            '<div class="a11y-segments a11y-segments-stack" role="radiogroup" aria-labelledby="a11yLblContrast">' +
              '<button type="button" class="a11y-seg" data-pref="contrast" data-value="default" aria-pressed="true">Predefinito</button>' +
              '<button type="button" class="a11y-seg" data-pref="contrast" data-value="high" aria-pressed="false">Alto (nero su bianco)</button>' +
              '<button type="button" class="a11y-seg" data-pref="contrast" data-value="invert" aria-pressed="false">Invertito (bianco su nero)</button>' +
              '<button type="button" class="a11y-seg" data-pref="contrast" data-value="yellow-black" aria-pressed="false">Giallo su nero</button>' +
              '<button type="button" class="a11y-seg" data-pref="contrast" data-value="blue-cream" aria-pressed="false">Blu su crema</button>' +
            '</div></div>' +
          '<button type="button" class="a11y-toggle" data-pref="grayscale" aria-pressed="false"><i class="bi bi-circle-half me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Scala di grigi</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
          '<button type="button" class="a11y-toggle" data-pref="hideImages" aria-pressed="false"><i class="bi bi-image me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Nascondi immagini decorative</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
          '<button type="button" class="a11y-toggle" data-pref="pauseAnimations" aria-pressed="false"><i class="bi bi-pause-circle me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Pausa animazioni</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
        '</fieldset>' +
        '<fieldset class="a11y-section">' +
          '<legend class="a11y-section-title"><i class="bi bi-compass me-2" aria-hidden="true"></i>Orientamento</legend>' +
          '<button type="button" class="a11y-toggle" data-pref="highlightLinks" aria-pressed="false"><i class="bi bi-link-45deg me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Evidenzia tutti i link</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
          '<button type="button" class="a11y-toggle" data-pref="bigCursor" aria-pressed="false"><i class="bi bi-cursor-fill me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Cursore grande</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
          '<a class="a11y-link-page" href="' + SITE_URL + '/accessibilita/"><i class="bi bi-info-circle me-2" aria-hidden="true"></i> Vai alla pagina Accessibilità del sito <i class="bi bi-arrow-right ms-auto" aria-hidden="true"></i></a>' +
        '</fieldset>' +
        '<fieldset class="a11y-section">' +
          '<legend class="a11y-section-title"><i class="bi bi-square me-2" aria-hidden="true"></i>Pulsanti flottanti</legend>' +
          '<button type="button" class="a11y-toggle" data-pref="hideAssistantFab" aria-pressed="false"><i class="bi bi-chat-dots me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Nascondi pulsante Assistente virtuale</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
          '<button type="button" class="a11y-toggle" data-pref="hideSosFab" aria-pressed="false"><i class="bi bi-telephone me-2" aria-hidden="true"></i><span class="a11y-toggle-text">Nascondi pulsante SOS 112</span><span class="a11y-toggle-state" aria-hidden="true">Off</span></button>' +
        '</fieldset>' +
        '<div class="a11y-status" role="status" aria-live="polite" id="a11yStatus"></div>' +
      '</div>' +
      '<footer class="a11y-dialog-footer">' +
        '<button type="button" id="a11yReset" class="a11y-btn a11y-btn-secondary"><i class="bi bi-arrow-counterclockwise me-1" aria-hidden="true"></i> Reimposta tutto</button>' +
        '<button type="button" id="a11yDialogCloseFooter" class="a11y-btn a11y-btn-primary"><i class="bi bi-check-lg me-1" aria-hidden="true"></i> Chiudi</button>' +
      '</footer>' +
    '</div>';

  function wireSos() {
    var btn = document.getElementById('sos-button');
    var modal = document.getElementById('sos-modal');
    var cancelBtn = document.getElementById('sos-modal-cancel');
    var callBtn = document.getElementById('sos-modal-call');
    if (!btn || !modal) return;
    var lastFocused = null;
    var focusableSel = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    function openModal() {
      lastFocused = document.activeElement;
      modal.hidden = false;
      document.body.style.overflow = 'hidden';
      setTimeout(function () { if (cancelBtn) cancelBtn.focus(); }, 30);
      document.addEventListener('keydown', onKeyDown);
    }
    function closeModal() {
      modal.hidden = true;
      document.body.style.overflow = '';
      document.removeEventListener('keydown', onKeyDown);
      if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
    }
    function onKeyDown(e) {
      if (e.key === 'Escape') { e.preventDefault(); closeModal(); return; }
      if (e.key === 'Tab') {
        var focusables = modal.querySelectorAll(focusableSel);
        if (!focusables.length) return;
        var first = focusables[0];
        var last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }
    btn.addEventListener('click', openModal);
    modal.querySelectorAll('[data-sos-close="true"]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        if (el.classList.contains('sos-modal-backdrop') && e.target !== el) return;
        closeModal();
      });
    });
    if (callBtn) callBtn.addEventListener('click', function () { setTimeout(closeModal, 800); });
  }

  function injectA11yAndSos() {
    // Idempotente: se la pagina ha già SOS o toolbar (es. include propri), non duplico.
    if (document.getElementById('sos-button') || document.getElementById('a11yToolbarOpen')) return;

    var sosWrap = document.createElement('div');
    sosWrap.innerHTML = SOS_HTML;
    while (sosWrap.firstChild) document.body.appendChild(sosWrap.firstChild);
    wireSos();

    var a11yWrap = document.createElement('div');
    a11yWrap.innerHTML = A11Y_HTML;
    while (a11yWrap.firstChild) document.body.appendChild(a11yWrap.firstChild);

    // CSS della toolbar (file dedicato, non in custom.css).
    if (!document.querySelector('link[data-a11y-toolbar]')) {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = SITE_URL + '/css/a11y-toolbar.css';
      link.setAttribute('data-a11y-toolbar', '1');
      document.head.appendChild(link);
    }
    // JS della toolbar: applica le preferenze salvate su <html> e fa il
    // wireup del dialog appena iniettato. Gestisce da sé il caso DOM già
    // pronto (else { onReady() }), quindi va bene caricarlo dopo il markup.
    if (!document.querySelector('script[data-a11y-toolbar]')) {
      var sc = document.createElement('script');
      sc.src = SITE_URL + '/js/a11y-toolbar.js';
      sc.setAttribute('data-a11y-toolbar', '1');
      document.body.appendChild(sc);
    }
  }

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

    // SOS 112 + toolbar accessibilità anche sulle pagine statiche (audit 2026-05-22).
    injectA11yAndSos();
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

  // Statistiche anonime senza cookie (GoatCounter), come sulle pagine Hugo.
  // Le pagine statiche non passano da baseof.html: lo iniettiamo qui.
  if (!document.querySelector('script[data-goatcounter]')) {
    var gc = document.createElement('script');
    gc.async = true;
    gc.src = '//gc.zgo.at/count.js';
    gc.setAttribute('data-goatcounter', 'https://apicuollo.goatcounter.com/count');
    (document.body || document.documentElement).appendChild(gc);
  }
})();
