# Serie di caratteri per il controllo dei fogli di stampa

Quattro configurazioni di fontconfig che `scripts/check-fogli-stampa.py` passa a
Chromium (variabile `FONTCONFIG_FILE`) per stampare schede, kit e storie con
caratteri di larghezza diversa.

## Perché servono

Le schede stampabili, le schede dei kit calamità e le storie non hanno caratteri
propri: usano quelli del computer che le stampa. La stessa riga è più larga o più
stretta a seconda del sistema, e una pagina che sulla macchina di controllo sta
in un foglio può mandare la fascia delle affiliazioni da sola su un foglio in più
su un altro computer.

Fino al 21/10/2026 il controllo stampava solo con i caratteri della CI
(Liberation, con le misure di Arial e Times). Il 22/10/2026 una misura con
queste serie ha trovato 72 pagine stampabili che con caratteri più larghi
lasciavano un foglio quasi vuoto: 68 corrette riducendo la loro scala di
stampa, 4 stringendo gli spazi o spostando un'interruzione di pagina.

## Le serie

| Serie | Si usa per | Caratteri della prova | Al posto di | Larghezza media |
|---|---|---|---|---|
| `liberation` | tutto | Liberation Sans, Serif, Mono | Arial, Times New Roman, Courier New (stesse misure) | riferimento |
| `windows-mac` | schede, storie | Inter; Gelasio per Georgia | i caratteri di sistema di Windows e Mac, Georgia | Inter +7% rispetto ad Arial; Gelasio come Georgia, +10% rispetto a Times |
| `adventor` | kit | TeX Gyre Adventor | Century Gothic (Windows e Mac con Office), URW Gothic (Linux), con le misure di Avant Garde | +10% rispetto ad Arial |
| `dejavu` | schede, kit, storie | DejaVu Sans, DejaVu Serif | un Linux senza i caratteri di Arial e Times | +14% rispetto ad Arial, +28% rispetto a Times |

Larghezza media misurata il 22/10/2026 su un testo italiano di 270 caratteri
(Pillow, corpo 100). Il campione di pagine del sito usa solo `liberation`: il
sito ha i suoi caratteri (Titillium Web).

## Come sono fatte

- Includono la configurazione di sistema e poi escludono (`rejectfont`) i
  caratteri delle altre serie: ogni serie dà sempre gli stessi caratteri.
- Escludono anche i caratteri che le pagine chiedono per nome (Arial, Verdana,
  Georgia, Comic Sans MS, Trebuchet MS, Segoe UI, Roboto…) e i caratteri
  Microsoft, se la macchina li avesse: la prova non deve cambiare con ciò che è
  installato. Fa eccezione Georgia nella serie `windows-mac`.
- `windows-mac` aggiunge la cartella `gelasio/` e, solo per la prova, presenta
  Gelasio con il nome di Georgia. Chromium accetta un carattere diverso da quello
  chiesto solo se ha lo stesso nome o se è nella sua tabella di sostituti con le
  stesse misure, dove Gelasio non c'è.
- Prima di stampare, lo script controlla dentro Chromium quale carattere esce da
  ogni pila dei fogli di stile (`PILE` e `ATTESI` nello script). Se non è quello
  atteso si ferma: meglio un controllo fermo che un controllo fatto con i
  caratteri sbagliati.

## Limiti

- Sono punti di larghezza, non i caratteri veri: quelli di sistema di Windows e
  Mac non si installano su Linux.
- Alcune pagine chiedono caratteri propri (Comic Sans MS, Trebuchet MS, Verdana,
  Courier New): nella prova ricadono sui caratteri della serie, per esempio Comic
  Sans MS diventa Liberation Sans, Inter, TeX Gyre Adventor o DejaVu Sans.
- Nelle serie `windows-mac` e `adventor` Times New Roman e il generico `serif`
  diventano DejaVu Serif, più largo di Times: la prova è più severa del vero, ma
  non più della serie `dejavu`, con cui quelle pagine si stampano comunque.
