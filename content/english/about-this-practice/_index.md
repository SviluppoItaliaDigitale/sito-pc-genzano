---
title: "About this practice — Accessible-by-design disaster communication"
description: "How the Civil Protection Volunteers of Genzano di Roma built a privacy-first, accessible-by-design public information platform for disaster risk reduction."
layout: "single"
language: "en"
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

**A good-practice note for the disaster risk reduction community.**

The **Civil Protection Volunteers Group of Genzano di Roma** is a volunteer organisation (OdV) of the Municipality of Genzano di Roma, part of Italy's National Civil Protection Service. Like most local civil protection groups, our core work is on the ground: prevention, monitoring, and assistance to the population before, during and after emergencies — earthquakes, floods, wildfires and severe weather.

This note describes something less common: the **public information platform** we built around that work, and the design choices that make it a transferable model rather than just a website.

## The problem we set out to solve

Emergency information usually reaches the people who need it least and misses the people who need it most: older adults, people with disabilities, people with low literacy, non-Italian speakers, and anyone under stress. We treated **accessibility not as a compliance checkbox but as the design starting point** — the principle that if a message does not reach *everyone*, it has not really been published.

## What the practice looks like

The platform is a **static, privacy-first website** (no trackers, no cookies for content, no third-party video embeds) with accessibility built into every layer:

- **Technical accessibility — WCAG 2.2 AA.** Semantic HTML, keyboard navigation, visible focus, computed colour contrast, and a native **accessibility toolbar** (text size, spacing, high-contrast and inverted palettes, dyslexia-friendly font, reduced motion). We deliberately avoid commercial accessibility overlays, which the W3C-WAI and disability organisations advise against.
- **Read-aloud everywhere.** A browser-native text-to-speech button (Web Speech API — no cost, no external service) on every content page, plus estimated reading time and automatic hyphenation to reduce the "wall of text" effect.
- **Cognitive access.** Plain-language *Easy-to-Read* versions of key content; standardised **pictograms** (ISO 7010 safety signs + ARASAAC), and an inline glossary that explains acronyms on first use.
- **Augmentative and Alternative Communication (AAC).** Printable **communication boards** of ARASAAC pictograms, so a person who cannot speak in an emergency — because of aphasia, a cognitive disability, stress, or not speaking Italian — can *point* to what they need.
- **Sign language.** A catalogue of content in **Italian Sign Language (LIS)**.
- **Braille.** A **Braille-ready (BRF) file is generated automatically for every news article** in our build pipeline (open-source *liblouis*, Italian Braille table), downloadable and embosser-ready — a real channel to blind and low-vision readers, complementary to screen readers.
- **Language access.** Core emergency information is available in **eight languages** (Italian plus English, French, German, Spanish, Portuguese, Romanian and Esperanto), with correct `lang`/`hreflang` handling; Easy-to-Read content is additionally offered in further languages, including Arabic.

Around this accessibility core sit the preparedness tools: risk pages with a consistent *before / during / after* structure, **disaster kits tailored to vulnerable groups** (older adults, people with disabilities, infants, pregnancy, pets, caregivers, people on life-saving therapies, people without a fixed address, second-language speakers), an **offline-savable family emergency plan**, school games and quizzes (interface in Italian), a **live dashboard** (real-time seismic, weather, air-quality and marine data from official sources such as INGV and Open-Meteo), and interactive **scrollytelling dossiers** on local risk history.

## Standards and sources

Every claim is traceable to a primary institutional source. Our reference hierarchy: Italian Civil Protection Department (DPC) and AgID content guidelines first; national scientific bodies (CNR, ISPRA, INGV); European operational references (EENA / the 112 single emergency number); and international standards — **WCAG 2.2 AA**, **ISO 22329** (social media in emergencies), and humanitarian references such as **Sphere** and **IFRC** for the vulnerable-groups kits. In Italy the single emergency number is **112**.

## Why it is transferable

The whole platform runs on **open, low-cost, standard technology**: a static site generator, an open design system, browser-native APIs, and open-source tooling (liblouis for Braille, ARASAAC pictograms). There is no proprietary CMS, no runtime server, no licence cost, and hosting is trivial. Any local authority or volunteer organisation can reproduce the model — the hard part is not the technology but the **editorial discipline** of treating accessibility as a starting requirement.

## Recognition

The Group is an accredited organisation of the **European Solidarity Corps** (Quality Label, organisation code **E10435833**, Regulation (EU) 2021/888), and is affiliated with **SNPC Volontariato** and the **FE.PI.VOL.** coordination.

---

**Contact.** Civil Protection Volunteers Group of Genzano di Roma — Via Sicilia 13-15, 00045 Genzano di Roma (RM), Italy · segreteria@protezionecivilegenzano.it · [www.protezionecivilegenzano.it](https://www.protezionecivilegenzano.it/)

*We are happy to share our approach and materials with other civil protection organisations and DRR practitioners.*
