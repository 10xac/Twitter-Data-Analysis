from model_eval import Model
from gensim.models import CoherenceModel


class Evaluation:
    def __init__(self, model):
        self.model = model

    def score(self):
        coherence_model_lda = CoherenceModel(
            model=self.model, texts=self.model.data_lemmatized, dictionary=self.model.vocab_to_int, coherence='c_v')
        return self.model.log_perplexity(self.model.corpus), coherence_model_lda.get_coherence()
