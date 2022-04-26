import json
from numpy import ndarray
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
    def find_statuses_count(self)->list:
        statuses_count = [x['user']['statuses_count']
                          for x in self.tweets_list]

        return statuses_count 
        
    def find_full_text(self)->list:
        text = []
        for x in self.tweets_list:
            try:
                text.append(x['retweeted_status']
                            ['extended_tweet']['full_text'])
            except KeyError:
                text.append(x['text'])
        return text     
    
    def find_sentiments(self, text)->list:
        polarity = [TextBlob(x).polarity for x in text]
        subjectivity = [TextBlob(x).subjectivity for x in text]
        return (polarity, subjectivity)

    def find_created_time(self)->list:
        created_at = [x['created_at'] for x in self.tweets_list]
        return created_at

    def find_source(self)->list:
        source = [x['source'] for x in self.tweets_list]
        return source

    def find_screen_name(self)->list:
        screen_name = [x['user']['screen_name'] for x in self.tweets_list]
        return screen_name

    def find_followers_count(self)->list:
        followers_count = [x['user']['followers_count'] for x in 
                                                        self.tweets_list]
        return followers_count

    def find_friends_count(self)->list:
        friends_count = [x['user']['friends_count'] for x in 
                                                        self.tweets_list]
        return friends_count

    def is_sensitive(self)->list:
        is_sensitive = []
        for tweet in self.tweets_list:
            if 'possibly_sensitive' in tweet.keys():
                is_sensitive.append(tweet['possibly_sensitive'])
            else: is_sensitive.append(None)
    
        return is_sensitive

    def find_favorite_count(self)->list:
        favorite_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                favorite_count.append(
                                tweet['retweeted_status']['favorite_count'])
            else: favorite_count.append(0)
    
        return favorite_count
    
    def find_retweet_count(self)->list:
        retweet_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(
                                tweet['retweeted_status']['retweet_count'])
            else: retweet_count.append(0)
    
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = [x['entities']['hashtags'] for x in self.tweets_list]
        return hashtags

    def find_mentions(self)->list:
        mentions = [x['entities']['user_mentions'] for x in self.tweets_list]
        return mentions

    def find_location(self)->list:
        location = [x.get('user', {}).get('location', None) for x in 
                                                            self.tweets_list]
        return location
        
    def find_lang(self)->list:
        lang = [x['lang'] for x in self.tweets_list]
        return lang

    def get_tweet_df(self, save=False)->pd.DataFrame:
        """
        required column to be generated you should be creative
        and add more features
        """
        column_Names = ['statuses_count', 'created_at', 'source', 
        'original_text', 'polarity','subjectivity', 'favorite_count',
        'retweet_count', 'screen_name', 'followers_count', 'friends_count',
        'possibly_sensitive', 'hashtags', 'user_mentions', 'location',
        'language']

        statuses_count = self.find_statuses_count()
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        fav_count = self.find_favorite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        followers_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        lang = self.find_lang()

        total_data = zip(statuses_count, created_at, source, text, polarity,
         subjectivity, fav_count, retweet_count, screen_name, 
         followers_count, friends_count, sensitivity, hashtags, mentions,
         location, lang)

        """"
        SECTION USED FOR DEBUGGING
        total_d = ndarray(total_data)
        print(f"Total_data_data type: {type(total_data)}, 
                Cols dat type: {type(column_Names)}, 
                total_d data type: {total_d}")
        length of the columns to insure data is returned to us from
        all the methods defined above
        print(f"{len(statuses_count)}, {len(created_at)}, {len(source)},
               {len(text)}, {len(polarity)}, {len(subjectivity)}, 
               {len(fav_count)}, {len(retweet_count)}, {len(screen_name)},
               {len(followers_count)}, {len(friends_count)},
               {len(sensitivity)}, {len(hashtags)}, {len(mentions)},
               {len(location)}, {len(lang)}")
        length  of the columns to insure data is returned to us from all
        the methods defined above [They are all lists]
        print(f"{type(statuses_count)}, {type(created_at)}, {type(source)},
                {type(text)}, {type(polarity)}, {type(subjectivity)},
                {type(fav_count)}, {type(retweet_count)}, {type(screen_name)},
                {type(followers_count)}, {type(friends_count)},
                {type(sensitivity)}, {type(hashtags)}, {type(mentions)},
                {type(location)}, {type(lang)}")
        SECTION USED FOR DEBUGGING
        """

        """
        mold the returned data and the columns defined above into
        a pandas dataframe
        """
        final_df = pd.DataFrame(data=total_data, columns=column_Names)

        # save to csv file and output success message
        if save:
            final_df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        # return the pandas dataframe
        return final_df

if __name__ == "__main__":
    """
    required column to be generated you should be creative and
    add more features
    """
    columns = ['created_at', 'source', 'original_text','clean_text',
             'sentiment','polarity', 'subjectivity', 'lang',
             'favorite_count', 'retweet_count', 'original_author',
             'screen_count', 'followers_count','friends_count',
             'possibly_sensitive', 'hashtags', 'user_mentions',
             'place', 'place_coord_boundaries']

    # read the json file into a list
    len_of_data, tweet_list = read_json("data/Economic_Twitter_Data.json")

    # crete a TweetDfExtractor object
    tweet = TweetDfExtractor(tweet_list)
    
    # to make sure all the data is passe to he 
    print(f"Total number of data: {len_of_data}")
    
    """
    use a method that  calls all defined functions to generate a dataframe
    with the specified columns above
    """
    tweet_df = tweet.get_tweet_df(True)
