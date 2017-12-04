import metapy
import pytoml
import search_for_news
from stringProcessor import StringProcessor
from corpusprocessor import CorpusProcessor

ranker = metapy.index.OkapiBM25()
query = metapy.index.Document()
text_list, url_list, title_list = CorpusProcessor().get_corpus_list()
config_path = 'resource/news-config.toml'
idx = metapy.index.make_inverted_index(config_path)

class Search:
    def get_query(self):
        ip_query = raw_input("Enter a query: ")
        return ip_query

    def get_processed_string(self,ip_string):
        processed_string = StringProcessor().process(ip_string)
        return processed_string

    def get_top_ranked_docs(self,query):
        top_docs = ranker.score(idx, query, num_results=50)
        return top_docs

    def add_topic_weight(self, document,processed_query,processed_title):
        title_tokens = processed_title.split()
        query_tokens = processed_query.split()
        term_weight = 1 / len(query_tokens)
        for token in query_tokens:
            if token in title_tokens:
                document[1] += term_weight
        return document

search_object = Search()
#accept query and process it
user_query = search_object.get_query()
processed_query = search_object.get_processed_string(user_query)
query.content(processed_query)

top_docs = search_object.get_top_ranked_docs(query)

#evaluate weight based on query & title and revise ranking
query_tokens = processed_query.split()

if len(query_tokens) != 0:
    revised_top_docs = []
    for document in top_docs:
        processed_title = search_object.get_processed_string(title_list[document[0]])
        print(processed_query)
        print(processed_title)
        revised_top_docs.append((search_object.add_topic_weight(document,processed_query,processed_title)))

print(top_docs)
print(revised_top_docs)

    #print(document)
    #print(url_list[document[0]])
    #print(title_list[document[0]])
    #print(text_list[document[0]])
#topic_miner(top_docs[])