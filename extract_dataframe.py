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
    def find_statuses_count(self):
         self.assertEqual(self.df.find_statuses_count())
        
    def find_full_text(self):
        self.assertEqual(self.df.find_full_text(), "name of the text(object)")
       
    
    def find_sentiments(self, text):
        
        self_1=self.assertEqual(self.df.find_sentiments(self.df.find_full_text()),text)
        
        
        return self_1

    def find_created_time(self):
        created=self.assertEqual(self.df.find_created_time())
        return created

    def find_source(self):
        
        source = ['']
        self.assertEqual(self.df.find_source(), source)
        return source





    def find_screen_name(self):
        screen_name1 = ["put all name"]
        self.assertEqual(self.df.find_screen_name(), screen_name1)
        
        
        
        

    def find_followers_count(self):
        self.assertEqual(self.df.find_followers_count())
        
        
        
        

    def find_friends_count(self):
        friends_count = self.assertEqual(self.df.find_friends_count())
        return friends_count 




    self=list
    def is_sensitive(self):
       s01= self.assertEqual(self.df.sensitive())
       return s01
   
    
   
    

    def find_favourite_count(self)->list:
        self.assertEqual(self.df.find_favourite_count())
    
    def find_retweet_count(self)->list:
         self.assertEqual(self.df.find_retweet_count())

    def find_hashtags(self)->list:
        hashtags =self.assertEqual(self.df.find_hashtags())
        return hashtags
    
    
    
    
   # def find_mentions(self)->list:
        
        


    def find_location(self):
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    
        
        
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

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("../covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above
