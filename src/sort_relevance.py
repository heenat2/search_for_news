"""
This module accepts a list of terms along with their weights and returns the same list of terms
but with revised weights. Revised weight is calculated using the formula -
revised_weight = lambda_ * log_weight + (1 - lambda_) * log_lift
where log_weight = log(original weight)
      log_lift = log(original_weight / marginal probability of term in corpus)
      lambda is between 0 and 1

References relevance calculation logic in paper 'LDAvis: A method for visualizing and interpreting topics'.
https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf
"""

from gensim.models import Word2Vec
import numpy as np

class Sort_Relevance:
    def __init__(self, w2v_model_path='models/word_2_vec/w2vmodel'):
        self.__w2v__ = Word2Vec.load(w2v_model_path)
        count_arr = [vocab_obj.count for word, vocab_obj in self.__w2v__.wv.vocab.items()]
        self.__corpus_length__ = sum(count_arr)

    def sort_terms_by_relevance(self, topic, lambda_):
        revised_topic = []
        for term, weight in topic:
            log_weight = np.log(weight)
            marginal_prob = float(self.__w2v__.wv.vocab[term].count) / self.__corpus_length__
            log_lift = np.log(weight / marginal_prob)
            revised_weight = lambda_ * log_weight + (1 - lambda_) * log_lift
            revised_topic.append((term, revised_weight))
        return revised_topic