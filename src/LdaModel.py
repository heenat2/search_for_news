from gensim import corpora, models
import re
from collections import defaultdict
import logging
import gensim

logging.basicConfig(filename='/home/rik/Heena/lda_training_log.txt',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
traindata2 = '/home/rik/Heena/traindata.txt'
testdata2 = '/home/rik/Heena/testdata.txt'
alldata = '/home/rik/Heena/news/news.dat'

class MyCorpus:

    def __init__(self,path):
        self.path = path

    def __iter__(self):
        for line in open(self.path):
            # one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.rstrip().split())

def main():
    print('in main')
    #train_corpus = MyCorpus(traindata)
    train_corpus = [dictionary.doc2bow(line.rstrip().split()) for line in open(traindata)]
    test_corpus = [dictionary.doc2bow(line.rstrip().split()) for line in open(testdata)]
    print('corpus iterators created')

    #topic_count = range(30, 150, 10)
    #for num_of_topics in topic_count:
    ldamodel = gensim.models.ldamulticore.LdaMulticore(train_corpus, num_topics=90, id2word=dictionary, passes=100,gamma_threshold=0.001,iterations=100,chunksize=10000,alpha='symmetric')
    ldamodel.save('/home/rik/Heena/lda_model/lda_model_90_sym')
    print('lda model saved')
        #ldamodel = gensim.models.ldamodel.LdaModel.load('/home/rik/Heena/lda_model/lda_model_1')


def create_dictionary(alldata):
    print('in create dictionary')
    from six import iteritems
    # collect statistics about all tokens
    dictionary = corpora.Dictionary(line.rstrip().split() for line in open(alldata))
    low_freq_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq < 5]
    high_freq_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq > 15000]
    for id, token in dictionary.iteritems():
        if id in (low_freq_ids + high_freq_ids):
            print(token)
    dictionary.filter_tokens(low_freq_ids + high_freq_ids)
    dictionary.compactify()  # remove gaps in id sequence after words that were
    #dictionary.filter_extremes(no_below=5,no_above=0.2)
    print(dictionary)
    dictionary.save('/home/rik/Heena/corpusdata2.dictionary')
    return dictionary

dictionary = create_dictionary(alldata)
#main()
'''
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=50, id2word = dictionary, passes=40   )
print 'done'

ldamodel.save('/home/rik/Heena/lda_model/lda_model_1')
print 'saved model'

topics = ldamodel.show_topics()
print(topics)
'''