import unittest
import pandas as pd

from ..extract_dataframe import read_json
from ..extract_dataframe import TweetDfExtractor

_, tweet_list = read_json("Economic_Twitter_Data.json")

columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']

class TestTweetDfExtractor(unittest.TestCase):

    def setUp(self) -> pd.DataFrame:
        self.df = TweetDfExtractor(tweet_list, columns)

    def test_find_statuses_count(self):
        self.assertEqual(self.df.find_statuses_count(),)

    def test_find_full_text(self):
        self.assertEqual(self.df.find_full_text(), )

    def test_find_sentiments(self):
        self.assertEqual(self.df.find_sentiments(), )

    def test_find_created_time(self):
        self.assertEqual(self.df.find_created_time(), )

    def test_find_source(self):
        self.assertEqual(self.df.find_source(), )

    def test_find_screen_name(self):
        self.assertEqual(self.df.find_screen_name(), )

    def test_find_followers_count(self):
        self.assertEqual(self.df.find_followers_count(), )

    def test_find_friends_count(self):
        self.assertEqual(self.df.find_friends_count(), )

    def test_find_is_sensitive(self):
        self.assertEqual(self.df.is_sensitive(), )

    def test_find_favourite_count(self):
        self.assertEqual(self.df.find_favourite_count(), )

    def test_find_retweet_count(self):
        self.assertEqual(self.df.find_retweet_count(), )

    def test_find_hashtags(self):
        self.assertEqual(self.df.find_hashtags(), )

    def test_find_mentions(self):
        self.assertEqual(self.df.find_mentions(), )

    def test_find_place(self):
        self.assertEqual(self.df.find_place(), )

    def test_find_location(self):
        self.assertEqual(self.df.find_location(), )
