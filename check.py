#!/usr/bin/python
# command -> ./check.py <gandi API key>

import sys
from pymongo import MongoClient
from time import sleep
import xmlrpclib
from pprint import pprint

db = MongoClient('localhost', 27017).hipsterdomainfinder
gandi = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
key = sys.argv[1]
gandi.version.info(key)

vowels = ('a', 'e', 'i', 'o', 'u', 'y')
domains = []
tlds = gandi.domain.tld.list(key)
for i, tld in enumerate(tlds):
    tlds[i] = tld['name']

tlds = tuple(tlds)

with open('popular_words.txt') as dictionary:
    for line in dictionary:
        word = line.strip('\n')
        chars = list(word)

        if len(word) > 3:
            if word.endswith(tlds):
                end = next((suf for suf in tlds if word.endswith(suf)), None)
                if len(word) > len(end):
                    chars.insert(-len(end), '.')
                    domains.append(''.join(chars))
            
            elif word.endswith('er') and chars[-3] not in vowels:
                chars.pop(-2)
                chars.append('.com')
                domains.append(''.join(chars))

statuses = gandi.domain.available(key, domains)
available = []

for name in statuses:
    while statuses[name] == 'pending':
        sleep(10)
        statuses = gandi.domain.available(key, domains)
    if statuses[name] == 'available':
        print('Adding -> ' + name)
        db.domains.update({'name': name}, {
            'name': name,
            'tld': name.split('.')[1],
            'length': len(name.split('.')[0])
        }, True)
    else:
        print('Removing -> ' + name)
        print('    > For reason: ' + statuses[name])
        db.domains.remove({'name': name})

    print('')
