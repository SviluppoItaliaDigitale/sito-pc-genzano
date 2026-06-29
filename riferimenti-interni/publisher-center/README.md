# Google Publisher Center — materiali pronti

Cartella **non pubblicata** (Hugo non costruisce `riferimenti-interni/`): serve a tenere
insieme i materiali per registrare la testata su **publishercenter.google.com**.
Vale insieme alla `news-sitemap.xml` (già attiva e dichiarata in `robots.txt`) e
all'invio della sitemap in Google Search Console.

## Loghi (caricali in Publisher Center)

| File | Misura | Uso |
|---|---|---|
| `logo-quadrato-1024.png` | 1024×1024, PNG trasparente | logo quadrato (stemma del Gruppo) |
| `logo-rettangolare-1000x300.png` | 1000×300, PNG sfondo bianco | logo orizzontale (stemma + dicitura) |

Se la schermata chiede una misura precisa diversa, rigenerali da
`static/images/logo-pc-genzano-hires.png` (stemma 1080×1080).

## Scheda dati della pubblicazione

| Campo | Valore |
|---|---|
| Nome testata | Protezione Civile Genzano di Roma |
| Sito principale | https://www.protezionecivilegenzano.it/ |
| Lingua | Italiano (it) |
| Paese | Italia |
| Categoria | Notizie locali / Sicurezza pubblica |
| Email | segreteria@protezionecivilegenzano.it |
| Telefono | +39 06 9362600 |

## Descrizione della pubblicazione (campo "Informazioni / About")

> Notiziario ufficiale del Gruppo Comunale Volontari di Protezione Civile di
> Genzano di Roma. Pubblichiamo allerte e avvisi, indicazioni di autoprotezione,
> attività ed esercitazioni del Gruppo, formazione e informazione di servizio per
> i cittadini dei Castelli Romani. Fonti istituzionali (Dipartimento della
> Protezione Civile, Regione Lazio, INGV, ISPRA), linguaggio chiaro AGID,
> contenuti accessibili (WCAG 2.2 AA).

Versione breve (se il campo è corto):

> Notiziario ufficiale del Gruppo Comunale Volontari di Protezione Civile di
> Genzano di Roma: allerte, autoprotezione, attività del Gruppo e informazione di
> servizio per i Castelli Romani.

## Sezione / Feed da aggiungere

Aggiungi una sezione di contenuti con questa fonte RSS:

| Campo | Valore |
|---|---|
| Titolo sezione | Comunicazioni e Notizie |
| Tipo di contenuto | Feed RSS |
| URL del feed | https://www.protezionecivilegenzano.it/comunicazioni/index.xml |
| Descrizione sezione | Comunicati, allerte, attività ed esercitazioni del Gruppo Comunale di Protezione Civile di Genzano di Roma. |

Feed alternativo dell'intero sito (home): `https://www.protezionecivilegenzano.it/index.xml`

## Passi (promemoria)

1. publishercenter.google.com → accedi con l'account che ha la **Search Console** del dominio.
2. Aggiungi pubblicazione → nome + URL come sopra.
3. Impostazioni: Paese Italia, Lingua Italiano, email/telefono, carica i due loghi.
4. Verifica proprietà (deve essere già verificata in Search Console, stesso account).
5. Aggiungi la sezione "Comunicazioni e Notizie" con il feed RSS sopra.
6. Salva e invia in revisione.

## Nota onesta

Publisher Center governa **come** appare la testata (nome, logo, sezioni) e aiuta il
riconoscimento come fonte; **non garantisce** l'ingresso nella scheda "Notizie" /
Google News, che resta algoritmico. Lavora insieme a: `news-sitemap.xml` (scoperta
rapida, già attiva) + invio della sitemap in Search Console.
