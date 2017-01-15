from pymongo import MongoClient
import praw
import json

from reddyt import Reddyt

def main():
    #TODO: expose env variables for URL
    mongo = MongoClient('mongodb://mongo:27017/')
    db = mongo.reddyt_db

    #TODO: parse subreddits from file.
    #TODO: make a polling schedule

    """
    Specifying limit param should fetch aa 'much as it can'.
    While testing I found that in only fetches the defaulit limit (100)
    Most of reddit's listings contains a max of 1000 so I'll go with that
    https://github.com/praw-dev/praw/blob/6deea4b331f98259223376d4a1f4da319e0dd420/praw/models/listing/generator.py#L23
    """
    reddyt = Reddyt()
    items = reddyt.fetch(subreddit = 'analog', items = 10)

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

if __name__ == '__main__':
    main()
