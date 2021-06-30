# Twitter-Data-Analysis


### So here are the bare minimum requirement for completing task 1

## Dataset
   -------
- The dataset used is the covid.json file in the data folder.

## Tasks
   -----

1. Fork repository to your github account
2. Create a branch called “fix_bug” to fix the bugs in the fix_clean_tweets_dataframe.py and fix_extract_dataframe.py 
3. In branch `fix_bug` copy or rename `fix_clean_tweets_dataframe.py` to `clean_tweets_dataframe.py` and `fix_extract_dataframe.py`  to `extract_dataframe.py` 
4. Fix the bugs on `clean_tweets_dataframe.py` and `extract_dataframe.py` 
5. Multiple times push the code you are working on to git, and once the fix is complete, merge the `fix_bug` branch to master
6. Create a new branch called `make_unittest` for creating a new unit test for extract_dataframe.py code.
7. After completing the unit test writing, merge  “make_unittest”  to main branch
8. In all cases when you merge, make sure you first do Pull Request, review, then accept the merge.
9. Setup Travis CI to your repository such that when you git push new code (or merge a branch) to the main branch, the 

### Processing the data (This step is implemented in the Notebooks Folder)

## Dataset
## -------
- The dataset used is the clean_tweet.csv file in the data folder.

## Tasks
   -----

1. Created a dataframe from the clean_tweet.csv
2. Created a function text_category that takes a value polarity and returns, depending on the value of polarity, a string 'positive', 'negative' or 'neutral'. The polarity >0 is positive, polarity < 0 is negative and polarity = 0 is neutral
3. Constructed a column  scoremap that mapped {'positive':1, 'negative':0} on the score column
4. Splittting the dataset into testing and training data
5. Built an SGDClassifier model from the vectorize train text data. Used CountVectorizer() with a  trigram  parameter.
7. Evaluate the model on the test data with the accuracy_score.

### Data Exploration and modelling(This step is implemented in the Modelling_and_sentiment_analysis Folder)

## Dataset
## -------
- The dataset used is the clean_tweet.csv file in the data folder.

## Tasks
   ----

1. Performed data preprocessing on the clean_tweet.csv:
   -   Contractions by removing the shortcuts in the text and automatically generating the proper formatting. for e.g: replacing I've with I have 
   - I'm applying lemmatization to tranform a conjugated verb into it's present verb and 
    later on specifying each word/tag as noun, adverb, adjective or noun (wordnet formatting) 
4. Performed data visualization to examine the correlation among features
5. Used the LatentDirichletAllocation for tweets modelling.

