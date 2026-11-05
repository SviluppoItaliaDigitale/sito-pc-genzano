"""Scrive content/formazione/video-per-la-classe/_index.md dai sottotitoli .vtt dei video.
Un video nuovo si aggiunge alla lista V; le durate le legge ffprobe, le trascrizioni i file .vtt in static/video/."""
import re, subprocess
V = [
  ("2026-11-01-112-numero-emergenza-video", "Il 112: come si chiama in emergenza",
   "Infanzia e primaria 1ª-2ª, ottobre: «Chi chiamo se ho bisogno», «Il 112: quando e come»", "/numeri-utili/", "Numeri utili"),
  ("2026-11-01-terremoto-cosa-fare-video", "Terremoto: cosa fare prima, durante e dopo",
   "Infanzia e primaria, ottobre-dicembre: «Quando trema la terra», «Terremoto: prima, durante, dopo»", "/rischi-prevenzione/rischio-sismico/", "Rischio sismico"),
  ("2026-11-01-vulcano-colli-albani-video", "Il vulcano dei Colli Albani",
   "Secondaria di primo grado, gennaio-febbraio, e di secondo grado, ottobre", "/rischi-prevenzione/rischio-vulcanico/", "Rischio vulcanico"),
  ("2026-11-01-alluvione-bambini-video", "Quando piove forte: come stare al sicuro dall'acqua",
   "Primaria 3ª-5ª, novembre-dicembre: «Acqua, frane e alluvioni»; secondaria, marzo-aprile e novembre-dicembre", "/rischi-prevenzione/rischio-idrogeologico/", "Rischio idrogeologico"),
  ("2026-11-01-allerta-colori-bambini-video", "I colori dell'allerta meteo e che cosa fare",
   "Infanzia e primaria, gennaio-febbraio: «I colori dell'allerta»; secondaria di primo grado, novembre-dicembre", "/allerte-meteo/", "Allerte meteo"),
  ("2026-11-01-kit-emergenza-bambini-video", "Il kit di emergenza",
   "Infanzia e primaria, marzo-maggio: «Il mio zainetto», «La mia casa preparata», «Il piano della mia famiglia»", "/rischi-prevenzione/kit-emergenza/", "Kit di emergenza"),
  ("2026-11-01-incendi-bambini-video", "Il fuoco nel bosco: come nasce e che cosa fare",
   "Primaria 1ª-2ª, marzo-aprile: «Fumo e fuoco»; tutte le classi prima dell'estate", "/rischi-prevenzione/rischio-incendio/", "Rischio incendio"),
  ("2026-11-01-caldo-ondate-di-calore-video", "Il caldo: come proteggersi",
   "Secondaria di secondo grado, marzo-aprile: «Il caldo e le persone fragili»; tutte le classi prima dell'estate", "/rischi-prevenzione/ondate-di-calore/", "Ondate di calore"),
  ("2026-11-01-notizie-false-emergenza-video", "Notizie vere e notizie false in emergenza",
   "Primaria 3ª-5ª, maggio; secondaria di primo grado, ottobre; secondaria di secondo grado, gennaio-febbraio", "/formazione/schede-stampabili/fake-news-emergenza-secondaria/", "Scheda «Notizie false in emergenza»"),
  ("2026-11-01-volontariato-protezione-civile-video", "La protezione civile e i volontari",
   "Infanzia, maggio: «Le persone che ci aiutano»; secondaria di secondo grado, maggio", "/diventa-volontario/", "Diventa volontario"),
]
def durata(f):
    s = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
    m, s = divmod(round(s), 60)
    return f"{m} min {s:02d} s" if m else f"{s} s"
def trascrizione(vtt):
    righe, out = open(vtt).read().splitlines(), []
    for r in righe:
        r = r.strip()
        if not r or r == "WEBVTT" or r.isdigit() or "-->" in r: continue
        out.append(r)
    return " ".join(out)
corpo = []
for base, titolo, incontro, link, etichetta in V:
    mp4 = f"static/video/{base}-16x9.mp4"
    corpo.append(f"""## {titolo}

**Durata:** {durata(mp4)} · **Nel programma dell'anno:** {incontro}

{{{{< video src="/video/{base}-16x9.mp4" poster="/video/{base}-16x9-poster.webp" titolo="Video con voce e sottotitoli: {titolo}" >}}}}

<details class="faq-item">
<summary><strong>Trascrizione del video</strong></summary>

{trascrizione(f"static/video/{base}.vtt")}

</details>

Per approfondire: [{etichetta}]({link}).
""")
testa = """---
title: "Video per la classe"
description: "Video brevi e animati, con voce e sottotitoli, da proiettare sulla LIM: uno per ogni argomento del Programma dell'anno, dall'infanzia alle superiori."
date: 2026-11-01
draft: false
type: "page"
layout: "single"
toc: true
dataUltimaRevisione: "2026-11-01"
---

Video brevi da proiettare in classe sulla LIM o con il proiettore. Hanno la voce e i sottotitoli già nel video, quindi si capiscono anche con l'audio basso. Sono in formato orizzontale 16:9: avviali e usa lo schermo intero del lettore.

I video seguono gli incontri del [Programma dell'anno per la classe](/formazione/programma-dell-anno/), dall'infanzia alla secondaria di secondo grado: c'è un video per ogni argomento. Sono animati e semplici, adatti ai più piccoli, ma il contenuto è quello delle pagine ufficiali del sito e va bene anche con i ragazzi più grandi. Sotto ogni video c'è la trascrizione, da leggere con chi non sente l'audio o da usare per preparare le domande.

## Come usarli in classe

1. Guarda il video da solo prima della lezione.
2. Proiettalo dopo una domanda alla classe: «Che cosa faresti se…?».
3. Fermalo dove serve e chiedi agli alunni di ripetere il gesto o la regola.
4. Chiudi con l'attività della lezione del mese, in [Crea la mia lezione](/formazione/crea-la-mia-lezione/).

"""
coda = """
## Per i ragazzi più grandi

Con la secondaria si può partire da uno di questi video e continuare con il [documentario sulla storia della protezione civile](/comunicazioni/2026-10-23-documentario-storia-protezione-civile/): meno di cinque minuti, da Messina 1908 a IT-alert, con foto vere dei disastri. Per questo è adatto ai ragazzi, non ai bambini.

Le pagine [Rischio idrogeologico](/rischi-prevenzione/rischio-idrogeologico/), [Allerte meteo](/allerte-meteo/), [Kit di emergenza](/rischi-prevenzione/kit-emergenza/) e [Rischio incendio](/rischi-prevenzione/rischio-incendio/) hanno anche video più lunghi e con più dettagli sugli stessi argomenti, adatti alla secondaria.

## Vedi anche

- [Programma dell'anno per la classe](/formazione/programma-dell-anno/)
- [Verifica prima e dopo](/formazione/verifica-prima-e-dopo/)
- [Audio e podcast](/audio-e-podcast/)
"""
open("content/formazione/video-per-la-classe/_index.md", "w").write(testa + "\n".join(corpo) + coda)
print("pagina scritta")
