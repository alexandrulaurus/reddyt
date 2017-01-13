import praw
import json

class Item:
    def __init__(self, fields):
        self.id = fields['id']
        self.created = fields['created'];
        self.all_fields = fields;
        self._updatable_fields = {}

    def updatable_fields(self):
        return self._updatable_fields

    def all_fields(self):
        return self.all_fields

class Submission(Item):
    def __init__(self, fields):
        Item.__init__(self, fields)
        self._updatable_fields = { 'title'.encode('UTF-8') : fields['title'].encode('UTF-8') }
    
class Comment(Item):
    def __init__(self, fields):
        Item.__init__(self, fields)
        self._updatable_fields = { 'body'.encode('UTF-8')  : fields['body'].encode('UTF-8') }
    
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
        return { 'submissions' : submissions, 'comments' : comments }
