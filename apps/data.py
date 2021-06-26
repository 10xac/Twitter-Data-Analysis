import streamlit as st
import numpy as np
import pandas as pd
from my_sql_connector import db_execute_fetch

def app():
    st.title('Data')

    st.write("This page shows the dataset obtained fro Twitter")

    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    st.write(df)