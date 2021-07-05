#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mysql.connector
from mysql.connector import Error
import pandas as pd


# In[21]:


def server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=" "
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
        
        
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
        
create_table= """"       
CREATE TABLE  TweetInformation
(
    id INT NOT NULL AUTO_INCREMENT,
    created_at TEXT NOT NULL,
    source VARCHAR(200) NOT NULL,
    clean_text TEXT DEFAULT NULL,
    polarity FLOAT DEFAULT NULL,
    subjectivity FLOAT DEFAULT NULL,
    language TEXT DEFAULT NULL,
    favorite_count INT DEFAULT NULL,
    retweet_count INT DEFAULT NULL,
    original_author TEXT DEFAULT NULL,
    screen_count INT NOT NULL,
    followers_count INT DEFAULT NULL,
    friends_count INT DEFAULT NULL,
    hashtags TEXT DEFAULT NULL,
    user_mentions TEXT DEFAULT NULL,
    place TEXT DEFAULT NULL,
    place_coordinate VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY (id)
);
""" 


def insert_data():
    cursor = connection.cursor()
    df=pd.read_csv('tweets.csv',delimiter=',')
    
    for i,row in df.iterrows(): 
        sql = f"""INSERT INTO TwitterInformation (created_at, source, clean_text, polarity, subjectivity, language,
                    favorite_count, retweet_count, original_author, screen_count, followers_count, friends_count,
                    hashtags, user_mentions, place, place_coordinate)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        try:
            cursor.execute(query)
            connection.commit()
            print("Record inserted:")
        except Error as err:
            print(f"Error: '{err}'")
        
      
     

 
connection = server_connection("localhost", "root", "doro19997")
create_database_query="CREATE DATABASE twitterdb"
create_database=create_database(connection,create_database_query)
execute_query(connection, create_table) 


# In[7]:





# In[8]:





# In[ ]:




