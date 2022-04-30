import pandas as pd
# pip install regex for regular expression
import re
# change our json data into dataframe
tweet_data = pd.read_json("Economic_Twitter_Data.json", lines = True)
# lets look at our data
# to get min ,max etc or summary of our data
tweet_data.describe()
#number of columns and dtypes of each column with non null count
tweet_data.info()
# first five rows
tweet_data.head()
#row and column 
tweet_data.shape # 24625 ,30
# Lets list what are our columns
tweet_data.columns # output is the following
"""
Index(['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'source',
       'in_reply_to_status_id', 'in_reply_to_status_id_str',
       'in_reply_to_user_id', 'in_reply_to_user_id_str',
       'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place',
       'contributors', 'retweeted_status', 'is_quote_status', 'retweet_count',
       'favorite_count', 'favorited', 'retweeted', 'lang', 'extended_entities',
       'possibly_sensitive', 'quoted_status_id', 'quoted_status_id_str',
       'quoted_status', 'withheld_in_countries'],
      dtype='object')
"""

#source colum
tweet_data["source"]
#tweet texts
tweet_data["text"]
# dates
tweet_data["created_at"]
#lets see id list only
tweet_data["id"]
#dtypes
tweet_data.dtypes
# wihtinhold
tweet_data["withheld_in_countries"]
# counting
tweet_data["retweet_count"].count()
#
tweet_data["withheld_in_countries"].count()
