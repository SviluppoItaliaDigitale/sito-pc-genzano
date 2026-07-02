---
title: "À propos de cette pratique — Une communication d'urgence accessible dès la conception"
description: "Les Volontaires de Protection civile de Genzano di Roma ont conçu une plateforme d'information d'urgence accessible et respectueuse de la vie privée."
layout: "single"
language: "fr"
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

**Une note de bonne pratique destinée à la communauté de la réduction des risques de catastrophe.**

Le **Groupe communal des Volontaires de Protection civile de Genzano di Roma** est une organisation de bénévoles (OdV) de la commune de Genzano di Roma, qui fait partie du Service national italien de protection civile. Comme la plupart des groupes locaux de protection civile, notre cœur de métier se déploie sur le terrain : prévention, surveillance et assistance à la population avant, pendant et après les situations d'urgence — séismes, inondations, feux de forêt et intempéries.

Cette note décrit une réalité moins répandue : la **plateforme d'information publique** que nous avons bâtie autour de ce travail, et les choix de conception qui en font un modèle transposable, et non un simple site web.

## Le problème que nous avons voulu résoudre

L'information d'urgence atteint le plus souvent les personnes qui en ont le moins besoin et néglige celles qui en ont le plus besoin : les personnes âgées, les personnes en situation de handicap, les personnes peu alphabétisées, celles qui ne parlent pas italien, et toute personne soumise au stress. Nous avons abordé **l'accessibilité non comme une case à cocher réglementaire, mais comme le point de départ de la conception** — partant du principe qu'un message qui n'atteint pas *tout le monde* n'a pas vraiment été publié.

## À quoi ressemble cette pratique

La plateforme est un **site web statique, respectueux de la vie privée** (aucun traceur, aucun cookie pour les contenus, aucune vidéo intégrée de tiers), avec l'accessibilité intégrée à chaque niveau :

- **Accessibilité technique — WCAG 2.2 AA.** HTML sémantique, navigation au clavier, focus visible, contraste des couleurs calculé, et une **barre d'outils d'accessibilité** native (taille du texte, espacement, palettes à fort contraste et inversées, police adaptée à la dyslexie, mouvement réduit). Nous évitons délibérément les surcouches d'accessibilité commerciales, déconseillées par le W3C-WAI et les organisations de personnes handicapées.
- **Lecture à voix haute partout.** Un bouton de synthèse vocale natif du navigateur (Web Speech API — sans coût, sans service externe) sur chaque page de contenu, ainsi qu'une durée de lecture estimée et une césure automatique pour atténuer l'effet « mur de texte ».
- **Accès cognitif.** Des versions en *langage clair* (Facile à lire) des contenus essentiels ; des **pictogrammes** normalisés (signaux de sécurité ISO 7010 + ARASAAC) ; et un glossaire en ligne qui explique les sigles dès leur première occurrence.
- **Communication alternative et améliorée (CAA).** Des **tableaux de communication** imprimables composés de pictogrammes ARASAAC, pour qu'une personne incapable de parler en situation d'urgence — à cause d'une aphasie, d'un handicap cognitif, du stress ou parce qu'elle ne parle pas italien — puisse *désigner* ce dont elle a besoin.
- **Langue des signes.** Un catalogue de contenus en **langue des signes italienne (LIS)**.
- **Braille.** Un **fichier braille (BRF) est généré automatiquement pour chaque article d'actualité** dans notre chaîne de production (le logiciel libre *liblouis*, table braille italienne), téléchargeable et prêt à être embossé — un canal réel vers les lecteurs aveugles et malvoyants, complémentaire des lecteurs d'écran.
- **Accès linguistique.** L'information d'urgence essentielle est disponible en **huit langues** (l'italien, plus l'anglais, le français, l'allemand, l'espagnol, le portugais, le roumain et l'espéranto), avec une gestion correcte des attributs `lang`/`hreflang` ; les contenus Facile à lire sont en outre proposés dans d'autres langues, dont l'arabe.

Autour de ce socle d'accessibilité s'articulent les outils de préparation : des pages sur les risques suivant une structure homogène *avant / pendant / après*, des **kits de catastrophe adaptés aux groupes vulnérables** (personnes âgées, personnes en situation de handicap, nourrissons, femmes enceintes, animaux de compagnie, aidants, personnes sous traitement vital, personnes sans domicile fixe, personnes de langue seconde), un **plan familial d'urgence enregistrable hors ligne**, des jeux et quiz scolaires (interface en italien), un **tableau de bord en temps réel** (données sismiques, météorologiques, de qualité de l'air et marines issues de sources officielles telles qu'INGV et Open-Meteo), et des **dossiers interactifs** de type scrollytelling sur l'histoire des risques locaux.

## Normes et sources

Chaque affirmation est traçable jusqu'à une source institutionnelle primaire. Notre hiérarchie de référence : d'abord le Département de la protection civile italienne (DPC) et les lignes directrices éditoriales de l'AgID ; puis les organismes scientifiques nationaux (CNR, ISPRA, INGV) ; les références opérationnelles européennes (EENA / le numéro d'urgence unique 112) ; et les normes internationales — **WCAG 2.2 AA**, **ISO 22329** (réseaux sociaux en situation d'urgence) et des références humanitaires telles que **Sphere** et l'**IFRC** pour les kits destinés aux groupes vulnérables. En Italie, le numéro d'urgence unique est le **112**.

## Pourquoi elle est transposable

L'ensemble de la plateforme repose sur des **technologies ouvertes, peu coûteuses et standard** : un générateur de site statique, un système de design ouvert, des API natives du navigateur et des outils libres (liblouis pour le braille, pictogrammes ARASAAC). Il n'y a aucun CMS propriétaire, aucun serveur d'exécution, aucun coût de licence, et l'hébergement est trivial. Toute collectivité locale ou organisation de bénévoles peut reproduire ce modèle — la difficulté ne réside pas dans la technologie, mais dans la **discipline éditoriale** consistant à traiter l'accessibilité comme une exigence de départ.

## Reconnaissance

Le Groupe est une organisation accréditée du **Corps européen de solidarité** (European Solidarity Corps — Quality Label, code d'organisation **E10435833**, règlement (UE) 2021/888), et il est affilié à **SNPC Volontariato** et à la coordination **FE.PI.VOL.**.

---

**Contact.** Groupe communal des Volontaires de Protection civile de Genzano di Roma — Via Sicilia 13-15, 00045 Genzano di Roma (RM), Italie · segreteria@protezionecivilegenzano.it · [www.protezionecivilegenzano.it](https://www.protezionecivilegenzano.it/)

*Nous serons heureux de partager notre approche et nos ressources avec d'autres organisations de protection civile et acteurs de la réduction des risques de catastrophe.*
