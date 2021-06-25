import json
import pandas as pd
from textblob import TextBlob

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
        df.to_csv(r'processed.csv', index=False)

        '''if save:
            df.to_csv(r'processedt.csv', index=False)
            print('File Successfully Saved.!!!')'''
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json(r"C:\Users\Jakinda\Twitter-Data-Analysis\data\covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()