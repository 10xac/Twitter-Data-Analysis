# Twitter-Data-Analysis

### Dataset
- The dataset used is the clean_tweet.csv file in the data folder.

### processing the data
1. Created a dataframe from the clean_tweet.csv
2. Created a function text_category that takes a value polarity and returns, depending on the value of polarity, a string 'positive', 'negative' or 'neutral'. The polarity >0 is positive, polarity < 0 is negative and polarity = 0 is neutral
3. Constructed a column  scoremap that mapped {'positive':1, 'negative':0} on the score column
4. Splittting the dataset into testing and training data
5. Built an SGDClassifier model from the vectorize train text data. Used CountVectorizer() with a  trigram  parameter.
7. Evaluate the model on the test data with the accuracy_score.

Have Fun and Cheers
