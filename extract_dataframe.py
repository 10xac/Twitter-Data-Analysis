import json
import pandas as pd
from textblob import TextBlob
import re

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
        for element in self.tweets_list:
            try:
                if 'user' in element:
                    statuses_count.append(element['user']['statuses_count'])

                else:
                    statuses_count.append(element['retweeted_status']['user']['statuses_count'])

            except Exception as e:
                print(e)
                statuses_count.append(None)

        return statuses_count
        
    def find_full_text(self)->list:
        text = []
        for element in self.tweets_list:
            if 'retweeted_status' in element:
                try:
                    if 'extended_tweet' in element['retweeted_status']:
                        text.append(element['retweeted_status']['extended_tweet']['full_text'])
                    else:
                        text.append(element['retweeted_status']['text'])
                except Exception as e:
                    print(e)

            else:
                try:
                    if 'extended_tweet' in element['quoted_status']:
                        text.append(element['quoted_status']['extended_tweet']['full_text'])
                    else:
                        text.append(element['quoted_status']['text'])
                except Exception as e:
                    print(e)
                    if 'text' in element:
                        text.append(element['text'])
                    else:
                        text.append(None)

        return text
    
    def find_sentiments(self, text)->list:
        polarity, subjectivity, sentiment = [], [], []
        tetx = ""
        for element in self.tweets_list:
            if 'retweeted_status' in element:
                try:
                    if 'extended_tweet' in element['retweeted_status']:
                        text = element['retweeted_status']['extended_tweet']['full_text']
                    else:
                        text = element['retweeted_status']['text']
                except Exception as e:
                    print(e)
            else:
                try:
                    if 'extended_tweet' in element['quoted_status']:
                        text = element['quoted_status']['extended_tweet']['full_text']
                    else:
                        text = element['quoted_status']['text']
                except:
                    # print(e)
                    text = element['text']
            polarity1 = TextBlob(text).polarity
            subjectivity1 = TextBlob(text).subjectivity
            polarity.append(polarity1)
            sentiment.append("Sentiment(polarity="+str(polarity1)+", subjectivity="+str(subjectivity1))
            subjectivity.append(subjectivity1)

        return polarity, subjectivity

    def find_sentiment_two(self, text)->list:
        sentiment = []
        tetx = ""
        for element in self.tweets_list:
            if 'retweeted_status' in element:
                try:
                    if 'extended_tweet' in element['retweeted_status']:
                        text = element['retweeted_status']['extended_tweet']['full_text']
                    else:
                        text = element['retweeted_status']['text']
                except Exception as e:
                    print(e)
            else:
                try:
                    if 'extended_tweet' in element['quoted_status']:
                        text = element['quoted_status']['extended_tweet']['full_text']
                    else:
                        text = element['quoted_status']['text']
                except:
                    # print(e)
                    text = element['text']
            sentiment1 = TextBlob(text).sentiment
            sentiment.append(sentiment1)

        return sentiment

    def find_created_time(self)->list:
        created_at = []  # Initialize empty list
        for element in self.tweets_list:
            try:
                if 'created_at' in element:
                    created_at.append(element['created_at'])

                else:
                    created_at.append(element['retweeted_status']['created_at'])
            except Exception as e:
                print(e)
                created_at.append(None)

        return created_at

    def find_source(self)->list:
        source = []
        for element in self.tweets_list:
            try:
                if 'source' in element:
                    source.append(element['source'])

                else:
                    source.append(element['retweeted_status']['source'])
            except Exception as e:
                print(e)
                source.append(None)
                
        return source

    def find_screen_name(self)->list:
        screen_name = []
        for element in self.tweets_list:
            try:
                if 'user' in element:
                    screen_name.append(element['user']['screen_name'])

                else:
                    screen_name.append(element['retweeted_status']['user']['screen_name'])

            except Exception as e:
                print(e)
                screen_name.append(None)

        return screen_name

    def find_followers_count(self)->list:
        followers_count = []
        for element in self.tweets_list:
            try:
                if 'user' in element:
                    followers_count.append(element['user']['followers_count'])

                else:
                    followers_count.append(element['retweeted_status']['user']['followers_count'])

            except Exception as e:
                print(e)
                followers_count.append(None)

        return followers_count

    def find_friends_count(self)->list:
        friends_count = []
        for element in self.tweets_list:
            try:
                if 'user' in element:
                    friends_count.append(element['user']['friends_count'])

                else:
                    friends_count.append(element['retweeted_status']['user']['friends_count'])

            except Exception as e:
                print(e)
                friends_count.append(None)
        return  friends_count


    def is_sensitive(self)->list:
        is_sensitive = []
        for element in self.tweets_list:
            # try:
            if 'retweeted_status' in element:
                try:
                    is_sensitive.append(element['retweeted_status']['possibly_sensitive'])
                except Exception as e:
                    print(e)

            else:
                is_sensit = None
                is_sensitive.append(is_sensit)

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count = []
        for element in self.tweets_list:
            try:
                if 'retweeted_status' in element:
                    favourite_count.append(element['retweeted_status']['favorite_count'])

                else:
                    favourite_count.append(element['favorite_count'])

            except Exception as e:
                print(e)
                favourite_count.append(None)

        return favourite_count
    
    def find_retweet_count(self)->list:
        retweet_count = []
        for element in self.tweets_list:
            try:
                if 'retweeted_status' in element:
                    retweet_count.append(element['retweeted_status']['retweet_count'])

                else:
                    retweet_count.append(element['retweet_count'])

            except Exception as e:
                print(e)

        return retweet_count

    def find_hashtags(self)->list:
        hashtags =[]
        text = self.find_full_text()
        for element in text:
            try:
                hashtags.append(re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', element))
            except Exception as e:
                print(e)
                hash = None
                hashtags.append(hash)

        return hashtags

    def find_lang(self)->list:
        lang = []
        for element in self.tweets_list:
            try:
                if 'lang' in element:
                    lang.append(element['lang'])

                else:
                    language = None
                    lang.append(language)
            except Exception as e:
                print(e)
                lang.append(None)

        return lang

    def find_mentions(self)->list:
        mentions = []
        for element in self.tweets_list:
            try:
                if 'retweeted_status' in element:
                    if 'extended_tweet' in element['retweeted_status']:
                        mentions.append(element['retweeted_status']['extended_tweet']['entities']['user_mentions'][0])
                    else:
                        mentions.append(element['retweeted_status']['entities']['user_mentions'][0])
                else:
                    mentions.append(element['entities']['user_mentions'][0])

            except Exception as e:
                print(e)
                mention = None
                mentions.append(mention)

        return mentions


    def find_location(self)->list:
        location = []
        for element in self.tweets_list:
            try:
                location1 = element['user']['location']
                location.append(location1)
            except TypeError:
                location1 = None
                location.append(location1)
        
        return location

    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','lang', 'sentiment','favorite_count', 'retweet_count','polarity', 'subjectivity',
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        # print(created_at)
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        sentiment = self.find_sentiment_two(text)
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
        print(">",len(polarity), len(subjectivity),len(sentiment))
        print(len(created_at),"-",len(source),"-",len(text),"-",len(lang),"-",len(fav_count),
              "-",len(retweet_count),"-",len(screen_name),"-",len(follower_count),
              "-",len(friends_count),"-",len(sensitivity),"-",len(hashtags),"-",len(mentions),"-",len(location) )
        data = zip(created_at, source, text, lang, sentiment, fav_count, retweet_count, polarity, subjectivity,  screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if True:
            try:
                df.to_csv('processed_tweet_data.csv', index=False)
                print('Data prepared and Saved in processed_tweet_data.csv File Successfully!!!')
            except Exception as e:
                print("File save Failed!", e)
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    
    tweets_length, tweet_list = read_json("data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    