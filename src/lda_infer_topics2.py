"""
This module is used to get topics for the retrieved documents for a search query.
The topics are inferred using a LDA model trained on the same corpus as used for
the text retrieval. Refer LdaModel.py for training logic.
TopicInference object is instantiated in app.py.
"""

from gensim import corpora, models
from sort_relevance import Sort_Relevance
from stringProcessor import StringProcessor


class TopicInference(object):
    def __init__(self, dict_path, lda_model_path):
        """
        :param dict_path: path to dictionary of corpus
        :type dict_path: str
        :param lda_model_path: path to lda model
        :type lda_model_path: str
        """
        self.__dictionary__ = corpora.Dictionary.load(dict_path)
        self.__lda_model__ = models.ldamodel.LdaModel.load(lda_model_path)
        self.__preprocessor__ = StringProcessor()
        self.__topic_term_dict__ = {}
        self.__num_topics__ = self.__lda_model__.get_topics().shape[0]
        for i in range(0, self.__num_topics__):
            self.__topic_term_dict__[i] = self.__lda_model__.get_topic_terms(i, 20)
        self.__bad_topics__ = (4, 13, 28, 40)

    def __filter_topics__(self, topics):
        """
        1. Eliminates bad topics - either made of background words or having low coherence. The bad topic set
           is hardcoded.
        2. Reorders topics for a document by their probability in decreasing order and retains only the first
           n topics such that sum of probability of those topics is at least 0.5.

        :param topics: topics for a retrieved document as inferred by lda model
        :type topics: List of tuples of type (topic_id, probability)
        :return: filtered topics as per the logic described above
        :rtype: List of tuples of type (topic_id, probability)
        """
        cumulative_weight = 0
        residual_topics = []
        good_topics = [topic for topic in topics if topic[0] not in self.__bad_topics__]
        sorted_topics = sorted(good_topics, key=lambda (id,weight):weight, reverse=True)
        for topic in sorted_topics:
            residual_topics.append(topic)
            cumulative_weight += topic[1]
            if cumulative_weight >= 0.5:
                break
        return residual_topics


    def infer_topics(self, query_results):
        """
        :param query_results: documents retrieved after query search
        :type query_results: List of SearchResult object. See core.py for class SearchResult.
        :return: top topics for query_results as inferred by lda model
        :rtype: List of str

        Performs the following steps -
        1. Infer topics for all retrieved documents and apply filter logic.
        2. Build dictionary 'topic_count_dict' = {topic_id : [topic_frequency, total_probability]}
           where topic frequency = count of docs sharing the topic
                 total probability = sum of topic probabilities of all docs sharing the topic
        3. Sort the topics in descending order of (total_probability) / (topic_frequency)
        4. Create sorted list 'final_terms' = [term, weight] where weight = topic probability * term probability
        5. Reorder final_terms to promote terms that have low corpus presence and demote terms that have high
           frequency in corpus
        """

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

        # sort the topics in descending order of (total_probability) / (topic_frequency)
        sorted_topics = sorted(
            map(lambda (key, (freq, prob_sum)): (key, prob_sum / freq), topic_count_dict.iteritems()),
            key=lambda (key, prob): prob, reverse=True)

        final_terms = []   # list of tuples (term, term_weight)
        for (k, v) in sorted_topics:    # k = topic_id; v = total_probability/topic_frequency
            for (i, j) in self.__lda_model__.get_topic_terms(k,10):  # i = term_id; j = term probability in topic k
                term_weight = j * v
                final_terms.append((self.__dictionary__[i],term_weight))

        # reorders topic terms such that - terms that are frequent in the corpus are demoted in ranking
        # setting lambda_ = 1 will not modify the results and result in relevance_ordered_terms = final_terms
        relevance_ordered_terms = sr.sort_terms_by_relevance(final_terms, 0.6)
        sorted_relevant_terms = sorted(relevance_ordered_terms, key=lambda (id, weight): weight, reverse=True)

        # sorted_terms and final_terms are not returned by this function. They are only printed to be able to observe the effect of lambda_
        # (set to 0.6 above) and adjust it if required.

        sorted_terms = sorted(final_terms, key=lambda (id, weight): weight, reverse=True)
        final_terms = set()
        for i, x in enumerate(sorted_terms):
            if i < 14:
                final_terms.add(x[0])
        print 'topic terms before ranking for relevancy'
        print final_terms

        # number of terms is limited to 14 to display 2 lines of recommended terms but can be adjusted as desired
        relevant_final_terms = set()
        for i, x in enumerate(sorted_relevant_terms):
            if i < 14:
                relevant_final_terms.add(x[0])
        print 'Final topic terms'
        print relevant_final_terms

        return relevant_final_terms