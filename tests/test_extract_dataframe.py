import unittest
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor

_, tweet_list = read_json("./data/covid19.json")
# path issues resolved 
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


    def test_find_statuses_count(self):
        self.assertEqual(self.df.find_statuses_count(), [204051, 3462, 6727, 45477, 277957])

#     def test_find_full_text(self):
#         text = ['RT @TelGlobalHealth: "Africa is in the midst of a full-blown third wave," @MoetiTshidi said. "The sobering trajectory of surging cases shou…',
#  'RT @Senators: Expect to see some different kind of shots at @CdnTireCtr next week!\n\xa0\nDo your part and get your #Covid19 vaccine.\n\nDETAILS:…',
#  'RT @stkirsch: **BIG NEWS**: Up to 25,800 may have been killed by the COVID vaccine.  I bet that this is a lower bound on the number killed…',
#  'Alpha, Beta &amp; Delta: We break down everything you need to know about the three #COVID19 variants that have been det… https://t.co/IN5AiroJ0U',
#  'Despite #COVID19 lockdowns and travel restrictions, still nearly 3 million people fled their homes from war, violen… https://t.co/DA1QZ7Ff06']

     #   self.assertEqual(self.df.find_full_text(), text)

    def test_find_sentiments(self):
        self.assertEqual(self.df.find_sentiments(self.df.find_full_text()), ([0.0,0.13333333333333333,0.3166666666666667,0.16666666666666666,0.3,], [0.0,0.45555555555555555,0.48333333333333334,0.16666666666666666,0.7666666666666666,]))
    def test_find_created_time(self):
        created_at = ['Fri Jun 18 17:55:49 +0000 2021', 'Fri Jun 18 17:55:59 +0000 2021', 'Fri Jun 18 17:56:07 +0000 2021',
         'Fri Jun 18 17:56:10 +0000 2021', 'Fri Jun 18 17:56:20 +0000 2021']

        self.assertEqual(self.df.find_created_time(), created_at)

    def test_find_source(self):
        source = ['<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>', 
        '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>',
         '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>']

        self.assertEqual(self.df.find_source(), source)

    def test_find_screen_name(self):
        name = ['ketuesriche', 'Grid1949', 'LeeTomlinson8', 'RIPNY08', 'pash22']
        self.assertEqual(self.df.find_screen_name(), name)

    def test_find_followers_count(self):
        f_count = [551, 66, 1195, 2666, 28250]
        self.assertEqual(self.df.find_followers_count(), f_count)

    def test_find_friends_count(self):
        friends_count = [351, 92, 1176, 2704, 30819]
        self.assertEqual(self.df.find_friends_count(), friends_count)

    def test_find_is_sensitive(self):
        self.assertEqual(self.df.is_sensitive(), [None, None, None, None, None])

    def test_find_favourite_count(self):
        self.assertEqual(self.df.find_favourite_count(), [8861, 48835, 9549, 42559, 10564])

    def test_find_retweet_count(self):
        self.assertEqual(self.df.find_retweet_count(), [0, 0, 0, 0, 0])

    def test_find_hashtags(self):
         self.assertEqual(self.df.find_hashtags(), [ [], [],[{'indices': [103, 116], 'text': 'red4research'}],[], []])

    def test_find_mentions(self):
         self.assertEqual(self.df.find_mentions(), '')

    def test_find_location(self):
        self.assertEqual(self.df.find_location(), '')

if __name__ == '__main__':
	unittest.main()
