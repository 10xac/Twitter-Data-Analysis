import pandas as pd


#Debugged by Ammon on April 25th 2022

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
        df = df[df['polarity'] != 'polarity']
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        #code to drop duplicates with the same entry on all columns
               
        for i in len(df. columns):
            df.drop_duplicates(subset=df.iloc[:, i], keep=False , inplace=True)
        
        return df
   
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        #changing the column to date format using todatetime() func
        
        df['created_at'] = pd.to_datetime()
        df = df[df['created_at'] >= '2020-12-31' ]
         
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        #changing the column to numbers format using tonumeric() func
        
        df['polarity'] = pd.to_numeric()
        df['subjectivity'] = pd.to_numeric()
        df['retweet_count'] = pd.to_numeric()
        df['favorite_count'] = pd.to_numeric()
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        self.df = df[df['lang']=='en']
        
        return df