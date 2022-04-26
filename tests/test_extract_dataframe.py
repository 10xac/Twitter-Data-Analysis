import unittest
import pandas as pd
from extract_dataframe import ExtractTweets





class TestExtractTweeets(unittest.TestCase):
    """
    - A class that tests the Extracts Tweet functions
	"""


    def setUp(self) -> pd.DataFrame:
        """
        - this function tests the setup for the environment
        """
        self.tweets = ExtractTweets("/home/martin/Documents/Dscience/Economic_Twitter_Data.json")
        self.df = self.tweets.get_tweet_df(save=False)

    def test_find_statuses_count(self):
        """
        -this function tests the status count function
        """
        status_counts = self.tweets.find_statuses_count()
        for status_count in status_counts:
            self.assertIsInstance(status_count,(int))

    def test_find_full_text(self):
        """
        - test the text results
        """
        for text in self.tweets.find_full_text():
            self.assertIsInstance(text, (str))

    def test_find_sentiments(self):
        """
        - testing finding the sentiments
        """
        polarity,subjectivity = self.tweets.find_sentiments(self.tweets.find_full_text())
        for i,_ in enumerate(polarity):
            self.assertIsInstance(polarity[i], (int,float))
            self.assertIsInstance(subjectivity[i], (int,float))

    def test_find_created_time(self):
        """
        - testing finding created time 
        """
        string_dates = self.tweets.find_created_time()
        for date in string_dates:
            self.assertIsInstance(date, (str))

    def test_find_source(self):
        """
        - tests the find sources function
        """
        sources = self.tweets.find_source()
        for source in sources:
            self.assertEqual("href" in source,True)
    
    def test_find_screen_name(self):
        """
        - tests the find screen names
        """
        screen_names = self.tweets.find_screen_name()
        for name in screen_names:
            self.assertIsInstance(name,(str))
    

    def test_find_followers_count(self):
        """
        - tests the find follower counts function
        """
        followers_count = self.tweets.find_followers_count()
        for follower in followers_count:
            self.assertIsInstance(follower,(int))
    
    def test_find_friends_count(self):
        """
        - tests the find friends counts function
        """
        friends_count = self.tweets.find_friends_count()
        for friend in friends_count:
            self.assertIsInstance(friend,(int))
        
    def test_find_is_sensitive(self):
        """
        - tests the finding is sensitive function
        """
        is_sensitive = self.tweets.is_sensitive()
        for is_sensitive_response in is_sensitive:
            if is_sensitive_response:
                self.assertIsInstance(is_sensitive_response,(bool,))
            
        
    def test_find_favourite_count(self):
        """
        - tests the finding favorite count function
        """
        favorites = self.tweets.find_favourite_count()
        for favorite in favorites:
            self.assertIsInstance(favorite,(int,))
    
    def test_find_retweet_count(self):
        """
        - tests the find retweet function
        """
        retweets = self.tweets.find_retweet_count()
        for retweet in retweets:
            self.assertIsInstance(retweet,(int))

    def test_find_location(self):
        """
        - tests the find location function
        """
        locations = self.tweets.find_location()
        for location in locations:
            if location:
                self.assertIsInstance(location,(str,))


if __name__ == '__main__':
	unittest.main()

    