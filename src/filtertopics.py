import pyLDAvis.gensim
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel

dictionary = corpora.Dictionary.load('/home/rik/Heena/corpusdata.dictionary')
ldamodel = models.ldamodel.LdaModel.load('/home/rik/Heena/LDA Model 50 Sym/lda_model_50_sym')
#corpus = [dictionary.doc2bow(line.rstrip().split()) for line in open('/home/rik/Heena/traindata.txt')]
corpora.MmCorpus.serialize('/home/rik/Heena/modelcorpus.mm', corpus)  # store to disk, for later use
corpus = corpora.MmCorpus('/home/rik/Heena/modelcorpus.mm')
print('done')

def get_filter_topics(threshold):
    filter_list = []
    cm = CoherenceModel(model=myldamodel, corpus=corpus, dictionary=dictionary, coherence='u_mass',topn=20)
    co_values = cm.get_coherence_per_topic()
    for val in co_values:
        if val < threshold:
            filter_list.append(co_values.index[val] + 1)
    return filter_list

