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

available = []
hold = [] # domains to check later due to rate limit

def move_to_hold(end):
    global domains
    global hold

    before = len(domains)
    for name in list(domains):
        if name.endswith(end):
            hold.append(name)
            domains.remove(name)
    print('Removed ' + str(before - len(domains)) + ' domains')

def check():
    global domains
    global hold
    
    statuses = gandi.domain.available(key, domains)

    types = [] # types of gandi responses

    while len(domains):
        name = domains[0]

        if statuses[name] not in types:
            types.append(statuses[name])

        while statuses[name] == 'pending':
            print('...pending...')
            sleep(10)
            statuses = gandi.domain.available(key, domains)

        if statuses[name] == 'available':
            print('Adding -> ' + name)
            db.domains.update({'name': name}, {
                'name': name,
                'tld': name.split('.')[1],
                'length': len(name)
            }, True)
            domains.remove(name)

        elif statuses[name] == 'error_unknown':
            print('Moving -> ' + name + ' and others alike')
            move_to_hold(name.split('.')[1])

        else:
            print('Removing -> ' + name)
            print('    > For reason: ' + statuses[name])
            db.domains.remove({'name': name})
            domains.remove(name)

        print('')

    print('types:')
    pprint(types)

    print('domains: ' + str(len(domains)))
    print('hold: ' + str(len(hold)))

    if len(hold):
        print('Sleeping..... ZZzzz')
        sleep(60 * 60)
        print('Going again!')
        domains = list(hold)
        hold = []
        check()

check()
