import pandas as pd

"""
The PEP8 Standard AMAZING!!!
"""

"""
The clean Tweets class for cleaning some features of the tweets dataframe. 
"""
class Clean_Tweets:

    def __init__(self, df:pd.DataFrame):
        """
        The initializer for the Clean_Tweets class, with an indication
        when the initialization is over.
        """
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from the 
        data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        return df
    
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        # drop duplicate rows based on the column text
        df.drop_duplicates().drop_duplicates(subset='text', inplace=True)
        return df
    
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        # convert datetime column to datetime
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df = df[df['created_at'] >= '2020-12-31' ]
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count 
        favorite_count etc to numbers.
        """
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        df['listed_count'] = pd.to_numeric(df['listed_count'], 
                                            errors='coerce')
        df['retweet_count'] = pd.to_numeric(df['retweet_count'], 
                                            errors='coerce')
        df['friends_count'] = pd.to_numeric(df['friends_count'],
                                            errors='coerce')
        df['favorite_count'] = pd.to_numeric(df['favorite_count'],
                                            errors='coerce')
        df['statuses_count'] = pd.to_numeric(df['statuses_count'],
                                            errors='coerce')
        df['followers_count'] = pd.to_numeric(df['followers_count'],
                                            errors='coerce')
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        # remove non english tweets from lang
        df.query("lang == 'en'", inplace=True)
        return df

if __name__ == "__main__":
    """
    read the twitter dataset and Pass the data to the Clean_Tweets
    class
    """ 
    tweet_df = pd.read_json("data/Economic_Twitter_Data.json", lines=True)
    cleaner = Clean_Tweets(tweet_df)
