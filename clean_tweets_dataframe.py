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
        df=self.df
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop([column_name],axis=1)
        
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        df=self.df
        df.drop_duplicates(inplace=True)
        
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        df=self.df
        df['created_at']=pd.to_datetime(df['created_at'])
        
       # df = df[df['created_at'] >= '2020-12-31' ]
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df=self.df
        df[['polarity','subjectivity','retweet_count','favourite_count']] = df[['polarity','subjectivity','retweet_count','favourite_count']].apply(pd.to_numeric)
        
       
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        df=self.df
        df = df[df['lang']==en]
        
        return df
