import unittest
import pandas as pd
import sys, os
import numpy as np
from pandas.core.indexing import convert_to_index_sliceable
sys.path.append(os.path.abspath(os.path.join('..')))

from clean_tweets_dataframe import Clean_Tweets

df = pd.read_csv("../clean_processed_tweet_data.csv")
columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']

class Test_Clean_Tweet(unittest.TestCase):


    def setUp(self) -> pd.DataFrame:
            
        self.df = df
        #  tweet_df = self.df.get_tweet_df()         


    # def test_drop_unwanted_column(self):
    #     self.assertEqual(self.df.drop_unwanted_column(df).columns, columns)

    def test_convert_to_datetime(self):
        self.assertEqual(self.df.dtypes['created_at'], "object")
    
    def test_drop_duplicate(self):
        self.assertEqual(self.df.duplicated().sum(),0)
    
    def test_convert_to_numbers(self):
        numeric_df=self.df[['polarity','subjectivity','retweet_count','favorite_count','followers_count','friends_count']]
        self.assertEqual(numeric_df.dtypes.tolist(), ["float64","float64","float64","float64","int64","int64"])

    def test_remove_non_english_tweets(self):
        self.assertEqual(self.df['lang'].values.all(),np.array(["en" for _ in range(len(self.df['lang'].values))],dtype=object).all())

if __name__ == '__main__':
	unittest.main()

    