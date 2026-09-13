# -*- coding: utf-8 -*-
"""Dati dei tre album di disegni da colorare.

Le illustrazioni sono pittogrammi ARASAAC nella variante in bianco e nero
(autore Sergio Palao, origine ARASAAC, CC BY-NC-SA 4.0), raccolti in
static/pittogrammi/arasaac-bn/ e citati per id in registro.json.

Ogni voce:
  img   nome del file in arasaac-bn (senza estensione)
  tit   titolo del foglio
  alt   descrizione di cio' che si vede davvero nel disegno
  dida  una riga che spiega a cosa serve, senza istruzioni di autoprotezione
        (quelle stanno nelle schede dedicate, non su un foglio da colorare)
"""

ALBUM = [
 dict(
  slug="disegni-mezzi-infanzia",
  titolo="I mezzi della protezione civile",
  sigla="DIS-M",
  sottotitolo="Album da colorare · Infanzia 4–6 anni e classe prima · 15–20 minuti a foglio · colori",
  intro="Dodici mezzi che si vedono quando la protezione civile lavora. Guarda il disegno, ascolta la frase, poi colora come vuoi.",
  fogli=[
   dict(img="dis-autopompa", tit="L'autopompa", alt="Camion dei pompieri con la scala, la manichetta arrotolata e il lampeggiante.",
        dida="I vigili del fuoco arrivano con l'autopompa: porta l'acqua e la scala."),
   dict(img="dis-ambulanza", tit="L'ambulanza", alt="Ambulanza vista di lato, con la croce e il lampeggiante sul tetto.",
        dida="L'ambulanza porta in ospedale chi sta male."),
   dict(img="dis-camion-rifornimenti", tit="Il camion dei rifornimenti", alt="Camion con il cassone chiuso, visto di lato.",
        dida="Il camion porta acqua, coperte e cibo dove servono."),
   dict(img="dis-camion-tende", tit="Il camion delle tende", alt="Camion con il cassone aperto e le sponde di legno.",
        dida="Sul cassone aperto viaggiano le tende e i materiali del campo."),
   dict(img="dis-furgone-accessibile", tit="Il furgone per tutti", alt="Furgone con la pedana e il simbolo della sedia a rotelle.",
        dida="Con questo furgone viaggia anche chi usa la sedia a rotelle."),
   dict(img="dis-auto", tit="L'auto di servizio", alt="Automobile vista di lato.",
        dida="L'auto serve per arrivare in fretta e per fare i controlli."),
   dict(img="dis-elicottero", tit="L'elicottero", alt="Elicottero in volo, visto di lato.",
        dida="L'elicottero arriva dove le strade non arrivano."),
   dict(img="dis-aereo", tit="L'aereo", alt="Aereo con le ali e i motori, visto da davanti di lato.",
        dida="L'aereo porta persone e materiali molto lontano."),
   dict(img="dis-gommone", tit="Il gommone", alt="Gommone con i remi, visto dall'alto.",
        dida="Il gommone serve quando l'acqua copre le strade."),
   dict(img="dis-drone", tit="Il drone", alt="Drone con quattro eliche e una piccola telecamera.",
        dida="Il drone vola in alto e fa vedere com’è fatto un posto."),
   dict(img="dis-radio", tit="La radio", alt="Radio ricetrasmittente portatile con l'antenna.",
        dida="Con la radio i volontari si parlano anche senza telefono."),
   dict(img="dis-nevicata", tit="La nevicata", alt="Nuvole e neve che cade sulle colline.",
        dida="Quando nevica tanto i volontari aiutano a liberare le strade."),
  ]),
 dict(
  slug="disegni-persone-infanzia",
  titolo="Le persone che aiutano",
  sigla="DIS-P",
  sottotitolo="Album da colorare · Infanzia 4–6 anni e classe prima · 15–20 minuti a foglio · colori",
  intro="Dodici disegni di persone e animali che aiutano. Guarda il disegno, ascolta la frase, poi colora come vuoi.",
  fogli=[
   dict(img="dis-volontari", tit="I volontari", alt="Tre volontari in divisa, uno accanto all'altro.",
        dida="I volontari aiutano gli altri per gentilezza, non per lavoro."),
   dict(img="dis-pompiere", tit="Il vigile del fuoco", alt="Vigile del fuoco che spegne le fiamme con la manichetta.",
        dida="Il vigile del fuoco spegne il fuoco con l'acqua."),
   dict(img="dis-medico", tit="Il medico", alt="Medico con il camice e lo stetoscopio al collo.",
        dida="Il medico visita chi si è fatto male."),
   dict(img="dis-infermiera", tit="L'infermiera", alt="Infermiera con la divisa da lavoro.",
        dida="L'infermiera cura e sta vicino a chi ne ha bisogno."),
   dict(img="dis-cane", tit="Il cane che lavora", alt="Cane seduto, con la pettorina da lavoro.",
        dida="Certi cani portano la pettorina e lavorano con le persone: c\u2019è chi cerca chi si è perso e chi fa compagnia a chi sta male."),
   dict(img="dis-al-telefono", tit="Chi risponde al telefono", alt="Persona che parla al telefono.",
        dida="Chi risponde al telefono ascolta e chiama chi può aiutare."),
   dict(img="dis-adulto-bambino", tit="La mano dell'adulto", alt="Due adulti che tengono per mano un bambino in mezzo a loro.",
        dida="Due adulti e un bambino, mano nella mano."),
   dict(img="dis-famiglia", tit="La famiglia", alt="Due adulti e due bambini, uno accanto all'altro.",
        dida="A casa si sta insieme, tutti quanti."),
   dict(img="dis-gatto", tit="Il gatto di casa", alt="Gatto che cammina, visto di lato.",
        dida="Anche gli animali di casa hanno bisogno di posto e di acqua."),
   dict(img="dis-tenda", tit="La tenda", alt="Tenda da campeggio chiusa, vista di lato.",
        dida="Nella tenda si dorme quando non si può stare in casa."),
   dict(img="dis-acqua", tit="L'acqua", alt="Bottiglia d'acqua accanto a un bicchiere.",
        dida="L’acqua si beve quando si ha sete."),
   dict(img="dis-cortile", tit="Il cortile della scuola", alt="Cortile aperto di una scuola, con gli alberi e il campo.",
        dida="Il cortile è il posto largo dove la classe si ritrova."),
  ]),
 dict(
  slug="disegni-momenti-infanzia",
  titolo="Le giornate insieme",
  sigla="DIS-G",
  sottotitolo="Album da colorare · Infanzia 4–6 anni e classe prima · 15–20 minuti a foglio · colori",
  intro="Dodici disegni delle cose che si fanno stando insieme. Guarda il disegno, ascolta la frase, poi colora come vuoi.",
  fogli=[
   dict(img="dis-campo", tit="Il campo", alt="Due persone sedute davanti a un fuoco, in mezzo alle tende.",
        dida="Al campo si sta insieme anche la sera."),
   dict(img="dis-pentola", tit="La cucina del campo", alt="Pentola grande con il coperchio.",
        dida="Nella pentola grande si cucina per tutti."),
   dict(img="dis-lettura", tit="La lettura", alt="Bambino che legge un libro aperto.",
        dida="Leggere insieme fa passare l'attesa."),
   dict(img="dis-disegno", tit="Il disegno", alt="Mano che disegna su un foglio con la matita.",
        dida="Disegnare aiuta a raccontare quello che si pensa."),
   dict(img="dis-gioco", tit="Il gioco", alt="Due bambini che si passano la palla.",
        dida="Giocare insieme fa stare meglio."),
   dict(img="dis-pallone", tit="Il pallone", alt="Pallone con gli spicchi.",
        dida="Basta un pallone e un posto largo."),
   dict(img="dis-lettera", tit="La lettera", alt="Busta da lettera con il francobollo e l'indirizzo scritto a mano.",
        dida="Scrivere a chi è lontano fa piacere a tutti e due."),
   dict(img="dis-scuola", tit="La scuola", alt="Edificio della scuola con il cortile e lo scivolo.",
        dida="A scuola si impara anche cosa fare se suona l'allarme."),
   dict(img="dis-strisce", tit="Le strisce", alt="Strisce pedonali disegnate sulla strada.",
        dida="Le strisce sono il posto giusto per attraversare la strada."),
   dict(img="dis-temporale", tit="Il temporale", alt="Nuvola con un fulmine.",
        dida="Il temporale porta lampi, tuoni e tanta pioggia."),
   dict(img="dis-sole", tit="Il sole", alt="Sole con i raggi.",
        dida="Dopo il temporale torna il sereno."),
   dict(img="dis-cuore", tit="Il cuore", alt="Cuore disegnato con una linea sola.",
        dida="Aiutare gli altri è una cosa che si fa col cuore."),
  ]),
]
