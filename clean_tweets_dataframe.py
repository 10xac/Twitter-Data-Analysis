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
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        df.drop_duplicates(subset="created_at" , keep=False, inplace= True)
        
    
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        df['created_at'] = pd.to_datetime(df['created_at'], format='%Y%m%d')
        
        df = df[df['created_at'] >= '2020-12-31']
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df["polarity", "subjectivity", "retweet_count", "favorite_count"] = df[["polarity", "subjectivity", "retweet_count", "favorite_count"]].apply(pd.to_numeric)

        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        self.df = df.query("lang == 'en' ")


        return self.df

if __name__ == "__main__":
    tweet_df = pd.read_csv("./processed_tweet_data.csv")
    c = Clean_Tweets(tweet_df)
    # print(c.df.head())
    df = c.drop_unwanted_column(c.df)
    df = c.convert_to_numbers(df)
    df = c.drop_duplicate(df)
    df = c.remove_non_english_tweets(df)
    df = c.convert_to_datetime(df)

    df.to_csv('cleaned_tweet_data.csv', index=False)