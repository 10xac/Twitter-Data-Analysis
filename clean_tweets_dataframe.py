import pandas as pd
#import re



class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self):
       # self.df = df
        print('Automation in Action...!!!')

    def drop_nullValue_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert original_text values to clean_text values
        """

        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        
        return df


    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
       # pass
        """
        drop duplicate rows
        """


        df.drop_duplicates(subset= "created_at" , keep=False, inplace=True)
        #df.reset_index(drop=True, inplace=True)

        return df
        

        

    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        #pass
        """
        convert column to datetime
        """

        self.df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

        self.df = df[df['created_at'] >= '2020-12-31']

        return self.df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        #pass
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df[['polarity', 'subjectivity', 'favorite_count', 'retweet_count', 'screen_count', 'followers_count',
            'friends_count']] = df[[
            'polarity', 'subjectivity', 'favorite_count', 'retweet_count', 'screen_count', 'followers_count',
            'friends_count']].apply(pd.to_numeric)

        return df

        


    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """

        index_names = df[df['lang'] != "en"].index

        df.drop(index_names, inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df
if __name__ == 'main':
    df = pd.read_csv('/data/processed_tweet_data.csv')
    clean = Clean_Tweets(df)

    df = clean.drop_duplicate(df)
    df = clean.remove_non_english_tweets(df)
    df = clean.convert_to_datetime(df)
    df = clean.convert_to_numbers(df)
    df = clean.drop_unwanted_column(df)

    df.to_csv('/data/clean_processed_tweet_data.csv')
