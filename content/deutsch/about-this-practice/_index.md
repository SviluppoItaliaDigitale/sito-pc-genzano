---
title: "Über diese Praxis — Barrierefrei konzipierte Krisenkommunikation"
description: "Wie die Zivilschutz-Freiwilligen von Genzano di Roma eine datenschutzfreundliche, barrierefrei konzipierte Informationsplattform für die Katastrophenvorsorge aufgebaut haben."
layout: "single"
language: "de"
hreflang:
  - lang: "it"
    url: "/modello-accessibile/"
  - lang: "en"
    url: "/english/about-this-practice/"
  - lang: "fr"
    url: "/francais/about-this-practice/"
  - lang: "de"
    url: "/deutsch/about-this-practice/"
sitemap:
  priority: 0.6
  changefreq: yearly
---

**Ein Good-Practice-Hinweis für die Fachgemeinschaft der Katastrophenvorsorge.**

Die **Gruppe der Zivilschutz-Freiwilligen von Genzano di Roma** ist eine Freiwilligenorganisation (OdV) der Gemeinde Genzano di Roma und Teil des Nationalen Zivilschutzdienstes Italiens. Wie bei den meisten örtlichen Zivilschutzgruppen liegt der Kern unserer Arbeit im Einsatz vor Ort: Vorbeugung, Überwachung und Unterstützung der Bevölkerung vor, während und nach Notlagen — Erdbeben, Überschwemmungen, Waldbrände und Unwetter.

Dieser Hinweis beschreibt etwas weniger Verbreitetes: die **öffentliche Informationsplattform**, die wir rund um diese Arbeit aufgebaut haben, und die Gestaltungsentscheidungen, die daraus ein übertragbares Modell machen und nicht nur eine Website.

## Das Problem, das wir lösen wollten

Notfallinformationen erreichen meist gerade die Menschen, die sie am wenigsten brauchen, und verfehlen jene, die sie am dringendsten benötigen: ältere Menschen, Menschen mit Behinderungen, Menschen mit geringer Lesekompetenz, Personen ohne Italienischkenntnisse und alle, die unter Stress stehen. Wir behandeln **Barrierefreiheit nicht als Häkchen zur Erfüllung von Vorschriften, sondern als Ausgangspunkt der Gestaltung** — nach dem Grundsatz: Erreicht eine Botschaft nicht *alle*, so ist sie nicht wirklich veröffentlicht.

## Wie die Praxis aussieht

Die Plattform ist eine **statische, datenschutzfreundliche Website** (keine Tracker, keine Cookies für Inhalte, keine eingebetteten Videos Dritter), bei der Barrierefreiheit in jeder Ebene verankert ist:

- **Technische Barrierefreiheit — WCAG 2.2 AA.** Semantisches HTML, Tastaturbedienung, sichtbarer Fokus, berechneter Farbkontrast und eine native **Werkzeugleiste für Barrierefreiheit** (Textgröße, Abstände, Paletten mit hohem Kontrast und invertierter Darstellung, legasthenikerfreundliche Schrift, reduzierte Bewegung). Auf kommerzielle Barrierefreiheits-Overlays verzichten wir bewusst, da das W3C-WAI und Behindertenverbände davon abraten.
- **Vorlesefunktion überall.** Eine browsereigene Vorlese-Schaltfläche (Web Speech API — kostenlos, ohne externen Dienst) auf jeder Inhaltsseite, dazu die geschätzte Lesedauer und automatische Silbentrennung, um den Eindruck einer „Textwüste" zu vermeiden.
- **Kognitive Zugänglichkeit.** In einfacher Sprache verfasste *Leicht-zu-lesen*-Fassungen wichtiger Inhalte, standardisierte **Piktogramme** (ISO 7010 Sicherheitszeichen + ARASAAC) sowie ein integriertes Glossar, das Abkürzungen bei der ersten Verwendung erläutert.
- **Unterstützte Kommunikation (UK).** Druckbare **Kommunikationstafeln** mit ARASAAC-Piktogrammen, damit eine Person, die in einer Notlage nicht sprechen kann — wegen einer Aphasie, einer kognitiven Behinderung, wegen Stress oder mangelnder Italienischkenntnisse — auf das *zeigen* kann, was sie braucht.
- **Gebärdensprache.** Ein Katalog von Inhalten in **Italienischer Gebärdensprache (LIS)**.
- **Blindenschrift.** In unserer Build-Pipeline wird für **jeden Nachrichtenartikel automatisch eine Braille-Datei (BRF) erzeugt** (die quelloffene *liblouis*, italienische Brailletabelle), herunterladbar und für Braille-Drucker geeignet — ein echter Kanal zu blinden und sehbehinderten Leserinnen und Lesern, ergänzend zu Screenreadern.
- **Sprachliche Zugänglichkeit.** Grundlegende Notfallinformationen stehen in **acht Sprachen** zur Verfügung (Italienisch sowie Englisch, Französisch, Deutsch, Spanisch, Portugiesisch, Rumänisch und Esperanto), mit korrekter Behandlung von `lang`/`hreflang`; Leicht-zu-lesen-Inhalte werden zusätzlich in weiteren Sprachen angeboten, darunter Arabisch.

