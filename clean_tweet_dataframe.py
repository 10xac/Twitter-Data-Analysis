import pandas as pd

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
        unwanted_rows = self.df[self.df['retweet_count'] == 'retweet_count' ].index
        self.df.drop(unwanted_rows , inplace=True)
        self.df = self.df[self.df['polarity'] != 'polarity']
        
        return self.df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        self.df = self.df.drop_duplicates(subset = 'original_text', keep = False, inplace = True)
        
        return self.df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = self.df['created_at'].apply(lambda x : pd.to_datetime(x))
        
        self.df = self.df[self.df['created_at'] >= '2020-12-31' ]
        
        return self.df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        self.df['polarity'] = self.df['polarity'].apply(lambda x :pd.to_numeric(x))
        self.df['retweet_count'] = self.df['retweet_count'].apply(lambda x :pd.to_numeric(x))
        self.df['favorite_count'] = self.df['favorite_count'].apply(lambda x :pd.to_numeric(x))
        
        return self.df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        self.df = self.df[self.df.lang == 'en'].drop('lang', axis=1).reset_index()
        
        return self.df

df_2 = pd.read_csv('processed_tweet_data.csv')
a = Clean_Tweets(df_2)
print(a.df)