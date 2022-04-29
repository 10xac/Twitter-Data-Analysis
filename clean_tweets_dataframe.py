import pandas as pd
from string import punctuation

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
<<<<<<< HEAD:clean_tweets_dataframe.py

=======
        
        ---
>>>>>>> 8d857d43ecfe5ea206f51bb26d1da8571f8e89e0:fix_clean_tweets_dataframe.py
        df = df.drop_duplicates(subset = 'id',keep=False, inplace=True)
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
<<<<<<< HEAD:clean_tweets_dataframe.py

=======
        ----
        
        ----
>>>>>>> 8d857d43ecfe5ea206f51bb26d1da8571f8e89e0:fix_clean_tweets_dataframe.py
        df['created_at'] = pd.to_datetime(df['created_at'],utc=True).dt.strftime('%m/%d/%Y')
        
        
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
<<<<<<< HEAD:clean_tweets_dataframe.py
        df['friends_count'] = pd.to_numeric(df['friends_count'])

=======
        df['find_friends_count'] = pd.to_numeric(df['find_friends_count'])
        ----
        ----
>>>>>>> 8d857d43ecfe5ea206f51bb26d1da8571f8e89e0:fix_clean_tweets_dataframe.py
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
<<<<<<< HEAD:clean_tweets_dataframe.py
        df = df.loc[df['lang'] =="en"]
=======
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
>>>>>>> 8d857d43ecfe5ea206f51bb26d1da8571f8e89e0:fix_clean_tweets_dataframe.py
        return df
