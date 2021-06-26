import nltk
import numpy as np
import pandas as pd
#from extract_dataframe import tweet_df


class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')

    def drop_unwanted_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.
        """
        df = df[df['retweet_count'] == 'retweet_count']
        df.reset_index()

        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        df = df.iloc[df.astype(str).drop_duplicates().index]
        df.reset_index()

        return df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """
        df['created_at'] = pd.to_datetime(df['created_at']).dt.date

        df = df[df['created_at'] >= pd.to_datetime("2020-12-31").date()]
        df.reset_index()
        return df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df['polarity'])
        df['subjectivity'] = pd.to_numeric(df['subjectivity'])
        # df['quote_count'] = pd.to_numeric(df['quote_count'])
        # df['reply_count'] = pd.to_numeric(df['reply_count'])
        df['retweet_count'] = pd.to_numeric(df['retweet_count'])
        df['favorite_count'] = pd.to_numeric(df['favorite_count'])
        df['followers_count'] = pd.to_numeric(df['followers_count'])
        df['friends_count'] = pd.to_numeric(df['friends_count'])

        return df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """
        df = df[df['lang'] == 'en']
        df.reset_index()
        return df

#cleaned_df = Clean_Tweets(tweet_df)
#cleaned_df.to_csv("./data/cleaned_covid19.csv")