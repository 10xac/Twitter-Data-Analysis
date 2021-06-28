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
        count = []
        for i in self.tweets_list:
            count.append(i['user']['statuses_count'])
        return count

    def find_full_text(self)->list:
        text = []

        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet and 'extended_tweet' in tweet['retweeted_status']:
                text.append(tweet['retweeted_status']['extended_tweet']['full_text'])
            else:
                text.append(tweet['text'])
        return text        
       
    
    def find_sentiments(self, text)->list:
        polarity = []
        subjectivity = []
        for t in text:
            t_blob = TextBlob(t)
            polarity.append(t_blob.polarity)
            subjectivity.append(t_blob.subjectivity)
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_time = []
        for date in self.tweets_list:
            created_time.append(date['created_at'])
        return created_time

    def find_source(self)->list:
        t_source = [] 
        for txt in self.tweets_list:
            t_source.append(txt['source'])
        return t_source

    def find_screen_name(self)->list:
        name = []
        for nm in self.tweets_list:
            name.append(nm['user']['screen_name'])
        return name

    def find_followers_count(self)->list:
        followers = []
        for f in self.tweets_list:
            followers.append(f['user']['followers_count'])
        return followers

    def find_friends_count(self)->list:
        friends = []
        for f in self.tweets_list:
            friends.append(f['user']['friends_count'])
        return friends

    def is_sensitive(self)->list:
        sensitive = []
        for s in self.tweets_list:
            try:
                sen = s['possibly_sensitive']
            except KeyError:
                sen = None
            sensitive.append(sen)
        return sensitive


    def find_favourite_count(self)->list:
        favor_count = []
        for f in self.tweets_list:
            if 'retweeted_status' in f:
                favor_count.append(f['retweeted_status']['favorite_count'])
            else:
                favor_count.append(f['favorite_count'])
        return favor_count        
    
    def find_retweet_count(self)->list:
        ret_count = []
        for rt in self.tweets_list:
            if 'retweeted_status' in rt:
                ret_count.append(rt['retweeted_status']['retweet_count'])
            else:
                ret_count.append(rt['retweet_count'])
        return ret_count

    def find_hashtags(self)->list:
        hashtag = []
        for h in self.tweets_list:
            hashtag.append(h['entities']['hashtags'])
        return hashtag

    def find_mentions(self)->list:
        f_mention = []
        for f in self.tweets_list:
            f_mention.append(f['entities']['user_mentions'] for m in self.tweets_list)
        return f_mention 


    def find_location(self)->list:
        locations = []
        for l in self.tweets_list:
            try:
                location = l['user']['location']
            except TypeError:
                location = ''
            locations.append(location)
        return locations

    def find_lang(self)->list:
        langs = []
        for l in self.tweets_list:
            langs.append(l['lang'])
        return langs
        
        
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