Um diesen Kern der Barrierefreiheit herum liegen die Werkzeuge zur Vorsorge: Risikoseiten mit einheitlicher Gliederung *vorher / während / danach*, **auf schutzbedürftige Gruppen zugeschnittene Notfallkits** (ältere Menschen, Menschen mit Behinderungen, Säuglinge, Schwangerschaft, Haustiere, pflegende Angehörige, Menschen unter lebenserhaltender Therapie, Menschen ohne festen Wohnsitz, Zweitsprachlerinnen und Zweitsprachler), ein **offline speicherbarer Familien-Notfallplan**, Spiele und Quizze für Schulen (Benutzeroberfläche auf Italienisch), ein **Live-Dashboard** (Echtzeitdaten zu Seismik, Wetter, Luftqualität und Meer aus offiziellen Quellen wie INGV und Open-Meteo) sowie interaktive **Scrollytelling-Dossiers** zur örtlichen Risikogeschichte.

## Standards und Quellen

Jede Aussage ist auf eine primäre institutionelle Quelle zurückführbar. Unsere Referenzhierarchie: an erster Stelle die Inhaltsleitlinien des italienischen Zivilschutz-Departements (DPC) und der AgID; dann die nationalen wissenschaftlichen Einrichtungen (CNR, ISPRA, INGV); die europäischen operativen Referenzen (EENA / die einheitliche Notrufnummer 112); und schließlich internationale Standards — **WCAG 2.2 AA**, **ISO 22329** (soziale Medien in Notlagen) sowie humanitäre Referenzen wie **Sphere** und **IFRC** für die Kits für schutzbedürftige Gruppen. In Italien ist die einheitliche Notrufnummer die **112**.

## Warum sie übertragbar ist

Die gesamte Plattform läuft auf **offener, kostengünstiger Standardtechnik**: ein statischer Website-Generator, ein offenes Designsystem, browsereigene Programmierschnittstellen und quelloffene Werkzeuge (liblouis für Blindenschrift, ARASAAC-Piktogramme). Es gibt kein proprietäres CMS, keinen Laufzeitserver, keine Lizenzkosten, und das Hosting ist unkompliziert. Jede Kommune oder Freiwilligenorganisation kann das Modell nachbilden — die eigentliche Herausforderung ist nicht die Technik, sondern die **redaktionelle Disziplin**, Barrierefreiheit als grundlegende Anforderung zu behandeln.

## Anerkennung

Die Gruppe ist eine akkreditierte Organisation des **Europäischen Solidaritätskorps** (European Solidarity Corps — Quality Label, Organisationscode **E10435833**, Verordnung (EU) 2021/888) und ist bei **SNPC Volontariato** sowie der Koordinierungsstelle **FE.PI.VOL.** angeschlossen.

---

**Kontakt.** Gruppe der Zivilschutz-Freiwilligen von Genzano di Roma — Via Sicilia 13-15, 00045 Genzano di Roma (RM), Italien · segreteria@protezionecivilegenzano.it · [www.protezionecivilegenzano.it](https://www.protezionecivilegenzano.it/)

*Wir teilen unseren Ansatz und unsere Materialien gerne mit anderen Zivilschutzorganisationen und Fachleuten der Katastrophenvorsorge.*
