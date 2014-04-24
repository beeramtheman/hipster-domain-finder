# namecheap api rules:
# 20 requests per minute, 20 domains per request, 8000 request per day

from pymongo import MongoClient
import requests

db = MongoClient('localhost', 27017).hipsterdomainfinder

# .ch doesn't have whois server, emailed robowhois about it
# namecheap does not support .ly :(
ext = ('us', 'me', 'co', 'io' , 'ca', 'pw', 'tv', 'in', 'de', 'cc', 'eu', 'cm',
       'li', 'es', 'pe', 'nu', 'bz', 'fr')

# extensions where min length is 3
stupid = ('in', 'us', 'pw', 'in', 'li', 'es', 'fr')

with open('popular_words.txt') as dictionary:
    for line in dictionary:
        word = line.strip('\n')

        if word.endswith(ext):
            if word[-2:] in stupid and len(word[:-2]) >= 3:
                short = False
            elif word[-2:] not in stupid and len(word[:-2]) >= 2:
                short = False
            else:
                short = True

            if not short:
                if True: # TODO: available according to namecheap API
                    chars = list(word)
                    chars.insert(-2, '.')
                    name = ''.join(chars)
                    db.domains.update({'name': name}, {
                        'name': name,
                        'ext': word[-2:],
                        'length': len(name)
                    }, True)
                else:
                    db.domains.remove({'name': name})
