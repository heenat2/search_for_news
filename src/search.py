import metapy
from core import SearchResult
from stringProcessor import StringProcessor
from corpusprocessor import CorpusProcessor


class Search(object):
    def __init__(self, config_path='resource/news-config.toml'):
        self.__ranker__ = metapy.index.OkapiBM25()
        self.__corpus_text__, self.__corpus_url__, self.__corpus_title__ = CorpusProcessor().get_corpus_list()
        self.__idx__ = metapy.index.make_inverted_index(config_path)
        self.__pre_processor = StringProcessor()
        print "done instantiating corpus and resources for search"

    #gets phrases, removes stop words and lemmatizes a string
    def __get_processed_string__(self, ip_string):
        processed_str = self.__pre_processor.process(ip_string)
        return processed_str

    #fetches results for a query
    def get_results_for_query(self, query, max_results=100):
        processed_query = self.__get_processed_string__(query.rstrip("\n"))
        metapy_doc = metapy.index.Document()
        metapy_doc.content(processed_query)
        print "ready to call index.."
        try:
            ranked_results = self.__ranker__.score(self.__idx__, metapy_doc, max_results)
            print "index returned num docs: ", len(ranked_results)
            result = []
            revised_result = []
            sorted_revised_result = []

            for document in ranked_results:
                title_tokens = self.__get_processed_string__(self.__corpus_title__[document[0]]).split()
                if len(processed_query) > 0:
                    revised_result.append(self.__get_revised_doc_score__(title_tokens,document,processed_query))

            sorted_revised_result = sorted(revised_result, key = lambda x:x[1], reverse=True)

            for document in sorted_revised_result:
                doc = SearchResult(self.__corpus_url__[document[0]],
                                   self.__corpus_title__[document[0]],
                                   self.__corpus_text__[document[0]])
                result.append(doc)
            return result
        except Exception as e:
            print e
            return None

    #adds to doc score an additional value = 1/len(query) for each query term if present in topic
    def __get_revised_doc_score__(self,title_tokens,document,processed_query):
        new_doc = [document[0],document[1]]
        print('in revised doc score')
        query_term_weight = float(1) / len(processed_query)
        print(query_term_weight)
        for term in processed_query.split():
            if term in title_tokens:
                new_doc[1] += query_term_weight
        return new_doc
