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
        statuses_count = [status['user']['statuses_count'] for status in self.tweets_list]
        return statuses_count
    def find_full_text(self)->list:
        full_text  = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet and 'extended_tweet' in tweet['retweeted_status']:
                full_text += [tweet['retweeted_status']['extended_tweet']['full_text']]
            else:
                full_text += [tweet['text']]
        return full_text
    def find_sentiments(self, text)->list:
        polarity, subjectivity = [], []
        for txt in text:
            t_blob = TextBlob(txt)
            polarity += [t_blob.polarity]
            subjectivity += [t_blob.subjectivity]
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at = [date['created_at'] for date in self.tweets_list]
        return created_at

    def find_source(self)->list:
        source = [tweet_source['source'] for tweet_source in self.tweets_list]
        return source

    def find_screen_name(self)->list:
        screen_name = [s_name['user']['screen_name'] for s_name in self.tweets_list]
        return screen_name
    def find_followers_count(self)->list:
        followers_count = [follower['user']['followers_count'] for follower in self.tweets_list]
        return followers_count

    def find_friends_count(self)->list:
        friends_count = [friend['user']['friends_count'] for friend in self.tweets_list]
        return friends_count 
    def is_sensitive(self)->list:
        isSensitive = []
        for sensitive in self.tweets_list:
            try:
                is_sensitive = sensitive['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            isSensitive += [is_sensitive]
        return isSensitive

    def find_favourite_count(self)->list:
        total_favourite = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet:
                total_favourite += [tweet['retweeted_status']['favorite_count']]
            else:
                total_favourite += [tweet['favorite_count']]
        return total_favourite
    
    def find_retweet_count(self)->list:
        total_retweet = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet:
                total_retweet += [tweet['retweeted_status']['retweet_count']]
            else:
                total_retweet += [tweet['retweet_count']]
        return total_retweet 

    def find_hashtags(self)->list:
        hashtags =[hashtag['entities']['hashtags'] for hashtag in self.tweets_list]
        return hashtags
    def find_mentions(self)->list:
        mentions = [mention['entities']['user_mentions'] for mention in self.tweets_list]
        return mentions

    def find_location(self)->list:
        locations = []
        for locate in self.tweets_list:
            try:
                location = locate['user']['location']
            except TypeError:
                location = ''
            locations += [location]
        return locations
    

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
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above

    
