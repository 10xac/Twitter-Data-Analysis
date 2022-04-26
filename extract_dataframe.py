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

    def find_statuses_count(self) -> list:
        """
        finds the number of tweets
        Returns
        -------
        list
        """
        statuses_count = [i['user']['status_count'] for i in self.tweets_list]
        return statuses_count

    def find_full_text(self) -> list:
        """
        Returns the tweet body including retweet status
        """
        try:
            retweeted_status = [x.get("retweeted_status", {}) for x in self.tweets_list]
            text =[(x.get("extended_tweet", {})).get("full_text", None) for x in retweeted_status]
            filtered = []
            for x in text:
                if x != None:
                    filtered.append(x)
                    text = ''.join(filtered)
        except KeyError:
            text = ''

        return text


    def find_sentiments(self, text) -> tuple:
        """
        returns lists of  polarity and subjectivity of the texts
        """
        polarity, subjectivity = [], []
        for x in text:
            blob = TextBlob(x)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)

        return polarity, subjectivity

    def find_created_time(self) -> list:
        """
        Returns a list of tweet created time
        """
        created_at = [i['created_at'] for i in self.tweets_list]

        return created_at

    def find_source(self) -> list:
        """
        Returns a list of application the tweet was sent on
        """
        source = [x['source'] for x in self.tweets_list]

        return source

    def find_screen_name(self) -> list:
        """
        Returns a list of authors usernames
        """
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]

        return screen_name

    def find_followers_count(self) -> list:
        """
        Returns a list of Author's followers count
        """
        followers_count = [x['user']['followers_count'] for x in self.tweets_list]

        return followers_count

    def find_friends_count(self) -> list:
        """
        Returns a list of users' friends count
        """
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]

        return friends_count

    def is_sensitive(self) -> list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self) -> list:
        """
        Returns number of favorites users' have
        """
        fav_count = []
        for x in self.tweets_list:
            if 'retweeted_status' in x.keys():
                fav_count.append(x['retweeted_status']['favourites_count'])
            else: fav_count.append(0)

        return fav_count

    def find_retweet_count(self) -> list:
        """
        Returns a list of tweets' retweet count
        """
        retweet_count = []
        for x in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(tweet['retweeted_status']['retweet_count'])
            else:
                retweet_count.append(0)

        return retweet_count

    def find_hashtags(self) -> list:
        """
        Returns a list of hashtags from the dataset
        """
        hashtags = []
        for t in self.tweets_list:
            hashtags.append(", ".join([hashtag_item['text'] for hashtag_item in t['entities']['hashtags']]))

        return hashtags

    def find_mentions(self) -> list:
        """
        Returns a list of mentions(if they exist)
        """
        mentions = []
        for t in self.tweets_list:
            mentions.append(", ".join([mention['screen_name'] for mention in t['entities']['user_mentions']]))

        return mentions

    def find_location(self) -> list:
        try:
            location = self.tweets_list['user']['location']
            # location = [x[self.tweets_list['user']['location']]for x in self.tweets_list]
        except TypeError:
            location = ''

        return location

    def find_lang(self) -> list:
        """
        Returns a list of tweets' language
        """
        language = self.tweets_list['user']['lang']
        return language

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        columns = ['created_at', 'source', 'original_text', 'polarity', 'subjectivity', 'lang', 'favorite_count',
                   'retweet_count', 'original_author', 'followers_count', 'friends_count', 'possibly_sensitive',
                   'hashtags', 'user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
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
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count,
                   screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    # use all defined functions to generate a dataframe with the specified columns above
