
class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self):
        self.df = pd.DataFrame
print ('Automation in Action...!!!')
        
def drop_unwanted_column(self):
        self.df = pd.DataFrame
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        return df
print ('It is working')

def drop_duplicate(self):
        self.df = pd.DataFrame
        """
        drop duplicate rows
        """
        df.drop_duplicate(keep=False, inplace=True)
        
        return df
print ('It is working')        

def to_datetime(self):
        self.df = pd.DataFrame
        """
        convert column to datetime
        """
       
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        df = df[df['created_at'] >= '2020-12-31' ]
        
        return df
print ('It is working')        

def to_numeric(self):
        self.df = pd.DataFrame
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df['polarity'])
        df = df.apply(pd.to_numeric)
        
        return df
print ('It is working')        
    
def remove_non_english_tweets(self):
        self.df = pd.DataFrame
        """
        remove non english tweets from lang
        """
        
        # df = 
        
        return df