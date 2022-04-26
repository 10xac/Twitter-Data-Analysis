import unittest
import pandas as pd
from clean_tweets_dataframe import TweetCleanser
import numpy as np

class TestTweetCleanser(unittest.TestCase):
    """
    - this class tests the TweeetCleanser class
    """


    def setUp(self) -> pd.DataFrame:
        """
        - this function is for the simple setting up of the dataframe
        """
        self.df = pd.read_csv("data/processed_tweet_data.csv")
        self.df_cleanser = TweetCleanser(self.df)
        
    def test_drop_unwanted_column(self):
        """
        - this function tests the drop unwanted columns
        """
        self.assertEqual(len(self.df.columns),len(self.df_cleanser.drop_unwanted_column(self.df).columns))
    
    
    def test_drop_duplicate(self):
        """
        - this function tests the drop duplicates function
        """
        self.assertGreater(len(self.df),len(self.df_cleanser.drop_duplicate(self.df)))
    

    
    def test_convert_to_numbers(self):
        """
        - this function tests the convert to numeric function
        """
        self.assertEqual(self.df_cleanser.convert_to_numbers(self.df)['polarity'].dtype,np.int64)


    def test_remove_non_english(self):
        """
        - this function tests whether the non english words have been removed
        """
        cleansed_df = self.df_cleanser.remove_non_english_tweets(self.df)
        self.assertEqual(cleansed_df['lang'].str.contains("de").sum(),0)


if __name__ == '__main__':
	unittest.main()

    