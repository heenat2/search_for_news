"""
1. Generate dictionary from corpus and save for future use
2. Train lda model and save for future use
This version creates a 50 topic lda model assuming a symmetric alpha.
Contains variable file paths which need to be verified before running
"""

from gensim import corpora, models
import re
from collections import defaultdict
import logging
import gensim

logging.basicConfig(filename='models/lda_training_log.txt',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
processed_data_path = 'resource/news/news.dat'
modelpath = 'models/lda_model/LDAModel50Symmetric/ldamodel'
dictionary_path = 'resource/corpusdata.dictionary'

def train_lda():
    """
    Trains and saves LDA Model
    """
    train_corpus = [dictionary.doc2bow(line.rstrip().split()) for line in open(processed_data_path)]
    ldamodel = gensim.models.ldamulticore.LdaMulticore(train_corpus, num_topics=50, id2word=dictionary, passes=400,gamma_threshold=0.001,iterations=100,chunksize=10000,alpha='symmetric')
    ldamodel.save(modelpath)
    print('lda model saved')

def create_dictionary(processed_data_path):
    '''
    :param processed_data_path: path to processed data file created by index generator program createIndex.py
    :type processed_data_path: str
    :return: dictionary i.e. id to token mapping
    :rtype: gensim.corpora.Dictionary object
    '''
    print('Creating dictionary...')
    from six import iteritems
    dictionary = corpora.Dictionary(line.rstrip().split() for line in open(processed_data_path))
    low_freq_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq < 5]
    high_freq_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq > 15000]
    dictionary.filter_tokens(low_freq_ids + high_freq_ids)
    dictionary.compactify()  # remove gaps in id sequence after words that were
    print(dictionary)
    dictionary.save(dictionary_path)
    return dictionary

if __name__ == '__main__':
    dictionary = create_dictionary(processed_data_path)
    train_lda()
