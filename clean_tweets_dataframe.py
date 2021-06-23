import pandas as pd
import re


class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """

    def __init__(self):
        print('Automation in Action...!!!')

    def add_clean_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert original_text values to clean_text values
        """

        df['clean_text'] = df['original_text'].apply(clean_text)

        return df

    def drop_nullValue_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert original_text values to clean_text values
        """

        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    def drop_unwanted_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
                   'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
        unwanted_rows = []
        for columnName in columns:
            unwanted_rows += df[df[columnName] == columnName].index

        df.drop(unwanted_rows, inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """
        df['created_at'] = pd.to_datetime(df['created_at'])

        return df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df[['polarity', 'subjectivity', 'favorite_count', 'retweet_count', 'screen_count', 'followers_count', 'friends_count']] = df[[
            'polarity', 'subjectivity', 'favorite_count', 'retweet_count', 'screen_count', 'followers_count', 'friends_count']].apply(pd.to_numeric)

        return df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """

        index_names = df[df['lang'] != "en"].index

        df.drop(index_names, inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df


def clean_text(original_text: str) -> str:
    cleaned_text = re.sub('\n', '', original_text)
    cleaned_text = re.findall(r'[a-zA-Z]+', cleaned_text)
    cleaned_text = " ".join(cleaned_text)

    return cleaned_text
