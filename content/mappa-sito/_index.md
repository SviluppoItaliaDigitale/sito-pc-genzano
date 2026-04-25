---
title: "Mappa del Sito"
description: "Tutte le pagine del sito della Protezione Civile di Genzano di Roma organizzate per area tematica: servizi, rischi, allerte, formazione, strumenti, contatti."
layout: "single"
aliases:
  - /sitemap.html
  - /mappa/
sitemap:
  priority: 0.6
  changefreq: monthly
---

In questa pagina trovi **tutte le sezioni del sito** organizzate per tema. Se non sai da dove cominciare, parti dai **"Servizi al cittadino"** in alto: contengono gli strumenti più utili in caso di emergenza.

<div class="alert alert-info" role="note">
<p class="mb-0"><i class="bi bi-search me-2" aria-hidden="true"></i><strong>Cerchi qualcosa di specifico?</strong> Usa il <a href="/cerca/">motore di ricerca interno</a> oppure premi <kbd>Ctrl+F</kbd> (Windows/Linux) o <kbd>Cmd+F</kbd> (Mac) sulla tastiera.</p>
</div>

<style>
.ms-section {
  margin: 2.5rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #003366;
  color: #003366;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.ms-section .ms-section-icon {
  width: 2.5rem;
  height: 2.5rem;
  background: #003366;
  color: #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  flex-shrink: 0;
}
.ms-section h2 {
  margin: 0;
  font-size: 1.4rem;
  flex: 1;
}

.ms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.ms-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.1rem 1.2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-left: 5px solid #003366;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.ms-card:hover, .ms-card:focus {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 51, 102, 0.18);
  text-decoration: none;
  color: inherit;
}
.ms-card-icon {
  font-size: 2rem;
  color: #003366;
  margin-bottom: 0.5rem;
}
.ms-card-title {
  color: #003366;
  font-weight: 700;
  font-size: 1.05rem;
  margin: 0 0 0.3rem 0;
  line-height: 1.3;
}
.ms-card-desc {
  font-size: 0.9rem;
  color: #495057;
  line-height: 1.4;
  margin: 0;
}
.ms-card-arrow {
  margin-top: auto;
  padding-top: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #003366;
}

