import pandas as pd
import re

tweet_data = pd.read_json("Economic_Twitter_Data.json", lines = True)
#first five rows
tweet_data.head() 
#last five rows
tweet_data.tail()
#column and type info
tweet_data.info()
# short summary of our data in each columns
tweet_data.describe()
#shape of our data
tweet_data.shape
#define function to remove tags
def remove_tags(string):
    removed_tag = re.sub(r'<.*>','', string)
    return removed_tag

columns = ['created_at','id','id_str','text','truncated','entities','source','in_reply_to_status_id',
           'in_reply_to_status_id_str','in_reply_to_user_id','in_reply_to_user_id_str','in_reply_to_screen_name',
           'user','geo','coordinates','place','contributors','retweeted_status','is_quote_status','retweet_count',
           'favorite_count','favorited','retweeted','lang','extended_entities','possibly_sensitive','quoted_status_id',
           'quoted_status_id_str','quoted_status','withheld_in_countries']
# call
def apply_columns(df,columns):
    for colm in columns:
        df[colm] = df[colm].apply(lambda x: remove_tags(x))
apply_columns(tweet_data,columns)

# give row number to be shown
pd.set_option('display.max_rows',100)
print(tweet_data)
# drop rows with non value
tweet_data.dropna(axis=0, inplace = True)
# source column of our data frame
tweet_data["source"]
tweet_data["text"]
tweet_data["created_at"]

# remove characte
def remove_characters(df,columns):
    for colm in columns:
        df[colm]= df[colm].str.replace('\[.*]', '' , regex = True)
        
        df[colm]= df[colm].str.replace(',', '' , regex = True)
        
        df[colm]= df[colm].str.replace('-', '' , regex = True)

remove_characters(tweet_data,columns)

def toNumeric(df,columns):
    for colm in columns:
        df[colm]= pd.to_numeric(df[colm])

toNumeric(tweet_data, columns)
# now lets check data type
tweet_data.dtypes
# fetch numberical data
tweet_data["retweet_count"].count()
# 8
tweet_data["withheld_in_countries"].count()
#source count
tweet_data["favorited"].count()

# Lets remove duplicate column

duplicate_cols = tweet_data.columns[tweet_data.columns.duplicated()]
tweet_data.drop(columns=duplicate_cols, inplace=True)
# null values 
tweet_data.isnull().sum()

#fill missing columns
in_reply_to_status_id = tweet_data["in_reply_to_status_id"]
# fill with my own string
in_reply_to_status_id.fillna("No reply to this status id")
#storing data o
in_reply_to_status_id_str = tweet_data["in_reply_to_status_id_str"]
# fill with text
in_reply_to_status_id.fillna("No reply to this status id string")
#user _id
in_reply_to_user_id = tweet_data["in_reply_to_user_id"]
#filna
in_reply_to_user_id.fillna("No reply to this User id")
# 
in_reply_to_user_id_str = tweet_data["in_reply_to_user_id_str"]
#Replace non values in user_id_str with This string user id has no reply
in_reply_to_user_id_str.fillna("This string user id has no reply")

#replace of column geo by geography
geography = tweet_data["geo"]
#
geography.isnull().sum()

# now lets remove contributors since it contains nothing
Contributors = tweet_data["contributors"]
#this is need to be removed
tweet_data["contributors"].describe()

"""count    0.0
mean     NaN
std      NaN
min      NaN
25%      NaN
50%      NaN
75%      NaN
max      NaN
Name: contributors, dtype: float64
This showw it has to be dropped
"""
# droping contibutors

tweet_data.drop(labels='contributors', axis=1)
# now lets check our data
tweet_data.columns

