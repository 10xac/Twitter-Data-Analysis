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
        statuses_count = [value['user']['statuses_count']for value in self.tweets_list]
        return statuses_count
        
    def find_full_text(self)->list:
        text = [value['text']for value in self.tweets_list]
        clean_text = ''.join([word for word in text.lower() if word not in punctuation])
        return text,clean_text
       
    
    def find_sentiments(self, text)->list:
        subjectivity = [TextBlob(data['text']).sentiment.subjectivity for data in self.tweets_list]
        polarity = [TextBlob(data['text']).sentiment.polarity for data in data[1]]
        
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at = [value['created_at']for value in self.tweets_list]
       
        return created_at

    def find_source(self)->list:
        source = [value['source'] for value in self.tweets_list]

        return source

    def find_screen_name(self)->list:
        find_screen_name = [value['user']['screen_name'] for value in self.tweets_list]
        return find_screen_name

    def find_followers_count(self)->list:
        followers_count = [value['user']['followers_count'] for value in self.tweets_list]
        return followers_count

    def find_friends_count(self)->list:
        friends_count = [value['user']['friends_count'] for value in self.tweets_list]
        return friends_count

    def is_sensitive(self)->list:
        is_sensitive = []
        try:
            is_sensitive = [value['possibly_sensitive'] for value in self.tweets_list]
        except KeyError:
            for value in self.tweets_list:
                value['possibly_sensitive']=''
                is_sensitive.append(value['possibly_sensitive'])

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = [value['user']['favourites_count'] for value in self.tweets_list]
        return favourite_count
    
    def find_retweet_count(self)->list:
        retweet_count = [value['retweet_count'] for value in self.tweets_list]
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = [value['entities']['hashtags'] for value in self.tweets_list]
        return hashtags

    def find_mentions(self)->list:
        mentions = [value['entities']['user_mentions'] for value in self.tweets_list]
        return mentions

    def find_location(self)->list:
        location = []
        try:
            location = [value['user']['location'] for value in self.tweets_list]
        except TypeError:
            for value in self.tweets_list:
                value['user']['location']=''
                location.append(value['user']['location'])
        
        return location   
    def find_lang(self)->list:
        lang = [value['lang']for value in self.tweets_list]
        return lang
    
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','clean_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text,clean_text = self.find_full_text()
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
       
        data = zip(created_at, source, text, clean_text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
    _, tweet_list = read_json("data/Twitter-Data-Analysis/Twitter-Data-Analysis.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above
    

    
