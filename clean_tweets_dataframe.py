import pandas as pd
df =pd.read_json(r"/Users/alex/Desktop/10_acadamy/Twitter-Data-Analysis/data/covid19.json" , lines= True)
df.to_csv(r'/Users/alex/Desktop/10_acadamy/Twitter-Data-Analysis/data/covid19.csv', index = None)
df = pd.read_csv("/Users/alex/Desktop/10_acadamy/Twitter-Data-Analysis/data/covid19.csv")
class CleanTweets:
    """
    This class is responsible for cleaning the twitter dataframe

    Returns:
    --------
    A dataframe
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
        self.df = self.df[self.df['polarity'] != 'polarity']

        return self.df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """

        self.df = self.df.drop_duplicates().drop_duplicates(subset='original_text')

        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = pd.to_datetime(self.df['created_at'], errors='coerce')

        self.df = self.df[self.df['created_at'] >= '2020-12-31' ]

        return self.df

    def convert_to_numbers(self)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """

        self.df['quote_count'] = pd.to_numeric(self.df["quote_count"], errors='coerce')
        self.df['retweet_count'] = pd.to_numeric(self.df['retweet_count'], errors='coerce')
        self.df['favorite_count'] = pd.to_numeric(self.df['favorite_count'], errors='coerce')
        self.df["reply_count"] = pd.to_numeric(self.df["reply_count"],error='coerce')


        return self.df

    def remove_non_english_tweets(self)->pd.DataFrame:
        """
        remove non english tweets from lang
        """

        self.df = self.df.query("lang == 'en' ")

        return self.df
if __name__ == "__main__":
    tweet_df = pd.read_csv("/Users/alex/Desktop/10_acadamy/Twitter-Data-Analysis/data/covid19.csv")
    cleaner = CleanTweets(tweet_df)
