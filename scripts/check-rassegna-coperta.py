#!/usr/bin/env python3
"""check-rassegna-coperta.py — nessuna notizia del territorio chiusa in silenzio.

La routine «Rassegna normativa e albo pretorio» lo esegue prima di chiudere
una issue: legge il JSON di scripts/normativa-watcher.py e il testo del
commento di chiusura, e si ferma (uscita 1) se una voce del territorio
(Genzano e Castelli Romani, rilevanza diretta o indiretta) non è nominata nel
commento con il suo link o con il suo titolo.

Nasce il 07/11/2026: il 06/11/2026 la notizia di Castelli Notizie sui 345 mila
euro per gli alberi di Genzano era fra le voci trovate, ma la sessione della
sera ha guardato solo una parte della rassegna e ha chiuso il giro con
«nessuna notizia nuova».

Uso:
  python3 scripts/check-rassegna-coperta.py --novita /tmp/novita.json --commento /tmp/commento.md
  python3 scripts/check-rassegna-coperta.py --prova
"""
import argparse
import json
import re
import sys
import unicodedata


def norma(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def titolo_breve(titolo):
    # Le voci di Google News finiscono con « - Testata»: si confronta la parte prima.
    t = re.split(r'\s+-\s+[^-]+$', titolo or '')[0]
    parole = norma(t).split()
    return ' '.join(parole[:8])


def voci_da_coprire(dati):
    out = []
    for v in dati.get('novita', []):
        if v.get('locale') and v.get('rilevanza') in ('diretta', 'indiretta'):
            out.append(v)
    return out


def mancanti(dati, commento):
    testo = norma(commento)
    grezzo = commento or ''
    res = []
    for v in voci_da_coprire(dati):
        link = v.get('link') or ''
        if link and link in grezzo:
            continue
        tb = titolo_breve(v.get('titolo'))
        if tb and tb in testo:
            continue
        res.append(v)
    return res


def prova():
    dati = {'novita': [
        {'locale': True, 'rilevanza': 'diretta', 'titolo': 'Genzano, alberi a rischio dopo il maltempo: stanziati 345mila euro per la messa in sicurezza',
         'link': 'https://www.castellinotizie.it/2026/11/06/genzano-alberi/'},
        {'locale': True, 'rilevanza': 'diretta', 'titolo': 'Genzano, albero caduto su due auto in via Fratelli Rosselli - Castelli Notizie',
         'link': 'https://news.google.com/rss/articles/XYZ'},
        {'locale': False, 'rilevanza': 'diretta', 'titolo': 'Allerta meteo nel Lazio', 'link': 'https://esempio.it/a'},
        {'locale': True, 'rilevanza': None, 'titolo': 'Genzano, mozione sul plesso', 'link': 'https://esempio.it/b'},
    ]}
    commento_vuoto = 'Nessuna notizia nuova.'
    if len(mancanti(dati, commento_vuoto)) != 2:
        raise SystemExit('Prova fallita: il commento vuoto doveva lasciare scoperte 2 voci')
    commento = ('- https://www.castellinotizie.it/2026/11/06/genzano-alberi/ — in attesa della delibera all\'albo\n'
                '- «Genzano, albero caduto su due auto in via Fratelli Rosselli»: già raccontato nell\'articolo del 01/11')
    if mancanti(dati, commento):
        raise SystemExit('Prova fallita: il commento completo risultava incompleto')
    print('OK: 2 prove del controllo di copertura della rassegna.')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--novita')
    ap.add_argument('--commento')
    ap.add_argument('--prova', action='store_true')
    a = ap.parse_args()
    if a.prova:
        prova()
        return 0
    if not a.novita or not a.commento:
        ap.error('servono --novita e --commento')
    with open(a.novita, encoding='utf-8') as fh:
        dati = json.load(fh)
    with open(a.commento, encoding='utf-8') as fh:
        commento = fh.read()
    voci = voci_da_coprire(dati)
    scoperte = mancanti(dati, commento)
    if scoperte:
        print(f'❌ {len(scoperte)} voci del territorio su {len(voci)} non sono nominate nel commento. '
              'Aprile, leggile e scrivi per ciascuna articolo, aggiornamento, attesa o motivo dello scarto:')
        for v in scoperte:
            print(f"- [{v.get('fonte')}] {v.get('titolo')}\n  {v.get('link')}")
        return 1
    print(f'OK: tutte le {len(voci)} voci del territorio sono nominate nel commento.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
