import json
import pandas as pd
from textblob import TextBlob
# to read the zipped data set we need to import this module
#from zipfile import ZipFile


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
    #with ZipFile(json_file, 'r') as zip_file:
        # extracting the zip
       # zip_file.extractall("data/")
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

        full_text = []
        for tweet in self.tweets_list:
            try:
                full_text.append(
                    tweet["retweeted_status"]['extended_tweet']['full_text'])
            except KeyError:
                full_text.append("")

        return full_text


    def find_sentiments(self, text) -> list:
        # pass
        polarityList = []
        subjectivityList = []
        for eachText in text:
            polarity, subjectivity = TextBlob(eachText).sentiment
            polarityList.append(polarity)
            subjectivityList.append(subjectivity)

        return polarityList, subjectivityList



    def find_lang(self) -> list:
        lang = [x['lang'] for x in self.tweets_list]

        return lang

    def find_created_time(self) -> list:
        # pass
        created_at = []
        for x in self.tweets_list:
            created_at.append(x['created_at'])
        return created_at

    def find_source(self) -> list:
        '''
        source = []
        for x in self.tweets_list:
            source.append(x['source'])
        return source
        :return:
        '''
        # pass
        source = [x['source'] for x in self.tweets_list]

        return source

    def find_screen_name(self) -> list:
        # pass
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]

        return screen_name

    def find_followers_count(self) -> list:
        # pass

        followers_count = [x['user']['followers_count'] for x in self.tweets_list]

        return followers_count

    def find_friends_count(self) -> list:
        # pass
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]

        return friends_count

    def is_sensitive(self) -> list:
        # pass
        is_sensitive = []
        for tweet in self.tweets_list:
            if 'possibly_sensitive' in tweet.keys():
                is_sensitive.append(tweet['possibly_sensitive'])
            else:
                is_sensitive.append(None)

        return is_sensitive

    def find_favourite_count(self) -> list:
        # pass
        favorite_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                favorite_count.append(tweet['retweeted_status']['favorite_count'])
            else:
                favorite_count.append(0)

        return favorite_count

    def find_retweet_count(self) -> list:
        #pass
        retweet_count = []
        for tweet in self.tweets_list:
            try:
                retweet_count.append(
                    tweet["retweeted_status"]['retweet_count'])
            except KeyError:
                retweet_count.append(0)

        return retweet_count


    def find_hashtags(self) -> list:
        hashtags = []
        for tweet in self.tweets_list:
            try:
                hashtags.append(tweet['entities']['hashtags'][0]['text'])
            except KeyError:
                hashtags.append(None)
            except IndexError:
                hashtags.append(None)

        return hashtags

    def find_mentions(self) -> list:
        #pass
        mentions = []
        main_mentions = [x['entities']['user_mentions']
                         for x in self.tweets_list]
        for mention in main_mentions:
            for each in mention:
                mentions.append(each['screen_name'])

        return mentions

    def find_location(self) -> list:
        #pass
        location = []
        for tweet in self.tweets_list:
            location.append(tweet['user']['location'])
        return location


    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        pass
        columns = ['created_at', 'source', 'original_text', 'polarity', 'subjectivity', 'lang', 'favorite_count','retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags','user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity= self.find_sentiments(text)
        subjectivity = self.find_sentiments(text)

        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity,  lang, fav_count, retweet_count, screen_name,
                   follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('./data/processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang',
               'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags',
               'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("./data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(save=True)

    # use all defined functions to generate a dataframe with the specified columns above
