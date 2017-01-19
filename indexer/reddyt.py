import praw
import json
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

class Item:
    def __init__(self, fields):
        self._id = fields['id']
        self._created = fields['created']
        self._update_fields = {}
        self._text_type = ''
        self._text_content = ''
    def get_id(self):
        return self._id
    def get_created(self):
        return self._created
    def get_type(self):
        return self._text_type
    def get_content(self):
        return self._text_content
    def get_update_fields(self):
        return self._update_fields
    def __str__(self):
        return '<id={0}, created={1}, type={2}, update_fields={3}, content={4}>'.format(
                self._id, self._created, self._text_type,
                self._update_fields, self._text_content)
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    def __eq__(self, other):
        if type(self) == type(other):
            return self.__dict__ == other.__dict__

class Submission(Item):
    def __init__(self, fields):
        Item.__init__(self, fields)
        self._text_content = fields['title']
        self._text_type = 'title'
        self._update_fields = { 'content' : fields['title'] }
    
class Comment(Item):
    def __init__(self, fields):
        Item.__init__(self, fields)
        self._text_content = fields['body']
        self._text_type = 'body'
        self._update_fields = { 'content' : fields['body'] }

class Reddyt:
    def __init__(self, client):
        self.__reddyt = client

    @classmethod
    def withClientConfig(self, client_id, client_secret, user_agent):
        self.__reddyt = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent)

    def fetch(self, subreddit, items):
        submissions = []
        comments = []
        for submission in self.__reddyt.subreddit(subreddit).new(limit=items):
            item = {
                    'id'        : submission.id,
                    'title'     : submission.title,
                    'created'   : submission.created_utc
                    }
            s = Submission(item)
            logging.debug("Fetched %s", s)
            submissions.append(s)
            
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                item = {
                        'id'        : comment.id,
                        'body'      : comment.body,
                        'created'   : comment.created_utc
                        }
                c = Comment(item)
                logging.debug("Fetched %s", c)
                comments.append(c)
            
        logging.info("Fetched for %s: %d submissions, %d comments", subreddit, len(submissions), len(comments))
        return submissions + comments
