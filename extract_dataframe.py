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
        
        statuses_count = []
        for i in self.tweets_list:
            statuses_count.append(i['user']['statuses_count'])
        return statuses_count 
        
    def find_full_text(self)->list:
        text=[]
        for i in self.tweets_list:
            text.append(i['text'])
            
        return text 
    def find_sentiments(self, text)->list:
            polarity = []
            subjectivity = []

            for each in text:
                if (each):
                    result = TextBlob(str(each)).sentiment
                    polarity.append(result.polarity)
                    subjectivity.append(result.subjectivity)
            
            return polarity, subjectivity

    def is_sensitive(self)->list:
        isSensitive = []
        for sensitive in self.tweets_list:
            try:
                is_sensitive = sensitive['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            isSensitive += [is_sensitive]
        return isSensitive

    def find_lang(self)->list:
        lang = []
        for i in self.tweets_list:
            lang.append(i['lang'])
        return lang

    def find_created_time(self)->list:
        created_at= []
        for i in self.tweets_list:
            created_at.append(i['created_at'])
       
        return created_at

    def find_source(self)->list:
        source = []
        for i in self.tweets_list:
            source.append(i['source'])

        return source

    def find_screen_name(self)->list:
        screen_name = []
        for i in self.tweets_list:
            screen_name.append(i['user']['screen_name'])
        return screen_name    

    def find_followers_count(self)->list:
        followers_count = []
        for i in self.tweets_list:
            followers_count.append(i['user']['followers_count'])
        return followers_count

    def find_friends_count(self)->list:
        friends_count = []
        for i in self.tweets_list:
            friends_count.append(i['user']['friends_count'])
        return friends_count    

    

    def find_favourite_count(self)->list:
        favourite_count=[]
        for i in self.tweets_list:
            favourite_count.append(i['user']['favourites_count'])
        return favourite_count    
            
    def find_retweet_count(self)->list:
        retweet_count = []
        for i in self.tweets_list:
            retweet_count.append(i['retweet_count'])
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = []
        for i in self.tweets_list:
            hashtags.append(i['entities']['hashtags'])
        return hashtags    

    def find_mentions(self)->list:
        try:
           mentions= self.tweets_list['location']
        except TypeError:
            mentions = ''
        
        return mentions
    
     
    def find_location(self)->list:
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
        # follower_count, friends_count, sensitivity, hashtags, mentions, location)
        print(type(follower_count), type(friends_count), type(sensitivity))
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
    _, tweet_list = read_json("/home/eyerusalem/mine/Twitter-Data-Analysis/data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 
