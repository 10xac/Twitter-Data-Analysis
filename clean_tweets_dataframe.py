{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled20.ipynb",
      "provenance": [],
      "authorship_tag": "ABX9TyOFp2cflE0xVVnQNDGyNH2k",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/d1m3j1/Twitter-Data-Analysis/blob/fix_bug/clean_tweets_dataframe.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "XHtsMRyDS3Q8"
      },
      "outputs": [],
      "source": [
        "class Clean_Tweets:\n",
        "    \"\"\"\n",
        "    The PEP8 Standard AMAZING!!!\n",
        "    \"\"\"\n",
        "    def __init__(self, df:pd.DataFrame):\n",
        "        self.df = df\n",
        "        print('Automation in Action...!!!')\n",
        "        \n",
        "    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:\n",
        "        \"\"\"\n",
        "        remove rows that has column names. This error originated from\n",
        "        the data collection stage.  \n",
        "        \"\"\"\n",
        "        unwanted_rows = self.df[self.df['retweet_count'] == 'retweet_count' ].index\n",
        "        self.df.drop(unwanted_rows , inplace=True)\n",
        "        self.df = self.df[self.df['polarity'] != 'polarity']\n",
        "        \n",
        "        return self.df\n",
        "    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:\n",
        "        \"\"\"\n",
        "        drop duplicate rows\n",
        "        \"\"\"\n",
        "        self.df = self.df.drop_duplicates(subset = 'original_text', keep = False, inplace = True)\n",
        "        \n",
        "        return self.df\n",
        "    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:\n",
        "        \"\"\"\n",
        "        convert column to datetime\n",
        "        \"\"\"\n",
        "        self.df['created_at'] = self.df['created_at'].apply(lambda x : pd.to_datetime(x))\n",
        "        \n",
        "        self.df = self.df[self.df['created_at'] >= '2020-12-31' ]\n",
        "        \n",
        "        return self.df\n",
        "    \n",
        "    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:\n",
        "        \"\"\"\n",
        "        convert columns like polarity, subjectivity, retweet_count\n",
        "        favorite_count etc to numbers\n",
        "        \"\"\"\n",
        "        self.df['polarity'] = self.df['polarity'].apply(lambda x :pd.to_numeric(x))\n",
        "        self.df['retweet_count'] = self.df['retweet_count'].apply(lambda x :pd.to_numeric(x))\n",
        "        self.df['favorite_count'] = self.df['favorite_count'].apply(lambda x :pd.to_numeric(x))\n",
        "        \n",
        "        return self.df\n",
        "    \n",
        "    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:\n",
        "        \"\"\"\n",
        "        remove non english tweets from lang\n",
        "        \"\"\"\n",
        "        \n",
        "        self.df = self.df[self.df.lang == 'en'].drop('lang', axis=1).reset_index()\n",
        "        \n",
        "        return self.df"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        ""
      ],
      "metadata": {
        "id": "olx1Peuvgz-n"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}