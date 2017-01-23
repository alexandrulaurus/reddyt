from flask import Flask, request, make_response
from bson.json_util import dumps
import pymongo
import os

app = Flask(__name__)

host = os.getenv('MONGO_HOST', 'localhost')
port = os.getenv('MONGO_PORT', '27017')

mongo = pymongo.MongoClient('mongodb://{}:{}/'.format(host, port))
db = mongo.reddyt_db

@app.route("/")
def main():
    return "This is a flask server running in Docker. Hi!"

@app.route("/items")
def search():
    try:
        search_options = {}
        if request.args.get('keyword') is not None:
            app.logger.debug("Keyword %s was specified. Will perform text search", 
                    request.args.get('keyword'))
            search_options = { '$text' : { '$search' : request.args.get('keyword') } } 
        
        search_options['created'] = {}
        search_options['created'] = {
            '$gte' : int(request.args.get('from')),
            '$lt' : int(request.args.get('to'))
        }

        """
        Maybe I can validate subrreddit name although an inexistent
        collection will return 0 results which is actually as expected
        """
        items = []
        items += db[request.args.get('subreddit')].find(
            search_options, 
            { '_id': 0 }
        )
        #TODO: need to mock the test with the sort call otherwise
        #TODO: keyword searches are not sorted
        #TODO: .sort([('created', pymongo.DESCENDING)])
        """
        'created' gets printed with .0 from json.dumps(). It's also in the same
        way in the request. However, it's stored correctly as an int in mongo
        I'm going to make an explicit cast to int()
        """
        formatted_items = [{'id':x['id'],x['type']:x['content'],'created':int(x['created'])} for x in items]

        app.logger.debug("Found %d items", len(formatted_items))
        response = make_response(dumps(formatted_items, indent=4, sort_keys=True), 200)
    except ValueError:
        app.logger.error("Invalid parameters")
        response = make_response(dumps({'error':'invalid request params'}), 400)
    except TypeError:
        app.logger.error("Missing parameters")
        response = make_response(dumps({'error':'missing request params'}), 400)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
