import pandas as pd

class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        
        return df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        df.drop_duplicates(subset=None, keep='first', inplace=False)
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
    
        
        
        df = df[df['created_at'] >= '2020-12-31' ]
        
        return df
        
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric()
        
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        df = pd.DataFrame({ 'colA': ['The' ,'PEP8', 'Standard', 'AMAZING!!!']})
        
        return df
    
    #tweet_df.head()
#tweet_df.info()

#Clean the text
def clean_tweet(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

tweet_df['text'] = tweet_df['text'].apply(lambda x: clean_tweet(x))

def clean_tweet1(source):
    source  = "".join([char for char in source if char not in string.punctuation])
    source = re.sub('[0-9]+', '', source)
    return source

tweet_df['source'] = tweet_df['source'].apply(lambda x: clean_tweet1(x))

# tweet_df.drop['source']
tweet_df.head()
df= tweet_df[[ 'fav_count',
       'follower_count', 'friends_count']]
plt.subplot(3,1,1)
plt.plot(df['fav_count'],df['follower_count'])
plt.subplot(3,1,2)
plt.plot(df['friends_count'],df['follower_count'])
plt.subplot(3,1,3)
plt.plot(df['friends_count'],df['fav_count'])
plt.show()
