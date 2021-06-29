import pandas as pd
import datetime
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
        list_col = list(df.columns)

        for col in list_col:
            try:
                unwanted_rows = df[df[col] == col ].index
            except:
                continue
            df.drop(unwanted_rows , inplace=True)
        
        return df

    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        
        df.drop_duplicates(subset=['created_at', 'source', 'original_text', 'clean_text', 'polarity','subjectivity','lang',
        'favorite_count', 'retweet_count','original_author', 'followers_count','friends_count','place'], keep = 'first', inplace=True)
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        df['created_at'] = pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S +0000 %Y')
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        "They are number"
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """   
        Non_english_tweets = df[df['lang']!='en']
        df.drop(Non_english_tweets , inplace=True, axis=0)

        return df