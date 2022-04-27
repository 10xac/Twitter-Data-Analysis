import pandas as pd

class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = self.df[self.df['retweet_count'] == 'retweet_count' ].index
        self.df.drop(unwanted_rows , inplace=True)
        
        return self.df
    
    def drop_duplicate(self)->pd.DataFrame:
        """
        drop duplicate rows
        """
        # Drop the posts that have the same text
        self.df = self.df.drop_duplicates(subset='text')
        
        return self.df
    
    def convert_to_datetime(self)->pd.DataFrame:
        """
        convert column to datetime
        """
        # Make a copy of the data frame
        self.df = self.df.copy()
        # Convert the corresponding column
        self.df.loc[:,'created_at'] = pd.to_datetime(self.df.loc[:,'created_at'],errors='coerce')
        
        self.df = self.df[self.df['created_at'] >= '2020-12-31' ]
        
        return self.df
    
    def convert_to_numbers(self)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        self.df = self.df.copy()
        # Convert polarity
        self.df.loc[:,"polarity"] = pd.to_numeric(self.df["polarity"],errors='coerce')
        # Convert subjectivity
        self.df.loc[:,"subjectivity"] = pd.to_numeric(self.df["subjectivity"],errors='coerce')
        # Convert friends_cout
        self.df.loc[:,"friends_count "] = pd.to_numeric(self.df["polarity"],errors='coerce')
        # Convert retweet_count
        self.df.loc[:,'retweet_count'] = pd.to_numeric(self.df['retweet_count'],errors='coerce')
        # Convert favorite_count
        self.df.loc[:,'favorite_count'] = pd.to_numeric(self.df['favorite_count'],errors='coerce')
        
        return self.df
    
    def remove_non_english_tweets(self)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        # Removing non english tweets from lang is the same as selecting only english tweets from lang
        self.df = self.df.query("lang=='en'") 
        
        return self.df