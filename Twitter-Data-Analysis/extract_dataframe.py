import pandas as pd
import json
from textblob import TextBlob


class ExtractTweets:
    """
    - class for extracting tweets
    """
    def __init__(self,json_file: str)->list:
        data = []
        for tweets in open(json_file,'r'):
            data.append(json.loads(tweets))
        self.tweets = data

    def find_statuses_count(self)->list:
        """
        - this function returns the status counts
        """
        return list(map(lambda tweet: tweet['user']['statuses_count'], self.tweets))
    
    def find_full_text(self)->list:
        """
        - this function extracts the full texts of
        the tweets
        """
        return list(map(lambda tweet: tweet['text'], self.tweets))
        

    def find_sentiments(self, data:list)->list:
        """
        - this function finds sentiments from the dataset
        """
        get_polarity = [TextBlob(text).sentiment.polarity for text in data]
        get_subjectivity = [TextBlob(text).sentiment.subjectivity for text in data]
        return get_polarity, get_subjectivity

    def find_created_time(self)->list:
        """
        - this function returns a list of 
        the created time tags for when the tweet was generated
        """
        return  list(map(lambda tweet: tweet['created_at'], self.tweets))


    def find_source(self)->list:
        """
        - this function returns the source of the tweet
        """
        return  list(map(lambda tweet: tweet['source'], self.tweets))
        
    def find_screen_name(self)->list:
        """
        - this function returns the screen name of the person who has tweeted
        """
        return  list(map(lambda tweet: tweet['user']['screen_name'], self.tweets))
        
    def find_followers_count(self)->list:
        """
        - this function returns the amount of followers per user
        """
        return  list(map(lambda tweet: tweet['user']['followers_count'], self.tweets))
        
    def find_friends_count(self)->list:
        """
        - this function returns the number of friends the user has
        """
        return  list(map(lambda tweet: tweet['user']['friends_count'], self.tweets))
        
    def is_sensitive(self)->list:
        """
        - this function checks whether the data is sensitive or not
        """
        return [tweet['possibly_sensitive'] if "possibly_sensitive" in tweet.keys() else None \
        for tweet in self.tweets]
               

    def find_favourite_count(self)->list:
        """
        - this function returns the amount of times the tweet has been counted
        as favorite
        """
        return [tweet['retweeted_status']['favorite_count'] if 'retweeted_status' in tweet.keys() else 0 \
        for tweet in self.tweets]
        
    def find_retweet_count(self)->list:
        """
        - this function finds how many times a tweet has been retweeted
        """
        return [tweet['retweeted_status']['retweet_count'] if 'retweeted_status' in tweet.keys() else 0 \
        for tweet in self.tweets]
        
    
    def find_hashtags(self) -> list:
        """
        return the amount of hashtags in tweets
        """
        return [tweet.get('entities',dict()).get('hashtags', None)
                    for tweet in self.tweets]

        
    def find_mentions(self)->list:
        """
        - this function returns how many times 
        a person was mentioned in a tweet
        """
        return [" , ".join([count_['screen_name']  for tweet in self.tweets for count_ in tweet['entities']['user_mentions']])]
    
    def find_lang(self)->list:
        """
        return the language used to tweet
        """
        return list(map(lambda tweet:tweet['lang'],self.tweets))

    def find_location(self)->list:
        """
        returns the location in which the tweet was published
        """
        return [tweet['user']['location'] for tweet in self.tweets]
        
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
        values = [created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location]
        data_ = dict(zip(columns,values))
        data  = { key:pd.Series(value) for key, value in data_.items() }
        df = pd.DataFrame(data=data)
        
        if save:
            df.to_csv('data/processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
            
        return df


if __name__ == "__main__":

    extracted_tweets = ExtractTweets("C:/Users/User/Documents/DScience/Twitter-Data-Analysis-One/data/Economic_Twitter_Data.json")
    df = extracted_tweets.get_tweet_df(save=True)
