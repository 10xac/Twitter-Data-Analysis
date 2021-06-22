import json
import pandas as pd
from textblob import TextBlob

def read_json(json_file: str)->list:
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
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    print(len(tweets_data))
    return len(tweets_data), tweets_data


class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    #------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = []
        count = 0
        for element in self.tweets_list:
            count = count +element['user']['friends_count']

        return statuses_count.append(count)
        
    def find_full_text(self)->list:
        text = []
        for element in self.tweets_list:
            if 'retweeted_status' in element:
                if 'extended_tweet' in element['retweeted_status']:
                    text.append(element['retweeted_status']['extended_tweet']['full_text'])
                else:
                    text.append(element['retweeted_status']['text'])

            if 'extended_tweet' in element['quoted_status']:
                text.append(element['quoted_status']['extended_tweet']['full_text'])
            else:
                text.append(element['quoted_status']['text'])

            else:
                text.append(element['text']) # Append to the txt

        return text
    
    def find_sentiments(self, text)->list:
        polarity = []
        for element in self.tweets_list:
            if 'retweeted_status' in element:
                if 'extended_tweet' in element['retweeted_status']:
                    polarity.append(element['retweeted_status']['extended_tweet']['polarity'])
                else:
                    polarity.append(element['retweeted_status']['polarity'])
            else:
                polarity.append(element['polarity'])
        return polarity, self.subjectivity

    def find_created_time(self)->list:
        created_at = [] # Initialize empty list
        for element in self.tweets_list:
            if 'retweeted_status' in element:
                if 'extended_tweet' in element['retweeted_status']:
                    created_at.append(element['retweeted_status']['extended_tweet']['created_at'])
                else:
                    created_at.append(element['retweeted_status']['created_at'])
            else:
                created_at.append(element['polarity'])

        return created_at

    def find_source(self)->list:
        source = []
        for element in self.tweets_list:
            if 'retweeted_status' in element:
                if 'quoted_status' in element['retweeted_status']:
                    source.append(element['retweeted_status']['quoted_status']['source'])
                else:
                    source.append(element['retweeted_status']['source'])

            if 'extended_tweet' in element['quoted_status']:
                source.append(element['quoted_status']['extended_tweet']['source'])
            else:
                source.append(element['quoted_status']['source'])


        return source

    def find_screen_name(self)->list:
        screen_name = ""

    def find_followers_count(self)->list:
        followers_count = []
        followers = 0
        for element in self.tweets_list:
            followers = followers + element['user']['followers_count']

        return followers_count.append(followers)

    def find_friends_count(self)->list:
        friends_count = []
        friends = 0
        for element in self.tweets_list:
            friends = friends + element['user']['friends_count']

        return friends_count.append(friends)

    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = []
        count = 0
        for element in self.tweets_list:
            count = count + element['user']['favourites_count']

        return favourite_count.append(count)
    
    def find_retweet_count(self)->list:
        retweet_count = ""

    def find_hashtags(self)->list:
        hashtags =""

    def find_lang(self)->list:
        try:
            lang = self.tweets_list['user']['lang']
        except TypeError:
            lang = ''

        return lang

    def find_mentions(self)->list:
        mentions = ""


    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        print(created_at)
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
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above
    