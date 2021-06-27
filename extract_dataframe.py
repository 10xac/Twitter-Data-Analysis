import unittest
import pandas as pd

from textblob import TextBlob
from clean_tweets_dataframe import Clean_Tweets

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list 
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):  
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = [(x.get('user', {})).get('statuses_count', 0) for x in self.tweets_list]
        return statuses_count
        
    def find_full_text(self)->list:
        try:
            text =[text['text']for text in self.tweets_list]
        except KeyError:
            text = ''
        return text
    
    def find_sentiments(self, text)->list:
        polarity = []
        subjectivity = []

        for tx in text:
              if (tx):
                result = TextBlob(str(tx)).sentiment
                polarity.append(result.polarity)
                subjectivity.append(result.subjectivity)
        
        return polarity, subjectivity


    def find_created_time(self)->list:
          return [x.get('created_at', None) for x in self.tweets_list]

    def find_source(self)->list:
          return [x.get('source', None) for x in self.tweets_list]
      
    def find_screen_name(self)->list:
          return [(x.get('user','')).get('screen_name', None) for x in self.tweets_list]

    def find_followers_count(self)->list:
        return [x.get('user', {}).get('followers_count') for x in self.tweets_list]

    def find_friends_count(self)->list:
        return [x.get('user', {}).get('friends_count') for x in self.tweets_list]

    def is_sensitive(self)->list:
        try:
            is_sensitive = [x.get('possibly_sensitive', None) for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self)->list:
        return [x.get('retweeted_status', {}).get('favorite_count',0) for x in self.tweets_list]

    def find_retweet_count(self)->list:
        return  [(x.get('retweeted_status',{})).get('retweet_count', None) for x in self.tweets_list]

    def find_hashtags(self)->list:
        return [x.get('hashtags', None) for x in self.tweets_list]

    def find_mentions(self)->list:
        return [x.get('mentions', None) for x in self.tweets_list]


    def find_location(self)->list:
        try:
            location = [(x.get('user', {})).get('location', None) for x in self.tweets_list]
        except TypeError:
            location = ''
        
        return location

    def find_lang(self) -> list:
        return [x.get('lang', None) for x in self.tweets_list]
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)
        df.to_csv('data/processed.csv', index=False)

        '''if save:
            df.to_csv('data/processed.csv', index=False)
            print('File Successfully Saved.!!!')'''
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    tweet_obj = Clean_Tweets(tweet_df)
    tweet_obj.drop_unwanted_column(tweet_df)
    tweet_obj.drop_duplicate(tweet_df)
    tweet_obj.convert_to_datetime(tweet_df)
    tweet_obj.convert_to_numbers(tweet_df)
    tweet_obj.remove_non_english_tweets(tweet_df)
    
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))

from extract_dataframe import read_json
from extract_dataframe import TweetDfExtractor

_, tweet_list = read_json("data/covid19.json")

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

    def test_find_sentiments(self):
        self.assertEqual(self.df.find_sentiments(self.df.find_full_text()), ([0.0, 0.13333333333333333, 0.3166666666666667, 0.16666666666666666, 0.3], [0.0, 0.45555555555555555, 0.48333333333333334, 0.16666666666666666, 0.7666666666666666]))

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
        self.assertEqual(self.df.find_favourite_count(),  [548, 195, 2, 1580, 72])

    def test_find_retweet_count(self):
        self.assertEqual(self.df.find_retweet_count(), [612, 92, 1, 899, 20])

    # def test_find_hashtags(self):
    #     self.assertEqual(self.df.find_hashtags(), )

    # def test_find_mentions(self):
    #     self.assertEqual(self.df.find_mentions(), )

    def test_find_location(self):
        self.assertEqual(self.df.find_location(), ['Mass', 'Edinburgh, Scotland', None, None, 'United Kingdom'])

if __name__ == '__main__':
	unittest.main()

