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
    def find_created_time(self)->list:
        created_at=[]
        for items in self.tweets_list:
            #print(items)
            #break;
            created_at.append(items['created_at'])
            #print(len(created_at)) #24625
        return created_at
         
    
    def find_source(self)->list:
        source=[]
        for items in self.tweets_list:
            #print (items)
            source.append(items['source'])
           
        return source
    def find_full_text(self)->list:
        

        text = [x.get('retweeted_status', {}).get('user', {}).get('text') for x in self.tweets_list]
    
          
        return text
        '''
        if 'retweeted_status' in tweet:
    	text = tweet['retweeted_status']['text']
         else:
    	text = tweet['text']
        '''
    
    
    def find_sentiments(self, text)-> str:
        polarity = [] # contains the polarity values from the sentiment analysis.
        self.subjectivity = [] # contains the subjectivity values from the sentiment analysis.
        for items in text:
            self.subjectivity.append(TextBlob(items).sentiment.subjectivity)
            polarity.append(TextBlob(items).sentiment.polarity)
         
        return polarity, self.subjectivity
    
    def find_lang(self)->list:
        lang=[]
        for items in self.tweets_list:
            lang.append(items['lang'])
          
        return lang
    
    def find_favourite_count(self)->list:
        favorites_count=[]
        for items in self.tweets_list:
            favorites_count.append(items['favorite_count'])
           
        return favorites_count
    
    def find_retweet_count(self)->list:
        retweet_count=[]
        for items in self.tweets_list:
            retweet_count.append(items['retweet_count'])
        
        return retweet_count
    
    def find_screen_name(self)->list:
        screen_name=[]
        for items in self.tweets_list:
            screen_name.append(items['user']['screen_name'])
            
        return screen_name
    
    def find_followers_count(self)->list:
        followers_count=[]
        for items in self.tweets_list:
            followers_count.append(items['user']['followers_count'])
         
        return followers_count

    def find_friends_count(self)->list:
        friends_count=[]
        for items in self.tweets_list:
            friends_count.append(items['user']['friends_count'])
            
        return friends_count

  
    def find_location(self)->list:
        """
        a function that extracts the location.
        returns list of locations
        """
        location = [x.get('retweeted_status', {}).get('user', {}).get('location', None) for x in self.tweets_list]
        return location
    
    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = ''
          

        return is_sensitive
    
    def find_hashtags(self)->list:
        hashtags = []
        for items in self.tweets_list:
            hashtags.append(items['entities']['hashtags'])
        return hashtags
    def find_mentions(self)->list:
        mentions=[ ]
        for items in self.tweets_list:
            mentions.append(items['entities']['user_mentions'])
        return mentions
    
    
    def find_statuses_count(self)->list:
        status_count
        status_count = self.tweets_list["status_count"]
        return status_count


    
    def get_tweet_df (self, save=True)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        '''columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']'''
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count', 'hashtags', 'user_mentions','place']
        
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
        
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count,
                        friends_count, hashtags, mentions,location)
      
        #this creates a list of tuples
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
            
        
        return df
    
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count',                   'retweet_count','original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags',                          'user_mentions', 'place', 'place_coord_boundaries']
    tweet_list = read_json("C:/Users/kachase/Desktop/task_one/Twitter-Data-Analysis/data/Economic_Twitter_Data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above

                


    
