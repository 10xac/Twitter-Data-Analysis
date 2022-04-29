import streamlit as st
import pandas as pd
import mysql.connector as mysql
import plotly.express as px
import seaborn as sns
from clean_tweets_dataframe import CleanTweets
import pandas.io.sql as sqlio
import re

st.set_page_config(page_title="Tweets Analysis Dashboard",
                   page_icon=":bar_chart:", layout="wide")
st.markdown("##")
st.markdown("<h1 style='text-align: center; color: grey;'>Tweets Analysis Dashboard</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: white;'> by Faith Bagire </h3>", unsafe_allow_html=True)


conn = mysql.connect(host='localhost', user='root', password='my_pass', database='tweets', buffered=True)
cursor = conn.cursor()

query = '''SELECT * FROM tweetinformation'''
df_tweet = data = sqlio.read_sql_query(query, conn)

# Data Preparation and Filtering
cleaner = CleanTweets(df_tweet)
df_tweet = cleaner.drop_unwanted_column(df_tweet)
df_tweet = cleaner.drop_duplicate(df_tweet)
df_tweet = cleaner.convert_to_datetime(df_tweet)
df_tweet = cleaner.convert_to_numbers(df_tweet)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

lang = st.sidebar.multiselect(
    "Select the language:",
    options=df_tweet["language"].unique(),
    default=['en', 'de', 'fr', 'es']
)

df_selection = df_tweet.query("language ==@lang")

# ---- MAINPAGE ----
st.markdown("##")

# Sentiment Analysis Summary

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Polarity and Subjectivity Over time:")
with middle_column:
    st.subheader("Top 10 Hashtags by language (default: english)")
with right_column:
    st.subheader("Sentiment class distribution:")
st.markdown("""---""")

text_grouped = df_tweet.groupby('sentiment').count()['cleaned_text'].reset_index()
sns.countplot(x='sentiment', data=df_tweet)

fig_product_sales = px.bar(text_grouped, x="sentiment", y="cleaned_text", orientation="v",
                           template="plotly_white", width=500, height=500
                           )
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)))

# sentiment summary
df_tweet_date = df_tweet.set_index('created_at')
df_tweet_date = df_tweet_date.resample('D').mean()[['polarity', 'subjectivity']].dropna()

# sentiment average per day
sent_over_time = px.line(df_tweet_date, x=df_tweet_date.index, y=['polarity', 'subjectivity'], width=500, height=500)

# Top 10 Hashtags by language (default: english)

hashtag_df = df_selection[['original_text', 'hashtags']]


def find_hashtags(df_selection):
    '''This function will extract hashtags'''
    return re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', df_selection)


hashtag_df['hashtag_check'] = df_tweet.original_text.apply(find_hashtags)

hashtag_df.dropna(subset=['hashtags', 'hashtag_check'], inplace=True)
tags_list = list(hashtag_df['hashtag_check'])
hashtags_list_df = pd.DataFrame([tag for tags_row in tags_list for tag in tags_row], columns=['hashtag'])
hashtags_list_df['hashtag'] = hashtags_list_df['hashtag'].str.lower()

hash_plotdf = pd.DataFrame(hashtags_list_df.value_counts()[:10]).reset_index()
hashtags_top = px.line(hash_plotdf, x='hashtag', y=0, width=500, height=500)


left_column, middle_column, right_column = st.columns(3)
left_column.plotly_chart(sent_over_time, use_container_width=True)
middle_column.plotly_chart(hashtags_top, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown("---")

st.caption("Source Data")
st.dataframe(df_selection)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
