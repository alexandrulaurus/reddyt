from flask import Flask
from flask import request
from flask import make_response
from pymongo import MongoClient
from datetime import datetime
import json
import os

app = Flask(__name__)
host = os.getenv('MONGO_HOST', 'localhost')
port = os.getenv('MONGO_PORT', '27017')

mongo = MongoClient('mongodb://{}:{}/'.format(host, port))
db = mongo.reddyt_db

@app.route("/")
def main():
    return "This is a flask server running in Docker. Hi!"

@app.route("/items")
def search():
    #TODO: validate parameters
    items = []
    items += db[request.args.get('subreddit')].find( {
        'created'   : { '$gte' : int(request.args.get('from')) },
        'created'   : { '$lt' : int(request.args.get('to')) }
    }, { '_id': 0 })
    app.logger.debug("Found %d items", len(items))
    response = make_response(json.dumps(items), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
