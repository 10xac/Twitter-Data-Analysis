import json
import pandas as pd
from textblob import TextBlob
# to read the zipped data set we need to import this module
from zipfile import ZipFile


def read_json(json_file: str) -> list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file

    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    # openning the zip in READ mode
    with ZipFile(json_file, 'r') as zip_file:
    # extracting the zip
        zip_file.extractall("data/")
    for tweets in open(json_file, 'r'):
        tweets_data.append(json.loads(tweets))

    return len(tweets_data), tweets_data


class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe

    Return
    ------
    dataframe
    """

    def __init__(self, tweets_list):
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self) -> list:
        statuses_count = [tweet['user']['statuses_count']
                          for tweet in self.tweets_list]
        return statuses_count

    def find_full_text(self) -> list:
        pass
        # text =

    def find_sentiments(self, text) -> list:
        pass

        # return polarity, self.subjectivity

    def find_created_time(self) -> list:
        pass
        # return created_at

    def find_source(self) -> list:
        pass
        # source =

        # return source

    def find_screen_name(self) -> list:
        pass
        # screen_name =

    def find_followers_count(self) -> list:
        pass
        # followers_count =

    def find_friends_count(self) -> list:
        pass
        # friends_count =

    def is_sensitive(self) -> list:
        pass
        # try:
        #   is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        # except KeyError:
        #   is_sensitive = None

        # return is_sensitive

    def find_favourite_count(self) -> list:
        pass

    def find_retweet_count(self) -> list:
        pass
        # retweet_count =

    def find_hashtags(self) -> list:
        pass
        # hashtags =

    def find_mentions(self) -> list:
        pass
        # mentions =

    def find_location(self) -> list:
        pass
        # try:
        #   location = self.tweets_list['user']['location']
        # except TypeError:
        # location = ''

    # return location

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        pass
        columns = ['created_at', 'source', 'original_text', 'polarity', 'subjectivity', 'lang', 'favorite_count',
                   'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags',
                   'user_mentions', 'place']

        # created_at = self.find_created_time()
        # source = self.find_source()
        text = self.find_full_text()
        # polarity, subjectivity = self.find_sentiments(text)
        # lang = self.find_lang()
        # fav_count = self.find_favourite_count()
        # retweet_count = self.find_retweet_count()
        # screen_name = self.find_screen_name()
        # follower_count = self.find_followers_count()
        # friends_count = self.find_friends_count()
        # sensitivity = self.is_sensitive()
        # hashtags = self.find_hashtags()
        # mentions = self.find_mentions()
        # location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang',
               'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags',
               'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("./data/Economic_Twitter_Data.zip")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    # use all defined functions to generate a dataframe with the specified columns above
