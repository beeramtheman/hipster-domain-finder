import domains
from configparser import SafeConfigParser
from pymongo import MongoClient
import logging
from datetime import datetime

config = SafeConfigParser()
config.read('config.ini')
logger = logging.getLogger(__name__)
db = MongoClient()[config.get('mongodb', 'db_name')]

def update_domain(domain, status):
    logger.debug('Updating %s to %s', domain, status)

    operation = db.domains.update({'domain': domain}, {
        '$set': {'status': status},
        '$push': {'history': {'status': status, 'date': datetime.now()}}
    }, upsert=True)

    if operation['err']:
        logger.error('Update error: %s' + operation['error'])

    else:
        logger.debug('Update success')

def update_all():
    logger.info('Updating all domains')

    for bundle in domains.bundle_domains(domains.hacks()):
        try:
            statuses = domains.status(bundle)

        except domains.NetworkError as e:
            logger.fatal(e)
            break

        for status in domains.status(bundle):
            logger.debug('Updating %s to %s', status['domain'], status['summary'])
            update_domain(status['domain'], status['summary'])

    logger.info('Finished updating all domains')

def main():
    logging.basicConfig(
        filename='update.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    update_all()

if __name__ == '__main__':
    main()
