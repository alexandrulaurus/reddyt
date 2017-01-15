import praw
import json

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
        #TODO: init from env variables
        self._reddyt = praw.Reddit(client_id='QrKWmDAiiMqmKg',
                client_secret='AzEuxi3VcfUhvynyXRZuChqQMow',
                username='_nothingistrue',
                password='_everythingispermitted',
                user_agent='testscript reddit API')

    def fetch(self, subreddit, items):
        submissions = []
        comments = []
        for submission in self._reddyt.subreddit(subreddit).new(limit=items):
            item = {
                    'id'        : submission.id,
                    'title'     : submission.title,
                    'created'   : submission.created
                    }
            print(json.dumps(item))
            submissions.append(Submission(item))
            
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                item = {
                        'id'        : comment.id,
                        'body'      : comment.body,
                        'created'   : comment.created
                        }
                print(json.dumps(item))
                comments.append(Comment(item))
            
        print("Fetched for {}: {} submissions, {} comments".format(subreddit, len(submissions), len(comments)))
        return submissions + comments
