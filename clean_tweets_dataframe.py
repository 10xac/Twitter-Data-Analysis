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
        
        ---
        df = df.drop_duplicates(subset = 'id',keep=False, inplace=True)
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        ----
        
        ----
        df['created_at'] = pd.to_datetime(df['created_at'],utc=True).dt.strftime('%m/%d/%Y')
        
        
        return df
    
    def convert_to_numbers(self,column, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df[column] = pd.to_numeric(df[column])
        ----
        ----
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        eng_text=[]
        """
        remove non english tweets from lang
        """
        text = df['lang']  
        for sen in text:
            for w in nltk.wordpunct_tokenize(sen):
                if w.lower() in words or not w.isalpha():
                    pass
            eng_text.append(sen)
            
        df['lang'] = eng_text
        return df