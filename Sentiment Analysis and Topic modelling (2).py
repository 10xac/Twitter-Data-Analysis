#!/usr/bin/env python
# coding: utf-8

# In[3]:


import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import STOPWORDS,WordCloud
import gensim
from gensim.models import CoherenceModel
from gensim.parsing.preprocessing import remove_stopwords
from gensim import corpora

import html
import warnings 
from textblob import TextBlob
warnings.filterwarnings("ignore", category=DeprecationWarning)

get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:



df=pd.read_json('covid19.json', lines=True)
df.head()


# In[ ]:





# In[5]:


tweets_df=df[['created_at', 'id','text','source','possibly_sensitive']].copy()
tweets_df.head()


# In[6]:


#extracting mentions
def extract_mentions(x):
    regex="@(\w+)"
    mentions=re.findall(regex,x)
    return mentions
tweets_df['user_mentions']=tweets_df['text'].apply(extract_mentions)

#extract hashtags
def extract_hash(x):
    regex="#(\w+)"
    hashtag=re.findall(regex,x)
    return hashtag
tweets_df['hashtags']=tweets_df['text'].apply(extract_hash)



# In[7]:


tweets_df.head()


# In[8]:


def hash_removed(text):
    return re.sub("#[a-zA-Z0-9_]+" , "",text)

def mentions_removed(text):
    return re.sub("@[a-zA-Z0-9_]+" , "",text)

def url_removal(text):
    return re.sub(r'http\S+','',text)

#remove punctuation
def punct_removed(text):
    return re.sub(r'[^a-zA-Z]',' ',text)

#convert to lowercase
def lowercase(text):
    return str(text).lower()

#tokenization
def token_text(text):
    return word_tokenize(text)

#remove stopwords
stop_words=set(stopwords.words('english'))
def sw_removed(text):
    return [item for item in text if item not in stop_words]

#remove words with less than 3 characters
def less_char(text):
    return [x for x in text if len(x)>3]

#convert back to string
def convert_str(text):
    return ' '.join(text)


tweets_df['clean_text']=tweets_df['text'].apply(hash_removed).apply(mentions_removed).apply(url_removal).apply(punct_removed).apply(lowercase).apply(token_text).apply(sw_removed).apply(less_char).apply(convert_str)

tweets_df.head()


# In[9]:


#sentiment score, first value is the polarity score and second value is the subjectivity score
def sentiment(x):
    return TextBlob(x).sentiment

tweets_df['sentiment_score'] =tweets_df['clean_text'].apply(sentiment)

tweets_df.head()


# In[10]:


#polarity
def polarity(x):
    return TextBlob(x).sentiment.polarity  

tweets_df['polarity'] = tweets_df['clean_text'].apply(polarity)

#subjectivity
def subjectivity(x):
    return TextBlob(x).sentiment.subjectivity 

tweets_df['subjectivity'] = tweets_df['clean_text'].apply(subjectivity)

tweets_df.head()


# In[11]:


def text_category(p):
  if p>0.0 and p<=1.0:
    return 'positive'
  elif p>=-1.0 and p<0.0:
    return 'negative'
  
  else:
     return 'neutral'

  return p

tweets_df.info()

tweets_df['polarity_score']=tweets_df['polarity'].apply(text_category)
tweets_df.head()


# In[12]:


tweets_df['scoremap']=tweets_df['polarity_score'].map({'positive':1, 'negative':0})
tweets_df.head()


# In[13]:


#visualization using pie chart and bar chart
#pie chart
data=tweets_df.groupby(['polarity_score']).size()
data.plot(kind='pie')


# In[14]:


#bar chart
data=tweets_df.groupby(['polarity_score']).size()
data.plot(kind='bar')


# In[15]:


#dropping the neutral column

tweets_df.drop(tweets_df[tweets_df['polarity_score'] =='neutral'].index, inplace = True)

tweets_df=tweets_df.reset_index(drop=True)
tweets_df.head()

data=tweets_df.groupby(['polarity_score']).size()
data.plot(kind='bar')


# In[16]:


#visualization using word cloud(general)
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
plt.rcParams['figure.figsize']=(12.0,12.0)  
plt.rcParams['font.size']=12            
plt.rcParams['savefig.dpi']=100             
plt.rcParams['figure.subplot.bottom']=.1 
stopwords = set(STOPWORDS)
wordcloud = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=500,
                          max_font_size=40, 
                          random_state=100
                         ).generate(str(tweets_df['clean_text']))
print(wordcloud)
fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show();


# In[17]:


pos_tweet=tweets_df[tweets_df['polarity_score']=='positive']['clean_text']
neg_tweet=tweets_df[tweets_df['polarity_score']=='negative']['clean_text']

pos_tweet_ls=pos_tweet.tolist()
neg_tweet_ls=neg_tweet.tolist()


# In[18]:


pos_token=[token for line in pos_tweet_ls for token in line.split()]
neg_token=[token for line in neg_tweet_ls for token in line.split()]


# In[33]:


#count of most positive and negative words
from collections import Counter

def common_words(text, num=30):
    tokens=Counter(text)
    most_common=tokens.most_common(num)
    result=dict(most_common)
    return result


common_pos_words=common_words(pos_token)
common_neg_words=common_words(neg_token)
neg_word_df=pd.DataFrame(common_neg_words.items(),columns=['words','count'])
#neg_word_df.to_csv('negative_words.csv')
pos_word_df=pd.DataFrame(common_pos_words.items(),columns=['words','count'])
#pos_word_df.to_csv('positive_words.csv')

plt.figure(figsize=(20,10))
sns.barplot(x='words',y='count', data=pos_word_df)
plt.xticks(rotation=45)
plt.show()


# In[20]:


X=tweets_df['clean_text']
y=tweets_df['scoremap']


# In[21]:


from sklearn.feature_extraction.text import CountVectorizer
# Fit the CountVectorizer to the training data
vect = CountVectorizer(max_df=0.90,min_df=2, max_features=100)
vectorizer=vect.fit_transform(X)


# In[22]:


from sklearn.model_selection import train_test_split
# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(vectorizer, y, random_state=0, test_size=0.25)


# In[23]:


from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)

from sklearn.metrics import f1_score , accuracy_score
predictions=model.predict(X_test)
f1_score=(y_test,predictions)


# In[24]:


accuracy_score(y_test,predictions)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




