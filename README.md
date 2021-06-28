### This folder is structred in such a way that I have cloned the original file from https://github.com/10xac/Twitter-Data-Analysis link.
After that I have implemented extract_dataframe and clean_tweet_dataframe. 
The clean_tweets_dataframe implements a class called Clean_Tweets and it implements drop unwanted column, duplicates and also convert to date time and number and also remove none_english tweets.


The TweeteDfExtractor implements a different function to get status count, get full text, get sentiment, get created time, find a source, find screen name, find followers count, find freinds count, find hash tags, find mentions, find location find lang and get tweet df.

 Up on completion of the above task I have been assigned to the second task on Task_2. found on Challenge_Day2.ipynb
 This uses cleaned_fintech_data.csv which was provided befor in the drive from the course.

 The notebook folder have Dataexploration and preprocessing.ipynb which implements extended from the extract_dataframe and clean_tweet_dataframe to perform reading, preprocessing and data exploration and visualization. And then another jyupiter file should be added to do topic modeling and sentiment analysis. 


This to to include a unit testing
Initial result of the test files added -- "case1.py" and "test_from_drive/test_case1.py"



The task_5 folder includes basically 4 files, one schema for a database created called "createDropTables.sql" which creates, deletes tables and also insert and update a value from a database called task_5. The "The day5_schema.sql" was provided. an update to the addData and dashboard.py. they will help read data from table and display it on streamlit. The webapp have two pages.  