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

    def find_statuses_count(self)->list:
        statuses_count = []
        for i in self.tweets_list:
            statuses_count.append(i.get('user').get('statuses_count'))
        return statuses_count     

    def find_full_text(self)->list:
        text = []
        for i in self.tweets_list:
            try: 
                text.append(i['retweeted_status']['extended_tweet']['full_text'])
            except KeyError:
                text.append(i['text'])
        return text
    
    def find_sentiments(self, text)->list:
        polarity = []
        subjectivity = []
        for i in text:
            blob = TextBlob(i)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at = []
        for i in self.tweets_list:
            created_at.append(i.get('created_at', None))
        return created_at

    def find_source(self)->list:
        source = []
        for i in self.tweets_list:
          source.append(i.get('source', None))
        return source

    def find_screen_name(self)->list:
        screen_name = []
        for i in self.tweets_list:
          screen_name.append(i.get('user', {}).get('screen_name', None))
        return screen_name

    def find_followers_count(self)->list:
        followers_count = []
        for i in self.tweets_list:
          followers_count.append(i.get('user', {}).get('followers_count', 0))
        return followers_count

    def find_friends_count(self)->list:
            friends_count = []
            for i in self.tweets_list:
                friends_count.append(i.get('user', {}).get('friends_count', 0))
            return friends_count
  
    def is_sensitive(self)->list:
        try:
            is_sensitive = [i['retweeted_status']['possibly_sensitive'] for i in self.tweets_list]
        except KeyError:
            is_sensitive = [None for i in self.tweets_list]

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = [i.get('retweeted_status', {}).get('favorite_count', 0) for i in self.tweets_list]
        return favourite_count
    
    def find_retweet_count(self)->list:
        retweet_count = [i.get('retweeted_status', {}).get('retweet_count', None) for i in self.tweets_list]
        return retweet_count

    def find_hashtags(self)->list:
        all_hashtags =[i.get('entities', {}).get('hashtags', None) for i in self.tweets_list]
        hash_tags = []
        for hashs in all_hashtags:
            if (hashs):
                cur_hashtags = []
                for hashs_obj in hashs:
                    try:
                        cur_hashtags.append(hashs_obj['text'])
                    except KeyError:
                        pass
                hash_tags.append(" ".join(cur_hashtags))
            else:
                hash_tags.append(None)

        return hash_tags

    def find_mentions(self)->list:
        all_mentions = [i.get('entities', {}).get('user_mentions', None) for i in self.tweets_list]
        mentions = []
        for mention_list_obj in all_mentions:
            if (mention_list_obj):
                cur_mentions = []
                for mention_obj in mention_list_obj:
                    try:
                        cur_mentions.append(mention_obj['screen_name'])
                    except KeyError:
                        pass
                mentions.append(" ".join(cur_mentions))
            else:
                mentions.append(None)
        return mentions

    def find_location(self)->list:
        location = []
        for i in self.tweets_list:
            location.append(i.get('user', {}).get('location', None))
        return location

    def find_lang(self)->list:
        lang = [i.get('lang', None) for i in self.tweets_list]
        return lang

    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['statuses_count', 'created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'screen_name', 'followers_count','friends_count','sensitivity', 'hashtags', 'user_mentions', 'place']
        
        statuses_count = self.find_statuses_count()
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
        data = zip(statuses_count, created_at, source, text, polarity, subjectivity, \
                lang, fav_count, retweet_count, screen_name, follower_count, \
                friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['statuses_count', 'created_at', 'source', 'original_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
     'screen_name','followers_count','friends_count','sensitivity', 'hashtags', 'user_mentions', 'place']
    # _, tweet_list = read_json("../Economic_Twitter_Data.json")
    _, tweet_list = read_json("/home/codeally/project/Twitter-Data-Analysis/data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(True) 