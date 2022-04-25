import json
import pandas as pd
import os
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
    path = os.path.dirname(__file__)

    json_file_path = os.path.join(path, json_file)
    for tweets in open(json_file_path,'r'):
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
        statuses_count=[]
        for i in self.tweets_list:
            statuses_count.append(i["user"]["statuses_count"])
        return statuses_count
        
    def find_full_text(self)->list:
        text=[]
        for i in self.tweets_list:
            try:
                text.append(i["retweeted_status"]["extended_tweet"]["full_text"])
            except KeyError:
                text.append('')
        return text
       
    
    def find_sentiments(self, text)->list:
        polarity=[]
        subjectivity=[]
        for i in self.tweets_list:
            try:   
                text=TextBlob(i["retweeted_status"]["extended_tweet"]["full_text"])
                polarity.append(text.sentiment.polarity)
                subjectivity.append (text.sentiment.subjectivity)
            except KeyError:
                polarity.append(None)
                subjectivity.append(None)
        return polarity, subjectivity

    def find_created_time(self)->list:
        
        created_at=[]
        for i in self.tweets_list:
            created_at.append(i["created_at"])
        return created_at

    def find_source(self)->list:
        source=[]
        for i in self.tweets_list:
            source.append(i["source"])
        return source

    def find_screen_name(self)->list:
        screen_name=[]
        for i in self.tweets_list:
            screen_name.append(i["user"]["screen_name"])
        return screen_name

    def find_followers_count(self)->list:
        followers_count=[]
        for i in self.tweets_list:
            followers_count.append(i["user"]["followers_count"])
        return followers_count

    def find_friends_count(self)->list:
        friends_count=[]
        for i in self.tweets_list:
            friends_count.append(i["user"]["friends_count"])
        return friends_count

    def is_sensitive(self)->list:
        is_sensitive=[]
        for x in self.tweets_list:
            try:
                is_sensitive.append(x['possibly_sensitive'])
            except KeyError:
                is_sensitive.append(None)

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count=[]
        for i in self.tweets_list:
            try:
                favourite_count.append(i["retweeted_status"]["favorite_count"])
            except KeyError:
                favourite_count.append(None)
        return favourite_count
    
    def find_retweet_count(self)->list:
        retweet_count=[]
        for i in self.tweets_list:
            try:
                retweet_count.append(int(i["retweeted_status"]["retweet_count"]))
            except KeyError:
                retweet_count.append(0)
        return retweet_count

    def find_hashtags(self)->list:
        
        hashtags=[]
        for i in self.tweets_list:
            hashtags.append(str(i["entities"]["hashtags"]))
        return hashtags

    def find_mentions(self)->list:
        
        mentions=[]
        for i in self.tweets_list:
            mentions.append(i["entities"]["user_mentions"])
        return mentions


    def find_location(self)->list:
        location=[]
        for i in self.tweets_list:
            try:
                location.append(i['user']['location'])
            except TypeError:
                location.append('')
        
        return location

    def find_lang(self)->list:
        lang=[]
        for i in self.tweets_list:
            try:
                lang.append(i['lang'])
            except TypeError:
                lang.append('')
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
    from zipfile import ZipFile
    file='C:/Users/Success/visual_try/data/Economic_Twitter_Data.zip'
    with ZipFile(file, 'r') as zip:
        #zip.printdir()
        file=zip.extractall()
    data = []
    with open('Economic_Twitter_Data.json', errors='ignore') as f:
        for line in f:
            data.append(json.loads(line))
#print(data[0])
    df = pd.DataFrame(data)
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above