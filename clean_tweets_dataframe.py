import pandas as pd
from extract_dataframe import read_json,TweetDfExtractor
class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        # df = df[df['polarity'] != 'polarity']
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        
        df["original_text"]=df["original_text"].astype(str)
        df.drop_duplicates(subset=["original_text"] , inplace=True)

        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        df['created_at']=pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S %z %Y')
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df['polarity'],errors='coerce')
        df['subjectivity'] = pd.to_numeric(df['subjectivity'],errors='coerce')
        df['retweet_count'] = pd.to_numeric(df['retweet_count'],errors='coerce')
        df['favorite_count'] = pd.to_numeric(df['favorite_count'],errors='coerce')
        
        df['followers_count'] = pd.to_numeric(df['followers_count'],errors='coerce')
        
        df['friends_count'] = pd.to_numeric(df['friends_count'],errors='coerce')
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        unwanted_rows=df[df['lang'] != "en"].index

        df.drop(unwanted_rows ,inplace=True)
        
        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 
    clean_tweets=Clean_Tweets(tweet_df)
    # unwantedDropped=clean_tweets.drop_unwanted_column(tweet_df)
    # print(unwantedDropped[unwantedDropped['retweet_count'] == 'retweet_count' ])

    # dropped=clean_tweets.drop_duplicate(tweet_df)
    # print(type(dropped))
    # print(dropped[dropped.duplicated(original=False)])
    

    # clean=clean_tweets.remove_non_english_tweets(tweet_df)

    # print(clean[clean['lang'] != 'en' ])

    # data=clean_tweets.convert_to_numbers(tweet_df)

    # print(data.dtypes)

    # data=clean_tweets.convert_to_datetime(tweet_df)

    # print(data.dtypes)

        
    # data=clean_tweets.drop_duplicate(tweet_df)

    # print(data.duplicated(subset=["original_text"],keep="last").sum().astype(int))