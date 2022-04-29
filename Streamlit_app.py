# Modules importation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re
from wordcloud import STOPWORDS,WordCloud

from extract_dataframe import TweetDfExtractor
from extract_dataframe import read_json
from clean_tweets_dataframe import Clean_Tweets
import streamlit as st

# Importation of the CSV file
tweet_df = pd.read_csv("clean_preprocessed.csv")

st.title("Tweeter Data Analysis Challenge")
st.write('''The aim of this challenge is to analyze data from Twitter to extract any insightful information. 
    The main objective is to understand and/or have a view on the opinions of Internet users regarding economic difficulties.''')
st.markdown("**The cleaned data set**")
st.write(tweet_df.head())

# Descriptive statistics
st.subheader("Descriptive statistics")
st.write(tweet_df.describe())
st.markdown('''The polarity average and median respectively equal to  0.08≈0.1  and  0.0  mean that most of the tweets are neutral.

"Subjectivity quantifies the amount of personal opinion and factual information contained in the text. The higher subjectivity means 
that the text contains personal opinion rather than factual information" (Medium). As we found an average and median values equal to 0.31  and  0.27  that are less than  0.5 , we can conclude that the majority of the tweets are based on factual information.

We can then rely on them – tweets – to understand or to have an overview of the economic hardships people are facing and tweeting about.
''')

# Define the functions for text pre-processing
## Remove numerical character
def remov_num(tweet):
    '''Remove the numerical character from the text of each tweet'''
    import re
    return re.sub(r'[0-9]+', '', tweet)

## Standardize the formatting
def stand_format(tweet):
    '''Standardize the formatting'''
    tweet = tweet.astype(str)
    return tweet.apply(lambda x: x.lower())

## Remove https
def remov_https(tweet):
    import re
    return re.sub('https','',tweet)

# Get the list of hashtags for each tweet
def extract_hashtags(tweet):
    '''Extract the hashtags from the tweet'''
    return re.findall(r'\B#\w*[a-zA-Z]+\w*', tweet)

# Extract the hashtags for the tweets
tweet_df["hashtags"] = tweet_df["original_text"].apply(extract_hashtags)

# Get each hastags from the list
hashtags_list = tweet_df["hashtags"].explode()
# Standardize formatting for the list of hashtags (can use lower case or upper case)
hashtags_list = stand_format(hashtags_list.dropna())
# Count the values of each hashtags
hashcount = hashtags_list.value_counts()

# lot the occurences of each hashtag
st.markdown("**Most used hashtags**")
fig = px.bar(hashcount,x=hashcount.index[:10],y=hashcount.values[:10],labels={'x':'Hashtag','y':'# of occurence'},
    title="Most used hashtag")
st.plotly_chart(fig)

# Word cloud
st.markdown("**Current words in the tweets**")
plt.figure(figsize=(20, 10))
plt.imshow(WordCloud(width=1000,height=600,stopwords=STOPWORDS,max_words=50,background_color="white").generate(' '.join(tweet_df.preproc_text .values)))
plt.axis('off')
plt.title('Most Frequent Words In Our Tweets',fontsize=16)
#plt.show()
st.pyplot(plt)