import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join('../sql')))

from add_data import db_execute_fetch


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


def selectLocAndAuth():
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


def app():
    st.title("Data Display")
    selectHashTag()
    st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Section Break</p>", unsafe_allow_html=True)
    selectLocAndAuth()
