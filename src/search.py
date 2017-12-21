"""
This module defines the Search class to be able to retrieve ranked news articles relevant to a query
"""

import metapy
from core import SearchResult
from stringProcessor import StringProcessor
from corpusprocessor import CorpusProcessor
import re


class Search(object):
    def __init__(self, config_path='resource/news-config.toml'):  #config required to create metapy index
        self.__ranker__ = metapy.index.OkapiBM25()
        self.__corpus_text__, self.__corpus_url__, self.__corpus_title__ = CorpusProcessor().get_corpus_list()
        self.__idx__ = metapy.index.make_inverted_index(config_path)
        self.__pre_processor = StringProcessor()
        print "done instantiating corpus and resources for search"

    #
    def __get_processed_string__(self, ip_string):
        """
        the default pipeline for preprocessing is set to
        tokenization, bigram phrase identification, stop word removal and lemmatization
        """
        processed_str = self.__pre_processor.process(ip_string)
        return processed_str


    def __highlight_results__(self, q, title, text):
        """
        sets color of query term q in title and text to red
        """
        title = re.sub(q, '<font color="FF0000">' + q + '</font>', title)
        title = re.sub(q.upper(), '<font color="FF0000">' + q.upper() + '</font>', title)
        title = re.sub(q.capitalize(), '<font color="FF0000">' + q.capitalize() + '</font>', title)
        title = re.sub(q.title(), '<font color="FF0000">' + q.title() + '</font>', title)
        text = re.sub(q, '<font color="FF0000">' + q + '</font>', text)
        text = re.sub(q.upper(), '<font color="FF0000">' + q.upper() + '</font>', text)
        text = re.sub(q.capitalize(), '<font color="FF0000">' + q.capitalize() + '</font>', text)
        text = re.sub(q.title(), '<font color="FF0000">' + q.title() + '</font>', text)
        return title, text


    def get_results_for_query(self, query, max_results=100):
        """
        Returns 'results' (list of SearchResult objects) for search string 'query'
        Primarily uses BM25 relevance ranking function to rank documents. The ranking is also
        influenced by presence of query terms in the news article title.
        """
        global colored_title, colored_text
        processed_query = self.__get_processed_string__(query.rstrip("\n"))
        metapy_doc = metapy.index.Document()
        metapy_doc.content(processed_query)
        print "ready to call index.."
        try:
            ranked_results = self.__ranker__.score(self.__idx__, metapy_doc, max_results)
            print "index returned num docs: ", len(ranked_results)
            result = []
            revised_result = []

            # update the BM25 score assigned to each document based on whether the query terms appear in the
            # title of the document and store the new doc_id, score mapping in revised_result
            for document in ranked_results:
                title_tokens = self.__get_processed_string__(self.__corpus_title__[document[0]]).split()
                if len(processed_query) > 0:
                    revised_result.append(self.__get_revised_doc_score__(title_tokens, document, processed_query))

            # sort ranked results in decreasing order of document score
            sorted_revised_result = sorted(revised_result, key=lambda x: x[1], reverse=True)

            # highlights query terms in document title and text in red
            for document in sorted_revised_result:
                colored_title = self.__corpus_title__[document[0]]
                colored_text = self.__corpus_text__[document[0]]
                for q in processed_query.split(" "):
                    if '_' in q:
                        q = q.replace('_', ' ')
                    colored_title, colored_text = self.__highlight_results__(q, colored_title, colored_text)
                doc = SearchResult(self.__corpus_url__[document[0]], colored_title, colored_text)
                result.append(doc)
            return result
        except Exception as e:
            print e
            return None


    def __get_revised_doc_score__(self, title_tokens, document, processed_query):
        """
        adds to doc score an additional value = 1/len(query) for each query term if present in title
        """
        new_doc = [document[0], document[1]]
        query_term_weight = float(1) / len(processed_query)
        for term in processed_query.split():
            if term in title_tokens:
                new_doc[1] += query_term_weight
        return new_doc
