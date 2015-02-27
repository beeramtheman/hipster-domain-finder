# Populate db without using Domainr API.
# For testing purposes only, no availability checking.

import domains
from configparser import SafeConfigParser
from datetime import datetime
from pymongo import MongoClient

config = SafeConfigParser()
config.read('config.ini')
db = MongoClient()[config.get('mongodb', 'db_name')]

def main():
    docs = [{
        'domain': x,
        'status': 'inactive',
        'history': [{'status': 'inactive', 'date': datetime.now()}]
    } for x in domains.hacks()[:100]]

    db.domains.insert(docs)

if __name__ == '__main__':
    main()
