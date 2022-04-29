_ = hashtags_list_df.value_counts()[:10].plot(kind='bar',
                                              figsize=(12, 5), xlabel='Hashtags in Lowercase')
