import pandas as pd


class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        '''
    def drop_unwanted_row(self, df:pd.DataFrame):
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_row = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_row , inplace=True )
        #df = df[df['polarity'] != 'polarity']
        
        '''
    def drop_duplicate(self, df:pd.DataFrame):
        """
        drop duplicate rows
        """
        
        df=df.drop_duplicates(inplace = False)    # Drop duplicates
        
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        
        df['created_at'] = pd.to_datetime(df['created_at'])
        #tweets from 2021 onwards
        #df['created_at'] = df[df['created_at'] >= '2020-12-31' ]
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        
        
        df['polarity'] = pd.to_numeric(df['polarity'])
        df['subjectivity'] = pd.to_numeric(df['subjectivity'])
        df['retweet_count'] = pd.to_numeric(df['retweet_count'])
        df['favorite_count'] = pd.to_numeric(df['favorite_count'])
        df['followers_count'] = pd.to_numeric(df['followers_count'])
        df['friends_count'] = pd.to_numeric(df['friends_count'])
       
        
        
        return df
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        df= df[df['lang'] == 'en']
    
        
        return df
    def drop_nan(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove nan values
        """
        df.dropna()
        
        return df
    def reset_index(self, df:pd.DataFrame)->pd.DataFrame:
        """
        resetting the index after dropping values
        """
        df.reset_index(drop=True)
        return df
    
    def clean_df(self, df: pd.DataFrame)->pd.DataFrame:
        
        #self.drop_unwanted_row(df) 
        cleaned_data=self.remove_non_english_tweets(df)
        cleaned_data =self.drop_duplicate(cleaned_data)
        cleaned_data= self.convert_to_datetime(cleaned_data)
        cleaned_data= self.convert_to_numbers(cleaned_data)
        cleaned_data= self.drop_nan(cleaned_data)
        cleaned_data= self.reset_index(cleaned_data)
               
        return cleaned_data
    
if __name__ == "__main__":
    df=pd.read_csv('processed_tweet_data.csv')
        
    cleaner=Clean_Tweets(df)
    
    cleaned_data=cleaner.clean_df(df)