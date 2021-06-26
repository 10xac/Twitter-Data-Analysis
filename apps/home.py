import streamlit as st
from PIL import Image
import os


def app():
    st.title('Home')

    st.write("The following is going to show the dataset on COVID 19 Tweets and a visualization of the topics mentioned in the tweets")
    #image1=Image.open("images\home_page.png")
    path = os.path.dirname(__file__)
    my_file = path + '\home_page.png'
    image1 = Image.open(my_file)
    #st.image(image1)
    st.image(image1)