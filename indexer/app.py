from pymongo import MongoClient
from reddyt import Reddyt
import time
import threading
import logging
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def process(reddyt, db, subreddit, limit):
    logging.info("Processing subreddit %s", subreddit)
    items = reddyt.fetch(subreddit, limit)

    for item in items:
        db_collection = db[item.__class__.__name__.lower()]
        db_collection.update(
                { 'id'  : item.id }, 
                { 
                    '$set'          : item.updatable_fields,
                    '$setOnInsert'  : {
                                        'id'        : item.id,
                                        'created'   : item.created
                                      }
                }, 
                True)
        
    logging.info("Finished processing %s", subreddit)
    
def main():
    #TODO: expose env variables for URL
    mongo = MongoClient('mongodb://mongo:27017/')
    db = mongo.reddyt_db

    with open('./config.json') as config_file:
        subreddits = json.load(config_file)

    reddyt = Reddyt()

    logging.info("Start processing subreddits for initial dump")
    workers = {}
    for config in subreddits['subreddits']:
        name = "Subreddit-{}".format(config['name'])
        worker = threading.Thread(
                name=name, 
                target=process, 
                args=[reddyt, db, config['name'], config['initial_dump']])
        workers[config['name']] = {}
        workers[config['name']]['worker'] = worker
        workers[config['name']]['initial_dump'] = config['initial_dump']
        workers[config['name']]['refresh_limit'] = config['refresh_limit']
        workers[config['name']]['refresh_interval'] =config['refresh_interval']
        worker.start()
 
    logging.info("Waiting for initial dump to complete and scheduling each subreddit")
    while (True):
        for k, v in workers.iteritems():
            if (v['worker'].isAlive() == False):
                logging.info(
                    "Worker %s finished. Scheduling work in the next %d seconds", 
                    k, 
                    workers[k]['refresh_interval'])
                #TODO: get schedule and limits from file
                sched_worker = threading.Timer(
                    workers[k]['refresh_interval'], 
                    process, 
                    [reddyt, db, k, workers[k]['refresh_limit']])
                sched_worker.setName("SubredditScheduledWorker-{}".format(k))
                workers[k]['worker'] = sched_worker
                sched_worker.start()

if __name__ == '__main__':
    main()
