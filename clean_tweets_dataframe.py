import pandas as pd
class Clean_Tweets:
	"""
	The PEP8 Standard AMAZING!!!
	"""
	def __init__(self, df:pd.DataFrame):
		self.df = df
		print('Automation in Action...!!!')
		
	def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
		"""
		remove rows that has column names. This error originated from
		the data collection stage.  
		"""
		unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
		df.drop(unwanted_rows , inplace=True)
		df = df[df['polarity'] != 'polarity']
		return df

	def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
		"""
		drop duplicate rows
		"""
		df = df.drop_duplicates().drop_duplicates(subset='original_text')

		return df

	def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
		"""
		convert column to datetime
		"""
		# ----
		
		# ----
		
		df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
		df = df[df['created_at'] >= '2020-12-31' ]
		return df

	def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
		"""
		convert columns like polarity, subjectivity, retweet_count
		favorite_count etc to numbers
		"""
		# df['polarity'] = pd.----
		
		# ----
		# ----
		df['polarity'] = pd.to_numeric(df['polarity'], errors='coerce')
		df['retweet_count'] = pd.to_numeric(df['retweet_count'], errors='coerce')
		df['favorite_count'] = pd.to_numeric(df['favorite_count'], errors='coerce')

		return df
	
	def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
		"""
		remove non english tweets from lang
		"""
		
		df = df.query('lang' == 'en' )
		#  pd.----
		
		return df