- Il problema non cresce in modo regolare con la larghezza: una pagina che passa
  con tutte le serie può ancora sforare con una larghezza che sta in mezzo. Il
  controllo copre i casi più comuni, non ogni computer.

## Che cosa serve

Ubuntu 24.04 con i pacchetti `fonts-liberation fonts-inter fonts-texgyre
fonts-dejavu-core fonts-noto-color-emoji`, Playwright con il suo Chromium e
PyMuPDF. I workflow fissano Playwright (e quindi Chromium) alla versione con cui
sono state misurate le scale: un aggiornamento si fa con una pull request
dedicata, dopo aver rifatto il controllo completo.

Gelasio non ha un pacchetto Ubuntu ed è qui, in `gelasio/`:

- disegnato da Eben Sorkin (copyright The Gelasio Project Authors), versione
  1.008, licenza SIL Open Font License 1.1 (`gelasio/OFL.txt`);
- dal repository ufficiale di Google Fonts, `github.com/google/fonts`, cartella
  `ofl/gelasio`, ramo `main`, scaricato il 22/10/2026;
- la descrizione ufficiale lo dichiara «metrics compatible with Georgia» nel
  tondo, nel nero e nei corsivi;
- sha256 `Gelasio[wght].ttf`
  `4daecea457258c9ebeb8bc99ed3fd24353618bfad3ea4b93fa0b5d0468fc04e4`,
  `Gelasio-Italic[wght].ttf`
  `52559e845a4d33514e5f93bb9ae7dbeae1894a53f2c565a15f18af40cd337c09`.

Serve solo a questa prova: nessuna pagina del sito lo usa. Il pacchetto
dell'Open Kit di questo controllo non lo contiene, come le altre librerie di
terzi: chi riusa il controllo lo scarica dalla fonte indicata qui sopra.

## Se il controllo si ferma

«I caratteri della prova non sono quelli attesi» vuol dire che una serie non dà
i caratteri previsti:

1. installa i pacchetti elencati sopra;
2. rifai le cache di fontconfig, anche quella della serie `windows-mac`, che
   contiene il nome di Georgia dato a Gelasio (il percorso deve essere
   assoluto):
   `fc-cache -f` e `FONTCONFIG_FILE="$PWD/scripts/fogli-stampa/caratteri/windows-mac.conf" fc-cache -f`;
3. controlla: `FONTCONFIG_FILE="$PWD/scripts/fogli-stampa/caratteri/windows-mac.conf" fc-match Georgia`
   deve rispondere con il file di Gelasio e il nome «Georgia».

Se invece è cambiata una pila di caratteri in un foglio di stile, lo script lo
dice: si aggiornano `PILE` e `ATTESI` nello script e, se serve, le serie.

## Quando una pagina non passa

Si riduce la scala di stampa della sola pagina, al massimo del 12%, con un
commento «controllo fogli di stampa» accanto alla regola. Si prendono le scale
che passano con tutte le serie e che, con `liberation` e con la seconda serie
della famiglia (`windows-mac` per schede e storie, `adventor` per i kit), non
stampano più fogli di prima; fra queste si preferiscono quelle che non lasciano
nessun foglio con meno del 15% stampato e, a parità, la più vicina alla scala
attuale. Se nessuna scala basta, si stringono gli spazi della pagina o si
sposta un'interruzione di pagina. Per vedere i fogli:

```
python3 scripts/check-fogli-stampa.py --pagine formazione/schede-stampabili/NOME/ --png /tmp/fogli
```

Una scheda stampabile si controlla anche dentro i pacchetti «Stampa tutto», e
`--pagine` stampa da sé le sue sezioni. Nel pacchetto la scala della scheda
diventa lo zoom della sua sezione, che rimpicciolisce anche gli spazi in
millimetri: la scala deve passare in tutti e due i modi. Dopo una scala nuova si
rigenerano i pacchetti con `python3 scripts/genera-pacchetti-schede.py` e gli
ZIP dei kit con `python3 scripts/genera-pacchetti-kit.py`.
