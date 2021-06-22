import unittest
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor

_, tweet_list = read_json("./data/covid19.json")

columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']


class TestTweetDfExtractor(unittest.TestCase):
    """
		A class for unit-testing function in the fix_clean_tweets_dataframe.py file

		Args:
        -----
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""

    def setUp(self) -> pd.DataFrame:
        self.df = TweetDfExtractor(tweet_list[:5])
        # tweet_df = self.df.get_tweet_df()         

    def test_find_mentions(self):
        self.assertEqual(self.df.find_mentions(), [[{'screen_name': 'TelGlobalHealth', 'name': 'Telegraph Global Health Security', 'id': 1149218984346230784, 'id_str': '1149218984346230784', 'indices': [3, 19]}, {'screen_name': 'WHOAFRO', 'name': 'WHO African Region', 'id': 544389588, 'id_str': '544389588', 'indices': [102, 110]}], [{'screen_name': 'globalhlthtwit', 'name': 'Anthony Costello', 'id': 83440337, 'id_str': '83440337', 'indices': [3, 18]}], [{'screen_name': 'NHSRDForum', 'name': 'NHS R&D Forum', 'id': 1381499726, 'id_str': '1381499726', 'indices': [3, 14]}, {'screen_name': 'Research2note', 'name': 'Research2note', 'id': 734054113940508672, 'id_str': '734054113940508672', 'indices': [26, 40]}, {'screen_name': 'NHSRDForum', 'name': 'NHS R&D Forum', 'id': 1381499726, 'id_str': '1381499726', 'indices': [124, 135]}], [{'screen_name': 'HighWireTalk', 'name': 'The HighWire', 'id': 851985789072408576, 'id_str': '851985789072408576', 'indices': [3, 16]}], [{'screen_name': 'PeterHotez', 'name': 'Prof Peter Hotez MD PhD', 'id': 593289567, 'id_str': '593289567', 'indices': [3, 14]}]])

if __name__ == '__main__':
	unittest.main()

    