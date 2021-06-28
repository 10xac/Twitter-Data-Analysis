import json
import pandas as pd
from textblob import TextBlob
import re
from clean_tweets_dataframe import *

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

    
    def find_statuses_count(self)->list:
        statuses_count = []
        for tweets in self.tweets_list:
            statuses_count.append(tweets['user']['statuses_count'])
        return statuses_count
    
    
    def find_full_text(self)->list:
        texts = []
        for tweets in self.tweets_list:
            if 'retweeted_status' in tweets.keys() and 'extended_tweet' in tweets['retweeted_status'].keys(): 
                texts.append(tweets['retweeted_status']['extended_tweet']['full_text'])
            else:
                texts.append(tweets['text'])     
                
        return texts
    
    def find_clean_text(self, text)->list:
        clean_text = []
        for t in text:
            new_t = re.sub('#', '',t)
            new_t = re.sub('@[a-zA-Z0-9]', '', new_t)
            new_t = re.sub('RT[\s]+', '',new_t)
            new_t = re.sub('https?:\/\/\S+','',new_t)
            clean_text.append(new_t)
            
        return clean_text
    
    def find_sentiments(self, text)->list:
        polarity_l = []
        subjectivity_l = []
        
        for tex in text:
            polarity= (TextBlob(tex).sentiment[0])
            self.subjectivity= (TextBlob(tex).sentiment[1])
            polarity_l.append(polarity)
            subjectivity_l.append(self.subjectivity)
            
        return polarity_l, subjectivity_l
    
    def find_sentiment(self, text)->list:
        sentiment = []
        for tex in text:
            sentiment.append(TextBlob(tex).sentiment)   
        return sentiment
    
    def find_lang(self) ->list:
        lang = []
        for tweets in self.tweets_list:
            lang.append(tweets['lang'])
        return lang
    
    def find_created_time(self)->list:
        created_at = []
        for tweets in self.tweets_list:
            created_at.append(tweets['created_at'])
        return created_at

    def find_source(self)->list:
        source = []
        for tweets in self.tweets_list:
            source.append(tweets['source'])
        return source
    
    def find_screen_name(self)->list:
        screen_name = []
        for tweets in self.tweets_list:
            screen_name.append(tweets['user']['screen_name'])
        return screen_name 
    
    def find_screen_count(self)->list:
        screen_count = []
        for tweets in self.tweets_list:
            screen_count.append(len(tweets['entities']['user_mentions']))
        return screen_count 

    def find_followers_count(self)->list:
        followers_count = []
        for tweets in self.tweets_list:
            followers_count.append(tweets['user']['followers_count'])
        return followers_count 
    
    def find_friends_count(self)->list:
        friends_count = []
        for tweets in self.tweets_list:
            friends_count.append(tweets['user']['friends_count'])
        return friends_count

    def is_sensitive(self)->list:
        is_sensitive = []
        for tweets in self.tweets_list:
            if 'possibly_sensitive' in tweets.keys():
                is_sensitive.append(tweets['possibly_sensitive'])
            else:
                is_sensitive.append(None)

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = []
        for tweets in self.tweets_list:
            if 'retweeted_status' in tweets.keys() and 'favorite_count' in tweets['retweeted_status'].keys(): 
                favourite_count.append(tweets['retweeted_status']['favorite_count'])
            else:
                favourite_count.append(tweets['favorite_count'])
            
        return favourite_count
    
    def find_retweet_count(self)->list:
        retweet_count = []
        for tweets in self.tweets_list:
            if 'retweeted_status' in tweets.keys() and 'retweet_count' in tweets['retweeted_status'].keys(): 
                retweet_count.append(tweets['retweeted_status']['retweet_count'])
            else:
                retweet_count.append(tweets['retweet_count'])        
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = [] 
        for tweets in self.tweets_list:
            hashtag = []
            for element in tweets['entities']['hashtags']:
                hashtag.append(element['text'])
            hashtags.append(hashtag)
        return hashtags
    
    def find_mentions(self)->list:
        mentions = []
        for tweets in self.tweets_list:
            mention = []
            for element in tweets['entities']['user_mentions']:
                mention.append(element['screen_name'])
            mentions.append(mention)
        return mentions
    
    def find_location(self)->list:
        locations = []
        for tweets in self.tweets_list:
            try:
                locations.append(tweets['user']['location'])
            except TypeError:
                locations.append(None)
        return locations
    
    def find_coordinates(self)->list:
        coordinates = []
        for tweets in self.tweets_list:
            if tweets['coordinates'] is None:
                coordinates.append(None)
            coordinates.append(tweets['coordinates'])
            
        return coordinates
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at','source','original_text','clean_text','sentiment','polarity','subjectivity','lang','favorite_count', 'retweet_count','original_author','screen_count','followers_count','friends_count','possibly_sensitive','user_mentions', 'place','place_coord_boundaries']
       
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        clean_text = self.find_clean_text(text)
        polarity, subjectivity = self.find_sentiments(text)
        sentiment = self.find_sentiment(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        screen_count = self.find_screen_count()
        followers_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        mentions = self.find_mentions()
        location = self.find_location()
        coordinates = self.find_coordinates()
        
        data = zip(created_at, source, text, clean_text, sentiment,polarity, subjectivity, lang, fav_count,retweet_count,screen_name, screen_count,followers_count,friends_count,sensitivity,mentions,location,coordinates)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df
                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = [ 'created_at','source','original_text','clean_text','sentiment','polarity','subjectivity','lang','favorite_count', 'retweet_count',
               'original_author','screen_count','followers_count','friends_count','possibly_sensitive','user_mentions','place','place_coord_boundaries']
    _,tweet_list = read_json("./data/covid19.json")

    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()
    clean = Clean_Tweets(tweet_df)
    clean_df =clean.drop_unwanted_column(tweet_df)
    clean_df =clean.drop_duplicate(clean_df)
    clean_df =clean.convert_to_datetime(clean_df)
    print(clean_df.head(5))
    clean_df.to_csv('./data/clean_tweet.csv')
