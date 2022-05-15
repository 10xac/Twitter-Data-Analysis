import sys, os
import unittest
import pandas as pd
import pandas.api.types as ptypes

sys.path.append(os.path.abspath(os.path.join('..')))
from clean_tweets_dataframe import Clean_Tweets

cleaned_tweets = pd.read_csv('/home/codeally/project/Twitter-Data-Analysis/processed_tweet_data.csv')


class TestCleanTweet(unittest.TestCase):


    def setUp(self):
        self.df = cleaned_tweets.copy(deep=True)
        self.clean_tweet = Clean_Tweets(self.df)

    def test_drop_unwanted_columns(self):
        df = self.clean_tweet.drop_duplicate(self.df)
        self.assertTrue(not self.df.duplicated().any())

    # def test_convert_to_datetime(self):
    #     df = self.clean_tweet.convert_to_datetime(self.df)
    #     # self.assertTrue(df['Created_at'].dtype == )
    #     self.assertTrue(ptypes.is_datetime64_any_dtype(df['created_at']))

    def test_convert_to_numbers(self):
        df = self.clean_tweet.convert_to_numbers(self.df)
        self.assertTrue(ptypes.is_numeric_dtype(df['polarity']))
        self.assertTrue(ptypes.is_numeric_dtype(df['subjectivity']))
        self.assertTrue(ptypes.is_numeric_dtype(df['retweet_count']))
        self.assertTrue(ptypes.is_numeric_dtype(df['favorite_count']))
    
    def test_remove_non_english_tweet(self):
        df = self.clean_tweet.remove_non_english_tweets(self.df)
        self.assertTrue(len(df.columns) == 15)