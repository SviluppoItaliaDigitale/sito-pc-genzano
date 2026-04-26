---
title: "Catalogo dei pittogrammi del sito"
description: "Catalogo dei pittogrammi standardizzati ISO 7010 e ARASAAC AAC utilizzati sul sito della Protezione Civile di Genzano di Roma per migliorare la comprensione di bambini, persone con disabilità cognitive e cittadini stranieri."
layout: "single"
toc: false
sitemap:
  priority: 0.4
  changefreq: monthly
---

Questa pagina elenca i **pittogrammi standardizzati** disponibili sul sito, utilizzabili dalla redazione tramite lo shortcode Hugo `{{</* pittogramma codice="..." alt="..." */>}}`. I pittogrammi affiancano i testi per renderli **comprensibili** a chi non parla bene l'italiano, ai bambini, alle persone con disabilità cognitive o difficoltà di lettura.

## ISO 7010 — Segnaletica internazionale di sicurezza

I pittogrammi della norma **ISO 7010** sono lo **standard mondiale** per la segnaletica di sicurezza nei luoghi di lavoro, negli edifici pubblici, nelle vie di esodo, sui veicoli di emergenza. Sono di **pubblico dominio** (la norma è pubblica). Riconoscibili in oltre 160 Paesi.

**Codici colore standardizzati:**
- 🟡 **Giallo + triangolo** = avvertimento (W001-W099): pericolo presente.
- 🔴 **Rosso + cerchio sbarrato** = divieto (P001-P099): comportamento vietato.
- 🔵 **Blu + cerchio pieno** = obbligo (M001-M099): comportamento obbligatorio.
- 🟢 **Verde + rettangolo** = soccorso e vie di fuga (E001-E099): condizione sicura.
- 🔴 **Rosso + rettangolo** = antincendio (F001-F099): attrezzature antincendio.

> **Stato della libreria.** La libreria parte vuota nel repository. Per garantire la **fedeltà grafica alla norma**, i pittogrammi ufficiali vanno scaricati da Wikimedia Commons (PD/CC0) eseguendo dalla macchina locale:
>
> ```bash
> bash scripts/scarica-pittogrammi-iso7010.sh
> git add static/pittogrammi/iso7010/
> git commit -m "Pittogrammi ISO 7010: download ufficiale Wikimedia"
> git push
> ```
>
> Una volta scaricati, le anteprime sotto saranno popolate automaticamente. **Non inserire pittogrammi disegnati a mano**: solo gli SVG Wikimedia hanno le geometrie e le proporzioni esatte della norma.

### Avvertimenti (giallo)

<div class="pittogrammi-galleria">

{{< pittogramma codice="W001" alt="Pericolo generale" label="W001 — Pericolo generale" size="80" >}}
{{< pittogramma codice="W002" alt="Esplosivo" label="W002 — Esplosivo" size="80" >}}
{{< pittogramma codice="W003" alt="Radioattivo" label="W003 — Radioattivo" size="80" >}}
{{< pittogramma codice="W009" alt="Rischio biologico" label="W009 — Biologico" size="80" >}}
{{< pittogramma codice="W012" alt="Tensione elettrica pericolosa" label="W012 — Tensione" size="80" >}}
{{< pittogramma codice="W016" alt="Sostanza tossica" label="W016 — Tossico" size="80" >}}
{{< pittogramma codice="W021" alt="Materiali infiammabili" label="W021 — Infiammabile" size="80" >}}
{{< pittogramma codice="W038" alt="Frana" label="W038 — Frana" size="80" >}}

</div>

### Vie di fuga e soccorso (verde)

<div class="pittogrammi-galleria">

{{< pittogramma codice="E001" alt="Uscita di emergenza a sinistra" label="E001 — Uscita ←" size="80" >}}
{{< pittogramma codice="E002" alt="Uscita di emergenza a destra" label="E002 — Uscita →" size="80" >}}
{{< pittogramma codice="E003" alt="Pronto soccorso" label="E003 — Pronto soccorso" size="80" >}}
{{< pittogramma codice="E004" alt="Telefono di emergenza" label="E004 — Telefono emergenza" size="80" >}}
{{< pittogramma codice="E007" alt="Punto di raccolta evacuazione" label="E007 — Punto raccolta" size="80" >}}
{{< pittogramma codice="E009" alt="Medico" label="E009 — Medico" size="80" >}}
{{< pittogramma codice="E011" alt="Acqua potabile" label="E011 — Acqua potabile" size="80" >}}

