import pandas as pd

class TweetCleanser:
    """
    -this class cleans the tweets and
    ensures that the data is easy to work with
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
        - this function drop duplicate rows
        """
        self.df = self.df.drop_duplicates(subset=['original_text'])
        return self.df
        
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        return self.df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        for key in self.df.columns:
            if self.df[key].dtype == 'float64':
                self.df[key] = self.df[key].astype(int)
        return self.df
    
    def remove_non_english_tweets(self,df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang that is the language 
        column
        """
        self.df = self.df[self.df['lang'].str.contains("en")]
        return self.df

    def save_changes(self)->pd.DataFrame:
        self.df.to_csv("data/cleaned_data.csv",index=False)


if __name__ == "__main__":
    df = pd.read_csv("data/processed_tweet_data.csv")
    cleanser = TweetCleanser(df)
    cleanser.drop_unwanted_column(df)
    cleanser.drop_duplicate(df)
    cleanser.convert_to_datetime(df)
    cleanser.remove_non_english_tweets(df)
    cleanser.save_changes()
