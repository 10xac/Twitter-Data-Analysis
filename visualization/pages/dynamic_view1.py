import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px

try:
    sys.path.append(os.path.abspath(os.path.join('sql')))
    print(sys.path)
    from add_data import db_execute_fetch

except Exception as e:
    print(e)
    sys.exit(1)


def loadData():
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    return df


def selectHashTag():
    df = loadData()
    hashTags = st.multiselect(
        "Classify Tweets Based On Hastags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)


def selectAuthor():
    df = loadData()
    authors = st.multiselect(
        "Classify Tweets Based On Author", list(df['original_author'].unique()))
    if authors:
        df = df[np.isin(df, authors).any(axis=1)]
        st.write(df)


def selectLocAndLang():
    df = loadData()
    location = st.multiselect("Classify Tweets Based On Location", list(
        df['place'].unique()))
    lang = st.multiselect("choose Language of tweets",
                          list(df['language'].unique()))

    if location and not lang:
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    elif lang and not location:
        df = df[np.isin(df, lang).any(axis=1)]
        st.write(df)
    elif lang and location:
        location.extend(lang)
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)


def mostFollowedUsers():
    df = loadData()
    most_followers = df[['original_author', 'followers_count']].sort_values(
        by='followers_count', ascending=False)
    most_followers.reset_index(drop=True, inplace=True)
    num = st.slider("Select Max Ranking", 0, 25, 5)
    st.text("Most Followed Users: ")
    st.dataframe(most_followers[:num])


def mostLikedTweets():
    df = loadData()
    most_liked = df[['clean_text', 'original_author', 'favorite_count']].sort_values(
        by='favorite_count', ascending=False)
    most_liked.reset_index(drop=True, inplace=True)
    numMLT = st.slider("Select Max Ranking", 0, 20, 5)
    st.text("Most Liked Tweets: ")
    st.dataframe(most_liked[:numMLT])


def app():
    st.title("Data Display")
    st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Hash Tag Classifier</p>", unsafe_allow_html=True)
    selectHashTag()
    st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Author Classifier</p>", unsafe_allow_html=True)
    selectAuthor()
    st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Location and Language Multi-Classifier</p>", unsafe_allow_html=True)
    selectLocAndLang()
    st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Most Followed Identifier</p>", unsafe_allow_html=True)
    mostFollowedUsers()
    st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Most Followed Identifier</p>", unsafe_allow_html=True)
    mostLikedTweets()
