# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# <h1>Data Analysis of Twitter Data<h1>
# %% [markdown]
# <h3>Collecting Data</h3>
# %% [markdown]
# Importing the Processed Tweet Data that was done through extract_datafram.py script

# %%
from clean_tweets_dataframe import Clean_Tweets
import os
import sys
import inspect
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import STOPWORDS, WordCloud
from gensim import corpora
import numpy as np
import string

processed_tweets = pd.read_csv('../data/processed_tweet_data.csv')
processed_tweets.head()

# %% [markdown]
# <h3>Exploring the Data</h3>
#
# *   Find what columns we have
# *   Find how many data we have
# *   Find out what type of data there is in each column
# *   Check for missing values

# %%
processed_tweets.columns


# %%
processed_tweets.info()


# %%
processed_tweets.shape

# %% [markdown]
# Check for missing values

# %%
print("The number of missing value(s) based on columns:\n{}".format(
    processed_tweets.isnull().sum()))
print("The number of missing value(s): {}".format(
    processed_tweets.isnull().sum().sum()))
print("Columns having missing value(s):{}".format(
    processed_tweets.columns[processed_tweets.isnull().any()]))

# %% [markdown]
# <h3>Data Preparation </h3>
#
# *   Making correction
# *   Reformatting
# *   Combining Dataset

# %%
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# %%

# %% [markdown]
# Chossing what which data is neccessary for our model

# %%
tweets_df = pd.DataFrame(
    columns=['original_text', 'sentiment', 'lang', 'hashtags'])

tweets_df['original_text'] = processed_tweets['original_text'].to_list()
tweets_df['sentiment'] = processed_tweets['sentiment'].to_list()
tweets_df['lang'] = processed_tweets['lang'].to_list()
tweets_df['hashtags'] = processed_tweets['hashtags'].to_list()

tweets_df.head()


# %%
tweet_cleaner = Clean_Tweets()
tweet_cleaner.add_clean_text(tweets_df)
tweets_df


# %%
tweets_df = tweets_df.fillna("")
tweets_df


# %%
tweets_df = tweet_cleaner.remove_non_english_tweets(tweets_df)
tweets_df


# %%
tweets_df.sentiment.value_counts().plot(kind='pie')


# %%
tweets_df['clean_text'] = tweets_df['clean_text'].astype(str)
tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: x.lower())
tweets_df['clean_text'] = tweets_df['clean_text'].apply(
    lambda x: x.translate(str.maketrans(' ', ' ', string.punctuation)))
tweets_df['sentiment'] = tweets_df['sentiment'].astype(int)
tweets_df['hashtags'] = tweets_df['hashtags'].astype(str)
tweets_df['hashtags'] = tweets_df['hashtags'].apply(lambda x: x.lower())
tweets_df['hashtags'] = tweets_df['hashtags'].apply(
    lambda x: x.translate(str.maketrans(' ', ' ', string.punctuation)))


# %%
flattened_words_df = pd.DataFrame(
    [word for words_list in tweets_df.clean_text
     for word in words_list.split(' ')],
    columns=['word'])

flattened_words_df


# %%
flattened_words_df.word.value_counts()[:20].plot(kind='bar')


# %%
flattened_hashtags_df = pd.DataFrame(
    [hashtag for hashtags_list in tweets_df.hashtags
     for hashtag in hashtags_list.split(',')],
    columns=['hashtag'])

flattened_hashtags_df.drop(
    flattened_hashtags_df[flattened_hashtags_df['hashtag'] == ""].index, inplace=True)
flattened_hashtags_df.reset_index(drop=True, inplace=True)
flattened_hashtags_df


# %%
flattened_hashtags_df.hashtag.value_counts()[:20].plot(kind='bar')


# %%
plt.figure(figsize=(20, 10))
plt.imshow(WordCloud(width=1000, height=600, stopwords=STOPWORDS).generate(
    ' '.join(tweets_df.clean_text.values)))
plt.axis('off')
plt.title('Most Frequent Words In Our Tweets', fontsize=16)
plt.show()


# %%
tweets_df = tweets_df.drop(['original_text'], axis=1)
tweets_df


# %%
tweets_df.to_csv('../data/model_ready_data.csv', index=False)
print('Model Ready Data Successfully Saved.!!!')
