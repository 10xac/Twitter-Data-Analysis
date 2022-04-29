from preparedata import PrepareData
from gensim import corpora
import gensim
import pickle


class Model:
    def __init__(self, df):
        self.df = df

    def model_evaluatio(self):
        data = PrepareData(self.df)
        vocab_list = data.preparedata(self.df)
        vocab_to_int = corpora.Dictionary(vocab_list)
        corpus = [vocab_to_int.doc2bow(vocab) for vocab in vocab_list]
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=vocab_to_int,
                                                    num_topics=20,
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)
        pickle.dump(lda_model, open('model.pkl', 'wb'))
        return lda_model
