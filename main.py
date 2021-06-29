import numpy as np
from numpy.lib.function_base import place
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
# from nltk.corpus import stopwords
from data import db_execute_fetch

st.set_page_config(page_title="Tweeter Sentiment Analysis", layout="wide")

def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df

def selectHashTag():
    st.title('Filter Tweets By HashTag')
    df = loadData()
    hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)
    else: # default filter
        df = df[np.isin(df, ['[]']).any(axis=1)]
        st.write(df)

def selectLocAndAuth():
    st.title('Filter Tweets By Location')
    df = loadData()
    location = st.multiselect("choose Location of tweets", list(df['place'].unique()))

    if location:
        st.title('Filter Data By Location')
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)

def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)

def wordCloud():
    df = loadData()
    cleanText = ''
    for text in df['original_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=1000, height=550, background_color='gray', max_words=100,  min_font_size=3).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())

def stBarChart():
    df = loadData()
    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['original_text'].count()}).reset_index()
    dfCount["original_author"] = dfCount["original_author"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "original_author", "Tweet_count")


def langPie():
    df = loadData()
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['lang'])['original_text'].count()}).reset_index()
    dfLangCount["lang"] = dfLangCount["lang"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
    st.title(" Tweets lang pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count', names='lang', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.beta_columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)

def placePie():
    df = loadData()
    dfPlaceCount = pd.DataFrame({'Tweet_count': df.groupby(['place'])['original_text'].count()}).reset_index()
    dfPlaceCount["place"] = dfPlaceCount["place"].astype(str)
    dfPlaceCount = dfPlaceCount.sort_values("Tweet_count", ascending=False)
    dfPlaceCount = dfPlaceCount[dfPlaceCount['place'] != '0']
    dfPlaceCount = dfPlaceCount.head(-1000)
    dfPlaceCount.loc[dfPlaceCount['Tweet_count'] < 20, 'place'] = 'Other languages'
    st.title(" Tweets Location pie chart")
    fig = px.pie(dfPlaceCount, values='Tweet_count', names='place', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.beta_columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfPlaceCount)



st.title("Twitter Data Analysis")
wordCloud()
st.markdown("<p style='padding:4px; background-color:gray;color:#00ECB9;font-size:16px;border-radius:6px;'></p>", unsafe_allow_html=True)
selectHashTag()
st.markdown("<p style='padding:4px; background-color:gray;color:#00ECB9;font-size:16px;border-radius:6px;'></p>", unsafe_allow_html=True)
selectLocAndAuth()
st.markdown("<p style='padding:4px; background-color:gray;color:#00ECB9;font-size:16px;border-radius:6px;'></p>", unsafe_allow_html=True)
st.title("Data Visualizations")
stBarChart()
st.markdown("<p style='padding:4px; background-color:gray;color:#00ECB9;font-size:16px;border-radius:6px;'></p>", unsafe_allow_html=True)
langPie()
st.markdown("<p style='padding:4px; background-color:gray;color:#00ECB9;font-size:16px;border-radius:6px;'></p>", unsafe_allow_html=True)

with st.beta_expander("Show More Graphs"): 
    placePie()
    # langPie()
