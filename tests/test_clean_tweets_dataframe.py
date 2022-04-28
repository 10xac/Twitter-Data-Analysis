#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
import pandas as pd
class Clean_Tweets(unittest.TestCase):
    
        
    def test_drop_duplicate(self, df:pd.DataFrame):
         df = ['created_at', 'source', 'original_text','clean_text', 'clean_text','sentiment','polarity','subjectivity']
            self.assertEqual(self.df.drop_duplicates, df)
            
       
    
    def test_convert_to_datetime(self, df:pd.DataFrame):
        
       
    
    def test_convert_to_numbers(self, df:pd.DataFrame)
    def remove_non_english_tweets(self, df:pd.DataFrame)
    
    

if __name__ == '__main__':
	unittest.main()

