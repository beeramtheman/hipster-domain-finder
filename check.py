#!/usr/bin/python
# command -> ./check.py <gandi API key>
# note: requires gandi corporate account for access to all TLD's in API

import argparse
import sys
import os
from pymongo import MongoClient
from time import sleep
import xmlrpclib
import subprocess
from pprint import pprint

def find_domains():
    domains = []
    vowels = ('a', 'e', 'i', 'o', 'u', 'y')
    tlds = ('ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'as', 'at', 'ax',
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
            'vc', 'vi', 'vn', 'vu', 'wf', 'ws', 'yt')

    fn = os.path.join(os.path.dirname(__file__), 'words.txt')
    with open(fn) as dictionary:
        for i, line in enumerate(dictionary, 1):
            if i % 100 == 0:
                sys.stdout.write('\r' + str(i).ljust(6) + ' / 50000')
                sys.stdout.flush()
            word = line.strip('\n').lower()
            chars = list(word)

            if word.endswith(tlds):
                end = next((suf for suf in tlds if word.endswith(suf)), None)
                if len(word[:-len(end)]) >= 3:
                    chars.insert(-len(end), '.')
                    if ''.join(chars) not in domains:
                        domains.append(''.join(chars))

            elif word.endswith('er') and len(word) > 3 and chars[-3] not in vowels:
                chars.pop(-2)
                chars.append('.com')
                if ''.join(chars) not in domains:
                    domains.append(''.join(chars))

    print('\nFound ' + str(len(domains)) + ' domains')
    return domains

def get_status(domains):
    new_domains = []
    results = {}
    pending = 0
    print(str(len(domains) / 500) + ' bunches...')

    for i in xrange(0, len(domains), 500):
        sys.stdout.write('\rGetting status of batch #' + str((i + 500) / 500))
        sys.stdout.flush()
        batch = gandi.domain.available(key, domains[i:i+500])
        sleep(2)
        batch = gandi.domain.available(key, domains[i:i+500])

        for name in batch:
            if batch[name] == 'pending':
                pending = pending + 1
            else:
                results[name] = batch[name]
                new_domains.append(name)

        sleep(0.067) # probably not even needed... gandi rate limit
    
    print('\nFinished. Total lost to pending: ' + str(pending))
    return (new_domains, results)

def update(domains):
    holding = []
    domains, statuses = get_status(domains)

    def move_to_holding(end):
        before = len(holding)
        for name in list(domains):
            if name.endswith(end):
                holding.append(name)
                domains.remove(name)
        print('"Held" ' + str(len(domains) - before + 1) + ' domains')

    while len(domains):
        name = domains[0]
        print(name)
        print(len(domains))

        if statuses[name] == 'available':
            print('Adding -> ' + name)
            db.domains.update({'name': name}, {
                'name': name,
                'tld': name.split('.')[1],
                'length': len(name)
            }, True)
            domains.remove(name)

        elif statuses[name] == 'error_unknown' or statuses[name] == 'error_timeout':
            print('Holding -> ' + name + ' and others alike')
            move_to_holding(name.split('.')[1])

        else:
            print('Removing -> ' + name + ' (' + statuses[name] + ')')
            db.domains.remove({'name': name})
            domains.remove(name)

    if len(holding):
        print('Holding: ' + str(len(holding)))
        print(holding)
        print('Sleeping..... ZZzzz')
        sleep(60 * 30)
        print('Going again!')
        check(holding)

parser = argparse.ArgumentParser()
parser.add_argument('--key', required=True)
key = parser.parse_args().key

db = MongoClient('localhost', 27017).hipsterdomainfinder
gandi = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
gandi.version.info(key)

domains = find_domains()
domains.sort(key=len) # check shorter names first (more important)
update(domains)
