# Convert the TLD's Gandi supports into valid JSON of only the TLD's HDF uses
# This script can be modified for other registrars

import requests
from bs4 import BeautifulSoup
import json

hdf_tlds = ['ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'as', 'at', 'ax',
            'ba', 'bb', 'be', 'bg', 'bi', 'bj', 'bo', 'bs', 'by', 'bz', 'ca',
            'cc', 'cd', 'cg', 'ch', 'ci', 'cl', 'cm', 'cn', 'co', 'cr', 'cu',
            'cx', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'es',
            'eu', 'fi', 'fm', 'fo', 'fr', 'ga', 'gd', 'gf', 'gg', 'gi', 'gl',
            'gm', 'gp', 'gr', 'gs', 'gt', 'gy', 'hm', 'hn', 'hr', 'ht',
            'hu', 'ie', 'im', 'in', 'io', 'iq', 'is', 'it', 'je', 'jm', 'jo',
            'jp', 'kg', 'ki', 'kn', 'kr', 'ky', 'kz', 'la', 'lc', 'li', 'lk',
            'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg', 'ml',
            'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mu', 'mw', 'mx', 'my', 'na',
            'nc', 'nf', 'ni', 'nl', 'no', 'nr', 'nu', 'pa', 'pe', 'ph', 'pk',
            'pl', 'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 'qa', 're', 'ro', 'rs',
            'ru', 'rw', 'sa', 'sc', 'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm',
            'sn', 'so', 'sr', 'st', 'sv', 'sx', 'sy', 'tc', 'tf', 'tj', 'tk',
            'tl', 'tm', 'tn', 'to', 'tt', 'tv', 'tw', 'ug', 'us', 'uy', 'uz',
            'vc', 'vi', 'vn', 'vu', 'wf', 'ws', 'yt']
for i, tld in enumerate(hdf_tlds):
    hdf_tlds[i] = '.' + tld

registrar_tlds = []
r = requests.get('http://www.gandi.net/domain/price/info')
dom = BeautifulSoup(r.text)
for tbody in dom.find_all('tbody'):
    for th in tbody.find_all('th'):
        tld = th.text.replace(' ', '')
        if tld in hdf_tlds:
            registrar_tlds.append(tld)

print(json.dumps(registrar_tlds))
