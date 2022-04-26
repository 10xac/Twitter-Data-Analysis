import pandas as pd

class TweetCleanser:
    """
    -this class cleans the tweets and
    ensures that the data is easy to work with
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
        df = df[df['polarity'] != 'polarity']
        return df
        
    
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        - this function drop duplicate rows
        """
        df = df.drop_duplicates(subset=['original_text'])
        return df
        
    