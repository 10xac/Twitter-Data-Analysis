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
        try:
            statuses_count = [x['user']['statuses_count'] if 'user' in x else '' for x in self.tweets_list]
            return statuses_count
        except TypeError:
            statuses_count = ''

    def find_full_text(self) -> list:
        try:
            text = [tweet['retweeted_status']['extended_tweet']['full_text']
                    if ('retweeted_status' in tweet and 'extended_tweet' in tweet['retweeted_status']) else '' for tweet in self.tweets_list]
        except TypeError:
            text = ''
        return text
       
    
    def find_sentiments(self, text)->list:
        polarity = []
        subjectivity = []

        for each in text:
            if (each):
                result = TextBlob(str(each)).sentiment
                polarity.append(result.polarity)
                subjectivity.append(result.subjectivity)
            else:
                polarity.append("")
                subjectivity.append("")
                
            
        return polarity, subjectivity
    def find_created_time(self)->list:
       
        return [tweet['created_at'] for tweet in self.tweets_list]


    def find_source(self)->list:
        source = [tweet['source'] for tweet in self.tweets_list]
        return source
        

    def find_screen_name(self)->list:
        screen_name = [tweet['user']['screen_name'] if 'user' in tweet else " "for tweet in self.tweets_list]
        return screen_name

    def find_followers_count(self)->list:
       followers_count = [tweet['user']['followers_count'] for tweet in self.tweets_list]
       return followers_count
    def find_friends_count(self)->list:
        friends_count =  friends_count = [tweet['user']['friends_count'] for tweet in self.tweets_list]
        return friends_count

    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] if 'possibly_sensitive' in x else None for x in self.tweets_list]
        except KeyError:
            is_sensitive = ""

        return is_sensitive

    def find_favourite_count(self)->list:
        try:
            favorites_count = [x['retweeted_status']['favorite_count'] if 'retweeted_status' in x else '' for x in self.tweets_list]
            
        except KeyError:
            favorites_count = ""

        return favorites_count
    
    def find_retweet_count(self)->list:
        try:
            retweet_count =  [x['retweeted_status']['retweet_count'] if 'retweeted_status' in x else '' for x in self.tweets_list]
        except KeyError:
            retweet_count = ""
        return retweet_count

    def find_hashtags(self)->list:
        try:
            hashtags =  [x['retweeted_status']['extended_tweet']['entities']['hashtags'] if ('retweeted_status' in x) and( 'extended_tweet' in x['retweeted_status']) else '' for x in self.tweets_list]
        except KeyError:
            hashtags = ''
        return hashtags

    def find_mentions(self)->list:
        try:
            mentions =  [x['extended_tweet']['entities']['user_mentions'] if 'extended_tweet'in x else "" for x in self.tweets_list]
        except KeyError:
            mentions=""
    
        return mentions

    def find_location(self)->list:
        try:
            location =  [x['user']['location'] if 'user'in x else "" for x in self.tweets_list]
        except TypeError:
            location = ''
        
        return location

    def find_lang(self)->list:
        try:
            lang = [x['lang'] if 'lang' in x else '' for x in self.tweets_list]
        except TypeError:
            lang = ''
        return lang
        
        
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
    _, tweet_list = read_json("./data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(save=True) 

    # use all defined functions to generate a dataframe with the specified columns above
