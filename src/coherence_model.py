from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel

dictionary = corpora.Dictionary.load('/home/rik/Heena/corpusdata.dictionary')
myldamodel = models.ldamodel.LdaModel.load('/home/rik/Heena/LDA Model 50 Sym/lda_model_50_sym')
corpus = [dictionary.doc2bow(line.rstrip().split()) for line in open('/home/rik/Heena/traindata.txt')]

cm = CoherenceModel(model=myldamodel, corpus=corpus, dictionary=dictionary, coherence='u_mass',topn=20)
cm.save('/home/rik/Heena/coherence.model')