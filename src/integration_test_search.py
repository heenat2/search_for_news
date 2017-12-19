from search import Search
from lda_infer_topics2 import TopicInference

search = Search()
#topic_inference = TopicInference('/home/rik/Heena/corpusdata.dictionary',
#                                 '/home/rik/Heena/LDA Model 50 Sym/lda_model_50_sym')
                               #  '/home/rik/Heena/coherence.model')

topic_inference = TopicInference('resource/corpusdata.dictionary',
                                 'models/lda_model/LDA Model 50 Asym/lda_model_50_asymmet')

results = search.get_results_for_query("michael", 25)
for res in results:
    print res.get_title()
    print res.get_url()
topic_inference.infer_topics(results)




