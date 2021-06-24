
import unittest
import centurySign

class Clean_Tweets:
    
    import pandas as pd
    #"""
    #The PEP8 Standard AMAZING!!!
    #"""
    
    
    
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
        
        
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        #"""
        #remove rows that has column names. This error originated from
        #the data collection stage.  
        #"""
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        df.drop(unwanted_rows , inplace=True)
        df = df[df['polarity'] != 'polarity']
        
        return df
    
    
    
    
    
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        #"""
        #drop duplicate rows
        #"""
        df.drop_duplicates(subset=("name of column which contains duplicate"))
        
        
        return df
    
    
    
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        #"""
        #convert column to datetime
        #"""
        df['columns'] = pd.to_datetime(df['columns'], format='%y%m%d')
        
        
        return df
    
    
    
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        #"""
        #convert columns like polarity, subjectivity, retweet_count
        #favorite_count etc to numbers
        #"""
        df['polarity'] = pd.to_numeric(df['polarity'])
        
        
        return df
    
    
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        #"""
        #remove non english tweets from lang
        #"""
        
        df = df.drop(index="non english tweets ",columns='lang')      
        return df
    
    
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df['polarity'] = pd.to_numeric(df['polarity'])
        
        
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        df = df.drop(index="non english tweets ",columns='lang')      
        return df

    
    
    
    
    
