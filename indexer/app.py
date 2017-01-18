from reddyt import Reddyt
import pymongo
import time
import threading
import logging
import json
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def process(reddyt, db, subreddit, limit):
    logging.info("Processing subreddit %s", subreddit)
    items = reddyt.fetch(subreddit, limit)

    for item in items:
        db_collection = db[subreddit]
        db_collection.update(
                { 'id'  : item.get_id() }, 
                { 
                    '$set'          : item.get_update_fields(),
                    '$setOnInsert'  : {
                                        'id'        : item.get_id(),
                                        'type'      : item.get_type(),
                                        'created'   : item.get_created()
                                      }
                }, 
                True)
    logging.info("Finished processing %s", subreddit)

def db_conn():
    host = os.getenv('MONGO_HOST', 'localhost')
    port = os.getenv('MONGO_PORT', '27017')

    mongo = pymongo.MongoClient('mongodb://{}:{}/'.format(host, port))
    db = mongo.reddyt_db
    return db

def reddyt_client():
    client_secret = os.getenv('CLIENT_SECRET', '')
    client_id = os.getenv('CLIENT_ID', '')
    user_agent = os.getenv('USER_AGENT', '')
    return Reddyt.withClientConfig(client_id, client_secret, user_agen)
    
def main():
    db = db_conn()

    with open('./config.json') as config_file:
        subreddits = json.load(config_file)

    reddyt = reddyt_client()

    logging.info("Start processing subreddits for initial dump")
    workers = {}
    for config in subreddits['subreddits']:
        db[config['name']].create_index([("id", pymongo.DESCENDING)], unique=True)
        db[config['name']].create_index([("content", pymongo.TEXT),
                                        ("created", pymongo.DESCENDING)])
        db[config['name']].create_index([("created", pymongo.DESCENDING)])

        name = "Subreddit-{}".format(config['name'])
        worker = threading.Thread(
                name=name, 
                target=process, 
                args=[reddyt, db, config['name'], config['initial_dump']])
        workers[config['name']] = {}
        workers[config['name']]['worker'] = worker
        workers[config['name']]['initial_dump'] = config['initial_dump']
        workers[config['name']]['refresh_limit'] = config['refresh_limit']
        workers[config['name']]['refresh_interval'] = config['refresh_interval']
        worker.start()
 
    logging.info("Waiting for initial dump to complete and scheduling each subreddit")
    while (True):
        for k, v in workers.iteritems():
            if (v['worker'].isAlive() == False):
                logging.info(
                    "Worker %s finished. Scheduling work in the next %d seconds", 
                    k, 
                    workers[k]['refresh_interval'])
                sched_worker = threading.Timer(
                    workers[k]['refresh_interval'], 
                    process, 
                    [reddyt, db, k, workers[k]['refresh_limit']])
                sched_worker.setName("SubredditScheduledWorker-{}".format(k))
                workers[k]['worker'] = sched_worker
                sched_worker.start()

if __name__ == '__main__':
    main()
