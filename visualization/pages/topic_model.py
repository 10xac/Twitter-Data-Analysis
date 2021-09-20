import joblib
import streamlit as st


def app():
    st.title("Topic Model")
    model_description = joblib.load('trained_models/trainedModelsData.jl')
    st.text("Model with:")
    st.text("\t- Perplexity Score of: {}".format(
        model_description['topic_modeling']['perplexity_score']))
    st.text("\t- Coherence Score of: {}".format(
        model_description['topic_modeling']['coherence_score']))
