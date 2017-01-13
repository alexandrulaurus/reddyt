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

    for collection in items:
        db_collection = db[collection]
        for item in items[collection]:
            print("Processing item with updatadable {}".format(item.id))
            db_collection.update(
                    { 'id'  : item.id }, 
                    { 
                        '$set'          : item.updatable_fields,
                        '$setOnInsert'  : item.all_fields
                    }, 
                    True)

if __name__ == '__main__':
    main()
