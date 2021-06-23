import json
import pandas as pd
from textblob import TextBlob


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
        statuses_count = [x["user"]["statuses_count"]
                          for x in self.tweets_list]

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

    def find_original_text(self) -> list:
        original_text = [x['text'] for x in self.tweets_list]

        return original_text

    def find_sentiment(self, polarity, subjectivity) -> list:
        sentiment = []
        for i in range(len(polarity)):
            sentiment.append((polarity[i] + subjectivity[i])/2)

        return sentiment

    def find_sentiments(self, text) -> list:
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
        created_at = [x['created_at'] for x in self.tweets_list]

        return created_at

    def find_source(self) -> list:
        source = [x['source'] for x in self.tweets_list]

        return source

    def find_screen_name(self) -> list:
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]

        return screen_name

    def find_screen_count(self) -> list:
        screen_count = [x['user']['listed_count']
                        for x in self.tweets_list]

        return screen_count

    def find_followers_count(self) -> list:
        followers_count = [x['user']['followers_count']
                           for x in self.tweets_list]

        return followers_count

    def find_friends_count(self) -> list:
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]

        return friends_count

    def is_sensitive(self) -> list:
        is_sensitive = []
        for tweet in self.tweets_list:
            try:
                value = tweet["retweeted_status"]['possibly_sensitive']
                if(not value):
                    is_sensitive.append(None)
                else:
                    is_sensitive.append(value)
            except KeyError:
                is_sensitive.append(None)

        return is_sensitive

    def find_favourite_count(self) -> list:
        favourite_count = []
        for tweet in self.tweets_list:
            try:
                favourite_count.append(
                    tweet["retweeted_status"]['favorite_count'])
            except KeyError:
                favourite_count.append(0)

        return favourite_count

    def find_retweet_count(self) -> list:
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
        mentions = []
        main_mentions = [x['entities']['user_mentions']
                         for x in self.tweets_list]
        for mention in main_mentions:
            for each in mention:
                mentions.append(each['screen_name'])

        return mentions

    def find_place(self) -> list:
        place = [x['place'] for x in self.tweets_list]

        return place

    def find_coordinates(self) -> list:
        coordinates = [x['coordinates'] for x in self.tweets_list]

        return coordinates

    def find_location(self) -> list:
        location = [x['user']['location'] for x in self.tweets_list]

        return location

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        columns = ['created_at', 'source', 'original_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        original_text = self.find_original_text()
        clean_text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(clean_text)
        sentiment = self.find_sentiment(polarity, subjectivity)
        lang = self.find_lang()
        favorite_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        original_author = self.find_screen_name()
        screen_count = self.find_screen_count()
        followers_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        possibly_sensitive = self.is_sensitive()
        hashtags = self.find_hashtags()
        user_mentions = self.find_mentions()
        place = self.find_location()
        place_coord_boundaries = self.find_coordinates()
        data = zip(created_at, source, original_text, sentiment, polarity, subjectivity, lang, favorite_count, retweet_count,
                   original_author, followers_count, friends_count, possibly_sensitive, hashtags, user_mentions, place)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('./data/processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("./data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(save=True)

    # use all defined functions to generate a dataframe with the specified columns above
