import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
from add_data import db_execute_fetch
import plotly.express as px
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from tweeter_data_explorator import TweeterDataExplorator



st.set_page_config(page_title="Tweet Data Information", layout="wide")

def wordCloud(df):
    cleanText = ''

    for text in df['clean_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white',
                   min_font_size=5).generate(cleanText)
    return wc


class Dashboard:

    def __init__(self, title: str) -> None:
        self.title = title
        self.page = None
        self.df = self.load_data()
        self.tweeterDataExplorator = TweeterDataExplorator(self.df)

    @st.cache
    def load_data(self):
        print("Data loaded")
        query = "select * from TweetInformation"
        df = db_execute_fetch(query, dbName="tweets", rdf=True)
        return df

    def barChart(self, data, X, Y):

        msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                    order='ascending')), y=f"{Y}:Q"))
        st.altair_chart(msgChart, use_container_width=True)

    def render_siderbar(self, pages, select_label):
        st.sidebar.markdown("# Pages")
        self.page = st.sidebar.selectbox(f'{select_label}', pages)

    def render_top_authors(self):
        st.markdown("### **Top authors**")

        plcae_filters = st.multiselect(
            label="Select location to include", options=self.df['place'].unique(), key="author_places")

        top = st.number_input(label="Top", step=1, value=5, key="top_authors")

        df_res = self.tweeterDataExplorator.authors(
            top=int(top), places=plcae_filters)

        st.bar_chart(data=df_res, width=0, height=0,
                     use_container_width=True)

    def render_top_hashtags(self):
        st.markdown("### **Top hashtags** ")

        plcae_filters = st.multiselect(
            label="Select location to include", options=self.df['place'].unique())

        top = st.number_input(label="Top", step=1, value=5, key="top_hashtags")
        df_res = self.tweeterDataExplorator.most_used_hash_tag(
            top=int(top), places=plcae_filters)

        st.bar_chart(data=df_res, width=0, height=0,
                     use_container_width=True)

    def render_polarity(self):
        st.markdown("### **Polarity score**")

        plcae_filters = st.multiselect(
            label="Select location to include", options=self.df['place'].unique(), key="polarity_places")
        df = self.tweeterDataExplorator.get_polarities_count(
            places=plcae_filters)

        fig = px.pie(df, values="polarity_score",
                     names="polarity_score", width=500, height=350)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig)

    def render_polarity_vs_retweet_count(self):
        chart_df = pd.DataFrame(columns=["polarity", "retweet_count"])

        chart_df['polarity'] = self.df['polarity']
        chart_df['retweet_count'] = self.df['retweet_count']

        # st.line_chart(chart_df)
        pass

    def render_visulazation(self):
        self.render_top_hashtags()
        self.render_top_authors()
        self.render_polarity()
        self.render_word_cloud()
        self.render_polarity_vs_retweet_count()

    def render_word_cloud(self):
        st.markdown("## **Tweet Text Word Cloud**")

        authors = places = polarity_score = []

        filter_mtd = st.selectbox(label="select filter method", options=[
                                  "Location", "Authors", "Polarity Score"])

        if (filter_mtd and filter_mtd == "Location"):
            places = st.multiselect(
                label="Location", options=self.df['place'].unique(), key="plcae_wc")
        if (filter_mtd and filter_mtd == "Authors"):
            authors = st.multiselect(
                label="Authors", options=self.df['original_author'].unique(), key="authros_wc")
        if (filter_mtd and filter_mtd == "Polarity Score"):
            polarity_score = st.selectbox(
                label="Polarity Score", options=["None", "Positive", "Neutral", "Negative"], key="authros_wc")

        df = self.df

        if (places and len(places) > 0):
            df = df[df['place'].apply(
                lambda x: x in places)]

        if (authors and len(authors) > 0):
            df = df[df['original_author'].apply(
                lambda x: x in authors)]

        if (polarity_score and len(polarity_score) > 0):

            if polarity_score == "Positive":
                df = df[df['polarity'].apply(
                    lambda x: x > 0)]
            elif polarity_score == "Negative":
                df = df[df['polarity'].apply(
                    lambda x: x < 0)]
            elif polarity_score == "Neutral":
                df = df[df['polarity'].apply(
                    lambda x: x == 0)]

        wc = wordCloud(df)
        st.image(wc.to_array())

    def render_data_page(self):
        location = author = hashtag = lang = polarity = user_mentions = None

        filters = st.sidebar.multiselect(
            label="Choose filter", options=["location", "lang", "hashtags", "authors", "polarity", "user_mentions"])

        column_filters = st.multiselect(
            "Choose columns to include", options=self.df.columns)

        if ("location" in filters):
            location = st.sidebar.multiselect("choose Location of tweets", list(
                self.df['place'].unique()))

        if ("lang" in filters):
            lang = st.sidebar.multiselect("choose Language of tweets",
                                          list(self.df['lang'].unique()))
        if ("user_mentions" in filters):
            user_mentions = st.sidebar.multiselect("choose user mentions of tweets",
                                                   list(self.df['user_mentions'].unique()))
        if ("hashtags" in filters):
            hashtag = st.sidebar.multiselect(
                "Hashtag", list(self.df['hashtags'].unique()))

        if ("authors" in filters):
            author = st.sidebar.text_input("Author")

        if ("polarity" in filters):
            polarity = st.sidebar.selectbox("choose polarity score",
                                            options=["None", "positive", "neutral", "negative"])

        filtered_df = self.df

        if (column_filters and len(column_filters) > 0):
            try:
                filtered_df = self.df[column_filters]
            except:
                pass

        if (location and len(location) > 0):
            try:
                filtered_df = filtered_df[filtered_df['place'].apply(
                    lambda x: x in location)]
            except:
                pass

        if (lang and len(lang) > 0):
            try:
                filtered_df = filtered_df[filtered_df['lang'].apply(
                    lambda x: x in lang)]
            except:
                pass

        if (hashtag):
            try:
                filtered_df = filtered_df[filtered_df['hashtags'].apply(
                    lambda x: x in hashtag)]
            except:
                pass

        if (user_mentions):
            try:
                filtered_df = filtered_df[filtered_df['user_mentions'].apply(
                    lambda x: x in user_mentions)]
            except:
                pass
        if (author):
            try:
                filtered_df = filtered_df[filtered_df['original_author'].apply(
                    lambda x: x.lower().find(author.lower()) != -1)]
            except:
                pass

        if (polarity):

            try:
                if polarity == "None":
                    pass
                elif polarity == "positive":
                    filtered_df = filtered_df[filtered_df['polarity'].apply(
                        lambda x: x > 0)]
                elif polarity == "negative":
                    filtered_df = filtered_df[filtered_df['polarity'].apply(
                        lambda x: x < 0)]
                else:
                    filtered_df = filtered_df[filtered_df['polarity'].apply(
                        lambda x: x == 0)]
            except:
                pass

        st.write(filtered_df)

    def render(self):
        st.title(f"Welcome To {self.title}")
        self.render_siderbar(['Data', "Data Visualizations"], "select page: ")

        if (self.page == "Data"):

            st.title("Data")
            self.render_data_page()

        elif (self.page == "Data Visualizations"):
            st.title("Data Visualizations")
            self.render_visulazation()


if __name__ == "__main__":
    dashboard = Dashboard("Tweeter Data Dashboard")
    dashboard.render()
