import json
import pandas as pd
from textblob import TextBlob
import re


def read_json(json_tweets_file: str) -> list:
    """
    json file reader to open and read json files into a list of tweets
    Args:
    -----
    json_tweets_file: str - path of a json file

    Returns
    -------
    A list of all tweets from a json file(input)
    """

    tweets_lst = []
    file_use = open(json_tweets_file, 'r')

    for tweets in file_use:
        tweets_lst.append(json.loads(tweets))

    file_use.close()

    return tweets_lst


class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe

    Return
    ------
    dataframe
    """

    def __init__(self, tweets_list):

        self.tweets_list = tweets_list

    # # an example function
    def find_statuses_count(self) -> list:
        statuses_count = [x['user']['statuses_count'] for x in self.tweets_list]

    def find_full_text(self) -> list:
        text = []
        # clean_text = []
        for tweet in self.tweets_list:
            if 'extended_tweet' in tweet.keys():
                # Store the extended tweet text if the tweet is a thread otherwise store just the text'
                text.append(tweet['extended_tweet']['full_text'])
            else:
                text.append(tweet['text'])
        return text

    def text_cleaner(self, text: list) -> list:
        clean_text = []
        for tweet_text in text:
            tweet_text = re.sub("^RT ", "", tweet_text)
            # mentions and hashtags
            tweet_text = re.sub("@[A-Za-z0-9:_]+", "", tweet_text)
            tweet_text = re.sub("#[A-Za-z0-9_]+", "", tweet_text)
            # remove links
            tweet_text = re.sub("http\S+", "", tweet_text)
            tweet_text = re.sub(r"www.\S+", "", tweet_text)
            tweet_text = re.sub("^ ", "", tweet_text)

            clean_text.append(tweet_text)
        return clean_text

    def find_sentiments(self, text: list) -> list:

        polarity = []
        subjectivity = []
        for tweet in text:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)

        return polarity, subjectivity

    def find_created_time(self) -> list:
        created_at = [x['created_at'] for x in self.tweets_list]

        return created_at

    def find_source(self) -> list:
        source = [x['source'] for x in self.tweets_list]

        return source

    def find_screen_name(self) -> list:
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]
        return screen_name

    def find_followers_count(self) -> list:
        followers_count = [x['user']['followers_count'] for x in self.tweets_list]
        return followers_count

    def find_friends_count(self) -> list:
        friends_count = [x['user']['friends_count'] for x in self.tweets_list]
        return friends_count

    def is_sensitive(self) -> list:

        is_sensitive = [tweet['possibly_sensitive'] if 'possibly_sensitive' in tweet.keys() else None for tweet in
                        self.tweets_list]

        return is_sensitive

    def find_favourite_count(self) -> list:
        favorite_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                favorite_count.append(tweet['retweeted_status']['favorite_count'])
            else:
                favorite_count.append(0)

        return favorite_count

    def find_retweet_count(self) -> list:

        retweet_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(tweet['retweeted_status']['retweet_count'])
            else:
                retweet_count.append(0)

        return retweet_count

    def find_hashtags(self) -> list:
        hashtags = []
        for tw in self.tweets_list:
            hashtags.append(", ".join([hashtag_item['text'] for hashtag_item in tw['entities']['hashtags']]))

    def find_hashtags(self) -> list:
        hashtags = [tw.get('entities', {}).get('hashtags', None)
                    for tw in self.tweets_list]

        return hashtags

    def find_mentions(self) -> list:
        mentions = []
        for tw in self.tweets_list:
            mentions.append(", ".join([mention['screen_name'] for mention in tw['entities']['user_mentions']]))

        return mentions

    def find_lang(self) -> list:
        lang = [x['lang'] for x in self.tweets_list]

        return lang

    def find_location(self) -> list:
        location = []
        for tweet in self.tweets_list:
            location.append(tweet['user']['location'])

        return location

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        # save = True
        """required column to be generated you should be creative and add more features"""
        columns = ['created_at', 'source', 'original_text', 'cleaned_text', 'polarity', 'polarity_clean',
                   'subjectivity', 'subjectivity_clean', 'lang',
                   'favorite_count',
                   'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags',
                   'user_mentions', 'place']

        # columns to add = ['sentiment','screen_count','place_coord_boundaries']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        text_new = self.text_cleaner(text)
        polarity, subjectivity = self.find_sentiments(text)
        polarity_clean, subjectivity_clean = self.find_sentiments(text_new)
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

        data_dic = {'created_at': created_at, 'source': source, 'original_text': text, 'cleaned_text': text_new,
                    'polarity': polarity, 'polarity_clean': polarity_clean, 'subjectivity_clean': subjectivity_clean,
                    'subjectivity': subjectivity, 'lang': lang, 'favorite_count': fav_count,
                    'retweet_count': retweet_count, 'original_author': screen_name, 'followers_count': follower_count,
                    'friends_count': friends_count, 'possibly_sensitive': sensitivity, 'hashtags': hashtags,
                    'user_mentions': mentions, 'place': location}
        df = pd.DataFrame(data=data_dic)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    tweet_list = read_json("data/Economic_Twitter_Data.json")

    tweet = TweetDfExtractor(tweet_list)
    df = tweet.get_tweet_df()