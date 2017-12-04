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

    def __get_processed_string__(self, ip_string):
        processed_str = self.__pre_processor.process(ip_string)
        print "pre processed query: ", processed_str
        return processed_str

    def get_results_for_query(self, query, max_results=100):
        processed_query = self.__get_processed_string__(query.rstrip("\n"))
        metapy_doc = metapy.index.Document()
        metapy_doc.content(processed_query)
        print "ready to call index.."
        try:
            ranked_results = self.__ranker__.score(self.__idx__, metapy_doc, max_results)
            print "index returned num docs: ", len(ranked_results)
            result = []
            for document in ranked_results:
                doc = SearchResult(self.__corpus_url__[document[0]],
                                   self.__corpus_title__[document[0]],
                                   self.__corpus_text__[document[0]])
                print doc.get_title()
                result.append(doc)
            return result
        except Exception as e:
            print e
            return None
