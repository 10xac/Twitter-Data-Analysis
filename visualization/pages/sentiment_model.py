import sys
import os
import joblib
import streamlit as st


def app():
    st.title("Sentiment Model")
    model_description = joblib.load('trained_models/trainedModelsData.jl')
    st.text("Sentiment Model:")
    st.text(
        "\t- Based on: {}".format(model_description['sentiment_analysis']['name']))
    st.text(
        "\t- Score of: {}".format(model_description['sentiment_analysis']['score']))
