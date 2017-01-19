from mock import patch
from mock import call
from mock import MagicMock
import unittest
import reddyt

def mock_submission(fields):
    item = MagicMock(id=fields['id'],
            created_utc=fields['created_utc'],
            title=fields['title'])
    return item

def mock_comment(fields):
    item = MagicMock(id=fields['id'],
            created_utc=fields['created_utc'],
            body=fields['body'])
    return item

class ReddytTest(unittest.TestCase):
    def setUp(self):
        self.expected_items = [
                reddyt.Submission({
                    'id':'id1','title':'title1','created':123432
                    }),
                reddyt.Submission({
                    'id':'id2','title':'title2','created':123433
                    }),
                reddyt.Comment({
                    'id':'id3','body':'body1','created':123435
                    })
                ]

    @patch('praw.Reddit')
    def test_fetch(self, mock):
        client_mock = mock.return_value
        subreddit_call = client_mock.subreddit
        list_new_call = subreddit_call.return_value.new
        s1 = mock_submission({'id':'id1','title':'title1','created_utc':123432})
        s2 = mock_submission({'id':'id2','title':'title2','created_utc':123433})
        list_new_call.return_value = [s1, s2]
        comments_call = s1.comments
        replace_comments_call = comments_call.replace_more
        list_comments_call = comments_call.list
        list_comments_call.return_value = [mock_comment({
            'id':'id3','body':'body1','created_utc':123435
            })]
        
        reddyt_client = reddyt.Reddyt(client_mock)
        results = reddyt_client.fetch('topic', 2)
        
        subreddit_call.assert_called_with('topic')
        list_new_call.assert_called_with(limit=2)
        replace_comments_call.assert_called_with(limit=0)
        list_comments_call.assert_called_with()
        for r in results:
            print(r)
        for e in self.expected_items:
            print(e)
        #TODO: assert fails with the Comment instance in the list
        self.assertItemsEqual(results, self.expected_items)
