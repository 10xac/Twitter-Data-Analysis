from preparedata import DataLoader
from string import punctuation
import pandas as pd
import nlp
from wordcloud import STOPWORDS, WordCloud
import gensim
import spacy
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

DataLoader_obj = DataLoader('processed_tweet_data.csv')
df = DataLoader_obj.read_csv()


class PrepareData:
    def __init__(self, df):
        self.df = df

    def prepare_data(self):
        df['clean_text'] = df['clean_text'].dropna()
        df['clean_text'] = df['clean_text'].astype(str)
        df['clean_text'] = df['clean_text'].apply(
            lambda x: x.translate(str.maketrans(' ', ' ', punctuation)))
        df['clean_text'] = df['clean_text'].apply(lambda x: x.lower())

        # clean and prepare for feature engineering
        sentence_list = [sentence for sentence in df['clean_text']]
        vocab_list = [vocab.split() for vocab in sentence_list]

        return vocab_list

    def remove_stopwords(self, vocab_list):
        stop_words = stopwords.words('english')
        stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in vocab_list]

    def make_bigrams(self, non_stop_words):
        # higher threshold fewer phrases.
        bigram = gensim.models.Phrases(
            self.vocab_list, min_count=5, threshold=100)

        bigram_mod = gensim.models.phrases.Phraser(bigram)

        return [bigram_mod[doc] for doc in non_stop_words]

    def lemmatization(self, make_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        texts_out = []
        nlp = spacy.load('en_core_web_sm')
        for sent in make_bigrams:
            doc = nlp(" ".join(sent))
            texts_out.append(
                [token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out
