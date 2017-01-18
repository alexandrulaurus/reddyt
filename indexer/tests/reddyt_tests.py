from mock import patch
from mock import call
import unittest
import reddyt

class ReddytTest(unittest.TestCase):
    @patch('praw.Reddit')
    def test_fetch(self, mock):
        client_mock = mock.return_value
        subreddit_call = client_mock.subreddit
        list_new_call = subreddit_call.return_value.new
        list_new_call.return_value = [{'id':'as','body':'bbb','created':123432}]
        
        reddyt_client = reddyt.Reddyt(client_mock)
        result = reddyt_client.fetch('topic', 2)
        
        subreddit_call.assert_called_with('topic')
        list_new_call.assert_called_with(limit=2)
        #TODO: assert items created from API
