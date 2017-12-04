import pyLDAvis.gensim
from gensim import corpora, models

# '/home/rik/Heena/LDA Model 50 Sym/lda_model_50_sym'
# /home/rik/Heena/corpusdata.dictionary
from stringProcessor import StringProcessor


class TopicInference(object):
    def __init__(self, dict_path, model_path):
        self.__dictionary__ = corpora.Dictionary.load(dict_path)
        self.__model__ = models.ldamodel.LdaModel.load(model_path)
        self.__preprocessor__ = StringProcessor()
        self.__topic_term_dict__ = {}
        self.__num_topics__ = self.__model__.get_topics().shape[0]
        for i in range(0, self.__num_topics__):
            self.__topic_term_dict__[i] = self.__model__.get_topic_terms(i, 20)

    def infer_topics(self, query_results):
        topic_count_dict = {}
        text_docs = [self.__preprocessor__.process(result.get_text()) for result in query_results]
        for doc in text_docs:
            bow = self.__dictionary__.doc2bow(doc.split(' '))
            topics = self.__model__[bow]
            for topic in topics:
                if topic[0] in topic_count_dict:
                    # increment occurence of topic by 1 for every document that has this topic
                    topic_count_dict[topic[0]][0] += 1
                    # increment probability
                    topic_count_dict[topic[0]][1] += topic[1]
                else:
                    topic_count_dict[topic[0]] = [1, topic[1]]
        sorted_topics = sorted(
            map(lambda (key, (freq, prob_sum)): (key, prob_sum / freq), topic_count_dict.iteritems()),
            key=lambda (key, prob): prob, reverse=True)
        final_terms = []
        for (k, v) in sorted_topics:
            for (i, j) in self.__model__.get_topic_terms(k):
                term_weight = j * v
                final_terms.append((self.__dictionary__[i],term_weight))

        sorted_terms = sorted(final_terms, key=lambda (id, weight): weight, reverse=True)
        final_terms = set()
        for i, x in enumerate(sorted_terms):
            print x
            if i < 20:
                final_terms.add(x[0])
        print final_terms
        return final_terms

