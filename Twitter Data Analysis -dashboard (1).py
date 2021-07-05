#!/usr/bin/env python
# coding: utf-8

# In[23]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import numpy as np


header=st.beta_container()
dataset=st.beta_container()
features=st.beta_container()
model_training=st.beta_container()

with header:
    st.title('TWITTER DATA ANALYSIS')
    st.markdown('This is a project that builds a system that will analyze data from twitter and present insights gained from this data this dashboard.It involves training ML models for topic modelling and sentiment analysis')    
    st.sidebar.title('Sentiment analysis')
    st.sidebar.markdown("The following is the analysis of sentiments by day and time")
    st.sidebar.subheader('Type of sentiment')


with dataset:
    data=pd.read_csv('tweets.csv',delimiter=',')
    pos_words=pd.read_csv('positive_words.csv',delimiter=',')
    neg_words=pd.read_csv('negative_words.csv',delimiter=',')
    cols=['created_at','clean_text','polarity','polarity_score']
    mselect=st.multiselect('Select columns to view',data.columns.tolist(),default=cols)
    st.dataframe(data.head())
   
    if st.checkbox("Show Dataframes"):
        st.markdown("Positive words")
        st.dataframe(pos_words.head())
        st.markdown("Negatve words")
        st.dataframe(neg_words.head())
        
st.subheader("Representation of the common words")      
select=st.selectbox('Select group of words:',['Positive words','Negative words'],key=2) 
if select=="Positive words":
    plt.figure(figsize=(20,10))
    sns.barplot(x="words", y="count",data=pos_words)
    plt.xticks(rotation=45)
    st.pyplot()
else:
    plt.figure(figsize=(20,10))
    sns.barplot(x="words", y="count",data=neg_words)
    plt.xticks(rotation=45)
    st.pyplot()   
        
tweets=st.sidebar.radio('Polarity Score ',('positive','negative'))

sentiment=data['polarity_score'].value_counts()
sentiment=pd.DataFrame({'polarity':sentiment.index,'Tweets':sentiment.values})
st.markdown("#  Sentiment Representation")
st.markdown("### This section shows the distribution of positive and negative tweets  ")
select=st.selectbox('Visualisation Of Tweets',['Histogram','Pie Chart'],key=1)
if select == "Histogram":
    fig = px.bar(sentiment, x='polarity', y='Tweets', height= 500)
    st.plotly_chart(fig)
else:
    fig = px.pie(sentiment, values='Tweets', names='polarity')
    st.plotly_chart(fig)
        
st.sidebar.markdown('Time of tweets')
hr = st.sidebar.slider("Hour of the day", 0, 23)
data['Date'] = pd.to_datetime (data['created_at'])
hr_data = data[data['Date'].dt.hour == hr]
if not st.sidebar.checkbox("Hide", True, key='2'):
        st.markdown("### Tweets based on the hour of the day")
        st.markdown("%i tweets during  %i:00 and %i:00" % (len(hr_data), hr, (hr+1)%24))
        fig1=px.bar(x=str(len(hr_data)),y=data['Date'])
        st.plotly_chart(fig1)
      
    
#polarity_score=pd.DataFrame(data['polarity_score'].value_counts()).head(50)
#st.bar_chart(polarity_score) 
#determine the positive hash tags
    
    

    

#multiselect


#word cloud    
st.title('Word cloud representation of the tweets')   
st.markdown(" The most common words are represented in a word cloud ")
def wordCloud():
    cleanText = ''
    for text in data['clean_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    #wc = WordCloud(width=1000, height=600, background_color='black', min_font_size=10).generate(cleanText)
    wc = WordCloud( background_color='white',max_words=500,max_font_size=40,width=1000, height=600,random_state=100).generate(cleanText)
    st.image(wc.to_array())
wordCloud()


st.set_option('deprecation.showPyplotGlobalUse', False)  


# In[37]:


st.set_option('deprecation.showPyplotGlobalUse', False)


# In[ ]:





# In[ ]:




