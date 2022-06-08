import re 
import pandas as pd
from datetime import datetime
from dateutil import parser
import os, sys

sys.path.append(os.path.abspath(os.path.join('/data')))


emoji_pattern = re.compile('['
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)

class Clean_Tweets:
    
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self)->pd.DataFrame:
        
        columns = ['statuses_count', 'created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'screen_name', 'followers_count','friends_count','sensitivity', 'hashtags', 'user_mentions', 'place']
        unwanted_rows = [] 
        for colName in columns: 
            unwanted_rows = self.df[self.df[colName] == colName].index
            self.df.drop(unwanted_rows , inplace=True)
            self.df.reset_index(drop = True, inplace = True)

        return self.df
    
    def drop_null_values(self) -> pd.DataFrame:        
        self.df.dropna(subset = ['original_text', 'retweet_count'], inplace = True)
        self.df.reset_index(drop = True, inplace = True)
        return self.df

    def drop_duplicate(self)->pd.DataFrame:
        self.df.drop_duplicates(inplace = True)
        self.df.reset_index(drop = True, inplace = True)
        return self.df

    def convert_to_datetime(self)->pd.DataFrame:
        self.df['created_at'] = pd.to_datetime(self.df['created_at'], errors = 'coerce')
        self.df['created_at'] = self.df['created_at'].apply(lambda x : x.strftime('%Y-%m-%d'))
        self.df = self.df[self.df['created_at'] >= '2020-12-31']
        return self.df
    
    def convert_to_numbers(self)->pd.DataFrame:
        self.df['sensitivity'] = self.df['sensitivity'].apply(pd.to_numeric, errors = 'coerce')
        self.df['polarity'] = self.df['polarity'].apply(lambda x :pd.to_numeric(x))
        self.df['retweet_count'] = self.df['retweet_count'].apply(lambda x :pd.to_numeric(x))
        self.df['statuses_count'] = self.df['statuses_count'].apply(lambda x :pd.to_numeric(x))
        self.df['favorite_count'] = self.df['favorite_count'].apply(lambda x :pd.to_numeric(x))
        return self.df
    
    def preprocess_data(self) -> pd.DataFrame:    
        #text Preprocessing
        self.df['original_text'] = self.df['original_text'].astype(str)
        self.df['clean_tweet'] = self.df['original_text'].apply(lambda x: x.lower())
        self.df['clean_tweet'] = self.df['clean_tweet'].apply(lambda x: x.lower())
        self.df['clean_tweet'] = self.df['clean_tweet'].str.replace('[^\w\s]', '') #Remove punctuations
        return self.df

    def clean_tweet(self) -> pd.DataFrame:
        self.df['clean_tweet'] = self.df['clean_tweet'].apply(lambda x: emoji_pattern.sub(r',', x)) #Remove emojis
        self.df['clean_tweet'] = self.df['clean_tweet'].apply(lambda x: re.sub(r'RT @\w+:', ',', x))#Remove identifications
        self.df['clean_tweet'] = self.df['clean_tweet'].apply(lambda x: re.sub(r'@\w+', ',', x)) #Remove mentions
        self.df['clean_tweet'] = self.df['clean_tweet'].apply(lambda x: re.sub(r'https,?://[^/s]+[/s]?', ',', x))#Remove links
        self.df['clean_tweet'] = self.df['clean_tweet'].apply(lambda x: re.sub(r'\b\w{1,2}\b', ',',x))#Remove words with 2 or fewer letters
        return self.df

    def fill_nullvalues(self) -> pd.DataFrame:
        self.df['polarity'] = self.df['polarity'].fillna(False)
        self.df['created_at'] = self.df['created_at'].fillna(" ")
        self.df['place'] = self.df['place'].fillna(" ")
        self.df['hashtags'] = self.df['hashtags'].fillna(" ")
        self.df['user_mentions'] = self.df['user_mentions'].fillna(" ")
        self.df['retweet_count'] = self.df['retweet_count'].fillna(0)
        self.df['favorite_count'] = self.df['favorite_count'].fillna(0)
        self.df['followers_count'] = self.df['followers_count'].fillna(0)
        self.df['friends_count'] = self.df['friends_count'].fillna(0)
        self.df['statuses_count'] = self.df['statuses_count'].fillna(0)
        self.df['screen_name'] = self.df['screen_name'].fillna(" ")
        self.df['lang'] = self.df['lang'].fillna(" ")
        self.df['original_text'] = self.df['original_text'].fillna(" ")
        self.df['clean_tweet'] = self.df['clean_tweet'].fillna(" ")
        self.df['source'] = self.df['source'].fillna(" ")
        return self.df

    def remove_non_english_tweets(self)->pd.DataFrame:
        index_name = self.df[self.df.lang != 'en'].index
        self.df.drop(index_name,inplace = True)
        self.df.reset_index(drop = True, inplace = True)
        return self.df

    def clean_data(self, save = False) -> pd.DataFrame:
        self.df = self.drop_unwanted_column()
        self.df = self.drop_null_values()
        self.df = self.drop_duplicate()
        self.df = self.convert_to_datetime()
        self.df = self.convert_to_numbers()
        self.df = self.preprocess_data()
        self.df = self.clean_tweet()
        self.df = self.remove_non_english_tweets()
        self.df = self.fill_nullvalues()
        
        self.df = self.df[['statuses_count', 'created_at', 'source', 'original_text', 'clean_tweet', 'polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'screen_name', 'followers_count','friends_count','sensitivity', 'hashtags', 'user_mentions', 'place']]
        if save:
            self.df.to_csv('data/clean_economic_data.csv', index=False)
            print('File Successfully Saved.!!!')
        return self.df

if __name__ == "__main__":
    df = pd.read_csv("data/processed_tweet_data.csv")
    cleaner = Clean_Tweets(df)
    cleaner.clean_data(True)