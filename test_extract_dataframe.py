import json 
import unittest
import pandas as pd
from extract_dataframe import TweetDfExtractor
from extract_dataframe import read_json

_, tweet_list = read_json('/home/codeally/project/Twitter-Data-Analysis/data/Economic_Twitter_Data.json')

columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'screen_name', 'followers_count','friends_count','sensitivity', 'hashtags', 'user_mentions', 'place']

class TestExtractor(unittest.TestCase):
    
    # @classmethod
    # def setUp(cls):
        
    # def setUp(self) ->pd.DataFrame:
    #     self.TweetDfExtractor(tweet_list[:10])
    
    def test_status_count(self):
        stat_count = [204051, 3462, 6727, 45477, 277957]
        self.assertEqual(TweetDfExtractor(tweet_list['statuses_count'][:5]), stat_count)
    
    # def test_full_text(self):
    #     text = []
    #     self.assertEqual(self.df.find_full_text(), text)
    
    # def test_sentiments(self):
    #     self.assertEqual(self.df.find_sentiments(self.df.find_full_text()), )

    # def test_created_time(self):
    #     created_time = []
    #     self.assertEqual(self.df.find_created_time(), created_time)

    # def test_source(self):
    #     self.assertEqual(self.df.find_source(), )

    # def test_screen_name(self):
    #     self.assertEqual(self.df.find_screen_name(), )

    # def test_follower_count(self):
    #     self.assertEqual(self.df.find_followers_count(), )

    # def test_is_sentitve(self):
    #     self.assertEqual(self.df.is_sensitive(), )

    # def test_favorite_count(self):
    #     self.assertEqual(self.df.find_favourite_count(), )

    # def test_retweet_count(self):
    #     self.assertEqual(self.df.find_retweet_count(), )

    # def test_hashtags(self):
    #     self.assertEqual(self.df.find_hashtags(), )
        
    # def test_mentions(self):
    #     self.assertEqual(self.df.find_mentions(), )

    # def test_location(self):
    #     self.assertEqual(self.df.find_location(), )

    # def test_lang(self):
    #     self.assertEqual(self.df.find_lang(), )


if __name__ == '__main_':
    unittest.main()

