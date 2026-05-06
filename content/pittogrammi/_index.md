---
title: "Catalogo dei pittogrammi del sito"
description: "Catalogo dei pittogrammi ISO 7010 e ARASAAC usati sul sito per migliorare la comprensione di bambini, persone con disabilità cognitive, anziani e L2."
layout: "single"
toc: false
sitemap:
  priority: 0.4
  changefreq: monthly
dataUltimaRevisione: "2026-04-27"
---

Questa pagina elenca tutti i **pittogrammi standardizzati** disponibili nella libreria del sito, utilizzabili dalla redazione tramite lo shortcode Hugo `{{</* pittogramma src="..." alt="..." */>}}`.

I pittogrammi affiancano i testi per renderli **comprensibili** a chi non parla bene l'italiano, ai bambini, alle persone con disabilità cognitive o difficoltà di lettura, agli anziani.

## Come si usano (per la redazione)

Uso block (figure centrata con didascalia opzionale):

```go-html-template
{{</* pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto" */>}}
```

Uso inline (dentro una frase):

```go-html-template
Chiama subito il {{</* pittogramma src="/pittogrammi/arasaac/112.png" alt="numero 112" inline="true" */>}} 112.
```

**Parametri:** `src` (obbligatorio), `alt` (obbligatorio), `caption` (opzionale, solo block), `inline="true"` per inserimento dentro una frase, `size` (small / medium / large / xlarge, default medium).

## Regole d'uso editoriale

1. Il pittogramma è **supporto** alla comprensione, mai sostituto del testo (WCAG 1.4.5).
2. Un pittogramma per concetto chiave, non come decorazione visiva continua.
3. Per segnali di sicurezza formali (obblighi, divieti, avvertimenti): preferire **ISO 7010**.
4. Per situazioni narrative o didattiche per bambini: preferire **ARASAAC**.
5. **`alt` sempre descrittivo**, mai stringa vuota o "Immagine di...".

Per istruzioni complete sull'uso, regole editoriali, attribuzioni e procedura di download, vedi `manuale/parte-03-immagini-per-gli-articoli.md` § 3.16 (sezione pittogrammi).

## Catalogo completo

## Kit consigliato per questo rischio

Per il rischio sismico tieni pronto un kit leggero e raggiungibile, utile sia se devi uscire rapidamente sia se devi restare in casa senza servizi.

- acqua in litri sufficienti per la famiglia;
- torcia con pile o ricarica funzionante;
- radio a pile o a manovella;
- power bank carico;
- fischietto per segnalare la presenza;
- scarpe chiuse, guanti da lavoro e piccola coperta termica;
- copie dei documenti, farmaci abituali e numeri utili.

Approfondisci nella pagina [Kit di emergenza: casa, evacuazione e auto](/rischi-prevenzione/kit-emergenza/).

