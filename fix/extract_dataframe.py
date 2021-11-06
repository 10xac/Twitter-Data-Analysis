import json
import pandas as pd
from textblob import TextBlob

def read_json(json_file: str)->list:
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    return len(tweets_data), tweets_data
class TweetDfExtractor:
    def __init__(self, tweets_list):
        self.tweets_list = tweets_list

    def find_statuses_count(self)->list:
        statuses_count = [x['user']['statuses_count'] for x in self.tweets_list]
        return statuses_count
        
    def find_full_text(self)->list:
        text = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys() and 'extended_tweet' in tweet['retweeted_status'].keys():
                text.append(tweet['retweeted_status']['extended_tweet']['full_text'])
            else: text.append('Empty')
        return text       
    
    def find_sentiments(self, text:list)->list:
        polarity, subjectivity = [], []
        for tweet in text:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at = [x['created_at'] for x in self.tweets_list]
        return created_at

    def find_source(self)->list:
        source = [x['source'] for x in self.tweets_list]
        return source

    def find_screen_name(self)->list:
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]
        return screen_name

    def find_followers_count(self)->list:
        followers_count = [x['user']['followers_count'] for x in self.tweets_list]
        return followers_count

    def find_friends_count(self)->list:
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]
        return friends_count

    def is_sensitive(self)->list:
        is_sensitive = []
        for tweet in self.tweets_list:
            if 'possibly_sensitive' in tweet.keys():
                is_sensitive.append(tweet['possibly_sensitive'])
            else: is_sensitive.append(None)
        return is_sensitive

    def find_favourite_count(self)->list:
        favorite_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                favorite_count.append(tweet['retweeted_status']['favorite_count'])
            else: favorite_count.append(0)
        return favorite_count

    def find_retweet_count(self)->list:
        retweet_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(tweet['retweeted_status']['retweet_count'])
            else: retweet_count.append(0)
        return retweet_count