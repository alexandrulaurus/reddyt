from mock import patch, call, MagicMock
from bson.json_util import dumps
import unittest
import reddyt_server

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.app = reddyt_server.app.test_client()

    def test_search_missing_required_params(self):
        result = self.app.get('/items?subreddit=testsub')
        assert result.status_code == 400
        assert result.data == dumps({'error':'missing request params'})
        assert result.headers['Content-Type'] == 'application/json'

    #TODO: refactor server so we can mock the MongoClient. This is not working
    @patch('pymongo.MongoClient')
    def test_serach_interval_queries_db(self, mock):
        result = self.app.get('/items?subreddit=testsub&from=12312312&to=14942322')
        assert result.status_code == 200
