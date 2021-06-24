import pandas as pd
<<<<<<< HEAD
=======


>>>>>>> make_unittest
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
<<<<<<< HEAD
        df = df.drop_duplicates()
=======
        df.drop_duplicates(inplace=True)
>>>>>>> make_unittest

        return df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """
<<<<<<< HEAD
        df = pd.to_datetime(df['created_at'], errors='coerce')
=======

        df['created_at'] = pd.to_datetime(
            df['created_at'])

>>>>>>> make_unittest
        return df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
<<<<<<< HEAD
        df['polarity', 'subjectivity', 'retweet_count', 'favorite_count'] = pd.to_numeric(df['polarity', 'subjectivity',
                                                                                             'retweet_count', 'favorite_count'])
=======
        df['polarity'] = pd.to_numeric(df["polarity"])
        df["subjectivity"] = pd.to_numeric(df["subjectivity"])
        df["retweet_count"] = pd.to_numeric(df["retweet_count"])
        df["favorite_count"] = pd.to_numeric(df["favorite_count"])
        df["friends_count "] = pd.to_numeric(df["polarity"])
>>>>>>> make_unittest

        return df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """
<<<<<<< HEAD
        df = df[df["lang"] == "en"]
=======

        df = df.drop(df[df['lang'] != 'en'].index)

        return df
>>>>>>> make_unittest
