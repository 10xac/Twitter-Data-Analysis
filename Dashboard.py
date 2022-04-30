import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 



tweet_data = pd.read_json("Economic_Twitter_Data.json", lines = True)
tweet_data.head() 
st.set_page_config(
    page_title = 'Twitter Data Science Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title

st.title("Twitter Data / Filter By Lanuage")

# top-level filters 

job_filter = st.selectbox("Select the language", pd.unique(tweet_data['lang']))


# creating a single-element container.
placeholder = st.empty()

# dataframe filter 

df = tweet_data[tweet_data['lang']=="lang"]

# near real-time / live feed simulation 

for seconds in range(200):
#while True: 
    source = tweet_data["source"]
    tweet_data['source'] = tweet_data['source'] * np.random.choice(range(1,5))
    tweet_data['favorited'] = tweet_data['favorited'] * np.random.choice(range(1,5))

    # creating KPIs 
    favorited = np.mean(tweet_data['favorited']) 

    count_favorited = int(tweet_data[(tweet_data["favorite_count"]=='favorite_count')]['favorite_count'].count() + np.random.choice(range(1,30)))
    
    retweet= np.mean(tweet_data['retweet_count '])

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Source ⏳", value=str(source))
        kpi2.metric(label="Favorite Count ", value= int(count_favorited))
        kpi3.metric(label="Favorited ", value= int(favorited) )

        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(data_frame=tweet_data, y = 'favorited', x = 'retweet')
            st.write(fig)
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame = tweet_data, x = 'favorited')
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(tweet_data)
        time.sleep(1)
    #placeholder.empty()
