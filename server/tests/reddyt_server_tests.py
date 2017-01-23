from mock import patch, call, MagicMock
from bson.json_util import dumps
import unittest
import reddyt_server
import pymongo

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.app = reddyt_server.app.test_client()
        self.db = reddyt_server.db = MagicMock()

    def test_search_missing_required_params(self):
        result = self.app.get('/items?subreddit=testsub')
        assert result.status_code == 400
        assert result.data == dumps({'error':'missing request params'})
        assert result.headers['Content-Type'] == 'application/json'
    
    def test_serach_interval(self):
        find_call = self.db['testsub'].find
        
        result = self.app.get('/items?subreddit=testsub&from=1483309088&to=1484526822')
        
        assert result.status_code == 200
        assert result.headers['Content-Type'] == 'application/json'
        find_call.assert_called_with({
            'created': {'$gte': 1483309088, '$lt': 1484526822}}, {'_id': 0})

    def test_serach_interval_with_keyword(self):
        find_call = self.db['testsub'].find
        
        result = self.app.get('/items?subreddit=testsub&from=1483309088&to=1484526822&keyword=word')
        
        assert result.status_code == 200
        assert result.headers['Content-Type'] == 'application/json'
        find_call.assert_called_with({
            '$text': {'$search': 'word'}, 
            'created': {'$gte': 1483309088, '$lt': 1484526822}}, {'_id': 0})

    def test_search_returns_json(self):
        find_call = self.db['testsub'].find
        db_items = [
                {'id':'id2', 'content':'body1', 'type':'body', 'created':1483309099},
                {'id':'id1', 'content':'title1', 'type':'title', 'created':1483309089}
                ]
        find_call.return_value = db_items
        expected_result = [
                {'id':'id2', 'body':'body1', 'created':1483309099},
                {'id':'id1', 'title':'title1', 'created':1483309089}
                ]

        result = self.app.get('/items?subreddit=testsub&from=1483309088&to=1484526822')

        assert result.status_code == 200
        assert result.headers['Content-Type'] == 'application/json'
        assert result.data == dumps(expected_result, indent=4, sort_keys=True)
        find_call.assert_called_with({
            'created': {'$gte': 1483309088, '$lt': 1484526822}}, {'_id': 0})

