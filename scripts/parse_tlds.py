# Convert the TLD's Gandi supports into valid JSON of only the TLD's HDF uses
# This script can be modified for other registrars

import requests
from bs4 import BeautifulSoup
import json

hdf_tlds = json.load(open('../website/tlds.json'))

for i, tld in enumerate(hdf_tlds):
    hdf_tlds[i] = '.' + tld

registrar_tlds = []
r = requests.get('http://www.gandi.net/domain/price/info')
dom = BeautifulSoup(r.text)
for tbody in dom.find_all('tbody'):
    for th in tbody.find_all('th'):
        tld = th.text.replace(' ', '')
        if tld in hdf_tlds:
            registrar_tlds.append(tld[1:])

print(json.dumps(registrar_tlds))
# NOTE: In this case of Gandi you must also use their API to eliminate
# corporate only TLDs.
