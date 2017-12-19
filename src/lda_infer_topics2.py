import pyLDAvis.gensim
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
from sort_relevance import Sort_Relevance

# '/home/rik/Heena/LDA Model 50 Sym/lda_model_50_sym'
# /home/rik/Heena/corpusdata.dictionary
from stringProcessor import StringProcessor


class TopicInference(object):
    def __init__(self, dict_path, lda_model_path):                      # , cm_path):
        self.__dictionary__ = corpora.Dictionary.load(dict_path)
        self.__lda_model__ = models.ldamodel.LdaModel.load(lda_model_path)
        self.__preprocessor__ = StringProcessor()
        self.__topic_term_dict__ = {}
        self.__num_topics__ = self.__lda_model__.get_topics().shape[0]
        for i in range(0, self.__num_topics__):
            self.__topic_term_dict__[i] = self.__lda_model__.get_topic_terms(i, 20)
        #cm = CoherenceModel.load(cm_path)
        #co_values = cm.get_coherence_per_topic()
        #self.__exclude_topics__ = [co_values.index(val) for val in co_values if val < -3]
        #print(self.__exclude_topics__)
        #print(self.__lda_model__.get_topic_terms(0))

    def __filter_topics__(self, topics):
        cumulative_weight = 0
        residual_topics = []
        sorted_topics = sorted(topics, key=lambda (id,weight):weight, reverse=True)
        for topic in sorted_topics:
            residual_topics.append(topic)
            cumulative_weight += topic[1]
            if cumulative_weight >= 0.5:
                break
        print residual_topics
        return residual_topics


    def infer_topics(self, query_results):
        topic_count_dict = {}
        sr = Sort_Relevance()
        text_docs = [self.__preprocessor__.process(result.get_text()) for result in query_results[:10]]
        for doc in text_docs:
            bow = self.__dictionary__.doc2bow(doc.split(' '))
            topics = self.__lda_model__[bow]
            filtered_top_topics = self.__filter_topics__(topics)
            for topic in filtered_top_topics:
                if topic[0] in topic_count_dict:
                    # increment occurence of topic by 1 for every document that has this topic
                    topic_count_dict[topic[0]][0] += 1
                    # increment probability
                    topic_count_dict[topic[0]][1] += topic[1]
                else:
                    topic_count_dict[topic[0]] = [1, topic[1]]

        for k, v in topic_count_dict.iteritems():
            print(k, v)

        sorted_topics = sorted(
            map(lambda (key, (freq, prob_sum)): (key, prob_sum / freq), topic_count_dict.iteritems()),
            key=lambda (key, prob): prob, reverse=True)

        print(sorted_topics)
        for topic in sorted_topics:
            print('topic = ',topic[0])
            for (i, j) in self.__lda_model__.get_topic_terms(topic[0],20):
                print(self.__dictionary__[i],j)

        final_terms = []
        for (k, v) in sorted_topics:
            for (i, j) in self.__lda_model__.get_topic_terms(k,10):
                term_weight = j * v
                final_terms.append((self.__dictionary__[i],term_weight))

        relevance_ordered_terms = sr.sort_terms_by_relevance(final_terms,0.6)
        print(relevance_ordered_terms)

        sorted_terms = sorted(final_terms, key=lambda (id, weight): weight, reverse=True)
        sorted_relevant_terms = sorted(relevance_ordered_terms, key=lambda (id, weight): weight, reverse=True)

        final_terms = set()
        for i, x in enumerate(sorted_terms):
            if i < 14:
                final_terms.add(x[0])
        print final_terms

        relevance_final_terms = set()
        for i, x in enumerate(sorted_relevant_terms):
            if i < 14:
                relevance_final_terms.add(x[0])
        print relevance_final_terms

        return relevance_final_terms