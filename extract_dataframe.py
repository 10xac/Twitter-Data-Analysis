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
        statuses_count = [t['user']['statuses_count'] for t in self.tweets_list]
        return statuses_count
        
    def find_full_text(self)->list:
        texts = [current_tweet['retweeted_status']['extended_tweet']['full_text'] for current_tweet in self.tweets_list]
        return texts
       
#############################################
    def find_sentiments(self, text)->list:
        polarity,subjectivity = [],[]
        for tx in text:
            blob = TextBlob(tx)
            polarity.append(blob.polarity)
            subjectivity.append(blob.subjectivity)
        return polarity, subjectivity
            
        return [0 for t in self.tweets_list], [0 for t in self.tweets_list]
###############################################
    def find_created_time(self)->list:
       
        return [t['created_at'] for t in self.tweets_list]

    def find_source(self)->list:
        source = [t['source'] for t in self.tweets_list]
        return source

    def find_screen_name(self)->list:
        screen_name = [t['user']['screen_name'] for t in self.tweets_list]
        return screen_name

    def find_followers_count(self)->list:
        followers_count = [t['user']['followers_count'] for t in self.tweets_list]
        return followers_count

    def find_friends_count(self)->list:
        friends_count = [t['user']['friends_count'] for t in self.tweets_list]
        return friends_count
##################################################
    def is_sensitive(self)->list:
        sensitivity = []
        for t in self.tweets_list:
            try:
                is_sensitive = t['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            sensitivity.append(is_sensitive)

        return sensitivity
###################################################
    def find_favourite_count(self)->list:
        favourites_count = [t['retweeted_status']['favorite_count'] for t in self.tweets_list]
        return favourites_count
    
    def find_retweet_count(self)->list:
        retweet_count = [t['retweeted_status']['retweet_count'] for t in self.tweets_list]
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = [t['entities']['hashtags'] for t in self.tweets_list]
        return hashtags

    def find_mentions(self)->list:
        mentions = [t['entities']['user_mentions'] for t in self.tweets_list]
        return mentions


    def find_location(self)->list:
        locations = []
        for t in self.tweets_list:
            try:
                location = t['user']['location']
                print(location)
            except TypeError:
                location = ''
            locations.append(location)
        return locations

    def find_lang(self)->list:
        langs = [t['lang'] for t in self.tweets_list]
        return langs
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at','statuses_count', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        statuses_count = self.find_statuses_count()
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
        data = list(zip(created_at,statuses_count, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location))
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
    #print(tweet_list[0].keys())
    #for key in tweet_list[0].keys():
        #print(key,':',tweet_list[0][key])
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above
