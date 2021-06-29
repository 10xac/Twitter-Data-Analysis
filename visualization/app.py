import streamlit as st
from multiapp import MultiApp
# import your app modules here
from pages import analysis, dynamic_view1, dynamic_view2, sentiment_model, topic_model

st.set_page_config(page_title="Twitter Analysis Visualization", layout="wide")

app = MultiApp()


st.sidebar.markdown("""
# Multi-Page App
This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
# Modifications
\t- Page Folder Based Access
\t- Presentation changed to SideBar
""")

# Add all your application here
app.add_app("Analysis", analysis.app)
app.add_app("Dynamic Analysis 1", dynamic_view1.app)
app.add_app("Dynamic Analysis 2", dynamic_view2.app)
app.add_app("Sentiment Model", sentiment_model.app)
app.add_app("Topic Model", topic_model.app)
# The main app
app.run()
