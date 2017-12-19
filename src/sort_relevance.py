from gensim import corpora
from gensim.models import Word2Vec
import numpy as np

class Sort_Relevance:
    def __init__(self,w2v_model_path='models/word_2_vec/w2vmodel'):
        self.__w2v__ = Word2Vec.load(w2v_model_path)
        count_arr = [vocab_obj.count for word, vocab_obj in self.__w2v__.wv.vocab.items()]
        self.__corpus_length__ = sum(count_arr)

    def sort_terms_by_relevance(self,topic,lambda_):
        revised_topic = []
        for term, weight in topic:
            print(term, weight)
            log_weight = np.log(weight)
            print(log_weight)
            term_proportion = float(self.__w2v__.wv.vocab[term].count) / self.__corpus_length__
            print(term_proportion)
            log_lift = np.log(weight / term_proportion)
            revised_weight = lambda_ * log_weight + (1 - lambda_) * log_lift
            print('revised_weight = ',revised_weight)
            revised_topic.append((term,revised_weight))
        return revised_topic