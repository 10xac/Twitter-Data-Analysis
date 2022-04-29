import pandas as pd
import extract_dataframe as ed


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
        unwanted_rows = df[df['retweet_count'] == 'retweet_count'].index
        df.drop(unwanted_rows, inplace=True)
        df = df[df['polarity'] != 'polarity']

        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        df.drop_duplicates(inplace=True)

        return df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """

        df['created_at'] = pd.to_datetime(
            df['created_at'])

        return df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df["polarity"])
        df["subjectivity"] = pd.to_numeric(df["subjectivity"])
        df["retweet_count"] = pd.to_numeric(df["retweet_count"])
        df["favorite_count"] = pd.to_numeric(df["favorite_count"])
#         df["friends_count "] = pd.to_numeric(df["friends_count"])

        return df

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
            handle missing values
        """

        df['possibly_sensitive'] = df['possibly_sensitive'].fillna(0)
        df['place'] = df['place'].fillna(" ")
        df['hashtags'] = df['hashtags'].fillna(" ")
        df['user_mentions'] = df['user_mentions'].fillna(" ")
        df['retweet_count'] = df['retweet_count'].fillna(0)

        return df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """

        df = df.drop(df[df['lang'] != 'en'].index)

        return df


if __name__ == '__main__':
    _, tweet_list = ed.read_json("data/Economic_Twitter_Data.zip")
    tweet = ed.TweetDfExtractor(tweet_list)
    df = tweet.get_tweet_df(True)
    ola = Clean_Tweets(df)