/* Variante colore per area "emergenza" */
.ms-card.ms-emerg { border-left-color: #dc3545; }
.ms-card.ms-emerg .ms-card-icon, .ms-card.ms-emerg .ms-card-title, .ms-card.ms-emerg .ms-card-arrow { color: #dc3545; }
/* Variante per "formazione" */
.ms-card.ms-edu { border-left-color: #7c3aed; }
.ms-card.ms-edu .ms-card-icon, .ms-card.ms-edu .ms-card-title, .ms-card.ms-edu .ms-card-arrow { color: #7c3aed; }
/* Variante per "strumenti" */
.ms-card.ms-tool { border-left-color: #0891b2; }
.ms-card.ms-tool .ms-card-icon, .ms-card.ms-tool .ms-card-title, .ms-card.ms-tool .ms-card-arrow { color: #0891b2; }
/* Variante per "comunicazione" */
.ms-card.ms-comm { border-left-color: #15803d; }
.ms-card.ms-comm .ms-card-icon, .ms-card.ms-comm .ms-card-title, .ms-card.ms-comm .ms-card-arrow { color: #15803d; }
/* Variante per "documenti" */
.ms-card.ms-doc { border-left-color: #6c757d; }
.ms-card.ms-doc .ms-card-icon, .ms-card.ms-doc .ms-card-title, .ms-card.ms-doc .ms-card-arrow { color: #6c757d; }
/* Variante per "speciale/accessibilità" */
.ms-card.ms-spec { border-left-color: #b45309; }
.ms-card.ms-spec .ms-card-icon, .ms-card.ms-spec .ms-card-title, .ms-card.ms-spec .ms-card-arrow { color: #b45309; }
</style>

<div class="ms-section"><span class="ms-section-icon"><i class="bi bi-house-heart-fill"></i></span><h2>Servizi al cittadino</h2></div>

<div class="ms-grid">
<a class="ms-card" href="/assistente/">
  <div class="ms-card-icon"><i class="bi bi-question-circle-fill"></i></div>
  <p class="ms-card-title">Cosa devo fare?</p>
  <p class="ms-card-desc">Assistente guidato passo-passo: rispondi a domande semplici e ricevi indicazioni in caso di emergenza.</p>
  <span class="ms-card-arrow">Apri assistente →</span>
</a>
<a class="ms-card" href="/piano-familiare/">
  <div class="ms-card-icon"><i class="bi bi-house-heart"></i></div>
  <p class="ms-card-title">Piano Familiare</p>
  <p class="ms-card-desc">Crea e stampa il piano di emergenza della tua famiglia: numeri, punti di ritrovo, kit.</p>
  <span class="ms-card-arrow">Crea il piano →</span>
</a>
<a class="ms-card" href="/cartografia/">
  <div class="ms-card-icon"><i class="bi bi-map-fill"></i></div>
  <p class="ms-card-title">Cartografia Operativa</p>
  <p class="ms-card-desc">Le 16 aree di emergenza del Piano Comunale: aree di attesa, ricovero e ammassamento.</p>
  <span class="ms-card-arrow">Consulta →</span>
</a>
<a class="ms-card ms-tool" href="/strumenti/">
  <div class="ms-card-icon"><i class="bi bi-broadcast-pin"></i></div>
  <p class="ms-card-title">Strumenti in Tempo Reale</p>
  <p class="ms-card-desc">12+ strumenti istituzionali: Windy, INGV, Radar DPC, MeteoAM, ISPRA, EFFIS, ARPA, ANAS.</p>
  <span class="ms-card-arrow">Apri hub →</span>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#dc3545"><i class="bi bi-exclamation-triangle-fill"></i></span><h2>Allerte ed emergenze</h2></div>

<div class="ms-grid">
<a class="ms-card ms-emerg" href="/allerte-meteo/">
  <div class="ms-card-icon"><i class="bi bi-cloud-rain-heavy-fill"></i></div>
  <p class="ms-card-title">Allerte Meteo</p>
  <p class="ms-card-desc">Codici colore, sistema di allertamento, widget Windy/Radar DPC/MeteoAM, fonti ufficiali.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-emerg" href="/numeri-utili/">
  <div class="ms-card-icon"><i class="bi bi-telephone-fill"></i></div>
  <p class="ms-card-title">Numeri Utili</p>
  <p class="ms-card-desc">112, ARES 118, 803 555, contatti del Comune e del Gruppo. Solo numeri verificati.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-emerg" href="/cosa-fare-adesso/">
  <div class="ms-card-icon"><i class="bi bi-list-check"></i></div>
  <p class="ms-card-title">Cosa fare adesso</p>
  <p class="ms-card-desc">Comportamenti concreti durante un'emergenza in corso. Pagina di consultazione rapida.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-emerg" href="/piano-emergenza/">
  <div class="ms-card-icon"><i class="bi bi-shield-fill-check"></i></div>
  <p class="ms-card-title">Piano di Emergenza Comunale</p>
  <p class="ms-card-desc">Struttura e contenuti del Piano di Emergenza del Comune di Genzano di Roma.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#dc3545"><i class="bi bi-bookmark-star-fill"></i></span><h2>Cosa fare in caso di…</h2></div>

<div class="ms-grid">
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischio-sismico/">
  <div class="ms-card-icon"><i class="bi bi-activity"></i></div>
  <p class="ms-card-title">Terremoto</p>
  <p class="ms-card-desc">Comportamenti prima/durante/dopo, mappa terremoti recenti INGV, Genzano in zona sismica 2B.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischio-idrogeologico/">
  <div class="ms-card-icon"><i class="bi bi-water"></i></div>
  <p class="ms-card-title">Frane e alluvioni</p>
  <p class="ms-card-desc">Rischio idrogeologico sul territorio dei Castelli Romani, comportamenti, fonti ISPRA.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischio-incendio/">
  <div class="ms-card-icon"><i class="bi bi-fire"></i></div>
  <p class="ms-card-title">Incendi boschivi</p>
  <p class="ms-card-desc">Periodo AIB giugno-settembre, prevenzione, segnalazione tramite 112.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/temporali-intensi/">
  <div class="ms-card-icon"><i class="bi bi-lightning-charge-fill"></i></div>
  <p class="ms-card-title">Temporali intensi</p>
  <p class="ms-card-desc">Pioggia forte, fulmini, grandine. Mappa fulmini in tempo reale (Lightning Maps).</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/vento-forte/">
  <div class="ms-card-icon"><i class="bi bi-wind"></i></div>
  <p class="ms-card-title">Vento forte</p>
  <p class="ms-card-desc">Raffiche, mareggiate, alberi caduti, precauzioni domestiche.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/ondate-di-calore/">
  <div class="ms-card-icon"><i class="bi bi-thermometer-sun"></i></div>
  <p class="ms-card-title">Ondate di calore</p>
  <p class="ms-card-desc">Temperature estreme, attenzione ad anziani e bambini, idratazione, qualità dell'aria.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/blackout/">
  <div class="ms-card-icon"><i class="bi bi-lightning-charge"></i></div>
  <p class="ms-card-title">Blackout</p>
  <p class="ms-card-desc">Interruzioni elettriche prolungate, comportamenti, riferimenti.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/persone-necessita-specifiche/">
  <div class="ms-card-icon"><i class="bi bi-person-arms-up"></i></div>
  <p class="ms-card-title">Persone con esigenze specifiche</p>
  <p class="ms-card-desc">Disabilità, anziani fragili, donne in gravidanza, bambini molto piccoli.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/kit-emergenza/">
  <div class="ms-card-icon"><i class="bi bi-bag-check-fill"></i></div>
  <p class="ms-card-title">Kit di emergenza</p>
  <p class="ms-card-desc">Cosa mettere nello zaino di emergenza domestico, lista completa e priorità.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#7c3aed"><i class="bi bi-mortarboard-fill"></i></span><h2>Formazione e didattica</h2></div>

<div class="ms-grid">
<a class="ms-card ms-edu" href="/formazione/">
  <div class="ms-card-icon"><i class="bi bi-book-half"></i></div>
  <p class="ms-card-title">Hub Formazione</p>
  <p class="ms-card-desc">Punto centrale della formazione: kit didattici, schede, giochi, primo soccorso.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/schede-stampabili/">
  <div class="ms-card-icon"><i class="bi bi-printer-fill"></i></div>
  <p class="ms-card-title">Schede stampabili</p>
  <p class="ms-card-desc">18 schede A4 pronte per la stampa: chiamata 112, vero/falso, labirinto, schede da colorare.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-infanzia/">
  <div class="ms-card-icon"><i class="bi bi-stars"></i></div>
  <p class="ms-card-title">Kit Scuola Infanzia</p>
  <p class="ms-card-desc">Materiale didattico per insegnanti 3-6 anni: percorso 4 incontri, filastrocche, schede.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-primaria/">
  <div class="ms-card-icon"><i class="bi bi-pencil-fill"></i></div>
  <p class="ms-card-title">Kit Scuola Primaria</p>
  <p class="ms-card-desc">Materiale didattico per insegnanti 6-11 anni: 6 moduli, esperimenti, role-play, verifiche.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-secondaria-primo-grado/">
  <div class="ms-card-icon"><i class="bi bi-bookmark-fill"></i></div>
  <p class="ms-card-title">Kit Secondaria I grado</p>
  <p class="ms-card-desc">Materiale 11-14 anni: UdA, casi studio italiani (Amatrice, Ischia), service learning.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-secondaria-secondo-grado/">
  <div class="ms-card-icon"><i class="bi bi-journal-bookmark-fill"></i></div>
  <p class="ms-card-title">Kit Secondaria II grado</p>
  <p class="ms-card-desc">Materiale 14-19 anni: PCTO, tracce Esame di Stato, dibattiti, compiti di realtà.</p>
</a>
<a class="ms-card ms-edu" href="/giochi/">
  <div class="ms-card-icon"><i class="bi bi-controller"></i></div>
  <p class="ms-card-title">Giochi della Sicurezza</p>
  <p class="ms-card-desc">30+ giochi educativi gratuiti per bambini 3-14 anni: terremoto, evacuazione, 112.</p>
</a>
<a class="ms-card ms-edu" href="/glossario/">
  <div class="ms-card-icon"><i class="bi bi-book"></i></div>
  <p class="ms-card-title">Glossario PC</p>
  <p class="ms-card-desc">50+ sigle e termini tecnici (PAI, COC, DICOMAC, IT-alert, ecc.) spiegati in parole semplici.</p>
</a>
<a class="ms-card ms-edu" href="/faq/">
  <div class="ms-card-icon"><i class="bi bi-patch-question-fill"></i></div>
  <p class="ms-card-title">Domande frequenti</p>
  <p class="ms-card-desc">30+ domande con risposta su allerte, emergenze, prevenzione, volontariato e numeri.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#15803d"><i class="bi bi-megaphone-fill"></i></span><h2>Comunicazioni e canali</h2></div>

<div class="ms-grid">
<a class="ms-card ms-comm" href="/comunicazioni/">
  <div class="ms-card-icon"><i class="bi bi-newspaper"></i></div>
  <p class="ms-card-title">Archivio Comunicazioni</p>
  <p class="ms-card-desc">Tutte le notizie pubblicate dal Gruppo: allerte, eventi, formazione, attivazioni, novità.</p>
</a>
<a class="ms-card ms-comm" href="/social-media-policy/">
  <div class="ms-card-icon"><i class="bi bi-share-fill"></i></div>
  <p class="ms-card-title">Social Media Policy</p>
  <p class="ms-card-desc">Le regole con cui il Gruppo usa i propri canali social: Facebook, Instagram, X, Telegram.</p>
</a>
<a class="ms-card ms-comm" href="/cerca/">
  <div class="ms-card-icon"><i class="bi bi-search"></i></div>
  <p class="ms-card-title">Motore di ricerca interno</p>
  <p class="ms-card-desc">Cerca tra tutte le pagine del sito per parole chiave, titolo, contenuto.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon"><i class="bi bi-people-fill"></i></span><h2>Sul Gruppo</h2></div>

<div class="ms-grid">
<a class="ms-card" href="/chi-siamo/">
  <div class="ms-card-icon"><i class="bi bi-info-circle-fill"></i></div>
  <p class="ms-card-title">Chi siamo</p>
  <p class="ms-card-desc">Storia, struttura e missione del Gruppo Comunale Volontari di Genzano (dal 1981).</p>
</a>
<a class="ms-card" href="/contatti/">
  <div class="ms-card-icon"><i class="bi bi-envelope-fill"></i></div>
  <p class="ms-card-title">Contatti</p>
  <p class="ms-card-desc">Sede in Via Sicilia 13-15, email, recapiti per emergenze e attività ordinarie.</p>
</a>
<a class="ms-card" href="/diventa-volontario/">
  <div class="ms-card-icon"><i class="bi bi-person-plus-fill"></i></div>
  <p class="ms-card-title">Diventa Volontario</p>
  <p class="ms-card-desc">Come iscriversi al Gruppo, requisiti, formazione obbligatoria, cosa puoi fare.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#0891b2"><i class="bi bi-grid-3x3-gap-fill"></i></span><h2>Strumenti, risorse, download</h2></div>

<div class="ms-grid">
<a class="ms-card ms-tool" href="/strumenti/">
  <div class="ms-card-icon"><i class="bi bi-broadcast-pin"></i></div>
  <p class="ms-card-title">Strumenti in Tempo Reale</p>
  <p class="ms-card-desc">Hub dei 12+ strumenti online: meteo, terremoti, idrogeologico, incendi, qualità aria.</p>
</a>
<a class="ms-card ms-tool" href="/cartografia/">
  <div class="ms-card-icon"><i class="bi bi-geo-alt-fill"></i></div>
  <p class="ms-card-title">Cartografia Operativa</p>
  <p class="ms-card-desc">Aree di Attesa (10), Aree di Ricovero (4), Aree di Ammassamento (2) con cartelli e indirizzi.</p>
</a>
<a class="ms-card ms-tool" href="/area-download/">
  <div class="ms-card-icon"><i class="bi bi-download"></i></div>
  <p class="ms-card-title">Area Download</p>
  <p class="ms-card-desc">Documenti, modulistica, normativa: PDF scaricabili del Piano, ordinanze, materiale ufficiale.</p>
</a>
<a class="ms-card ms-tool" href="/siti-utili/">
  <div class="ms-card-icon"><i class="bi bi-link-45deg"></i></div>
  <p class="ms-card-title">Siti utili</p>
  <p class="ms-card-desc">Link a istituzioni di Protezione Civile: DPC, Regione Lazio, INGV, ISPRA, Comune.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#b45309"><i class="bi bi-universal-access-circle"></i></span><h2>Versioni speciali e accessibilità</h2></div>

<div class="ms-grid">
<a class="ms-card ms-spec" href="/facile-da-leggere/">
  <div class="ms-card-icon"><i class="bi bi-emoji-smile-fill"></i></div>
  <p class="ms-card-title">Facile da leggere</p>
  <p class="ms-card-desc">Le informazioni essenziali in versione semplice. Frasi corte, parole facili. Per tutti.</p>
</a>
<a class="ms-card ms-spec" href="/english/">
  <div class="ms-card-icon"><i class="bi bi-translate"></i></div>
  <p class="ms-card-title">English version</p>
  <p class="ms-card-desc">Essential Civil Protection info in English for tourists and foreign residents.</p>
</a>
<a class="ms-card ms-spec" href="/accessibilita/">
  <div class="ms-card-icon"><i class="bi bi-eye-fill"></i></div>
  <p class="ms-card-title">Dichiarazione di Accessibilità</p>
  <p class="ms-card-desc">Conformità WCAG 2.2 AA, contenuti di terze parti, meccanismo di feedback.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#6c757d"><i class="bi bi-file-earmark-text-fill"></i></span><h2>Documenti legali e privacy</h2></div>

<div class="ms-grid">
<a class="ms-card ms-doc" href="/privacy/">
  <div class="ms-card-icon"><i class="bi bi-shield-lock-fill"></i></div>
  <p class="ms-card-title">Privacy e Cookie</p>
  <p class="ms-card-desc">Informativa GDPR, gestione dei cookie, widget di terze parti, diritti dell'utente.</p>
</a>
<a class="ms-card ms-doc" href="/note-legali/">
  <div class="ms-card-icon"><i class="bi bi-file-text-fill"></i></div>
  <p class="ms-card-title">Note Legali</p>
  <p class="ms-card-desc">Titolarità, condizioni d'uso, copyright dei contenuti del sito.</p>
</a>
<a class="ms-card ms-doc" href="/social-media-policy/">
  <div class="ms-card-icon"><i class="bi bi-chat-square-quote-fill"></i></div>
  <p class="ms-card-title">Social Media Policy</p>
  <p class="ms-card-desc">Linee guida e regole di comportamento sui canali social ufficiali del Gruppo.</p>
</a>
</div>

---

<p class="text-center text-muted mt-4">
<i class="bi bi-info-circle me-1" aria-hidden="true"></i>
Pagina aggiornata automaticamente quando vengono pubblicate nuove sezioni del sito.
Se trovi un link rotto o una pagina mancante, segnalacelo a
<a href="mailto:segreteria@protezionecivilegenzano.it">segreteria@protezionecivilegenzano.it</a>.
</p>
