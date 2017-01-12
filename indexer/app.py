import praw
import json
from datetime import datetime
from pymongo import MongoClient

def main():
    #TODO: expose env variables for URL
    mongo = MongoClient('mongodb://mongo:27017/')
    db = mongo.reddyt_db

    reddit = praw.Reddit(client_id='QrKWmDAiiMqmKg',
			client_secret='AzEuxi3VcfUhvynyXRZuChqQMow',
			username='_nothingistrue',
			password='_everythingispermitted',
			user_agent='testscript reddit API')

    #TODO: parse subreddits from file.
    #TODO: make a polling schedule

    """
    Specifying limit param should fetch aa 'much as it can'.
    While testing I found that in only fetches the defaulit limit (100)
    Most of reddit's listings contains a max of 1000 so I'll go with that
    https://github.com/praw-dev/praw/blob/6deea4b331f98259223376d4a1f4da319e0dd420/praw/models/listing/generator.py#L23
    """
    c = 0
    for submission in reddit.subreddit('analog').new(limit=50):
        c += 1
        item = {
                'id'        : submission.id,
                'title'     : submission.title,
                'created'   : submission.created
                }
        print(json.dumps(item))
        db.comments.insert(item)
        
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            item = {
                    'id'        : comment.id,
                    'body'      : comment.body,
                    'created'   : comment.created
                    }
            print(json.dumps(item))
            db.comments.insert(item)

    print('Total new posts {}'.format(c))

if __name__ == '__main__':
    main()
