from search import Search
from lda_infer_topics import TopicInference

search = Search()
topic_inference = TopicInference('/home/rik/Heena/corpusdata.dictionary',
                                 '/home/rik/Heena/LDA Model 50 Sym/lda_model_50_sym')
results = search.get_results_for_query("donald trump", 10)
for res in results:
    print res.get_title()
    print res.get_url()
topic_inference.infer_topics(results)




