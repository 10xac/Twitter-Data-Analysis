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
        unwanted_rows = df[df['retweet_count'] == 'retweet_count'].index
        df.drop(unwanted_rows, inplace=True)
        # df = df[df['polarity'] != 'polarity']  # I think this needs modification
        ####  Modifications
        unwanted_rows = df[df['favorite_count'] == 'favorite_count'].index
        df.drop(unwanted_rows, inplace=True)
        unwanted_rows = df[df['created_at'] == 'created_at'].index
        df.drop(unwanted_rows, inplace=True)
        unwanted_rows = df[df['id'] == 'id'].index
        df.drop(unwanted_rows, inplace=True)
        unwanted_rows = df[df['id_str'] == 'id_str'].index
        df.drop(unwanted_rows, inplace=True)
        unwanted_rows = df[df['source'] == 'source'].index
        df.drop(unwanted_rows, inplace=True)
        unwanted_rows = df[df['lang'] == 'lang'].index
        df.drop(unwanted_rows, inplace=True)
        unwanted_rows = df[df['retweet_count'] == 'retweet_count'].index
        df.drop(unwanted_rows, inplace=True)
        unwanted_rows = df[df['original_author'] == 'original_author'].index
        df.drop(unwanted_rows, inplace=True) # Think of a way to automate this
        
        return df

    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        ---
        """
        rows_without_duplicates = df.drop_duplicates(subset="id")
        df = rows_without_duplicates
        return df

    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime

        ----
        ----
        """
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df['polarity'], errors ='coerce') # changed
        df['subjectivity'] = pd.to_numeric(df['subjectivity'], errors ='coerce')  # changed
        df['retweet_count'] = pd.to_numeric(df['retweet_count'], errors ='coerce')  # changed
        df['favorite_count'] = pd.to_numeric(df['favorite_count'], errors ='coerce')  # changed
        
        # ----
        # ----
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        for index in df.index:
            if df.loc[index, 'lang'] != "en":
                df.drop(index, inplace=True)

            else:
                pass
        
        return df