</div>

### Antincendio (rosso)

<div class="pittogrammi-galleria">

{{< pittogramma codice="F001" alt="Estintore" label="F001 — Estintore" size="80" >}}
{{< pittogramma codice="F002" alt="Idrante" label="F002 — Idrante" size="80" >}}
{{< pittogramma codice="F004" alt="Presidi antincendio" label="F004 — Presidi" size="80" >}}
{{< pittogramma codice="F005" alt="Allarme antincendio" label="F005 — Allarme incendio" size="80" >}}

</div>

### Obbligo e divieto

<div class="pittogrammi-galleria">

{{< pittogramma codice="M001" alt="Obbligo generale" label="M001 — Obbligo" size="80" >}}
{{< pittogramma codice="M002" alt="Leggere le istruzioni" label="M002 — Leggi istruzioni" size="80" >}}
{{< pittogramma codice="P001" alt="Divieto generale" label="P001 — Divieto" size="80" >}}
{{< pittogramma codice="P002" alt="Vietato fumare" label="P002 — Vietato fumare" size="80" >}}

</div>

## ARASAAC — Comunicazione Aumentativa Alternativa (CAA/AAC)

I pittogrammi **ARASAAC** sono la libreria **Open** del Centro Aragonese di Comunicazione Aumentativa Alternativa, usata in tutto il mondo nella didattica, nella riabilitazione, nella comunicazione con persone con autismo, disabilità cognitive, afasia, demenze.

**Licenza:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.it). Attribuzione: Sergio Palao — ARASAAC ([arasaac.org](https://arasaac.org)) — Governo dell'Aragona (Spagna).

I pittogrammi ARASAAC sul nostro sito sono usati principalmente nella pagina [Facile da leggere](/facile-da-leggere/) e in alcuni contenuti di [Abili a Proteggere](/abili-a-proteggere/).

> **Nota tecnica.** Sull'ambiente di sviluppo i pittogrammi ARASAAC vanno scaricati eseguendo `bash scripts/scarica-pittogrammi-arasaac.sh` sulla macchina locale (la sandbox Claude Code blocca gli host esterni). Una volta scaricati, lo shortcode `{{</* pittogramma codice="<id>" set="arasaac" */>}}` li rende disponibili.

## Come usare i pittogrammi nei contenuti

```markdown
{{</* pittogramma codice="W001" alt="Attenzione: pericolo generale" */>}}
{{</* pittogramma codice="E002" alt="Uscita di emergenza" label="Uscita" size="96" */>}}
{{</* pittogramma codice="2453" set="arasaac" alt="Bambino che corre via" */>}}
```

**Regole d'uso (linee editoriali):**

1. **Mai sostituire il testo**: il pittogramma è un *complemento*, non un sostituto. L'`alt` deve essere sempre testuale ed equivalente.
2. **Massimo 3-4 pittogrammi per pagina**: evitare il sovraccarico visivo.
3. **Coerenza tematica**: usa pittogrammi che corrispondono effettivamente al contenuto vicino, non come decorazione.
4. **Dimensione standard**: 64 px (default) per inserimento inline; 80-96 px per gallerie o blocchi evidenti.
5. **Toolbar di accessibilità**: i pittogrammi sono **funzionali** e restano visibili anche con "Nascondi immagini" attivo.

## Per chi vuole approfondire

- [ISO 7010 — Wikipedia](https://it.wikipedia.org/wiki/ISO_7010) — elenco completo dei codici e dei significati.
- [ARASAAC — portale ufficiale](https://arasaac.org) — ricerca e download di oltre 12.000 pittogrammi.
- [WCAG 2.2 — non solo testo](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) — perché immagini funzionali devono avere alternativa testuale.
- [Designers Italia — Accessibilità cognitiva](https://designers.italia.it/) — linee guida AGID per testi facili da capire.

---

*Aggiunte di nuovi pittogrammi: usa lo script `scripts/scarica-pittogrammi-iso7010.sh` (per ISO) o `scripts/scarica-pittogrammi-arasaac.sh` (per ARASAAC). I file SVG/PNG vanno in `static/pittogrammi/iso7010/` o `static/pittogrammi/arasaac/`. Lo shortcode li trova automaticamente.*
