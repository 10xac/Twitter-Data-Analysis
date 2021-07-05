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
    def find_statuses_count(self)->list:
        for i in range(len(self.tweets_list)):
          statuses_count =self.tweets_list[i] ['user']['statuses_count']
        return statuses_count
    
    def find_full_text(self)->list:
        text=[]
        for i in range(len(self.tweets_list)):    
          text.append(i)
        return text
          

    def find_sentiments(self, text)->list:
        polarity,subjectivity=([] for x in range(2))
        for i in (self.tweets_list):
          polarity=TextBlob(i).sentiment.polarity
          subjectivity=TextBlob(i).sentiment.subjectivity     
        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at=[]
        for i in range(len(self.tweets_list)):    
          created_at.append([i])
        return created_at
          
        
    def find_source(self)->list:
        source=[]
        for i in range(len(self.tweets_list)):    
          source.append([i])
        return source

           
    
    def find_screen_name(self)->list:
        screen_name=[]
        for i in range(len(self.tweets_list)):   
          screen_name.append(i)
        return screen_name

    def find_followers_count(self)->list:
        followers_count=[]
        for i in range(len(self.tweets_list)):  
          followers_count.append(i)
        return followers_count

    def find_friends_count(self)->list:
        friends_count=[]
        for i in range(len(self.tweets_list)):
          friends_count.append(i)
        return friends_count



    def is_sensitive(self)->list:
        is_sensitive=[]
        for x in range(len(self.tweets_list)):
          is_sensitive.append(x)
     

        return is_sensitive

    def find_favourite_count(self)->list:
        favourite_count=[]
        for i in range(len(self.tweets_list)):
            favourite_count.append(i)
        return favourite_count
      
        
    
    def find_retweet_count(self)->list:
        retweet_count=[]
        for i in range(len(self.tweets_list)):
          retweet_count.append(i)
        return retweet_count

    def find_hashtags(self)->list:
        hashtags=[]
        for i in range(len(self.tweets_list)):
          hashtags.append(i)
        return hashtags
        

    def find_mentions(self)->list:
        mentions=[]
        for i in range(len(self.tweets_list)):  
          mentions.append(i)
        return mentions


    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    def find_lang(self)->list:
        lang=[]
        for i in range(len(self.tweets_list)):
          lang.append(i)
        return lang



    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at','id','id_str', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity = self.find_sentiments(text)
        subjectivity=self.find_sentiments(text)
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

        
        data =zip(created_at,source,text,lang,fav_count, retweet_count, polarity, subjectivity, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location) #created_at, source, text, polarity, subjectivity, lang,fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("../covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above
