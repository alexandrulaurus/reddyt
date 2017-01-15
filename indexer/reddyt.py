import praw
import json
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

class Item:
    def __init__(self, fields):
        self.id = fields['id']
        self.created = fields['created']
        self.updatable_fields = {}

class Submission(Item):
    def __init__(self, fields):
        Item.__init__(self, fields)
        self.updatable_fields = { 'title' : fields['title'] }
    
class Comment(Item):
    def __init__(self, fields):
        Item.__init__(self, fields)
        self.updatable_fields = { 'body' : fields['body'] }
    
class Reddyt:

    def __init__(self):
        client_secret = os.getenv('CLIENT_SECRET', '')
        client_id = os.getenv('CLIENT_ID', '')
        user_agent = os.getenv('USER_AGENT', '')
        self._reddyt = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent)

    def fetch(self, subreddit, items):
        submissions = []
        comments = []
        for submission in self._reddyt.subreddit(subreddit).new(limit=items):
            item = {
                    'id'        : submission.id,
                    'title'     : submission.title,
                    'created'   : submission.created_utc
                    }
            logging.debug("Fetched %s", item['id'])
            submissions.append(Submission(item))
            
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                item = {
                        'id'        : comment.id,
                        'body'      : comment.body,
                        'created'   : comment.created_utc
                        }
                logging.debug("Fetched %s", item['id'])
                comments.append(Comment(item))
            
        logging.info("Fetched for %s: %d submissions, %d comments", subreddit, len(submissions), len(comments))
        return submissions + comments
