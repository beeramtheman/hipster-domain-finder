import domains
from configparser import SafeConfigParser
from pymongo import MongoClient
import logging
from datetime import datetime, timedelta

config = SafeConfigParser()
config.read('config.ini')
logger = logging.getLogger(__name__)
db = MongoClient()[config.get('mongodb', 'db_name')]

def update_domain(domain, status):
    logger.debug('Updating %s to %s', domain, status)

    operation = db.domains.update({'domain': domain}, {
        '$set': {'status': status, 'length': len(domain)},
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

def mark_purchased():
    # a simpler way exists, somewhere.
    logger.info('Marking domains as purchased during last week or not')

    db.domains.update({}, {'$set': {'purchased_this_week': False}}, multi=True)
    week_ago = datetime.today() - timedelta(days=7)

    purchased = {
        'history': {
            '$elemMatch': {
                'status': 'inactive',
                'date': {'$gte': week_ago}
            }
        },
        'status': 'active'
    }

    db.domains.update(
        purchased,
        {'$set': {'purchased_this_week': True}},
        multi=True
    )

    logger.info('Finished marking domains as purchased')

def main():
    logging.basicConfig(
        filename='update.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    update_all()
    mark_purchased()

if __name__ == '__main__':
    main()
