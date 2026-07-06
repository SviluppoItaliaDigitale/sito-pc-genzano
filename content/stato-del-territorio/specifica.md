---
title: "La specifica aperta della matrice di stato del territorio (v1.0)"
description: "Schema, valori ammessi, endpoint JSON e licenza della matrice di stato del territorio: una specifica aperta che ogni Comune può adottare."
layout: "single"
toc: true
image: ""
date: 2026-07-06
dataUltimaRevisione: "2026-07-06"
---

La [matrice di stato del territorio](/stato-del-territorio/) non è solo una pagina di questo sito: è un **formato aperto** che qualunque Comune, Gruppo comunale o organizzazione di protezione civile può adottare. Questa pagina è la sua specifica: lo schema dei dati, le regole di compilazione, l'endpoint machine-readable e la licenza.

<div class="alert alert-info" role="note">
<p class="mb-0"><i class="bi bi-info-circle me-2" aria-hidden="true"></i><strong>Una proposta aperta, non uno standard ufficiale.</strong> Questa specifica è un'iniziativa del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma, coerente con il concetto illustrato in <a href="/conoscere/oltre-il-ciclo/">Oltre il ciclo</a>. Non è un formato del Dipartimento della Protezione Civile né della Regione Lazio.</p>
</div>

## L'idea in una frase

Per ogni rischio del territorio si dichiara **in quale fase del ciclo di protezione civile ci si trova** (prevenzione, previsione, gestione, superamento), con una descrizione della situazione, la **data dell'ultima verifica** e la **fonte**. Uno stato senza data e senza fonte non vale niente: la disciplina del bollettino di allerta, estesa all'intero quadro dei rischi.

## Lo schema dei dati (v1.0)

La matrice vive in un file dati (`stato_territorio.yaml`). Ogni riga è un rischio, con questi campi:

| Campo | Obbligatorio | Contenuto |
|---|---|---|
| `id` | sì | Identificatore stabile della riga (minuscole e trattini, es. `sismico`). |
| `rischio` | sì | Nome del rischio mostrato al cittadino (es. "Incendi boschivi (AIB)"). |
| `fase` | sì* | Una tra: `prevenzione`, `previsione`, `gestione`, `superamento`. |
| `stato` | sì* | La situazione in una frase, onesta e verificabile. |
| `verificato` | sì* | Data dell'ultima verifica redazionale, formato `AAAA-MM-GG`. |
| `fonte_label` | sì | Etichetta della fonte (es. "Rischio sismico"). |
| `fonte_url` | sì | Collegamento alla pagina che spiega il rischio e cosa fare. |
| `dinamico` | no | Se presente (`allerta` o `incendi`), fase e situazione derivano automaticamente dai dati live del sistema di allertamento; i campi con * diventano il valore di riserva. |
| `stato_verde` | no | Solo per righe `dinamico: allerta`: la frase mostrata quando non c'è allerta. |
| `icona` | no | Icona decorativa (nel nostro caso Bootstrap Icons). |

**Regole di compilazione:**

1. **Ogni stato ha una data.** Una riga non riverificata da troppo tempo è un'informazione scaduta: va ricontrollata e ridatata, non lasciata lì.
2. **Ogni stato ha una fonte.** Il cittadino deve poter risalire alla pagina che spiega il rischio.
3. **L'onestà prima della rassicurazione.** La situazione descrive ciò che è documentabile ("nessun segnale anomalo comunicato"), mai garanzie assolute.
4. **Le righe dinamiche non si compilano a mano.** Dove esiste un dato live (livello di allerta, bollettino AIB), la matrice lo eredita: una sola fonte di verità.
5. **La fase `gestione` compare solo a evento in corso**, e la fase `superamento` solo finché il ritorno alla normalità non è completo.

## L'endpoint machine-readable

La matrice è pubblicata anche in formato JSON, ricostruita a ogni build del sito:

- **[`/stato-del-territorio/index.json`](/stato-del-territorio/index.json)** — l'intera matrice con fase risolta (comprese le righe dinamiche), data di verifica, fonte e metadati (`specifica`, `versione`, `licenza`, `generato`).

Si affianca agli altri dati aperti del sito: il [feed CAP delle allerte](/allerte-meteo/), l'[endpoint dello stato di allerta](/open-data/) e i dataset climatici.

## Licenza e riuso

I dati della matrice sono pubblicati con licenza **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.it)**: puoi riusarli, anche a fini commerciali, citando la fonte ("Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"). Lo schema descritto in questa pagina è liberamente adottabile senza alcuna condizione.

## Come adottarla nel tuo Comune

1. **Elenca i rischi** del tuo territorio (il piano di protezione civile comunale li contiene già).
2. **Compila una riga per rischio** secondo lo schema qui sopra, con data e fonte per ciascuna.
3. **Pubblica la tabella** su una pagina del sito istituzionale e, se puoi, anche il JSON.
4. **Aggancia le righe dinamiche** ai dati di allertamento che già usi (bollettini del Centro Funzionale, campagna AIB).
5. **Datati ogni verifica.** È la regola che tiene in vita tutto il resto.

Per il quadro completo di come questo sito è costruito con strumenti aperti e replicabili, vedi [Un modello replicabile](/modello-accessibile/). Per domande sull'adozione: [contatti](/contatti/).

## Approfondimenti sul nostro sito

- [Lo stato del territorio](/stato-del-territorio/) — la matrice in funzione.
- [Oltre il ciclo: le fasi, le persone, la memoria](/conoscere/oltre-il-ciclo/) — il concetto da cui nasce.
- [Il registro dei disastri che non sono successi](/registro-prevenzione/) — l'altra faccia della trasparenza: gli esiti.
- [Open data](/open-data/) — tutti i dataset aperti del sito.
