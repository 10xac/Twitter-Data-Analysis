import unittest
import pandas as pd
import sys
import numpy as np


sys.path.insert(1, '/Users/alex/Desktop/10_acadamy/Twitter-Data-Analysis')
from clean_tweets_dataframe import df
from clean_tweets_dataframe import CleanTweets
df = pd.read_csv("/Users/alex/Desktop/10_acadamy/Twitter-Data-Analysis/data/covid19.csv")
class Testclen_Tweet(unittest.TestCase):

    def test_drop_dupplicate(self):
        self.assertEqual(df.duplicated().sum(),0)

    def test_convert_to_datetime(self):
        self.assertEqual(df.dtypes['created_at'], "object")
    def test_convert_to_number(self):
         df1=df[['quote_count','retweet_count','favorite_count','reply_count']]
         self.assertEqual(df1.dtypes.tolist(),["int64","int64" ,"int64","int64"])
    def test_remove_non_english_tweets(self):
        self.assertEqual(df['lang'].values.all(),np.array(["en" for _ in range(len(df['lang'].values))],dtype=object).all())



if __name__ == '__main__':
    unittest.main()
