#!/usr/bin/env python
# coding: utf-8

# In[2]:


import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import STOPWORDS,WordCloud
import gensim
from gensim.models import CoherenceModel
from gensim import corpora
import pandas as pd
from pprint import pprint
import string
import os
import re


# In[3]:


#data loader class
class DataLoader:
  def __init__(self,dir_name,file_name):
    self.dir_name=dir_name
    self.file_name = file_name
    
 
  def read_csv(self):
    os.chdir(self.dir_name)
    tweets_df=pd.read_csv(self.file_name)
    return tweets_df


# In[12]:


# object creation
tweets_df=pd.read_csv(r'/home/stacy/Downloads/cleaned_fintech_data.csv')
tweets_df.head()


# In[13]:


tweets_df.dropna()


# In[14]:


len(tweets_df)


# In[25]:


class PrepareData:
    def __init__(self,df):
      self.df=df
    
    def preprocess_data(self):
      tweets_df = self.df.loc[self.df['lang'] =="en"]

    
    #text Preprocessing
      tweets_df['clean_text']=tweets_df['clean_text'].astype(str)
      tweets_df['clean_text'] = tweets_df['clean_text'].apply(lambda x: x.lower())
      tweets_df['clean_text']= tweets_df['clean_text'].apply(lambda x: x.translate(str.maketrans(' ', ' ', string.punctuation)))
    
    #Converting tweets to list of words For feature engineering
      sentence_list = [tweet for tweet in tweets_df['clean_text']]
      word_list = [sent.split() for sent in sentence_list]

    #Create dictionary which contains Id and word 
      word_to_id = corpora.Dictionary(word_list)
      corpus_1= [word_to_id.doc2bow(tweet) for tweet in word_list]



    
      return word_list, word_to_id, corpus_1


# In[26]:


PrepareData_obj=PrepareData(tweets_df)
word_list ,id2word,corpus=PrepareData_obj.preprocess_data()


# In[27]:


print(corpus)


# In[28]:


# Build LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus,
                                           id2word=id2word,
                                           num_topics=5, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)


# In[29]:


pprint(lda_model.show_topics(formatted=False))


# In[30]:


# Compute Perplexity

#It's a measure of how good the model is. The lower the better. Perplexity is a negative value
print('\nPerplexity: ', lda_model.log_perplexity(corpus))  
doc_lda = lda_model[corpus]


# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=word_list, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\n Ldamodel Coherence Score/Accuracy on Tweets: ', coherence_lda)


# In[ ]:


# Basic Ldamodel Coherence Score 0.61 This means that the model has performed reasonably well in topic modeling.


# In[31]:


import pyLDAvis.gensim_models as gensimvis
import pickle 
import pyLDAvis
# Visualize the topics
pyLDAvis.enable_notebook()

LDAvis_prepared = gensimvis.prepare(lda_model, corpus, id2word)
LDAvis_prepared


# In[ ]:




