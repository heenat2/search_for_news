"""
This module provides a way to debug search results and topics without using front-end of the application
"""

from search import Search
from lda_infer_topics2 import TopicInference

search = Search()
topic_inference = TopicInference('resource/corpusdata.dictionary',
                                 'models/lda_model/LDAModel50Symmetric/ldamodel')

results = search.get_results_for_query("michael", 25)
for res in results:
    print res.get_title()
    print res.get_url()
topic_inference.infer_topics(results)




