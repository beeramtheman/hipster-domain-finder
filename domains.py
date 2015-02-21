from configparser import SafeConfigParser
import requests
import json
import re
from time import sleep
import logging

config = SafeConfigParser()
config.read('config.ini')
logger = logging.getLogger(__name__)

class NetworkError(RuntimeError):
    def __init__(self, arg):
        self.arg = arg

def _endswithwhat(string, ends):
    for e in ends:
        if string.endswith(e):
            return e

    return False

def hacks():
    logger.info('Calculating domain hacks')
    words = [l.strip('\n') for l in open('words.txt').readlines()]
    tlds = tuple(json.loads(config.get('tld', 'all')))

    can_hack = [w for w in words if w.endswith(tlds)]
    tld_len = [len(_endswithwhat(e, tlds)) for e in can_hack]
    domains = [ can_hack[i][:-tld_len[i]] + '.' + can_hack[i][-tld_len[i]:]
                for i in range(len(can_hack)) ]
    valid = [d for d in domains if re.match(r'.{2,}\..+', d)]

    logger.info('Calculated %s domain hacks', len(valid))
    return valid

def bundle_domains(domains):
    max_domains = int(config.get('domainr', 'max_domains'))
    return [ domains[i:i+max_domains] for i in
             range(0, len(domains), max_domains) ]

def status(domains):
    logger.info('Requesting Domainr "status" of %s domains', len(domains))
    base = "https://api.domainr.com/v2/"

    payload = {
        'client_id': config.get('domainr', 'client_id'),
        'domain': ','.join(domains)
    }

    bad_codes = 0

    while True:
        r = requests.get(base + 'status', params=payload)

        # temporarily allow 504 while Domainr fixes issues
        if r.status_code == 504:
            logger.warn('Domainr "status" returned 504')
            sleep(30)

        elif r.status_code != 200:
            logger.warn('Domainr "status" returned %s', r.status_code)
            bad_codes += 1

            if bad_codes == 3:
                logger.error('Domainr "status" returned %s', r.status_code)
                raise NetworkError(
                    'Domainr "status" returned ' + str(r.status_code)
                )

            sleep(30)

        else:
            logger.info('Domainr "status" returned 200')
            return r.json()['status']
